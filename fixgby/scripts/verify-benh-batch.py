# -*- coding: utf-8 -*-
"""
Verify mot lo "duong di cua BENH" (docs/11-duong-di-benh/batch-*.json).

4 phep kiem:
  1. Moi PMID ton tai that qua Europe PMC EXT_ID (va tra ve dung pmid).
  2. Moi con so trong mo_ta / diem_cat / da_that_bai / tac_dong phai nam trong
     abstractText cua chinh (cac) PMID duoc trich trong o do.
     So sanh tren chuoi da chuan hoa: 10.000 == 10,000 == 10000, va 4.0 == 4,0.
  3. Cau truc: du 8 chang, tag_H khop dung cac o "chua co nguon", moi pmid verify duoc.
  4. Do phu diem_cat: MOI benh nen co >=1 diem cat tren MOI chang (8/8).
     Thieu = CAN SOI (mem), khong phai loi cung — nhung phai doc ra truoc khi nop.

Chay:
  python verify-benh-batch.py "D:/Hermes Proj/fixgby/docs/11-duong-di-benh/batch-c-ho-hap.json"
  python verify-benh-batch.py            # mac dinh batch-c trong docs/11

Exit code 1 neu co loi cung (PMID chet, thieu chang).
So khong tim thay in ra de soi tay — KHONG tu dong ket luan bia.
"""
import io
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

DEFAULT = r"D:/Hermes Proj/fixgby/docs/11-duong-di-benh/batch-c-ho-hap.json"
EPMC = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
CHANG = ["1_xam_nhap", "2_qua_hang_rao", "3_bam_cu_tru", "4_nhan_len",
         "5_lan_he_thong", "6_tin_hieu_hai", "7_hau_qua", "8_thai_lay"]
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/131.0 Safari/537.36")

# Chi lay token so DUNG RIENG: tranh CD163, H1N1, IL-8, ApxII, gp5, SA-alpha-2,3.
NUM = re.compile(r"(?<![A-Za-z0-9])(\d+(?:[.,]\d+)?)(?![A-Za-z0-9])")


def norm(s):
    return (s or "").replace("\u00b7", ".")


def canon(s):
    """10.000 / 10,000 / 10000 -> 10000 ; 4.0 / 4,0 -> 40.

    So khop trong khong gian chi-con-chu-so, co bien so o hai dau, nen
    '252' khong an vao '12521' va '10.000' khop '10,000'.
    """
    return re.sub(r"[.,]", "", s or "")


def num_in(n, ab):
    c = canon(n)
    if not c:
        return True
    if re.search(r"(?<!\d)" + re.escape(c) + r"(?!\d)", canon(ab)):
        return True
    return n in (ab or "")          # du phong: so nam trong nhan/ten hoa chat


def fetch(pmid):
    url = EPMC + "?" + urllib.parse.urlencode(
        {"query": "EXT_ID:%s" % pmid, "resultType": "core", "format": "json"})
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for _ in range(3):
        try:
            with urllib.request.urlopen(req, timeout=45) as r:
                j = json.loads(r.read().decode("utf-8"))
            res = j.get("resultList", {}).get("result", [])
            if res and str(res[0].get("pmid")) == str(pmid):
                return {"ok": True, "a": norm(res[0].get("abstractText", "")),
                        "t": res[0].get("title", ""),
                        "y": res[0].get("pubYear", "")}
        except Exception as e:  # noqa: BLE001
            err = str(e)
            time.sleep(1.5)
    return {"ok": False, "a": "", "t": "", "err": locals().get("err", "")}


def nums(text):
    out = []
    for m in NUM.finditer(text or ""):
        t = m.group(1)
        if len(canon(t)) < 2:
            continue
        out.append(t)
    return out


def load(path):
    j = json.load(io.open(path, encoding="utf-8"))
    if isinstance(j, list):
        return {"benh": j, "yeu_to_anh_huong": []}
    return j


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT
    doc = load(path)
    benh = doc.get("benh") or doc.get("chat") or []
    env = doc.get("yeu_to_anh_huong") or []
    src_dir = os.path.dirname(os.path.abspath(path))
    cache_path = os.path.join(src_dir, "_verified_abstracts.json")

    # ---- tap PMID ----
    all_pm = set()
    for b in benh:
        for p in b.get("pmids", []):
            all_pm.add(str(p))
        for c in (b.get("chang") or {}).values():
            all_pm.update(str(p) for p in c.get("pmid", []))
        for d in b.get("diem_cat", []):
            all_pm.update(str(p) for p in d.get("pmid", []))
        for d in b.get("da_that_bai", []):
            all_pm.update(str(p) for p in d.get("pmid", []))
        for d in b.get("chi_dau_do_duoc", []):
            all_pm.update(str(p) for p in d.get("pmid", []))
    for y in env:
        all_pm.update(str(p) for p in y.get("pmid", []))
    all_pm = sorted(all_pm, key=lambda x: int(x) if x.isdigit() else 0)

    cache = {}
    if os.path.exists(cache_path):
        cache = json.load(io.open(cache_path, encoding="utf-8"))

    print("file:", path)
    print("benh: %d | diem_cat: %d | PMID duy nhat: %d | yeu_to: %d"
          % (len(benh), sum(len(b.get("diem_cat", [])) for b in benh),
             len(all_pm), len(env)))

    # ---- 1. ton tai ----
    for p in all_pm:
        if cache.get(p, {}).get("ok"):
            continue
        cache[p] = fetch(p)
        time.sleep(0.25)
    json.dump(cache, io.open(cache_path, "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    dead = [p for p in all_pm if not cache.get(p, {}).get("ok")]
    print("PMID khong ton tai/khong lay duoc:", dead if dead else "khong co")

    # ---- 2. so vs abstract ----
    def hay(pmids):
        return " || ".join(cache.get(str(p), {}).get("a", "") for p in pmids)

    flags = []
    for b in benh:
        for k, c in (b.get("chang") or {}).items():
            txt = c.get("mo_ta", "")
            ab = hay(c.get("pmid", []))
            for n in nums(txt):
                if not num_in(n, ab):
                    flags.append((b.get("id"), k, n, c.get("pmid", []), "mo_ta"))
        for d in b.get("diem_cat", []):
            ab = hay(d.get("pmid", []))
            for n in nums(d.get("ly_do", "") + " " + d.get("diem", "")):
                if not num_in(n, ab):
                    flags.append((b.get("id"), d.get("chang"), n, d.get("pmid", []), "diem_cat"))
        for d in b.get("da_that_bai", []):
            ab = hay(d.get("pmid", []))
            for n in nums(d.get("ket_qua", "")):
                if not num_in(n, ab):
                    flags.append((b.get("id"), "da_that_bai", n, d.get("pmid", []), "da_that_bai"))
    for y in env:
        ab = hay(y.get("pmid", []))
        for n in nums(y.get("tac_dong", "")):
            if not num_in(n, ab):
                flags.append((y.get("yeu_to"), "env", n, y.get("pmid", []), "tac_dong"))

    print("\nSo khong tim thay trong abstract cua PMID duoc trich: %d" % len(flags))
    for f in flags:
        print("   ", f)

    # ---- 3. cau truc ----
    hard = list(dead)
    h_note = []
    for b in benh:
        ch = b.get("chang") or {}
        missing = [k for k in CHANG if k not in ch]
        if missing:
            hard.append("%s thieu chang %s" % (b.get("id"), missing))
        for k, c in ch.items():
            if (c.get("mo_ta") or "").strip() == "chua co nguon":
                if k not in (b.get("tag_H") or []):
                    h_note.append("%s/%s 'chua co nguon' nhung thieu tag_H" % (b.get("id"), k))
            if c.get("mo_ta") and c.get("mo_ta").strip() != "chua co nguon" and not c.get("pmid"):
                h_note.append("%s/%s co mo_ta nhung khong co pmid" % (b.get("id"), k))

    print("\n== CAU TRUC ==")
    print("  du 8 chang:", "OK" if not any("thieu chang" in x for x in hard) else "LOI")
    print("  tag_H:", "OK" if not h_note else "CAN SOI")
    for x in h_note:
        print("   ", x)
    print("  tong tag_H:", sum(len(b.get("tag_H") or []) for b in benh))
    for k in CHANG:
        n = sum(1 for b in benh if (b.get("chang") or {}).get(k, {}).get("mo_ta", "").strip()
                and (b.get("chang") or {}).get(k, {}).get("mo_ta") != "chua co nguon")
        print("  %-16s %d/%d" % (k, n, len(benh)))

    # ---- 4. do phu diem_cat theo chang (mem) ----
    print("\n== DIEM_CAT THEO CHANG (moi benh nen 8/8) ==")
    gap_total = 0
    for b in benh:
        have = {d.get("chang") for d in b.get("diem_cat", [])}
        gap = [k for k in CHANG if k not in have]
        gap_total += len(gap)
        print("  %-14s %d/8 %s" % (b.get("id"), 8 - len(gap),
                                   ("thieu: " + ", ".join(gap)) if gap else ""))
    if gap_total:
        print("  -> CAN SOI: chang khong co diem cat nao. Chang 'khong xay ra' (vd mầm")
        print("     khong xam nhap) van nen co 1 dong chan doan/loai tru, khong bo trong.")
    else:
        print("  -> OK 8/8 moi benh")

    if hard:
        print("\nLOI CUNG:")
        for x in hard:
            print("  -", x)
        sys.exit(1)
    print("\nOK" if not flags else "\nOK phan cung; con %d so can soi tay." % len(flags))


if __name__ == "__main__":
    main()
