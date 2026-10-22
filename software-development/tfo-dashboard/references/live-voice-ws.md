# TFO — Live Voice WS module (Tất cả tầng đã code + verify 07/09)

Ghi chú module "Nói chuyện trực tiếp" + Router/RAG + TTS swap trên TFO, đối chiếu
code thật trong `D:/Hermes Proj/ai-company/`. Đã code + verify từng hạng mục
trong phiên 07/09/2026.

## Files & nơi đứng code

| File | Vai trò |
|------|---------|
| `app/streaming.py` | `StreamSession` — VAD chunking server-side + **cổng tần số giọng người** (chống hallucinate). VAD_THRESHOLD 0.008, SPEECH_TAIL_MS 700, MAX_SPEECH_S 6.0, OVERLAP_S 1.0, MIN_SPEECH_FRAMES 4. |
| `app/main.py` | `@app.websocket("/ws/stream")` — loop nhận binary → `sess.feed(raw)`; JSON `{interrupt:true}` → `tm.cancel()`. `_answer_and_speak` wire router→rag/chat/execute. `@app.get("/tts/{h}.mp3")` sniff media type. |
| `app/tts.py` | `TTSProvider` interface + `EdgeTTSProvider` + **`VieNeuProvider`** (mặc định, giọng "Thanh Bình" via HTTP Mac) + `CachedTTSProvider` (LRU 64). `get_provider()` → VieNeu; `get_edge()` → fallback. |
| `app/router.py` | **Phase B (07/09)** — `classify(text)` → `chat|rag|execute`, rule-first 0đ, khỏi gọi LLM mọi câu. 12/12 test đúng. |
| `app/rag.py` | **Phase B (07/09)** — nguồn tasks.json/workspace.md/briefing.md/context_scan.json/users-meetings → chunk → keyword query → `answer(text)` LLM synthesize cite nguồn, fallback trung thực (không bịa). |
| `app/turn_manager.py` | `TurnManager` — `new_turn()`/`is_active(turn)`/`cancel()`. |
| `app/voice_lemma.py` | `normalize_vi(text)` — normalize tên riêng tiếng Việt. |

## Luồng khi anh nói (up → down)

**UP (mic → server):**
1. Trình duyệt `startLiveStream(stream)` (index.html, nút "Nói chuyện trực tiếp"): getUserMedia → AudioContext downmix mono + resample 16k float32 → frame 1600 sample → `liveWs.send(frame.buffer)`.
2. `streaming.py` VAD tích lũy giọng; im lặng 700ms → flush; >6s → flush sớm; <0.4s → bỏ.
3. **Cổng tần số** (`_speech_ratio`): FFT, năng lượng trong 300–3400Hz / tổng. `rms < 0.02` HOẶC ratio < 0.55 → bỏ, KHÔNG gửi Groq (loại hum 50/100Hz, gió, tạp âm → hết self-hallucinate khi im lặng).
4. `_groq_micro` → Groq Whisper STT (overlap 1s, browser headers chống CF 403, KHÔNG boost audio).
5. `_on_text` → `normalize_vi` → `{type:"text"}` realtime → `tm.new_turn()` → `_answer_and_speak`.

**DOWN (trả lời):**
6. `_answer_and_speak` (Phase B wire): `classify(text)` → 
   - `rag` → `rag.answer(text, top_k=5)` (LLM DeepSeek qua `hub.store.call_deepseek`, cite nguồn "(theo: <file>)"),
   - `execute` → trả "Tầng 3 đang trì hoãn",
   - `chat` → `call_deepseek` trả lời ngắn.
7. TTS: `synth_cached_async(reply)` — **VieNeuProvider mặc định**; nếu Mac lỗi → `except` → fallback `get_edge()`. Gửi `{answer}` + `{audio:url}` → `{state:speaking}`.
8. `/tts/<hash>.mp3` sniff: file bắt đầu `RIFF` → `audio/wav` (VieNeu), ngược lại `audio/mpeg` (edge). **PHẢI sniff — VieNeu trả WAV nhưng cache giữ đuôi .mp3.**

**NGẮT LỜI:** `{interrupt:true}` → `tm.cancel()` → `{interrupted}` → `listening`.

## Giọng "Thanh Bình" — VieNeu local trên Mac, TFO gọi HTTP

Chốt giọng 07/09: **Thanh Bình** (Nam·Bắc·kể chuyện, preset #13 VieNeu v3 Turbo).

- **Trên Mac (192.168.1.3):** micro HTTP server `~/tts_server.py` (port **8899**), chạy `~/vieneu-venv/bin/python /Users/tquang/tts_server.py`. Endpoint `GET /tts?text=<urlencoded>` → `tts.infer(text, voice="Thanh Bình")` → trả raw WAV. Deploy bằng paramiko (sftp ghi script, `pkill -f tts_server.py` rồi nohup).
- **Trên Windows (TFO):** `app/tts.py` `VieNeuProvider` — `httpx.AsyncClient.get("http://192.168.1.3:8899/tts?text=...", timeout=60)`, `_synth_async` PHẢI là `async def` (bên gọi `await`). Model init lần đầu ~20s (log "HF Hub warning" bình thường). Latency LAN ~2-4s/câu.
- **Fallback:** trong `_answer_and_speak` try VieNeu → except → `synth_cached_async(reply, provider=get_edge())`.
- **Verify:** curl trên Mac `-w 'HTTP:%{http_code} size:%{size_download}'` → 200 + wav ~84KB; test Windows qua `get_cached().synth_cached_async(...)` trả bytes RIFF. Phòng tách: Mac chết = VieNeu timeout 60s → edge fallback chờ 60s (đáng cân nhắc giảm timeout về ~8s).

## TÁCH NÚT — DONE 07/09 (commit ebdb4f5)

THỰC HIỆN XONG (không còn là plan):
- UI (index.html): thêm card **"Nói chuyện trực tiếp"** với nút `liveTalkBtn` (id liveTalkBtn, label "Bắt đầu nói chuyện" ↔ "Dừng nói chuyện") ở TRƯỚC card "Ghi âm / Upload cuộc họp".
- JS: block live-talk riêng — click start → `navigator.mediaDevices.getUserMedia({audio:true})` → `startLiveStream(stream)`; click stop → tắt track + `stopLiveStream()` + ẩn liveCard. Chặn nếu `isRecording` đang chạy (alert "dừng ghi xong rồi mới nói").
- Record handler: **BỎ** `startLiveStream(stream)` (dòng cũ L1025) và `stopLiveStream()` trong onstop — ghi âm meeting giờ KHÔNG kéo live theo → hết echo vòng lặp.
- `liveCard` ẩn mặc định (`style="display:none"`) — chỉ hiện khi bấm "Nói chuyện".
- Verify browser: playwright login passcode → đếm `#liveTalkBtn` + `#recordBtn`, check `src.includes("startLiveStream(stream); // H1")===false`, pageerror rỗng.

## Bản đồ HTML đã publish (07/09)

- `D:/Hermes Proj/tts_samples/tfo-live-voice-flow.html` (+png) — sequence luồng live voice: `https://preview.thefirstonly.com/godcqxsg52l9`.
- `D:/Hermes Proj/tts_samples/tfo-full-plan-3-tang.html` (+png) — toàn bộ plan 3 tầng (T1 voice/T2 router+RAG/T3 execution trì hoãn): `https://preview.thefirstonly.com/ygu5ajsj710x`.

## Pitfall kỹ thuật
- Groq KHÔNG có WS STT thật → "realtime" = VAD chunking, không skin được.
- Gọi Groq bằng requests/urllib PHẢI kèm browser headers (User-Agent/Origin/Referer) → thiếu = Cloudflare 403 code 1010.
- Không volume boost/lọc trước STT (hallucinate) — NHƯNG cổng tần số FFT (loại, không biến đổi) là ĐƯỢC và cần thiết.
- VieNeu `_synth_async` phải async (bug `TypeError: object bytes can't be used in 'await'`).
- `call_deepseek` đọc key từ env `OPENCODE_GO_API_KEY` — standalone test phải tự set key trước khi import app.rag.
- Keep-alive: Mac tts_server không auto-restart; sau khi Mac reboot phải nohup lại (`pkill -f` trước, két nohup sau).