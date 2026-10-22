# -*- coding: utf-8 -*-
"""Verify deliverables of the daily psychology cron (bai N trong ngay).

Usage:
    python verify_psy_outputs.py <draft_5phan> <thread_draft>
    python verify_psy_outputs.py "D:/Hermes Proj/psy/drafts/psy_1.txt" "D:/Hermes Proj/psy/threads_drafts/psy_1_thread.txt"

Checks:
  Article (drafts/psy_N.txt, 5 phan):
    - words <= 450 (len(text.split()), dem CA 5 nhan phan)
    - >= 5 label lines matching ^N. <ten>
    - diacritics >= 20
    - no forbidden chars
  Thread (threads_drafts/psy_N_thread.txt):
    - posts = split on 2+ blank lines (regex \\n\\s*\\n\\s*\\n) -> 2 to 3
    - each post <= 500 chars and ends with a complete sentence (. ? !)
    - total chars <= 1300
    - diacritics >= 20
    - no forbidden chars

Forbidden chars: em dash (U+2014), en dash (U+2013), arrows (->, <-, =>, <=),
CJK (Han/Kana/Hangul), emoji ranges, Greek, and any char outside ASCII /
Latin-1..Latin Extended Additional (0x00C0-0x1EFF).

Exit 0 = ALL PASS. Run via `terminal` only: execute_code, heredoc and
`python -c` are approval-blocked in cron mode. Tested pass on psy_1
(442 words; posts 257/444/466).
"""
import re
import sys

V = "àáảãạăằắẳẵặâầấẩẫậđèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵ"
DIACRITIC_SET = set(V + V.upper())


def diacritics(t):
    return sum(1 for c in t if c in DIACRITIC_SET)


def forbidden(t):
    bad = []
    for c in t:
        o = ord(c)
        if o in (0x2014, 0x2013):  # em dash, en dash
            bad.append((c, hex(o), 'dash'))
        elif c in "→←⇒⇐":
            bad.append((c, hex(o), 'arrow'))
        elif 0x4E00 <= o <= 0x9FFF or 0x3040 <= o <= 0x30FF or 0xAC00 <= o <= 0xD7AF:
            bad.append((c, hex(o), 'cjk'))
        elif 0x1F000 <= o <= 0x1FAFF or 0x2600 <= o <= 0x27BF:
            bad.append((c, hex(o), 'emoji'))
        elif 0x0370 <= o <= 0x03FF:
            bad.append((c, hex(o), 'greek'))
        elif not (c.isascii() or 0x00C0 <= o <= 0x1EFF):
            bad.append((c, hex(o), 'other'))
    return bad


def check_article(path):
    t = open(path, encoding='utf-8').read()
    words = len(t.split())
    labels = len(re.findall(r"(?m)^[1-5]\.\s", t))
    dia = diacritics(t)
    fb = forbidden(t)
    ok = words <= 450 and labels >= 5 and dia >= 20 and not fb
    print("ARTICLE %s | words=%d (<=450) | labels=%d (>=5) | diacritics=%d | forbidden=%s"
          % ("PASS" if ok else "FAIL", words, labels, dia, fb or "none"))
    return ok


def check_thread(path):
    t = open(path, encoding='utf-8').read()
    posts = [p.strip() for p in re.split(r"\n\s*\n\s*\n", t) if p.strip()]
    lens = [len(p) for p in posts]
    size_ok = 2 <= len(posts) <= 3 and all(n <= 500 and p.endswith((".", "?", "!"))
                                      for p, n in zip(posts, lens))
    tot = sum(lens)
    dia = diacritics(t)
    fb = forbidden(t)
    ok = size_ok and tot <= 1300 and dia >= 20 and not fb
    print("THREAD %s | posts=%d | chars=%s | total=%d (<=1300) | diacritics=%d | forbidden=%s"
          % ("PASS" if ok else "FAIL", len(posts), lens, tot, dia, fb or "none"))
    return ok


def main():
    if len(sys.argv) < 3:
        print("Usage: python verify_psy_outputs.py <draft_5phan> <thread_draft>")
        return 2
    ok = check_article(sys.argv[1]) and check_thread(sys.argv[2])
    print("VERDICT:", "ALL PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
