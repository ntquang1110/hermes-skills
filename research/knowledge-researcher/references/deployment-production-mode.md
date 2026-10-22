## Deployment — Production Mode

**Use `next start` (production) not `next dev` (development) for daily use.** The production server is stable, uses webpack instead of Turbopack, and has zero risk of "Jest worker" crashes.

### Start production server

```bash
cd /c/Users/NTQUANG_DELL/knowledge-flow

# Export env vars (required — next start does NOT read .env.local)
export NEXT_PUBLIC_SUPABASE_URL="https://vgozvweyqcqkayafntwx.supabase.co"
export NEXT_PUBLIC_SUPABASE_ANON_KEY="<key>"

# Build + Start
npx next build && npx next start --port 3003
```

**Why env vars must be exported:** `next start` (production mode) does NOT read `.env.local`. Only `next dev` does. Without the Supabase URL and anon key, the Supabase client fails silently at runtime and returns empty card lists. Export them before starting.

### Update after code changes (VERIFIED workflow)

```bash
# Step 1: Kill ALL processes on port 3003 — process(action='kill') can silently target WRONG PID
netstat -ano | grep ":3003 " | grep LISTENING
# Note every PID. Kill them one by one:
cmd.exe /c "taskkill /F /PID <PID>"
# Repeat netstat until port is free
netstat -ano | grep ":3003 " | grep LISTENING || echo "port free"

# Step 2: Clean build
rm -rf .next node_modules/.cache
npx next build

# Step 3: Start server
npx next start --port 3003

# Step 4: Verify
curl -s -o /dev/null -w "%{http_code}" http://localhost:3003   # Must return 200

# Step 5: Restart tunnel if needed
cloudflared tunnel --url http://localhost:3003 --protocol http2 --config ""
```

**⚠️ CRITICAL: `process(action='kill')` silently fails on Windows.** The Hermes tool kills the TRACKED session PID, but the ACTUAL server process on port 3003 is often a DIFFERENT PID (from an earlier start that the tool lost track of). The "killed" success message is misleading — the old server keeps running, serving stale built code. All subsequent `next start` attempts fail with EADDRINUSE.

**Always verify with `netstat` after any kill attempt. If the port shows LISTENING, the kill didn't work.**

**Common failure scenario:** 10+ builds and restarts, but the browser still shows old code. Every new server exited with EADDRINUSE. The ORIGINAL server (PID from hours ago) is still running on the port, serving the very first build's output. ALL subsequent builds were compiled correctly into `.next/` but NEVER DEPLOYED because no new server could bind the port.

**Verify deployment freshness:** After restart, check the server's `.next` chunks modification time — they should be < 1 minute old. If they're hours old, the old server is serving them.

```bash
cd /c/Users/NTQUANG_DELL/knowledge-flow
npx next build
# Kill old server — VERIFY with netstat, process(action='kill') can silently fail on Windows
netstat -ano | grep 3003 | grep LISTENING
# Kill EVERY PID listed, not just one. Use cmd.exe /c to avoid MSYS path conversion of /F
cmd.exe /c "taskkill /F /PID <each-pid>"
# Full cache clean (required when changes don't take effect despite build success)
rm -rf .next node_modules/.cache
# Rebuild (cache was nuked)
npx next build
# Restart
npx next start --port 3003
# Verify
curl -s -o /dev/null -w "%{http_code}" http://localhost:3003
# Restart tunnel if needed
cloudflared tunnel --url http://localhost:3003 --protocol http2 --config ""
```

**⚠️ Critical — `process(action='kill')` can silently target wrong PID on Windows**

The Hermes tool `process(action='kill', session_id='...')` kills the TRACKED session, not necessarily the process on the port. If the tracked session has already exited and a different process inherited the port, `process(action='kill')` reports "killed" but does NOTHING useful. The REAL server keeps running serving old built code.

**Always verify with `netstat -ano | grep 3003 | grep LISTENING`** after any kill attempt. If a PID is still listening:
- Kill it via `taskkill /F /PID $PID` — use `cmd.exe /c "taskkill /F /PID $PID"` in git-bash to avoid MSYS path conversion issues with `/F`
- If multiple processes are holding the port, kill each one
- Only start the new server when `netstat` shows the port is free

### Why not dev mode

The Turbopack dev server (`npx next dev`) on Next.js 16.2.10 Windows has a known crash: `Jest worker encountered 2 child process exceptions, exceeding retry limit`. The crash chain:

1. File edit → HMR updates client code → old server HTML mismatches new client code → hydration error
2. Next.js dev overlay opens → tries to compile the card detail route (dynamic)
3. Turbopack's internal worker crashes processing the dynamic route → "Jest worker" error
4. Cascade kills the server

Production mode (`next start`) uses webpack-compiled bundles — no Turbopack, no Jest workers, no dev overlay, no HMR. It's rock-solid for daily browsing.

