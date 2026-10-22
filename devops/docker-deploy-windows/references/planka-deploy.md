# Planka self-host (Trello clone) — D:\planka, port 3010

## Trạng thái
- URL: https://kan.thefirstonly.com (Cloudflare tunnel → localhost:3010)
- Data: `D:\planka\db` (bind mount, không đụng ổ C)
- Admin: `<EMAIL>` / `<PASSWORD>` (role admin, username `quang`)
- Kan (kanbn/kan) đã bị gỡ — Planka thay thế vì UI mượt hơn, nhẹ hơn (1 app + postgres), admin bootstrap qua env.

## docker-compose.yml tối thiểu
```yaml
services:
  planka:
    image: ghcr.io/plankanban/planka:latest
    restart: unless-stopped
    ports:
      - "${PLANKA_PORT:-3010}:1337"
    environment:
      BASE_URL: https://kan.thefirstonly.com
      SECRET_KEY: <token_urlsafe(48)>
      DATABASE_URL: postgresql://postgres@postgres/planka
      DEFAULT_ADMIN_EMAIL: <EMAIL>
      DEFAULT_ADMIN_PASSWORD: "<PASSWORD>"
      DEFAULT_ADMIN_NAME: Nguyen Thanh Quang
      DEFAULT_ADMIN_USERNAME: quang
    depends_on:
      - postgres

  postgres:
    image: postgres:15-alpine
    restart: unless-stopped
    volumes:
      - /d/planka/db:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: planka
      POSTGRES_HOST_AUTH_METHOD: trust
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 10
```

## ⚠️ Admin seeding — sai tên env var = âm thầm không tạo admin
- Tên đúng là **`DEFAULT_ADMIN_EMAIL` / `DEFAULT_ADMIN_PASSWORD` / `DEFAULT_ADMIN_NAME` / `DEFAULT_ADMIN_USERNAME`** (đọc từ `docker-compose.yml` của repo Planka).
- Dùng nhầm `ADMIN_EMAIL` (tên cũ của bản khác) → app chạy bình thường, login trả `E_NOT_FOUND`, DB `user_account` trống, không có lỗi nào trong log.
- Seed chỉ chạy khi bảng `user_account` RỖNG lúc boot. Nếu container crash lúc postgres chưa ready (log `connect ECONNREFUSED 172.18.0.2:5432`) ở lần boot đầu, seed bị bỏ qua VĨNH VIỄN:
  ```bash
  cd /d/planka && docker compose down
  powershell -Command "Remove-Item -Path 'D:\planka\db' -Recurse -Force"
  mkdir -p /d/planka/db && docker compose up -d   # seed lại từ env
  ```
- Verify: `docker exec planka-db psql -U postgres -d planka -t -c "SELECT email, role FROM user_account;"`
- Bản mới cũng hiện trang `/setup` wizard trên web khi chưa có admin (HTTP 200).

## API notes
- `POST /api/users` (Sails blueprint) đòi token — trả `E_UNAUTHORIZED`, không dùng để bootstrap được.
- `POST /api/login` với admin đã seed trả `E_NOT_FOUND` khi test qua curl — không phải route chuẩn của bản này. Login thật qua web UI. Đừng mất thời gian mò endpoint login API.
- Các route mẫu trong repo: `server/config/routes.js` (Sails blueprint style, `GET/POST /api/users`, `/api/cards/...`).

## Local vs tunnel (đừng đổ lỗi cho Planka)
- localhost:3010: 5-18ms. Qua tunnel chậm/404 → xem skill `cloudflare-tunnel` (benchmark localhost trước, check duplicate cloudflared process, WARP, config ingress).
