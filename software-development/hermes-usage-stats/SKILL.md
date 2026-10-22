---
name: hermes-usage-stats
description: "Use when user asks request/tokens usage theo tháng."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [hermes, state.db, sqlite, usage, tokens, stats, sessions]
    related_skills: [hermes-dashboard, cron-job, hermes-model-provider-troubleshooting]
---

# Hermes Usage Stats (state.db queries)

Thống kê số lượng request, tokens, cost, session theo tháng từ chính state.db của Hermes — khi user hỏi "đã dùng bao nhiêu request/tokens?", KHÔNG đoán, query DB trực tiếp.

## Khi nào dùng

- User hỏi tổng request / tokens / chi phí theo tháng, tuần, ngày
- Cần phân tích xu hướng usage (tháng nào cao, chủ yếu chat hay cron)
- Cần tìm session cũ nhanh bằng SQL thay vì session_search

## Bước 1 — Xác định DB ĐÚNG (pitfall số 1)

Trên máy Quang (Windows), có HAI state.db:

| Path | Trạng thái |
|---|---|
| `C:\Users\NTQUANG_DELL\AppData\Local\hermes\state.db` | **ACTIVE** ~1.7GB, cập nhật liên tục |
| `D:\Hermes\hermes-home\state.db` | Bản cũ ~771MB (pha 2 migration chưa chạy, chỉ tới ~10/08) |

Query nhầm bản D → số liệu hụt cả tháng 9. Verify trước:
```sql
SELECT MIN(started_at), MAX(started_at) FROM sessions;
```
MAX phải = hôm nay. Trong bash MSYS nhớ dùng `python -c "..."` với `r'C:\Users\...'` — không dùng path MSYS `/c/Users/...`.

## Bước 2 — Bảng và cột

- **`session_model_usage`** — mỗi row 1 (session × model): `session_id, model, api_call_count` (= số request), `input_tokens, output_tokens, cache_read_tokens, cache_write_tokens, reasoning_tokens, estimated_cost_usd, actual_cost_usd, first_seen, last_seen`
- **`sessions`** — `id, started_at, ended_at, message_count, tool_call_count, api_call_count, input_tokens, output_tokens, title, source, chat_id`

## Bước 2b — Tách lưu lượng theo NHÀ CUNG CẤP (billing_provider)

Khi user hỏi "provider nào đang ngốn lưu lượng" (ByteDance / Command Code / OpenCode), dùng cột `billing_provider` trong `session_model_usage`:

```python
rows = cur.execute("""SELECT billing_provider, SUM(api_call_count), SUM(input_tokens), SUM(output_tokens)
                      FROM session_model_usage WHERE first_seen >= ? GROUP BY 1""", (month_start_ts,)).fetchall()
```

Tên provider thực tế trên máy Quang: `bytedance`, `command-code`, `opencode-go`, `opencode-zen`, `custom` / `custom:unsloth`, `auto` (router tự chọn), `gemini`, `openrouter`, `custom:omniroute`, và chuỗi rỗng.

**⚠️ KHÔNG có API usage nào của provider** (verified 25/09/2026):
- ByteDance Ark: `GET /api/v3/usage`, `/api/v3/billing/usage`, `/api/coding/v3/usage` → **200 nhưng body RỖNG** (route không tồn tại, trả 200 rỗng — đừng tưởng có data). `/api/v3/models` thì thật.
- Command Code: mọi path (`/me`, `/usage`, `/v1/usage`, `/credits`, `/billing`, `/subscription`, `/quota`) → **404** `is not a registered API route`.
- OpenCode: `/zen/v1/models` OK; `/api/user`, `/api/me`, `/api/billing`, `/api/usage` → **404 HTML**.

→ **state.db là nguồn duy nhất đáng tin.** Đừng hứa với user "lấy usage từ API nhà cung cấp".

**Probe sức khoẻ endpoint kèm báo cáo** (1 token, rẻ, không bao giờ raise): POST `max_tokens=1` tới từng provider, parse `error.message` khi HTTPError — nhờ vậy đọc được thông báo thật như `AccountQuotaExceeded ... reset at <giờ>` (ByteDance 429 quota 5 giờ) hay `Insufficient account funds` (OpenCode 402). Đây là cách duy nhất biết provider chết trước khi user phát hiện giữa task.

**Script tham chiếu:** `scripts/usage_monthly.py` trong hermes home — báo cáo tháng + hôm nay + xu hướng 3 tháng + model chính + trạng thái endpoint. Chạy qua cron `no_agent` 2 giờ/lần (`0 */2 * * *`, job `usage-3-provider-2h`), stdout gửi thẳng chat, **không tốn token LLM**.

## Bước 3 — Pitfall timestamp (số 2, hay dính)

**`first_seen`/`last_seen`/`started_at` là epoch seconds dạng float** (1782383604.66), KHÔNG phải chuỗi ISO. Substr thẳng → ra mã tháng vô nghĩa (1782383...). Phải convert:
```python
import sqlite3, datetime
from collections import defaultdict
conn = sqlite3.connect(r'C:\Users\NTQUANG_DELL\AppData\Local\hermes\state.db')
cur = conn.cursor()
rows = cur.execute('''SELECT first_seen, api_call_count, input_tokens, output_tokens, estimated_cost_usd
                      FROM session_model_usage WHERE first_seen IS NOT NULL''').fetchall()
bym = defaultdict(lambda: [0,0,0,0,0.0])
for ts, req, it, ot, cost in rows:
    m = datetime.datetime.fromtimestamp(int(ts)).strftime('%Y-%m')
    d = bym[m]; d[0]+=1; d[1]+=req or 0; d[2]+=it or 0; d[3]+=ot or 0; d[4]+=cost or 0
# in bảng: Tháng | Rows | Request | Input tok | Output tok | Cost USD
```

Group theo tháng: `strftime('%Y-%m')`; theo ngày: `'%Y-%m-%d'`.

## Bước 4 — Session counts (bảng sessions)

```python
rows = cur.execute('''SELECT started_at, message_count, tool_call_count, api_call_count
                      FROM sessions WHERE started_at IS NOT NULL''').fetchall()
# nhóm theo tháng tương tự — cột session = COUNT, msg/tool/api = SUM
```

`api_call_count` ở `sessions` ≈ `session_model_usage` nhưng có thể lệch nhẹ (usage bảng model kể cả retry). Trình bày cả 2 nếu user muốn chéo check.

## Diễn giải khi báo cáo

- **Input tokens chiếm ~85–90% tổng** — context dài là chi phí chính, output rẻ hơn nhiều
- **Cron chiếm phần lớn session** khi chạy nhiều lần/ngày (knowledge-researcher-4h, KFlow push): tháng 9 ví dụ có ~493 sessions nhưng đa phần là cron. Tách chat vs cron bằng cột `source`/`chat_id` trên `sessions`
- Mức tham chiếu (máy Quang 09/2026, provider opencode-zen/go free): 06/2026 ~878 req · 07/2026 ~14k req · 08/2026 ~21k req (134M tok) · 09/2026 (7 ngày đầu) ~5.6k req. Chi phí tracked ~$0.02 (chủ yếu free tier)

## Pitfalls đã gặp

1. **DB active ở C:, không phải D:** dù AGENTS.md nói data đã junction sang D — state.db/logs CHƯA (pha 2 chờ gateway tắt). Luôn check MAX(started_at).
2. **Epoch float, không phải chuỗi:** convert trước khi group.
3. **`api_call_count` có thể NULL** — dùng `req or 0` trong SUM.
4. **Bảng `messages` có FTS — đừng đụng:** `messages_fts*` là index phục vụ session_search; query usage chỉ cần 2 bảng trên.
5. **Path trong bash MSYS:** dùng `r'C:\Users\...'` trong Python, đừng để git-bash convert `/c/...` thành `D:\c\...` — python Windows không hiểu MSYS path.