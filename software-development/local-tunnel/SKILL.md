---
name: local-tunnel
title: local-tunnel
description: Expose a local web server to the internet via tunneling tools so the user (on mobile/Telegram) can access it from any device.
tags:
  - tunnel
  - localtunnel
  - serveo
  - cloudflared
  - public-url
  - dev-server
  - windows
domain: software-development
---

# local-tunnel

Expose a locally-running web server to the internet so the user — who accesses Hermes via Telegram on their phone — can open it on any device.

## When to use

- User asked you to start a web server / file server on the dev machine
- User needs to view an HTML page or web app from their phone
- User shared a `localhost:<port>` URL and said "I can't open this"
- User wants to view a file from a **GitHub private repo** via browser (raw.githubusercontent.com returns 404 for private repos — the only way is to serve locally + tunnel)
- Any "serve and view" workflow targeting a mobile Telegram user

## Available tools on this system

| Tool | Status | Command | URL pattern | How it works |
|------|--------|---------|-------------|-------------|
| **localtunnel** (npm) | ✅ Works | `node /path/to/lt.js --port <port>` (via `terminal(background=true)`) | `https://<name>.loca.lt` | Best dev tunnel on Windows: works silently even when output is invisible. Use a subdomain you choose so you can predict the URL. |
| **cloudflared (named tunnel)** | ✅ Production | `cloudflared tunnel create <name>` → `--config <win-path> run` | `https://<domain>` | Reliable for production. Requires a Cloudflare account + domain in zone. Use with --config and native Windows paths. See workflow below. |
| **cloudflared (quick tunnel)** | ⚠️ Needs `--config ""` | `cloudflared tunnel --url http://localhost:<PORT> --protocol http2 --config ""` | `https://<words>.trycloudflare.com` | Works when `--config ""` is passed to avoid catch-all 404 from existing Cloudflare config (cert.pem loads default ingress with http_status:404). Without the flag, quick tunnels get intercepted by the existing tunnel's catch-all rule. |
| **localtunnel** via npx | ⚠️ Inconsistent on Windows | `npx.cmd localtunnel --port <port>` | `https://<random>.loca.lt` | npx.cmd may hang on Windows git-bash. Use the direct node lt.js path instead. |
| **serveo.net** (SSH) | ⚠️ Inconsistent on Windows | `ssh -R 80:localhost:<port> serveo.net` | `https://<random>.serveo.net` | May produce zero output on Windows git-bash. |

**Default choice:** localtunnel for dev/quick previews; Cloudflare named tunnel for production with a custom domain.

## Workflow

### 1. Ensure the port is free, then start the server

**Proactively check for port conflicts** before starting the target server — don't wait for EADDRINUSE.

```bash
# List all listening ports to find a free one
python -c "
import subprocess, re
r = subprocess.run(['netstat', '-ano'], capture_output=True, text=True)
ports = set()
for line in r.stdout.split('\n'):
    if 'LISTENING' not in line: continue
    parts = line.strip().split()
    if len(parts) >= 5:
        addr = parts[1]
        if ':' in addr:
            port = addr.rsplit(':', 1)[-1]
            if port.isdigit(): ports.add(int(port))
free_ports = sorted(set(range(3000, 3020)) - ports)
print(f'Free ports 3000-3019: {free_ports[:5]}...')
"

# Check a specific port
netstat -ano | grep ":<PORT> " | grep LISTENING

# If EADDRINUSE or port is taken, find the PID and what's using it:
netstat -ano | grep ":<PORT> " | awk '{print "PID:", $NF}'
# Then: tasklist //FI "PID eq <PID>"
# Kill if needed: taskkill //F //PID <PID>
```

### 2. Start the tunnel

#### With localtunnel CLI (simpler, works if lt is in PATH)

```bash
npm install -g localtunnel
lt --port <PORT> --subdomain <your-name>
# URL: https://<your-name>.loca.lt
```

The `lt` CLI tool works in the background and usually shows the URL in the output preview shortly after starting.

#### With localtunnel via direct Node.js path

```bash
# Find the lt.js path first (runs once)
npm root -g
# Output like: C:\\Users\\<user>\\AppData\\Roaming\\npm\\node_modules
# The lt binary: <root>/localtunnel/bin/lt.js

# Start tunnel in background with a predictable subdomain
terminal(background=true, command="node <npm_root>/localtunnel/bin/lt.js --port <PORT> --subdomain <your-name>")
```

The tunnel may show **zero output** in the background process log. **This is normal on Windows git-bash.** Verify by curling the expected URL directly (step 3).

Example:
```bash
# First find the path
npm_root=$(npm root -g)
# Then start — adjust port and subdomain
terminal(background=true, command="node $npm_root/localtunnel/bin/lt.js --port 8765 --subdomain metelligent-demo")
```

The URL will be: `https://<subdomain>.loca.lt` (e.g. `https://metelligent-demo.loca.lt`)

**Important:** Choose a subdomain that's likely unique enough (add a suffix like `-123` or your initials if `--subdomain` returns a conflict error). If you see a random auto-generated URL (`https://random-words-123.loca.lt`) instead of your chosen subdomain, the name is taken — use a different one.

**Recovery from subdomain collision:** Check the tunnel's output preview for the actual URL. The URL shown is what you got — use that, not what you intended. Do NOT retry the same subdomain on the same machine — it will still be reserved.

#### With cloudflared (named tunnel — production)

For a production setup with a custom domain, use a Cloudflare named tunnel. This requires a Cloudflare account with the domain in a zone.

**Step 1:** Create the tunnel
```bash
cloudflared tunnel create <tunnel-name>
# Output: Created tunnel <name> with id <uuid>
# Credentials saved to ~\.cloudflared\<uuid>.json
```

**Step 2:** Create config file using native Windows path
```yaml
# ~\.cloudflared\<name>-config.yml
tunnel: <uuid>
credentials-file: C:\Users\<user>\.cloudflared\<uuid>.json

ingress:
  - hostname: <your-domain.com>
    service: http://localhost:<PORT>
  - hostname: www.<your-domain.com>
    service: http://localhost:<PORT>
  - service: http_status:404
```

**IMPORTANT:** Use native Windows paths (e.g., `C:\Users\...`) in the config file. POSIX paths (`/c/Users/...` or `~/`) will fail with "The system cannot find the path specified" when cloudflared tries to open them.

**Step 3:** Route DNS
```bash
cloudflared tunnel route dns <tunnel-name> <your-domain.com>
```
If DNS records already exist, you'll get error code 1003 "An A, AAAA, or CNAME record with that host already exists". Fix: Delete the existing records in Cloudflare Dashboard → DNS, then rerun the command, OR create a CNAME record manually pointing to `<uuid>.cfargotunnel.com`.

**Step 4:** Run the tunnel
```bash
# Must use native Windows path for --config
cloudflared tunnel --config "C:\Users\<user>\.cloudflared\<name>-config.yml" run
```

The tunnel connects with multiple connections (typically 4) across different Cloudflare PoPs. Verify with:
```bash
# Check tunnel status (must be running first)
cloudflared tunnel info <tunnel-name>
```

**Step 5:** Verify end-to-end
```bash
# Local server check
curl -s -o /dev/null -w "%{http_code}" http://localhost:<PORT>/
# Expected: 200

# Cloudflare DNS propagation may take a minute. Test via:
curl -s -o /dev/null -w "%{http_code}" https://<your-domain.com>/ --connect-timeout 15
```

**Troubleshooting:**
- "Failed to add route: code 1003" → DNS record already exists, delete it in Cloudflare Dashboard first
- "open ... The system cannot find the path specified" → config path must be native Windows style (C:\Users\...)
- "Invalid project directory provided" when using `pnpm start -- --port X` → Next.js doesn't accept `--port` as a pnpm arg. Use `PORT=X npx next start -p X` instead.

```bash
# WARP must be OFF — cloudflared QUIC/HTTP2 won't connect through WARP
warp-cli disconnect

# Do NOT add --protocol http2 — auto-detect (QUIC) connects faster on most networks
# Use tee to capture URL (background output invisible on Windows git-bash):
terminal(background=true, command="cloudflared tunnel --url http://localhost:<PORT> 2>&1 | tee /c/Users/NTQUANG_DELL/tunnel_url.txt")
```

Then wait ~15-30s and check the URL file:
```bash
grep "trycloudflare.com" /c/Users/NTQUANG_DELL/tunnel_url.txt
```

If that's empty, wait another 15s and retry. If still empty, verify the local server is up and try without `--protocol http2` (omit the flag entirely).

#### With localtunnel via npx.cmd (last resort)

```bash
terminal(background=true, command="npx.cmd localtunnel --port <PORT>")
```

Same caveat: output may be invisible on Windows. Verify via curl.

### 3. Verify the tunnel works

```bash
# For localtunnel (predictable URL via --subdomain):
curl -s -o /dev/null -w "%{http_code}" --connect-timeout 10 "https://<your-subdomain>.loca.lt/<path>"
# Expect: 200

# For cloudflared (random subdomain — verify by checking process log):
process(action="log", session_id="<proc_id>")
# Look for "https://<words>.trycloudflare.com" in the output
```

If curl fails with a timeout, the tunnel may need a few more seconds to propagate. Retry once.

### 4. Deliver the URL to the user

```
👉 **https://<your-subdomain>.loca.lt**
```

If the file is from a **GitHub private repo**, note to the user why raw.githubusercontent.com didn't work — private repos block raw content access, so the local tunnel is the intended solution.

## Pitfalls & Troubleshooting

### 🚨 SECURITY: Python http.server exposes full directory listing

**Symptom:** You run `python -m http.server <PORT>` to serve static files, then expose it via a tunnel. Visitors see a complete directory listing of the project root — including `.env.local`, `.git/`, source code, config files, and secrets.

**Why it happens:** Python's built-in `http.server` (SimpleHTTP) defaults to **directory listing mode**. When no `index.html` exists, it lists every file in the served directory. A tunnel makes this publicly accessible.

**Fix immediately:**
```bash
# Kill the Python http.server — never use it behind a tunnel
taskkill /F /PID <PID>

# For quick static serving, use a proper single-page server:
python -m http.server 3000 --directory /path/to/public/  # only serves /public/
# OR use 'serve' npm package:
npx serve -s /path/to/public/ -p 3000  # -s = single-page mode, no listing
```

**Prevention checklist before exposing any server via tunnel:**
- [ ] Is the server production-grade (Next.js, Express, Nginx) and NOT Python `http.server`?
- [ ] If using Python `http.server`, does the directory have an `index.html`?
- [ ] Is there a `.env`, `.git/`, or any sensitive file in the served directory?
- [ ] Does the server bind to `127.0.0.1` (local only) or `0.0.0.0` (all interfaces)?
- [ ] Have you verified the content served through the tunnel, not just locally?

**Verification:**
```bash
# Check locally — don't trust local, verify through tunnel
curl -sI http://localhost:<PORT>/ | grep -i "content-type"
# If "text/html" with directory listing → unsafe

# Check through tunnel (if running)
curl -sI https://<tunnel-url>/ | grep -i "content-type"
# Same check — if you see directory listing, fix immediately
```

**Caveat about `--bind 127.0.0.1`:** Binding to localhost alone does NOT secure a tunneled server. Cloudflare tunnel connects *outbound* to Cloudflare's edge, so the binding only blocks direct HTTP traffic to the port, not tunnel traffic. The tunnel bypasses the bind restriction entirely.

### 🚨 TROUBLESHOOTING: Tunnel serves wrong content — multiple tunnels conflict

**Symptom:** You configured a tunnel to point `yourdomain.com → localhost:PORT_A`, but `https://yourdomain.com/` shows content from a *different* port (`PORT_B`). The cloudflare tunnel process appears to be running with the right config, but traffic goes elsewhere.

**Root cause:** Multiple cloudflared tunnels may be registered at the Cloudflare edge, and the **DNS record** for your domain still points to a different tunnel's CNAME (`<old-tunnel-uuid>.cfargotunnel.com`). The tunnel you just started may:
- Use a different tunnel UUID than what the DNS CNAME points to
- Point to a different config file than expected
- Be a newly created tunnel that hasn't had DNS routed to it yet

**Diagnosis — 4 steps:**

**Step 1: List all running cloudflared processes and their config files**

On **Linux/macOS** (or WSL):
```bash
# Find all cloudflared PIDs
ps aux | grep cloudflared | grep -v grep

# Check each one's command line to see which config it's using
for pid in $(pgrep cloudflared); do
  echo "PID $pid: $(cat /proc/$pid/cmdline | tr '\0' ' ')"
done
```

On **Windows git-bash (MSYS2)**: `/proc/<PID>/cmdline` works only for processes started in the same MSYS2 session. For Windows-native processes (started by Task Scheduler, direct CLI, or Explorer), fall back to `wmic`:
```bash
# List all cloudflared processes
ps -W | grep cloudflared

# Get command lines via wmic
wmic process where "name like '%cloudflared%'" get processid,commandline /format:list

# Or check a specific PID
wmic process where "processid=<PID>" get commandline /format:list

# For MSYS2-spawned processes only, /proc works:
cat /proc/<PID>/cmdline 2>/dev/null | tr '\0' ' '
```

**Key distinction:** If `wmic` returns an empty commandline AND `/proc/<PID>/cmdline` doesn't exist, the process may be a child of a different session or a Windows service — use `tasklist //V` / `tasklist //FI "PID eq <PID>"` for extra info.

**Step 2: List all registered tunnels with connection status**
```bash
cloudflared tunnel list
```
Look for tunnels with active CONNECTIONS — those are serving traffic. Note each tunnel's UUID.

**Step 3: Identify DNS target for your domain**
```bash
# Check which tunnel the domain is pointed to
dig CNAME yourdomain.com +short
# Expected: <uuid>.cfargotunnel.com
# If this UUID doesn't match the running tunnel's config, that's the root cause.
```

**Step 4: Match DNS UUID to running tunnel**
```bash
cloudflared tunnel info <uuid-from-dns>
```
Compare connectors and origin IPs to your current machine. If the DNS-targeted tunnel shows different connector IDs or an older version, it's routing to a stale config.

**Fix options:**

| Scenario | Fix |
|----------|------|
| DNS points to old tunnel UUID | Delete old DNS record, route DNS to new tunnel: `cloudflared tunnel route dns <new-tunnel> yourdomain.com` |
| Old tunnel still connected with stale config | Delete old tunnel: `cloudflared tunnel delete <old-uuid>` |
| Config points to wrong port | Update YAML config file, restart tunnel: `cloudflared tunnel --config <path> run` |
| Multiple tunnels claim same domain | In Cloudflare Dashboard → DNS, ensure only ONE CNAME record exists for the domain |

**Prevention:** Name tunnels clearly and document which domain each serves. Reuse the same tunnel UUID for a domain — just update its config — rather than creating new tunnels.

See `references/tunnel-config-mismatch-diagnosis.md` for a complete worked example.

### 🚨 REMOTE CONFIG IS LIVE SHARED STATE — it can be reverted by other agents

**Symptom:** You PUT the corrected remote config (domain → correct port), verify it works, and the user confirms. **Days later the domain serves the old content again** — same symptom as before, and the local YAML is still correct.

**Root cause:** The tunnel's remote config lives on the Cloudflare edge and **any agent/session with the API token can re-PUT it**. In this setup multiple Hermes sessions and crons manage the same account; one of them re-applied a config that pointed `thefirstonly.com → localhost:5099` (plus added new records: erp.kiemion.online, uploadhtml.thefirstonly.com...) — silently reverting your fix.

**Rules to prevent silent regressions:**
1. **Never assume a remote-config fix persists.** Before concluding "it's fixed", re-GET the config via API and diff the ingress list against what you PUT.
2. **When re-PUTting, read the CURRENT config first.** Other agents may have added hostnames you don't know about. Send the union of {what's there now} ∪ {your correction} — a PUT that only contains your known hostnames wipes the additions others made.
3. **Keep a canonical inventory** of every hostname each tunnel serves (a table in the skill reference or a note file), so any re-PUT can reconstruct the full list.
4. If the same domain keeps flipping back, identify the OTHER writer (a cron like the Tunnel & WARP health script, or another Hermes session with API access) and fix the config at that source, not just at the edge.

Worked example and full ingress inventory: `references/cloudflare-api-tunnel-management.md` (section "Remote config can be silently reverted").

### ⚙️ Cron watchdog for tunnel origin servers (Windows)

Keeping the origin server alive so the tunnel keeps serving is a recurring need. Two hard-won rules:

1. **Hermes cron `no_agent` scripts must be Python (`.py`), NOT bash (`.sh`).** On Windows the cron runner does NOT have `bash` on PATH — a `.sh` script fails every tick with `Cannot run .sh/.bash script '...': bash not found on PATH`. Rewrite the watchdog as `.py` (stdlib `socket.connect_ex` for port checks, `subprocess.Popen` with `creationflags=CREATE_NO_WINDOW` for restarts). The `.sh` may work when run manually from git-bash but STILL fails under cron — test via `cronjob action=list` → `last_status: error`, not by running it by hand.

2. **A generic port-health watchdog can restart a port with the WRONG service.** Example: `port_health.py` had entry `(3000, "Company Site", "C:\\Users\\<user>\\projects", "<python> -m http.server 3000")` — if port 3000 ever dies, this cron starts a **directory-listing http.server over `~/projects`** instead of the real app (first-only-profile), recreating the exact security hole from this session. Watchdogs must carry the **exact restart command of the real service** (same cwd, same binary). If a dedicated watchdog already covers a port (e.g. `watchdog-firstonly.py`), remove that port from generic health scripts to avoid two writers fighting.

3. **Verify a watchdog actually works** by checking `cronjob action=list` → `last_status` after the first scheduled tick, and read the script's log file. A watchdog that silently fails is worse than none — the server dies and nothing restarts it.

See `references/cron-watchdog-patterns.md` for the worked example: the `.sh`→`.py` cron failure, the port-health cron that restarts port 3000 with the WRONG service, and an inventory of this machine's watchdog crons (some of which are the concurrent writers that revert remote configs).

### 🚨 Named tunnel crash detection and restart

**Symptom:** A Cloudflare named tunnel that was running for days suddenly stops serving traffic. `https://<domain>/` returns connection timeout or ERR_CONNECTION_CLOSED, but the local server on the origin port is still responding fine.

**Root cause:** The `cloudflared.exe` process crashed (memory pressure, Windows update, network disruption, or silent exit after idle). On Windows, the process can disappear without any error log. Unlike localtunnel which shows a clear `status: exited`, cloudflared's named tunnel can go silent and the Hermes process manager still shows partial output from the last connected state.

**Diagnosis:**

```bash
# Step 1: Check if any cloudflared process is still running
ps aux | grep cloudflared | grep -v grep
# If empty → tunnel died. If processes exist but the tunnel was serving your domain,
# check if the CONFIG file being used matches the domain's tunnel UUID.

# Step 2: Check DNS still points to the right tunnel
dig CNAME <domain> +short 2>/dev/null || nslookup <domain> 2>/dev/null
# Expected: <uuid>.cfargotunnel.com

# Step 3: Quick health check through the tunnel
curl -s -o /dev/null -w "%{http_code}" --max-time 10 https://<domain>/
# Expected: 200. If timeout/000 → tunnel is dead.

# Step 4: Check local server still running (the origin)
curl -s -o /dev/null -w "%{http_code}" http://localhost:<PORT>/
# Expected: 200. If this fails too → server died, fix server first.
```

**Restart the tunnel:**

```bash
# Use native Windows path — MSYS path fails
cloudflared tunnel --config "C:\Users\<user>\.cloudflared\<name>-config.yml" run

# Verify it connected (wait ~5s, then test)
sleep 5 && curl -s -o /dev/null -w "%{http_code}" --max-time 10 https://<domain>/
# Expected: 200
```

**Common crash patterns on this system:**
- `cloudflared.exe` crashes silently after 1-7 days of uptime on Windows (observed with both theliems and firstonly tunnels)
- Multiple named tunnels (firstonly, theliems) are independent — one can crash while the other keeps running
- A tunnel that exited may leave a zombie process entry in `ps aux` that does zero I/O — verify with `cloudflared tunnel info <uuid>` not just `ps aux`
- The Port Health Check cron job (`d550d5785738`, runs hourly) is the monitoring mechanism — if it stopped reporting, the tunnel may have died

### 🔍 Cloudflare DNS route creates record under wrong zone

**Symptom:** `cloudflared tunnel route dns <tunnel> bot.domain.com` succeeds but creates `bot.domain.com.otherdomain.com` (a concatenated hostname). The DNS record appears under the wrong Cloudflare zone.

**Root cause:** cloudflared uses the **first zone** it finds on the account that matches any part of the hostname. With multiple zones (`domain.com` + `otherdomain.com`), it may match the wrong one and append the subdomain there. CLI confirms: `Added CNAME bot.domain.com.otherdomain.com`.

**Fix — use Cloudflare API directly:**
```bash
# Get correct zone ID by exact name
ZONE_ID=$(curl -s "https://api.cloudflare.com/client/v4/zones?name=domain.com" \
  -H "Authorization: Bearer <TOKEN>" | python3 -c "import sys,json;print(json.load(sys.stdin)['result'][0]['id'])")

# Create CNAME pointing to tunnel
curl -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records" \
  -H "Authorization: Bearer <TOKEN>" -H "Content-Type: application/json" \
  -d '{"type":"CNAME","name":"bot","content":"<TUNNEL_UUID>.cfargotunnel.com","ttl":1,"proxied":true}'
```

**Prevention:** Verify DNS after creation: `nslookup bot.domain.com` should return Cloudflare IPs, not a concatenated hostname.

Always use the Cloudflare API for DNS management when you have multiple zones on the same account — `cloudflared tunnel route dns` is unreliable in this scenario.

### 🔍 Cloudflare quick tunnel returns 404 — existing config catch-all intercepts traffic

**Symptom:** `cloudflared tunnel --url http://localhost:<PORT>` creates a quick tunnel at `https://<words>.trycloudflare.com`, but all requests return HTTP 404. Local server serves 200 fine. Running `cloudflared tunnel --url` again generates a new URL but same 404 result.

**Root cause:** The machine has an existing Cloudflare tunnel configuration (`~/.cloudflared/config.yml` or `cert.pem`) with an ingress catch-all rule:
```yaml
ingress:
  - hostname: app.example.com
    service: http://localhost:3001
  - service: http_status:404   # ← this catches ALL traffic including quick tunnels
```

Since `cert.pem` exists (from previous `cloudflared login`), the quick tunnel authenticates as the existing account. Cloudflare's edge routes the quick tunnel's random `*.trycloudflare.com` hostname through the existing tunnel's ingress rules, which hit the catch-all 404 before reaching the target server.

**Fix — suppress config loading:**
```bash
cloudflared tunnel --url http://localhost:<PORT> --protocol http2 --config ""
```
The `--config ""` flag prevents cloudflared from loading the default `config.yml`, keeping the tunnel in ephemeral (non-account) mode where the catch-all rule doesn't apply.

**Alternative — modify existing config:**
If you want the tunnel on a named domain instead, either:
- Add a new ingress rule to the existing config (e.g., `research.myproject.com → localhost:<PORT>`) and set up DNS
- Or use localtunnel instead, which never conflicts with Cloudflare configs

**Diagnosis — confirm the root cause:**
```bash
# Check if existing config exists
ls ~/.cloudflared/config.yml ~/.cloudflared/*.pem

# Read the ingress rules
grep -A 20 "ingress:" ~/.cloudflared/config.yml
# Look for http_status:404 or http_status:403 as the last rule
```

**Symptom:** cloudflared registers successfully (shows "Registered tunnel connection" in logs), but all requests return HTTP 530 with body `"The origin has been unregistered from Argo Tunnel"` or HTTP 404 from Cloudflare's edge (see `CF-Ray` and `Server: cloudflare` headers).

**Root cause:** On Windows, cloudflared quick tunnels (trycloudflare.com) often fail to maintain the origin registration after the initial QUIC connection. The tunnel control plane thinks the origin is connected, but Cloudflare's edge can't route requests to it. This is a known Windows-specific issue with cloudflared's QUIC protocol implementation.

**Fix: switch to localtunnel instead.** Do not try to restart cloudflared or use a quick tunnel — the Windows QUIC issue will persist.

If you MUST use cloudflared: use a named tunnel (see "With cloudflared (named tunnel — production)" above), which uses a different connection path and is more reliable.

### `pnpm start -- --port` doesn't work

Next.js does NOT accept `--port` as a pnpm script argument. Doing `pnpm start -- --port 3001` passes `--port` as a directory path, causing "Invalid project directory provided".

**Fix:** Use environment variable or direct npx:
```bash
# Correct:
PORT=3001 npx next start -p 3001

# Also correct (modify package.json):
# "start": "next start" + set PORT env var
```

### Cloudflare named tunnel config path must be native Windows

When running `cloudflared tunnel --config <path> run`, the path must be a native Windows path (`C:\Users\...`). POSIX paths like `/c/Users/...` or `~/...` will fail with "The system cannot find the path specified".

**Fix:** Always use:
```bash
cloudflared tunnel --config "C:\Users\<user>\.cloudflared\<name>-config.yml" run
```

### Port conflict when another server is already running

When starting a dev server, the port may already be in use by another process. Always check proactively before starting.

```bash
# List all listening ports with process names (clean table output):
python -c "
import subprocess
r = subprocess.run(['netstat', '-ano'], capture_output=True, text=True)
ports = {}
for line in r.stdout.split('\n'):
    if 'LISTENING' not in line: continue
    parts = line.strip().split()
    if len(parts) < 5: continue
    addr = parts[1]
    if ':' not in addr: continue
    port = addr.rsplit(':', 1)[-1]
    if not port.isdigit(): continue
    pid = parts[-1]
    ports.setdefault(port, set()).add(pid)

print('╔════════╦══════════╦═══════════════════╗')
print('║  Port  ║  PID     ║  Process          ║')
print('╠════════╬══════════╬═══════════════════╣')
for port in sorted(ports.keys(), key=int):
    for pid in sorted(ports[port]):
        r2 = subprocess.run(['tasklist', '/FI', f'PID eq {pid}', '/NH'], capture_output=True, text=True)
        name = '?'
        for line2 in r2.stdout.split('\n'):
            if pid in line2:
                name = line2.strip().split()[0] if line2.strip().split() else '?'
                break
        print(f'║ {port:>5}  ║ {pid:<7} ║ {name:<18} ║')
print('╚════════╩══════════╩═══════════════════╝')
"

# Check a specific port
netstat -ano | grep ":3000 " | grep LISTENING

### Background process captures zero output

Both `terminal(background=true)` and the Hermes process manager (`process` tool) strip most tunnel output on Windows. Don't use them to capture tunnel URLs.

**Working patterns instead:**

1. **Use `tee` to capture URL to a file** (best for cloudflared):
   ```bash
   cloudflared tunnel --url http://localhost:<PORT> 2>&1 | tee /c/Users/NTQUANG_DELL/tunnel_url.txt
   ```
   After ~15-30s: `grep "trycloudflare.com" /c/Users/NTQUANG_DELL/tunnel_url.txt`

2. **Accept invisible output and verify via curl** (works for localtunnel with --subdomain):
   Run the tunnel in the background with `terminal(background=true)`, accept that you won't see the URL, and verify by curling the expected URL pattern directly:
   ```bash
   curl -s --max-time 10 https://my-subdomain.loca.lt/api/health
   ```

   **For cloudflared** (random subdomain — harder to guess): check the process log after ~15s with `process(action="log", session_id="proc_xxx")`. If empty, curl the local port directly as a health check:
   ```bash
   curl -s http://localhost:<PORT>/api/health
   ```

**Key insight:** Zero background output on Windows ≠ tunnel failure. The tunnel is frequently running and serving perfectly even when the process manager shows an empty output buffer. Always verify with curl before concluding the tunnel failed.

### Direct lt.js path not found

If you installed `localtunnel` via npm but can't find `lt.js`:

```bash
# Find where npm puts global modules
npm root -g
# → C:\Users\USER\AppData\Roaming\npm\node_modules

# The lt binary is at:
# <root>/localtunnel/bin/lt.js

# Verify it exists:
ls "$(npm root -g)/localtunnel/bin/lt.js"
```

**Key insight:** Zero background output on Windows ≠ tunnel failure. The tunnel is frequently running and serving perfectly even when the process manager shows an empty output buffer. Always verify with curl before concluding the tunnel failed.

Some npm bootstrap tools (`npx`, `npx.cmd`) hang or produce no output on Windows git-bash. This is a known MSYS2/Node.js interop issue. The workaround is to bypass npx entirely and invoke the Node.js script directly (see step 2 above).

### Fork failure on Windows (MSYS2/bash)

Some npm/node packages fail in MSYS2 because of path translation or fork semantics. If that happens:

- **Don't use `npx` or `npx.cmd`** — both can hang or produce no output
- Instead, find the installed package path and run the script directly with `node`:
  ```bash
  npm_root=$(npm root -g)
  node "$npm_root/localtunnel/bin/lt.js" --port <PORT> --subdomain <name>
  ```
- Prefer localtunnel via node direct path over cloudflared to avoid cloudflared-specific output issues

### Tool not found

- `localtunnel` is an npm package: `npx.cmd localtunnel` auto-downloads it
- `cloudflared` lives at `/c/Program Files (x86)/cloudflared/cloudflared`
- `serveo.net` only needs the system SSH client

## Verification

```bash
# 1. Server is up locally
curl -s -o /dev/null -w "%{http_code}" http://localhost:<PORT>

# 2. Tunnel is up (use the expected URL pattern)
# For localtunnel: https://<your-subdomain>.loca.lt
curl -s -o /dev/null -w "%{http_code}" --connect-timeout 10 https://<subdomain>.loca.lt

# 3. Content serves properly through the tunnel
curl -s --max-time 10 https://<subdomain>.loca.lt/<path> | head -5
```

**If curl through the tunnel returns empty or times out**, it may just need a few more seconds to propagate. Wait 5-10s and retry once before concluding the tunnel failed.

</skill_name>

## Related skills

- `voice-and-stt` — Hermes STT setup (tunneling may be used to test WebSocket streams)
- `system-design-workflow` — full project design (may involve serving previews)

## Reference files

- `references/port-management.md` — port checking, conflict resolution, and free port discovery commands
- `references/tunnel-config-mismatch-diagnosis.md` — worked example: diagnosing directory listing exposure caused by tunnel config mismatch (multiple tunnels, DNS pointing to wrong UUID)
- `references/supabase-postgrest-relationship-debugging.md` — debugging PostgREST join failures caused by missing direct FK constraints between public tables (common when `profiles` and `posts` both reference `auth.users` independently)
- `references/cloudflare-api-tunnel-management.md` — managing Cloudflare tunnel configs and DNS records via API (remote config, DNS CNAME records, cert.pem token extraction, bot-to-bot relay pattern)
