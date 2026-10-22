---
name: hermes-mcp-integration
title: Hermes MCP Integration
description: "Cài/verify MCP servers trong Hermes (Lark/Feishu...)."
tags: [hermes, mcp, lark, feishu, integration, config]
domain: software-development
---

# Hermes MCP Integration

Cài MCP server vào Hermes: config nằm ở `mcp_servers` trong `~/AppData/Local/hermes/config.yaml`; Hermes tự discover tools lúc gateway start, đặt prefix `mcp_<server>_<tool>`.

## Khi nào dùng

- User yêu cầu "cài/kết nối MCP X", "connect lark/feishu/notion...", "dùng API Lark qua agent"
- Thêm/kiểm tra/sửa MCP server trong Hermes config
- Verify MCP server chạy được trước khi restart gateway

## Cấu hình

Hai transport (xem thêm reference `hermes-agent` bundled skill → native-mcp.md):

```yaml
mcp_servers:
  # stdio — command chạy subprocess
  time:
    command: "uvx"
    args: ["mcp-server-time"]
  # stdio qua wrapper script (secret không nhét thẳng config)
  lark:
    command: "bash"
    args: ["C:/Users/NTQUANG_DELL/AppData/Local/hermes/scripts/lark_mcp.sh"]
  # HTTP
  remote_api:
    url: "https://mcp.example.com/mcp"
    headers:
      Authorization: "Bearer sk-..."
```

**QUY TẮC VÀNG — secret KHÔNG vào config.yaml:**
- `patch` tool CHẶN ghi config.yaml (security-sensitive) → dùng `hermes config set mcp_servers.<name>.command bash` + `hermes config set mcp_servers.<name>.args '["..."]'` (set được, args là list).
- Secret (app_id, app_secret, token) đặt trong `~/AppData/Local/hermes/.env` với tên rõ ràng, rồi wrapper script đọc từ đó.
- MCP subprocess chỉ nhận env trắng + biến khai báo trong `env:` — KHÔNG tự kế thừa .env, nên wrapper script đọc file là bắt buộc.

## Pattern wrapper script (stdio + secret từ .env)

Script trong `~/AppData/Local/hermes/scripts/<name>_mcp.sh`:

```bash
#!/usr/bin/env bash
ENV_FILE="$HOME/AppData/Local/hermes/.env"
APP_ID=""
APP_SECRET=""
if [ -f "$ENV_FILE" ]; then
  APP_ID=$(grep -E '^XXX_MCP_APP_ID=' "$ENV_FILE" | head -1 | cut -d= -f2-)
  APP_SECRET=$(grep -E '^XXX_MCP_APP_SECRET=' "$ENV_FILE" | head -1 | cut -d= -f2-)
fi
if [ -z "$APP_ID" ] || [ -z "$APP_SECRET" ]; then
  echo "missing XXX_MCP_APP_ID/SECRET in .env" >&2
  exit 1
fi
exec npx -y @some/mcp-package mcp -a "$APP_ID" -s "$APP_SECRET" [flags]
```

Ghi key vào .env: `echo "XXX_MCP_APP_ID=<value>" >> .env` (sed nếu đã có). Verify: `grep -E "^XXX_MCP_" .env | sed 's/=\(.\{6\}\).*/=\1.../'`.

## Verify MCP server KHÔNG cần restart gateway

Pipe JSON-RPC vào stdin (stdio transport):

```bash
printf '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}\n{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}\n' | timeout 45 bash C:/Users/NTQUANG_DELL/AppData/Local/hermes/scripts/lark_mcp.sh 2>/dev/null | python -c "
import json,sys
for line in sys.stdin:
    line=line.strip()
    if not line: continue
    try:
        d=json.loads(line)
        if d.get('id')==1:
            print('INIT OK:', d.get('result',{}).get('serverInfo',{}).get('name'))
        if d.get('id')==2:
            tools=d.get('result',{}).get('tools',[])
            print('TOOLS:', len(tools))
    except: pass
"
```

Kỳ vọng: `INIT OK` + số tools. Server im lặng chờ stdin là BÌNH THƯỜNG — đừng kết luận hỏng vì không có output khi chạy trần.

## Restart gateway

Sau khi config xong cần restart Hermes gateway để nạp MCP tools. Hermes shell không admin → user tự restart (Terminal Admin).

## Pitfalls

- **args phải là YAML list**, không phải string JSON: `args: ["-y", "pkg"]` ✓ / `args: '["-y","pkg"]'` ✗ (ValidationError `args Input should be a valid list` — lỗi graft_volden đã gặp, spam errors.log mỗi ~3 phút). Fix bằng `hermes config set` hoặc sed.
- **`context_length: ''` rỗng** → warning mỗi session `Invalid model.context_length` → sửa thành số nguyên.
- Nếu MCP server cần OAuth user token (vd lark --oauth): redirect URL mặc định `http://localhost:3000/callback` phải khai trong dev console app.
- **Remote MCP server có OAuth (vd Canva `https://mcp.canva.com/mcp`) — dùng `mcp-remote` wrapper:**
  `args: ['-y', 'mcp-remote@latest', '<remote-mcp-url>']`. mcp-remote tự lo OAuth (PKCE, callback local).
  Callback trỏ `127.0.0.1:<port>` → phải bấm link authorize TRÊN CHÍNH máy chạy mcp-remote. Mở từ
  phone/máy khác thì callback báo "refused to connect", **nhưng URL trên address bar vẫn còn nguyên
  `?code=...&state=...` để copy** — đó là đường vòng duy nhất, đừng bỏ qua. Sau khi "authorization
  successful", process mcp-remote có thể tự exit → restart Hermes để spawn lại + đọc token cache
  (không phải login lại).
  - **Token cache KHÔNG phải `~/.mcp-auth/mcp-remote-v1/tokens.json` — ghi vậy là SAI** (đã verify
    2026-10-07). Thật ra là **2 file đặt tên theo hash của server URL**:
    `~/.mcp-auth/mcp-remote-v1/<md5(serverUrl)>_tokens.json` +
    `<md5(serverUrl)>_client_info.json`. Vd `md5("https://mcp.canva.com/mcp")` =
    `67a2071180bfcf76a3985779a9a38813`. `_tokens.json`: `refresh_token, access_token, token_type,
    expires_in, scope, expires_at` (`expires_at` là epoch **ms**). `_client_info.json`: `client_id,
    redirect_uris, token_endpoint_auth_method`.
  - **"(4h + refresh)" nghe như tự gia hạn mãi — KHÔNG đúng.** access token 14400s (4h), còn refresh
    token chết sau khoảng 30 ngày. Cache tạo 04/09 dùng tới 07/10 → `Proactive token refresh failed,
    falling back to the stored token` rồi vẫn đòi auth lại. **Copy cache sang máy khác KHÔNG phải cách
    bắc cầu** — chỉ hoãn được khi token còn sống. Muốn máy mới dùng được thì authorize lại tại máy đó.
  - **Đường ngắn nhất để cài: `hermes mcp catalog` → `hermes mcp install <name>`** (Canva có sẵn trong
    catalog). ⚠️ `install` in `✓ Installed '<name>' (enabled)` nhưng khi OAuth chưa xong thì **không có
    tool nào**, mà `hermes mcp list` vẫn báo `✓ enabled`. **`enabled` KHÔNG phải bằng chứng dùng được** —
    phải thấy tool thật load (agent liệt kê tool, hoặc `hermes mcp test <name>`).
  - `hermes mcp add` và `hermes mcp remove` **treo khi không có TTY**: `remove` chờ xác nhận (`--yes`
    không tồn tại → `usage: hermes`), `add` probe server (tải npx + OAuth) không bao giờ xong. Chạy
    trong PTY (`get_pty=True` rồi bơm `y\n`), hoặc sửa thẳng entry trong `config.yaml`.
  - Chi tiết đầy đủ (metadata OAuth của Canva, dynamic client registration, vì sao nên đăng ký client
    mới): `references/canva-connect-oauth.md`, và skill `remote-hermes-windows`
    → `references/remote-credential-porting.md`.
- Tool naming: `mcp_<server_name>_<tool_name>` — server name là key trong mcp_servers (vd `mcp_lark_im_v1_message_create`).
- KHÔNG nhét giá trị secret vào SKILL.md/reference — chỉ ghi tên biến + vị trí lưu.

## Verify quyền Lark sau khi user cấp permission — tách 2 vấn đề

Khi user nói "đã cấp quyền rồi" mà test vẫn fail, ĐỪNG kết luận thiếu quyền vội. Tách bạch:

1. **Lỗi quyền** (permission scope thiếu) → test bằng `im_v1_chat_create` + `im_v1_message_create` với `receive_id_type=chat_id`. Bot tự vào group, không phụ thuộc user trong tenant. Nếu gửi vào group OK → quyền im:message ĐÃ đủ.
2. **Lỗi receive_id** (230001 invalid receive_id) → test `contact_v3_user_batchGetId` trước. Nếu response echo lại email nhưng KHÔNG có open_id/user_id → user KHÔNG tồn tại trong tenant với email đó. Đây KHÔNG phải lỗi quyền.
3. Test thẳng bằng curl (tenant_access_token) để loại trừ MCP strip field: `POST /open-apis/contact/v3/users/batch_get_id` và `POST /open-apis/im/v1/messages?receive_id_type=email`.

**Pitfall quan trọng (đã gặp 09/08):** email Gmail cá nhân (`xxx@gmail.com`) KHÔNG match user trong tenant Lark. batch_get_id echo lại email nhưng không trả open_id → message_create lỗi 230001. PHẢI dùng email domain công ty (`@kiemsaphia.com`) hoặc open_id từ console (Contacts → user → Open ID). Chi tiết: `references/lark-mcp-2026-08.md`.

## CLI bên thứ ba tự đăng ký MCP (TinyFish, ...)

Vài vendor có CLI tự ghi MCP entry + tải skill/plugin vào Hermes:
`npx -y @tiny-fish/cli@latest connect --all --api-key <key> --skip-launch --url "<mcp-url>"`

Chạy được, nhưng phải kiểm 3 điểm sau:

1. **Tên env var KHÔNG khớp.** CLI ghi `MCP_TINYFISH_API_KEY` vào `.env`, còn plugin bundled đọc
   `TINYFISH_API_KEY`. Thiếu biến thứ hai thì `hermes tinyfish status` báo `api_key_configured: false`
   dù MCP đã kết nối. Fix: **copy giá trị, không gõ lại key** —
   ```bash
   python -c "
   import re; p=r'C:\Users\NTQUANG_DELL\AppData\Local\hermes\.env'
   t=open(p,encoding='utf-8').read()
   k=re.search(r'^MCP_TINYFISH_API_KEY=(.+)$',t,re.M).group(1).strip()
   if not re.search(r'^TINYFISH_API_KEY=',t,re.M):
       L=t.split('\n'); i=next(i for i,l in enumerate(L) if l.startswith('MCP_TINYFISH_API_KEY='))
       L.insert(i+1,'TINYFISH_API_KEY='+k); open(p,'w',encoding='utf-8',newline='\n').write('\n'.join(L))
   "
   ```
2. **Bước cài plugin của CLI fail trên Windows.** Nó clone qua `file://` path MSYS
   (`file:///C:/Users/NTQUAN%7E1/...`) → `fatal: does not appear to be a git repository`.
   Đừng retry CLI. Cài thẳng bằng Hermes vì nó clone HTTPS:
   `hermes plugins install <org>/<repo>/<subdir> --enable` → `hermes gateway restart`.
   Plugin vào `plugins/<name>/`, đọc env từ `.env`.
3. **`doctor` KHÔNG tự sửa.** `npx -y @tiny-fish/cli@latest doctor --pretty` chỉ in `✓ / ⚠ / …`;
   tự đọc rồi chạy repair tương ứng. `… harness not installed` = máy không có harness đó, bỏ qua,
   đừng cố cài.

**Gọi TinyFish KHÔNG cần model Hermes** (dùng khi Hermes hết credit provider):
```bash
npx -y @tiny-fish/cli@latest search query "hacker news today top story"   # JSON ra stdout
```
Cú pháp là `search query <q>` — KHÔNG có `search <q>`, không có `web`, không có `call`.

⚠️ `hermes tinyfish status` có thể trả `ok: false` + `web_backend_configured: false` — plugin đã nạp
nhưng chưa trỏ backend web. Không phải lỗi cài đặt; tool MCP vẫn dùng được.

⚠️ Tool MCP chỉ xuất hiện ở session KHỞI ĐỘNG SAU khi cài. Thiếu tool thì **nói thiếu**, đừng cài lại.

## References

- `references/canva-connect-oauth.md` — Canva: **DÙNG OFFICIAL MCP server** (`mcp-remote @ https://mcp.canva.com/mcp`). Tự build Connect API OAuth thất bại (invalid_scope + Canva chặn hướng này). Đường tự-build chỉ để fallback. Có: phân biệt Apps SDK vs Connect API, PKCE flow, DNS route sai zone, thêm ingress callback qua tunnel.

- `references/lark-mcp-2026-08.md` — Lark/Feishu MCP chi tiết: package, domain Trung vs quốc tế, key set "KSP", tool presets, verify đã chạy + kết quả test 09/08.
- `references/lark-approval-api.md` — Approval API (duyệt phiếu Lark): dùng `tasks/query?topic=1` cho to-do (tasks/search trả 5.350 task lịch sử — BẪY), approve payload + field mapping, lỗi thường gặp, batch pattern + an toàn khi approve hàng loạt.
- `scripts/lark_approval_todo.py` — list + batch approve task approval Lark (tasks/query topic=1, loại trừ "Yêu cầu duyệt chi" mặc định, field mapping sẵn). Chạy `python <path>/lark_approval_todo.py [--approve]`.
