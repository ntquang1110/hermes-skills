# Cross-Machine Inbox: Git Merge Conflict Resolution

When two agents (e.g. Hermes and OpenClaw) both write to `shared/inbox.json`, git conflicts are inevitable.

## Root Cause

Both machines:
1. Pull the current state
2. Add messages
3. Commit + push

If B push while A hasn't pushed yet, B's push succeeds. When A tries to push, git rejects with "Updates were rejected". If A pulled just before B pushed, the rebase/merge creates a conflict in the JSON.

## Resolution Pattern

### Step 1: Detect the conflict
```bash
git pull --rebase
# → CONFLICT (content): Merge conflict in shared/inbox.json
```

### Step 2: Read the conflicted file
Look for `<<<<<<< HEAD`, `=======`, `>>>>>>>` markers. Each side has valid JSON fragments that need merging.

### Step 3: Merge manually
Keep ALL messages from both sides, renumber to avoid duplicate IDs.

```python
# Manual resolution: keep all messages, fix IDs, fix next_id
messages = [msg1, msg2, msg3, ...]  # All unique messages
next_id = max(m["id"] for m in messages) + 1
```

Write the clean JSON back, then:
```bash
git add shared/inbox.json
git rebase --continue
# or if not in rebase:
git commit -m "inbox: merge conflict resolved"
git push
```

### Step 4: If detached HEAD
```bash
git push origin HEAD:main
git checkout main
git reset --hard origin/main
```

## Prevention

**Best fix:** Each agent writes to its own file:
```
shared/to_claw.json     # Hermes writes, Claw reads
shared/to_hermes.json   # Claw writes, Hermes reads
```

No conflict because each file has only one writer.

## Recovery from stuck rebase

```bash
# If rebase --continue opens editor and hangs:
GIT_EDITOR=true git rebase --continue

# If stuck in middle of rebase:
git rebase --abort
# then:
git reset --hard origin/main
git push origin HEAD:main
git checkout main
```
