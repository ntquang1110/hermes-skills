---
name: nvidia-nim-fallback
description: "Dựng chain fallback NVIDIA NIM cho Hermes. Test trước."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [nvidia, nim, fallback, providers, hermes, model-testing, triaging]
    related_skills: [hermes-agent, hermes-model-provider-troubleshooting]
---

# NVIDIA NIM làm fallback chain cho Hermes

Dùng khi: cần provider dự phòng cho Hermes mà không phụ thuộc OpenRouter.
NVIDIA NIM (`https://integrate.api.nvidia.com/v1`) là OpenAI-compatible,
key `nvapi-...`, free tier có quota.

## Ba điều PHẢI biết trước khi cắm

### 1. Model trong `/v1/models` KHÔNG đồng nghĩa với model gọi được

Free tier trả về **82 model** trong catalog nhưng phần lớn trả:

```
HTTP 404 {"detail":"Function '<uuid>': Not found for account '<uuid>'"}
```

Đó là entitlement, không phải model hỏng. Phải test từng cái.

### 2. Model có thể trả 200 nhưng HỎNG trong agent loop

Bằng chứng thật: `moonshotai/kimi-k3` (1T params) trả lời đúng mọi prompt
thường, nhưng ở **lượt thứ hai sau tool call** đẻ:

```
reasoning_content = '!!!!!!!!!!!!!!!!!!!!!!!!'
content = ''   (rỗng)
```

4/6 session thất bại. Nên **luôn test bằng prompt bắt buộc gọi tool**, không
chỉ prompt hỏi đáp.

### 3. Model chuyên dụng không làm được agent

- `nvidia/riva-translate-4b-instruct-v1.1` / `-v2` → HTTP 400
  `"auto" tool choice requires --enable-auto-tool-choice`
- `poolside/laguna-xs-2.1` → HTTP 503 `ResourceExhausted (84/32)`

## Quy trình

### Bước 1 — Test khả năng trả lời (lọc 404)

```python
import json, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed

def test(mid):
    body = json.dumps({"model": mid,
                       "messages": [{"role": "user", "content": "hi"}],
                       "max_tokens": 8, "temperature": 0.1}).encode()
    r = urllib.request.Request(
        f"{BASE}/chat/completions", data=body, method="POST",
        headers={"Authorization": f"Bearer {KEY}",
                 "Content-Type": "application/json"})
    try:
        urllib.request.urlopen(r, timeout=90)
        return (mid, True)
    except urllib.error.HTTPError as e:
        return (mid, False, e.code)
```

Timeout 90-240s, chạy song song 5-6 luồng. Ba lần timeout liên tiếp thì
coi như hỏng (cold start model lớn rất lâu).

### Bước 2 — Test tool-call round trip (lọc model hỏng)

Bước **bắt buộc**, không được bỏ:

```python
TOOLS = [{"type": "function", "function": {
    "name": "run_shell",
    "parameters": {"type": "object",
                   "properties": {"command": {"type": "string"}},
                   "required": ["command"]}}}]

# Turn 1: model phải gọi tool
# Turn 2: trả tool result "30" về, model phải trả lời chứa "30"
```

Phân loại kết quả:

| Kết quả | Nghĩa là | Xử lý |
|---------|---------|--------|
| `OK` | dùng được trong agent | ưu tiên đầu chain |
| `DEGENERATE` | reasoning/content toàn ký tự lặp | loại hoặc đẩy cuối |
| `NO_TOOL_CALL` | không gọi tool dù được yêu cầu | đẩy cuối |
| `NO_ANSWER` | có tool call nhưng không dùng kết quả | đẩy cuối |
| `HTTP400` + `tool choice` | chuyên dụng, không phải agent | loại |
| `HTTP503 ResourceExhausted` | quota worker | loại |

Detect degenerate bằng regex, không so sánh chuỗi:

```python
def degenerate(text):
    return bool(re.fullmatch(r"[!?.,;:\-_*#=~]{6,}", (text or "").strip()))
```

### Bước 3 — Test trong harness Hermes THẬT

Test API trần không đủ. Phải chạy qua Hermes vì system prompt ~15K token +
17 tool schema:

```
hermes --provider nvidia -m <model> -z "Dung lenh terminal de tinh 5 nhan 6, roi tra loi ngan gon."
```

Kết quả phải là `30`, không phải `!!!!`.

Câu hỏi đối chiếu (không cần tool) cũng nên chạy để tách lỗi context khỏi
lỗi tool:

```
hermes --provider nvidia -m <model> -z "Tra loi ngan: thu do Viet Nam la gi? 1 cau."
```

### Bước 4 — Ghi config

Key vào `.env`, **không** đưa vào config.yaml:

```
NVIDIA_API_KEY=nvapi-...
```

Config:

```yaml
fallback_providers:
  - provider: nvidia
    model: nvidia/nemotron-3-ultra-550b-a55b
  - provider: nvidia
    model: z-ai/glm-5.3
```

`nvidia` là provider native của Hermes — không cần khai báo
`custom_providers`. Docs: https://hermes-agent.nousresearch.com/docs/user-guide/features/fallback-providers

### Bước 5 — Verify qua log

Đọc `~/.hermes/state.db` để biết model nào thực sự phục vụ:

```sql
SELECT s.id, s.model, s.billing_provider, s.message_count,
       (SELECT substr(group_concat(m.reasoning_content,'|'),1,60)
        FROM messages m WHERE m.session_id=s.id AND m.reasoning_content IS NOT NULL) rsn
FROM sessions s ORDER BY s.started_at DESC LIMIT 12;
```

`rsn` toàn ký tự `!!!!` = model hỏng, không phải lỗi hiển thị.
`messages.content` rỗng kèm `finish_reason=tool_calls` là model đang chờ
tool, đó bình thường.

## Chain đã verify (13 model, free tier, 2026-09)

Tier 1 — test tool round trip trong Hermes thật, đều trả lời đúng:

| Model | Size |
|-------|------|
| `nvidia/nemotron-3-ultra-550b-a55b` | 550B |
| `z-ai/glm-5.3` | 355B |
| `deepseek-ai/deepseek-v4.1-flash` | 200B |
| `z-ai/glm-5.3-flash` | 100B |
| `google/gemma-4-31b-it` | 31B |
| `meta/muse-glimmer-30b` | 30B |
| `nvidia/nemotron-3.5-lightning-30b-a3b` | 30B |

Tier 2 — gọi được nhưng chưa verify đủ agent loop:

`mistralai/mistral-nemotron`, `nvidia/nemotron-3-super-120b-a12b`,
`nvidia/ising-calibration-1.5-31b`,
`nvidia/nemotron-3-nano-omni-30b-a3b-reasoning`, `openai/gpt-oss-20b`,
`meta/llama-3.2-11b-vision-instruct`

Đã loại: `moonshotai/kimi-k3` (degenerate),
`nvidia/riva-translate-4b-*` (HTTP 400), `poolside/laguna-xs-2.1` (HTTP 503).

## Pitfall khi patch config từ xa

Regex `(?ms)^fallback_providers:\n(?:[ \t]+.*\n|\n)*?(?=^\S)` với `re.S`
**ăn quá nhiều dòng** rồi nuốt mất key khác. Xử lý theo dòng, giữ nguyên
CRLF:

```python
lines = text.replace("\r\n", "\n").split("\n")
out, i = [], 0
while i < len(lines):
    if lines[i] == "fallback_providers:":
        i += 1
        while i < len(lines) and (lines[i].startswith((" ", "\t")) or not lines[i].strip()):
            i += 1
        continue
    out.append(lines[i]); i += 1

block = ["fallback_providers:"]
for m in chain:
    block += ["  - provider: nvidia", f"    model: {m}"]
idx = out.index("platforms:")
new = "\r\n".join(out[:idx] + block + out[idx:])
```

Sau khi ghi, luôn `hermes fallback list` để xác nhận số entry.

## Pitfall: `key_env` vs `api_key`

Với key format ByteDance `VxCg...`, `key_env` trong `custom_providers` bị
trả về:

```
HTTP 401 The API key format is incorrect
```

Trong khi `api_key` trực tiếp chạy được. Nếu gặp lỗi này, đổi sang `api_key`.

## Liên quan

- `hermes-model-provider-troubleshooting` — chẩn đoán 401/429/404 theo provider
- `hermes-agent` — cấu hình chung, fallback_providers schema
