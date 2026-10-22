#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DuckDuckGo search qua POST — chạy được khi GET bị challenge (HTTP 202).

Vì sao: ddg GET `html.duckduckgo.com/html/?q=...` từ urllib/curl trả **202 + trang
challenge** (0 kết quả), nhưng **POST form `q=`** tới cùng endpoint với UA trình
duyệt trả **200 + 10 kết quả parse được**. Đã verify 09/2026 cho query tiếng Việt
(giá thuốc sát trùng, giá xút, giá vôi).

Rate limit: sau ~8–10 query liên tiếp DDG bắt đầu trả **0 kết quả** (không báo lỗi).
→ sleep **10–12 s** giữa các query khi chạy batch. Nếu vẫn 0, fallback:
Hermes browser → `https://duckduckgo.com/?q=<urlencoded>&ia=web` (đọc snapshot),
hoặc lấy snippet trực tiếp từ trang nhà cung cấp qua `fetch2.py`.

Usage:
    python ddg_search.py "query 1" "query 2" ...      # in title/url/snippet
    # import:  from ddg_search import ddg, strip
"""
import sys, re, json, gzip, time, html as _html, urllib.request, urllib.parse

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
SLEEP_BETWEEN = 11  # giây — dưới ngưỡng này DDG trả rỗng


def strip(h):
    h = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", h, flags=re.S | re.I)
    h = re.sub(r"<b>|</b>", "", h)
    h = re.sub(r"<[^>]+>", "", h)
    return re.sub(r"\s{2,}", " ", _html.unescape(h)).strip()


def ddg(q, tries=3, kl="vn-vi"):
    """Trả list {title,url,snippet}. Rỗng = bị rate limit → sleep rồi thử lại."""
    data = urllib.parse.urlencode({"q": q, "kl": kl}).encode()
    for _ in range(tries):
        try:
            req = urllib.request.Request(
                "https://html.duckduckgo.com/html/", data=data,
                headers={"User-Agent": UA,
                         "Content-Type": "application/x-www-form-urlencoded",
                         "Accept-Language": "vi,en;q=0.9",
                         "Accept-Encoding": "gzip"})
            with urllib.request.urlopen(req, timeout=30) as r:
                raw = r.read()
                if r.headers.get("Content-Encoding") == "gzip":
                    raw = gzip.decompress(raw)
                h = raw.decode("utf-8", "replace")
            out = []
            for m in re.finditer(
                r'<a rel="nofollow" class="result__a" href="([^"]+)">(.*?)</a>(.*?)(?=<a rel="nofollow" class="result__a"|</div>\s*</div>\s*$)',
                h, re.S):
                url = _html.unescape(m.group(1))
                if "uddg=" in url:                    # redirect wrapper
                    url = urllib.parse.unquote(url.split("uddg=")[1].split("&")[0])
                sm = re.search(r'class="result__snippet"[^>]*>(.*?)</a>', m.group(3), re.S)
                out.append({"title": strip(m.group(2)), "url": url,
                            "snippet": strip(sm.group(1))[:400] if sm else ""})
            if out:
                return out
        except Exception:
            pass
        time.sleep(6)
    return []


if __name__ == "__main__":
    for q in sys.argv[1:]:
        res = ddg(q)
        print("=== %s -> %d" % (q, len(res)))
        for x in res:
            print("  -", x["title"][:120])
            print("    ", x["url"][:160])
            if x["snippet"]:
                print("    >", x["snippet"][:250])
        time.sleep(SLEEP_BETWEEN)
