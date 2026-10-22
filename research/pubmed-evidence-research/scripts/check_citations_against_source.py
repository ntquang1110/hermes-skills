#!/usr/bin/env python3
"""Offline citation-integrity gate: does an integration draft cite ONLY what its source file contains?

Use when a NEW research file is merged into an existing document (plan/spec/report appendix) and you
must prove "không bịa PMID/DOI" WITHOUT network access. Cheap and fast: pure set comparison of every
PMID:<digits> and DOI:10.xxxx/... token found in the draft vs the source evidence file.

Complements verify_pmids.py (network gate: does the PMID exist + title match?). Run THIS one first:
it catches a citation that exists in the world but does NOT belong to the source you were told to use.

Usage:
    python check_citations_against_source.py <draft_file> <source_file> [<source_file> ...]
    python check_citations_against_source.py --allow-extra draft.md source.md   # warn instead of fail

Exit codes: 0 = every citation in the draft is present in the sources; 1 = fabricated/foreign citation
(or a source file missing / no citations found at all, which usually means a path or encoding problem).
"""
import re
import sys

PMID_RE = re.compile(r"PMID[:\s]*(\d{4,9})", re.I)
DOI_RE = re.compile(r"10\.\d{4,9}/[^\s\)\]\};,]+")


def toks(text):
    pmids = set(PMID_RE.findall(text))
    dois = {d.rstrip(".,;:") for d in DOI_RE.findall(text)}
    return pmids, dois


def main(argv):
    allow_extra = "--allow-extra" in argv
    args = [a for a in argv if not a.startswith("--")]
    if len(args) < 2:
        print(__doc__)
        return 2

    draft_path, source_paths = args[0], args[1:]
    draft = open(draft_path, encoding="utf-8", errors="replace").read()
    d_pmids, d_dois = toks(draft)
    if not (d_pmids or d_dois):
        print(f"FAIL: no PMID/DOI tokens found in draft {draft_path!r} — check path/encoding")
        return 1

    s_pmids, s_dois = set(), set()
    for p in source_paths:
        try:
            s = open(p, encoding="utf-8", errors="replace").read()
        except OSError as e:
            print(f"FAIL: cannot read source {p!r}: {e}")
            return 1
        sp, sd = toks(s)
        print(f"source {p}: {len(sp)} PMID, {len(sd)} DOI")
        s_pmids |= sp
        s_dois |= sd

    missing_p = sorted(d_pmids - s_pmids)
    missing_d = sorted(d_dois - s_dois)
    print(f"draft {draft_path}: {len(d_pmids)} PMID, {len(d_dois)} DOI")
    print(f"missing from sources: {len(missing_p)} PMID, {len(missing_d)} DOI")

    if missing_p:
        print("PMID NOT IN SOURCE:", ", ".join("PMID:" + m for m in missing_p))
    if missing_d:
        print("DOI NOT IN SOURCE:", ", ".join(missing_d))
    if missing_p or missing_d:
        detail = ("Dùng --allow-extra nếu citation ngoài nguồn là chủ ý và đã có nguồn riêng."
                  if allow_extra else "Bịa citation hoặc lấy từ nguồn khác ⇒ sửa trước khi commit.")
        print(f"{'WARN' if allow_extra else 'FAIL'}: {detail}")
        return 0 if allow_extra else 1

    print("OK: mọi citation trong bản tích hợp đều có trong nguồn")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
