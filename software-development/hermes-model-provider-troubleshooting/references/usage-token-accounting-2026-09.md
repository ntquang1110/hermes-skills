# Hermes Usage / Token Accounting qua state.db (2026-09)

Chẩn đoán "mỗi tháng dùng bao nhiêu request / sao input token cao" bằng truy vấn trực tiếp SQLite. Đo thật 2026-09-07 trên máy Windows của Quang.

## ⚠️ CÓ 2 BẢN state.db — phải query bản LIVE

| Path | Kích thước | Live? |
|---|---|---|
| `C:\Users\NTQUANG_DELL\AppData\Local\hermes\state.db` | ~1.7 GB | ✅ LIVE (cập nhật liên tục, updated hôm nay) |
| `D:\Hermes\hermes-home\state.db` | ~771 MB | ❌ STALE (chỉ tới 10/08/2026 — phase-2 migration chưa chạy) |

AGENTS.md nói "state.db chờ pha 2" — nhưng data hiện tại vẫn ghi vào bản C:. Query nhầm bản D: → thiếu toàn bộ tháng 8 sau ngày 10 và tháng 9. **Luôn dùng bản C: AppData\Local\hermes.**

Kiểm tra nhanh bản nào live:
```sql
SELECT datetime(MAX(started_at),'unixepoch') FROM sessions;
```
Bản trả ngày gần hôm nay = live.

## Schema liên quan (bảng quan trọng)

- `sessions` — mỗi row 1 session: `started_at` (epoch), `message_count`, `tool_call_count`, `api_call_count`, `title`, `source`, `session_key`, `last_activity_at`.
- `session_model_usage` — per (session, model): `api_call_count`, `input_tokens`, `output_tokens`, `cache_read_tokens`, `cache_write_tokens`, `reasoning_tokens`, `estimated_cost_usd`, `first_seen`, `last_seen` (epoch).
- `messages` — per message: `role`, `timestamp` (epoch), `token_count` (**thường NULL** — đừng dựa vào), `content`.
- `system_prompts` — các system prompt đã dùng (kích thước ~41.8K chars = ~12K tokens nền mỗi request).

⚠️ `first_seen`, `started_at`, `timestamp` đều là **epoch seconds** — dùng `strftime('%Y-%m', col, 'unixepoch')`, KHÔNG `substr(col,1,7)`.

## Query tháng (request/session/token)

```sql
-- SESSION theo tháng
SELECT strftime('%Y-%m', started_at,'unixepoch') as thang,
       COUNT(*) sess, SUM(api_call_count) req,
       SUM(tool_call_count) tool, SUM(message_count) msg
FROM sessions WHERE started_at IS NOT NULL
GROUP BY thang ORDER BY thang;

-- TOKEN theo tháng (input/output/cost) — từ session_model_usage
SELECT strftime('%Y-%m', first_seen,'unixepoch') as thang,
       SUM(api_call_count) req,
       SUM(input_tokens) in_tok,
       SUM(output_tokens) out_tok,
       SUM(estimated_cost_usd) cost
FROM session_model_usage WHERE first_seen IS NOT NULL
GROUP BY thang ORDER BY thang;
```

## Tìm session "tốn token bất thường"

```sql
-- Top session theo tổng input (tìm đứa ăn nhiều nhất tuyệt đối)
SELECT s.started_at, s.title, COALESCE(u.api_call_count, s.api_call_count) req,
       u.input_tokens, u.output_tokens
FROM sessions s LEFT JOIN session_model_usage u ON u.session_id = s.id
WHERE s.started_at IS NOT NULL AND u.input_tokens > 0
ORDER BY u.input_tokens DESC LIMIT 25;

-- Top session theo TRUNG BÌNH input/request (tìm "200k/request" — session dài không nén)
SELECT s.started_at, s.title, u.api_call_count req, u.input_tokens,
       u.input_tokens * 1.0 / NULLIF(u.api_call_count,0) as avg_in
FROM session_model_usage u LEFT JOIN sessions s ON s.id = u.session_id
WHERE u.api_call_count > 0 AND u.input_tokens IS NOT NULL
ORDER BY avg_in DESC LIMIT 30;
```

## Đọc kết quả — cái gì "bình thường"

- **avg_in/req 5K-15K** — bình thường (system prompt ~12K nền + history ngắn).
- **avg_in/req 70K-250K** — session HẾT SỨC dài hoặc compression tắt:
  - Một số session single-request 249K/233K (research nặng).
  - Session chat dài 300+ messages gửi toàn bộ history mỗi turn.
- **Điều chỉnh chẩn đoán:** trong cùng session, `history=N` trong agent.log tăng dần theo turn = context phình. `compression.enabled: false` = không bao giờ nén.

## Liên kết

- Cách fix (bật compression + quirk desktop app ghi đè config) → SKILL.md mục "PITFALL — compression.enabled: false → input token 200k+/request" và "PITFALL — Desktop app ĐANG CHẠY ghi đè config".