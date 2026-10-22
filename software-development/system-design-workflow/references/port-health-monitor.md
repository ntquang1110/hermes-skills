# Port Health Monitor — Windows Service Watchdog

Keep self-hosted services alive on a Windows machine. Checks ports every hour and auto-restarts dead processes.

## Script

Path: `~/AppData/Local/hermes/scripts/port_health.py`

```python
#!/usr/bin/env python3
"""Port health checker — checks all service ports and restarts dead ones."""
import subprocess, sys, os, socket, time

HERMES_PYTHON = r"C:\Users\<USER>\AppData\Local\Programs\Python\Python311\python.exe"

SERVICES = [
    (5099, "Visit Card", r"C:\Users\<USER>\visit-card",
     f'{HERMES_PYTHON} -m http.server 5099'),
    (3000, "Company Site", r"C:\Users\<USER>\projects",
     f'{HERMES_PYTHON} -m http.server 3000'),
    (3003, "Knowledge Flow", r"C:\Users\<USER>\knowledge-flow",
     f'start /B cmd /c "npm run start -- -p 3003"'),
    (5011, "Status Dashboard", r"C:\Users\<USER>\hermes-dashboard",
     f'{HERMES_PYTHON} server.py'),
]

def port_alive(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    try:
        s.connect(('127.0.0.1', port))
        s.close()
        return True
    except:
        return False

for port, name, cwd, cmd in SERVICES:
    if port_alive(port):
        print(f"🟢 {name} (:{port}) - OK")
    else:
        print(f"🔴 {name} (:{port}) - DEAD, restarting...")
        try:
            subprocess.Popen(cmd, cwd=cwd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            time.sleep(3)
            if port_alive(port): print(f"   ✅ Restarted successfully")
            else: print(f"   ❌ Failed to restart")
        except Exception as e: print(f"   ❌ Error: {e}")
```

## Cron Setup

Create a cron job via `cronjob action=create`:
- Schedule: `0 * * * *` (every hour)
- No script mode — use prompt to run the Python script
- Deliver results to origin chat

## Pitfalls

- **Stale TCP entries on Windows**: `netstat -ano` can show LISTENING for dead processes. Use `Get-NetTCPConnection` in PowerShell to confirm.
- **taskkill not enough**: Use `Stop-Process -Force` in PowerShell when normal kill fails.
- **Port conflicts**: Old processes can hold a port even after being killed. Change to a different port if the port won't free.
