# -*- coding: utf-8 -*-
"""Dung cay meeting note theo dong thoi gian cho D:/Hermes Proj/Meetings/.

Script IDEMPOTENT: chay bao lan cung ra ket qua, khong mat file.
Dung sau moi cuoc hop: tao HTML -> chay script nay -> INDEX.md + CONTEXT.md
duoc cap nhat.

QUAN TRONG: thu muc nay la ban goc. Ban dich nam trong Meetings/20XX-YY/
va KHONG duoc quet lai (chi quet ROOT + _archive).
"""
import io, os, re, glob, json, shutil, datetime, hashlib, unicodedata

ROOT = r"D:/Hermes Proj"
OUT  = os.path.join(ROOT, "Meetings")
STAGE = os.path.join(OUT, "_stage")
ARCH = os.path.join(OUT, "_archive")

# Ngay hop that. mtime khong tin duoc (copy file lam doi no).
# Cap nhat bang ngay meeting moi, XOA dong cu neu khong con dung.
NGAY_GAN = {
    "meeting_affiliate_20260811.html":               "2026-08-11",
    "meeting_2026-08-15_ez80.html":                  "2026-08-15",
    "meeting_nung_hoptac.html":                      "2026-08-21",
    "meeting_vaukuem_invest.html":                   "2026-08-22",
    "meeting_kiemsaphia_noibo.html":                 "2026-08-22",
    "meeting_channuoi_sanpham.html":                 "2026-08-27",
    "meeting_he_sinh_thai_nong_nghiep.html":         "2026-08-28",
    "meeting_hoptac_truyenthong.html":               "2026-09-03",
    "meeting_dinhhuong-sanpham-chan-nuoi.html":      "2026-09-26",
    "meeting_hop-tac-khcn-nong-nghiep.html":         "2026-09-26",
    "meeting_chien-luoc-san-pham-chan-nuoi.html":    "2026-09-26",
    "infographic_hop-tac-khcn-nong-nghiep.html":     "2026-09-26",
    "infographic_chien-luoc-san-pham-chan-nuoi.html": "2026-09-26",
    "meeting_quan-tri-san-pham-tpcn.html":              "2026-10-09",
}


def text_of(html, pattern):
    m = re.search(pattern, html, re.S | re.I)
    if not m:
        return ""
    s = re.sub(r"<[^>]+>", " ", m.group(1))
    s = s.replace("&amp;", "&").replace("&nbsp;", " ")
    return re.sub(r"\s+", " ", s).strip()


def slugify(s, maxlen=48):
    s = s.lower().replace("\u0111", "d")
    s = unicodedata.normalize("NFD", s)
    s = "".join(ch for ch in s if unicodedata.category(ch) != "Mn")
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    if len(s) > maxlen:
        cut = s[:maxlen]
        if "-" in cut[maxlen // 2:]:
            cut = cut.rsplit("-", 1)[0]
        s = cut.strip("-")
    return s or "meeting"


def guess_date(fname):
    if fname in NGAY_GAN:
        return datetime.date.fromisoformat(NGAY_GAN[fname])
    m = re.search(r"(20\d{2})[-_]?(\d{2})[-_]?(\d{2})", fname)
    if m:
        try:
            return datetime.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        except ValueError:
            pass
    return None


def _nodau(s):
    s = s.lower().replace("\u0111", "d")
    s = unicodedata.normalize("NFD", s)
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


def classify(blob):
    b = _nodau(blob)
    if "infographic" in b or "hai muoi tam ngay vang" in b or "cong nghe hoat hoa" in b:
        return "Infographic"
    if any(k in b for k in ["dau tu", "trinh ", "vua kiem", "mana", "tai chinh"]):
        return "Dau tu / Tai chinh"
    if any(k in b for k in ["hop tac", "khcn", "khoa hoc", "truyen thong", "bao chi"]):
        return "Hop tac / KHCN"
    if any(k in b for k in ["chien luoc", "dinh huong", "san pham", "ton kho", "chot gia",
                            "cong thuc", "quan tri san pham", "thuc pham"]):
        return "Quan ly san pham"
    if any(k in b for k in ["noi bo", "affiliate"]):
        return "Noi bo"
    return "Khac"


def collect():
    """Chi quet ban goc o ROOT + ban trung chu de trong _archive.
    KHONG quet Meetings/20XX-YY/ (do la ban dich, quet se lap vo on)."""
    found = list(glob.glob(os.path.join(ROOT, "meeting_*.html")))
    found += list(glob.glob(os.path.join(ROOT, "infographic_*.html")))
    found += list(glob.glob(os.path.join(ARCH, "meeting_*.html")))
    found += list(glob.glob(os.path.join(ARCH, "infographic_*.html")))
    seen, out = set(), []
    for f in sorted(found):
        rp = os.path.realpath(f)
        if rp in seen:
            continue
        seen.add(rp)
        out.append(f)
    return out


def main():
    previews = {}
    pm = os.path.join(OUT, "_previews.json")
    if os.path.exists(pm):
        try:
            previews = json.load(io.open(pm, encoding="utf-8"))
        except Exception:
            pass

    entries = []
    for f in collect():
        base = os.path.basename(f)
        try:
            html = io.open(f, encoding="utf-8", errors="replace").read()
        except Exception:
            continue
        title = text_of(html, r"<title>(.*?)</title>")
        h1 = text_of(html, r"<h1[^>]*>(.*?)</h1>")
        display = h1 or title or base[:-5]
        display = re.sub(r"^Meeting\s*[:\u2014-]\s*", "", display).strip()
        if display.lower().startswith("meeting"):
            display = display[7:].strip(" :\u2014-")
        entries.append(dict(
            src=f, base=base, title=title, h1=h1, display=display,
            slug=slugify(display), date=guess_date(base),
            cat=classify(title + " " + h1),
            size=len(html.encode("utf-8")),
            md5=hashlib.md5(re.sub(r"\s+", " ", html).encode("utf-8")).hexdigest(),
        ))

    if not entries:
        print("KHONG tim thay file goc nao o ROOT hoac _archive.")
        print("Cay hien tai:")
        for d in sorted(glob.glob(os.path.join(OUT, "20*"))):
            for x in sorted(glob.glob(os.path.join(d, "*"))):
                print("  ", os.path.relpath(x, OUT))
        return

    byslug = {}
    for e in entries:
        byslug.setdefault(e["slug"], []).append(e)
    keep, archived = [], []
    for slug, group in byslug.items():
        group.sort(key=lambda x: -x["size"])
        keep.append(group[0])
        for e in group[1:]:
            archived.append(dict(e, kept_as=group[0]["base"]))

    final, seen = [], {}
    for e in sorted(keep, key=lambda x: (x["date"] or datetime.date(1970, 1, 1), -x["size"])):
        if e["md5"] in seen:
            archived.append(dict(e, kept_as=seen[e["md5"]]))
            continue
        seen[e["md5"]] = e["base"]
        final.append(e)

    # dedupe danh sach archive (cung base se xuat hien 2 lan khi quet ROOT + _archive)
    arch_seen, arch_dedup = set(), []
    for e in archived:
        if e["base"] in arch_seen:
            continue
        arch_seen.add(e["base"])
        arch_dedup.append(e)
    archived = arch_dedup

    need_date = [e for e in final if e["date"] is None]
    for e in final:
        if e["date"] is None:
            e["date"] = datetime.date.fromtimestamp(os.path.getmtime(e["src"]))

    used = set()
    for e in sorted(final, key=lambda x: x["date"]):
        n, base = 2, f"{e['date'].isoformat()}_{e['slug']}.html"
        while base in used:
            base = f"{e['date'].isoformat()}_{e['slug']}_{n}.html"
            n += 1
        used.add(base)
        e["outname"] = base

    # GIAI DOAN 1: copy moi vao staging (khong dung ban cu)
    if os.path.isdir(STAGE):
        shutil.rmtree(STAGE, ignore_errors=True)
    os.makedirs(STAGE, exist_ok=True)
    for e in final:
        shutil.copy2(e["src"], os.path.join(STAGE, e["outname"]))
    for e in archived:
        if os.path.exists(e["src"]):
            shutil.copy2(e["src"], os.path.join(STAGE, "__arch__" + e["base"]))

    # GIAI DOAN 2: xoa cay cu
    for d in glob.glob(os.path.join(OUT, "20*")):
        shutil.rmtree(d, ignore_errors=True)

    # GIAI DOAN 3: danh lai tu staging
    for e in final:
        sub = os.path.join(OUT, e["date"].strftime("%Y-%m"))
        os.makedirs(sub, exist_ok=True)
        dst = os.path.join(sub, e["outname"])
        shutil.move(os.path.join(STAGE, e["outname"]), dst)
        e["dst"] = dst
        e["preview"] = previews.get(e["base"], "")

    os.makedirs(ARCH, exist_ok=True)
    for e in archived:
        s = os.path.join(STAGE, "__arch__" + e["base"])
        if os.path.exists(s):
            shutil.move(s, os.path.join(ARCH, e["base"]))
        e["dst"] = os.path.join(ARCH, e["base"])
    shutil.rmtree(STAGE, ignore_errors=True)

    # CHI INDEX.md duoc regenerate. CONTEXT.md / DECISIONS.md la tai lieu
    # viet tay, KHONG de xoa.
    L = ["# Meeting notes: dong thoi gian", "",
         f"{len(final)} bien ban, {len(archived)} ban archive. Sap xep theo ngay họp.",
         "Dung lai bang: `python <skill>/scripts/build-meetings-index.py`",
         "",
         "| Ngay | Chu de | Nhom | Preview |", "|---|---|---|---|"]
    for e in sorted(final, key=lambda x: x["date"]):
        rel = os.path.relpath(e["dst"], OUT).replace("\\", "/")
        pv = f"[xem]({e['preview']})" if e["preview"] else "-"
        L.append(f"| {e['date'].isoformat()} | [{e['display']}]({rel}) | {e['cat']} | {pv} |")

    L += ["", "## Chi tiet theo thang", ""]
    bym = {}
    for e in final:
        bym.setdefault(e["date"].strftime("%Y-%m"), []).append(e)
    for m in sorted(bym, reverse=True):
        L += [f"### {m}", ""]
        for e in sorted(bym[m], key=lambda x: x["date"]):
            rel = os.path.relpath(e["dst"], OUT).replace("\\", "/")
            L += [f"**{e['date'].strftime('%d/%m')} - {e['display']}**", "",
                  f"- File: [{os.path.basename(e['dst'])}]({rel})",
                  f"- Nhom: {e['cat']} | Kich thuoc: {e['size']:,} bytes"]
            if e["preview"]:
                L.append(f"- Preview: {e['preview']}")
            L.append("")

    if archived:
        L += ["## Archive", "",
              "Ban trung chu de, dua sang `_archive/`.", "",
              "| File | Kich thuoc | Giu lai bang |", "|---|---|---|"]
        for e in sorted(archived, key=lambda x: x["base"]):
            L.append(f"| `{e['base']}` | {e['size']:,} | `{e.get('kept_as','trung byte')}` |")
        L.append("")
    if need_date:
        L += ["## Can xac nhan ngay", ""]
        for e in need_date:
            L.append(f"- `{e['base']}` (dung ngay sua file)")
        L.append("")

    io.open(os.path.join(OUT, "INDEX.md"), "w", encoding="utf-8").write("\n".join(L))

    print(f"Da dung {len(final)} file, archive {len(archived)} file")
    for m in sorted(bym, reverse=True):
        print(f"  {m} -> {len(bym[m])} file")
    for e in sorted(final, key=lambda x: x["date"]):
        print("  ", e["date"], e["cat"][:20].ljust(22), e["outname"])
    for e in archived:
        print("   ARCHIVE", e["base"], f"({e['size']:,}b)", "-> giu:", e.get("kept_as", "trung byte"))


if __name__ == "__main__":
    main()
