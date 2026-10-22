# Viewing Files from Private Repositories

## Problem

`raw.githubusercontent.com` returns **404** for private repos.
`htmlpreview.github.io/?https://raw.githubusercontent.com/...` also fails (400/404).
GitHub API also returns 404 for unauthenticated requests to private repos.

## Solution: Run a Local File Server

Clone (or cd into) the repo and serve files via any HTTP server:

### Node.js (if `server.js` exists)
```bash
cd /path/to/repo
node server.js
# → http://localhost:8080
```

### Python one-liner (no deps needed)
```bash
cd /path/to/repo
python3 -m http.server 8080
# → http://localhost:8080
```

### Then open in browser
```
http://localhost:8080/filename.html
```

## Handling Port Conflicts on Windows

When port 8080 is already in use:

```bash
# Find the process using the port
netstat -ano | grep ":8080 " | grep LISTENING

# Kill it (PID is the last column from netstat output)
taskkill //F //PID <PID>

# Verify free
netstat -ano | grep ":8080 " | grep LISTENING || echo "Port free"
```

Note: MSYS2/bash `kill -9 <PID>` won't work with Windows-native PIDs. Always use `taskkill` for Windows processes.

## GitHub Blob View (Alternative — works when logged in)

If the user is logged into github.com in their browser:

```
https://github.com/OWNER/REPO/blob/BRANCH/path/to/file.html
```

GitHub renders HTML files as raw source (does not execute JS/CSS). Use local server for actual rendered preview.

## Quick Decision

| Repo visibility | Best approach |
|----------------|---------------|
| Public | `htmlpreview.github.io/?https://raw.githubusercontent.com/...` |
| Private | Local file server (`node server.js` or `python3 -m http.server`) |
