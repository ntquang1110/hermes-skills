# Silent Cron Pattern for Agent Sync

Standard pattern for cross-machine agent sync via git, running every 1 minute silently.

## Requirements

- Must NOT spam the user's chat (Telegram)
- Only notify on important events (decisions, approvals, blockers)
- Must handle git pull/push gracefully (network failures -> silent)

## Implementation

```python
#!/usr/bin/env python3
"""sync_minute.py — Silent cron. Only output when important."""

import sys, os, json, subprocess

BASE = "/path/to/repo"
INBOX = os.path.join(BASE, "shared", "inbox.json")

def git(cmd):
    subprocess.run(["git"] + cmd, cwd=BASE, capture_output=True, timeout=30)

# 1. Pull latest
git(["pull", "--rebase"])

# 2. Read new messages for me
data = json.load(open(INBOX))
new = [m for m in data["messages"] if m["to"] == "Me" and m["status"] == "unread"]

if not new:
    sys.exit(0)  # SILENT — nothing to report

# 3. Process — only output if important
for msg in new:
    msg["status"] = "read"
    body = msg.get("body", "")
    subject = msg.get("subject", "")
    
    important = any(kw in (subject + " " + body).lower() for kw in [
        "chốt", "quyết định", "done", "xong", 
        "approved", "pass", "fail",
        "triển khai", "đồng ý", "reject", "cần anh"
    ])
    
    if important:
        print(f"📨 {msg['from']}: {subject}")
        print(f"   {body[:200]}")

json.dump(data, open(INBOX, "w"), indent=2, ensure_ascii=False)

# 4. Push back (mark as read)
git(["add", "shared/inbox.json"])
git(["commit", "-m", "inbox: sync auto"])
git(["push"])
```

## Hermes Cron Setup

```yaml
# In Hermes config or via cronjob tool:
- name: ai-company-inbox
  schedule: "every 1m"
  no_agent: true          # Skip LLM — run script directly
  script: ai-inbox-sync.py
  deliver: origin         # Only deliver to origin chat
```

## Key Design Decisions

1. **`no_agent=true`** — no LLM call, no token cost, the script's stdout IS the delivery. Empty stdout = nothing sent to user.
2. **Importance filter** — only keywords like "chốt", "approved", "cần anh" trigger output. Everything else is dropped silently.
3. **Network resilience** — `capture_output=True, timeout=30` — if network is down, the script exits silently.
4. **Non-zero exit ≠ failure** — git pull failing (network) should not alert. The script exits cleanly even on git failures.
