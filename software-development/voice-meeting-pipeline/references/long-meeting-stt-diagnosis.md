# Chẩn đoán transcript họp dài "THIẾU nội dung" (Groq chunked Whisper)

Dùng khi transcript của bản ghi âm họp dài (>55 phút) chỉ ra vài trăm từ trong
khi audio dài hàng tiếng. Quy trình CHỨNG MINH gốc rễ bằng đo, không đoán —
tránh chạy transcribe 14..50 lần một cách lan man.

## Bước 0 — Đo coverage sạch
Nếu repo có tool: `hub/transcript_coverage.py <audio> <transcript>`.
Công thức: `score = transcript_words / (total_minutes × 120)` (<40% THIẾU, ≥60% OK).
LƯU Ý: metric này đếm CẢ hallucination — strip ad xong coverage có thể GIẢM dù
chất lượng cao hơn. Là metric thô, không phải thước chất lượng tuyệt đối.

## Bước 1 — Phân biệt 3 gốc rễ (đều bắt đầu bằng 1 file)
Không chạy full pipeline trước. Cắt vài window nhỏ trên CHÍNH file đó:

1. **Groq whisper RƠI nội dung trên chunk dài** (gốc rễ #1, chứng minh 27/08):
   - Lấy 1 span, transcribe CẢ span ở 2 chế độ:
     - 1 chunk dài (vd 600s=10 phút) → đếm từ
     - chia thành 4× window 150s (2.5 phút) → SUM từ
   - SUM nhỏ-window >> chunk dài (vd 273 → 563, gần 2x) = **truncation**.
     Fix: chunk ≤150s. Chú ý chunk ĐẦU file ít bị hơn chunk giữa — đừng lấy đầu
     file làm kết luận rằng "không truncate".
2. **Hallucination Whisper trên audio êm** ("đăng ký kênh/subscribe/bài hát/
   kênh giả lalaschool/Ghiền Mì Gõ"): 1 window 150s vùng mờ có thể trả toàn ad.
   Clean theo CỤM ad (giữ câu thật), KHÔNG drop cả câu ở global.
3. **Cleaner over-aggressive drop cả câu khi dính ad** → mất nội dung thật trộn
   chung câu. Verify: áp cleaner lên câu có cả ad + nội dung thật, xem phần thật
   còn sống không. Chuyển sang strip-clause-ad thay vì drop-sentence.

## Bước 2 — Fix mô hình chuẩn
- chunk 150s + overlap 15s (thay 600s/30s)
- transcribe từng chunk `clean=False`, rồi strip ad NGAY từng chunk
- retry 3 lần/chunk (network/rate-limit/empty); 1 chunk hư thì BỎ, không chết cả bản dài
- `requests.post` STT bọc try/except → trả sentinel thay vì để `r` undefined (NameError)

## Pitfall regex (đã vấp)
Đừng để regex có MỌI group optional (cả `(?:...)?`): `re.sub` khớp chuỗi rỗng ở
mọi vị trí → chèn space giữa TỪNG ký tự, hỏng cả câu thật (39 từ → 0). Mỗi
alternative phải có token bắt buộc (`\s+kênh\b`, `nhận`, `subscribe`...).

## Verify sau fix
- Chạy LẠI full pipeline (không tinker tay file) → tái lập gần đúng số từ.
- Check path single-call (<55 phút) không regress từ try/except.
- Check anchor thật còn tồn tại (kháng thể, Chú Tiến/ông Cần, hợp đồng...).
- LƯU Ý Whisper stochastic: cùng span 2 lần chạy cho từ khác nhau ("Chú Tiến" vs
  "ông Cần") — KHÔNG phải bug. Chỉ coi là mất nội dung thật khi CẢ đoạn biến mất.
- Media file dài 20 phút đi qua path single-call (`_groq_transcribe`) — có thể cũng truncate một phần.