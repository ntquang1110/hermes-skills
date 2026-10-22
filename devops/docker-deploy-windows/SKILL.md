---
name: docker-deploy-windows
description: "Deploy Docker Compose services on Quang's Windows machine — mandatory port-conflict check before binding, D: drive data placement (never C:), flaky-network retry pulls, Docker Desktop lifecycle quirks."
version: 1.0.0
---

# Docker Deploy trên Windows (máy NTQUANG_DELL)

## Khi nào dùng
- User yêu cầu deploy / self-host một service bằng Docker Compose trên máy Windows này
- Pull image thất bại vì mạng chập chờn (TLS handshake timeout)
- Cần giữ dữ liệu service KHÔNG nằm trên ổ C:

## ⚠️ BƯỚC 0 — BẮT BUỘC: Check port TRƯỚC khi bind
Máy này có port map cố định: 5099=site, 3000=Company, 3001=TheLiem, 3003=KFlow, 5011=Status (hermes-dashboard), 8090=company dash (ai-company/dashboard), 8100=tfo CEO (FastAPI), 3010=Planka (kan.thefirstonly.com).

Chạy `netstat -ano | grep -E ":30[0-9][0-9]|:50[0-9][0-9]" | grep LISTEN` để xác nhận port thực tế. KHÔNG bind vào port đang dùng — user từng sửa lỗi này ("port 3000 đang run company site mà").

Nếu lỡ bind trùng: sửa `WEB_PORT` + `NEXT_PUBLIC_BASE_URL` trong `.env`, rồi `docker compose up -d --force-recreate web` (chạy background=true).

## Không dùng ổ C: — bind mount vào D:
- Code + dự án đặt tại `D:\<project>\`
- Dữ liệu DB: sửa docker-compose.yml, thay named volume bằng bind mount:
  ```yaml
  volumes:
    - /d/<project>/pgdata:/var/lib/postgresql/data
  ```
- Images/containers vẫn nằm trên C: (Docker Desktop data dir) trừ khi user đổi settings — giải thích 2 lớp này cho user, đừng hứa "sạch ổ C" khi chỉ làm bind mount.

## Mạng chập chờn — retry loop (pull lỗi TLS handshake timeout)
- Viết script retry chạy nền (xem `scripts/retry_pull.sh`): loop tới khi `docker image inspect <img>` thành công cho TẤT CẢ images, giữa các lần sleep 15s.
- Kinh nghiệm: từng image sẽ pull được ở các attempt khác nhau — kiên nhẫn loop.
- Git clone đứt giữa chừng: set `git config --global http.postBuffer 524288000 && git config --global http.lowSpeedLimit 0 && git config --global http.lowSpeedTime 999999` rồi clone lại. Fallback: tải ZIP qua curl/urllib (repo nhỏ) hoặc `git clone --depth 1`.

## Docker Desktop lifecycle
- Nếu `docker ps` báo daemon không chạy: start Docker Desktop bằng terminal background process (`"C:\Program Files\Docker\Docker\Docker Desktop.exe"`), chờ loop tới khi `docker ps` OK (30-60s).
- Windows shell của Hermes KHÔNG có quyền admin — không `net stop/start` service, không taskkill service Windows. Báo user tự chạy trong Terminal (Admin) hoặc restart máy.

## Tool quirks
- `docker compose up -d` bị terminal tool flag là long-lived → luôn chạy background=true (+ notify_on_complete).
- `python3` gọi ra Windows Store alias lỗi ("Python was not found") → dùng `python`.
- Container migrate đôi khi "kẹt" ở spinner "applying migrations" — thực ra đang chạy chậm. Chờ + xem log. Nếu exit ≠ 0: `docker start kan-migrate` để chạy lại (idempotent).

## Verify sau deploy
- `docker compose ps` — web/db Up (healthy), migrate Exited (0).
- `curl -s -o /dev/null -w "%{http_code}" http://localhost:<PORT>` → 200.
- Test trang thực tế (login/landing), không chỉ dừng ở "container up".

## Keep-alive: watchdog script + cron (silent-on-success)
Services (không chỉ Docker) nên có watchdog tự restart khi chết — đã chạy: `watchdog-firstonly.py` (port 3000) + `watchdog-erp.py` (ports 8080, 10000).
1. Script đặt tại `~/AppData/Local/hermes/scripts/watchdog-<name>.py`:
   - `is_port_open(port)` check socket; nếu DOWN → kill process giữ port (PowerShell `Get-NetTCPConnection ... Stop-Process`), `subprocess.Popen` start lại với `CREATE_NO_WINDOW`, log vào `<project>/logs/watchdog-<name>.log`
   - **Silent-on-success**: chỉ `print` khi có restart (cron no_agent: stdout rỗng = im lặng, không spam Telegram)
2. Cron job: `no_agent=true`, `script=watchdog-<name>.py`, `schedule=every 60m`, deliver origin.
3. Test thủ công trước khi tạo cron: `python watchdog-<name>.py` — không output khi UP = OK.
4. Dịch vụ non-Docker cần lệnh start đúng (VD `npx vite dev --port 8080 --strictPort` trong `cwd=PROJECT_DIR`); 1 project có thể chạy 2 dev server khác port để serve 2 domain (demo-erp 10000 + erp 8080).

## Admin seeding của app (nếu app tự tạo admin khi boot)
- Đọc repo app để lấy ĐÚNG tên env var admin — đừng đoán. Planka dùng `DEFAULT_ADMIN_EMAIL/PASSWORD/NAME/USERNAME`; dùng nhầm `ADMIN_EMAIL` thì âm thầm không seed gì (xem `references/planka-deploy.md`).
- Nếu app crash trong lúc postgres chưa ready lúc boot đầu, seed có thể bị bỏ qua VĨNH VIỄN → down stack, xoá thư mục bind mount DB, up lại (mất dữ liệu — chấp nhận được khi chưa có data).
- Verify seed qua SQL trực tiếp (`docker exec <db> psql ...`), đừng chỉ test UI.

## Expose qua Cloudflare tunnel (nếu user yêu cầu domain)
- Sau khi service chạy local, bước tiếp theo thường là trỏ subdomain qua tunnel — xem skill `cloudflare-tunnel` (ingress PUT + DNS CNAME + verify).
- ⚠️ Bẫy zone: cert.pem zoneID có thể là zone KHÁC với domain đích (máy này cert.pem là theliems.com nhưng account quản cả thefirstonly.com). LUÔN resolve zone qua `GET /zones?name=<domain>` trước khi POST DNS record — đừng dùng zoneID từ cert.pem.
- Sau khi thêm ingress: đổi `NEXT_PUBLIC_BASE_URL` trong `.env` sang domain thật → `docker compose up -d --force-recreate web` → verify `curl https://domain/login`.

## Support files
- `scripts/retry_pull.sh` — retry loop pull images tới khi đủ (dùng khi mạng chập chờn)
- `references/planka-deploy.md` — recipe deploy Planka (Trello clone đang chạy) lên 3010: compose, env admin seeding, lỗi thường gặp
- `references/kan-deploy.md` — recipe Kan (Trello alternative) — **đã gỡ, thay bằng Planka**, giữ làm ví dụ deploy general
- `references/favicon-branding.md` — quét & thêm favicon brand TFO cho mọi site tự host (khi user hỏi "trang nào chưa favicon"): probe từng port, extract data URI favicon, path /static/ của FastAPI, restart server HTML-inline
