# Voice Assistant Phase A — Whisper local Mac node + TTS/interrupt techniques

Session 03-04/09/2026. Plan: `D:/Hermes Proj/voice-live-plan-final.md` + contrib files
`D:/Hermes Proj/.hermes-state/plan-contrib-*.md` (BA/SA/CTO/Dev). Demo initial = Phase A + B read-only.

## Whisper local STT node (Mac mini M1) — verified thật

Doc từ Quang: preview.thefirstonly.com/4us8yrbjfr51. Node: transcribe local fallback cho file dài.

- SSH: `tquang@192.168.1.3` pw `<PASSWORD>` (LAN nội bộ).
- Script: `~/whisper-venv/bin/python ~/whisper/run_whisper.py <audio> --lang vi [--json]`.
- Model: Systran/faster-whisper-large-v3 cached (~/.cache/huggingface/hub), faster-whisper 1.2.1, ctranslate2 4.8.2, Python 3.9.6.
- Agent gọi qua paramiko (no sshpass trên Windows): `SSHClient + set_missing_host_key_policy(AutoAddPolicy)`, SFTP `put` trước rồi exec_command run_whisper.py.
- **Latency đo thật: ~10.6s cho clip ngắn + SSH roundtrip + model load.** → Chỉ dùng cho FILE DÀI / fallback, KHÔNG dùng realtime từng câu (cần <3s). Realtime vẫn đi Groq.

## Phase A techniques (voice realtime 2 chiều)

Modules mới trong `app/`:
- `voice_lemma.py` + `voice_lemma.json` — post-STT normalize tên riêng tiếng Việt (Kiềm Khoáng Thảo Mộc/Tía tô/Saphia/Xạ đen/Hoàn ngọc/Chè dây). Deterministic 0đ, chìa khóa demo.
- `tts.py` — TTSProvider interface + EdgeTTSProvider + CachedTTSProvider (LRU + file cache cho `/tts/<hash>.mp3`).
- `turn_manager.py` — turn_id đơn điệu + cancel; kết quả trễ có turn≠active bị bỏ.
- `ws_stream` trong main.py — dùng `websocket.receive()` để nhánh `text` (JSON control interrupt) vs `bytes` (PCM). Gửi JSON down: `text/state/answer/audio/interrupted`.

### TTS edge pitfalls (đã dính, đã fix)
1. **`synth()` sync wrapper dùng `asyncio.run()` SẼ LỖI khi gọi trong event loop đang chạy** ("asyncio.run() cannot be called from a running event loop"). Phải có `synth_cached_async()` async method gọi thẳng `await inner._synth_async(text)`.
2. **`asyncio.nop()` KHÔNG tồn tại trong Python 3.9** (chỉ 3.10+). Đừng dùng.
3. edge-tts "No audio was received" đôi khi là transient / do câu test là hallucination STT (sine giả). Test riêng edge-tts thuần với câu tiếng Việt bình thường để cô lập.

### Test end-to-end WS
Gửi PCM float32 16k mono frame (sine amp 0.3 + silence 0.9s để flush) → nhận
`text` (normalize) → `thinking` → `answer` → `audio` url → `speaking` → gửi `{"interrupt":true}` → `interrupted`. Fetch `/tts/<hash>.mp3` verify MP3 header `ff\ f3`.

## Frontend (index.html)
- `setLiveState(state)` hiện 👂nghe/🤔nghĩ/⚙️làm/🗣️nói; `interruptTts()` pause audio + clear src; nút `sendInterrupt()` gửi `{"interrupt":true}` qua WS.
- Phát audio TTS bằng `new Audio(url)`, append `?t=Date.now()` tránh cache.
- `node --check` từng `<script>` block sau patch (file 3577 dòng dễ cúp).

## Xác nhận với user luôn test mic thật trước khi tiến Phase B (chưa dùng mic thật — tất cả test bằng sine giả).