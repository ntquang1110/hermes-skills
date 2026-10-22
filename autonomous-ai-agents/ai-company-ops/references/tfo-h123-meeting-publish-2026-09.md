# TFO: meeting-publish + H1/H2/H3 (03/09) — chi tiết kỹ thuật

Bổ sung cho section "TFO MVP Web" trong SKILL.md. SKILL.md đã ở trần kích thước
(~100k) nên chi tiết dồn vào đây.

## ✅ Meeting SHARE phải ra trang MEETING 2 tab, KHÔNG chỉ transcript trần

Tín hiệu (Quang): "em chưa áp dụng skill meeting-sum, trang chỉ có transcript".
Không nói "đã xử lý rồi" khi check thấy link preview — bug nằm ở `_publish_preview`.

- Cũ: `_publish_preview(transcript, title)` chỉ đóng `f"<pre>{safe}</pre>"` → 1 tab trần.
- Mới: `_publish_preview(transcript, title, summary="")` parse summary JSON
  `{summary, issues, decisions, tasks}` → trang 2 tab B/W/Y:
  - Tab "Tổng quan": Bối cảnh / Chỉ số (KPI cards) / Vấn đề & Blockers / Quyết định /
    Action Items (bảng Việc/ Người/ Hạn).
  - Tab "Transcript": full text `white-space:pre-wrap`.
  - `switchTab(n)` dùng `b.dataset.tab` — tránh lỗi f-string nháy kép (pitfall cũ).
- Republish trang cũ sau khi đổi code: xóa `preview_url=""` trong meetings.json rồi
  gọi lại `/api/meetings/share` → build mới. (Meeting có preview_url cũ → share bỏ qua.)
- Summary lưu dạng double-encoded JSON string trong meetings.json field `summary`.
- Verify bằng browser thật (không chỉ curl): `switchTab('transcript')` chuyển pane,
  transcript đầy đủ. Curl chỉ check HTTP 200 + có chuỗi — chưa đủ.
- Commit tham chiếu: `df0606d`.

## ✅ H1 Streaming Realtime — WS /ws/stream (nền cho Gemini Live)

Files:
- `app/streaming.py` (mới): `StreamSession`, VAD server-side.
- `app/main.py`: `@app.websocket("/ws/stream")`, `_groq_micro(pcm_bytes)`.

`StreamSession`:
- `FRAME_SAMPLES = 1600`, `FRAME_BYTES = 6400` (frame 100ms float32 mono 16kHz).
- `feed(raw)` lặp qua MỌI frame trong message (nếu 1 message chứa nhiều frame) —
  PITFALL: phiên bản đầu chỉ xử lý frame đầu → không flush khi client gửi cả cụm.
- `_feed_frame`: RMS >= `VAD_THRESHOLD`(0.008) → speech_mode, tích lũy; im lặng →
  `_hang` đếm tới 700ms thì flush; vượt 6s chủ động flush (realtime).
- Quá ngắn (< 0.4s giọng) → bỏ (nhiễu). Im lặng nền không speech_mode → drop.
- Overlap 1s: nối `self.overlap` (1s cuối đoạn trước) vào đoạn mới — không cắt mất
  cuối từ. Đoạn đầu (seg==1) không overlap.
- **PITFALL float slice index:** `OVERLAP_S * FRAME_SAMPLES` = float 1600.0 →
  `pcm[-s*4:]` lỗi "slice indices must be integers or None" → ép `int(OVERLAP_S*FRAME_SAMPLES)`.
- `_TASK_HINT` regex detect đề xuất task/việc/deadline/ngày từ text realtime.

`_groq_micro(pcm_bytes)`:
- float32 PCM → int16 (`array.array('h', ...)`) → WAV 16kHz mono → Groq transcribe.
- **Bắt buộc browser headers** `User-Agent`+`Origin: https://console.groq.com`+
  `Referer` chống Cloudflare 403 code 1010 (call bằng requests).
- Prompt INITIAL ngắn (`"Cuộc họp nội bộ."`) — prompt dài làm Whisper hallucinate lặp.
- `_strip_ads(text)` dọn như pipeline cũ.
- **Groq KHÔNG có WS STT streaming thật** — "realtime" phải VAD chunking, không skin.

Frontend (index.html):
- `startLiveStream(stream)` / `stopLiveStream()` gắn vào recordBtn.
- `AudioContext` + `createScriptProcessor(1024,1,1)`: downmix stereo→mono + resample
  48k→16k tuyến tính, gửi frame 1600 sample / 100ms qua WS.
- Live card hiện text realtime + task hint (ẩn khi chưa ghi).
- JS verify bắt buộc: extract từng `<script>` block + `node --check`.

Verify H1: unit VAD (flush/im lặng/nhiễu), WS thật gửi sine PCM → Groq trả text,
disconnect không crash, 7/7 node --check, login browser.
Commit: `b00103e` (backend), `5cea701` (frontend).

## H2 Context-scan chủ động

- `hub/context_scan.py`: proposals → JSON action `{noi_dung, ly_do, owner_de_duat, effort}`
  (`_normalize_proposals`, fallback giữ text). Commit `07929fc`.
- `hub/store.py::sync_context_scan_to_tasks()`: proposal → task draft
  planning/kanban/tag "context-scan", `scan_key=sha256(noi_dung)` dedup. Direct write,
  KHÔNG qua worker. Commit `0c910b9`. Push TG top 3 + HTML parse: `dd0c269`.
- Approve: `POST /api/context-scan/{id}/approve` (main.py, token Form, admin-only) +
  `POST /api/approve/context-scan` (server.py 8090, cookie auth). planning→approved +
  auto done_criteria. Nút `✓ Chốt` dashboard/index.html. Commit `a0bb160`.
- **PITFALL server.py 8090 chỉ đọc JSON body** → frontend gửi form-urlencoded bị
  "thiếu task_id" 400. Fix: parse `Content-Type: form` bằng `urllib.parse.parse_qsl`.
  Sửa server.py phải restart 8090 thủ công (http.server không auto-reload).
- **PITFALL draft context-scan trùng lặp:** LLM tái từ text gần giống khác sha256 →
  nhiều task gần-nhau (#35/#40 Đồng Nai, #36/#39 tiêu chảy, #37/#41 Excel). Đóng lô theo
  lệnh Quang: ghi trực tiếp store/tasks.json phase=completed + close_note, KHÔNG commit
  (store/ gitignored).

## H3 Reliability

- `hub/watchdog_8100.py`: ping /api/health (timeout 8s), fail → taskkill port + launch
  tfo_launch.py detached → chờ health. Verify: kill server → tự dậy 1.6s. Silent khi ok.
- `hub/backup_tfo.py`: snapshot `D:/Hermes/backups/tfo/<ts>/` (store+tfo_data), giữ 10,
  xóa cũ, restore test MD5. Chỉ Ổ D.
- `hub/uptime_probe_8100.py`: down ≥2 → TG beFounders beep, HTML+escape, no-spam
  transition-based (state file). VERIFY đủ UP→down→recover.
- Cron đăng ký: watchdog-8100 (1m), uptime-probe (5m), backup (3am). Xác nhận qua
  `cronjob action=list` last_status=ok.
- **PITFALL bash:** `taskkill /PID X //F` bị MSYS biến `//F` → dùng `taskkill /PID X /F`.
- script default = 1 lượt bounded (cron no_agent, stdio rỗng=silent); daemon nền `--loop`.

## Hướng Gemini Live (3 tầng) — đang triển khai plan (03/09)

Khung plan: `D:/Hermes Proj/.hermes-state/voice-live-plan.md`. Team BA/SA/CTO/Dev mỗi
người viết `plan-contrib-<role>.md` trong .hermes-state. 3 tầng:
1. Voice realtime 2 chiều (nền WS `/ws/stream`, thêm TTS playback + interrupt).
2. Router 3 loại câu (chat/rag/execute) + RAG tri thức (embed local fastembed/BGE →
   SQLite+vector; nguồn store/tasks + meetings + workspace + context_scan).
3. Thực thi agentic: SubAgent nền (delegate_task), không block, human-in-the-loop.
Không code trước khi Quang duyệt plan.