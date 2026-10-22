# -*- coding: utf-8 -*-
"""
Kiem SO TRONG O CO THAT NAM TRONG ABSTRACT KHONG.
Day moi la phep kiem chong bia so (qc-batch.py chi kiem PMID ton tai).

Voi moi o (chat, chang) co PMID: lay abstract THAT cua tung PMID duoc trich,
roi kiem tung con so trong o co xuat hien trong abstract nao khong.
Chuan hoa: dau cham giua '·' -> '.', ',' <-> '.', bo dau phan nghin.

Chay: python audit-num.py   (cache abstract vao _abstracts.json)
"""
import io, json, os, re, time, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = os.path.join(ROOT, "docs", "09-tra-cuu-duong-di")
CACHE = os.path.join(SRC, "_abstracts.json")
EPMC = ("https://www.ebi.ac.uk/europepmc/webservices/rest/search?"
        "query=EXT_ID:%s&format=json&resultType=core")
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/131.0 Safari/537.36")
CHANG = ["cua_vao", "qua_hang_rao", "gan_lan_dau", "gan_de_di", "toi_mo",
         "ra_khoi_te_bao", "thai", "o_lai"]

# Chi lay token so DUNG RIENG. Ban cu \d+(?:[.,]\d+)? bat ca so trong ten
# hoa chat/gen/bom (1,25(OH)2D3, SLC47A1, CD163, IL-8) -> 6/7 co flag la
# duong tinh gia (xem pitfall 17). Lookaround loai chung tu goc.
NUM = re.compile(r"(?<![A-Za-z0-9])(\d+(?:[.,]\d+)?)(?![A-Za-z0-9])")


def norm(s):
    return (s or "").replace("·", ".").replace("\u00b7", ".")


def tight(s):
    """bo het dau phan cach so de bat 2,300 vs 2300"""
    return re.sub(r"(?<=\d)[.,](?=\d{3}\b)", "", s)


def fetch(pmid):
    req = urllib.request.Request(EPMC % pmid, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        j = json.loads(r.read().decode("utf-8"))
    res = j.get("resultList", {}).get("result", [])
    if not res:
        return None
    return {"t": res[0].get("title", ""), "a": norm(res[0].get("abstractText", ""))}


def cells(c):
    out = []
    for k in CHANG:
        blk = c.get(k) or {}
        nums, pm = [], []
        for f, v in blk.items():
            if f == "pmid":
                pm += [str(x).strip() for x in (v or [])]
            elif isinstance(v, str):
                nums += [m.group(1) for m in NUM.finditer(v)]
            elif isinstance(v, (int, float)):
                nums.append(str(v))
        if pm:
            out.append((k, nums, pm))
    return out


def main():
    cache = {}
    if os.path.exists(CACHE):
        cache = json.loads(io.open(CACHE, encoding="utf-8").read())

    chats = []
    for b in ("a", "b", "c"):
        p = os.path.join(SRC, "batch-%s.json" % b)
        if not os.path.exists(p):
            continue
        j = json.loads(io.open(p, encoding="utf-8").read())
        arr = j if isinstance(j, list) else j.get("chat") or j.get("chats") or j.get("data")
        chats += [c for c in arr if isinstance(c, dict) and c.get("chat")]

    need = sorted({p for c in chats for _k, _n, pm in cells(c) for p in pm if p and p not in cache})
    print("chat %d | PMID can lay abstract: %d (co cache: %d)" % (len(chats), len(need), len(cache)))
    for i, p in enumerate(need, 1):
        try:
            cache[p] = fetch(p)
        except Exception as e:
            cache[p] = {"t": "", "a": "", "err": str(e)}
        if i % 20 == 0:
            print("  ...%d/%d" % (i, len(need)))
            json.dump(cache, io.open(CACHE, "w", encoding="utf-8"), ensure_ascii=False)
        time.sleep(0.3)
    json.dump(cache, io.open(CACHE, "w", encoding="utf-8"), ensure_ascii=False)

    tot_cells = tot_ok = 0
    flags = []
    for c in chats:
        for k, nums, pm in cells(c):
            tot_cells += 1
            hay = " || ".join(norm((cache.get(p) or {}).get("a") or "") for p in pm).lower()
            hay_t = tight(hay)
            miss = []
            for n in nums:
                n = norm(n)
                if len(n) < 2 or n in ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"):
                    continue
                cands = {n, n.replace(".", ","), n.replace(",", "."), tight(n)}
                if any(x and (x in hay or x in hay_t) for x in cands):
                    continue
                miss.append(n)
            if miss:
                flags.append((c["chat"], k, sorted(set(miss))[:6], len(pm)))
            else:
                tot_ok += 1

    print("\n== SO TRONG O vs ABSTRACT ==")
    print("o co PMID: %d | khop het: %d | co so khong tim thay: %d" % (tot_cells, tot_ok, len(flags)))
    for chat, k, miss, npm in flags:
        print("  ? %-16s %-15s PMID:%-2d so=%s" % (chat, k, npm, ", ".join(miss)))
    print("\nLUU Y: co 'khong tim thay' KHONG tu dong la bia — so co the duoc tinh lai, doi don vi,")
    print("hoac nam o bang/hinh (abstract chi co text). Nhung day la danh sach phai soi bang mat.")

    json.dump({"cells": tot_cells, "ok": tot_ok, "flags": len(flags),
               "detail": [{"chat": a, "chang": b, "so": c, "n_pmid": d} for a, b, c, d in flags]},
              io.open(os.path.join(SRC, "_num-report.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
