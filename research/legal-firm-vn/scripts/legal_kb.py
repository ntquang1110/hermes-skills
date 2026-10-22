#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
legal_kb.py — Vietnamese Legal Knowledge Base Layer (deterministic)

Muc dich: kiem tra hieu luc van ban phap luat bang CODE, khong de LLM doan.

Khong phai tu van phap ly. Chi la lop kiem chung du lieu.

Commands
--------
check   Kiem tra 1 van ban co con hieu luc khong (theo ngay)
find    Tim van ban theo chu de / tieu de
audit   Danh gia do bao pho cua KB: van ban het han, thieu ngay, trung so
add     Them / cap nhat 1 van ban vao KB
list    Liet ke tat ca van ban (nhom / trang thai)
expired Liet ke van ban da het hieu luc
stale   Liet ke van ban sap het hieu luc (canh bao truoc)

Exit codes
----------
0  OK / khong van de
1  Van ban het hieu luc hoac khong tim thay (BLOCKING)
2  Loi cu phap / input sai
"""

import json
import os
import sys
import argparse
from datetime import date, datetime, timedelta

KB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "legal_registry.json")

# Nhom van ban — dung de gan nhanh
GROUPS = {
    "hienphap": "Hien phap",
    "bo_luat": "Bo luat",
    "luat": "Luat",
    "nghi_dinh": "Nghi dinh",
    "thong_tu": "Thong tu",
    "quyet_dinh": "Quyet dinh",
    "chi_thi": "Chi thi",
    "van_ban_gop": "Van ban gop / lien van ban",
    "qcvn_tcvn": "QCVN / TCVN",
    "ban_an": "Ban an / An le",
    "khac": "Khac",
}

# Trang thai hieu luc
STATUS = {
    "hieu_luc": "Dang co hieu luc",
    "het_hieu_luc": "Da het hieu luc",
    "chua_hieu_luc": "Chua co hieu luc",
    "khong_xac_dinh": "Khong xac dinh duoc",
    "het_hieu_luc_bo_sung": "Het hieu luc, duoc bo sung / thay the",
}

# So ngay canh bao truoc khi het han
STALE_WARNING_DAYS = 180


# ---------------------------------------------------------------- utilities

def die(msg, code=2):
    sys.stderr.write("[LOI] %s\n" % msg)
    sys.exit(code)


def load_kb(path=KB_PATH):
    if not os.path.exists(path):
        die("Khong tim thay KB: %s\n"
            "Tao file JSON rong: {\"van_ban\": [], \"cap_nhat\": null}" % path)
    with open(path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError as e:
            die("KB khong phai JSON hop le (%s): %s" % (e, path))


def save_kb(kb, path=KB_PATH):
    kb["cap_nhat"] = datetime.now().isoformat(timespec="seconds")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(kb, f, ensure_ascii=False, indent=2)


def parse_date(s):
    if not s:
        return None
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%Y/%m/%d"):
        try:
            return datetime.strptime(s.strip(), fmt).date()
        except ValueError:
            continue
    return None


def strip_diacritics(s):
    """Bo dau tieng Viet de so sanh doc noi (co dau) voi registry (khong dau)."""
    if not s:
        return ""
    import unicodedata
    return "".join(ch for ch in unicodedata.normalize("NFD", s)
                   if unicodedata.category(ch) != "Mn")


def norm(s):
    """Chuan hoa chuoi de so sanh: bo dau, bo ky tu dac biet, lower."""
    if not s:
        return ""
    s = strip_diacritics(s).lower()
    out = []
    for ch in s:
        if ch.isalnum():
            out.append(ch)
        elif ch in " -_/.":
            out.append(" ")
    return " ".join("".join(out).split())


def today():
    return date.today()


def status_of(doc, on_date=None):
    """
    Xac dinh trang thai hieu luc cua 1 van ban tai 1 moc thoi gian.
    Tra ve (trang_thai, ly_do)
    """
    on_date = on_date or today()
    declared = doc.get("trang_thai")

    # Neu van ban tu khai bao het han truoc hon muc ngay thi luon tin
    if declared == "het_hieu_luc":
        return "het_hieu_luc", doc.get("ly_do", "KB khai bao het hieu luc")

    if declared == "chua_hieu_luc":
        # van ban chua ban hanh / chua co hieu luc
        start = parse_date(doc.get("ngay_hieu_luc"))
        if start and on_date < start:
            return "chua_hieu_luc", "Chua toi ngay %s" % start.strftime("%d/%m/%Y")
        # Neu den ngay roi ma KB van chua co ngay hieu luc -> khong xac dinh
        return "khong_xac_dinh", "KB chua cap nhat ngay_hieu_luc"

    if declared == "khong_xac_dinh":
        return "khong_xac_dinh", doc.get("ly_do", "Chua xac minh duoc")

    # Trang thai dang co hieu luc: kiem tra bang ngay
    start = parse_date(doc.get("ngay_hieu_luc"))
    end = parse_date(doc.get("ngay_het_hieu_luc"))

    if start and on_date < start:
        return "chua_hieu_luc", "Hieu luc tu %s" % start.strftime("%d/%m/%Y")

    if end and on_date > end:
        # Kiem tra xem co bi thay the bang van ban khac khong
        replaced_by = doc.get("thay_the_boi")
        if replaced_by:
            return "het_hieu_luc_bo_sung", "Het han %s, thay the boi %s" % (
                end.strftime("%d/%m/%Y"), replaced_by)
        return "het_hieu_luc", "Het han %s" % end.strftime("%d/%m/%Y")

    if not start and not end:
        return "khong_xac_dinh", "KB thieu ngay_hieu_luc va ngay_het_hieu_luc"

    return "hieu_luc", "Trong han"


# ---------------------------------------------------------------- commands

def cmd_check(args):
    kb = load_kb()
    on_date = parse_date(args.date) if args.date else today()

    target = norm(args.doc)
    hits = []
    # Vong 1a — so hieu khớp CHÍNH XÁC (số hiệu sai phải bị chặn)
    exact = [d for d in kb.get("van_ban", []) if norm(d.get("so_hieu", "")) == target]
    if exact:
        hits = exact
    else:
        # Vong 1b — so hieu chua chuan hoa (vd bo khoang trang, tach dau /ND-CP).
        # Chi chap nhan khi mot ben la TIEN TO cua ben kia (cung loai van ban),
        # de tranh khop nham khi chi khac o so hieu: "78/2024/QH15" KHONG duoc
        # khop "98/2024/QH15" (cung nam, cung co quan ban hanh, khac so hieu).
        for doc in kb.get("van_ban", []):
            so_hieu = norm(doc.get("so_hieu", ""))
            if not so_hieu:
                continue
            short, long_ = (target, so_hieu) if len(target) <= len(so_hieu) else (so_hieu, target)
            if len(short) >= 8 and long_.startswith(short) and short != long_:
                hits.append(doc)
    # Vong 2 — ten van ban (chi khi truy van co TỪ KHÓA RIÊNG, khong phai chi
    # nam nien + co quan ban hanh — vi "78/2024/QH15" se khop nham "luat dien
    # luc 2024" neu chi so sanh nam + qh15)
    if not hits:
        words_t = [w for w in target.split()
                   if len(w) > 3 and w not in ("luat", "nghi", "thong", "quyet")
                   and not w.isdigit() and w not in ("qh13", "qh14", "qh15", "ndcp", "cp")]
        # Neu truy van chi la so hieu (khong co tu khoa rieng) thi bo qua vong nay
        for doc in kb.get("van_ban", []):
            ten = norm(doc.get("ten", ""))
            if not ten:
                continue
            if target == ten:
                hits.append(doc)
                continue
            if words_t:
                words_d = ten.split()
                if all(w in words_d for w in words_t):
                    hits.append(doc)

    if not hits:
        sys.stderr.write(
            "[BLOCKING] Khong tim thay van ban '%s' trong KB.\n"
            "  → KHONG duoc doan so hieu. Tra nguon goc roi them vao KB:\n"
            "    python legal_kb.py add --so-hieu \"...\" --ten \"...\" "
            "--ngay-hieu-luc YYYY-MM-DD\n" % args.doc)
        return 1

    worst = None
    for doc in hits:
        st, why = status_of(doc, on_date)
        line = "%-28s %-24s %s" % (
            doc.get("so_hieu", "?"), STATUS.get(st, st), why)
        print(line)
        if worst is None or st in ("het_hieu_luc",):
            worst = st

    print("")
    if worst == "het_hieu_luc":
        sys.stderr.write(
            "[BLOCKING] Van ban tren DA HET HIEU LUC.\n"
            "  → KHONG trich dan vao tu van. Tim van ban thay the truoc.\n")
        return 1
    if worst == "het_hieu_luc_bo_sung":
        sys.stderr.write(
            "[CANH BAO] Van ban da het han nhung duoc thay the.\n"
            "  → Phai trich dan van ban THAY THE, khong trich dan ban cu.\n")
        return 0
    if worst == "khong_xac_dinh":
        sys.stderr.write(
            "[CANH BAO] KB chua xac minh hieu luc van ban nay.\n"
            "  → Verify lai tren nguon chinh thuc truoc khi dua vao tu van.\n")
        return 0
    if worst == "chua_hieu_luc":
        sys.stderr.write(
            "[CANH BAO] Van ban chua co hieu luc tai moc thoi gian nay.\n")
        return 0

    print("[OK] Van ban con hieu luc tai %s." % on_date.strftime("%d/%m/%Y"))
    return 0


def cmd_find(args):
    kb = load_kb()
    q = norm(args.topic)
    if not q:
        die("Thieu --topic")

    keywords = [k for k in q.split() if len(k) > 1]
    if not keywords:
        keywords = [q]

    scored = []
    for doc in kb.get("van_ban", []):
        blob = norm(" ".join([
            doc.get("ten", ""),
            doc.get("so_hieu", ""),
            " ".join(doc.get("chude", []) or []),
            doc.get("tom_tat", ""),
            " ".join(doc.get("pham_vi", []) or []),
        ]))
        if not blob:
            continue
        hits = sum(1 for k in keywords if k in blob)
        if hits == 0 and q not in blob:
            continue
        st, _ = status_of(doc)
        scored.append((hits, st, doc))

    if not scored:
        print("[KHONG TIM THAY] Tu khoa: %r" % args.topic)
        print("Hay bo sung vao KB: python legal_kb.py add --so-hieu ... --ten ... "
              "--chude \"a, b, c\"")
        return 1

    # Sap xep: het hieu luc cuoi, nhieu diem truoc
    order = {"hieu_luc": 0, "chua_hieu_luc": 1, "khong_xac_dinh": 2,
             "het_hieu_luc_bo_sung": 3, "het_hieu_luc": 4}
    scored.sort(key=lambda x: (order.get(x[1], 9), -x[0]))

    print("Tim thay %d van ban (sap xep theo do phu hop + tinh trang):\n" % len(scored))
    for hits, st, doc in scored:
        flag = ""
        if st == "het_hieu_luc":
            flag = "  << HET HIEU LUC"
        elif st == "khong_xac_dinh":
            flag = "  << CHUA XAC MINH"
        elif st == "het_hieu_luc_bo_sung":
            flag = "  << DA THAY THE"
        print("  %-26s %s%s" % (doc.get("so_hieu", "?"), doc.get("ten", "?"), flag))
        if args.verbose:
            print("      %s" % doc.get("tom_tat", "")[:150])
            ph = doc.get("pham_vi")
            if ph:
                print("      Pham vi: %s" % ", ".join(ph[:6]))
            end = parse_date(doc.get("ngay_het_hieu_luc"))
            if end:
                print("      Het han: %s" % end.strftime("%d/%m/%Y"))

    # Neu tat ca deu het han -> canh bao
    if all(s[1] == "het_hieu_luc" for s in scored):
        sys.stderr.write(
            "\n[BLOCKING] Tat ca van ban khop deu da het hieu luc.\n"
            "  → Can ban hanh/thay the truoc khi tu van.\n")
        return 1
    return 0


def cmd_list(args):
    kb = load_kb()
    docs = kb.get("van_ban", [])
    if args.group:
        docs = [d for d in docs if d.get("nhom") == args.group]
    docs = sorted(docs, key=lambda d: (d.get("nhom", ""), d.get("so_hieu", "")))

    print("KB chua %d van ban" % len(docs))
    if kb.get("cap_nhat"):
        print("Cap nhat gan nhat: %s" % kb["cap_nhat"])
    print("")
    for d in docs:
        st, why = status_of(d)
        print("  [%-12s] %-26s %s" % (d.get("nhom", "?"),
                                       d.get("so_hieu", "?"), d.get("ten", "?")))
        if args.verbose:
            print("              %s — %s" % (STATUS.get(st, st), why))
    return 0


def cmd_expired(args):
    kb = load_kb()
    rows = []
    for doc in kb.get("van_ban", []):
        st, why = status_of(doc)
        if st in ("het_hieu_luc", "het_hieu_luc_bo_sung"):
            rows.append((doc.get("ngay_het_hieu_luc") or "", doc, st, why))
    rows.sort()
    if not rows:
        print("Khong co van ban nao het hieu luc.")
        return 0
    print("VAN BAN HET HIEU LUC (%d):\n" % len(rows))
    for _, doc, st, why in rows:
        print("  %-26s %s" % (doc.get("so_hieu", "?"), doc.get("ten", "?")))
        print("      %s" % why)
        if doc.get("thay_the_boi"):
            print("      Thay the boi: %s" % doc["thay_the_boi"])
    return 0


def cmd_stale(args):
    kb = load_kb()
    days = args.days if args.days else STALE_WARNING_DAYS
    cutoff = today() + timedelta(days=days)
    rows = []
    for doc in kb.get("van_ban", []):
        st, _ = status_of(doc)
        if st != "hieu_luc":
            continue
        end = parse_date(doc.get("ngay_het_hieu_luc"))
        if end and end <= cutoff:
            rows.append((end, doc))
    rows.sort()
    if not rows:
        print("Khong co van ban nao het han trong %d ngay toi." % days)
        return 0
    print("VAN BAN SAP HET HAN TRONG %d NGAY (%d):\n" % (days, len(rows)))
    for end, doc in rows:
        left = (end - today()).days
        print("  %-26s het han %s (con %d ngay)" % (
            doc.get("so_hieu", "?"), end.strftime("%d/%m/%Y"), left))
        print("      %s" % doc.get("ten", "?"))
    return 0


def cmd_audit(args):
    """Danh gia do bao pho cua KB. Day la lenh quan trong nhat de bao dam
    chat luong he thong: KB bao pho thap -> moi tu van deu co rui ro."""
    kb = load_kb()
    docs = kb.get("van_ban", [])
    n = len(docs)
    if n == 0:
        print("[LOI] KB rong. Chua co van ban nao.")
        return 1

    counts = {}
    missing_dates = 0
    missing_group = 0
    missing_status = 0
    replaced_only = 0

    for doc in docs:
        st, _ = status_of(doc)
        counts[st] = counts.get(st, 0) + 1
        if not doc.get("ngay_hieu_luc") and not doc.get("trang_thai"):
            missing_dates += 1
        if not doc.get("ngay_het_hieu_luc"):
            replaced_only += 1
        if not doc.get("nhom"):
            missing_group += 1
        if not doc.get("trang_thai"):
            missing_status += 1

    pct = lambda k: (counts.get(k, 0) * 100.0 / n)

    print("=" * 66)
    print("DANH GIA KB PHAP LY — %d van ban" % n)
    print("Cap nhat: %s" % (kb.get("cap_nhat") or "chua co"))
    print("=" * 66)
    print("")
    print("Trang thai hieu luc:")
    print("  Dang co hieu luc      %3d  (%.0f%%)" % (counts.get("hieu_luc", 0), pct("hieu_luc")))
    print("  Het hieu luc          %3d  (%.0f%%)" % (counts.get("het_hieu_luc", 0), pct("het_hieu_luc")))
    print("  Het han, thay the     %3d  (%.0f%%)" % (counts.get("het_hieu_luc_bo_sung", 0), pct("het_hieu_luc_bo_sung")))
    print("  Chua co hieu luc      %3d  (%.0f%%)" % (counts.get("chua_hieu_luc", 0), pct("chua_hieu_luc")))
    print("  Khong xac minh        %3d  (%.0f%%)" % (counts.get("khong_xac_dinh", 0), pct("khong_xac_dinh")))
    print("")
    print("Chuyen mon:")
    print("  Thieu nhom            %3d  (%.0f%%)" % (missing_group, missing_group * 100.0 / n))
    print("  Thieu trang thai      %3d  (%.0f%%)" % (missing_status, missing_status * 100.0 / n))
    print("  Khong ro han (may vo han) %3d  (%.0f%%)" % (replaced_only, replaced_only * 100.0 / n))
    print("")

    # Diem chat luong
    verified = pct("hieu_luc") + pct("khong_xac_dinh") * 0.5
    score = verified * 0.6 + (n - missing_status) / n * 100 * 0.2 + \
        (n - missing_group) / n * 100 * 0.2

    print("DIEM CHAT LUONG KB: %.0f / 100" % score)
    if score >= 80:
        print("  [DAT] Kha dung cho tu van thuong.")
    elif score >= 60:
        print("  [CANH BAO] Dung duoc nhung phai verify them ve hieu luc.")
    else:
        print("  [KHONG DU] Chua du lam nen. Bo sung van ban truoc khi tu van.")
    print("")

    # Goi y hanh dong
    if counts.get("khong_xac_dinh", 0) > 0:
        print("VIEC CAN LAM:")
        print("  - %d van ban chua xac minh hieu luc → verify tren "
              "vbpl.vn / cong bao" % counts["khong_xac_dinh"])
    if missing_group > 0:
        print("  - %d van ban thieu nhom → gan nhom de find hoat dong" % missing_group)
    if n < 50:
        print("  - KB chi co %d van ban. Nen >= 150 de bao pho pho bien "
              "quyet dinh nganh." % n)
    print("")
    return 0 if score >= 60 else 1


def cmd_add(args):
    kb = load_kb()
    if not args.so_hieu or not args.ten:
        die("Can --so-hieu va --ten")

    docs = kb.get("van_ban", [])
    # Cap nhat neu da ton tai
    for d in docs:
        if norm(d.get("so_hieu", "")) == norm(args.so_hieu):
            if args.ngay_hieu_luc:
                d["ngay_hieu_luc"] = args.ngay_hieu_luc
            if args.ngay_het_hieu_luc:
                d["ngay_het_hieu_luc"] = args.ngay_het_hieu_luc
            if args.nhom:
                d["nhom"] = args.nhom
            if args.trang_thai:
                d["trang_thai"] = args.trang_thai
            if args.chude:
                d["chude"] = [c.strip() for c in args.chude.split(",")]
            d["ten"] = args.ten
            save_kb(kb)
            print("[CAP NHAT] %s" % args.so_hieu)
            return 0

    doc = {
        "so_hieu": args.so_hieu,
        "ten": args.ten,
        "nhom": args.nhom or "khac",
        "trang_thai": args.trang_thai or "hieu_luc",
        "ngay_hieu_luc": args.ngay_hieu_luc,
        "ngay_het_hieu_luc": args.ngay_het_hieu_luc,
        "chude": [c.strip() for c in (args.chude or "").split(",") if c.strip()],
        "pham_vi": [c.strip() for c in (args.pham_vi or "").split(",") if c.strip()],
        "tom_tat": args.tom_tat or "",
        "nguon": args.nguon or "",
        "thay_the_boi": args.thay_the_boi or None,
        "ngay_them": today().isoformat(),
    }
    docs.append(doc)
    save_kb(kb)
    print("[DA THEM] %s — %s" % (args.so_hieu, args.ten))
    st, why = status_of(doc)
    print("         Trang thai: %s (%s)" % (STATUS.get(st, st), why))
    return 0


# ---------------------------------------------------------------- main

def main():
    p = argparse.ArgumentParser(
        description="KB phap ly Viet Nam — kiem tra hieu luc van ban (deterministic)")
    sub = p.add_subparsers(dest="cmd")

    c = sub.add_parser("check", help="Kiem tra van ban con hieu luc")
    c.add_argument("--doc", required=True, help="So hieu van ban")
    c.add_argument("--date", help="Ngay kiem tra YYYY-MM-DD (mac dinh: hom nay)")
    c.set_defaults(func=cmd_check)

    f = sub.add_parser("find", help="Tim van ban theo chu de")
    f.add_argument("--topic", required=True, help="Tu khoa")
    f.add_argument("--verbose", action="store_true")
    f.set_defaults(func=cmd_find)

    l = sub.add_parser("list", help="Liet ke van ban")
    l.add_argument("--group")
    l.add_argument("--verbose", action="store_true")
    l.set_defaults(func=cmd_list)

    e = sub.add_parser("expired", help="Van ban het hieu luc")
    e.set_defaults(func=cmd_expired)

    s = sub.add_parser("stale", help="Van ban sap het han")
    s.add_argument("--days", type=int)
    s.set_defaults(func=cmd_stale)

    a = sub.add_parser("audit", help="Danh gia do bao pho cua KB")
    a.set_defaults(func=cmd_audit)

    ad = sub.add_parser("add", help="Them/cap nhat van ban")
    ad.add_argument("--so-hieu", required=True)
    ad.add_argument("--ten", required=True)
    ad.add_argument("--nhom", choices=list(GROUPS.keys()))
    ad.add_argument("--trang-thai",
                    choices=list(STATUS.keys()) + ["hieu_luc"])
    ad.add_argument("--ngay-hieu-luc")
    ad.add_argument("--ngay-het-hieu-luc")
    ad.add_argument("--chude", help="Danh sach chude, ngan cach dau phay")
    ad.add_argument("--pham-vi", help="Danh sach pham vi, ngan cach dau phay")
    ad.add_argument("--tom-tat")
    ad.add_argument("--nguon")
    ad.add_argument("--thay-the-boi")
    ad.set_defaults(func=cmd_add)

    args = p.parse_args()
    if not getattr(args, "func", None):
        p.print_help()
        sys.exit(0)
    sys.exit(args.func(args))


if __name__ == "__main__":
    main()