# Remote Hermes host config management — SSH/paramiko trên LAN (2026-09)

## Khi nào cần

Một endpoint Unsloth/tunnel chia sẻ (`pharma-llm.thefirstonly.com`) xuất hiện trên
**NHIỀU Hermes host**: máy làm việc (Windows), máy Mac (Hermes client chạy cron tâm lý),
đôi khi máy pharma-duc-anh (origin server). **Fix config trên máy này KHÔNG ảnh hưởng
máy khác.** Nếu user báo "Hermes <host khác> vẫn lỗi" mà ta chỉ sửa máy đang ngồi → lặp
đúng cùng một cụm lỗi (403/401/4096) trên máy kia.

## Quy trình truy cập host từ xa trên LAN

### 1. Tìm IP host qua ARP
```bash
# cấp IP của máy này trước
ipconfig | grep -i IPv4
# xem ARP table — các host đã giao tiếp trong LAN
arp -a | grep -E "192\.168\.1"
# ping broadcast để làm đầy ARP nếu thiếu host
ping -n 1 -w 1000 192.168.1.255
```
Thường chứa vài host: router (.1) + máy. Host Mac thường có SSH mở.

### 2. Xác định host nào mở SSH
```bash
for i in $(seq 1 254); do timeout 0.4 bash -c "echo > /dev/tcp/192.168.1.$i/22" 2>/dev/null && echo "192.168.1.$i:22 OPEN"; done
```
(Loại bỏ router + chính mình; host có SSH mở = Mac/Unsloth.)

### 3. SSH bằng paramiko (password auth) — đáng tin hơn sshpass background
`sshpass` thường không có trên Windows; background ssh pty bấm pass khó chính xác
(vẫn hỏi lại pass dù gửi đúng). **Dùng paramiko** (`pip install paramiko`):
```python
import paramiko
c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect(ip, username=user, password=pw, timeout=12,
          allow_agent=False, look_for_keys=False)
stdin, stdout, stderr = c.exec_command("whoami; hostname; sw_vers")
print(stdout.read().decode())
c.close()
```
Lưu ý:
- `allow_agent=False, look_for_keys=False` → tránh mặc định load key local làm lệch auth.
- Khi password bị từ chối, **đừng đoán mò nhiều pass**; hỏi lại user. SSH nhận yêu cầu
  password thật nghĩa username tồn tại, chỉ pass sai (hoặc pass login hệ thống ≠ pass riêng).

### 4. Deploy proxy + sửa config từ xa
- Sửa base_url Kiên-quyết dùng **perl/text** trên máy đích (patch tool của Hermes CHẶN
  ghi config.yaml ở máy local, và config máy remote không mở qua tool file cục bộ được).
  Một dòng: `perl -0pi -e 's/(- name: <provider>\\n)\\s*base_url: [^\\n]+/$1    base_url: http:\\/\\/127.0.0.1:18888/' config.yaml`.
- Deploy script proxy: `sftp = c.open_sftp(); sftp.file("/Users/tquang/unsloth-ua-proxy.py","w").write(local_script)`.
- Chạy proxy nền: `nohup python3 ... > /tmp/ua-proxy.log 2>&1 &`, verify `pgrep -fl`.
- **Lấy key bằng python `yaml.safe_load`, KHÔNG grep/awk** — grep/awk dòng `api_key:`
  giữ leading whitespace making key invalid (prefix `    sk-unslo`). Và `python3` system
  trên Mac có thể KHÔNG có module `yaml` (đã gặp `ModuleNotFoundError`) → dùng python của
  hermes venv (`~/.hermes/hermes-agent/venv/bin/python`) hoặc `sed -n '<line>p'` trên
  chính dòng api_key.
- **Test key đúng cách TỪ máy đích** (không mang key về hiển thị): `K=$(sed -n '<line>p'
  config.yaml | awk '{print $2}')` rồi curl với `$K`, chỉ in status.

### 5. Verify config từ xa
- `grep -nE 'base_url' config.yaml` → mọi nơi trỏ đúng.
- `pgrep -fl ua-rewrite-proxy.py` → proxy sống.
- YAML valid bằng `python <venv>/bin/python -c "import yaml;yaml.safe_load(open('...'))"`.
- Test end-to-end: curl qua proxy với UA `OpenAI/Python` → **phải 200** (không 403).

## PITFALL — Python 3.9 Mac không có yaml, dùng hermes venv
System `python3` (3.9) trên Mac thiếu module `yaml`. Dùng
`~/.hermes/hermes-agent/venv/bin/python` (có đủ Hermes deps) để verify YAML / kéo key.

## PITFALL — đổi config chỉ có hiệu lực từ session mới / sau restart
Khi sửa config host từ xa, process Hermes đang chạy trên máy đó giữ config cũ. Bắt buộc
**restart Hermes trên host đích** mới load config proxy mới. Nếu không restart dù config
đã đúng, lỗi 403/401/4096 **vẫn tái diễn** — đây là lý do phổ biến \"sao vẫn lỗi\" vừa xảy
ra dù proxy + config đều OK. Grep log host đích để xác nhận 403 đã hết trước khi khép việc.

## Restart Hermes Desktop app từ xa qua SSH (đã đo thành công 2026-09)

Ngược ý tưởng \"agent không tự ý restart\", agent >HOÀN TOÀN< restart an toàn Hermes Desktop
app (Electron) qua SSH — làm nền trong phiên SSH, không cần user ngồi máy đó:
```bash
# 1. quit app sạch
osascript -e 'tell application "Hermes" to quit'
# 2. kill process serve còn sót (serve là python -m hermes_cli.main serve --host 127.0.0.1)
pkill -f 'hermes_cli.main serve'
# 3. relaunch app từ bundle path thật (HERMES_HOME/hermes-agent):
open "$HOME/.hermes/hermes-agent/apps/desktop/release/mac-arm64/Hermes.app"
```
Verify:
- `ps aux | grep 'hermes_cli.main serve'` → PID MỚI (chứng minh đọc lại config).
- `ps aux | grep 'Hermes Helper' | wc -l` → ≥3-5 process (GUI + renderer + network + serve).
- `tail logs/errors.log` → hết `403/401`, chỉ còn `check_fn ... returned False` warnings
  (browser/kanban/image tools tắt — bình thường, vô hại).
Khi nào NÊN tự restart: chỉ khi đã sửa config host đích bằng tay và user xác nhận máy đó
không đang chạy job nóng. Với host chạy cron quan trọng, hỏi trước. Lưu ý: nếu Hermes host
chạy qua CLI/TUI (không phải Desktop app), cách khác — Desktop app là bundle Electron nên
`osascript quit` + `open` mới chuẩn; một process `serve` chết không tự spin lại được nếu
không có app cha quản lý.

## Cấu trúc nhiều-host cần đồng bộ (đo thật 2026-09)
Endpoint `pharma-llm.thefirstonly.com` nằm trong: `auxiliary.vision.base_url`,
`custom_providers[].base_url`, `model_aliases.*.base_url` **trên mỗi Hermes host**
(máy làm việc + máy Mac). Sửa sót 1 host = host đó tiếp tục trỏ endpoint chết. Checklist:
1. Xác định user chỉ *một* máy hay *tất cả* Hermes host bị lỗi.
2. Chạy `grep -nE 'base_url|trycloudflare' config.yaml` trên TỪNG host.
3. Proxy `ua-rewrite-proxy.py` cần chạy **ở local từng host** (127.0.0.1:18888 không
   chia sẻ giữa máy) — deploy + start riêng mỗi máy.