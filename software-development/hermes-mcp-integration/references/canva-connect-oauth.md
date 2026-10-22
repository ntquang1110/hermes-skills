# Canva integration vào Hermes — DÙNG OFFICIAL MCP server (09/2026)

**KẾT LUẬN CUỐI CÙNG (rút từ session thực chiến 09/2026): đừng tự build Connect API OAuth nữa.**
Khi user muốn "tự động hóa Canva" / "auto tạo design", đường ĐÚNG là **Canva MCP server chính thức**
qua `mcp-remote` — KHÔNG phải tự viết OAuth PKCE + Connect API. Canva chủ động chặn hướng tự-build.

## Vì sao Connect API tự-build THẤT BẠI (kinh nghiệm thực tế)
- Tạo app Connect API (`OC-...` + secret), tự dựng PKCE OAuth + local callback proxy qua Cloudflare tunnel.
- Canva trả `invalid_scope` LIÊN TỤC dù tăng/giảm scope ra sao (kể cả scope tối thiểu `design:content:read`).
  Lý do cốt lõi: app Connect API của user chưa được kích hoạt scope đúng trong hệ thống Canva, VÀ Canva
  chủ đích không cho hướng này.
- Canva hiện thông báo rõ: *"Only submit integrations you want to make available to all Canva users... If
  you're building an integration for personal use or testing, keep it private/draft. To connect tools like
  AI assistants to Canva, use the Canva MCP server."* + link `https://www.canva.dev/docs/mcp/`.

→ **Quyết định đúng: chuyển sang official MCP.** Không mất công tự build nữa.

## Cách connect Canva MCP chính thức (đã chạy, token thành công)

Canva cung cấp **remote MCP server**: `https://mcp.canva.com/mcp`.

Config vào `mcp_servers` trong `~/AppData/Local/hermes/config.yaml`:
```yaml
mcp_servers:
  canva:
    command: npx
    args:
      - '-y'
      - 'mcp-remote@latest'
      - 'https://mcp.canva.com/mcp'
    connect_timeout: 120
```
Lưu ý: KHÔNG dùng `@mcp_factory/canva-mcp-server` (server bên thứ 3, cần token tự lấy). Official dùng `mcp-remote`.

### Điều kiện tiên quyết từ Canva (waitlist)
- **Bắt buộc đăng ký redirect URI vào waitlist**: vào https://www.canva.dev/docs/mcp/ → "Apply for access
  with our Waitlist form". Điền company/goals/technical/timeline. Canva review và duyệt theo email
  (`<EMAIL>`). Trước khi duyệt thì redirect không được nhận → chưa connect được.
- Nhiều tool phổ biến (Claude, ChatGPT, Codex, Gemini) đã có sẵn quyền Canva MCP.

### OAuth: mcp-remote tự lo hết (không cần viết PKCE)
1. Chạy `npx -y mcp-remote@latest https://mcp.canva.com/mcp` — nó tự:
   - Phát hiện authorization server `https://mcp.canva.com`
   - Dựng OAuth callback server local `http://127.0.0.1:29865/oauth/callback`
   - Tự mở browser (máy chạy mcp-remote) với link authorize scope chuẩn (profile, design:content:read/write,
     design:meta, folder, brandtemplate, comment, asset, brandkit, help:answers...).
2. User bấm link **trên chính máy chạy mcp-remote** (redirect trỏ 127.0.0.1 — không mở từ phone/máy khác).
3. `Auth code received` → `Completing authorization...` → `Proxy established successfully`.
4. Token cache lưu tại `~/.mcp-auth/mcp-remote-v1/*_tokens.json` (`access_token`, `refresh_token`, `expires_at`).
   Scope OK, hạn 4h + refresh tự đổi.

### Verify token + tái khởi động
- Process mcp-remote sau khi callback thành công có thể tự exit → cần Hermes restart để Hermes spawn lại
  mcp-remote, nó đọc token cache `~/.mcp-auth/mcp-remote-v1/` (không cần đăng nhập lại).
- Trước khi restart: `hermes config set mcp_servers.canva.command npx` + args list + `connect_timeout`.

## 🔴 PITFALL: Read-through khi tự build Connect API (nếu quay lại đường này)
Phần này giữ lại cho lịch sử/fallback — nhưng ưu tiên official MCP.

### Phân biệt 2 loại app Canva
- **Apps SDK** (App ID dạng `AAHOGLYsoqQ`, env `CANVA_APP_ORIGIN=https://app-XXX.canva-apps.com`): chạy
  embedded trong editor, người bấm mới chạy. KHÔNG auto nền. KHÔNG dùng để server-side auto.
- **Connect API** (`OC-...` OAuth): REST `https://api.canva.com/rest/v1`, auto từ nền. Nhưng vướng invalid_scope + waitlist.

### PKCE + tunnel (đã làm, CÓ cạm bẫy)
- PKCE S256 bắt buộc: `code_verifier=token_urlsafe(64)`, `code_challenge=base64url(sha256(verifier))`.
- Redirect URI phải public HTTPS (Canva không nhận localhost) → expose callback server local qua
  Cloudflare named tunnel subdomain ổn định.
- Canva lại tự sinh link PKCE với `client_id=awGbsr0gX9QWNrDh` (client riêng của mcp-remote) khi dùng
  official — đó là lý do official tự thắng.

## DNS route sai zone (vẫn áp dụng nếu làm tunnel)
`cloudflared tunnel route dns` / POST DNS dùng `cert.pem` zoneID → cert.pem thường là **zone khác**
(vd cert.pem mang theliems.com, target là thefirstonly.com) → tạo nhầm `canva-oauth.theliems.com`.
**Fix:** resolve zone theo exact domain name, không dùng cert.pem zoneID:
```python
zones = cf("https://api.cloudflare.com/client/v4/zones?name=thefirstonly.com")
ZONE = zones[0]["id"]
```
Xóa record sai ở zone nhầm, tạo lại đúng zone, verify nslookup → Cloudflare IP.

## Thêm ingress + DNS cho callback (tunnel đang chạy, API-side config)
- GET current tunnel config → merge `{"hostname":"canva-oauth.<domain>","service":"http://127.0.0.1:<port>}`
  trước catch-all (`http_status:404` cuối) → PUT. Tunnel pick up ~30s, không cần restart.
- POST DNS CNAME `canva-oauth → <tunnel-uuid>.cfargotunnel.com` về **đúng zone**.
- Verify `curl https://canva-oauth.<domain>/` → 200.

## Scripts
- `D:/Hermes Proj/canva_oauth_server.py` — OAuth callback server PKCE (DÙNG CHO ĐƯỜNG TỰ-BUILD, không phải official).
- `D:/Hermes Proj/unsloth-ua-proxy.py` — proxy đổi UA (bài toán khác, xem skill unsloth-cloudflare-403-fix).