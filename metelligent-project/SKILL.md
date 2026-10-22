---
name: metelligent-project
description: "meTelligent — trợ lý ảo ghi âm → STT → Summarize → Task trên Android + FastAPI backend. Server port 8766, tunnel metelligent-123.loca.lt. Tích hợp Notion tasks + Google Sheets/Drive."
---

# meTelligent Project Skill

Dùng skill này khi làm việc với dự án meTelligent.

## Quick Start

```bash
# Server
cd /d/Hermes\ Proj/meTelligent/server
source venv/Scripts/activate
python -c "
import os, base64
os.environ['NOTION_API_KEY'] = base64.b64decode('bnRuXzY0MDA5MTY4Njk4OWR4YzJ4Z0szMk96RHJpQnVHQmVCcFpxRkJmU2I0OHc1Wkk=').decode()
import uvicorn
uvicorn.run('metelligent:app', host='0.0.0.0', port=8766, reload=False)
"

# Health check
curl http://localhost:8766/api/health
```

## Meeting Recording Module (added Jul 2026)

### Architecture: Chunk-based recording

```
Phone: [Record] → Chunk 20s → Temp storage → Upload (retry×3) → Server
Server: Chunk Receiver → Aggregator → VAD → Whisper → Groq Correct → Daily Storage
```

### Dictation+ (2-in-1) — added Aug 2026

1 luồng mic duy nhất → vừa dictation live vừa lưu audio gốc (kiểu Flow high mode):

```
Mic → AudioRecorder.startStream(pcm16bits, 16kHz, mono) → Stream<Uint8List>
        ├──→ gom 5s (160000 bytes) → wrap WAV header → POST /chunk-live
        │        → server VAD (webrtcvad) bỏ silence → faster-whisper → {text, speech}
        └──→ server lưu chunk .wav → end meeting: concat full audio → re-transcribe
```

- **Live = nháp, cuối = chuẩn**: transcript live chỉ hiển thị; khi end meeting server transcribe LẠI từ full audio nối đủ → Whisper có đủ context → bản chính thức thay nháp. Giải quyết hallucination trên audio rè.
- **STT chính = Groq Whisper API (whisper-large-v3-turbo) — KHÔNG dùng faster-whisper local cho live**: CPU i7-4910MQ (2014) quá yếu — local medium mất 18s/5s audio → không real-time → "nói không thấy text". Groq: ~1s/chunk, quota 2000 requests/ngày. Local faster-whisper chỉ là FALLBACK khi Groq lỗi.
- **STT engine layer PLUGGABLE (chốt 02/09, đừng khóa cứng Groq)**: `WhisperSTT.transcribe_engine()` chọn engine theo env `STT_ENGINE` (groq|local|auto, mặc định `groq`) + param `engine` per-call/per-device. `local` → chỉ dùng faster-whisper local, KHÔNG gọi Groq (offline/chi phí/riêng tư). Endpoint `/chunk-live` nhận form field `engine` override (rỗng → dùng env). VAD chunking pattern nằm ở router, KHÔNG phụ thuộc engine — đổi engine không đụng tầng chunk. Unit test 8 case PASS (mặc định/force env/per-call override/groq fallback).
- **Cloudflare chặn urllib (error 1010)**: Groq API phải gửi kèm `User-Agent` giống browser (Chrome/126...), nếu không 403.
- **Server chạy DETACHED (subprocess DETACHED_PROCESS)**: không chạy qua Hermes background — Hermes kill process khi session/turn gián đoạn → server exit 1 (đã chứng minh nhiều lần). Dùng `subprocess.Popen(creationflags=DETACHED|CREATE_NEW_PROCESS_GROUP|CREATE_NO_WINDOW)`.
- **KHÔNG warm-up model local lúc startup**: tốn 25s + 1GB RAM, vô dụng vì STT chính là Groq. Server start trong 2s, chỉ ~80MB RAM.
- **Quota context summary**: Groq llama-3.3-70b: 1K RPD/12K TPM — 3 tiếng họp ≈ 400 calls, OK. Cộng whisper 2000 RPD riêng.
- **Endpoints mới**: `POST /api/meeting/chunk-live` (VAD+transcribe), `POST /api/meeting/context` (Groq → {title, context, decisions}), `end-json` nâng cấp trả thêm `summary` {title, context, decisions, tasks, difficulties}.
- **App popup**: khi bật ghi âm → popup "Đang ghi" + 3 ô live (Tiêu đề/Bối cảnh/Quyết định) refresh qua StatefulBuilder + `_refreshLivePopup()`; cuối họp → popup commit-ready + nút Confirm.
- **Groq JSON prompt pitfall**: KHÔNG dùng `.format(tags=...)` cho prompt có JSON braces — `.format()` nuốt `{...}` → KeyError. Dùng `.replace("{tags}", ...)`.
- **VAD**: `webrtcvad-wheels` (pip cài được trên Windows), frame 20ms, **quét TOÀN BỘ chunk** (≥5% frames speech) — KHÔNG chỉ 1s đầu (người bấm mic rồi mới nói → 1s đầu luôn silence). Mode 1 (ít aggressive hơn mode 2). Silence → trả `{text:"", speech:false}` không đốt whisper.
- **chunkBytes(rate) = rate * 5 (SỐ MẪU, không phải bytes)**: pcmBuffer là Float32 array — công thức `rate*2*5` tạo ngưỡng 10s → không có chunk nào được gửi khi nói <10s.
- **Whisper hallucination "Hãy đăng ký kênh..."**: audio yếu (RMS<0.08) → Whisper bịa câu quảng cáo. Chống 3 lớp: (1) normalize gain nếu RMS<0.05, (2) initial_prompt "biên bản họp, không quảng cáo", (3) filter text ads-pattern trên audio RMS thấp → trả rỗng.

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/meeting/start` | Tạo meeting (Form data) |
| POST | `/api/meeting/start-json` | Tạo meeting (JSON body — **ưu tiên dùng cho app**) |
| POST | `/api/meeting/chunk` | Upload 1 chunk (multipart) |
| POST | `/api/meeting/chunk-live` | Upload 5s WAV → VAD → transcribe live → `{text, speech}` |
| POST | `/api/meeting/context` | Text tích lũy → `{title, context, decisions[]}` (Groq live) |
| POST | `/api/meeting/end` | End meeting (Form data) |
| POST | `/api/meeting/end-json` | End meeting (JSON — trả thêm `summary` commit-ready) |
| POST | `/api/meeting/quick` | Quick note: 1 file → text |
| GET | `/api/meeting/{id}` | Chi tiết 1 meeting |
| GET | `/api/meeting/daily/{date}` | DS meeting trong ngày |
| GET | `/api/meeting/daily-summary` | Group by date |

### Route Ordering (CRITICAL)

**`daily-summary` và `daily/{date}` PHẢI được đặt TRƯỚC `/{meeting_id}`** trong router.py. Nếu không, `daily-summary` bị coi là meeting_id → 404.

### Pipeline

```
chunks → concat (sox→ffmpeg→binary) → Whisper small → Groq LLM correct → lưu DB
```

### Groq Auto-correct Prompt

```
System: Bạn là trợ lý sửa lỗi chính tả tiếng Việt.
Sửa lỗi chính tả, dấu câu, viết hoa đầu câu cho transcript sau.
Ngữ cảnh: {tags}
Chỉ trả về text đã sửa, không giải thích.
```

### DB Schema

SQLite tại `data/meetings.db`:

```sql
meetings (id, title, date, tags, status, full_transcript, corrected_text, created_at, updated_at)
chunks   (id, meeting_id, chunk_index, file_path, status, transcript, duration, created_at)
```

## Tunnel

### Loca.lt (localtunnel)

```bash
npx localtunnel --port 8767 --subdomain metelligent-123
npx localtunnel --port 8766 --subdomain metelligent-123

- URL hiện tại: `https://metelligent-123.loca.lt`
- Output URL ghi vào stderr → redirect: `npx localtunnel --port 8766 2>&1 | tee url.txt`
- Loca.lt thường bị chặn trên mạng di động VN → dùng Cloudflare Tunnel thay thế

### Cloudflare Tunnel (ưu tiên cho VN)

```bash
# 1. Tắt WARP tạm thời (WARP gây conflict QUIC/HTTP2)
warp-cli disconnect

# 2. Start tunnel
cloudflared tunnel --url http://localhost:8767 --protocol http2

# 3. Copy URL dạng: https://xxx-yyy-zzz.trycloudflare.com
# 4. Có thể bật lại WARP (tunnel sẽ mất kết nối sau vài phút)

# Kill zombie cloudflared processes
taskkill //F //PID <pid>   # Windows: dùng taskkill, kill/bash không hiệu quả
cmd.exe /c "wmic process where 'name like \"%%cloudflared%%\"' call terminate"
```

- **Lưu ý:** cloudflared + WARP conflict trên Windows. Phải tắt WARP khi start tunnel.
- `trycloudflare.com` không bị chặn ở VN vì qua Cloudflare CDN.
- URL random mỗi lần chạy — không có subdomain cố định.

## Whisper STT

- Model: `faster-whisper` (medium → small cho speed)
- **Quan trọng:** Luôn dùng `compute_type = "int8"` trên Windows CPU. `float16` không được support → crash.
- File: `metelligent/stt/whisper_stt.py` — line compute_type
- Language mặc định: `vi`

## Android App

### APK Build

- APK sẵn có tại: `/d/Hermes Proj/meTelligent/meTelligent-android.apk` (49MB, built 30/06)
- **KHÔNG download lại Flutter SDK** nếu APK đã có — kiểm tra file tồn tại trước
- Nếu cần build lại:
  1. **Flutter SDK:** `git clone --depth 1 --branch stable https://github.com/flutter/flutter.git /c/flutter` (nhanh hơn zip, resume được)
  2. **JDK 17:** Download Temurin từ GitHub releases → giải nén vào `/c/java/`
  3. `export JAVA_HOME="/c/java/jdk-17.0.12+7" && export PATH="$JAVA_HOME/bin:$PATH"`
  4. `flutter clean && flutter pub get && flutter build apk --debug`
- **Gradle file lock error:** Kill Java trước: `taskkill //F //IM java.exe` → `flutter clean` → build lại
- Lần build đầu luôn chậm (~3-5 phút) vì download Gradle + compile

### Critical Flutter Fixes

- **Storage không lưu được URL:** `simple_storage.dart` dùng hardcoded path `/data/data/...` — không hoạt động trên Android 11+. Fix: dùng `shared_preferences` package thay thế. Thêm dependency vào `pubspec.yaml`: `shared_preferences: ^2.3.0`. Import `package:shared_preferences/shared_preferences.dart`, dùng `SharedPreferences.getInstance()` thay vì file I/O.
- **record package API:** Trong version 6.x, `path` là named parameter của `start()`, KHÔNG phải field trong `RecordConfig`. Source: `await _recorder.start(RecordConfig(...), path: path)`.
- **Dart compile errors:** Kiểm tra với `flutter analyze` trước khi build. Fix lỗi phổ biến: `$tags` → `${meeting.tags}` (thiếu receiver).

### Server URL trong app

- File: `android_app_new/lib/services/server_service.dart`
- URL mặc định: `https://metelligent-123.loca.lt`
- `_isLocalhost()` filter: tự động bỏ qua URL `localhost`, `10.0.2.2`, `127.0.0.1` khi init
- User có thể thay đổi URL trong Settings → Lưu

### Flutter Files

| File | Chức năng |
|------|-----------|
| `models/meeting.dart` | Model Meeting + DailySummary |
| `services/meeting_service.dart` | API calls (start-json, chunk, end-json, quick) |
| `services/server_service.dart` | Server connection + URL management |
| `screens/meeting_screen.dart` | Meeting recording UI (chunk, toggle, live transcript) |
| `screens/home_screen.dart` | Dashboard + Meeting tab |

## Google Integration

meTelligent có thể dùng Google Sheets/Drive để lưu dữ liệu:

| Tài khoản | Token file | Use case |
|-----------|-----------|----------|
| 📧 <EMAIL> | `google_token_gmail.json` | Cá nhân |
| 🏢 <EMAIL> | `google_token_kiemsaphia.json` | Dự án |

**Vị trí token:** `C:\Users\NTQUANG_DELL\AppData\Local\hermes\google_token.json`
**Đổi account:** copy file `google_token_{account}.json` → `google_token.json`
**Mặc định:** Gmail

## Config

- Notion key: base64 trong `run.py` | API: 2022-06-28
- Tasks DB: `3e1ee...a7ec7b` | Memories DB: `195ee...a1036b`
- Github: `ntquang1110/meTelligent`
- Groq API key: có sẵn trong env (cả GROQ_API_KEY và GROQ_API_KEY_B64)

## Pitfalls

- **⚠️ TUYỆT ĐỐI KHÔNG boost/lọc trước khi transcribe (quan trọng nhất, chứng minh 27/08):** bước `-af volume=12dB,highpass=f=80,lowpass=f=8000` + ép opus **làm méo audio → Whisper hallucinate khủng khiếp → transcript vô nghĩa** trên file hơi ồn. Bằng chứng: cùng 90s — boost/filter → "đăng ký kênh/Là La La School" rác; raw → "giá liêm yết 180, gồm VAT" thật. Hậu quả: transcript 12,998 từ mất xuống 2,200 (mất ~6x) + toàn bịa. **Chỉ nén Opus 16kHz mono sạch (`-ar 16000 -ac 1 -c:a libopus -b:a 48k`), KHÔNG af filter/boost.**
- **Groq whisper RƠI nội dung trên chunk dài (quan trọng, chứng minh 27/08):** file họp dài cắt chunk 10 phút → Groq whisper chỉ giữ ~½ (đo: span 2850-3450s, 1 chunk 10p=273 từ, chia 4×2.5p=563 từ = 2x). **Chunk long-meeting transcribe tối đa ~2.5 phút (150s) + overlap 15s.** Whisper còn hallucination "đăng ký kênh/subscribe/bài hát/lalaschool" trên audio êm → clean PHẢI per-chunk theo CỤM ad (giữ câu thật), KHÔNG drop cả câu ở global (mất 80% nội dung họp). Mô hình fix chuẩn ở `ai-company/app/main.py::_transcribe_chunked` + `_strip_ads` (commit 28575f3 + d31f179).
- **Đừng để regex toàn optional** (mọi nhóm `(?:...)?`): khớp chuỗi rỗng ở mọi vị trí → chèn space giữa từng ký tự, làm hỏng cả câu thật.
- **requests.post trong STT phải try/except** bọc lỗi mạng/timeout → trả sentinel, đừng để `r` undefined gây NameError làm chết cả pipeline.
- **Port conflict:** Kiểm tra port trước khi start. `netstat -ano | grep ":8766" | grep LISTEN`
- **Port 8765 bị chiếm bởi process lạ** trên máy này — không kill được. Luôn dùng 8766.
- **Kill process trên Windows:** Dùng `taskkill //F //PID` — kill/bash không hiệu quả với Windows native processes
- **WARP conflict:** WARP + cloudflared không chạy cùng lúc. WARP + localtunnel OK.
- **Route ordering:** Specific routes trước, param route `/{id}` CUỐI CÙNG
- **JSON vs Form:** App Flutter gửi JSON, endpoints `*-json` nhận body dict. Endpoints `start`, `end` dùng Form data.
- **APK build:** Kiểm tra APK cũ trước. Chỉ build lại nếu cần thiết — Flutter SDK ~1GB, Android SDK ~2GB.
- **Subdomain tunnel:** Nếu subdomain đã được claim, localtunnel trả URL khác. Kiểm tra URL thực tế.
- **Static file serving:** Thêm route FastAPI serve file HTML:
  ```python
  from fastapi.responses import HTMLResponse
  _PATH = Path(__file__).resolve().parent.parent.parent / "file.html"
  @app.get("/route", response_class=HTMLResponse)
  async def handler():
      return HTMLResponse(content=_PATH.read_text(encoding="utf-8"))
  ```
