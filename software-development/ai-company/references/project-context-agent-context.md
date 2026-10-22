# Project Context + Agent Context + UI fixes (05/08/2026)

Session detail cho 3 cụm việc trên tfo web (ai-company): (1) Project Context model
+ export, (2) agent `_build_context` fix, (3) UI chốt kanban/agent/record.

## 1. Project Context Model (user: "file dự án luôn đủ bối cảnh, import vào AI làm được")

`projects.json` (per-user) mỗi project:
```
{ id, name, color,
  objective, context, scope, kpi, risks, stakeholders,
  deadline, resources, status, created_at, updated_at }
```

- `POST /api/projects` — nhận toàn bộ fields (status default on_track)
- `PATCH /api/projects/{pid}` — nhận toàn bộ fields, CHỈ update field có giá trị mới
  (`if v:`), set `updated_at` khi có thay đổi. status validate whitelist.
- `POST /api/projects/{pid}/export` — markdown đóng gói:
  metadata (id/status/updated) + Mục tiêu + Bối cảnh + Phạm vi + KPI + Rủi ro +
  Stakeholders + Deadline/Nguồn lực + Tasks (từ tasks.json theo project_id) +
  Issues (từ issues.json) + Meetings liên quan (từ meetings.json theo project_id).
  Lưu `tfo_data/exports/project_<id>_<sanitized-name>.md`, trả `{ok, path, content}`.
  Frontend download qua Blob + `URL.createObjectURL`.

**PITFALL:** `re` phải import ở top main.py (`import os, sys, json, uuid, subprocess, time, re`)
— export dùng `re.sub` cho filename, thiếu import → NameError 500.

**Frontend:** project card có nút "✏️ Bối cảnh" (`openProjectModal(pid)` — stopPropagation vì
card onclick mở detail) + status icon map `{on_track:'🟢', behind:'🟡', blocked:'🔴',
paused:'⏸', completed:'✅'}`. Modal `projectModal` (z-index 460, click-outside đóng) đầy đủ
fields + nút "💾 Lưu dự án" (saveProject: PATCH nếu editingProjectId else POST) + nút
"📤 Xuất bối cảnh" (exportProject → download). `addProjectPrompt()` → `createProjectModal()`.

## 2. Agent thiếu bối cảnh — root cause + `_build_context` (fix 05/08)

**Triệu chứng (user):** "agent giao việc trong task / chat trong task lại không có quyền
access hay thiếu bối cảnh" — trả lời chung chung, hỏi lại "task nào?".

**Root cause:** `AgentWorker._process()` gọi `_call_agent(agent, content)` với content =
chỉ message mới nhất từ queue. Agent KHÔNG thấy: task title/description/deadline,
project, lịch sử chat, transcript cuộc họp liên quan.

**Fix:** `_process()` build context trước khi gọi LLM:
```python
context = self._build_context(task_id, content, source)
response = self._call_agent(agent, context)
```

`_build_context` đóng gói (thứ tự):
1. `📋 TASK #{id}: title` + Mô tả + Hạn + Người phụ trách + Ưu tiên
   (đọc theo source: ai → `store/tasks.json`, user → `tfo_data/users/*/tasks.json`)
2. `📁 DỰ ÁN {name}:` Mục tiêu + Bối cảnh + Phạm vi + KPI + Rủi ro + Stakeholders +
   Deadline + Trạng thái (nếu task có `project_id`, đọc `projects.json`)
3. `📄 TRANSCRIPT CUỘC HỌP LIÊN QUAN (trích)` — 1500 chars đầu từ meetings.json
   theo `task.meeting_id`
4. `🗣️ LỊCH SỬ CHAT` — 6 message gần nhất (loại message hiện tại), `source` theo nguồn
5. `📨 YÊU CẦU MỚI NHẤT CỦA QUANG:` — content gốc

Verify: chat vào task thuộc project có context điền → agent trả lời trích "Thử nghiệm
phòng tả", "cám chưa xác thực, pháp lý mập mờ" = đã dùng bối cảnh thật.

## 3. UI chốt 05/08 (user corrections)

### Kanban 2 tab con
- Header: nút `setKanbanView('task'|'issue')` — active nền vàng, biến `kanbanView`.
- `renderKanban()` chỉ render board view đang chọn (Task hoặc Issue), không render cả 2.

### Nút ghi âm nổi = ghi luôn
- `floatingRecord()` cũ: scrollIntoView + focus → user "bấm không thấy gì".
- Fix: `document.getElementById('recordBtn').click()` — trigger đúng handler ghi/dừng.

### Agent tab — popup + task con chi tiết
- `agentSubCard` đổi từ `<div class="card">` (hiện dưới board) → modal:
  `position:fixed; inset:0; z-index:470; display:flex` + click-outside đóng
  (`onclick="if(event.target===this) closeAgentSub()"`), content `stopPropagation`,
  header sticky trong popup.
- `openAgentSub` set `display = 'flex'` (không phải `''`).
- **BUG task con không mở:** `openTaskModal(id,'ai')` cũ tìm trong `allTasks` (user tasks)
  → task agent id không có → không mở. Fix: `openAgentSubTask(subId)` tìm trong
  `agentTasks` → `openTaskModalFrom(subId, taskObj, 'ai')` (hàm mới, nhận task object
  thay vì tìm lại). `openTaskModal(id, source)` giờ branch: `source==='ai' ? agentTasks : allTasks`.
- Bỏ nút "+ Task con" + "+ Task lớn mới" trong sub-kanban — tạo task qua nút ➕ header.

### Nút ➕ Thêm việc — header only
- Treo ở header (cạnh menu •••), bỏ nút trong Kanban tab và Agent tab.
- Agent tab chỉ còn dòng hint text.
- Modal `newTaskModal` (z-index 450) dùng chung, radio newTaskType:
  👤 Việc của người (kanban) / 🤖 Giao cho Agent (mode=agent → auto-enqueue critique).

## 4. Meeting note demo (chờ user chốt — pipeline summarize)

Demo transcript v8 (5331 chars) → `/api/summarize` → JSON `{summary, issues, decisions, tasks}`:
- Lần 1 (chạy demo): 2 task đủ assignee + deadline "thứ 7" ✅
- Lần 2 (demo đầy đủ): 4 task, sai assignee ("Gọi cho mẹ → Anh Mão" — sai, phải Quang),
  3/4 thiếu deadline ❌

**LLM summarize không ổn định giữa các lần chạy** (cùng input, output khác nhau).
Đề xuất chốt (3 điểm):
1. Heuristic fix sai người gán: "gọi mẹ / thuyết phục mẹ" → assignee Quang
2. Fallback deadline: transcript chứa "chốt sáng thứ 7" → task deadline "Thứ 7"
3. Chạy 2 lần + chọn bản tốt hơn (nhiều task đủ assignee+deadline)

Format lưu đề xuất: meetings.json có `summary (text) + issues[] + decisions[] + tasks[] + notes_url`
(hiện tại chỉ lưu `summary` là text thô → meeting note không tách được fields).
