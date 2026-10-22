# DoD + Worker Fixes — AI Company (2026-08-12)

## Bối cảnh
Quang chê standup lặp lại ("mấy ngày cứ lặp lại nhau thế nhỉ") → chốt quy tắc Definition of Done:
mọi task khi lên phải có done criteria + deadline; báo "xong" = có bằng chứng (QA/test pass/link).
Sau đó hỏi "tại sao task agent treo planning mà không thấy plan" → chẩn đoán + fix 2 lớp.

## Chẩn đoán task treo planning

### Lớp 1 — Task seed không qua pipeline
16 task tạo thẳng `store/tasks.json` (02/08, cùng timestamp = seed script) → không đi qua
`create_ai_task` → không auto-enqueue → agent không bao giờ thức dậy → không ai viết plan.
Worker chỉ chạy khi có message vào thread. Bằng chứng: 9 task planning có phase_logs = 0,
thread messages = 0; chỉ task 7 (có tin nhắn của Quang) có 4 messages.

### Lớp 2 — Worker bugs (`app/agent_exec.py`)
- `_set_task_status`/`_set_task_assignee` ghi vào user tasks.json kể cả source="ai"
  → store/tasks.json (AI Company) không bao giờ đổi phase dù agent có xử lý.
- flash trả rỗng ~80% prompt dài → queue item `status=error` + log
  `[agent-worker] LLM call failed: Expecting value: line 1 column 1 (char 0)`.
  Log xác nhận: 16 queue → 11 done + 5 error.

## Fix đã build + verify
- `_set_task_status(task_id, status, source)` + `_set_task_assignee(task_id, agent, source)`:
  source="ai" → ghi `store/tasks.json`; `status=="done"` + `phase=="planning"` → `phase="review"`.
- `_call_agent(agent, content, force_pro=False)`: force_pro → model `deepseek-v4-pro`.
  `_process` retry: response rỗng → CTO force_pro → PO force_pro.
- `route_agent`: rule ưu tiên `viết plan|viet plan|viết kế hoạch|...` → PO trước DOMAIN_AGENTS
  (tránh "thread" bị Content regex nuốt).
- done_criteria: 4 endpoints (create_task mode=agent + create_ai_task task lớn → 400 nếu thiếu;
  update_task + update_ai_task nhận field), UI modal/kanban/filter, `_build_context` đưa DC vào prompt.

## Recipe: đánh thức task planning cũ
```python
import sys; sys.path.insert(0, "D:/Hermes Proj/ai-company")
from app.agent_exec import enqueue
email = "quang@kiemsaphia.com"
for t in planning_tasks:  # filter phase=='planning' and not parent_id
    content = (
        f"Anh yêu cầu viết PLAN thực hiện cho task #{t['id']}: {t['title']}\n"
        f"Định nghĩa hoàn thành (done criteria): {t.get('done_criteria') or ''}\n"
        f"Mô tả: {t.get('description') or ''}\n\n"
        f"Em là {t.get('assignee') or 'CTO'}, viết plan chi tiết: mục tiêu, các bước thực hiện, "
        f"đầu ra mỗi bước, ước lượng thời gian, rủi ro/điểm cần làm rõ. Trình plan vào thread này. "
        f"KHÔNG code. Chỉ viết plan."
    )
    enqueue(email, t['id'], "Quang", content, source="ai")
```

## ⚠️ Race: enqueue bằng script khi worker pool đang chạy
- Triệu chứng: queue JSON bị corrupt — `JSONDecodeError: Extra data: line N column 2 (char M)`
  hoặc queue mất items (2 process ghi đè cùng file: worker cũ + script).
- Cách chạy ĐÚNG (đã verify 12/08):
  1. Dừng server: `taskkill /PID <pid> /F` (lấy PID qua `netstat -ano | grep :8100 | grep LISTEN`).
  2. Reset queue: `{"queue": [], "next_id": 1}` ghi đè `tfo_data/users/<email>/task_queue.json`.
  3. Enqueue bằng script (lúc này KHÔNG có worker nào chạy).
  4. Start server (background, watch "Application startup complete").
  5. Chạy script standalone `WorkerPool().ensure(email)` + poll queue file tới khi hết pending
     (worker daemon claim + xử lý; log `[agent-worker] task N → AGENT done`).
- Lưu ý: worker pool chỉ tự start qua API (`agent_pool.ensure` trong create_task/create_ai_task/
  post_task_message) — enqueue thẳng file KHÔNG trigger pool, cần bước 5.

## Verify kết quả 12/08
- 4 task planning lớn (#7 pilot CEO #2, #8 test meeting, #9 demo, #10 feature A)
  → phase `review` + plan 2-2.5k ký tự trong thread (hiểu yêu cầu, điểm mơ hồ, phản biện, các bước).
- Route nhầm Content (do "thread") đã được nhận diện khi review plan — fix rule ưu tiên ở trên.
- Commit: af82589 (DoD TFO), c352ebe (worker fixes).
