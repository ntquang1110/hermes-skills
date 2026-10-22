## Streaming realtime STT — Groq KHÔNG có WebSocket streaming (spike 01/09, Quang chốt value 1)

Khi Quang yêu cầu "lắng nghe liên tục / transcribe realtime trong lúc nói" — **đừng tìm WebSocket STT của Groq (không tồn tại)**. API `/audio/transcriptions` chỉ nhận file/chunk hoàn chỉnh. "Realtime" buộc theo **pattern VAD chunking**:

- Client MediaRecorder + WebAudio analyser → phát hiện giọng → cắt PCM 16kHz mono thành chunk **2-5s** → gửi tuần tự (WS hoặc POST) với **overlap 1-1.5s** cuối đoạn trước (tránh cắt mất cuối từ).
- Server gọi `whisper-large-v3` từng chunk → text hiện realtime. Pipeline cũ (`_groq_transcribe` / `_transcribe_chunked` 10-55') GIỮ NGUYÊN — live stream cho xem realtime + ghi chú, khi End vẫn gom qua pipeline cũ nếu cần chính xác tối đa.
- **Latency đo thật (spike 01/09): ~0.8s/chunk 4s audio** — vượt mốc "<3s". Không rate-limit ở tần suất vài chunk liên tiếp.
- **Chất lượng chunk có thể bóp méo tên riêng** ("Giao Vị Châu on Dương Chuan" thay vì "giao việc cho anh Dương") — nhưng đây do giọng TTS máy test (đã biết TTS bóp méo tên riêng), giọng thật tốt hơn nhiều. KHÔNG kết luận "pipeline lỗi" khi test bằng TTS.
- Plan chi tiết: `shared/plan-H1-streaming-2026-09.md`.
- **BẢN BUILD XONG + verify thật (03/09):** `references/h1-streaming-realtime-2026-09.md`. Gồm `app/streaming.py` (VAD RMS + regex task-hint) + `_groq_micro` (browser headers chống 403 1010) + `app/static/index.html` (live card + `startLiveStream`). Pitfall nhanh dính trong build:
  - `OVERLAP_S * FRAME_SAMPLES` ra **float** → `pcm[-s*4:]` ném `TypeError: slice indices must be integers` → WS client thấy "no close frame received" (server chết handler im). Phải `int(OVERLAP_S*FRAME_SAMPLES)`.
  - `StreamSession.feed()` phải lặp qua MỌI frame trong 1 WS message (`for off in range(0,len(raw),FRAME_BYTES)`), đừng chỉ xử lý frame đầu — client gửi nhiều frame/lần thì chẳng bao giờ đủ speech để flush. Triệu chứng: WS không trả về gì dù gửi PCM.
  - uvicorn mặc định dùng websockets protocol (websockets 15 sẵn) — WS chạy ngay không cần wsproto.
  - Client AudioContext: ScriptProcessor channel=1 mono + resample ratio=SR/16000 bằng nội suy tuyến tính (chỉ lấy 1 sample bỏ qua → lệch thời gian chồng chất méo).

### ⚠️ Pitfall Groq API 403 error 1010 (Cloudflare) từ urllib/python

Gọi `https://api.groq.com/openai/v1/...` bằng urllib không kèm browser-headers → **HTTP 403 code 1010** (Cloudflare chặn) dù key đúng (model list cũng dính). Test chẩn đoán: `/models` trả 200 thì key OK, lỗi nằm ở headers.

**Fix: luôn kèm 3 headers — `User-Agent` (browser), `Origin: https://console.groq.com`, `Referer: https://console.groq.com/`.** Kèm đủ 3 → 200. Kiểm tra `_groq_transcribe` trong app TFO có đủ headers này chưa (nếu đang dùng urllib mà không có → thêm vào).
