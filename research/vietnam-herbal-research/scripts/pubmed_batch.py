#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PubMed batch: nhiều query → esearch + esummary + efetch → 1 file JSON.

Tốt hơn `pubmed_verify.py` (chỉ in ra màn hình) khi cần 20–30 query: gom hết
title/journal/year/doi + ABSTRACT NGUYÊN VĂN vào JSON để làm audit trail và
trích số liệu về sau mà không phải gọi lại API.

Usage:
    python pubmed_batch.py queries.json out.json
    # queries.json = ["query 1", "query 2", ...]

Thời gian: mỗi query ~9,6 s (1 esearch + 1 esummary + 6 efetch, mỗi call sleep 1.2 s)
→ 25 query ≈ 4–5 phút. **Chạy background** (terminal background=true,
notify_on_complete=true) rồi làm việc web/market research song song.

Đã verify 09/2026: 25 + 24 query, >150 abstract, không bị throttle.
TUYỆT ĐỐI không chạy 2 call eutils song song trong cùng một turn (rate limit 3 req/s).
"""
import json, sys, time, urllib.request, urllib.parse

BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
SLEEP = 1.2   # no api_key: ~3 req/s → 1,2 s là an toàn


def _get(url, tries=4):
    for _ in range(tries):
        try:
            with urllib.request.urlopen(url, timeout=40) as r:
                return r.read().decode("utf-8", "replace")
        except Exception:
            time.sleep(3)
    return "ERR"


def esearch(term, retmax=6):
    url = BASE + "esearch.fcgi?db=pubmed&retmode=json&retmax=%d&sort=relevance&term=%s" \
          % (retmax, urllib.parse.quote(term))
    for _ in range(4):
        try:
            return json.loads(_get(url))["esearchresult"]["idlist"]
        except Exception:
            time.sleep(3)
    return []


def esummary(ids):
    if not ids:
        return {}
    url = BASE + "esummary.fcgi?db=pubmed&retmode=json&id=%s" % ",".join(ids)
    try:
        d = json.loads(_get(url))
        out = {}
        for i in d.get("result", {}).get("uids", []):
            r = d["result"][i]
            out[i] = {
                "title": r.get("title", ""),
                "journal": r.get("fulljournalname") or r.get("source", ""),
                "year": (r.get("pubdate", "") or "")[:4],
                "authors": [a.get("name", "") for a in r.get("authors", [])][:3],
                "doi": next((x.get("value") for x in r.get("articleids", [])
                             if x.get("idtype") == "doi"), ""),
            }
        return out
    except Exception:
        return {}


def efetch(pmid):
    return _get(BASE + "efetch.fcgi?db=pubmed&id=%s&rettype=abstract&retmode=text" % pmid)


if __name__ == "__main__":
    queries = json.load(open(sys.argv[1], encoding="utf-8"))
    out = {}
    for q in queries:
        ids = esearch(q); time.sleep(SLEEP)
        meta = esummary(ids); time.sleep(SLEEP)
        recs = []
        for i in ids:
            recs.append({"pmid": i, "meta": meta.get(i, {}), "abstract": efetch(i)})
            time.sleep(SLEEP)
        out[q] = recs
        print("DONE: %s -> %d hits" % (q, len(ids)), flush=True)
    json.dump(out, open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("saved", sys.argv[2])
