#!/usr/bin/env python
"""Fat report: show WHERE the overweight is, so a draft gets trimmed in ONE pass.

Why (2026-10-19): a 9.0K draft was walked down to 6.999K with SEVEN successive
small `patch` calls (7.72 -> 7.34 -> 7.27 -> 7.10 -> 7.07 -> 7.02 -> 7.00), each
one blind. Measure first, then cut the two or three fattest paragraphs once.

Usage:
  python draft_fat_report.py "C:/Users/NTQUANG_DELL/hermes-temp/draft_x.txt"
  python draft_fat_report.py "<draft>" --target 7000 --max-part 500

Notes it prints for you:
  - total chars, delta to target (default 7000 = hard ceiling for a Threads draft)
  - every paragraph sorted fattest-first with a preview
  - paragraphs over --max-part (poster will split those across several replies)
  - TRIM PLAN: the smallest set of fattest paragraphs that clears the overage

Exit 0 always (report only, read-only).
"""
import argparse
import sys

ACCENTS = (
    "àáảãạâầấẩẫậăằắẳẵặèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợ"
    "ùúủũụưừứửữựỳýỷỹỵđ"
)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("draft")
    ap.add_argument("--target", type=int, default=7000,
                    help="hard char ceiling (default 7000 for a YouTube draft)")
    ap.add_argument("--max-part", type=int, default=500,
                    help="max chars per Threads post (default 500)")
    ap.add_argument("--top", type=int, default=12, help="how many paragraphs to list")
    a = ap.parse_args()

    t = open(a.draft, encoding="utf-8").read()
    paras = [p.strip() for p in t.split("\n") if p.strip()]
    total = len(t)
    need = max(0, total - a.target)
    n_acc = sum(1 for ch in t if ch in ACCENTS)

    print("FILE   %s" % a.draft)
    print("CHARS  %d | TARGET %d | %s" % (
        total, a.target,
        ("OVER BY %d -- MUST TRIM" % need) if need else "within budget"))
    print("ACCENTS %d | PARAS %d | em/en dash %d | 'toi' %d" % (
        n_acc, len(paras), t.count("\u2014") + t.count("\u2013"),
        sum(1 for w in t.split() if w.lower().strip(".,;:!?") == "tôi")))

    heavy = [(i, len(p)) for i, p in enumerate(paras) if len(p) > a.max_part]
    print("PARAS > %d chars (poster will split these into extra replies): %s"
          % (a.max_part, [i for i, _ in heavy] or "none"))

    print("\nFATTEST PARAGRAPHS")
    order = sorted(range(len(paras)), key=lambda i: -len(paras[i]))
    for i in order[:a.top]:
        print("  #%-3d %5d  %s" % (i, len(paras[i]), paras[i][:64].replace("\n", " ")))

    if need:
        print("\nTRIM PLAN (cut fattest first, smallest set that clears the overage)")
        cut, freed = [], 0
        for i in order:
            if freed >= need:
                break
            cut.append(i)
            freed += len(paras[i])
        print("  cut paragraphs %s" % sorted(cut))
        print("  frees ~%d chars -> est. final %d (target %d)" % (freed, total - freed, a.target))
        print("  keep intact: verbatim quotes, the numbered solution list, "
              "the source-disclosure sentence")
        print("  che bang cach GOP cau trong doan to nhat truoc khi xoa han mot doan")
    else:
        print("\nTRIM PLAN: none needed. Margin = %d chars." % (a.target - total))

    sys.exit(0)


if __name__ == "__main__":
    main()
