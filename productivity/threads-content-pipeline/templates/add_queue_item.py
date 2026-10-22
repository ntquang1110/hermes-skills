#!/usr/bin/env python
"""Add ONE draft to the Threads schedule queue + processed tracker.

Why this template exists (2026-10-18/19): the add-queue script got hand-written
from scratch FOUR times in two sessions, and every rewrite re-introduced the same
two bugs -- (a) `p["items"][VID] = ...` when `items` is a LIST -> TypeError, and
(b) forgetting to embed the `content` field so the item was silent-skipped by the
poster. Copy this file, pass args, run it. Do not re-derive it.

Usage:
  python add_queue_item.py --video-id 2TKRSX9tbNQ \
      --draft "C:/Users/NTQUANG_DELL/hermes-temp/draft_x.txt" \
      --title "The Blue Guy - Hieu suat = tiem nang - can nhieu" \
      --channel "The Blue Guy"
  # --date omitted  -> auto = max(scheduled_date in queue) + 1 day
  # --date 2027-02-01 to force a date (refused if that date is already taken)

Exit codes: 0 = added, 1 = refused, 2 = usage / bad input.
"""
import argparse
import json
import os
import sys
from datetime import datetime, timedelta

CACHE = os.path.expanduser("~/AppData/Local/hermes/cache")
SCHED = os.path.join(CACHE, "youtube-schedule.json")
PROC = os.path.join(CACHE, "youtube-processed.json")

ACCENTS = (
    "àáảãạâầấẩẫậăằắẳẵặèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợ"
    "ùúủũụưừứửữựỳýỷỹỵđ"
)


def die(msg, code=1):
    print("FAIL:", msg)
    sys.exit(code)


def next_date(queue):
    dates = [i.get("scheduled_date") for i in queue if i.get("scheduled_date")]
    if not dates:
        return datetime.now().strftime("%Y-%m-%d")
    last = max(dates)
    return (datetime.strptime(last, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--video-id", required=True)
    ap.add_argument("--draft", required=True)
    ap.add_argument("--title", required=True)
    ap.add_argument("--channel", default="")
    ap.add_argument("--date", default="")
    ap.add_argument("--time", default="20:00")
    ap.add_argument("--url", default="")
    ap.add_argument("--source", default="youtube", help="youtube | tiktok | article | auto")
    a = ap.parse_args()

    if not os.path.isfile(a.draft):
        die("draft not found: " + a.draft, 2)

    content = open(a.draft, encoding="utf-8").read().strip()
    if not content:
        die("draft file is empty: " + a.draft, 2)
    n_acc = sum(1 for ch in content if ch in ACCENTS)
    if n_acc < 20:
        die("only %d Vietnamese accented chars -- rewrite the draft, "
            "never paste content through a shell heredoc" % n_acc, 2)

    d = json.load(open(SCHED, encoding="utf-8"))
    q = d["queue"]

    date = a.date or next_date(q)
    item_id = "%s-%s" % (a.video_id, date.replace("-", ""))

    if any(i.get("id") == item_id for i in q):
        die("item already in queue: " + item_id)
    taken = [i.get("id") for i in q if i.get("scheduled_date") == date]
    if taken:
        die("date %s already taken by %s (use --date or omit it)" % (date, taken))

    url = a.url or "https://www.youtube.com/watch?v=%s" % a.video_id
    q.append({
        "id": item_id,
        "video_id": a.video_id,
        "scheduled_date": date,
        "scheduled_time": a.time,
        "status": "pending",
        "title": a.title,
        "channel": a.channel,
        "source": a.source,
        "url": url,
        "chars": len(content),
        "draft_path": os.path.abspath(a.draft),
        "added_at": datetime.now().isoformat(timespec="seconds"),
        # THE WHOLE POST BODY. Without this the poster returns early, silently.
        "content": content,
    })
    q.sort(key=lambda i: (i.get("scheduled_date") or "", i.get("id") or ""))
    json.dump(d, open(SCHED, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    # Tracker: `items` is a LIST of records, NOT a dict keyed by video id.
    # Keep this step re-runnable -- if a partial write ever happens, you re-run and
    # only the tracker gets patched; never delete the queue item.
    proc_note = "ok"
    try:
        p = json.load(open(PROC, encoding="utf-8"))
        p.setdefault("video_ids", [])
        p.setdefault("urls", [])
        p.setdefault("items", [])
        if a.video_id not in p["video_ids"]:
            p["video_ids"].append(a.video_id)
        if url not in p["urls"]:
            p["urls"].append(url)
        p["items"].append({
            "id": item_id, "video_id": a.video_id, "title": a.title,
            "url": url, "date": date,
        })
        p["last_updated"] = datetime.now().strftime("%Y-%m-%d")
        json.dump(p, open(PROC, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    except Exception as exc:  # queue is already written; report, do not roll back
        proc_note = "TRACKER FAILED (%s) -- patch youtube-processed.json by hand" % exc

    # Audit (always run, never skip)
    ids = [i.get("id") for i in q]
    dates = [i.get("scheduled_date") for i in q]
    dup_id = sorted({x for x in ids if ids.count(x) > 1})
    missing = [i.get("id") for i in q
               if i.get("status") == "pending" and not (i.get("content") or "").strip()]
    ok = (not dup_id) and (not missing)
    print("ADDED %s | chars=%d | queue=%d | pending_missing_content=%d | dup_id=%s | tracker=%s"
          % (item_id, len(content), len(q), len(missing), dup_id or "none", proc_note))
    print("AUDIT %s | dup_date=%s"
          % ("PASS" if ok else "REVIEW",
             sorted({x for x in dates if dates.count(x) > 1}) or "none"))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
