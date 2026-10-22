# Biên bản: gateway chết vì mạng, và cái bẫy state file

Case thật — máy `lqremote` (anh Quân), 12/10/2026. Đã verify từng bước.
Dùng làm mẫu pattern-matching, không phải reproducer từng lệnh.

## Triệu chứng ban đầu

Anh báo Hermes máy đó không trả lời. `hermes gateway status`:

```
✗ No gateway process detected
```

Nhưng `tasklist` vẫn thấy `python.exe 12556` (đây là `hermes serve`, tiến trình
desktop app — **không phải gateway**). Hai thứ hay bị nhầm lẫn vào nhau.

## Chuỗi thời gian đọc từ log

```
09/10 10:05:32  telegram.state → "retrying"          ← CHẶT LẠI Ở ĐÂY
12/10 11:25:11  [Telegram] Discovering API fallback IPs via DoH
12/10 11:25:12  DoH discovery yielded no usable IPs (system DNS: unknown)
12/10 11:25:12  IPv4 API IP 149.154.166.110 failed: All connection attempts failed
12/10 11:25:12  IPv4 API IP 149.154.167.220 failed: All connection attempts failed
12/10 11:31:30  Connect attempt 4/8 failed: [Errno 11001] getaddrinfo failed
12/10 11:31:53  Disconnected from Telegram
12/10 11:31:53  Reconnect telegram error: connect timed out after 30s, next retry in 300s
```

Log dừng hẳn ở đó. Không có dòng nào sau 11:31:53.

**Bài học:** `retrying_since` = 09/10, nghĩa là Telegram đã fail **3 ngày** trước
khi tiến trình chết. Nếu chỉ đọc timestamp cái chết (11:31) sẽ kết luận "mất
mạng một lúc", bỏ sót nguyên nhân gốc là mạng chập chờn kéo dài.

## Vì sao tiến trình chết hẳn thay vì tự hồi

`errors.log` ghi:

```
WARNING gateway.lifecycle_ledger: Previous gateway life (pid=12672,
started_at=2026-10-07T16:21:45) exited UNCLEANLY (no exit path ran — SIGKILL /
OOM / VM death, or a process kill issued by the agent or one of its descendants,
e.g. a pkill/taskkill of the host interpreter image; see #113667).
last_heartbeat_at=2026-10-12T04:32:53  last_mem=None  suspected_oom=False
```

Và `gateway-exit-diag.log` đối chiếu:

```
{"tag": "gateway.previous_unclean_exit", "pid": 12672,
 "last_heartbeat_at": "2026-10-12T04:32:53"}
```

`suspected_oom=False`, `last_mem=None` → **không phải hết RAM**. Là bị kill.
Adapters Telegram fail quá lâu rồi tiến trình bị terminate, không chạy exit path.

## Bẫy: state file kẹt chặn gateway mới

`gateway_state.json` vẫn còn, ghi:

```json
{"pid": 12672, "gateway_state": "running", "exit_reason": null}
```

PID 12672 đã chết từ 11:32. File này không được ghi lại vì tiến trình bị kill.
Kết quả: `hermes gateway start` báo `✓ Gateway already running (PID: 14800)`.

`14800` là gì? `tasklist /FI "PID eq 14800"`:

```
conhost.exe   14800   Services   0   5,576 K
```

**`conhost.exe`, không phải gateway.** Lệnh đó đọc lock/pid file rác.

Sửa: `Remove-Item gateway_state.json -Force` rồi mới khởi động.

## Bẫy thứ hai: khởi động từ SSH chết theo phiên

Đã thử và KHÔNG sống được qua SSH:

| Cách | Kết quả |
|---|---|
| `Start-Process -WindowStyle Hidden` | không có tiến trình mới |
| VBS startup (`wscript.exe` + `sh.Run ... , 0, False`) | không có tiến trình mới |
| `Start-Process` + `-RedirectStandardOutput` | không có tiến trình, log rỗng |
| `schtasks` không kèm credential | task "SUCCESS" chạy nhưng không có tiến trình |
| `hermes gateway run` chạy thẳng trong SSH | **chạy được, Telegram kết nối OK**, nhưng chết khi SSH đóng |

Cách sống được qua SSH:

```powershell
schtasks /Create /TN HermesGW /TR "C:/Users/NLQuan/AppData/Local/hermes/start_gw.bat" ^
         /SC ONCE /ST 23:59 /RU nlquan /RP <password> /RL LIMITED /F
schtasks /Run /TN HermesGW
```

Kết quả:

```
python.exe   2256   Services   0   266,248 K
[Telegram] set_my_commands OK for scope BotCommandScopeDefault (60 cmds)
[Telegram] Telegram menu: 60 commands registered, 369 hidden (over 60 limit)
```

`/RU` + `/RP` tường minh là điểm quyết định. Thiếu `/RP`, task chạy trong session
của SSH và chết theo. Có `/RP`, Windows tạo tiến trình trong session Services
(session 0) độc lập hoàn toàn.

Verify bằng **phiên SSH mới**, không phải phiên vừa launch — chỉ vậy mới chắc
nó sống thật.

Sau khi xong: `schtasks /Delete /TN HermesGW /F` để task không chạy lại lúc 23:59
và sinh gateway thứ hai. Giữ lại file `.bat` làm công cụ phục hồi.

## Kết quả cuối, verify bằng phiên SSH mới

```
tasklist /FI "PID eq 2256"  →  python.exe  2256  Services  266,248 K
gateway status              →  ✓ Gateway process running (PID: 2256)
gateway_state.json          →  {"pid":2256, "gateway_state":"running",
                                "exit_reason":null}
```

Ba nguồn đồng thuận = xong. Một nguồn thì chưa đủ.

## Chú ý về kết nối từ xa

Máy đích ở sau router (`1.53.98.175`), SSH vào bằng host động. Khi SSH bị
`Authentication failed`, nguyên nhân đầu tiên cần nghi là **credential đổi**,
không phải port hay firewall — server vẫn banner `SSH-2.0-OpenSSH_for_Windows_8.1`
bình thường. Hỏi anh lấy mật khẩu mới, đừng thử brute.

Windows OpenSSH cho phép cả `password` và `keyboard-interactive`; paramiko
`auth_password` thử cả hai, nên không cần tách riêng trừ khi server từ chối
cả hai.