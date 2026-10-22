# -*- coding: utf-8 -*-
"""QC hai cong cho BAN DO TUONG KY premix (docs/14-*).

  python qc-tuong-ky.py <batch-lo-N-tuong-ky.json>

Cong 1: verify MOI pmid (truong `pmid` + tag `nguon_nen_<pmid>`) qua Europe PMC:
        hitCount == 1 VA resultList.result[0].pmid dung bang so do.
Cong 2: moi GIA TRI so trong co_che / hau_qua / xu_ly phai nam trong abstractText
        cua chinh cac PMID duoc cap do trich (ke ca nguon nen).

Bai hoc da tra gia (xem references/ban-do-tuong-ky-premix-lo-1.md):
  * Haystack PHAI gom ca nguon nen trong tag_H, neu khong se bao co gia hang loat
    (lo 1: 36 co gia -> 0 sau khi bom nen vao tag).
  * So sanh theo GIA TRI, khong theo cum "so + don vi": abstract viet
    `231.60 mg.g-1` / `0.011 mg mL-1`, bai viet `mg/g` / `mg/mL`.
  * Chuan hoa `·`->`.`, bo NBSP, bo dau phan cach nghin o CA HAI phia.
  * p-value bi Europe PMC cat (chuoi ket thuc bang `(p`) => khong trich so.
"""
import json, os, re, sys, time, urllib.parse, urllib.request

BASE = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
CACHE_NAME = "_abstracts-qc.json"
NUM = re.compile(r"\d+(?:[.,]\d+)?\s?(?:%|mg/kg|mg/L|mg/ngay|mg/ngày|g/kg|g/ton|g/tan|g/tấn|"
                 r"mg\.g-1|mg/g|mg/mL|mg mL-1|ug/mL|μg/mL|ng\.h/mL|CFU|ppm|meq/kg|log|μm|um)")
CTX = {"70", "90", "5", "30", "60", "1", "2", "3", "4", "7", "24", "48"}  # hang so boi canh de bai


def norm(t):
    t = (t or "").replace("·", ".").replace("\u00a0", " ").replace("*", "")
    return re.sub(r"[,\s]", "", t)


def fetch(pmid, cache):
    if pmid in cache:
        return cache[pmid]
    out = ""
    try:
        url = BASE + "?query=" + urllib.parse.quote("EXT_ID:%s AND SRC:MED" % pmid) + \
              "&resultType=core&format=json"
        d = json.load(urllib.request.urlopen(url, timeout=60))
        if d.get("hitCount") == 1 and d["resultList"]["result"][0].get("pmid") == pmid:
            out = d["resultList"]["result"][0].get("abstractText", "") or ""
    except Exception as e:                                    # noqa: BLE001
        print("   !! fetch loi %s: %s" % (pmid, e))
    cache[pmid] = out
    return out


def main(path):
    data = json.load(open(path, encoding="utf-8"))
    pairs = data["cap_tuong_ky"] if isinstance(data, dict) else data
    here = os.path.dirname(os.path.abspath(path))
    cache_path = os.path.join(here, CACHE_NAME)
    cache = {}
    if os.path.exists(cache_path):
        cache = json.load(open(cache_path, encoding="utf-8"))

    used, fail, miss, err_missing = [], [], [], []
    for i, p in enumerate(pairs, 1):
        nen = [t.replace("nguon_nen_", "") for t in p.get("tag_H", []) if t.startswith("nguon_nen_")]
        pmids = [str(x) for x in (p.get("pmid") or [])] + nen
        if p.get("muc_bang_chung") == "chua_co_nguon" and p.get("pmid"):
            err_missing.append((i, "chua_co_nguon nhung van co pmid[]"))
        if p.get("muc_bang_chung") != "chua_co_nguon" and not p.get("pmid"):
            err_missing.append((i, "co bang chung nhung pmid[] rong"))
        used += pmids

        hay = ""
        for m in pmids:
            txt = fetch(m, cache)
            if not txt:
                fail.append(m)
            hay += " " + norm(txt)
        for f in ("co_che", "hau_qua", "xu_ly"):
            for tok in NUM.findall(p.get(f) or ""):
                c = tok.strip()
                if c in CTX:
                    continue
                val = norm(re.match(r"[\d.,]+", c).group(0))
                if val not in hay and val.rstrip("0").rstrip(".") not in hay:
                    miss.append((i, f, c, pmids))

    ids = sorted(set(used))
    print("CAP        %d" % len(pairs))
    print("PMID       %d/%d verify" % (len(ids) - len(set(fail)), len(ids)))
    if fail:
        print("  FAIL     %s" % sorted(set(fail)))
    print("NUM_MISS   %d" % len(miss))
    for m in miss:
        print("   ", m)
    if err_missing:
        print("SCHEMA_LOI %d" % len(err_missing))
        for e in err_missing:
            print("   ", e)
    json.dump(cache, open(cache_path, "w", encoding="utf-8"), ensure_ascii=False)
    return 1 if (fail or miss or err_missing) else 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
