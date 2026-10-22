#!/usr/bin/env python3
"""Chunk a Vietnamese Threads draft into <=500-char parts cut at sentence boundaries,
plus pre-approval checks (accents, em dash, emoji).

Usage: python chunk_500.py <draft.txt>

Matches Quang's approved pipeline: draft -> verify accents/em-dash/emoji -> split
into parts max 500 chars, cutting at sentence boundaries, never mid-word.
"""
import io
import re
import sys

VIET_MARKS = ('àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợ'
              'ùúủũụưừứửữựỳýỷỹỵđ'
              'ÀÁẢÃẠĂẰẮẲẴẶÂẦẤẨẪẬÈÉẺẼẸÊỀẾỂỄỆÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢ'
              'ÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴĐ')


def main():
    if len(sys.argv) < 2:
        print("Usage: python chunk_500.py <draft.txt>")
        sys.exit(1)
    path = sys.argv[1]
    with io.open(path, encoding='utf-8') as f:
        text = f.read()

    marks = sum(1 for ch in text if ch in VIET_MARKS)
    em = text.count('\u2014') + text.count('\u2013')
    emoji = any(ord(ch) > 0x1F000 for ch in text)

    print(f"Chars: {len(text)} | Accents: {marks} | Em dash: {em} | Emoji: {emoji}")
    if marks < 20:
        print("WARNING: <20 accents - encoding likely stripped, rewrite via write_file (NOT heredoc)")
    if em or emoji:
        print("WARNING: em dash / emoji found - fix before sending for approval")

    flat = text.replace('\n', ' ').strip()
    sentences = re.split(r'(?<=[.!?]) ', flat)
    parts, cur = [], ''
    for s in sentences:
        if len(cur) + len(s) + 1 > 500 and cur:
            parts.append(cur.strip())
            cur = s
        else:
            cur = (cur + ' ' + s).strip()
    if cur:
        parts.append(cur.strip())

    print(f"Parts: {len(parts)} (max {max(len(p) for p in parts)})")
    for i, p in enumerate(parts, 1):
        print(f"\n--- Part {i} ({len(p)} chars) ---\n{p}")


if __name__ == '__main__':
    main()
