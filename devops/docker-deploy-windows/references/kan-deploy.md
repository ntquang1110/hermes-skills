# Deploy Kan (open-source Trello alternative) — recipe ví dụ

Repo: https://github.com/kanbn/kan — Next.js 15 + tRPC + Drizzle + PostgreSQL 15.
Docker compose có sẵn, images: ghcr.io/kanbn/kan:latest, ghcr.io/kanbn/kan-migrate:latest, postgres:15.

## Các bước đã chạy được (Jul 2026)

1. Clone vào ổ D (KHÔNG dùng ổ C):
   ```bash
   cd /d/ && git clone https://github.com/kanbn/kan.git
   # Mạng chập chờn → git clone đứt. Fix: git config --global http.postBuffer 524288000
   # Fallback: curl -sL -o kan.zip https://github.com/kanbn/kan/archive/refs/heads/main.zip
   ```

2. Tạo `.env` (tối thiểu):
   ```env
   NEXT_PUBLIC_BASE_URL=http://localhost:3010
   BETTER_AUTH_SECRET=<32 ký tự ngẫu nhiên>   # python -c "import secrets,string; print(''.join(secrets.choice(string.ascii_letters+string.digits) for _ in range(32)))"
   POSTGRES_PASSWORD=<password>
   POSTGRES_URL=postgresql://kan:<password>@kan-db:5432/kan_db
   WEB_PORT=3010
   ```
   ⚠️ Port 3010 vì 3000 = Company site (xem port map trong memory).

3. Sửa docker-compose.yml — dữ liệu DB không nằm trên C::
   ```yaml
   volumes:
     - /d/kan/pgdata:/var/lib/postgresql/data   # thay vì named volume kan_postgres_data
   ```
   mkdir -p /d/kan/pgdata

4. Docker Desktop phải chạy trước. Nếu `docker ps` lỗi daemon:
   start bằng background process, chờ tới khi `docker ps` OK.

5. Pull images với retry loop (scripts/retry_pull.sh trong skill này) — mạng chập chờn,
   từng image pull được ở attempt khác nhau.

6. Up stack:
   ```bash
   cd /d/kan && docker compose up -d    # background=true
   ```
   - Migrate container đôi khi "kẹt" spinner "applying migrations" — thực ra chạy chậm.
     Nếu exit ≠ 0: `docker start kan-migrate` (idempotent).
   - Web: `docker start kan-web` nếu Created mà không Up.

7. Verify: `curl -s -o /dev/null -w "%{http_code}" http://localhost:3010/login` → 200.

## Vận hành
```bash
cd /d/kan && docker compose ps          # status
docker compose logs -f                  # log
docker compose stop / up -d             # dừng / chạy lại
```

## Ghi chú
- Đăng ký tài khoản đầu tiên trên UI = tạo admin.
- Kan có sẵn TIKTOK_CLIENT_ID/SECRET trong env example — liên quan tới OAuth provider config, không phải auto-upload.

## BẮT BUỘC: bật đăng ký email/password (Better Auth)
Kan mặc định TẮT email/password sign-up → API trả:
`{"code":"EMAIL_AND_PASSWORD_SIGN_UP_IS_NOT_ENABLED", ...}`
(UI vẫn hiện form nhưng submit lỗi).

Fix: thêm vào `.env` rồi recreate web:
```env
NEXT_PUBLIC_ALLOW_CREDENTIALS=true
```
```bash
docker compose up -d --force-recreate web    # background=true
```
Verify qua API (không cần mở browser):
```bash
curl -s -X POST https://<domain>/api/auth/sign-up/email \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","email":"test@example.com","password":"Test@123456"}'
# → {"token":"...","user":{...}} là OK
```
Test xong xoá user test qua DB:
```bash
docker exec kan-db psql -U kan -d kan_db -c "DELETE FROM \"user\" WHERE email='test@example.com';"
```

## Lưu ý email verification
Không config SMTP → user mới có `emailVerified:false` nhưng login vẫn OK. Chỉ khi cần quên mật khẩu / invite member qua email mới phải config SMTP (SMTP_HOST/PORT/USER/PASSWORD/EMAIL_FROM).
