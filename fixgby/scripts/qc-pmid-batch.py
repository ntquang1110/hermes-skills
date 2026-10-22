# -*- coding: utf-8 -*-
"""
QC file JSON do subagent nghien cuu sinh ra (fixgby).

Viec lam:
  1. Kiem TON TAI tung PMID qua Europe PMC REST (resultType=core) — KHONG dung snippet.
  2. Bat co title-vs-claim: PMID nao ma ten chat KHONG xuat hien trong tieu de.
  3. Dem so o tag H (cho chua co nguon).

CANH BAO: `verified N/N` CHI chung minh PMID TON TAI. No KHONG chung minh phat bieu
khop nguon. Buoc (2) chi la CO BAY de nguoi doc lai tieu de — khong phai ket luan.

Dung:
    python qc-pmid-batch.py                                  # mac dinh docs/09-tra-cuu-duong-di
    python qc-pmid-batch.py <thu-muc-chua-batch-*.json>
    python qc-pmid-batch.py <thu-muc> --keys cua_vao,toi_mo  # chi kiem vai khoa chang

Chay TREN CHINH FILE subagent ghi, khong doc ban tom tat no tu khai.
"""
import io, json, os, re, sys, time, urllib.request

EPMC = ("https://www.ebi.ac.uk/europepmc/webservices/rest/search?"
        "query=EXT_ID:%s&format=json&resultType=core")
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/131.0 Safari/537.36")

DEFAULT_KEYS = ["cua_vao", "qua_hang_rao", "gan_lan_dau", "gan_de_di", "toi_mo",
                "ra_khoi_te_bao", "thai", "o_lai"]


def norm(s):
    """Dau thap phan cua Lancet la '·' (middle dot) — phai chuan hoa truoc khi so so."""
    return (s or "").replace("·", ".").replace("\u00b7", ".")


def fetch(pmid, tries=3):
    """Tra 1 PMID. None = khong ton tai. {'ERROR':...} = loi mang."""
    for i in range(tries):
        try:
            req = urllib.request.Request(EPMC % pmid, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=30) as r:
                j = json.loads(r.read().decode("utf-8"))
            res = j.get("resultList", {}).get("result", [])
            if not res:
                return None
            r0 = res[0]
            return {"title": r0.get("title", ""),
                    "journal": (r0.get("journalInfo") or {}).get("journal", {}).get("title", ""),
                    "year": r0.get("pubYear", ""), "doi": r0.get("doi", ""),
                    "abstract": norm(r0.get("abstractText", ""))}
        except Exception as e:
            if i == tries - 1:
                return {"ERROR": str(e)}
            time.sleep(1.5 * (i + 1))


def load(src, keys):
    chats = []
    files = sorted(f for f in os.listdir(src) if f.endswith(".json") and not f.startswith("_"))
    for f in files:
        p = os.path.join(src, f)
        try:
            j = json.loads(io.open(p, encoding="utf-8").read())
        except Exception as e:
            print("!! LOI JSON %s: %s" % (p, e)); continue
        arr = j if isinstance(j, list) else j.get("chats") or j.get("data") or [j]
        for c in arr:
            if isinstance(c, dict) and c.get("chat"):
                c["_file"] = f; chats.append(c)
    return chats, files


def keys_of(c, keys):
    out = []
    for k in keys:
        blk = c.get(k) or {}
        for p in (blk.get("pmid") or []):
            out.append((k, str(p).strip()))
    for p in (c.get("pmids") or []):
        out.append(("pmids[]", str(p).strip()))
    return out


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    src = args[0] if args else os.path.join("docs", "09-tra-cuu-duong-di")
    keys = DEFAULT_KEYS
    for a in sys.argv[1:]:
        if a.startswith("--keys="):
            keys = a.split("=", 1)[1].split(",")
    if not os.path.isdir(src):
        print("khong thay thu muc: %s" % src); return

    chats, files = load(src, keys)
    if not chats:
        print("khong co ban ghi nao co khoa 'chat' trong %s" % src); return

    pairs = [(c["chat"], k, p) for c in chats for k, p in keys_of(c, keys)]
    pairset = {(k, p) for _c, k, p in pairs if p}
    uniq = []
    for _c, _k, p in pairs:
        if p and p not in uniq:
            uniq.append(p)
    print("file: %d | ban ghi: %d | o co PMID: %d | PMID duy nhat: %d"
          % (len(files), len(chats), len(pairset), len(uniq)))
    print("file:", ", ".join(files))

    bad, cache = [], {}
    for i, p in enumerate(uniq, 1):
        d = fetch(p)
        cache[p] = d
        if d is None:
            bad.append((p, "KHONG TON TAI"))
        elif "ERROR" in d:
            bad.append((p, "LOI MANG: " + d["ERROR"]))
        if i % 10 == 0:
            print("  ...%d/%d" % (i, len(uniq)))
        time.sleep(0.34)

    print("\n== TON TAI ==  verified %d/%d" % (len(uniq) - len(bad), len(uniq)))
    for p, why in bad:
        print("  X %s — %s" % (p, why))

    print("\n== CO BAY title-vs-claim (ten chat KHONG co trong tieu de) ==")
    flag = 0
    for c in chats:
        toks = [t for t in re.split(r"[^0-9A-Za-z]+",
                "%s %s" % (c.get("chat", ""), c.get("ten_vi", ""))) if len(t) > 3]
        for k, p in keys_of(c, keys):
            d = cache.get(p) or {}
            t = (d.get("title") or "").lower()
            if t and toks and not any(x.lower() in t for x in toks):
                flag += 1
                print("  ? %-14s %-14s PMID %-9s | %s"
                      % (c["chat"], k, p, (d.get("title") or "")[:96]))
    print("  -> %d o CAN DOC LAI TIEU DE bang mat (co bay, KHONG phai loi)" % flag)

    tagh = sum(len(c.get("tag_H") or []) for c in chats)
    print("\n== TAG H == %d o chua co nguon" % tagh)
    for c in chats:
        if c.get("tag_H"):
            print("  %-16s %s" % (c["chat"], " · ".join(c["tag_H"])))

    out = os.path.join(src, "_qc-report.json")
    json.dump({"files": files, "n_chat": len(chats), "verified": len(uniq) - len(bad),
               "total": len(uniq), "bad": bad, "flag": flag, "tag_h": tagh},
              io.open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("\nghi %s" % out)


if __name__ == "__main__":
    main()
