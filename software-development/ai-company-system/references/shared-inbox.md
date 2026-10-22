# Shared Inbox — Hermes ↔ OpenClaw (Split-File, No Conflict)

Both Hermes and OpenClaw run on separate machines. They communicate asynchronously via **two separate files** pushed/pulled through the same GitHub repo. **Zero merge conflicts.**

## File Layout

| File | Writer | Reader | Purpose |
|------|--------|--------|---------|
| `shared/to_hermes.json` | OpenClaw | Hermes | Claw → Hermes |
| `shared/to_claw.json` | Hermes | OpenClaw | Hermes → Claw |

## Architecture

```
Hermes (Dell)
  │  write to shared/to_claw.json → git push
  ▼
GitHub (ntquang1110/ai-company)
  ▼
OpenClaw: git pull → read to_claw.json → process → write to_hermes.json → push
  ▼
Hermes: git pull → read to_hermes.json → reply
```

## Python API (`shared/inbox.py`)

```python
from shared.inbox import send, read, mark_read, reply

send(to="OpenClaw", subject="Review", body="Task #5 ready", msg_type="review_request")

new_msgs = read(me="Hermes")
for msg in new_msgs:
    print(msg["subject"])
    mark_read(msg["id"])
```

| Function | Auto Git? | Description |
|----------|-----------|-------------|
| `send(to, subject, body, type, ref)` | ✅ push after write | Writes to `to_{recipient}.json` |
| `read(me, status="unread")` | ✅ pull before read | Reads `to_{me}.json` |
| `mark_read(msg_id)` | ✅ push | Marks message read |
| `reply(msg, body)` | ✅ push | Auto-routed reply |
| `get_conversation(limit=10)` | ✅ pull both | Merged history |

## Sync Cron (v3 — output ALL messages)

Every 1m, `no_agent=True` cron runs sync script:

```python
for msg in new_msgs:
    msg["status"] = "read"
    snippet = msg.get('body','')[:120].replace('\n',' | ')
    print(f"📨 {msg['from']}: {msg['subject']}")
    print(f"   {snippet}")
```

**v3=FIX**: Earlier v2 had keyword filters (chốt/done/approved…) — Claw's "PLAN" and "Phản biện" messages did NOT match → silently consumed without delivery. v3 outputs ALL messages, no filter.

## Pitfalls

- **⚠️ `_write_file` bug**: Must pass `data` (full structure), not `msg` (single message). Writing `msg` drops all prior messages.
- **⚠️ `mark_message_read` import**: Must be imported from `store` in `hub/run.py`. Missing → `NameError`.
- **⚠️ Detached HEAD after conflict**: `git rebase --abort`, resolve JSON, `git push origin HEAD:main && git checkout main`.
- **❌ v2 keyword filter**: DO NOT filter by keyword in sync scripts — non-matching messages are silently lost. Output ALL messages.
- **⚠️ Keep messages under 5KB**: git push times out on large bodies.
