---
name: whisper-groq-transcription
description: "Use when transcribing long/noisy audio via Groq Whisper."
---

# Whisper / Groq Long-Audio Transcription

Chuyển giọng nói dài (họp, ghi âm meeting) thành transcript sạch bằng Groq Whisper
(`whisper-large-v3`, tối ưu tiếng Việt). Đã verify bằng đo thật trên họp 124 phút + 49 phút (27/08).

## Khi nào dùng
- File audio > 5 phút (họp, recording dài) cần transcribe.
- Transcript bị THIẾU / ngắn bất thường / đầy "đăng ký kênh / subscribe / video h d" (hallucination).
- User hỏi "sao transcript ngắn thế" / "sao cứ lặp nghiền video" — cần chẩn đoán bằng dữ liệu trước khi báo.

## Quick start — pipeline chuẩn
```
_get_duration(path)
chunk_s = 150        # 2.5 phút — Groq cắt trước đó mất ~½ nội dung
overlap_s = 15
mỗi chunk: cắt ffmpeg -ss start -t dur -ar 16000 -ac 1
  → _groq_transcribe(force_compress=True, clean=False)  # nén opus 16k+boost 12dB
  → _strip_ads(raw)                                     # lọc hallucination theo CỤM
  → retry 3 lần lỗi tạm; fail/bỏ chunk (không chết cả bản)
nối + dedup overlap → _strip_ads(final)                  # pass cuối toàn bản
```
Mã fix chuẩn tham khảo: `ai-company/app/main.py::_transcribe_chunked` + `_strip_ads`.

## BẮT BUỘC: check audio TRƯỚC khi gọi STT (verify 03/10/2026)

**Voice từ Telegram KHÔNG phải lúc nào cũng có tiếng.** File rỗng → Whisper hallucinate template mặc định ("Hãy subscribe cho kênh...") → user tưởng STT hỏng.

Chạy check trước, 2 giây, chặn trước khi tốn 1 call API:

```bash
python scripts/audio_check.py <file.ogg>
# exit 0 = PASS (có tiếng) · exit 1 = FAIL (đừng gọi STT)
```

Đo được trên voice rỗng thật (03/10/2026): 149.2s, **1.824 bps**, **mean/peak -91.0 dB**, **100% im lặng**, **0% khung có tiếng**. Whisper đọc ra `Hãy subscribe cho kênh La La School...` lặp 4 lần — không phải lỗi Groq, mà là không có gì để nghe.

**Khi audio FAIL:** báo user là file không có sóng âm (mic/app ghi âm), **không** gọi STT, **không** đoán nội dung.

**Khi transcript vừa nhận mà toàn template lặp:** nghi audio rỗng, chạy `audio_check.py` xác nhận trước khi báo. Kiểm tra `has_hallucination()` nếu cần tự động hoá.

File trùng nhau: md5 giống = cùng 1 file, đếm 1 lần. Đừng kết luận "nhiều file hỏng" khi thực ra là 1 file bị gửi nhiều lần.

---

## Voice message NGẮN từ Telegram (đã verify 08/09/2026)

Khi user gửi voice < 60s mà Hermes auto-transcribe BỊ LỖI ("could not be transcribed automatically", file .ogg trong cache/audio) — user chờ, đừng mất thời gian mở skill/pipeline. **1 call Groq thẳng, không chunk, không compress:**

```python
import requests
r = requests.post('https://api.groq.com/openai/v1/audio/transcriptions',
    headers={'Authorization': f'Bearer {GROQ_API_KEY}'},
    files={'file': ('a.ogg', open(path,'rb'), 'audio/ogg')},
    data={'model': 'whisper-large-v3', 'language': 'vi'}, timeout=90)
text = r.json().get('text')
```

- GROQ_API_KEY đọc từ `~/AppData/Local/hermes/.env` (regex `GROQ_API_KEY\s*=\s*(\S+)`).
- File 10–60s trả về trong ~5–15s. Voice lẫn tiếng Việt lẫn tiếng Anh vẫn giữ nguyên 2 ngôn ngữ.
- Lỗi voice của Hermes thường do mô hình auto-STT mặc định, KHÔNG phải do file hỏng — đẩy Groq là thoát ngay. User phản hồi: "đẩy qua groq là được mà, gì mà lâu vậy" — tốc độ quan trọng hơn hoàn hảo.

## Ngưỡng quan trọng
- **Chunk ≤ 150s (2.5 phút).** Chunk 10 phút → Groq rơi ~½ nội dung (đo: 273 vs 563 từ cho cùng span).
- **Chunk nếu duration > 300s (5 phút).** Đừng dùng ngưỡng 55 phút — single-call file 5–55 phút cũng truncate.

## Hallucination của Whisper — 2 dạng phải lọc
1. **Template full-word:** `đăng ký kênh, subscribe, ủng hộ kênh của mình, Ghiền Mì Gõ, lalaschool, cảm ơn các bạn đã theo dõi, phần bình luận, like and share, để không bỏ lỡ những video hấp dẫn`.
2. **Dạng bóp méo (regex chuẩn KHÔNG trúng):** Whisper bóp "đăng ký kênh để nhận thông tin" thành rời nguyên âm:
   `H k k nh th tin nh, video h d, C c b theo tin nh, Ghiền tin nh, T d ki l..., bộ phim này có nhiều phần, các bạn có thể (nhìn thấy|tìm hiểu)..., nếu bạn muốn (tìm hiểu|biết thêm)...`.
   Cứ tái diễn trên audio mờ — phải add vào strip pattern.

Xem catalog đầy đủ + bài học chi tiết: `references/whisper-hallucination-cleaning.md`.

## Pitfalls
- **Dấu hiệu "bóp méo" cũng rơi vào NỘI DUNG THẬT, không chỉ template quảng cáo — đừng strip, phải GẮN CỜ (verify 18/10/2026).** Cùng dấu hiệu (chuỗi token ngắn, mất dấu, đọc không thành câu: `anh bi r l C c th c m ho nh th n`) nhưng lần này nó nằm **giữa nội dung thật** của user, không phải ad. Nếu đem regex strip-hallucination ra xử → **xoá mất chính câu hỏi của user**; nếu im lặng đoán → bịa. Luật:
  1. Phân biệt bằng **vị trí**: chuỗi méo nằm giữa câu chuyện có nghĩa ⇒ nội dung thật bị mờ; méo + lặp + có `subscribe/kênh/video h d` ⇒ hallucination.
  2. Nội dung thật bị mờ ⇒ **KHÔNG strip.** Khôi phục ý từ ngữ cảnh hai đầu nếu chắc, rồi **nói thẳng với user đoạn nào không nghe rõ và xin xác nhận** — thay vì trình bày bản khôi phục như thể chắc chắn.
  3. Mẫu câu đã dùng được: *"Đoạn giữa audio bị mờ nên Whisper rớt chữ — nếu đệ hiểu sai chỗ nào thì là do audio, anh sửa giúp."*
  4. **Không bao giờ để bản khôi phục đoạn mờ gánh một quyết định** (đổi hướng task, đổi tham số, đổi phạm vi). Chỗ nào dựa vào đoạn mờ thì hỏi lại.
- **Clean TỪNG chunk, không clean cả bản 1 lần** — chunk hallucination nặng khi clean toàn bản sẽ nuốt nội dung thật (mất 80% họp).
- **Strip theo CỤM ad, không drop cả câu.** Câu trộn ad + nội dung thật ("Nếu không làm bên tôi yêu cầu... Hãy đăng ký kênh") → chỉ xoá clause ad, giữ thân câu.
- **Regex toàn optional phá câu:** alternative nào cũng có token bắt buộc. `(?:...)?(?:...)?` khớp chuỗi rỗng khắp nơi → chèn space giữa từng ký tự.
- **Bọc `requests.post` trong try/except** → trả sentinel, đừng để `r` undefined (NameError) chết cả pipeline.
- **Noise reduction (afftdn) KHÔNG cứu Whisper** — đo thật raw thậm chí giảm. Whisper hallucinate do nhiễu nền từ gốc; chỉ ghi lại chỗ yên mới khắc phục.
- **Coverage guard 120 từ/phút là miscalibrate** cho họp thật (~25–30 từ/phút hiệu dụng). Đừng kết luận "THIẾU = lỗi pipeline" khi chỉ là audio thưa. Metric đếm cả hallucination.
- **Khi user hỏi "sao ngắn": đo raw (chưa strip) + mean_volume + % silence TRƯỚC khi báo.** Nếu raw đã thấp + ồn → là chất lượng ghi âm, không phải lỗi pipeline.

## YouTube / Video audio fallback khi transcript bị chặn (2026-09-22)

Khi `youtube_transcript_api` ném `IpBlocked` hoặc timedtext trả 429, transcript không lấy được. Fallback đã verify trên video 15 phút `xVRZdN3UeiE` (Beyond Limits, 916s, 19.5K chars thu được):

1. `yt-dlp` `extract_info` lấy title/channel/duration + kiểm tra `automatic_captions` có `vi`/`vi-orig`.
2. Nếu timedtext 429: tải `bestaudio` (format 251 webm) → `ffmpeg -ar 16000 -ac 1 -b:a 48k` sang mp3 → chunk 150s + overlap 15s → Groq `whisper-large-v3` với `language='vi'` (hoặc `'en'`) từng chunk → nối. Kiểm tra `len(full) > 1000` trước khi viết draft.
3. Lưu ý GROQ_API_KEY: file `.env` có thể chứa 2 dòng trùng + bản rút gọn `gsk_yH...2HZE` (do tool cắt). Luôn lấy dòng cuối cùng, verify `len==56` và không chứa `...` trước khi gọi API. Mẫu đọc đúng: `[l.strip().split("=",1)[1] for l in open(env).readlines() if l.strip().startswith("GROQ_API_KEY=gsk")][-1]`.

## Verify
- So raw (clean=False) vs stripped: raw thấp nghĩa là Whisper không bắt được, không phải strip quá tay.
- Đếm residual marker (`video|ghiền|h k k|đăng ký`) trước/sau strip → target ~0.
- Anchor-check: bảo đảm từ khoá nội dung thật (tên đối tác, số liệu, thuật ngữ) còn nguyên sau strip.