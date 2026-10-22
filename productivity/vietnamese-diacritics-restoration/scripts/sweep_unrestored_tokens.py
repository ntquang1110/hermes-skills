#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Post-verify QA sweep: find Vietnamese words still left as plain ASCII.

WHY: the strip-identity check (scripts/strip_identity_check.py) only proves you added,
dropped or reordered no BASE LETTERS.  A word you forgot to map, or a wrong reading
(hoc vs học), strips identically and still prints IDENTICAL.  This sweep is the second
pass that catches those.  Run it AFTER the strip check, then re-read the output once.

Usage:
    python sweep_unrestored_tokens.py DIR [stem ...]

    DIR      directory containing <stem>.vn.md restored files
    stem     file stems to check (default: every *.vn.md in DIR)

Exit code 0 always (this is a review aid, not a gate); read the report.
Prefix substrings are false positives -- e.g. `quy` inside `quyết`, `khu` inside `khuỷu`,
`kho` inside `khoảng`, `so` inside `soát`, `thuy` inside `thuyết`, `tu` inside `tuân`.
"""
import io
import os
import re
import sys

# Tokens that must NEVER survive as plain ASCII in restored Vietnamese prose.
SUSPECT = """cac chat khong nhiet phan tien xam xay xu xuc ung vat vay vao voi phap nghien
duoc thanh phuong thuc tinh toc trien trinh tuong tung quy quyet hieu hoat hoc dung dong khu
khuon khuyu nguoi nhieu tam trai tron trieu tru truc truong tuan tuyet uu vuc vuot xac hinh
hon hong hop ich kha khang khao kho khoang khoi kiem kien lam lan lich lieu linh loai loi lon
luc manh mem mon mot muc nam nang nau nen neu nghe nghiep ngoai nguyen nhan nhat nhay nhiem
nhom nhot nhu nhung noi nuoc nuoi phai phat phong phu phuc quoc rao rang rat ren roi sanh sat
soat suat tac tang tao tap than thap thai them thep thien thiet thong thua thuoc thuong thuy
thuyet tich tiep tieu ton tong tot buoc bac banh beo ben bien bot canh cat cau chan chay chinh
chiu chung chuyen cong cuc cum cuoi dac dang dap dau de dich diem dieu doan doc duc duong giam
giay gioi giua gom goc gap gay gan giong ham han hang hao ap dat boi cai hu ket thep trang""".split()

# Legitimately unaccented Vietnamese / identifiers seen in real files -- do NOT flag.
ALLOW = {
    'tinh',    # tinh bột (starch)
    'va',      # va chạm (collision compound)
    'ban',     # ban đầu
    'bi',      # bi nghiền (grinding media)
    'so',      # so sánh
    'trung',   # Trung Quốc / trung tâm / trung gian
    'trong', 'tranh', 'cho', 'nhanh', 'cao', 'gang', 'loang', 'rung', 'lai',
    'quang', 'kim', 'sinh', 'minh', 'tham', 'tang',
}


def sweep_line(line, bad):
    """Return the suspicious bare tokens present on one line."""
    return [w for w in bad
            if re.search(r'(?<![0-9A-Za-z])' + w + r'(?![0-9A-Za-z])', line, re.IGNORECASE)]


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    directory = argv[1]
    stems = argv[2:]
    if not stems:
        stems = sorted(f[:-len('.vn.md')]
                       for f in os.listdir(directory) if f.endswith('.vn.md'))
        if not stems:
            print('no *.vn.md files in', directory)
            return 2

    bad = sorted({w for w in SUSPECT if w not in ALLOW})
    total = 0
    for stem in stems:
        path = os.path.join(directory, stem + '.vn.md')
        if not os.path.exists(path):
            print('!! missing:', path)
            continue
        lines = io.open(path, encoding='utf-8').read().split('\n')
        hits = []
        for i, line in enumerate(lines, 1):
            for w in sweep_line(line, bad):
                hits.append((i, w, line.strip()))
        total += len(hits)
        print('### %s : %d suspicious hit(s)' % (stem, len(hits)))
        for i, w, line in hits:
            print('  L%-4d [%s] %s' % (i, w, line[:140]))
    print('\nTotal suspicious hits: %d' % total)
    print('Review each: prefix substrings (quy in quyết, khu in khuỷu, kho in khoảng,')
    print('so in soát) and the ALLOW set are false positives. Anything else is unrestored.')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
