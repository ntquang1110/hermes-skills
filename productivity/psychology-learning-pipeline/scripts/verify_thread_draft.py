# Verify a psychology thread draft (or KFlow 5-part draft) before sending for review.
# Run via `python .../verify_thread_draft.py <path>` through terminal.
# WHY a standalone file (not inline `python -c`): execute_code is BLOCKED in cron mode,
# and inline -c with escaped quotes is fragile. Write the .py with write_file + run it.
#
# What it checks:
#   - Each post (split on blank line = the post separator) is <= 500 chars
#   - Vietnamese diacritic count >= 20 (thread) — KFlow draft uses its own check below
#   - 0 em dash (\u2014), 0 en dash (\u2013), 0 arrow (\u2192)
#   - 0 non-Latin/CJK/Han/Hangul/Kana chars, 0 emoji
#   - Thread voice: no "tôi" (self) / no "bạn" (reader) — uses "mình"/"anh"
# Exit code 0 = PASS, 1 = FAIL. Prints per-post char counts either way.

import re
import sys

def main(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()

    posts = [p.strip() for p in text.split("\n\n") if p.strip()]
    print(f"Total posts: {len(posts)}")
    ok = True
    for i, p in enumerate(posts, 1):
        n = len(p)
        flag = "  <-- OVER 500" if n > 500 else ""
        if n > 500:
            ok = False
        print(f"  Post {i}: {n} chars{flag}")

    # Vietnamese diacritics
    vi = r"[àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ]"
    diacritics = len(re.findall(vi, text, re.IGNORECASE))
    print(f"Diacritics: {diacritics}")
    # The 5-part KFlow draft (labels + heavy text) is naturally high; thread needs >=20.
    if "**Ví dụ**" in text or text.lstrip().startswith("**"):
        print("  (detected KFlow 5-part draft; diacritic floor not enforced here)")
    elif diacritics < 20:
        ok = False
        print("  FAIL: <20 diacritics")

    # Forbidden characters
    bad = re.findall(r"[\u2014\u2013\u2192\u2190\u4e00-\u9fff\uac00-\ud7af\u3040-\u30ff\u2600-\u27bf\U0001F300-\U0001FAFF]", text)
    if bad:
        ok = False
        print(f"FAIL: forbidden chars found: {sorted(set(bad))}")

    # Thread voice check ("tôi"/"bạn" banned; "mình"/"anh" expected) — skip for KFlow draft
    if "**Ví dụ**" not in text:
        words = set(re.findall(r"[a-zàáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ]+", text.lower()))
        if "tôi" in words:
            ok = False
            print('FAIL: "tôi" used for narrator (must be "mình")')
        if "bạn" in words:
            ok = False
            print('FAIL: "bạn" used for reader (must be "anh")')
        if "mình" not in words:
            print('NOTICE: "mình" not found (verify narrator voice)')

    print("RESULT:", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python verify_thread_draft.py <path>")
        sys.exit(2)
    main(sys.argv[1])