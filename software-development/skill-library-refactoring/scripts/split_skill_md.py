#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Losslessly split an oversized SKILL.md into a router SKILL.md + references/*.md.

A SKILL.md past ~20k chars should progressively disclose bulky sections into
references/. Editing that by hand risks silent information loss, so this script
moves chunks byte-for-byte with code and then PROVES the move was lossless.

Usage
-----
python split_skill_md.py path/to/SKILL.md \
  --move 'START_PREFIX|END|ref-name.md|short description' [--move ...] \
  [--refs-dir references] [--index] [--dry-run]

START_PREFIX : exact line prefix that starts the section (include '## '/'### ').
END          : exact line prefix of the first line to KEEP (exclusive),
               or the token NEXT_H2 (next '## ' heading) or EOF.
ref-name.md  : file to create under --refs-dir (must not already exist)
description  : optional; appended to the router line inside SKILL.md

Moved text is copied verbatim (same bytes, same line endings) to
<refs-dir>/<ref-name.md>. SKILL.md keeps the original heading line plus a
2-3 line router block pointing at the new file.

Verification (exit 0 only if all pass):
  V1 each ref file is byte-identical to the chunk it replaced
  V2 original == inline-remainder + ref file contents (nothing dropped/added)
  V3 every h1-h4 heading of the original still exists in SKILL.md or a ref file

A timestamped backup (SKILL.md.bak-<ts>) is written next to SKILL.md first.
"""
from __future__ import annotations

import argparse
import os
import re
import shutil
import sys
import time

HEADING = re.compile(r'^#{1,4} ')


def headings(text):
    return [l.rstrip('\r\n') for l in text.splitlines() if HEADING.match(l)]


def find_unique(lines, prefix, what):
    hits = [i for i, l in enumerate(lines) if l.startswith(prefix)]
    if len(hits) != 1:
        sys.exit(f'ERROR: {what} prefix {prefix!r} matched {len(hits)} lines (need exactly 1)')
    return hits[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('skill_md')
    ap.add_argument('--move', action='append', default=[], metavar='START|END|REF|DESC')
    ap.add_argument('--refs-dir', default='references')
    ap.add_argument('--index', action='store_true',
                    help='append a References index section listing refs-dir')
    ap.add_argument('--dry-run', action='store_true', help='report only, change nothing')
    args = ap.parse_args()

    path = os.path.abspath(args.skill_md)
    base = os.path.dirname(path)
    refdir = os.path.join(base, args.refs_dir)
    if not args.move:
        sys.exit('ERROR: pass at least one --move')

    raw = open(path, 'rb').read()
    text = raw.decode('utf-8')
    nl = '\r\n' if '\r\n' in text else '\n'
    lines = text.splitlines(keepends=True)

    moves = []
    for spec in args.move:
        start_p, end_p, ref, desc = (spec.split('|') + ['', '', ''])[:4]
        if not ref:
            sys.exit(f'ERROR: bad --move {spec!r} (need START|END|ref.md|desc)')
        s = find_unique(lines, start_p, 'start')
        if end_p == 'NEXT_H2':
            e = next((i for i in range(s + 1, len(lines))
                      if lines[i].startswith('## ') and not lines[i].startswith('### ')), None)
            if e is None:
                sys.exit(f'ERROR: no next ## heading after {start_p!r}')
        elif end_p == 'EOF':
            e = len(lines)
        else:
            e = find_unique(lines, end_p, 'end')
        if e <= s:
            sys.exit(f'ERROR: end before start for {spec!r}')
        ref_path = os.path.join(refdir, ref)
        if os.path.exists(ref_path):
            sys.exit(f'ERROR: {ref_path} already exists - pick another name')
        moves.append(dict(start=s, end=e, ref=ref, desc=desc))

    moves.sort(key=lambda m: m['start'])
    for a, b in zip(moves, moves[1:]):
        if b['start'] < a['end']:
            sys.exit(f"ERROR: overlapping moves ({a['ref']}, {b['ref']})")

    routers, chunks, out, cursor = [], [], [], 0
    for m in moves:
        chunk = ''.join(lines[m['start']:m['end']])
        chunks.append((m['ref'], chunk))
        pointer = f"Chi tiết: `references/{m['ref']}`"
        if m['desc']:
            pointer += f" — {m['desc']}"
        router = lines[m['start']] + nl + pointer + nl + nl + '---' + nl + nl
        routers.append(router)
        out.append(''.join(lines[cursor:m['start']]))
        out.append(router)
        cursor = m['end']
    out.append(''.join(lines[cursor:]))
    new_text = ''.join(out)

    index_text = ''
    if args.index:
        ref_files = (sorted(f for f in os.listdir(refdir) if f.endswith('.md'))
                     if os.path.isdir(refdir) else [m['ref'] for m in moves])
        index_text = nl + '## References — chi tiết tách riêng' + nl + nl
        index_text += ''.join(f'- `references/{f}`' + nl for f in ref_files)
        new_text += index_text

    # ---- verify in memory BEFORE touching the filesystem ----
    orig_minus = text
    for ref, chunk in chunks:
        if orig_minus.count(chunk) != 1:
            sys.exit(f'ERROR: chunk for {ref} is not unique in the original')
        orig_minus = orig_minus.replace(chunk, '', 1)

    core = new_text
    for r in routers:
        if r not in core:
            sys.exit('ERROR: internal - router block missing from output')
        core = core.replace(r, '', 1)
    if index_text:
        core = core[:core.index(index_text)]

    ok2 = core == orig_minus
    pool = headings(new_text)
    for _, chunk in chunks:
        pool += headings(chunk)
    missing = []
    for h in headings(text):
        if h in pool:
            pool.remove(h)
        else:
            missing.append(h)
    ok3 = not missing

    print(f'SKILL.md: {len(raw)} -> {len(new_text.encode("utf-8"))} bytes')
    for ref, chunk in chunks:
        print(f"  moved -> {os.path.join(args.refs_dir, ref)}: {len(chunk.encode('utf-8'))} bytes")
    print('V2 reconstruct-lossless:', ok2)
    print('V3 headings preserved:', ok3, (f'missing: {missing}' if missing else ''))
    if not (ok2 and ok3):
        sys.exit('FAILED verification - nothing written')
    if args.dry_run:
        print('dry-run: nothing written')
        return

    os.makedirs(refdir, exist_ok=True)
    for ref, chunk in chunks:
        with open(os.path.join(refdir, ref), 'wb') as f:
            f.write(chunk.encode('utf-8'))

    bak = path + '.bak-' + time.strftime('%Y%m%d-%H%M%S')
    shutil.copy2(path, bak)
    # never open the target with 'wb' directly: that truncates the file before
    # encode() can fail. Build bytes, write a temp file, then replace atomically.
    tmp = path + '.tmp'
    with open(tmp, 'wb') as f:
        f.write(new_text.encode('utf-8'))
    os.replace(tmp, path)

    for ref, chunk in chunks:  # V1
        on_disk = open(os.path.join(refdir, ref), 'rb').read()
        if on_disk != chunk.encode('utf-8'):
            sys.exit(f'FAILED V1: {ref} differs from its original chunk')
    print('V1 refs byte-identical: True')
    print('backup:', bak)
    print('DONE')


if __name__ == '__main__':
    main()
