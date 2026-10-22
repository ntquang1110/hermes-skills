# Lark/Feishu MCP — cài đặt 07/08/2026

## Package

`@larksuiteoapi/lark-mcp` (v0.5.1, MIT) — MCP CHÍNH THỨC từ Lark OpenAPI team (maintainers @bytedance). Node >= 24, chạy qua npx. Repo: `larksuite/lark-openapi-mcp`.

## Domain — phân biệt QUAN TRỌNG

- **Feishu (Trung Quốc)**: mặc định `https://open.feishu.cn` — KHÔNG cần flag
- **Lark (quốc tế)**: phải thêm `-d https://open.larksuite.com` (hoặc `--domain`)

⚠️ App tạo ở domain nào chỉ dùng được ở domain đó. Máy Quang dùng **Lark quốc tế** (`.env` có `FEISHU_DOMAIN=lark`).

## Key set "KSP"

- User đặt tên bộ key MCP riêng là **"KSP"** (khác với app Feishu gateway `FEISHU_APP_ID/FEISHU_APP_SECRET` — app gateway KHÔNG dùng cho MCP).
- Lưu trong `~/AppData/Local/hermes/.env`: `KSP_MCP_APP_ID`, `KSP_MCP_APP_SECRET` (giá trị KHÔNG ghi vào skill/reference).
- Launcher: `~/AppData/Local/hermes/scripts/lark_mcp.sh` đọc 2 biến này từ .env, chạy:

```bash
exec npx -y @larksuiteoapi/lark-mcp mcp -a "$APP_ID" -s "$APP_SECRET" -d "https://open.larksuite.com" -l en
```

## Config trong Hermes

```yaml
mcp_servers:
  lark:
    command: bash
    args: ["C:/Users/NTQUANG_DELL/AppData/Local/hermes/scripts/lark_mcp.sh"]
```

Set bằng `hermes config set mcp_servers.lark.command bash` + `hermes config set mcp_servers.lark.args '["..."]'` (patch tool chặn config.yaml).

## Tool presets (đã verify 07/08 — 19 tools mặc định)

Preset mặc định `preset.default` expose 19 tools:
- **Bitable** (Base): `bitable_v1_app_create`, `appTable_create`, `appTableField_list`, `appTable_list`, `appTableRecord_create/search/update`
- **Contact**: `contact_v3_user_batchGetId` (email/phone → user id)
- **Docx**: `docx_v1_document_rawContent`, `docx_builtin_search`, `docx_builtin_import`
- **Drive**: `drive_v1_permissionMember_create`
- **IM**: `im_v1_chat_create`, `im_v1_chat_list`, `im_v1_chatMembers_get`, `im_v1_message_create` (gửi tin), `im_v1_message_list` (chat history)
- **Wiki**: `wiki_v1_node_search`, `wiki_v2_space_getNode`

Chọn tool riêng bằng `-t`: vd `-t "im.v1.message.create,im.v1.message.list,im.v1.chat.create,preset.calendar.default"`. Preset khác: xem docs `docs/reference/tool-presets/presets.md`.

## Flags hữu ích

- `-l en|zh` — ngôn ngữ mô tả tool (mặc định en)
- `--token-mode auto|user_access_token|tenant_access_token` — auto mặc định; user_access_token cho API truy cập data cá nhân
- `--oauth` — bật OAuth server lấy user token (redirect URL mặc định `http://localhost:3000/callback` phải khai trong dev console)
- `-m stdio|sse|streamable` — transport (mặc định stdio)
- `--debug` — debug mode

## Verify đã chạy (07/08)

- `npx -y @larksuiteoapi/lark-mcp mcp --help` → ok
- Pipe initialize + tools/list → `INIT OK: Feishu/Lark MCP Server`, `TOOLS: 19`
- Lưu ý: chạy trần (không pipe) server im lặng chờ stdin — BÌNH THƯỜNG, không phải lỗi.

## Verify 09/08 — sau khi cấp quyền (test OK đầy đủ)

Quyền app KSP đã cấp đủ (im:message, contact, chat...). Toàn bộ flow hoạt động:
- `contact_v3_user_batchGetId` với email `<EMAIL>` → trả `user_id: ou_eac881f6920ef15f97970faf059ddc1f` (activated)
- `im_v1_message_create` receive_id_type=email → GỬI THÀNH CÔNG (message_id om_...)
- `im_v1_chat_create` → tạo group OK; `im_v1_message_create` với chat_id → OK; `im_v1_message_list` → đọc history OK

**PITFALL QUAN TRỌNG:** email Gmail (`<EMAIL>`) KHÔNG match user trong tenant — batch_get_id echo lại email nhưng không trả open_id → message_create lỗi `230001 invalid receive_id`. PHẢI dùng email domain công ty (`@kiemsaphia.com`) hoặc open_id lấy từ console (Contacts → user → Open ID).

## Giới hạn đã biết

- File upload/download CHƯA hỗ trợ
- Chỉnh sửa cloud doc trực tiếp CHƯA hỗ trợ (chỉ import + đọc)
- Non-preset API chưa qua compat testing — dùng preset trước
