# Mac Whisper Server Hang Recovery (verified 2026-09-25)

## Symptoms
- `/health` endpoint stops responding (curl hangs indefinitely)
- `ps aux | grep whisper` shows 414% CPU (4 cores pinned)
- RSS memory 3.9GB+
- `lsof -i :9000` shows TCP socket in `CLOSE_WAIT` state

## Root Cause
The client (Windows STT wrapper via `stt_mac_local.py` or `stt_mac_wrapper.py`) half-closes the TCP connection after POST. The server's uvicorn thread doesn't detect the half-close, enters an infinite loop reading from a closed socket, spinning at 100% per core.

## Fix
```bash
# Find the stuck PID
lsof -i :9000
# Kill it — launchd auto-restarts within 2-3 seconds
kill -9 <PID>
# Verify
curl http://127.0.0.1:9000/health
# Should return {"status":"ok","model":"large-v3","pid":<new_pid>}
```

launchd's `KeepAlive` detects the exit and spawns a fresh process automatically. No restart script needed.

## If launchd doesn't restart
```bash
launchctl kickstart gui/501/com.user.whisper-server
```

## Prevention
None practical — depends on client TCP behavior. The 30-minute watchdog (`watchdog_mac_whisper.py`, cron `cf98f6545a66`) detects the hang and alerts via Telegram. Recovery is automatic once the stuck PID is killed.
