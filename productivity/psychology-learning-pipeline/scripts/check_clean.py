#!/usr/bin/env python3
"""Check a file for genuinely FOREIGN scripts / emoji (NOT Vietnamese punctuation).
Allows Vietnamese diacritics + punctuation (em dash, arrows, quotes, +, %, etc).
Used by the KFlow push cron (Bước 0) before publishing a psychology draft.

Usage: python check_clean.py <file>
Prints: CLEAN  or  FOREIGN: <unique chars>
Exit: 0 if clean, 1 if foreign.

WHY deterministic: an earlier version let the LLM judge "foreign chars" and it
falsely rejected good articles for containing legitimate VN punctuation like
em dash (—) and arrow (→). Byte-level script = no model variance.
Deploy copy: D:/Hermes Proj/psy/scripts/check_clean.py
"""
import sys

def is_forbidden(ch):
    o = ord(ch)
    return (
        # CJK Unified / Ext (Chinese, Japanese kanji)
        (0x3400 <= o <= 0x4DBF) or (0x4E00 <= o <= 0x9FFF)
        # Hangul Jamo / Syllables (Korean)
        or (0x1100 <= o <= 0x11FF) or (0xAC00 <= o <= 0xD7A3) or (0x3130 <= o <= 0x318F)
        # Hiragana / Katakana (Japanese)
        or (0x3040 <= o <= 0x30FF) or (0x31F0 <= o <= 0x31FF)
        # Thai / Lao
        or (0x0E00 <= o <= 0x0E7F) or (0x0E80 <= o <= 0x0EFF)
        # Arabic / Hebrew / Devanagari / Cyrillic / Greek / Georgian / Bengali / Tamil / Telugu / Kannada / Malayalam / Sinhala / Khmer / Myanmar
        or (0x0590 <= o <= 0x08FF) or (0x0400 <= o <= 0x04FF) or (0x0370 <= o <= 0x03FF)
        or (0x0530 <= o <= 0x05FF) or (0x0900 <= o <= 0x097F) or (0x0980 <= o <= 0x09FF)
        or (0x0A00 <= o <= 0x0AFF) or (0x0B00 <= o <= 0x0B7F) or (0x0B80 <= o <= 0x0BFF)
        or (0x0C00 <= o <= 0x0C7F) or (0x0C80 <= o <= 0x0CFF) or (0x0D00 <= o <= 0x0D7F)
        or (0x0D80 <= o <= 0x0DFF) or (0x0E80 <= o <= 0x0EFF) or (0x1000 <= o <= 0x109F)
        # Emoji / pictographs / dingbats
        or (0x1F300 <= o <= 0x1FAFF) or (0x2600 <= o <= 0x27BF)
        or (0x10A0 <= o <= 0x10FF)   # Georgian
        or (0xFB00 <= o <= 0xFBFF) or (0xFE70 <= o <= 0xFEFF)
        or (0x0250 <= o <= 0x02AF and ch.isalpha())  # IPA letters
    )

def main(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    bad = [ch for ch in text if is_forbidden(ch)]
    if not bad:
        print("CLEAN")
        return 0
    uniq = list(dict.fromkeys(bad))
    print("FOREIGN: " + " ".join(repr(ch) for ch in uniq))
    return 1

if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))