#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Search web qua Camofox + DuckDuckGo — dùng khi Google/Bing chặn bot.
Verified 08/2026: DDG hoạt động qua Camofox browser, còn html.duckduckgo.com (lite/html) qua curl bị chặn.

Usage:
  python camsearch.py "<query>" [num_results]
  # hoặc import: from camsearch import search_ddg, page_text

Requires: Camofox server chạy tại http://localhost:9377 (node server.js, background).
"""
import json, sys, time, urllib.parse, urllib.request

BASE = "http://localhost:9377"
USER = "pricer"  # userId riêng — tránh bị Hermes browser client chiếm tab


def api(method, path, body=None):
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(BASE + path, data=data, method=method,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read().decode())


def new_tab(url="https://duckduckgo.com"):
    """Tạo tab mới — KHÔNG dùng tab cũ (tab chết sau restart server trả 410 Gone)."""
    r = api("POST", "/tabs", {"userId": USER, "sessionKey": "research", "url": url})
    return r["tabId"]


def nav(tab, url):
    return api("POST", f"/tabs/{tab}/navigate", {"userId": USER, "url": url})


def evaljs(tab, expr):
    r = api("POST", f"/tabs/{tab}/evaluate", {"userId": USER, "expression": expr})
    return r.get("result") if isinstance(r, dict) else r


def search_ddg(query, num=10):
    """Search DuckDuckGo, trả list {u: url, t: title}. Mở tab mới mỗi lần gọi."""
    tab = new_tab()
    q = urllib.parse.quote(query)
    nav(tab, f"https://duckduckgo.com/?q={q}&ia=web")
    time.sleep(4)
    expr = """
    (() => {
      const out = [];
      document.querySelectorAll('a').forEach(a => {
        const h = a.getAttribute('href') || '';
        if (h.startsWith('http') && !h.includes('duckduckgo.com') && !h.includes('duck.co')) {
          const t = (a.innerText || '').trim();
          if (t.length > 8) out.push({u: h, t: t.slice(0,160)});
        }
      });
      const seen = new Set(); const res = [];
      for (const o of out) { if (!seen.has(o.u)) { seen.add(o.u); res.push(o); } }
      return res.slice(0, 25);
    })()
    """
    res = evaljs(tab, expr)
    return res if isinstance(res, list) else []


def page_text(url, wait=4, maxlen=6000):
    """Mở 1 URL và trả innerText (trích giá/số liệu từ trang kết quả)."""
    tab = new_tab()
    nav(tab, url)
    time.sleep(wait)
    r = evaljs(tab, f'document.body ? document.body.innerText.slice(0,{maxlen}) : "NO BODY"')
    return r if isinstance(r, str) else str(r)


if __name__ == "__main__":
    q = sys.argv[1]
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    results = search_ddg(q, n)
    if results:
        for i, r in enumerate(results[:n], 1):
            print(f"{i}. {r.get('t','')[:110]}")
            print(f"   {r.get('u','')[:170]}")
    else:
        print("NO RESULTS — kiểm tra Camofox server (curl -s http://localhost:9377/)")
