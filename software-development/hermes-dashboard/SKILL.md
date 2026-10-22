---
name: hermes-dashboard
description: "Hermes Dashboard — web overview live của Hermes activities, projects, processes. Server Python stdlib port 5000 + Cloudflare Tunnel."
---

# Hermes Dashboard

Dashboard web hiển thị real-time các hoạt động của Hermes: sessions gần đây, processes, platform status, cron jobs, project overview.

Deployed tại **`status.thefirstonly.com`** (qua tunnel TQUANG-DELL, port 5011).

## Files

- **Server:** `C:\Users\NTQUANG_DELL\hermes-dashboard\server.py`
- **Data source:** `~/AppData/Local/hermes/state.db` + processes.json + gateway_state.json + cron/jobs.json

## Start Dashboard

```bash
# Step 1: Start server
python "C:\Users\NTQUANG_DELL\hermes-dashboard\server.py"
# → http://localhost:5011

# Step 2: Port is served via TQUANG-DELL tunnel → status.thefirstonly.com
```

## Tabs
- **Overview** 📊 — Stats, Platform Status, Processes, Cron, Activity Feed
- **Goals** 🎯 — Project context: objectives, achievements, blockers, next actions, tech stack
- **System** ⚙️ — **System Resources** (CPU, RAM, Disk, Uptime) + **Service Health** (6 ports)

## API Endpoints

| Endpoint | Returns | Description |
|----------|---------|-------------|
| `GET /api/overview` | JSON | All aggregated data |
| `GET /api/activity` | JSON | Recent sessions |
| `GET /api/processes` | JSON | Running processes |
| `GET /api/gateway` | JSON | Gateway + platform status |
| `GET /api/cron` | JSON | Cron job status |
| `GET /api/stats` | JSON | Session/message/token stats |
| `GET /api/projects/context` | JSON | Goals & milestones |
| `GET /api/system` | JSON | **CPU, RAM, Disk C:, Disk D:, Uptime** (requires `psutil`) |
| `GET /api/services` | JSON | **TCP health check** cho 6 service ports |

## System Monitoring (thêm vào)

Requires `psutil`:
```bash
pip install psutil
```

**`/api/system`** response shape:
```json
{
  "cpu": {"percent": 14.1, "cores": 8},
  "ram": {"percent": 64.6, "used_gb": 11.0, "total_gb": 17.1},
  "disk_c": {"percent": 81.1, "used_gb": 122.1, "total_gb": 150.6},
  "disk_d": {"...": "..."},
  "uptime": "43d 13h 12m",
  "hostname": "TQUANG-DELL"
}
```

**`/api/services`** — Server health check bằng TCP socket:
```python
SERVICES = [
    ("Visit Card", 5099),
    ("Company Site", 3000),
    ("Knowledge Flow", 3003),
    ("TheLiem", 3001),
    ("ERP", 8080),
    ("Demo ERP", 10000),
]
```

Trong HTML, mỗi service item có `.svc-dot.running` (🟢) hoặc `.svc-dot.stopped` (🔴).

## System Grid CSS Classes
```css
.sys-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
.sys-item { background: rgba(255,255,255,.03); border: 1px solid var(--border); border-radius: 12px; padding: 14px; }
.sys-label { font-size: 11px; color: var(--text-dim); text-transform: uppercase; letter-spacing: 0.5px; }
.sys-value { font-size: 18px; font-weight: 700; color: var(--text); display: block; margin-top: 4px; }
.sys-value.warn { color: var(--yellow); }
.sys-value.danger { color: #FF4B4B; }
.sys-detail { font-size: 11px; color: var(--text-dim); display: block; margin-top: 2px; }
```

## Cloudflare Tunnel Config via API

Cập nhật tunnel config từ xa (override local config.yml bằng remote dashboard config):

```bash
export CLOUDFLARE_API_TOKEN="cfut_..."
curl -s -X PUT \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  "https://api.cloudflare.com/client/v4/accounts/{account_id}/cfd_tunnel/{tunnel_id}/configurations" \
  -d '{"config": {"ingress": [...], "warp-routing": {"enabled": false}}}'
```

DNS record management:
```bash
# List zones
curl -H "Authorization: Bearer $TOKEN" "https://api.cloudflare.com/client/v4/zones"
# Add CNAME
curl -X POST -H "Authorization: Bearer $TOKEN" \
  "https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records" \
  -d '{"type":"CNAME","name":"subdomain","content":"{tunnel_id}.cfargotunnel.com","ttl":1,"proxied":true}'
```

Token từ `~/.cloudflared/cert.pem` — chứa `AccountTag`, `zoneID`, `apiToken` (cần update scope trong Cloudflare Dashboard nếu thiếu DNS/Workers).

## Lưu ý quan trọng

- **`--config ""` bắt buộc** — nếu không, file `~/.cloudflared/config.yml` có ingress catch-all `http_status:404` sẽ chặn tunnel
- Tunnel URL mới mỗi lần restart (free trycloudflare)
- Server dùng `ThreadingHTTPServer` để handle concurrent requests
- HTML dashboard dark theme, auto-refresh mỗi 15s
- API endpoints: `/api/overview`, `/api/activity`, `/api/processes`, `/api/gateway`, `/api/cron`, `/api/stats`

## Passcode gate + branding (2026-07-31)

- **Passcode gate:** `server.py` có `PASSCODE_HASH = sha256("<PASSCODE>")` (cookie `tfo_auth`). `do_GET` chặn trước mọi route; `do_POST /_auth` verify → 302 + Set-Cookie khi đúng, HTML lỗi khi sai. Trang passcode = `PASSCODE_HTML` (form "Mở khoá").
- **Favicon:** `<link rel="icon" href="/favicon.png">` — file `favicon.png` đặt cạnh `server.py` (logo TFO, extract từ data URI thefirstonly.com).
- **Header:** badge link `◆ TFO → http://tfo.thefirstonly.com` cạnh LIVE badge.
- **Restart sau khi sửa:** kill process đang giữ port 5011 → `cd C:\Users\NTQUANG_DELL\hermes-dashboard && python server.py` (background).
- **Test:** `curl -b "tfo_auth=<hash>" http://localhost:5011/` mới thấy dashboard; không cookie → thấy form passcode.
- Recipe chi tiết → skill `web-passcode-gate`.

## Troubleshooting

- **404 từ Cloudflare:** Kiểm tra tunnel config — `status.thefirstonly.com` phải trỏ tới `localhost:5011`
- **Port 5011 không lắng nghe:** Kill process cũ: `taskkill //F //PID <pid>` rồi restart
- **Tunnel không kết nối:** WARP disconnected? `warp-cli status`
- **Server chết:** `tasklist //FI "PID eq $(netstat -ano | findstr :5011 | findstr LISTENING | awk '{print $5}')"` để kiểm tra

## Port Health Cron — Auto-Restart

Cron job chạy mỗi 1 giờ kiểm tra các service ports. Nếu port nào chết → tự động restart.

**Script:** `C:\Users\NTQUANG_DELL\AppData\Local\hermes\scripts\port_health.py`

Kiểm tra 4 port chính: 5099 (Visit Card), 3000 (Company Site), 3003 (KFlow), 5011 (Dashboard). Dùng TCP socket connect với timeout 2s. Nếu fail → subprocess.Popen restart.

**Cron job config:**
- Schedule: `0 * * * *` (đầu mỗi giờ)
- Deliver về origin (Telegram)
- Script path: `C:\Users\NTQUANG_DELL\AppData\Local\hermes\scripts\port_health.py`

Tạo cron job:
```bash
cronjob(action='create', name='Port Health Check', schedule='0 * * * *',
  prompt='Run python "C:\\Users\\NTQUANG_DELL\\AppData\\Local\\hermes\\scripts\\port_health.py" and report status')
```

**Pitfall — Python process stacking:** Khi kill all Python (taskkill //F //IM python.exe), các port listener cũ vẫn còn (TIME_WAIT). Process mới start không bind được port. Giải pháp: kiểm tra bằng PowerShell `Get-NetTCPConnection -LocalPort <port> -State Listen` thay vì netstat.

## Kill all

```bash
# Kill server
tasklist //FI "PID eq $(netstat -ano | findstr :5011 | findstr LISTENING | awk '{print $5}')" && taskkill //F //PID <pid>
```
