---
name: canva-automation
description: "Connect Hermes to Canva (MCP server) for automated design."
version: 1.0.0
platforms: [windows, macos, linux]
---

# Canva automation — connect Hermes to Canva for auto design/create

Khi agent cần tự động tạo/sửa/xuất Canva design (bulk posts, biến content thành ảnh).

## Có 3 đường — đừng nhầm

### 1. Canva MCP server CHÍNH THỨC (ưu tiên, khuyên dùng)
Canva cung cấp remote MCP server tại: `https://mcp.canva.com/mcp`
Docs: https://www.canva.dev/docs/mcp/

- Dùng **Client ID Metadata Document (CIMD)** — client_id là HTTPS URL trỏ JSON mô tả client, KHÔNG cần pre-register client hay quản client secret.
- Nhiều AI tool phổ biến (Claude, ChatGPT, Codex, Gemini...) đã tự publish CIMD → chạy out-of-box.
- Trong Hermes: đăng ký dạng HTTP MCP:
  ```yaml
  mcp_servers:
    canva:
      url: "https://mcp.canva.com/mcp"
  ```
- **Điều kiện bắt buộc**: phải **đăng ký redirect URI vào Canva MCP allowlist qua form Waitlist** (canva.dev → MCP → "Apply for access"). Canva xét: brand alignment, trust/safety, technical fit, strategic alignment. KHÔNG tự kích hoạt ngay — chờ duyệt.
- Nếu agent không support remote MCP, dùng stdio: `npx -y mcp-remote@latest https://mcp.canva.com/mcp`

### 2. Tự build qua Connect API + OAuth (làm được nhưng Canva KHÔNG khuyến khích)
Canva cảnh báo khi submit integration kiểu "chỉ cho mọi user Canva" — họ khuyên cá nhân/private/test DÙNG MCP SERVER thay vì tự build OAuth.

**Community server:** `@mcp_factory/canva-mcp-server`
```yaml
mcp_servers:
  canva:
    command: "npx"
    args: ["-y", "@mcp_factory/canva-mcp-server"]
    env:
      CANVA_ACCESS_TOKEN: "<token>"
```
**QUAN TRỌNG**: server này chỉ đọc `CANVA_ACCESS_TOKEN` (access token trực tiếp), KHÔNG dùng `CANVA_CLIENT_ID`/`CANVA_CLIENT_SECRET` (2 cái đó là cho MCP Bind riêng của hãng — không dùng được).

### 3. Hermes có sẵn Canva trong catalog MCP — đường ngắn nhất (đã verify)

```powershell
hermes mcp catalog                 # canva → "Create, search, and manage Canva designs."
hermes mcp install canva
```

Ghi vào config dạng native OAuth:

```yaml
mcp_servers:
  canva:
    url: https://mcp.canva.com/mcp
    auth: oauth
    enabled: true
```

**Nhưng vẫn bắt buộc có một NGƯỜI bấm Approve.** Trên máy không có browser
(SSH/headless) `mcp install` in authorize URL rồi chờ paste redirect URL, cuối cùng:

```
Probe failed: Connecting to MCP server 'canva' timed out after 30s
Couldn't probe server; installed with no tool filter (all tools enabled when reachable)
```

→ Cài xong, `hermes mcp list` báo `✓ enabled`, mà **không có tool nào**. `enabled`
KHÔNG phải bằng chứng dùng được. Đừng hứa với anh "cài xong là chạy" — hoặc đưa anh
một link để bấm, hoặc nói rõ còn thiếu bước người.

### Token/cache Canva bền bao lâu — copy cache KHÔNG phải cách bắc cầu

- access token `expires_in` = **14400s (4 giờ)**.
- refresh token KHÔNG sống lâu. Cache tạo 04/09 dùng tới 07/10 là chết; `mcp-remote`
  log `Proactive token refresh failed, falling back to the stored token` rồi **vẫn
  đòi auth lại**.
- Cache ở `~/.mcp-auth/mcp-remote-v1/<md5(server URL)>_tokens.json` +
  `..._client_info.json`. Tên file suy từ URL, không random:
  `md5("https://mcp.canva.com/mcp") = 67a2071180bfcf76a3985779a9a38813`.
- `_tokens.json` gồm `refresh_token, access_token, token_type, expires_in, scope,
  expires_at` (`expires_at` là **epoch ms**).

→ Muốn máy mới dùng được thì authorize lại **tại máy đó**. Copy cache chỉ hoãn được
khi token còn sống. Cách bê credential + phần Google liên quan ở skill
`remote-hermes-windows`, `references/remote-credential-porting.md`.

### Đăng ký client MỚI thay vì tái dùng client cũ

Metadata OAuth (đã verify HTTP 200):

```
https://mcp.canva.com/.well-known/oauth-authorization-server
  authorization_endpoint https://mcp.canva.com/authorize
  token_endpoint         https://mcp.canva.com/token
  registration_endpoint  https://mcp.canva.com/register
  client_id_metadata_document_supported true
  code_challenge_methods_supported      ["plain","S256"]

https://mcp.canva.com/.well-known/oauth-protected-resource
  resource https://mcp.canva.com   + 16 scope hợp lệ
```

Đây là **authorization server của MCP** (`mcp.canva.com`), KHÁC Connect API
(`api.canva.com`) ở mục 2. Đừng lẫn hai bộ endpoint.

Client đăng ký động từ tháng trước có thể đã hỏng; đăng ký mới mất 1 giây:

```python
POST https://mcp.canva.com/register
{"client_name": "Hermes Agent (<MÁY>)",
 "redirect_uris": ["http://127.0.0.1:29865/oauth/callback"],
 "grant_types": ["authorization_code", "refresh_token"],
 "response_types": ["code"], "token_endpoint_auth_method": "none"}
# → 201 {"client_id": "q2HLifbzP-5jP72n", "registration_client_uri": "/register/..."}
```

### Test link authorize TRƯỚC khi gửi anh

Link đúng khi mở ra **trang login Canva**, không phải trang lỗi. Đây là cách verify
duy nhất mà không cần bấm Approve — mở bằng browser tool trước; thấy form đăng nhập
nghĩa là link sống. Gửi anh link chết là mất cả một lượt.

**Fallback khi browser tool chết** (đã dùng 10/2026 khi Camofox trả 500 `/tabs`) —
validate bằng `curl`, không cần render trang:

```bash
curl -s -o /tmp/canva_check.html \
     -w "status=%{http_code}  redirect=%{redirect_url}\n" \
     -L --max-redirs 0 "<LINK AUTHORIZE>"
grep -oiE 'invalid_client|invalid_scope|invalid_request|unauthorized_client' /tmp/canva_check.html
```

Kỳ vọng: `status=302` + `redirect_url` trỏ sang
`https://www.canva.com/api/oauth/authorize?client_id=OC-AZb1vOWcedZR&...` —
mcp.canva.com tự proxy vào app Canva của họ và **tự sinh `code_challenge`/`state`
mới**. Cái đó không liên quan tới PKCE của mình, đừng nhầm là link hỏng. Body không
chứa chuỗi `invalid_*` = link sống.

Server re-write `code_challenge`/`state` khi proxy, nhưng verifier mình lưu lúc sinh
link **vẫn đổi được code** (server giữ mapping) — không cần sinh link mới sau mỗi lần
curl.

## OAuth flow (nếu tự build) — PKCE bắt buộc
Canva OAuth dùng **PKCE S256** (authorize link có `code_challenge_method=s256&code_challenge=...`). Không PKCE → Canva tự trả về link yêu cầu code_challenge.

Quy trình:
1. Server local sinh `code_verifier` + `code_challenge` (sha256 → base64url không padding)
2. Auth link: `https://www.canva.com/api/oauth/authorize?code_challenge_method=s256&response_type=code&client_id=<ID>&redirect_uri=<uri>&scope=<scopes>&code_challenge=<challenge>`
3. User bấm → login → approve → redirect `/callback?code=...`
4. Đổi code tại `https://api.canva.com/oauth/token` (grant_type=authorization_code, kèm `code_verifier`)
5. Token endpoint: `https://api.canva.com/oauth/token`

**Redirect URI PHẢI là HTTPS public** (Canva không nhận localhost) → expose qua Cloudflare subdomain tunnel (xem local-tunnel skill).

## Scope Canva — format `resource:permission`
Tên scope đúng (từ dashboard Canva, format `resource:read` / `resource:write`):
`app`, `asset`, `brandtemplate:content`, `brandtemplate:meta`, `comment`, `design:content`, `design:meta`, `design:permission`, `folder`, `folder:permission`, `profile`

Ví dụ scope string hợp lệ:
```
asset:read asset:write design:content:read design:content:write design:meta:read design:meta:write brandtemplate:content:read brandtemplate:content:write comment:read comment:write folder:read folder:write profile:read
```

**Pitfall invalid_scope**: `design:read:design`, `design:read:pages`, `export:write`, `export:read` KHÔNG nằm trong dashboard scope → gây `invalid_scope`. Phải match đúng tên scope trong dashboard của app. Nếu app chưa khai scope trong cài đặt thì dù link đúng cũng bị `invalid_scope` — KHÔNG phải lỗi link.

## Pitfall Cloudflare zone (khi expose callback)
cert.pem `zoneID` có thể là zone KHÁC với domain đích → `cloudflared tunnel route dns` tạo nhầm `sub.domain2.com`. Luôn resolve zone đúng:
```python
zones = cf("https://api.cloudflare.com/client/v4/zones?name=<domain>")["result"]
ZONE = zones[0]["id"]
```

## Files mẫu
- `canva_oauth_server.py` ở `D:/Hermes Proj/` — callback server PKCE, public qua tunnel `canva-oauth.thefirstonly.com`, lưu token vào `canva_token.json` + `canva_token.txt` (CANVA_ACCESS_TOKEN=...).
- Template sao chép được: `templates/canva_oauth_server.py` (đổi CLIENT_ID/CLIENT_SECRET/REDIRECT_URI/SCOPES cho từng app).
- Tunnel callback: dùng subdomain Cloudflare ỔN ĐỊNH (sub.thefirstonly.com), KHÔNG trycloudflare random vì redirect URI phải cố định để đăng ký. Đã dùng: `canva-oauth.thefirstonly.com` → localhost:8790 qua tunnel TQUANG-DELL.