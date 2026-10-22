# Git Troubleshooting for Cross-Machine Inbox

## Merge Conflict in Tracked File

Both machines writing to same file causes conflicts.

**v1 problem:** `shared/inbox.json` shared file → conflict every time both push.
**v2 fix:** Separate files — Hermes writes `to_claw.json`, Claw writes `to_hermes.json`.

If conflict still occurs (e.g. during migration):

```bash
# Pull and accept remote version
git pull --rebase origin main
# If conflict: resolve manually, then
git add <file>
git rebase --continue
# If hit detached HEAD:
git push origin HEAD:main
git checkout main
git reset --hard origin/main
```

## Detached HEAD Recovery

Symptoms: `git push` says "You are not currently on a branch"

```bash
# Quick fix — push detached HEAD to main then reset
git push origin HEAD:main
git checkout main
git pull --rebase origin main
```

## Rebase Stuck (Rebase-merge directory exists)

```bash
rm -rf .git/rebase-merge
git pull --rebase origin main
```

## Latest Commit Lost (Commit left behind after branch switch)

```bash
# Find the lost commit
git reflog
git cherry-pick <lost-commit-hash>
# Or create temp branch
git branch temp <hash>
git checkout main
git merge temp
```
