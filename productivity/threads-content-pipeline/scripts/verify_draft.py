#!/usr/bin/env python
"""verify_draft.py — READ-ONLY verify + chunk report cho draft Threads.

Dung thay cho viec tu viet lai doan `python -c` moi lan verify draft truoc khi
gui user duyet (phien 2026-10-18 goi lai doan inline 6 lan cho 6 draft).

    python scripts/verify_draft.py "C:/Users/NTQUANG_DELL/hermes-temp/draft_x.txt"
    python scripts/verify_draft.py <draft.txt> --json

Kiem:
  - chars tong, so ky tu co dau tieng Viet (>= 20 bat buoc; draft chuan > 300)
  - 0 em dash, 0 en dash, 0 mui ten, 0 emoji, 0 CJK (Han/Nhat/Trung)
  - khong nhan "Tang"
  - so lan "toi" (phai nam TRONG quote nguyen van, khong phai loi xung ho)
  - chunk report theo dung thuat toan split_posts: tach block bang \\n\\n,
    cat tiep tai cau khi block > 500, noi block khi con cho
    -> part > 500 la FAIL (Threads khoa nut Post, dang bai that bai im lang)
    -> part dung 500 la WARN (nen bot con <= 498 cho an toan)

Exit: 0 = PASS, 1 = FAIL, 2 = usage.
"""
import json
import re
import sys
from pathlib import Path

ACCENTS = "àáảãạâầấẩẫậăằắẳẵặèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ"
MAX_PART = 500
SAFE_PART = 498
EMOJI_RE = re.compile(
    "[\U0001F1E6-\U0001F1FF\U0001F300-\U0001F5FF\U0001F600-\U0001F64F"
    "\U0001F680-\U0001F6FF\U0001F900-\U0001F9FF\U00002600-\U000027BF\U0001FA70-\U0001FAFF]"
)


def split_posts(text, max_len=MAX_PART):
    """Giong split_posts trong SKILL.md — trach lech hanh vi voi poster that."""
    parts = []
    for block in text.split("\n\n"):
        block = block.strip()
        if not block:
            continue
        if not parts or len(parts[-1]) + len(block) + 2 > max_len:
            if len(block) > max_len:
                chunk = ""
                for s in re.split(r"(?<=[.!?])\s+", block):
                    if len(chunk) + len(s) + 1 <= max_len:
                        chunk = (chunk + " " + s).strip()
                    else:
                        if chunk:
                            parts.append(chunk)
                        chunk = s
                if chunk:
                    parts.append(chunk)
            else:
                parts.append(block)
        else:
            parts[-1] += "\n\n" + block
    return parts


def verify(path):
    text = Path(path).read_text(encoding="utf-8").strip()
    if not text:
        return {"error": "file rong"}

    parts = split_posts(text)
    chars = [len(p) for p in parts]
    accents = sum(1 for c in text if c in ACCENTS)
    emoji = EMOJI_RE.findall(text)
    cjk = sorted({c for c in text if 0x3040 <= ord(c) <= 0x30FF
                  or 0x4E00 <= ord(c) <= 0x9FFF or 0xAC00 <= ord(c) <= 0xD7AF})
    over = [(i + 1, n) for i, n in enumerate(chars) if n > MAX_PART]
    at_cap = [i + 1 for i, n in enumerate(chars) if n == MAX_PART]

    fails = []
    if accents < 20:
        fails.append("dau tieng Viet qua it (%d)" % accents)
    if "\u2014" in text:
        fails.append("em dash x%d" % text.count("\u2014"))
    if "\u2013" in text:
        fails.append("en dash x%d" % text.count("\u2013"))
    if "\u2192" in text or "\u2190" in text:
        fails.append("mui ten")
    if emoji:
        fails.append("emoji x%d" % len(emoji))
    if cjk:
        fails.append("CJK " + "".join(cjk))
    if "Tầng" in text:
        fails.append('nhan "Tang"')
    if over:
        fails.append("part >500: " + repr(over))

    warns = []
    if at_cap:
        warns.append("part dung 500 (nen <= %d): %s" % (SAFE_PART, at_cap))

    toi = len(re.findall(r"\btôi\b", text, re.I))
    return {
        "path": str(path),
        "chars": len(text),
        "accents": accents,
        "parts": len(parts),
        "part_chars": chars,
        "max_part": max(chars) if chars else 0,
        "over_500": over,
        "at_500": at_cap,
        "em_dash": text.count("\u2014"),
        "en_dash": text.count("\u2013"),
        "arrow": text.count("\u2192") + text.count("\u2190"),
        "emoji": len(emoji),
        "cjk": "".join(cjk),
        "tang_label": "Tầng" in text,
        "toi_count": toi,
        "fails": fails,
        "warns": warns,
        "pass": not fails,
    }


def main(argv):
    args = [a for a in argv[1:] if not a.startswith("--")]
    as_json = "--json" in argv
    if len(args) != 1:
        print("usage: python verify_draft.py <draft.txt> [--json]")
        return 2

    if not Path(args[0]).exists():
        print("KHONG THAY FILE: %s" % args[0])
        return 2

    r = verify(args[0])
    if as_json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
        return 0 if r.get("pass") else 1

    print("=== VERIFY DRAFT ===")
    print("file          : %s" % r["path"])
    print("Chars         : %d" % r["chars"])
    print("Dau TV        : %d" % r["accents"])
    print("Parts         : %d  (max %d)" % (r["parts"], r["max_part"]))
    print("Part chars    : %s" % r["part_chars"])
    print("Em/En dash    : %d / %d" % (r["em_dash"], r["en_dash"]))
    print("Arrow / Emoji : %d / %d" % (r["arrow"], r["emoji"]))
    print("CJK           : %s" % (r["cjk"] or "none"))
    print('Nhan "Tang"   : %s' % ("CO" if r["tang_label"] else "khong"))
    print("Chu 'toi'     : %d  (chi duoc nam trong quote nguyen van)" % r["toi_count"])
    for w in r["warns"]:
        print("  WARN: %s" % w)
    if not r["pass"]:
        for f in r["fails"]:
            print("  FAIL: %s" % f)
        print("KET LUAN: FAIL")
        return 1
    print("  OK: khong flag nao")
    print("KET LUAN: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
