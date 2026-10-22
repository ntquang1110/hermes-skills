#!/usr/bin/env python
"""Quét queue Threads để (a) check trùng video và (b) tìm vùng chủ đề đã bão hoà.

Dùng TRƯỚC khi viết draft: biết vùng nào đã dày để chọn góc khác hẳn,
không trùng quote/ví dụ với bài đã có.

    python queue_topic_scan.py 63FPhjGWjvk
    python queue_topic_scan.py --kw dopamin,thoi quen,tri hoan
    python queue_topic_scan.py --kw dopamin --window 2027-01-01

Stdlib only. Bỏ dấu tiếng Việt khi so khớp để 'học' khớp 'hoc'/'học'.
"""
import argparse
import json
import os
import unicodedata

CACHE = os.path.expanduser("~/AppData/Local/hermes/cache")
SCHED = os.path.join(CACHE, "youtube-schedule.json")
PROC = os.path.join(CACHE, "youtube-processed.json")

DEFAULT_KW = [
    "dopamin", "thoi quen", "tri hoan", "dong luc", "tap trung", "ky luat",
    "hoc", "nao", "nghien", "chuoi ngay", "phan hoi", "skin", "tu hoc",
]


def nz(s):
    """Bỏ dấu + hạ chữ thường để so khớp từ khoá."""
    s = unicodedata.normalize("NFD", s or "")
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return s.replace("đ", "d").replace("Đ", "D").lower()


def load():
    d = json.load(open(SCHED, encoding="utf-8"))
    p = json.load(open(PROC, encoding="utf-8"))
    return d.get("queue", []), d, p


def dup_check(vid, queue, proc):
    hits = []
    for i in queue:
        if i.get("video_id") == vid or (i.get("id") or "").startswith(vid):
            hits.append(("queue", i.get("scheduled_date"), i.get("status"), i.get("id")))
    if vid in (proc.get("video_ids") or []):
        hits.append(("processed.video_ids", "", "", vid))
    for it in proc.get("items") or []:
        if isinstance(it, dict) and it.get("video_id") == vid:
            hits.append(("processed.items", it.get("date"), "", it.get("id")))
    return hits


def scan(queue, kws, window):
    groups = {}
    for i in queue:
        if window and (i.get("scheduled_date") or "") < window:
            continue
        blob = nz((i.get("title") or "") + " " + (i.get("content") or "")[:500])
        for k in kws:
            if nz(k) in blob:
                groups.setdefault(k, []).append(
                    (i.get("scheduled_date") or "?", i.get("status") or "?", (i.get("title") or "")[:64])
                )
    return groups


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video_id", nargs="?", help="video id để check trùng")
    ap.add_argument("--kw", help="danh sách từ khoá, cách nhau dấu phẩy")
    ap.add_argument("--window", help="chỉ tính item từ ngày này trở đi (YYYY-MM-DD)")
    a = ap.parse_args()

    queue, sched, proc = load()
    print(f"queue={len(queue)} items | last_posted={sched.get('last_posted_date')} | processed_ids={len(proc.get('video_ids') or [])}")
    print(f"ngày trống kế tiếp gợi ý: {next_free_date(queue)}")

    if a.video_id:
        hits = dup_check(a.video_id, queue, proc)
        print(f"\n== check trùng {a.video_id}: {'TRÙNG' if hits else 'NEW'}")
        for h in hits:
            print("   ", h)

    kws = [k.strip() for k in a.kw.split(",")] if a.kw else DEFAULT_KW
    groups = scan(queue, kws, a.window)
    print("\n== mật độ vùng chủ đề (item >= 3 là đã dày, chọn góc khác hẳn) ==")
    for k in kws:
        rows = groups.get(k) or []
        if rows:
            print(f"\n## {k}  ({len(rows)})")
            for d, st, t in rows:
                print(f"    {d} | {st:8s} | {t}")
    empty = [i.get("id") for i in queue if i.get("status") == "pending" and not (i.get("content") or "").strip()]
    print(f"\npending thiếu content: {len(empty)} {empty[:5]}")


def next_free_date(queue):
    """Ngày kế tiếp sau scheduled_date lớn nhất (idempotent, không phụ thuộc ngày hiện tại)."""
    import datetime
    mx = max((i.get("scheduled_date") or "" for i in queue), default="")
    if not mx:
        return "?"
    return (datetime.date.fromisoformat(mx) + datetime.timedelta(days=1)).isoformat()


if __name__ == "__main__":
    main()
