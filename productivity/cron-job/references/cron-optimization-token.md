# Cron Optimization — Token Reduction Workflow

Verified 2026-09-26 on Hermes instance NTQUANG_DELL. Profile: 44 cron jobs, 32 active, ~62K requests/month, ~387M token thật/month.

## Where token goes (state.db session_model_usage)

| Source | Token thật | % |
|---|---|---|
| Cron jobs | 180.7M | 46.6% |
| Chat/Telegram | 206.9M | 53.4% |

Top cron jobs by token thật:
1. KFlow Push Tâm lý — 52.2M (28.9%) — ALREADY PAUSED 21/09, do not resume
2. knowledge-researcher-4h — 48.9M (27.0%) — 6 lần/ngày → CUT TO 1
3. Auto Threads - Ministral — 11.5M (6.3%) — 1 lần/ngày, keep
4. Auto-push research to KFlow — 10.8M (6.0%) — 2 lần/ngày → CUT TO 1
5. knowledge-researcher (old) — 10.2M (5.6%) — superseded by -4h rotation

## Verified cuts (2026-09-26)

- KFlow Push: already paused, 0 action needed
- HLL Daily + HLL Poster: paused (queue empty — 7/7 posted, last_posted 2026-09-04)
- knowledge-researcher: 6→1 lần/ngày (0 8 * * *), prompt updated to "1 lần/ngày, 4 bài"
- Auto-push research: 2→1 lần/ngày (0 22 * * *)
- Tâm lý 1/4, 2/4, 3/4, 4/4: kept at 1/ngày (was 6/ngày before)

## Before cutting any cron — verify data source

1. Schedule-based: read `hll-schedule.json`, `macro-schedule.json` — check queue length + last_posted_date
2. Research-based: `sqlite3 state.db "SELECT COUNT(*), SUM(input_tokens+output_tokens) FROM session_model_usage WHERE session_id LIKE 'cron%'"` 
3. Post-based: check post log/backlog file

## Files modified

- `~/AppData/Local/hermes/cron/jobs.json` — schedules + prompts updated
- `~/AppData/Local/hermes/state.db` — session data for analysis

## Scripts used

- `D:\ai-router-test\usage_by_month.py` — monthly token stats
- `D:\ai-router-test\cron_group.py` — token by job name
- `D:\ai-router-test\check_cache.py` — cache_read/input ratio analysis

## Model swap candidates (Tầng 2, not done yet)

unsloth/Ministral-3-8B-Instruct-2512-GGUF → space-bunny-alpha (0$, 1M context, 3.2s)
Risk: stealth preview, no long-term guarantee. Keep fallback chain.
