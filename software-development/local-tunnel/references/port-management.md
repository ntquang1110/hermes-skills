# Port Management on Windows

Quick reference for checking and resolving port conflicts on this Windows machine (git-bash / MSYS).

## List all listening ports (clean table)

```python
# Single command via python heredoc — paste into terminal:
python << 'PYEOF'
import subprocess
r = subprocess.run(["netstat", "-ano"], capture_output=True, text=True)
ports = {}
for line in r.stdout.split("\n"):
    if "LISTENING" not in line: continue
    parts = line.strip().split()
    if len(parts) < 5: continue
    addr = parts[1]
    if ":" not in addr: continue
    port = addr.rsplit(":", 1)[-1]
    if not port.isdigit(): continue
    pid = parts[-1]
    ports.setdefault(port, set()).add(pid)

print("╔════════╦══════════╦══════════════════════╗")
print("║  Port  ║  PID     ║  Process             ║")
print("╠════════╬══════════╬══════════════════════╣")
for port in sorted(ports.keys(), key=int):
    for pid in sorted(ports[port]):
        r2 = subprocess.run(["tasklist", "/FI", f"PID eq {pid}", "/NH"], capture_output=True, text=True)
        name = "?"
        for line2 in r2.stdout.split("\n"):
            if pid in line2:
                parts2 = line2.strip().split()
                if parts2:
                    name = parts2[0]
                break
        print(f"║ {port:>5}  ║ {pid:<7} ║ {name:<20} ║")
print("╚════════╩══════════╩══════════════════════╝")
PYEOF
```

## Quick port check

```bash
# Check if a specific port is in use
netstat -ano | grep ":PORT " | grep LISTENING

# Find the PID — the last column of the LISTENING line
# Column layout: Protocol LocalAddr ForeignAddr State PID
netstat -ano | grep ":3000 " | grep LISTENING
# Output example:
#   TCP    0.0.0.0:3000     0.0.0.0:0     LISTENING     2644
# The PID is the LAST whitespace-separated field (column 5)

# Identify the process
tasklist /FI "PID eq <PID>"
```

## Kill processes

### ⚠️ CRITICAL: `kill -9` silently fails on Windows-native processes

**Always use `taskkill` to kill Windows-native processes** (`node.exe`, `python.exe`, `cloudflared.exe`). Git-bash's `kill -9` sends SIGKILL via MSYS2's `TerminateProcess()`, but this **only works for processes in the same MSYS2 process tree**. A process started independently (from another terminal, Task Scheduler, or spawned directly as a child of `init`) is outside that tree — `kill -9` appears to succeed but the process stays alive and the port remains held.

```bash
# ✅ WORKS — kills ANY Windows process
cmd.exe /c "taskkill /F /PID <PID>"

# ❌ DOES NOT WORK for node.exe started by npx/next/Task Scheduler:
kill -9 <PID>         # Silently fails, port still held

# ❌ DOES NOT WORK for cloudflared started as Windows service:
kill -9 <PID>         # Silently fails, tunnel still running from old config
```

**Try with `-9` first (portable, works for MSYS2-spawned processes), then fall back to `taskkill` when the port stays held.**

```bash
# Kill by PID — preferred approach
kill -9 <PID> 2>/dev/null          # May silently fail on Windows-native
# Check if it worked:
curl -s -o /dev/null -w "%{http_code}" http://localhost:<PORT>/
# If still 200 → kill -9 failed, use taskkill:
cmd.exe /c "taskkill /F /PID <PID>"

# Kill all instances of a process (use when you don't know the PID)
cmd.exe /c "taskkill /F /IM node.exe"          # Kills ALL node processes
cmd.exe /c "taskkill /F /IM python.exe"        # Kills ALL python processes
cmd.exe /c "taskkill /F /IM cloudflared.exe"   # Kills ALL cloudflared tunnels
```

**WARNING:** `taskkill /F /IM node.exe` kills ALL Node.js processes — not just the one you want. If you have multiple projects running (theliems on 3001, Kflow on 3003), they all die. Prefer PID-specific kills.

### Why this happens (Windows arcana)

`kill -9` in MSYS2 works by calling Windows `TerminateProcess()` via the MSYS2 runtime. The runtime maintains a process table of child processes it knows about. If the process was spawned outside MSYS2 (by Task Scheduler, another cmd.exe, double-clicking, Windows startup), MSYS2 has no record of it and `kill` silently no-ops despite exit code 0.

The `netstat` output PID is always the real Windows PID. If `kill -9 <PID>` reports success but the port is still occupied, the process is outside MSYS2's tree — switch to `taskkill`.

### cloudflared process management

Multiple cloudflared named tunnels may be running as separate processes. When they crash/exit, they leave no trace in `ps aux` but the origin server is up. To restart:

1. Verify tunnel is down: check via tunnel URL
2. Kill ALL instances: `cmd.exe /c "taskkill /F /IM cloudflared.exe"`
3. Start fresh: `cloudflared tunnel --config "C:\Users\<user>\.cloudflared\<name>-config.yml" run`

### Avoiding port conflicts when starting servers

```bash
# Proactively check for port conflicts before starting
netstat -ano | grep ":3001 " | grep LISTENING

# If occupied, either:
# a) Kill the existing process (see above)
# b) Use a different port
```

## Start Next.js on a specific port

```bash
# Correct (pnpm script doesn't accept --port arg)
PORT=3001 npx next start -p 3001

# Dev mode
cd ~/project && pnpm dev
# Then check what port (default 3000, if occupied Next.js asks to use another)
```

## Check free port range

```bash
python -c "
import subprocess
r = subprocess.run(['netstat', '-ano'], capture_output=True, text=True)
used = set()
for line in r.stdout.split('\n'):
    if 'LISTENING' not in line: continue
    parts = line.strip().split()
    if len(parts) < 5: continue
    addr = parts[1]
    if ':' not in addr: continue
    p = addr.rsplit(':', 1)[-1]
    if p.isdigit(): used.add(int(p))
free = sorted(set(range(3000, 3020)) - used)
print(f'Free ports 3000-3019: {free}')
"
```
