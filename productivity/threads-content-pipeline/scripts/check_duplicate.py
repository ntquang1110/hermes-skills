#!/usr/bin/env python
"""check_duplicate.py <video_id_or_url> [<video_id_or_url> ...]

READ-ONLY duplicate check for the Threads content pipeline.

Checks BOTH sources before any fetch/write:
  1. youtube-processed.json  -> video_ids[] and urls[]
  2. youtube-schedule.json   -> queue[] (ANY status: pending AND posted)

If the video is already queued, audits that queue item so you can report it to
the user (length, accents, forbidden chars, CJK/emoji, "Tang" labels, part split)
and offer the three choices: keep as-is / move earlier / rewrite from a new angle.

Exit codes:
  0 = NEW      -> safe to fetch transcript and write a draft
  3 = DUP      -> do NOT fetch, do NOT write; audit is printed instead
  2 = usage    -> no id given

Never writes anything. Safe to run any time.

Known pitfall this script guards against (hit 2026-10-07): queue items may have
`"url": null`, so `item.get('url','') + item.get('id','')` raises
`TypeError: unsupported operand type(s) for +: 'NoneType' and 'str'`.
Use `json.dumps(item)` for substring search, or `(x.get('url') or '')`.
"""
import json
import os
import re
import sys

CACHE = os.path.expanduser("~/AppData/Local/hermes/cache")
PROCESSED = os.path.join(CACHE, "youtube-processed.json")
SCHEDULE = os.path.join(CACHE, "youtube-schedule.json")

ACCENTS = ("àáảãạâầấẩẫậăằắẳẵặèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợ"
           "ùúủũụưừứửữựỳýỷỹỵđ")
CJK = r"[가-힣一-龥ぁ-ゔァ-ヺ]"
EMOJI = r"[\U0001F300-\U0001FAFF\u2600-\u27BF]"


def vid_of(s):
    """Accept a full YouTube URL or a bare 11-char id."""
    m = re.search(r"(?:v=|youtu\.be/|shorts/|embed/|live/)([A-Za-z0-9_-]{11})", s or "")
    return m.group(1) if m else (s or "").strip()


def split_posts(text, MAX=500):
    """Same splitter the poster uses: blank-line blocks, then sentences."""
    if len(text) <= MAX:
        return [text]
    parts = []
    for block in text.split("\n\n"):
        block = block.strip()
        if not block:
            continue
        if not parts or len(parts[-1]) + len(block) + 2 > MAX:
            if len(block) > MAX:
                for s in re.split(r"(?<=[.!?])\s+", block):
                    if not parts:
                        parts.append(s)
                    elif len(parts[-1]) + len(s) + 1 <= MAX:
                        parts[-1] = (parts[-1] + " " + s).strip()
                    else:
                        parts.append(s)
            else:
                parts.append(block)
        else:
            parts[-1] += "\n\n" + block
    return parts


def audit(item):
    c = item.get("content") or ""
    parts = split_posts(c)
    print("    scheduled_date : %s" % item.get("scheduled_date"))
    print("    status         : %s" % item.get("status"))
    print("    title          : %s" % item.get("title"))
    print("    chars          : %d" % len(c))
    print("    accents        : %d" % sum(1 for ch in c if ch in ACCENTS))
    print("    em/en dash     : %d / %d" % (c.count("\u2014"), c.count("\u2013")))
    print("    arrows         : %d / %d" % (c.count("\u2192"), c.count("\u2190")))
    print("    CJK hits       : %s" % (re.findall(CJK, c)[:5] or "none"))
    print("    emoji hits     : %s" % (re.findall(EMOJI, c)[:5] or "none"))
    print("    'Tang' labels  : %d" % c.count("Tầng"))
    toi = re.findall(r".{40}\btôi\b.{40}", c, re.I)
    print("    'toi' hits     : %d" % len(toi))
    for t in toi:
        print("        ... %s ..." % t.replace("\n", " | "))
    print("    parts / max    : %d / %d" % (len(parts), max(len(p) for p in parts)))
    print("")
    print("    -> Report to user: date + status + chars + accents + audit result, then offer")
    print("       (1) keep as-is, (2) move earlier, (3) rewrite from a different angle.")
    print("       If the user replies with a NEW link instead of answering, treat it as")
    print("       'keep as-is'. Do NOT move it. Do NOT rewrite it unprompted.")
    print("       A 'toi' hit inside a translated on-stage quote is NOT a xung ho error.")


def main(ids):
    if not ids:
        print(__doc__)
        return 2

    processed = json.load(open(PROCESSED, encoding="utf-8"))
    schedule = json.load(open(SCHEDULE, encoding="utf-8"))
    queue = schedule.get("queue") or []
    vids = processed.get("video_ids") or []
    urls = processed.get("urls") or []

    dup_found = False
    for raw in ids:
        vid = vid_of(raw)
        print("=== %s ===" % vid)

        in_vids = vid in vids
        in_urls = any(vid in (u or "") for u in urls)
        print("  processed.json : video_ids=%s  urls=%s" % (in_vids, in_urls))

        # json.dumps() avoids the NoneType+str crash on items with url: null
        hits = [i for i in queue if vid in json.dumps(i)]
        print("  queue hits     : %d" % len(hits))
        for it in hits:
            audit(it)

        if in_vids or in_urls or hits:
            dup_found = True
            print("  VERDICT: DUPLICATE. Do not fetch, do not write. Audit above.")
        else:
            print("  VERDICT: NEW. Safe to fetch transcript -> read full -> draft.")
        print("")

    return 3 if dup_found else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
