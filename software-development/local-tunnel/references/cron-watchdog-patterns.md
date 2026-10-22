# Cron Watchdog Patterns on Windows (worked example)

Session context: firstonly.com kept reverting to the visit card even after remote-config fixes. Two culprits emerged: concurrent cron writers on the Cloudflare account, and a buggy port-health cron.

## Rule 1: Hermes cron `no_agent` scripts MUST be Python, not bash

On Windows the cron runner has NO `bash` on PATH. A `.sh` watchdog fails every tick:

```
Cannot run .sh/.bash script 'watchdog-firstonly.sh': bash not found on PATH.
On Windows, install Git for Windows (which ships Git Bash) or rewrite the script as Python (.py).
```

- The `.sh` may work when run manually from git-bash (`bash script.sh`) — that lulls you into thinking it's fine. Under cron it fails deterministically.
- Detect via `cronjob action=list` → `last_status: error` (the cron runner records it), not by running the script by hand.
- Rewrite as `.py`: port check via `socket.connect_ex(("127.0.0.1", port)) == 0`; restart via `subprocess.Popen(cmd, cwd=PROJECT_DIR, creationflags=subprocess.CREATE_NO_WINDOW)`.

## Rule 2: a generic port-health cron can restart a port with the WRONG service

`port_health.py` (cron `d550d5785738`, every 3h) contained:

```python
(3000, "Company Site", r"C:\Users\NTQUANG_DELL\projects",
 f'{HERMES_PYTHON} -m http.server 3000'),
```

If port 3000 ever dies, this starts a **Python http.server over `~/projects`** — directory listing — instead of the real app (first-only-profile). That recreates the exact security hole from the earlier session (source code exposure).

**Fix:** watchdog entries must carry the REAL service's exact start command (cwd + binary + args). If a dedicated watchdog already owns a port (e.g. `watchdog-firstonly.py`), remove that port from generic health scripts to avoid two writers fighting over one port.

## Rule 3: watch for crons that restart cloudflared — they can be the config reverter

`tunnel_health.py` (cron `da03e5bba42e`, every 2h) does `taskkill //F //IM cloudflared.exe` then restarts with `--protocol quic`. It checks tunnel health via `curl -sI https://me.thefirstonly.com` and `https://status.thefirstonly.com`.

A cron that kills+restarts cloudflared can push a stale LOCAL config or re-pull a stale REMOTE config, appearing to "revert" your API fix. When a remote-config fix flips back, list ALL crons (`cronjob action=list`) and inspect every script that mentions cloudflared/port restart before re-applying the fix.

## Inventory of watchdog crons on this machine (as of this session)

| Cron | Schedule | Script | Watches | Risk |
|------|----------|--------|---------|------|
| `d550d5785738` Port Health Check | every 3h | `port_health.py` | 5099, 3000, 3003, 5011 | ⚠️ restarts 3000 with wrong service |
| `da03e5bba42e` Tunnel & WARP Health | every 2h | `tunnel_health.py` | cloudflared + WARP | ⚠️ kills/restarts all cloudflared |
| `85b1ae121a04` watchdog-firstonly | every 60m | `watchdog-firstonly.py` | port 3000 (first-only-profile) | OK — correct restart cmd |
| `b4488662a34b` watchdog-erp | every 60m | `watchdog-erp.py` | 10000, 8080 | OK |
| `9b5fcc2833a5` watchdog-upload | every 60m | `watchdog-upload.py` | 8899 (uploadhtml.tfo) | OK |

**Lesson:** when debugging "why does my domain keep serving the wrong app", the answer may be a cron — check `cronjob action=list` + read each script before touching the Cloudflare edge again.
