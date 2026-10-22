# Khả năng AGENT của model fallback — đo thật (2026-09, NVIDIA NIM free tier)

Case: chain fallback 17 entry trên host Hermes mới (lqremote, Windows). User đặt chain theo
size giảm dần ("ưu tiên model lớn lên đầu"). Output nhiều lần là `!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!`
thay vì câu trả lời. Truy ra KHÔNG phải lỗi hiển thị và KHÔNG phải lỗi harness.

## 1. Triệu chứng và cách chốt nguyên nhân

Chỉ xuất hiện khi primary đã fail (đang chạy fallback), và chỉ với prompt **buộc gọi tool**.

Hai lần chạy cùng prompt qua harness, cách nhau vài phút:

```
hermes -z "Tra loi ngan: 5x6 bang may?"   ->  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
hermes -z "Tra loi ngan: 5x6 bang may?"   ->  30
hermes -z "Say hello in one word."        ->  Hello
```

Bất định → ban đầu dễ tưởng race condition lúc cold start. **Sai.** Đọc `state.db` mới ra sự thật:

```python
import sqlite3
con = sqlite3.connect(r"C:\Users\Admin\AppData\Local\hermes\state.db")
con.row_factory = sqlite3.Row
for r in con.execute("""
  SELECT session_id, role, substr(content,1,80) c, finish_reason, reasoning_content, tool_calls
  FROM messages WHERE session_id IN (
      SELECT id FROM sessions ORDER BY started_at DESC LIMIT 8)
  ORDER BY session_id DESC, rowid ASC"""):
    print(dict(r))
```

Kết quả thật (rút gọn) — chuỗi 4 message của một session hỏng:

```
user      fr=None        c='Tra loi ngan: 5x6 bang may?'
assistant fr=tool_calls  c=''      rsn='Simple arithmetic. Use tool.'   tc='[{"id":"terminal:0",...}]'
tool      fr=None        c='{"output": "30", "exit_code": 0, "error": null}'
assistant fr=stop        c=''      rsn='!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
```

→ Model **gọi tool đúng**, nhận `{"output":"30"}`, rồi lượt sau đẻ `!` vào `reasoning_content`
và để `content` rỗng. Hermes in dấu `!` ra ngoài. Không có gì hỏng ở phía Hermes.

`SELECT id, model FROM sessions ORDER BY started_at DESC LIMIT 12` → model là
`moonshotai/kimi-k3` (entry #1 của chain). Đối chiếu toàn bộ session gần đó:

| session | model | message cuối có `!`? |
|---|---|---|
| …_174838 | moonshotai/kimi-k3 | ❌ `!!!!!!!!` (32) |
| …_174734 | nvidia/nemotron-3-ultra-550b-a55b | ✅ sạch |
| …_174655 | moonshotai/kimi-k3 | ✅ sạch (prompt không cần tool) |
| …_174523 | moonshotai/kimi-k3 | ✅ sạch |
| …_174330 | moonshotai/kimi-k3 | ❌ `Simple arithmetic. Use tool.` \| `!!!!` |
| …_174012 | moonshotai/kimi-k3 | ❌ `Must use tool for arithmetic.` \| `!!!!` |
| …_173110 | moonshotai/kimi-k3 | ❌ `!!!!!!!!` (32) |
| …_171947 | nvidia/nemotron-3-ultra-550b-a55b | ✅ sạch |

4/6 session của kimi-k3 hỏng; 2 model khác cùng lúc sạch → lỗi ở MODEL, không phải provider/host.

## 2. Vì sao probe thường KHÔNG bắt được

| Probe | kimi-k3 | Ghi chú |
|---|---|---|
| Direct API, 1 lượt, `"Tra loi ngan: thu do Viet Nam?"` | ✅ đúng | không có tool schema, prompt ngắn |
| Harness Hermes, prompt kiến thức | ✅ đúng | vẫn không buộc gọi tool |
| Direct API, 2 lượt có tool schema (tool round trip) | ✅ PASS | prompt nhỏ — bug chưa lộ |
| **Harness Hermes, prompt BUỘC gọi tool** | ❌ `!!!!` | đúng điều kiện thật: system prompt ~15K token + 17 tool schema + tool-result lượt sau |

→ Bug chỉ lộ khi **tool schema + system prompt lớn + lượt tool-result** cùng có. Verification
duy nhất đáng tin là chạy trong chính harness Hermes với prompt buộc gọi tool:

```powershell
hermes --provider nvidia -m moonshotai/kimi-k3 -z "Dung lenh terminal de tinh 5 nhan 6, roi tra loi ngan gon."
# "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"  = HỎNG
# "5 × 6 = **30**"                    = TỐT
```

## 3. Ma trận khả năng agent (đo 2026-09)

Tool round trip qua harness Hermes, prompt `"Dung lenh terminal de tinh 5 nhan 6, roi tra loi ngan gon."`:

| Kết quả | Model | Ghi chú |
|---|---|---|
| ✅ PASS | `nvidia/nemotron-3-ultra-550b-a55b` | 550B, ổn định nhất |
| ✅ PASS | `z-ai/glm-5.3` | 355B, trả `5 × 6 = 30` |
| ✅ PASS | `deepseek-ai/deepseek-v4.1-flash` | 200B, cùng họ với primary |
| ✅ PASS | `z-ai/glm-5.3-flash` | 100B |
| ✅ PASS | `google/gemma-4-31b-it` | 31B |
| ✅ PASS | `meta/muse-glimmer-30b` | 30B |
| ✅ PASS | `nvidia/nemotron-3.5-lightning-30b-a3b` | 30B |
| ❌ DEGENERATE | `moonshotai/kimi-k3` | 1T — `reasoning_content='!!!!'`, content rỗng ở lượt tool-result |
| ✗ NO_TOOL_CALL | `mistralai/mistral-nemotron` | không chịu gọi tool |
| ✗ NO_TOOL_CALL | `nvidia/ising-calibration-1.5-31b` | model calibration, không gọi tool |
| ✗ HTTP500 | `nvidia/nemotron-3-super-120b-a12b` | có thể transient — retry riêng trước khi loại |
| ✗ HTTP503 | `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning` | pool free tier chia sẻ, retryable |
| ✗ HTTP503 | `poolside/laguna-xs-2.1` | pool free tier |
| ✗ Timeout | `openai/gpt-oss-20b` | trong probe song song; retry tuần tự thì CHẠY được |
| ✗ NO_ANSWER | `meta/llama-3.2-11b-vision-instruct` | gọi tool nhưng không trả `30` |
| ✗ HTTP400 | `nvidia/riva-translate-4b-instruct-v1.1` | `"auto" tool choice requires --enable-auto-tool-choice` = NMT, không hỗ trợ tool |
| ✗ HTTP400 | `nvidia/riva-translate-4b-instruct-v2` | như trên |

Đọc bảng này đúng cách: **503/timeout là transient** (pool free tier / cold start) → retry riêng
tuần tự, đừng loại vĩnh viễn. **DEGENERATE / NO_TOOL_CALL / HTTP400-tool-choice là thuộc tính của
model** → đẩy xuống cuối hoặc bỏ.

## 4. Thứ tự chain cuối cùng (17 entry) — theo khả năng agent, không theo size

```
1-7   PASS models, size giảm dần:
      nemotron-3-ultra-550b-a55b, glm-5.3, deepseek-v4.1-flash,
      glm-5.3-flash, gemma-4-31b-it, muse-glimmer-30b, nemotron-3.5-lightning-30b-a3b
8-13  chưa verify đủ / intermittent:
      mistral-nemotron, nemotron-3-super-120b-a12b, ising-calibration-1.5-31b,
      nemotron-3-nano-omni-30b-a3b-reasoning, gpt-oss-20b, llama-3.2-11b-vision-instruct
14-17 last resort: kimi-k3 (hỏng lượt tool), riva-translate x2 (NMT), laguna-xs (code)
```

Kimi-k3 vẫn được giữ trong file vì user yêu cầu "list hết model", nhưng **đẩy xuống cuối** và nói
rõ lý do. Muốn bỏ hẳn thì hỏi user, đừng tự ý xóa entry user đã yêu cầu.

Verify sau khi đổi thứ tự — prompt buộc gọi tool phải KHÔNG còn ra `!`:

```
hermes -z "Dung lenh terminal de tinh 5 nhan 6, roi tra loi ngan gon."  ->  5 × 6 = **30**
hermes -z "Tra loi ngan: thu do Viet Nam?"                              ->  Hà Nội.
```

## 5. Quy tắc rút ra

1. **Size ≠ khả năng agent.** Model 1T hỏng, model 30B chạy tốt. Thứ tự chain là quyết định
   kỹ thuật, không phải bảng xếp hạng tham số.
2. **Probe 1 lượt là chưa đủ.** Muốn biết model có dùng được làm fallback không, phải test qua
   lượt tool-result (có tool schema + system prompt thật).
3. **`!!!!` / rác lặp = đọc `state.db`, không đoán.** `content`, `reasoning_content`,
   `finish_reason`, `tool_calls` tách riêng trong bảng `messages` — đây là nơi duy nhất thấy
   output RAW của model và model nào đã sinh ra nó.
4. **Chain hỏng ở entry #1 = cả chain vô dụng.** Một entry đầu hỏng làm mọi lần fallback thất bại
   dù 16 entry sau đều tốt.
