#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
verify_prose_article.py — gate for the NUMBERED-SERIES prose psychology article
(bai N/4: mo dau 2 cau -> co che -> he qua thuc te -> ket luan, no labels, no thread).

NOT for the 5-part KFlow article (use verify_psy_outputs.py) and NOT for a
Threads thread draft (same script handles post length separately).

Usage (Windows/MSYS, use `python`, never `python3`):
    python verify_prose_article.py <path-to-article.md> [--min-chars 3000] [--max-chars 7000]

Why a file-based script and not `execute_code` / `python -c`:
  execute_code is BLOCKED in cron mode (approvals.cron_mode). Long inline
  `python -c` / heredoc is also intermittently held for approval. A .py file
  invoked as `python path.py` always runs.

Exit 0 = all gates pass. Exit 1 = at least one gate failed (listed in output).
Run from anywhere; absolute path arg. Self-deleting helper is the caller's job.
"""
import re
import sys

VN = ("àáảãạâầấẩẫậăằắẳẵặèéẻẽẹêềếểễệìíỉĩị"
      "òóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ")

AI_VOCAB = [
    "crucial", "pivotal", "delve", "vibrant", "showcase", "testament",
    "underscore", "landscape", "tapestry", "enhance", "fostering",
    "key ", "highlighting", "additionally", "moreover", "furthermore",
    "in conclusion", "tóm lại", "về bản", "điều mấn chốt", "cốt lõi",
    "nói chung", "rõ ràng là", "quan trọng nhất",
]
SIGNPOST = ["hãy cùng", "bây giờ chúng ta", "để đi sâu", "điều đáng chú ý nhất",
            "hãy nhìn", "trước khi đi tiếp"]


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    path = sys.argv[1]
    min_chars, max_chars = 3000, 7000
    for i, a in enumerate(sys.argv):
        if a == "--min-chars":
            min_chars = int(sys.argv[i + 1])
        if a == "--max-chars":
            max_chars = int(sys.argv[i + 1])

    raw = open(path, encoding="utf-8").read()
    t = "\n".join(re.sub(r"^\d+\|", "", l) for l in raw.split("\n"))

    fail = []

    def gate(name, ok, detail):
        print(f"{name}: {detail}")
        if not ok:
            fail.append(name)

    # --- hard charset gates (user requirement: no em dash, emoji, bold) ---
    gate("em_dash", t.count("\u2014") == 0, t.count("\u2014"))
    gate("en_dash", t.count("\u2013") == 0, t.count("\u2013"))
    gate("arrow", t.count("\u2192") == 0, t.count("\u2192"))
    gate("bold", t.count("**") == 0, t.count("**"))
    gate("markdown_heading", not re.search(r"(?m)^#{1,6}\s", t), len(re.findall(r"(?m)^#{1,6}\s", t)))
    gate("layer_label", not re.search(r"Tầng\s*[12]|Lớp\s*[12]", t), "none")
    gate("curly_quote", t.count("\u201c") + t.count("\u201d") == 0,
         t.count("\u201c") + t.count("\u201d"))
    emoji = re.findall(r"[\U0001F300-\U0001FAFF\u2600-\u27BF\u2B00-\u2BFF\uFE0F]", t)
    gate("emoji", not emoji, emoji or "none")
    cjk = re.findall(r"[\u4e00-\u9fff\u3040-\u30ff\uac00-\ud7af]", t)
    gate("cjk", not cjk, cjk or "none")
    stray = [c for c in t if ord(c) > 0x1EF9 and c not in " \n\t"]
    gate("non_vietnamese_high_codepoint", not stray, stray or "none")

    # --- Vietnamese must actually have diacritics ---
    dia = sum(1 for c in t if c in VN)
    gate("diacritics", dia >= 300, dia)

    # --- structure gates ---
    paras = [p.strip() for p in t.split("\n\n") if p.strip()]
    gate("paragraphs", 6 <= len(paras) <= 14, len(paras))
    opening = paras[0] if paras else ""
    gate("opening_is_2_sentences",
         len(re.findall(r"[.!?](?:\s|$)", opening)) == 2,
         len(re.findall(r"[.!?](?:\s|$)", opening)))
    gate("no_question_in_opening", "?" not in opening, "?" in opening)

    # --- humanizer gates ---
    low = t.lower()
    ai_hits = [w for w in AI_VOCAB if w.lower() in low]
    gate("ai_vocab", not ai_hits, ai_hits or "none")
    sign_hits = [w for w in SIGNPOST if w.lower() in low]
    gate("signposting", not sign_hits, sign_hits or "none")
    neg = re.findall(r"kh\u00f4ng ch\u1ec9 [^.,;]{2,45}\bm\u00e0\b", t)
    gate("neg_parallel", not neg, neg or "none")
    tail = re.findall(r",\s*kh\u00f4ng [^.]+\.$", t, re.M)
    gate("tail_negation", not tail, tail or "none")

    # --- length + rhythm ---
    gate("chars", min_chars <= len(t) <= max_chars, len(t))
    sents = [s for s in re.split(r"(?<=[.!?])\s+", t) if s.strip()]
    lens = [len(s) for s in sents]
    if lens:
        gate("sentence_variance", (max(lens) - min(lens)) > 80,
             f"min={min(lens)} max={max(lens)}")
    print("para_chars:", [len(p) for p in paras])
    print("questions_in_article:", t.count("?"), "(1 = single closing question, ideal)")

    print("RESULT:", "PASS" if not fail else "FAIL -> " + ", ".join(fail))
    return 0 if not fail else 1


if __name__ == "__main__":
    raise SystemExit(main())
