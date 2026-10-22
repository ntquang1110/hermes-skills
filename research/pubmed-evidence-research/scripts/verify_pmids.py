#!/usr/bin/env python3
"""Batch-verify PMIDs in a deliverable against Europe PMC.

WHY: a PMID that "looks right" is not a verified citation. This is the tool to
run on research you RECEIVED (subagent / sibling session / pasted report)
before you relay it, and on your own deliverable before you ship it. It prints
the REAL title for each PMID so you can eyeball it against the claim the PMID is
supposedly supporting -- title/claim mismatch is the failure mode it catches.

USAGE
    python verify_pmids.py deliverable.md
    python verify_pmids.py a.md b.json other.txt --json report.json
    python verify_pmids.py dir/ --pattern "*.md"

EXIT CODE
    0 = every PMID found in Europe PMC and has a non-empty title
    1 = at least one PMID missing, or title empty (suspicious/extinct record)
    2 = no PMIDs found at all (probably the wrong file, or citations are DOIs)

NOTES
    * Uses Europe PMC REST (no API key, no observed rate limiting), 1 request
      per PMID with a small sleep. `resultType=lite` keeps the payload small --
      `core` would pull full abstracts and blow up stdout on big files.
    * `json.loads(..., strict=False)` because abstracts (core) and some titles
      carry raw control characters.
    * DOI-only citations (preprints: 10.1101/... , 10.64898/...) are listed
      separately and are NOT treated as failures -- but they must be flagged as
      not-peer-reviewed in the deliverable.
    * This verifies EXISTENCE + TITLE ONLY. It does not confirm the paper says
      what the claim says -- read the abstract for load-bearing claims.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
import time
import urllib.parse
import urllib.request

EPMC = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
UA = "Mozilla/5.0 (compatible; hermes-pmid-verifier/1.0)"

PMID_RE = re.compile(r"\bPMID[:\s]*(\d{6,9})\b", re.I)
BARE_PMID_RE = re.compile(r'"pmid"\s*:\s*"(\d{6,9})"', re.I)
DOI_RE = re.compile(r"\b(10\.\d{4,9}/[^\s\])>,;\"]+)")


def collect_pmids(paths: list[pathlib.Path]) -> tuple[dict[str, set[str]], dict[str, set[str]]]:
    """Return ({pmid: {files}}, {doi: {files}})."""
    pmids: dict[str, set[str]] = {}
    dois: dict[str, set[str]] = {}
    for p in paths:
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except Exception as exc:  # noqa: BLE001
            print(f"  !! cannot read {p}: {exc}", file=sys.stderr)
            continue
        for rx in (PMID_RE, BARE_PMID_RE):
            for m in rx.finditer(text):
                pmids.setdefault(m.group(1), set()).add(p.name)
        for m in DOI_RE.finditer(text):
            dois.setdefault(m.group(1).rstrip(".,;"), set()).add(p.name)
    return pmids, dois


def lookup(pmid: str, attempts: int = 3) -> dict:
    q = urllib.parse.urlencode(
        {"query": f"EXT_ID:{pmid}", "format": "json", "pageSize": 1, "resultType": "lite"}
    )
    last = ""
    for i in range(attempts):
        try:
            req = urllib.request.Request(f"{EPMC}?{q}", headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=25) as r:
                data = json.loads(r.read().decode("utf-8", "replace"), strict=False)
            hits = (data.get("resultList") or {}).get("result") or []
            return hits[0] if hits else {}
        except Exception as exc:  # noqa: BLE001
            last = str(exc)
            time.sleep(2 * (i + 1))
    return {"_error": last}


def expand_inputs(raw: list[str], pattern: str) -> list[pathlib.Path]:
    out: list[pathlib.Path] = []
    for item in raw:
        p = pathlib.Path(item).expanduser()
        if p.is_dir():
            out.extend(sorted(q for q in p.glob(pattern) if q.is_file()))
        elif p.is_file():
            out.append(p)
        else:
            print(f"  !! not found, skipped: {p}", file=sys.stderr)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="Verify PMIDs against Europe PMC.")
    ap.add_argument("paths", nargs="+", help="files or directories to scan")
    ap.add_argument("--pattern", default="*.md", help="glob when a directory is given (default: *.md)")
    ap.add_argument("--json", dest="json_out", help="write the full report here")
    ap.add_argument("--sleep", type=float, default=0.4, help="seconds between lookups")
    args = ap.parse_args()

    files = expand_inputs(args.paths, args.pattern)
    if not files:
        print("No readable input files.", file=sys.stderr)
        return 2

    pmids, dois = collect_pmids(files)
    if not pmids:
        print(f"Scanned {len(files)} file(s): found 0 PMIDs.")
        if dois:
            print(f"  (found {len(dois)} DOI(s) instead -- check DOIs separately)")
        return 2

    print(f"Scanned {len(files)} file(s) -> {len(pmids)} unique PMID(s), {len(dois)} unique DOI(s)\n")

    ok, bad, report = [], [], {}
    for n, pmid in enumerate(sorted(pmids), 1):
        rec = lookup(pmid)
        title = (rec.get("title") or "").strip()
        journal = (rec.get("journalTitle") or rec.get("journalInfo", {}).get("journal", {}).get("title") or "").strip()
        year = str(rec.get("pubYear") or "").strip()
        err = rec.get("_error")
        entry = {
            "pmid": pmid,
            "found": bool(rec) and not err,
            "title": title,
            "journal": journal,
            "year": year,
            "files": sorted(pmids[pmid]),
            "error": err or "",
        }
        report[pmid] = entry
        if entry["found"] and title:
            ok.append(pmid)
            print(f"  [{n}/{len(pmids)}] OK   {pmid}  {year:4s} {journal[:38]:38s} {title[:80]}")
        else:
            bad.append(pmid)
            why = err or ("title empty" if entry["found"] else "NOT FOUND in Europe PMC")
            print(f"  [{n}/{len(pmids)}] FAIL {pmid}  <-- {why}")
        time.sleep(args.sleep)

    print(f"\n{len(ok)}/{len(pmids)} verified, {len(bad)} suspect")
    if bad:
        print("Suspect PMIDs: " + ", ".join(bad))
        print("-> Do NOT ship these. Either they are fabricated/mistyped, or the")
        print("   record is a citation-only/editorial entry. Re-resolve by title")
        print("   search, or drop the citation and say why in the deliverable.")
    if dois:
        print(f"\n{len(dois)} DOI(s) seen (verify separately; preprints 10.1101/* must be")
        print("flagged as not peer-reviewed):")
        for d in sorted(dois)[:20]:
            print(f"   {d}")
        if len(dois) > 20:
            print(f"   ... +{len(dois) - 20} more")

    if args.json_out:
        pathlib.Path(args.json_out).write_text(
            json.dumps({"report": report, "ok": ok, "suspect": bad, "dois": sorted(dois)},
                       ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(f"\nReport written: {args.json_out}")

    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
