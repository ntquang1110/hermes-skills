#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
legal_qa_gate.py — QA Gate cho bo Bat ky output phap ly Viet Nam.

Pha 7 cua pipeline legal-firm-vn. KHONG publish output khi chua chay gate nay.

Vai tro: chan truoc nhung loi lam output khong dung:
  - trich dan thieu so hieu / dieu / khoan
  - trich dan van ban da het hieu luc
  - tu doan ("theo quy dinh phap luat") ma khong kem can cu
  - bia so vu an
  - tu phan bien bi bo qua
  - phan loai gap sai (nhac GAP-4)
  - khai bao "khong vi pham" / "an toan" tuyet doi

Exit codes
----------
0  PASS (co the kem warning)
1  FAIL — BLOCKING, phai sua
2  Loi cu phap / input sai
"""

import json
import os
import re
import sys
import argparse
from datetime import date, datetime

KB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "legal_registry.json")

# ---------------------------------------------------------------- patterns

# Trich dan day du: so hieu + Dieu/Khoan
# Vi du: Dieu 351 Bo luat Dan su 2015 | Điều 301 Luật Thương mại 2005 | khoản 3 Điều 12 NĐ 15/2018/NĐ-CP
P_CITE_FULL = re.compile(
    r"(?:Điều|Dieu|khoản)\s*\d+[^.\n]{0,80}?"
    r"(?:\d{2,4}/(?:QH\d+|NĐ-CP|ND-CP|TT-[A-Z]+)|Luật\s+\w+|Luat\s+\w+|Nghị định|Nghi dinh|Bộ luật|Bo luat)",
    re.IGNORECASE)

# So hieu van ban co the trich dan
P_DOCNO = re.compile(
    r"\b\d{1,3}/\d{4}/(?:QH\d+|NĐ-CP|ND-CP|TT-[A-Z]{2,20}|QĐ-TTg|QD-TTg)\b"
    r"|\bQCVN\s*\d+[:\-\d/]*[A-Z]*"
    r"|\b\d+[-/]MT:\d{4}\b"
    r"|\bLuật\s+[A-ZĐ][\w\s]{2,40}?(\s+(?:19|20)\d{2})\b"
    r"|\bNgị định\s+\d+/\d{4}/NĐ-CP\b",
    re.IGNORECASE)

# Mau cau cam ket tuyet doi — nguy hiem
P_ABSOLUTE_CLAIM = re.compile(
    r"(?:không bao giờ vi phạm|khong bao gio vi pham|chắc chắn không vi phạm|"
    r"chac chan khong vi pham|đảm bảo không vi phạm|dam bao khong vi pham|"
    r"hoàn toàn hợp pháp|hoan toan hop phap|chắc chắn là hợp pháp|"
    r"chac chan la hop phap|100% hợp pháp|100% hop phap|"
    r"tuyệt đối an toàn pháp lý|tuyet doi an toan phap ly)",
    re.IGNORECASE)

# Phai co can cu — "theo quy dinh phap luat" khong kem so hieu
P_VAGUE_LEGAL = re.compile(
    r"(?:theo quy định pháp luật|theo quy dinh phap luat|"
    r"theo pháp luật quy định|theo phap luat quy dinh|"
    r"theo luật|theo quy chuẩn áp dụng)",
    re.IGNORECASE)

# Tu phan bien — bat buoc co trong output phap ly
P_SELF_CRITIQUE = re.compile(
    r"(?:phản biện|phan bien|tự phản biện|tu phan bien|"
    r"rủi ro của chính lập luận|rui ro cua chinh lap luan|"
    r"xem ngược lại|xem nguoc lai|"
    r"nếu bên kia không chịu|neu ben kia khong chiu|"
    r"trường hợp đối phương phản biện|truong hop doi phuong phan bien|"
    r"điểm yếu của lập luận|diem yeu cua lap luan)",
    re.IGNORECASE)

# So vu an — phai co so vu hoac ghi ro "khong tim thay"
P_CASE_NO = re.compile(
    r"(?:vụ án|vu an|bản án|ban án|án lệ|an le|hồ sơ vụ án)"
    r"[^\n]{0,40}?(?:số|so|No\.?|#)\s*(\d+)",
    re.IGNORECASE)

# Phan loai GAP — phai co khai bao loai
P_GAP_CLASS = re.compile(
    r"(?:GAP-1|GAP-2|GAP-3|GAP-4|Khoảng trống luật|Khoang trong luat|"
    r"chưa có hướng dẫn|chua co huong dan|thiếu quy chuẩn|thieu quy chuan|"
    r"đại lý hiểu sai|dai ly hieu sai)",
    re.IGNORECASE)

# Loai 4 — phai canh bao manh, khong duoc bo qua
P_GAP4 = re.compile(
    r"(?:đại lý hiểu sai|dai ly hieu sai|thực tế áp dụng|thuc te ap dung|"
    r"cần luật sư người|can luat su nguoi|không tự kết luận|khong tu ket luan)",
    re.IGNORECASE)


def strip_diacritics(s):
    """Bo dau tieng Viet, chuan hoa ve ASCII de so sanh doc noi,
    doc registry (registry luu ten khong dau)."""
    if not s:
        return ""
    import unicodedata
    out = []
    for ch in unicodedata.normalize("NFD", s):
        if unicodedata.category(ch) != "Mn":  # bo dau (combining marks)
            out.append(ch)
    return "".join(out)


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


def load_kb(path=KB_PATH):
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return None


def parse_date(s):
    if not s:
        return None
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%Y/%m/%d"):
        try:
            return datetime.strptime(s.strip(), fmt).date()
        except ValueError:
            continue
    return None


def _resolve_status(doc, on_date):
    """Xac dinh trang thai hieu luc cua 1 doc trong KB."""
    declared = doc.get("trang_thai")
    ten = doc.get("ten", "")
    if declared == "het_hieu_luc":
        return ("het_hieu_luc", ten)
    if declared == "khong_xac_dinh":
        return ("khong_xac_dinh", ten)
    end = parse_date(doc.get("ngay_het_hieu_luc"))
    start = parse_date(doc.get("ngay_hieu_luc"))
    if start and on_date < start:
        return ("chua_hieu_luc", ten)
    if end and on_date > end:
        if doc.get("thay_the_boi"):
            return ("het_hieu_luc_bo_sung", ten)
        return ("het_hieu_luc", ten)
    if not start and not end:
        return ("khong_xac_dinh", ten)
    return ("hieu_luc", ten)


def kb_status_for_docno(docno, kb, on_date):
    """
    Tra ve (trang_thai, ten) cho van ban.
    Match theo so hieu truoc, sau do moi den TEN (tranh false positive khi
    trich dan bang ten thay vi so hieu, vd "Luat An toan thuc pham 2024").
    """
    if not kb:
        return ("khong_xac_dinh", "")
    docs = kb.get("van_ban", [])
    target = norm(docno)

    # Vong 1 — so hieu: KHOP CHIN XAC truoc, substring chi khi du dai
    for doc in docs:
        so = norm(doc.get("so_hieu", ""))
        if not so:
            continue
        if target == so:
            return _resolve_status(doc, on_date)
    for doc in docs:
        so = norm(doc.get("so_hieu", ""))
        if not so:
            continue
        short, long_ = (target, so) if len(target) <= len(so) else (so, target)
        if len(short) >= 8 and long_.startswith(short) and short != long_:
            return _resolve_status(doc, on_date)

    # Vong 2 — ten van ban: chi khi truy van co TU KHOA RIENG (khong phai chi
    # nam + co quan ban hanh — tranh "78/2024/QH15" khop "luat dien luc 2024")
    ten_target = norm(docno)
    words_t = [w for w in ten_target.split()
               if len(w) > 3 and w != "luat" and not w.isdigit()
               and w not in ("qh13", "qh14", "qh15", "ndcp", "cp")]
    for doc in docs:
        ten = norm(doc.get("ten", ""))
        if not ten:
            continue
        if ten_target == ten:
            return _resolve_status(doc, on_date)
        if words_t:
            words_d = ten.split()
            if all(w in words_d for w in words_t):
                return _resolve_status(doc, on_date)

    return ("khong_trong_kb", "")


# ---------------------------------------------------------------- rules

class Finding:
    def __init__(self, rule, level, msg, hint=""):
        self.rule = rule
        self.level = level        # BLOCK | WARN
        self.msg = msg
        self.hint = hint


def run_rules(text, kb, on_date, mode, cho_phep_luat_kiem_hieu_luc=False):
    f = []
    lines = text.splitlines()
    body = text

    # R0 — file qua nhe
    if len(body.strip()) < 200:
        f.append(Finding("R0", "BLOCK",
                         "Output qua ngan (thi thieu %d ky tu). Khong the kiem chung." % len(body.strip()),
                         "Phai la bao cao day du, khong phai ghi chu ngan."))

    # R1 — trich dan day du (chi ap dung khi co trich dan luat)
    cites = P_CITE_FULL.findall(body)
    docnos = P_DOCNO.findall(body)
    has_legal_content = bool(cites) or bool(docnos) or ("luật" in body.lower() or "pháp lý" in body.lower())

    if has_legal_content:
        # Khong trich dan gi
        if not docnos:
            f.append(Finding("R1", "BLOCK",
                             "Khong tim thay so hieu van ban nao duoc trich dan.",
                             "Moi luat phai trich so hieu: NĐ 15/2018/NĐ-CP, Luật ATTP 2024, TT 13/2020/..."))
        # Có "theo quy định pháp luật" mà không kèm số hiệu gần đó
        for i, ln in enumerate(lines, 1):
            if P_VAGUE_LEGAL.search(ln):
                window = " ".join(lines[max(0, i - 2): i + 2])
                if not P_DOCNO.search(window):
                    f.append(Finding("R2", "WARN",
                                     "Dong %d: 'theo quy dinh phap luat' ma khong kem so hieu." % i,
                                     "Ghi ro: theo khoan X Dieu Y Luật Z so A/B/..."))

    # R3 — van ban da het hieu luc ma van trich dan
    for m in P_DOCNO.finditer(body):
        docno = m.group(0).strip()
        st, ten = kb_status_for_docno(docno, kb, on_date)
        if st == "het_hieu_luc":
            if cho_phep_luat_kiem_hieu_luc:
                # Su kien xay ra TRUOC khi luat het hieu luc: trich dan VAN DUNG.
                # VD: giao dich nam 2005 chieu Luot Dat dai 2003 (het hieu luc 2014).
                pass  # khong bao loi
            else:
                f.append(Finding("R3", "BLOCK",
                                 "Van ban '%s' (%s) DA HET HIEU LUC nhung van duoc trich dan." % (docno, ten),
                                 "Tim van ban thay the hoac hieu trich dan. Neu su kien xay ra TRUOC khi luat het hieu luc, dung co so phap luyen dich ra va chay voi co -cho-phep-luat-kiem-hieu-luc"))
        elif st == "het_hieu_luc_bo_sung":
            f.append(Finding("R3", "WARN",
                             "Van ban '%s' (%s) da het han, duoc thay the — phai trich ban thay the."
                             % (docno, ten),
                             "Doi sang van ban moi trong KB."))
        elif st == "khong_trong_kb":
            f.append(Finding("R4", "WARN",
                             "Van ban '%s' khong co trong KB — chua verify hieu luc." % docno,
                             "Tra nguon goc roi: python legal_kb.py add --so-hieu \"%s\" ..." % docno))

    # R5 — cam ket tuyet doi
    for m in P_ABSOLUTE_CLAIM.finditer(body):
        f.append(Finding("R5", "BLOCK",
                         "Cam ket tuyet doi: '%s'." % m.group(0),
                         "Khong the bao dam phap ly tuyet doi. Doi bang: 'chua thay quy dinh nao ap dung, da check [danh sach]'."))

    # R6 — tu phan bien (bat buoc trong mode phap ly)
    if mode in ("phap_ly", "case", "advisory", "critique") and len(body) > 400:
        if not P_SELF_CRITIQUE.search(body):
            f.append(Finding("R6", "BLOCK",
                             "Thieu tu phan bien. Output phap ly phai co phan 'ne neu doi phuong phan bien'.",
                             "Them: 'Rui ro cua chinh lap luan: ...' hoac 'Neu ben kia khong chiu sua thi ...'."))

    # R7 — bia so vu an: so vu khong co trong KB -> warning manh
    if mode in ("case", "critique"):
        cases = P_CASE_NO.findall(body)
        for cno in cases:
            f.append(Finding("R7", "WARN",
                             "So vu an '%s' — phai verify la chinh xac, khong tin vao tri nho." % cno,
                             "Tra CSDL toa an (anle.toaan.gov.vn) hoac ghi 'chua tim thay an le tuong tu'."))

    # R8 — phan loai gap: neu co noi den loai 4 phai canh bao
    if P_GAP_CLASS.search(body):
        if ("đại lý hiểu sai" in body.lower() or "dai ly hieu sai" in body.lower()) \
                and not P_GAP4.search(body):
            f.append(Finding("R8", "BLOCK",
                             "Nho GAP-4 (dai ly hieu sai) ma khong co canh bao.",
                             "Phai them: 'CAN LUAT SU NGUOI XAC NHAN — khong tu ket luan'."))
    # Nếu nói về khai thác lo hổng mà không canh báo loại 4
    if re.search(r"(?:khai thác|khai thac|lo hong|lo hổng|hở|hem)", body, re.IGNORECASE) \
            and re.search(r"(?:luat|phap ly|quy dinh)", body, re.IGNORECASE):
        if not P_GAP4.search(body):
            f.append(Finding("R8", "WARN",
                             "Noi ve khai thac lo hong luat nhung khong co canh bao GAP-4.",
                             "Phan loai 4 loai gap. Loai 4 (dai ly hieu sai) = nguy hiem, can nguoi."))

    return f


# ---------------------------------------------------------------- main

def main():
    p = argparse.ArgumentParser(
        description="QA Gate — chan output phap ly loi, thieu can cu, trich van ban het han")
    p.add_argument("--file", help="File output can kiem (.md / .txt / .html)")
    p.add_argument("--text", help="Noi dung truc tiep (dung khi khong co file)")
    p.add_argument("--mode", default="phap_ly",
                   choices=["phap_ly", "contract", "case", "advisory", "critique"],
                   help="Loai output. contract/case/advisory/critique yeu cau tu phan bien.")
    p.add_argument("--date", help="Ngay kiem tra YYYY-MM-DD")
    p.add_argument("--warn-only", action="store_true",
                   help="Khong exit 1 du co BLOCK (chi de xem)")
    p.add_argument("--cho-phep-luat-kiem-hieu-luc",
                   dest="cho_phep_luat_kiem_hieu_luc", action="store_true",
                   help=("Cho phep trich dan van ban DA HET HIEU LUC khi su kien xay ra "
                         "TRUOC ngay luat het hieu luc. VD: giao dich nam 2005 chieu Luot "
                         "Dat dai 2003 (het hieu luc 01/07/2014). CHI dung khi van ban "
                         "dich da ghi ro ly do trich dan - luật la van ban co hieu luc "
                         "tai thoi diem su kien."))
    args = p.parse_args()

    if args.file:
        if not os.path.exists(args.file):
            sys.stderr.write("[LOI] Khong tim thay file: %s\n" % args.file)
            sys.exit(2)
        with open(args.file, "r", encoding="utf-8", errors="replace") as f:
            text = f.read()
        source = args.file
    elif args.text:
        text = args.text
        source = "(stdin)"
    else:
        sys.stderr.write("[LOI] Can --file hoac --text\n")
        sys.exit(2)

    on_date = parse_date(args.date) if args.date else date.today()
    kb = load_kb()

    findings = run_rules(text, kb, on_date, args.mode,
                          args.cho_phep_luat_kiem_hieu_luc)

    blocks = [x for x in findings if x.level == "BLOCK"]
    warns = [x for x in findings if x.level == "WARN"]

    print("=" * 70)
    print("QA GATE PHAP LY — %s" % source)
    print("Mode: %-10s  Ngay: %s" % (args.mode, on_date.strftime("%d/%m/%Y")))
    print("=" * 70)

    if not findings:
        print("")
        print("[PASS] Khong phat hien van de. Output du dieu kien publish.")
        print("")
        return 0

    if blocks:
        print("")
        print("BLOCKING (%d) — BAT BUOC SUA:" % len(blocks))
        for i, x in enumerate(blocks, 1):
            print("  %d. [%s] %s" % (i, x.rule, x.msg))
            if x.hint:
                print("      → %s" % x.hint)

    if warns:
        print("")
        print("WARNING (%d) — nen xem lai:" % len(warns))
        for i, x in enumerate(warns, 1):
            print("  %d. [%s] %s" % (i, x.rule, x.msg))
            if x.hint:
                print("      → %s" % x.hint)

    print("")
    if blocks:
        print("KET QUA: FAIL — %d blocking. KHONG publish." % len(blocks))
        print("")
        return 0 if args.warn_only else 1

    print("KET QUA: PASS (co %d warning)" % len(warns))
    print("")
    return 0


if __name__ == "__main__":
    sys.exit(main())