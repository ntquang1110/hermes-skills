# Chất lượng pipeline STT → Summary: checklist chẩn đoán (đã triển khai + verify 08/2026)

## Triệu chứng
User phàn nàn: "meeting sum tệ, transcript loss nhiều từ, convert sang vấn đề/task/decision không chuẩn".
Đây là phàn nàn lặp lại về chất lượng, không phải lỗi chạy 1 lần. Khi gặp: ĐỌC pipeline code thật theo từng tầng, không đoán.

## Quy trình chẩn đoán
1. Đọc pipeline code theo tầng: record → compress → STT → summarize → extract.
2. Verify tham số từng tầng: bitrate nén, có `prompt`/initial_prompt không, chunk size + overlap, có truncate transcript trước LLM không, parse kết quả thế nào.
3. Xếp hạng fix theo tác động, trình user duyệt trước khi code (critique-first).
4. **Test bằng file audio thật, so sánh transcript cũ vs mới** — không tin code đúng chỉ vì chạy không lỗi.

## 6 nguyên nhân gây mất từ (đã fix + verify bằng file 0880bf48a6, 20 phút)

### 1. Nén audio quá tay + THIẾU VOLUME BOOST — yếu tố quyết định
- Opus 16kHz mono @ 24kbps quá thấp cho tiếng Việt (thanh điệu + từ chuyên ngành: kiềm, ASF, kim loại nặng...).
- **Volume boost 12dB + highpass 80 + lowpass 8000 là CHÌA KHÓA**: test thực tế không boost → mất hẳn nội dung ("anh Mão giới thiệu trại 20-30 con"), có boost → bắt đủ. ffmpeg: `-af "volume=12dB,highpass=f=80,lowpass=f=8000" -ar 16000 -ac 1 -c:a libopus -b:a 48k`.
- Rule: file < 25MB (Groq limit) → vẫn NÉN + BOOST (Opus 16kHz nén Whisper xử lý tốt hơn mp3 gốc — verified). Trừ voice note < 1MB gửi thẳng.
- Nơi gặp: ai-company/app/main.py `_groq_transcribe`.

### 2. Whisper hallucination (subscribe/like/share lặp)
- Triệu chứng: transcript chèn "Hãy subscribe cho kênh Ghiền Mì Gõ", "đăng ký kênh", "like share" lặp hàng chục lần.
- **Fix: heuristic clean theo CÂU** (tách bằng regex `(?<=[.!?])\s+`), xóa câu chứa marker quảng cáo + câu vô nghĩa (avg word len < 2.5) + câu lặp y hệt.
- **KHÔNG dùng LLM clean** — llama-3.3-70b xóa nhầm nội dung thật, trả câu meta "Không có nội dung...". Heuristic an toàn, giữ số liệu + tên.
- Cũng thay từ sai chuẩn: "kiếm vãi nặng"→"kim loại nặng", "tiêu sảy"→"tiêu chảy", "chủ chạy"→"chủ trại".

### 3. initial_prompt DÀI gây hallucination lặp lại chính nó
- Truyền danh sách từ khóa dài (kiềm, ASF, kim loại nặng...) → Whisper NHẮC LẠI CẢ PROMPT trong transcript ("...châu Phi, ASF, phòng dịch, trại lợn châu Phi, ASF...").
- Rule: initial_prompt GIỮ NGẮN 1 câu: `"Cuộc họp nội bộ về chăn nuôi, sản xuất, kinh doanh."`. Đủ định hướng, không bị lặp.

### 4. Chunk theo SIZE thay vì DURATION — Whisper direct trên file dài mất nội dung
- File 20 phút gửi thẳng (dù < 25MB) → transcript chỉ 3-5k ký tự (mất 2/3). Chunk 10 phút → 6-13k ký tự đầy đủ.
- Rule: chunk theo DURATION (> 55 phút mới chunk vì nén Opus 48k ~7MB/30p, 24MB limit ~100p; nhưng nếu thấy mất nội dung thì giảm ngưỡng). Chunk 10 phút + overlap 30s + dedup biên (so 30-60 từ đầu chunk sau với cuối chunk trước).
- **Thứ tự boost/chunk quan trọng**: boost TOÀN FILE trước khi cắt chunk, không chunk trước rồi boost sau (khuếch đại nhiễu + hallucination).

### 5. Truncate transcript trước khi LLM summarize — lỗi nặng nhất
- `transcript[:8000]` → cuộc họp 30-60 phút (~15-30k ký tự) mất 2/3 nội dung TRƯỚC khi extract vấn đề/task/decision.
- Rule: KHÔNG BAO GIỜ truncate. Chunk-summarize: chia ~3500 ký tự/đoạn → summarize từng đoạn (system prompt NGẮN) → gom → summarize tổng → JSON.

### 6. DeepSeek/OpenCode endpoint trả RỖNG — 2 pitfall chết người
- **`response_format={"type": "json_object"}` trên OpenCode endpoint → trả content RỖNG 100%** (status 200, content `''`). PHẢI bỏ, chỉ ép JSON bằng prompt ("OUTPUT: CHỈ JSON thuần, bắt đầu bằng {, không markdown").
- **Prompt dài → trả rỗng ~40-50%** ngẫu nhiên (không theo quy luật độ dài; system dài + input 5000 chars thường rỗng, system ngắn + input 5000 OK). Fix: retry loop trong `call_deepseek` (3 lần) + chunk nhỏ (3500) + system prompt NGẮN cho bước partial.
- Model trả markdown thay vì JSON khi input dài → ép lại lần 2 với output NGẮN vừa có (retry tối đa 4 lần cho bước ép JSON).
- **PA A chuẩn (đã chọn)**: chunk-summarize DeepSeek flash → bước JSON cuối dùng **Groq llama-3.3-70b + response_format json_object** (Groq ổn định, không trả rỗng, JSON chuẩn, assignee/deadline đầy đủ). Fallback: ép JSON lại bằng DeepSeek prompt thuần.

## TFO app — bản đồ code (D:/Hermes Proj/ai-company/app/main.py, port 8100)
- Flow: `/api/record/end` → `_finalize_recording` → `_groq_transcribe` (duration > 3300s → `_transcribe_chunked`) → `/api/summarize` (`_summarize_full`: chunk → Groq JSON) → task gen từ JSON → push Telegram.
- Các hàm: `_groq_transcribe` (boost+Opus 48k+clean heuristic), `_transcribe_chunked` (chunk 10p + dedup), `_summarize_full`/`_summarize_single`/`_groq_summarize_json`, `call_deepseek` (retry 3 lần) trong hub/store.py.
- INITIAL_PROMPT: 1 câu ngắn (xem mục 3). `_clean_transcript`: heuristic theo câu (xem mục 2).

## Frontend dashboard — pitfall JS date parsing (đã fix 08/2026)
- **V8 `new Date('Thứ 7')` → Sun Jul 01 2001! `new Date('Tuần 1')` → Jan 01 2001** — V8 nhặt SỐ trong chuỗi làm month → mọi deadline text ("Thứ 7", "Tuần X") bị coi là quá hạn → KPI "Task quá hạn" toàn đỏ.
- Rule: parseDate KHÔNG fallback `new Date(s)`. Chỉ regex 2 dạng: `^(\d{1,2})\/(\d{1,2})\/(\d{4})$` (dd/mm/yyyy) hoặc `^(\d{4})-(\d{2})-(\d{2})(?:[ T].*)?$` (ISO). Còn lại (mốc tương đối) → null → không tính quá hạn.
- Test: node chạy parseDate với từng deadline thật trước khi tin KPI.

## Verify checklist (chạy sau khi sửa pipeline)
1. Transcribe file audio thật → transcript phải ≥ 5k ký tự / 20 phút, không còn "subscribe/like/share", giữ tên + số liệu.
2. Summarize → JSON hợp lệ có summary/issues/decisions/tasks, không bị cắt (`transcript[:8000]`).
3. KPI dashboard: deadline "Thứ 7"/"Tuần X" KHÔNG tính quá hạn; ngày cụ thể dd/mm/yyyy mới tính.
4. JS syntax: extract `<script>` → `node --check` sau mỗi patch HTML lớn.
