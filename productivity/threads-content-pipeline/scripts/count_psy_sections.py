#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Đo ngân sách bài psy: số từ TỪNG phần (bài 5 đoạn) + ký tự TỪNG post (bản thread).

Dùng TRƯỚC khi trim, để cắt đúng phần đang vượt thay vì đoán rồi trim mù
(mỗi lượt trim mù tốn 1 write_file + 1 verify_psy_thread.py).

Ngưỡng: bài KFlow <= 450 từ, mỗi post thread <= 500 ký tự, tổng thread <= 1500.
Ngân sách an toàn đã dùng đạt PASS (psy_3 2026-10-20): Ví dụ ~85, Nêu vấn đề ~70,
Vấn đề gốc rễ ~85, First principle ~100, Giải pháp ~105.

Dùng:
    python count_psy_sections.py "<draft psy_N.txt>" ["<threads psy_N_thread.txt>"]

READ-ONLY. Exit 0 luôn (chỉ đo, không phán PASS/FAIL — việc đó là của verify_psy_thread.py).
"""
import io
import sys

LIMIT_DRAFT = 450
LIMIT_POST = 500
LIMIT_THREAD = 1500


def read(path):
    with io.open(path, encoding="utf-8") as f:
        return f.read()


def sections(path):
    t = read(path)
    total = len(t.split())
    print("DRAFT %s" % path)
    for b in t.split("\n\n"):
        b = b.strip()
        if not b:
            continue
        label = b.split("\n")[0].strip()
        print("  %-18s %4d từ" % (label, len(b.split())))
    print("  %-18s %4d từ | ngân sách %d | còn %d"
          % ("TOTAL", total, LIMIT_DRAFT, LIMIT_DRAFT - total))


def posts(path):
    t = read(path)
    parts = [p for p in t.split("\n\n") if p.strip()]
    print("THREAD %s" % path)
    for i, p in enumerate(parts, 1):
        flag = "  <-- VƯỢT" if len(p) > LIMIT_POST else ""
        print("  post %d: %4d ký tự%s" % (i, len(p), flag))
    print("  tổng %d ký tự (trần %d) | %d post"
          % (len(t), LIMIT_THREAD, len(parts)))


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 0
    sections(argv[1])
    if len(argv) > 2:
        posts(argv[2])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
