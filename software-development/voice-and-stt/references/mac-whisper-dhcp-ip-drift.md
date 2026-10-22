# Mac Whisper + DHCP IP drift — 2026-10 session

## Symptom
Watchdog cron báo `Mac Whisper Server unreachable (192.168.1.3:9000): timed out`
dù Mac vẫn đang bật, SSH 22 + Whisper 9000 đang chạy.

## Root cause
Mac Mini 192.168.1.x **lấy IP mới mỗi lần DHCP lease refresh** (cũng có thể là MAC address
randomization do Wi-Fi private address). IP ổ cứng trong script/cron/watchdog bị thụt.

Session 2026-10 trace:
- 192.168.1.3 → ARP entry `1c-56-8e-80-96-59` — IP cũ, máy không còn
- 192.168.1.4 → MAC `bc-00-23-ae-86-48` — Apple, port 22/9000 REFUSED (sshd chưa lên)
- 192.168.1.5 → MAC `6a-7b-91-18-62-f4` — **MAC MINI MỚI NHẤT**, IP tại thời điểm này
- Verify: `socket.connect_ex('192.168.1.5',22)==0` (OPEN), `/health` trả 200 `{"status":"ok","model":"large-v3","pid":34030}`

## Fix (apply to ALL scripts that reference the Mac IP)
1. **Không hardcode IP** — dùng mDNS hostname `Mac-mini-cua-kiem.local` (verify:
   `socket.gethostbyname('Mac-mini-cua-kiem.local')` → đúng IP).

   Nếu hostname không resolve được → fallback scan subnet `/24` tìm host có port 9000/22 OPEN.
   Resolver: `scripts/mac_whisper_resolve.py` (Python, <4s).

2. **Watchdog cron** (`scripts/watchdog_mac_whisper.py`) — thay `HOST = "192.168.1.3"`
   bằng dynamic resolve qua `mac_whisper_resolve.resolve(force=True)`.

3. **STT wrapper** (`scripts/stt_mac_wrapper.py`) — dynamic resolve.

4. **Cố định IP (tuỳ chọn)** — đặt DHCP reservation cho MAC `6a-7b-91-18-62-f4`
   trên router (IP sẽ ổn định) + static hostname trong `/etc/hosts`.

## Diagnosis recipe (Windows git-bash)
```bash
# 1. ARP table — MAC address là dấu hiệu chắn nhất, không phải IP
arp -a | grep "192.168.1" | grep -v multicast | grep -v broadcast

# 2. Sweep subnet tìm máy mở port 22 + 9000
for i in $(seq 1 254); do
  (python -c "import socket;s=socket.socket();s.settimeout(0.7);
   print('$i', 'OPEN' if s.connect_ex(('192.168.1.$i',9000))==0 else 'closed');s.close()") 2>/dev/null &
done | grep OPEN

# 3. SSH test (paramiko — git-bash không có sshpass)
python -c "
import paramiko
c=paramiko.SSHClient(); c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect('192.168.1.5', username='tquang', password='<PASSWORD>', timeout=20)
i,o,e = c.exec_command('hostname; uptime; scutil --get ComputerName')
print(o.read().decode())
"

# 4. Whisper health
curl -sf http://192.168.1.5:9000/health
```

## Files affected
- `scripts/stt_mac_wrapper.py` — HOST hardcoded
- `scripts/stt_mac_local.py` — HOST reference
- `scripts/watchdog_mac_whisper.py` — HOST = "192.168.1.3"
- `.env` — HERMES_LOCAL_STT_COMMAND may embed IP

## Resolver (drop-in replacement for hardcoded IP)
```python
from scripts.mac_whisper_resolve import resolve, base_url
ip = resolve(force=True)  # returns "192.168.1.5" or None
url = base_url()          # returns "http://192.168.1.5:9000"
```
Cache: stores last-known IP in `~/.hermes/scripts/.mac_whisper_ip`.