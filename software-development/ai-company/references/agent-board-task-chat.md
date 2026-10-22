# Agent Board (kanban 2 cấp) + Task Chat — build 05/08/2026

## Agent Board — kanban 2 cấp (user chốt: "2 kanban: task lớn → kanban bên trong")

User yêu cầu: kanban task lớn có các phase, mỗi phase agent KHÁC NHAU thực hiện và
log lại kết quả phase (Planning → vấn đề/bối cảnh/task/quyết định), task con liên kết
task gốc (Tính năng A → con 1 plan, con 2 BA/SA, con 3 testcase, con 4 thực thi).

### Data model — store/tasks.json (AI Company tasks, KHÁC tfo_data users tasks.json)

```python
task = {
    "id": 10,
    "title": "Tính năng A: Meeting → Task tự động",
    "assignee": "PO",           # agent đang phụ trách phase HIỆN TẠI
    "phase": "planning",        # planning→review→approved→in_progress→testing→completed
    "priority": "P0",
    "parent_id": None,          # task con → id task gốc; task gốc = None
    "sub_status": "todo",       # task con: todo/in_progress/done (KHÔNG 6 phase)
    "phase_logs": [             # log kết quả TỪNG phase
        {"phase": "planning", "agent": "PO", "result": "...", "at": "2026-08-05 18:00"}
    ],
    "sub_tasks": [],
}
```

Chốt thiết kế với user: task lớn = 6 phase (luồng sản phẩm), task con = 3 trạng thái
(todo/in_progress/done) — KHÔNG bắt task con qua 6 phase (6x6 ma trận rối).

### Phase → agent mặc định (kéo card = TỰ CHUYỂN assignee — user chốt "Agent tự chuyển nhé")

```python
PHASE_AGENT = {
    "planning": "PO", "review": "SA", "approved": "CTO",
    "in_progress": "Dev1", "testing": "QA", "completed": "QA",
}
```

### Endpoints (app/main.py)

| Endpoint | Chức năng |
|----------|-----------|
| `GET /api/agent-board` | Gom tasks + agents (từ agents/profiles.json) + stats per agent (total/done/running) + phase_agent/phase_label |
| `POST /api/agent-tasks` | Tạo task lớn hoặc task con (Form: title, description, assignee, `parent_id`, priority) |
| `POST /api/agent-tasks/{id}/phase` | Chuyển phase → auto-log + tự chuyển assignee theo PHASE_AGENT |
| `POST /api/agent-tasks/{id}/sub-status` | Task con: todo/in_progress/done |
| `POST /api/agent-tasks/{id}/update` | Edit AI task: title/assignee/deadline/priority/notes/estimate/tags |

Stats per agent: đếm task theo `assignee` — completed→done, còn lại→running.
Kéo thả phase → prompt "Kết quả phase ... (log lại)" → ghi phase_logs.

### Frontend (tab Agent, viewAgent)

- Header: agent filter + 2 nút chuyển view 📊 Kanban / 📋 List (`setAgentView('kanban'|'list')`)
- Kanban cấp 1: 6 cột phase, card task lớn hiện progress bar task con (x/y + %)
- Bấm card task lớn → `openAgentSub(id)` mở sub-kanban: log các phase đã qua (tl-item) + 3 cột task con kéo thả
- List: `Dev1: 🏃 2 · ✅ 3 · 📋 5` — bấm agent → openAgentDetail (toàn bộ task)
- Có sẵn từ subagent: mini-dashboard stats (agPlanning...) + thread chat (`/api/agent/overview`) — HỢP NHẤT, không xóa
- `loadAgentOverview()` (subagent, /api/agent/overview) giữ chỉ stats/alerts; board render bởi `loadAgentBoard()` (em, /api/agent-board) — tránh 2 nguồn render đè nhau

## Task Chat — tương tác với em trong từng task (user: "bấm task → live chat/ghi âm")

### Backend

```python
@app.post("/api/tasks/{task_id}/voice")
async def post_task_voice(task_id, file: UploadFile, token):
    # lưu webm tạm → _groq_transcribe(tmp, force_compress=True) → append_message(user)
    # → append ACK agent → agent_pool.ensure + enqueue → trả transcript
```

- `POST /api/tasks/{id}/messages` + `GET` (đã có từ subagent — dùng agent_exec: Manager route domain → agent AI Company)
- `POST /api/tasks/{id}/voice` (mới): voice → Groq Whisper (pipeline boost/Opus sẵn) → append user message → enqueue agent

### Frontend — modal taskChatModal (z-index 500, cao hơn taskModal 400)

- Mở từ: Dashboard task (nút 💬 + click task-info), Kanban card (nút "💬 Chat"), Agent card (nút 💬 + ✏️ Sửa)
- Poll 3s `loadChatMessages()` → messages render bubble (user vàng phải / agent surface2 trái)
- 🎤 `toggleChatVoice()`: MediaRecorder → blob webm → POST voice → transcript hiện như message user
- Ai trả lời: Manager route domain → Senior Dev/Legal/Purchaser/Researcher/Design/PO/CFO (mặc định CTO) — 8 domain regex trong agent_exec.py DOMAIN_AGENTS

### SOURCE SEPARATION — user task vs AI task (quan trọng, build 05/08)

Task dashboard (tfo_data/users/*/tasks.json) và task AI Company (store/tasks.json) **TRÙNG id**
(cả 2 bắt đầu từ 1) → chat phải tách namespace, nếu không messages 2 hệ thống lẫn nhau.

- `POST/GET /api/tasks/{id}/messages` + `POST /api/tasks/{id}/voice` nhận Form/query `source` (`user` mặc định, `ai` cho task AI Company)
- `agent_exec.py`: `append_message(email, task_id, role, content, agent="", source="user")` + `list_messages(..., source)` + `enqueue(..., source)` — message lưu kèm field `source`; list filter theo source
- Worker `_process()`: `source = item.get("source", "user")` → truyền vào append_message khi ghi ACK + response
- Verify task tồn tại theo source: `source=ai` → `_ai_store("tasks.json")`; `source=user` → `_user_read(email, "tasks.json")`
- Frontend: `openTaskChat(taskId, title, meta, source)` set `chatSource`; mọi fetch messages/voice gửi kèm source; Agent card gọi `openTaskChat(id, title, meta, 'ai')`

### Click-outside đóng popup (user: "bấm ra ngoài là thoát")

```html
<div id="taskChatModal" onclick="if(event.target === this) closeTaskChat();" ...>
  <div onclick="event.stopPropagation();" ...>  <!-- content — bấm trong KHÔNG đóng -->
```

Áp cho CẢ taskChatModal và taskModal (edit). Verify: `html.count("event.target === this") == 2`.

### Reload giữ tab (user: "reload thì ở lại đúng tab đang xem")

```js
function switchTab(tab) { ...; try { localStorage.setItem('tfo_tab', tab); } catch(e){} }
function initApp() {
  ...;
  const saved = localStorage.getItem('tfo_tab');
  if (saved && ['dashboard','calendar','projects','kanban','agent','system'].includes(saved)) switchTab(saved);
}
```

### Modal edit task — dùng chung user + AI task (build 05/08)

- Trường: title, assignee, priority (high/medium/low), deadline (text + date picker), project_id, status, **phase** (planning→completed), **parent_id** (task cha dropdown), **estimate** (4h, 1d), **tags** (phân cách phẩy), notes
- `let editingTaskSource = 'user'` — `openTaskModal(taskId, source)`; `saveTaskEdit()` POST `/api/tasks/{id}/update` (user) hay `/api/agent-tasks/{id}/update` (AI)
- Backend: `/api/tasks/{id}/update` thêm Form phase/parent_id/estimate/tags; `/api/agent-tasks/{id}/update` (mới) nhận title/assignee/deadline/priority/notes/estimate/tags → `_ai_write`
- User task thêm field: `phase`, `parent_id`, `estimate`, `tags` (lưu vào tfo_data tasks.json)

### Pitfall — 2 agents/session sửa chung 1 HTML → duplicate container id

Sibling subagent thêm `viewAgent` (overview + thread) và em thêm `viewAgent` (kanban 2 cấp)
→ 2 div cùng id="viewAgent" → JS getElementById lấy cái ĐẦU TIÊN, cái sau vô dụng.
Phải: xóa bản trùng, hợp nhất nội dung (giữ cả stats + thread + kanban 2 cấp), rồi
verify `html.count('id="viewAgent"') == 1` + div balance + `node --check` JS.
