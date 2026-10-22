#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extract article body from nav-heavy Vietnamese news HTML (vietnamnet, kenh14, 24h...).
Whole-page tag-stripping on these sites returns nav/footer junk; the reliable pattern is:
find <h1>, then collect <p> tags AFTER it.
Usage: python extract_vn_article.py file.html [max_chars]
"""
import re, html, sys


def extract(path, minlen=120):
    raw = open(path, encoding="utf-8", errors="ignore").read()
    m = re.search(r'<h1[^>]*>(.*?)</h1>', raw, re.S)
    h1 = re.sub(r'<[^>]+>', '', m.group(1)) if m else ""
    start = m.end() if m else 0
    paras = re.findall(r'<p[^>]*>(.*?)</p>', raw[start:], re.S)
    out = [html.unescape(h1).strip()]
    for p in paras:
        t = html.unescape(re.sub(r'<[^>]+>', '', p)).strip()
        if len(t) >= minlen // 4:
            out.append(t)
    return "\n\n".join(out)


if __name__ == "__main__":
    body = extract(sys.argv[1])
    print(body[: int(sys.argv[2]) if len(sys.argv) > 2 else 8000])
