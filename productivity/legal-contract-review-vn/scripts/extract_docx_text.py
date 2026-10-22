#!/usr/bin/env python3
"""Trích xuất text từ .docx — an toàn với ObservationPack.

VÌ SAO CẦN SCRIPT NÀY:
  - `read_file` trên .docx >500 ký tự bị Hermes ObservationPack archive: chỉ trả về
    handle + excerpt, KHÔNG có nội dung. File observation .json là binary nén,
    `read_file` báo "Binary file - cannot display as text".
  - Đọc "theo trí nhớ" về file rồi review = bịa điều khoản. Luôn trích xuất tường minh.

DÙNG:
  python extract_docx_text.py <file.docx> [--marks] [--out out.txt]

  --marks : in thêm các đoạn được bôi màu / tô màu chữ (để review theo vùng đánh dấu).
            Ghi chú: "bôi xanh" trong Word thường là w:color 0000FF (màu CHỮ),
            không phải w:highlight — phải scan cả hai.
"""
import sys
import html
import re
import zipfile
import xml.etree.ElementTree as ET

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def _para_text(p):
    """Ghép toàn bộ w:t trong một paragraph, giữ w:tab và w:br."""
    parts = []
    for node in p.iter():
        tag = node.tag
        if tag == W + "t":
            parts.append(node.text or "")
        elif tag == W + "tab":
            parts.append("\t")
        elif tag == W + "br":
            parts.append("\n")
    return "".join(parts)


def extract(path):
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        if "word/document.xml" not in names:
            raise SystemExit("Không phải .docx hợp lệ (thiếu word/document.xml): %s" % path)
        root = ET.fromstring(z.read("word/document.xml"))
    out = []
    # bảng: lấy cả ô, đánh dấu bằng tab để giữ cấu trúc cột
    for para in root.iter(W + "p"):
        t = _para_text(para).strip()
        if t:
            out.append(t)
    return "\n".join(out)


def _marks(rpr):
    got = set()
    if rpr is None:
        return got
    hl = rpr.find(W + "highlight")
    if hl is not None:
        got.add("HL:" + (hl.get(W + "val") or "?"))
    col = rpr.find(W + "color")
    if col is not None:
        v = (col.get(W + "val") or "").upper()
        if v and v not in ("AUTO", "000000"):
            got.add("COL:" + v)
    return got


def marked_paragraphs(path):
    with zipfile.ZipFile(path) as z:
        root = ET.fromstring(z.read("word/document.xml"))
    rows = []
    for para in root.iter(W + "p"):
        runs = []
        for r in para.iter(W + "r"):
            txt = "".join(t.text or "" for t in r.iter(W + "t"))
            runs.append((txt, _marks(r.find(W + "rPr"))))
        full = "".join(t for t, _ in runs)
        if not full.strip():
            continue
        m = set()
        for _, mk in runs:
            m |= mk
        if m:
            rows.append("[%s] %s" % (" ".join(sorted(m)), full.strip()))
    return "\n".join(rows)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        raise SystemExit(__doc__)
    path = args[0]
    want_marks = "--marks" in sys.argv
    text = extract(path)
    if want_marks:
        mp = marked_paragraphs(path)
        text += "\n\n===== ĐOẠN CÓ ĐÁNH DẤU MÀU =====\n" + (mp or "(không có)")
    if "--out" in sys.argv:
        dest = sys.argv[sys.argv.index("--out") + 1]
        with open(dest, "w", encoding="utf-8") as f:
            f.write(text)
        print("Đã ghi %d ký tự -> %s" % (len(text), dest))
    else:
        sys.stdout.reconfigure(encoding="utf-8")
        print(text)


if __name__ == "__main__":
    main()
