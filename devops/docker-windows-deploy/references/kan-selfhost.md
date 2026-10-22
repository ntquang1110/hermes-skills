# Kan self-host notes (github.com/kanbn/kan)

Open-source Trello alternative — Next.js 15 + tRPC + Better Auth + Drizzle ORM, PostgreSQL 15, Docker Compose.

## Deploy layout (this user's machine)
- Project: `D:\kan` (deliberately NOT on C: — user requirement "không dùng ổ C")
- Postgres data: `D:\kan\pgdata` via bind mount (compose edit, Option A)
- Web: `http://localhost:<WEB_PORT>` (default 3000 — **watch out: this user's port map has 3000 = "Company"**, override WEB_PORT in .env if Company runs on this box)
- DB container: `kan-db`, port 5432 exposed on host

## Images
- `ghcr.io/kanbn/kan:latest` (web) — NOT always published; compose falls back to `docker compose build web`
- `ghcr.io/kanbn/kan-migrate:latest` (migrations) — runs once; web `depends_on: migrate (service_completed_successfully)`
- `postgres:15` (Docker Hub — the flakiest pull on bad networks)

## Minimal .env
```env
NEXT_PUBLIC_BASE_URL=http://localhost:3000
BETTER_AUTH_SECRET=<32+ random chars>
POSTGRES_PASSWORD=<pw>
POSTGRES_URL=postgresql://kan:<pw>@kan-db:5432/kan_db   # service name (kan-db) = host inside compose network
WEB_PORT=3000
```
Note: compose sets `POSTGRES_DB=kan_db`, `POSTGRES_USER=kan` for the postgres service — the URL must match.

## Flow
1. Clone to D:\kan
2. Write .env (above)
3. Bind-mount pgdata on D: (replace `kan_postgres_data:/var/lib/postgresql/data` with `/d/kan/pgdata:/var/lib/postgresql/data`)
4. `docker compose up -d` → migrate completes → web starts
5. Verify: `curl -sI http://localhost:3000`

## Observed failure mode (flaky VN network)
- Docker Hub `postgres:15` repeatedly failed with `TLS handshake timeout` while ghcr.io images succeeded.
- Git clone dropped with `curl 56 Recv failure` / `early EOF` until `http.postBuffer` was raised, then succeeded.
- Root cause was network latency to gateway ~1.3–2.6s, not the app or Docker config. The retry loop (`scripts/retry_pull.sh`) is the correct response; don't change app config to "fix" it.
