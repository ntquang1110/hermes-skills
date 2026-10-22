# Windows remote Hermes — gotcha đã gặp thật

Kiểm chứng trên Windows 10 Pro, Hermes v0.21.5 (git install), qua SSH từ máy khác.

## 0. Cách lấy lỗi THẬT khi `gateway install` có vẻ treo

CLI hay nuốt traceback. Chạy lại qua PTY để đọc stack:

```python
ch = c.get_transport().open_session()
ch.get_pty(width=200, height=50)
ch.exec_command(f"powershell -NoProfile -EncodedCommand {enc}")
# đọc ch.recv() tới khi hết
```

Hoặc chạy detached + ghi log, rồi đọc log. Đừng kết luận "treo" khi chưa thấy traceback.

## 1. `hermes gateway install` chết ở schtasks

Triệu chứng:

```
RuntimeError: Windows gateway install failed: schtasks /Create failed (code 1):
ERROR: No mapping between account names and security IDs was done.
(17,8):UserId:
```

Nguyên nhân: chạy qua SSH, `schtasks` không resolve được account → SID khi UserId rỗng.
Đây là lỗi môi trường SSH, **không** phải lỗi user/password.

Cách chữa: bỏ scheduled task, dùng Startup folder.

```powershell
$startup = [Environment]::GetFolderPath('Startup')
# ghi Hermes_Gateway.vbs (utf-8, CRLF):
# Set sh = CreateObject("WScript.Shell")
# sh.Run """C:\Users\<u>\AppData\Local\hermes\bin\hermes.exe"" gateway run", 0, False
```

Verify: `hermes gateway status` → `✓ Windows login item installed ...` + `✓ Gateway process running (PID: N)`.
Lưu ý: status có thể báo "not running" sai ngay sau khi start; đối chiếu `Get-Process hermes`.

## 2. KHÔNG redirect stdout của gateway vào gateway.log

Hermes tự mở `logs\gateway.log` bằng `concurrent_log_handler`. Redirect thêm `>> gateway.log`
→ `PermissionError: [Errno 13] Permission denied: '...\logs\gateway.log'`, log handler chết.

Redirrect sang file khác: `%TEMP%\gw_out.log`.

## 3. Gateway phải sống sót khi SSH đóng

`Start-Process` có thể bị giết theo session. Dùng WMI để tách hẳn:

```powershell
$cmd = 'cmd.exe /c ""' + $h + '" gateway run 1> "' + $out + '" 2>&1"'
$r = ([wmiclass]"Win32_Process").Create($cmd)   # ReturnValue 0 = ok
```

Dòng log xác nhận chạy được:
`[Telegram] Connected to Telegram (polling mode)`

Restart sạch: `Get-Process hermes | Stop-Process -Force` → sleep 5 → tạo lại qua WMI.
(Bỏ qua cảnh báo `lifecycle_ledger: Previous gateway life exited UNCLEANLY` — do chính mình kill.)

## 4. `hermes config set` — key nào nhận, key nào không

NHẬN:

- `providers.<tên>.base_url` / `.api_key` / `.name` / `.discover_models`
- `model.provider` / `model.default` / `model.base_url`
- `platforms.<platform>.<key>`
- `display.personality`

TỪ CHỐI:

- `agent.personalities.<tên>` → `'agent.personalities.X' is not a recognized config key — nothing was written.`
- Truyền JSON cho cả dict cũng hỏng (in usage error của argparse).

→ Muốn thêm persona/xưng hô: nhúng vào **SOUL.md** (mục 6), đừng đánh vật với `personalities`.

Phụ: set `model.provider` sang provider khác sẽ tự xoá `model.base_url` cũ và in thông báo — set lại `base_url` sau đó.

## 5. Nhiều tên personality là BUILT-IN

`hermes_cli/personality.py` có sẵn: helpful, `concise`, technical, creative, teacher, kawaii,
catgirl, pirate, shakespeare, surfer, noir, uwu, philosopher, hype.

→ Chỉ cần `hermes config set display.personality concise`. KHÔNG khai báo lại trong `agent.personalities`.
Comment trong config xác nhận: entry trùng tên sẽ OVERRIDE built-in, không phải bắt buộc khai báo.

## 6. Ép persona / xưng hô cho một máy → sửa SOUL.md

`%LOCALAPPDATA%\hermes\SOUL.md` là tầng identity, luôn nạp mỗi phiên. Ghi UTF-8 **không BOM**:

```powershell
[System.IO.File]::WriteAllBytes($p, [Convert]::FromBase64String($b64))
```

- Verify: 3 byte đầu KHÔNG được là `239,187,191`.
- Đọc lại để kiểm UTF-8 thì đọc qua **base64** rồi giải mã ở phía mình. Console PowerShell sẽ
  hiện mojibake dù file hoàn toàn đúng — đừng "sửa" theo console.
- Test hiệu lực: `hermes -z "Chào, bạn là ai và gọi tôi là gì?"` rồi xem xưng hô.
- Backup trước khi đè: copy sang `SOUL.md.bak`.
- `security.protected_instruction_files` chặn agent ghi SOUL.md qua tool file của nó,
  nhưng ghi qua SFTP/SSH thì không bị chặn.

## 6b. Sửa SOUL.md KHÔNG đủ cho phiên ĐANG tồn tại — prompt bị ghim

Đây là bẫy đã làm hỏng một lần giao việc thật: ghi SOUL.md xong, `hermes -z` test
**đã** ra xưng hô mới, restart gateway, mà anh nhắn vào bot vẫn bị gọi "anh".

Nguyên nhân: Hermes **ghim system prompt theo từng session** để giữ prompt cache.
Mỗi dòng trong bảng `sessions` có `system_prompt_hash` trỏ tới bảng
`system_prompts`. Phiên tạo TRƯỚC lúc sửa SOUL.md giữ nguyên prompt cũ và không
bao giờ tự nạp lại. Session mới thì nhận bản mới.

Mốc thời gian là bằng chứng: SOUL.md ghi lúc 16:07, còn session Telegram tạo lúc
15:00 → hash cũ (không có chữ "sư phụ"/"đệ"), dù oneshot test lúc 16:09 ra hash
mới có đủ. **Thời điểm tạo session quan trọng hơn thời điểm restart.**

Cách chữa (giữ nguyên lịch sử chat, không phải xoá session):

```powershell
# 1. Xem session nào đang bị ghim
& $H sessions list --source telegram --limit 10

# 2. Xoá prompt đã lưu -> lượt sau tự dựng lại từ SOUL.md hiện tại
& $H sessions repair-prompts <session_id> --apply --json
#   -> {"cleared": ["<session_id>"], "findings":[{"reason":"targeted clear"}]}

# 3. Restart gateway để xoá luôn state trong RAM
```

`repair-prompts` gốc để sửa session hỏng do bug hygiene/compress, nhưng
truyền `session_id` là **destructive override**: nó clear cả prompt đang khoẻ.
`--apply` mới thực sự ghi, không có `--apply` thì chỉ báo cáo.

**Verify bằng DB, đừng tin cảm giác.** Tải `state.db` (+ `state.db-wal`) qua SFTP
rồi query bằng sqlite3 ở máy mình:

```python
con = sqlite3.connect("state.db")           # tải cả -wal nếu có
cur.execute("SELECT id, source, chat_id, system_prompt_hash, message_count FROM sessions")
cur.execute("SELECT hash, prompt FROM system_prompts")
# kiểm prompt chứa từ khoá persona không:
#   "sư phụ" in prompt  → bản mới
#   hash = NULL         → đã clear, lượt sau dựng lại
```

Đọc `system_prompts.prompt` và grep từ khoá persona là cách duy nhất chứng minh
được prompt nào đang có hiệu lực. Session key có dạng
`agent:main:<platform>:<chat_type>:<chat_id>`.

Cũng đọc luôn `messages` để thấy bot **thực sự** trả lời gì — đây là bằng chứng
mạnh hơn log `response ready: ... response=47 chars`.

Nếu vẫn chưa ăn: bảo anh gõ `/new` trong chat đó để mở phiên hoàn toàn mới (không
còn phụ thuộc việc clear prompt có đúng không).

Xoá hẳn (mất lịch sử) chỉ khi chat toàn tin test:
`& $H sessions delete <session_id> --yes`.

## 7. Đồng bộ skills sang máy đích

SFTP từng file, so `sftp.stat(path).st_size` để bỏ qua file đã giống. Bỏ `.archive`.
Tham chiếu: 341 skill / 1466 file ≈ 2 phút. `sftp.mkdir` cần tạo tuần tự từng cấp.
Verify: đếm `SKILL.md` trên máy đích (không đếm thư mục).

## 8. `.env` — ghi không BOM, giữ CRLF

```powershell
$sw = New-Object System.IO.StreamWriter($path, $false, [System.Text.UTF8Encoding]::new($false))
```

BOM làm Hermes đọc sai key đầu tiên. Bỏ dòng cũ cùng tên trước khi ghi lại.
Secret vào `.env`, settings vào `config.yaml`.

## 9. Telegram chập chờn là bình thường

```
[Telegram] Telegram polling degraded (heartbeat probe); gateway stays alive and will retry. Error: <TimeoutError>
```

Tự retry, tự hồi. Không phải lỗi cấu hình — đừng "sửa" gì.
Cũng bình thường: `platform 'teams'/'google_chat' has no valid toolsets configured` và
`Skill 'plan' ... collides with a core Hermes command`.

## Checklist nhanh sau khi cài xong

1. `hermes --version` — chạy được
2. `hermes config get display.personality` — đúng tên
3. `hermes -z "<câu hỏi test>"` — model trả lời (bắt buộc, đây mới là proof provider OK)
4. `hermes gateway status` — process running
5. Đếm `SKILL.md` trên máy đích
6. Log có `Connected to Telegram (polling mode)`
7. Kiểm `errors.log` không có `not connected to any AI provider` / 401
