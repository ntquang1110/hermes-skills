---
name: auto-social-publisher
description: "Auto-process YouTube/source content, schedule, and publish to social platforms (Threads). Includes Playwright-based posting, queue management, stats tracking, and daily cron research."
platforms: [windows]
tags: [youtube, threads, scheduling, social-media, publishing, playwrigt]
---

# Auto Social Publisher

Auto-publish YouTube video summaries to social platforms (Threads) on a schedule. Supports user-sent links AND auto-research daily.

## Architecture

```
User link / Cron research
        |
        v
  Fetch transcript
        |
        v
  Summarize (user style)
        |
        v
  Add to schedule queue (JSON)
        |
        v
  Cron 20:00 -> Post to Threads
```

## Files

- Schedule queue: `C:\Users\NTQUANG_DELL\AppData\Local\hermes\cache\youtube-schedule.json`
- Stats tracker: `C:\Users\NTQUANG_DELL\AppData\Local\hermes\cache\youtube-stats.json`
- Threads poster script: `C:\Users\NTQUANG_DELL\AppData\Local\hermes\scripts\threads_poster.py`
- Threads session: `~/.hermes/threads_state.json`

## Cron Jobs

| Job | Time | Function |
|-----|------|----------|
| Daily Research | 06:00 | Auto-research content, summarize, add to queue |
| Schedule Poster | 20:00 | Post next pending item to Threads |

## Writing Style (Vietnamese Threads format)

Mandatory rules:
- Vietnamese with FULL diacritics - NEVER post without diacritics
- No icons/emojis
- No em dashes (—) - only hyphens (-)
- Plain text, no fancy formatting
- Short, direct sentences
- Numbered structure: "1/ Title", "2/ Topic"
- Bullets with single hyphen (-)
- Clear sections, no verbose explanations
- Tom lai (summary) at end with numbered points

## Scheduling Rules

- Read queue, find latest date (posted or pending)
- New date = that date + 1
- If new date = today AND >= 20:00 -> post now
- If new date = today AND < 20:00 -> schedule 20:00 today
- If new date > today -> schedule 20:00 that day
- If pending items exist -> last pending + 1

## Topics for Auto-Research

- Than kinh (neuroscience, brain plasticity, cognition)
- Hanh phuc (happiness, well-being, meaning, psychology)
- AI (AI skills, AI and humans)
- Business mind (business mindset, leadership, strategy, productivity, habits)

## Threads Posting via Playwright

### Setup
1. Install: `uv pip install playwright`
2. Install browser: `python -m playwright install chromium`
3. Login: run `threads_login.py` (headless, credentials from THREADS_CREDS_B64 in .env)
4. Session saved to `~/.hermes/threads_state.json`

### Key techniques
- Use **Ctrl+Enter** to submit (clicking Post button is unreliable)
- First part = main post, subsequent parts = replies to same post (reply chain)
- When reply editor is hidden: use JS `editor.style` to make visible first, then `fill()` and `press("Control+Enter")`
- Or use `page.evaluate()` to set textContent + dispatch input/change events

### Login refresh
If session expires, re-run login script. Threads uses Instagram auth.

## Stats Tracking

File: `youtube-stats.json`
Track: total posts, total videos, by source (user_sent/auto_research), by topic, posting history

## ThreadsBot tasks

When processing a user-sent YouTube link:
1. Fetch transcript via youtube-content fetch script
2. Summarize in writing style (see above)
3. Calculate schedule date (see Scheduling Rules)
4. Add to queue with content, url, title, scheduled_date
5. Update stats file
6. Report schedule to user

## Pitfalls

- Vietnamese diacritics: ALWAYS verify before publishing. User requires repost if missing.
- Threads web: no delete button. Use mobile app to delete if needed.
- Reply editor on Threads may be hidden for 2nd+ reply. Make visible via JS before fill().
- Content must be >= 1000 chars to split into multiple Threads posts.
- Windows git-bash: python3 may not work. Use python or full venv path.
- Threads session cookie: check expiry; may need re-login every few weeks.
