# meTelligent — Design Critique Case Study

> Session: 2026-06-28 → 2026-06-30 | Full design doc: `meTelligent-design.md`
> Critique doc: `02-phan-bien-va-phan-tich.md`
> Android app: `android_app/`
> Roadmap: `04-roadmap-phase1.md`, `05-voice-feature-plan.md`

## Context

User wanted a "trợ lý ảo toàn diện" (comprehensive virtual assistant) with:
- Real-time speech recognition
- Conversation analysis + real-time critique
- Memory (facts, decisions, user profile)
- Task auto-extraction from conversations
- Web dashboard + CLI
- **Android app** (added later) with notification + background service

---

## Phase 0 — Design Critique (2026-06-28)

### What Went Wrong (first attempt)

Jumped straight to **coding** — created 8 module files with actual Python code,
SQLAlchemy models, CLI commands etc.

User stopped and said: **"Đừng code trước — thu thập thông tin dự án và phản
biện trước để sắc nét những việc cần làm"** (Don't code first — collect project
info and critique first to sharpen what needs to be done).

### What We Did After (the right way)

**Critique found these issues:**

| Issue | Severity | Fix |
|-------|----------|-----|
| Linear pipeline = 5-7s latency | 🔴 Critical | Event bus + thread pool |
| Critique 100% regex = shallow | 🔴 Critical | Rule + LLM hybrid |
| PyAudio blocking on Windows | 🟡 Important | sounddevice (async) |
| spaCy vi model accuracy low | 🟡 Important | Underthesea hybrid |
| SQLAlchemy too heavy for SQLite | 🟡 Important | aiosqlite |
| No speaker diarization | 🟡 Important | WhisperX (P2) |
| No LLM integration | 🟡 Important | Add optional LLM layer |
| No notification system | 💡 Gap | Defer to P2 |
| No auth/security | 💡 Gap | API key (P1) |
| Dependency order was wrong | 🔴 Critical | Reverse the build order |

**Dependency map:**
```
Audio Capture → STT → Analyzer → Critique → Memory → Tasks
                ↑        ↑          ↑
           (needs   (needs    (needs
            audio)   text)     memory)
```

**Priorities:**
| Phase | Focus | Components |
|-------|-------|------------|
| P0 | Foundation | Data models, Audio capture, STT, Memory store |
| P1 | Core value | Analyzer, Critique, Tasks, CLI, API |
| P2 | Polish | Profile, Dashboard, Diarization |
| P3 | Future | Telegram, TTS, Plugins |

---

## Phase 1 — Android App & Integration (2026-06-30)

### Tech Stack Decision

| Layer | Chosen | Why |
|-------|--------|-----|
| Mobile | **Flutter** | Code nhanh, APK nhẹ (~10MB), hot reload, notification + background support native |
| Server | **FastAPI** + Python | Async, easy to build, already has faster-whisper |
| STT | **faster-whisper** (model `medium`) | Local, free, đã download sẵn |
| Tunnel | **localtunnel** (`npx.cmd`) | Free, không cần đăng ký, hoạt động trên Windows git-bash |

### Android App Structure

```
android_app/
├── lib/
│   ├── main.dart                          # Entry point + dark theme
│   ├── screens/
│   │   ├── home_screen.dart               # Dashboard: kết nối server, quick actions
│   │   ├── settings_screen.dart           # Cấu hình server URL
│   │   ├── voice_screen.dart              # 🆕 Ghi âm + gửi lên server (Phase 2)
│   │   └── result_screen.dart             # 🆕 Hiển thị summary + tasks (Phase 2)
│   └── services/
│       ├── server_service.dart            # HTTP + WebSocket singleton
│       ├── notification_service.dart       # Push notification Android
│       ├── audio_service.dart             # 🆕 Ghi âm microphone (Phase 2)
│       └── simple_storage.dart            # File-based storage thay shared_preferences
```

### Windows Flutter Build — Known Issues & Fixes

**Problem:** Gradle 9.1.0 + Kotlin incremental compilation cache corruption
```
Storage for [...].tab is already registered
```

**Root cause:** `shared_preferences_android` plugin's Kotlin code conflicts with incremental cache on Windows when Gradle daemon reuses caches across failed builds.

**Fix sequence (verified working):**
1. Remove `shared_preferences` → use `simple_storage.dart` (file-based JSON)
2. Add `coreLibraryDesugaring` to `build.gradle.kts` for `flutter_local_notifications`
3. Always `flutter clean` before retry after a failure
4. Prefer **fresh `flutter create`** → copy code in → one-shot build, rather than retrying in a dirty build directory
5. If Kotlin daemon caches are corrupted: kill all Java processes + delete `.gradle/caches/`

**Dependencies that work with Flutter 3.44.4 on Windows:**
- ✅ `http` (pure Dart)
- ✅ `web_socket_channel` (pure Dart)
- ✅ `flutter_local_notifications` (needs desugaring)
- ✅ `google_fonts` (pure Dart)
- ❌ `shared_preferences` (Kotlin cache issue)
- ❌ `workmanager` (Kotlin compile error, unresolved references)
- ❌ `flutter_background_service` (Gradle CMake issue)
- ❌ `webview_flutter` (Kotlin cache issue, needs isolation)

### External Integrations

#### Understand-Anything (⭐69k)
Knowledge graph tool. Integrated as Hermes Agent skill:
```bash
# Clone → Install for Hermes → Copy to Windows Hermes skills dir
git clone https://github.com/Egonex-AI/Understand-Anything.git
bash install.sh hermes
cp -r ~/.hermes/skills/understand-anything ~/AppData/Local/hermes/skills/understand-anything
```
**7 skills added:** `understand`, `understand-chat`, `understand-dashboard`, `understand-diff`, `understand-domain`, `understand-explain`, `understand-knowledge`

⚠️ **Windows path difference:** Install script links to `~/.hermes/skills/` but Hermes on Windows reads from `~/AppData/Local/hermes/skills/`. Must copy manually.

#### Harness Engineering (⭐9k)
Applied `harness-creator` to meTelligent project:
```bash
cd learn-harness-engineering
node skills/harness-creator/scripts/create-harness.mjs --target /path/to/meTelligent --agent-file AGENTS.md
```
**Generated:** `AGENTS.md`, `feature_list.json`, `progress.md`, `session-handoff.md`, `init.sh`

### Public Access Setup

**Preferred tunnel for Windows git-bash:**
```bash
npx.cmd localtunnel --port 8080
# → URL: https://random-words.loca.lt
```

**Why `npx.cmd` not `npx`:** In MSYS2/git-bash, `npx` can hang; `npx.cmd` forces Windows cmd resolution and works.

**Alternatives tried and issues:**
- `lhr tunnel` — needed token, not installed
- `cloudflared tunnel` — zero output on Windows git-bash
- `serveo.net` (SSH) — zero output on Windows git-bash
- `ngrok` — not tested (could work if installed)

### Voice Feature Roadmap (Phase 2)

```
📱 Android ghi âm → POST audio → 💻 Server Whisper STT
→ Summarize (Groq API) → Extract tasks → SQLite
→ 📱 Android hiển thị kết quả + Notification
```

**Server modules to build:**
- `server/main.py` — FastAPI + uvicorn
- `server/stt/whisper_stt.py` — faster-whisper medium
- `server/nlp/summarizer.py` — Groq API summarize
- `server/nlp/task_extractor.py` — Groq API extract tasks
- `server/memory/store.py` — SQLite storage

**Android additions:**
- `voice_screen.dart` — ghi âm + gửi audio
- `result_screen.dart` — hiển thị summary + tasks
- `audio_service.dart` — record package integration

---

## Key Takeaways

1. **Never code before critique** — even a simple 5-minute review saves hours of rework
2. **Rule-based NLP is fragile** for real-world Vietnamese — plan for hybrid with LLM
3. **Whisper latency is the bottleneck** — need thread pool + interim results for "real-time"
4. **Dependencies are never what they seem** — map them explicitly before prioritizing
5. **Flutter on Windows + Gradle 9.x has Kotlin cache issues** — use minimal deps, clean builds, avoid `shared_preferences`
6. **Hermes Agent on Windows uses different paths** than install scripts assume (`AppData/Local/` vs `~/.hermes/`)
7. **Tunnel tools behave differently on Windows git-bash** — prefer `npx.cmd localtunnel` when others fail
8. **When APK build fails, create a fresh `flutter create` project first** — verify minimal build works before adding custom code
