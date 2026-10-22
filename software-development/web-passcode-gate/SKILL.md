---
name: web-passcode-gate
description: "Protect internal web pages/dashboards with a cookie-based passcode gate — server-side check, sha256 hash, 30-day cookie. Recipes for Python http.server (inline HTML), Python SimpleHTTPRequestHandler (company dashboard 8090), and Next.js 16 (proxy.ts, NOT middleware.ts). Verified on Status dashboard (5011), Knowledge Flow (3003), and AI Company dashboard (8090)."
version: 1.0.0
---

# Web Passcode Gate (chặn trang nội bộ bằng passcode)

## Khi nào dùng
- User muốn thêm "lớp mở passcode" cho 1 trang/dashboard nội bộ trước khi access được
- User đưa passcode dạng "mặc định là XXXX" — cần gate nhẹ, không phải auth hệ thống (không OAuth, không user/pass DB)
- Mẫu đã triển khai trên máy này: **Status** (5011, Python http.server) + **Knowledge Flow** (3003, Next.js 16), passcode `<PASSCODE>`

## Nguyên tắc (bắt buộc)
1. **Server-side check** — client-only JS gate bị bypass bằng curl. Gate phải chặn ngay trong handler/proxy trước khi serve nội dung.
2. **Không lưu plaintext passcode trong code** — lưu `sha256(passcode)`, so sánh hash. Tính hash:
   ```bash
   python -c "import hashlib; print(hashlib.sha256(b'<PASSCODE>').hexdigest())"
   # 1d1e977a218bfa01fe61106c360c8acf667047e35f17fdb0f1a8484e06cfdb55
   ```
3. **Cookie xác thực**: `tfo_auth=<sha256>; Path=/; HttpOnly; SameSite=Lax; Max-Age=2592000` (30 ngày). HttpOnly để JS không đọc được.
4. **Luôn cho qua**: trang login/passcode, endpoint verify, favicon, static assets (`_next/static`, `_next/image`).
5. **Đổi passcode sau này** = đổi 1 chỗ (hash) rồi restart.

## Verify sau deploy (bắt buộc, đừng chỉ "container up")
```bash
# 1. Không cookie → phải thấy form passcode
curl -s http://localhost:PORT/ | grep -E "Mở khoá|Nhập passcode"
# 2. Sai passcode → bị chặn (error / redirect ?error=1)
curl -s -X POST http://localhost:PORT/_auth -d "passcode=wrong"
# 3. Đúng passcode → 302 + set cookie
curl -s -c /tmp/c.txt -X POST http://localhost:PORT/_auth -d "passcode=<PASSCODE>" -o /dev/null -w "%{http_code} → %{redirect_url}"
# 4. Có cookie → vào trang thật: KHÔNG còn form passcode (count = 0)
curl -s -b /tmp/c.txt http://localhost:PORT/ | grep -c "name=\"passcode\""
```
Test qua tunnel luôn (`https://domain/`), không chỉ localhost.

## Recipe 1: Python http.server (BaseHTTPRequestHandler, HTML inline)
Áp dụng cho dashboard serve bằng Python stdlib (VD `hermes-dashboard/server.py`, port 5011):
- `PASSCODE_HASH` + `PASSCODE_HTML` (form `method="POST" action="/_auth"`, input `name="passcode"`) khai báo cạnh handler.
- `do_GET`: NGAY SAU parse path, trước mọi route:
  ```python
  if not self._is_authed() and path not in ("/_auth", "/favicon.png", "/favicon.ico"):
      # trả PASSCODE_HTML, return
  ```
- `_is_authed()`: parse header `Cookie`, tìm `tfo_auth=` == `PASSCODE_HASH`.
- `do_POST` cho `/_auth`: `urllib.parse.parse_qs(body)` lấy `passcode` → sha256 so sánh → đúng: 302 `/` + `Set-Cookie`; sai: trả PASSCODE_HTML có dòng lỗi.
- Import `hashlib` (đừng quên).
- **Restart bắt buộc** sau khi sửa (HTML inline trong biến Python): kill process cũ, `cd <dir> && python server.py` background.

## Recipe 2: Next.js 16 — proxy.ts (KHÔNG middleware.ts)
Next.js 16 **đã đổi tên** `middleware.ts` → `proxy.ts`. Cảnh báo trong `AGENTS.md` của project: "This is NOT the Next.js you know — read node_modules/next/dist/docs/01-app/03-api-reference/03-file-conventions/proxy.md". Lỗi dùng middleware.ts = proxy không chạy.

3 file (đã verify trên `knowledge-flow`, port 3003):

`src/proxy.ts` (DÙNG BẢN NÀY — bản `new URL(..., request.url)` bị lỗi redirect về localhost khi sau Cloudflare tunnel):
```ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'
const PASSCODE_HASH = '<sha256>'
// Next.js KHÔNG trust X-Forwarded-* → request.url tự build thành localhost:PORT.
// Phải tự dựng base URL từ headers để redirect giữ đúng domain công khai.
function getBaseUrl(request: NextRequest): string {
  const host = request.headers.get('x-forwarded-host') || request.headers.get('host') || 'localhost'
  const proto = request.headers.get('x-forwarded-proto') || 'http'
  return `${proto}://${host}`
}
export function proxy(request: NextRequest) {
  const { pathname } = request.nextUrl
  if (pathname.startsWith('/passcode') || pathname === '/api/passcode' || pathname === '/favicon.ico') return NextResponse.next()
  if (request.cookies.get('tfo_auth')?.value === PASSCODE_HASH) return NextResponse.next()
  if (pathname !== '/' && pathname !== '') return NextResponse.redirect(new URL(`/passcode?next=${encodeURIComponent(pathname)}`, getBaseUrl(request)))
  return NextResponse.redirect(new URL('/passcode', getBaseUrl(request)))
}
export const config = { matcher: ['/((?!_next/static|_next/image|favicon.ico).*)'] }
```

`src/app/api/passcode/route.ts` (DÙNG BẢN NÀY — fix redirect domain):
```ts
import { NextRequest, NextResponse } from 'next/server'
import { createHash } from 'crypto'
function getBaseUrl(request: NextRequest): string {
  const host = request.headers.get('x-forwarded-host') || request.headers.get('host') || 'localhost'
  const proto = request.headers.get('x-forwarded-proto') || 'http'
  return `${proto}://${host}`
}
export async function POST(request: NextRequest) {
  const form = await request.formData()
  const passcode = String(form.get('passcode') || '')
  const next = request.nextUrl.searchParams.get('next') || '/'
  if (createHash('sha256').update(passcode).digest('hex') === PASSCODE_HASH) {
    const res = NextResponse.redirect(new URL(next, getBaseUrl(request)))
    res.cookies.set('tfo_auth', PASSCODE_HASH, { path: '/', httpOnly: true, sameSite: 'lax', maxAge: 60*60*24*30 })
    return res
  }
  return NextResponse.redirect(new URL('/passcode?error=1', getBaseUrl(request)))
}
```

`src/app/passcode/page.tsx` — **server component PHẢI async + searchParams là Promise**:
```tsx
export default async function PasscodePage({ searchParams }: { searchParams: Promise<{ error?: string }> }) {
  const params = await searchParams
  const hasError = !!params?.error
  // form method="POST" action="/api/passcode", input name="passcode", nút "Mở khoá"
  // hiển thị "Passcode sai, thử lại." khi hasError
}
```
⚠️ Không dùng `window.location` trong server component (không có window). Lấy error qua `searchParams` prop.

**Build + restart** (production): `npm run build` → kill process cũ (`next start --port 3003`) → `npx next start --port 3003` background. Verify route list trong build output phải có `ƒ /passcode`, `ƒ /api/passcode`, `ƒ Proxy (Middleware)`.

## Recipe 3: Python SimpleHTTPRequestHandler variant (file-based + company_auth) — Company 8090
Verified on `D:\Hermes Proj\ai-company\server.py` (serves `dashboard/index.html`). AI Company agents tự thêm gate — khác Recipe 1:
- `COOKIE_NAME="company_auth"` + `COOKIE_VALUE="tfo_company_ok_2026"` — so sánh plaintext constant, KHÔNG sha256 (kém hơn Recipe 1, nhưng đã chạy)
- `LOCK_HTML` có placeholder `<!--error-->` — thay bằng `<div class="err">Sai passcode...</div>` khi sai
- POST endpoint là `/api/login` (không phải `/_auth`): đúng → 302 + Set-Cookie; sai → 401 + LOCK_HTML lỗi
- `/company-data.json` trả 401 JSON khi chưa auth (API cũng bị gate)
- Passcode cũng `<PASSCODE>` — đồng bộ passcode chung máy

⚠️ File này có thể bị agent AI Company tự sửa bất kỳ lúc nào. Trước khi đụng: `grep -n "PASSCODE\|COOKIE" server.py` xem có gate chưa. Test: `curl -b "company_auth=tfo_company_ok_2026" http://localhost:8090/`.

## Recipe 4: FastAPI — login page RIÊNG + dashboard chỉ ở /app (overlay CSS không phải auth!)
Verified on `tfo.thefirstonly.com` (FastAPI, port 8100, 2026-08). Anh Quang mắng khi login là overlay: "xóa overlay đi là thấy dashboard phía sau" — lesson chung: **overlay CSS ẩn dashboard = KHÔNG PHẢI AUTH** (DevTools xóa div là thấy data trong DOM). Gate phải ở server, dashboard HTML không bao giờ được gửi trước auth:
- Tách 2 file static: `login.html` (chỉ form + JS login) và `index.html` (dashboard thuần, KHÔNG chứa overlay).
- FastAPI routes: `GET /` → login.html; `GET /app` → `request.cookies.get("tfo_token")` → `_check_token()` hợp lệ mới trả index.html, sai trả login.html.
- Login endpoints (`/api/login`, `/api/face/login`) dùng `resp = JSONResponse(...)` + `resp.set_cookie("tfo_token", token, max_age=2592000, path="/")`. Logout: `resp.delete_cookie("tfo_token", path="/")`.
- Frontend dashboard `checkAuth()` đọc token từ cookie (regex `document.cookie.replace(/(?:(?:^|.*;\s*)tfo_token\s*=\s*([^;]*).*$)|^.*$/, "$1")`) + localStorage → không có → `location.href='/'`.
- Test bắt buộc: `curl -s :PORT/ | grep -c viewDashboard` = 0 (login page không chứa dashboard); `curl -s -b "tfo_token=<valid>" :PORT/app | grep -c viewDashboard` > 0.
- Cookie cũng giúp API automation: mọi request cần token — GET query `?token=` hoặc Cookie header.

## Pitfalls
- **API routes cũng bị gate — automation phải gửi cookie (tested 2026-08 trên KF 3003)**: matcher `/((?!_next/static|_next/image|favicon.ico).*)` chặn cả `/api/*`. curl/Python gọi API không cookie nhận `307 → /passcode?next=...` (không phải form login). Fix: mọi request tự động thêm header `Cookie: tfo_auth=<hash>` (curl `-b`, urllib `headers={'Cookie': ...}`). Điều này áp dụng cho research queue, `/api/cards`, POST `/api/knowledge` — các cron/script cũ viết trước khi thêm gate sẽ vỡ hàng loạt, đừng tưởng API "nội bộ" thì không bị chặn.
- **Next 16 ≠ Next 15**: dùng `proxy.ts` export `proxy` (không `middleware`), searchParams là Promise (await nó), không đọc AGENTS.md thì dễ viết sai convention.
- **REDIRECT VỀ LOCALHOST (lỗi #1 khi sau tunnel)**: `NextResponse.redirect(new URL(path, request.url))` → `request.url` được Next.js build từ server address (localhost:PORT), KHÔNG đọc Host/X-Forwarded-* headers. Kết quả: sau khi nhập passcode đúng, browser bị đưa về `https://localhost:3003/`. Fix: tự build base URL từ `x-forwarded-host` (hoặc `host`) + `x-forwarded-proto` — xem code Recipe 2. Lưu ý `experimental.trustHostHeader` tồn tại ở runtime nhưng type Next 16.2.10 KHÔNG nhận → đừng dựa vào nó.
- **`NextResponse.redirect` BẮT BUỘC absolute URL**: truyền relative (`/passcode?next=...`) ném `URL is malformed ... Please use only absolute URLs` (500). Phải `new URL(path, baseUrl)`.
- Matcher thiếu exclude static → chặn cả CSS/JS làm trang passcode vỡ layout.
- Nếu app là FastAPI/StaticFiles (VD tfo.thefirstonly.com): static chỉ mount ở `/static/` → favicon/css href phải là `/static/...`, không phải `/...` (404 ngay).
- Sau khi thêm gate, test bằng curl với/không cookie — đừng tin "trang hiện form" là đủ, phải xác nhận có cookie thì KHÔNG còn form.
- Restart Python http.server cần kill đúng PID cũ (netstat tìm port → PID → Stop-Process).

## Related
- `docker-deploy-windows` — references/favicon-branding.md (quét toàn bộ site tự host, thêm favicon brand)
- `cloudflare-tunnel` — expose trang qua subdomain sau khi có gate
- `nextjs-supabase-fullstack` — Next.js 15/16 app patterns
