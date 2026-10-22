#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Verify bài tâm lý 5 đoạn + bản thread psy (pipeline D:/Hermes Proj/psy).

Dùng:
    python verify_psy_thread.py "<draft psy_N.txt>" ["<threads psy_N_thread.txt>"]

Kiểm tra:
  Bài KFlow (5 đoạn):
    - <= 450 từ, đúng 5 nhãn phần: Ví dụ / Nêu vấn đề / Vấn đề gốc rễ / First principle / Giải pháp
  Bản thread:
    - đúng 2-3 block (mỗi block = 1 post), mỗi block <= 500 ký tự, kết ở câu hoàn chỉnh
    - tổng <= 1500 ký tự (3 x 500)
  Cả hai:
    - 0 em dash / en dash / mũi tên / CJK (Hàn, Nhật, Trung) / emoji
    - ký tự có dấu tiếng Việt >= 20
  Riêng thread:
    - KHÔNG có "tôi" (người kể), KHÔNG "bạn" (người đọc), KHÔNG nhãn "Tầng"
    - PHẢI có "mình" + "anh" (xưng hô chế độ psy)
    - Cảnh báo "tôi"/"bạn" nằm trong quote nguyên văn là ngoại lệ đã biết: đọc context in ra rồi tự quyết.

Exit 0 = PASS, 1 = FAIL. Không sửa gì, chỉ đọc (READ-ONLY).
"""

import os
import re
import sys

ACCENT_CHARS = (
    "àáảãạăắằẳẵặâấầẩẫậ"
    "èéẻẽẹêếềểễệ"
    "ìíỉĩị"
    "òóỏõọôốồổỗộơớờởỡợ"
    "ùúủũụưứừửữự"
    "ỳýỷỹỵđ"
)
ACCENT_RE = re.compile("[" + ACCENT_CHARS + ACCENT_CHARS.upper() + "]")
# CJK (Hàn, Nhật, Trung), arrow, em/en dash
FORBIDDEN_RE = re.compile(
    "[\uac00-\ud7a3\u4e00-\u9fff\u3041-\u3094\u30a1-\u30fa\u2190-\u21ff\u2014\u2013]"
)
EMOJI_RE = re.compile(
    "[\U0001F300-\U0001FAFF\u2600-\u27BF\uFE0F\u2708\u2764]"
)
WANT_LABELS = [
    "Ví dụ",
    "Nêu vấn đề",
    "Vấn đề gốc rễ",
    "First principle",
    "Giải pháp",
]
SENTENCE_END = (".", "!", "?", '"', "'", "\u201d", "\u2019", ")")
MAX_WORDS = 450
MAX_POST = 500
MAX_TOTAL = 1500


def forbidden_hits(text):
    hits = []
    for name, rx in (("non-latin/arrow/dash", FORBIDDEN_RE), ("emoji", EMOJI_RE)):
        found = rx.findall(text)
        if found:
            hits.append("%s %r" % (name, found[:8]))
    return hits


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def check_draft(path, fails, notes):
    text = read(path)
    words = len(text.split())
    blocks = [b for b in text.split("\n\n") if b.strip()]
    labels = [b.split("\n")[0].strip() for b in blocks]
    notes.append("DRAFT %s: %d từ, %d ký tự, %d phần" % (os.path.basename(path), words, len(text), len(blocks)))
    notes.append("  nhãn: %s" % labels)
    if words > MAX_WORDS:
        fails.append("draft %d từ > %d" % (words, MAX_WORDS))
    if labels != WANT_LABELS:
        fails.append("draft nhãn sai thứ tự/thiếu: %r" % labels)
    if len(ACCENT_RE.findall(text)) < 20:
        fails.append("draft thiếu dấu tiếng Việt (<20)")
    fails.extend("draft " + h for h in forbidden_hits(text))


def check_thread(path, fails, notes):
    text = read(path)
    posts = [p for p in text.split("\n\n") if p.strip()]
    lens = [len(p) for p in posts]
    notes.append("THREAD %s: %d post, chars %s, tổng %d" % (os.path.basename(path), len(posts), lens, len(text)))
    notes.append("  dấu tiếng Việt: %d" % len(ACCENT_RE.findall(text)))
    if not 2 <= len(posts) <= 3:
        fails.append("thread có %d block (mỗi block = 1 post) — phải 2-3" % len(posts))
    for i, p in enumerate(posts, 1):
        if len(p) > MAX_POST:
            fails.append("post %d dài %d ký tự > %d" % (i, len(p), MAX_POST))
        tail = p.rstrip()
        if not tail.endswith(SENTENCE_END):
            fails.append("post %d cắt giữa câu: %r" % (i, tail[-40:]))
    if len(text) > MAX_TOTAL:
        fails.append("thread tổng %d ký tự > %d" % (len(text), MAX_TOTAL))
    if len(ACCENT_RE.findall(text)) < 20:
        fails.append("thread thiếu dấu tiếng Việt (<20)")
    fails.extend("thread " + h for h in forbidden_hits(text))
    low = text.lower()
    if "tầng" in low:
        fails.append('thread có nhãn "Tầng"')
    for tok, why in (("tôi", 'người kể phải là "mình"'), ("bạn", 'người đọc phải là "anh"')):
        if tok in low:
            ctx = re.findall(r".{0,25}" + tok + r".{0,25}", low)[:3]
            fails.append('thread có %r (%s) — nếu nằm trong QUOTE nguyên văn thì bỏ qua; context: %r' % (tok, why, ctx))
    if "mình" not in low or "anh" not in low:
        fails.append('thread thiếu xưng hô "mình"/"anh"')


def main(argv):
    if not 2 <= len(argv) <= 3:
        print(__doc__)
        return 2
    fails, notes = [], []
    draft = argv[1]
    if not os.path.exists(draft):
        print("KHÔNG thấy file: %s" % draft)
        return 2
    check_draft(draft, fails, notes)
    if len(argv) == 3:
        if not os.path.exists(argv[2]):
            print("KHÔNG thấy file thread: %s" % argv[2])
            return 2
        check_thread(argv[2], fails, notes)

    print("\n".join(notes))
    print("RESULT:", "PASS" if not fails else "FAIL")
    for f in fails:
        print(" - " + f)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
