---
name: skill-library-maintenance
description: "Use when compacting or auditing an oversized skill library."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [skills, maintenance, refactor, progressive-disclosure, token-efficiency, skill-md]
    related_skills: [hermes-core-token-efficiency, state-file-protocol]
---

# Skill Library Maintenance

A skill library inflates over time, and every oversized SKILL.md is paid for in context on each
load. This skill covers the maintenance side of skills:

1. **Audit** — find which SKILL.md files are oversized.
2. **Split** — turn an oversized SKILL.md into a compact router + `references/` files, moving
   content **verbatim** (never summarising it away).
3. **Verify** — prove mechanically that no heading and no line was lost.

Scope note: the bundled `hermes-agent-skill-authoring` skill owns *authoring new* skills
(frontmatter, placement, peer structure) — it is bundled, so curator writes to it are refused.
This skill owns *maintaining and compacting existing* skills. Overlap is intentional; extend this
one when the task is "shrink / reorganise an existing skill".

## When to use

- A SKILL.md is over ~20k chars (hard cap: `MAX_SKILL_CONTENT_CHARS` = 100,000 chars)
- User says "tách skill", "compact this skill", "skill quá to / ngốn context"
- A task requires **100 % information retention** while shrinking a skill (move, don't delete)
- You need evidence that a skill refactor lost nothing (heading audit + line audit)
- Reference files have grown unwieldy (no index, mixed naming, orphans)

## Step 1 — Audit sizes

```bash
wc -c */SKILL.md | sort -n          # per-category directories
python scripts/skill_split_helpers.py analyze path/to/SKILL.md
```

`analyze` prints every `## ` heading with its line range and byte size, plus the `### ` sub-headings
that mark further cut points. Completion criterion: an explicit line-range → bytes table, because
Step 3 slices **by line range** — no table, no split.

Target shape per skill: body 8–15k chars, with bulky/branch-specific detail behind pointers.

## Step 2 — Back up outside the skill dir

```bash
cp SKILL.md /path/outside/skill-dir/SKILL.md.orig.bak
```

Keep the backup **outside** the skill directory (so it is not mistaken for a skill file). It is the
"before" file that Step 5 verifies against and the rollback if the split goes wrong.

## Step 3 — Slice verbatim by line range (never retype)

```python
raw   = open(SKILL, 'rb').read()
lines = raw.split(b'\n')                 # CRLF preserved: each element keeps its trailing \r
def L(a, b):                             # 1-indexed inclusive, byte-for-byte
    return b'\n'.join(lines[a-1:b])
def T(s):                                # str -> utf-8 bytes
    return s.encode('utf-8')

# refuse to clobber an existing reference file
if os.path.exists(p): raise SystemExit("REFUSE: existing file -> " + p)
open(p, 'wb').write(T("# Section title\n\n") + L(475, 691) + b'\n')
```

Pick sections that are **large and rarely needed together with the rest**: long code/API
walkthroughs, history, case studies, long tables, provider quirks. Keep in SKILL.md the short
high-frequency sections, the frontmatter, every `## ` heading, and any index table that already
works as a router (that is discovery value, not sprawl).

Completion criterion: one `references/<topic>.md` per moved section, each with only a one-line H1
title prepended, body untouched.

## Step 4 — Rebuild SKILL.md as a router

Each remaining section = its original heading + intro, then **1–3 lines** naming what the moved
file contains and pointing at it:

```
**Level 2c — PubMed E-utilities.** Full three-endpoint workflow, query-quality traps, verified-PMID
discipline, E-utilities pitfall list: `references/strategy-level-2c-pubmed-eutils.md`
```

Concatenate pieces with an explicit `b'\n'` between them (see pitfall 2). Keep the description's
meaning intact; shortening wording is fine, changing the trigger is not.

## Step 5 — Verify mechanically, then report

```bash
python scripts/skill_split_helpers.py verify path/to/SKILL.md.orig.bak path/to/skill-dir
```

Exit 0 means: every non-empty line **and** every `## ` heading of the original still exists
somewhere in `SKILL.md` + `references/*.md`. Then additionally confirm:

- each moved block is **byte-identical** to its original slice (normalise line endings on both
  sides before comparing bytes — see pitfall 4);
- `skill_view(name='<skill>')` still loads and lists the new files;
- grep for your own escaping artifacts (`\\u20`, stray `\r\r`).

Report: bytes before → after, each new reference file with its byte size, and an explicit
"No heading lost / 0 lines lost" confirmation.

## Pitfalls

1. **`\u` escapes are NOT processed inside bytes literals.** `b"\u2014"` writes the literal text
   `\u2014`, not an em dash. Build text as `str` and `.encode('utf-8')`. Symptom: section titles
   read `Level 1 \u2014 search engines`.
2. **`b'\n'.join(chunk)` has no trailing newline.** `sliceA + sliceB` fuses the last line of A with
   the first line of B, and the verifier then reports the fused heading as "missing". Always insert
   an explicit `b'\n'` between concatenated pieces.
3. **Mixed line endings.** Sliced originals are CRLF; freshly written Python strings are LF.
   Normalise the whole set once at the end:
   `.replace(b'\r\n', b'\n').replace(b'\r', b'\n').replace(b'\n', b'\r\n')` — match whatever the
   rest of the library uses rather than forcing LF.
4. **A verifier that normalises only one side gives false failures.** `.replace(b'\n', b'\r\n')` on
   text that already contains CRLF yields `\r\r\n` and every comparison fails. Normalise **both**
   sides to the same form first.
5. **Text-only checks are not enough.** The line audit passes happily on a file whose titles are
   corrupted by pitfall 1 — grep your artifacts after writing.
6. **Never "summarise instead of move".** The 1–3 line router entry is the only place you may write
   prose; if a sentence is worth keeping it must exist verbatim in one of the files.
7. **Do not write over an existing reference file.** Name-check before every write; a colliding name
   silently destroys prior content that `wc -c` will not flag.
8. **Editing a skill dir that is junctioned elsewhere** still hits the live skill — verify by
   `skill_view`, not by path bookkeeping.

## Verification checklist

- [ ] Size audit table exists (heading → line range → bytes) before any slicing
- [ ] Backup of the original SKILL.md exists **outside** the skill dir
- [ ] Every moved block is byte-identical to its original slice (line endings normalised for the comparison)
- [ ] `python scripts/skill_split_helpers.py verify <orig> <skill_dir>` exits 0
- [ ] Every original `## ` heading still present in SKILL.md
- [ ] Frontmatter kept; description meaning unchanged
- [ ] No existing reference file was overwritten
- [ ] `skill_view(name='<skill>')` loads and lists the new files
- [ ] Report states before/after bytes, new files + their bytes, and the no-loss confirmation

## Support files

- `scripts/skill_split_helpers.py` — `analyze <SKILL.md>` (section line ranges + bytes) and
  `verify <orig> <skill_dir>` (zero-loss + heading audit, exit 1 on loss).
- `references/splitting-skill-md-into-references.md` — full worked recipe with the exact slicing and
  verification code, plus the debugging traps behind the pitfalls above.
