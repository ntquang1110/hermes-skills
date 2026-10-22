---
name: skill-library-refactoring
description: "Use when a SKILL.md is too big/oversized/over budget and must be split losslessly into references/ (tách skill gọn, chuyển section dài ra file tham chiếu, giữ nguyên 100% thông tin, verify không mất heading/byte), or when a skill library must be compacted without deleting content. MUST use whenever a byte/char budget is given for a skill file. Not for authoring a new skill (use hermes-agent-skill-authoring) or for deleting obsolete content."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [skills, refactoring, progressive-disclosure, context-efficiency, verification]
    related_skills: [hermes-core-token-efficiency, state-file-protocol]
---

# Skill Library Refactoring

## Overview

Reshape skill files without losing a single byte of information: turn an oversized
`SKILL.md` into a lean **router** plus `references/*.md` payload files, re-index orphan
references, and re-home knowledge that was pasted into the wrong skill.

Two rules define this class of work:

1. **Move, never summarise.** Refactoring is a change of *location*, not of content.
   Every moved chunk is copied verbatim, and the result is *proven* lossless by
   reconstruction — not by eyeballing a diff.
2. **Do it with code, not by retyping.** Re-emitting 60 KB of a file through the model
   invites silent paraphrase/omission. Slice the original bytes with a script and let
   verification (not trust) establish correctness.

Rule of thumb for when a SKILL.md needs this: past ~20k chars, or past whatever budget
its owner set (e.g. "get it under 50,000 bytes") — bulky, low-frequency sections (run
logs, history, implementation detail, long tables, case studies) belong in `references/`.

## When to Use

- A `SKILL.md` is over budget and must shrink while keeping 100% of the detail.
- Sections in one skill are clearly payload (chronological logs, deep implementation
  notes, long reference tables) that an agent only needs on demand.
- Reference files exist but nothing in SKILL.md points at them (orphan refs).
- Knowledge was pasted into the wrong skill and needs re-homing.

Don't use for: authoring a brand-new skill from scratch, or trimming content that is
genuinely obsolete (that is deletion, and needs explicit user intent). For frontmatter/
structure conventions of SKILL.md itself, see the bundled `hermes-agent-skill-authoring`.

## Workflow

1. **Measure before moving.** List every level-2 heading with its line range and byte
   size:
   ```python
   starts = [i for i, l in enumerate(lines) if l.startswith('## ')]
   # bytes per chunk = len('\n'.join(lines[s:e]).encode('utf-8'))
   ```
   Completion criterion: you have a table heading → bytes for the whole file, and the
   sections you will move sum to more than (current size − target).
2. **Pick the payload sections**, largest and lowest-frequency first (history/run-log →
   implementation detail → long tables → case studies). Keep operational sections inline
   (deploy, verify, quality gates) — a router that points everything away is worse than
   the original.
3. **Move with code.** `scripts/split_skill_md.py` (bundled with this skill) does the
   whole job: slices chunks verbatim, writes refs, keeps each original heading as a
   2-3 line router, appends a References index, backs up, writes atomically, and
   verifies. Example:
   ```bash
   python scripts/split_skill_md.py path/to/SKILL.md \
     --move '## Feed View|## Book View|feed-view-ux.md|card preview, scroll, read-status, share, OG redirect' \
     --move '### Sync run 2026-09-25|## Card Detail|kflow-sync-run-log.md|per-run history and lessons' \
     --index
   ```
   Router line shape (1-3 lines, always naming the file):
   "Chi tiết: `references/<file>.md` — <what is inside>".
4. **Copy the original FIRST, then prove losslessness** (the script exits non-zero
   otherwise):
   - **V0** snapshot the untouched original (`SKILL.md.bak-<ts>` / `bak/SKILL.md.orig`)
     *before* the first write. Every equality check below is against this file, and it
     is the only copy — the split overwrites the only other one.
   - **V1** each ref file is byte-identical to the chunk it replaced;
   - **V2** original == inline remainder + ref contents (reconstruct the original and
     compare exactly);
   - **V3** every h1–h4 heading of the original still exists in SKILL.md or a ref;
   - **V4** after ANY post-split edit (index block, reworded pointer), V2's exact
     equality is invalidated by design — prove the delta is only intentional by
     enumerating diffs: `difflib.unified_diff(original_non_moved_lines,
     current_minus_router_blocks_minus_added_block)`. Expect a short, reviewable diff,
     not an empty one.
   Lost the original before V0? Recover it from Hermes observation logs — see
   `references/independent-loss-verification.md`. Re-runnable checker for V2/V3/V4:
   `scripts/verify_split_against_original.py`.
5. **Verify on disk and report.** `wc -c SKILL.md`, list `references/` with sizes, then
   `skill_view` the skill to confirm the loader sees the new refs. Report: sizes
   before/after, each new ref + bytes, and the V1/V2/V3 confirmation.
6. **Keep a rollback copy.** The script writes `SKILL.md.bak-<ts>`; leave it in place
   until the user confirms.

## Pitfalls

1. **Opening the target with `'wb'` truncates it before the write can fail.** A single
   `UnicodeEncodeError` mid-run leaves a 0-byte SKILL.md. Build the bytes first, write a
   `.tmp`, then `os.replace()`; copy a `.bak` before anything else.
2. **Lone surrogate escapes blow up the encode.** A Python literal like
   `'\ud83d\udcda'` (half an emoji) raises
   `UnicodeEncodeError: 'utf-8' codec can't encode ... surrogates not allowed`.
   Use real emoji characters, or omit them.
3. **Mixed line endings.** Router/index text written with `'\n'` into a CRLF file leaves
   LF-only lines. Normalise at the end
   (`t.replace('\r\n','\n').replace('\n','\r\n')`) and check `CR count == LF count`.
4. **Chars ≠ bytes.** `len(text)` counts CRLF as 2 chars and Vietnamese as 1 char;
   budgets and `wc -c` are bytes. Always report `len(s.encode('utf-8'))` / `wc -c`.
5. **Hand-written routers drift from reality.** Describe only what the moved chunk
   actually contains — read it before writing the pointer line. No invented headings.
6. **Orphan references.** After moving, add (or refresh) a trailing
   `## References — chi tiết tách riêng` index listing *every* ref file so pre-existing
   orphans get linked too.
7. **Protected skills refuse writes.** Bundled/hub/pinned/user-owned skills answer with
   e.g. `Refusing background curator write_file for bundled skill '<name>'`. Don't fight
   it: put the technique in a curator-managed skill and tell the user
   (`hermes curator adopt <name>` if they want the original editable).
8. **`skill_manage(action='patch'|'edit')` can refuse an oversized result** — once the
   file is small, plain `write_file` (or the script) is the reliable path.
9. **Assume nothing about paths.** The same skill tree can be reachable through two
   roots (e.g. `…\AppData\Local\hermes\skills\…` symlinked to `D:\Hermes\hermes-home\skills\…`);
   the same file is behind both. Confirm identity with `wc -c` instead of "fixing" a
   phantom second copy.
10. **Deleting to hit a budget is a different task.** If a section genuinely no longer
    applies, surface it to the user for a decision — this skill only relocates.
11. **Skipping the pre-split snapshot costs an hour of forensic recovery.** Once the new
    SKILL.md is written, the original exists nowhere — no git, no `.bak`, and the
    user's stated "before" size is not proof. Recovery is possible (observation logs,
    see `references/independent-loss-verification.md`) but it is archaeology. Snapshot
    first; it is one line.
12. **Reporting "0 lost" from a self-referential check.** "refs contain what I wrote to
    refs" and "rebuilt-from-my-own-router == original" only prove internal consistency.
    Anchor at least one check to an artifact you did not produce: an independent copy of
    the original, a `wc -c` taken before the edit, or the observation log.
13. **Proof buried in stdout is proof nobody reads.** Long verification printouts can
    come back collapsed/truncated from the terminal tool. Write the report to a file
    (`python verify.py > verify_out.txt`) and `read_file` it — same discipline for V1–V4
    evidence as for the sizes you report at the end.
14. **Moving a section that other sections point at.** A pointer like "see the section
    below" / "chi tiết ở mục X bên dưới" silently rots when X becomes a ref file. After
    the move, grep for `bên dưới` / `below` / `above` / `mục` and repoint each one at the
    ref file — that rewording is the one legitimate content *edit* in this workflow, and
    it belongs in the V4 delta list.

## Verification Checklist

- [ ] Byte table of original computed (per level-2 section) and target size stated
- [ ] Moved sections are payload-class (history/detail/tables), not operational steps
- [ ] Content cut/pasted by code — no section retyped or paraphrased
- [ ] V0 pre-split snapshot taken BEFORE the first write (`SKILL.md.bak-<ts>`), and its
      location reported to the user
- [ ] V1 refs byte-identical to their original chunks
- [ ] V2 original == inline remainder + refs (exact equality, not "looks fine")
- [ ] V3 no heading lost (h1–h4 census across SKILL.md + refs)
- [ ] V4 post-edit delta enumerated with `difflib.unified_diff` and every hunk
      accounted for (index block, repointed pointers, nothing else)
- [ ] Byte closure printed: original − moved + router(+index) == new size, exactly
- [ ] Pointers that said "below/above/bên dưới/mục X" repointed at their new ref file
- [ ] SKILL.md retains frontmatter and every surviving section has a 1-3 line pointer
- [ ] `wc -c` SKILL.md within the stated budget; refs listed with sizes
- [ ] References index lists all ref files, including previously orphaned ones
- [ ] `skill_view` loads the skill and shows the new linked files
- [ ] Rollback copy (`SKILL.md.bak-<ts>`) left in place; report delivered

## Support files

- `scripts/split_skill_md.py` — the lossless splitter + verifier described above
  (`--move`, `--index`, `--dry-run`; exit 0 only when V1/V2/V3 pass).
- `scripts/verify_split_against_original.py` — re-runnable V0–V4 checker for
  *after* the split, including post-split edits: `--original <bak>` `--skill <SKILL.md>`
  `--refs <references/> [--added-block-prefix "**Reference files"] [--out report.txt]`.
- `references/independent-loss-verification.md` — how to recover the pre-split bytes from
  `~/.hermes/observations/*.json` when no snapshot exists, plus the V4 accepted-diff
  recipe and the byte-closure table of the 112,959 → 38,521 byte `ai-company-ops` split.
- `references/knowledge-researcher-split.md` — worked example with measured numbers,
  exact command line, and the verification output of a 104,674 → 46,156 byte split.
