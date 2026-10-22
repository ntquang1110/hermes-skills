# Verifying Delegated Research Output — runnable recipes

Session-specific detail backing the "Extension: Verifying Delegated Research
Output" section of `design-critique`. Use when a subagent batch (or any external
worker) hands back a research artifact and its summary.

Pitfall this exists to prevent: **trusting the child's self-report.** A summary
claiming "102 PMIDs verified by reading abstracts, file written, 145 KB" is a
statement about the child's intent, not evidence about the world.

---

## 1. Artifact stat check

```python
import os
for p in [r"D:\proj\docs\03a-findings.md", r"D:\proj\docs\04-analysis.md"]:
    print(f"{'OK ' if os.path.exists(p) else 'MISSING'} "
          f"{os.path.getsize(p) if os.path.exists(p) else 0:>9,} bytes  {os.path.basename(p)}")
```

`os.path.getsize` returns **bytes**. Vietnamese text in UTF-8 runs ~1.12 bytes
per char, so 83,916 bytes ≈ 75,031 chars. Both figures are "correct" — don't
raise a false alarm by comparing a byte count to a char count.

---

## 2. PMID spot-check via Europe PMC (no API key)

```python
import json, time, urllib.parse, urllib.request

def resolve_pmid(pmid: str) -> dict | None:
    q = urllib.parse.quote(f"EXT_ID:{pmid} AND SRC:MED")
    url = ("https://www.ebi.ac.uk/europepmc/webservices/rest/search"
           f"?query={q}&format=json&resultType=core&pageSize=1")
    with urllib.request.urlopen(url, timeout=25) as r:
        d = json.load(r)
    res = d.get("resultList", {}).get("result", [])
    return res[0] if res else None

for pmid in ["39912370", "39340562", "31379533"]:
    rr = resolve_pmid(pmid)
    if rr:
        j = rr.get("journalInfo", {}).get("journal", {}).get("title", "?")
        print(f"OK  {pmid} | {j} {rr.get('pubYear')} | {rr.get('title','')[:90]}")
    else:
        print(f"BAD {pmid} -> NOT FOUND on Europe PMC")
    time.sleep(0.35)          # be polite to the API
```

Read the printed **title** and compare it to the claim the artifact attaches to
that PMID. Existence alone is not enough — a real PMID attached to an unrelated
claim is the classic mis-attribution failure.

Limits worth knowing:
- `SRC:MED` restricts to MEDLINE/PubMed; `EXT_ID` also resolves preprints and
  Agricola records, so a miss under `SRC:MED` may still be a real (non-PubMed)
  record — re-query without the source filter before declaring it fabricated.
- Very high PMIDs (e.g. 42xxxxxx) are plausible for 2026-era records; do not
  dismiss an identifier as "too high to exist" — resolve it.

---

## 3. Superseding-document hunt (the high-value check)

Citation verification answers "does this document exist and say that?". It does
**not** answer "is that still the rule today?". For any legal/regulatory/
standards claim, run a second search for the amending instruments.

Query patterns that surface Vietnamese amending documents:

| Pattern | Finds |
|---|---|
| `<số hiệu>` + `sửa đổi bổ sung` | amending decrees/circulars |
| `<số hiệu>` + `bãi bỏ` / `thay thế` | repeals and replacements |
| `<số hiệu>` + `dừng thực hiện thủ tục hành chính` | procedures cancelled by resolution |
| `<số hiệu>` + `VBHN` | consolidated ("văn bản hợp nhất") text |
| `<số hiệu>` + `nội dung hợp nhất` | luatvietnam consolidated view |

Prefer, in order: (1) the issuing body's own site (e.g. `cucthuy.gov.vn`,
`vanban.chinhphu.vn`, `congbao.chinhphu.vn`), (2) the consolidated text on a
legal database, (3) news summaries — **summaries are the weakest**, they cover
only the headline provisions and routinely omit articles that matter.

### Case study — claim true when written, false when read

- Artifact asserted, tagged `[F]` and labelled "cực kỳ quan trọng": supplementary
  feed products (TĂBS) must be **appraised by the provincial People's Committee
  chairman** before publication — citing `NĐ 32/2026/NĐ-CP` (21/01/2026).
- Confirm step: the decree **does** say exactly that (Điều 8b, added to
  `NĐ 13/2020/NĐ-CP`), 5-15 working days. Citation was accurate.
- Supersede step: `NQ 66.19/2026/NQ-CP` (**18/5/2026**) **stopped all four
  administrative procedures** for publishing / re-publishing / changing
  information on supplementary feed, domestic and imported, from 18/5/2026 —
  moving the whole category to **self-declaration** on the Ministry portal.
- Consequence: the artifact's operational conclusion inverted. "Expect 2-4
  months of provincial appraisal" became "barrier went down; file
  self-declaration documents with the department". A downstream action item and
  a risk-register row were both wrong.
- Confirming source: the department's own notice (`cucthuy.gov.vn`) plus its
  implementing circular letter; the primary decree text from `congbao.chinhphu.vn`
  was correct but superseded.

Lesson: **"the document says X" and "X is the rule" are two separate checks.**
Run both for anything tagged as hard fact in a regulated domain.

---

## 4. In-place correction sweep

After finding a wrong claim, count how many places it appears before declaring
the artifact fixed:

```python
import re
t = open(path, encoding="utf-8").read()
lines = t.split("\n")
MARK = ("DỪNG", "ĐÃ SỬA", "ĐÃ SAI", "ĐÍNH CHÍNH", "NQ 66.19")   # your correction markers
bad = [(i, l.strip()[:160]) for i, l in enumerate(lines, 1)
       if "<keyword>" in l and not any(m in l for m in MARK)]
print(f"{len(bad)} unmarked occurrences remain")
for i, l in bad:
    print(f"  {i}: {l}")
```

Expect hits inside the correction banner itself (it quotes the old claim) —
those are fine. The real find is a **method/procedure line or an appendix
lookup row** that the banner does not cover; in this session that was a
validation-plan method line still telling the reader to run the cancelled
procedure.

Finish with: banner added, inline markers placed, references extended, sweep
clean, correction committed separately from the original dump.
