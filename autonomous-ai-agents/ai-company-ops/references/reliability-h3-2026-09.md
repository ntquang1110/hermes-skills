# H3 — Reliability (watchdog + backup + uptime probe) — ĐÃ BUILD + VERIFY THẬT 03/09

Server TFO 8100: `D:/Hermes Proj/ai-company`. SCripts live in `hub/` and copies in
`~/AppData/Local/hermes/scripts/` (cron script path phải relative filename).

## L1 — Watchdog auto-restart (`hub/watchdog_8100.py`)
- Ping `http://127.0.0.1:8100/api/health` timeout 8s. Fail → taskkill port + launch
  `tfo_launch.py` detached (`DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP | CREATE_NO_WINDOW`,
  stdout→`logs/tfo_watchdog_server.log`, env load keys từ .env hermes) → chờ health OK ≤75s.
- Verify thật: kill server → tự kéo dậy 1.6s, health OK, log `✓ RESTART OK ... launch pid=`.
- **KHÔNG restart khi healthy** (chống vòng lặp): `once()` chỉ làm gì khi health fail.
- Cron no_agent every 1m: `ai-company-watchdog-8100`. Script default = 1 lượt bounded;
  daemon nền qua `--loop` (60s).

## L2 — Backup store+tfo_data → Ổ D (`hub/backup_tfo.py`)
- Snapshot `D:/Hermes/backups/tfo/<ts>/`, giữ 10 bản bằng `sorted(glob)` + prune, xóa cũ.
  `shutil.copytree(src,dst,dirs_exist_ok=True)`. Ghi `LATEST.json` manifest.
- Verify: snapshot store(0.16MB)+tfo_data(294MB); restore test chép meetings.json khỏi
  snapshot → `md5sum` TRÙNG, JSON parse OK. `restore_test_*` phải gitignore.
- Cron no_agent `0 3 * * *`: `ai-company-backup-tfo`.

## L3 — Uptime probe → Telegram (`hub/uptime_probe_8100.py`)
- Ping local health + tunnel `https://tfo.thefirstonly.com/api/health`. Down ≥2 lần liên
  tiếp → gửi Telegram beFounders `chat_id=-1004368353156`, `parse_mode=HTML`+`html.escape`.
- **PITFALL CHẾT NGƯỜI — transition-based no-spam:** đừng bắt transition bằng state string
  `"healthy"/"down"`. Nếu fail#1 đã ghi `state="down"`, thì fail#2 thấy `was_healthy=False`
  → KHÔNG báo → alert không bao giờ bắn. **Đúng:** track `consecutive_fails`, báo khi
  `new_fails >= CONSECUTIVE_FAILS and prev_fails < CONSECUTIVE_FAILS` (vượt ngưỡng). Còn
  down tiếp (prev >= thres) → im lặng. Recover → reset 0. Verify: healthy~silent, fail1~silent,
  fail2~1 alert (status 200), fail3~no re-alert, recover~silent+reset.
- Cron no_agent every 5m: `ai-company-uptime-probe-8100`.

## Pattern cron no_agent chung
- Script default = **bounded 1 lượt** (cron gọi không args, tự exit, stdio rỗng=silent).
  Daemon nền dùng `--loop`. KHÔNG để script loop vô hạn trong cron.
- **Pitfall bash (đã verify nhiều lần):** CẢ `//F //PID` lẫn `taskkill /PID X /F` gọi TRỰC TIẾP trong terminal tool git-bash đều fail ("Invalid argument/option - '//PID'" / path-mangle MSYS); process vẫn LISTENING sau khi lệnh "chạy". Cách ĐÃ VERIFY: bọc qua cmd — `cmd //c "taskkill /F /PID <pid>"` (git-bash convert `//c` → `/c`, inner command giữ nguyên single-slash). Sau kill luôn `netstat -ano | grep :<port> | grep LISTENING` xác nhận port thật free trước khi spawn lại.
  Dùng **1 slash** `taskkill /PID X /F`.
- Push TG bằng `urllib.request` + `urllib.parse.urlencode` (không cần requests):
  POST form-encoded, đọc `resp["ok"]`. Đảm bảo `html.escape(text, quote=False)`.
- State file: `logs/uptime_probe_state.json` — JSON ghi qua tmp+`os.replace` (atomic).

## Dev quy trình
1. CLI test trước (`python hub/*.py`), 2. kill test thật cho watchdog/probe,
3. chạy cron `hermes cron run <name>` xác nhận `Ran now: succeeded`,
4. copy sang `~/AppData/Local/hermes/scripts/`, 5. push git (chỉ code/scripts + features.json).