# Parallel Content Channel — setup for a second topic queue (Macro example)

When Quang adds a NEW content channel (different topic/domain) that must run
*publishing the same way* (YouTube transcript -> Threads) but as a SEPARATE
queue so it never collides with the psychology/business queue, replicate this
pattern. Verified 2026-08-27 for "MIT 14.02 Principles of Macroeconomics".

## Principle: one channel = one queue + one scheduler + one cron

Do NOT append the new channel's items to `youtube-schedule.json`. That file is
the psychology queue (often 70+ pending, booked out weeks). A second channel
needs its own files so approval/posting flows stay independent.

### Files
- `~/AppData/Local/hermes/cache/macro-schedule.json` — channel queue (identical
  JSON shape as youtube-schedule.json: `last_posted_date` + `queue[]`).
- `~/AppData/Local/hermes/scripts/macro-scheduler.py` — copy of
  `youtube-scheduler.py`, ONLY change = `SCHEDULE_PATH` to the channel file.
  Keeps the same success-gating (mark posted only on rc==0 AND
  `https://www.threads.com` in stdout AND no "Session expired").
- `~/AppData/Local/hermes/scripts/macro-next.py` — "what lecture/item next"
  resolver (see below).
- Project metadata lives on ổ D per disk policy: playlist + drafts under
  `D:/Hermes .../<channel>/` (e.g. `D:/Hermes Proj/macro-14.02/`).

### Crons (both no_agent, script-backed)
- Channel poster: schedule at `30 20 * * *` (20:30), NOT 20:00. The psychology
  "YouTube Schedule Poster" (`1d919d76614a`) already posts at 20:00 and both
  open Chromium on the SAME `threads_state.json`. Same-minute concurrent runs
  risk cookie/session collision. Offset the second channel by 30 min.
- **3+ channels on the same host**: every additional channel needs its OWN
  distinct time slot on `threads_state.json` (shared session cookie). Living
  config 2026-08-27 = psychology 20:00, macro (MIT) 20:30, How Leaders Lead
  21:00. Rule of thumb: stagger poster crons 30 min apart in order of addition;
  never two posters at the same minute. The drafter crons can stay any time
  they don't collide with each other's Edge profile (they only touch Chromium
  for the syllable check, not posting).

### Multi-post-per-run poster (3 bài/ngày variation)
A course plays 1/day so the scheduler posts 1 item/run. A PODCAST channel at
3 bài/ngày needs the scheduler to post up to N DUE items per run: sort pending
by scheduled_date, take the first N whose date <= today, post each, mark each
posted only on per-item success. HLL uses `hll-scheduler.py` (POSTS_PER_RUN=3)
-> "HLL POSTED 3: id1, id2, id3" in stdout. Keep the write-out of the queue
file until AFTER the loop so it flushes once with all newly-posted items.
- Channel daily drafter: `0 9 * * *`, script = the next-item resolver, with a
  long agent prompt that embeds the channel's writing-style rules and approval
  protocol ("gửi draft cho Quang duyệt, không tự đăng").

## draft-waiting resolver (prevents duplicate/overlap drafts)

`macro-next.py` decides what to draft next. A lecture is DONE if its video id
is in the queue (any status) OR a processed.json tracker. But approval is
human-delayed, so naive "next not-done lecture" re-drafts the UN-approved one
or stacks a new draft on top -> spam. Fix: if the earliest not-done lecture
already has a draft file on disk (`draft_lecture<index>.txt`) that is NOT yet
in the queue, emit `{"waiting": "lectureN"}` and the daily cron just says
"đang chờ anh duyệt lecture N" instead of drafting a new one. Only draft the
next lecture when no earlier draft is pending approval. This preserves the
"1 bài/ngày + duyệt 1 ngày trước đăng" rhythm.

## Content-domain style variants (IMPORTANT)

The 2-tầng mechanism structure ("Tầng 1 ... Tầng 2 vòng lặp", mở đầu phá giả
định, kết quote nguyên văn) is domain-flexible. The TEMPLATE stays; the
DOMAIN CONTENT changes. For a MATH/ECONOMICS course do NOT force the
neuroscience vocabulary (amygdala, PFC, dopamine, cortisol) — that reads
fabricated. Switch the mechanism layer to the discipline's models/terms:
- Economics: "Tầng 1, cơ chế:" name the model (GDP, IS-LM, Phillips curve,
  Mundell-Fleming, exchange rate) in plain language + exact figures quoted
  verbatim with the professor's name; "Tầng 2, vòng lặp/hệ quả:" what happens
  when the mechanism persists, applied to US/Vietnam. Same Quang voice
  (câu ngắn, kể chuyện, dấu đầy đủ, khẩu ngữ tự nhiên, no emoji/em dash).

Always ask Quang upfront which of: (a) separate channel posting immediately,
or (b) append to the shared queue's tail — before building. He chose (a) here.

## Verify before trusting the schedule
- `python scripts/macro-next.py` -> expect `next_index` of the earliest
  undrafted lecture.
- Run the channel poster manually same-day: it must exit silently (rc 0, no
  output) when the only pending item's scheduled_date > today (correct skip),
  leaving status `pending`.
- Confirm the venv python (`~/AppData/Local/hermes/hermes-agent/venv/Scripts/python.exe`)
  has playwright and `~/.hermes/threads_state.json` exists before relying on
  any future auto-post.