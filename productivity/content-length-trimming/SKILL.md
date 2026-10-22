---
name: content-length-trimming
description: Use when trimming a draft to a target character-count range.
---

# Content Length Trimming

Shorten an existing draft to fit a hard min/max character-count window (e.g. "reduce to 3900-4400 chars") **without** losing or fabricating any factual data.

## Golden rule: never trim by eye

On multibyte text (Vietnamese diacritics, accented languages, CJK), your character/word estimates are consistently WRONG — in practice the real `len()` is often far larger than you guess. Every rewrite must be measured by Python's actual `len()` on the exact string before it is committed to the file.

**Calibrated ratio (measured 2026-10, full Vietnamese diacritics): ≈1.32 bytes per character.**
- 6,999 chars = 9,244 bytes
- 7,773 chars = 10,263 bytes

Two consequences, both free:
- `write_file` returns `bytes_written` — divide by **1.32** for an instant char count with zero extra round trips. Use it as your first check after every write.
- To *hit* a target, write to a byte target: a **7,000-char cap ≈ a 9,200-byte write**. A 12,000-byte write is ~9,100 chars, i.e. already over.

`read_file` reports `file_size` in bytes too — same conversion applies; never read it as the char count.

If you write the file first and then check with a second call, you'll waste write-check cycles. Measure first, write last.

## Budget the first draft (not just trim it)

Trimming is damage control; budgeting avoids it. Vietnamese paragraphs with diacritics average **200-230 chars**, so:

- A 7,000-char cap ≈ **30-35 paragraphs** of ~2 sentences each.
- A 45-paragraph draft lands ~10,000 chars — already over the ceiling.
- Outline first and count the blocks. If the outline is longer than ~35 blocks, cut blocks **from the outline**, not from the finished text later.

See `references/vietnamese-draft-length-budget.md` for the full skeleton and the ranked cut list.

## Workflow

1. **Read** the whole file: `read_file(path)`.
2. **Baseline**: `python -c "s=open('F',encoding='utf-8').read(); print(len(s))"`. Note target and how much to cut (current - desired).
3. **Author the condensed version inside a Python script**, not directly into the file. Put each paragraph as an element of a list, `body="\n\n".join(paras)`, then print `len(body)` and each paragraph's length. This gives real numbers before any file write.
4. **Iterate in Python**: if total is still over the cap, apply targeted `.replace()` removals (drop filler clauses, merge sentences) against the exact strings in the script, and re-measure per-paragraph until the total lands inside the window.
5. Only when the script reports an in-range `len()` do you write the final content to the target file.
6. **Verify after writing**: re-open the actual file and confirm final `len()`, em/en-dash count = 0, and that every required key token (names, numbers, %, quotes) is still present.

### Fast path when the draft already exists

You will often already have a full-length draft sitting in a file — do not re-author it from scratch. Measure it, then delete whole blocks with `patch` (each patch prints a diff, so you see exactly what left). Re-measure every 2-3 cuts with `scripts/draft_metrics.py` rather than after every single cut.

## Preserve-data checklist (mandatory)

- Keep verbatim: all numbers, percentages, person names, company names, quoted phrases, show/product names.
- Keep `%`, decimal/grouped numbers exactly (`180.000`, `200.000`, `20%`).
- Never fabricate or add new content while trimming.
- Preserve section/paragraph structure (keep the same numbered paragraphs / blank-line blocks).
- Keep full Vietnamese diacritics.
- Do not introduce em dash (`—`, U+2014) or en dash (`–`, U+2013); use `:` or `;` instead. Verify with `count()`.
- Quotes are the last thing to cut. If a block you delete carries a pull-quote, keep the quote and shorten the narration around it instead.

## Pitfalls

- **Deleting beats rewording, and by a lot.** Measured on a real 10,524 → 6,999 pass: five successive *reword* attempts (tightening clauses, merging sentences) recovered only ~5-10% each and cost a tool call apiece; deleting three whole paragraphs (a side observation, a caveat, a redundant summary) landed the target in one move. **Rule: if you are more than ~15% over, stop rewording and delete whole blocks.** Rewording is for the last 5%, never the first 25%.
- **Accidentally cutting a pull-quote.** After deleting a block, re-read the diff. If a quote you meant to keep went with it, re-insert quote + one lead-in clause (~185 chars) as a single small patch — much cheaper than reworking a paragraph.
- **Estimating paragraph lengths is unreliable.** I repeatedly believed a paragraph was ~600 chars when it was ~800. Trust only the measured numbers.
- **Don't trim too timidly.** First trim passes may only shave a few dozen chars off a doc that needs ~800 cut. Make decisive cuts (drop whole expendable explanation sentences), then restore slightly if you dip below the lower bound.
- **Authoring in a helper script then copying to the file** avoids the write-check-the-real-file loop entirely. Keep a scratch file (e.g. `draft_new.txt`) for iteration, then overwrite the real target once, and `rm` the scratch + helper afterwards.
- **Windows bash `/tmp` quirk:** writing a script to `/tmp/x.py` in git-bash resolves to `D:\tmp` and python may not find it. Write helper scripts to an absolute path under the working dir instead.
- A `read_file` line like `N|text` carries a line-number prefix; the paragraph content starts after the `N|` — don't mistake that for content.

## Support files

- `scripts/check_length.py PATH [LO] [HI]` — re-runnable verification: prints `len()`, em/en-dash counts, per-paragraph lengths, and fails if final length is outside the target range.
- `scripts/draft_metrics.py PATH [LO] [HI]` — superset gate for social drafts: adds accent count, forbidden-CJK count, narrator-pronoun (`tôi`) count, and how the draft splits into ≤500-char Telegram parts (PARTS / MAX / OVER500). Use this one when the draft is headed to a chat platform.
- `references/vietnamese-draft-length-budget.md` — measured byte/char ratio, the ~30-block skeleton that lands in a 3-7K window, the ranked list of blocks to delete first, and the iteration order that actually converged.

## Related

- This complements the voice/AI-ism cleanup skills (`humanizer`, `html-unslop`); trim length first for structure, then apply voice edits if both are requested.
- For drafts that go to social platforms, the `threads-content-pipeline` / `auto-social-publisher` skills own the scheduling/posting side; this skill covers the length-constraint editing step they may reuse.
