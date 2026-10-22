# Rakazo deploy (rakazo.thefirstonly.com) — pull-based GHCR self-host

Rakazo = self-hosted "team of AI agents" app (elie222/rakazo). Pull-based compose: không cần source code, chỉ `docker-compose.images.yml` + `.env`. Deploy thành công Sep 2026 trên máy NTQUANG_DELL.

## Layout
- Project dir: `D:/Hermes/rakazo/` (KHÔNG git repo — chỉ compose + env + install script)
- Compose: `docker-compose.images.yml` (pull GHCR `edge` images), `.env` (đã đủ secret)

## Services
| Service | Image | Port | Ghi chú |
|---------|-------|------|---------|
| postgres | postgres:16 digest-pinned | internal | healthcheck pg_isready |
| computer | ghcr.io/.../computer:edge | — | pull stub, exits 0 |
| data-init | busybox:1 | — | chown appdata |
| supervisor | app:edge | 7091 internal | sandbox docker, cần docker.sock |
| api | app:edge | 127.0.0.1:3100 | prisma migrate + api, health /health |
| worker | app:edge | — | graphile jobs |
| web | app:edge | 127.0.0.1:5173 | vite preview, health qua api |

Lệnh up:
```bash
cd /d/Hermes/rakazo
docker compose --env-file .env -f docker-compose.images.yml up -d
```

## Lỗi Vite allowedHosts (403 qua tunnel)
Web chạy `vite preview`; `apps/web/vite.config.ts` có:
```ts
const previewHost = process.env.RAKAZO_HOST ?? "localhost";
// ...
preview: { host: "0.0.0.0", allowedHosts: [previewHost] }
```
Nếu `.env` còn `RAKAZO_HOST=localhost` → localhost 200, qua tunnel 403 body `Blocked request. This host ("...") is not allowed`.
Fix: `sed -i 's/^RAKAZO_HOST=.*/RAKAZO_HOST=rakazo.thefirstonly.com/' .env` → `docker compose up -d web`.

## Auth origin (BETTER_AUTH_URL / WEB_ORIGIN)
Phải là `https://rakazo.thefirstonly.com` (không phải 127.0.0.1) thì signup/login qua tunnel không vỡ cookie/CORS. Đổi xong recreate **api + worker + web** (cả 3 dùng .env):
```bash
docker compose --env-file .env -f docker-compose.images.yml up -d api worker web
```
Chờ `docker compose ps` healthy trước khi tạo account. Env khác trong .env: SANDBOX_PROVIDER=docker, OPENROUTER_API_KEY, SCREEN_PROXY_SECRET, SANDBOX_SUPERVISOR_TOKEN.

## Tạo tài khoản
- Signup route thật là `/sign-up` (không phải `/signup`); nút "Sign up" trên landing là `<button>` onclick (SPA), không phải `<a>`.
- Form React controlled → điền bằng browser_type, KHÔNG set .value bằng JS console (sẽ submit rỗng: `[body.email] Invalid email address; [body.password] Too small`).
- Sau khi tạo: verify trong DB. Lưu ý schema Prisma dùng bảng `user` (số ít, lowercase) — `User`/`users` đều sai:
```bash
docker exec rakazo-postgres-1 psql -U rakazo -d rakazo -c "SELECT email, name, \"emailVerified\" FROM \"user\";"
```
- Sau signup tự chuyển tới `/onboarding` (Connect a model: OpenRouter + API key...).
- SMTP đã set trong .env → email verify có thể đến hộp; nếu không thì set `emailVerified=true` trong DB.

## Tunnel
Thêm ingress + DNS CNAME vào token-service tunnel TQUANG-DELL (xem cloudflare-tunnel skill): `rakazo.thefirstonly.com -> http://127.0.0.1:5173`.
