## Research → KFlow sync (job `da7c6b38c7d9`, 00:00 daily) — 2026-09-23

**Gap it exists to close:** the `knowledge-researcher-4h-rotation` job (d43697af1322) goes
`research → HTML 2-tab → preview.thefirstonly.com → research-log.md` and **does NOT POST to
KFlow** (its STATE notes: "không POST KF, tránh duplicate"). Result: from 2026-09-20 16:00
onwards, every research item existed only as HTML + preview URL. The daily 00:00 job
"Auto-push research to Knowledge Flow" is the sync step.

**Reusable scripts (built 2026-09-23, work end-to-end):**
- `C:/Users/NTQUANG_DELL/hermes-temp/html2md.py` — tolerant HTML→markdown via `html.parser`
  (handles `<p>`-based AND div-based layouts: fn-t/fn-d/callout/card/stat).
- `C:/Users/NTQUANG_DELL/hermes-temp/kf_push_backlog.py` — parses `research-log.md`
  entries for title/summary/source_url, extracts the **academic tab**, builds the
  `<!--OVERVIEW-->` block from the **visual tab**, dedups against `/api/cards`,
  runs the diacritics gate, POSTs. Modes: `--dry ALL`, `--dry <key>`, `--force <key>`.
- Verification: `C:/Users/NTQUANG_DELL/hermes-temp/kf_verify.py` (prints new cards since a
  timestamp with OVERVIEW/length/tags/source).

**HTML structure varies per file — never rely on fixed panel ids.** Seen in the wild:
`viz/acad`, `pv/pa`, `pane-v/pane-a`, `tab-visualize/tab-academic`, `panel_vis/panel_hoc`,
`pa0/pa1`, and index-based `showTab(0)/showTab(1)`. Robust recipe:
1. Read the tab buttons: `<button ... onclick="showTab('id'|N)">Visualize|Học thuật</button>`
   → map label → panel id (or index).
2. Extract each panel as a **region**: from the panel's opening tag to the NEXT panel's
   opening tag (or `</body>`). Do NOT use depth-matching div scans — one unclosed inner
   `<div>` truncates the content silently (polymer/co-dinh-dam lost 60-70% of text this way).
3. Convert with `html2md.html_to_md` (regex-only converters miss div-based text blocks:
   superconductivity-2tab.html has only 3 `<p>` tags and md collapsed to 998 chars;
   after html2md it is 5855 chars).

**Passcode gate:** every KFlow call needs
`Cookie: tfo_auth=1d1e977a218bfa01fe61106c360c8acf667047e35f17fdb0f1a8484e06cfdb55`
(headers: `Authorization: Bearer hermes-knowledge-secret`). Without it `/api/*` → 307 → `/passcode`.

**PITFALL — never PATCH/POST Vietnamese via `curl -d`.** The MSYS shell mangles UTF-8 in the
request body and the DB row ends up as `? ??ng h? sinh h?c` (happened 2026-09-23 on the
circadian card title; fixed with a `write_file` + `urllib.request` script). Use Python
(`json.dumps(..., ensure_ascii=False).encode("utf-8")`) for ALL writes with diacritics.
`GET` via curl is fine.

**Diacritics gate before pushing:** `accent_ratio(md) < 0.15` → reject. The 2026-09-22 20:00
run shipped `nuclear-fusion-2tab.html` and `activated-carbon-2tab.html` with **zero
diacritics** (Q1 fail) — they were deliberately NOT pushed and need regeneration.

**Dedup false positives:** keyword overlap ≥ 0.6 fires on shared compound lists
(e.g. "Biochar … Pb/Cd/As/Cr" vs "Xử lý KHÔ — As, Pb, Hg, Cd"). Always read the flagged
title before skipping; use `--force <key>` for a false positive. Real duplicates (2 existing
PRRSV mechanism cards) should stay skipped.

