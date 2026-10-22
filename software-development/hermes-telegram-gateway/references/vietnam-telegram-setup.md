# Vietnam Telegram Gateway Setup

## Background
Telegram is blocked/throttled in Vietnam. api.telegram.org is unreachable from most Vietnamese ISPs (Viettel, FPT, VNPT). Hermes auto-discovers fallback IPs (149.154.166.110) but these are also unreliable.

## Recommended Stack
1. Install Cloudflare WARP (free VPN) — works reliably in Vietnam
2. Set no TELEGRAM_PROXY (empty) — WARP routes all traffic in VPN mode
3. Disable BotFather Group Privacy
4. Set `telegram.require_mention: false` in Hermes config

## Connectivity Checks

### Fast reachability check (no token needed)
```bash
curl -so /dev/null -w "%{http_code}" --connect-timeout 5 https://api.telegram.org/bot
# 404  = Reachable (Telegram is up, path is deliberately empty)
# 000  = Connection timeout / blocked (WARP or proxy needed)
# Other = Something else wrong
```

### Check WARP status
```bash
"/c/Program Files/Cloudflare/Cloudflare WARP/warp-cli.exe" status
# Expected: "Status update: Connected" + "Network: healthy"
# If disconnected: "/c/Program Files/Cloudflare/Cloudflare WARP/warp-cli.exe" connect
```

### Verify gateway
```bash
# Process running?
hermes gateway status

# Connected to Telegram?
grep "Connected to Telegram\|✓ telegram connected" ~/AppData/Local/hermes/logs/gateway.log | tail -1
```

## WARP Silent Disconnection

WARP can disconnect mid-session without warning (`Reason: Settings Changed`). When this happens:

1. Gateway process keeps running but can't reach Telegram
2. Logs show repeated `Polling heartbeat probe failed` → reconnect attempts → eventual silent death
3. **Fix order matters**: reconnect WARP FIRST, then restart gateway

Full troubleshooting is in the main SKILL.md (`Common Fixes > #5 WARP disconnected mid-session`).

## User Expectations
- Normal messages (without @bot) in groups should be responded to
- @bot mentions still work for explicit targeting
- Bot responds in all groups it's added to
