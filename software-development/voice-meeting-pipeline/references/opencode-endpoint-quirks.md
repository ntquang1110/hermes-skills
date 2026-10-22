# OpenCode/DeepSeek endpoint quirks (đã debug 05/08/2026)

## Hiện tượng
- Endpoint `http://192.168.1.110:20128/v1` (OpenCode) trả **content RỖNG ~40-50%** số lần gọi khi input dài
  — status 200 nhưng `choices[0].message.content == ""`. Không theo quy luật độ dài rõ ràng
  (1000-4000 chars đôi khi rỗng, 5000 OK — random).
- `response_format: {"type": "json_object"}` → trả rỗng **~100%** — endpoint không hỗ trợ đúng chuẩn.
- Tổng prompt (system + input) vượt **~5000 chars** → trả rỗng. System prompt dài cũng kích hoạt.

## Workaround đã xác nhận hoạt động
1. **Bỏ `response_format` hoàn toàn** — ép JSON bằng prompt thuần ("Trả về JSON..."). Model vẫn ra JSON chuẩn.
2. **System prompt NGẮN** (1-2 câu), chunk input ≤ ~5000 chars.
3. **Retry 3-4 lần khi content rỗng** — bắt buộc trong mọi wrapper gọi endpoint.
4. Nếu kết quả không phải JSON (markdown/text) → **gọi lại lần 2 với chính output NGẮN đó** làm input,
   payload nhỏ → ít trả rỗng hơn.
5. Model chậm (`deepseek-v4-pro`) → timeout 60s → None → fallback mất dữ liệu.
   Dùng `deepseek-v4-flash`, timeout 180s.

## Kết quả so sánh 3 phương án (PA) — đã test trên transcript 5340 chars
| PA | Cách | JSON | Chất lượng | Kết luận |
|---|---|---|---|---|
| **A** | Groq llama-3.3-70b + `response_format=json_object` | ✅ chuẩn lần đầu | Summary ngắn, ít chi tiết số | **CHỐT — dùng cho production** |
| B | DeepSeek text + Python heuristic parse | ⚠️ bẩn | Nhiều chi tiết | Loại — parse phụ thuộc format LLM |
| C | DeepSeek chunk 2000 + retry 6 | ✅ sau retry | Khá đầy đủ | Tốt nhưng dựa endpoint yếu |

**Chốt:** chunk-summarize bằng DeepSeek flash → bước JSON cuối bằng **Groq llama-3.3-70b** (Groq ổn định, hỗ trợ json_object thật, cùng provider đang chạy STT).

## Verify nhanh
- `debug_json_no_fmt.py` pattern: bỏ response_format → model trả JSON hoàn hảo.
- `debug_retry.py` pattern: retry vòng lặp khi content rỗng → trả `{"ok": true}` với 5340 chars.
