# Bê credential Google + Canva sang máy đích

Ghi lại từ session 2026-10-07 (máy `lqremote`, user `NLQuan`). Phân biệt rõ
**đã verify** với **chưa chạy hết** — đừng đọc phần chưa verify thành công thức.

## 1. Google: token của Hermes port được sang máy khác — ĐÃ VERIFY

`google_token.json` là OAuth user token có `refresh_token`, nên **copy nguyên file
sang máy khác là dùng được ngay**. Không cần OAuth lại, không cần Cloud Console.

```python
sftp.put(local_google_token, f"C:/Users/<user>/AppData/Local/hermes/google_token.json")
```

Verify bằng query thật từ máy đích (không đoán): `drive.files().list()` +
`spreadsheets().get()` đều trả dữ liệu thật. Access token hết hạn thì
`Credentials.from_authorized_user_file()` + `c.refresh(Request())` tự gia hạn và
ghi lại file.

### Field `account` thường TRỐNG — đừng đọc nó để trả lời "tài khoản nào"

`google_token.json` có field `account` nhưng thường rỗng. Hỏi thẳng API:

```python
u = build("drive", "v3", credentials=c).about().get(
        fields="user(displayName,emailAddress)").execute()
print(u["user"]["emailAddress"], u["user"]["displayName"])
```

Đây là câu trả lời đúng cho câu hỏi "máy đó dùng tài khoản Google nào".

### Nhiều file token: kiểm từng cái, đừng copy cả loạt

Session này copy 3 file (`google_token.json`, `_kiemsaphia`, `_gmail`) — chỉ 1 file
sống. Hai file kia chết theo hai kiểu khác nhau:

| File | Lỗi | Nghĩa |
|---|---|---|
| `google_token_kiemsaphia.json` | `ValueError: time data '1784275931' does not match format '%Y-%m-%dT%H:%M:%S'` | field `expiry` là **unix timestamp số**, không phải ISO — client hiện tại không parse được |
| `google_token_gmail.json` | `RefreshError: invalid_grant` | refresh token đã bị thu hồi/hết hạn |

→ Verify từng token trên máy đích rồi **xoá file chết** khỏi máy đích, để lượt sau
không mất thời gian thử nhầm.

### Dựng `google_client_secret.json` từ token cũ (bỏ qua Cloud Console)

Token đã có sẵn `client_id` + `client_secret`. Bơm thẳng vào file desktop-app:

```python
secret = {"installed": {
    "client_id": token["client_id"], "client_secret": token["client_secret"],
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "redirect_uris": ["http://localhost"]}}
```

Rồi `setup.py --client-secret <path>`. Tiết kiệm cho anh cả bước tạo OAuth client.

⚠️ Nhưng tài khoản Google MỚI phải là **test user** của project đó (hoặc app đã
publish), không thì `Error 403: access_denied`. Console ở
`https://console.cloud.google.com/auth/audience` → Audience → Test users.

### `setup.py --auth-url` bản trên máy đích có thể KHÔNG có `--services`/`--format`

Skill `google-workspace` (bản Nous) ghi `--auth-url --services all --format json`.
Bản script trên máy thật chỉ nhận:

```
setup.py [-h] (--check | --check-live | --client-secret PATH |
          --auth-url | --auth-code CODE | --revoke | --install-deps)
```

Gọi kèm `--services` → `error: unrecognized arguments` (exit 2). Đọc usage từ
chính máy đó trước, rồi gọi `--auth-url` trần.

Session OAuth dở dang **lưu trên disk** (`google_oauth_pending.json`) nên sống qua
nhiều lượt chat — sinh URL ở lượt này, đổi code ở lượt sau vẫn được. Hết hạn thì
sinh lại URL mới.

## 2. Canva MCP: những gì ĐÃ VERIFY

### Canva có sẵn trong catalog của Hermes

```powershell
& $H mcp catalog                    # canva → "Create, search, and manage Canva designs."
& $H mcp install canva
```

`mcp install canva` cài xong ở dạng **native OAuth**, ghi vào config:

```yaml
mcp_servers:
  canva:
    url: https://mcp.canva.com/mcp
    auth: oauth
    enabled: true
```

Nhưng khi probe nó cần OAuth → over SSH nó in ra authorize URL rồi **chờ paste
redirect URL**, cuối cùng `PROBE FAILED ... timed out after 30s`. Cài được nhưng
vẫn "installed with no tool filter (all tools enabled when reachable)".

### Metadata OAuth — ĐÃ VERIFY (HTTP 200)

```
https://mcp.canva.com/.well-known/oauth-authorization-server
  authorization_endpoint  https://mcp.canva.com/authorize
  token_endpoint          https://mcp.canva.com/token
  registration_endpoint   https://mcp.canva.com/register
  client_id_metadata_document_supported  true
  code_challenge_methods_supported       ["plain","S256"]

https://mcp.canva.com/.well-known/oauth-protected-resource
  resource https://mcp.canva.com
  16 scope: profile:read design:meta:read design:content:read|write
            folder:read|write brandtemplate:content|meta:read,
            brandtemplate:content:write comment:read|write asset:read|write
            brandkit:read help:answers:read|write
```

### Dynamic client registration chạy được — ĐÃ VERIFY

```python
POST https://mcp.canva.com/register
{"client_name": "Hermes Agent (<MACHINE>)",
 "redirect_uris": ["http://127.0.0.1:29865/oauth/callback"],
 "grant_types": ["authorization_code", "refresh_token"],
 "response_types": ["code"], "token_endpoint_auth_method": "none"}
# → 201 {"client_id": "q2HLifbzP-5jP72n", "registration_client_uri": "/register/..."}
```

**Đừng tái dùng client đăng ký từ tháng trước** — đăng ký mới rẻ và chắc hơn.

### Token cache của `mcp-remote`: tên file = md5(server URL) — ĐÃ VERIFY

```
~/.mcp-auth/mcp-remote-v1/<md5>_tokens.json
~/.mcp-auth/mcp-remote-v1/<md5>_client_info.json
md5("https://mcp.canva.com/mcp") = 67a2071180bfcf76a3985779a9a38813
```

Trong `_tokens.json`: `refresh_token, access_token, token_type, expires_in,
scope, expires_at` (expires_at là **epoch ms**). `_client_info.json`:
`client_id, redirect_uris, token_endpoint_auth_method, client_name`.

### Token Canva CHẾT sau ~30 ngày — copy sang máy khác là vô ích

`expires_in` chỉ 14400s (4h) và refresh token không sống lâu. Copy cache sang máy
mới thì `mcp-remote` log:

```
Proactive token refresh failed, falling back to the stored token
Please authorize this client by visiting: https://mcp.canva.com/authorize?...
```

rồi vẫn đòi auth lại. **Đừng copy cache Canva sang máy khác như một cách bắc cầu** —
nó chỉ hoãn được khi token còn sống.

### Config sang dạng stdio mcp-remote (để dùng token cache)

```yaml
mcp_servers:
  canva:
    command: C:\Users\<user>\AppData\Local\hermes\tools\node\npx.cmd
    args:
      - "-y"
      - mcp-remote@latest
      - https://mcp.canva.com/mcp
    enabled: true
```

`hermes mcp list` và `hermes config check` đọc đúng dạng này — đã verify.

## 3. Phần CHƯA chạy hết — đừng trích thành công thức

Còn lại là bước người dùng bấm Approve rồi `--auth-code` / đổi code lấy token.
**Session chưa chạy xong bước đó.** Khi cần, đọc lại flow thật rồi mới kết luận;
đừng tin phần này như đã kiểm chứng.

Cấu trúc flow để tham chiếu: sinh PKCE (`code_verifier` → S256 → base64url không
padding) → build `authorize` URL kèm `resource=https://mcp.canva.com/mcp` → người
dùng approve → browser fail ở `http://127.0.0.1:29865/oauth/callback` (bình thường,
URL còn nguyên trên address bar để copy) → đổi code ở `token_endpoint`.

Link authorize hợp lệ khi mở ra **trang login Canva**, không phải trang lỗi. Test
trước khi gửi anh — đó là cách verify duy nhất không cần bấm Approve.
