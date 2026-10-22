#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bing News search for Vietnamese queries (validated 8/2026).
Usage: python bing_news_search.py "query" [count]
Output: JSON list of {title, url, snippet}.
Why this endpoint: Bing *web* search tokenizes Vietnamese diacritics badly
("Phạm Nhật Vượng" -> surname results). The News endpoint + setlang=vi works.
"""
import re, html, json, sys, urllib.parse, urllib.request

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"


def bing_news(q, count=14, lang="vi"):
    url = ("https://www.bing.com/news/search?q=" + urllib.parse.quote(q)
           + "&setlang=" + lang + "&count=" + str(count))
    req = urllib.request.Request(url, headers={
        "User-Agent": UA,
        "Accept-Language": "vi-VN,vi;q=0.9,en;q=0.8",
    })
    raw = urllib.request.urlopen(req, timeout=25).read().decode("utf-8", "ignore")
    cards = []
    # Each news card: <a class="title" href=...>TITLE</a> ... <div class="snippet">...
    for m in re.finditer(
            r'<a[^>]*class="title"[^>]*href="([^"]+)"[^>]*>(.*?)</a>\s*(.*?)(?=<a[^>]*class="title"|$)',
            raw, re.S):
        u = m.group(1)
        t = re.sub(r'<[^>]+>', '', m.group(2))
        sn = re.search(r'class="snippet"[^>]*>(.*?)</div>', m.group(3), re.S)
        s = re.sub(r'<[^>]+>', '', sn.group(1)) if sn else ""
        cards.append({
            "title": html.unescape(t).strip()[:170],
            "url": u,
            "snippet": html.unescape(s).strip()[:300],
        })
    return cards


if __name__ == "__main__":
    q = sys.argv[1]
    count = int(sys.argv[2]) if len(sys.argv) > 2 else 14
    print(json.dumps(bing_news(q, count), ensure_ascii=False, indent=1))
