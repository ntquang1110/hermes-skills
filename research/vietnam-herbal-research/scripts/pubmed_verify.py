#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PubMed E-utilities verification, rate-limit safe (no API key: ~3 req/s).

Usage:
  python pubmed_verify.py search "zinc oxide piglets diarrhea" "diosmectite piglets"
  python pubmed_verify.py fetch 33670980 23308387 31286936

Rules proven 08/2026 (piglet-diarrhea catalog, 28 PMID verified in one session):
- SEQUENTIAL calls only; parallel curl/esearch => {"error":"API rate limit exceeded"}
- sleep 1.1s between calls; retry 4x with sleep(3) on transient failures
- always efetch and READ the abstract before citing a PMID
- save fetched abstracts to a file (e.g. _abstracts.json) as audit evidence
"""
import json, sys, time, urllib.request, urllib.parse

BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"


def _get(url, tries=4):
    for attempt in range(tries):
        try:
            with urllib.request.urlopen(url, timeout=30) as r:
                return r.read().decode("utf-8", "replace")
        except Exception:
            time.sleep(3)
    return "ERR"


def esearch(term, retmax=5):
    url = BASE + "esearch.fcgi?db=pubmed&retmode=json&retmax=%d&term=%s" % (
        retmax, urllib.parse.quote(term))
    for attempt in range(4):
        try:
            return json.loads(_get(url))["esearchresult"]["idlist"]
        except Exception:
            time.sleep(3)
    return ["ERR"]


def efetch(pmid):
    url = BASE + "efetch.fcgi?db=pubmed&id=%s&rettype=abstract&retmode=text" % pmid
    return _get(url)


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    mode = sys.argv[1]
    if mode == "search":
        for term in sys.argv[2:]:
            print("%-40s -> %s" % (term[:40], esearch(term)))
            time.sleep(1.1)
    elif mode == "fetch":
        for pmid in sys.argv[2:]:
            txt = efetch(pmid)
            print("==== %s ====" % pmid)
            print(txt[:1200].replace("\n", " "))
            time.sleep(1.2)
    else:
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
