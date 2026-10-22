#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Verify BOTH deliverables of a psy slot in one command.

Usage (run as a FILE via terminal — inline `python -c` and `execute_code` are blocked in cron):
    python "<skill_dir>/scripts/verify_psy_plainname.py" "D:/Hermes Proj/psy/drafts/psy_1.txt" "D:/Hermes Proj/psy/threads_drafts/psy_1_thread.txt"

Why this script exists (gapped 2026-10-14, psy_1 "Giấc ngủ và ảnh hưởng lên tâm trí"):
  `verify_psy_2deliverables.py` và `verify_psy_outputs.py` đếm nhãn phần bằng regex `^[1-5]\\.`
  → với variant NHÃN TÊN TRẦN (`Ví dụ` / `Nêu vấn đề` / `Vấn đề gốc rễ` / `First principle` /
  `Giải pháp`) chúng in labels=0 và `ARTICLE FAIL` GIẢ. Lần 2026-10-14 agent tự viết checker
  rác vào %TEMP% rồi xoá — đúng cái pitfall skill đã cấm. Dùng script này thay vì tự chế.

Verdict thật CHỈ dựa vào: words<=450, 5 nhãn phần đúng tên (hoặc biến thể đánh số),
diacritics>=20, forbidden=none, thread 2-3 post mỗi post <=500 và kết ở câu hoàn chỉnh.
"""
import re
import sys
import unicodedata

VN = "ăâđêôơưáàảãạấầẩẫậắằẳẵặéèẻẽẹếềểễệíìỉĩịóòỏõọốồổỗộớờởỡợúùủũụứừửữựýỳỷỹỵ"
PLAIN_LABELS = ["Ví dụ", "Nêu vấn đề", "Vấn đề gốc rễ", "First principle", "Giải pháp"]
NUMBERED_LABELS = ["1. Mở đầu", "2. Cơ chế", "3. Hệ quả", "4. Giải pháp", "5. Kết luận"]
FORBIDDEN = {"\u2014": "em dash", "\u2013": "en dash", "\u2192": "arrow", "\u2018": "curly quote", "\u2019": "curly quote"}
DIACRITIC_FLOOR = 20


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read().strip()


def foreign_chars(text):
    """Chars that are neither ASCII/Latin-Vietnamese nor a legal VN diacritic.

    VN precomposed runs up to U+1EF9 — do NOT set the threshold lower (that is the
    documented "bad=200 chars" fake-rubbish trap).
    """
    out = []
    for ch in text:
        if ord(ch) < 128 or ch in "\n\r\t":
            continue
        if ch.lower() in VN or ch in VN:
            continue
        if unicodedata.category(ch) in ("Mn", "Mc") and ord(ch) < 0x300:
            continue
        out.append(ch)
    return sorted(set(out))


def count_diacritics(text):
    return sum(1 for ch in text if ch.lower() in VN)


def check_article(path):
    t = read(path)
    words = len(t.split())
    lines = [l.strip() for l in t.splitlines()]
    found_plain = [lab for lab in PLAIN_LABELS if lab in lines]
    found_num = [lab for lab in NUMBERED_LABELS if any(l.startswith(lab) for l in lines)]
    labels = len(found_plain) if found_plain else len(found_num)
    foreign = foreign_chars(t)
    dashes = [name for ch, name in FORBIDDEN.items() if ch in t]
    fails = []
    if words > 450:
        fails.append("words %d > 450" % words)
    if labels < 5:
        fails.append("labels %d/5 (plain=%s numbered=%s)" % (labels, found_plain, found_num))
    if count_diacritics(t) < DIACRITIC_FLOOR:
        fails.append("diacritics < %d" % DIACRITIC_FLOOR)
    if foreign:
        fails.append("foreign chars: %s" % foreign)
    if dashes:
        fails.append("forbidden: %s" % dashes)
    print("ARTICLE %s | labels=%d | words=%d | diacritics=%d | forbidden=%s"
          % (path, labels, words, count_diacritics(t), ",".join(dashes) or "none"))
    return fails


def check_thread(path):
    t = read(path)
    posts = [p.strip() for p in re.split(r"\n\s*\n", t) if p.strip()]
    foreign = foreign_chars(t)
    dashes = [name for ch, name in FORBIDDEN.items() if ch in t]
    fails = []
    if not 2 <= len(posts) <= 3:
        fails.append("posts=%d (task allows 2-3)" % len(posts))
    for i, p in enumerate(posts, 1):
        if len(p) > 500:
            fails.append("post %d = %d chars > 500" % (i, len(p)))
        if p and p[-1] not in ".!?":
            fails.append("post %d does not end on a complete sentence" % i)
    if count_diacritics(t) < DIACRITIC_FLOOR:
        fails.append("diacritics < %d" % DIACRITIC_FLOOR)
    if foreign:
        fails.append("foreign chars: %s" % foreign)
    if dashes:
        fails.append("forbidden: %s" % dashes)
    # Pronoun gate: nguoi ke = "minh", nguoi doc = "anh". Soi dong match, dung tin count tho.
    for bad in ("tôi", "bạn"):
        for m in re.finditer(r"\b%s\b" % bad, t):
            print("  NOTE pronoun '%s' -> %r  (soi dong: co the la danh tu / noi tam, KHONG tu dong cat)" % (bad, t[max(0, m.start() - 30):m.end() + 30]))
    print("THREAD %s | posts=%d | lengths=%s | total=%d | diacritics=%d | forbidden=%s"
          % (path, len(posts), [len(p) for p in posts], sum(len(p) for p in posts),
             count_diacritics(t), ",".join(dashes) or "none"))
    return fails


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    fails = check_article(sys.argv[1]) + check_thread(sys.argv[2])
    print("RESULT:", "PASS" if not fails else "FAIL " + "; ".join(fails))
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
