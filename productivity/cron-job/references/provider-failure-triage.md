# Chẩn đoán "session hay lỗi model provider" — biên bản 2026-10-16

Câu hỏi của anh: *"Tìm hiểu cho anh tại sao là các section gần đây rất hay bị lỗi model
provider bị có vấn đề thì em check lại cho anh."*

Kết luận: **provider không hỏng. 18/41 cron job bị ghim vào 2 provider đã chết.** Sau khi
đổi model mặc định sang command-code, các pin cũ nằm lại nguyên chỗ.

---

## 1. Trạng thái config lúc chẩn đoán

```yaml
model:
  default: deepseek/deepseek-v4-flash
  provider: command-code
  base_url: https://api.commandcode.ai/provider/v1

providers:
  unsloth:      { base_url: http://192.168.1.3:18888 }        # IP chet
  custom:       { }
  bytedance:    { base_url: https://ark.ap-southeast.bytepluses.com/api/coding/v3 }
  command-code: { key_env: HERMES_CUSTOM_COMMAND_CODE_API_KEY, ... }

fallback_providers:
  - provider: command-code
    model: deepseek/deepseek-v4.1-flash                        # OK, nhung bap benh
  - provider: custom:ark.ap-southeast.bytepluses.com
    model: deepseek-v4-1-flash-260910                          # HTTP 400 het han
```

Nhớ: `fallback_providers` **chỉ đọc bản top-level**. `model.fallback_providers` không có
tác dụng.

---

## 2. Đếm job ghim provider — bước ra thủ phạm

```python
import json, io, os
from collections import Counter
p = os.path.expanduser("~/AppData/Local/hermes/cron/jobs.json")
d = json.loads(io.open(p, encoding="utf-8").read())     # io.open, KHONG read_file
jobs = d if isinstance(d, list) else d.get("jobs", d)
c = Counter()
for j in jobs:
    m = j.get("model")
    prov = j.get("provider") or (m.get("provider") if isinstance(m, dict) else None)
    c[prov or "(dung mac dinh)"] += 1
print(len(jobs), "job")
for k, v in c.most_common():
    print("  %-24s %d" % (k, v))
```

Kết quả thật:

```
41 job
  (dung mac dinh)          23     <- chay duoc
  bytedance                12     <- khong co key
  unsloth                   6     <- IP 192.168.1.3:18888 chet
```

Các job bị ghim `bytedance` (12) — tất cả đều mang
`model: deepseek-v4-flash-260425`, đúng định dạng tên model **của byteplus**, tức viết
từ thời còn dùng byteplus và chưa bao giờ cập nhật:

```
knowledge-researcher-4h-rotation, KFlow Push Tâm lý, Auto-push research to Knowledge Flow,
ai-company-standup, Tâm lý 1/4 sáng 6h, Tâm lý 2/4 10h, Tâm lý 3/4 14h, Tâm lý 4/4 18h,
Auto Threads - Ministral, Tâm lý auto-post Threads 06:10, Macro Daily MIT, HLL Daily
```

Các job bị ghim `unsloth` (6): `Daily Research for Threads Schedule`, `Tâm lý học 6
bài/ngày`, `Tâm lý 5/8 7h`, `6/8 11h`, `7/8 15h`, `8/8 19h`.

**Bài học:** sau MỌI lần đổi `model.default`/`model.provider`, chạy lại script này. Pin
per-job là thứ duy nhất không tự theo.

---

## 3. Bốn loại lỗi provider — phân biệt theo câu log

```bash
grep -oE "Job '[a-f0-9]{12}': primary auth failed \(No usable credentials found for provider '[a-z-]+'" \
  ~/AppData/Local/hermes/logs/agent.log | sort | uniq -c | sort -rn
```

| Câu log | Nghĩa | Sửa |
|---|---|---|
| `No usable credentials found for provider 'bytedance'` | **THIẾU KEY**. `BYTEDANCE_ARK_API_KEY` không có trong `.env` | thêm key hoặc bỏ pin |
| `APIConnectionError ... summary=Connection error` | key OK, kết nối bập bênh | giữ / đổi sang bản `-fast` |
| `BadRequestError ... InvalidSubscription` + `CodingPlan subscription has expired` | gói hết hạn | bỏ entry khỏi `fallback_providers` |
| `BadRequestError ... Model is not supported` | pin sai cặp provider↔model | pin lại đúng cặp |

Chuỗi chết hoàn chỉnh ghi trong `errors.log` (job `knowledge-researcher-4h-rotation`):

```
22:41:16 APIConnectionError  provider=command-code   model=deepseek/deepseek-v4.1-flash
22:41:16 BadRequestError     provider=custom:ark.ap-southeast.bytepluses.com
         HTTP 400: Your account (3002415332) does not have a valid CodingPlan subscription
22:41:16 ERROR Job 'knowledge-researcher-4h-rotation' failed: RuntimeError HTTP 400 ...
```

Đếm trong ngày: `primary auth failed` = **64 lần**, tất cả đều `provider 'bytedance'`.

---

## 4. Probe provider — HAI cái bẫy làm kết quả nói dối

### Bẫy 1: thiếu User-Agent browser → Cloudflare trả 403/1010 GIẢ

Lần đầu probe bằng `urllib` trần:

```
command-code   deepseek/deepseek-v4-flash    -> HTTP 403  error code: 1010
command-code   deepseek/deepseek-v4.1-flash  -> HTTP 403  error code: 1010
```

`error code: 1010` là **Cloudflare chặn chữ ký browser**, không phải lỗi provider. Thêm
`User-Agent` browser → cả hai model trả **200 OK** với `reasoning_content` đầy đủ. Nếu
tin kết quả 403 đó thì đã kết luận sai "command-code hỏng" và đi sửa một provider khoẻ.

### Bẫy 2: GET vào `/chat/completions` → 404 GIẢ

```
{"success":false,"status":404,"message":"404 Not found. Check the docs for available routes.",
 "cause":"GET https://api.commandcode.ai/provider/v1/chat/completions is not a registered API route"}
```

Chữ `GET` trong `cause` là mấu chốt — endpoint **phải POST**. Không phải route thiếu.

### Code probe đúng

```python
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")

def post(url, payload, key, timeout=60):
    req = urllib.request.Request(url, data=json.dumps(payload).encode(), method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("Authorization", "Bearer %s" % key)
    req.add_header("User-Agent", UA)          # <- THIEU LA 403/1010 GIA
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read().decode(errors="replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode(errors="replace")
```

### `GET /models` — nguồn sự thật về model nào tồn tại

```
GET https://api.commandcode.ai/provider/v1/models   -> 200, 92 model
```

Mỗi entry có `context_length` + `supported_endpoints`. Vài ví dụ đáng nhớ:

| id | ctx | supported_endpoints |
|---|---|---|
| `claude-sonnet-4-6` | 1.000.000 | `['/messages']` |
| `deepseek/deepseek-v4-flash` | 1.000.000 | `['/chat/completions', '/responses']` |
| `deepseek/deepseek-v4.1-flash` | 1.000.000 | `['/chat/completions', '/responses']` |
| `deepseek/deepseek-v4-pro` | 1.000.000 | `['/chat/completions', '/responses']` |
| `xai/grok-4.7` | 500.000 | `['/chat/completions', '/responses']` |

Hai điều rút ra:

- Model họ Claude **chỉ** phục vụ ở `/messages` (Anthropic Messages API), không phải
  `/chat/completions`. Gọi sai endpoint → `Model "X" is not supported on this endpoint`.
- Model Claude cần gói Pro: `403 MODEL_NOT_IN_PLAN: Claude Sonnet 4.6 available in Pro and
  above plans`. Không phải lỗi cấu hình của mình.

---

## 5. Đo tỉ lệ lỗi thật

```bash
grep -c "agent.conversation_loop: API call #" agent.log    # 841
grep -c "API call failed"                     agent.log    #  51
grep -c "Streaming failed before delivery"    agent.log    #  17
```

Phân loại 51 lỗi:

```
45  error_type=APIConnectionError
 6  error_type=BadRequestError
```

→ **841 thành công / 51 thất bại = 5,7%**, cộng 17 `Streaming failed before delivery`.
Con số này chứng minh provider không hỏng; job ghim sai mới là gốc.

---

## 6. Tách nhiễu khỏi tín hiệu TRƯỚC khi kết luận

```bash
grep -oE "(ERROR|WARNING) [a-zA-Z_.]+: [A-Za-z][^:]{0,60}" errors.log | sort | uniq -c | sort -rn | head
```

`errors.log` ngày 16/10 (1.779 dòng):

```
1404  ERROR   gateway.run: kanban dispatcher        <- moi 60 giay
  53  WARNING tools.mcp_tool: MCP server 'notion' failed initial OAuth ... 401
  53  WARNING tools.mcp_tool: Failed to connect to MCP server 'notion'
  48  WARNING cron.scheduler: Job '7b7bf3c056aa'
  17  ERROR   agent.chat_completion_helpers: Streaming failed before delivery
   6  WARNING cron.scheduler: Job 'd43697af1322'
```

**Chỉ 126/1.779 dòng là provider.** 1.404 dòng là bug kanban bắn mỗi phút.

`gateway-stdio.log` — 128 MB:

```
637784 MCP server 'notion'
   433 MCP server 'graft_volden'
   115 MCP server 'lark'
```

Nội dung một dòng:
`WARNING tools.mcp_tool: MCP server 'notion' initial connection failed (attempt 1/3),
retrying in 1s: unhandled errors in a TaskGroup (1 sub-exception)`

Một MCP server chết trong vòng retry vô hạn đủ để phình log lên hàng trăm MB. Sửa hai
thứ này trước khi đổ cho provider — chúng che mất lỗi thật và ăn đĩa.

Phân bố lỗi theo giờ rất phẳng (~70 dòng/giờ, cả ngày) → lỗi hệ thống đều đặn, không
phải sự cố bùng phát. Cách đọc này loại bỏ giả thuyết "provider chết theo đợt".

---

## 7. Thứ tự xử lý đề xuất

1. Bỏ pin `provider`/`model` sai ở 18 job → về mặc định command-code.
   Mục tiêu: hết 64 lần auth-fail/ngày, job chạy ngay thay vì đốt provider chết.
2. Xoá entry `custom:ark.ap-southeast.bytepluses.com` khỏi `fallback_providers` (gói hết
   hạn) → fallback rơi thẳng vào tầng sống.
3. Sửa hoặc tắt MCP `notion` (401 + loop 637k dòng) → cắt 128 MB log.
4. Sửa `kanban dispatcher` (1.404 lỗi/ngày) → `errors.log` sạch.

### Xác minh sau khi pin lại

```bash
hermes cron runs <job_id>          # entry top phai completed (source=direct)
grep -c "primary auth failed" ~/AppData/Local/hermes/logs/agent.log
```

Số `primary auth failed` phải NGỪNG tăng. `last_status: ok` một mình không đủ — nó vẫn
có thể là fallback im lặng sang provider khác (xem pitfall 13 trong SKILL.md).
