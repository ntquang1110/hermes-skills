---
name: ai-company-ops
description: Vận hành AI Company — hệ thống multi-agent (13 agents + Hermes + OpenClaw) tại D:/Hermes Proj/ai-company. Workflow bắt buộc plan→review→approve→implement→test, giao tiếp qua Git shared inbox, dashboard company.thefirstonly.com (passcode <PASSCODE>).
---

# AI Company Ops

Hệ thống công ty AI của Quang: **13 agents** (PO, PM, SA, CTO, Dev1, Dev2, QA, CMO, Content, Social, COO, CFO, Design) + Hermes (Back) + OpenClaw (Front) làm việc trên cùng repo `github.com/ntquang1110/ai-company`.

## Org chart mới (anh Quang chốt 2026-08)

```
👑 Quang
└── 🛡 CTO
    ├── 📦 PO — Product Owner: backlog, ưu tiên feature, định nghĩa product
    ├── 📅 PM — Project Manager: điều phối task, deadline, tiến độ
    ├── 🏗 SA — System Architect: kiến trúc, data flow
    ├── Senior Dev1 / Senior Dev2 — implement core
    └── Senior Tester (QA) — verify, test trước khi ship
```

- **+3 agents mới:** PO, PM, SA — profiles.json + AGENT_SYSTEM_PROMPTS + store.py `get_agent_statuses()` đều phải thêm (tổng 13).
- Dev1/Dev2 role → "Senior Dev", QA → "Senior Tester".
- **CMO = Chiến lược gia GTM** — định hướng product + GTM strategy, STEALTH (chưa publish).
- Content/Social/COO/CFO/Design: GIỮ NHƯNG IDLE — chờ GTM (hiển thị mờ + "* Idle — chờ GTM" trên org chart UI).
- `store/org.json` structure = "hierarchical" (trước là flat) — cập nhật khi đổi cấu trúc.

## Reference files
- `references/vision-status-check.md` — protocol check vision (6 nguồn: features/tasks/git/state/plan/services)
- `references/standup-credit-outage-*.md` — hết credit + fix briefing (sed URL) + prolonged 11d (models 200≠credit, MissingSessionID vs funds, call_deepseek list)

**Reference files chi tiết (tách từ SKILL.md 19/10/2026 — nội dung nguyên văn):**
- `references/tfo-mvp-web-2026-08.md` — TFO MVP web: restart 8100, login server-side, recording resilient, Groq/chunking/volume boost, diagnose, clean transcript, push TG, audio local + retry
- `references/tfo-task-thread-agent-tab-2026-08.md` — Tab Agent + task-thread + worker context + mode=agent/kanban + LLM domain routing (regex-first)
- `references/tfo-ui-taskboard-and-features-2026-08.md` — Calendar + Multi-tenancy + Task Board popup + Feature Tracker/SPIN/paused/đóng task theo quyết định Quang
- `references/tfo-face-login-mediapipe-2026-08.md` — Face login MediaPipe (embedding, auto-login 1:N, enroll, pitfall deps venv)
- `references/tfo-meeting-pipeline-flow.md` — Pipeline meeting + test không cần meeting thật + pitfall `/api/summarize`
- `references/hermes-openclaw-inbox-protocol.md` — Inbox Protocol v3 (ACK, spam/loop, watchdog silent, verify 2 chiều)
- `references/inbox-git-tracking-and-meeting-note-json.md` — Inbox files phải tracked + meeting note JSON stabilizer
- `references/context-scan-build-2026-09.md` — Context Scan build (2026-08-28) + H2 context-scan chủ động (C1-C4)
- `references/silent-cron-and-verifier-patterns.md` — Silent cron + cron mode + kỷ luật verify/mutation test
- `references/standup-runbook-full-2026-08.md` — Standup runbook: 4 nguồn bằng chứng, 4 pattern lặp, Standup None, chẩn đoán cron
- `references/streaming-realtime-stt-2026-09.md` — Streaming realtime STT (spike) + pitfall Groq 403 code 1010
- `references/llm-provider-opencode-deepseek.md` — DeepSeek qua OpenCode: endpoint/key/models/pricing/fallback

## CEO Operating Plan — khi Quang yêu cầu "plan để run company as ceo" (08/09/2026)

Build plan vận hành CEO, KHÔNG code. Data thật TRƯỚC khi viết: state `D:/Hermes Proj/.hermes-state/ai-company.md`, `shared/workspace.md`, `shared/launch_plan.md` (phase gates), `store/goals.json`, `store/tasks.json` (đếm completed/paused/planning/in_progress).

Cấu trúc chuẩn: CEO 5 việc (chốt mục tiêu / duyệt task / test thật / mở-đóng cổng / quyết hạ tầng) → nhịp tự động dạng bảng → decision flow + quy tắc cứng → KPI Mission Control 3 card → hiện trạng + bảng "quyết định cần anh chốt NGAY" kèm ước lượng thời gian → launch gates → phản biện → cam kết Hermes. Bottleneck thật = quyết định chờ Quang, KHÔNG phải code. Deliverable: md master `shared/ceo-operating-plan.md` → publish (md-to-html → content-upload) → verify browser → flush state. CHƯA commit git tới khi Quang duyệt. Chi tiết + mẫu: `references/ceo-operating-plan-2026-09.md`.

## ⚠️ QUY TẮC QUAN TRỌNG NHẤT (user correction — từng bị mắng vì vi phạm)

**KHÔNG code trước khi duyệt.** Vòng bắt buộc:
```
Anh giao task → brainstorm/propose → phản biện (Claw/CTO) → anh duyệt "triển khai đi" → code → review → test → merge
```
- Anh từng hỏi "ủa, anh đã duyệt gì đâu mà thực thi vậy" khi em code OKR trước khi chốt plan. Đừng lặp lại.
- Mọi task mới PHẢI đi qua phases: `planning → review → approved → in_progress → testing → completed`
- Task sinh ra ở `planning` — agent phải viết plan → gửi review → được approve mới implement.
- Proposal phải có cost + time estimate trước khi trình anh.

**CHỐT PHƯƠNG THỨC TRƯỚC KHI BUILD (anh mắng: "Hai em đã tự giao tiếp để chốt lại phương thức chưa? Tại sao anh thấy hai em mỗi người làm một cái vậy?"):**
- Có việc mới → Hermes + Claw **chốt phương thức qua inbox TRƯỚC** khi bắt tay làm.
- **Chỉ 1 người build, người kia review** — KHÔNG làm song song 2 hướng.
- Bài học thực tế: face recognition bị mỗi đứa làm một kiểu (Hermes MediaPipe trên tfo vs Claw Faceplugin spike trycloudflare) → anh Quang phát hiện và nhắc. Khi thấy Claw làm khác hướng → gửi inbox chốt ngay, không mặc kệ.

**QUY TẮC BẮT BUỘC "1 VIỆC 1 NGƯỜI" (anh Quang chốt 04/08, nhắc đi nhắc lại — ĐÃ GHI vào workspace.md + briefing.md):**
- **KHÔNG BAO GIỜ 2 đứa làm cùng 1 nhiệm vụ** — đã xảy ra nhiều lần (face recognition, voice processing) → anh hỏi "Sao hai đứa cùng thực hiện cùng một nhiệm vụ thế?".
- Mọi công việc mới → chốt qua inbox TRƯỚC: ai build, ai review, ai trả lời anh.
- **CUỐI CÙNG CHỈ 1 ĐỨA TRẢ LỜI ANH** — không 2 đứa cùng trả lời 1 câu hỏi.
- Hermes transcribe voice → gửi text Claw → Claw xử lý + trả lời anh (hoặc Hermes nếu đã phân công).
- Nghi ngờ bên kia đang làm → HỎI QUA INBOX trước, KHÔNG tự làm luôn.
- Khi anh chốt quy tắc mới kiểu này → GHI NGAY vào briefing.md (agents đọc khi thức dậy) + workspace.md, không chỉ nhớ trong đầu.

**QUY TẮC BẮT BUỘC — DEFINITION OF DONE (anh Quang chốt 12/08, sau khi chê standup lặp lại "mấy ngày cứ lặp lại nhau thế nhỉ"):**
- **MỌI task khi lên PHẢI có done criteria** (thế nào là xong, đo được) + deadline. Không có done criteria = task chưa hợp lệ → bổ sung NGAY trước khi làm.
- Báo "xong" phải kèm BẰNG CHỨNG: QA xác nhận / test pass / link kiểm chứng. Lời nói không tính.
- Standup báo "hôm qua ĐÓNG được gì" — không có done thì không có "đang làm" để kể.
- **Chẩn đoán vòng lặp standup** (khi Quang than "lặp lại nhau"): 3 nguyên nhân hệ thống — (1) task thiếu chuẩn xong → ai cũng "đang làm" mãi; (2) cờ trắng "chờ Quang chốt" lan man (nhiều agent chờ 1 người → team đứng im, không tự quyết được thì propose thay vì chờ); (3) 1 mắt xích vỡ (QA report hỏng) làm tê liệt cả vòng verify → fix: verify bằng tay, không chờ mắt xích đó.
- **Triển khai quy tắc mới kiểu này** (đã làm 12/08): ghi briefing.md + workspace.md + broadcast message bus + sửa cron standup prompt (bắt buộc báo done + bằng chứng, đánh dấu 🔁 LẶP cho task ≥2 ngày chưa đóng kèm lý do) + gửi inbox nhắc agent cụ thể xử lý việc đang kẹt. Push git để đồng bộ máy Claw.
- **DoD ĐÃ BUILD TRÊN TFO (commit af82589, server 8100, test pass):**
  - Backend (`app/main.py`): `POST /api/tasks` mode=agent → **400 `done_criteria_required`** nếu thiếu done_criteria; `POST /api/agent-tasks` task lớn (không parent_id) cũng 400. `update_task` + `update_ai_task` đều nhận field `done_criteria` (Form, trim, max 300).
  - UI (`app/static/index.html`): modal Thêm việc có textarea "XONG KHI NÀO? — ĐỊNH NGHĨA HOÀN THÀNH" (`newTaskDoneCriteria`) — chọn agent mà trống → alert chặn; kanban card hiện done_criteria + badge `⚠️ THIẾU done criteria` khi trống; panel chi tiết (`openAgentSub`) + task chat (`loadChatMessages` dcBanner) hiện banner "XONG KHI NÀO"; select `agentDcFilter` lọc missing/has (filter trong `renderAgentBoard`); modal edit có `editTaskDoneCriteria`.
  - Agent prompt: `app/agent_exec.py` `_build_context()` thêm dòng `✅ XONG KHI NÀO (done criteria — BẮT BUỘC đối chiếu khi báo hoàn thành): <criteria>` — agent phải thấy khi xử lý task.
  - Backfill task cũ: script map task id → done criteria theo tiêu đề (không bịa số liệu), ghi thẳng `store/tasks.json`.
  - **Pitfall: `store/tasks.json` + `store/*.json` runtime nằm trong .gitignore** → `git add store/tasks.json` bị từ chối "paths are ignored". Cập nhật data trực tiếp, chỉ git add code (app/*, hub/*, shared/*).

## Kiến trúc

```
D:/Hermes Proj/ai-company/
├── agents/base_agent.py    # BaseAgent + format_system_prompt (personality+framework+skills từ profiles.json)
├── agents/profiles.json    # Personality, framework, skills (level 1-5) cho từng agent
├── hub/store.py            # CRUD: tasks, proposals, okrs, skills, features, messages, cost, org
├── hub/run.py              # CLI: process, agent, status, proposals, standup
├── hub/process.py          # NLP routing — goal auto-parse, wake agents theo keyword
├── hub/aggregate.py        # Dashboard data JSON (gồm features tracker)
├── company.py              # Quick CLI: python company.py [status|okr|skills|...]
├── dashboard/index.html    # Dashboard B/W/Y (#FFD600, #0D0D0D, #1B1B1D) — Feature Tracker ở đầu trang
├── server.py               # port 8090 — dashboard company.thefirstonly.com (passcode lock <PASSCODE>)
│                           #   không cookie → LOCK_HTML; POST /api/login set cookie company_auth; data 401 nếu chưa login
├── app/                    # 🚀 TFO MVP WEB (FastAPI + venv .venv Python 3.11) — port 8100
│   ├── main.py             # Auth, transcribe (Groq), summarize (DeepSeek), tasks, meetings, skills, recording resilient
│   └── static/index.html   # UI B/W/Y — login email+passcode, ghi âm, task, meetings history, skills, org chart
├── tfo_data/               # MVP runtime: uploads/, recordings/, meetings.json, tasks.json, sessions.json
├── install_deps.py         # Cài deps venv (pip install bị terminal flag là long-lived → chạy qua script này)
├── shared/                 # GIAO TIẾP CROSS-MACHINE (tracked bởi git)
│   ├── inbox.py            # send/read/mark_read/reply — phân file theo hướng
│   ├── to_claw.json        # Hermes ghi → Claw đọc
│   ├── to_hermes.json      # Claw ghi → Hermes đọc
│   ├── workspace.md        # BỐI CẢNH CHUNG — source of truth, cả 2 cập nhật
│   └── transcripts/        # <meeting_id>.txt — transcript Hermes transcribe → Claw xử lý
└── store/                  # Runtime data (gitignored)
```

## Context Scan — value #2 (quét bối cảnh công ty → hỗ trợ quyết định)

ĐÃ BUILD — chi tiết ở `references/context-scan-value2-2026-08.md` + `references/context-scan-build-2026-09.md`. Điểm mấu chốt: dedup = sha256 của BRIEF NGUỒN (KHÔNG dedup synthesis — LLM sinh headline khác mỗi lần); `str.__hash__()` bị PYTHONHASHSEED random hóa giữa process → phải `hashlib.sha256`.

## ⚠️ Python venv trên máy này (đã dính lỗi)

- `python` mặc định = **3.14.5** (C:\Python314) → cài pydantic-core cp314 → `ModuleNotFoundError: No module named 'pydantic_core._pydantic_core'`. Luôn chạy MVP bằng `.venv/Scripts/python.exe`.
- **Fix:** tạo venv bằng Python 3.11: `"/c/Users/NTQUANG_DELL/AppData/Local/Programs/Python/Python311/python.exe" -m venv .venv`.
- `pip install` trực tiếp bị flag "long-lived server" → chạy qua `install_deps.py` (subprocess pip) hoặc background.

## TFO MVP Web (app/ — port 8100, tfo.thefirstonly.com)

Sản phẩm trợ lý CEO: ghi âm/upload meeting → Groq Whisper transcribe → DeepSeek summarize → task tự sinh. Chi tiết đầy đủ (restart server 8100 qua `tfo_launch.py`, login server-side cổng thật, recording resilient + SESSIONS persist, Groq 16MB/chunking theo duration, volume boost quyết định chất lượng, diagnose "treo/thiếu transcript", clean transcript regex, push Telegram, audio luôn lưu local + retry theo file_id): `references/tfo-mvp-web-2026-08.md`.
Chi tiết meeting-publish 2 tab, H1 streaming WS, H2 context-scan, H3 reliability (03/09): `references/tfo-h123-meeting-publish-2026-09.md`.

## Task-thread + Tab "Agent" trong TFO (2026-08, anh Quang chốt định hướng — ĐÃ BUILD + TEST 2026-08-05→06)

Kanban 2 cấp + task chat (poll 3s + ghi âm) + agent context + auto-critique; source=user vs source=ai tách biệt; mode=agent vs mode=kanban; pitfall JS Date parsing tiếng Việt, popup trùng tên hàm `openTaskModal`, template literal giết cả script block, sibling agent edit conflict. Chi tiết build + pitfall + test thật: `references/tfo-task-thread-agent-tab-2026-08.md`.
Recipe đánh thức task planning cũ (enqueue + race queue corrupt): `references/dod-and-worker-fixes-2026-08.md`.

## ⚠️ LLM KHÔNG đáng tin cho domain routing — regex-first là chuẩn (2026-08, test thật)

LLM chọn agent sai 3/4 test → regex deterministic TRƯỚC, LLM chỉ fallback cuối; bẫy `post` nuốt "postbiotics" + bẫy `thread` → Content. 5 fix + test verify 8/8 đúng: `references/tfo-task-thread-agent-tab-2026-08.md`.

## Calendar — Tab "Lịch họp" (2026-08, tfo web)

Week view → click ngày → meeting → overview + tasks; meeting `title`/`meeting_time`; task link meeting; xóa meeting; pitfall nút Xem "không có gì" + JS async `recSid`. Chi tiết: `references/tfo-ui-taskboard-and-features-2026-08.md`.

## Multi-tenancy (2026-08 — anh Quang chốt: account tách riêng, Quang là admin)

Chung domain, mỗi user 1 folder `tfo_data/users/<email_sanitized>/`; API token-scoped; `/api/admin/users` cho Quang; demo isolation 15/08 PASS; pitfall migrate folder email thật vs sanitized. Chi tiết: `references/tfo-ui-taskboard-and-features-2026-08.md`.

## Face Login — MediaPipe (2026-08, on-premise, thay passcode)

MediaPipe Tasks API (478 landmarks, cosine ≥ 0.93), auto-login 1:N, enroll ngay trong app (menu ⋯), UI login 2 tab, auto-scan 2s, nút 🔒 Khóa, không liveness; pitfall treo "đang nhận diện" do thiếu deps venv. Chi tiết: `references/tfo-face-login-mediapipe-2026-08.md`.

## Stealth mode + Launch plan (2026-08)

- **STEALTH MODE:** KHÔNG content/truyền thông/marketing giai đoạn này — không publish gì ra ngoài. Xong product + GTM mới đến lượt content. Ý tưởng ra sớm → mất lợi thế ra mắt.
- Content/Social/CMO agents: chỉ chuẩn bị nội bộ, KHÔNG đăng tải.
- Plan: `shared/launch_plan.md` — Phase 1 (multi-tenancy, fix bug, pilot CEO #2, test meeting thật) → Phase 2 (onboarding, pricing ẩn, landing draft, backup/HA, test load, demo) → Phase 3 (GTM — chờ Quang bật đèn xanh). Chưa mở đăng ký.

## Dashboard Company passcode (2026-08 — "cho anh access chứ k public nhé")

- Dashboard KHÔNG public — passcode `<PASSCODE>` (hằng số trong server.py, đổi được bằng cách sửa PASSCODE).
- Cơ chế: cookie `company_auth`; chưa có cookie → server trả LOCK_HTML (trang nhập passcode B/W/Y); POST `/api/login` đúng → 302 + Set-Cookie 30 ngày; sai → 401 + error hiện trên form.
- `company-data.json` cũng 401 nếu chưa cookie — data không lộ.
- Test nhanh: `curl -b /tmp/cookie -X POST http://localhost:8090/api/login -d "passcode=<PASSCODE>"` → 302, rồi `curl -b /tmp/cookie http://localhost:8090/` → 200.
- LOCK_HTML là chuỗi nhúng trong server.py — form POST /api/login; do_POST phải xử lý path đó (SimpleHTTPRequestHandler mặc định không có do_POST).

## Mission Control (Dashboard Company — 3 câu hỏi anh cần)

Anh Quang: "em trình bày rất khó hiểu... tổng hợp hết lên dashboard để anh vào xem cái gì đang diễn ra, mục tiêu nào, ai đang có mục tiêu nào."

- Card đầu trang: 3 cột — **MỤC TIÊU HIỆN TẠI** (goal to, viền vàng) | **ĐANG DIỄN RA** (task active + phase) | **AI ĐANG LÀM GÌ** (agent không idle + task của họ).
- Data từ `company-data.json`: `current_goal.title` (lưu ý: store trả `title`, KHÔNG phải `goal` — pitfall từng render "—" vì đọc sai field), `tasks.all` filter phase, `agents` filter status != Idle.
- Nếu tất cả idle → hiện rõ "Tất cả 10/13 agents đang idle — chờ task" — anh biết ngay team không có việc, không phải đoán.

## Task Board — 10 task đầu + "Xem thêm" popup infinite scroll (2026-08-15)

Dashboard Company + TFO web (`app/static/index.html`): 10 task đầu + popup bottom-sheet batch 30, state global; pitfall trùng tên hàm popup, template literal đóng sai giết script (`node --check` bắt buộc), test login TFO (quang@kiemsaphia.com / <PASSCODE> / key `tfo_token`). Chi tiết: `references/tfo-ui-taskboard-and-features-2026-08.md`. Mobile overflow ngang: `references/mobile-overflow-checklist.md`.

## Feature Tracker (Dashboard Company — 1 trang theo dõi mọi thứ)

`store/features.json` + enum status live/done/in_progress/planned/blocked; thêm feature ghi thẳng file; pattern SPIN; gác SPIN/nhóm task (paused + paused_reason); đóng task theo QUYẾT ĐỊNH của Quang (close_note); format "list all tasks để Quang quyết". Chi tiết: `references/tfo-ui-taskboard-and-features-2026-08.md`.

## ⚠️ Git security — repo ai-company PRIVATE + sensitive files (2026-08-06, phát hiện lộ token)

- Repo `github.com/ntquang1110/ai-company` đã **chuyển private** (PATCH `/repos/{owner}/{repo}` với `{"private": true}`).
- **File NHẠY CẢM đã từng bị track trên git — phải `git rm --cached` + thêm .gitignore ngay lập tức:**
  - `tfo_data/tg_env.json` — **chứa Telegram bot token thật** → đã từng push lên history (commit cũ) → rủi ro còn trong history dù repo private. Cân nhắc đổi token hoặc `git filter-repo`.
  - `tfo_data/users/*/face_embedding.json` — sinh trắc học khuôn mặt.
  - `*.webm /*.mp3 /*.opus /*.wav /*.ogg`, `tfo_data/recordings/`, `tfo_data/uploads/*.mp3/*.opus/*.webm`, `tfo_data/users/*/recordings/` — audio cuộc họp (nặng + riêng tư).
- **Trước khi `git add -A` lần đầu trên repo có data user — luôn check:**
  ```bash
  git ls-files | grep -E "\.webm|\.mp3|\.opus|\.ogg|\.wav|tg_env|face_embedding"
  git status --porcelain | grep -iE "\.mp3|\.opus|\.wav|recording|export|\.env|key|token"
  ```
  Nếu còn → thêm vào .gitignore + `git rm --cached` (giữ file trên disk).
- **`.gitignore` pattern an toàn:** `*.env`, `tfo_data/tg_env.json`, `tfo_data/users/*/face_embedding.json`, audio patterns, `tfo_data/exports/` (regenerable), `*.log`, `logs/`.

## ⚠️ Inbox files PHẢI tracked trên git — đừng gitignore (pitfall 2026-08-06, suýt vỡ kênh)

Inbox đồng bộ QUA GIT (`send()` tự commit+push, `read()` tự pull) → PHẢI track `shared/to_claw.json` + `shared/to_hermes.json` (bỏ track = vỡ kênh); KHÔNG BAO GIỜ gửi token qua inbox. Kèm meeting note JSON: LLM summarize không deterministic → heuristic gán người/deadline, chạy 2 lần, pitfall JSON cắt ngang sinh task rác. Chi tiết: `references/inbox-git-tracking-and-meeting-note-json.md`.

## Giao tiếp Hermes ↔ OpenClaw (2 máy riêng)

Cơ chế Git shared files (`shared/inbox.py`: `send/read/ack/find_stale`); Inbox Protocol v3 ACK bắt buộc; pitfall ACK spam vô hạn + ACK loop + watchdog cron phải silent; verify 2 chiều bằng số liệu thật. Chi tiết: `references/hermes-openclaw-inbox-protocol.md`. Kênh LAN chat 8890 + watchdog: `references/lan-chat-channel.md`.

## 🛡 CHỐNG TRÔI (24/08) — Claw OFF, Hermes giữ Front

**OpenClaw (máy front) ĐÃ TẮT từ 24/08.** Khi Claw tắt: KHÔNG ghi wake vào `shared/to_claw.json` chờ relay — wake đó chết im (đúng 4 wake 22/08 kẹt vì Claw không ACK). Thay bằng:

1. **Wake TRỰC TIẾP vào worker port 8100:** `python hub/wake_agent.py <task_id> "<msg>" "<agent>"` — script tự login (`/api/login` email=quang@kiemsaphia.com passcode=<PASSCODE>) + POST `/api/tasks/<id>/messages` (source=ai) → worker pool tự claim. KHÔNG cần máy Claw.
   - ⚠️ **Arg thứ 3 (tên agent) CHỈ là text prefix `(QA)` nhét vào message, KHÔNG điều khiển routing** (verify 26/09: wake #8 ghi rõ "QA" nhưng `route_agent` chọn agent **Content** và Content trả lời). Muốn biết AI thực sự xử lý: đọc `tfo_data/users/<email>/task_messages.json`, xem message mới nhất `role=agent` + field `agent`. Muốn gọi ĐÚNG agent thì phải sửa regex `route_agent` (chờ Quang duyệt) hoặc set assignee trên task trước khi wake.
   - ⚠️ **`"🤖 Đã nhận — agent đang xử lý..."` KHÔNG phải đã xong.** Wake thành công (queue status `done`) vẫn có thể ra output bị CẮT giữa nội dung (26/09: 3707 ký tự, đứt ở test case thứ 2) và agent KHÔNG tạo file nào dù tự đề xuất đường dẫn. Luôn `ls` đường dẫn thật trước khi tin báo cáo.
2. **SLA determinist:** `python hub/ops_guard.py [--json]` — scan `store/tasks.json`: STALE (phase không-terminal ≥48h không đổi theo updated_at), NO_DC (active thiếu done_criteria), WAKE (tin to_claw còn status=sent). Chạy mỗi standup cron. Env `SLA_FAKE_NOW` ISO để test deterministic, `SLA_STALE_HOURS` đổi ngưỡng.
3. **DoD verify bằng script:** `python hub/verify_done.py --claim "<bằng chứng>"` — claim là file path (tồn tại?) hoặc commit hash (có trên `origin`?, `git branch -r --contains`). ACCEPT (exit 0) / REJECT bịa (exit 1) / link chưa kiểm chứng (exit 2). Chặn "báo done bằng thư mục không tồn tại" kiểu CMO lần 2.
4. Standup cron `9b6eb3205750`: prompt BƯỚC 1 chạy ops_guard trước, verify_done mọi claim trước khi tin agent, wake thẳng worker, escalate stale->Quang.
5. **Biến số guard thành HÀNH ĐỘNG (24/09, sau 3 tuần standup lặp y hệt):** NO_DC → backfill `done_criteria` ngay (bám title, KHÔNG bịa số) nhưng **KHÔNG bump `updated_at`** (bump = che STALE thật). STALE toàn task của NGƯỜI (mode=kanban) → **KHÔNG wake**, gom 1 nút cho Quang. Blocker giả ("OpenCode hết credit") = `briefing.md` cũ bị `think()` inject → sửa GỐC ở briefing. `verify_done` ACCEPT hash đã push ≠ claim đúng. Số agent tự báo hay lệch (32/4 vs 41/7) → đếm lại `Counter(t['phase'])`. Chi tiết: `references/standup-guard-actions-2026-09.md`

**Pitfall terminal guard đọc nhầm env inline:** lệnh `FOO=bar python script.py` trong terminal tool bị lifecycle guard đọc nhầm làm path script → `open: embedded null character in path`. Tránh inline env; set env trong code (test runner .py set os.environ rồi import) hoặc chạy qua `execute_code`.

## ⚠️ PITFALL UPLOAD FILE LỚN + TRANSCRIBE ASYNC (24-25/08) → `references/tfo-big-file-async-2026-08.md`
- Upload >100MB → browser "treo" nhưng **0 file tới server** (CF cắt body ~100MB) → chunk 10MB gửi **tuần tự** + reassemble theo index.
- Chunk cuối transcribe **đồng bộ** → XHR timeout 120s giết, meeting không lưu (`uploads/` có `.m4a` nhưng thiếu `.opus`) → `_JOBS` + thread nền + `GET /api/transcribe/job` poll. **Đừng copy cụm `if size_mb > 60 → 413` sang đường chunk** — giới hạn theo DURATION.

## 📏 ĐO ĐỘ ĐỦ CỦA TRANSCRIPT — "transcript thiếu text so với voice input" (25/08, Quang phát hiện)

Chạy `hub/transcript_coverage.py <audio> <transcript_file|text>` (JSON, exit 1 nếu THIẾU) — 3 tầng: tỉ lệ từ/phút (<40% THIẾU) → bản đồ giọng `ffmpeg silencedetect` → cross-check từng chunk. Pitfall đếm từ (ký tự ≠ từ) + cách chạy trong/ngoài cron: `references/transcript-coverage-2026-08.md`.

## E2E Encryption opt-in (2026-08-28) — value prop "key user cầm, zero-knowledge"
Chi tiết + pitfall token query param: `references/tfo-e2e-encryption.md`. Chỉ CHO EXPORT (opt-in), KHÔNG mã hóa at-rest realtime.

## Context Scan — value #2 (quét bối cảnh công ty → hỗ trợ quyết định) (2026-08-28)

`hub/context_scan.py` (build_brief → synthesize JSON), CLI + `tfo_data/context_scan.json`, aggregate + card dashboard, push TG HTML; cron 6h dedup bằng `hashlib.sha256` (KHÔNG `str.__hash__`). Chi tiết: `references/context-scan-build-2026-09.md`.

## H2 — Context-scan CHỦ ĐỘNG (09/2026) — nâng value #2: proposal → task draft → anh chốt → push TG gọn

C1 proposals thành JSON action · C2 auto task draft (`sync_context_scan_to_tasks`, dedup `scan_key`) · C3 nút chốt approve (8090 cookie-auth + 8100 token-auth admin) · C4 push TG top 3 đề xuất mới; pitfall patch tool giết Python indentation. Chi tiết: `references/context-scan-build-2026-09.md`.

## Silent cron pattern (đã chốt với anh)

`no_agent=True` + script: stdout = delivered, rỗng = silent; cron mode (`execute_code` BỊ CHẶN, `$TEMP` không resolve, background không inherit `cd`); kỷ luật verify số liệu (mutation test phải FAIL được, KHÔNG xoá script đo trước khi mutation PASS, 4 kiểu PASS giả, lone LF, STALE ảo do wake bump `updated_at`). Chi tiết: `references/silent-cron-and-verifier-patterns.md` + `references/verifier-mutation-design-2026-10.md` + `references/cron-mode-scripts-2026-09.md`.

## ⚠️ Watchdog/backup/probe script pattern — cron no_agent PHẢI bounded 1 lượt (H3, build 03/09)

Chi tiết đầy đủ + verify thật + 3 script mẫu (watchdog_8100, backup_tfo, uptime_probe_8100): `references/reliability-h3-2026-09.md`.

Quy tắc lõi: script default = 1 lượt rồi exit (stdio rỗng = silent khi OK); daemon nền dùng `--loop`, TUYỆT ĐỐI không loop vô hạn trong cron. Uptime probe chống spam = bắt transition bằng counter `consecutive_fails`, KHÔNG bằng state string. Pitfall taskkill git-bash: bọc qua `cmd //c "taskkill /F /PID <pid>"` rồi `netstat -ano | grep :<port> | grep LISTENING` xác nhận port free. Mọi script cron no_agent: copy sang `~/AppData/Local/hermes/scripts/`, verify `hermes cron run <name>` → "Ran now: succeeded".

## Standup cron — runbook chạy + verify (2026-08-14, áp dụng từ 14/08)

Chạy `python hub/run.py standup` KHÔNG đủ — verify 4 nguồn bằng chứng (git log / file / `store/tasks.json` dict / inbox), 4 pattern lặp (done không bằng chứng, chốt không bằng chứng, report lệch ngày → inject ngày hệ thống vào prompt, task xong chưa đóng phase + chưa push), Standup None (401/429/403/empty), chẩn đoán "cron có chạy không" bằng file output + khối `## Error` + chain 2 chân `hub/store.py`, kỷ luật số liệu (đo bằng script, không cộng tay). Chi tiết: `references/standup-runbook-full-2026-08.md`.
Cơ chế standup trong CRON (timeout, dedup, mutation): `references/standup-cron-runbook-2026-09.md` · `references/standup-agent-output-to-artifact.md` · `references/standup-number-discipline-2026-10.md` · `references/briefing-staleness-2026-10.md`.

## Vai trò (chốt 2026-07, đã đảo — Claw OFF từ 24/08)

- **Hermes = Front + Back**: logic, phản biện kín, review, triển khai kỹ thuật, giữ hạ tầng, và phản hồi anh trực tiếp.
- OpenClaw (front cũ) ĐÃ TẮT ⇒ cron `follow-claw-lan-chat` (03c52d4c23fd) hết ý nghĩa; recipe watchdog silent 1 lượt + state file chống spam ở `references/lan-chat-channel.md`.
- Còn hiệu lực: **chỉ 1 giọng hỏi/trả lời anh** (anh từng mắng "sao 2 đứa đều hỏi anh thế"); phản biện nội bộ trước, chốt xong mới báo anh.
- Chiến lược TFO (purpose/mission/vision, M-series): `references/tfo-vision.md` + `shared/workspace.md`.
- 📌 **Standup 25/09** — lô trùng context-scan tái sinh (dedup `sha256(noi_dung)` vô dụng vì LLM diễn đạt lại) + verify bằng chứng giả (CMO bịa file + commit hash + nhận task người khác) + số liệu guard trôi giữa 2 lần chạy: `references/standup-dup-loop-and-fake-evidence-2026-09.md`.

## Vision/Mission phổ biến cho team (lesson: "team vẫn hỏi mục tiêu là gì")

- Agents đọc **briefing.md** mỗi khi thức dậy — KHÔNG đọc `workspace.md` (chỉ Hermes/Claw đọc workspace). Vision/mission/goal chỉ nằm trong workspace.md → team không thấy → hỏi "mục tiêu là gì" dù anh đã chốt.
- Fix đã làm (2026-08): rewrite `briefing.md` với VISION/MISSION/ĐỊNH HƯỚNG/CURRENT GOAL ở đầu + broadcast message bus tới cả 13 agents (subject "🎯 VISION & MISSION ĐÃ CHỐT — ĐỌC NGAY") + thêm section "Vision & Mission" vào đầu Dashboard Company.
- Ghi chú cuối briefing.md: "Team KHÔNG hỏi mục tiêu là gì nữa — nếu chưa rõ việc phải làm thì propose cho Quang, đừng đứng yên chờ hỏi."
- Quy tắc: khi anh Quang chốt quyết định chiến lược mới → cập nhật briefing.md NGAY, không chỉ workspace.md.

## Chế độ làm việc (anh Quang chốt 2026-07)

- **CHẠY SONG SONG — KHÔNG KILL TASK ĐANG CHẠY (Quang chốt 15/08):** có order mới → làm song song với việc đang dở, KHÔNG được kill process/task/background job đang chạy. Nhiều việc cùng lúc OK. (Lưu ý phân biệt với "1 VIỆC 1 NGƯỜI" — quy tắc đó là Hermes vs Claw không làm TRÙNG 1 nhiệm vụ; quy tắc này là Hermes không hủy việc đang chạy khi nhận việc mới.)
- **Làm liên tục, không dừng:** không phải làm xong 1 tính năng rồi chờ. Cứ build tiếp cho đến khi hoàn thiện toàn bộ. Mỗi ngày xong tính năng nào thì cập nhật Feature Tracker.
- **LÀM ĐƯỢC THÌ LÀM, KHÔNG CHỜ CHỐT DEADLINE (Quang chốt 12/08 — "cái gì làm được luôn thì em làm đi, chờ chốt deadline làm gì"):** task treo vì chờ Quang chốt giờ/người → chuẩn bị TRƯỚC toàn bộ phần tự làm được (kịch bản, checklist, test thử, verify); khi Quang chốt chỉ còn phần phụ thuộc anh. Agent tự đề xuất scope giả định + làm, KHÔNG hỏi "làm gì tiếp theo". Đã ghi `shared/workspace.md`.
- **Cần anh duyệt thì trình anh duyệt** (login hướng, scope, thứ tự ưu tiên) — không tự ý quyết định thay anh.
- Khi anh chốt "triển khai đi" → GO ngay, không hỏi lại.
- Báo cáo tiến độ dạng bảng (feature/status/progress) — anh đọc nhanh, không cần hỏi lại "team đang chạy gì".

## Pipeline xử lý meeting (đã chốt)

Hermes = transcribe (Groq Whisper) → xử lý + phản hồi anh (Claw OFF 24/08 → Hermes giữ cả 2 vai); trao đổi qua `shared/transcripts/<meeting_id>.txt` + inbox metadata; test pipeline không cần meeting thật (TTS → `/api/transcribe` → `/api/summarize`); pitfall `/api/summarize` transcript là TEXT field (422 với `-F @file`), summary double-encoded. Chi tiết: `references/tfo-meeting-pipeline-flow.md` + `references/tfo-pipeline-pitfalls-2026-08.md`.

## OKR System

- `create_objective()` → `add_key_result(kr, target, baseline, owner, metric)` → `auto_gen_tasks_for_kr()` sinh 2-3 tasks gán agent theo context (SEO→Content, conversion→Dev1/Design, traffic→CMO).
- KR auto-calc: `(current - baseline) / (target - baseline) * 100`. Objective progress = avg KRs.
- `get_objective_tree()` — full hierarchy. `python company.py okr` — CLI tree.
- Tasks giữ workflow bắt buộc — auto-gen KHÔNG skip phases.
- **Pitfall test data lẫn vào data thật:** sau khi test OKR/tasks/auto-gen bằng data giả (vd "Tối ưu conversion rate", "SEO content 4 bài") PHẢI dọn sạch ngay — anh từng hỏi "sao lại có SEO với content ở đây" vì test data cũ nằm trên dashboard. Dọn: reset `store/tasks.json` + `store/okrs.json` + `store/goals.json` về rỗng, tạo lại task thật duy nhất cho mục tiêu hiện tại. Kiểm tra qua `/company-data.json` sau khi dọn.

## Agent message bus (nội bộ)

- `store/messages.json` — agents gửi/nhận review requests, tự phản biện.
- `request_review(task_id)` — auto route theo keyword: technical→CTO, marketing→CMO, design→Design, cost→CFO.
- Reviewer PASS → task `approved` + notify Quang chờ confirm "triển khai đi".
- Reviewer FAIL → task quay lại `planning` + ghi review_notes.
- Pitfall: `cmd_agent` với `prompt` param sẽ BỎ QUA workflow phase logic — chỉ dùng prompt khi muốn bypass; còn lại gọi agent không prompt để tự xử lý theo phase.
- Pitfall: agent pickup task đầu tiên trong list → task cũ phase review chặn task mới. Ưu tiên task mới nhất theo updated_at.

## 🌀 H1+H2+H3 ĐÃ BUILD XONG 03/09 — code + pitfall + verify thật: `references/h1-h3-build-2026-09.md`

- H1 live streaming (`WS /ws/stream` VAD + `_groq_micro`) · H2 context-scan → task draft + nút `✓ Chốt` (8100 + 8090, phải nhận CẢ JSON lẫn form-urlencoded) · H3 reliability: watchdog_8100 + backup_tfo 10 bản + uptime_probe TG no-spam (3 cron đang chạy).
- Pitfall H1: `feed()` phải loop hết frame trong 1 WS message; `OVERLAP_S*FRAME_SAMPLES` ra float → `int()`.
- ⚠️ Subagent delegation: tin báo "code xong" rồi VẪN tự verify + restart server + commit/push + revert task test.

## Voice Assistant (Gemini Live) — Phase A hiện thực + Whisper local Mac node
- Plan + contrib (BA/SA/CTO/Dev): `D:/Hermes Proj/voice-live-plan-final.md` + `D:/Hermes Proj/.hermes-state/plan-contrib-*.md`.
- Demo initial = Phase A (voice 2 chiều) + tối thiểu Phase B (RAG read-only), KHÔNG chạm execution (CTO trì hoãn).
- TTS trong event loop phải dùng method async (synth_cached_async) — `asyncio.run()` trong loop đang chạy SẼ LỖI; `asyncio.nop()` không tồn tại trên Python 3.9.
- Chi tiết modules, test WS end-to-end, Whisper local Mac node (đã verify 03/09): `references/voice-assistant-phaseA-live.md`.

## Streaming realtime STT — Groq KHÔNG có WebSocket streaming (spike 01/09, Quang chốt value 1)

Groq không có WS STT → pattern VAD chunking 2-5s + overlap 1-1.5s (~0.8s/chunk), pipeline cũ giữ nguyên; bản build 03/09 (`app/streaming.py`, `_groq_micro`); pitfall `OVERLAP_S*FRAME_SAMPLES` ra float, `feed()` chỉ xử lý 1 frame, headers chống 403 code 1010. Chi tiết: `references/streaming-realtime-stt-2026-09.md` + `references/h1-streaming-realtime-2026-09.md`.

## DeepSeek via OpenCode (LLM calls — agent.think)

Endpoint `https://opencode.ai/zen/go/v1/chat/completions` + `OPENCODE_GO_API_KEY` (rotate → 3 chỗ); models flash (chat/coder) / pro (reasoner), cost `store/cost.json`; retry/fallback pro khi flash rỗng; chain 4 chân OpenCode → Ark → OpenRouter → Gemini. Chi tiết: `references/llm-provider-opencode-deepseek.md` + `references/opencode-model-ids-2026-09.md` + `references/bytedance-ark-fallback-2026-09.md` + `references/llm-chain-fallback-2026-10.md`.

## Domain/DNS (đã đấu tranh)
- Cloudflare tunnel chạy như Windows Service với `--token` → config nằm trên Zero Trust dashboard, KHÔNG đọc/sửa file config local được. Sửa được **qua API**: `PUT /accounts/{TAG}/cfd_tunnel/{ID}/configurations` với full ingress list → tự load ~30s. Skill `cloudflare-tunnel`.
- `company.thefirstonly.com`→8090, `tfo.thefirstonly.com`→8100, `me`→5099, `upload`→8769 (cũng serve `/company`). DNS = CNAME → tunnel `.cfargotunnel.com`.
- Dashboard không lên data mới → restart server.py (import code cũ trong process).

## Style

- Trả lời anh bằng tiếng Việt, ngắn gọn, đi thẳng vào vấn đề.
- **QUY TẮC "1 VIỆC TRỌNG TÂM" (anh mắng: "Em trả lời nhiều quá, chọn 1 cái làm trọng tâm thôi, xong 1 cái và final lại mới trả lời anh"):**
  - Chọn 1 việc quan trọng nhất → làm XONG (build + test + push) → rồi mới báo cáo final ngắn.
  - Không trả lời/nhận việc lan man nhiều đầu việc trong 1 message. Không báo giữa chừng "đang làm A, B, C...".
  - Báo cáo = 1 việc đã xong + kết quả cụ thể, không phải danh sách dự định.
- Khi anh chốt: "triển khai đi" → làm. Khi anh hỏi "thế nào rồi" → báo trạng thái cụ thể.
- Dashboard theo Premium B/W/Y (#FFD600, #0D0D0D, #1B1B1D).
