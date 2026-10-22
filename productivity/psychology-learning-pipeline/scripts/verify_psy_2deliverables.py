#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Verify a 2-deliverable psychology cron run: 5-part KFlow article + Threads draft.

Usage (via terminal, NOT execute_code -- blocked in cron mode):
    python verify_psy_2deliverables.py <article_5phan> <thread_draft>

Article criteria (drafts/psy_N_YYYYMMDD_slug.txt):
  - >= 4 plain labels matching ^N. <name>  (5-part = 5+; 4-part variant = 4, PASS)
  - no em dash / en dash / arrow / CJK / emoji
  - enough Vietnamese diacritics

Thread criteria (threads_drafts/psy_N_thread.txt):
  - 2-3 posts, split on blank line (blank line INSIDE a post = a separate post, a bug)
  - each post <= 500 chars, cut at a complete sentence
  - total <= ~1300 chars
  - no em dash / en dash / arrow / CJK / emoji
  - Vietnamese diacritics >= 20
  - no second-person "bạn" / no "tôi" narrator  (REVIEW each grep hit by hand --
    "bạn bè" = friends, "trong bạn" = in you, "đứa bạn" = a buddy: all valid)

Exit 0 = pass, 1 = fail. Prints one verdict line per deliverable.
"""

import re
import sys

FORBIDDEN = {
    "em-dash": "—",
    "en-dash": "–",
    "arrow": "→",
    "emoji": None,  # checked by codepoint
}

VN_DIACRITICS = re.compile(
    r"[àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩị"
    r"òóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ]",
    re.I,
)
CJK = re.compile(r"[　-鿿가-힯぀-ヿ]")


def scan_charset(text):
    """Return list of forbidden-character findings."""
    bad = []
    for name, ch in FORBIDDEN.items():
        if ch and ch in text:
            bad.append("%s x%d" % (name, text.count(ch)))
    if CJK.search(text):
        bad.append("CJK %r" % (CJK.findall(text)[:5],))
    if any(ord(c) > 0x1F000 for c in text):
        bad.append("emoji")
    if any(0x300 <= ord(c) <= 0x36F for c in text):
        bad.append("combining-mark")
    # Latin-extended junk (z with dot, eth...) is category Ll and NOT caught by CJK
    stray = sorted(
        {
            c
            for c in text
            if ord(c) > 0x7F
            and not VN_DIACRITICS.match(c)
            and c not in " \n\t\r"
            and not (0x00C0 <= ord(c) <= 0x024F and c in "àáảãạăâêôơưđÀÁẢÃẠĂÂÊÔƠƯĐ")
        }
    )
    return bad, stray


def check_article(path):
    text = open(path, encoding="utf-8").read()
    labels = re.findall(r"^[1-5]\. .+$", text, re.M)
    bad, stray = scan_charset(text)
    diacritics = len(VN_DIACRITICS.findall(text))
    print("ARTICLE %s | labels=%d | diacritics=%d | forbidden=%s | words=%d"
          % (path.split("/")[-1], len(labels), diacritics,
             ",".join(bad) if bad else "none", len(text.split())))
    if stray:
        print("  stray non-VN chars: %r" % (stray[:12],))
    ok = not bad and diacritics >= 20 and len(labels) >= 4
    if len(labels) == 4:
        print("  NOTE labels=4 is the 4-part variant -- valid, not a fail.")
    return ok


def check_thread(path):
    text = open(path, encoding="utf-8").read()
    posts = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    lengths = [len(p) for p in posts]
    bad, stray = scan_charset(text)
    diacritics = len(VN_DIACRITICS.findall(text))
    pronouns = {}
    for word in ("tôi", "bạn", "mình", "anh"):
        pronouns[word] = len(re.findall(r"\b%s\b" % word, text))
    over = [(i + 1, n) for i, n in enumerate(lengths) if n > 500]
    not_ending = [(i + 1, p[-1]) for i, p in enumerate(posts) if p[-1] not in ".!?"]
    print("THREAD %s | posts=%d | lengths=%s | total=%d | diacritics=%d | forbidden=%s"
          % (path.split("/")[-1], len(posts), lengths, len(text),
             diacritics, ",".join(bad) if bad else "none"))
    print("  pronouns: %s" % pronouns)
    if pronouns.get("tôi"):
        print("  NOTE 'tôi' must be 0 -- rewrite as 'mình' even inside quotes.")
    if pronouns.get("bạn"):
        print("  NOTE review each 'bạn' by hand: 'bạn bè'/'trong bạn' are valid.")
    if not_ending:
        print("  NOTE post must END at a complete sentence, never mid-cut: %r" % (not_ending,))
    if stray:
        print("  stray non-VN chars: %r" % (stray[:12],))
    ok = (2 <= len(posts) <= 3 and not over and not not_ending and not bad
          and diacritics >= 20 and len(text) <= 1300)
    return ok


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        return 1
    art_ok = check_article(sys.argv[1])
    thr_ok = check_thread(sys.argv[2])
    print("RESULT %s" % ("PASS" if (art_ok and thr_ok) else "FAIL"))
    return 0 if (art_ok and thr_ok) else 1


if __name__ == "__main__":
    sys.exit(main())