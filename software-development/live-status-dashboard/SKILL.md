---
name: live-status-dashboard
description: Build a live, auto-refreshing web dashboard that surfaces Hermes internal state — sessions, processes, cron jobs, gateway health — using only Python stdlib. Zero-dependency monitoring UI exposed via tunnel for mobile access.
---

# Live Status Dashboard

When the user asks for a "screen to see what's happening", "live overview", "dashboard cập nhật liên tục" — build a lightweight Python HTTP server that reads Hermes internal data stores and serves an auto-refreshing HTML/JS dashboard.

## Architecture

```
Browser (phone/desktop)
    │
    ▼  Cloudflare Tunnel (trycloudflare.com)
    │
Python stdlib HTTP server (localhost:PORT)
    │
    ├── state.db (SQLite)       — sessions, messages
    ├── processes.json          — running servers/tunnels
    ├── gateway_state.json      — Telegram/Feishu status
    └── cron/jobs.json          — scheduled jobs
```

## Data Sources

All under `~/AppData/Local/hermes/`:

| Source | Format | Key query |
|--------|--------|-----------|
| `state.db` | SQLite (table: `sessions`, `messages`) | Recent sessions, message count, token usage |
| `sessions/sessions.json` | JSON | Active session routing |
| `processes.json` | JSON array | Running background processes |
| `gateway_state.json` | JSON | Gateway + platform health |
| `cron/jobs.json` | JSON (`jobs[]`) | Cron schedule + status |
| `gateway_state.json` | JSON | Active agents count |

### state.db — key schema

```python
sessions: id TEXT PK, title TEXT, source TEXT, started_at REAL,
          ended_at REAL, message_count INT, tool_call_count INT,
          input_tokens INT, output_tokens INT, estimated_cost_usd REAL,
          archived INT DEFAULT 0

messages: id INT PK, session_id TEXT FK, role TEXT, content TEXT,
          timestamp REAL, token_count INT
```

## Building the Server

### Minimal pattern (stdlib only)

```python
import http.server, json, sqlite3, os, urllib.parse

HERMES_DIR = os.path.expanduser("~/AppData/Local/hermes")

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        path = urllib.parse.urlparse(self.path).path.rstrip("/")
        if path == "/api/overview":
            self._json(api_overview())
        elif path == "/":
            self._html(DASHBOARD_HTML)
        else:
            self.send_response(404)
            self._json({"error": "not found"})

    def _json(self, data):
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))

    def _html(self, html):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

if __name__ == "__main__":
    server = http.server.ThreadingHTTPServer(("0.0.0.0", 5000), Handler)
    server.timeout = 5  # don't let slow clients block
    print(f"Dashboard: http://localhost:5000")
    server.serve_forever()
```

### CRITICAL: Use ThreadingHTTPServer

`http.server.HTTPServer` (the default) is **single-threaded**. If a request stalls (slow client, connection timeout), the entire server freezes. Always use:

```python
server = http.server.ThreadingHTTPServer((HOST, PORT), Handler)
server.timeout = 5
```

## HTML / JS Dashboard Pattern

The dashboard is a single self-contained HTML string embedded in server.py (no separate files). Pattern:

```html
<style>
  :root { --bg: #0d1117; --card: #161b22; --text: #e6edf3; ... }
  body { font-family: system-ui; background: var(--bg); color: var(--text); }
  .card { background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 20px; }
  .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
  .status-dot { width: 10px; height: 10px; border-radius: 50%; }
  .dot-ok { background: #3fb950; box-shadow: 0 0 8px rgba(63,185,80,0.4); }
  .dot-err { background: #f85149; }
</style>
<div id="app">
  <h1>⚡ Dashboard</h1>
  <div id="statsGrid" class="stats-grid">...</div>
  <div id="activityList" class="activity-list">...</div>
</div>
<script>
  const REFRESH = 15000;  // 15 seconds
  async function fetchJSON(url) { const r = await fetch(url); return r.json(); }
  async function refresh() {
    const data = await fetchJSON('/api/overview');
    // Update DOM with data.stats, data.activity, data.processes, etc.
  }
  refresh();
  setInterval(refresh, REFRESH);
</script>
```

### Recommended sections

| Section | Data | HTML element |
|---------|------|-------------|
| **Quick Stats** | total_sessions, total_messages, input_tokens, cost | `.stats-grid` with `.stat-box` |
| **Platform Status** | gateway.*, platforms.* | `.platform-grid` with `.platform-badge` + status dots |
| **Running Processes** | processes[] | `.proc-list` with name, PID, started_ago |
| **Project Cards** | hardcoded + derived from processes/gateway | `.project-grid` with `.project-card` + status dot |
| **Activity Feed** | activity[] | `.activity-list` with title, source, last message, time ago |
| **Cron Jobs** | cron[] | `.cron-list` with name, next_run, status |
| **System Resources** | system (CPU, RAM, Disk, Uptime via psutil) | `.sys-grid` with `.sys-item` — pct value + detail line (used/total) |
| **Service Health** | services[] (port check) | `.svc-grid` with hostname, port, status dot (running/stopped) |

## System Resource Monitoring (Extended Feature)

Add `/api/system` and `/api/services` endpoints to the dashboard server for hardware + service monitoring.

### API: `/api/system`

Returns CPU, RAM, Disk C:, Disk D:, Uptime using `psutil` (must be installed: `pip install psutil`):

```python
def api_system():
    import psutil, socket, time
    cpu = psutil.cpu_percent(interval=0.5)
    mem = psutil.virtual_memory()
    disk_c = psutil.disk_usage("C:/")
    boot = psutil.boot_time()
    uptime_sec = time.time() - boot
    return {
        "cpu": {"percent": cpu, "cores": psutil.cpu_count()},
        "ram": {"total_gb": round(mem.total/1e9,1), "used_gb": round(mem.used/1e9,1), "percent": mem.percent},
        "disk_c": {"total_gb": round(disk_c.total/1e9,1), "used_gb": round(disk_c.used/1e9,1), "percent": disk_c.percent},
        "disk_d": same or None if D: doesn't exist,
        "uptime": f"{days}d {hours}h {mins}m"
    }
```

### API: `/api/services`

```python
SERVICES = [("Visit Card", 5099), ("Company Site", 3000), ...]

def api_services():
    results = []
    for name, port in SERVICES:
        s = socket.socket()
        s.settimeout(1)
        try:
            s.connect(("127.0.0.1", port))
            results.append({"name": name, "port": port, "status": "running"})
        except:
            results.append({"name": name, "port": port, "status": "stopped"})
        finally:
            s.close()
    return results
```

### Frontend: System Resource Cards

```html
.sys-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
.sys-item { background: rgba(255,255,255,.03); border: 1px solid var(--border); border-radius: 12px; padding: 14px; }
.sys-label { font-size: 11px; color: var(--text-dim); text-transform: uppercase; }
.sys-value { font-size: 18px; font-weight: 700; color: var(--text); }
.sys-value.warn { color: var(--yellow); }
.sys-value.danger { color: #FF4B4B; }
.sys-detail { font-size: 11px; color: var(--text-dim); margin-top: 2px; }
```

Display as **percentage** (large) + **detail** (small, e.g. `11.0GB / 17.1GB`). Color thresholds: warn=80%, danger=90% for RAM/Disk; warn=70% for CPU.

### Frontend: Service Health Cards

```html
.svc-item { display: flex; align-items: center; justify-content: space-between; padding: 8px 12px; }
.svc-dot.running { background: #44C767; box-shadow: 0 0 6px rgba(68,199,103,.3); }
.svc-dot.stopped { background: #FF4B4B; }
```

### Color thresholds (JS helper)

```javascript
const colorClass = (v, warn=80, danger=90) =>
    v >= danger ? 'danger' : v >= warn ? 'warn' : '';
```

## Port Health Checker (Cron)

For production, set up a cron job that checks all service ports every hour and restarts dead ones. Script pattern:

```python
#!/usr/bin/env python3
"""port_health.py — check ports, restart dead services."""
import socket, subprocess, time, os

SERVICES = [
    (5099, "Visit Card", r"C:\path\to\visit-card", f'python -m http.server 5099'),
    (5011, "Status Dashboard", r"C:\path\to\hermes-dashboard", f'python server.py'),
]

def port_alive(port):
    s = socket.socket(); s.settimeout(2)
    try: s.connect(('127.0.0.1', port)); s.close(); return True
    except: return False

for port, name, cwd, cmd in SERVICES:
    if port_alive(port): print(f"🟢 {name} - OK")
    else:
        print(f"🔴 {name} - DEAD, restarting...")
        subprocess.Popen(cmd, cwd=cwd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
```

Cron schedule: `0 * * * *` (every hour at minute 0).

## Tunnel Setup

After the dashboard server is running, expose it via cloudflared:

```bash
# WARP must be OFF
warp-cli disconnect

# Start tunnel — DO NOT add --protocol http2 (auto-detect QUIC works better)
# Use tee to capture URL (background process output is often invisible on Windows)
cloudflared tunnel --url http://localhost:5000 2>&1 | tee /c/Users/NTQUANG_DELL/tunnel_url.txt

# Wait ~20-30s, then grab URL:
grep "trycloudflare.com" /c/Users/NTQUANG_DELL/tunnel_url.txt
```

**Important:** cloudflared creates a new random URL each restart. If the tunnel process dies, the URL changes. For production, consider localtunnel with a fixed subdomain or a named cloudflared tunnel.

## Pitfalls

### 1. Single-threaded server blocks
`http.server.HTTPServer` processes one request at a time. A slow client or an unclosed connection stalls everything. **Always use `ThreadingHTTPServer`** and set `server.timeout`.

### 2. Stale processes on the port
After killing a Python HTTP server, the old listener may linger (even if the Python process is dead). Windows shows multiple LISTENING entries for the same port:
```bash
netstat -ano | findstr ":5000 " | findstr LISTENING
# Kill each stale PID:
taskkill //F //PID <PID>
```

### 3. Tunnel URL is ephemeral
- cloudflared trycloudflare.com URLs are random and die with the process
- If the tunnel disconnects, the old URL is dead forever
- **Solution:** store the URL in a file (`tee` pattern) so you can recover it if the process restarts
- **Better:** use named cloudflared tunnel or a localtunnel subdomain for stable URLs

### 4. Zero background output on Windows git-bash
`terminal(background=true)` often captures no output from cloudflared on MSYS2. This doesn't mean the tunnel is failing. Workarounds:
- Pipe through `tee` to a file
- Verify via curl against the local port to confirm the server is up
- Check `netstat` to confirm the tunnel process is LISTENING on the Cloudflare edge

### 5. state.db is locked during writes
Hermes may hold a write lock on `state.db` during active sessions. The SQLite read (SELECT) should succeed since SQLite supports concurrent reads, but if you get "database is locked":
- Add a retry with exponential backoff
- Open with `timeout=5000` (5s timeout for lock)
- Structure queries to be fast (< 100ms)

### 6. JSON files may be empty or malformed
`processes.json`, `gateway_state.json` may be empty during startup or after cleanup. Always handle `FileNotFoundError` and `json.JSONDecodeError` gracefully.

## Verification

```bash
# Local
curl -s http://localhost:5000/api/overview | head -c 200

# Through tunnel
curl -sL --max-time 15 https://<tunnel-url>.trycloudflare.com/ | head -5
```

## When to use this skill

- User asks for "màn hình tổng quan", "dashboard", "live status", "theo dõi tiến độ"
- User wants to see what Hermes is doing / has done across multiple projects
- Need to monitor Hermes infrastructure (gateway, processes, cron)
- Any scenario requiring real-time visibility into Hermes internal state from a phone or browser

## References

- `references/hermes-data-sources.md` — detailed schema of state.db, processes.json, gateway_state.json, cron/jobs.json

## Related skills

- `local-tunnel` — tunnel setup details, cloudflared/localtunnel comparisons
- `metelligent-project` — project-specific dashboarding (combined dashboard + server monitoring)
