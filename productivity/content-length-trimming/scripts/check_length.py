#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify a trimmed text file stays inside a target char-count window.

Usage:
    python check_length.py PATH [LO] [HI]

Prints total len(), em-dash/en-dash counts, and per-paragraph lengths.
If LO/HI given, exits 1 (with a message) when len() is outside [LO, HI].
len() is Python character count, NOT byte count — the right unit for
multi-byte text (Vietnamese, accents, CJK).
"""
import sys

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    path = sys.argv[1]
    lo = int(sys.argv[2]) if len(sys.argv) > 2 else None
    hi = int(sys.argv[3]) if len(sys.argv) > 3 else None

    with open(path, encoding="utf-8") as fh:
        s = fh.read()

    n = len(s)
    em = s.count("\u2014")
    en = s.count("\u2013")
    print(f"len={n}  em_dash={em}  en_dash={en}")

    paras = [p for p in s.split("\n") if p.strip()]
    for i, p in enumerate(paras, 1):
        print(f"  para {i}: {len(p)}")

    ok = True
    if lo is not None and n < lo:
        print(f"FAIL: len {n} < LO {lo}")
        ok = False
    if hi is not None and n > hi:
        print(f"FAIL: len {n} > HI {hi}")
        ok = False
    if em or en:
        print("FAIL: found em/en dashes")
        ok = False
    if not ok:
        sys.exit(1)

if __name__ == "__main__":
    main()