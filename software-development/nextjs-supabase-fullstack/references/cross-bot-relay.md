# Cross-Bot HTTP Relay Server

## Problem

Two AI agents (Hermes instances or separate bots like OpenClaw) need to communicate but cannot see each other's messages due to platform restrictions (e.g., Telegram blocks bot-to-bot message delivery entirely). Users resort to manual copy-paste, which defeats collaboration.

## Solution: Shared HTTP Relay

Run a minimal HTTP server (Python stdlib, no dependencies) on one machine and expose it through the existing Cloudflare tunnel. Both bots write to and read from the relay using simple HTTP calls — no polling, no shared filesystem, no GitHub tokens.

```
POST /relay  {"bot":"Claw", "msg":"..."}   → saved to messages.json
GET  /relay  → [{"id":1, "bot":"Claw", "msg":"...", "ts":"..."}]
GET  /relay?since=5 → only messages newer than id 5
```

## Implementation

### 1. Relay Server (Python stdlib)

```python
#!/usr/bin/env python3
import http.server, json, os, urllib.parse
from datetime import datetime, timezone, timedelta

VN_TZ = timezone(timedelta(hours=7))
DATA_FILE = os.path.expanduser("~/AppData/Local/hermes/cron/output/relay_messages.json")

def load_messages():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_messages(msgs):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(msgs, f, ensure_ascii=False, indent=2)

class RelayHandler(http.server.BaseHTTPRequestHandler):
    def _send_json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path.rstrip("/") == "/relay":
            msgs = load_messages()
            params = urllib.parse.parse_qs(parsed.query)
            since = params.get("since", [None])[0]
            if since:
                msgs = [m for m in msgs if m.get("id", 0) > int(since)]
            self._send_json({"ok": True, "count": len(msgs), "messages": msgs})
        else:
            self._send_json({"error": "not_found"}, 404)

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path.rstrip("/") == "/relay":
            content_len = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_len)
            data = json.loads(body)
            bot = data.get("bot", "unknown")
            msg = data.get("msg", "")
            if not msg.strip():
                self._send_json({"error": "msg_required"}, 400)
                return
            msgs = load_messages()
            new_id = (msgs[-1]["id"] + 1) if msgs else 1
            now = datetime.now(VN_TZ).strftime("%Y-%m-%d %H:%M:%S")
            entry = {"id": new_id, "bot": bot, "msg": msg, "ts": now}
            msgs.append(entry)
            save_messages(msgs)
            self._send_json({"ok": True, "id": new_id, "message": entry}, 201)
        else:
            self._send_json({"error": "not_found"}, 404)

http.server.HTTPServer(("0.0.0.0", 9877), RelayHandler).serve_forever()
```

### 2. Tunnel Integration

Add the relay port to the existing Cloudflare tunnel config:

```yaml
# ~/.cloudflared/firstonly-config.yml
ingress:
  - hostname: bot.yourdomain.com
    service: http://localhost:9877      # ← relay server
  - hostname: me.yourdomain.com
    service: http://localhost:5099
  - hostname: yourdomain.com
    service: http://localhost:5099
  - service: http_status:404
```

Then add the DNS CNAME record (either via Cloudflare API or cloudflared CLI):

```bash
# Via cloudflared
cloudflared tunnel route dns <tunnel-id> bot.yourdomain.com

# Or via Cloudflare Dashboard → DNS → Add CNAME record
```

### 3. Client Usage (from any machine)

```bash
# Write a message
curl -X POST https://bot.yourdomain.com/relay \
  -H "Content-Type: application/json" \
  -d '{"bot":"Claw","msg":"Phản biện của tôi..."}'

# Read all messages
curl -s https://bot.yourdomain.com/relay | jq '.messages'

# Read only new messages (since id=5)
curl -s "https://bot.yourdomain.com/relay?since=5"
```

### 4. Helper Script (`relay_client.py`)

Distribute this to both bots:

```python
#!/usr/bin/env python3
"""Simple relay client — both bots use this."""
import sys, requests

RELAY_URL = "https://bot.yourdomain.com/relay"
BOT_NAME = "Hermes"  # Change per bot

def read(limit=None, after=None):
    url = RELAY_URL
    if after:
        url += f"?since={after}"
    r = requests.get(url, timeout=10)
    data = r.json()
    msgs = data.get("messages", [])
    if limit: msgs = msgs[-limit:]
    return msgs

def write(msg):
    r = requests.post(RELAY_URL, json={"bot": BOT_NAME, "msg": msg}, timeout=10)
    return r.status_code == 201

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: relay_client.py <write|read> [args]")
        sys.exit(1)
    if sys.argv[1] == "write":
        write(" ".join(sys.argv[2:]))
    elif sys.argv[1] == "read":
        for m in read(limit=int(sys.argv[2]) if len(sys.argv) > 2 else None):
            print(f"[{m['ts']}] {m['bot'].upper()}: {m['msg']}")
```

## Design Decisions

| Decision | Rationale |
|----------|-----------|
| **File-backed** (not DB) | Zero dependencies, easy to inspect/edit, no schema |
| **Sequential IDs** | Simple `?since=N` for incremental reads |
| **No auth** | Protected by Cloudflare tunnel + domain obscurity. Add API key if needed. |
| **Polling (30s)** vs Push | No WebSocket complexity; 2 lightweight HTTP calls/minute is negligible |
| **Python stdlib** | Runs anywhere — no pip install needed |
| **Same machine as tunnel** | The relay must be on the same LAN/WAN as Cloudflare tunnel's local endpoint |

## When to Use

- ✅ Two bots need to collaborate but can't see each other's messages
- ✅ Both bots can make HTTP requests
- ✅ One bot has a publicly accessible server (via tunnel/ngrok)
- ❌ Real-time chat — use WebSocket or polling < 5s instead
- ❌ Persistent storage needed — use a DB instead of file

## Related

- `nextjs-supabase-fullstack` — main deployment skill (tunnel config, port management)
- `local-tunnel` — alternative tunnel approaches
