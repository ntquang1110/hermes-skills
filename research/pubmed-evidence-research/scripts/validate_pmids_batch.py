#!/usr/bin/env python3
"""Batch-validate EVERY PMID-like number in a deliverable against Europe PMC.

Why this exists (separate from verify_pmids.py): verify_pmids.py queries
Europe PMC ONE pmid at a time and only picks up explicit `PMID: <n>` / `pmid`
field tokens. Two failure modes it does not cover:

  (a) SPEED. A 100-PMID deliverable = 100 calls. Europe PMC accepts
      `EXT_ID:a OR EXT_ID:b ...` batches, so the same check is ~3 calls.
      Verified 18/10/2026: 101 PMIDs validated in 3 batched calls.

  (b) MISSED PMIDs IN TABLES. When a deliverable puts PMIDs in a markdown
      table column (very common: `| ... | 41513748, 42218208 |`), there is no
      `PMID:` prefix to match. A prefix-based grep silently validated only
      40 of the 101 PMIDs in one file and would have reported "all verified".
      This script scans the WIDEST set -- every bare 7-8 digit number that
      could be a PMID -- so a fabricated number cannot hide in a table cell.

Usage:
    python validate_pmids_batch.py deliverable.md [more files...]
    python validate_pmids_batch.py docs/*.md

Exit 0 = every candidate resolved on Europe PMC.
Exit 1 = at least one number did not resolve -> DO NOT SHIP.
"""

import json
import re
import sys
import urllib.parse
import urllib.request

API = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
BATCH = 40  # EXT_ID terms per call; 40 keeps the payload comfortably small

# PMIDs are 7-8 digits. Anchor the leading digit range so we do not sweep up
# years (2026), byte counts (90854), doses, or accession numbers beyond 8
# digits. Covers 1xxxxxxx (older) and 2-4xxxxxxx (current era).
PMID_RE = re.compile(r"\b(?:1[0-9]{7}|[2-4][0-9]{7})\b")


def harvest(text):
    """All candidate PMID-like numbers, deduped, order preserved."""
    seen, out = set(), []
    for m in PMID_RE.findall(text):
        if m not in seen:
            seen.add(m)
            out.append(m)
    return out


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "hermes-pmid-check/1.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8", "replace")


def resolve(batch):
    """Return (set_of_resolved_ids, raw_result_count)."""
    ids = " OR ".join("EXT_ID:" + p for p in batch)
    url = (
        API
        + "?query="
        + urllib.parse.quote(ids)
        + "&format=json&pageSize=100&resultType=lite"
    )
    try:
        payload = json.loads(fetch(url), strict=False)
    except Exception as exc:  # noqa: BLE001 - report, never silently pass
        print("  ! batch failed (%s): %s" % (type(exc).__name__, exc))
        return set(), 0
    res = (payload.get("resultList") or {}).get("result") or []
    found = set()
    for hit in res:
        ident = hit.get("pmid") or hit.get("id")
        if ident:
            found.add(str(ident))
    return found, len(res)


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2

    overall_missing = 0
    for path in argv[1:]:
        try:
            with open(path, encoding="utf-8") as fh:
                text = fh.read()
        except OSError as exc:
            print("SKIP %s (%s)" % (path, exc))
            continue

        cands = harvest(text)
        print("\n%s\n  candidates: %d" % (path, len(cands)))
        if not cands:
            continue

        resolved = set()
        for i in range(0, len(cands), BATCH):
            chunk = cands[i : i + BATCH]
            found, n = resolve(chunk)
            resolved |= found
            print(
                "  batch %2d: sent %2d, resolved %2d"
                % (i // BATCH + 1, len(chunk), len(found))
            )

        missing = [c for c in cands if c not in resolved]
        if missing:
            overall_missing += len(missing)
            print("  FAIL - %d number(s) NOT on Europe PMC:" % len(missing))
            for m in missing:
                print("      %s" % m)
        else:
            print("  OK - all %d resolved" % len(cands))

    print("\n%s" % ("=" * 60))
    if overall_missing:
        print("RESULT: FAIL (%d unresolved) - do not ship" % overall_missing)
        return 1
    print("RESULT: PASS - every PMID-like number in the deliverable is real")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
