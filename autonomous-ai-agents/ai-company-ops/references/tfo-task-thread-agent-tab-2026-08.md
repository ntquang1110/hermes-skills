## Task-thread + Tab "Agent" trong TFO (2026-08, anh Quang chốt định hướng — ĐÃ BUILD + TEST 2026-08-05→06)

Anh muốn TFO thành nơi giao việc liên tục theo từng task, kiểu Trello: rất nhiều task, agent phản hồi riêng từng task, có mini dashboard để hiểu anh.

### ĐÃ BUILD — kanban 2 cấp + task chat + agent context (anh duyệt "em chiến đi")

**Tab "Agent" hiện có 2 view (nút 📊 Kanban | 📋 List trên header tab):**
- **Kanban 2 cấp:** Cấp 1 = task lớn theo 6 phase (`planning → review → approved → in_progress → testing → completed`), kéo thả card qua phase → **agent tự chuyển** (Planning=PO, Review=SA, Approve=CTO, Implement=Dev1, Test=QA) + prompt nhập kết quả phase → ghi vào `phase_logs`. Cấp 2 = task con (parent_id) chỉ 3 trạng thái `todo/in_progress/done` — sub-kanban mở khi bấm card task lớn. Card task lớn hiện progress bar (x/y task con done).
- **List view:** thống kê per agent — `Dev1: 🏃 2 · ✅ 3 · 📋 5` + task hiện tại, bấm agent → xem toàn bộ task.
- **Task Chat (💬) mở từ MỌI task** (dashboard task, kanban card, tab Agent card): popup chat riêng từng task, poll 3s, có **🎤 ghi âm** (MediaRecorder → `/api/tasks/{id}/voice` → Groq transcribe → append message → enqueue agent). Agent trả lời trong chính thread task đó.
- **"➕ Thêm việc" = 1 nút DUY NHẤT trên header** (cạnh menu •••) — popup điền đủ trường (title, description, assignee, P0/P1/P2, deadline, estimate, tags, project) + radio chọn 👤 người (kanban) / 🤖 agent (AI Company). KHÔNG treo nút thêm việc trong từng tab (anh yêu cầu bỏ — 1 nơi duy nhất).

### ⚠️ source=user vs source=ai — 2 hệ thống task TÁCH BIỆT (pitfall trọng yếu)

- **User tasks** (`tfo_data/users/<email>/tasks.json`) — dashboard/kanban.
- **AI Company tasks** (`store/tasks.json`) — tab Agent, id TRÙNG với user tasks.
- Mọi API messages/voice/chat phải nhận `source` (`user`|`ai`) và verify task theo đúng source, nếu không: chat task id 1 ở tab Agent lẫn vào chat task id 1 ở dashboard.
- `append_message(email, task_id, role, content, agent, source)` + `list_messages(email, task_id, source)` — message có field `source`.
- `enqueue(email, task_id, sender, content, source)` — worker ghi response với source đúng.
- Tab Agent card: `openTaskChat(id, title, meta, 'ai')`; dashboard/kanban: `openTaskModal(id)` / `openTaskChat(id, ...)` không source (mặc định user).

### ⚠️ Worker phải ghi ĐÚNG file theo source — task AI không đổi phase (fix 2026-08-12, test thật)

Triệu chứng: task AI Company treo `planning` mãi dù agent có xử lý, plan không bao giờ xuất hiện. Nguyên nhân: `AgentWorker._set_task_status()` + `_set_task_assignee()` ban đầu **chỉ ghi vào user tasks.json** (`tfo_data/users/<email>/tasks.json`) kể cả khi source="ai" → `store/tasks.json` (AI Company) không bao giờ đổi phase.

**Fix (`app/agent_exec.py`):**
- `_set_task_status(task_id, status, source)` + `_set_task_assignee(task_id, agent, source)` — source="ai" → ghi `store/tasks.json`; source="user" → ghi user dir.
- **Plan xong → tự chuyển phase:** trong `_set_task_status`, nếu `status == "done"` và `t.get("phase") == "planning"` → `t["phase"] = "review"` (task AI). Sau khi worker viết plan, task tự nhảy sang review — Quang thấy plan trong thread + card ở cột Review.
- **Flash câm → fallback pro:** `_process` gọi `_call_agent(agent, context)` → response rỗng thì retry `_call_agent("CTO", context, force_pro=True)` → vẫn rỗng thì `_call_agent("PO", context, force_pro=True)`. `_call_agent` có param `force_pro=False` → model `deepseek-v4-pro`. Trước fix: flash trả rỗng ~80% prompt dài → queue item `status=error` + log `LLM call failed: Expecting value: line 1 column 1 (char 0)` → task treo vĩnh viễn.

### ⚠️ Task seed thẳng vào store → agent KHÔNG BAO GIỜ thức dậy (fix 2026-08-12)

Triệu chứng: 16 task tạo thẳng `store/tasks.json` (seed script, cùng timestamp) → không đi qua `create_ai_task` → **không auto-enqueue** → agent không biết có việc → không ai viết plan → treo planning. Worker chỉ chạy khi có message vào thread (`enqueue`).

**Recipe đánh thức task planning cũ — xem `references/dod-and-worker-fixes-2026-08.md`** (script enqueue "viết PLAN" + ⚠️ race khi enqueue bằng script trong lúc worker pool đang chạy → queue JSON bị corrupt "Extra data"; cách chạy đúng: dừng server → reset queue → enqueue → start server → `WorkerPool().ensure(email)` standalone → chờ worker xử lý).

### ⚠️ Agent "mù bối cảnh" — worker phải build context (fix 2026-08-06, test thật)

Triệu chứng: agent trả lời chung chung, hỏi lại "task nào?", thiếu thông tin thực tế. Nguyên nhân: worker chỉ gửi message mới nhất cho LLM, KHÔNG có task context, lịch sử, project, transcript.

**Fix: `_build_context(task_id, content, source)` trong `AgentWorker._process`** — đóng gói trước khi gọi LLM:
```
📋 TASK #id: title | description | deadline | assignee | priority
📁 DỰ ÁN (nếu task có project_id): mục tiêu, bối cảnh, phạm vi, KPI, rủi ro, stakeholders, deadline, status
📄 TRANSCRIPT CUỘC HỌP LIÊN QUAN (nếu task có meeting_id): trích 1500 chars
🗣️ LỊCH SỬ CHAT: 6 message gần nhất
📨 YÊU CẦU MỚI NHẤT CỦA QUANG: <content>
```
Test thật: hỏi "tóm tắt dự án đang làm gì, KPI, rủi ro" → agent trả lời ĐÚNG bối cảnh project p1 (Thử nghiệm phòng tả, rủi ro cám chưa xác thực, pháp lý) — trước fix thì không.

### Auto-critique khi giao việc cho agent (anh yêu cầu: "task agent trước khi nhận việc phải tự hỏi, làm rõ, phản biện")

- `create_task(mode=agent)` + `create_ai_task` (có description) → enqueue với critique_prompt:
  "Trước khi thực hiện: 1) Tự hỏi và nêu rõ mình hiểu yêu cầu gì, 2) Làm rõ điểm mơ hồ/cần xác nhận, 3) Phản biện nếu yêu cầu có vấn đề. Rồi mới trình kế hoạch."
- Worker prompt cũng ép critique: "TRƯỚC khi trả lời/thực hiện: nêu 1) hiểu yêu cầu, 2) điểm mơ hồ, 3) phản biện, rồi mới đưa kế hoạch".
- Test thật: PO trả lời đúng 3 bước (Hiểu yêu cầu → Điểm mơ hồ → Phản biện) trước khi đề xuất.

### ⚠️ JS Date parsing — V8 nhặt số trong chuỗi làm month (pitfall rất dễ dính)

`new Date('Thứ 7')` → **Jul 01 2001**; `new Date('Tuần 1')` → **Jan 01 2001**; `new Date('Thứ 7 (mùng 8)')` → Jul 2001. V8 parse tiếng Việt linh tinh — nhặt số 7/1 làm month. **KHÔNG BAO GIỜ fallback `new Date(s)` cho deadline text** ("Thứ 7", "Tuần X" = mốc tương đối → KHÔNG tính quá hạn).

```js
// Chỉ parse ngày CỤ THỂ; "Thứ 7"/"Tuần X" → null (không quá hạn, không due-today)
const parseDate = d => {
  if (!d) return null;
  const s = String(d).trim();
  let m;
  if ((m = s.match(/^(\d{1,2})\/(\d{1,2})\/(\d{4})$/))) { const dt = new Date(+m[3], +m[2]-1, +m[1]); return isNaN(dt)?null:dt; }
  if ((m = s.match(/^(\d{4})-(\d{2})-(\d{2})(?:[ T].*)?$/))) { const dt = new Date(+m[1], +m[2]-1, +m[3]); return isNaN(dt)?null:dt; }
  return null;
};
```
Triệu chứng: "toàn task quá hạn" — deadline "Thứ 7"/"Tuần 1" bị parse thành 2001 < hôm nay.

### Project model đầy đủ bối cảnh (2026-08-06, anh yêu cầu "file dự án luôn có đủ bối cảnh để export → AI import làm được")

`projects.json` mở rộng: `objective, context, scope, kpi, risks, stakeholders, deadline, resources, status` (on_track/behind/blocked/paused/completed) + `updated_at`. UI modal ✏️ Bối cảnh trên project card (click card mở detail timeline, nút ✏️ mở modal edit).

**`POST /api/projects/{pid}/export`** — sinh markdown đóng gói: metadata + mục tiêu + bối cảnh + phạm vi + KPI + rủi ro + stakeholders + deadline/nguồn lực + Tasks + Issues + Meetings liên quan. File lưu `tfo_data/exports/project_<id>_<name>.md`, trả content → frontend download. Đưa file này cho AI bất kỳ = AI nắm toàn bộ dự án.

### UI patterns chung (2026-08-06, anh yêu cầu)
- **Popup đóng bằng bấm ra ngoài:** overlay `onclick="if(event.target === this) closeX()"` + inner div `onclick="event.stopPropagation()"`.
- **Reload giữ tab:** `switchTab()` lưu `localStorage.setItem('tfo_tab', tab)`; `initApp()` đọc lại và `switchTab(saved)`.
- **Tab bar sticky:** `.tab-bar { position: sticky; top: <header height>; z-index: 95; background: var(--black) }` — set top bằng JS đo `header.offsetHeight` + resize listener.
- **Hover affordance:** `.kb-card:hover { border-color: var(--yellow); transform: translateY(-1px); box-shadow: ... }` + `.kb-card button:hover { background: var(--yellow); color: var(--black) }`.
- **Kanban 2 tab con Task/Issue:** trong cùng 1 tab Kanban — 2 nút `setKanbanView('task'|'issue')` render riêng board (không hiện cả 2 cùng lúc). State `kanbanView` biến global.
- **Nút ghi âm nổi bấm = GHI LUÔN** (không scroll+focus như trước — anh nói "bấm không thấy gì xảy ra"): `floatingRecord()` → `document.getElementById('recordBtn').click()` — chạy đúng logic ghi/dừng của nút chính.
- **Bấm task con agent phải mở chi tiết:** `openTaskModal(id)` chỉ tìm trong `allTasks` (user) — task agent nằm `agentTasks` nên không tìm thấy → không mở. Fix: `openTaskModalFrom(taskId, taskObj, source)` nhận task object trực tiếp; `openAgentSubTask(subId)` tìm trong `agentTasks` rồi gọi. Mở modal edit từ task con agent = `openAgentSubTask`.
- **Bỏ nút "+ Task con" / "+ Task lớn" trong sub-kanban** (anh yêu cầu) — tạo task tập trung ở nút ➕ Thêm việc header, không nhân bản nút ở nhiều nơi.

### ⚠️ Sibling agent edit conflict — duplicate viewAgent (pitfall 2026-08-06)

Khi nhiều agent/session cùng sửa `app/static/index.html`, patch có thể tạo 2 container `id="viewAgent"` (subagent thêm bản cũ + mình thêm bản mới) → JS getElementById lấy cái ĐẦU → bản mới chết im. Sau mỗi patch lớn: `grep -c 'id="viewAgent"'` phải = 1, đếm ID duplicate toàn file, cân bằng div, `node --check` JS.

### Giai đoạn đầu (2026-08-05) — thread engine gốc
- Queue per-user `tfo_data/users/<email>/task_queue.json` + messages `task_messages.json` + `WorkerPool` 3 thread daemon/email + `route_agent()` regex-first + `call_deepseek` theo persona. API: `POST/GET /api/tasks/{id}/messages`, `GET /api/agent/overview`, `POST /api/tasks` nhận `description` + status mặc định `planning`. Chạy nền độc lập (PowerShell Start-Process) + nằm trong watchdog-all-ports (port 8100).

### ⚠️ mode=agent vs mode=kanban — agent CHỈ thực thi task được giao (anh chốt 2026-08, sau khi thấy tab Agent hiện hết mọi task)

Anh sửa: "bản chất là anh giao cho agent việc gì thì mới vào task của agent thôi, còn việc nào của anh hay người khác thì để ở kanban thôi, chứ agent không thực thi cho anh những task kia được". Đây là **1 bảng task chung, nhưng phân loại theo NGƯỜI THỰC THI**:

- Mỗi task có field `mode`: `"agent"` (agent thực thi — vô tab Agent, auto-enqueue) | `"kanban"` (việc của người — agent KHÔNG đụng, chỉ hiện kanban).
- Task tạo từ **tab Agent** (`createAgentTask()` frontend gửi `mode=agent`) → agent nhận + xử lý thread.
- Task tạo từ **kanban** / sinh từ summarize cuộc họp / task cũ → mặc định `mode=kanban`, agent không bao giờ claim.
- **`create_task` API nhận `mode: Form("kanban")` mặc định** — chỉ khi `mode == "agent"` mới gọi `append_message` + `enqueue` (xem main.py).
- **`/api/agent/overview` và tab Agent render PHẢI filter `mode == "agent"`** — nếu quên, tab Agent hiện cả task của người và overview đếm sai (test thật: task kanban → messages = 0, overview total chỉ đếm agent task).
- Task cũ thiếu field `mode` khi migrate → set `mode: "kanban"` (script loop qua tasks.json).
- Không có khái niệm "agent bận thì task vào kanban" — task là agent hay không do anh giao, không tự suy diễn.

## ⚠️ LLM KHÔNG đáng tin cho domain routing — regex-first là chuẩn (2026-08, test thật)

Khi build Tab Agent, `route_agent()` ban đầu gọi DeepSeek để chọn agent theo domain → **sai 3/4 test thật** (hợp đồng follow-up → Design thay vì Legal; "Nghien cuu postbiotics" → Content thay vì Researcher; "Phan tich dong tien" → CTO thay vì CFO). LLM không ổn định cho việc chọn 1 trong 9 agent cố định.

**Fix đã verify 8/8 đúng:** regex deterministic TRƯỚC, LLM chỉ là fallback cuối:
1. `DOMAIN_AGENTS` regex có CẢ bản có dấu + không dấu (user gõ không dấu rất thường): `hợp đồng|hop dong|dieu khoan|điều khoản|luat|luật|chấm dứt|phạt vi phạm|boi thuong...` → Legal; `nghien cuu|nghiên cứu|postbiotic|patent|sáng chế...` → Researcher; `bug|loi|lỗi|fix|deploy|database|server` → Senior Dev...
2. **Bẫy regex: `post` trong Content pattern nuốt "postbiotics"** → Researcher. Không dùng từ quá ngắn/generic (`post`, `mua` — "mua" match cả hợp đồng mua bán). Ưu tiên từ khóa dài hơn + specific.
3. LLM fallback chỉ khi regex không khớp — chấp nhận 1 call tốn token, không dùng cho routing thường.
4. Test route không cần LLM: `OPENCODE_GO_API_KEY=""` chạy → regex path chạy, verify từng input domain.
5. **Bẫy "thread" → Content (12/08):** prompt yêu cầu agent viết plan kiểu "Trình plan vào thread này" chứa từ "thread" → regex Content (`content|bài viết|thread|social|marketing`) nuốt → route nhầm sang Content thay vì PO/PM/QA. Fix: thêm rule ưu tiên TRƯỚC `DOMAIN_AGENTS`: `re.search(r"viết plan|viet plan|viết kế hoạch|viet ke hoach|lên plan|len plan|plan thực hiện|plan thuc hien|viết bản plan", content)` → return "PO". Khi viết prompt đánh thức agent, tránh từ khóa regex của agent khác (hoặc thêm rule ưu tiên).
