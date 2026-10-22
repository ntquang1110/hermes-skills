# H1 — Streaming Realtime TFO (build thật, verify 03/09)

Bản build hoàn chỉnh của plan-H1-streaming-2026-09.md. Khớp value 1 vision (CEO nói
trong meeting → transcribe + task hint tức thời). Server 8100 chạy code này rồi.

## Kiến trúc đã build

```
Browser: AudioContext.createScriptProcessor(1024,1,1) → downmix+resample 48k→16k float32
   → mỗi 100ms gửi 1 frame (1600 samples) qua WS binary
Server /ws/stream (FastAPI WebSocket): StreamSession VAD (RMS) tích giọng
   → im lặng 700ms / >6s lời → Groq micro-chunk transcribe 1 đoạn
   → broadcast {"type":"text","seg":N,...} + {"type":"task_hint","hints":[..]}
```

Files: `app/streaming.py` (VAD + task-hint regex) + `app/main.py` (`_groq_micro` +
`@app.websocket("/ws/stream")`) + `app/static/index.html` (live card + `startLiveStream`).

## Pitfalls (dính thật trong build)

1. **Không có WS STT thật của Groq** — "realtime" = VAD chunking, không skin. Đã biết từ trước, lặp lại cho chắc.
2. **`_groq_micro` PHẢI kèm browser headers** (User-Agent + Origin + Referer console.groq.com) khi gọi `/audio/transcriptions` bằng `requests`/`urllib` → thiếu = 403 code 1010 Cloudflare.
3. **`StreamSession.feed()` phải lặp qua MỌI frame trong 1 message.** Bản đầu chỉ xử lý `raw[:FRAME_BYTES]` (frame đầu) → client gửi nhiều frame 1 lần thì chỉ nạp 1 → không bao giờ đủ speech để flush. Fix: `for off in range(0,len(raw),FRAME_BYTES): _feed_frame(...)`.
4. **`OVERLAP_S * FRAME_SAMPLES` = float** (1.0×1600=1600.0) → `pcm[-s*4:]` ném `TypeError: slice indices must be integers`. Phải `int(OVERLAP_S*FRAME_SAMPLES)`. Triệu chứng: WS client "no close frame received" — server chết handler im.
5. **VAD "đoạn quá dài" check dùng số lượng frame**, đổi thành `*10` so với giây (int frame/s, 0.1s/frame) — dễ nhầm đơn vị.
6. **PCM float32 chỉ gửi dạng frame chuẩn 1600 samples.** Set ScriptProcessor channel=1 (mono), resample ratio=SR/16000 với nội suy tuyến tính để tránh lệch thời gian chồng chất (bị méo nếu chỉ lấy 1 sample bỏ qua).

## Test thật (bằng chứng H1 done)

- Unit `StreamSession`: speech+silence → 1 flush; 2 đoạn → 2; im lặng/nhiễu thấp → 0.
- WS thật (client gửi sine PCM): server nhận → Groq trả text realtime → disconnect không crash.
- 7/7 script blocks `node --check` PASS; login browser + dashboard load sạch, `startLiveStream` global, liveCard ẩn khi chưa ghi.
- Auth gate giữ nguyên: `/` không lộ `viewDashboard`, `/app` cần cookie.

## Chạy/restart server 8100

Respect lifecycle guard: `.venv/Scripts/python.exe` inline trong terminal bị chặn
(`embedded null character in path`). Chạy bằng script `python C:/Users/NTQUANG_DELL/
AppData/Local/hermes/scripts/tfo_launch.py` (background, watch "Application startup
complete"). uvicorn mặc định dùng websockets protocol (websockets 15 đã có) — WS chạy
ngay không cần wsproto. Kill PID cũ qua `taskkill /PID <pid> /F` (tra `netstat -ano |
grep :8100`).

## H2/H3 (chưa làm lúc ghi file — 03/09)

- H2 Context-scan chủ động: có sẵn `hub/context_scan.py` trả `proposals[]` text; cần C1 (JSON action + effort), C2 (task draft store), C3 (chốt 1-click), C4 (push TG gọn).
- H3 Reliability: L1 auto-restart/health, L2 backup D, L3 uptime probe.