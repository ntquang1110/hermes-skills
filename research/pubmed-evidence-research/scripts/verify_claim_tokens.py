#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""verify_claim_tokens.py — CHỐNG BỊA SỐ/TÊN ENZYME trong deliverable có PMID.

Hai chế độ, dùng cùng một bộ fetch Europe PMC:

  1) --sentences 3319346 6886969 ...   (chống OUTPUT BỊ NUỐT)
     In RA CHỈ NHỮNG CÂU CÓ CHỮ SỐ của từng abstract, upstream viết thường.
     Mục đích: khi `execute_code`/`read_file` nuốt output (trả "(N lines output)"
     + con trỏ observation) thì bạn KHÔNG được viết số từ trí nhớ.
     In theo nhóm 3-4 bài một lượt, mỗi lượt ≤ ~6 KB stdout, để không bị nuốt lại.

  2) --spec spec.json  (hoặc --spec '-' đọc stdin)
     spec = {"3319346": ["8.5 g/h/70 kg", "0.7%", "80 mg/L"], "16792560": ["ADH1B"]}
     Với MỖI cặp (pmid → token), khẳng định token CÓ trong title+abstract thật.
     In CHỈ những cái FAIL + 1 dòng tổng kết. Exit 1 nếu có FAIL.

Tại sao cần: ca thật 19/10/2026 (fixgby lô A) — bản nháp đầu được viết trong lúc
output fetch bị nuốt, tức số nằm trong bài là số NHỚ LẠI. Chạy --spec trên 67 PMID
bắt 13 FAIL; đọc lại abstract thật cho thấy 12/13 là artifact dấu câu/gạch nối
('first-pass' vs 'First pass', 'GABA(A)' vs 'GABAA') NHƯNG 1 cái là lỗi thật cần sửa.
Luật: FAIL KHÔNG tự động = nguồn sai, cũng KHÔNG tự động = nguồn đúng ⇒ đọc abstract
của đúng những bài FAIL.

Bẫy đã xử lý sẵn trong code:
  - `EXT_ID:<pmid>` KHÔNG tồn tại → Europe PMC RƠI VỀ tìm kiếm text và trả bài
    KHÁC HOÀN TOÀN (PMID 540449 → bài "Antenatal care uptake in Nepal"). Guard bắt buộc:
    record trả về phải có `pmid == pmid yêu cầu`, nếu không ⇒ NOTFOUND.
  - `·` (U+00B7) là DẤU THẬP PHÂN của Lancet ⇒ normalize trước khi so token.
  - abstract rỗng (conference/editorial/old paper) ⇒ ghi NO_ABSTRACT, token không
    kiểm được ⇒ bài đó KHÔNG được gánh số nào.
  - Build query bằng urlencode trên dict, KHÔNG hand-quote chuỗi curl (quote lồng
    trong execute_code từng trả body rỗng).

Dùng:
  python verify_claim_tokens.py --sentences 16792560 3319346 6886969
  python verify_claim_tokens.py --spec spec.json
"""
import argparse
import json
import re
import sys
import time
import urllib.parse
import urllib.request

HDR = {"User-Agent": "Mozilla/5.0"}
EPMC = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"


def fetch_core(pmid, attempts=3):
    """Trả dict record hoặc None. None = không tồn tại / không khớp EXT_ID."""
    q = urllib.parse.urlencode(
        {"query": "EXT_ID:%s" % pmid, "format": "json",
         "resultType": "core", "pageSize": 1}
    )
    for i in range(attempts):
        try:
            req = urllib.request.Request(EPMC + "?" + q, headers=HDR)
            with urllib.request.urlopen(req, timeout=30) as r:
                raw = r.read().decode("utf-8", "replace")
            data = json.loads(raw, strict=False)  # strict=False: control chars in abstractText
            hits = data.get("resultList", {}).get("result", [])
            if not hits:
                return None
            rec = hits[0]
            # GUARD: Europe PMC rơi về text-search khi EXT_ID không tồn tại
            if str(rec.get("pmid") or "") != str(pmid):
                return None
            return {
                "pmid": str(rec.get("pmid")),
                "year": rec.get("pubYear", ""),
                "journal": (rec.get("journalInfo") or {}).get("journal", {}).get("title", ""),
                "title": rec.get("title") or "",
                "abstract": (rec.get("abstractText") or "").replace("\u00b7", "."),
            }
        except Exception:
            time.sleep(2 * (i + 1))
    return None


def cmd_sentences(pmids):
    """In chỉ những câu CHỨA CHỮ SỐ → stdout nhỏ, không bị nuốt."""
    for p in pmids:
        c = fetch_core(p)
        if not c:
            print("### %s  NOTFOUND (EXT_ID không tồn tại hoặc record khác pmid)" % p)
            continue
        if not c["abstract"]:
            print("### %s | %s | NO_ABSTRACT" % (p, c["title"][:90]))
            continue
        sents = [s.strip() for s in re.split(r"(?<=[.;])\s+", c["abstract"])
                 if re.search(r"\d", s)]
        print("### %s | %s | %s" % (p, c["year"], c["title"][:90]))
        for s in sents:
            print("  -", s)


def cmd_spec(spec):
    fails = []
    for pmid, tokens in spec.items():
        c = fetch_core(pmid)
        if not c:
            fails.append((pmid, ["<NOTFOUND>"], ""))
            continue
        if not c["abstract"]:
            fails.append((pmid, ["<NO_ABSTRACT>"], c["title"][:70]))
            continue
        hay = (c["title"] + " " + c["abstract"]).lower()
        miss = [t for t in tokens if t.lower() not in hay]
        if miss:
            fails.append((pmid, miss, c["title"][:70]))
    print("CHECKED %d PMID; FAIL %d" % (len(spec), len(fails)))
    for pmid, miss, title in fails:
        print("FAIL %s %s | %s" % (pmid, miss, title))
    print("\nNHẮC: FAIL có thể chỉ là artifact gạch nối/ngoặc "
          "('first-pass' vs 'First pass'). Đọc abstract của ĐÚNG các bài FAIL "
          "trước khi kết luận nguồn sai — và trước khi chấp nhận là nguồn đúng.")
    return 1 if fails else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sentences", nargs="+", metavar="PMID")
    ap.add_argument("--spec", help="file JSON {pmid: [token,...]} hoặc '-' cho stdin")
    a = ap.parse_args()
    if a.sentences:
        cmd_sentences(a.sentences)
        return 0
    if a.spec:
        raw = sys.stdin.read() if a.spec == "-" else open(a.spec, encoding="utf-8").read()
        return cmd_spec(json.loads(raw))
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
