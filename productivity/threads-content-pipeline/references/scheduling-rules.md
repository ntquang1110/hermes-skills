# Scheduling Rules (đã xác nhận 2026-07-16)

## Core Rule

When user sends new URL → calculate schedule date:

1. Read `youtube-schedule.json` queue
2. Find the latest date among posted + pending items
3. New date = latest_date + 1 day

## Today Check

If new_date == today:
- Current time >= 20:00 → post immediately via threads_poster.py
- Current time < 20:00 → schedule for 20:00 today

If new_date > today:
- Schedule for 20:00 on that date

## Queue Priority

If queue already has pending items:
- Last pending date in queue + 1, NOT last posted date + 1

## Cron Jobs

- **Daily Research** (06:00): auto-research content → summarize → add to queue
- **Schedule Poster** (20:00): post next pending item from queue

## Scheduling Format

Items stored in `youtube-schedule.json`:
- `status`: "pending" | "posted"
- `scheduled_date`: ISO date (YYYY-MM-DD)
- `posted_date`: ISO date (when actually posted)
- Content posted at 20:00 by cron job

## Cron Script

`youtube-scheduler.py` (no_agent = true) runs at 20:00 daily:
1. Read schedule
2. Find next pending item with scheduled_date <= today
3. Call threads_poster.py with content
4. Mark as posted (main post success = posted, even if replies fail)
