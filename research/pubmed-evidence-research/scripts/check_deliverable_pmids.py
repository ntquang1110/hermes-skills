#!/usr/bin/env python3
"""Check that every pmid in a deliverable JSON was actually efetched this session.

Catches title-only citations (esummary triage is NOT verification) before a
deliverable ships. Usage:

    python check_deliverable_pmids.py --deliverable data/group2_infection.json \
        --verified verified_pmids.txt

--verified accepts a file with one PMID per line (or comma/space separated),
or a comma-separated inline string. Exit code 1 + report if any pmid in the
deliverable is missing from the verified set; 0 if all pass.
"""
import argparse
import json
import re
import sys


def collect_pmids(obj, acc):
    """Recursively collect every value under a 'pmid' key."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == "pmid" and isinstance(v, str) and v.strip():
                acc.add(v.strip())
            else:
                collect_pmids(v, acc)
    elif isinstance(obj, list):
        for item in obj:
            collect_pmids(item, acc)
    return acc


def parse_verified(raw):
    ids = set()
    for chunk in re.split(r"[\s,;]+", raw):
        chunk = chunk.strip()
        if chunk.isdigit():
            ids.add(chunk)
    return ids


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--deliverable", required=True, help="Output JSON to audit")
    ap.add_argument("--verified", required=True,
                    help="File (or inline comma list) of PMIDs efetched this session")
    args = ap.parse_args()

    with open(args.deliverable, encoding="utf-8") as f:
        data = json.load(f)

    if os.path.exists(args.verified):
        with open(args.verified, encoding="utf-8") as f:
            verified = parse_verified(f.read())
    else:
        verified = parse_verified(args.verified)

    deliverable_pmids = collect_pmids(data, set())
    missing = sorted(deliverable_pmids - verified, key=int)

    print(f"Deliverable PMIDs: {len(deliverable_pmids)} | Verified (efetched): {len(verified)}")
    if missing:
        print("UNVERIFIED PMIDs (title-only or invented?):")
        for pid in missing:
            print(f"  - {pid}")
        print("Fix: efetch each before shipping, or drop the fact.")
        sys.exit(1)
    print("OK: every PMID in the deliverable was efetched.")
    sys.exit(0)


if __name__ == "__main__":
    import os  # noqa: E402 (kept local for clarity)
    main()
