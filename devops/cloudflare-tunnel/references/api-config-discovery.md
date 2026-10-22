# API-based config discovery

## Problem

The tunnel wasn't routing `bot.thefirstonly.com` despite the local YAML config having the correct ingress rule. The tunnel log showed "Updated to new configuration" but the hostname returned 404.

## Root cause

The tunnel's `config_src` was `cloudflare`, not `local`. This means the tunnel was using ingress rules stored on Cloudflare's servers (via the API), **completely ignoring** the local `--config` YAML file. The local YAML file was loaded at startup but immediately superseded by the API-side config.

## How to detect

```bash
# Option 1: Check tunnel info output
cloudflared tunnel info <TUNNEL_ID>
# Look for: Config source: cloudflare

# Option 2: Check running tunnel's startup logs
# If you see: "Updated to new configuration config=..." with the JSON,
# that's the API-side config being loaded

# Option 3: Via Cloudflare API
curl -s https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/cfd_tunnel/{TUNNEL_ID}/configurations \
  -H "Authorization: Bearer {API_TOKEN}"
# The response shows the current ingress rules
```

## How to fix

Use the API to update the config directly (see main skill for PUT request), or clear the API-side config to force local YAML usage.

## Local liveness check with ZERO credentials (verified 2026-10-14)

Before reaching for an API token, prove whether the tunnel on THIS machine is alive. cloudflared
exposes Prometheus metrics on a localhost port (on this host: `127.0.0.1:20241`; find it with
`netstat -ano | grep <cloudflared-PID> | grep LISTENING`):

```bash
curl -s -o /dev/null -w "%{http_code}\n" --max-time 8 http://127.0.0.1:20241/ready   # 200 = up
curl -s --max-time 8 http://127.0.0.1:20241/metrics | grep -E \
  "cloudflared_tunnel_ha_connections|cloudflared_tunnel_request_errors"
# cloudflared_tunnel_ha_connections 4      <- edge connections (>0 = tunnel alive)
# cloudflared_tunnel_request_errors 256    <- cumulative "error proxying to origin"
```

`/ready` 200 + `ha_connections > 0` = the tunnel itself is fine, so a 502 must be blamed on the
origin (down / wrong port / on another machine), NOT on the tunnel. A climbing
`cloudflared_tunnel_request_errors` alongside a live tunnel means requests land on a connector
that cannot reach its origin.

## Which tunnel does the local Windows SERVICE run? Decode its token

`sc qc cloudflared` prints the full `tunnel run --token eyJ...`. The token is base64url JSON, so
account tag + tunnel ID come out with no API access at all:

```bash
python -c "
import base64, json, re, subprocess
out = subprocess.run(['sc','qc','cloudflared'], capture_output=True, text=True).stdout
t = re.search(r'--token (\S+)', out).group(1)
d = json.loads(base64.urlsafe_b64decode(t + '=' * (-len(t) % 4)))
print('account tag:', d.get('a')); print('tunnel ID:', d.get('t')); print('service:', d.get('s'))
"
```

Cross-check against `~/.cloudflared/*.json`: a credentials file named `<first-8-hex>-<host>.json`
means that tunnel was created from this machine. (On this host the service decoded to
`0ce9aa47-7d52-4d6a-9a16-13b48c508cff`, matching `~/.cloudflared/0ce9aa47-tquangdell.json`.)

This settles "is my local service even the tunnel that owns this hostname?" BEFORE hunting for API
tokens — and it is the fast way to rule your own machine out when the answer is no.

## TRAP: `~/.cloudflared/config.yml` can be stale and point at the WRONG origin

On a token-managed service the local `config.yml` is not what runs. Treat its contents as history,
never as the live ingress. Verified 2026-10-14: `config.yml` mapped `llm.theliems.com →
http://127.0.0.1:8080`, but port 8080 on that machine was a **Vite dev server for an unrelated ERP
app**, not an LLM endpoint. Reading that file to reason about the live tunnel would have produced a
completely wrong conclusion about where traffic lands.

Rule: derive the live ingress from the Cloudflare API (`GET .../cfd_tunnel/{id}/configurations`) or
from the tunnel logs' "Updated to new configuration" JSON. Never from `config.yml` when the service
was started with `--token`.

## Why this matters

When you first create a tunnel via `cloudflared tunnel create`, it may be created with `config_src: local`. But if you ever use `cloudflared tunnel route dns` or the Cloudflare dashboard to modify routing, it can switch to `config_src: cloudflare`. After that, all local YAML changes are ignored — you must use the API to update routing rules.

## Reproduction path

1. Created tunnel with local YAML config
2. Ran `cloudflared tunnel route dns <id> bot.domain.com` 
3. This created a DNS record AND switched the tunnel to API-based config
4. All subsequent local YAML edits had no effect
5. Tunnel returned 404 for new hostnames because the API config still had the old rules
6. Fix: `PUT /cfd_tunnel/{id}/configurations` with the full ingress array including the new hostname
