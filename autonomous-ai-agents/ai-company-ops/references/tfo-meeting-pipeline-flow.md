## Pipeline xử lý meeting (đã chốt)
- **Hermes = transcribe** (Groq Whisper tốt hơn) → **Claw = xử lý + phản hồi anh** (summarize, phân lời việc). Claw ĐÃ TẮT 24/08 → Hermes giữ cả 2 vai, xem mục "🛡 CHỐNG TRÔI".
- Trao đổi: transcript ở `shared/transcripts/<meeting_id>.txt`, inbox chỉ metadata (meeting_id, giờ, duration, path).
- **Test pipeline khi anh KHÔNG có meeting thật (2026-08, anh yêu cầu "tự tạo transcribe rồi import"):**
  1. Viết transcript giả (text tiếng Việt) → `text_to_speech` tool tạo audio `.ogg`
  2. Upload qua `/api/transcribe` (token qua FORM field, không phải query — 401 nếu để query) → verify transcript trả về
  3. `/api/summarize` với transcript chuẩn → nếu DeepSeek trả rỗng (transient) → retry 2-3 lần, cách 3s
  4. Lưu ý: TTS giọng máy bóp méo tên riêng (EZ80→"EZ80V", Virusto→"Varesto") → transcribe kém hơn giọng thật — KHÔNG phải lỗi pipeline, dùng transcript gốc để test summarize/tasks

- **⚠️ `/api/summarize` — transcript là TEXT field, KHÔNG phải file upload (verify 15/08):**
  - ❌ `curl -F "transcript=@file.txt"` → **422** `Input should be a valid string` (FastAPI field khai báo `str`, không nhận UploadFile).
  - ✅ `curl --data-urlencode "transcript@file.txt"` (kèm `token` + `title` cũng dạng text field) → 200.
  - Response `summary` là **JSON string double-encoded** (chuỗi chứa JSON thoát — `summary` field là `"{\"summary\":...}"`), phải parse 2 lần. `session_id` trả **rỗng** khi gọi API tay — chỉ flow UI đầy đủ (upload→transcribe→summarize) mới tạo meeting hoàn chỉnh có session + lưu vào meetings.json.
  - Triệu chứng 422 giống hệt `type:["string_type"]` trong detail → check field type TRƯỚC khi đổ lỗi pipeline/LLM.
