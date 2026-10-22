# Auditing a cron research run that produced NOTHING (the inverse of a healthy batch)

`references/auditing-daily-research-batches.md` covers the **healthy** case: a
day's `research-log-YYYY-MM-DD.md` exists listing N published articles.

This file covers the **inverse**, verified 2026-10-04 on job `d43697af1322`
(`knowledge-researcher-4h-rotation`): the log route yields *nothing*, because
the job died before writing a log. Without this branch you conclude "no research
today" and report an empty day — which was wrong; 728 KB of good sources were on
disk, orphaned.

**Trigger:** the truncated audit prompt fires, the log for today is absent, and
`ls` of the expected research dir shows source files but no `.html`.

## The signature — check these four together

A dead-mid-run research job leaves a very specific fingerprint:

| Check | Dead-run result | Healthy-run result |
|---|---|---|
| `research-log-YYYY-MM-DD.md` | **missing** (newest log is days old) | present, today's date |
| `*.html` in the day dir | **zero** | one per article |
| raw source `.txt`/`.json` | **many, large** (fetch succeeded) | few/absent |
| `preview.thefirstonly.com` links in dir | **zero** | one per article |

Sources present + zero HTML + zero preview URLs = **the job died between fetch
and build.** The research was real; the deliverable was never produced. Report
it as wasted work, not as "no research happened".

## Why the log route fails here (do not keep retrying it)

The existing recipe's Step 0 says "read the day's research log first — it is the
manifest." That works only if a previous run logged. Oct 04 had 82 prior
`cron_complete` runs but the newest log was **Oct 02** — the log had already
stopped being written for days. So the manifest was stale, not merely absent.

Corollary worth stating in any report: *a job that reports `cron_complete` every
day may have produced nothing for days.* `end_reason` is a lifecycle marker, not
a success assertion. Check artifacts on disk.

## Step 1 — Reconstruct from state.db, not from the filesystem

`search_files` / `find` over `~` or `/d` starves (exit 124 at 180 s on this
host). Go straight to `state.db` and list the day's cron sessions:

```bash
python "C:/Users/NTQUANG_DELL/AppData/Local/hermes/skills/productivity/cron-job/scripts/audit_cron_session.py" --date 2026-10-04 --jobs-json --job d43697af1322
```

Schema facts that cost calls if forgotten:

- `sessions.started_at`, **not** `created_at` (querying `created_at` raises
  `sqlite3.OperationalError: no such column`).
- `sessions.ended_at` / `end_reason` — `NULL` means never finalised.
- `messages.timestamp` is a float unix ts; convert with
  `datetime.datetime.fromtimestamp(ts)`.
- `messages.tool_calls` is a **JSON string** — `json.loads` it to see the
  `write_file` paths and `terminal` commands. This is how you learn which
  directory the job actually wrote to.
- Build the epoch with `datetime.datetime(2026,10,4).timestamp()` (local time),
  not a UTC assumption.

## Step 2 — Dump the one session that matters

```bash
python ".../scripts/audit_cron_session.py" --session cron_d43697af1322_20261004_080019 --jobs-json
```

The full dump (62 messages on Oct 04) reconstructs the entire run: which fetch
scripts it wrote, which sources came back empty, and **the last assistant text
before it stopped**. On Oct 04 that last line was *"Giờ build bài 1 — Cơ học lưu
chất (Vật lý)"* — it died exactly at the first build step.

Reading the last assistant message is the single highest-signal move in the
whole audit. It names the step that failed.

## Step 3 — `--jobs-json` finds the dead skill in the config

The script walks the job's `skills:` list against the real skill directories and
prints which entries do not exist. Oct 04:

```
skills   : ['web-research', 'visual-academic-html', 'html-publishing', 'dashboard-design-system']
!! MISSING SKILL: 'html-publishing' is listed but not on disk.
```

`visual-academic-html` also moved category (`software-development/`, not
`creative/` as the skills list claims) — so a category-based search will miss a
skill that is actually present. Always search by **directory name across all
roots**, never by the category column of the skills list.

Fix: `hermes cron edit <job> --skills <list minus the dead one>`. A job that
lists a skill it does not have runs fine until it reaches that step, then stops.

## Step 4 — Triage the fetched sources by size before reporting

Same byte-size check as the healthy path, inverted in meaning: here it tells you
*how much of the fetch phase succeeded*, which sizes the loss.

```bash
cd ~/hermes-temp/research-YYYYMMDD
for f in *.txt; do printf "%-24s %8d\n" "$f" $(wc -c < "$f"); done | sort -k2 -n
ls *.html 2>/dev/null || echo "KHONG CO FILE HTML NAO"
grep -rn "preview.thefirstonly.com" . || echo "0 preview URL"
```

Oct 04: 13/19 files >500 bytes, 728 KB total — solid sources. 6 empty, and **every
one carried the text `ERROR HTTP Error 429: Too Many Requests` inside the file**.
That is a distinct tell from the Wikimedia "You are making too many requests"
rate-limit text in the sibling reference: here the fetch script *recorded the
error as file content and moved on*, so the file exists and looks like data.

**Name the failure per file** in the report (`wiki_thei.txt` 93 bytes, contains
429) — never "some sources failed".

## Step 5 — Rank causes by what actually cost the work

On Oct 04 the causes were, in order of consequence:

1. **Job died at first build step.** 62 messages in, zero HTML out. Root cause
   was the provider/model — check `sessions.billing_provider` against the job's
   configured `provider`; if they differ, a silent fallback fired.
2. **Dead skill in `skills:`** — `html-publishing`. Would have killed the run at
   the publish step regardless of provider health.
3. **6 rate-limited fetches silently accepted** — the fetch script printed the
   429 into the file and continued.

Report all three. The tempting-but-wrong summary is "the job failed"; the useful
one is "the fetch phase worked and its output is still on disk — the build phase
never ran, here are the three reasons."

## Report shape for a zero-deliverable day

Quang reads for defects. Lead with the verdict, not the process:

1. **Verdict first:** how many research items were created (often 0), stated plainly.
2. **Table** of what the job *did* produce (topic group → sources → byte size),
   so the salvageable work is visible.
3. **Numbered causes**, each naming the file / job field / line.
4. **What is still on disk** — the exact directory, since a follow-up run can
   reuse those sources instead of re-fetching.
5. **Ordered fixes** with the real cost, ending by offering to execute.

Do **not** recommend re-running the job blind. First fix the provider and the
dead skill, or the re-run reproduces the same zero.

## Related

- `references/auditing-daily-research-batches.md` — the healthy-batch recipe
  (log as manifest, preview curl checks, structural grep). Read that first; this
  file is what to do when it returns nothing.
- `scripts/audit_cron_session.py` — the state.db forensic scanner used here.