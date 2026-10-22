#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""check-cut-lines.py — Cổng 3 của lô hoạt chất `docs/12-hoat-chat-mo-rong`.

Kiểm: mỗi `nham_diem_cat` trong batch JSON phải là TRÍCH NGUYÊN VĂN một dòng
điểm cắt có thật trong `00-cua-mo.md` (schema luật 9), và `chang_tac_dong`
phải khớp chặng của chính dòng đó.

Vì sao cần: luật 9 chỉ nói "khớp một dòng có thật", không nói "chép đúng chữ".
Một câu diễn giải lại ("bù nước điện giải" vs "Bù nước và điện giải") vẫn qua
mắt người, rồi trang ráp sau nối vào dòng không tồn tại.

    python check-cut-lines.py                       # tự tìm file quanh nó
    python check-cut-lines.py --batch batch-lo-2-kinh-te-va-tai-thai.json
    python check-cut-lines.py --map 00-cua-mo.md --batch X.json --quiet

Exit 1 = KHÔNG ship.
"""
from __future__ import print_function

import argparse
import json
import os
import re
import sys
import unicodedata

SRC = os.path.dirname(os.path.abspath(__file__))

CUA_HEX = "ABCDE"
CHANG_OK = {
    "1_xam_nhap", "2_qua_hang_rao", "3_bam_cu_tru", "4_nhan_len",
    "5_lan_he_thong", "6_tin_hieu_hai", "7_hau_qua", "8_thai_lay",
}
# dòng điểm cắt: "- **[cao]** `etec` · chặng 7_hau_qua — Bù nước và điện giải"
LINE_RE = re.compile(
    r"- \*\*\[(\w+)\]\*\*\s+`([A-Za-z0-9\-]+)`\s+·\s+(chặng \w+)\s+—\s+(.+)$"
)
# `nham_diem_cat` trong batch JSON KHÔNG đồng nhất giữa các lô — phải parse cả hai:
#   lô 2: "`etec` · chặng 7_hau_qua — Bù nước và điện giải"          (khoá trước)
#   lô 3: "Bù nước và điện giải (`etec` · chặng 7_hau_qua) — lý do"  (câu trước, khoá sau)
# Chỉ nhận một dạng ⇒ checker im lặng FAIL cả lô 3 dù dữ liệu đúng.
CUT_RE_A = re.compile(r"^`?([A-Za-z0-9\-]+)`?\s+·\s+(chặng \w+)\s+—\s+(.+)$")
CUT_RE_B = re.compile(
    r"^(.+?)\s*\(\s*`?([A-Za-z0-9\-]+)`?\s+·\s+(chặng \w+)\s*\)\s*(?:—.*)?$"
)


def parse_cut(s):
    """-> (mam, chang, text) hoặc None. Nhận cả hai thứ tự khoá/câu của lô 2 và lô 3."""
    s = (s or "").strip()
    m = CUT_RE_A.match(s)
    if m:
        return m.group(1), m.group(2), m.group(3).strip()
    m = CUT_RE_B.match(s)
    if m:
        return m.group(2), m.group(3), m.group(1).strip()
    return None


def norm(s):
    """So khớp chịu được khác biệt khoảng trắng / NBSP / NFKC / gạch nối / hoa-thường.

    NFKC chứ không NFC: bản đồ và batch JSON có thể lệch nhau ở ký tự tương thích.
    Gộp cả ba loại gạch (em —, en –, minus −) vì chúng trông giống nhau nhưng khác
    codepoint — lô 3 gặp đúng ca này và một checker không gộp sẽ báo FAIL oan.
    """
    s = unicodedata.normalize("NFKC", s or "")
    s = s.replace("\xa0", " ")
    for d in ("\u2014", "\u2013", "\u2212"):
        s = s.replace(d, "-")
    return re.sub(r"\s+", " ", s).strip().lower()


def load_map(path):
    # 00-cua-mo.md là UTF-8 + CRLF; read_file có thể báo is_binary -> đọc thẳng bytes.
    raw = open(path, "rb").read().decode("utf-8").replace("\r", "")
    lines = []
    for ln in raw.split("\n"):
        m = LINE_RE.search(ln)
        if m:
            lines.append({
                "muc": m.group(1),
                "mam": m.group(2),
                "chang": m.group(3),
                "text": m.group(4).strip(),
            })
    return lines


def find_one(pattern):
    for base in (SRC, os.path.join(SRC, ".."), os.path.join(SRC, "..", "..")):
        base = os.path.abspath(base)
        if not os.path.isdir(base):
            continue
        for f in sorted(os.listdir(base)):
            if re.search(pattern, f):
                return os.path.join(base, f)
    return None


def substances(doc):
    if isinstance(doc, list):
        return doc
    for key in ("hoat_chat", "chat", "chats", "batch", "data", "items"):
        v = doc.get(key)
        if isinstance(v, list):
            return v
    return []


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--map", default=None, help="00-cua-mo.md")
    ap.add_argument("--batch", default=None, help="batch-*.json")
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args()

    mpath = a.map or find_one(r"^00-cua-mo\.md$")
    bpath = a.batch or find_one(r"^batch-.*\.json$")
    if not mpath or not os.path.exists(mpath):
        print("KHÔNG TÌM THẤY 00-cua-mo.md — truyền --map", file=sys.stderr)
        return 2
    if not bpath or not os.path.exists(bpath):
        print("KHÔNG TÌM THẤY batch-*.json — truyền --batch", file=sys.stderr)
        return 2

    lines = load_map(mpath)
    if not lines:
        print("!! Parse 0 dòng điểm cắt — regex LINE_RE không khớp format file bản đồ.",
              file=sys.stderr)
        return 2

    doc = json.load(open(bpath, encoding="utf-8"))
    subs = substances(doc)
    if not subs:
        print("!! Không tìm thấy mảng hoạt chất trong %s" % os.path.basename(bpath),
              file=sys.stderr)
        return 2

    if not a.quiet:
        print("bản đồ : %s  (%d dòng điểm cắt)" % (os.path.basename(mpath), len(lines)))
        print("batch  : %s  (%d hoạt chất)\n" % (os.path.basename(bpath), len(subs)))

    bad, used, mams = [], set(), {}
    for h in subs:
        hid = h.get("id") or h.get("ten") or "?"
        cut = (h.get("nham_diem_cat") or "").strip()
        p = parse_cut(cut)
        if not p:
            bad.append("%s: nham_diem_cat KHÔNG parse được -> %r" % (hid, cut))
            continue
        mam, chang, text = p
        if mam not in mams:
            mams[mam] = 0
        mams[mam] += 1

        cands = [l for l in lines if l["mam"] == mam and l["chang"] == chang]
        hits = [l for l in cands if norm(l["text"]) == norm(text)]
        if not hits:
            bad.append(
                "%s: KHÔNG khớp dòng thật  [%s/%s]\n    trích : %s\n    có thật: %s"
                % (hid, mam, chang, text,
                   " | ".join(l["text"] for l in cands) or "(mầm+chặng này không có dòng nào)")
            )
            continue
        used.add((mam, chang, norm(text)))

        # chang_tac_dong phải chứa chặng của dòng cắt
        ch = chang.replace("chặng ", "")
        if ch not in (h.get("chang_tac_dong") or []):
            bad.append("%s: chang_tac_dong=%r không chứa %r"
                       % (hid, h.get("chang_tac_dong"), ch))

        # cua khai báo phải khớp vùng của dòng (suy từ chặng)
        cua = set(h.get("cua") or [])
        if cua and not cua <= set(CUA_HEX):
            bad.append("%s: cua=%r ngoài A–E" % (hid, h.get("cua")))

    for b in bad:
        print("FAIL " + b)

    print("\n%d/%d hoạt chất khớp nguyên văn · %d/%d dòng điểm cắt được dùng"
          % (len(subs) - len([b for b in bad if "KHÔNG" in b]), len(subs), len(used), len(lines)))
    print("phân bố theo mầm: " + " · ".join(
        "%s×%d" % (k, v) for k, v in sorted(mams.items(), key=lambda kv: -kv[1])))
    if bad:
        print("\n=> KHÔNG SHIP (exit 1)")
        return 1
    print("=> PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
