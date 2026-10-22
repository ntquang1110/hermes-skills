# Context window & compression — chi tiết

> Tách từ `SKILL.md` ngày 19/10/2026. Nội dung giữ nguyên văn.


---

## Tắt compression hẳn — `compression.enabled false`

```bash
hermes config set compression.enabled false
```

Cờ này gate TOÀN BỘ luồng nén (verify source 2026-08):
- `agent/conversation_loop.py` dòng ~1971, 2068 (preflight compression), 6426 (`should_compress`), 6465 (warning over-threshold)
- `agent/turn_context.py` dòng ~663 (idle compact), 740 (preflight estimate)
- `agent/conversation_compression.py` dòng ~1589 (feasibility warning lúc start)

**Cái giá phải trả:** tắt hẳn → nếu session vượt window thật của provider (~1M)
thì request **lỗi overflow từ provider** (Hermes có nhánh báo lỗi rõ, không crash
im lặng) thay vì tự nén gọn. Context dài + compression tắt = đánh đổi: giữ nguyên
nội dung nhưng rủi ro overflow ở session cực dài. Các tham số phụ
(`proactive_prune_tokens`, `micro_compact`, `idle_compact_after_seconds`) đều mặc
định tắt sẵn — không cần đụng.


---

## PITFALL — `compression.enabled: false` → input token 200k+/request trên session dài (chẩn đoán "sao tốn token vậy?")

Triệu chứng user hỏi "sao gần đây input token rất cao toàn 200k token/request".
**Nguyên nhân chính thường là compression TẮT** (`compression.enabled: false`):
session chat dài (300–400 messages) mỗi turn gửi TOÀN BỘ history lên model →
input phình không kiểm soát. Session càng dài, trung bình input/request càng tăng
(đo 2026-09-07: 5.8K → 6.2K → 12.9K → 16.7K input/req trong 5 ngày cùng session).

**Chẩn đoán nhanh (2 bước):**
1. `grep -A3 "^compression:" ~/AppData/Local/hermes/config.yaml` → `enabled: false` = nghi phạm chính.
2. `grep turn_context ~/AppData/Local/hermes/logs/agent.log | tail` → thấy `history=290` → 339 (tăng dần cùng session) chứng minh history phình.

**Chi tiết phân bố token — query state.db:**
```sql
-- sessions theo tháng (request/tool call/message)
SELECT strftime('%Y-%m', started_at,'unixepoch') thang, COUNT(*) sess,
       SUM(api_call_count) req, SUM(tool_call_count) tool, SUM(message_count) msg
FROM sessions GROUP BY thang ORDER BY thang;
-- token theo tháng (input/output + cost)
SELECT strftime('%Y-%m', first_seen,'unixepoch') thang, SUM(api_call_count) req,
       SUM(input_tokens) in_tok, SUM(output_tokens) out_tok, SUM(estimated_cost_usd) cost
FROM session_model_usage GROUP BY thang ORDER BY thang;
-- top session theo input/request trung bình (tìm session "200k/req")
SELECT s.started_at, s.title, u.api_call_count req, u.input_tokens,
       u.input_tokens*1.0/NULLIF(u.api_call_count,0) avg_in
FROM session_model_usage u LEFT JOIN sessions s ON s.id=u.session_id
WHERE u.api_call_count>0 ORDER BY avg_in DESC LIMIT 20;
```
`started_at`/`first_seen` là **epoch seconds** — phải `strftime('%Y-%m', col,'unixepoch')`, không được `substr` trực tiếp. Bảng `session_model_usage` chứa `api_call_count, input_tokens, output_tokens, estimated_cost_usd` per (session, model). Chi tiết schema + query đầy đủ → `references/usage-token-accounting-2026-09.md`.

**Fix:** bật compression `hermes config set compression.enabled true` → session dài
tự nén ở 50% (`threshold`), giữ `protect_last_n: 20` turn cuối. Hiệu quả giảm input
5–10× cho session dài. Lưu ý: config chỉ áp dụng cho **session mới** — session đang
chạy giữ nguyên (đổi giữa chừng phá prompt cache).


---

## PITFALL — override `context_length` đủ để Hermes QUA rào 64K, nhưng server vẫn hard-reject lúc call

Quy tắc 2 tầng độc lập — phải giải quyết CẢ HAI:
- **Tầng Hermes (khởi tạo):** model must ≥ 64K để Hermes khởi tạo agent. Đặt
  `context_length` trong entry `custom_providers`.models (vd 131072 cho Ministral
  native 262K) → vượt được rào init này.
- **Tầng server (lúc call):** nếu **Unsloth/serving thật chỉ serve context nhỏ**
  (vd Ministral đang `context_length:4096` qua `/v1/models`), server NGHIÊM TÚC
  từ chối sau khi Hermes gửi cả system prompt (~22K token):
  ```
  API call failed: Message too long: 22040 tokens exceeds the 4096-token context window.
  ```
  → config override KHÔNG giúp — lỗi này nằm ở phía server, không còn phía Hermes.

**KL:** `context_length` override là cần nhưng KHÔNG đủ. Sau khi qua rào Hermes,
phải đo `/v1/models` xem server đang serve context bao nhiêu; nếu thấp (< kích thước
prompt Hermes ~20K+), bắt user **nâng context serve trên Unsloth Studio** cho đúng
model đang load (Ministral → ≥32K), rồi mới test qua Hermes. Đừng tưởng "set
context 131K trong config là xong" — server vẫn từ chối riêng của nó.


---

## PITFALL — Hermes hard-chặn model có context window < 64K

Triệu chứng khởi tạo thất bại:
```
Failed to initialize agent: Model <X> has a context window of 32,768 tokens,
which is below the minimum 64,000 required by Hermes Agent.
```
Lý do: Hermes (agent_init / model_metadata) không cho chạy agent trên model có
window < 64K. **Rào này KHÔNG vượt được bằng mẹo config** — ghi đè
`context_length` thật lên ≥64K cho model THẬT có window đó; nếu model/serving
thật chỉ có 4K (như Qwen3-VL-8B qua Unsloth báo `context_length:4096`) thì không
dùng được làm backend cho Hermes.

Quan trọng: **đừng tin `native_context_length` server báo** — Unsloth báo
`native_context_length:262144` nhưng `context_length:4096` (giá trị đang serve).
Đo qua `/v1/models` trước khi chốt. Model local bị khóa 4-32K context qua
Unsloth/tunnel thường KHÔNG đạt 64K Hermes cần → nói thẳng với user: cái đó
không dùng được cho Hermes Agent, cần Ollama chạy local (Qwen3 8B báo 128K)
hoặc query qua endpoint không giới hạn ngặt.

Còn nữa — khi model có indexup tăng context: `switch by request` phải ON trong
Unsloth Studio để serve nhiều model; chỉ 1 model được nạp 1 lúc, các model khác
trả `model_not_found` ("downloaded but not loaded").


---

## PITFALL — Cron job dùng model local LOGO + skill stack nặng → Context overflow

Khi gắn model local/tunneled (context hạn chế) vào một cron job KHÔNG phải task nhẹ,
job fail ngay lúc chạy:
```
RuntimeError: Context overflow and auto-compaction is disabled (compression.enabled: false).
Run /compress... or switch to a larger-context model.
```
Test thật 2026-08: job "Tâm lý học 6 bài/ngày" vốn gắn 4 skill **web-research +
visual-academic-html + html-publishing + dashboard-design-system** → gắn LFM2.5-8B
(vốn giải quyết 128K, vượt rào 64K) vẫn overflow vì prompt từ mớ skill + history
kéo dài quá window serve thật. **Model local không phải DeepSeek — nó không gánh
nổi job đầy skill research + build HTML.**

**Fix (đúng hướng user chọn "làm từng bài 1"):**
1. **Bỏ skill nặng khỏi job local** — job dùng local chỉ nên có skill đơn giản,
   hoặc 0 skill. Research sâu (web-research/citation/HTML) giữ ở API strong.
2. **Tách thành N job nhỏ, mỗi job 1 đơn vị output** (mỗi job 1 bài tâm lý, 1 tóm
   tắt), lệch giờ qua ngày → prompt ngắn, không tràn. Đừng gom 6 bài vào 1 job.
3. Chạy thử bằng job one-shot timestamp trước khi nhân rộng.

PITFALL phụ — **cron one-shot schedule:** chuỗi `"once"` KHÔNG hợp lệ; dùng ISO
timestamp `2026-08-23T01:45:00` cho 1-lần. Khi tạo job qua tool cronjob model để
null — gắn model sau bằng CLI: `hermes cron edit <id> --model "<full-model-id>"
--provider <custom-provider-name>`, rồi `--provider` đặt theo tên entry trong
`custom_providers`.

PITFALL phụ — **humalike (hay plugin OAuth) chặn CLI `hermes chat`, nhưng KHÔNG
chặn cron.** Plugin xã hội (turn-taking) tự hiện link approve OAuth mỗi lần
`hermes chat` CLI chạy → nghẽn test tay. Cron chạy qua gateway thì humalike báo
`passthrough` và để trôi — cron vận hành bình thường. Muốn test model nhanh bằng
CLI không vướng plugin: `hermes chat ... --safe-mode` (tắt mọi plugin), KHÔNG cần
tắt plugin trong config.
