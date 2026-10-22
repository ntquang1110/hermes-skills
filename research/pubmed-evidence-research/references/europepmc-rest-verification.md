# Europe PMC REST — one-call search + abstract verification

Use when a deliverable needs many PMIDs verified by reading **real abstracts**, or when
you want search + verification in a single HTTP call. Europe PMC is a drop-in second
source alongside PubMed E-utilities; it needs **no API key** and observed no rate-limit
failures (contrast: NCBI unauthenticated E-utilities is 3 req/s → 429s).

Endpoint:

```
https://www.ebi.ac.uk/europepmc/webservices/rest/search
  ?query=<url-encoded>&format=json&pageSize=10&resultType=<lite|core>[&sort=CITED desc]
```

## Why it beats the esearch→esummary→efetch chain for verification

`resultType=core` returns, in ONE response: `pmid`, `doi`, `pmcid`, `pubYear`,
`journalInfo.journal.title`, `title`, `authorString`, and **`abstractText`**. That
collapses the 3-call PubMed chain into 1 call, which is the whole game when you must
read ~100 abstracts in a session.

| Need | Call |
|---|---|
| Triage many hits (titles only, small payload) | `resultType=lite`, `pageSize=8..15` |
| Verify ONE pmid against its real abstract | `resultType=core`, query `EXT_ID:<pmid>`, `pageSize=1` |
| Exact-lookup several PMIDs at once | `EXT_ID:a OR EXT_ID:b OR ...`, `pageSize=<n>` |
| **Validate an ENTIRE deliverable's reference list** | `EXT_ID:` batch, **40 ids per call**, `resultType=lite`, `pageSize=100` |

### Batch-validate the whole deliverable before shipping (verified 18/10/2026)

`EXT_ID:a OR EXT_ID:b …` accepts a large batch, so the final gate on any deliverable is a
handful of calls, not one per PMID. **101 PMIDs validated in 3 calls.** Run
`scripts/validate_pmids_batch.py <file.md>` — it harvests candidates itself and exits 1 on
any unresolved id.

**The false-negative trap that makes this script necessary.** The obvious check is
`grep -oE 'PMID[ :]*[0-9]{7,8}'`, but that only matches PMIDs written with a literal
`PMID:` prefix. Deliverables that put PMIDs in a **markdown table column**
(`| ... | 41513748, 42218208 |`) have no prefix, so the grep found only **40 of 101**
PMIDs in one real file — and reported success. A fabricated PMID sitting in a table cell
would have shipped undetected. Harvest the widest set instead:

```python
PMID_RE = re.compile(r"\b(?:1[0-9]{7}|[2-4][0-9]{7})\b")   # any 7-8 digit number
```

The leading-digit anchor keeps years (`2026`), byte counts (`90854`) and doses out while
still catching every real PMID. Validate the superset, then report the count sent vs
resolved per batch so a silently-empty batch is visible.

Parse with `strict=False` only for `resultType=core` (control chars live in
`abstractText`); `lite` payloads are safe with a plain `json.loads`.

## Query cookbook (the parameters that matter)

- **Field-scope to kill noise.** Unscoped terms give huge `hitCount` and return
  recent-but-irrelevant records. Use `TITLE_ABS:"phrase"` for title+abstract,
  `TITLE:"..."` for title only. Example that worked:
  `TITLE_ABS:(pig OR porcine OR swine) AND TITLE_ABS:gyrencephalic AND TITLE_ABS:(human OR compar*)`
- **Sort by impact to surface the canonical reviews.** Default relevance drifts to
  whatever is newest; `&sort=CITED%20desc` surfaces the 2007/2019 landmark papers that
  are the real evidence base. `&sort=P_PDATE_D%20desc` for recency.
- **Publication type / year filters** (find review-type sources 2018-2026):
  `PUB_TYPE:"Review"`, `PUB_YEAR:2018 OR PUB_YEAR:2019 OR ...` (no ranges — OR them).
- `hitCount` in the response tells you if the query is too broad before you parse results.

## The two traps that actually bite

### 1. `resultType=core` payloads trigger the truncation/parse failure
10 core results ≈ 20 KB+ of JSON. Capturing that through `terminal()`/`execute_code`
stdout truncates, and the truncated text fails `json.loads` with
`Expecting ':' delimiter` at a suspiciously round offset (~char 20000). This is
**truncation**, not a content bug. Fix: `curl -s "<url>" -o file.json` then parse the file.

### 2. Contrast with the *other* JSONDecodeError — control characters in abstracts
`json.loads` on a **complete, untruncated** Europe PMC response can still fail with
`Invalid control character at: line 1 column ...`. Cause: raw control characters inside
`abstractText` (some abstracts carry them via the `<h4>` section markup Europe PMC
returns). Fix: **`json.loads(s, strict=False)`**. Apply it to every Europe PMC parse.

> Do not let the existing skill note "JSONDecodeError on esummary → almost always
> truncation" mislead you here. Two distinct root causes; symptom look similar.
> Diagnostic: if the error offset is at/near ~20000 and the string ends mid-token →
> truncation (save to file). If the JSON looks complete but errors early with
> `Invalid control character` → `strict=False`.

## Working helper pattern (write-to-file + strict=False + one PMID per call)

```python
from hermes_tools import terminal
import json, urllib.parse, os

TMP = "<workspace>/epmc_tmp"; os.makedirs(TMP, exist_ok=True)

def abstract_of(pmid, abslen=1500):
    """Verify ONE pmid by reading its real abstract. Write-to-file avoids truncation."""
    f = f"{TMP}/{pmid}.json"
    q = urllib.parse.quote(f"EXT_ID:{pmid}")
    terminal(command=(f'curl -s "https://www.ebi.ac.uk/europepmc/webservices/rest/search'
                      f'?query={q}&format=json&pageSize=1&resultType=core" -o "{f}"'))
    d = json.load(open(f, encoding="utf-8"), strict=False)   # strict=False is required
    res = d.get("resultList", {}).get("result", [])
    if not res:
        print(f"PMID {pmid}: NO RESULT"); return
    x = res[0]
    print(x.get("pmid"), x.get("doi"), x.get("pubYear"),
          x.get("journalInfo", {}).get("journal", {}).get("title", ""))
    print("TITLE:", x.get("title"))
    print("ABS:", (x.get("abstractText") or "NO ABSTRACT").replace("\n", " ")[:abslen])

# Triage (titles only, cheap) — loop queries in ONE execute_code run
def triage(query, n=8, sort="CITED desc"):
    q = urllib.parse.quote(query); s = urllib.parse.quote(sort)
    cmd = (f'curl -s "https://www.ebi.ac.uk/europepmc/webservices/rest/search'
           f'?query={q}&format=json&pageSize={n}&resultType=lite&sort={s}"')
    d = json.loads(terminal(command=cmd)["output"], strict=False)
    for x in d.get("resultList", {}).get("result", []):
        print(f"PMID:{x.get('pmid','-')} DOI:{x.get('doi','-')} {x.get('pubYear','-')} "
              f"[{x.get('journalTitle','')[:24]}] {x.get('title','')[:165]}")
```

Batch `abstract_of` in a loop inside one `execute_code` call to verify 10-20 PMIDs fast.
Delete the temp dir at the end.

## Record-integrity notes

- **`NO ABSTRACT` is a real outcome.** Some records (conference abstracts, editorials)
  return no `abstractText`. Verify title/journal/DOI and **flag in the deliverable** that
  only metadata was confirmed — never imply full abstract verification. (Observed:
  PMID 40653083, *Brain Stimul* 2025 — title/DOI confirmed, abstract absent.)
- **Preprints appear in Europe PMC with `pmid` missing and a DOI like `10.1101/...` or
  `10.64898/...`.** They are NOT peer-reviewed. Cite the DOI, and mark them explicitly as
  preprints in the deliverable (keep a separate list). Never let a preprint count as
  peer-reviewed evidence for a load-bearing claim.
- **`source` field** distinguishes `MED` (PubMed-indexed) from preprint servers — a quick
  machine-readable indicator, though the missing `pmid` is the simpler tell.
- Both `pmid` and `doi` come back together, so Europe PMC is also the cheapest way to
  grab DOIs without a separate esummary pass.

## Related
- Cross-check any Europe PMC finding against PubMed E-utilities (SKILL.md Workflow) when
  a claim is load-bearing — two independent indexes agreeing is real corroboration.
- `scripts/validate_pmids_batch.py` — the shippable gate: harvests every PMID-like number
  in a deliverable (including bare table-cell ids) and batch-validates it. Exit 1 = do not ship.
- `scripts/check_deliverable_pmids.py` still governs the JSON-deliverable gate: every PMID in
  the deliverable must be one you actually read this session.
- `scripts/verify_pmids.py` — the slow path (1 call/PMID) that prints the **real title** so you
  can eyeball it against the claim; use it when you also need title-vs-claim checking, which
  the batch script does not do.
- `references/invivo-biosensor-resolution-layers.md` — bank built with this method (101 PMIDs,
  in-vivo biosensor resolution ladder for the fixgby project).
