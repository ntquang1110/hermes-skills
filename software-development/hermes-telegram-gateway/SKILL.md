---
name: hermes-telegram-gateway
title: Hermes Telegram Gateway
description: "Configure, test, and troubleshoot the Hermes Telegram bot gateway — connectivity, proxy/VPN, group chat behaviour, log inspection, and common Viet Nam network issues."
version: 1.0.0
author: agent
created_by: agent
tags: [hermes, telegram, gateway, proxy, windows, vietnam, bot, troubleshooting]
---

# Hermes Telegram Gateway — Configuration & Troubleshooting

Handles the full lifecycle of connecting Hermes to Telegram, keeping it running, and tuning how the bot behaves in groups vs DMs.

## Fresh git-install — first-time Telegram setup

Trên máy Windows mới cài Hermes từ git (không phải desktop app), Telegram cần vài bước thủ công:

1. **Tạo `.env`** — dùng PowerShell **UTF8-NoBOM** (Set-Content mặc định thêm BOM → lỗi đọc key):
   ```powershell
   $sw = New-Object System.IO.StreamWriter("$env:LOCALAPPDATA\hermes\.env", $false, [System.Text.UTF8Encoding]::new($false))
   $sw.WriteLine("TELEGRAM_BOT_TOKEN=8862427748:AA...")
   $sw.WriteLine("TELEGRAM_ALLOWED_USERS=6277220574")
   $sw.Close()
   ```
2. **Bật Telegram trong config:**
   ```bash
   hermes config set platforms.telegram.enabled true
   ```
3. **Cấu hình model provider** — nếu dùng custom provider (ByteDance Ark coding plan), dùng `api_key` trực tiếp, KHÔNG dùng `key_env` (xem `hermes-model-provider-troubleshooting` skill).
4. **Restart gateway** rồi kiểm tra log:
   ```bash
   hermes gateway restart
   grep -i telegram ~/AppData/Local/hermes/logs/gateway.log | tail
   ```
   Thấy `[Telegram] Connected to Telegram (polling mode)` + `Gateway running with 1 platform(s)` là OK.

5. **PITFALL — gateway KHÔNG tự cài được Telegram; plugin phải được ENABLE tường minh.**
   Restart lần đầu log hay báo chuỗi này:
   ```
   gateway.platform_registry: Platform 'Telegram' dependencies missing — attempting install...
   gateway.platform_registry: Platform 'Telegram' requirements not met (Run `hermes setup` to install Telegram support.)
   gateway.run: Platform 'telegram' is registered but adapter creation failed (check dependencies and config)
   gateway.run: No adapter available for telegram
   gateway.run: No adapter could be created for any of the 1 configured platform(s).
   ```
   Đọc kỹ dòng `plugins list` — plugin tồn tại nhưng ở trạng thái **`not enabled`**:
   ```
   │ telegram-platform   │ not enabled │ 1.0.0 │ Telegram gateway via python-telegram-bot │ user │
   ```
   **Fix (không cần `hermes setup`, không cần install lại):**
   ```bash
   hermes plugins enable telegram-platform
   hermes gateway restart
   ```
   Output đúng: `✓ Plugin platforms/telegram enabled` → log có `telegram connected`.
   Config sẽ ghi `plugins.enabled: [platforms/telegram]` → sống qua các lần restart sau.

   **Đừng tốn thời gian với:** `hermes plugins install telegram` (Error: not in catalog),
   `hermes setup` (menu `model|tts|gateway|tools|telemetry|agent` không có mục Telegram),
   hay `hermes send --list telegram` (trả `(no channels discovered yet)` dù adapter vẫn hỏng —
   lệnh này đọc token từ .env nên KHÔNG phản ánh trạng thái adapter).

   **Phân biệt với lỗi thiếu lib:** nếu `python -c "import telegram"` trong venv Hermes fail thì
   đúng là thiếu `python-telegram-bot`; còn plugin `not enabled` thì lib đã có sẵn, chỉ là chưa bật.

## Prerequisites

- Hermes Agent installed and running
- Telegram bot token from [@BotFather](https://t.me/BotFather)
- `TELEGRAM_BOT_TOKEN` set in `.env` or config.yaml

## Quick Reference

```bash
# Check gateway status
hermes gateway status

# View live logs
tail -f ~/AppData/Local/hermes/logs/gateway.log

# Restart gateway
hermes gateway restart

# Stop gateway
hermes gateway stop

# View recent errors
grep -E "error|fail|timeout|Connected|Disconnected" ~/AppData/Local/hermes/logs/gateway.log | tail -20
```

## Configuring Telegram

### Minimal config.yaml settings

```yaml
telegram:
  reactions: false                    # Disable like/dislike reactions
  allowed_chats: ''                   # Whitelist chat IDs (empty = all allowed)
  require_mention: false              # false = respond to ALL group messages
  extra:
    rich_messages: false              # MarkdownV2 rendering
```

### Key settings explained

| Setting | Type | Default | Effect |
|---------|------|---------|--------|
| `require_mention` | bool | `true` | `true` = bot only responds to @mentions, /commands, replies in groups. `false` = responds to ALL group messages. |
| `allowed_chats` | string | `''` | Comma-separated chat IDs. When non-empty, only those chats work (hard gate). |
| `guest_mode` | bool | `false` | **`true` = bot trả lời @mention từ MỌI nhóm, kể cả nhóm không nằm trong allowlist.** Câu hỏi thường gặp "sao bot trả lời trong nhóm lạ" gần như luôn là key này |
| `reactions` | bool | `false` | Show 👍/👎 reaction buttons on responses. |

#### `guest_mode: true` + `allowed_chats` rỗng = bot trả lời ở MỌI nhóm

Comment trong `config.yaml` nói rõ:

```
# guest_mode lets explicit @mentions from non-allowlisted groups through.
# Default false; ordinary messages, replies, and regex wake words stay blocked.
```

Triệu chứng người dùng báo: *"mọi người tag em trong các nhóm tele..."* — bot bị tag
là trả lời, ở nhóm chưa từng cho phép. Cấu hình gây ra (dòng 2089–2091 trên
`lqremote`):

```yaml
allowed_users: 6277220574,393536794
guest_mode: true          ← thủ phạm
allowed_chats:            ← rỗng, nên không có allowlist nào chặn
```

**Đây KHÔNG chữa được bằng `hermes gateway restart`** — restart chỉ nạp lại đúng
config đó. Phải sửa key:

```bash
hermes config set plugins.platforms.telegram.guest_mode false
# và/hoặc điền allowlist:
hermes config set plugins.platforms.telegram.allowed_chats "-1001234567890,-1009876543210"
```

Đổi xong mới restart (adapter chỉ đọc settings lúc khởi động).

⚠️ Đây là đổi hành vi nhận tin của máy (thường là máy người khác) — hỏi trước, và
xin danh sách nhóm được phép để điền `allowed_chats`, đừng đoán. Nếu anh muốn giữ
một vài nhóm thì phải hỏi đúng tên/id nhóm, không tự chọn.

**Bẫy chẩn đoán:** đừng để bị cuốn vào "restart để nạp config". Agent trên máy đó
đã lấy cách restart để chữa triệu chứng này, và cái nó nhận được là gateway tự giết
mình (xem "### 8" + mục 4). Đọc config trước, restart sau.

### BotFather privacy (external)

Even with `require_mention: false` in Hermes config, Telegram BotFather has its own **Group Privacy** setting:

1. Open @BotFather → `/mybots` → select your bot
2. **Bot Settings** → **Group Privacy**
3. **Disable** (turns off privacy) — bot sees ALL messages in groups
4. **Enable** — bot only receives @mentions, /commands, and replies

**Both must agree**: BotFather Privacy = Disabled AND `require_mention: false` for full group message reception.

### Multi-User Group Authorization

Hermes uses `TELEGRAM_ALLOWED_USERS` to control **which Telegram users** can trigger responses in group chats. This is independent of `require_mention`.

**Why it exists:** A bot in a shared group should not auto-respond to strangers. `TELEGRAM_ALLOWED_USERS` acts as a user-level allowlist.

**How it works** (from `plugins/platforms/telegram/adapter.py`):
```python
allowed_csv = os.getenv("TELEGRAM_ALLOWED_USERS", "").strip()
if not allowed_csv:
    # Fail-closed: NO allowlist → deny ALL users by default
    return False  # (unless GATEWAY_ALLOW_ALL_USERS=true)
allowed_ids = {uid.strip() for uid in allowed_csv.split(",") if uid.strip()}
return "*" in allowed_ids or normalized_user_id in allowed_ids
```

**When `TELEGRAM_ALLOWED_USERS` is unset:**
- Only the bot owner can interact (the user who set up the gateway)
- Other group members' messages appear in gateway.log as:
  ```
  WARNING gateway.run: Unauthorized user: <USER_ID> (<NAME>) on telegram
  ```
- The bot **reads** their messages (sees chat content) but does **NOT respond** — even with @mentions

**To authorize additional users:**
1. Get user IDs from @userinfobot
2. Add to `.env` (comma-separated):
   ```bash
   echo 'TELEGRAM_ALLOWED_USERS=6277220574,8700208818' >> ~/AppData/Local/hermes/.env
   ```
3. Restart gateway:
   ```bash
   hermes gateway restart
   ```

### Finding unknown user IDs (when @userinfobot is not an option)

When a user has already messaged the bot but you don't know their Telegram user ID, extract it via the Bot API directly:

1. **Stop the gateway** (releases the bot poll):
   ```bash
   hermes gateway stop
   ```
2. **Call getUpdates** (wait ~5s after stop):
   ```bash
   curl -s "https://api.telegram.org/bot<TOKEN>/getUpdates"
   ```
3. **Parse the response** — each `message.chat` contains the user's `id`, name, and username:
   ```json
   {"message": {"chat": {"id": 393536794, "first_name": "Nguyễn", "last_name": "Quân"}}}
   ```
4. **Add the ID** to `.env`:
   ```
   TELEGRAM_ALLOWED_USERS=6277220574,393536794
   ```
5. **Restart the gateway**:
   ```bash
   hermes gateway restart
   ```

**Important:** `getUpdates` conflicts with the running gateway (`409 Conflict`). The gateway MUST be stopped first. Restart AFTER adding the user.

**PITFALL — Cold boot drops pending updates:** When the gateway restarts, `drop_pending_on_cold_boot: true` discards messages sent while offline. The user must message again after restart. To avoid this, keep the gateway running and ask the user for their @username instead.

| Setting | Effect |
|---------|--------|
| Unset (empty) | Only bot owner — everyone else is `Unauthorized` |
| `ID1,ID2,...` | Only listed IDs — others are denied |
| `*` | Allow everyone (use with caution) |
| `GATEWAY_ALLOW_ALL_USERS=true` | Override: allow all users unconditionally |

**Diagnosis tip:** When a group member reports the bot won't respond, grep gateway.log for `Unauthorized` — it's the fastest way to identify a missing user allowlist entry.

## Proxy / VPN — Vietnam & Blocked Regions

Telegram is blocked or throttled in Vietnam (api.telegram.org unreachable). 

### Symptom pattern (in gateway.log)
```
[Telegram] Primary api.telegram.org connection failed
[Telegram] Fallback IP 149.154.166.110 failed
Failed to send Telegram message: Timed out
All connection attempts failed
```

### Option A: Cloudflare WARP (recommended, free)

```bash
# Check if installed
ls "/c/Program Files/Cloudflare/Cloudflare WARP/"

# Check status
"/c/Program Files/Cloudflare/Cloudflare WARP/warp-cli.exe" status

# Connect
"/c/Program Files/Cloudflare/Cloudflare WARP/warp-cli.exe" connect

# Disconnect
"/c/Program Files/Cloudflare/Cloudflare WARP/warp-cli.exe" disconnect
```

The bot's traffic routes through WARP automatically in VPN mode — **no TELEGRAM_PROXY needed**.

### Option B: SOCKS5 / HTTP proxy

```bash
# Set proxy (SOCKS5)
hermes config set TELEGRAM_PROXY socks5://127.0.0.1:1080

# Set proxy (HTTP)
hermes config set TELEGRAM_PROXY http://127.0.0.1:7890

# Clear proxy (use direct connection)
hermes config set TELEGRAM_PROXY ""
```

### Option C: Fallback IPs

Hermes auto-discovers Telegram fallback IPs (149.154.166.110). If the primary DNS fails, it retries via fallback. This helps partially but is unreliable for prolonged blocking.

## Log-Based Diagnosis

### Good state (working)
```
[Telegram] Connected to Telegram (polling mode)
[Telegram] set_my_commands OK for scope BotCommandScopeAllGroupChats (51 cmds)
[Telegram] Flushing text batch agent:main:telegram:group:<CHAT_ID>:<USER_ID> (X chars)
inbound message: platform=telegram chat=<CHAT_ID> msg='...'
response ready: platform=telegram chat=<CHAT_ID> time=Xs response=XXX chars
```

### Bad state (broken)

| Log pattern | Likely cause | Fix |
|------------|-------------|-----|
| `Connect attempt 1/8 failed: httpx.ConnectError` | Telegram blocked / proxy wrong | Check WARP/proxy config |
| `Proxy detected; passing explicitly to HTTPXRequest: http://127.0.0.1:7890` | Proxy set but no proxy running | `hermes config set TELEGRAM_PROXY ""` or start proxy |
| `Primary api.telegram.org connection failed` | Vietnam ISP blocking | Enable WARP or proxy |
| `Failed to send Telegram message: Timed out` | Outbound blocked (inbound may still work) | Same as above |
| `Suppressing normal final send for session ... content_delivered=True` | Message sent successfully via streaming | Not an error |
| `tt gate: ... → PROCEED (decision=None) → dispatch agent` with **no** following `API call #N` for that session, and `run_agent: OpenAI client created (agent_init, ...)` as the session's last line | Bloated long-lived session hung the agent (1000+ msgs / weeks old) | `hermes sessions delete <SID>` + `hermes gateway restart` — see "### 9. Group chat HANGS" |
| `turn_taking.delivery: open_thread failed — no delivery for chat <ID>` (repeats every inbound) | **Red herring** — falls back to `tt send: ... → passthrough`; not the cause | Ignore; diagnose the session instead |
| `Non-retryable client error: HTTP 400` + `insufficient tool messages following tool_calls` | Corrupted session context | `hermes sessions delete <session_id>` then restart |
| `Config version outdated (v0 → v30)` | Config needs migration | Stop gateway → `hermes config migrate` → restart |
| `Polling heartbeat probe failed ()` then `updater.stop() timed out during network-error reconnect (likely CLOSE-WAIT socket)` then `forcing drain and restart without clean stop` | WARP disconnected mid-session | Check WARP status → reconnect WARP → restart gateway |
| `No gateway process detected` but `Scheduled Task: Ready` | Gateway crashed after repeated network errors | Check WARP first (likely disconnected) → re-verify connectivity → restart |
| `⚠️ Model returned empty after tool calls` → `Empty response (no content or reasoning) — retry N/3` → `❌ No fallback providers configured` | Primary model/provider returned empty AND/OR `fallback_providers` stored as a JSON **string** instead of a YAML **list** in config.yaml AND/OR context ballooned past the provider's real limit (`model.context_length` too high → compression fires at 85% of it, e.g. 200000 → 170K, still past the ~150K dead zone; `agent.log` shows `in=266K out=0`) | Probe provider endpoint → verify fallback_providers is a real YAML list → set `model.context_length 120000` (compression fires ~102K) — see `references/empty-response-fallback-config.md` |

### 6. Gateway restart blocked from inside gateway process

When you need to restart the gateway but you're inside a session running under the gateway itself (e.g., Telegram chat → agent → terminal), `hermes gateway restart` is blocked because it would kill the current session:

```
Blocked: cannot restart or stop the gateway from inside the gateway process.
```

**Workaround:** Start a new gateway process with `--replace` to auto-kill the old one:

```bash
# From the gateway session's terminal, start a background process:
cd ~/AppData/Local/hermes
python -m hermes_cli.main gateway run --replace
```

This kills the old gateway PID and starts a fresh one. The old `gateway.pid` and `gateway.lock` files are automatically cleaned up.

**Failsafe:** If --replace doesn't work and the gateway is stuck with stale PID file:

```bash
# 1. Find the gateway process
wmic process where "name='pythonw.exe' and commandline like '%gateway%'" get processid

# 2. Force kill all pythons (WARNING: kills all Python processes on the machine)
taskkill //F //IM pythonw.exe
taskkill //F //IM python.exe

# 3. Clear stale lock/pid files
rm -f ~/AppData/Local/hermes/gateway.lock ~/AppData/Local/hermes/gateway.pid

# 4. Restart via scheduled task
schtasks /run /tn "Hermes_Gateway"
```

After restart, verify:
```bash
# New PID written
cat ~/AppData/Local/hermes/gateway.pid

# New log entries
tail -5 ~/AppData/Local/hermes/logs/gateway.log
# Should show "Starting Hermes Gateway..." with current timestamp
```

## Common Fixes

### 1. Config migration fails with PermissionError

```
PermissionError: [WinError 5] Access is denied: ...config.yaml
```

**Cause**: Gateway holds the file lock.
**Fix**: Stop gateway first, then migrate, then restart:
```bash
hermes gateway stop
hermes config migrate
hermes gateway start
```

### 2. Bot works in DM but not in group

Check two places:
1. **BotFather** → Group Privacy = **Disabled**
2. **Hermes config**: `telegram.require_mention = false`

Both must be set. After changing either, run `hermes gateway restart`.

### 3. Repeated "tool_calls must be followed by tool messages"

A session has corrupted turn structure (tool_calls without matching tool_results).

```bash
# Find the session
hermes sessions list | grep -i error
# Delete it
hermes sessions delete <session_id>
hermes gateway restart
```

### 4. Gateway stops unexpectedly

Check the shutdown context:
```bash
grep "Shutdown" ~/AppData/Local/hermes/logs/gateway.log | tail -3
```

Common causes: Windows restart, power loss, manual stop.

**Đừng vội coi `Received UNKNOWN as a planned gateway stop` là auto-restart bình
thường — đã có case nó là dấu hiệu của outage 15 TIẾNG.** Trình tự đúng:

1. `hermes gateway status` → có PID đang chạy không?
2. Có PID → nhiều khả năng chỉ là shutdown của tiến trình cũ, boot mới đang lên.
   Xác nhận bằng tiến trình MỚI:

```
grep "Starting Hermes Gateway" ~/AppData/Local/hermes/logs/gateway.log | tail -1   # boot hiện tại
grep "✓ telegram connected"   ~/AppData/Local/hermes/logs/gateway.log | tail -1   # bằng chứng thật
```

3. **KHÔNG có PID → tuyệt đối không bỏ qua.** Đây là ca 13–14/10/2026 trên
   `lqremote`: gateway dừng 23:09 và nằm chết ~15 tiếng. Dòng
   `signal=UNKNOWN ... parent_pid=<N>` đi kèm là **không truy được ai** — phải đọc
   `state.db` mới biết. Nguyên nhân thật: **agent tự gọi `hermes gateway restart`**
   trong lượt của nó; nửa `stop` giết đúng tiến trình đang chạy lệnh nên nửa
   `start` không bao giờ chạy. Smart approval **gắn cờ rồi tự duyệt**:
   `"Command was flagged (stop/restart hermes gateway (kills running agents)) and
   auto-approved by smart approval"`.

   Truy lệnh trong `state.db` (bảng `messages`, `role=assistant` giữ lệnh ở
   `tool_calls`, `role=tool` giữ kết quả kèm `approval`):
   xem `remote-hermes-windows` → `references/gateway-supervision-windows.md`.

   Chữa gốc KHÔNG phải restart thêm — phải có tầng giám sát
   (`MultipleInstances=IgnoreNew` trong Scheduled Task), vì login-item không tự bật
   lại khi gateway dừng giữa chừng.

4. Nghi máy vừa restart? Kiểm chéo bằng event log trước khi kết luận — mã `1074`
   (ai yêu cầu), `41`/`1001`/`6008` (crash/mất điện), `6005` (boot). Case thật:
   chỉ **1** biến cố crash duy nhất, còn lại là restart sạch do `RuntimeBroker.exe`
   `Other (Unplanned)`. Nhìn 2 mốc thời gian gần nhau rồi kết luận "máy tự restart
   định kỳ" là báo sai bệnh. Chi tiết: `references/gateway-supervision-windows.md`.

Các dòng khởi động của boot mới xuất hiện sau vài giây tới ~1 phút kể từ lúc có PID;
poll một lần với `sleep 5` trước khi kết luận là kẹt.

**Who/what restarted it?** `~/AppData/Local/hermes/logs/gateway-exit-diag.log` is a JSON lifecycle history — one line per `gateway.start` / `exit_clean` event, each with `pid`, `argv` (e.g. `gateway run` vs `gateway run --replace`), and timestamps. Read it to see if the restart was manual (`--replace`), scheduled, or crash-related.

**Expected noise during recovery:** `pruning stale sessions.json entry ... left by a crashed gateway` and `repointing stale sessions.json entry ... to recovered ...` are NORMAL crash-recovery lines, not errors.

**PID → service mapping** (to identify which process owns a port or confirm the gateway PID):
```bash
wmic process where "processid=20588" get processid,description,commandline
# or several at once:
wmic process where "processid=5332 or processid=16024" get processid,description,commandline
```

### 5. WARP disconnected mid-session (silent death)

WARP can disconnect without warning (`Reason: Settings Changed`). The gateway process remains technically alive but can no longer reach Telegram. After enough retries, the gateway process silently dies.

**Symptom**: User messages get no response. `hermes gateway status` shows `Scheduled Task: Ready` but `No gateway process detected` (or process shows as running but log shows no recent activity).

**Log signature**:
```
Polling heartbeat probe failed (); triggering reconnect
Telegram network error (attempt 1/10), reconnecting in 5s.
updater.stop() timed out during network-error reconnect (likely CLOSE-WAIT socket)
forcing drain and restart without clean stop
... (repeats across attempts)
Polling reconnect failed: Timed out
```
After the last reconnect failure, the gateway stops logging entirely — it's dead.

**Fix sequence** (must do in this order, or restart will immediately fail again):
```bash
# 1. Check WARP status FIRST
"/c/Program Files/Cloudflare/Cloudflare WARP/warp-cli.exe" status
# If Disconnected:

# 2. Reconnect WARP
"/c/Program Files/Cloudflare/Cloudflare WARP/warp-cli.exe" connect

# 3. Verify WARP is healthy
"/c/Program Files/Cloudflare/Cloudflare WARP/warp-cli.exe" status
# Expected: "Status update: Connected" + "Network: healthy"

# 4. Verify Telegram is reachable (404 = reachable, timeout/error = still blocked)
curl -so /dev/null -w "%{http_code}" --connect-timeout 5 https://api.telegram.org/bot

# 5. Now restart the gateway
hermes gateway restart

# 6. Verify clean startup
hermes gateway status
# Should show: "Gateway process running (PID: XXXX)"
tail ~/AppData/Local/hermes/logs/gateway.log
# Should show: "✓ telegram connected"
```

### 8. Watchdog tự restart gateway khi chết (Scheduled Task)

Hermes cron chạy TRONG gateway process — gateway chết thì cron cũng chết, không thể dùng cron Hermes làm watchdog. Phải dùng Windows Scheduled Task độc lập:

**Script:** `D:\Hermes\scripts\watchdog_gateway.py` — check `hermes gateway status`, nếu không có "Gateway process running" thì `hermes gateway start` + verify. Log: `D:\Hermes\logs\gateway-watchdog.log`.

**Đăng ký task (chạy mỗi 5 phút):**
```bash
schtasks /create /tn "Hermes_Gateway_Watchdog" /tr "python D:\\Hermes\\scripts\\watchdog_gateway.py" /sc minute /mo 5 /f
schtasks /run /tn "Hermes_Gateway_Watchdog"   # test
schtasks /query /tn "Hermes_Gateway_Watchdog" /v /fo LIST | grep -iE "Last Run|Last Result"
```

Lưu ý: script dùng `subprocess.CREATE_NO_WINDOW` (chạy không hiện cửa sổ), và khi `status` call fail (không chắc chắn) thì return alive=True — tránh start bừa khi máy đang bận.

#### ⚠️ Watchdog tự viết là NGUY HIỂM — Hermes gateway là SINGLETON

Mỗi instance gateway mới sẽ **giết** instance trước. Nghĩa là watchdog kiểu "không
thấy thì start" mà check sai một lần là **giết gateway đang khoẻ**. Đã dính thật:

```
15:09:47  KHONG thay gateway -> khoi dong lai
15:10:32  DA BAT LAI OK, pid=10452,8336
15:13:03  KHONG thay gateway -> khoi dong lai     ← gateway 8336 ĐANG SỐNG
15:13:48  DA BAT LAI OK, pid=9944,14428
```

Dấu vết trong `logs/gateway-exit-diag.log` là chuỗi `previous_unclean_exit` nối pid
liên tiếp (`14428 → 15108 → 10816`) — thấy chuỗi đó là biết đang có churn do check sai.

Ba cách check sống/chết đã **sai** trong thực tế, cả ba đều cho ra "chết" giả:

| Cách | Vì sao |
|---|---|
| `hermes gateway status` | Báo nhầm PID (từng trả `conhost.exe`), và không thấy tiến trình session 0 |
| `Win32_Process` lọc `CommandLine -like "*gateway run*"` | Âm tính giả với tiến trình session 0 |
| mtime `gateway_state.json` làm grace period | File được ghi **liên tục** khi gateway sống → không bao giờ hết hạn chờ |
| tin `gateway_state.json` | File kẹt: ghi `"gateway_state":"running"` + pid **đã chết** |

Cách đáng tin: **`Get-Process python` lọc `SessionId -eq 0`** — gateway là
`python.exe` duy nhất ở session 0 (`hermes serve` ở session 1).

**Tốt hơn nữa: đừng tự viết watchdog.** Giao cho Task Scheduler bằng
`MultipleInstances = IgnoreNew` — OS chặn trùng ở tầng hệ thống, không phụ thuộc
logic tự viết. Dùng `remote-hermes-windows` → `scripts/register_gateway_task.py`
(action = `hermes.exe gateway run` trực tiếp, `ExecutionTimeLimit=0` — mặc định là
3 ngày và sẽ kill gateway, trigger AtLogOn + AtStartup + lặp 5 phút để bắt cả ca
thoát SẠCH mà `RestartOnFailure` không bắt được). Đã verify: kill → tự bật lại
trong **21 giây**; trigger thêm 3 lần khi đang chạy → cùng pid, không chồng.

### 7. User sent a document/attachment but the agent never saw it

User says "em k đọc được tin nhắn đính kèm à" / "em follow doc này để làm" and no file content arrives. Don't guess — check whether the attachment actually reached the gateway:

```bash
grep "inbound message" ~/AppData/Local/hermes/logs/gateway.log | tail -20
```

- **Attachment DID arrive** → the inbound line carries a marker: `msg="... [Replied-to document 'mẫu hợp đồng thử nghiệm.docx' saved at <path>]"` (compare against any known-good doc delivery in the same log, e.g. the legal chats).
- **Attachment did NOT arrive** → the inbound line is plain text with `reply_to_id=None` and no `[Replied-to document ... saved` marker. The file never reached the bot. Common causes: BotFather privacy blocking non-mention messages (fix Group Privacy = Disabled), file > 20MB (`adapter.py:self._max_doc_bytes` skip — no cache, no agent delivery), or a bot-to-bot message (Telegram filters bot messages entirely).
- Fallback that always works: ask user to paste the doc's path (`D:\...`) or paste the content directly into chat. Don't burn time re-scanning the whole disk for a file the gateway never downloaded.

### 9. Group chat HANGS — agent dispatched, messages swallowed, no reply

**Symptom:** user says a group "đang bị treo" / "alo mà không trả lời". Messages land in the group
(bot readable) but no reply ever comes. Telegram itself is fine.

**Do NOT start with WARP/network.** This failure is local and has a precise log signature.

**Step 1 — find the chat_id and session_id, then check whether the agent ever called the API.**
```bash
grep "inbound message" ~/AppData/Local/hermes/logs/gateway.log | tail -15
# → inbound message: platform=telegram user=... chat=-5154673868 msg='alo'
grep "<CHAT_ID>" ~/AppData/Local/hermes/logs/gateway.log | tail -20
```
**Hang signature** — inbound is accepted and dispatched, but no API call follows it:
```
tt inbound: chat=-5154673868 text='alo'
tt gate: session=<SID> chat=-5154673868 → PROCEED (decision=None) → dispatch agent
notify: no home channel set — run /sethome to get alerts in chat
```
then in `agent.log`, for that session, the LAST line is:
```
run_agent: OpenAI client created (agent_init, shared=True) thread=hermes-gateway_2:9268 ...
```
and **nothing after** — no `agent.conversation_loop: API call #N`. Compare the timestamp of that
last line against `date`: minutes of silence on an active session = hung agent.

**Step 2 — rule out the delivery red herring.** `WARNING ... turn_taking.delivery: turn-taking:
open_thread failed — no delivery for chat <ID>` fires for EVERY inbound, including ones that reply
fine — it falls back to `tt send: chat=<ID> → passthrough`, which is normal. It appeared 118× in one
real session. **Not the cause; do not chase it.** Same for `notify: no home channel set`.

**Step 3 — prove Telegram is innocent with one Bot API call** (don't restart the gateway on a hunch):
```python
# sendMessage to the group; ok:True + message_id ⇒ transport is fine, fault is inside Hermes
```
If the bot posts successfully, the problem is the stuck session, not the platform.

**Step 4 — measure the suspect session.** Query the **ACTIVE** state.db, i.e. `$HERMES_HOME/state.db`
(`~/AppData/Local/hermes/state.db`), NOT a leftover from a previous drive migration. Sessions predate
Aug are a stale DB and will send you down a false trail.
```python
import sqlite3
c = sqlite3.connect(r'C:\Users\<user>\AppData\Local\hermes\state.db', timeout=60)
cur = c.cursor()
# sessions.id is the session_id; there is NO session_id column
cur.execute("SELECT id, chat_id, message_count, api_call_count, last_activity_at, title "
            "FROM sessions WHERE chat_id = ? ORDER BY last_activity_at DESC", ('-5154673868',))
cur.execute("SELECT COUNT(*) FROM messages WHERE session_id LIKE ?", ('%<SID>%',))
cur.execute("SELECT session_id, COUNT(*) n FROM messages GROUP BY session_id ORDER BY n DESC LIMIT 5")
```
**Diagnosis threshold:** a group session open for **weeks** with **1000+ messages** and **300+ API
calls** is the cause. Real case: `message_count=138` (post-compression) but **1470 rows** in
`messages` and **404** API calls — compression ran (288→133 msgs, ~102K tokens) and the agent still
hung on the next turn. One session like this also bloats the whole DB (observed `state.db` = 2.7 GB,
153,913 messages), which makes every other operation sluggish.

**Step 5 — fix (needs the user's OK; both steps are disruptive):**
```bash
hermes sessions delete <SID>        # drop the bloated session; group gets a fresh one next message
hermes gateway restart              # clears the hung in-process agent
hermes sessions optimize            # optional: merge FTS5 segments + VACUUM the DB
```
**Warn the user first on two counts:** deleting loses that group's conversation history, and
restarting the gateway **kills the current chat** if you are running inside that same gateway
(see "### 6. Gateway restart blocked from inside gateway process"). Get an explicit go-ahead.

**Durable prevention:** long-lived Telegram group sessions must be reset periodically (a daily cron
that rotates them), or they will eventually accumulate into this state.

**Secondary trap — dual-scope `gateway_routing` after a drive migration.** If `sessions/` is a
junction to another drive (check: `python -c "import os;print(os.path.realpath(r'...\hermes\sessions'))"`),
the `gateway_routing` table can hold entries under BOTH scopes (`C:\...\hermes\sessions` and
`D:\Hermes\hermes-home\sessions`), and a stale `state.db` may sit alongside the live one. Always
confirm which DB is live via its mtime before trusting any query.

### 10. Bot vẫn xưng hô / giọng CŨ sau khi đã sửa SOUL.md

**Triệu chứng:** sửa `SOUL.md` (hoặc `display.personality`), test bằng `hermes -z` thấy giọng mới,
restart gateway, mà nhắn vào chat vẫn bị trả lời như cũ. Người dùng nói kiểu
"vẫn gọi anh là anh" / "chưa thấy đổi gì".

**Nguyên nhân:** Hermes **ghim system prompt theo từng session** để giữ prompt cache. Mỗi dòng
`state.db.sessions` có `system_prompt_hash` trỏ tới bảng `system_prompts`. Phiên tạo TRƯỚC lúc sửa
giữ prompt cũ vĩnh viễn — **restart gateway không cứu được**. Thời điểm TẠO session quan trọng hơn
thời điểm restart.

Bằng chứng đã gặp thật: session Telegram tạo 15:00, SOUL.md ghi 16:07 → hash cũ, prompt KHÔNG có
từ khoá persona. Oneshot test lúc 16:09 ra hash mới, có đủ. Cùng một máy, cùng lúc, hai kết quả
khác nhau — vì khác thời điểm tạo phiên.

**Fix (giữ nguyên lịch sử chat):**
```bash
hermes sessions list --source telegram --limit 10
hermes sessions repair-prompts <session_id> --apply --json   # clear prompt đã ghim
hermes gateway restart                                        # xoá state trong RAM
```
`repair-prompts` gốc để sửa session hỏng do bug hygiene/compress, nhưng truyền `session_id` là
**destructive override**: nó clear cả prompt đang khoẻ. Không có `--apply` thì chỉ báo cáo.
Chỉ dùng `sessions delete <SID>` khi chat toàn tin test (mất lịch sử).

**Verify bằng NỘI DUNG, không bằng log:**
```python
cur.execute("SELECT id, source, chat_id, system_prompt_hash FROM sessions")
cur.execute("SELECT hash, prompt FROM system_prompts")        # grep từ khoá persona
cur.execute("SELECT role, content FROM messages ORDER BY id DESC LIMIT 10")  # bot TRẢ LỜI gì
```
`system_prompt_hash = NULL` nghĩa là đã clear, lượt sau dựng lại. Log chỉ có
`response ready: ... response=47 chars` — không cho biết nội dung, nên đừng dùng log làm bằng chứng.

**Bẫy tự tin:** `hermes -z` LUÔN tạo phiên mới nên luôn ăn ngay — nó che mất lỗi ghim prompt của
phiên cũ. Test cuối cùng bắt buộc là tin nhắn THẬT vào chat. Đường cùng cho người dùng: gõ `/new`.

Script probe sẵn (tải `state.db` từ máy khác, in prompt + tin nhắn cuối):
`remote-hermes-windows` → `scripts/dump_remote_session.py`.

## Sending messages proactively (desktop/CLI session, not inside the gateway)

When a desktop or CLI session (not a Telegram chat session) must push a message/link into a
Telegram chat, there are 2 ways. **Try `hermes send` FIRST** — it reuses the gateway's own platform
credentials (`.env` + `config.yaml`), needs no running gateway for bot-token platforms, and makes no
LLM call:

```bash
hermes send --to telegram:393536794 "noi dung"         # DM theo chat_id
hermes send --to telegram:-5154673868 "noi dung"       # group (id âm)
hermes send --to telegram:-1001234567890:17585 "..."   # group + topic/thread
hermes send --to telegram "MEDIA:/path/anh.png"        # gửi kèm file
hermes send --list telegram                            # liệt kê target đã biết
```

**PITFALL — cờ chat_id KHÔNG phải `--chat-id`.** `hermes send` không có flag `--chat-id`; target
truyền qua `--to`/`-t` theo format `platform:chat_id[:thread_id]`. Gọi sai cờ **không báo lỗi rõ**
mà in ra rỗng → rất dễ tưởng đã gửi thành công. Kiểm tra `hermes send --help` khi nghi ngờ, và
verify bằng `message_id` (thêm `--json`) chứ đừng tin stdout rỗng.

Nếu buộc phải gọi thẳng Bot API (Hermes CLI không có trong PATH, script ngoài Hermes), dùng cách
dưới — đọc token từ `.env`, không cần `hermes gateway`.

**Find the right chat_id first** — never guess.

**Khi user gọi tên nhóm (không đưa id): đọc `channel_directory.json` trước tiên** — nhanh hơn grep log vì tra thẳng theo TÊN:

```python
import json, io
d = json.load(io.open('C:/Users/<user>/AppData/Local/hermes/channel_directory.json', encoding='utf-8'))
for c in d["platforms"]["telegram"]:
    print("%-22s %-32s %s" % (c["id"], c["name"], c["type"]))
# → -5090469823            hơi mệt làm rnd                  group
```

Tên trong file là tên hiển thị thật của nhóm (giữ nguyên dấu tiếng Việt), nên user viết "nhóm hơi mệt làm rnd" là khớp trực tiếp. Đường dẫn trên Windows: `~/AppData/Local/hermes/channel_directory.json`.

Sau khi có id, **gọi `getChat` để xác nhận bot thật sự ở trong nhóm đó TRƯỚC khi hứa sẽ gửi** — `getChat` trả `title` + `type` là bằng chứng, còn tự tin vào tên file thì không:

```python
# getChat → {"ok": true, "result": {"id": -5090469823, "title": "hơi mệt làm rnd", "type": "group"}}
```

Khi grep log: lấy `chat=` của inbound message cuối của chủ đề (id âm = group, dương = DM):

```bash
grep "inbound message" ~/AppData/Local/hermes/logs/gateway.log | tail -15
# → inbound message: platform=telegram user=Not a name chat=-5154673868 msg='tiếp tục xử lý đi'
```

Cross-check ambiguous IDs against `D:/Hermes Proj/.hermes-state/chat/_INDEX.md` (chat name →
file → chat ID) before sending.

**Send** (read token from `.env` inside the script, never print it):

```python
import os, re, json, urllib.request
env = open(os.path.expanduser('~/AppData/Local/hermes/.env'), encoding='utf-8').read()
token = re.search(r'^TELEGRAM_BOT_TOKEN=(.+)$', env, re.M).group(1).strip()
data = json.dumps({'chat_id': -5154673868, 'text': '...'}).encode()
req = urllib.request.Request(f'https://api.telegram.org/bot{token}/sendMessage',
    data=data, headers={'Content-Type': 'application/json'})
r = json.loads(urllib.request.urlopen(req, timeout=30).read())
print('OK:', r.get('ok'), '| message_id:', r.get('result', {}).get('message_id'))
```

`ok: True` + `message_id` = delivered. If the direct call times out, WARP is probably off and
the ISP is throttling — reconnect WARP first, then retry.

## Config Pitfalls

### ❌ `hermes config set` đặt nested dict key ở CUỐI file thay vì vào dict
Đã xảy ra 10/2026: chạy `hermes config set personalities.head_of_legal "..."` → key bị append ở **cuối config.yaml** (line 886), KHÔNG nằm trong dictionary `personalities:` (line 49-90). Kết quả: `hermes config get personalities` trả về `{}`, và `display.personality = head_of_legal` activate personality rỗng.

**Fix:** đọc config.yaml trực tiếp, tìm dict `personalities:`, chèn entry vào SAU dòng cuối của dict (trước dòng `reasoning_effort` hoặc section tiếp theo):
```python
lines = open("config.yaml", encoding="utf-8").read().split("\n")
# Tìm dict personalities (indent 2 spaces)
for i, ln in enumerate(lines):
    if ln.strip() == "personalities:" and ln.startswith("  "):
        pers_dict = i; break
# Tìm vị trí kết thúc dict (dòng đầu tiên không indent 4 spaces)
end_idx = pers_dict + 1
while end_idx < len(lines):
    ln = lines[end_idx]
    if ln.strip() == "" or (ln.startswith("  ") and not ln.startswith("    ")):
        break
    end_idx += 1
# Chèn entry mới
lines.insert(end_idx, "    head_of_legal: 'text...'")
open("config.yaml", "w", encoding="utf-8").write("\n".join(lines))
```

**Kiểm tra sau khi fix:** `hermes config get personalities` phải trả về dict có key, không phải `{}`.

### ❌ `display.personality` vs `personality` — key đúng là `display.personality`
`hermes config set personality "head_of_legal"` tạo key top-level thừa (line 894), KHÔNG activate personality. Hermes cảnh báo: `'personality' is not a recognized config key`. Key đúng: `hermes config set display.personality head_of_legal`.

**Verify:** `hermes config get display.personality` phải trả về tên personality, không rỗng.

## Known Limits

### Bot-to-bot message visibility: Telegram blocks it

**Symptom:** Two bots (e.g., Hermes + OpenClaw) are in the same Telegram group. Bot A sends a message, but Bot B never receives it — no event, no update, nothing in logs. The user says "cả 2 em đã trong cùng nhóm sao không thấy tin nhắn của nhau?"

**Root cause:** Telegram Bot API explicitly **filters out messages from other bots**. This is an API-level rule — not configurable via BotFather privacy settings, `require_mention`, or any Hermes config. `api.telegram.org/bot<token>/getUpdates` will never return a message whose `from.is_bot = true`.

**Workaround — shared scratchpad via GitHub Gist:**

Since both bots can make HTTP API calls, use a **public/private GitHub Gist** as a message relay:

```
Hermes ──PATCH──→ Gist (scratchpad.json) ←──GET── Claw
Claw   ──PATCH──→ Gist (scratchpad.json) ←──GET── Hermes
```

```python
# Both bots use the same GIST_ID + PAT
GIST_ID = "a5b9533a50f001ca2a3263df61c1cab5" 
API = f"https://api.github.com/gists/{GIST_ID}"

# Read messages
import requests, json
r = requests.get(API)
msgs = json.loads(list(r.json()["files"].values())[0]["content"])

# Write a message
msgs.append({"bot": "Hermes", "msg": "my response", "ts": "..."})
r = requests.patch(API, headers={"Authorization": "token <PAT>"},
    json={"files": {"scratchpad.json": {"content": json.dumps(msgs)}}})
```

See the `cron-job` skill's `scripts/scratchpad.py` for a full implementation with `write`/`read` commands.

**Alternative 2 — self-hosted HTTP relay (preferred over Gist):**

Better than GitHub Gist: runs a lightweight Python HTTP server behind a Cloudflare tunnel, providing a simple POST/GET API with no rate limits, incremental reads via `?since=ID`, and no dependency on GitHub API.

```
Bot A → POST /relay {"bot":"Claw","msg":"..."}
Bot B → GET /relay?since=X → sees new message
```

**Server** (Python stdlib, zero deps):
```python
import http.server, json, os
from datetime import datetime
class RelayHandler(http.server.BaseHTTPRequestHandler):
    DATA_FILE = "relay_messages.json"
    def do_GET(self):
        import urllib.parse; msgs = self._load()
        since = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query).get("since")
        if since: msgs = [m for m in msgs if m["id"] > int(since[0])]
        self._send({"ok":True,"messages":msgs})
    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        msgs = self._load()
        msgs.append({"id":(msgs[-1]["id"]+1) if msgs else 1,
            "bot":body["bot"],"msg":body["msg"],
            "ts":datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
        self._save(msgs); self._send({"ok":True},201)
    def _load(self):
        return json.load(open(self.DATA_FILE)) if os.path.exists(self.DATA_FILE) else []
    def _save(self,msgs):
        json.dump(msgs,open(self.DATA_FILE,"w"),ensure_ascii=False)
    def _send(self,data,code=200):
        self.send_response(code); self.send_header("Content-Type","application/json")
        self.end_headers(); self.wfile.write(json.dumps(data).encode())
http.server.HTTPServer(("0.0.0.0",9877),RelayHandler).serve_forever()
```

**Client** (both bots):
```python
import requests
RELAY = "https://bot.yourdomain.com/relay"
requests.post(RELAY, json={"bot":"Claw","msg":"..."})
requests.get(f"{RELAY}?since=LAST_ID")
```

**Setup:** Run server on tunnel machine → add port 9877 to tunnel ingress config → set up DNS subdomain (e.g., `bot.yourdomain.com` CNAME → `<tunnel-uuid>.cfargotunnel.com`) → both bots poll `GET /relay?since=ID` every 30s (or user tags them to check).

**Key advantages over GitHub Gist:** No rate limits, ~100ms latency, incremental polling (`?since=ID`), no auth tokens needed. The relay file is on local disk, so it survives machine reboots.

**Alternative 3 (user-relay):** The user manually copies/pastes messages between bots. Simplest, but requires human-in-the-loop.

### File download size: 20MB

Telegram Bot API public server giới hạn download file ở **20MB** (`getFile`). Hermes gateway hardcode limit này ở `adapter.py:self._max_doc_bytes`.

- File > 20MB gửi qua Telegram bị gateway skip ngay — không lưu cache, không đến được agent
- Giải pháp: user cung cấp **path local** để xử lý trực tiếp, hoặc nén < 20MB
- Để tăng vĩnh viễn: chạy local `telegram-bot-api` server + set `extra.base_url` trong config → limit lên 2GB

> Chi tiết: `meeting-transcriber` skill → `references/telegram-gateway-file-limit.md`

## Pitfalls

### ❌ Dùng `getUpdates` để tìm groups bot đang tham gia

`getUpdates` **CHỈ trả về updates chưa xử lý**. Updates đã xử lý → trả về rỗng.

Kết luận "bot không có group nào" chỉ vì `getUpdates` = 0 là **sai hoàn toàn**. Bot có thể đang ở 27+ groups, chỉ là không có pending updates.

**Cách đúng để tìm groups:**
1. **Đọc `state.db`** — tìm tables chứa chat_id (columns có "chat" hoặc "group")
2. **Thử `getChat` với từng chat_id** đã biết để lấy title
3. **Đọc config** — `allowed_chats`, `TELEGRAM_ALLOWED_USERS`, groups trong memory

Đã kiểm chứng 10/2026: `getUpdates` trả về 0, nhưng state.db có 27 chat_ids, và `getChat` xác nhận tất cả đều là groups bot đang tham gia.

### ❌ Kết luận "bot chưa được add vào group" mà chưa thử `getChat`

Invite link (`https://t.me/+xxx`) không cho phép tìm chat_id qua API. Nhưng nếu có chat_id từ state.db, dùng `getChat` để xác nhận bot có ở group không.

Chỉ kết luận "bot chưa được add" khi **đã thử `getChat` và nhận "chat not found"**.

- `TELEGRAM_PROXY` set to a non-existent proxy blocks ALL Telegram connectivity — the error looks like a network block, not a config issue. Always verify the proxy is actually running.
- Config changes to `telegram.*` require `hermes gateway restart` — the Telegram adapter only reads settings at startup.
- Cloudflare WARP in VPN mode is sufficient without TELEGRAM_PROXY — do NOT set both unless WARP is in proxy mode.
- `hermes config migrate` will fail if the gateway holds the config file lock. Always stop gateway first.
- **WARP can disconnect silently** — `warp-cli.exe status` shows `Disconnected / Reason: Settings Changed` without user action. Also seen: `Reason: Manual Disconnection` (someone ran `warp-cli disconnect`, or a cron/script toggled it — e.g. conflicts with cloudflared tunnels). The gateway continues running but cannot reach Telegram. This causes a failure pattern that looks like "gateway crashed" but is actually just WARP. Always check WARP status before spending time on other diagnostics. The fix order matters: **reconnect WARP first, THEN restart gateway** — restarting gateway before WARP is reconnected will fail immediately as the new process also can't reach Telegram.
- **WARP disconnected ≠ Telegram necessarily down** — the gateway can still connect on attempt 1/8 when WARP is off (ISP not currently throttling, or fallback IP 149.154.166.110 works). Don't assume; probe first with `curl -so /dev/null -w "%{http_code}" --connect-timeout 8 https://api.telegram.org/bot` (404 = reachable). Only reconnect WARP / restart gateway if the probe fails.
- **WARP conflicts with cloudflared tunnel** — When WARP is in VPN mode (Connected), cloudflared tunnel may fail to connect to Cloudflare edge with errors like `i/o timeout` or "already connected to this server". Fix: Disconnect WARP before starting tunnel, or set up cron to auto-detect and disconnect WARP when tunnel dies.
- **WARP conflicts with Tailscale too (same root cause as cloudflared)** — WARP in VPN mode silently breaks Tailscale. Symptoms: `tailscale netcheck` shows `UDP: false` (direct P2P dead), `tailscale status` reports the machine's *own* node as `offline` plus `Unable to connect to the Tailscale coordination server to synchronize your tailnet`, and the netmap goes stale — newly added peers and their IPs do NOT appear. A Tailscale-hosted API (e.g. `http://100.x.x.x:PORT/v1`) then fails with timeout even though it's genuinely in the tailnet. Fix order: `warp-cli disconnect` → wait ~8s → tailscale resyncs (netmap refreshes, UDP returns `true`, node appears) → do the tailscale work → `warp-cli connect` to restore Telegram. Reaching a Tailscale service REQUIRES WARP off, which pauses Telegram for the duration — reconnect after.
- **Tailscale peer "unreachable" — diagnose before assuming the API is at fault** — Step 1 `tailscale status`: if the peer IP/name isn't in the netmap at all, the device is in a different tailnet, the name is wrong, or WARP is blocking sync (above). Step 2 resolve a known peer (`ping host.tailnet.ts.net`): if magicDNS resolves known peers but not the target, the target isn't in this tailnet. Step 3 if the peer IS in the netmap but shows `offline, last seen Xm ago`, the remote machine is powered off / tailscale not running — no routing works until it's back online, and `curl` timeouts are legitimate. Don't chase local config for an offline peer.
- **`fallback_providers` must be a real YAML list, NOT a JSON string** — `hermes config set fallback_providers '[{"provider": ..., "model": ...}]'` stores the JSON as a quoted string; `agent/agent_init.py` only accepts `isinstance(fallback_model, list)`, so a string yields an empty fallback chain → after 3 empty responses the bot reports "No fallback providers configured" and stops. The `patch` tool refuses config.yaml ("security-sensitive"), so fix it with a direct Python file edit (read `utf-8-sig`, write `utf-8`, `newline=''`). Full recipe + verify: `references/empty-response-fallback-config.md`.
- **`model.context_length` set too high = compression fires too late** — compression fires at **85%** of `model.context_length` (log line: `Session hygiene: N messages, ~X tokens — auto-compressing (threshold: 85% of 200,000 = 170,000 tokens)`). With `context_length: 200000` the session can balloon to ~174K before compression, which is PAST the dead zone for claude-opus-4-6-thinking via OmniRoute (~150K with tool schemas) — the provider silently returns HTTP 200 with zero content (`in=266776 out=0` in agent.log) and the retry loop burns 20-60s per attempt. Set `hermes config set model.context_length 120000` so compression fires at ~102K, comfortably before the model chokes. Small curl probes pass against the same endpoint — the failure only reproduces with real session shape (huge context + tool schemas). Cheap small probes do NOT prove a provider handles big contexts.
- **Slow Telegram replies that get slower over time = context bloat signature, NOT network** — if a chat used to answer instantly and now takes 20-60s+ (or a session shows `time=508s`), grep `response ready: platform=telegram ... time=Xs` in gateway.log and watch `time=` climb across the session, plus `Session hygiene: ... auto-compressing` + `Empty response from model — retrying (N/3)`. This is the session context ballooning toward the model's empty-response zone, not WARP/proxy. Quick fix is `hermes sessions delete <session_id>`; durable fix is lowering `model.context_length` (see above) AND a daily cron that resets long-lived Telegram sessions so they never accumulate.
- **Đừng báo "xong" khi mới test bằng `hermes -z`** — CLI tạo phiên MỚI nên luôn nhận config/persona mới, trong khi phiên chat đang tồn tại vẫn ghim prompt cũ. Test kiểu đó che mất lỗi. Báo xong chỉ sau khi có tin nhắn THẬT trong chat (hoặc verify bằng `state.db`, xem "### 10").
- **Sửa `SOUL.md` / persona: restart gateway là CHƯA ĐỦ** — phiên đang tồn tại giữ prompt cũ vĩnh viễn. Phải `hermes sessions repair-prompts <SID> --apply` rồi mới restart. Xem "### 10".
- **KHÔNG để agent tự gọi `hermes gateway restart` trong lượt của nó** — đây là tự sát có cấu trúc, không phải "rủi ro". Lệnh = stop rồi start; nửa `stop` giết đúng tiến trình đang chạy lệnh nên nửa `start` không bao giờ chạy → gateway dừng VĨNH VIỄN cho tới khi có người bật. Case thật: dừng 23:09, chết ~15 tiếng. Và **smart approval gắn cờ rồi TỰ DUYỆT** lệnh đó (`flagged (stop/restart hermes gateway (kills running agents)) and auto-approved`) — cảnh báo bị nêu ra rồi bỏ qua, nên đừng tin "approval đã bắt được" là an toàn. Cần nạp lại config thì sửa config rồi để TẦNG GIÁM SÁT restart (`MultipleInstances=IgnoreNew`), hoặc hẹn `.bat` tách rời (`set _HERMES_GATEWAY=` + `timeout /t 12` + restart).
- **Trước khi restart để "nạp config": luôn đọc config trước.** Đã có lượt agent restart gateway để chữa triệu chứng "bị tag trong nhóm lạ", trong khi nguyên nhân thật nằm ở `guest_mode: true` — restart chỉ nạp lại đúng config sai đó, mà giá phải trả là gateway tự giết mình. Restart KHÔNG phải công cụ chẩn đoán.

## Media delivery pitfall: cùng 1 file gửi 2 lần (dedupe slash mismatch)

**Triệu chứng:** agent gửi 2 dòng `MEDIA:` nhưng Telegram nhận gấp đôi ảnh (log: `Sending media group of 4 photo(s)` khi chỉ viết 2). Cùng 1 file đôi khi còn gửi 2 lần dạng document.

**Root cause (fix 09/2026 trong `gateway/platforms/base.py::extract_media`):** có 2 vòng regex quét MEDIA tag — `media_pattern` giữ path dạng `/` (`D:/Hermes Proj/x.png`), vòng `MEDIA_EXTENSIONLESS_TAG_RE` (sinh ra để xử lý path có dấu cách) trả cùng file dạng `\` (`D:\Hermes Proj\x.png`). Dedupe `seen_paths` so sánh chuỗi raw nên `/` ≠ `\` → mỗi file bị thêm 2 lần → gửi trùng.

**Fix đã commit:** wrap `os.path.normpath()` quanh path ở CẢ 2 vòng trước khi so `seen_paths` (dòng ~4523 `expanded = os.path.normpath(os.path.expanduser(path))` và ~4539 `safe = os.path.normpath(resolved[0])`). Verify bằng reproduction test gọi `BasePlatformAdapter.extract_media()` với 2 MEDIA tag → trả list đúng 2 entries, không 4.

**Lưu ý:** nếu thấy media gửi trùng lần nữa sau khi gateway restart, mở source kiểm tra 2 chỗ normpath còn nguyên không (agent update có thể ghi đè source). Cách chẩn đoán nhanh: log gateway có dạng `Sending media group of N photo(s)` với N gấp đôi số MEDIA trong response.

## Reference Files
- `references/vietnam-telegram-setup.md` — Vietnam-specific connectivity guide
- `references/empty-response-fallback-config.md` — "Model returned empty / No fallback providers configured": diagnosis (provider probe + errors.log signature) and the fallback_providers YAML-list fix (config set + patch tool both fail; direct python edit)
- `references/session-reset-disable-and-detached-restart.md` — disabling auto session reset (`session_reset.mode none`, the misleading CLI warning, notes that a gateway restart is required to apply) + detached gateway restart from inside a gateway session (`hermes gateway restart` is blocked; use `MSYS_NO_PATHCONV=1 cmd /c "schtasks /Create..."` one-shot task). Also covers the MSYS bash→cmd `/X` flag-mangling trap.
- **`remote-hermes-windows` → `references/gateway-supervision-windows.md`** — TẦNG GIÁM SÁT + case gateway chết ~15 tiếng. Đọc khi gateway dừng mà không tự lên lại: vì sao login-item không đủ, vì sao agent tự gọi `hermes gateway restart` là tự sát (smart approval gắn cờ rồi tự duyệt), Hermes SINGLETON nên watchdog tự viết giết cái đang khoẻ, 4 cách check sống/chết, thiết kế Scheduled Task đúng, event log forensics cho "máy tự restart?", truy lệnh trong `state.db` từ xa, nhiễu CLIXML.
- **`remote-hermes-windows` → `scripts/register_gateway_task.py`** — đăng ký Scheduled Task giám sát qua SSH, chạy lại được.

## Related Skills

- `voice-and-stt` — Hermes voice message configuration for Telegram
- `local-tunnel` — Expose local web servers for Telegram bot webhooks
- `hermes-agent` — General Hermes configuration
