# Cloudflare Tunnel Remote Config via API

When tunnel runs, it picks up config from **Cloudflare Dashboard** (remote) — not the local `config.yml`. The tunnel log shows:

```
Updated to new configuration config={...} version=N
```

This means any local `config.yml` changes are ignored unless the tunnel is stopped and the remote config is cleared. Better approach: **update the remote config directly via API**.

## Find tunnel token

The tunnel token is stored in `~/.cloudflared/cert.pem`:

```
-----BEGIN ARGO TUNNEL TOKEN-----
eyJ...base64...
-----END ARGO TUNNEL TOKEN-----
```

Decode the base64 payload:

```python
import base64, json
b64 = "eyJ..."  # without headers/footers
b64 += '=' * (4 - len(b64) % 4) if len(b64) % 4 else ''
data = json.loads(base64.b64decode(b64))
# data = {"zoneID":"...","accountID":"...","apiToken":"cfut_..."}
```

The `apiToken` field (`cfut_...`) is a Cloudflare API token scoped for Tunnel operations.

## Get current tunnel config

```bash
TOKEN="cfut_..."
ACCOUNT="<accountID>"
TUNNEL_ID="<tunnel-uuid>"

curl -s -H "Authorization: Bearer $TOKEN" \
  "https://api.cloudflare.com/client/v4/accounts/${ACCOUNT}/cfd_tunnel/${TUNNEL_ID}/configurations"
```

## Update tunnel config (add hostname)

```bash
curl -s -X PUT \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  "https://api.cloudflare.com/client/v4/accounts/${ACCOUNT}/cfd_tunnel/${TUNNEL_ID}/configurations" \
  -d '{
    "config": {
      "ingress": [
        {"service": "http://localhost:5099", "hostname": "me.example.com"},
        {"service": "http://localhost:3000", "hostname": "example.com"},
        {"service": "http_status:404"}
      ],
      "warp-routing": {"enabled": false}
    }
  }'
```

Update is immediate — tunnel picks up new config in seconds without restart.

## Pitfalls

### 🔴 Credentials mismatch: "Unauthorized: Tunnel not found"

The credential JSON file (`*.json`) contains a `TunnelID` field. If this ID doesn't match the actual tunnel in your Cloudflare account, the tunnel fails with:

```
ERR Register tunnel error from server side error="Unauthorized: Tunnel not found"
```

**Fix:** Get the correct token and credentials for the tunnel:

```bash
# 1. List tunnels to find the correct UUID
cloudflared tunnel list

# 2. Get the tunnel's token
cloudflared tunnel token TUNNEL-NAME

# 3. Decode token (JSON base64) to extract accountTag + secret + tunnelID
python -c "
import base64, json, sys
b64 = sys.stdin.read().strip()
b64 += '=' * (4 - len(b64) % 4) if len(b64) % 4 else ''
d = json.loads(base64.b64decode(b64))
creds = {'AccountTag': d['a'], 'TunnelSecret': d['s'], 'TunnelID': d['t'], 'Endpoint': ''}
with open('tunnel-creds.json', 'w') as f:
    json.dump(creds, f)
"

# 4. Update config.yml to reference the new credentials file
# tunnel: <correct-uuid>
# credentials-file: C:\Users\<user>\.cloudflared\tunnel-creds.json
```

### 🔴 Protocol failure (QUIC)

If tunnel reconnects in a loop with `control stream failure`:

```bash
# Switch from QUIC (default) to HTTP2
cloudflared tunnel --config config.yml run --protocol http2
```

HTTP2 is more reliable behind restrictive networks (Vietnam, corporate firewalls).

### 🔴 WARP interference (Vietnam users)

Cloudflare WARP + cloudflared tunnel conflict. Symptoms: tunnel connects/disconnects in loop, no stable connection.

**Fix:** Disconnect WARP before starting tunnel:
```bash
"c:\Program Files\Cloudflare\Cloudflare WARP\warp-cli.exe" disconnect
# Then start tunnel
```

### 🔴 Windows path for --config flag

cloudflared is a Windows native binary — it does NOT understand MSYS paths like `/c/Users/...`.

✅ Correct: `--config "C:\Users\user\.cloudflared\config.yml"`
❌ Wrong: `--config /c/Users/user/.cloudflared/config.yml`

In bash scripts, use single or double quotes around the Windows path.

## DNS Record Creation via API

The tunnel API token (`cfut_*`) from `cert.pem` can also manage DNS records for zones it has access to.

### 1. Find zone ID

```bash
TOKEN="cfut_..."
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://api.cloudflare.com/client/v4/zones" \
  | python -c "import sys,json; [print(z['name'], z['id']) for z in json.load(sys.stdin)['result']]"
```

### 2. List existing CNAME records

```bash
ZONE_ID="<zone-id>"
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://api.cloudflare.com/client/v4/zones/${ZONE_ID}/dns_records?type=CNAME&per_page=50"
```

### 3. Create CNAME (point subdomain to tunnel)

```bash
curl -s -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  "https://api.cloudflare.com/client/v4/zones/${ZONE_ID}/dns_records" \
  -d '{
    "type": "CNAME",
    "name": "subdomain",       # just "kflow" → becomes kflow.example.com
    "content": "<tunnel-uuid>.cfargotunnel.com",
    "ttl": 1,                   # 1 = Auto
    "proxied": true             # ☁️ Orange cloud
  }'
```

### 4. Create A record (change root domain IP)

```bash
curl -s -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  "https://api.cloudflare.com/client/v4/zones/${ZONE_ID}/dns_records" \
  -d '{
    "type": "A",
    "name": "@",
    "content": "<ip-address>",
    "ttl": 1,
    "proxied": true
  }'
```

### 5. Delete DNS record

```bash
RECORD_ID="<record-id>"
curl -s -X DELETE \
  -H "Authorization: Bearer $TOKEN" \
  "https://api.cloudflare.com/client/v4/zones/${ZONE_ID}/dns_records/${RECORD_ID}"
```

**⚠️ Note:** The `cfut_*` token may NOT have DNS permissions by default. If `zones` API returns zones but record creation fails, user needs to update the token scope in Cloudflare Dashboard to include `DNS:Edit`.

## Limitations

- The `cfut_*` token from `cert.pem` is **Tunnel-only scope** by default. Does NOT work for Workers, Pages, or other Cloudflare APIs without scope updates.
- For Workers, user needs a separate API token with `workers:edit` scope.
- DNS API requires the token to have `DNS:Edit` permission — can be added from Cloudflare Dashboard → API Tokens → edit token → add DNS permission.
