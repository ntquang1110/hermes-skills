# Scheduling Rules Reference

## Date calculation priority

1. Read queue from youtube-schedule.json
2. Find latest date among ALL items:
   - last_posted_date (str)
   - sorted_date of last pending item
3. Pick the most recent
4. New date = that date + 1 day

## Edge cases

| Condition | Action |
|-----------|--------|
| New date = today, time >= 20:00 | Post immediately via threads_poster.py |
| New date = today, time < 20:00 | Schedule for 20:00 today |
| New date > today | Schedule for 20:00 that day |
| Queue has pending items | Use pending items' last date + 1 |

## Cron timing

- Research cron: 06:00 daily (before posting cron)
- Poster cron: 20:00 daily (after research cron)
- Both use +07:00 timezone (SE Asia)

## Stats fields

```json
{
  "total_posts": 0,
  "total_videos_processed": 0,
  "by_source": {
    "user_sent": 0,
    "auto_research": 0
  },
  "by_topic": {
    "skill_philosophy": 0,
    "ai": 0,
    "happiness_meaning": 0,
    "neuroscience": 0,
    "business_mind": 0
  },
  "posting_history": [],
  "pending_queue": []
}
```
