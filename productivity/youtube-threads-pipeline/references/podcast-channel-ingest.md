# Podcast / whole-channel ingest (parallel content channel variant)

When Quang adds a full YouTube CHANNEL as a content source (hundreds of
podcast episodes), not a closed course playlist, use the parallel-channel
mechanism (see `parallel-content-channel.md`) with these channel-specific
rules. Verified 2026-08-27 case: `@HowLeadersLead` (How Leaders Lead, David
Novak) — 282 uploads, kept 109 after duration filter. User order: "xếp sau
các bài đó" (queue AFTER the preceding channel's items — macro first, then
this channel).

## Filter: drop SHORT videos (<30 min) at ingest
User correction: "bỏ hết video ngắn đi, chỉ lấy >30p thôi." A channel's
uploads tab is full of 2-5 min promo/teaser clips that are NOT podcast
episodes and give thin transcripts (HLL: 173/282 were <=30 min).

- `yt-dlp --flat-playlist -J` channel dump: each entry already carries
  `duration` (seconds) — no second pass needed.
- Keep only `duration > 1800` (30 min). HLL went 282 -> 109, avg ~60 min,
  range 33-92.
- Do the keep-drop in the SAME python that writes the channel playlist JSON,
  and recompute a fresh sequential `index` over the kept set (indices shift
  when clips are dropped — a stale index breaks the draft-waiting resolver).

## Cadence + style (differ from a course)
- Course (formal lecture, e.g. MIT 14.02): 1 bài/ngày, full 2-tầng mechanism
  structure.
- Podcast channel (conversational interview): user chose **3 bài/ngày** and
  **"transcript + summarize"** style — a tighter one-pass summary, NOT the
  full 2-tầng mechanism build. Keep the Quang voice (câu ngắn, mở đầu phá
  giả định / hồi tưởng, quote nguyên văn con số + câu chốt) but go lighter:
  pick the 1-3 strongest ideas, the most human moment, and one punchline
  quote. ~3-4K chars (≈7 parts at 500) vs a course's 6.5-8K.
- Confirm cadence + style ONCE per channel before bulk-building. Quang said
  "làm thử trước đi để anh duyệt": draft ONE episode, show the FULL draft,
  get "ok" on the voice, then queue the rest.

## Approval model — offer A/B/C once, let Quang pick (2026-08-27)
For a HIGH-VOLUME channel (100+ episodes) the per-draft approval cadence is a
bottleneck (3/day x 109 episodes = ~36 days of 3 approvals a day). Rather than
assume, offer three modes and let him choose:
- **A full-auto**: cron writes + posts 3/day, NO per-draft approval. Lightest
  for him; risk a weaker episode slips through.
- **B batch weekly** (Quang chose B): cron writes drafts to disk daily, one
  weekly review of the whole lot (e.g. "có N draft chờ, cuối tuần duyệt cả
  lô"), only then queue + post. Balances control vs his time.
- **C per-draft** (course rhythm): approve each before scheduling. Safest,
  heaviest on him.
His pick B => the drafter cron should SEND A ONE-LINE SUMMARY (titles +
chars/parts + one punchline quote each) instead of the full draft, and
explicitly say draft files wait for the batch review. Full drafts stay on disk
(`draft_hll_ep<index>.txt`) until the batch "ok"; the resolver treats an
un-approved on-disk draft as NOT done (so it isn't re-drafted), and a
drafted-but-not-queued episode blocks the next one only in "waiting" mode, not
in B mode where drafts accumulate freely.

## Trap: first episode is a short clip
If the first episode's transcript is only a few K chars (vs 40-65K for a real
episode), it's a promo clip that fell through the duration filter. Re-check
durations and pick the first episode that is genuinely >30 min as the sample.