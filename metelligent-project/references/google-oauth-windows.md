# Google OAuth Setup on Windows — Troubleshooting Reference

## Setup Flow (từ skill google-workspace)

```bash
GSETUP="python /c/Users/NTQUANG_DELL/AppData/Local/hermes/skills/productivity/google-workspace/scripts/setup.py"
$GSETUP --client-secret /path/to/client_secret.json   # Bước 1
$GSETUP --auth-url                                     # Bước 2 → gửi link cho user
$GSETUP --auth-code "CODE_OR_URL"                      # Bước 3 → exchange token
```

## Windows-specific Paths

- Hermes home: `C:\Users\<user>\AppData\Local\hermes\` (NOT `~/.hermes/`)
- Token: `AppData\Local\hermes\google_token.json`
- Pending OAuth: `AppData\Local\hermes\google_oauth_pending.json`
- Client secret: `AppData\Local\hermes\google_client_secret.json`

## Multiple Google Accounts

Lưu token riêng cho mỗi account:

```bash
# Backup current
cp google_token.json google_token_accountA.json

# After new --auth-code exchange:
cp google_token.json google_token_accountB.json

# Switch:
cp google_token_{accountA,accountB}.json google_token.json
```

## Common Errors & Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `403: access_denied` | User not in test users list | [Add test user](https://console.cloud.google.com/auth/audience) |
| `403: org_internal` | OAuth consent = Internal | Chuyển sang **External** in [OAuth consent screen](https://console.cloud.google.com/auth/overview) |
| `ERR_UNSAFE_PORT` | redirect_uri=localhost:1 | **Expected** — code ở trong URL, chỉ cần copy URL |
| `invalid_grant: code_verifier mismatch` | Auth URL không khớp pending state | Luôn dùng URL từ `--auth-url`, không tự rút gọn/thay đổi |
| `ModuleNotFoundError: _cffi_backend` | Thiếu cffi trong venv | `pip install cffi` vào Python chính (không phải Hermes venv) |
| Token expired | Hết hạn (24h với testing app) | Chạy lại `--auth-url` + `--auth-code` |

## Scope Notes

- Chỉ request scopes cần thiết. Nếu chỉ cần Sheets + Drive, không request Gmail/Calendar.
- Testing app: token hết hạn sau 7 ngày. Publish app để có token vĩnh viễn.
- Khi grant chỉ 1 phần scopes, script tự động lưu granted_scopes thay vì requested_scopes.
