# 2-level kanban data model (task lớn + task con) — đã triển khai TFO 05/08/2026

## Nguyên tắc (user đã chốt)
- **2 kanban lồng nhau**: kanban task lớn (6 phase) → bấm card mở sub-kanban task con bên trong.
- **Task con KHÔNG lặp lại 6 phase** — chỉ 3 trạng thái đơn giản (todo/in_progress/done).
- Kéo card qua phase → **agent tự chuyển** theo map phase→agent + **ghi log kết quả** phase.
- Card task lớn hiển thị **progress = % task con done**.

## Data model
```python
task = {
    "id": 1,
    "title": "Tính năng A",
    "parent_id": None,          # task con → id task gốc; task gốc = None
    "phase": "planning",        # task lớn: 6 phase
    "assignee": "PO",           # auto đổi theo PHASE_AGENT khi kéo
    "sub_status": "todo",       # task con: todo/in_progress/done
    "phase_logs": [             # log kết quả từng phase
        {"phase": "planning", "agent": "PO",
         "result": "Vấn đề, bối cảnh, task, quyết định", "at": "2026-08-05 18:00"}
    ],
    "priority": "P0",
}
```

## Phase → agent mặc định
| Phase | Agent |
|---|---|
| planning | PO |
| review | SA |
| approved | CTO |
| in_progress | Dev1 |
| testing | QA |
| completed | QA |

## API (FastAPI)
- `GET /api/agent-board` — gom tasks + agents + stats per agent (total/done/running) + phase map
- `POST /api/agent-tasks` — tạo task (body có `parent_id` để tạo task con)
- `POST /api/agent-tasks/{id}/phase` — chuyển phase task lớn: auto đổi assignee + append phase_logs
- `POST /api/agent-tasks/{id}/sub-status` — chuyển trạng thái task con (todo/in_progress/done)

## UI (tab Agent)
- Nút chuyển view: 📊 Kanban | 📋 List
- Kanban: 6 cột phase; card = task lớn (priority icon + progress bar + badge task con)
- Bấm card → sub-kanban 3 cột task con + 📝 log các phase đã qua ở trên
- List: mỗi agent 1 dòng `🏃 Running · ✅ Done · 📋 Tổng` + task hiện tại; bấm → xem chi tiết
- Filter theo agent (select)

## Pitfall
- Khi nhiều agent/session sửa chung file HTML: **check duplicate ID + div balance trước deploy**
  (đã gặp duplicate viewAgent + tabAgent từ sibling subagent).
- Stats per agent phải khởi tạo trước cho mọi agent (kể cả idle) để list không lỗi.
