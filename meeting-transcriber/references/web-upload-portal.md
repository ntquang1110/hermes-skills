# Web Upload Portal — upload.thefirstonly.com

## Khi nào dùng

User muốn upload file ghi âm từ điện thoại/máy khác mà không qua Telegram (file >20MB hoặc không tiện gửi Telegram).

## URL

**https://upload.thefirstonly.com**

Cloudflare Tunnel → `localhost:8769` (Python stdlib HTTP server)

## Server code

**Location:** `D:/hermes_upload_server/server.py`

**Static page:** `D:/hermes_upload_server/upload.html` — served by the same server.

Dependencies: Python stdlib only (http.server, requests for Groq API, subprocess for ffmpeg). **Không** cần Flask/FastAPI.

## Architecture

```
Phone browser ──https──→ Cloudflare ──tunnel──→ localhost:8769
  Upload file (multipart POST /upload)
       ↓
  Server saves to D:/hermes_uploads/<uuid>.ext
       ↓
  Background thread:
    1. Compress (ffmpeg Opus 16kHz mono, multi-level fallback: 39k→12k→retry)
    2. Transcribe (Groq Whisper large-v3, vi) — 413 retry pattern
    3. Save transcript → publish via content-publish script
    4. Create 2-tab HTML notes (Tổng quan + Transcript) → publish via content-publish script
       ↓
  Preview URLs — gửi kết quả về chat
```

## How it works

### Frontend (upload.html)
- Mobile-first, dark theme (B/W/Y design system)
- Drag-and-drop OR tap to select file
- Progress bar (fake client-side, actual processing async)
- After upload: shows pending message

### Backend (server.py)
- **GET /** → serves upload.html
- **POST /upload** → receives multipart file, saves to disk, queues for processing
- **Background processor** → dequeues, compresses (3-level fallback), transcribes (Groq, 413 retry), publishes
- **2-tab HTML output** → `_make_html()` auto-generates Tổng quan tab (first 200 chars) + Transcript tab
- Raw multipart parser (no Flask — pure stdlib `parse_multipart()`)

## Dashboard integration

Link added at **https://me.thefirstonly.com/dashboard.html**

File: `C:\Users\NTQUANG_DELL\visit-card\dashboard.html` — served by `python -m http.server 5099` from `visit-card/`.

## Infrastructure

### Tunnel: TQUANG-DELL (ID: `0ce9aa47-7d52-4d6a-9a16-13b48c508cff`)
Runs as Windows service with `--token`. Remote config via Cloudflare API — **local config.yml ignored** when running with `--token`.

### Add ingress rule (remote config)

```python
import requests
API_TOKEN = "..."     # from cert.pem (see below)
ACCOUNT_ID = "..."
TUNNEL_ID = "0ce9aa47-7d52-4d6a-9a16-13b48c508cff"
headers = {"Authorization": f"Bearer {API_TOKEN}", "Content-Type": "application/json"}

resp = requests.get(
    f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/cfd_tunnel/{TUNNEL_ID}/configurations",
    headers=headers)
ingress = resp.json()["result"]["config"]["ingress"]
ingress.insert(-1, {"service": "http://localhost:8769", "hostname": "upload.thefirstonly.com"})

payload = {"config": {"ingress": ingress, "warp-routing": {"enabled": False}}}
resp = requests.put(
    f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/cfd_tunnel/{TUNNEL_ID}/configurations",
    headers=headers, json=payload)
# 200 = OK, auto-picks up in seconds — no restart needed
```

### Extract API Token from cert.pem

```bash
cat ~/.cloudflared/cert.pem | grep -v "BEGIN\|END" | tr -d '\n' | base64 -d | python -m json.tool
# → {"zoneID": "...", "accountID": "...", "apiToken": "cfut_..."}
```

Token scope: tunnel management only — does NOT cover DNS.

### Add DNS record (cross-zone)

cert.pem token may belong to zone A but target domain is zone B. Use correct zone ID:

```python
ZONE_ID = "09a2d553b4c5ce037065260ea1feb732"  # thefirstonly.com

# Remove old record
resp = requests.get(
    f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records?name=upload.thefirstonly.com",
    headers=headers)
for r in resp.json().get("result", []):
    requests.delete(
        f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records/{r['id']}",
        headers=headers)

# Add CNAME
requests.post(
    f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records",
    headers=headers,
    json={"type": "CNAME", "name": "upload",
          "content": f"{TUNNEL_ID}.cfargotunnel.com",
          "ttl": 1, "proxied": True})
```

### Zone IDs (known)

| Zone | ID |
|------|----|
| thefirstonly.com | `09a2d553b4c5ce037065260ea1feb732` |
| theliems.com | `551586f8e7873643b0d3686600a4e887` |
| kiemion.online | `c1d13e6ea307f4dc914ddb0f324fdd43` |

## Starting / Restarting

### Server
```bash
python "D:/hermes_upload_server/server.py"
# Port 8769, auto-starts background thread
# Verify: curl http://localhost:8769/health
```

### Tunnel
Runs as Windows service. Remote config auto-picked up. Full restart:
```bash
sc stop cloudflared && sc start cloudflared   # admin required
```

## Dependencies
- Python 3.11+ stdlib + `requests`
- `ffmpeg` in PATH (for audio compression)
- Groq API key in `~/.hermes/.env`
- `content-publish` skill (`scripts/content-upload.py`)

## Pitfalls

1. **cert.pem zone vs target zone** — Token scope covers tunnel management only. Use it ONLY for tunnel config. For DNS, POST to the target zone ID directly, not via `cloudflared tunnel route dns`.

2. **`cloudflared tunnel route dns` appends wrong suffix** — Produces `upload.thefirstonly.com.theliems.com` instead of `upload.thefirstonly.com`. Always use the REST API for cross-zone DNS.

3. **WARP conflict** — WARP + cloudflared QUIC timeout on Windows. Use `--protocol http2` or disconnect WARP.

4. **No auth on upload** — Relies on Cloudflare proxy obscurity. Add basic auth or secret header if needed.

5. **Python http.server cwd** — Serves from the directory where the process was started. If dashboard.html edits don't appear, verify cwd:
   ```bash
   wmic process where "processid=<PID>" get commandline
   ```

6. **File data in RAM** — Server reads entire body before parsing. Fine for <200MB. Larger files need streaming.

7. **Groq API key bị Hermes redact** — Khi đọc `.env` qua terminal, Hermes tự động redact `GROQ_API_KEY=gsk_...` thành `gsk_NZ...UTdM`. Dùng `set -a; source ~/.hermes/.env; set +a` rồi `${GROQ_API_KEY}` trong curl, hoặc parse file trong Python như `server.py` làm (kiểm tra `"..." not in s` để skip dòng đã bị redact).

8. **Cron tunnel restart ghi đè config mới** — Nếu tunnel restart (do service crash/boot) sau khi cập nhật remote config, config mới vẫn được giữ (remote config lưu ở Cloudflare, không local). Tuy nhiên, **các thay đổi local** (thêm ingress rule vào config.yml) bị ignore khi tunnel chạy với `--token`.

## Files
- `D:/hermes_upload_server/server.py` — Python HTTP server
- `D:/hermes_upload_server/upload.html` — Upload page
- `D:/hermes_uploads/` — Processed files

## Limitations
- Serial processing queue (chỉ 1 background thread xử lý file tuần tự)
- No auto-cleanup of uploaded files
- No webhook notification (results sent via chat manually)
- **File data streaming** — từ 15/08 không còn đọc cả body vào RAM, upload file lớn OK
- **Cloudflare free plan giới hạn request body ~99MB** — file >90MB phải chunked upload (đã implement: 80MB/chunk, tự động trên frontend, verify 100MB qua tunnel OK 15/08)
