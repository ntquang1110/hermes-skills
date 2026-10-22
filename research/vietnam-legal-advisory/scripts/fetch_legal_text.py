#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
fetch_legal_text.py — tải toàn văn văn bản pháp luật VN rồi strip thành text để grep/trích.

Usage:
    python fetch_legal_text.py <url> <outname>
    python fetch_legal_text.py <url> <name> m     # 'm' dùng mobile User-Agent

Output:
    <outname>.txt    text đã strip (grep theo số điều)
    <outname>.html   HTML gốc (để đối chiếu khi trích nguyên văn)

Nguồn ưu tiên (đã kiểm chứng 10/2026):
    https://hethongphapluat.com/<slug>            # trang index chứa TOÀN VĂN bộ luật
    https://hethongphapluat.com/<slug>/dieu-<N>    # từng điều

Sau khi tải, tìm thân điều (mỗi điều xuất hiện 2 lần — lần 1 là mục lục):
    import re
    lines = open(name + '.txt', encoding='utf-8').read().split('\n')
    hits = [i for i, l in enumerate(lines) if re.match(r'^Điều %d\\.\\s' % N, l)]
    print('\n'.join(lines[hits[-1]:hits[-1] + 25]))
"""

import sys
import re
import html
import urllib.request
import ssl

UA_DESK = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
           '(KHTML, like Gecko) Chrome/126.0 Safari/537.36')
UA_MOBILE = ('Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 '
             '(KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1')


def get(url, ua=UA_DESK, timeout=90):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request(url, headers={
        'User-Agent': ua,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'vi,en;q=0.8',
    })
    with urllib.request.urlopen(req, context=ctx, timeout=timeout) as f:
        raw = f.read()
    for enc in ('utf-8', 'utf-8-sig', 'latin-1'):
        try:
            return raw.decode(enc)
        except Exception:
            continue
    return raw.decode('utf-8', 'replace')


def strip(d):
    d = re.sub(r'(?is)<(script|style|noscript|svg).*?</\1>', ' ', d)
    d = re.sub(r'(?i)<br\s*/?>', '\n', d)
    d = re.sub(r'(?i)</(p|div|li|tr|h\d)>', '\n', d)
    d = re.sub(r'(?s)<[^>]+>', ' ', d)
    d = html.unescape(d)
    d = d.replace('\u00a0', ' ').replace('\u200b', '')
    lines = [re.sub(r'[ \t]+', ' ', l).strip() for l in d.split('\n')]
    out, prev = [], None
    for l in lines:
        if not l or l == prev:
            continue
        out.append(l)
        prev = l
    return '\n'.join(out)


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(2)
    url, name = sys.argv[1], sys.argv[2]
    ua = UA_MOBILE if len(sys.argv) > 3 and sys.argv[3] == 'm' else UA_DESK
    try:
        h = get(url, ua)
    except Exception as e:
        # KHÔNG im lặng bỏ qua — caller cần biết nguồn này hỏng để thử nguồn khác
        sys.stderr.write('FETCH_FAIL %s %s\n' % (url, e))
        sys.exit(1)
    t = strip(h)
    with open(name + '.txt', 'w', encoding='utf-8') as f:
        f.write(t)
    with open(name + '.html', 'w', encoding='utf-8') as f:
        f.write(h)
    print('OK %s %d chars %d lines' % (name, len(t), len(t.split('\n'))))


if __name__ == '__main__':
    main()