# OpenClaw vs OpenCode — wiring reference (2026-09-22)

Do not confuse. Shared name root, different platforms. Mixing causes 403/auth errors.

| | OpenClaw (gateway / frontend) | OpenCode (LLM provider backend) |
|---|---|---|
| Role | Agent gateway, channel multiplexer (Telegram/Discord/Slack…), `openclaw gateway run`, `openclaw channels`, `openclaw pairing` | LLM inference API (Zen free + paid, Go paid catalogs) |
| Install | `npm i -g openclaw` — requires Node 24.16+ (`nvm install 24` via paramiko on Mac) | `npm i -g opencode-ai` |
| Endpoints | Local gateway `ws://127.0.0.1:18789` (dashboard http), LaunchAgent optional | `https://opencode.ai/zen/v1` (Zen) and `https://opencode.ai/zen/go/v1` (Go) |
| Auth | `openclaw onboard --opencode-go-api-key OC_SK_…` writes `auth.profiles`; runtime key in `models.providers.<id>.apiKey` (set via `openclaw config set models.providers.opencode.apiKey …` and `opencode-go.apiKey …` + matching `baseUrl`) | `OPENCODE_API_KEY` / `opencode auth login` |
| Models | `agents.defaults.model.primary` + `agents.defaults.models{}` in `~/.openclaw/openclaw.json`; validate with `openclaw config validate` | `openclaw models list --provider opencode` vs `--provider opencode-go` |
| Paid catalog (2026-09-22) | Zen paid: `deepseek-v4-flash`, `deepseek-v4.1-flash`, `qwen3.8-flash`. Go requires active subscription or 403. | |

## Gotchas discovered

- `agents.defaults.model.fallback` is not a valid key (schema rejects `fallback`). Use `primary` + all candidates in `agents.defaults.models{}`.
- Free-tier models (`*-free`) return `FreeTierError: can only be used from within OpenCode` when called via gateway — must use paid Zen models.
- Go 403 with `Insufficient account funds` (402 body) means top-up needed; do not retry as auth error.
- HTTP 403 `error code: 1010` from direct curl is Cloudflare WAF — needs `User-Agent: Mozilla/5.0` header to get real JSON error (`{"error":{"type":"server_error","message":"Upstream request failed: Insufficient account funds"}}`).
- Keys set via `models.providers.*.apiKey` require matching `baseUrl` or gateway falls back to empty `baseUrl` and 403.
- Mac deploy: Node 24 via `NVM_DIR="$HOME/.nvm"; . "$NVM_DIR/nvm.sh"; nvm use 24` before every `openclaw` call; `openclaw gateway run` must be kept alive (no LaunchAgent = `nohup … > ~/.openclaw/gateway.log 2>&1 &`), check with `curl http://127.0.0.1:18789/health`.
- Telegram: `openclaw channels add --channel telegram --token <BOT_TOKEN>` then `openclaw pairing approve telegram <CODE>` for user `6277220574` (@ntq_openClaw_bot).

## Current Mac state

- Host `192.168.1.3` (tquang/<PASSWORD>), Node v24.21.0, OpenClaw 2026.9.5, Whisper large-v3 :9000.
- Config: `primary: opencode/muse-spark-1.3-contributor-free` (will 403 until switched to paid), `models: opencode/muse-spark-1.3-contributor-free, opencode/deepseek-v4.1-flash`, providers both have `apiKey` + `baseUrl`.
- Fix on top-up: `openclaw config set agents.defaults.model.primary opencode/deepseek-v4.1-flash` then `kill $(lsof -t -i:18789); nohup openclaw gateway run > ~/.openclaw/gateway.log 2>&1 &`.
