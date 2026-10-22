#!/usr/bin/env python3
"""Helpers for splitting an oversized SKILL.md into a router + references/.

Modes
-----
  analyze <SKILL.md>
      Print file size and the line range + byte size of every `## ` section, so you can pick the
      large, rarely-needed sections to move into references/. Also lists `### ` sub-headings
      (further cut points).

  verify  <orig-SKILL.md.bak> <skill_dir>
      Zero-loss audit after a split: every non-empty line and every `## ` heading of the ORIGINAL
      must still exist somewhere in <skill_dir>/SKILL.md or <skill_dir>/references/*.md.
      Exits 1 if anything is missing.

Usage (Windows git-bash / POSIX alike)
-------------------------------------
  python scripts/skill_split_helpers.py analyze D:/path/to/skill/SKILL.md
  python scripts/skill_split_helpers.py verify D:/path/SKILL.md.orig.bak D:/path/to/skill

Line endings are normalised for comparison, so a CRLF/LF mismatch between the original and the
new files never produces a false failure.
"""
import glob
import os
import sys


def read_lines(path):
    """Raw bytes split on LF; CRLF originals keep a trailing \\r on each element."""
    with open(path, 'rb') as fh:
        return fh.read().split(b'\n')


def as_text(b):
    return b.rstrip(b'\r').decode('utf-8', 'replace')


def analyze(path):
    lines = read_lines(path)
    heads = [(i + 1, as_text(l)) for i, l in enumerate(lines) if l.startswith(b'## ')]
    if not heads:
        print("no '## ' headings found in %s" % path)
        return 1
    print("file : %s" % path)
    print("bytes: %d   lines: %d" % (os.path.getsize(path), len(lines) - 1))
    for i, (ln, txt) in enumerate(heads):
        end = heads[i + 1][0] - 1 if i + 1 < len(heads) else len(lines)
        size = len(b'\n'.join(lines[ln - 1:end]))
        print("%6d-%-6d %8d B   %s" % (ln, end, size, txt))
    pre = heads[0][0] - 1
    print("\npre-heading body (frontmatter + intro): lines 1-%d, %d B"
          % (pre, len(b'\n'.join(lines[:pre]))))
    subs = [(i + 1, as_text(l)) for i, l in enumerate(lines) if l.startswith(b'### ')]
    if subs:
        print("\nsub-headings (further cut points):")
        for ln, txt in subs:
            print("  %6d  %s" % (ln, txt))
    return 0


def verify(orig_path, skill_dir):
    if not os.path.isfile(orig_path):
        print("FAIL: original/backup not found -> %s" % orig_path)
        return 2
    skill_md = os.path.join(skill_dir, 'SKILL.md')
    if not os.path.isfile(skill_md):
        print("FAIL: SKILL.md not found -> %s" % skill_md)
        return 2

    orig = read_lines(orig_path)
    pool = set()
    scanned = []
    for path in glob.glob(os.path.join(skill_dir, 'references', '*.md')) + [skill_md]:
        scanned.append(path)
        for ln in read_lines(path):
            if ln.strip():
                pool.add(as_text(ln))

    missing_lines = [l for l in orig if l.strip() and as_text(l) not in pool]
    missing_heads = [l for l in orig if l.startswith(b'## ') and as_text(l) not in pool]
    total_lines = sum(1 for l in orig if l.strip())
    total_heads = sum(1 for l in orig if l.startswith(b'## '))

    print("scanned %d files under %s" % (len(scanned), skill_dir))
    print("original non-empty lines : %d" % total_lines)
    print("original '## ' headings : %d" % total_heads)
    print("lines lost               : %d" % len(missing_lines))
    print("headings lost            : %d" % len(missing_heads))
    for l in missing_heads:
        print("   HEADING MISSING:", as_text(l))
    for l in missing_lines[:20]:
        print("   LINE MISSING   :", as_text(l)[:160])
    if missing_lines or missing_heads:
        print("\nRESULT: LOSS DETECTED - do not report success")
        return 1
    print("\nRESULT: OK - no information lost")
    return 0


def main(argv):
    if len(argv) < 3:
        print(__doc__)
        return 2
    mode = argv[1]
    if mode == 'analyze':
        return analyze(argv[2])
    if mode == 'verify':
        if len(argv) < 4:
            print(__doc__)
            return 2
        return verify(argv[2], argv[3])
    print("unknown mode: %s\n" % mode)
    print(__doc__)
    return 2


if __name__ == '__main__':
    sys.exit(main(sys.argv))
