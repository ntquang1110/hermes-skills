# Hermes Multi-Agent v2 — Registry + Message Bus Pattern (2026-09)

Single Hermes instance + Agent Registry. Không dùng multi-profile.

## Registry (SQLite)
`ai-company-v2/registry/agents.db` — bảng `agents(id, name, role, persona JSON, skills JSON, tools JSON, memory_path, reports_to, status)` + `agent_memory(agent_id, key, value)`.
Pilots: ceo (orchestrator), sales, research, dev. CRUD in `registry/agent_registry.py`: `init_db()`, `seed_pilots()`, `get_agent()`, `list_agents()`, `set_status()`, `save_memory()`.

## Message Bus (file-based queue)
`ai-company-v2/messages/` — `inbox/{agent_id}.json`, `outbox/`, `queue/tasks.json`, `archive/{date}/`.
API in `messages/message_bus.py`: `send(from,to,subject,body,type)`, `read_inbox()`, `mark_read()`, `dispatch_task()`, `report_done()`, `inbox_status()`.
Không qua git. Watchdog 5s polling (v2), sau này inotify/ReadDirectoryChanges.

## CEO Orchestrator
`agents/ceo.py` — `route_task(text)` keyword→agent, `ceo_dispatch(task_id,title,desc,deadline,context,to_agent)` auto-route nếu to_agent rỗng, set agent busy, dispatch qua bus.
Skill: `skills/ceo-orchestrator/SKILL.md`.

## Worker
`agents/worker.py` — `process_tasks(agent_id)` đọc inbox type task/handoff, ghi `tasks/{task_id}/result.json`, report về ceo, mark read, set idle, save memory.

## Progress tracking (user expects)
- `todo` list 5 steps (registry→bus→ceo→pilots→e2e test)
- `python registry/agent_registry.py` → status
- `python -c "from message_bus import inbox_status; print(inbox_status())"`
- `tasks/{id}/result.json`
- `python agents/ceo.py dispatch "Title" --to sales`

## Pitfalls
- Không dùng `~/` literal với python cpython-314 — dùng `cd ~/ai-company-v2 && python messages/...`
- V1 Git inbox chậm/conflict → V2 file-based local.
- ceo dispatch phải handle `reports_to` chain.
- Dashboard server dùng `HTTPServer` — cần `cd ~/ai-company-v2 && python dashboard/server.py <port>` (không dùng path literal, không dùng `&` foreground).
- Tunnel (`lt --port 5050 --subdomain ai-company-v2`) mất kết nối khi background process bị kill giữa session. Restart: `terminal(background=true)` cho server + tunnel riêng biệt.
- Worker v2 log activity: phải có `from activity import log` + `log(agent, action, detail, task_id, status)` ở mỗi bước. Nếu thiếu, dashboard và report sẽ không có activity feed.
- Report HTML chỉ được tạo nếu `_generate_report()` được gọi sau khi ghi `result.json`. Worker_v2 gọi tự động; worker.py cũ thì không.

## Transparency components (v2)

| File | Purpose |
|------|---------|
| `activity.py` | `log()` JSONL to `logs/activity.jsonl`, `get_recent(limit)`, `get_task_activity(task_id)` |
| `tasks/report.py` | `generate_report(task_id)` → `tasks/{id}/report.html` (Task Info + Activity + Result + Raw JSON) |
| `dashboard/server.py` | `GET /data` (JSON API), `GET /task/{id}` (HTML report), `POST /dispatch` |
| `dashboard/index.html` | Dashboard UI: agents, inbox, activity feed, task list with Report → links |
| `agents/worker_v2.py` | Replaces worker.py: logs steps, writes result.json, calls `_generate_report()` |
| `watchdog.py` | Delegates to `worker_v2.process_tasks` (not worker.py) |
| `company.py` | Imports `worker_v2`, not `worker` |
