# Cloudflare Tunnel Ingress via REST API

## When to use

- You need to add/remove/modify a subdomain route on an existing named tunnel
- You cannot use `wrangler` (lack of Workers API permissions) or edit config locally
- The tunnel uses **remote config** (ingress rules managed via Cloudflare API)

## Key endpoints

```
GET    /accounts/{account_id}/cfd_tunnel/{tunnel_id}/configurations  → read current ingress
PUT    /accounts/{account_id}/cfd_tunnel/{tunnel_id}/configurations  → replace ingress
```

## Authentication

Header: `Authorization: Bearer <API_TOKEN>`

**Token permissions required:**
- `Account > Tunnel > Edit` (minimum)
- NOT the same as Workers API token

## Read current config

```bash
curl -s "https://api.cloudflare.com/client/v4/accounts/$ACCOUNT_ID/cfd_tunnel/$TUNNEL_ID/configurations" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" | python -c "
import json, sys
d = json.loads(sys.stdin.read())
if d.get('success'):
    for r in d['result']['config']['ingress']:
        print(f'{r.get(\"hostname\",\"*\")} -> {r.get(\"service\",\"\")}')
"
```

## Add a new subdomain

Insert the new rule BEFORE the catch-all (`* → http_status:404`), which is always the last ingress entry.

```bash
# 1. Get current config
CURRENT=$(curl -s "https://api.cloudflare.com/client/v4/accounts/$ACCOUNT_ID/cfd_tunnel/$TUNNEL_ID/configurations" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN")

# 2. Add new rule before the catch-all
echo "$CURRENT" | python -c "
import json, sys
d = json.loads(sys.stdin.read())
config = d['result']['config']
ingress = config.get('ingress', [])
new_rule = {'hostname': 'preview.thefirstonly.com', 'service': 'http://localhost:3003'}
ingress.insert(-1, new_rule)  # before catch-all
config['ingress'] = ingress
print(json.dumps(config, ensure_ascii=False))
" > /tmp/new_config.json

# 3. Upload updated config
UPDATED=$(cat /tmp/new_config.json)
curl -s -X PUT "https://api.cloudflare.com/client/v4/accounts/$ACCOUNT_ID/cfd_tunnel/$TUNNEL_ID/configurations" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"config\": $UPDATED}"
```

## Verify

```bash
curl -sI "https://preview.thefirstonly.com" | head -1
# Expected: HTTP/2 200 or relevant response code
```

## Pitfalls

1. The `hostname` must already have a DNS CNAME record pointing to the tunnel (tunnel-id.cfargotunnel.com). Add via Cloudflare Dashboard → DNS.
2. The catch-all rule (`* → http_status:404`) is always the LAST rule in ingress. When inserting, always use `ingress.insert(-1, ...)`.
3. Config update propagates to tunnels within ~30 seconds. No restart needed.
4. If the API token lacks permissions, the PUT will return 403. Use the local config file approach instead.
