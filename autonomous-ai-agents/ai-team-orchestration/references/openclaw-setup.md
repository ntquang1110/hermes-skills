# OpenClaw Agent Platform — Setup Reference

**OpenClaw** (`npm i -g openclaw`) is an open-source agent infrastructure platform (390K+ stars). "All your chats, one OpenClaw."

**Critical: OpenClaw ≠ OpenCode.** They are separate products sharing API keys.
- OpenCode = coding agent CLI (`opencode run`).
- OpenClaw = multi-channel agent platform with Gateway, chat integrations.

## Install & Onboard

```bash
npm i -g openclaw
openclaw onboard --non-interactive \
  --accept-risk \
  --opencode-go-api-key 'oc_sk_...' \
  --mode local --no-install-daemon --gateway-bind auto \
  --skip-bootstrap --skip-skills --skip-search --skip-hooks
```

## Model Routing

Set primary model:
```bash
openclaw config set agents.defaults.model.primary "opencode-go/deepseek-v4.1-flash"
openclaw config set "agents.defaults.models[opencode-go/deepseek-v4.1-flash]" '{}'
```

**No native fallback field** — schema rejects `fallback`. Register multiple models in `agents.defaults.models{}`.

Provider distinction:
- `opencode` prefix → free tier (`-free` suffix models)
- `opencode-go` prefix → paid tier (subscription required; 403 if no sub)

## Telegram

```bash
openclaw channels add --channel telegram --token <BOT_TOKEN>
openclaw channels status --probe
openclaw pairing approve telegram <PAIRING_CODE>
```

## Gateway

```bash
nohup openclaw gateway run > ~/.openclaw/gateway.log 2>&1 &
# Default port 18789
```

## Pitfalls

- 403 on `opencode-go/muse-spark-1.3-contributor` if no subscription — use `opencode/muse-spark-1.3-contributor-free`.
- Restart gateway after config change.
- Each Telegram user must pair individually.
- The `opencode` Hermes skill is bundled — `hermes curator adopt opencode` before patching.
