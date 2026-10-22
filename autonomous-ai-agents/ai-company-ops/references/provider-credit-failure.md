# OpenCode Go — Credit Exhaustion (Insufficient Balance)

## Triệu chứng
- Mọi `call_deepseek` trả None đồng loạt (5/5 agent chết, không phải từng agent lẻ).
- Raw HTTP request trực tiếp tới `https://opencode.ai/zen/go/v1/chat/completions` trả **401**:
  ```json
  {"type":"error","error":{"type":"CreditsError","message":"Insufficient balance. Manage your billing here: https://opencode.ai/workspace/..."}}
  ```

## Chẩn đoán nhanh
```python
import os, requests
key = os.environ.get('OPENCODE_GO_API_KEY')
r = requests.post(
    'https://opencode.ai/zen/go/v1/chat/completions',
    headers={
        'Authorization': f'Bearer {key}',
        'Content-Type': 'application/json',
        'User-Agent': 'ai-company-agent/1.0',
        'x-opencode-session': 'ac-test-session'
    },
    json={'model': 'deepseek-v4-flash', 'messages': [{'role':'user','content':'hi'}], 'temperature': 0.3, 'max_tokens': 50},
    timeout=15
)
print(r.status_code, r.text[:300])
```
- 200 OK = provider hoạt động, lỗi ở code/context.
- 401 `Insufficient balance` = hết credit.
- 400 `MissingSessionID` = thiếu header `x-opencode-session` (khác lỗi, khác fix).
- 401 `Model is disabled` = model bị tắt trên plan (deepseek-v4-pro đã gặp).

## Phân biệt với các lỗi None khác
| HTTP Status | Lỗi | Fix |
|-------------|-----|-----|
| 200 (content rỗng) | Transient / context quá dài | Retry 3 lần, fallback pro |
| 400 | Missing `x-opencode-session` header | Thêm header vào call |
| 401 Insufficient balance | **Hết credit** | Nạp tiền hoặc đổi provider |
| 401 Model is disabled | Model không có trên plan | Đổi model map |

## Hành động khi credit hết
1. Gửi link billing cho Quang: `https://opencode.ai/workspace/wrk_01KS52FWVYXBS15WZAJRJFVB34/billing`
2. Đề xuất provider fallback: GLM-5.3 / Kimi K3 trên OpenCode Go, hoặc BytePlus ModelArk (deepseek-v4-flash-260425).
3. Sau khi nạp credit → chạy lại standup để agent báo cáo.

## Lịch sử
- **09/09/2026:** Lần đầu OpenCode Go hết credit. Trước đó (08/09) còn OK sau fix MissingSessionID. Credit vừa hết giữa 2 ngày.
- **08/09/2026:** deepseek-v4-pro bị disable trên Go plan (401 Model is disabled).
- BytePlus ModelArk trước đó cũng từng hết quota (rate limit 1.5M TPM, burst 3M TPM → 429).
