---
name: cloudflare-tunnel
title: Cloudflare Tunnel Management (Windows)
description: Manage Cloudflare tunnels on Windows — create, configure, DNS, API-based vs local config, crash recovery, and multi-tunnel orchestration.
tags:
  - cloudflare
  - tunnel
  - dns
  - windows
  - networking
  - cloudflared
domain: devops
---

# Cloudflare Tunnel Management (Windows)

Manage Cloudflare tunnels (`cloudflared`) on a Windows host running git-bash (MSYS2). Covers setup, configuration, DNS management, crash recovery, and the critical distinction between **local YAML config** vs **Cloudflare-side API config**.

## Architecture

```
Browser ──HTTPS──→ Cloudflare Edge ──tunnel──→ cloudflared ──HTTP──→ localhost:PORT
                          │
                    [DNS CNAME]
                    bot.domain.com ──CNAME──→ tunnel-id.cfargotunnel.com
```

**Key insight:** cloudflared can source its ingress rules from **two places**, and they DO NOT mix:

| Config Source | How to set | Lives where | Updated how |
|--------------|-----------|-------------|-------------|
| **Local YAML** (`--config file.yml`) | `cloudflared tunnel run --config path` | Local file system | Edit YAML + restart tunnel |
| **Cloudflare API** (`config_src: cloudflare`) | `PUT /accounts/{id}/cfd_tunnel/{id}/configurations` | Cloudflare servers | API call (tunnel auto-loads) |

**When you pass `--config`, cloudflared checks:** If the tunnel has `config_src: cloudflare` on Cloudflare's servers, it IGNORES the local YAML and uses the API-side config instead. To force local config, you must clear the API-side config (set it to empty ingress + `{"warp-routing":{"enabled":false}}`).

## Diagnosis: Which config is active?

**Important:** `cloudflared tunnel info <TUNNEL_ID>` shows the tunnel name and connections — it does NOT show `config_src`. Always use the API:

```bash
# ✅ Shows config_src (cloudflare vs local)
curl -s https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/cfd_tunnel/{TUNNEL_ID} \
  -H "Authorization: Bearer {API_TOKEN}"
# Response has: "config_src": "cloudflare" | "local"

# ✅ Shows full live config (ingress rules + version number)
curl -s https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/cfd_tunnel/{TUNNEL_ID}/configurations \
  -H "Authorization: Bearer {API_TOKEN}"
# Response has "version": N (increments on each PUT), "config": {"ingress": [...]}
```

**Check tunnel logs for config loading at startup:**
```
"Updated to new configuration config=... version=12"
```
This log line means API-side config was loaded (version matches the API).
If absent, the tunnel is likely reading a local YAML (check `--config`).

## Authentication

### Required credentials

You need a **Cloudflare API token** with these permissions:
- `Account > Cloudflare Tunnel > Edit`
- `Zone > DNS > Edit`

Where to find it:

| Location | File | Format |
|----------|------|--------|
| **cert.pem** | `~/.cloudflared/cert.pem` | Base64-encoded Argo Tunnel token |
| **Decoded from cert.pem** | Parse the token | JSON with `zoneID`, `accountID`, `apiToken` |
| **Hermes terminal cache** (fallback) | `~/AppData/Local/hermes/cache/terminal/hermes-results/call_*.txt` | Plaintext of every command env that ever ran — grep for the token prefix |

**When the env var is gone mid-session** (e.g. `$CLOUDFLARE_API_TOKEN` empty), recover it from Hermes' own terminal cache instead of asking the user:
```bash
grep -rh "cfut_" ~/AppData/Local/hermes/cache/terminal/hermes-results/*.txt | grep -o "cfut_[a-zA-Z0-9]*" | sort -u | head
export CLOUDFLARE_API_TOKEN="cfut_..."
```
(Works for `cfut_` tokens that were ever exported in a previous terminal call. If the token has been rotated, the API returns `{"code": 10000, "message": "Authentication error"}` — then ask the user for a fresh one.)

```bash
# Decode API token from cert.pem
python -c "
import json, base64
with open(r'C:\Users\<USER>\.cloudflared\cert.pem') as f:
    content = f.read()
b64 = content.replace('-----BEGIN ARGO TUNNEL TOKEN-----', '') \
    .replace('-----END ARGO TUNNEL TOKEN-----', '') \
    .strip().replace('\n', '')
data = json.loads(base64.b64decode(b64).decode())
print('ZoneID:', data.get('zoneID'))
print('AccountID:', data.get('accountID'))
print('APIToken:', data.get('apiToken', '')[:30] + '...')
"
```

## API-based tunnel config management (preferred)

### Get current config

```python
import requests
API = f'https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/cfd_tunnel/{TUNNEL_ID}/configurations'
r = requests.get(API, headers={'Authorization': f'Bearer {API_TOKEN}'})
config = r.json()['result']['config']
```

### Update config (add a new ingress rule)

```python
# 1. GET current config
# 2. Add new rule before the catch-all (http_status:404)
current_config = {
    'ingress': [
        # ... existing rules ...
        {'service': 'http://localhost:9877', 'hostname': 'bot.domain.com'},
        {'service': 'http_status:404'}  # catch-all MUST be last
    ],
    'warp-routing': {'enabled': False}
}

# 3. PUT updated config
r = requests.put(API,
    headers={'Authorization': f'Bearer {API_TOKEN}', 'Content-Type': 'application/json'},
    json={'config': current_config}
)
# Expect: status 200, success: true
```

**Rules:**
- The catch-all (`http_status:404`) **must be last** in the ingress array
- Hostnames must be exact match (not wildcard)
- After PUT, the running tunnel picks up the new config within ~30s — NO restart needed
- Version number auto-increments; tunnel shows "Updated to new configuration" in logs

### Add DNS CNAME record

```bash
# Via cloudflared CLI (if zone is managed by same Cloudflare account)
cloudflared tunnel route dns <TUNNEL_ID> <hostname.domain.com>

# OR via API directly:
curl -X POST https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records \
  -H "Authorization: Bearer {API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "CNAME",
    "name": "subdomain",
    "content": "<TUNNEL_ID>.cfargotunnel.com",
    "ttl": 1,
    "proxied": true
  }'
```

**DNS propagation:** Cloudflare DNS updates are instant within Cloudflare's network. External resolvers take 1-5 minutes for new records.

## Local YAML config (alternative)

```yaml
# ~/.cloudflared/my-tunnel-config.yml
tunnel: <TUNNEL_UUID>
credentials-file: C:\Users\<USER>\.cloudflared\<TUNNEL_UUID>.json

ingress:
  - hostname: app.domain.com
    service: http://localhost:3000
  - hostname: api.domain.com
    service: http://localhost:8765
  - service: http_status:404
```

**⚠️ Critical detail:** Paths in the YAML must use Windows backslash style (`C:\Users\...`). MSYS2 paths (`/c/Users/...`) will fail with "The system cannot find the path specified" because `cloudflared.exe` is a Windows-native binary.

Run with:
```bash
# Use Windows-native path in quotes
/c/Program\ Files\ \(x86\)/cloudflared/cloudflared.exe tunnel \
  --config "C:\Users\<USER>\.cloudflared\my-tunnel-config.yml" run --protocol http2
```

## Start a tunnel (background)

```bash
# Use background=true — tunnel is a long-lived process
terminal(background=true, command='...cloudflared.exe tunnel --config "..." run --protocol http2')
```

**Why `--protocol http2`:** Default protocol (QUIC) can have connectivity issues on some networks. HTTP/2 is more reliable, especially on networks with strict firewalls (Vietnam, China, etc.).

## Tunnel crash recovery

**Symptom:** Tunnel runs for minutes/hours then exits with code 1. Logs show:
```
ERR failed to serve incoming request error="connection with edge closed"
WRN Connection terminated error="DialContext error: dial tcp [...]:7844: i/o timeout"
```

**Root cause:** Network instability between the Windows host and Cloudflare edge. Common on:
- Vietnamese ISPs (FPT, VNPT, Viettel)
- WiFi connections with packet loss
- IPv6 transition networks (6to4/Teredo)

**Cannot fix from cloudflared side** — the root cause is network connectivity. Mitigations:

### WARP conflict (WARP disconnects when both tunnel and WARP run)

When **Cloudflare WARP** is also running on the same machine, cloudflared tunnel connections are **interrupted within seconds** — the error log shows:

```
ERR already connected to this server, trying another address
ERR Connection terminated error="dial tcp [...]:7844: i/o timeout"
```

The two Cloudflare services (WARP VPN + cloudflared tunnel) compete for connections to Cloudflare edge, and **the tunnel loses** — WARP's VPN routing breaks cloudflared's QUIC/HTTP2 control connections.

**Fix:** Disconnect WARP before starting the tunnel. Use QUIC protocol after WARP is off for best stability:

```bash
"c:/Program Files/Cloudflare/Cloudflare WARP/warp-cli.exe" disconnect
sleep 3
cloudflared tunnel --config "..." run --protocol quic
```

**Detection:** If the tunnel connects momentarily (shows "Registered tunnel connection") then immediately drops all connections with "already connected" errors, WARP is the first thing to check.

**Symptom signature: service RUNNING but tunnel has 0 edge connections (HTTP 530 / "unable to resolve").** Cloudflare reports a tunnel-as-live page ("host configured as a Cloudflare Tunnel, currently unable to resolve it") or every tunneled hostname returns HTTP 530 even though:
- DNS CNAME exists and resolves to 104.21.x / 172.67.x,
- the tunnel config has the correct ingress (`hostname -> localhost:PORT`),
- the local origin on that port responds fine (localhost 200/307),
- `sc query cloudflared` says `STATE: 4 RUNNING` and the process exists.

Tunnel API `connections` count is the decisive check — if the tunnel template returns `"connections": 0` while the origin and DNS are fine, the tunnel is effectively dead despite the service showing RUNNING. Top cause on this host: **WARP re-connected** (kills edge connections silently). Fix verified Aug 2026: disconnect WARP, then restart the token service:

```bash
# check connections count (decisive): 0 = dead edge, regardless of service state
curl -s "https://api.cloudflare.com/client/v4/accounts/$ACC/cfd_tunnel/$TUNNEL_ID" \
  -H "Authorization: Bearer $CF_TOKEN" | python -c "import sys,json; print('connections:', len(json.load(sys.stdin)['result'].get('connections',[])))"

# fix: disconnect WARP + restart the token service (goto the API-count check again)
"/c/Program Files/Cloudflare/Cloudflare WARP/warp-cli.exe" disconnect
powershell -Command "Stop-Service cloudflared -Force -ErrorAction SilentlyContinue; Start-Sleep 2; Start-Service cloudflared; Start-Sleep 6; (Get-Service cloudflared).Status"
sleep 8   # allow re-registration, then re-check: connections should be >0 and hostnames serve again
```

Restart via the Windows service is safe here because this is a **token-managed** tunnel (`tunnel run --token`); do NOT `taskkill /IM cloudflared.exe` blindly if the tunnel is a service — restart the service instead.

**Monitoring:** Set up a cron health check script that:
1. Checks tunnel health (curl one of the tunneled domains) **AND the edge-connections count via the CF API** — either signal healthy is enough.
2. If unhealthy AND WARP is connected → disconnect WARP + restart tunnel
3. `None`/dropped CF API response during the check is "unknown", NOT a failure — skip the fix pass so a slow API call can't false-restart a healthy tunnel.
4. Outputs only on failure (silent-on-success pattern)

See `cron-job` skill's `Silent-on-success watchdog` pattern for the template.

### Option A: Watchdog script (recommended)

```python
# watchdog-tunnel.py — run as cron job every 5 minutes
import subprocess, time, requests

TUNNEL_NAME = "firstonly"
# Check if tunnel process exists and domain responds
try:
    r = requests.get("https://me.domain.com/", timeout=10)
    if r.status_code == 200:
        exit(0)  # healthy
except:
    pass

# Tunnel is down — restart
subprocess.run(["taskkill", "/F", "/IM", "cloudflared.exe"], capture_output=True)
time.sleep(3)
subprocess.Popen([
    r"C:\Program Files (x86)\cloudflared\cloudflared.exe",
    "tunnel", "--config", f"C:\Users\<USER>\.cloudflared\{TUNNEL_NAME}-config.yml",
    "run", "--protocol", "http2"
])
```

### Option B: Accept periodic restarts

The tunnel self-heals when network recovers. Users may see brief downtime during reconnection intervals (~30-60s).

## Kill a tunnel process

**Critical:** Windows-native `cloudflared.exe` processes are OUTSIDE the git-bash/MSYS2 process tree. `kill -9` from bash will FAIL silently.

```bash
# ✅ WORKS — Windows-native process management
cmd.exe /c "taskkill /F /IM cloudflared.exe"

# ✅ Also works per PID
cmd.exe /c "taskkill /F /PID <PID>"

# ❌ DOES NOT WORK — bash reports success but process survives
kill -9 <PID>
```

**⚠️ taskkill /F /PID can SILENTLY FAIL on Console-session cloudflared** — returns exit 0 but the process survives (`tasklist | grep cloudflared` still shows it). Reliable fallback (verified on this host):
```bash
powershell -Command "Stop-Process -Id <PID> -Force; Start-Sleep 2; Get-Process cloudflared -ErrorAction SilentlyContinue"
```
Service-session PIDs are protected — if the target is the Windows service, tell the user to run `sc stop cloudflared` as Admin instead of force-killing.

**⚠️ MSYS mangling: `taskkill //F //PID` FAILS in git-bash** — MSYS translates `//F` to a path, giving `ERROR: Invalid argument/option - '//F'`. Use the single-dash form in bash (still reaches Windows taskkill), or route through cmd.exe:
```bash
taskkill -F -PID <PID>              # ✅ single-dash works in git-bash
cmd.exe /c "taskkill /F /PID <PID>" # ✅ also works
```

## Restart sequence after config change

When you update the tunnel config (either YAML or API), you DON'T need to restart if using API-based config (tunnel picks it up within ~30s). If you MUST restart:

```bash
# Step 1: Kill all tunnel processes
cmd.exe /c "taskkill /F /IM cloudflared.exe"
sleep 3

# Step 2: Start both tunnels (if multi-tunnel setup)
# First tunnel
terminal(background=true, command='... tunnel --config "config1.yml" run')
# Second tunnel
terminal(background=true, command='... tunnel --config "config2.yml" run')

# Step 3: Verify all domains
for domain in domain1.com domain2.com; do
  curl -s -o /dev/null -w "HTTP %{http_code}\n" --max-time 10 https://$domain/
done
```

## Multi-tunnel setup (separate tunnels for separate domains)

Some setups need separate tunnels for different groups of domains. Example:

```yaml
# firstonly-config.yml — tunnel: 0ce9aa47-... (TQUANG-DELL)
# Handles: thefirstonly.com, me.thefirstonly.com, bot.thefirstonly.com, ...

# theliems-config.yml — tunnel: 1a837010-... (theliems)
# Handles: theliems.com, www.theliems.com
```

Each tunnel runs as a separate `cloudflared.exe` process and maintains its own connections to Cloudflare edge.

## Slow / erratic tunnel performance — localize with benchmark

When the user reports the tunneled site "loads 3-4s per click" / "chậm vãi", do NOT blame the app first:

1. **Benchmark localhost first** (5 requests):
   ```bash
   for i in 1 2 3 4 5; do curl -s -o /dev/null -w "req$i: TTFB %{time_starttransfer}s | Total %{time_total}s\n" http://localhost:PORT/login; done
   ```
2. **Benchmark via tunnel** with full timing breakdown:
   ```bash
   for i in 1 2 3 4 5; do curl -s -o /dev/null -w "req$i: DNS %{time_namelookup}s | TLS %{time_appconnect}s | TTFB %{time_starttransfer}s | Total %{time_total}s\n" https://sub.domain.com/login; done
   ```
   - localhost fast (5-20ms) + tunnel erratic (1-13s, TLS 0.6-10s) → the problem is the machine→Cloudflare-edge path, NOT the app/container.

3. **TWO cloudflared processes running the SAME tunnel is a top cause of erratic slowness.** A manually-started `cloudflared tunnel --config ... run --protocol quic` (Console session) PLUS a cloudflared Windows service (Services session) serving the same tunnel compete for edge connections → TLS handshakes 10x slower and wildly inconsistent.

   **Detection:**
   ```bash
   powershell -Command "Get-CimInstance Win32_Process -Filter \"Name='cloudflared.exe'\" | Select-Object ProcessId, CommandLine | Format-List"
   sc query cloudflared                    # service present?
   netstat -ano | grep <PID> | grep ESTABLISHED   # which PID actually holds connections to localhost ports
   ```
   The service PID often shows blank CommandLine but ESTABLISHED connections to the local services; the manual one shows the full `--config ... run` command.

   **Fix:** kill the MANUAL instance, keep the service (API-side config auto-loads new ingress in ~30s, no restart needed). Before starting ANY manual cloudflared, run `sc query cloudflared` — if a service already exists, do NOT duplicate it.

4. **WARP conflict** (see Pitfalls): `warp-svc.exe` running alongside the tunnel ruins TLS handshakes. `warp-cli disconnect` works from a NON-admin git-bash shell:
   ```bash
   "/c/Program Files/Cloudflare/Cloudflare WARP/warp-cli.exe" disconnect
   "/c/Program Files/Cloudflare/Cloudflare WARP/warp-cli.exe" status   # → "Disconnected"
   ```

5. **Switching the service protocol** QUIC → HTTP/2 (more reliable on strict-firewall networks: VN ISPs, etc.) needs admin: `cloudflared service uninstall && cloudflared service install && net start cloudflared`. Non-admin shell cannot do this — give the user the exact Admin-terminal commands.

## Adding a named subdomain to a token-service tunnel (verified Aug 2026)

The Cloudflared **Windows service** (`sc query Cloudflared` → `BINARY_PATH_NAME: ... tunnel run --token eyJ...`) runs a token-managed tunnel. **Editing `~/.cloudflared/config.yml` does NOT work for this tunnel** — token-mode tunnels ignore local YAML entirely; their ingress lives on the Cloudflare side (dashboard / API `config_src: cloudflare`). Verified Aug 2026: added hostname to config.yml + restarted service → hostname still HTTP 530.

**Do NOT go down the config.yml + restart-service path for a token-managed tunnel.** Two working approaches exist:

**Approach A (zero-new-tunnel, verified Aug 2026):** if the token tunnel has `config_src: cloudflare` (check via the API — the service-managed token tunnel on this host does), extend it directly with the **API PUT** path from the "API-based tunnel config management" section: GET current config → merge `{"hostname": "sub.domain.com", "service": "http://localhost:PORT"}` before the catch-all → PUT → tunnel reloads in ~30s. No new tunnel, no restart, no credentials file. Used to add `dithi.thefirstonly.com → localhost:5100` to the TQUANG-DELL service tunnel (v27→v28, verified). Ready-made helpers: `scripts/add-cf-ingress.py` and `scripts/add-cf-dns.py`.

**Approach B (separate local-managed tunnel)** — use only when the token tunnel is NOT API-managed (config_src: local/unknown):

```bash
# 1. Create a NEW tunnel (local-managed, credentials file written)
"/c/Program Files (x86)/cloudflared/cloudflared.exe" tunnel create <name>
# → credentials written to C:\Users\<USER>\.cloudflared\<UUID>.json, "Created tunnel <name> with id <UUID>"

# 2. Route DNS — will FAIL with code 1003 if a CNAME for that hostname already exists:
#    "An A, AAAA, or CNAME record with that host already exists"
#    Fix: delete the existing record via API FIRST (see DNS record cleanup below), then re-run:
cloudflared tunnel route dns <UUID> <hostname.domain.com>

# 3. Write a dedicated config (Windows backslash paths — see Local YAML section)
#    tunnel: <UUID>
#    credentials-file: C:\Users\<USER>\.cloudflared\<UUID>.json
#    ingress:
#      - hostname: <hostname.domain.com>
#        service: http://127.0.0.1:<PORT>
#      - service: http_status:404

# 4. Run as a background process (NOT via the token service — separate process is fine,
#    it's a different tunnel so no duplicate-connection conflict)
cloudflared tunnel --config "C:\Users\<USER>\.cloudflared\<name>-config.yml" run <UUID>
```

**Delete an existing CNAME before re-routing (code 1003 fix):**
```bash
# Get token from cert.pem (see Authentication section) → $API_TOKEN
# 1. Find the record
curl -s -X GET "https://api.cloudflare.com/client/v4/zones/$ZONE/dns_records?name=<hostname.domain.com>" \
  -H "Authorization: Bearer $API_TOKEN" | python -c "import sys,json; [print(r['id'], r['type'], r['name']) for r in json.load(sys.stdin)['result']]"
# 2. Delete it (record ID from step 1)
curl -s -X DELETE "https://api.cloudflare.com/client/v4/zones/$ZONE/dns_records/<RECORD_ID>" \
  -H "Authorization: Bearer $API_TOKEN"   # → {"success": true}
# 3. Now `cloudflared tunnel route dns <UUID> <hostname>` works
```

**Diagnostic: HTTP 530 = DNS routed but tunnel not serving that hostname yet.**
CNAME resolves and hits Cloudflare edge, but the running tunnel hasn't loaded the ingress rule. For a local-managed tunnel: check the process picked up `--config` correctly (log shows "Registered tunnel connection"). For a token-managed service: config.yml edits will NEVER take effect — create a local-managed tunnel instead.

**Do NOT try `cloudflared tunnel run <TUNNEL_ID>` for a token-managed tunnel** — fails with `Unauthorized: Tunnel not found`. Token-managed tunnels (service installed via `cloudflared service install <TOKEN>`) must run via `tunnel run --token`, not by ID. (But creating a NEW local-managed tunnel and running it by ID works fine — that's the recommended path.)

## Verify tunnel health

```bash
# Layer 1: Process exists
ps aux | grep cloudflared | grep -v grep

# Layer 2: Local origin responds
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:PORT/

# Layer 3: Via tunnel (external)
curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://domain.com/

# Layer 4: DNS resolves to Cloudflare IPs
nslookup domain.com | grep -E "104\.21\.|172\.67\.|2606:4700:"
```

## Pitfalls

### config_src: cloudflare overrides local YAML
If the tunnel has API-side config, passing `--config` is IGNORED. Always check `config_src` first. To force local YAML, clear the API config first.

### New ingress rules take 30s to propagate after API PUT
The running tunnel prints "Updated to new configuration" when it picks up changes. Don't restart — wait 30s and verify.

### Catch-all must be last
If `http_status:404` is NOT the last ingress rule, rules after it are unreachable. The tunnel doesn't warn about this.

### Universal SSL covers only 1-level subdomains — 2-level subdomains fail TLS
`*.domain.com` is covered, but `upload.html.domain.com` / `result.uploadhtml.domain.com` (2 levels) fail TLS handshake until a cert exists. Symptom: DNS resolves to Cloudflare IPs, tunnel routes (other hostnames fine), but curl exits 35 with `SEC_E_ILLEGAL_MESSAGE` / `schannel: next InitializeSecurityContext failed`; `--resolve` to the edge IP gives the same. A 1-level subdomain (`uploadhtml.domain.com`) on the SAME zone+tunnel works immediately — the cert is the only difference.

Fixes:
- **Total TLS** (zone → SSL/TLS → Total TLS): covers all subdomain levels. BUT the tunnel+DNS token cannot enable it — `PATCH /zones/{id}/settings/total_tls` returns `Unauthorized to access requested resource` (needs SSL/TLS settings permission). Ask the user to toggle it in the dashboard, or use a fuller token.
- **Use a 1-level domain** instead — zero config, works now.

Diagnosis:
```bash
curl -s -o /dev/null -w "%{http_code}\n" --max-time 25 --resolve "upload.html.domain.com:443:104.21.1.191" https://upload.html.domain.com/
# TLS error = cert missing (2-level + no Total TLS) → switch to 1-level or enable Total TLS
# 404      = cert OK, but no ingress rule for this hostname → check tunnel config
```

### taskkill /F /IM kills ALL cloudflared.exe processes
If you have multiple tunnels (firstonly, theliems), they ALL die. Use `/PID` for targeted kills.

### `cloudflared tunnel route dns` can route to wrong zone
When using `cloudflared tunnel route dns`, the CNAME may be added to the **first zone found** in the authenticated account. If the account manages multiple domains, the record may get appended to the wrong zone (e.g., `bot.domain1.com.domain2.com`).

**Fix:** Use the Cloudflare API with the correct ZONE_ID instead:
```bash
curl -X POST https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records \
  -H "Authorization: Bearer {API_TOKEN}" \
  -d '{"type":"CNAME","name":"subdomain","content":"<TUNNEL_ID>.cfargotunnel.com","proxied":true}'
```
Find ZONE_ID via: `GET /zones?name=<domain>` with the same auth header.
If you have multiple tunnels (firstonly, theliems), they ALL die. Use `/PID` for targeted kills.

### cert.pem zoneID may be a DIFFERENT zone than your target domain (API variant)
The zoneID decoded from `~/.cloudflared/cert.pem` belongs to whatever zone cert.pem was issued for — often NOT the zone you're adding a record to (this account manages thefirstonly.com AND theliems.com; cert.pem carries theliems.com). POSTing to `zones/{cert.pem-zoneID}/dns_records` with `"name": "kan"` SILENTLY creates `kan.theliems.com` when you wanted `kan.thefirstonly.com` — no error, no warning, the wrong record just appears.

**Rule: never use cert.pem's zoneID for DNS record creation.** Resolve the zone for the EXACT target domain first, then verify the returned record's `name`:
```bash
# 1. Resolve zone ID for the exact domain (NOT cert.pem's zoneID)
curl -s "https://api.cloudflare.com/client/v4/zones?name=thefirstonly.com" \
  -H "Authorization: Bearer $API_TOKEN" | python -c "import sys,json; [print(r['id']) for r in json.load(sys.stdin)['result']]"
# 2. POST the CNAME to THAT zone ID
# 3. Read back the returned "name" field — it tells you which zone you actually wrote to
```

**Cleanup when the wrong record already exists:**
```bash
REC_ID=$(curl -s "https://api.cloudflare.com/client/v4/zones/{WRONG_ZONE_ID}/dns_records?name=kan.theliems.com" -H "Authorization: Bearer $API_TOKEN" | python -c "import sys,json; rs=json.load(sys.stdin)['result']; print(rs[0]['id'] if rs else '')")
curl -s -X DELETE "https://api.cloudflare.com/client/v4/zones/{WRONG_ZONE_ID}/dns_records/$REC_ID" -H "Authorization: Bearer $API_TOKEN"
```

### Flaky network → curl retry for CF API calls
On this host (unstable Vietnamese ISP/Wi-Fi), Cloudflare API calls sometimes return EMPTY bodies — `python -c json.load` then fails with `JSONDecodeError: Expecting value`. That's a dropped connection, not an API error. Wrap every CF API call in:
```bash
curl -s --retry 5 --retry-delay 3 --retry-all-errors --max-time 60 ...
```
Verify `"success": true` in the response before moving on.

### Tunnel API config can be overwritten externally — merge, don't rebuild
Config `version` can jump without your PUT (user edits the Cloudflare dashboard, another session/agent edits). Before PUT, GET the CURRENT config and merge your ingress rule into it — do NOT send a hand-built full config from memory, or you silently drop rules others added. After PUT, verify the returned version AND re-GET to confirm all expected hostnames exist. (Observed: v19 with kan rule → v21 without kan but with new tfo rule → re-merged v22.)

### 404 vs 502 semantics from the tunnel
- HTTP 404 with `Server: cloudflare` and no origin headers = request hit the catch-all `http_status:404` — the hostname has NO ingress rule in the config currently loaded by the tunnel.
- HTTP 502 = ingress rule exists but origin unreachable (wrong port, app down/restarting).
- Decide by code: 404 → check/merge tunnel config; 502 → check the container/origin. Local 200 + tunnel 404 = tunnel config problem, not the app.

### 502 with healthy edge (4 conns) but origin on another machine (verified 2026-09-09: pharma-llm.thefirstonly.com)

If `curl https://host/` → 502 with `Server: cloudflare` + `CF-RAY`, DNS CNAME correct, tunnel shows 4 conns, but `curl http://127.0.0.1:<port>` on YOUR machine is 000 → the ingress owner is a DIFFERENT tunnel/host, not yours. Diagnosis:

1. Resolve CNAME: `GET /zones/{zone}/dns_records?name=host` → `content` = `<tunnel-id>.cfargotunnel.com` → owner tunnel ID.
2. List tunnels: `GET /accounts/{acc}/cfd_tunnel` → find that ID → check `connections` (4 = edge healthy) + `name` (e.g. `pharma-duc-anh`).
3. Get ingress: `GET /accounts/{acc}/cfd_tunnel/{id}/configurations` → `ingress[].hostname` + `service` (e.g. `localhost:8888`).
4. Probe origin on all LAN candidates (`127.0.0.1`, `192.168.1.3`, `192.168.1.110`) on that port → all 000 = origin dead on its own host (Unsloth Studio not running). Conclusion: tunnel healthy, origin dead externally — cannot fix from this host; start service on owner machine. Meanwhile, migrate dependent cron jobs off that endpoint immediately (see `hermes-model-provider-troubleshooting/references/bulk-cron-migration-2026-09.md`).

This case produced 502 `Server: cloudflare` + `Cache-Control: private` + 4 edge conns, ingress `pharma-llm.thefirstonly.com → localhost:8888`, but no process listening on 8888 at any local/LAN host. Tunnel was `32f09491-56b2-40e7-b883-6886d6b2a9ef` (pharma-duc-anh), not TQUANG-DELL or Mac.

### 403 via tunnel + 200 localhost = origin-side allowedHosts block (Vite), NOT a tunnel problem
Symptom: `curl https://sub.domain.com/` → **403** with `Server: cloudflare`, `cf-cache-status: DYNAMIC`, `vary: Origin`, and body **`Blocked request. This host ("sub.domain.com") is not allowed. To allow this host, add ... to preview.allowedHosts in vite.config.js.`** Meanwhile `curl http://127.0.0.1:PORT/` → 200 with real app HTML. 403 persists with a browser User-Agent and under `-I`.

Cause: a Vite dev / `vite preview` server only accepts Host headers in `allowedHosts`, often derived from an env var defaulting to `localhost`. The tunnel forwards `Host: sub.domain.com`; Vite rejects it before the app renders. Looks like a tunnel/DNS/CF problem but is purely the app's host allowlist.

Fix (containerized Vite app, verified on Rakazo edge stack Sep 2026): the compose file maps `allowedHosts` to an env var (`allowedHosts: [process.env.RAKAZO_HOST ?? "localhost"]` in `vite.config.ts`). Set that env to the public hostname and recreate only that service:
```bash
sed -i 's/^RAKAZO_HOST=.*/RAKAZO_HOST=sub.domain.com/' .env
docker compose --env-file .env -f docker-compose.yml up -d web
```
Then 403 → 200, `<title>` renders. For a non-compose Vite app: add the hostname to `allowedHosts` in `vite.config` (or `--allowedHosts`) and restart.

**Tell apart from the CF bot-filter 403** (also `Server: cloudflare`): the bot-filter returns an HTML/empty body and only bites Python/urllib/default UA; the allowedHosts block returns the plain-text `Blocked request...` body at EVERY UA including browsers and `-I`. Read the response body to classify before touching the tunnel.

### Auth origin envs (Better Auth / cookie auth) must point at the PUBLIC domain before signup/login works through the tunnel
Verified on Rakazo (Sep 2026): app's auth worked at localhost but `BETTER_AUTH_URL` / `WEB_ORIGIN` were still `http://127.0.0.1:5173` from the local .env. Any signup/login attempted through the public hostname breaks (CORS/cookie bound to the localhost origin). Fix: change BOTH to `https://<public-domain>`, then recreate EVERY service that uses the .env as `env_file` (api/worker/web — not just web), wait for `docker compose ps` healthy, then create the account. Check `grep -E '^(BETTER_AUTH_URL|WEB_ORIGIN)=' .env` as part of first-account setup for any tunneled app with server-side auth.

### Creating the first account in a React SPA through the tunnel: use browser_type, never set `.value` from JS console
React controlled inputs ignore direct `.value` assignment (state doesn't update) — the form submits with empty fields: zod/API error `[body.email] Invalid email address; [body.password] Too small` even though the fields LOOK filled. Correct flow: navigate to the signup route (may be `/sign-up`, not `/signup`; the landing "Sign up" is often a `<button>` with an onclick, not an `<a>`), `browser_snapshot` for refs, `browser_type` each field (triggers onChange), click submit, then verify the row in the DB container (`docker exec <db> psql ...`).

### curl 000 "could not resolve host" = missing DNS record, NOT a tunnel problem
`curl https://sub.domain/` returning `000` with exit 6 (`could not resolve host`) means the CNAME doesn't exist yet — before touching the tunnel, check DNS records for that zone via API:
```bash
# 1. Resolve zone ID for the exact domain (NOT cert.pem's zoneID)
ZONE=$(curl -s "https://api.cloudflare.com/client/v4/zones?name=kiemion.online" -H "Authorization: Bearer $API_TOKEN" | python -c "import sys,json; [print(r['id']) for r in json.load(sys.stdin)['result']]")
# 2. List CNAMEs — is the subdomain there?
curl -s "https://api.cloudflare.com/client/v4/zones/$ZONE/dns_records?type=CNAME" -H "Authorization: Bearer $API_TOKEN" | python -c "import sys,json; [print(f\"{r['name']} -> {r['content']}\") for r in json.load(sys.stdin)['result']]"
# 3. If missing: POST the CNAME (see "Add DNS CNAME record")
```
DNS propagates in seconds inside Cloudflare, but the system resolver may cache — re-run `nslookup sub.domain` to confirm. (Observed: `erp.kiemion.online` 404→000 until its CNAME was created; tunnel ingress existed the whole time.)

### Next.js 16 behind tunnel: redirects break to localhost — build URL from headers
Next.js 16 does NOT trust proxy headers by default: `request.url` / `request.nextUrl` inside `proxy.ts` and route handlers resolves to the ORIGIN address (`http://localhost:3003`) even when Cloudflare forwards `Host: sub.domain.com`. `NextResponse.redirect(new URL('/', request.url))` then emits `location: https://localhost:3003/` → the browser bounces to localhost. Symptoms: passcode/login redirect "về hết localhost".

**Fixes that DON'T work in Next 16.2:** `experimental.trustHostHeader` (type error — removed from `ExperimentalConfig` type) and relative-path redirects (`NextResponse.redirect('/passcode')` → runtime `ERR_INVALID_URL`; redirect requires absolute URLs).

**Fix that works:** build the base URL manually from proxy headers in both `proxy.ts` and route handlers:
```ts
function getBaseUrl(request: NextRequest): string {
  const host = request.headers.get('x-forwarded-host') || request.headers.get('host') || 'localhost'
  const proto = request.headers.get('x-forwarded-proto') || 'http'
  return `${proto}://${host}`
}
// then: NextResponse.redirect(new URL('/passcode', getBaseUrl(request)))
```
Python http.server handlers avoid the issue entirely with relative `Location: /` (browsers resolve against the current domain). KFlow (Next 16, kflow.thefirstonly.com) is the canonical example.

### HTTP 530 mà tunnel khỏe (conns>0) + DNS/CNAME đúng nhưng hostname không route — CROSS-ACCOUNT
Verified 2026-08. Mọi dấu hiệu "thường" đều xanh:
- CNAME trỏ đúng `tunnel-id.cfargotunnel.com`, DNS resolve ra IP CF (104.21/172.67), cert SSL OK,
- tunnel có `connections`: 4 (edge khỏe), con local-managed mới tạo + `--config` đúng,
- localhost origin 200.

Nhưng `curl https://hostname/` trả **530** (error code 1033), và **metrics tunnel = 0** (`cloudflared_proxy_connect_latency_sum 0`) → edge KHÔNG forward request vào tunnel này.

**Root cause: zone của hostname nằm ở CLOUDFLARE ACCOUNT KHÁC với account tạo tunnel.** CF edge chỉ route hostname tới tunnel khi zone đó cùng account với tunnel. Dấu hiệu nhận biết trước: token quản zone là zone-scoped (`GET /accounts` → success:true result:[]; `GET /memberships` → Authentication error) — không tạo được tunnel trong account đó.

**Kỹ thuật chẩn đoán dứt điểm (control hostname cùng account):** thêm 1 ingress tạm `test.X.thefirstonly.com` (thuộc account TỪNG tạo tunnel) trỏ cùng origin → tạo CNAME → curl:
- control trả **200** + hostname cross-account trả **530** → khẳng định cross-account.
- control cũng **530/404** → vấn đề config tunnel, không phải account.

Không có cách sửa từ phía tunnel (không thể route chéo account bằng ingress/CNAME hợp lệ). 2 hướng cho user:
- **A (làm được ngay):** dùng subdomain của domain cùng account (vd `document.thefirstonly.com`) — chỉ cần ingress + CNAME.
- **B (đúng tên muốn):** user cấp token có quyền `Account > Cloudflare Tunnel > Edit` trong account chứa zone cross-account, tạo tunnel mới ở account đó.

⚠️ `cloudflared tunnel route dns` trên tunnel thuộc account A, hostname thuộc zone account B → tạo nhầm CNAME `hostname.zoneB.<accountA-zone>.com` (cert.pem zone). Nhớ dọn record sai (xem "cert.pem zoneID may be DIFFERENT zone").

### API-created tunnel: credentials-file JSON from the API needs the SAME secret cloudflared expects
`cloudflared tunnel create <name>` writes the credentials `.json` itself (`{AccountTag, TunnelID, TunnelSecret}`). If you create the tunnel via `POST /accounts/{acc}/cfd_tunnel` and hand-build that `.json` yourself, cloudflared fails to start with:
```
ERR Invalid JSON when parsing credentials file: illegal base64 data at input byte N
```
Fix (verified 2026-08):
- Generate the secret as **standard base64 of exactly 32 bytes**, pass THAT string to the API as `tunnel_secret`, and write the SAME string into `TunnelSecret`. Do NOT `urlsafe`/strip padding — cloudflared decodes the credentials `TunnelSecret` itself and rejects `-_`/unpadded forms (`illegal base64 data`). Python check: `len(base64.b64decode(secret)) == 32`.
- The API may also reject a secret containing `_` (JSON deserialize `Invalid symbol 95`) — retry with a fresh `os.urandom(32)` until no `-`/`_` appears.
- Keep env tokens per-session; after editing `vukiem-creds.json` (or any creds file) restart ONLY that tunnel's `cloudflared` process, not the shared service.

### Via-tunnel testing gotchas: edge caches 404s (rename asset to bust) + bot filter 403s Python/urllib
Verified 2026-08 on `document.vuakiem.com` (Node app through a dedicated tunnel):
- **Edge caches a 404 for a static path once it has 404'd.** A new `public/admin.js` returned 404 via the tunnel even after the file existed + server served it 200 locally, because CF edge had cached the earlier 404 for that exact path. `?v=1` / `--resolve` → 200, bare `/path` → 404. And `POST /zones/{id}/purge_cache` returned `401 Authentication error` (token lacked Cache Purge). **Workaround: rename the asset file** (`admin.js` → `admin-app.js`) so the path has no cached 404, update the reference, restart. Do this before chasing phantom server/tunnel bugs.
- **Bot filter returns 403 (non-JSON body) to Python `urllib`/`requests` default user-agent through the tunnel**, while `curl` with the same request works (200/401 JSON). Localhost probes are unblocked. When an API test script through the tunnel gets 403 + empty/HTML body, re-test the same call with `curl`; and keep the automated check on localhost instead of via-tunnel.
- Dict: to be sure a tunneled route truly works end-to-end, curl the exact public URL (GET + POST + a redirect) rather than trusting a localhost-only or urllib-only result.

### Quoted heredoc (`<<'PYEOF'`) KHÔNG substitute shell var → token literal → API fail
Viết script Python gọi CF API qua heredoc QUOTED (đúng chuẩn giữ dấu tiếng Việt) thì `$TOKEN`/`$VAR` trong nội dung KHÔNG được thay → API nhận literal `TOKEN_PLACEHOLDER` → HTTP 400/401. Không nhúng shell var vào heredoc quoted. Pattern đúng: viết script `.py` thật bằng write_file, đọc secret từ `os.environ["CF_TOKEN"]`, chạy `export CF_TOKEN=$(python -c 'decode cert.pem -> apiToken') && python script.py`. (Gặp thật khi thêm ingress dithi 2026 — script heredoc đầu fail, viết file .py riêng qua thì OK.)

## Related skills

- `nextjs-supabase-fullstack` — full-stack deployment to Cloudflare tunnel
- `systematic-debugging` — debugging tunnel connectivity issues
