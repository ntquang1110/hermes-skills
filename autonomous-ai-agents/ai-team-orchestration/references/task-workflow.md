# Task Workflow: Plan → Review → Approve → Implement → Test

Phase-gate workflow enforced by `cmd_agent()` in `hub/run.py`.

## Phase State Machine

```
📋 Planning ──(write plan)──→ 🔍 Review ──(PASS)──→ ✅ Approved
                                        ↑                    │
                                   (FAIL)               (Quang: "triển khai")
                                        │                    ↓
                                        └──── planning ←─── 🔵 In Progress
                                                                    │
                                                                    ↓
                                                               🧪 Testing
                                                                    │
                                                              (PASS)│  (FAIL)
                                                                    ↓    │
                                                                ✅ Done  │
                                                                        └──→ in_progress
```

## code Implementation

```python
# In cmd_agent() — auto-routes based on phase
if phase == "planning":
    result = agent.think("Viết spec/design doc...")
    transition_task(task_id, "review", plan_doc=result)
    request_review(task_id)  # Sends message to reviewer

elif phase == "review":
    # This is handled via the message bus now
    # Agent checks get_messages(to=me, type="review_request") first
    result = agent.think("Phản biện plan này...")
    if "PASS" in result:
        transition_task(task_id, "approved", approved_by=agent)
        notify_quang(f"Cần anh confirm: triển khai đi")
    else:
        transition_task(task_id, "planning")

elif phase == "approved":
    transition_task(task_id, "in_progress")
    result = agent.think("Implement theo plan...")
    transition_task(task_id, "testing", output=result)

elif phase == "testing":
    result = agent.think("Verify output. PASS hay FAIL?")
    if "PASS" in result.lower():
        transition_task(task_id, "completed")
    else:
        transition_task(task_id, "in_progress")
```

## Quang Notification Rules

Only notify Quang (via `notify_quang()`) for:

| Event | Notify? | Message |
|-------|---------|---------|
| Plan written, sent for review | ✅ Pending | "Task #X đang chờ Y review" |
| Review PASSED | ✅ Approval needed | "Task #X đã duyệt. Cần anh confirm: triển khai đi" |
| Review FAILED | ✅ Revision | "Task #X cần sửa. Yêu cầu: ..." |
| Implement done | ❌ Silent | (auto-transitions to testing) |
| Testing PASS | ✅ Complete | "Task #X hoàn thành" |
| Testing FAIL | ❌ Silent | (auto-transitions back to implement) |
| Agent idle | ❌ Silent | (proposal goes to board, not Telegram) |

## Auto-Review Routing

When a task transitions to `review`, `request_review()` picks the reviewer:

```python
REVIEWER_ROUTES = {
    "technical|code|architecture": "CTO",
    "marketing|campaign|content": "CMO",
    "design|visual": "Design",
    "operation|process": "COO", 
    "cost|budget": "CFO",
}
```

The assignee agent sends a `review_request` message to the reviewer via the message bus.
