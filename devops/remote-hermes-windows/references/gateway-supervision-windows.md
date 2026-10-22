# Giám sát gateway trên Windows — thiết kế đúng và các bẫy

Case thật: 13–14/10/2026, máy `lqremote` (anh Quân). Gateway chết lúc **23:09 ngày
13/10** và nằm chết **~15 tiếng** cho tới khi có người bật lại thủ công. File này ghi
lại nguyên nhân đã verify, các cách SAI đã thử, và thiết kế đã chạy được.

## 1. Nguyên nhân: agent tự tắt gateway để nạp config, rồi chết theo

Trình tự lấy từ `logs/agent.log` + bảng `messages` trong `state.db`:

```
23:07:56  inbound message: user=Nguyễn Quân chat=393536794
          msg='mọi người tag em trong các nhóm tele, 2 nhóm Redsky + 1 nhóm Ma...'
23:08:10  API call #1 → tool terminal (1.46s)
23:08:18  API call #2 → tool terminal (8.48s)
23:08:35  API call #3 → assistant gọi tool:
              hermes gateway restart 2>&1
23:08:35  agent.auxiliary_client: Auxiliary approval: using custom (...)
23:09:16  WARNING hermes_cli.gateway: Gateway PID 14800 did not exit within 30s of
          the stop request (SIGTERM, or the planned-stop marker on Windows)
          — sending SIGKILL. A kill during a WAL checkpoint can corrupt state.db
23:09:17  Received UNKNOWN as a planned gateway stop — exiting cleanly
          Shutdown context: signal=UNKNOWN under_systemd=no parent_pid=5984
23:09:23  tool result: {"output": "[Command interrupted]", "exit_code": 130,
          "approval": "Command was flagged (stop/restart hermes gateway (kills
                       running agents)) and auto-approved by smart approval,
                       then interrupted."}
23:09:26  Gateway stopped (total teardown 8.64s)
```

Ba điều rút ra, cả ba đều phản trực giác:

1. **`hermes gateway restart` chạy TỪ TRONG agent là tự sát.** Lệnh `restart` = stop
   rồi start. Nửa `stop` giết đúng tiến trình đang chạy lệnh → **nửa `start` không
   bao giờ chạy**. Kết quả là gateway dừng và ở lại dừng. Không phải "restart hỏng",
   mà là restart không thể hoàn tất về mặt cấu trúc.
2. **Smart approval GẮN CỜ rồi TỰ DUYỆT.** Nó nhận đúng nguy hiểm — chuỗi
   `Command was flagged (stop/restart hermes gateway (kills running agents))` — và
   vẫn cho chạy. Cảnh báo bị nêu ra rồi bỏ qua. Đừng tin "approval đã bắt được" là
   an toàn.
3. **Guard `_HERMES_GATEWAY` không phải lúc nào cũng chặn.** Trên máy này lệnh vẫn
   đi qua (chạy qua `hermes_cli.gateway` dưới dạng tiến trình con). Đừng thiết kế
   dựa trên giả định guard sẽ cứu.

**Nếu agent cần nạp lại config Telegram:** sửa config rồi để **Task Scheduler /
watchdog** restart, hoặc hẹn một `.bat` tách rời (`set _HERMES_GATEWAY=` +
`timeout /t 12` + restart) — KHÔNG gọi `hermes gateway restart` trực tiếp trong lượt.

## 2. Hermes gateway là SINGLETON — bật thêm là GIẾT cái đang sống

Đây là bẫy nguy hiểm nhất, và nó phá mọi watchdog ngây thơ.

`logs/gateway-exit-diag.log` sau khi watchdog cũ chạy:

```
{"tag":"gateway.start","pid":14428}
{"tag":"gateway.previous_unclean_exit","pid":14428,"prior_pid":8336,
 "prior_started_at":"2026-10-14T08:09:55Z","last_heartbeat_at":"2026-10-14T08:10:14Z"}
{"tag":"gateway.start","pid":15108}
{"tag":"gateway.previous_unclean_exit","pid":15108,"prior_pid":14428}
{"tag":"gateway.start","pid":10816}
{"tag":"gateway.previous_unclean_exit","pid":10816,"prior_pid":15108}
```

Mỗi dòng `previous_unclean_exit` = **instance mới đã giết instance trước**. Chuỗi
pids nối tiếp nhau 14428 → 15108 → 10816 là dấu hiệu của vòng lặp: check báo "chết"
sai → bật mới → giết cái đang khoẻ → check lại báo sai → bật tiếp.

Log watchdog tự viết, cho thấy đúng vòng lặp đó:

```
15:09:47  KHONG thay gateway -> khoi dong lai
15:10:32  DA BAT LAI OK, pid=10452,8336
15:13:03  KHONG thay gateway -> khoi dong lai     ← gateway 8336 ĐANG SỐNG
15:13:48  DA BAT LAI OK, pid=9944,14428
```

**Hệ quả thiết kế:** watchdog phải dùng cơ chế mà Windows tự chặn trùng
(`MultipleInstances = IgnoreNew`) thay vì tự quyết định bật hay không. Đừng viết
logic "nếu không thấy thì start" — sai một lần là mất một gateway khoẻ.

## 3. Bốn cách kiểm tra sống/chết, ba cách SAI

| Cách | Kết quả thật |
|---|---|
| `Win32_Process` lọc `CommandLine -like "*gateway run*"` | ❌ **Âm tính giả** với tiến trình session 0. Trả rỗng dù gateway đang chạy |
| `gateway_state.json` mtime làm grace period | ❌ File được ghi lại **liên tục** khi gateway sống → `age` luôn nhỏ → watchdog không bao giờ dám restart. Log: `state bao pid 14428 nhung file moi ghi 17s - dang khoi dong, cho` |
| Tin `gateway_state.json` là đủ | ❌ File kẹt: ghi `"gateway_state":"running"` + pid **đã chết**. Đã gặp: state báo `pid=8140 running` trong khi `session-0 python` = rỗng |
| `hermes gateway status` | ❌ Báo nhầm PID — từng trả `PID 14800` là `conhost.exe` |
| **`Get-Process python` lọc `SessionId -eq 0`** | ✅ **Đáng tin.** Gateway luôn là `python.exe` **duy nhất** ở session 0; `hermes serve` (desktop) ở session 1 |

Cách kiểm tra đã verify:

```powershell
# (a) pid trong state file con song?
$j = Get-Content "$hm/gateway_state.json" -Raw | ConvertFrom-Json
$p = Get-Process -Id $j.pid -ErrorAction SilentlyContinue
$aliveA = ($p -and $p.ProcessName -like "python*")
# (b) co python.exe nao o session 0 khong?
$aliveB = @(Get-Process python -ErrorAction SilentlyContinue |
            Where-Object { $_.SessionId -eq 0 }).Count -ge 1
```

⚠️ Nhưng **ngay cả cách này vẫn không đủ** để làm watchdog tự viết, vì vẫn là
"tự quyết định". Xem mục 4 — dùng Task Scheduler.

## 4. Thiết kế ĐÚNG: Scheduled Task sở hữu tiến trình gateway

Ý tưởng: để **Task Scheduler** theo dõi tiến trình, không tự viết logic. Action của
task CHÍNH LÀ `hermes.exe gateway run` (không bọc `.bat`, không `start ""`).

```powershell
$gw  = "C:\Users\<user>\AppData\Local\hermes\bin\hermes.exe"
$act = New-ScheduledTaskAction -Execute $gw -Argument "gateway run"
$t1  = New-ScheduledTaskTrigger -AtLogOn
$t2  = New-ScheduledTaskTrigger -AtStartup
$t3  = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(1) `
       -RepetitionInterval (New-TimeSpan -Minutes 5)
$set = New-ScheduledTaskSettingsSet -MultipleInstances IgnoreNew `
       -ExecutionTimeLimit ([TimeSpan]::Zero) `
       -RestartInterval (New-TimeSpan -Minutes 1) -RestartCount 999 `
       -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries `
       -StartWhenAvailable
Register-ScheduledTask -TaskName "HermesGateway" -Action $act `
  -Trigger $t1,$t2,$t3 -Settings $set `
  -User "<user>" -Password "<password>" -RunLevel Limited -Force
```

Vì sao từng tham số — không tham số nào là trang trí:

| Tham số | Vì sao bắt buộc |
|---|---|
| Action = `gateway run` trực tiếp | Task Scheduler phải **sở hữu** tiến trình thì nó mới biết task đang chạy hay đã chết. Bọc `.bat` + `start ""` là process tách rời, Task Scheduler mù |
| `MultipleInstances IgnoreNew` | **Chốt chặn trùng.** Trigger bắn trong lúc task đang chạy → bị BỎ QUA. Đây là thứ thay thế cho watchdog tự viết |
| `ExecutionTimeLimit = 0` (`PT0S`) | Mặc định là **3 ngày** — Task Scheduler sẽ kill gateway sau 72h. Phải tắt |
| `RestartCount 999` / `RestartInterval 1m` | Tự bật lại khi tiến trình chết |
| `Trigger AtLogOn` + `AtStartup` | Sống qua reboot máy, kể cả khi không ai đăng nhập |
| `Trigger Time` lặp 5 phút | Lưới an toàn cho ca **thoát sạch** (exit 0) — `RestartOnFailure` KHÔNG bắt được ca này, vì task không "fail" |
| `-User` + `-Password` (⇒ `LogonType: Password`) | Chạy được khi **không** đăng nhập. `S4U` có thể mất quyền ra mạng → Telegram không kết nối |
| `StartWhenAvailable` | Máy boot xong muộn vẫn chạy được |

### Đã verify chạy thật (không phải lý thuyết)

| Test | Kết quả |
|---|---|
| `Start-ScheduledTask` thêm 3 lần khi đang chạy | cùng pid, **không tạo chồng** |
| Kill pid bằng `taskkill /F` | task → `Ready`, rồi tự bật lại (lần đầu ~160s) |
| Ca thật ngoài đời: agent taskkill pid 2316 lúc **16:18:30** | pid mới 14724 lúc **16:18:51** = **21 giây** |

Kiểm tra cấu hình sau khi tạo:

```powershell
$t = Get-ScheduledTask -TaskName "HermesGateway"
"State         : " + $t.State
"MultipleInst  : " + $t.Settings.MultipleInstances      # phai la IgnoreNew
"ExecTimeLimit : " + $t.Settings.ExecutionTimeLimit     # phai la PT0S
"RestartCount  : " + $t.Settings.RestartCount
"RestartEvery  : " + $t.Settings.RestartInterval
"LogonType     : " + $t.Principal.LogonType             # phai la Password
```

### Phải tắt VBS trong Startup folder, không thì trùng ở mỗi lần đăng nhập

`hermes gateway install` / `gateway start` tạo login item
`...\Startup\Hermes_Gateway.vbs`. Task mới đã có trigger `AtLogOn`, nên VBS là
thừa — và ở mỗi lần đăng nhập cả hai cùng bắn. Hermes singleton sẽ giết một cái
(churn ~30s) chứ không hỏng hẳn, nhưng vô ích:

```powershell
Rename-Item "<Startup>/Hermes_Gateway.vbs" "Hermes_Gateway.vbs.disabled" -ErrorAction SilentlyContinue
```

Đổi tên chứ đừng xóa — giữ đường lùi.

⚠️ Sau bước này `hermes gateway status` sẽ không còn in dòng login-item. Đó là
mong đợi, không phải lỗi.

## 5. Truy "vì sao gateway dừng" — đọc DB, không chỉ đọc log

`gateway-exit-diag.log` nói **bị kill** (`previous_unclean_exit`), nhưng KHÔNG nói
**ai**. Muốn biết ai thì phải vào bảng `messages` của `state.db`.

Trên máy Windows đích, python đi kèm Hermes nằm ở `tools/`:

```powershell
$py = (Get-ChildItem "C:/Users/<user>/AppData/Local/hermes/tools" -Directory `
       -Filter "python-*" | Select-Object -First 1).FullName + "/python.exe"
$env:PYTHONIOENCODING="utf-8"
& $py "C:/Users/<user>/AppData/Local/hermes/q.py"
```

Schema bảng `messages` (verify được):

```
id, session_id, role, content, tool_call_id, tool_calls, tool_name,
effect_disposition, timestamp, token_count, finish_reason, reasoning,
reasoning_content, reason
```

`timestamp` là Unix epoch dạng float. Truy lệnh đã chạy:

```python
import sqlite3, sys, datetime
sys.stdout.reconfigure(encoding="utf-8", errors="replace")   # BAT BUOC
con = sqlite3.connect("file:%s?mode=ro" % DB, uri=True)
cur = con.cursor()
for ts, role, tname, content, tcalls in cur.execute(
        "SELECT timestamp, role, tool_name, content, tool_calls FROM messages "
        "WHERE session_id=? ORDER BY timestamp DESC LIMIT 400", (SID,)):
    blob = ((tcalls or "") + " " + (content or "")).lower()
    if "gateway restart" in blob or "gateway stop" in blob:
        print(datetime.datetime.fromtimestamp(ts), role, tname)
        print(blob[:600])
```

Hai chi tiết bắt buộc:

- `sys.stdout.reconfigure(encoding="utf-8", errors="replace")` — console Windows
  mặc định cp1252, gặp chữ có dấu là `UnicodeEncodeError: 'charmap' codec can't
  encode character '\u0110'`. Kèm `$env:PYTHONIOENCODING="utf-8"` phía PowerShell.
- `role='assistant'` giữ lệnh ở `tool_calls` (JSON), còn `role='tool'` giữ kết quả ở
  `content` — trong đó có `"approval": "...auto-approved by smart approval..."`.
  Đọc CẢ HAI mới thấy được chuyện gì đã xảy ra.

## 6. Máy tự restart? — đọc event log, đừng đoán

```powershell
# Ai/khi nào yêu cầu restart
Get-WinEvent -FilterHashtable @{LogName="System"; ID=1074} -MaxEvents 12 |
  ForEach-Object { "{0} | {1}" -f $_.TimeCreated, ($_.Message -replace "\s+"," ") }

# Crash / mất điện
Get-WinEvent -FilterHashtable @{LogName="System"; ID=41,1001,6008} -MaxEvents 10

# Lịch sử boot
Get-WinEvent -FilterHashtable @{LogName="System"; ID=6005} -MaxEvents 8
```

Đọc đúng ý nghĩa từng mã:

| Mã | Nghĩa |
|---|---|
| `1074` | Ai đó/lệnh gì đó yêu cầu restart. `Message` ghi rõ tên tiến trình khởi xướng + user |
| `41` | Kernel-Power: reboot không tắt máy sạch → **mất điện / treo cứng** |
| `1001` | BugCheck (blue screen) |
| `6008` | Lần tắt máy trước là bất thường |
| `6005` | Event log khởi động = máy vừa boot |

Đọc tiến trình khởi xướng trong `1074`:

- `RuntimeBroker.exe` + `reason: Other (Unplanned)` → app hoặc **người bấm Restart**.
  Đây là restart **sạch**, không phải bệnh.
- `MusNotificationUx.exe` + `reason: Operating System: Recovery (Planned)` →
  **Windows Update** restart.

Case thật, để thấy vì sao phải kiểm tra chéo: máy báo gateway chết 11:31 rồi máy
restart 11:33. Nhìn qua tưởng "máy tự restart định kỳ". Kiểm tra chéo:

- Lịch sử boot: `10-06 ×7` (ngày dựng máy — tên đổi
  `WIN-E72ENL05ER3` → `DESKTOP-BOTAD25` → `LONGQUAN`), `10-07`, `10-12`. Sau 10-12
  không restart lần nào.
- Mã `41`/`6008`: **đúng 1 lần duy nhất**, 10-06 17:35 (lúc dựng máy).
- Pending reboot của Windows Update: `False` cả ba cờ.

Kết luận đúng: **không** phải mất điện, **không** phải crash, **không** phải chu kỳ
tự động. Chỉ là 2 lần restart sạch lẻ tẻ. Nếu chỉ nhìn 2 mốc thời gian gần nhau thì
đã báo sai bệnh và đi sửa nhầm chỗ.

## 7. Nhiễu CLIXML khi lệnh trả về RỖNG

Khi một lệnh PowerShell từ xa **không in gì**, stdout có thể chứa khối XML tiến trình
của PowerShell thay vì rỗng:

```
#< CLIXML
<Objs Version="1.1.0.1" xmlns="http://schemas.microsoft.com/powershell/2004/04">
<Obj S="progress" RefId="0">...<AV>Preparing modules for first use.</AV>...
```

Đọc nhầm khối này thành "có kết quả" là sai. Hai hệ quả:

1. **Co rỗng = không tìm thấy.** Đừng kết luận "không có tiến trình nào" từ khối này.
2. **`Format-Table | Out-String` có thể làm mất sạch output.** Nhiều lệnh
   `Get-ChildItem ... | Format-Table` trả về rỗng lặng lẽ. Dùng
   `ForEach-Object { $_.FullName }` (in chuỗi phẳng) thay vì `Format-Table`.

Thêm một bẫy chuỗi: `"%s\\tools" % HM` với `HM` là chuỗi thường có thể biến `\t`
thành **TAB**, làm path hỏng (`hermes<TAB>ools` → `Illegal characters in path`).
**Dùng gạch chéo xuôi** (`C:/Users/.../tools`) là hết — đúng như quy tắc ở SKILL.md.

## 8. `guest_mode` — vì sao bot trả lời khi bị tag trong nhóm lạ

Config trên máy case (dòng 2089–2091):

```yaml
allowed_users: 6277220574,393536794
guest_mode: true          ← thủ phạm
allowed_chats:            ← rỗng
```

Comment trong `config.yaml` nói rõ:

```
# guest_mode lets explicit @mentions from non-allowlisted groups through.
# Default false; ordinary messages, replies, and regex wake words stay blocked.
```

`guest_mode: true` + `allowed_chats` rỗng = **mọi nhóm, ai tag là bot trả lời**.
Đây đúng là triệu chứng người dùng báo ("mọi người tag em trong các nhóm tele"),
và nó **không** chữa được bằng restart — restart chỉ nạp lại cùng config đó.

Chữa đúng:

```
hermes config set plugins.platforms.telegram.guest_mode false
# và/hoặc điền allowed_chats: "-1001234567890,-1009876543210"
```

⚠️ Đây là đổi hành vi nhận tin của máy người khác — hỏi trước khi sửa, và xin danh
sách nhóm được phép để điền `allowed_chats`, chứ đừng đoán.
