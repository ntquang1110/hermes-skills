# Message Bus Pattern — Hermes Multi-Agent 2.0

File-based inbox/outbox queue for inter-agent communication on a single machine.

## Directory Structure

```
~/ai-company-v2/messages/
├── inbox/{agent_id}.json    → Messages TO an agent. Each agent reads its own.
├── outbox/{agent_id}.json   → Messages FROM an agent (optional mirror).
├── queue/tasks.json         → Shared task queue (future use).
└── archive/{date}/          → Completed messages, moved on clear.
```

## Message Format

```json
{
  "id": "8char-uuid",
  "from": "ceo | research | sales | dev",
  "to": "ceo | research | sales | dev",
  "type": "task | result | handoff | error",
  "subject": "Task: <title> | Done: <task_id> | Handoff: ...",
  "body": "{... JSON payload ...}",
  "ref_task_id": "T-001",
  "status": "unread | read",
  "created_at": "2026-09-22 00:17:10",
  "timestamp": 1790011030.478389
}
```

## API (message_bus.py)

| Function | What |
|----------|------|
| `send(from_id, to_id, subject, body, msg_type, ref_task_id)` | Send message to an agent's inbox |
| `read_inbox(agent_id, unread_only=True)` | Read messages for an agent |
| `mark_read(agent_id, msg_id)` | Mark single message read |
| `mark_all_read(agent_id)` | Mark all read |
| `clear_inbox(agent_id)` | Archive + clear inbox |
| `dispatch_task(task_id, task_data, to_agent, from_agent)` | Shortcut: send typed task |
| `report_done(from_id, to_id, task_id, result)` | Shortcut: send result |
| `inbox_status()` | Human-readable summary |

## Agent Status (agent_registry.py)

| Status | Meaning | Set by |
|--------|---------|--------|
| `idle` | Waiting for tasks | Watchdog / worker |
| `pending` | Task in inbox, not yet dispatched | Watchdog |
| `busy` | Subagent processing | CEO on dispatch |
| `error` | Failed task | Worker on exception |

## Key Rules

1. Watchdog (`no_agent=True` cron) ONLY detects + sets status. Does NOT process.
2. CEO (`delegate_task`) does the actual processing with tool access.
3. Each agent reads its OWN inbox file — no shared file, no conflicts.
4. Results go back to CEO inbox via `report_done()`.
5. Handoff between agents via `send(from, to, ..., msg_type="handoff")`.
