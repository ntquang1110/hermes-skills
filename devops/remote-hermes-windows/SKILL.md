---
name: remote-hermes-windows
description: "Cài, sửa, debug Hermes trên máy Windows khác qua SSH."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [ssh, windows, remote, gateway, telegram, config, paramiko, troubleshooting]
    related_skills: [hermes-agent, hermes-telegram-gateway, hermes-model-provider-troubleshooting, docker-windows-deploy]
---

# Quản lý Hermes trên máy Windows từ xa qua SSH

Dùng khi anh có máy tính khác (văn phòng, máy đồng nghiệp, cloud VPS Windows)
chạy Hermes và cần cài, sửa config, chẩn đoán lỗi mà không ngồi trước máy.

Bao gồm cả máy của người khác dùng chung (đổi tên máy theo tên chủ máy, ví dụ
"hermes anh Quân"), vì đó là cách anh gọi và cũng là cách nên ghi vào memory.

## Kiểm tra SSH được không, trước tiên

```bash
python -c "
import socket
for p in (22, 2222, 3389, 5985, 5986):
    s=socket.socket(); s.settimeout(3)
    r=s.connect_ex(('host',p)); s.close()
    print(p, 'OPEN' if r==0 else 'closed')"
```

RDP (3389) mở không có nghĩa SSH mở. Nhiều máy Windows chỉ forward 3389 ra
ngoài. Thiếu SSH thì bắt anh bật ở PowerShell Admin:

```powershell
Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0
Start-Service sshd
Set-Service -Name sshd -StartupType 'Automatic'
netsh advfirewall firewall add rule name="OpenSSH" dir=in action=allow `
  protocol=TCP localport=22 profile=any
```

Ba lỗi phổ biến khi anh báo "vẫn không vào được":

| Triệu chứng | Nguyên nhân thật |
|-------------|-----------------|
| `Authentication failed` | sai mật khẩu, **không phải** sai port. Thử lại cẩn thận, hỏi lại anh |
| `Errno None] Unable to connect` | port đóng hoặc router chưa forward |
| Bật service xong vẫn không vào | router chỉ forward 3389, cần thêm rule port 22 |

### Port scan: đừng quét nhanh, nó nói dối

Quét song song nhiều luồng cho ra **âm tính giả**. Thực tế một session: quét
`1-1024` + ~25 port cao với **250 luồng / timeout 2s** trả về **0 port mở**. Quét lại
cùng host với 40 luồng / timeout 4s → `3389 OPEN`. Router/NAT drop khi bị dội SYN,
nên port đang mở vẫn báo closed.

Quy tắc: **≤ 40 luồng, timeout ≥ 4s**. Nếu kết quả là "không port nào mở" mà anh nói
máy đang bật, **quét lại chậm trước khi kết luận** — báo sai "không vào được" trong khi
RDP mở sờ sờ là lỗi nặng và làm mất cả một lượt của anh.

Errno phân biệt hai tình huống hoàn toàn khác nhau, đọc đúng rồi mới kết luận:

| `connect_ex` trả | Nghĩa | Cách sửa |
|---|---|---|
| `0` | mở | — |
| `10061` ECONNREFUSED | tới được máy, **không có gì lắng nghe** | bật service (sshd) trên máy đích |
| `10035` EWOULDBLOCK / hết timeout | **firewall/router DROP** — gói đi vào hư không | rule firewall trên host, hoặc forward port trên router |
| `10060` ETIMEDOUT | như trên, đường mạng đứt | kiểm tra IP public / DNS còn trỏ đúng |

**Cẩn thận: `10035` KHÔNG phân biệt được hai nguyên nhân.** Router không forward 22 và
Windows Firewall DROP 22 (mặc định Windows là drop, không phải RST) cho ra timeout y hệt
nhau. Đừng nói với anh "router chưa forward" rồi để anh đi sửa router trong khi thứ thiếu
chỉ là một rule firewall trên host.

Cách phân biệt thật:

- `10061` (refused) ở port 22 = có gì đó **đã trả lời** → đường tới máy thông, chỉ thiếu
  service. Bật sshd là xong.
- `10035` ở 22 mà port khác (`3389`) cho `0` = **hoặc** router chỉ forward RDP, **hoặc**
  host firewall drop 22. Kiểm từ TRONG máy (qua RDP/console): `Get-Service sshd`,
  `Get-NetFirewallRule -Name *ssh*`, `netstat -ano | findstr :22`. sshd chạy + rule có mà
  ngoài vẫn timeout thì lúc đó mới kết luận router.

Trong một session thực tế, port 80/443 trả `10061` (refused) còn 22 trả `10035` (timeout)
trên CÙNG host: đường tới máy có thông, nên nhiều khả năng thứ chặn 22 nằm ở phía host chứ
không phải router. Đừng kết luận từ một con errno.

WinRM (5985/5986) là đường dự phòng nhưng thường cũng bị chặn, và khi network
profile là Public thì `Set-WSManQuickConfig` báo lỗi firewall dù đã bật được
service. Không đừng mất thời gian, bảo anh forward port 22 trên router.

## Dựng script SSH một lần, dùng lại nhiều lần

Không gõ `python -c "..."` dài trong terminal — escape `C:\` và `\U` trong Python
sinh `SyntaxError: (unicode error) 'unicodeescape' codec` ngay lập tức. Viết
file `.py` rồi chạy:

```python
import paramiko, base64

HOST, USER, PASS = "host.example.com", "Admin", "..."

def connect():
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    c.connect(HOST, username=USER, password=PASS, timeout=20,
              allow_agent=False, look_for_keys=False)
    return c

def ps(c, script, timeout=300):
    """Chạy PowerShell từ xa. luôn dùng -EncodedCommand (UTF-16LE, base64)
    để khỏi escape quote."""
    enc = base64.b64encode(script.encode("utf-16-le")).decode()
    stdin, stdout, stderr = c.exec_command(
        f'powershell -NoProfile -EncodedCommand {enc}', timeout=timeout)
    return stdout.read().decode("utf-8", "replace").strip()
```

Ba điều không được bỏ:

- `allow_agent=False, look_for_keys=False` — nếu không, SSH tự thử key trong
  `~/.ssh` trước rồi fail chậm.
- `-EncodedCommand` UTF-16LE base64 — script có dấu nháy tiếng Việt, `$`, `` ` ``
  thì truyền thẳng sẽ vỡ.
- `.decode("utf-8", "replace")` — output Windows console không phải lúc nào
  cũng UTF-8, thiếu `replace` là crash.

### Dùng gạch chéo XUÔI cho mọi path trong script sinh ra

Đây là cách rẻ nhất để hết sạch một họ lỗi escape. Gạch chéo xuôi chạy được ở
PowerShell, cmd, và Python — không cần nhân đôi gì cả:

```python
# DỄ VỠ: chuỗi Python thường + đường dẫn Windows
H = 'C:\Users\NLQuan\AppData\Local\hermes\bin\hermes.exe'
#   -> SyntaxError: (unicode error) 'unicodeescape' codec
#      can't decode bytes in position 2-3: truncated \UXXXXXXXX escape

# CHẮC: gạch chéo xuôi, không escape gì
H = 'C:/Users/NLQuan/AppData/Local/hermes/bin/hermes.exe'
```

`\U`, `\N`, `\x` trong đường dẫn Windows đều là escape hợp lệ của Python nên
chuỗi vỡ ngay lúc parse, trước cả khi SSH được gọi. Đã dính thật khi viết script
trỏ tới `C:\Users\NLQuan\...` (`\U` → `\Users`) và `C:\Users\NTQUANG_DELL\...`
(`\NT`). Ba cách xử lý, chọn theo thứ tự: **gạch chéo xuôi** → chuỗi raw `r'...'`
→ nhân đôi `\\`. Chỉ đổi sang `\\` khi path cần nhúng vào .bat/.vbs, vì ở đó
phải là backslash thật.

Trong PowerShell, gọi file bằng `&` khi path có nháy:

```powershell
& "C:/Users/<user>/AppData/Local/hermes/bin/hermes.exe" gateway status
# thieu & -> ParserError: Unexpected token 'gateway'
```

Và trong script PowerShell gửi đi, tránh `$_` — dùng `$Error[0]` thay thế. Cả hai
viết cùng ý "lỗi vừa xảy ra", nhưng `$_` từng làm nội dung script bị cắt cụt khi
sinh file, còn `$Error[0]` đi qua sạch:

```powershell
try   { Invoke-WebRequest "https://api.telegram.org" -TimeoutSec 20 -UseBasicParsing }
catch { Write-Output ("LOI " + $Error[0].Exception.Message) }
```

### Ghi file trên máy Windows rồi chạy, thay vì nhồi một lệnh dài

Chuỗi lệnh quá dài qua `exec_command` bị cắt hoặc in ra rỗng. Khi script dài hơn
khoảng chục dòng, ghi nó thành file trên máy đích rồi gọi. Ghi bằng SFTP — ổn
định hơn heredoc và không bị shell của máy mình ăn mất ký tự:

```python
sftp = c.open_sftp()
with sftp.open('C:/Users/<user>/AppData/Local/hermes/start_gw.bat', 'w') as f:
    f.write(bat_text)
sftp.close()
```

Sau khi ghi, **đọc lại kiểm tra** (`sftp.open(path).read()`) trước khi chạy — file
cụt mà không biết thì lỗi hiện ra ở chỗ khác, rất khó lần.

## Đọc/ghi file: dùng SFTP, không dùng shell

```python
sftp = c.open_sftp()
raw = sftp.open(PATH, "r").read().decode("utf-8-sig")   # BOM-safe
...
with sftp.open(PATH, "w") as f:
    f.write(new_text)
```

`utf-8-sig` là bắt buộc: file do PowerShell `Set-Content -Encoding UTF8` ghi ra
có BOM, `decode("utf-8")` sẽ để lại `\ufeff` ở đầu và YAML parser có thể chết.

Script PowerShell dài chạy qua SSH cũng **in ra rỗng** khi quá dài (giới hạn
độ dài command line). Chuyển việc đó sang một file `.py` upload qua SFTP rồi
gọi bằng `python -c "import base64;exec(base64.b64decode('...').decode())"`.

## Sửa config.yaml từ xa: KHÔNG regex

Regex đa dòng ăn quá nhiều dòng rồi nuốt mất key khác. Ranh giới chỉ liên quan
khi thay khối cấu hình. Lần này regex `(?ms)^fallback_providers:\n(?:[ \t]+.*\n|\n)*?(?=^\S)`
xóa luôn khối kế tiếp, mất `platforms:`.

Giữ nguyên CRLF, xử lý theo dòng:

```python
lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")

out, i = [], 0
while i < len(lines):
    if lines[i] == "fallback_providers:":
        i += 1
        while i < len(lines) and (lines[i].startswith((" ", "\t")) or not lines[i].strip()):
            i += 1
        continue
    out.append(lines[i]); i += 1

block = ["fallback_providers:"]
for m in chain:
    block += ["  - provider: nvidia", f"    model: {m}"]

idx = out.index("platforms:")
new_text = "\r\n".join(out[:idx] + block + out[idx:])
if not new_text.endswith("\r\n"):
    new_text += "\r\n"
```

**Trước khi ghi:** `hermes config get <key>` để xác nhận key đích. **Sau khi ghi:**
`hermes config check` rồi `hermes fallback list` (hoặc lệnh tương ứng) để xác
nhận số entry. Nếu lệnh trả rỗng, script hỏng chứ không phải máy.

## Ghi .env không sinh BOM

`Set-Content -Encoding UTF8` trên Windows PowerShell 5.1 sinh BOM. Hermes đọc
`BYTEDANCE_ARK_API_KEY` thì giá trị có BOM ở đầu → **401 "API key format is
incorrect"** dù key đúng. Đây là nguyên nhân phổ biến nhất khi setup thất bại
âm thầm.

Dùng .NET writer không BOM:

```powershell
$sw = New-Object System.IO.StreamWriter($f, $false, [System.Text.UTF8Encoding]::new($false))
$sw.WriteLine("KEY=value")
$sw.Close()
```

Thêm biến mới thì lọc bỏ dòng cũ trước, không append trực tiếp:

```powershell
$lines = @(Get-Content $envFile | Where-Object { $_ -notmatch '^KEYNAME=' })
$lines += "KEYNAME=value"
Set-Content $envFile -Value $lines -Encoding UTF8
```

## Thêm biến môi trường cho tiến trình đang chạy

Đổi `.env` không tự nạp lại vào gateway đang chạy. Phải restart:

```powershell
& "C:\Users\<user>\hermes-agent\venv\Scripts\hermes.exe" gateway restart
```

## Plugin platform hay bị tắt

Sau khi bật `platforms.telegram.enabled: true` lần đầu, gateway vẫn có thể log:

```
Platform 'Telegram' requirements not met (Run `hermes setup` to install)
```

Đây là **plugin chưa được bật**, khác với thiếu thư viện. Bật tường minh rồi
restart:

```powershell
& "C:\Users\<user>\hermes-agent\venv\Scripts\hermes.exe" plugins enable platforms/telegram
& "..." gateway restart
```

Và xem log đúng chỗ, không đoán:

```
C:\Users\<user>\AppData\Local\hermes\logs\gateway.log   ← trạng thái platform
C:\Users\<user>\AppData\Local\hermes\logs\errors.log    ← lỗi model, lỗi API
C:\Users\<user>\AppData\Local\hermes\logs\agent.log     ← từng lượt gọi model
```

## Chạy gateway và auto-start

### Chạy nền sao cho sống qua SSH

`Start-Process` từ session SSH **không** đủ tin: tiến trình con có thể chết theo
session. Cách detached thật là WMI:

```powershell
$h = "$env:LOCALAPPDATA\hermes\bin\hermes.exe"
$out = "$env:TEMP\gw_out.log"
$cmd = 'cmd.exe /c ""' + $h + '" gateway run 1> "' + $out + '" 2>&1"'
$r = ([wmiclass]"Win32_Process").Create($cmd)
"ReturnValue: " + $r.ReturnValue + "  PID: " + $r.ProcessId
```

`ReturnValue: 0` là tạo được. Sau đó `sleep 45` rồi đọc log — gateway cần ~15s để
cài dependency platform lần đầu và ~12s để connect Telegram.

#### Gateway chết rồi không chịu sống lại: state file kẹt

Khi gateway bị kill cưỡng bức (SIGKILL / OOM / `taskkill`), file
`gateway_state.json` **không được ghi lại** và còn giữ `pid` đã chết +
`"gateway_state": "running"`. Hậu quả: `gateway run` từ chối khởi động vì nghĩ
một gateway khác đang chạy, và `gateway start` báo nhầm "already running".

```powershell
Remove-Item "$env:LOCALAPPDATA\hermes\gateway_state.json" -Force
```

Xóa file này **an toàn** — nó chỉ là trạng thái, Hermes ghi lại từ đầu khi
startup. Xóa xong mới khởi động được.

### `gateway_state.json` là nguồn chẩn đoán, không chỉ là lock

`hermes gateway status` chỉ in hai dòng. File state giữ nhiều hơn:

```json
"platforms": {
  "telegram": {
    "state": "retrying",
    "error_message": "telegram connect timed out after 30s",
    "needs_attention": true,
    "retrying_since": "2026-10-09T10:05:32"    ← CHẶT LẠI Ở ĐÂY
  }
}
```

`retrying_since` là chìa khóa. Một gateway báo "running" bình thường vẫn có thể
đã chập chờn **ngày nào** — và cái chết cuối cùng chỉ là đỉnh của chuỗi đó.
Đã dính thật: máy anh Quân báo gateway chết lúc 11:31, nhưng `retrying_since`
lại là **09/10**, nghĩa là Telegram đã fail 3 ngày trước khi tiến trình bị kill.
Đọc `retrying_since` trước, rồi mới đi tìm nguyên nhân cái chết.

### Phân biệt gateway bị kill cưỡng bức với gateway thoát sạch

```powershell
Get-Content "$env:LOCALAPPDATA\hermes\logs\gateway-exit-diag.log" -Tail 5
```

| Dòng | Nghĩa |
|---|---|
| `tag: gateway.exit_clean` | thoát bình thường — không có gì phải làm |
| `tag: asyncio.run.returned` + `success: true` | cũng sạch |
| `tag: gateway.previous_unclean_exit` | **bị kill** — không có exit path nào chạy |

Log của `gateway.lifecycle_ledger` trong `errors.log` còn nói rõ nghi vấn:

```
exited UNCLEANLY (no exit path ran — SIGKILL / OOM / VM death, or a process kill
issued by the agent or one of its descendants, e.g. a pkill/taskkill of the host
interpreter image)  last_mem=None  suspected_oom=False
```

`suspected_oom=False` + `last_mem=None` = không phải hết RAM. Thường là tiến trình
cha (SSH session, service manager, hoặc chính agent) kill con.

### Khởi động tách phiên: schtasks với credential tường minh

`Start-Process` và WMI từ session SSH đều **có thể** chết theo session — không
đảm bảo được, tùy cách SSH server xử lý con process. Cách chắc chắn nhất đã
verify chạy được và sống qua cả một phiên SSH mới:

```powershell
schtasks /Create /TN HermesGW /TR "C:/Users/<user>/AppData/Local/hermes/start_gw.bat" `
         /SC ONCE /ST 23:59 /RU <user> /RP <password> /RL LIMITED /F
schtasks /Run /TN HermesGW
```

Tiến trình ra ở **session Services (session 0)**, sống độc lập với SSH. Kiểm
chứng bằng `tasklist` — phải thấy `python.exe` với session name `Services`.

⚠️ **Task phải là một lần.** Dùng `/SC ONCE` rồi **xóa task ngay sau khi chạy**,
không thì tới giờ nó chạy lại và sinh gateway thứ hai. Ví dụ chạy file .bat:

```bat
@echo off
set HM=C:\Users\<user>\AppData\Local\hermes
del "%HM%\gateway_state.json" 2>nul
start "" "%HM%\bin\hermes.exe" gateway run
```

Giữ file `.bat` này lại trong thư mục Hermes — đó là công cụ phục hồi, anh chạy
một lần là gateway lên.

### ⚠️ Khởi động được ≠ tự sống lại. Phải có TẦNG GIÁM SÁT

`/SC ONCE` + Startup VBS chỉ lo **khởi động**. Khi gateway **dừng giữa chừng** thì
không có gì bật lại — login item chỉ chạy lúc đăng nhập. Đã trả giá thật 13/10/2026
trên `lqremote`: gateway dừng 23:09, nằm chết **~15 tiếng** tới khi bật tay.

Nguyên nhân cái chết còn đáng nhớ hơn: **agent tự gọi `hermes gateway restart`** để
nạp lại config Telegram. Lệnh `restart` = stop rồi start, mà nửa `stop` giết đúng
tiến trình đang chạy lệnh → **nửa `start` không bao giờ chạy**. Tệ hơn, smart
approval **gắn cờ rồi tự duyệt**:

```
"approval": "Command was flagged (stop/restart hermes gateway (kills running
             agents)) and auto-approved by smart approval, then interrupted."
```

Nó nhận đúng nguy hiểm và vẫn cho qua. **Đừng để agent tự restart gateway trong
lượt của nó** — sửa config rồi để tầng giám sát bật lại.

#### Hermes gateway là SINGLETON — bật thêm là GIẾT cái đang sống

Bẫy nguy hiểm nhất, phá mọi watchdog tự viết. Mỗi instance mới giết instance trước;
`gateway-exit-diag.log` ghi lại thành chuỗi:

```
{"tag":"gateway.previous_unclean_exit","pid":15108,"prior_pid":14428, ...}
{"tag":"gateway.previous_unclean_exit","pid":10816,"prior_pid":15108, ...}
```

Chuỗi pids nối tiếp = vòng lặp: check báo "chết" SAI → bật mới → giết cái khoẻ.
Đã dính đúng vậy với watchdog tự viết (`pid=10452,8336` rồi `pid=9944,14428`).

Ba cách check sống/chết **SAI**, gặp hết trong một session:

| Cách | Vì sao sai |
|---|---|
| `Win32_Process` lọc `CommandLine -like "*gateway run*"` | **Âm tính giả** với tiến trình session 0 |
| mtime `gateway_state.json` làm grace period | File được ghi **liên tục** khi sống → không bao giờ hết hạn chờ |
| Tin `gateway_state.json` | File kẹt: ghi `running` + pid **đã chết** |
| `hermes gateway status` | Báo nhầm PID (từng trả `conhost.exe`) |

Cách đáng tin duy nhất: **`Get-Process python` lọc `SessionId -eq 0`** — gateway là
`python.exe` duy nhất ở session 0, `hermes serve` ở session 1.

#### Thiết kế ĐÚNG: để Task Scheduler sở hữu tiến trình

Đừng tự viết logic "thấy chết thì start". Dùng `MultipleInstances=IgnoreNew` để OS
chặn trùng. Action của task CHÍNH LÀ `hermes.exe gateway run` (không bọc `.bat`,
không `start ""` — bọc là Task Scheduler mù, không biết tiến trình sống hay chết).

Dùng `scripts/register_gateway_task.py` (đăng ký + verify qua SSH, chạy lại được):

```bash
python scripts/register_gateway_task.py --host <host> --user <user> --pass '<pass>'
```

Cấu hình chốt và lý do từng tham số:

| Tham số | Bắt buộc vì |
|---|---|
| `MultipleInstances IgnoreNew` | **Chốt chặn trùng.** Thay thế hoàn toàn watchdog tự viết |
| `ExecutionTimeLimit = 0` | Mặc định **3 ngày** — không tắt là Task Scheduler kill gateway sau 72h |
| `RestartCount 999` / `RestartInterval 1m` | Tự bật lại khi tiến trình chết |
| Trigger `AtLogOn` + `AtStartup` | Sống qua reboot, kể cả không ai đăng nhập |
| Trigger lặp mỗi 5 phút | Lưới cho ca **thoát sạch** (exit 0) — `RestartOnFailure` KHÔNG bắt được |
| `-User` + `-Password` (⇒ `LogonType: Password`) | Chạy được khi không đăng nhập. `S4U` có thể mất quyền ra mạng → Telegram không nối |

**Phải tắt VBS trong Startup** sau khi tạo task, không thì mỗi lần đăng nhập cả hai
cùng bắn (Hermes giết một cái, churn ~30s). Đổi tên, đừng xóa:

```powershell
Rename-Item (Join-Path ([Environment]::GetFolderPath('Startup')) 'Hermes_Gateway.vbs') `
            'Hermes_Gateway.vbs.disabled' -Force
```

Đã verify chạy thật: `Start-ScheduledTask` thêm 3 lần khi đang chạy → **cùng pid,
không chồng**; kill pid → tự bật lại; ca thật ngoài đời agent `taskkill` lúc
**16:18:30** → pid mới lúc **16:18:51**, tức **21 giây**.

Chi tiết đầy đủ (case 15 tiếng, 4 cách check, event log forensics, truy `state.db`,
nhiễu CLIXML, `guest_mode`):
`references/gateway-supervision-windows.md`. **Đọc trước khi sửa auto-start.**

Lưu ý `/RP` bắt buộc phải có mật khẩu thật. `hermes gateway install` từng fail
với `No mapping between account names and security IDs was done` vì nó để `/RU`
rỗng (không map được SID qua SSH). Truyền tường minh `/RU` + `/RP` thì chạy ngay
— nên mục trên nói "ĐỪNG đánh vật với schtasks" chỉ đúng khi để Hermes tự sinh
lệnh, không đúng khi chính mình tạo task.

### Hermes CHẶN restart từ chính nó — và cách gỡ

Khi một tiến trình do gateway sinh ra (terminal của agent, cron job, script chạy
trong phiên Hermes) gọi `hermes gateway restart`, nó in:

```
Refusing to restart the gateway from inside the gateway process.
```

Kiểm tra nằm ở `hermes_cli/gateway.py`:

```python
if os.getenv("_HERMES_GATEWAY") == "1":
    ...
```

Tiến trình con **kế thừa biến này** từ gateway cha, nên `Start-Process` hay bat
con đều bị chặn. Gỡ bằng cách xóa biến trước khi gọi:

```bat
@echo off
set _HERMES_GATEWAY=
hermes gateway restart
```

Muốn hẹn giờ restart để tin nhắn cuối kịp gửi đi trước khi gateway ngắt (vì
agent đang trả lời nằm trong chính gateway đó), viết file `.bat` rồi tách tiến
trình:

```powershell
# trong .bat: set _HERMES_GATEWAY=   rồi timeout /t 12  rồi hermes gateway restart
Start-Process -FilePath "C:\...\restart_gateway.bat" -WindowStyle Hidden
```

Delay 12 giây đủ để lượt trả lời hiện tại hoàn tất và giao đi trước khi tiến
trình bị kill. Không có delay thì tin nhắn cuối của agent mất tiêu.

## ĐỪNG redirect stdout vào `gateway.log`

Hermes tự mở `logs\gateway.log`. Nếu shell cũng redirect vào chính file đó, hai
tiến trình tranh nhau và Hermes chết:

```
PermissionError: [Errno 13] Permission denied:
  'C:\Users\<user>\AppData\Local\hermes\logs\gateway.log'
```

Log stdout của shell phải đi file KHÁC (`$env:TEMP\gw_out.log`). Log thật của
Hermes đọc ở `logs\gateway.log`.

### `gateway install` có thể chết ở schtasks

Trên Windows qua SSH, `hermes gateway install --force --start-now --start-on-login`
có thể trả:

```
RuntimeError: Windows gateway install failed: schtasks /Create failed (code 1):
ERROR: No mapping between account names and security IDs was done.
(17,8):UserId:
```

WMI/SSH không map được account sang SID nên `/RU` ra rỗng. **Đừng đánh vật với
schtasks.** Dùng Startup folder — đúng cơ chế mà `hermes gateway start` vẫn dùng:

```powershell
Set-Content -Path (Join-Path ([Environment]::GetFolderPath('Startup')) 'Hermes_Gateway.vbs') `
  -Encoding ASCII -Value @(
    'Set sh = CreateObject("WScript.Shell")',
    'sh.Run """C:\Users\<user>\AppData\Local\hermes\bin\hermes.exe"" gateway run", 0, False'
  )
```

Xác nhận `gateway status` in ra cả hai dòng (login item đã cài + process đang
chạy). Đó là bằng chứng auto-start thật, không phải suy đoán.

⚠️ **Nhưng VBS Startup là mức TỐI THIỂU, không phải đích.** Nó chỉ chạy lúc đăng
nhập: gateway dừng giữa chừng thì nằm chết tới khi có người đăng nhập lại (đã trả
giá ~15 tiếng, xem mục "Phải có TẦNG GIÁM SÁT" phía trên). VBS là đường lùi khi
`schtasks` hỏng; khi `schtasks` chạy được thì dựng Scheduled Task có
`MultipleInstances=IgnoreNew` — xem `scripts/register_gateway_task.py`.

**NHƯNG ĐỪNG tin PID mà `gateway status` in ra — kiểm tra nó là tiến trình gì.**
Đã dính thật: `hermes gateway start` và `status` đều báo
`✓ Gateway already running (PID: 14800)`, nhưng `tasklist /FI "PID eq 14800"`
cho ra **`conhost.exe`** (console host rác còn sót) trong session Services.
Lệnh đó đọc một lock/pid file không được dọn, không đọc tiến trình thật.

```powershell
tasklist /FI "PID eq <N>"      # phải ra python.exe, nếu ra conhost.exe = false positive
```

Chỉ tin `gateway status` khi PID đó là `python.exe`. Và luôn đọc luôn
`gateway_state.json` (mục dưới) để đối chiếu `pid` — file đó là nguồn thật.

## Cài Hermes trên Windows từ đầu (máy chưa có gì)

Bootstrap chính thức cho Windows là **`install.ps1`** (đã verify HTTP 200):

```powershell
$s = Invoke-RestMethod -Uri "https://hermes-agent.nousresearch.com/install.ps1" -UseBasicParsing
& ([scriptblock]::Create($s)) -NonInteractive -SkipBrowser -SkipComputerUse
```

- `install.sh` là bản unix, **`install.cmd` không tồn tại** (404) — đừng đi tìm.
- `-NonInteractive` bỏ mọi stage cần hỏi; `-SkipBrowser` / `-SkipComputerUse` bỏ
  agent-browser + Chromium và cua-driver (máy đích chỉ chạy gateway thì không cần,
  tiết kiệm vài trăm MB). Cả hai được **ghi nhớ**, `hermes update` sau này cũng
  không cài lại cho tới khi `hermes pm install agent-browser`.
- `-ShowResolvedPaths` in ra JSON các path nó sẽ dùng rồi thoát, không sửa gì —
  câu hỏi đầu tiên khi installer báo "path không tồn tại".
- `-Manifest` in danh sách stage dạng JSON; `-Stage NAME` chạy một stage lẻ.
- Installer mất 10–20 phút. Chạy qua `exec_command` phải đặt timeout ≥ 2400s, và
  bọc `$ProgressPreference="SilentlyContinue"` ở đầu không thì `Invoke-RestMethod`
  chậm kinh khủng trên PS 5.1.

Cài xong, **launcher chuẩn luôn là**:

```
%LOCALAPPDATA%\hermes\bin\hermes.exe
```

Dùng đường này trong mọi script. Nó ổn định qua cả hai kiểu cài. Kiểm tra:

```powershell
& "$env:LOCALAPPDATA\hermes\bin\hermes.exe" --version
```

in ra version **kèm `Install method:` và `Install directory:`** — cách nhanh nhất
để biết máy đó cài kiểu gì:

| `Install method` | venv nằm ở đâu |
|---|---|
| `git` (bootstrap) | `%LOCALAPPDATA%\hermes\installs\<hash>\environments\<hash>\venv\` |
| pip/wheel | `%LOCALAPPDATA%\hermes\hermes-agent\venv\` |

Bản `git` **không có** `hermes-agent\venv\Scripts\hermes.exe` — `venv` dưới
`hermes-agent\` trả `False`. Đừng hardcode đường venv đó; gọi `bin\hermes.exe`
rồi để nó tự tìm interpreter. Vài đoạn dưới đây còn ví dụ cũ dạng
`hermes-agent\venv\Scripts\hermes.exe`, cứ thay bằng `bin\hermes.exe`.

`Add-WindowsCapability` cho OpenSSH có thể fail khi Windows Update service tắt hoặc
máy không ra internet. Ba tầng dự phòng theo thứ tự: capability → `winget install
--id Microsoft.OpenSSH.Beta` → tải zip `OpenSSH-Win64` từ GitHub release rồi chạy
`install-sshd.ps1`. Xem `templates/open-ssh-remote.ps1`.

## Vị trí cài đặt trên máy đích

```
C:\Users\<user>\hermes-agent\                 ← mã nguồn + venv, KHÔNG có data
C:\Users\<user>\hermes-agent\venv\Scripts\hermes.exe
C:\Users\<user>\AppData\Local\hermes\         ← toàn bộ data
    config.yaml  .env  state.db  skills/  plugins/  sessions/  logs/
```

Trả lời câu hỏi "folder chứa Hermes ở đâu" phải nói cả hai, và nói rõ cái nào
chứa gì.

## Chẩn đoán model không trả lời

Theo đúng thứ tự, đọc file log thật thay vì suy đoán:

1. `hermes config get model.default` / `.provider` / `.base_url`
2. Gọi thẳng API bằng PowerShell `Invoke-RestMethod` với key trong `.env`.
   Nếu gọi thẳng OK mà Hermes fail → vấn đề ở cách Hermes đọc key (BOM, sai
   tên biến, `key_env` không được hỗ trợ cho provider đó).
3. `errors.log` — tìm `summary=` hoặc `Error code:`.
4. Phân biệt `provider=custom` với provider native.

`key_env` trong `custom_providers` đã trả 401 với key định dạng ByteDance, trong
khi `api_key` trực tiếp chạy được. Gặp "API key format is incorrect" thì đổi
sang `api_key`, đừng đổi key.

Và luôn **gọi thẳng endpoint bằng `curl`/`Invoke-RestMethod` trước khi set vào
Hermes**. Một lần gọi 20 giây phân biệt được ba thứ rất khác nhau: key sai,
model không được endpoint hỗ trợ, hay Hermes đọc key sai. Chi tiết endpoint
BytePlus Ark (model nào được, model nào bị `UnsupportedModel`) ở
`references/byteplus-ark-coding-endpoint.md`.

### ⚠️ Probe THIẾU User-Agent browser = kết quả 403 GIẢ (VERIFIED 2026-10-16)

Đây là cái bẫy phá hỏng đúng bước "gọi thẳng endpoint" ở trên. `urllib` trần hoặc
`curl` không có `-A` bị Cloudflare chặn theo chữ ký browser và trả `403`, khiến bạn kết
luận provider CHẾT trong khi nó đang khoẻ:

```
deepseek/deepseek-v4-flash    -> HTTP 403  error code: 1010
deepseek/deepseek-v4.1-flash  -> HTTP 403  error code: 1010
# them User-Agent browser -> 200 OK ca hai
```

Hai chữ ký CF, cách sửa giống nhau (gửi UA browser thật):

| Dấu hiệu | Nghĩa |
|---|---|
| `403` + `Server: cloudflare` + `CF-RAY` + body `"Your request was blocked."` | UA `/OpenAI/` bị managed-rule chặn |
| `403` + `error code: 1010`, body rỗng | CF chặn theo chữ ký browser — thiếu/sai UA |

```python
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")
req = urllib.request.Request(url, data=json.dumps(payload).encode(), method="POST")
req.add_header("Content-Type", "application/json")
req.add_header("Authorization", "Bearer %s" % key)
req.add_header("User-Agent", UA)      # <- THIEU DONG NAY = 403/1010 GIA
```

Hai bẫy phụ hay đi kèm, cả hai đều làm bạn đổ oan cho provider:

- **GET vào `/chat/completions` trả `404 ... is not a registered API route`** — endpoint
  **phải POST**. Chữ `GET` trong trường `cause` là mấu chốt. Đọc `cause` trước khi kết luận.
- **Kết luận từ một request duy nhất.** `GET /models` (có UA) trả về toàn bộ model kèm
  `context_length` + `supported_endpoints` — nguồn sự thật để phân biệt "model không tồn
  tại" với "model có nhưng gọi sai endpoint". VERIFIED 2026-10-16:
  `api.commandcode.ai/provider/v1/models` → 92 model; model họ Claude chỉ phục vụ ở
  `/messages` (nhận `400 Model "X" is not supported on this endpoint` khi gọi
  `/chat/completions`), và một số cần gói Pro (`403 MODEL_NOT_IN_PLAN`).

**Quy tắc:** trước khi nói "provider chết", kiểm lại probe đã gửi UA browser chưa. Không
có UA thì kết quả 403 vô nghĩa. Chi tiết bộ chẩn đoán đầy đủ (đếm job ghim provider, đo
tỉ lệ lỗi thật, tách nhiễu log) ở skill `cron-job` →
`references/provider-failure-triage.md`.

## Gửi tin nhắn thử bằng CLI

```powershell
& "...\hermes.exe" send --to telegram:<chat_id> "nội dung"
```

Đúng cú pháp là `send --to`, **không phải** `send telegram --chat-id`. Cú sai
không in lỗi, chỉ không gửi gì, dễ tưởng là hỏng.

Xem các target đã biết:

```powershell
& "...\hermes.exe" send --list telegram
& "...\hermes.exe" send --list
```

Lưu ý `getUpdates` của Telegram trả 409 khi gateway đang poll. Muốn đọc hàng
đợi thì `gateway stop` trước, đọc xong `gateway restart`. Không tắt cả gateway
để tra cứu rồi quên bật lại.

## Skill và personality trên máy đích

Skills là thư mục, copy thẳng được:
`skills/<category>/<tên>/SKILL.md`. Personality thì nằm trong `config.yaml`.

### Personality: `concise` và các bản built-in

ĐỪNG định nghĩa personality `concise` — nó là **built-in** của Hermes. Danh sách
nằm ở `hermes-agent/hermes_cli/personality.py`:

`helpful, concise, technical, creative, teacher, kawaii, catgirl, pirate,
shakespeare, surfer, noir, uwu, philosopher, hype`

⚠️ **`display.personality` CHỈ ĐỂ HIỂN THỊ — nó KHÔNG điều khiển hành vi.** Verify
bằng source 13/10/2026: cả `agent/system_prompt.py` lẫn `agent/prompt_builder.py`
đều KHÔNG đọc key này. Nó xuất hiện đúng một chỗ trong toàn bộ repo, một lệnh `print()`:

```
hermes_cli/config.py:4337:  print(f"  Personality:  {display.get('personality') or 'none'}")
```

Nên `display.personality: head_of_legal` chỉ in ra chữ `head_of_legal` khi anh chạy
`hermes config`; agent vẫn cư xử theo `SOUL.md`. Set key này rồi tưởng đã đổi tính
cách là hiểu sai — nguy hiểm hơn, nó **che mất việc `SOUL.md` mới là thứ cần sửa**.
Dọn cho khỏi hiểu nhầm: `hermes config unset display.personality`.

Liệt kê built-in có sẵn trước khi tự viết cái mới:

```powershell
Get-ChildItem "$env:LOCALAPPDATA\hermes\hermes-agent\hermes_cli\personality.py" |
  Select-String -Pattern '^\s*"[a-z_]+"\s*:' | ForEach-Object { $_.Line.Trim() }
```

### Ép persona riêng (xưng hô, giọng điệu): dùng SOUL.md

`agent.personalities.<tên>` không set được qua CLI (xem mục dưới), nên đường đúng
cho persona riêng là `%LOCALAPPDATA%\hermes\SOUL.md` — tầng identity, luôn nạp.
Ghi UTF-8 **không BOM** qua SFTP hoặc `[System.IO.File]::WriteAllBytes`, backup
bản cũ sang `SOUL.md.bak` trước.

#### Nội dung SOUL.md: khối quy tắc ứng xử là phần BẮT BUỘC

Anh yêu cầu tường minh, đây là chuẩn cố định. SOUL.md cho máy nào cũng phải có mục
`## Cách nói (bắt buộc, mọi lúc)`, chia 4 nhóm con: `### Giọng`, `### Cấm`,
`### Bắt buộc`, `### Cách làm việc` — 16 điều.

⚠️ **Đừng chép bản 11 điều cũ.** Bản này đã bị anh **đảo ngược ba điều ngay trong
cùng buổi 13/10/2026**. Bản 16 điều đầy đủ nằm ở
`references/hermes-prompt-assembly.md` — đọc file đó, đừng dựng lại từ trí nhớ.
Ba chỗ đảo, ghi lại vì bản cũ là bẫy:

| Bản cũ (SAI, đã bỏ) | Bản chốt |
|---|---|
| "Cấm hỏi lại. Chỉ hỏi khi thiếu thông tin…" | **"Luôn phải có output"** — *"Không phải là không hỏi là kết quả, luôn luôn phải có kết quả để mình confirm là hiểu được output mà người dùng muốn là gì"*. Hỏi mà không kèm output là VI PHẠM, không phải thận trọng |
| "Không đề xuất thêm việc ngoài yêu cầu" | **"Phải đề xuất thêm khi nó làm output tốt hơn"** — *"nếu như việc đề xuất thêm mà tạo ra hiệu quả về output thì vẫn phải cần đề xuất"*. Cấm đề xuất chung chung, nhưng đề xuất CÓ ĐÍCH là bắt buộc |
| "Xong việc thì dừng" | bỏ hẳn |

Không còn mục `## Writing rules for this character` riêng — nội dung gộp vào
`### Giọng` và `### Cách làm việc`. Vẫn phải giữ câu chống tự khen:
`Critique fast, demand better when not. Never praise, never congratulate.`
(bản gốc `praise when earned` mâu thuẫn trực tiếp với quy tắc "cấm khen").

Kiểm bằng cách đọc lại file (`grep -n -A 20 "^## Cách nói"` + `wc -l`), không chỉ
tin thao tác ghi thành công.

⚠️ **`display.personality` KHÔNG nạp vào prompt — xem mục "Personality" phía trên.**
Đừng set rồi tưởng đã đổi tính cách.

**Nhưng sửa SOUL.md KHÔNG tự áp vào phiên đang tồn tại.** Hermes ghim system
prompt theo từng session (`sessions.system_prompt_hash` → bảng `system_prompts`)
để giữ prompt cache. Phiên tạo trước lúc sửa giữ prompt cũ vĩnh viễn, dù có
restart gateway. **Thời điểm tạo session quan trọng hơn thời điểm restart.**

Đã dính thật: ghi SOUL.md 16:07, `hermes -z` test ra xưng hô mới, restart gateway,
mà nhắn vào bot vẫn bị gọi "anh" — vì phiên Telegram tạo lúc 15:00.

Chữa, giữ nguyên lịch sử chat:

```powershell
& $H sessions list --source telegram --limit 10
& $H sessions repair-prompts <session_id> --apply --json   # clear prompt đã ghim
# rồi restart gateway để xoá state trong RAM
```

`repair-prompts` + `session_id` là **destructive override** — clear cả prompt đang
khoẻ. Không có `--apply` thì chỉ báo cáo, không ghi.

**Verify bằng DB, không bằng cảm giác:** tải `state.db` (+`state.db-wal`) qua SFTP,
query `sessions` và `system_prompts`, `grep` từ khoá persona trong
`system_prompts.prompt`, và đọc bảng `messages` để thấy bot TRẢ LỜI gì. Log
`response ready: ... response=47 chars` không cho biết nội dung.

Đường cùng: bảo anh gõ `/new` trong chat đó. Xem
`references/windows-remote-gotchas.md` mục 6b.

### `agent.personalities.<tên>` — CLI TỪ CHỐI, không phải "cảnh báo vô hại"

Bản cũ của skill này nói cảnh báo đó vô hại và Hermes vẫn ghi đúng chỗ. **Sai.**
Thực tế Hermes in:

```
✗ 'agent.personalities.concise' is not a recognized config key — nothing was written.
```

và đọc lại YAML thấy `personalities: {}` **vẫn rỗng**. Chữ "nothing was written"
là thật. Set cả dict cũng hỏng — `config set agent.personalities '{"x":"..."}'`
làm argparse nuốt nhầm và in `usage: hermes [-h] ...`.

Hai đường còn lại khi cần personality không có sẵn:

- Sửa `config.yaml` theo dòng (mục "KHÔNG regex" ở trên): thay `  personalities: {}`
  bằng block dict đúng indent 2 space, giữ CRLF, ghi không BOM.
- Hoặc bù bằng `SOUL.md`. **Quên `display.personality` đi — nó không nạp vào prompt**
  (xem mục "Personality" phía trên), nên nó không phải đường nào cả.

### Nhưng `providers.<tên>.<key>` thì CLI NHẬN bình thường

Bất đối xứng này đáng nhớ — khóa lồng dưới `providers:` set được:

```powershell
& "$H" config set providers.ark.base_url "https://ark.ap-southeast.bytepluses.com/api/coding/v3"
& "$H" config set providers.ark.name "BytePlus Ark"
& "$H" config set providers.ark.api_key "<key>"
& "$H" config set providers.ark.discover_models true
```

Ghi đúng vào `providers:` ở cuối `config.yaml`. Nên gặp "not a recognized config
key", hãy **`hermes config get <key>` để kiểm tra thật** trước khi kết luận vô hại.

### `config set model.provider` TỰ XÓA `model.base_url`

Đổi provider sẽ in: `Cleared model.base_url (...) — that route belonged to the old
provider`. Thứ tự bắt buộc:

```powershell
config set model.provider ark          # bước này xóa base_url cũ
config set model.default deepseek-v4-flash-260425
config set model.base_url https://...  # PHẢI set lại SAU provider
```

Set `base_url` trước `provider` là mất trắng, và triệu chứng nhìn giống "sai key".

Copy cả bộ skill thì dùng `scripts/sync_skills_sftp.py` (SFTP, bỏ `.archive/`, so
kích thước nên chạy lại rất nhanh):

```bash
python scripts/sync_skills_sftp.py --host <host> --user <user> --pass '<pass>'
```

Thực tế đã chạy: 341 skill / 1466 file, ~2 phút, 0 lỗi. Đường dẫn đích suy từ
`--user`, không hardcode user cũ.

Kiểm tra lại sau khi copy — đếm phải **≥** số skill local:

```powershell
(Get-ChildItem "C:\Users\<user>\AppData\Local\hermes\skills" -Recurse -Filter SKILL.md).Count
```

Lần đầu enable Telegram, `set_my_commands` báo `60 commands registered, N hidden
(over 60 limit)` — bình thường, Telegram giới hạn 60 lệnh trong menu. Không phải
lỗi, đừng đi "sửa".

## MCP server trên máy đích: cài Node trước, coi chừng lệnh tương tác

### Máy Windows đích thường KHÔNG có Node

MCP stdio kiểu `npx -y mcp-remote@latest <url>` cần Node. Máy đích sạch thường
thiếu cả `node`, `npx`, `winget`, `uv` — kiểm hết trước khi hứa. Không có winget
thì cài bản portable vào `%LOCALAPPDATA%\hermes\tools\node` (không cần admin,
không reboot):

```powershell
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
$idx = Invoke-RestMethod "https://nodejs.org/dist/index.json" -TimeoutSec 60
$ver = ($idx | Where-Object { $_.lts } | Select-Object -First 1).version
$zip = "$env:TEMP\node.zip"
Invoke-WebRequest "https://nodejs.org/dist/$ver/node-$ver-win-x64.zip" -OutFile $zip -UseBasicParsing -TimeoutSec 300
$dest = "$env:LOCALAPPDATA\hermes\tools"
Expand-Archive -Path $zip -DestinationPath $dest -Force
Rename-Item (Join-Path $dest "node-$ver-win-x64") "node"
$nd = Join-Path $dest "node"
[Environment]::SetEnvironmentVariable("Path",
  ([Environment]::GetEnvironmentVariable("Path","User").TrimEnd(';') + ";" + $nd), "User")
& "$nd\node.exe" -v; & "$nd\npx.cmd" -v
```

Đã verify trên máy đích sạch: Node v24.21.0 / npx 11.19.0, ~38MB tải + giải nén
trong ~1 phút. Ghi vào **PATH của User**, không phải máy — không cần admin.

Chạy script này **trực tiếp qua `exec_command`**, đừng `Start-Process` detached:
session này `Start-Process` sinh process chết ngay và không tạo được cả file log
(`log: False`, `node.exe: False` sau 90s), trong khi chạy thẳng thì xong trong 58s.
Lệnh tải vài chục MB vẫn nằm trong timeout 300s của `execute_code`; chỉ chia nhỏ
khi lớn hơn.

Đường dẫn tuyệt đối tới `npx.cmd` dùng được trong config MCP, không cần PATH:

```yaml
mcp_servers:
  <name>:
    command: C:\Users\<user>\AppData\Local\hermes\tools\node\npx.cmd
    args:
      - "-y"
      - mcp-remote@latest
      - https://<server-url>
    enabled: true
```

### `hermes mcp` qua SSH: `add` và `remove` TREO, `install`/`list` thì không

Đã dính thật trong một session:

| Lệnh | Kết quả qua SSH |
|---|---|
| `hermes mcp catalog` / `list` | OK |
| `hermes mcp install canva` | OK — cài xong (OAuth thì còn phải bấm, xem dưới) |
| `hermes mcp remove canva` | **treo** — chờ xác nhận tương tác, `--yes` không tồn tại → `usage: hermes` |
| `hermes mcp add canva --command ... --args ...` | **treo** — probe server (tải npx + OAuth) không bao giờ xong |

Không có TTY thì `input()` không hiện prompt và bạn không biết nó đang chờ gì. Ba
đường, theo thứ tự rẻ:

1. Chạy trong **PTY** (`exec_command` của paramiko với `get_pty=True`) rồi bơm
   `y\n` khi thấy chữ `confirm`/`(y/n)` trong output.
2. Cho `mcp add` một `--connect-timeout` ngắn để probe bỏ cuộc sớm.
3. **Sửa thẳng entry trong `config.yaml`** theo dòng — nhanh và chắc nhất khi chỉ
   cần đổi `url`/`auth` thành `command`/`args`. Vẫn giữ nguyên tắc "KHÔNG regex ở
   trên": đọc khối bằng `[System.IO.File]::ReadAllText` + `IndexOf`, thay bằng
   `.Replace(old, new)` từ chuỗi base64, ghi lại bằng `UTF8Encoding($false)`.

⚠️ `IndexOf("mcp_servers:")` trả về **khối ví dụ bị comment** ở đầu `config.yaml`
(dòng ~1330), không phải entry thật. Dùng `LastIndexOf` hoặc lặp tìm tất cả rồi
chọn cái có dòng con không bắt đầu bằng `#`. Kiểm `[regex]::Matches(...).Count`
phải bằng 1 trước khi ghi, và `hermes mcp list` + `hermes config check` sau khi ghi.

### MCP dùng OAuth: trên máy không có browser thì phải nhờ người bấm

`hermes mcp install <name>` cho MCP OAuth sẽ in authorize URL rồi chờ paste
redirect URL. Headless/SSH thì nó `PROBE FAILED ... timed out after 30s`, vẫn cài
nhưng không lấy được tool. Không có đường vòng: cần một người đăng nhập và bấm
Approve. Chuẩn bị sẵn mọi thứ rồi đưa anh **một link** để bấm, thay vì bắt anh
chạy lệnh.

Chi tiết Google (port token, xác định account, dựng client_secret từ token cũ) và
Canva (metadata OAuth, dynamic client registration, cache `mcp-remote`, token chết
sau ~30 ngày) ở `references/remote-credential-porting.md`.

## Danh sách kiểm tra trước khi báo "xong"

- [ ] `gateway status` thấy process đang chạy
- [ ] `gateway.log` có dòng platform connected, không phải "No adapter available"
- [ ] Model trả lời được bằng prompt thật, không chỉ API test
- [ ] Bot token đúng: `GET https://api.telegram.org/bot<token>/getMe` ra đúng username
- [ ] `getWebhookInfo` có `url: ""` — không thì polling bị webhook tranh
- [ ] `errors.log` không còn `not connected to any AI provider` / `401`
- [ ] Số `SKILL.md` trên máy đích ≥ số skill local
- [ ] `.env` không có BOM (kiểm tra khi gặp 401)
- [ ] Số entry trong `config.yaml` khớp số liệu kỳ vọng
- [ ] `hermes config check` không báo lỗi
- [ ] Nếu là sau reboot: login item đã cài và process đã chạy
- [ ] Nếu gateway "chết": đọc `gateway_state.json` (`retrying_since`,
      `needs_attention`) và `gateway-exit-diag.log` TRƯỚC khi khởi động lại —
      khởi động lại sẽ xóa dấu vết và mất nguyên nhân thật
- [ ] PID do `gateway status` in ra đã qua `tasklist /FI "PID eq N"` xác nhận
      là `python.exe`, không phải `conhost.exe`
- [ ] Nếu vừa đổi SOUL.md/persona: phiên CŨ đã được clear prompt
      (`sessions repair-prompts <id> --apply`) — chưa clear thì coi như chưa xong,
      vì bot vẫn trả lời bằng persona cũ
- [ ] Test bằng tin nhắn THẬT vào bot, không chỉ `hermes -z` (CLI tạo phiên mới nên
      luôn ăn ngay, che mất lỗi ghim prompt của phiên cũ)
- [ ] Nếu có MCP server: `hermes mcp list` thấy `enabled` là CHƯA đủ — MCP OAuth
      chưa bấm Approve thì vẫn `enabled` mà không có tool nào. Phải xác nhận tool
      thật load được (gọi `hermes mcp test <name>`, hoặc để agent liệt kê tool)

## Dựng chuỗi fallback: test model trước, không tin danh mục

Dùng `scripts/probe_models.py` (provider-agnostic, chạy được với mọi endpoint
OpenAI-compatible):

```bash
PROVIDER_KEY=nvapi-... \
PROVIDER_BASE=https://integrate.api.nvidia.com/v1 \
python scripts/probe_models.py
```

Ba cổng kiểm, mỗi cổng bắt một loại hỏng khác nhau:

| Cổng | Kiểm | Bắt được |
|------|------|----------|
| 1 | gọi thường, có retry | 403/404 entitlement, timeout |
| 2 | có tool thì phải gọi tool | model chuyên dụng, `tool_choice` không hỗ trợ |
| 3 | trả kết quả tool về, phải dùng | **suy sụp decoder** — `reasoning_content` thành `!!!!!!!` |

Cổng 3 là cổng quyết định. Model 1T tham số trả lời đúng mọi câu hỏi thường
nhưng hỏng ở lượt ngay sau tool call, làm sập mọi lượt agent dùng tới nó. Chỉ
xếp chain theo **kết quả cổng 3**, không theo số tham số.

Sau khi có danh sách PASS, xác nhận lại qua harness thật — system prompt 15K
token + 17 tool là bài kiểm tra khác:

```
hermes --provider <p> -m <model> -z "Use terminal to compute 5*6, then answer briefly."
```

Kết quả phải là `30`, không phải `!!!!`.

## Liên quan

- `hermes-agent` — cấu hình chung, schema `fallback_providers`
- `hermes-telegram-gateway` — lỗi adapter, polling, DNS-over-HTTPS
- `hermes-model-provider-troubleshooting` — 401/429/404 theo provider
- `nvidia-nim-fallback` — chuỗi NVIDIA cụ thể đã verify (skill user-owned, chưa
  curator quản lý; chạy `hermes curator adopt nvidia-nim-fallback` nếu muốn em
  bảo trì tiếp)
- `windows-quirks` trong `hermes-agent` — lỗi Windows khác
- `scripts/probe_models.py` trong skill này — probe 3 cổng, dùng lại được cho
  mọi endpoint OpenAI-compatible
- `scripts/sync_skills_sftp.py` trong skill này — copy cả bộ skill sang máy đích
  qua SFTP, bỏ `.archive/`, so kích thước nên chạy lại nhanh
- `scripts/dump_remote_session.py` trong skill này — tải `state.db` từ máy đích,
  in ra mỗi phiên đang dùng prompt nào (có/không từ khoá persona) + n tin nhắn
  cuối. Dùng để chứng minh persona đã ăn hay chưa, thay vì đoán từ log
- `references/byteplus-ark-coding-endpoint.md` — endpoint `/api/coding/v3` giới
  hạn model thế nào, khối config `providers.ark` đã verify, thứ tự lệnh set
- `references/hermes-prompt-assembly.md` — kiến trúc prompt 3 tầng và TẦNG NÀO THẬT
  SỰ điều khiển tính cách: `SOUL.md` là slot #1 identity (`system_prompt.py:189`),
  `display.personality` KHÔNG được nạp vào prompt (chỉ xuất hiện trong một lệnh
  `print()` ở `config.py:4337`), `agent.system_prompt` chen vào tầng `context` SAU
  SOUL.md nên có thể đá ngược persona. Kèm khối 16 điều CHỐT (thay bản 11 điều) và
  cách đo rồi cắt nội dung chỉ-dùng-khi-viết-bài khỏi SOUL.md. **Đọc TRƯỚC khi sửa
  persona.**
- `references/gateway-death-diagnosis.md` — biên bản case thật: gateway chết vì
  mạng, `retrying_since` lộ ra 3 ngày chập chờn, state file kẹt chặn restart,
  `gateway status` báo nhầm PID là `conhost.exe`, và bảng so sánh 5 cách khởi
  động từ SSH (chỉ `schtasks /RU + /RP` sống được). Dùng làm pattern-matching
  khi gặp "gateway không chạy".
- `references/gateway-supervision-windows.md` — TẦNG GIÁM SÁT: vì sao login-item
  không đủ (case chết ~15 tiếng), vì sao agent tự gọi `hermes gateway restart` là
  tự sát và smart approval tự duyệt lệnh nó vừa gắn cờ, Hermes gateway là
  SINGLETON nên watchdog tự viết GIẾT cái đang sống, 4 cách check sống/chết (3
  cách sai), thiết kế Scheduled Task đúng + lý do từng tham số, event log
  forensics cho "máy tự restart?", truy lệnh trong `state.db` từ xa, nhiễu CLIXML,
  và `guest_mode`. **Đọc TRƯỚC khi sửa auto-start.**
- `scripts/register_gateway_task.py` — đăng ký Scheduled Task giám sát qua SSH
  (tắt VBS Startup + `MultipleInstances=IgnoreNew` + `ExecutionTimeLimit=0` +
  restart + verify), in ra bước test thật ở cuối. Chạy lại được, có `--dry-run`.
- `references/remote-credential-porting.md` — bê credential sang máy đích: Google
  token port được nguyên file, cách xác định account khi field `account` trống,
  dựng `client_secret.json` từ token cũ; Canva MCP (catalog, metadata OAuth,
  dynamic client registration, cache `mcp-remote`, vì sao token chết sau ~30 ngày).
  Phân biệt rõ phần ĐÃ verify với phần chưa chạy hết.
- `templates/open-ssh-remote.ps1` trong skill này — mở port 22 trên máy đích
  (Admin, chạy tại máy đó): OpenSSH 3 tầng dự phòng + firewall rule + DefaultShell
  + in IP nội bộ để forward router. Kèm biến thể dán thẳng không cần file.

## Credential và trạng thái máy đích: không tin bản ghi cũ

Credential của máy đích **đổi giữa các session** và bản ghi trong memory sẽ cũ.
Thực tế: `lqremote` từng vào bằng `Admin/<PASSWORD>`, session sau cả **user lẫn
password** đều đổi (`nlquan` / mật khẩu mới). Đổi user thường kèm máy cài lại
hoặc tạo profile mới → sshd, firewall rule, và cả đường dẫn
`C:\Users\<user>\hermes-agent\` đều phải kiểm lại từ đầu, không suy ra từ lần
trước.

⚠️ **Cảnh báo tinh vi: credential bị gửi nhầm vào một session/channel đang treo
thì mất.** Đã xảy thật — anh gửi `tài khoản là nlquan` + mật khẩu mới vào
**nhóm Telegram**, mà nhóm đó gateway đang treo nên agent không bao giờ xử lý tin
nhắn. Agent ở session khác hoàn toàn không thấy. Nếu anh nói "em đã gửi thông
tìn rồi" mà mình vẫn không có, hãy hỏi lại chỗ anh gửi, thay vì kết luận anh
chưa gửi.

Ngoài ra, khi đã có user mới, hãy **suy ra host thật từ lệnh kết quả** chứ không
tin tên host trong memory: `hostname` trên máy đích có thể là `LONGQUAN` trong
khi DNS public trỏ `lqremote.thefirstonly.com`. Path của mọi lệnh đều suy từ
`$env:LOCALAPPDATA` của user mới.

Thứ tự bắt buộc trước khi hứa gì với anh:

1. **Port scan chậm** (≤ 40 luồng) — đừng kết luận từ một lần quét nhanh.
2. Thử SSH bằng credential HIỆN TẠI anh vừa đưa. `Authentication failed` là sai
   mật khẩu, **không phải** sai port — hỏi lại anh chứ đừng đoán.
3. Chỉ sau khi SSH OK mới `Test-Path` đường dẫn Hermes. Đường dẫn suy từ
   `$env:LOCALAPPDATA` của user mới, đừng hardcode user cũ.

Khi không vào được, nói thẳng **cái gì đang chặn** (port 22 `10035` = router không
forward, hay `10061` = chưa bật service) và **anh cần làm gì** — bật sshd hay
forward router. Đó là câu trả lời hữu ích; "không vào được" thì không.
