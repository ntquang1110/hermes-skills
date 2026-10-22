# Independent loss verification (when you already overwrote the original)

Worked example + recipes from the `ai-company-ops` split (2026-10-19):
**SKILL.md 112,959 → 38,521 bytes**, 17 sections moved, 12 new refs (+84,556 bytes),
refs dir 42 → 54 files, 736 → 333 lines, 42/42 `## ` headings kept.

The split itself was trivial. The hard part was *proving* nothing was lost — because the
new SKILL.md had already been written with no snapshot of the original, in a directory
with **no git and no `.bak`**. What follows is the recovery path, then the check that
closes the loop.

## 1. Recover the pre-edit bytes from Hermes observation logs

Hermes persists raw tool output under `~/.hermes/observations/<handle>.json`. If you
ever printed the original file (headings, chunked dumps, `wc -c`), the bytes are there.

- Schema: `{"handle", "tool", "tool_use_id", "excerpt", "total_chars", "total_lines",
  "content", "stored_at", "last_recalled"}`
- `content` is a JSON *string* holding the tool's output envelope → parse twice:
  `json.loads(j["content"])["output"]`.
- If the printer used `print(f"{i} | {line}")` after `raw.split("\n")` on a CRLF file,
  every recovered line keeps a trailing `\r`. Strip it.
- Lines are otherwise faithful: a spot-check of range 113-166 matched the verbatim ref
  slice 54/54 lines, byte for byte.

```python
import json, os, re
d = os.path.expanduser("~/.hermes/observations")
orig = {}
for fn in os.listdir(d):
    try:
        j = json.load(open(os.path.join(d, fn), encoding="utf-8"))
        out = json.loads(j["content"])["output"]
    except Exception:
        continue                      # many observation files are unrelated
    for raw in out.split("\n"):
        m = re.match(r"^(\d+) \| ?(.*)$", raw)
        if m:
            orig[int(m.group(1))] = m.group(2)
O = [(orig[i][:-1] if orig[i].endswith("\r") else orig[i])
     for i in range(1, max(orig) + 1)]

# the pre-edit file, byte-exact (join = 112,957 + trailing CRLF = 112,959)
open("bak/SKILL.md.orig", "w", encoding="utf-8", newline="").write(
    "\r\n".join(O) + "\r\n")
```

Sanity gates on the recovery: no missing line numbers (`max(orig)` == line count),
heading census matches what you measured before the edit, and the byte total matches the
size the user quoted. All three held here (112,957 + 2 = 112,959).

**Only then** can V1 (per-range verbatim) and V2 (reconstruction equality) be claimed
honestly. Recovered 112,959 + 84,556 moved − 8,400 router text = 36,803 = the file the
split script reported — independent arithmetic agreement, not a hopeful reading.

## 2. V4 — enumerate the delta once you have edited the new file

Post-split edits (an index block, one repointed sentence) make exact equality
impossible on purpose. Don't weaken the check; enumerate it.

```python
import difflib
# moved = set of original line numbers inside moved ranges
nm = [O[i - 1] for i in range(1, len(O) + 1) if i not in moved]
for line in difflib.unified_diff(nm, current_minus_router_blocks_minus_added_block,
                                 lineterm="", n=0):
    print(line[:160])
```

Accepted diff from the real run — three hunks, all intentional:

1. `@@ -30,0 +31,14 @@` — the 14-line `**Reference files chi tiết …**` index I added.
2. `@@ -105 +119 @@` — one pointer reworded from `… ở mục "Context Scan …" bên dưới + …`
   to `… ở references/context-scan-build-2026-09.md + …`, because that section had become
   a ref file (pitfall 14 in SKILL.md).
3. `@@ -247,0 +262 @@` — one added blank line.

Any other hunk = real loss. This is the strongest available evidence and it is cheap.

## 3. Byte-closure arithmetic (report this to the user)

```
original 112,959
 − moved out   84,556
 + router text  8,400
 + added index  1,718
 = new SKILL.md 38,521   ✓ matches measured size
```

If the four numbers don't close exactly, one of the three verification claims is wrong —
do not report success on a near-miss.

## 4. What to report

- `wc -c` before → after, plus line count and heading count (`42/42`).
- Table of new ref files with byte sizes.
- The one-line V1/V2/V3/V4 result, and the accepted-diff summary (count of hunks + why
  each is intentional).
- Location of the snapshot (`bak/SKILL.md.orig`) so the user can roll back.
- Explicitly flag any judgment call you made, e.g. "I moved the *Inbox files PHẢI
  tracked* pitfall into a ref and kept only its headline inline — say the word if you
  want it back inline."
