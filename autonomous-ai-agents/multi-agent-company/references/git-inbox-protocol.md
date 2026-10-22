# Git Inbox Protocol — cross-machine agent communication

Pattern for two AI agents (Hermes + OpenClaw) on **separate machines** exchanging messages with zero infra beyond a shared git repo.

## Why separate files (the core trick)
A single shared `inbox.json` mutated by both machines → constant merge conflicts when both push near-simultaneously (hit repeatedly in practice). Fix: **each sender writes only to the recipient's own file** → no shared mutable file, no conflicts.

```
Hermes ghi → shared/to_claw.json   (Claw đọc)
Claw ghi   → shared/to_hermes.json (Hermes đọc)
```

`send(to=...)` picks the file by recipient. `read()` reads only YOUR mailbox.

## Message shape
```json
{
  "id": 3,
  "from": "OpenClaw",
  "to": "Hermes",
  "subject": "🧠 BRAINSTORM ...",
  "body": "...",
  "type": "direct | reply | review_request | consensus",
  "ref": null,
  "status": "unread | read",
  "created_at": "2026-07-27 00:17:51"
}
```

## inbox.py API (shared/inbox.py)
```python
send(to="OpenClaw", subject="...", body="...")   # writes to to_claw.json, pushes
read()                                            # pulls, returns unread to me (Hermes)
mark_read(msg_id)                                 # status→read, pushes
reply(msg, "body")                                # send back to msg["from"]
get_conversation(limit)                           # merge both files, newest first
```

## Sync script (no_agent cron, every 1m)
```python
# scripts/ai-inbox-sync.py (Hermes side: MY_FILE = shared/to_hermes.json)
git(["pull", "--rebase"])
msgs = [m for m in data["messages"] if m["status"] == "unread"]
if not msgs: sys.exit(0)             # silent — nothing delivered
for m in msgs:
    m["status"] = "read"
    print(f"📨 {m['from']}: {m['subject']}")   # output ALL — no keyword filter
    print(f"   {m['body'][:120]}")
git(["add", "shared/to_hermes.json"]); git(["commit", "-m", "inbox: sync auto"]); git(["push"])
```

Cron creation (Hermes): script MUST live in `~/AppData/Local/hermes/scripts/` and be referenced by filename only; `no_agent=true` so stdout is delivered verbatim and empty stdout = silent.

## Rules learned the hard way
1. **NO keyword filtering in the sync cron.** The first version only printed messages matching "chốt/done/approved/triển khai..." — routine messages like "PLAN" / "Phản biện" were marked read and swallowed silently, and the user saw delays. Output every new message; let the human decide importance.
2. **Pull before read, push after write.** Both sides run the same loop; stale pull → missed messages.
3. **Role model: one FRONT, one BACK.** User gets ONE voice. Front asks + synthesizes to the user; back does logic/critique/implementation and relays through the inbox. (Current: OpenClaw=front, Hermes=back.) Never have both agents ask the user different questions.
4. **workspace.md is source of truth** for vision/decisions/roles — update + push it when anything is decided.

## Conflict recovery (if it ever happens anyway)
Manual merge: keep BOTH conflicting messages, renumber one, write clean JSON, `git add` + commit + push. Detached HEAD from aborted rebases: `git checkout main && git pull --rebase origin main`, or `git push origin HEAD:main`, then `git reset --hard origin/main` if divergent.

## Alternatives considered
- HTTP endpoint on Cloudflare tunnel (near-realtime) — works but adds auth surface; git inbox chosen for zero infra and full audit trail.
