---
name: youtube-schedule
description: "YouTube transcribe + summarize in Vietnamese + schedule daily post via cron queue. Points to youtube-to-threads for the authoritative writing style."
platforms: [windows]
---

# YouTube Schedule

Use when the user sends a YouTube URL and expects a Vietnamese summary posted on a daily schedule (queue + cron). This skill extends generic `youtube-content` with user-specific preferences.

## When to Use

- User sends a YouTube URL (youtube.com, youtu.be, shorts, etc.)
- User expects transcription, Vietnamese summary, and scheduled posting
- User says "post lên thread" or similar

## Writing Style

**IMPORTANT**: The authoritative writing style is now in the `youtube-to-threads` skill. Key rules from SOUL.md:
- Full Vietnamese diacritics — NEVER skip
- No icons, no emoji, plain text
- 2-layer depth structure (mechanism → feedback loop)
- Exact quotes from source, not vague paraphrase
- Short sentences, conversational tone
- Read full transcript before writing

See `youtube-to-threads` skill → "User's Vietnamese Writing Style" section for complete rules.
See `C:\Users\NTQUANG_DELL\AppData\Local\hermes\SOUL.md` for the definitive persona file.

## Scheduling Workflow

### User Approval Required (UPDATED)

Do NOT auto-add to queue. Follow this flow:
1. Fetch transcript with timestamps
2. Read complete transcript text
3. Write summary in approved 2-layer style with exact quotes
4. Present to user for approval
5. Only after user says "ok" → add to queue

### Queue Addition (After User Approval)

Read `C:\Users\NTQUANG_DELL\AppData\Local\hermes\cache\youtube-schedule.json`:
- Find latest date among: `last_posted_date` + all pending items' `scheduled_date`
- New item date = latest_date + 1 day
- Append to queue with `status: "pending"`, `scheduled_date: that date`
- Save with `json.dump(..., ensure_ascii=False, indent=2)`

### Vietnamese Accent Preservation

Python heredocs in git-bash strip Vietnamese diacritics. To preserve accents:
1. Write content to a `.txt` file using `write_file()` (handles UTF-8)
2. Read file back with Python: `open(path, encoding="utf-8").read()`
3. Verify accent count before saving to queue
4. Update queue item with verified content

### Cron Jobs

| Name | Schedule | Function |
|------|----------|----------|
| Daily Research | `30 7 * * *` | Research + draft + deliver to user for approval |
| Schedule Poster | `0 20 * * *` | Post next pending item to Threads |

## Duplicate Check

Before processing any URL:
1. Extract video ID: `(?:v=|youtu\.be/)([a-zA-Z0-9_-]{11})`
2. Check `C:\Users\NTQUANG_DELL\AppData\Local\hermes\cache\youtube-processed.json`
3. If exists → reject. If new → process and add.

## Pitfalls

- **Vietnamese diacritics lost in heredocs**: Always use write_file for content, then read_file + Python to update schedule
- **YouTube rate-limiting**: ~8-10 fetches then blocked. Wait or use proxy.
- **Threads 500-char limit**: Split by sentences, never mid-sentence
- **fill() fails on replies**: Use keyboard.type(delay=5) for reply editors
- **Post-verification**: "Posted!" ≠ content saved. Verify on post page.
- **Bulk-posting**: Never post multiple items at once — one per day.
- **User approval workflow**: Never auto-add to queue. Always get "ok" first.
- **Cron 07:30**: Research only. Cron 20:00: Post only. Keep them separate.

## Related Skills

- `youtube-content` — generic YouTube transcript service (bundled)
- `youtube-to-threads` — authoritative writing style, 2-layer depth, SOUL.md integration
