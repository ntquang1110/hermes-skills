#!/usr/bin/env python3
"""
Check Knowledge Flow cards for duplicate titles before researching.

Usage:
    python check_kflow_duplicate.py "Title of proposed research"

Returns:
    UNIQUE              → safe to proceed
    DUPLICATE:<card-id> → card with this title/topic already exists

Environment:
    KF_URL (default: http://localhost:3003)
"""
import json, sys, os, urllib.request

KF_URL = os.environ.get("KF_URL", "http://localhost:3003")


def fetch_cards():
    """Get all cards from KF."""
    req = urllib.request.Request(f"{KF_URL}/api/cards")
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read())


def is_duplicate(candidate: str, existing_title: str) -> bool:
    """Heuristic duplicate check between two titles."""
    cand = candidate.lower().strip()
    exist = existing_title.lower().strip()

    if cand == exist:
        return True
    if len(cand) > 10 and len(exist) > 10:
        if cand in exist or exist in cand:
            return True
    cand_words = set(cand.split())
    exist_words = set(exist.split())
    if not cand_words or not exist_words:
        return False
    common = cand_words & exist_words
    overlap_ratio = len(common) / max(len(cand_words), len(exist_words))
    return overlap_ratio >= 0.6


def main(title: str):
    try:
        cards = fetch_cards()
    except Exception as e:
        print(f"ERROR:fetch failed - {e}")
        sys.exit(2)

    for c in cards:
        if is_duplicate(title, c.get("title", "")):
            print(f"DUPLICATE:{c['id']}")
            return

    print("UNIQUE")


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print("Usage: check_kflow_duplicate.py <title>")
        sys.exit(1)
    main(" ".join(args))
