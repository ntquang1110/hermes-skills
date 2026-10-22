# Whisper hallucination cleaning + Groq long-audio transcribe — verified detail (27/08)

Nguồn: họp chăn nuôi dài (30acc46edf 124.8 phút, 6f9b5f0216 49 phút). Mã fix chuẩn trong
`ai-company/app/main.py::_transcribe_chunked` + `_strip_ads` (commit 28575f3 → 568b229).

## 1. Groq Whisper RƠI nội dung trên chunk dài (đo thật, không phải đoán)
- Chunk 10 phút → mất ~½. Đo: span 2850–3450s, 1 chunk 10p = 273 từ; chia 4×2.5p = 563 từ (2×).
- **Chunk long-meeting tối đa ~150s (2.5 phút) + overlap 15s.**
- Ngưỡng chunk `duration > 3300` là SAI cho file 5–55 phút (single-call cũng truncate). Đặt `> 300` (5 phút).
- Raw có thể chỉ ~36 từ/phút trên audio ồn — Whisper không bắt nổi chứ không phải file nghỉ.

## 2. Hallucination của Whisper (Vietnamese), 2 dạng phải lọc khác nhau
### a) Template full-word (bắt được bằng regex chuẩn)
`đăng ký kênh`, `subscribe`, `ủng hộ kênh của mình`, `nhận thêm bài hát/video`, `Ghiền Mì Gõ`,
`lalaschool`, `cảm ơn các bạn đã theo dõi và hẹn gặp lại`, `trong phần bình luận`, `like và share`,
`để không bỏ lỡ những video hấp dẫn`.

### b) Dạng bóp méo — con-son skeleton (regex chuẩn KHÔNG trúng)
Whisper bóp "đăng ký kênh để nhận thông tin nhất" thành rời nguyên âm. Các biến thể quan sát được
(add vào `_strip_ads`/GUZZ — cái này cứ tái diễn trên audio mờ):
```
H k k nh th tin nh | H k c m nh | C c b theo (tin nh) | c c b theo d v h g l
Ghiền tin nh | (kênh )?ghiền mì gõ
tin video h d | Ghi video h d | video h d | tin video tin nh | k kh b l nh video
T d ki l ... | sinh th chi ph (c c h)
bộ phim (này) có nhiều phần | những video tiếp theo | nhiều video mới
các bạn có thể (nhìn thấy|tìm hiểu|nhận thêm|video|tin)... | nếu bạn muốn (tìm hiểu|biết thêm)...
(^|\s)tin nh\b | (^|\s)tin theo\b
```

## 3. Clean TỪNG CHUNK, không clean cả bản ghép 1 lần
- Clean cả bản (drop câu) → chunk hallucination nặng nuốt nội dung thật, mất ~80% cuộc họp.
- Strip theo **CỤM ad** (xoá clause ad, GIỮ thân câu thật) — không drop cả câu khi câu trộn ad + nội dung.
- Sau khi nối, **1 pass cuối `_strip_ads(final)`** để hết residual cross-chunk.

## 4. Regex pitfall — toàn optional = phá câu
Mọi alternative PHẢI có token bắt buộc. `(?:của ...)?(?:trên ...)?` (cả 2 optional) khớp chuỗi rỗng
ở mọi vị trí → `re.sub` chèn space giữa từng ký tự, hỏng cả câu thật.

## 5. Per-chunk resilience
- Bọc `requests.post` Groq trong try/except → trả sentinel `"Groq error request-failed: ..."`,
  đừng để `r` undefined (NameError) chết cả pipeline.
- Retry 3 lần/chunk (backoff 2·attempt) cho lỗi tạm; chunk toàn ad / fail thì BỎ chunk, không chết bản dài.

## 6. Coverage guard miscalibrate
`transcript_coverage.py` kỳ vọng 120 từ/phút (nói liên tục) — KHÔNG hợp họp thật (~25–30 từ/phút
hiệu dụng, nhiều khoảng nền/im). Metric đếm cả hallucination nên strip ad làm coverage giảm dù chất lượng tăng.
Cần calibrate theo mật độ họp thật, không tự đổi khi chưa có chỉ đạo.

## 7. Noise reduction KHÔNG giúp Whisper (đo 27/08)
`ffmpeg afftdn=nr=25/35:nf=-35/-45` trên audio nhiễu nền → raw KO tăng, thậm chí giảm (71→51–61 từ thật).
Whisper bị hallucination do noise từ GỐC, preprocess không cứu được. Chỉ ghi âm lại chỗ yên mới khắc phục.