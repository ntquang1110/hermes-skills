# Worked example — splitting `knowledge-researcher` (2026-10-19)

Measured case for the router split. Use it as a sizing reference: how much a real
oversized SKILL.md holds per section, and what a healthy post-split shape looks like.

## Target

| item | value |
|---|---|
| Skill | `research/knowledge-researcher` (Knowledge Flow app ops skill) |
| SKILL.md before | **104,674 bytes** (1,738 lines, pure CRLF) |
| Budget | under 50,000 bytes |
| SKILL.md after | **46,156 bytes** (818 lines) |
| Moved bytes | 62,000 (against 104,674 total = 59%) |
| New refs | 5 files |
| refs/ after | 13 files / 101,181 bytes |

## Byte table that drove the choice (level-2 sections)

| section | bytes | kept inline? |
|---|---|---|
| Research → KFlow sync (run history 2026-09-25 → 2026-10-19) | 31,931 | moved (split: pipeline inline, log moved) |
| Feed View — UX Patterns | 16,050 | moved |
| Pitfalls | 12,683 | kept (consulted when things break) |
| Card Detail — 2-Tab System | 8,254 | moved |
| ⚠️ QUALITY GATES | 6,492 | kept |
| Research Queue — Auto-Research Cron | 5,641 | kept (operational) |
| Systematic Gap Analysis | 4,983 | kept |
| Deployment — Production Mode | 4,802 | moved |
| Real-Time Search | 2,000 | kept |

Rule observed: keep operational/quality/debugging sections inline; move chronological
logs, UI implementation detail, and long-documented feature sections.

## Files created

| ref file | bytes |
|---|---|
| `references/kflow-sync-run-log.md` (per-run history + lessons, `### Sync run …`) | 29,014 |
| `references/feed-view-ux.md` | 16,417 |
| `references/card-detail-2tab.md` | 8,361 |
| `references/deployment-production-mode.md` | 4,893 |
| `references/kflow-sync-pipeline.md` (job + scripts + tab-extraction recipe) | 3,317 |

SKILL.md kept each original `## heading` as a router title + 1-3 pointer lines, and
gained a trailing `## References — chi tiết tách riêng` index (which also linked three
previously orphaned refs: `design-system-v1.md`, `cron-port-hallucination.md`,
`production-deployment.md`).

## Command that produced it

Done with an inline Python script (slice by heading anchors, write chunks, rebuild),
equivalent to:

```bash
python scripts/split_skill_md.py SKILL.md \
  --move '## Feed View|## Book View|feed-view-ux.md|card preview, infinite scroll, read-status, live search, share, OG redirect, route handler, schedule page, responsive' \
  --move '## Research → KFlow sync|### Sync run 2026-09-25|kflow-sync-pipeline.md|gap the job fills, html2md/kf_push_backlog/kf_verify, tab-extraction recipe, passcode cookie, diacritics gate, dedup' \
  --move '### Sync run 2026-09-25|## Card Detail|kflow-sync-run-log.md|per-run history and lessons 2026-09-25 → 2026-10-19' \
  --move '## Card Detail|## Dashboard View|card-detail-2tab.md|2 tabs, 13/08/2026 standard, OVERVIEW-block pitfall, Structured Overview/parseAzuEasy' \
  --move '## Deployment — Production Mode|## Verification|deployment-production-mode.md|start/update runbook, cache clean, why not dev mode' \
  --index
```

Note the sub-section split: the KFlow `##` section was cut in two — `## …` → first
`###` went to the pipeline ref, `### …` → next `##` went to the run-log ref, and the
router listed both files.

## Verification output (all three gates)

```
orig bytes 104674 lines 1738
WROTE feed-view-ux.md                          16417 bytes  (orig lines 48-413)
WROTE kflow-sync-pipeline.md                    3317 bytes  (orig lines 1037-1085)
WROTE kflow-sync-run-log.md                    29014 bytes  (orig lines 1086-1435)
WROTE card-detail-2tab.md                       8361 bytes  (orig lines 1436-1541)
WROTE deployment-production-mode.md             4893 bytes  (orig lines 1638-1727)
NEW SKILL.md bytes 46115
VERIFY1 ok: all ref files byte-identical to their original chunk
VERIFY2 reconstruct == original: True
orig headings 117 missing: []
VERIFY3 ok
```

Final on-disk check: `orig-minus-moved == SKILL.md-minus-routers-minus-index` → True
(the only delta was a 2-byte trailing CRLF produced by the check itself).

## What went wrong on the way (now encoded as pitfalls in SKILL.md)

1. `open(SKILL.md, 'wb')` truncated the skill to **0 bytes** before
   `new_text.encode('utf-8')` raised. Root cause of the encode error: a Python literal
   containing half an emoji (`'\ud83d\udcda'`) →
   `UnicodeEncodeError: surrogates not allowed`. Fixed by (a) real emoji/omitted emoji,
   (b) temp file + `os.replace()` after building the bytes, (c) restoring from the
   backup copy that had been taken first.
2. Routers and the appended index were written with `\n` into a CRLF file → 26 LF-only
   lines. Normalised the whole file afterwards; `CR == LF == 818`.
3. `skill_view` reported a different `skill_dir`
   (`…\AppData\Local\hermes\skills\research\knowledge-researcher`) than the path edited
   (`D:\Hermes\hermes-home\skills\research\knowledge-researcher`). Both roots resolve to
   the same file (`wc -c` identical: 46,156) — the skills tree is symlinked, so there was
   never a second copy to fix.
