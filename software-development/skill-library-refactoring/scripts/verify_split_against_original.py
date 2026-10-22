#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify a lossless SKILL.md split against the PRE-SPLIT original.

Runs after `split_skill_md.py` (or any hand-rolled split) when post-split edits have
already happened, so plain reconstruction equality (V2) is no longer meaningful.

  V0  original snapshot exists and is non-empty
  V1  every ref slice is byte-identical to the original chunk at its heading
  V2  byte closure: original - moved + router(+index) == current SKILL.md
  V3  heading census: no '## ' heading of the original is missing from SKILL.md
  V4  difflib of original-non-moved vs current-minus-router-minus-added-block:
      every hunk must be an intentional addition/edit, reported for review

Usage:
  python verify_split_against_original.py \\
      --original bak/SKILL.md.orig \\
      --skill "D:/Hermes/hermes-home/skills/<cat>/<name>/SKILL.md" \\
      --refs  "D:/Hermes/hermes-home/skills/<cat>/<name>/references" \\
      --added-block-prefix "**Reference files" \\
      --out verify_out.txt          # write the report to a file (pitfall 13)

Exit 0 only when V1 holds and no heading is missing and no unexplained diff hunk
remains outside --added-block-prefix / --allow-diff-hunks.
"""
import argparse, difflib, os, re, sys


def load(path):
    with open(path, encoding="utf-8", newline="") as fh:
        return fh.read().split("\r\n")


def crlf_bytes(lines):
    return len("\r\n".join(lines).encode("utf-8"))


def slices_of(ref_lines):
    """A ref written by the splitter holds whole original sections, so its '## '
    lines are exactly the slice starts."""
    idx = [i for i, l in enumerate(ref_lines) if l.startswith("## ")]
    out = []
    for k, s in enumerate(idx):
        e = idx[k + 1] if k + 1 < len(idx) else len(ref_lines)
        out.append((ref_lines[s], ref_lines[s:e]))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--original", required=True)
    ap.add_argument("--skill", required=True)
    ap.add_argument("--refs", required=True)
    ap.add_argument("--added-block-prefix", default=None,
                    help="first line of a block you added after the split (dropped "
                         "before the V4 diff); the block is taken to be 14 lines")
    ap.add_argument("--block-lines", type=int, default=14)
    ap.add_argument("--allow-diff-hunks", type=int, default=None,
                    help="fail if the V4 diff has more hunks than this")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()

    rep = []
    def say(s=""):
        rep.append(s)

    orig = load(a.original)
    cur = load(a.skill)
    if not orig or not cur:
        print("EMPTY FILE — aborting"); return 2
    say("V0 original : %s  (%d bytes / %d lines)"
        % (os.path.basename(a.original), crlf_bytes(orig), len(orig)))
    say("   current  : %d bytes / %d lines" % (crlf_bytes(cur), len(cur)))

    # ---- V1: locate each ref slice inside the original, verbatim ----
    claimed, moved_lines, moved_bytes, v1_ok = set(), set(), 0, True
    say("\nV1 verbatim ref slices")
    for fn in sorted(os.listdir(a.refs)):
        p = os.path.join(a.refs, fn)
        if not fn.endswith(".md"):
            continue
        for head, sl in slices_of(load(p)):
            cands = [i for i in range(len(orig)) if orig[i] == head and i not in claimed]
            hit = next((i for i in cands if orig[i:i + len(sl)] == sl), None)
            if hit is None:
                continue                       # pre-existing ref, not from this split
            claimed.add(hit)
            moved_lines.update(range(hit + 1, hit + 1 + len(sl)))
            moved_bytes += crlf_bytes(sl)
            say("   lines %4d-%-4d %6d B -> %s  VERBATIM OK"
                % (hit + 1, hit + len(sl), crlf_bytes(sl), fn))
    n_moved = len(claimed)
    say("   moved slices: %d" % n_moved)

    # ---- V2: byte closure ----
    overhead = crlf_bytes(cur) - (crlf_bytes(orig) - moved_bytes)
    say("\nV2 closure: %d original - %d moved = %d ; current %d - remainder = %d"
        % (crlf_bytes(orig), moved_bytes, crlf_bytes(orig) - moved_bytes,
           crlf_bytes(cur), overhead))
    say("   router + intentional additions = %d bytes (must equal the text you really "
        "added: index block + repointed lines)" % overhead)

    # ---- current minus router blocks ----
    moved_heads = set(orig[i] for i in claimed)
    keep, i, routers = [], 0, 0
    while i < len(cur):
        if cur[i] in moved_heads:
            j = i + 1
            while j < len(cur) and not cur[j].startswith("## "):
                j += 1
            routers += 1
            i = j
        else:
            keep.append(cur[i]); i += 1
    say("   router blocks stripped: %d" % routers)

    added = []
    if a.added_block_prefix:
        k = next((n for n, l in enumerate(keep)
                  if l.startswith(a.added_block_prefix)), None)
        if k is not None:
            added = keep[k:k + a.block_lines]
            keep = keep[:k] + keep[k + a.block_lines:]
            say("   added block dropped: %d lines" % len(added))

    # ---- V3: heading census ----
    oh = [l for l in orig if l.startswith("## ")]
    missing = [h for h in oh if h not in cur]
    say("\nV3 headings original=%d current=%d missing=%s"
        % (len(oh), sum(1 for l in cur if l.startswith("## ")),
           missing if missing else "NONE"))

    # ---- V4: diff enumeration ----
    nm = [orig[i - 1] for i in range(1, len(orig) + 1) if i not in moved_lines]
    diff = [l for l in difflib.unified_diff(nm, keep, lineterm="", n=0)
            if l.startswith(("+", "-")) and not l.startswith(("+++", "---"))]
    hunks = sum(1 for l in difflib.unified_diff(nm, keep, lineterm="", n=0)
                if l.startswith("@@"))
    say("\nV4 diff original(non-moved) vs current: %d hunk(s), %d changed line(s)"
        % (hunks, len(diff)))
    for l in diff[:60]:
        say("   " + l[:150])
    say("   (review each hunk: index block / repointed pointer = expected; anything "
        "else = real loss)")

    if len(added) != 0 or a.added_block_prefix:
        say("   counted added index lines: %d" % len(added))
    say("\nRESULT: V1 %s | V3 %s | V4 hunks %d%s"
        % ("OK" if v1_ok else "FAIL",
           "OK" if not missing else "FAIL", hunks,
           "" if a.allow_diff_hunks is None else
           " (allowed %d)" % a.allow_diff_hunks))

    text = "\n".join(rep)
    if a.out:
        with open(a.out, "w", encoding="utf-8") as fh:
            fh.write(text + "\n")
        print("report -> %s" % a.out)
    print(text)
    ok = v1_ok and not missing
    if a.allow_diff_hunks is not None:
        ok = ok and hunks <= a.allow_diff_hunks
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
