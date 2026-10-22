# Groq Rate Limits + Dictation (2-in-1) Design

Nguồn: https://console.groq.com/docs/rate-limits (checked 2026-08)

## Free plan limits (cột "Free Plan Limits")

| Model | RPM | RPD | Ghi chú |
|-------|-----|-----|---------|
| whisper-large-v3 / -turbo | 20 | 2.000 | ASH 7.200s audio/h, ASD 28.800s/ngày |
| llama-3.3-70b-versatile | 30 | 1.000 | TPM 12K, TPD 100K |

- Rate limit headers: `x-ratelimit-remaining-requests` (RPD), `x-ratelimit-remaining-tokens` (TPM), `retry-after` khi 429.
- Cached tokens không tính vào rate limits. Limits theo organization, không theo user.

## Chunk sizing math (quota tính theo REQUESTS, không theo audio)

3h meeting = 10.800s audio:

- Chunk 5s → 2.160 requests → **VƯỢT RPD 2.000** → 429 giữa họp. Không dùng.
- Chunk 10s → 1.080 requests → OK nhưng chiếm >50% quota ngày; 2 meeting 3h/ngày → vỡ.
- Chunk 15s → 720 requests → điểm cân bằng, an toàn 2-3 meeting/ngày.
- ASH 7.200s/h: họp 1h chunk 15s xử lý 3.600s audio/h → không chạm.
- Context summary mỗi ~450 ký tự mới: 3h ≈ 180K ký tự ≈ 400 calls llama-3.3-70b → OK dưới 1K RPD, nhưng 2 meeting/ngày chạm trần.
- Full audio 3h transcribe 1 lần = 10.800s > ASH 7.200 → phải tách 2-3 lần gọi giãn cách → summary cuối trễ 1-2h. Không đáng.

## Mic conflict Android — vì sao không chạy 2 luồng thu

Android mic: 1 luồng thu đáng tin cậy. SpeechRecognizer (Google service) + record package chạy song song → recognition failed / audio nhiễu trên nhiều máy.

## Dictation+ (2-in-1) — 1 mic, 2 nhánh (kiểu Flow high mode)

```
Mic → 1 AudioRecorder (record ^6.0.0, onAudioStream() PCM 16kHz)
        ├──→ ghi WAV/m4a liên tục (audio gốc đầy đủ, lưu lại)
        └──→ gom 5s PCM → VAD (webrtc-vad) → segment có tiếng → STT → text nối live
```

- Không xung đột mic: chỉ 1 luồng thu, tách nhánh sau.
- VAD cắt silence → tiết kiệm 50-70% quota (im lặng không gửi).
- record ^6.0.0 có `onAudioStream()` → không cần đổi package.
- STT lựa chọn: Groq whisper segment (chất lượng cao, tốn quota) hoặc Vosk on-device (~50MB, free, chất lượng kém hơn).
- 3 đường STT đã cân nhắc: (1) Android SpeechRecognizer on-device — free, <1s, không lưu audio gốc; (2) model nhỏ on-device sherpa-onnx/Vosk — free nhưng phức tạp, vẫn dính mic conflict nếu ghi song song; (3) server streaming — Whisper không phải streaming model thật, chunk+VAD trễ 2-5s, tốn quota. Loại (3) cho dictation Gboard-style.

## 2 mode thiết kế (không nhét làm 1)

- **Mode Dictation:** Android SpeechRecognizer partial liên tục, trễ <1s, free, không lưu audio gốc chất lượng.
- **Mode Meeting:** chunk 15s + whisper server, transcript chuẩn + audio gốc, trễ ~15s, tốn quota.

## Live transcript = nháp, final = chuẩn

- Chunk transcribe rời rạc chỉ để hiển thị live — sai kệ nó.
- Khi stop: concat toàn bộ audio → transcribe lại 1 lần trên full audio → bản chuẩn thay thế hoàn toàn (đã có pipeline chunks → concat → Whisper → Groq correct).
- Tối ưu: chunk kế tiếp gửi kèm 1-2 dòng transcript trước làm `initial_prompt` → giảm lỗi cross-chunk (context trượt).

## Fallback quota

Theo dõi `x-ratelimit-remaining-requests` mỗi lần gọi → chạm ~20% → tự chuyển sang Vosk on-device hoặc chunk 15s, không chết giữa họp.

## Final summary shape (commit-ready)

`end-json` nâng cấp trả JSON: `{title, context, decisions[], tasks[], difficulties[]}` → popup tổng kết + nút Confirm → lưu meeting + đẩy task + transcript chuẩn.
