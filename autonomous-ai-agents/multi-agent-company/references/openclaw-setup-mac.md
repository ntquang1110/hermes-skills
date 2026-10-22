# OpenClaw Setup on Mac Mini

Reference for setting up OpenClaw agent platform on the Mac Mini (192.168.1.3) — used as the FRONT agent in the AI Company (asks user, synthesizes).

## Distinction from OpenCode

**OpenClaw ≠ OpenCode.** OpenClaw is an agent platform with gateway, channels (Telegram), and model providers. OpenCode is a coding agent CLI. OpenClaw uses OpenCode as a model provider via `opencode-go`.

In AI Company architecture: OpenClaw = FRONT agent (asks user + synthesizes), Hermes = BACK agent (logic/critique/implementation).

## Session Commands (Sept 2026)

```bash
# Install / upgrade Node.js
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"
nvm install 24
nvm alias default 24
nvm use 24

# Install OpenClaw
npm i -g openclaw
npm config set allow-scripts=openclaw,@google/genai,koffi,tree-sitter-bash,protobufjs --location=user
npm i -g --allow-scripts=openclaw openclaw

# Onboard non-interactive with OpenCode API key
openclaw onboard --non-interactive --accept-risk --skip-bootstrap --skip-skills --skip-search --skip-hooks --opencode-go-api-key 'oc_sk_...' --mode local --no-install-daemon --gateway-bind auto

# Model config — free models
openclaw config set agents.defaults.model.primary "opencode/muse-spark-1.3-contributor-free"
openclaw config set "agents.defaults.models[opencode/muse-spark-1.3-contributor-free]" '{}'

# Telegram channel
openclaw channels add --channel telegram --token '<bot_token>'

# Approve user pairing (user messages bot first, gets code)
openclaw pairing approve telegram <code>

# Start gateway
nohup openclaw gateway run > ~/.openclaw/gateway.log 2>&1 &
```

## Model Provider Matrix

| Provider | Model | Access | Cost |
|----------|-------|--------|------|
| opencode | muse-spark-1.3-contributor-free | Free key | Free |
| opencode | deepseek-v4-flash | Free key | Free |
| opencode-go | muse-spark-1.3-contributor | Paid subscription | 403 if unpaid |
| opencode-go | deepseek-v4.1-flash | Paid subscription | Paid |
| opencode-go | deepseek-v4-pro | Paid subscription | Paid (default) |

## Schema Quirks

- `model.fallback` — invalid key, don't use
- `apiType` — invalid under models.providers
- Workaround: edit ~/.openclaw/openclaw.json directly with Node.js
- Gateway: port 18789, needs manual restart after config changes
