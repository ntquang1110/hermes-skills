#!/usr/bin/env python3
"""Audit PubMed/Europe PMC citations and quoted numbers before shipping a deliverable.

Why: tasks like "every PMID must verify; every figure must sit inside the cited
abstract; a fabricated PMID kills the batch" are impossible to satisfy by eyeballing.
This script does it mechanically.

Usage
-----
1) Existence check (hitCount == 1 and pmid matches):

    python verify_pmid_claims.py --pmids 34237915 40980502 42462087

2) Per-claim audit — every numeric token in `text` must appear in that PMID's
   abstractText (HTML stripped):

    python verify_pmid_claims.py --claims claims.json --strict

   claims.json:
   {
     "spelled": {"96": "ninety-six", "72": "seventy-two"},
     "claims": [
       {"label": "calcium-butyrate / 34237915",
        "pmid": "34237915",
        "text": "Seventy-two piglets weaned at 28 d, 0.15% pre-starter, 0.075% starter"}
     ]
   }

3) Entry-level audit — a claim pool is allowed to draw on ANY of the entry's PMIDs:

   {"spelled": {...},
    "entries": [{"id": "mcfamonoglyceride-c8c10",
                 "pmids": ["40133511", "42520476"],
                 "fields": {"hieu_qua": "pH dịch ruột giảm, tế bào hình đài tăng",
                            "co_che": "..."}}]}

Exit code is 0 when everything verifies; 1 when any PMID fails to verify; 2 when
numbers are unverified and --strict was passed.

Reading the output: an UNSUPPORTED number is a signal to FIX THE TEXT (soften or
retitle the claim), not to doubt the paper. Europe PMC truncates some p-values to
"(p" — see references/europepmc-rest-quirks.md.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.parse
import urllib.request

EPMC = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
NUM = re.compile(r"\d+(?:[.,]\d+)?%?")
TAG = re.compile(r"<[^>]+>")
WS = re.compile(r"\s+")


def fetch(pmid: str, cache: dict, sleep: float = 0.15) -> str:
    """Return whitespace-normalised, tag-stripped abstractText. Raises on verify failure."""
    if pmid in cache:
        return cache[pmid]
    url = EPMC + "?" + urllib.parse.urlencode(
        {"query": "EXT_ID:%s" % pmid, "resultType": "core", "format": "json"}
    )
    with urllib.request.urlopen(url, timeout=60) as resp:
        data = json.load(resp)
    if data.get("hitCount") != 1:
        raise LookupError("hitCount != 1 for PMID %s (got %s)" % (pmid, data.get("hitCount")))
    hit = data["resultList"]["result"][0]
    if str(hit.get("pmid")) != str(pmid):
        raise LookupError("pmid mismatch: asked %s, got %s" % (pmid, hit.get("pmid")))
    text = WS.sub(" ", TAG.sub(" ", hit.get("abstractText") or ""))
    cache[pmid] = text
    time.sleep(sleep)
    return text


def tokens(text: str) -> set:
    return {t for t in NUM.findall(text or "")}


def supported(tok: str, abstract: str, spelled: dict) -> bool:
    bare = tok.rstrip("%")
    if bare in abstract:
        return True
    if bare.replace(",", ".") in abstract or bare.replace(".", ",") in abstract:
        return True
    word = spelled.get(bare)
    return bool(word) and word in abstract.lower()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pmids", nargs="*", default=[])
    ap.add_argument("--claims", help="JSON file with 'claims' and/or 'entries'")
    ap.add_argument("--strict", action="store_true", help="fail (exit 2) on unverified numbers")
    args = ap.parse_args()

    cache: dict = {}
    failures, unverified, verified = [], [], 0

    for pmid in args.pmids:
        try:
            fetch(pmid, cache)
            verified += 1
            print("OK    %s" % pmid)
        except Exception as exc:  # noqa: BLE001 - report, never crash the audit
            failures.append((pmid, str(exc)))
            print("FAIL  %s -> %s" % (pmid, exc))

    if args.claims:
        with open(args.claims, encoding="utf-8") as fh:
            payload = json.load(fh)
        spelled = {str(k): str(v).lower() for k, v in (payload.get("spelled") or {}).items()}

        for c in payload.get("claims", []):
            pmid = str(c["pmid"])
            try:
                abstract = fetch(pmid, cache)
                verified += 1
            except Exception as exc:  # noqa: BLE001
                failures.append((pmid, str(exc)))
                print("FAIL  %s (%s) -> %s" % (c.get("label", pmid), pmid, exc))
                continue
            missing = sorted(t for t in tokens(c.get("text", "")) if not supported(t, abstract, spelled))
            if missing:
                unverified.append((c.get("label", pmid), pmid, missing))
                print("NUMS  %-40s %s -> %s" % (c.get("label", ""), pmid, missing))
            else:
                print("OK    %-40s %s (%d tokens)" % (c.get("label", ""), pmid, len(tokens(c.get("text", "")))))

        for e in payload.get("entries", []):
            pmids = [str(p) for p in e.get("pmids", [])]
            pool = ""
            for pmid in pmids:
                try:
                    pool += fetch(pmid, cache) + " "
                    verified += 1
                except Exception as exc:  # noqa: BLE001
                    failures.append((pmid, str(exc)))
                    print("FAIL  %s (%s) -> %s" % (e.get("id", "?"), pmid, exc))
            for field, text in (e.get("fields") or {}).items():
                missing = sorted(t for t in tokens(text) if not supported(t, pool, spelled))
                if missing:
                    unverified.append(("%s.%s" % (e.get("id", "?"), field), ",".join(pmids), missing))
                    print("NUMS  %-40s %s -> %s" % ("%s.%s" % (e.get("id", "?"), field), pmids, missing))
                else:
                    print("OK    %-40s %s" % ("%s.%s" % (e.get("id", "?"), field), pmids))

    print("\nverified calls=%d | verify failures=%d | unverified-number groups=%d"
          % (verified, len(failures), len(unverified)))
    if failures:
        return 1
    if unverified and args.strict:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
