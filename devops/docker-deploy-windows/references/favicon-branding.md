# Favicon Branding — quét & thêm favicon TFO cho mọi site tự host trên máy

Khi user yêu cầu "check trang nào chưa favicon / thêm favicon brand vào", làm theo recipe này. Máy chạy NHIỀU site cùng lúc (xem port map trong SKILL.md), mỗi site có thể thiếu favicon.

## Bước 1 — Quét favicon từng site đang chạy

Enumerate các port đang LISTEN, rồi probe từng trang:

```bash
netstat -ano | grep LISTEN | grep -E ":(5099|3000|3001|3003|5011|3010|8090|8100|8769|9877|3456) " | awk '{print $2}' | sort -u
```

Với mỗi port, grep `<link rel="icon">`:
```bash
curl -s --max-time 10 http://localhost:PORT/ | grep -oiE '<link[^>]*(icon|favicon)[^>]*>' | head -3
```

## Bước 2 — Lấy favicon brand gốc

Favicon TFO (thefirstonly.com) là data URI PNG 48x48 inline trong `<head>`:
```bash
curl -s --max-time 10 https://thefirstonly.com/ | grep -oE 'data:image/png;base64,([A-Za-z0-9+/=]+)'
```
⚠️ thefirstonly.com chặn urllib mặc định (403) → cần `User-Agent: Mozilla/5.0 ...` trong request (curl mặc định OK).

Giải mã base64 → lưu `favicon.png` (≈4.6KB) vào thư mục của từng site thiếu.

## Bước 3 — Thêm `<link rel="icon">` vào HTML

```html
<link rel="icon" type="image/png" href="/favicon.png">
```

**Phân loại server — quyết định path + có cần restart không:**

| Server | Thư mục HTML | Path favicon | Restart? |
|--------|--------------|--------------|----------|
| Python `http.server` / SimpleHTTPRequestHandler | file tĩnh trong thư mục serve (vd `dashboard/index.html`) | `/favicon.png` | ❌ Không — file tĩnh đọc mỗi request |
| **FastAPI + StaticFiles mount** | `app/static/index.html` | **`/static/favicon.png`** | ❌ Không |
| HTML inline trong Python (biến string) | vd `hermes-dashboard/server.py` `DASHBOARD_HTML = r"""..."""` | `/favicon.png` (file cùng cwd) | ✅ **Có — restart process** |

⚠️ **Bẫy FastAPI:** `app.mount("/static", StaticFiles(directory=...))` chỉ serve ở prefix `/static/`. Link `/favicon.png` sẽ trả 404 dù file nằm cạnh index.html. Dùng `/static/favicon.png`.

## Bước 4 — Restart khi cần

- HTML inline trong Python: kill PID bằng `Stop-Process -Id <PID> -Force`, rồi chạy lại `python server.py` (background=true) từ đúng thư mục.
- File tĩnh: không cần restart — verify ngay.

## Verify

```bash
curl -s http://localhost:PORT/ | grep -oE '<link[^>]*icon[^>]*>'   # link đã có
curl -s -o /dev/null -w "%{http_code}" http://localhost:PORT/favicon.png   # 200
# Qua tunnel nếu có:
curl -s --max-time 12 https://sub.domain.com/ | grep -oE '<link[^>]*icon[^>]*>'
```

## Trạng thái máy này (đã quét 2026-07-31)

- ✅ Có sẵn: Company 3000 (`/assets/brand/OnlyO1.svg`), KFlow 3003, me 5099 (data URI TFO), Planka 3010 (logo riêng)
- ❌ Đã thêm: Status 5011 (`hermes-dashboard/server.py`, cần restart), company 8090 (`D:\Hermes Proj\ai-company\dashboard\index.html`), tfo 8100 (`D:\Hermes Proj\ai-company\app\static\index.html`, path `/static/favicon.png`)
- Favicon file đã lưu: 3 bản copy `favicon.png` (dashboard/, app/static/, hermes-dashboard/)
