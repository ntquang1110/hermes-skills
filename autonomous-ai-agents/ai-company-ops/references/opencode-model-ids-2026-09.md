# OpenCode model IDs — prefix `bytedance/` chết từ 15/09/2026

## Phát hiện (standup 15/09, verify thật bằng urllib + browser headers)
- Gọi `/chat/completions` với `bytedance/deepseek-v4-flash-260425` → **401 `ModelError "Model ... is not supported"`**.
- `GET /models` (200, 37 models) liệt kê bare IDs: `deepseek-v4-flash`, `deepseek-v4-pro`, `deepseek-flash`, `deepseek-v4.1-flash`, `deepseek-v4-flash-vision-exp` (+ kimi, glm, qwen, mimo, grok, gpt-5.6-luna...). KHÔNG còn ID nào mang prefix `bytedance/`.
- Gọi lại bằng bare IDs khi workspace hết credit → **401 `CreditsError "Insufficient balance"`** kèm link billing — phân biệt rõ 2 loại 401:
  - `ModelError/not supported` = sai tên model → đổi ID.
  - `CreditsError/Insufficient balance` = hết tiền → escalate Quang, đừng retry/wake agent.

## Quy tắc
- Mọi call mới dùng bare ID (`deepseek-v4-flash` default, `deepseek-v4-pro` fallback). Đừng dùng prefix `bytedance/...-260425` cũ trong code mới.
- Khi standup trả None toàn bộ: chẩn đoán theo thứ tự key hỏng (models 401) → model ID sai (chat 401 ModelError) → hết credit (chat 401 CreditsError) → transient (models+chat 200 nhưng standup None → retry).
- Đừng sửa hàng loạt model string cũ trong repo khi chỉ cần chẩn đoán — đổi ID trong call mới là đủ; refactor toàn repo chờ Quang duyệt (tuân plan→review→approve).

## Recipe verify nhanh (cron mode: write_file script → `python <file>` → `rm` ngay; KHÔNG `python -c`, KHÔNG /tmp)
```python
# GET /models với đủ 3 browser headers (UA/Origin/Referer) rồi lọc ID theo substring
# POST /chat/completions từng bare ID, đọc trường error.type trong body
```
