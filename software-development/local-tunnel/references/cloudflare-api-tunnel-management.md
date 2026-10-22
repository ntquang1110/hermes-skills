# Cloudflare Tunnel API & DNS Management

Cloudflare tunnels can be configured via **API** (remote/cloudflare-side config) instead of local YAML files. When `cloudflared tunnel list` shows a tunnel with active connections but changes to the local `-config.yml` have no effect, the tunnel is using **cloudflare-side config**.

## Detect config source

```bash
# Get tunnel details
cloudflared tunnel info <tunnel-uuid-or-name>

# Check via Cloudflare API (requires API token)
curl -s https://api.cloudflare.com/client/v4/accounts/<ACCOUNT_ID>/cfd_tunnel/<TUNNEL_ID>/configurations \
  -H "Authorization: Bearer <API_TOKEN>"
```

If the API returns ingress rules, the tunnel uses **remote config** — local YAML is ignored.

### 🚨 PITFALL: cloudflared installed as a Windows service cannot be killed with taskkill

`sc query Cloudflared` shows a service whose `BINARY_PATH_NAME` is `"C:\Program Files (x86)\cloudflared\cloudflared.exe" tunnel run --token eyJhIj...` — a **remotely-managed tunnel running as a Windows service** (parent = `services.exe`). You CANNOT kill it with `taskkill /F /PID <pid>` (→ "Access is denied", it's a child of services.exe) or `powershell Stop-Process -Force`.

**Symptoms:** the service tunnel holds connections at the Cloudflare edge and keeps serving with its own (stale) remote config even after you start a fresh `cloudflared tunnel --config ... run` with corrected local YAML. Domain still shows old content.

**Diagnosis — is a service tunnel involved?**
```bash
# 1. Cloudflared service exists?
sc query Cloudflared | grep -i state
# 2. Full binary path shows --token (remote-managed, not local config)?
sc qc Cloudflared | grep -i BINARY_PATH_NAME
# 3. Which tunnels have live connections (the service one among them)?
cloudflared tunnel list
```

**Fix options (in order):**
1. **Update the tunnel's REMOTE config via API** (PUT configurations) — the service picks it up without restart. This is the fix that works.
2. Stop the service if it's not needed: `sc stop Cloudflared` (admin) — the service tunnel's remote config then stops serving; your locally-started tunnel with corrected YAML takes over.
3. Do NOT waste time on `taskkill`/`Stop-Process` against the service PID — access is denied by design.

### 🚨 PITFALL: site serves wrong content — check remote config, not local YAML

**Symptom:** You edit `~/.cloudflared/<name>-config.yml` to point `domain.com → localhost:3000`, restart the tunnel, but `https://domain.com/` still serves old content (e.g. a different app on port 5099).

**Root cause:** the tunnel has a **remote config on the Cloudflare edge** that overrides your local YAML entirely. Editing the local file has ZERO effect — the edge config wins. (The local YAML is only used when the tunnel has NO remote config.)

**Diagnosis:**
```bash
# 1. Confirm domain DNS → which tunnel UUID:
#    GET /zones/<ZONE_ID>/dns_records — look for CNAME domain.com → <uuid>.cfargotunnel.com
# 2. GET /accounts/<ACCOUNT>/cfd_tunnel/<uuid>/configurations — print ingress list:
#    this shows the REAL routing (e.g. hostname=domain.com service=http://localhost:5099)
```

**Fix:** PUT the corrected full ingress list via API (see "Update tunnel ingress via API" below). Verify after ~10s with `curl -s https://domain.com/ | grep <title>` — cloudflared picks up remote config changes without restart.

## Extract API token from cert.pem

The Cloudflare API token is embedded in `~/.cloudflared/cert.pem`:

```bash
python3 -c "
import json, base64
with open('$HOME/.cloudflared/cert.pem') as f:
    content = f.read()
b64 = content.replace('-----BEGIN ARGO TUNNEL TOKEN-----', '') \
              .replace('-----END ARGO TUNNEL TOKEN-----', '') \
              .strip().replace('\n', '')
data = json.loads(base64.b64decode(b64))
print('AccountID:', data['accountID'])
print('ZoneID:', data.get('zoneID', 'N/A'))
print('APIToken:', data['apiToken'])
"
```

On Windows (git-bash), use native Windows paths.

## Update tunnel ingress via API

```bash
# Full replacement — PUT the entire config
curl -X PUT https://api.cloudflare.com/client/v4/accounts/<ACCOUNT_ID>/cfd_tunnel/<TUNNEL_ID>/configurations \
  -H "Authorization: Bearer <API_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "config": {
      "ingress": [
        {"hostname": "domain1.com", "service": "http://localhost:3000"},
        {"hostname": "domain2.com", "service": "http://localhost:9877"},
        {"service": "http_status:404"}
      ],
      "warp-routing": {"enabled": false}
    }
  }'
```

There is no partial-update endpoint — always send the full ingress list.

### 🚨 PITFALL: PUT is FULL REPLACEMENT — always re-list EVERY hostname

The PUT replaces the ENTIRE ingress config, not just adds one rule. If you send only the new hostname + catch-all, you **wipe out all other working domains** in that tunnel.

**Symptom:** You add one new hostname via PUT with just `[new-host, 404-catchall]` → other domains (me.tfo, upload.tfo, company.tfo...) start returning 404/502 because their ingress rules vanished.

**Prevention — before any PUT, reconstruct the complete list:**
1. Read current config first (if API GET works), OR keep a documented inventory of every hostname the tunnel serves
2. Include ALL of them in the PUT, plus the new one, plus the final `http_status:404` catch-all
3. After PUT, verify every domain, not just the new one:
```bash
for d in new.tfo company.tfo upload.tfo me.tfo root.tfo; do
  echo -n "$d: "; curl -s -o /dev/null -w "%{http_code}\n" --connect-timeout 15 "https://$d/";
done
```

Worked example from a real session — the firstonly tunnel serves: `tfo`, `company`, `upload`, `bot`, `me`, `root` (thefirstonly.com), `www`. A PUT that forgot 6 of those 7 domains broke them all until re-PUT with the full list. Always send the union of {existing hostnames} ∪ {new hostname}.

### 🚨 PITFALL: remote config is LIVE SHARED STATE — other agents can revert your fix

**Symptom:** You PUT the corrected remote config (domain → correct port), verify it works, user confirms. **Days later the domain serves the old content again**, local YAML still correct, and your PUT is gone from the API.

**Root cause:** The tunnel's remote config lives on the Cloudflare edge and **any agent/session holding the API token can re-PUT it**. On this machine multiple Hermes sessions and cron jobs manage the same Cloudflare account. A concurrent writer re-applied an OLD config — e.g. `thefirstonly.com → localhost:5099` (visit card) — silently undoing your fix. (Observed: the reverted config also contained brand-new hostnames — erp.kiemion.online, uploadhtml.thefirstonly.com — proving another writer had been editing the same tunnel.)

**Prevention rules:**
1. **Never trust a remote-config fix to persist.** Before claiming "fixed", re-GET `/configurations` via API and diff the ingress against what you PUT. If it flipped back, a concurrent writer is the cause.
2. **Always GET current config before every PUT** — merge {current ingress} with your correction. A PUT built only from your known hostnames wipes additions other agents made.
3. **Keep a canonical hostname inventory** for each tunnel (see list above) so any re-PUT reconstructs the full list.
4. If a domain keeps flipping back, find the OTHER writer (a cron like the Tunnel & WARP health script that restarts cloudflared, or another session with API access) and fix the config at that source — not just at the edge.

**Diagnosis shortcut — who changed it:** compare the API's current ingress list against the last list you saw. New hostnames you never added = concurrent writer active. Check `cronjob action=list` for health/watchdog crons (`port_health.py`, `tunnel_health.py`) and other sessions' logs before re-applying.

### Config version tracking

Each PUT updates the config **version number** (visible in tunnel logs):

```
INF Updated to new configuration config="{"ingress":[...]}" version=12
```

The version increments by 1 each time you update the config via API. When the tunnel restarts (after crash or manual restart), it re-reads the remote config from Cloudflare. **If the tunnel loads an older version** than your last PUT, your update didn't persist — check the API response for errors.

**Crash resilience:** API config updates survive tunnel crashes. A tunnel that exits with `i/o timeout` (common on unstable networks like Vietnam) will pick up the latest remote config on restart. You do NOT need to re-apply config changes after a tunnel restart.

## Manage DNS records via API

Zone ID can be retrieved by name:

```bash
curl -s "https://api.cloudflare.com/client/v4/zones?name=example.com" \
  -H "Authorization: Bearer <API_TOKEN>"
# → result[0].id is the zone ID
```

### Create DNS CNAME for tunnel

```bash
curl -X POST "https://api.cloudflare.com/client/v4/zones/<ZONE_ID>/dns_records" \
  -H "Authorization: Bearer <API_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "CNAME",
    "name": "subdomain",     # subdomain.example.com
    "content": "<TUNNEL_UUID>.cfargotunnel.com",
    "ttl": 1,
    "proxied": true
  }'
```

### List existing records

```bash
curl -s "https://api.cloudflare.com/client/v4/zones/<ZONE_ID>/dns_records?type=CNAME&name=subdomain.example.com" \
  -H "Authorization: Bearer <API_TOKEN>"
```

### Delete a record

```bash
curl -X DELETE "https://api.cloudflare.com/client/v4/zones/<ZONE_ID>/dns_records/<RECORD_ID>" \
  -H "Authorization: Bearer <API_TOKEN>"
```

## Bot-to-bot communication relay

When two Telegram bots (Hermes + another) need to collaborate but Telegram blocks bot-to-bot message delivery, use an **HTTP relay**:

### Architecture

```
Bot A ──POST /relay──→ Relay Server ──GET /relay──→ Bot B
                       (saves to JSON)
```

### Minimal relay server (Python stdlib)

```python
import http.server, json, time, os, urllib.parse
from datetime import datetime

DATA_FILE = "relay_messages.json"

class RelayHandler(http.server.BaseHTTPRequestHandler):
    def _send_json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)
    
    def do_GET(self):
        path = urllib.parse.urlparse(self.path).path.rstrip("/")
        if path == "/relay":
            msgs = json.load(open(DATA_FILE)) if os.path.exists(DATA_FILE) else []
            # ?since=ID for incremental reads
            params = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            since = params.get("since", [None])[0]
            if since:
                msgs = [m for m in msgs if m.get("id", 0) > int(since)]
            self._send_json({"ok": True, "count": len(msgs), "messages": msgs})
        elif path == "/relay/health":
            self._send_json({"status": "ok"})
        else:
            self._send_json({"error": "not_found"}, 404)
    
    def do_POST(self):
        path = urllib.parse.urlparse(self.path).path.rstrip("/")
        if path == "/relay":
            data = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))))
            msgs = json.load(open(DATA_FILE)) if os.path.exists(DATA_FILE) else []
            new_id = (msgs[-1]["id"] + 1) if msgs else 1
            entry = {"id": new_id, "bot": data["bot"], "msg": data["msg"], "ts": datetime.now().isoformat()}
            msgs.append(entry)
            json.dump(msgs, open(DATA_FILE, "w"), ensure_ascii=False, indent=2)
            self._send_json({"ok": True, "id": new_id, "message": entry}, 201)

http.server.HTTPServer(("0.0.0.0", 9877), RelayHandler).serve_forever()
```

### Expose via Cloudflare tunnel

Add to tunnel ingress:
```yaml
- hostname: bot.yourdomain.com
  service: http://localhost:9877
```

Then create DNS CNAME:
```
bot.yourdomain.com → <TUNNEL_UUID>.cfargotunnel.com
```

### Relay API

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/relay` | Write `{"bot": "Name", "msg": "..."}` |
| `GET` | `/relay` | Read all messages |
| `GET` | `/relay?since=ID` | Read messages newer than ID |
| `GET` | `/relay/health` | Health check |

### Client usage

```python
# Write
requests.post("https://bot.yourdomain.com/relay",
    json={"bot": "Hermes", "msg": "Hello!"})

# Read (incremental)
requests.get("https://bot.yourdomain.com/relay?since=5")

# Poll loop (30s interval)
import time
last_id = 0
while True:
    msgs = requests.get(f"https://bot.yourdomain.com/relay?since={last_id}").json()["messages"]
    for m in msgs:
        if m["bot"] != "me":
            print(f"[{m['ts']}] {m['bot']}: {m['msg']}")
            last_id = m["id"]
    time.sleep(30)
```

## Key distinctions

| Aspect | Local YAML config | Cloudflare-side config |
|--------|------------------|----------------------|
| Config file | `~/.cloudflared/<name>.yml` | Stored on Cloudflare edge |
| Update method | Edit YAML + restart tunnel | PUT via API (tunnel picks up without restart) |
| Detection | `config_src: local` in tunnel info | `config_src: cloudflare` in tunnel info |
| Override priority | API config overrides local YAML | Always use the one with `config_src` |
| Crash resilience | Config file stays, re-read on restart | Cloudflare persists, re-read on restart |

## Pitfall: DNS route creates record under wrong zone

`cloudflared tunnel route dns <tunnel> sub.domain.com` can create the record under the **wrong Cloudflare zone** when the account has multiple zones. The CLI may output `Added CNAME sub.domain.com.otherzone.com` — a concatenated hostname.

**Fix:** Always manage DNS via the Cloudflare API with explicit zone ID:

```python
import requests
TOKEN = "<api-token>"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

# 1. Get zone ID by exact domain name
zones = requests.get("https://api.cloudflare.com/client/v4/zones?name=domain.com", headers=HEADERS)
zone_id = zones.json()["result"][0]["id"]

# 2. Create CNAME
record = {
    "type": "CNAME", "name": "sub",
    "content": "<tunnel-uuid>.cfargotunnel.com",
    "ttl": 1, "proxied": True
}
r = requests.post(f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records",
    headers=HEADERS, json=record)
print("OK" if r.json().get("success") else r.text)
```

**Prevention:** Verify with: `nslookup sub.domain.com` — should resolve to Cloudflare IPs (104.x / 172.x), not a concatenated hostname.
