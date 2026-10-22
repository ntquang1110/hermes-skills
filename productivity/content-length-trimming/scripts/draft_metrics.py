#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Draft quality + length metrics for long-form Vietnamese posts.

Usage:
    python draft_metrics.py PATH [LO] [HI]

Prints:
  CHARS / ACC          total char count and Vietnamese accent-character count
  EMDASH/ENDASH/ARROW  forbidden punctuation counts (must be 0)
  CJK                  any CJK codepoints (must be none)
  TOI                  count of the standalone Vietnamese pronoun "toi/Toi" WITH diacritics
                       (narrator voice must be "minh"; "toi" only inside verbatim quotes)
  PARTS / MAX          how many <=CHUNK-char messages the draft splits into for Telegram,
                       and the longest part (must be <= CHUNK)
  OVER500              parts that exceed CHUNK

Exit 1 if length is outside [LO, HI], forbidden punctuation/CJK present, or a part overflows.
CHUNK defaults to 500; override with env CHUNK.
"""
import os
import re
import sys

CHUNK = int(os.environ.get("CHUNK", "500"))

ACCENTS = (
    "àáảãạâầấẩẫậăằắẳẵặèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợ"
    "ùúủũụưừứửữựỳýỷỹỵđ"
)


def parts_of(text, limit=CHUNK):
    """Split into <=limit-char messages on blank-line paragraph boundaries."""
    out, cur = [], ""
    for para in [p for p in text.split("\n\n") if p.strip()]:
        block = (cur + "\n\n" + para) if cur else para
        if len(block) <= limit:
            cur = block
            continue
        if cur:
            out.append(cur)
        while len(para) > limit:          # a single oversized paragraph
            cut = para.rfind(" ", 0, limit)
            cut = cut if cut > 0 else limit
            out.append(para[:cut])
            para = para[cut:].lstrip()
        cur = para
    if cur:
        out.append(cur)
    return out


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    path = sys.argv[1]
    lo = int(sys.argv[2]) if len(sys.argv) > 2 else None
    hi = int(sys.argv[3]) if len(sys.argv) > 3 else None

    with open(path, encoding="utf-8") as fh:
        t = fh.read()

    n = len(t)
    acc = sum(1 for c in t if c in ACCENTS)
    em, en, arrow = t.count("\u2014"), t.count("\u2013"), t.count("\u2192")
    cjk = re.findall(r"[\u3000-\u9fff\uff00-\uffef]", t)
    toi = len(re.findall(r"\b(?:tôi|Tôi)\b", t))
    ps = parts_of(t)
    over = [p for p in ps if len(p) > CHUNK]

    print(f"CHARS: {n} | ACC: {acc}")
    print(f"EMDASH: {em} | ENDASH: {en} | ARROW: {arrow}")
    print(f"CJK: {len(cjk)}")
    print(f"TOI: {toi}")
    print(f"PARTS: {len(ps)} | MAX: {max((len(p) for p in ps), default=0)} | OVER{CHUNK}: {len(over)}")

    bad = False
    if lo is not None and n < lo:
        print(f"FAIL: {n} < {lo}")
        bad = True
    if hi is not None and n > hi:
        print(f"FAIL: {n} > {hi}")
        bad = True
    if em or en or arrow or cjk or over:
        print("FAIL: forbidden punctuation / CJK / oversized part")
        bad = True
    print("VERDICT:", "FAIL" if bad else "PASS")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
