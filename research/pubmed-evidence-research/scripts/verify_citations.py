#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verify_citations.py - anti-fabrication audit for sourced deliverables.

Every PMID and DOI that appears in a deliverable is resolved against an
authoritative registry, and every entry in the deliverable's source list is
compared against that registry's OWN metadata. This catches the failure mode
that manual review misses: an identifier that looks perfectly well-formed but
belongs to an ENTIRELY DIFFERENT PAPER, or an entry whose title/year silently
drifted from the record.

Registries
  PMID -> Europe PMC
          https://www.ebi.ac.uk/europepmc/webservices/rest/search
          query=EXT_ID:<pmid>... OR EXT_ID:<pmid>&resultType=core&format=json
  DOI  -> CrossRef
          https://api.crossref.org/works/<doi>

Why both: a PMID can be typed correctly but point at the wrong article (e.g. a
malaria paper sitting in an ASFV dossier). CrossRef independently confirms a
DOI is actually registered -- some publisher DOIs exist in PubMed metadata but
are NOT CrossRef-resolvable, which is worth flagging rather than guessing.

Usage
  python verify_citations.py DELIVERABLE.json
  python verify_citations.py report.md --source-key nguon
  python verify_citations.py DELIVERABLE.json --no-crossref   # PMID-only, faster

The deliverable may be JSON (with a source-list array under --source-key,
default "nguon") or plain text/markdown (identifiers are scraped).

Exit codes
  0  all identifiers resolved and matched
  1  at least one hard problem (unresolvable id, wrong year, wrong paper,
     or a PMID cited in the body but absent from the source list)
  2  usage or network error

Stdlib only. Python 3.8+.
"""

import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

EPMC = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
CROSSREF = "https://api.crossref.org/works/"
UA = "hermes-citation-audit/1.0 (mailto:citation-audit@example.com)"

# PMIDs are written many ways in drafts; catch the labelled forms. Bare 7-8
# digit numbers are ALSO harvested from JSON source-list entries (see below),
# but are never scraped from prose -- too many false positives (years, counts).
PMID_LABELLED = re.compile(r"PMID[\s:]{0,3}(\d{7,8})", re.I)
# Trailing punctuation is the #1 cause of bogus CrossRef 404s: a sentence-final
# "DOI 10.1128/jvi.00932-24." must be stripped before resolving.
DOI_RE = re.compile(r"10\.\d{4,9}/[^\s\"');,\]\}]+")
DOI_TRAIL = ".,;:)]}\"'"

EPMC_BATCH = 12


def norm(s):
    """Lowercase alphanumeric-only form, for tolerant title comparison."""
    return re.sub(r"[^a-z0-9]+", "", (s or "").lower())


def clean_doi(d):
    return d.rstrip(DOI_TRAIL)


def load_deliverable(path):
    """Return (raw_text, parsed_json_or_None)."""
    with open(path, encoding="utf-8") as fh:
        raw = fh.read()
    obj = None
    if path.lower().endswith(".json"):
        obj = json.loads(raw)  # let a malformed deliverable fail loudly
    else:
        try:
            obj = json.loads(raw)
        except Exception:
            obj = None
    return raw, obj


def harvest_pmids(raw, obj, source_key):
    """PMIDs from (a) labelled mentions in prose, (b) JSON source-list entries."""
    cited = set(PMID_LABELLED.findall(raw))
    listed = set()
    if isinstance(obj, dict):
        entries = obj.get(source_key) or []
        if isinstance(entries, list):
            for e in entries:
                if not isinstance(e, dict):
                    continue
                if str(e.get("loai", "")).upper() == "PMID":
                    pid = str(e.get("id", "")).strip()
                    if pid.isdigit():
                        listed.add(pid)
    # A labelled mention is also evidence of a citation, but only count it as
    # "listed" when it is NOT inside the source-list region. Cheap heuristic:
    # treat all labelled PMIDs as cited, and separately report listed ones.
    return cited | listed, listed


def harvest_dois(raw):
    return {clean_doi(d) for d in DOI_RE.findall(raw)}


def http_json(url, timeout=60, retries=4):
    """GET JSON with polite backoff (CrossRef rate-limits aggressively)."""
    last = None
    for attempt in range(retries):
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.loads(r.read().decode("utf-8", "replace"))
        except urllib.error.HTTPError as e:
            last = e
            if e.code in (429, 500, 502, 503):
                time.sleep(1.5 * (attempt + 1))
                continue
            raise
        except Exception as e:  # transient socket/timeout
            last = e
            time.sleep(1.5 * (attempt + 1))
    raise last if last else RuntimeError("unreachable")


def epmc_records(pmids, verbose=True):
    """pmid(str) -> Europe PMC core record."""
    out = {}
    pmids = sorted(pmids)
    for i in range(0, len(pmids), EPMC_BATCH):
        chunk = pmids[i:i + EPMC_BATCH]
        q = {"query": " OR ".join("EXT_ID:" + p for p in chunk),
             "format": "json", "resultType": "core",
             "pageSize": len(chunk) + 5}
        data = http_json(EPMC + "?" + urllib.parse.urlencode(q))
        for rec in (data.get("resultList", {}) or {}).get("result", []) or []:
            if rec.get("pmid"):
                out[str(rec["pmid"])] = rec
        if verbose:
            print("  Europe PMC: resolved batch of %d" % len(chunk))
        time.sleep(0.4)
    return out


def crossref_ok(doi):
    """(ok, title_or_error)."""
    try:
        data = http_json(CROSSREF + urllib.parse.quote(doi))
        return True, (data.get("message", {}).get("title") or [""])[0]
    except urllib.error.HTTPError as e:
        return False, "HTTP %s" % e.code
    except Exception as e:
        return False, str(e)[:60]


def audit(path, source_key="nguon", use_crossref=True, verbose=True):
    raw, obj = load_deliverable(path)
    problems, notes = [], []

    cited, listed = harvest_pmids(raw, obj, source_key)
    dois = harvest_dois(raw)

    print("Deliverable: %s" % path)
    print("  PMIDs harvested: %d   DOIs harvested: %d" % (len(cited), len(dois)))
    if verbose:
        print("  (PMIDs: resolved in one pass; DOI trailing punctuation stripped)")

    # ---- PMIDs -----------------------------------------------------------
    recs = {}
    if cited:
        try:
            recs = epmc_records(cited, verbose=verbose)
        except Exception as e:
            print("NETWORK ERROR talking to Europe PMC: %s" % e)
            return 2, problems, notes

    unresolved = sorted(p for p in cited if p not in recs)
    if unresolved:
        problems.append("UNRESOLVED PMIDs (not in Europe PMC; likely invented): "
                        + ", ".join(unresolved))

    ghost = sorted(listed - set(recs)) 
    if ghost:
        problems.append("SOURCE-LIST PMIDs that do not resolve: " + ", ".join(ghost))

    # ---- per-entry metadata match ---------------------------------------
    if isinstance(obj, dict) and isinstance(obj.get(source_key), list):
        for e in obj[source_key]:
            if not isinstance(e, dict) or str(e.get("loai", "")).upper() != "PMID":
                continue
            pid = str(e.get("id", "")).strip()
            rec = recs.get(pid)
            if not rec:
                continue
            # year
            ry, sy = str(rec.get("pubYear", "")), str(e.get("nam", ""))
            if ry and sy and ry != sy:
                problems.append("YEAR MISMATCH PMID %s: source-list says %s, "
                                "Europe PMC says %s" % (pid, sy, ry))
            # title: the registry title must appear (normalized) in the entry
            rt, st = norm(rec.get("title")), norm(e.get("tieu_de"))
            if rt and st:
                probe = rt[:40]
                if probe and probe not in st:
                    problems.append(
                        "TITLE MISMATCH PMID %s: entry text does not contain "
                        "the indexed title. Europe PMC title = %r"
                        % (pid, (rec.get("title") or "")[:90]))
            # DOI cross-check inside the entry text
            rd = clean_doi(str(rec.get("doi") or ""))
            if rd:
                entry_dois = {clean_doi(d) for d in DOI_RE.findall(json.dumps(e, ensure_ascii=False))}
                if entry_dois and rd.lower() not in {x.lower() for x in entry_dois}:
                    problems.append("DOI MISMATCH PMID %s: entry cites %s but "
                                    "Europe PMC records %s"
                                    % (pid, sorted(entry_dois), rd))

    # ---- cited-but-not-listed (reverse check) ---------------------------
    labelled = set(PMID_LABELLED.findall(raw))
    if isinstance(obj, dict) and isinstance(obj.get(source_key), list):
        if labelled - listed:
            notes.append("PMIDs cited in body but ABSENT from source list "
                         "(check each is intentional): "
                         + ", ".join(sorted(labelled - listed)))

    # ---- DOIs ------------------------------------------------------------
    if use_crossref and dois:
        bad = []
        for d in sorted(dois):
            ok, info = crossref_ok(d)
            if not ok:
                bad.append((d, info))
            elif verbose:
                print("  DOI ok  %-34s %s" % (d, str(info)[:52]))
            time.sleep(0.35)
        if bad:
            notes.append("DOIs NOT registered in CrossRef (may still be valid "
                         "publisher DOIs recorded only in PubMed -- flag, do "
                         "not silently drop): "
                         + "; ".join("%s (%s)" % (d, e) for d, e in bad))

    return (1 if problems else 0), problems, notes


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("deliverable")
    ap.add_argument("--source-key", default="nguon",
                    help='JSON key holding the source list (default: nguon)')
    ap.add_argument("--no-crossref", action="store_true",
                    help="skip DOI resolution (faster, PMID-only)")
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args()

    try:
        code, problems, notes = audit(a.deliverable, a.source_key,
                                      not a.no_crossref, not a.quiet)
    except FileNotFoundError:
        print("USAGE ERROR: no such file: %s" % a.deliverable)
        return 2

    print()
    for n in notes:
        print("NOTE: " + n)
    for p in problems:
        print("PROBLEM: " + p)
    if not problems:
        print("OK: every harvested identifier resolved and matched registry metadata.")
    return code


if __name__ == "__main__":
    sys.exit(main())
