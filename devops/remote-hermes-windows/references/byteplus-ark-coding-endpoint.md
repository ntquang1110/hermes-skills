# BytePlus Ark — endpoint coding plan

Ghi lại từ session setup `lqremote` (2026-10-07). Key dạng
`VxCgNvLTE.<base64>.<base64>`; phần base64 giữa decode ra chuỗi có `kkey-<YYYYMMDD>`
nên nhìn là đoán được ngày phát hành.

## Hai endpoint khác nhau, đừng lẫn

| Endpoint | Dùng cho |
|----------|----------|
| `https://ark.ap-southeast.bytepluses.com/api/v3` | Model Ark thường (pay-as-you-go) |
| `https://ark.ap-southeast.bytepluses.com/api/coding/v3` | **coding plan** — chỉ nhóm model nằm trong gói |

Cùng một key có thể chạy ở endpoint này mà 401/`UnsupportedModel` ở endpoint kia.

## `/api/coding/v3` giới hạn model

Gọi `deepseek-v3-1-250821` (model hợp lệ ở endpoint thường) vào coding endpoint:

```json
{"error":{"code":"UnsupportedModel","message":"The requested model does not
support the coding plan feature. Please refer to the documentation at
https://docs.byteplus.com/en/docs/ModelArk/1925114 to select a compatible model."}}
```

Verify được chạy:

| Model | Kết quả |
|-------|---------|
| `deepseek-v4-flash-260425` | PASS — trả `"5"`, có cả `reasoning_content` |
| `deepseek-v3-1-250821` | `UnsupportedModel` |

Nên **probe model trước khi set `model.default`**, đừng tin danh mục.

## Probe 20 giây, trước khi đụng vào Hermes

```bash
KEY='<key>'
URL='https://ark.ap-southeast.bytepluses.com/api/coding/v3/chat/completions'
curl -s -m 40 -X POST "$URL" \
  -H "Authorization: Bearer $KEY" -H 'Content-Type: application/json' \
  -d '{"model":"deepseek-v4-flash-260425",
       "messages":[{"role":"user","content":"Tra loi ngan: 2+3=?"}],
       "max_tokens":40}' | head -c 600
```

Phân loại kết quả:

- `choices[...]` có `content` → key + model OK, set vào Hermes được.
- `UnsupportedModel` → key **đúng**, chỉ sai model cho endpoint này.
- `401` / `InvalidApiKey` → key sai hoặc dính BOM khi ghi `.env`.

## Khối config đã chạy được

```yaml
model:
  default: deepseek-v4-flash-260425
  provider: ark
  base_url: https://ark.ap-southeast.bytepluses.com/api/coding/v3
providers:
  ark:
    base_url: https://ark.ap-southeast.bytepluses.com/api/coding/v3
    name: BytePlus Ark
    api_key: <key>          # TRỰC TIẾP, không dùng key_env
    discover_models: true
```

Lệnh set, **đúng thứ tự** (đổi `provider` sẽ xóa `base_url` cũ):

```powershell
& "$H" config set providers.ark.base_url "https://ark.ap-southeast.bytepluses.com/api/coding/v3"
& "$H" config set providers.ark.name "BytePlus Ark"
& "$H" config set providers.ark.api_key "<key>"
& "$H" config set providers.ark.discover_models true
& "$H" config set model.provider ark
& "$H" config set model.default deepseek-v4-flash-260425
& "$H" config set model.base_url "https://ark.ap-southeast.bytepluses.com/api/coding/v3"
```

`api_key` để trực tiếp trong `config.yaml` — `key_env` đã trả 401 với key dạng này.

## Nghiệm thu cuối

```powershell
& "$H" -z "Tra loi ngan gon: 2 cong 3 bang may?"
```

Phải ra `5.`. Nếu ra `Hermes is not connected to any AI provider yet` thì
provider chưa nhận — đọc lại `hermes config get model.provider` và
`hermes config get providers.ark.base_url`, đừng đoán.

## Chưa có fallback

Setup này chỉ có 1 provider. Endpoint Ark chết là bot đứng. Muốn chain thì thêm
`fallback_providers` ở top-level (xem mục "Dựng chuỗi fallback" trong SKILL.md).
