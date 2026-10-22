# Tunnel Config Mismatch Diagnosis — Worked Example

## Situation

User reported: domain `thefirstonly.com` was showing a **directory listing** of source code (`.env.local`, `.git/`, all source files). Expected: a business card page.

## Environment

- Windows 10, git-bash (MSYS2)
- Cloudflare named tunnels via `cloudflared`
- Python `http.server` on port 3000 serving a Next.js project root (theliems)
- Proper Next.js dev server on port 3001
- Visit card (static HTML) on port 5099

## Step-by-Step Diagnosis

### 1. Identify running servers and ports

```bash
netstat -ano | grep LISTENING
```

Result:
| Port | PID | Process | Content |
|------|-----|---------|---------|
| 3000 | 20080 | python.exe | Python http.server (directory listing ⚠️) |
| 3001 | 9360 | node.exe | Next.js (proper app) |
| 5099 | 10412 | python.exe | Visit card (static HTML) |

### 2. Check the public URL directly

```bash
curl -s https://thefirstonly.com/ | head -5
# → <title>Directory listing for /</title>
# → Lists .env.local, .git/, source files...
```

Content matched `localhost:3000` (same MD5 hash, same 1201 bytes).

### 3. Find the tunnel config

```bash
ls ~/.cloudflared/*.yml
# → config.yml, firstonly-config.yml, theliems-config.yml
```

The `firstonly-config.yml` claimed:
```yaml
ingress:
  - hostname: thefirstonly.com
    service: http://localhost:5099
```

But the actual content was from port **3000**, not **5099**. Config mismatch.

### 4. List all running cloudflared instances

```bash
ps aux | grep cloudflared | grep -v grep
# → PID 24108  (theliems tunnel)
# → PID 25017  (firstonly tunnel — just started)

cat /proc/25017/cmdline | tr '\0' ' '
# → "cloudflared.exe tunnel --config firstonly-config.yml run"

cat /proc/24108/cmdline | tr '\0' ' '
# → "cloudflared.exe tunnel --config theliems-config.yml run"
```

### 5. List all registered tunnels

```bash
cloudflared tunnel list
```

| UUID | Name | Connections |
|------|------|-------------|
| ee75ab7b... | Home Server | active |
| **0ce9aa47...** | **TQUANG-DELL** | **active (from Jun 2)** |
| 1a837010... | theliems | active |

### 6. Find the tunnel the DNS actually points to

```bash
dig CNAME thefirstonly.com +short
# → likely <some-uuid>.cfargotunnel.com
```

Compare the DNS CNAME target UUID to the tunnel UUIDs from `cloudflared tunnel list`. If the DNS points to `0ce9aa47...` (TQUANG-DELL) but the newly started tunnel uses `0c9e449d...` (a different UUID), the old tunnel is the one routing traffic.

### 7. Check old tunnel's config

```bash
cloudflared tunnel info 0ce9aa47-7d52-4d6a-9a16-13b48c508cff
# Shows active connectors from this machine, version 2026.5.0
```

No local config file existed for `0ce9aa47...` — its config was set at the Cloudflare edge (dashboard web UI). The old tunnel's edge config pointed to port 3000, where the Python http.server was running with directory listing.

## Root Cause

| Layer | Expected | Actual |
|-------|----------|--------|
| DNS CNAME | `new-tunnel.cfargotunnel.com` | `old-tunnel.cfargotunnel.com` |
| Old tunnel config | — | Points to port **3000** (Python http.server) |
| New tunnel config | Points to port **5099** (visit card) | Not connected to DNS |
| Port 3000 server | Should not exist | Python SimpleHTTP with directory listing |

Two issues:
1. **Security:** Python `http.server` on port 3000 with directory listing exposed source code
2. **Config mismatch:** New tunnel created but DNS still pointed to old tunnel's UUID

## Fix

1. Kill the Python http.server: `taskkill /F /PID 20080`
2. Delete the old tunnel from Cloudflare dashboard or route DNS to the new tunnel
3. Ensure the new tunnel's config points to the correct port

## Key Commands Reference

```bash
# List cloudflared processes with their config files (Linux/macOS/WSL)
for pid in $(pgrep cloudflared); do
  echo "PID $pid: $(cat /proc/$pid/cmdline 2>/dev/null | tr '\0' ' ')"
done

# On Windows git-bash (MSYS2) — fallback when /proc/<PID> is empty:
wmic process where "name like '%cloudflared%'" get processid,commandline /format:list

# List all registered tunnels
cloudflared tunnel list

# Check tunnel details
cloudflared tunnel info <uuid-or-name>

# Check DNS CNAME for domain
dig CNAME yourdomain.com +short

# Route DNS to a tunnel
cloudflared tunnel route dns <tunnel-name> yourdomain.com

# Compare local vs remote content (checksum verification)
curl -s http://localhost:<PORT>/ | md5sum
curl -s https://yourdomain.com/ | md5sum
```

## Prevention

1. Never use `python -m http.server` behind a tunnel — it enables directory listing
2. Before creating a new tunnel, verify which tunnel UUID the DNS currently points to
3. Delete old tunnels at the Cloudflare dashboard when migrating configs
4. Always verify content THROUGH the tunnel, not just locally
