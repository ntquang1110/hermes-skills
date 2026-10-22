# TFO MVP Web — Trợ lý CEO (FastAPI track)

TheFirstOnly product MVP: a CEO assistant web app. Lives in the SAME repo as the AI Company (`D:/Hermes Proj/ai-company/`) but is a separate product track. URL: `https://tfo.thefirstonly.com` (port 8100).

## Stack (locked by CTO agent + Quang)

- Backend: FastAPI + uvicorn, venv at `.venv` (MUST be Python 3.11 — see SKILL pitfalls)
- STT: Groq Whisper `whisper-large-v3` (API key in hermes `.env` as `GROQ_API_KEY`)
- Summarize/reasoning: DeepSeek via OpenCode endpoint (`OPENCODE_GO_API_KEY`), model `deepseek-v4-pro` for the "não" (reasoning) part
- Frontend: single `app/static/index.html` — premium B/W/Y theme, no framework
- Data: `tfo_data/` (uploads/, recordings/, tasks.json, meetings.json, sessions.json) — NOT the AI-company `store/`

## Files

```
app/main.py            # FastAPI app — all routes
app/static/index.html  # SPA (login overlay, record, tasks, meetings, skills, org chart)
app/tg_push.py         # Telegram push helper
```

## Auth (email + passcode — Quang's choice)

- `ALLOWED_EMAILS` list + one shared `PASSCODE` (default `<PASSCODE>`, override env `TFO_PASSCODE`)
- POST `/api/login` → token; `/api/me?token=` validates; `/api/logout`
- Tokens in `tfo_data/sessions.json`; frontend stores token in `localStorage` (`tfo_token`)
- Sensitive endpoints (`/api/transcribe`, `/api/summarize`) take `token: Form("")` and call `_check_token(token)` → 401 otherwise
- Frontend: `checkAuth()` on load; only call `initApp()` (loadTasks/loadMeetings/loadSkills) after auth OK
- Add pilot users by appending emails to `ALLOWED_EMAILS`

## Recording Resilient (Quang-mandated: no lost audio on network drop)

User requirement: bấm ghi → bấm End → lưu. NHƯNG nếu không bấm End mà mất mạng/session end → VẪN phải lưu bản ghi.

Flow:
1. POST `/api/record/start` → `session_id`, server creates `tfo_data/recordings/{sid}.webm`
2. Client `MediaRecorder.start(10000)` → `ondataavailable` fires every 10s → POST `/api/record/chunk` (session_id + audio blob) → server appends
3. POST `/api/record/end` → pops session → transcribe + save meeting + push Telegram
4. **Watchdog thread** (daemon, checks every 10s): any session with `last_seen > 30s` → auto-finalize (save file + transcript) so a dropped connection never loses audio

Test evidence pattern: create session, send 3 chunks, verify `parts` increments and file size grows; create a session WITHOUT end, wait 35s, verify `.webm` + `.transcript.txt` appear in `recordings/`.

## Meetings History

- GET `/api/meetings`, POST `/api/meetings`, GET `/api/meetings/{id}`
- On record end, meeting is saved automatically (session_id + transcript + created_at)
- Frontend: "Lịch sử cuộc họp" card, click "Xem" to open transcript in result box

## Groq chunking for meetings >16MB

Groq Whisper upload limit ~16MB. For long meetings:
1. Get duration via `ffmpeg -i file` stderr regex `Duration: HH:MM:SS`
2. Cut chunks of 600s (10 min) + 20s overlap using ffmpeg (`-ss start -t dur -ar 16000 -ac 1`)
3. Transcribe each chunk, join with `\n\n`
4. Fallback on 413: lower bitrate + smaller chunks + retry

## Telegram push (beFounders group)

- Token: `TELEGRAM_BOT_TOKEN` in `C:/Users/NTQUANG_DELL/AppData/Local/hermes/.env`
- Chat ID for beFounders group: `-1004368353156` (from `hermes/channel_directory.json` — read it, don't guess)
- `app/tg_push.py::send_meeting_result(meeting_id, summary, tasks, transcript_preview)` → `sendMessage` with `parse_mode: Markdown`
- Wired into `/api/summarize` — after DeepSeek summary, auto-push to Telegram (beFounders) so Quang sees results on his phone
- Verify: run script with test args → expect `✅ TG push: 200`; check the group chat for the message

## Deploy / run

```bash
cd /d/Hermes\ Proj/ai-company
.venv/Scripts/python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8100
# background=true, watch_patterns=["Application startup complete"]
```

Tunnel ingress already configured: `tfo.thefirstonly.com → localhost:8100` (see SKILL Cloudflare section — full ingress list on every PUT).
