# Agent Message Bus API

All functions in `hub/store.py`.

## Send & Receive

```python
send_message(from_agent, to_agent, subject, body, msg_type="direct", ref_task_id=None)
get_messages(to_agent=None, status="unread")  # → list of messages
mark_message_read(message_id)
get_all_messages(limit=20)
```

## Review Routing

```python
assign_reviewer(task_dict)  # → str (CTO/CMO/Design/COO/CFO)
request_review(task_id)     # → str (reviewer name)
```

Keywords for routing (from `REVIEWER_ROUTES` dict):
- technical/code/architecture → CTO
- marketing/content/campaign → CMO
- design/visual → Design
- operation/process → COO
- cost/budget → CFO

## Quang Notifications

```python
notify_quang(message, msg_type="info")
get_quang_notifications(limit=10)
```

Notification types: `info`, `approval`, `pending`, `revision`

## Task Phase Transitions

```python
transition_task(task_id, new_phase, **extra_fields)
# Valid phases: planning, review, approved, in_progress, testing, completed, cancelled
# Extra fields: plan_doc, review_notes, approved_by, test_results, output
```

## Key Files

- `store/messages.json` — all inter-agent messages
- `store/quang_notifications.json` — pending notifications for user
- `store/tasks.json` — tasks with phase tracking
