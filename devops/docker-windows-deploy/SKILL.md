---
name: docker-windows-deploy
description: "Deploy/self-host Docker Compose apps on a Windows host — keep data off the C: drive (bind mounts on D:), start Docker Desktop headless, retry flaky registry pulls, verify remote access (RDP/Tailscale) when the user can't connect."
version: 1.0.0
author: hermes
license: MIT
platforms: [windows]
metadata:
  hermes:
    tags: [docker, windows, selfhost, compose, devops, deployment, git-bash]
    category: devops
---

# Docker Deploy on Windows (keep data off C:)

Deploy a Docker Compose app on a Windows host where the shell is git-bash/MSYS, especially when the user demands data NOT live on the C: drive — for this user that means "không dùng ổ C" / "dời hẳn sang ổ D" (D: has the space).

## When to use
- User says "chạy bằng docker nhưng không dùng ổ C" / "dời hẳn sang ổ D" and hands you a repo (e.g. a self-hostable GitHub project).
- Docker pulls fail with `net/http: TLS handshake timeout`, `curl 56 Recv failure`, `early EOF` on a flaky network.
- User reports "không remote vào được" the Windows box (RDP/Tailscale diagnosis below).

## Drive placement — decision first
| Option | What | When |
|--------|------|------|
| **A. Bind mount (fast, default)** | Change the compose named volume into a bind mount pointing at D:; keep project on D: | First step unless user explicitly wants ALL Docker data moved |
| **B. Move Docker data dir** | Docker Desktop → Settings → Resources → Advanced → Disk image location → `D:\DockerData` → Apply & Restart | Only when user wants images/volumes/cache off C: too |

Option A compose edit (postgres example):
```yaml
  postgres:
    volumes:
      - /d/<app>/pgdata:/var/lib/postgresql/data   # bind mount — NOT the named volume
```
Create `mkdir -p /d/<app>/pgdata` first. Run everything from `/d/<app>`.

## Steps
1. **Clone to target drive**: `cd /d/ && git clone <url> <app>`
   - Flaky network → set `git config --global http.postBuffer 524288000` and retry; if git still drops mid-transfer, fall back to downloading the GitHub ZIP (`curl -sL -o app.zip https://github.com/<o>/<r>/archive/refs/heads/main.zip`).
   - ALWAYS verify the clone finished: `git log --oneline -1`. A timed-out clone leaves a broken `.git` — `rm -rf` it and redo.
2. **Create `.env`** from `.env.example` with the app's required vars (secrets, DB URL, port). Generate secrets with python one-liner (NOT `openssl` if flaky, but openssl works too):
   `python -c "import secrets,string;print(''.join(secrets.choice(string.ascii_letters+string.digits) for _ in range(32)))"`
3. **Edit compose** to bind-mount DB data on D: (Option A).
4. **Start Docker Desktop** if daemon is down (`docker ps` fails with "pipe dockerDesktopLinuxEngine"): launch `"C:\Program Files\Docker\Docker\Docker Desktop.exe"` as a background process, then poll `docker ps` every ~3s until it responds (10–60s).
5. **Pull images with a retry loop** (flaky network): use `scripts/retry_pull.sh` (run background with notify_on_complete). TLS handshake timeout ≠ registry down — the loop wins.
6. **`docker compose up -d`**, then verify: `docker compose ps` + `curl -sI http://localhost:<port>`.

## Pitfalls (Windows / git-bash / Docker)
- `python3` → "Python was not found; run without arguments to install from the Microsoft Store" (Store alias). Use `python`.
- MSYS mangles `/F` → `taskkill //F //IM x.exe` still fails. Wrap: `cmd //c "taskkill /F /IM x.exe"`.
- `net stop/start <service>` requires admin — probe with `net session` (non-admin → "System error 5"). A non-admin shell CANNOT restart services; tell the user to use an Admin terminal or reboot.
- Compose `image:` + `build:` blocks: image may not exist on the registry yet even though compose references it → docker compose falls back to `docker compose build` (needs node/pnpm toolchain for Next.js apps).
- Pull can partially succeed: `kan-migrate` pulled while `postgres` timed out. Pull per-image with the retry loop rather than one giant `docker compose pull`.
- Port conflicts: check the app's default port against the user's fixed port map BEFORE `up` (this user: 5099=site, 3000=Company, 3001=TheLiem, 3003=KFlow, 5011=Status). Override via `.env` (e.g. `WEB_PORT=3000`).

## Remote-access diagnosis (user can't RDP into the box)
Order of checks, all from the local shell:
1. `netstat -an | grep ":3389 "` — RDP listening?
2. `netsh advfirewall firewall show rule name=all | grep -B1 -A12 "Remote Desktop"` — the `Remote Desktop - User Mode (TCP-In)` 3389 allow rule present/enabled?
3. `ipconfig` — active interface IP; then `ping -n 2 <gateway>` — **latency >1s explains every network symptom** (Docker TLS timeouts, git drops, "remote feels broken"). Do NOT blame the app first.
4. Tailscale: `tailscale status` — `unexpected state: NoState` + "Tailscale is starting" = tailnet is down, so remote-over-Tailscale fails even though RDP is fine. Fix needs admin (restart service) or a reboot.
5. Firewall/RDP can be OK while the REAL issue is network quality — report latency numbers to the user, don't chase ghosts.

## Files
- `scripts/retry_pull.sh` — generic retry loop: keeps `docker pull`-ing until every image is present, exits 0 on success. Run with background=true + notify_on_complete.
- `references/kan-selfhost.md` — Kan (kanbn/kan, Trello alternative) env/compose specifics from the first deployment of this pattern.
