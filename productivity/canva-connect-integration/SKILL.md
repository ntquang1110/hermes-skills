---
name: canva-connect-integration
description: "Integrate Canva Connect API: OAuth token, MCP, auto-design."
version: 1.0.0
platforms: [linux, macos, windows]
---

# Canva Connect API integration (auto-design + MCP)

## Khi nào dùng
User muốn tự động hóa Canva: tự tạo design, tự fill template, xuất ảnh/bài đăng mà
không cần người bấm trong editor. Hai route khác nhau, đừng nhầm:

| Route | Cái gì | Cần gì |
|-------|--------|--------|
| **Connect API (REST)** | Hermes gọi thẳng từ nền, auto hoàn toàn | Client ID + Secret + OAuth access token |
| **Apps SDK** | App chạy embedded trong editor, người bấm mới chạy | CANVA_APP_ID + origin (khác hẳn) |

Nếu mục tiêu là "auto hoàn toàn, không ai bấm" → **Connect API**, KHÔNG dùng Apps SDK
(Apps SDK app id không dùng cho auto nền).

## MCP server (ưu tiên — user thích MCP hơn viết REST tay)

Package: `@mcp_factory/canva-mcp-server`. Tools: create design, upload asset, autofill
brand template, export PNG/PDF/PPTX/MP4, quản lý folders/comments.

**QUAN TRỌNG — auth của server nó:** bản này chỉ đọc **`CANVA_ACCESS_TOKEN`** (env).
Còn `CANVA_CLIENT_ID`/`CANVA_CLIENT_SECRET` trong README của hãng là để dùng dịch vụ
"MCP Bind" riêng (không tự đổi OAuth). Nên khi tự setup: phải lấy access token bằng
flow riêng, rồi truyền `CANVA_ACCESS_TOKEN`.

Đăng ký MCP trong config.yaml:
```yaml
mcp_servers:
  canva:
    command: npx
    args:
      - '-y'
      - '@mcp_factory/canva-mcp-server'
    env:
      CANVA_ACCESS_TOKEN: <oauth_token>
```
Lưu ý: `hermes config set mcp_servers.canva.args '[...]'` lưu thành **string JSON** chứ
không phải list YAML → phải sửa thành list thật (mỗi phần tử 1 dòng `- '...'`). Verify:
```bash
python -c "import yaml;d=yaml.safe_load(open(CFG));print(d['mcp_servers']['canva']['args'])"  # phải là list
```
Cần `pip install mcp` cho venv Hermes (nếu thiếu thì Hermes báo "MCP SDK not available").

## OAuth flow tự chạy (lấy access token)

Vì server chỉ đọc token, tự chạy OAuth:
1. App Connect API trên canva.com/developers → Client ID + Client Secret + set Redirect URI
2. Redirect URI PHẢI public HTTPS (Canva không nhận localhost). Expose local callback server
   qua tunnel ổn định (không dùng trycloudflare đổi liên tục).
3. Auth URL dạng:
   `https://www.canva.com/api/oauth/authorize?response_type=code&client_id=<ID>&redirect_uri=<URL_ENCODED>&scope=design:read:design,design:content:write,asset:write,export:write`
4. User bấm → đăng nhập Canva → approve → Canva redirect `?code=xxx` về callback
5. Đổi code lấy token: POST `https://api.canva.com/oauth/token`
   `grant_type=authorization_code&code=<code>&client_id=<ID>&client_secret=<SECRET>&redirect_uri=<URI>`
6. Lưu `access_token` + `refresh_token`, set CANVA_ACCESS_TOKEN

Redirect URI phải được khai đúng trên app Canva (Authentication tab). Nếu flow dài,
dùng dev-redirect nếu Canva cho phép (tránh phải expose tunnel khi chỉ muốn code 1 lần).

## Cloudflare tunnel cho redirect URI — pitfall zone

Khi thêm subdomain redirect vào named tunnel (như `canva-oauth.thefirstonly.com` → localhost:8790):
- **Thêm ingress**: GET config hiện tại `GET /accounts/{ACC}/cfd_tunnel/{TUNNEL}/configurations`,
  merge rule `{hostname, service: http://127.0.0.1:<PORT>}` TRƯỚC catch-all, PUT. Tunnel tự nhận ~30s.
- **DNS CNAME**: giải zone đúng cho domain (GET `/zones?name=<domain>`), KHÔNG dùng zoneID
  từ cert.pem — cert.pem mang zone của zone được issue (vd theliems.com), POST nhầm tạo
  `canva-oauth.theliems.com`. Luôn verify record tạo ra có tên đúng.

## Files đã có trên máy này
- `D:/Hermes Proj/canva_oauth_server.py` — callback server port 8790, redirect `https://canva-oauth.thefirstonly.com/callback`
- `D:/Hermes Proj/unsloth-ua-proxy.py` — UA rewrite proxy

## Trạng thái (09/2026)
Đã setup xong: MCP registered, OAuth server public sống. **Còn thiếu: access token**
(user cần thêm redirect URI + bấm auth link). Token chưa có → MCP chưa gọi được tool Canva.