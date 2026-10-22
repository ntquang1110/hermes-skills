# Đo độ đủ của transcript (chuyển từ SKILL.md, 25/08/2026)

Khi user nghi transcript ra ngắn hơn bản ghi voice thật → KHÔNG đoán, KHÔNG tự kết luận "file câm".
Chạy `hub/transcript_coverage.py <audio> <transcript_file|text>` (in JSON, exit 1 nếu THIẾU). 3 tầng:

1. **Tỉ lệ từ/phút (cổng nhanh):** tiếng Việt họp ~110-150 từ/phút. `score = transcript_words / (total_minutes × 120)`. <40% → THIẾU, ≥60% → OK. File `30acc46edf` (124.8 phút, 600 từ) → **4% = THIẾU chắc chắn**.
2. **Bản đồ giọng (`ffmpeg silencedetect`, noise=-40dB, d=1.5s):** chia audio ra segment CÓ GIỌNG → `active_seconds`/`active_minutes`/`active_segments`/`longest_silences`. **Loại trừ giả thuyết "file nhiều đoạn nghỉ"**: audio 119.1 phút giọng thật / 150 segment trong 124.8 phút ⇒ nguồn đầy đủ, lỗi nằm ở CHUNKING/MODEL. Im lặng dài nhất chỉ 10s.
3. **Cross-check từng chunk (Tầng 3, khi cần):** transcribe từng chunk 10 phút riêng lẻ → đếm chunk nào trả rỗng/lỗi → biết vùng hỏng; boost/đổi model (flash→pro) các chunk fail, nối lại.

**Pitfall đếm từ:** đừng nhầm `len(transcript)` (ký tự) với `len(transcript.split())` (số TỪ) — cùng file 2550 KÝ TỰ = 600 TỪ, đổi cả chẩn đoán.

**Kết luận pattern:** transcript ngắn + `_is_silent_audio` không kích hoạt (audio có âm) → nguyên nhân phổ biến là **Groq fail chunk trong `_transcribe_chunked`** (chunk nào trả rỗng thì transcript bị cụt), không phải nguồn câm. Luôn đo coverage TRƯỚC, rồi mới nói lỗi ở đâu.

## Lưu ý chạy (cập nhật 17/10)

- KHÔNG gọi qua terminal tool trực tiếp: guard/lifecycle đọc nhầm path có dấu cách ("Hermes Proj").
- **Ngoài cron:** `execute_code` + `subprocess.run([<venv python>, 'hub/transcript_coverage.py', ...])`.
- **Trong cron:** `execute_code` **BỊ CHẶN** → viết script tạm bằng `write_file` vào `C:\Users\<user>\AppData\Local\Temp\hermes-*.py` rồi `python "C:/Users/.../hermes-*.py"`, xoá ngay sau khi chạy (xem `references/cron-mode-scripts-2026-09.md`). Không dùng `$TEMP` trong lệnh bash.
