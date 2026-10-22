# ByteDance Ark — Provider Fallback cho AI Company

## Lý do

`call_deepseek` trong `hub/store.py` gọi trực tiếp OpenCode Go endpoint
(`https://opencode.ai/zen/go/v1/chat/completions`) qua `requests.post`.
Không đi qua Hermes provider chain → fallback Hermes không áp dụng.

Khi OpenCode Go hết credit (Insufficient account funds) hoặc key không set,
cần fallback sang provider khác.

## Fallback architecture (3 lớp)

```
call_deepseek():
  ├── key rỗng? → ByteDance Ark (BYTEDANCE_ARK_API_KEY)
  ├── OpenCode 200? → parse content → retry 3 → fallback pro
  └── OpenCode !=200? → ByteDance Ark (credit error, timeout, ...)
```

Hermes config.yaml fallback_providers (dùng khi Hermes tự gọi API, không qua call_deepseek):
1. `bytedance` → `deepseek-v4-flash-ga-260731`
2. `command-code` → `deepseek/deepseek-v4-flash`
3. `opencode-go` → `deepseek-v4-flash`

## ByteDance Ark Endpoints

Có 2 endpoint:
- **General:** `https://ark.ap.southeast.bytepluses.com/api/v3/chat/completions`
- **Coding:** `https://ark.ap.southeast.bytepluses.com/api/coding/v3/chat/completions`

Đang dùng coding endpoint. Model list giống nhau giữa 2 endpoint, nhưng
không phải model nào cũng available trên coding endpoint.

## Model compatibility (coding endpoint)

| Model | Coding endpoint | Ghi chú |
|-------|:---:|---------|
| `deepseek-v4-flash-ga-260731` | OK | Đã dùng từ trước |
| `deepseek-v4-flash-260425` | OK | Bản cũ |
| `deepseek-v4-1-flash-260910` | 404 | Chỉ chạy trên general endpoint |

## Implementation

File: `hub/store.py`

```python
BYTEDANCE_URL = "https://ark.ap.southeast.bytepluses.com/api/coding/v3/chat/completions"
BYTEDANCE_KEY_ENV = "BYTEDANCE_ARK_API_KEY"
BYTEDANCE_MODEL = "deepseek-v4-flash-ga-260731"

def _call_bytedance(system, messages, temperature, max_tokens, response_format, agent_name):
    """Fallback gọi ByteDance Ark API (OpenAI-compatible)."""

def _ensure_env_keys():
    """Đọc BYTEDANCE_ARK_API_KEY từ .env nếu chưa có trong os.environ."""
```

ByteDance key được auto-load từ `~/AppData/Local/hermes/.env` khi import module.

## Command Code (fallback thứ 2 trong Hermes config)

- URL: `https://api.commandcode.ai/provider/v1/chat/completions`
- Key env: `HERMES_CUSTOM_COMMAND_CODE_API_KEY`
- Model: `deepseek/deepseek-v4-flash`
- **Pitfall:** `meituan/longcat-2.0:free` đã retired (trả 403 FORBIDDEN)

## Config guard

File: `~/AppData/Local/hermes/scripts/config_guard.py`

Guard chạy mỗi 15 phút, ép cứng config.yaml:
- Model default: `deepseek-v4-flash-ga-260731`
- Base URL: `https://ark.ap.southeast.bytepluses.com/api/coding/v3`
- Fallback providers: bytedance → command-code → opencode-go

Guard cũng tự tắt Hermes desktop app (Hermes.exe) nếu đang chạy.

## Test fallback

```bash
# Test ByteDance trực tiếp
python -c "
from hub.store import _call_bytedance
result = _call_bytedance(system='Say hello', messages=[...], ...)
print(result)
"

# Test full flow (xoá OpenCode key)
python -c "
saved = os.environ.pop('OPENCODE_GO_API_KEY', None)
from hub.store import call_deepseek
result = call_deepseek(model='deepseek-chat', ...)
# Nếu có kết quả → fallback hoạt động
"
```
