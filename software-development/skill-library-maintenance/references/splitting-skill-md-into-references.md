# Splitting an Oversized SKILL.md into a Router + references/

Worked, verified recipe for the "SKILL.md > 20k chars → tách chi tiết ra references/" rule.
Goal: shrink the always-loaded body to 8–15k chars **without losing a single byte** — content moves,
it is never summarised or deleted.

Measured result of the run this recipe came from (`research/web-research`):
**102,431 → 19,659 bytes, 7 new reference files, 0 of 1,135 original non-empty lines lost.**

## When to use

- A SKILL.md is over ~20k chars and its body is mostly branch-specific detail (long code dumps,
  API walkthroughs, case studies, history, long tables).
- The user says "tách ra", "compact this skill", "reduce the skill to a router", or complains the
  skill is too big / eats context.
- The task explicitly requires **100 % information retention** — this recipe is built for that
  constraint (move verbatim, verify mechanically).

## Core idea

SKILL.md keeps: frontmatter → intro → the *short* sections → one router entry per moved section.
Everything else is **copied verbatim** (byte-for-byte, by line slice) into `references/<topic>.md`.
The router entry is 1–3 lines naming what is in the file, e.g.

```
**Level 2c — PubMed NCBI E-utilities.** Full three-endpoint workflow, query-quality traps,
verified-PMID discipline, E-utilities pitfall list: `references/strategy-level-2c-pubmed-eutils.md`
```

An index table that already functions as a router (e.g. a "reference bank" table listing sibling
files) should **stay** in SKILL.md — that is discovery value, not sprawl.

## Procedure

**Step 1 — Map the structure.**
```bash
python scripts/skill_split_helpers.py analyze path/to/SKILL.md
```
Prints the file size, every `## ` heading with its line range and byte size, the pre-heading body
(frontmatter + intro), and the `### ` sub-headings that mark further cut points. Completion
criterion: an explicit line-range → bytes table, plus a decision about which sections are large
**and** rarely needed.

**Step 2 — Back up the original.**
```bash
cp SKILL.md /path/outside/skill-dir/SKILL.md.orig.bak
```
Keep it outside the skill dir so it is not mistaken for a skill file. It doubles as the "before"
reference for verification (and as rollback).

**Step 3 — Slice verbatim in Python; never retype.**
```python
raw   = open(SKILL, 'rb').read()
lines = raw.split(b'\n')                       # CRLF preserved: each element keeps its \r
def L(a, b):                                   # 1-indexed inclusive, verbatim
    return b'\n'.join(lines[a-1:b])
def T(s):                                      # str -> utf-8 bytes (never bytes-literal \u escapes)
    return s.encode('utf-8')

content = T("# Section title\n\n") + L(475, 691) + b'\n'
```
Guard against clobbering existing files before writing:
```python
if os.path.exists(p): raise SystemExit("REFUSE: existing file -> " + p)
```
Completion criterion: each chunk written to `references/<topic>.md` with only a one-line H1 title
prepended; body untouched.

**Step 4 — Rebuild SKILL.md** as `keep-slices + router entries`, concatenating with an explicit
`b'\n'` between every piece. Keep the frontmatter, every original `## ` heading, and the short
high-frequency sections.

**Step 5 — Verify mechanically, then report.**
```bash
python scripts/skill_split_helpers.py verify path/to/SKILL.md.orig.bak path/to/skill-dir
```
Checks (exit 1 on failure): (a) every original non-empty line still exists somewhere in SKILL.md +
`references/*.md`; (b) no original `## ` heading disappeared. Then also confirm each moved block is
byte-identical to its original slice, and `skill_view(name='<skill>')` still loads. Report: bytes
before/after, each new reference file with its byte size, and the explicit "No heading lost /
0 lines lost" confirmation.

## Pitfalls that cost real time

1. **`\u` escapes are NOT processed in bytes literals.** `b"\u2014"` writes the literal character
   sequence `\u2014` into the file — not an em dash. Build router/title text as `str` and
   `.encode('utf-8')`, or use byte strings containing the real characters. Symptom: titles read
   `Level 1 \u2014 search engines`. Fix afterward, then grep for `\\u20` etc.
2. **`b'\n'.join(chunk)` has no trailing newline.** `A + B`, where `A` came from a slice, merges the
   last line of A with the first line of B. Always insert an explicit `b'\n'` between concatenated
   pieces. Symptom: two headings/paragraphs fused into one line, and the verifier reporting the
   second one as "missing".
3. **Mixed line endings.** Sliced originals are CRLF; freshly written Python strings are LF.
   Normalise the whole file set once at the end:
   `.replace(b'\r\n', b'\n').replace(b'\r', b'\n').replace(b'\n', b'\r\n')`.
   Match whatever the rest of the library uses rather than forcing LF.
4. **A verifier that normalises one side only returns false failures.**
   `.replace(b'\n', b'\r\n')` applied to text that already contains CRLF produces `\r\r\n` and
   every comparison fails. Normalise **both** sides to the same form before comparing bytes.
5. **Text-only checking is not enough.** The loss check will happily pass on a file whose titles are
   corrupted by pitfall 1 — grep your own artifacts after writing.
6. **Verify against the backup, not against memory.** The line-set check is only meaningful if the
   "before" file is the untouched original.
7. **Do not let the loss check tempt you into a text summary.** If a section is too big to keep, it
   *moves*; if a sentence is worth keeping it must exist verbatim in one of the files. Summarise
   only in the 1–3 line router entry, where the wording is explicitly yours and the detail lives in
   the linked file.

## Verification snippet (self-contained)

```python
import glob, os
orig   = open(orig_bak, 'rb').read()
lines  = orig.split(b'\n')
pool   = set()
for p in glob.glob(os.path.join(skill_dir, 'references', '*.md')) + [os.path.join(skill_dir, 'SKILL.md')]:
    for ln in open(p, 'rb').read().split(b'\n'):
        if ln.strip(): pool.add(ln.rstrip(b'\r'))
missing       = [l for l in lines if l.strip() and l.rstrip(b'\r') not in pool]
missing_heads = [l for l in lines if l.startswith(b'## ') and l.rstrip(b'\r') not in pool]
print("lines lost:", len(missing), "| ## headings lost:", len(missing_heads))
```

## Reporting template

```
SKILL.md: <before> → <after> bytes   (<after> < 50000 ✓)
new reference files:
   references/<a>.md   <bytes>
   references/<b>.md   <bytes>
verification: 0 of <N> original non-empty lines lost; all <K> original '## ' headings present;
              each moved block byte-identical to its original slice; skill_view loads.
```
