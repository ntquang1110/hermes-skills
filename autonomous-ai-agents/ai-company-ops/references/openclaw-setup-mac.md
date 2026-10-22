# OpenClaw Setup on Mac Mini

Reference for setting up OpenClaw agent platform on the Mac Mini (192.168.1.3).

## Distinction from OpenCode

OpenClaw is NOT OpenCode. OpenClaw is an agent platform ("all your chats, one OpenClaw") with gateway, channels (Telegram), and model providers. OpenCode is a coding agent CLI. OpenClaw uses OpenCode as a model provider via `opencode-go`.

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

# Onboard non-interactive
openclaw onboard --non-interactive --accept-risk --skip-bootstrap --skip-skills --skip-search --skip-hooks --opencode-go-api-key 'oc_sk_...' --mode local --no-install-daemon --gateway-bind auto

# Model config (free models)
# opencode/ = free models (-free suffix), opencode-go/ = paid models
# Primary: opencode/muse-spark-1.3-contributor-free
# Fallback: opencode/deepseek-v4-flash

# Telegram channel
openclaw channels add --channel telegram --token '8465282859:...'

# Approve user pairing
openclaw pairing approve telegram <pairing_code>

# Start gateway
nohup openclaw gateway run > ~/.openclaw/gateway.log 2>&1 &

# Verify
openclaw status
openclaw channels status --probe
```

## Schema Quirks

- `model.fallback` — invalid key, don't use
- `apiType` — invalid under models.providers
- For schema-rejected values: edit ~/.openclaw/openclaw.json directly with Node.js
- Gateway port: 18789
- Gateway needs manual restart after config changes

## Model Provider Matrix

| Provider | Model | Access | Cost |
|----------|-------|--------|------|
| opencode | muse-spark-1.3-contributor-free | Free key | Free |
| opencode | deepseek-v4-flash | Free key | Free |
| opencode-go | muse-spark-1.3-contributor | Paid subscription | 403 if unpaid |
| opencode-go | deepseek-v4.1-flash | Paid subscription | Paid |
| opencode-go | deepseek-v4-pro | Paid subscription | Paid |
