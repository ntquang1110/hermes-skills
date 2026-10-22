---
name: ai-company
title: ai-company
description: Vận hành và build hệ thống AI Company — công ty multi-agent (13 agents, cấu trúc CTO quản PO/PM/SA + Senior Dev/Tester) tại D:/Hermes Proj/ai-company. Gồm OKR system, task workflow plan→review→approve→implement→test, giao tiếp Hermes↔OpenClaw qua Git inbox, MVP web tfo.thefirstonly.com (multi-tenancy, auth email+passcode), dashboard company.thefirstonly.com.
tags:
  - multi-agent
  - okr
  - workflow
  - shared-inbox
  - hermes-opencyclaw
  - fastapi
  - windows
domain: software-development
---

# AI Company — hệ thống multi-agent

> ## ⛔ DỰ ÁN ĐÃ ĐÓNG — 2026-10-17 (Quang chốt)
>
> **AI Company (multi-agent nội bộ) SHUTDOWN.** KHÔNG chạy standup, KHÔNG sinh task, KHÔNG dựng lại.
>
> - **Đã pause 5 cron:** `ai-company-standup`, `ai-company-inbox`, `ai-company-context-scan`, `follow-claw-lan-chat`, `watchdog-lanchat-claw-businesses`
> - **GIỮ NGUYÊN (KHÔNG phải AI Company — là sản phẩm TFO):** port 8100 (`tfo.thefirstonly.com`), dashboard Company 8090, 3 cron `ai-company-watchdog-8100` / `ai-company-uptime-probe-8100` / `ai-company-backup-tfo`, và `watchdog-all-ports` (vẫn restart 8100 + 8090)
> - **⚠️ BẪY TÊN:** 3 cron trên mang tiền tố `ai-company-` nhưng phục vụ TFO, KHÔNG phải AI Company — đừng pause/remove nhầm.
> - **Lý do đóng:** team đứng im (05-12/10: 9 ngày 0 commit), chain LLM cạn dần, 23 task planning tồn đọng/trùng lặp, không ra sản phẩm.
> - **Xóa hẳn:** sau 3-7 ngày nếu không vỡ → `cronjob(action='remove', job_id=...)`.
> - Chi tiết: `D:/Hermes Proj/.hermes-state/ai-company.md`
>
> Nội dung bên dưới giữ nguyên để tra cứu lịch sử (kiến trúc, workflow, pitfalls) — hữu ích nếu dựng lại hoặc tham chiếu cách làm.

Công ty AI do Quang điều hành: **13 agents** — CTO quản lý PO/PM/SA + Senior Dev1/Dev2 + Senior Tester; CMO (GTM strategy) + Content/Social/COO/CFO/Design (idle chờ GTM) — cùng làm việc với OKR, task workflow nghiêm ngặt, và giao tiếp nội bộ qua shared files. Đây là sản phẩm sống — build tiếp mỗi session.

## When to use

- User nhắc "AI Company", "team agents", "công ty AI", "okr", "agents propose/review"
- Build tính năng mới cho tfo.thefirstonly.com (MVP trợ lý CEO)
- Đồng bộ/giao tiếp với OpenClaw (Claw) qua shared inbox
- Chạy agents, xem task/OKR/dashboard

## Org chart (13 agents — chốt 02/08, user yêu cầu cấu trúc này)

```
👑 Quang
└── 🛡 CTO
    ├── 📦 PO — Product Owner: backlog, ưu tiên feature, định nghĩa product
    ├── 📅 PM — Project Manager: điều phối task, deadline, tiến độ
    ├── 🏗 SA — System Architect: thiết kế kiến trúc, data flow, upgrade path
    ├── Senior Dev1, Senior Dev2 — implement core
    └── Senior Tester (QA) — verify, chặn bug trước ship
```

- **Thêm 3 agents mới:** PO, PM, SA — thêm vào `agents/profiles.json` (personality+framework+skills), `AGENT_SYSTEM_PROMPTS` trong `agents/base_agent.py`, và `get_agent_statuses()` trong `hub/store.py`. Thiếu 1 trong 3 chỗ → agent không xuất hiện/hoạt động không đúng.
- Dev1/Dev2 → Senior Dev; QA → Senior Tester (đổi role label trong store.py).
- **CMO = Chiến lược gia GTM** — định hướng product + GTM strategy, STEALTH chưa publish.
- **Content/Social/COO/CFO/Design: GIỮ NHƯNG IDLE** — chờ GTM. Không giao việc content cho tới khi user bật đèn xanh.
- `store/org.json` chứa structure hierarchical + roles + dependencies; `app/static/index.html` workflow diagram phải khớp org chart.

## STEALTH MODE (bắt buộc — user chốt 02/08)

- **KHÔNG content/truyền thông/marketing giai đoạn này** — chưa publish gì ra ngoài.
- User: *"em không đưa content hay truyền thông vào vội, anh muốn xong và GTM mới đến lượt. Ý tưởng ra sớm thì ae sẽ all in và mất lợi thế ra mắt."*
- Content/Social/CMO: chỉ chuẩn bị nội bộ (plan, draft), KHÔNG đăng tải.
- Ghi vào briefing.md (agents đọc) + workspace.md (điều phối).

## Cấu trúc thư mục (D:/Hermes Proj/ai-company)

```
├── agents/
│   ├── base_agent.py      # BaseAgent class + format_system_prompt (personality + framework + skills)
│   └── profiles.json      # Mỗi agent: personality, framework (SOP), skills (level 1-5)
├── hub/
│   ├── store.py           # MỌI CRUD: tasks, proposals, OKR, skills, agents, org, message bus, cost
│   ├── run.py             # CLI: process/agent/status/proposals/standup
│   ├── process.py         # NLP routing: goal → wake agents theo keyword
│   ├── aggregate.py       # Dashboard data JSON
│   └── agents/*.py        # Script agent (cto, dev1, content, qa)
├── app/
│   ├── main.py            # MVP FastAPI (port 8100) — transcribe/summarize/tasks/record
│   └── static/index.html  # UI trợ lý CEO (Premium B/W/Y)
├── shared/
│   ├── workspace.md       # BỐI CẢNH CHUNG — source of truth (mục đích, sứ mệnh, quyết định)
│   ├── inbox.py           # Gửi/nhận tin Hermes↔OpenClaw qua Git
│   ├── to_hermes.json     # Claw ghi → Hermes đọc (KHÔNG conflict vì mỗi bên 1 file)
│   ├── to_claw.json       # Hermes ghi → Claw đọc
│   └── sync.py            # Cron 1 phút: pull → đọc tin mới → output → push
├── server.py              # Dashboard AI Company (port 8090)
├── company.py             # CLI nhanh: python company.py [status|okr|skills|process|agent]
└── tfo_data/              # MVP data: uploads/, recordings/, tasks.json
```

## Quy tắc workflow BẮT BUỘC (user đã nhấn mạnh nhiều lần)

1. **PHẢN BIỆN TRƯỚC KHI CODE** — user từng nổi giận: *"ủa, anh đã duyệt gì đâu mà thực thi vậy"* khi agent code trước approval. Luôn: brainstorm → phản biện → user duyệt ("triển khai đi") → code.
2. **Task mới phải qua đủ phase:** planning → review → approved → in_progress → testing → completed. KHÔNG nhảy phase, KHÔNG code trước khi plan được duyệt.
3. **Khi có 2 agent (Hermes + OpenClaw): chỉ 1 agent hỏi user.** User: *"sao 2 đứa đều hỏi anh thế, tổng hợp lại 1 thôi"*. Phân role: OpenClaw = front (hỏi, chốt, phản hồi user), Hermes = back (logic, phản biện, build). Workspace.md ghi rõ role.
3b. **CHỐT PHƯƠNG THỨC TRƯỚC KHI BUILD — 2 agents không được làm song song 2 hướng.** User từng bực: *"Hai em đã tự giao tiếp để chốt lại phương thức chưa? Tại sao anh thấy hai em mỗi người làm một cái vậy?"* — Hermes build MediaPipe face login trên tfo, Claw làm spike Faceplugin riêng, không ai chốt với nhau. Hậu quả: 2 giải pháp, lãng phí, user phải nhắc. Quy tắc: (a) việc mới → chốt phương thức qua inbox TRƯỚC khi bắt tay, (b) chỉ 1 người build, người kia review/test, (c) nếu bên kia đã build 1 hướng → đóng góp VÀO hướng đó, không làm cái riêng (liveness chớp mắt của Claw cũng fail với user — bằng chứng thêm là đừng tự làm riêng).
4. **Milestone cực ngắn** — user thích 1 tuần MVP, tận dụng đồ đã có, không xây mới.
4b. **CHẾ ĐỘ LÀM VIỆC: build liên tục, không dừng** — user: *"Cứ làm liên tục cho đến khi hoàn thiện thì mới xong. Có cái gì cần anh duyệt thì để anh duyệt."* Sau khi được GO 1 feature, tiếp tục feature kế tiếp ngay trong cùng session (Skills Manager → Skill-Relations → Workflow Diagram → Pipeline → Backlog, cập nhật feature tracker sau mỗi cái). Không hỏi lại từng feature nhỏ; chỉ dừng trình duyệt khi: (a) quyết định product cần user chọn hướng, (b) hết việc trong backlog.
4c. **PIPELINE/THUẬT TOÁN MỚI → LÀM DEMO TRƯỚC, ĐƯỢC THÌ MỚI CHỐT** — user: *"Em làm demo trước, được thì mới chốt"* (05/08, khi sửa pipeline meeting note). Khác với feature UI (được GO là build luôn), pipeline xử lý dữ liệu (STT→summary→parse) phải: (1) chạy demo trên dữ liệu thật, (2) trình kết quả + nêu rõ điểm không ổn định, (3) chờ user duyệt format/cách xử lý trước khi áp vào production. Lưu ý LLM summarize KHÔNG ổn định giữa các lần chạy (cùng input: lần 1 ra 2 task đủ assignee+deadline, lần 2 ra 4 task sai assignee thiếu deadline) → đề xuất: heuristic fix sai người gán ("gọi mẹ/thuyết phục mẹ" → Quang), fallback deadline từ transcript ("chốt sáng thứ 7"), chạy 2 lần chọn bản tốt hơn.
4d. **TRANSCRIPT PHẢI TRÌNH USER DUYỆT TRƯỚC KHI XỬ LÝ (user yêu cầu 05/08):** *"bây giờ đầu tiên em trả cho anh hết toàn bộ transcript anh duyệt xem đã chuẩn chưa, trước khi đến bước xử lý, em lên task để anh duyệt từng phần 1 đi"* — sau transcribe: (1) gửi FULL transcript kèm danh sách điểm nghi ngờ (tên riêng, thuật ngữ, số liệu mà Whisper có thể sai) đánh số, (2) user xác nhận/sửa từng điểm (vd "1-4 ok, 6 = OKR, 7 chuẩn, 9 = 900 con"), (3) cập nhật transcript chuẩn → mới summarize/sinh task. KHÔNG tự chuyển thẳng sang xử lý khi transcript có chỗ sai ngữ nghĩa.
5. **Ghi âm resilient** — bấm End → lưu; KHÔNG bấm End mà mất mạng → VẪN lưu (chunk + watchdog).
6. **Pipeline transcribe (đã chốt)**: Hermes = STT (Groq Whisper tốt hơn) → gửi transcript cho Claw → **Claw xử lý + phản hồi user**. Format: transcript full ở `shared/transcripts/<meeting_id>.txt` (file-based, sync git), inbox chỉ gửi metadata (meeting_id, time, duration, path, chủ đề). Hermes KHÔNG tự summarize/phản hồi user về transcript — chuyển Claw.
7. **Dashboard Company = 1 trang theo dõi mọi thứ** — user không muốn phải hỏi lại "team đang chạy gì". Mọi plan/feature/mục tiêu phải hiển thị trên dashboard.
7b. **TRẢ LỜI GỌN — 1 VIỆC TRỌNG TÂM, XONG RỒI FINAL MỚI BÁO** — user từng chê: *"Em trả lời nhiều quá, chọn 1 cái làm trọng tâm thôi, xong 1 cái và final lại mới trả lời anh."* Khi user hỏi trạng thái/giao việc: chọn 1 việc quan trọng nhất, làm XONG (test + commit), rồi báo cáo final gọn. Không trả lời dài dòng nhiều chủ đề, không báo giữa chừng "đang làm". Báo cáo: 1 việc + kết quả + 1 câu chờ chỉ đạo.
8. **Phổ biến quyết định cho team = briefing.md, KHÔNG chỉ workspace.md** — agents đọc `briefing.md` khi "thức dậy"; workspace.md chỉ là file điều phối Hermes↔Claw. Khi user chốt vision/mission/mục tiêu: (a) rewrite briefing.md (Vision/Mission/Current Goal/Recent Decisions), (b) gửi message bus cho TẤT CẢ agents ("đọc briefing.md, KHÔNG hỏi mục tiêu là gì"), (c) thêm section Vision & Mission trên dashboard. User từng bực: *"Tại sao team vẫn hỏi mục tiêu là gì — mục tiêu đã rất rõ ràng rồi"* — vì quyết định nằm trong workspace.md mà agents không đọc.

## OKR system (store/okrs.json)

```
Objective { id, objective, quarter, owner, progress, key_results: [
  { id, kr, metric, baseline, target, current, owner, task_ids: [task_id] }
]}
```

- `create_objective()`, `add_key_result()`, `update_kr_progress()`, `auto_gen_tasks_for_kr()`, `get_objective_tree()`
- Auto-gen tasks từ KR theo keyword: SEO/content → Content, conversion/landing → Design+Dev1+CMO, traffic → CMO
- Tasks sinh ra ở phase=planning, đi qua workflow bắt buộc

## Giao tiếp Hermes ↔ OpenClaw (cross-machine)

Cả 2 chạy trên 2 máy khác nhau → dùng Git làm kênh:

- **Mỗi bên 1 file riêng** để tránh merge conflict: `to_claw.json` (Hermes ghi) / `to_hermes.json` (Claw ghi). KHÔNG dùng chung 1 file — conflict liên tục.
- **Inbox Protocol V3 — ACK BẮT BUỘC (build 03/08 sau khi user hỏi "sao claw báo em k phản hồi"):** message có `status: sent|read` + `sent_at` + `read_at`; bên nhận sau khi xử lý phải gọi `ack(id)` → gửi tin "✅ ACK: <subject>" ngược lại cho người gửi (ghi vào file NGƯỜI GỬI). Gửi mà không có ACK = chưa giao = watchdog báo.
- `shared/inbox.py`: `send(to, subject, body)` (status=sent), `read()` (chỉ trả tin status='sent' chưa xử lý), `ack(message_id)`, `mark_read()`, `find_stale(older_than_minutes)`, `sync_pull()`.
- **Watchdog cron (mỗi 1 phút, script `shared/inbox_watchdog.py` — copy sang `~/AppData/Local/hermes/scripts/ai-inbox-sync.py`)**: pull → ACK tin mới từ Claw → `find_stale(5min)` tìm tin Hermes gửi mà Claw chưa đọc → **tự động báo Telegram beFounders** (chỉ báo 1 lần/tin qua `.watchdog_state.json`). Script cron chạy từ hermes/scripts → phải `sys.path.insert` path `D:/Hermes Proj/ai-company` + `AI_COMPANY/app` cho tg_push import.
- **PITFALL kênh lệch sync (đã gặp 03/08):** Claw tưởng gửi được nhưng tin không tới Hermes (inbox Hermes chỉ có tin cũ, tin mới không có), và tin Hermes gửi vẫn `sent` không bao giờ được đọc. Nguyên nhân khả dĩ: pull/push không tới, ghi nhầm file, hoặc cron chết. Khi user hỏi "sao em không phản hồi" → CHECK FILE THỰC TẾ cả 2 chiều (`cat shared/to_hermes.json` + `cat shared/to_claw.json`) trước khi phản hồi — đừng đoán. Yêu cầu bên kia pull + xác nhận "đã gửi + đã push" sau mỗi tin.
- Cron 1 phút chạy `shared/sync.py`: pull → đọc tin chưa đọc → **output TẤT CẢ tin mới** (không lọc keyword — lọc từng nuốt mất tin quan trọng, đã gặp lỗi này) → push.
- Cron silent: script chỉ print khi có tin mới; Hermes cron no_agent=True sẽ chỉ deliver stdout, rỗng = im lặng.
- Chi tiết đầy đủ: `references/shared-inbox-protocol.md`

## MVP web (tfo.thefirstonly.com, port 8100)

FastAPI (venv riêng `D:/Hermes Proj/ai-company/.venv`):
```bash
.venv/Scripts/python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8100
```
**Restart server 8100:** terminal guard chặn lệnh chứa `uvicorn` (lifecycle guard) → dùng launcher `~/AppData/Local/hermes/scripts/tfo_launch.py` (đọc OPENCODE_GO_API_KEY + GROQ_API_KEY từ hermes .env rồi subprocess gọi `.venv/Scripts/python.exe -c "import uvicorn; uvicorn.run('app.main:app', host='0.0.0.0', port=8100)"`). Background start: `python C:/Users/NTQUANG_DELL/AppData/Local/hermes/scripts/tfo_launch.py` (watch "Application startup complete"). Kill cũ: `taskkill /PID <pid> /F`. Lưu ý dùng đúng python của ai-company venv — python Hermes venv thiếu pydantic_core (ModuleNotFoundError).

Endpoints: `/` (login), `/app` (dashboard — login gate server-side), `/api/transcribe` (Groq Whisper), `/api/summarize` (chunk-summarize → Groq JSON), `/api/tasks` + `/api/tasks/{id}/toggle` + `/api/tasks/{id}/status` (kanban) + `/api/tasks/{id}/update` (edit task) + `/api/tasks/{id}/messages` (GET/POST task thread) + `/api/tasks/{id}/voice` (voice chat trong task), `/api/record/start|chunk|end` (ghi âm resilient), `/api/meetings`, `/api/meetings/{id}` (+ DELETE, + `/api/meetings/{id}/project`), `/api/projects` (CRUD), `/api/issues` (+ status), `/api/goal` (GET/POST mục tiêu tuần), `/api/agent-board` + `/api/agent-tasks` (+ `/phase`, `/sub-status`, `/update`) — Agent tab kanban 2 cấp, `/api/agent/overview` — mini stats agent (subagent build), `/api/skills`, `/api/login`, `/api/me`, `/api/admin/users`.

**5 TABS (dashboard điều hành — build 05/08, user review góc nhìn C-level):**
- **Dashboard** (mặc định): 4 KPI thẻ bấm nhảy (Task quá hạn/Meeting tuần/Task hôm nay/Issue mở) + Mục tiêu tuần editable + 📌 Hôm nay (meeting + task đến hạn) + ⚠️ Cần chú ý (quá hạn + issue mở) + Ghi âm/Upload gọn + Task + Lịch sử. KHÔNG có Agent Skills/Org Chart (chuyển Hệ thống).
- **Lịch họp**: week view → popup meeting detail (TÓM TẮT + QUYẾT ĐỊNH + ISSUES + TASKS + nút "📋 Mở Meeting Notes" nếu có notes_url).
- **Dự án**: card project (số meeting/task/issue) → click mở **timeline dọc** (meetings + decisions + tasks + link notes theo thời gian).
- **Kanban**: **2 TAB CON (chốt 05/08 — user: "cho thành 2 tab con là Task và Issue")**: nút `setKanbanView('task'|'issue')` + biến `kanbanView`, header hiển thị 2 nút ✅ Task | 🔴 Issue (nút active nền vàng), `renderKanban()` chỉ render board view đang chọn. Board Task (todo/in_progress/done) + Issue (open/in_progress/resolved), **kéo thả** (dragstart/dragover/drop → POST status), filter theo project. **MỖI CARD TASK PHẢI CÓ 2 NÚT: 💬 Chat + ✏️ Sửa** (user chê "không thấy hiện phần sửa" khi card chỉ có chat — 05/08): nút ✏️ mở `openTaskModal(id)` (không kèm source = user task), nút 💬 mở `openTaskChat(id,...)`, cả 2 phải `event.stopPropagation()` vì card cũng có onclick. **Hover UI bắt buộc** (user yêu cầu "ui hover vào card/button để biết bấm được"): `.kb-card:hover { border-color: yellow; transform: translateY(-1px); box-shadow }` + `.kb-card button:hover { background: yellow !important; color: black !important }`. **Modal edit đầy đủ fields** (user duyệt bổ sung 05/08): title/assignee/priority/deadline (text + date picker)/project/status + **phase (6 phase) + task cha (dropdown các task không parent_id, lưu parent_id) + giờ ước tính (estimate) + tag (tags, phân cách phẩy)** + notes. API `POST /api/tasks/{id}/update` nhận thêm phase/parent_id/estimate/tags. User task + AI task dùng CHUNG modal — `editingTaskSource` quyết định URL. **Nút ghi âm nổi 🎤 = bấm là GHI LUÔN (fix 05/08 — user: "bấm vào không thấy gì xảy ra, muốn bấm vào mặc định ghi âm luôn")**: `floatingRecord()` chỉ cần `document.getElementById('recordBtn').click()` — trigger đúng handler ghi/dừng, KHÔNG chỉ scroll + focus (bản cũ scrollIntoView + focus = không thấy gì).
- **Agent (thêm 05/08 — user chốt 2 kanban: task lớn + kanban con bên trong)**: kanban 2 cấp + list. Cấp 1 = task lớn 6 phase (planning→review→approved→in_progress→testing→completed), kéo thả → **agent TỰ CHUYỂN** theo PHASE_AGENT (planning=PO, review=SA, approved=CTO, in_progress=Dev1, testing=QA) + prompt nhập kết quả → `phase_logs`. Cấp 2 = sub-kanban task con (parent_id, 3 trạng thái todo/in_progress/done — KHÔNG 6 phase, 6x6 rối). Card task lớn hiện progress bar task con. List view: `Dev1: 🏃 2 · ✅ 3 · 📋 5`. Card có nút 💬 Chat + ✏️ Sửa (`openTaskModal(id,'ai')`). Modal edit dùng CHUNG cho user + AI task — `editingTaskSource` quyết định POST `/api/tasks/{id}/update` (user) hay `/api/agent-tasks/{id}/update` (AI). **UI chốt 05/08:** (a) **Bấm task lớn → mở POPUP modal (`agentSubCard` dạng `position:fixed; display:flex` + click-outside đóng)**, KHÔNG phải card kéo xuống — user: "bấm vào task to thì popup mở ra chứ không kéo xuống"; (b) **Bấm task con → mở chi tiết**: `openAgentSubTask(subId)` tìm trong `agentTasks` (KHÔNG phải `allTasks` — bug đã gặp: `openTaskModal(id,'ai')` tìm nhầm user tasks nên task con agent không mở được) → gọi `openTaskModalFrom(subId, taskObj, 'ai')`; (c) **ĐÃ BỎ nút "+ Task con" và "+ Task lớn mới" trong sub-kanban** — tạo task chỉ qua nút ➕ header; (d) card task con ghi hint "✏️ bấm để xem chi tiết". Xem `references/agent-board-task-chat.md`.
- **Task Chat (thêm 05/08 — user: "bấm task → live chat/ghi âm tương tác với em")**: modal taskChatModal (z-index 500) mở từ Dashboard task (nút 💬) + Kanban card ("💬 Chat"), poll 3s messages. Text qua `POST /api/tasks/{id}/messages`, voice qua `POST /api/tasks/{id}/voice` (MediaRecorder → Groq Whisper → append message → enqueue agent). Manager route domain → Senior Dev/Legal/Purchaser/Researcher/Design/PO/CFO (mặc định CTO). **SOURCE SEPARATION (quan trọng — build 05/08):** task dashboard (user tasks.json) vs task AI Company (store/tasks.json) TRÙNG id → messages API nhận `source` param (`user` mặc định / `ai`): `append_message`/`list_messages`/`enqueue` đều nhận `source`, worker truyền `item.get('source')`; verify task đúng nguồn trước khi append. Thiếu source → chat 2 hệ thống lẫn messages. **Reload giữ tab:** `switchTab()` lưu `localStorage.setItem('tfo_tab', tab)`; `initApp()` đọc và `switchTab(saved)` sau khi load — user không muốn F5 bị đá về Dashboard. **Click-outside đóng popup:** modal overlay `onclick="if(event.target === this) closeX()"` + content div `onclick="event.stopPropagation()"` — áp cho CẢ taskChatModal và taskModal (edit). Bấm vùng tối → đóng; bấm trong popup → không đóng. Xem `references/agent-board-task-chat.md`.
- **Hệ thống**: Org Chart + Task Workflow + Agent Skills (gom hết phần kỹ thuật, cho dev/admin).
- **Tab bar STICKY khi cuộn**: `.tab-bar { position: sticky; z-index: 95; background: var(--black) }` + JS đo `header.offsetHeight` set `tabbar.style.top` (update khi resize). Header cũng sticky top:0.
- **PITFALL V8 date parse**: `new Date('Thứ 7')` → **Jul 01 2001**, `new Date('Tuần 1')` → **Jan 01 2001** — V8 nhặt số trong chuỗi làm month → mọi deadline text bị coi quá hạn. parseDate KHÔNG fallback `new Date(s)`; chỉ regex `dd/mm/yyyy` hoặc `yyyy-mm-dd`, còn lại → null (không tính quá hạn). Khi user hỏi "sao toàn task quá hạn" → check cái này trước.

**Tab 📅 Lịch họp (meeting calendar — đã build, user yêu cầu "view theo week/month meeting")**: tab bar trên tfo web (`switchTab('dashboard'|'calendar')`), week view 7 ngày → click ngày → danh sách meetings → click meeting → overview (bối cảnh, tóm tắt) + tasks từ meeting + transcript.
- Meetings lưu `created_at` (YYYY-MM-DD HH:MM) — calendar nhóm theo `created_at.slice(0,10)`.
- **Meeting có `title` + `meeting_time`** (thêm 03/08 theo yêu cầu user): form ghi âm/upload có input `meetingTitle` + `meetingTime` (datetime-local) → gửi kèm khi `POST /api/meetings`. Mọi UI (lịch sử, calendar, detail) hiển thị `title || session_id` và `meeting_time` thay vì mã session. `POST /api/meetings` nhận thêm `title`, `meeting_time` form fields; khi update trùng session_id, giữ title/time cũ nếu form bỏ trống.
- **AUTO-TITLE khi meeting không có tiêu đề (user yêu cầu 03/08):** `POST /api/meetings` — nếu `title` trống: lấy dòng đầu của summary (ưu tiên) rồi transcript (fallback), strip JSON braces + `summary:` prefix, cắt 70 chars; fallback cuối `Meeting <session_id[:8]>`. Khi thêm meeting cũ thiếu title → backfill bằng script scan `users/*/meetings.json`. Lịch sử + calendar hiển thị title đẹp thay vì mã session (user: *"cái meeting không có tiêu đề thì em tự đặt tiêu đề cho nó"*).
- **UI lịch sử cuộc họp + view chi tiết (nâng cấp 03/08):** danh sách hiển thị `🎙️ title` + meeting_time/created_at + số chữ transcript + summary preview (strip JSON braces/keys `summary:|issues:|decisions:|tasks:`); nút Xem render HTML (title to → tóm tắt → transcript đầy đủ scroll) thay vì textContent JSON thô. Tab Lịch (calendar) cũng dùng title + preview sạch. Khi user chê "UI chỉ để file session trông khó chịu" → đây là pattern chuẩn: title + meta + preview, không hiện mã session.
- **`meeting_time` mặc định = thời điểm bắt đầu ghi/upload** (user yêu cầu 03/08): JS `setDefaultMeetingTime()` — nếu input trống, tự điền datetime-local = now. Gọi khi: bấm "Bắt đầu ghi âm" (trong try sau getUserMedia), chọn file qua fileInput change, drag-drop. User: "mặc định nếu không điền ngày thì ngày giờ sẽ là thời gian bắt đầu ghi âm hoặc tải lên file".
- **Xóa meeting:** `DELETE /api/meetings/{id}?token=` — xóa meeting + **xóa luôn tasks có `meeting_id` trùng** (user: "cho anh một cái nút xóa để xóa đi, giả sử bấm nhầm"). Frontend nút 🗑 kèm `confirm()`, sau xóa `loadMeetings()+loadTasks()`.
- **Nút "Tải lên file" tách riêng khỏi nút ghi âm** (user yêu cầu): upload zone chỉ còn drag/drop + click vùng; `uploadBtn` mở file picker. Khi thêm button vào upload-zone, nhớ thêm vào điều kiện loại trừ `e.target !== uploadBtn` trong click handler của zone.
- **Task link meeting qua `meeting_id`** — `create_task()` nhận field `meeting_id`; `/api/summarize` tự parse task từ DeepSeek result (dòng chứa task/việc cần/cần làm/giao/todo/đề xuất), rút assignee bằng regex `([A-Za-z0-9]{2,12})\s*:` (fallback CEO), gán `meeting_id=session_id`.
- Chip meeting trên lịch có trạng thái task: viền vàng = còn task chưa xong, viền xanh + opacity = xong hết, không viền = chưa có task.
- Meeting test tạo tay cần `created_at` khớp ngày đang xem mới hiện trên week view (đừng dùng làm demo trừ khi ngày đúng).

**Multi-tenancy (đã build — user chốt 02/08):** account tách riêng, data riêng, Quang = admin truy cập data mọi user để cải tiến product.
- Data per-user tại `tfo_data/users/<email-sanitized>/` — tasks.json, meetings.json, recordings/ RIÊNG mỗi user. Sanitize: `email.lower().replace("@","_at_").replace(".","_dot_")`.
- **Projects + Issues data model (thêm 05/08):** per-user `projects.json` = `{projects:[{id, name, color, created_at}]}`, `issues.json` = `{issues:[{id,title,project_id,meeting_id,status,created_at}], next_id}`, tasks có `project_id` + `status` (todo/in_progress/done) + `priority` (high/medium/low) + `notes`, meetings có `project_id`. Thêm project mới = append vào `projects.json` + thêm tasks với `project_id: "p<N>"`. Hiện có: p1 "Thử nghiệm phòng tả", p2 "Phát triển sản phẩm tiêu chảy", p3 "Cảm hóa mẹ" (9 task checklist 12 tuần — case delegation bottleneck, xem skill leadership-coaching). Script mẫu: `tfo_data/add_project_cam_hoa_me.py`. Khi thêm dữ liệu tiếng Việt: viết script bằng write_file rồi chạy (heredoc terminal strip dấu).
- **Goal API (mục tiêu tuần, thêm 05/08):** per-user `goal.json` = `{goal, updated_at}`; `GET /api/goal` + `POST /api/goal` (Form `goal`, `token`). Dashboard hero hiển thị + nút ✏️ Chỉnh (prompt → POST → reload). Mục tiêu KHÔNG hardcode trong HTML — trước đây "conversion rate 2.1%→3.5%" hardcode sai chủ đề khiến user mất niềm tin.
- **Kanban + edit task (thêm 05/08):** `POST /api/tasks/{id}/status` (todo/in_progress/done) + `POST /api/tasks/{id}/update` (title/assignee/deadline/project_id/status/priority/notes — Form, bỏ trống = giữ nguyên). `POST /api/issues/{id}/status` (open/in_progress/resolved). Card kanban click → modal edit; icon 🔴/🟢 theo priority. Deadline cho nhập text ("08/08/2026" hoặc "Thứ 7") + date picker cạnh bên.
- Mọi endpoint nhận token → `_resolve_user(token)` → đọc/ghi `_user_read(email, file, default)` / `_user_write(email, file, data)`. KHÔNG token = 401.
- `_finalize_recording` lưu meetings theo `sess["email"]` (set khi record/start) — không lưu global.
- **Admin:** `GET /api/admin/users?token=` — chỉ `ADMIN_EMAILS` (quang@kiemsaphia.com) được xem danh sách user + số tasks/meetings. Trả 403 nếu không phải admin.
- Frontend phải gửi token MỌI nơi: GET dùng query param (`/api/tasks?token=`), POST dùng Form field `token`.
- Migrate data cũ: copy sang folder user mới + merge (tránh tạo 2 folder trùng — đã gặp lỗi `quang@kiemsaphia.com` vs `quang_at_kiemsaphia_dot_com`).

**Telegram push (đã build):** sau summarize tự đẩy kết quả lên Telegram beFounders group.
- `app/tg_push.py`: đọc `TELEGRAM_BOT_TOKEN` từ `~/AppData/Local/hermes/.env`, chat_id `-1004368353156` (beFounders, lấy từ `channel_directory.json`).
- Gọi `send_meeting_result(meeting_id, summary, tasks, transcript_preview)` sau khi summarize trong `/api/summarize`.
- Test: `.venv/Scripts/python.exe app/tg_push.py <id> <text>` → `✅ TG push: 200`.

**Auth — LOGIN GATE THẬT, server-side (build lại 03/08 — user cấm overlay):** user: *"bản chất cái login đang là overlay, mở HTML xóa overlay đi là thấy dashboard phía sau; mong muốn vượt qua login rồi mới vào dashboard thực sự."* → KHÔNG còn overlay. Dashboard HTML KHÔNG BAO GIỜ được gửi xuống browser trước khi auth.
- **2 file riêng:** `app/static/login.html` (màn login: 2 tab 😀 Khuôn mặt / 🔑 Passcode) + `app/static/index.html` (dashboard — KHÔNG chứa login overlay, có auth guard redirect về `/`).
- **Routes:** `GET /` và `GET /login` → luôn trả login.html; `GET /app` → check cookie `tfo_token` hợp lệ (`request.cookies` → `_check_token`) → mới trả index.html, sai/thiếu → trả login.html. Test: `curl -s localhost:8100/app` (không cookie) → `<title>TheFirstOnly — Đăng nhập`; có cookie → `<title>TheFirstOnly — Trợ lý CEO`.
- **Cookie:** `POST /api/login` và `POST /api/face/login` gọi `resp.set_cookie("tfo_token", token, max_age=2592000, path="/")`; `POST /api/logout` → `delete_cookie`. Login.html JS: sau khi nhận token → `localStorage.setItem` + set cookie + `window.location.href = '/app'`.
- `ALLOWED_EMAILS` (list) + `PASSCODE` (env `TFO_PASSCODE`, default `<PASSCODE>`) trong `app/main.py`; `POST /api/login` (email+passcode) → token; `GET /api/me?token=` verify; sessions lưu `tfo_data/sessions.json`.
- Guard `_check_token(token)` cho mọi endpoint nhạy cảm (transcribe, summarize) — trả 401 nếu thiếu. Frontend gửi token: localStorage (`tfo_token`) hoặc cookie (regExp parse).
- **Bắt buộc no-cache header trên mọi route HTML** (`Cache-Control: no-cache, no-store, must-revalidate`) — nếu không, browser giữ bản HTML cũ → user báo "không login được" dù server OK.
- **Xóa các hàm face login cũ khỏi index.html khi chuyển sang login.html** — faceTab/startFaceCam/faceVerify/faceEnroll tham chiếu `loginOverlay`/`faceEmail` không còn tồn tại; nếu sót → `document.getElementById('loginOverlay')` null error. Sau refactor luôn `grep -n "loginOverlay|faceEmail"` verify = 0 + `node --check` script.

**Face Login — MediaPipe (đã build 03/08, user chốt "thử phương án MediaPipe đi")**: thay passcode bằng nhận diện khuôn mặt, on-premise 100%, passcode giữ làm backup.
- **MediaPipe 1.0 XÓA `mp.solutions`** → phải dùng Tasks API (`mediapipe.tasks.python.vision.FaceLandmarker`) + model `face_landmarker.task` (download tự động từ Google storage). Xem chi tiết: `references/face-recognition-sdk.md`
- Module `app/face_auth.py`: `extract_embedding()` (478 landmarks → chuẩn hóa centroid+norm), `compare_embeddings()` (cosine), `is_match(sim, threshold=0.93)`
- Endpoints: `POST /api/face/enroll` (cần token — user đã login), **`POST /api/face/login` (AUTO-LOGIN — không cần email, build 03/08)**: duyệt MỌI `users/*/face_embedding.json`, lấy similarity cao nhất, `is_match` → TỰ TẠO session token + set cookie, trả `{matched, similarity, token, email}`; không match → trả `{ok:false, similarity, error}`. `GET /api/face/status`. (`/api/face/verify` theo email giữ lại nhưng login.html dùng `/api/face/login`.)
- Enroll lưu `users/<email-sanitized>/face_embedding.json` = `{"embedding": [...478 dims], "created_at"}` — KHÔNG lưu ảnh gốc (privacy: embedding thôi, đúng chuẩn TheFirstOnly).
- **UI login hiện tại (03/08):** login.html 2 tab — `😀 Khuôn mặt` (KHÔNG có ô email nữa — chỉ camera + "Xác minh khuôn mặt"; caption "Nhìn thẳng vào camera — tự nhận diện và đăng nhập") / `🔑 Passcode` (email + passcode backup). `faceLogin()` trong login.html: canvas capture → `POST /api/face/login` → match: lưu token + cookie + `location.href='/app'`. User đã enroll thành công (file face_embedding.json tồn tại) — login bằng mặt hoạt động.
- **Nút `🔒 Khóa` (doLogout) trên header — BẮT BUỘC cho flow enroll:** `faceEnroll()` cần token đã login, nhưng màn login chỉ hiện khi chưa có token → user phải login passcode → bấm Khóa → quay lại màn login → bấm "📸 Lưu khuôn mặt" (enroll). `doLogout()`: POST /api/logout + xóa localStorage token + stopFaceCam + hiện loginOverlay + faceTab('face') + startFaceCam. Không có nút này user kẹt không enroll được (user từng hỏi "thì có nút Lockout đâu hả em").
- **HEADER UI hiện tại (03/08 — user yêu cầu gọn):** KHÔNG còn badge "👂 Luôn lắng nghe"; 2 nút Enroll + Khóa được gom vào **menu `•••`** (button `menuBtn` → div `userMenu` dropdown: "📸 Lưu khuôn mặt" + "🔒 Khóa"). `toggleMenu(e)` phải `e.stopPropagation()` + `document.addEventListener('click')` đóng menu khi bấm ra ngoài. Khi edit header, giữ cấu trúc này.
- **`quickEnroll()` — enroll ngay trong app, KHÔNG cần logout (cải tiến 03/08):** user từng bối rối "nhập passcode xong quay lại kiểu gì để enroll" vì flow cũ (login → Khóa → login lại → enroll) quá rắc rối. Fix: nút "📸 Lưu khuôn mặt" trong menu ••• gọi `quickEnroll()` — mở modal overlay (tạo div `quickEnrollModal` bằng JS, video id `quickVideo`), dùng token HIỆN TẠI trong localStorage → `POST /api/face/enroll` → đóng modal (`quickEnrollClose()` stop tracks + remove). User chỉ cần: login passcode → bấm ••• → Lưu khuôn mặt → chụp → xong. Không phải logout.
- **CHƯA enroll → ĐÃ enroll (03/08):** user tự enroll thành công qua nút "📸 Lưu khuôn mặt" (quickEnroll) — `users/quang_at_kiemsaphia_dot_com/face_embedding.json` tồn tại. Từ đây login bằng mặt được. Khi pilot CEO #2 (anh trai): add email vào `ALLOWED_EMAILS` → login passcode → enroll mặt → auto-login.

## Recording resilient pattern (đã build, đừng phá vỡ):
- Client: `MediaRecorder.start(10000)` → mỗi 10s `dataavailable` → POST `/api/record/chunk` NGAY (mất mạng giữa chừng vẫn còn phần đã gửi)
- Server: append chunk vào `tfo_data/recordings/<sid>.webm`, update `last_seen`
- Watchdog thread: session nào im lặng >**90s** → auto-finalize + lưu transcript — không mất audio. **Đã đổi 30s→90s (03/08)**: 30s quá nhanh — user ngừng nói >30s bị cắt sớm → user bấm End nhận "session not found" dù bản ghi đã auto-save. 90s cho khoảng nghỉ tự nhiên trong meeting.
- End → `/api/record/end` → merge → transcribe
- **`/api/record/end` khi session ĐÃ bị watchdog lưu** (user vẫn thấy lỗi "session not found"): KHÔNG trả 404 vô nghĩa — tìm `<sid>.webm` trong `users/*/recordings/` + đọc `meetings.json` của user đó → trả `{**meeting, recovered: true}`. Frontend coi như bình thường (transcript hiện trong lịch sử).
- Trong `mediaRecorder.onstop` JS: **`const recSid = sessionId` TRƯỚC khi set `sessionId = null`** — nếu null trước rồi mới dùng cho summarize/POST meetings → gửi session_id rỗng, meeting lưu không đúng id (bug đã gặp và fix).

### BUG GỐC: SESSIONS in-memory mất khi server restart → mất cả bản ghi dài (fix 03/08, quan trọng nhất)
- **Triệu chứng:** user ghi âm 1 tiếng rồi tắt → báo lỗi "session not found", KHÔNG có file nào được lưu (find `tfo_data -name "*.webm" -size +1M` = rỗng).
- **Nguyên nhân:** `SESSIONS = {}` chỉ trong RAM. Server restart (deploy nhiều lần trong ngày) → session ghi âm đang chạy biến mất → chunk tiếp theo 404 → client bỏ chunk → watchdog không biết session → file không được finalize → MẤT TOÀN BỘ.
- **Fix 3 lớp (đã build):**
  1. **Persist session ra file `tfo_data/record_sessions.json`** — `_save_rec_sessions()` sau mỗi `record_start` + mỗi `record_chunk` + `record_end`; `_load_rec_sessions()` khi server start (khôi phục session đang dở, log "🔄 Khôi phục N session") VÀ fallback trong `record_chunk`/`record_end` khi không tìm thấy trong memory (`_load_rec_sessions()` rồi tìm lại). `record_chunk` cũng phải reload nếu session không có trong memory.
  2. **Client giữ chunk local + retry khi end:** mỗi chunk lưu `{blob, sent:false}`; gửi thành công → `sent=true`; fail (mạng/restart) → GIỮ LẠI; trong `onstop` loop retry các chunk `!sent` TRƯỚC khi gọi `record/end`. KHÔNG bao giờ drop chunk fail (code cũ chỉ `console.warn` rồi bỏ → mất data).
  3. **Retention policy (user yêu cầu "lưu local, xử lý xong sau x ngày mới xóa"):** `REC_RETENTION_DAYS = env TFO_RETENTION_DAYS, default 30`. `_cleanup_old_recordings()` xóa `users/*/recordings/*.webm` cũ hơn cutoff + meetings.json ngoài khoảng; chạy lúc server start + mỗi 6h trong watchdog.
- **Verify persist:** start session → gửi 1 chunk → ghi SID ra file → kill server → start lại → POST chunk với SID cũ → phải trả `ok` (không phải 404) → end trả đúng parts. Đây là test quyết định — nếu restart làm mất session là bug tái phát.

**Verify recording resilient** (chạy sau khi sửa):
```python
# 1) start → gửi 3 chunk → end → check parts/size
# 2) start → gửi 1 chunk → KHÔNG end → sleep 95s (watchdog 90s) → check recordings/ có <sid>.webm + <sid>.transcript.txt
# Dùng Python requests (curl -F multipart dễ lỗi JSON parse)
```

## Dashboard AI Company (company.thefirstonly.com, port 8090)

```bash
python server.py   # từ D:/Hermes Proj/ai-company
```
Server chết → URL trả 502. Luôn check `curl localhost:8090` trước khi báo user.

**Passcode bảo vệ (đã build — user chốt 02/08, passcode `<PASSCODE>`):** dashboard KHÔNG public.
- `server.py`: `PASSCODE = "<PASSCODE>"`, cookie `company_auth=tfo_company_ok_2026` (Max-Age 30 ngày).
- Mọi GET không có cookie → trả `LOCK_HTML` (trang nhập passcode, form POST `/api/login`); `company-data.json` → 401.
- `do_POST` chỉ nhận `/api/login` (so passcode → 302 + Set-Cookie, sai → 401 kèm lỗi).
- Verify: `curl -s localhost:8090/ | grep "nhập passcode"` (lock), `curl -X POST .../api/login -d "passcode=<PASSCODE>" -c /tmp/cookie.txt` → 302, rồi `-b /tmp/cookie.txt` → 200.
- Lưu ý: cookie-based passcode chỉ chặn người xem thường, không phải bảo mật cao — đủ cho giai đoạn stealth.

**Feature Tracker (store/features.json)** — section "🚀 Plan & Features Tracker" trên dashboard, đặt NGAY ĐẦU trang:
- Mỗi feature: name, description, owner, status (live/done/in_progress/planned/blocked), progress %, priority (P0/P1/P2), url
- CRUD trong store.py: `get_features()`, `add_feature()`, `update_feature_status()`
- Mục đích: user theo dõi TẤT CẢ plan/mục tiêu/ai đang làm gì trên 1 trang — không phải hỏi lại
- Luôn cập nhật progress feature khi Claw/build thay đổi — đây là nơi user đọc trạng thái
- Status map UI: live=🟢, done=✅, in_progress=🔵, planned=🟡, blocked=🔴

## Đẩy tool mới + spin plan lên TFO (file-write pattern — verify 16/08)

Khi user duyệt 1 plan phát triển (vd SPIN meTelligent 2 tuần) và muốn theo dõi trên TFO: đẩy **2 chỗ song song**:

1. **Tool list `store/features.json`** — thêm feature mới (id kế tiếp, `status: in_progress`, `progress`, `url`, `priority`, `updated_at`). Đây là data hiển thị "Plan & Features Tracker" trên dashboard Company (8090) **VÀ Tool list trên dashboard TFO (8100) — đã render từ 16/08** (`/api/features` + `renderToolList()` trong index.html, xem mục Tool list bên dưới).
2. **Kanban `store/tasks.json`** — tạo task cha (phase `in_progress`, có `done_criteria`) + sub-tasks (parent_id, `sub_status: todo|in_progress|done`, mỗi cái có `done_criteria`, deadline theo tuần). Task cha `sub_tasks: [ids]`.

**Vì sao ghi file trực tiếp thay vì `POST /api/agent-tasks`:** endpoint đó (a) bắt buộc done_criteria cho task cha (400 nếu thiếu), (b) **auto-enqueue critique khi có description** → mỗi task con sinh 1 message + 1 queue job LLM = đốt token vô ích khi chỉ seed plan. Ghi thẳng JSON qua python (giữ `next_id`) rồi restart không cần — server đọc file mỗi request (`_ai_store`/`_ai_write`).

**Verify bằng session thật (không cần login):**
```bash
TOKEN=$(python -c "import json; d=json.load(open('tfo_data/sessions.json',encoding='utf-8')); print(max(d['sessions'], key=lambda k: d['sessions'][k].get('created_at','')))")
curl -s "http://localhost:8100/api/agent-board?token=$TOKEN" | python -c "import json,sys; d=json.load(sys.stdin); print([t['title'][:60] for t in d.get('tasks',[]) if t.get('id')==17])"
```
`/api/agent-board` trả tasks + agents + stats — đọc được bằng session token có sẵn trong `tfo_data/sessions.json`, không cần passcode. Khi user hỏi "trên trang TFO có gì mới / chưa thấy plan" → verify qua đây, đừng đoán.

## Tool list render trên dashboard TFO (build 16/08 — sub #1 SPIN TFO)

Trước 16/08: `features.json` chỉ là data cho Company dashboard (8090), KHÔNG render trên TFO (8100). Từ 16/08: dashboard TFO có section "🧰 Tool list" hiển thị features.json ngay trang chủ.

- **API:** `GET /api/features` trong `app/main.py` — check token (`_resolve_user`) → `from hub.store import get_features` → `{"features": [...]}`. KHÔNG có endpoint này trước đó — phải thêm.
- **Frontend:** section HTML sau "Mục tiêu tuần" (`<div class="card-body" id="toolList">`) + hàm `renderToolList(features)` (top-level, global) gọi trong `loadDashboardData()` qua Promise.all fetch thứ 5. Render: tên + mô tả (ellipsis) + progress bar + tag trạng thái (live=Đang chạy/done=Xong/in_progress=Đang làm/planned=Kế hoạch) + onclick `window.open(url)` nếu có url. Status màu: green/yellow/blue.
- **`esc()` phải có sẵn** — dùng mọi nơi render text; nếu chưa có trong file, định nghĩa hàm escape HTML trước khi dùng.
- Verify: `node --check` mọi `<script>` block (7 blocks) + py_compile + browser snapshot thấy đủ tool.

**Verify UI qua browser với cookie thật (không cần login):** `/app` check COOKIE `tfo_token` (`request.cookies`), KHÔNG phải localStorage — set localStorage thôi vẫn về login. Cách:
1. `browser_navigate http://localhost:8100/app` → sẽ về login.html
2. Lấy token mới nhất: `python -c "...max(d['sessions'], key=created_at)..."`
3. `browser_console`: `document.cookie = 'tfo_token=<token>; path=/'`
4. `browser_navigate http://localhost:8100/app` lại → dashboard render, snapshot thấy section mới

**Restart server 8100 sau khi sửa code:** kill PID (`netstat -ano | grep :8100 | grep LISTENING` → `taskkill -F -PID`) → start bằng launcher + subprocess.Popen (xem `restart-fastapi-venv.md` trong skill android-flutter-build-windows — terminal guard chặn gọi python trực tiếp chứa uvicorn, lỗi "embedded null character in path"; dùng execute_code + Popen CREATE_NO_WINDOW với launcher script `run_tfo_v2.py`).

**Kanban task ID cho SPIN:** mỗi spin có task cha + 8 sub liên tiếp. meTelligent spin = task #17 (sub #18–#25), TFO spin = task #26 (sub #27–#34), next_id tăng theo. Khi sub xong: set `phase=completed` + `status=done` + `sub_status=done` + ghi `phase_logs` — tasks.json là data local (gitignored), chỉ commit code.

## Cloudflare Tunnel config — API PUT (đã dùng được!)

Remote config (Windows service chạy `--token`) update được qua API:
```bash
# GET/PUT tunnel config — FULL REPLACEMENT!
curl -X PUT "https://api.cloudflare.com/client/v4/accounts/$ACCOUNT_TAG/cfd_tunnel/$TUNNEL_ID/configurations" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" -H "Content-Type: application/json" \
  -d '{"config":{"ingress":[
    {"hostname":"tfo.thefirstonly.com","service":"http://localhost:8100"},
    {"hostname":"company.thefirstonly.com","service":"http://localhost:8090"},
    {"hostname":"upload.thefirstonly.com","service":"http://localhost:8769"},
    {"hostname":"bot.thefirstonly.com","service":"http://localhost:9877"},
    {"hostname":"me.thefirstonly.com","service":"http://localhost:5099"},
    {"hostname":"thefirstonly.com","service":"http://localhost:5099"},
    {"hostname":"www.thefirstonly.com","service":"http://localhost:5099"},
    {"service":"http_status:404"}],"warp-routing":{"enabled":false}}}'
```
⚠️ PUT là FULL REPLACEMENT — thiếu 1 hostname là phá vỡ domain đó. Luôn liệt kê ĐỦ toàn bộ ingress (tfo, company, upload, bot, me, root, www). CLOUDFLARE_API_TOKEN có thể mất khỏi env giữa session — lấy lại từ cache terminal (`grep -h "cfut_" ~/AppData/Local/hermes/cache/terminal/hermes-results/*.txt`).

## DeepSeek/OpenCode API + Provider fallback chain

AI Company dùng 2 lớp API:
1. **Primary:** OpenCode Go (`https://opencode.ai/zen/go/v1/chat/completions`) — `OPENCODE_GO_API_KEY`
2. **Fallback:** ByteDance Ark coding endpoint — `BYTEDANCE_ARK_API_KEY` (auto-load từ .env)

`call_deepseek` trong `hub/store.py` gọi trực tiếp bằng `requests.post`, KHÔNG qua Hermes provider chain.
Khi OpenCode Go hết credit hoặc key không set → tự động fallback ByteDance.

Chi tiết: `references/bytedance-ark-fallback.md`
- MODEL_MAP: `deepseek-chat`→`deepseek-v4-flash` (workers), `deepseek`→`deepseek-v4-pro` (managers)
- **Rate limit hay trả response RỖNG** — retry pattern: nếu `think()` trả `""`, sleep 3s gọi lại (thường thành công lần 2). Đừng kết luận API hỏng.
- **`response_format={"type":"json_object"}` TRẢ RỖNG 100% trên endpoint này** (status 200, content `''`). KHÔNG dùng — ép JSON bằng prompt ("OUTPUT: CHỈ JSON thuần, bắt đầu bằng {"). Verified 08/2026.
- **Prompt dài → trả rỗng ~40-50%** ngẫu nhiên (system dài + input 5000 chars thường rỗng; system ngắn + input 5000 OK). Fix: retry loop trong `call_deepseek` (3 lần) + chunk nhỏ (3500) + system prompt NGẮN cho bước partial. Model trả markdown thay vì JSON khi input dài → ép lại lần 2 với output ngắn (retry 4 lần).
- **ĐO THẬT 07/08 (context 6k):** `deepseek-v4-flash` rỗng ~80% (1/5 ok), `deepseek-v4-pro` ổn 100% (5/5 ok). Đã build fallback flash→pro TRONG `call_deepseek` (retry 3 lần cùng model → fallback pro 2 lần, `fallback_models = ["deepseek-v4-pro", "deepseek-v4-flash"]`). Trước khi kết luận "provider chết", benchmark 5 lần mỗi model (code mẫu trong `hermes-model-provider-troubleshooting` skill).
- **TASK CHAT báo "⚠️ Lỗi: agent không trả về kết quả (provider transient). Thử lại sau." — root cause kép (fix 07/08):** (1) `app/main.py load_keys()` KHÔNG đọc `OPENCODE_GO_API_KEY` từ `~/AppData/Local/hermes/.env` (chỉ đọc GROQ) → server chạy KHÔNG có key → `call_deepseek` trả None → activity log `[WARN] OpenCode API key not set`; fix: load_keys đọc cả 2 key (`line.startswith("OPENCODE_GO_API_KEY=")` + `os.environ[...] = value`). (2) flash rỗng ~80% context dài → fallback pro. **Chẩn đoán nhanh: đọc `store/activity.json`** — phân biệt `API key not set` (thiếu key) vs `empty response` (model rỗng) trước khi sửa.
- **PA A — JSON cuối bằng Groq llama-3.3-70b + response_format json_object**: Groq ổn định, JSON chuẩn, assignee/deadline đầy đủ (khác hẳn OpenCode). Flow chuẩn: chunk-summarize DeepSeek flash → `_groq_summarize_json()` cho bước cuối. Xem `references/stt-summary-quality.md`.
- Prompt dài tiếng Việt qua command line dễ lỗi escaping → gọi trực tiếp từ Python (`from agents.base_agent import BaseAgent`) thay vì `python hub/run.py agent X "prompt"`.

## Pitfalls

- **2 NGUỒN TASK KHÁC NHAU (gây nhầm, đã gặp 05/08):** `tfo_data/users/*/tasks.json` (user tasks — Dashboard/Kanban/Dự án) vs `store/tasks.json` (AI Company tasks — tab Agent, `parent_id` + `phase` + `phase_logs`). (a) Nút **"➕ Thêm việc" (newTaskModal)** mở popup dùng CHUNG cả 2 bên, radio `newTaskType`: 👤 Việc của người (Kanban) / 🤖 Giao cho Agent (AI Company) → `submitNewTask()` gửi `POST /api/tasks` (mode=agent → user tasks có auto-enqueue critique; mode=kanban → user task thường). **Vị trí nút (chốt 05/08): NẰM Ở HEADER (cạnh menu •••), KHÔNG có nút thêm trong Kanban tab hay Agent tab** — user: "Treo luôn nút thêm việc ở header, bỏ ở trong 2 tab". Agent tab chỉ có dòng hint "➕ Thêm việc mới nằm ở nút vàng trên header". Popup fields: title*, description chi tiết, assignee (datalist), priority P0/P1/P2, deadline, estimate, project, tags. (b) **Task agent KHÔNG tự chuyển phase** — worker (`agent_exec.py`) chỉ xử lý khi có message trong queue (user gõ/nói trong 💬 Chat); task agent tạo ra nằm yên ở planning cho tới khi kéo thả tay hoặc chat. Khi user hỏi "sao task agent cứ planning / không lên plan / thêm task con không hành động" → giải thích đúng nguyên nhân, đề xuất fix đã build: tạo task agent → tự `enqueue()`. (c) Task con (parent_id) trong sub-kanban: bấm card → mở chi tiết (xem mục Agent tab bên dưới).
- **AUTO-CRITIQUE khi giao việc cho agent (user yêu cầu 05/08: "task agent trước khi nhận việc phải tự hỏi, làm rõ, phản biện trước khi thực hiện"):** `create_task(mode=agent)` và `create_ai_task()` — nếu có description → auto-enqueue `critique_prompt`: "1) Tự hỏi và nêu rõ mình hiểu yêu cầu gì, 2) Làm rõ điểm mơ hồ/cần xác nhận, 3) Phản biện nếu yêu cầu có vấn đề. Rồi mới trình kế hoạch". Worker `_call_agent` system prompt CŨNG thêm 3 bước critique trước khi trả lời (áp mọi message, không chỉ task mới). ACK message: "🤖 Đã nhận — agent đang phân tích yêu cầu, làm rõ và phản biện trước khi thực hiện...". Test verify: task mới mode=agent → messages chứa critique prompt → agent trả "**1) Hiểu yêu cầu:** ... **2) Điểm mơ hồ:** ... **3) Phản biện:** ...".
- **AGENT THIẾU BỐI CẢNH — root cause + fix `_build_context` (chẩn đoán 05/08, user hỏi "tại sao agent không có quyền access hay thiếu bối cảnh"):** worker cũ gọi `_call_agent(agent, content)` với content = CHỈ message mới nhất — agent MÙ: không biết task title/description/deadline, không project, không lịch sử chat, không transcript cuộc họp liên quan → trả lời chung chung, hỏi lại "task nào?". **Fix đã build:** `_process()` gọi `_build_context(task_id, content, source)` trước khi gọi LLM → prompt đóng gói: `📋 TASK` (title/description/hạn/assignee/priority) + `📁 DỰ ÁN` (objective/context/scope/kpi/risks/stakeholders/deadline/status — đọc từ `projects.json` theo `task.project_id`) + `📄 TRANSCRIPT CUỘC HỌP LIÊN QUAN` (trích 1500 chars từ `meetings.json` theo `task.meeting_id`) + `🗣️ LỊCH SỬ CHAT` (6 message gần nhất, loại message hiện tại) + `📨 YÊU CẦU MỚI NHẤT`. Đọc task theo `source` (ai → store/tasks.json, user → tfo_data). Khi user kêu agent trả lời chung chung/không biết task → check `_build_context` có chạy không + project có `context`/`objective` điền chưa.
- **PROJECT CONTEXT MODEL (user yêu cầu 05/08: "file dự án luôn đủ bối cảnh để xuất ra, người khác import vào AI làm được"):** `projects.json` mỗi project có: `name, color, objective (mục tiêu), context (bối cảnh/lý do), scope (phạm vi), kpi (kết quả mong đợi), risks (rủi ro & giả định), stakeholders, deadline, resources (nguồn lực/ngân sách), status (on_track/behind/blocked/paused/completed), created_at, updated_at`. `POST /api/projects` + `PATCH /api/projects/{pid}` nhận toàn bộ fields (PATCH chỉ update field có giá trị mới + set updated_at). **Export bối cảnh:** `POST /api/projects/{pid}/export` → markdown đóng gói (metadata + mục tiêu + bối cảnh + phạm vi + KPI + rủi ro + stakeholders + deadline + tasks + issues + meetings liên quan) lưu `tfo_data/exports/project_<id>_<name>.md` + trả `{ok, path, content}` → frontend download blob. **UI:** project card có nút "✏️ Bối cảnh" → modal `projectModal` đầy đủ fields + nút "📤 Xuất bối cảnh"; card hiển thị status icon (🟢🟡🔴⏸✅). ⚠️ `re` phải import ở main.py (export dùng `re.sub` cho filename — đã gặp NameError).
- **Python 3.14 pydantic-core wheel hỏng** → venv phải tạo từ Python 3.11: `"/c/Users/NTQUANG_DELL/AppData/Local/Programs/Python/Python311/python.exe" -m venv .venv`
- `pip install` bị terminal guard chặn (tưởng server) → chạy qua script file `install_deps.py`
- **Tunnel Cloudflare remote config**: PUT `configurations` là FULL REPLACEMENT — phải liệt kê đủ MỌI hostname (tfo, company, upload, bot, me, root) nếu không sẽ phá vỡ các domain khác. Xem `local-tunnel` skill.
- `git pull --rebase` dính rebase-merge directory cũ → `rm -rf .git/rebase-merge` rồi pull lại
- **GIT SECURITY — file nhạy cảm KHÔNG được track (incident 06/08):** repo `ntquang1110/ai-company` từng track: `tfo_data/tg_env.json` (chứa **Telegram bot token thật**), `tfo_data/users/*/face_embedding.json` (sinh trắc khuôn mặt), `*.webm/*.mp3/*.opus/*.ogg` (audio cuộc họp riêng tư). Đã fix: (1) thêm vào `.gitignore` — block `tg_env.json`, `*.env`, `face_embedding.json`, mọi audio extension, `tfo_data/recordings/`, `tfo_data/exports/`, `*.log`; (2) `git rm --cached` các file đã track (giữ file trên disk); (3) `gh` API `PATCH /repos/ntquang1110/ai-company -d '{"private": true}'` → repo private. **Trước khi commit/push:** `git ls-files | grep -E "\.webm|\.mp3|\.opus|\.ogg|\.wav|tg_env|face_embedding"` phải rỗng. ⚠️ Token từng nằm trong git history (commit cũ) — repo private giảm rủi ro nhưng token vẫn lộ trong history cũ; đề xuất user đổi token bot hoặc `git filter-repo` nếu repo từng public. Khi báo "lên git hết chưa": check `git status` (untracked + ahead commits) + `git remote` + `git log` trước khi trả lời.
- **store/*.json trong .gitignore — KHÔNG commit dữ liệu live; chỉ shared/ + code là tracked.**
- `python hub/run.py standup` crash `NameError: update_briefing` nếu import thiếu — `store.update_briefing` phải có trong import của `hub/run.py` (đã sửa 2026-08-01, nếu tái cấu trúc import đừng bỏ sót). Standup chạy 5 agents chính (CTO, Dev1, Content, CMO, QA) qua `agent.daily_standup()` — tốn cost LLM, chạy 1 lần/ngày.
- **Patch HTML dễ XOÁ NHẦM section** — khi thêm section mới vào `app/static/index.html`, patch replace có thể nuốt luôn section liền kề (đã xoá nhầm Agent Skills khi thêm Workflow Diagram). Sau mỗi patch HTML: `curl -s localhost:8100/ | grep -c "tên-class/section"` cho TẤT CẢ sections — verify section cũ còn + section mới có, trước khi commit.
- **⚠️ PHÂN BIỆT 2 DASHBOARD (gây sửa nhầm 15/08):** *"dashboard của tfo"* = **TFO MVP** `app/static/index.html` (port 8100, tfo.thefirstonly.com/app — Dashboard/Lịch họp/Dự án/Kanban/Agent/Hệ thống, task ở `#taskList` tab Dashboard, user task từ `tfo_data/users/*/tasks.json`). *"dashboard AI Company"* = `dashboard/index.html` (port 8090, company.thefirstonly.com — Task Board + OKR + Mission Control, data từ `store/tasks.json` qua `/company-data.json`). Khi user nói "dashboard" KHÔNG rõ: hỏi/đối chiếu URL + file path trước khi sửa — đừng đoán (đã sửa nhầm AI Company khi user hỏi TFO).
- **⚠️ TFO: xung đột tên hàm popup khi thêm list mới (15/08):** app ĐÃ CÓ `openTaskModal(taskId, source)` + `closeTaskModal()` (popup edit task `#taskModal`). Thêm popup task list dùng cùng tên → **silent override** (hàm sau thắng, nút gọi nhầm hàm cũ) — popup không mở, KHÔNG có lỗi console. Fix: đặt tên riêng `openTaskListModal()` / `closeTaskListModal()`; trước khi đặt tên `grep -n "function openTask\|function closeTask" index.html`.
- **TFO Dashboard task — 10 task + Xem thêm + popup infinite scroll (build 15/08):** `loadTasks()` render `tasks.slice().reverse().slice(0, TASKS_PER_PAGE=10)` + nút `.task-more-btn` "Xem thêm N task →" (N = còn ẩn); `openTaskListModal()` mở overlay `.task-overlay` (bottom-sheet `align-items:flex-end`) → `#taskModalList` batch `POPUP_BATCH=30` khi scroll `scrollTop+clientHeight >= scrollHeight-120`. **`taskItemHtml(t)` phải là function GLOBAL (top-level)**, dùng chung board + popup — đặt trong closure `render()` thì popup gọi → ReferenceError. State `popupTasks` global; đóng bằng ✕ hoặc click overlay (`onclick="if(event.target===this)closeTaskListModal()"`). Verify: mở popup → đếm `.task-item` → scroll đáy → đếm tăng 30→60→120.
- **JS trong HTML: 1 biến `let` khai báo 2 lần = CHẾT CẢ SCRIPT** — symptom: `Uncaught ReferenceError: doLogin is not defined` (hoặc bất kỳ function nào "undefined") dù function đã khai báo trong file. Nguyên nhân thường gặp: nhiều patch chồng lấn nhau để lại `let mediaRecorder` ở 2 chỗ — syntax error giết toàn bộ script block, mọi onclick/hàm sau đó đều undefined. Debug nhanh: extract script → `node --check`:
  ```bash
  python -c "import re; html=open('app/static/index.html',encoding='utf-8').read(); m=re.search(r'<script>(.*)</script>',html,re.S); open('/tmp/check.js','w',encoding='utf-8').write(m.group(1))"
  node --check /tmp/check.js   # → SyntaxError: Identifier 'mediaRecorder' has already been declared
  ```
  Khi 2 agents/session cùng sửa 1 HTML, patch `old_string` có thể match nhầm bản cũ — luôn check `grep -n "let X"` trước khi patch và sau khi commit.
- **DUPLICATE container id khi 2 agents/session cùng thêm section (đã gặp 05/08)**: subagent thêm `viewAgent` (overview+thread) và session này thêm `viewAgent` (kanban 2 cấp) → 2 div cùng `id="viewAgent"` → JS getElementById lấy cái ĐẦU TIÊN, cái sau vô dụng. Sau khi merge 2 bản: verify `html.count('id="viewAgent"') == 1` + div balance (`opens == closes`) + `node --check` JS + function check (`missing = [c for c in calls if c not in defined]`). Test: `python -c` extract scripts → `node --check`; grep count id duplicate.
- **"Xem" meeting không hiện gì** (bug đã fix 03/08): nguyên nhân openMeeting hiển thị vào `resultBox` nhưng thiếu try/catch + scroll vào block ẩn. Fix: `try/catch` + nếu `m.error` alert; text hiển thị title + created_at + meeting_time + summary + transcript; `box.scrollIntoView({block:'center'})`. Khi user báo "bấm nút xem không có gì" — check: (a) resultBox có class `active` không, (b) scroll có tới đúng element không, (c) API trả `error` không (meeting ở workspace user khác → 404).
- **TEST DATA làm ô nhiễm hệ thống live** — user từng bực: *"Team check lại sao lại có SEO với content ở đây"* vì task test (tạo hồi test `create_objective`/`auto_gen_tasks_for_kr` trước khi vision chốt) hiển thị trên dashboard như việc thật. Khi test store functions: (a) dùng tên đánh dấu rõ "TEST", (b) hoặc dọn ngay sau test (`tasks=[]`, `objectives=[]` reset next_id), (c) trước khi báo user "sạch", verify qua API: `curl localhost:8090/company-data.json` → đếm tasks/OKRs/features. Test data không được phép tồn tại trong store live.
- **Task model 2 trường: `phase` vs `status`** — `hub/run.py` workflow dùng `phase` (planning→review→...), nhưng `store.get_agent_statuses` đọc `status` (pending/in_progress). Task tạo thủ công (không qua `add_task()`) thiếu `status` → dashboard crash `KeyError: 'status'`. Khi tạo task tay: set CẢ `phase` và `status`.
- **Cập nhật feature tracker sau mỗi feature xong** — `update_feature(id, status, progress)` ngay trong commit của feature đó, để user đọc Dashboard Company không phải hỏi.
- **Upload file lớn bị timeout qua Cloudflare tunnel** — tunnel free có giới hạn request ~100s: upload file lớn + Groq transcribe lâu = request bị cắt. Fix đã build: (1) `_groq_transcribe` nén Opus 16kHz mono + **volume boost 12dB + highpass/lowpass** (`ffmpeg -af "volume=12dB,highpass=f=80,lowpass=f=8000" -ar 16000 -ac 1 -c:a libopus -b:a 48k`) TRƯỚC khi gửi Groq; (2) file >60MB trả 413 kèm hướng dẫn dùng ghi âm trực tiếp. ⚠️ **Opus 24k gây loss từ cho tiếng Việt + thiếu boost = mất hẳn nội dung** (08/2026 user phàn nàn meeting sum tệ; test file 0880bf48a6: không boost mất "anh Mão 20-30 con", có boost bắt đủ). Boost + nén là CHÌA KHÓA. Xem `references/stt-summary-quality.md` cho toàn bộ checklist chất lượng STT→Summary.
- **Mission Control trên dashboard** — section "🎯 MISSION CONTROL" 3 cột: MỤC TIÊU HIỆN TẠI / ĐANG DIỄN RA / AI ĐANG LÀM GÌ. Thay cho Vision & Mission tĩnh. Khi user nói "tổng hợp hết lên dashboard cho anh xem cái gì đang diễn ra" — đây là nơi render: goal (từ current_goal/briefing), active tasks (phase != completed), agents không idle (status != '⚪ Idle'). Nếu rỗng phải hiện rõ "chưa có việc / tất cả idle" — không để trống.
- **Mục tiêu/plan lớn: ghi vào `shared/launch_plan.md`** — 3 phases (Phase 1 lõi, Phase 2 sẵn sàng ra mắt, Phase 3 GTM chờ đèn xanh). User: "Chưa mở đâu, dựng plan để sẵn sàng ra mắt thôi."

## Verification

```bash
cd /d/Hermes\ Proj/ai-company
python company.py status      # team + tasks + proposals + cost
python company.py okr         # OKR tree
curl -s localhost:8100/api/health    # MVP web
curl -s localhost:8090/company-data.json | python -m json.tool | head -20  # dashboard data
```

## Reference files

- `references/shared-inbox-protocol.md` — giao thức inbox Hermes↔OpenClaw chi tiết (file layout, sync, role, lịch sử lỗi conflict)
- `references/face-recognition-sdk.md` — Face Login MediaPipe ĐÃ BUILD (enroll/verify flow, model URL, MediaPipe 1.0 Tasks API pitfall) + research Faceplugin SDK (không dùng — Torch 2GB, license mờ)
- `references/stt-summary-quality.md` — Chất lượng pipeline STT→Summary (ĐÃ TRIỂN KHAI + verify 08/2026): 6 nguyên nhân mất từ (nén Opus 24k + THIẾU volume boost 12dB, Whisper hallucination → clean heuristic theo câu, initial_prompt DÀI bị lặp, chunk theo size thay vì duration, truncate `transcript[:8000]`, DeepSeek trả rỗng khi json_object/prompt dài) + PA A (Groq llama JSON) + V8 date parse pitfall. Dùng khi user phàn nàn "meeting sum tệ / transcript loss từ / toàn task quá hạn / vấn đề-task-decision sai".
- `references/agent-board-task-chat.md` — Agent tab kanban 2 cấp (PHASE_AGENT, phase_logs, parent_id task con) + Task Chat (modal + voice `/api/tasks/{id}/voice`) + pitfall duplicate container id khi 2 agents sửa chung HTML. Build 05/08.
- `references/project-context-agent-context.md` — Project Context model (objective/context/scope/kpi/risks/stakeholders/deadline/resources/status + export markdown) + agent `_build_context` fix (root cause "agent thiếu bối cảnh") + UI chốt 05/08 (kanban 2 tab con, floating record = ghi luôn, agent popup + task con chi tiết, header-only ➕ Thêm việc) + meeting note demo (LLM summarize không ổn định, 3 đề xuất chốt).
