# DDG Lite search probe — complete working pattern with CAPTCHA detection.
# ⚠️ As of mid-2026, lite.duckduckgo.com consistently returns CAPTCHA pages
# ("select all squares containing a duck") from automated environments.
# Treat this as a FIRST PROBE only — expect to fall through to Wikipedia API
# (Level 2a) at the first sign of CAPTCHA.
#
# Usage:
#   from ddg_lite_search import ddg_search
#   r = ddg_search('your query')
#   if r.get('captcha'): ...skip to Wikipedia API...
#   for hit in r['results'][:5]: print(hit['title'], hit['url'])
#
# Rate limits: DDG Lite silently returns 0 results after ~4-6 rapid queries.
# Always time.sleep(2) between queries when doing more than 3 searches.
# Keep queries short (3-6 words, <80 chars) — longer queries fail silently.

import urllib.request, urllib.parse, re, ssl

ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE


def ddg_search(query):
    data = urllib.parse.urlencode({'q': query}).encode()
    req = urllib.request.Request(
        'https://lite.duckduckgo.com/lite/',
        data=data,
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    )
    resp = urllib.request.urlopen(req, context=ssl_ctx, timeout=15)
    html = resp.read().decode('utf-8', errors='replace')
    # Detect CAPTCHA early
    if 'anomaly-modal' in html:
        return {'captcha': True, 'results': []}
    # Extract links
    links = re.findall(
        r'<a rel="nofollow" href="(https?://[^"]+)" class=.result-link.>(.*?)</a>',
        html, re.DOTALL
    )
    # Extract snippets
    snippets = re.findall(r'class=.result-snippet.>(.*?)</td>', html, re.DOTALL)
    results = []
    for i, (url, title) in enumerate(links):
        t = re.sub(r'<[^>]+>', '', title).strip()
        s = re.sub(r'<[^>]+>', '', snippets[i]).strip() if i < len(snippets) else ''
        results.append({'title': t, 'url': url, 'snippet': s})
    return {'captcha': False, 'results': results}


def batch_search(queries):
    """Batch several queries with pacing (avoids silent rate-limiting)."""
    import time
    for q in queries:
        result = ddg_search(q)
        if result.get('captcha'):
            print(f'=== {q} === [CAPTCHA BLOCKED — skip to Wikipedia API]')
            break
        for r in result.get('results', [])[:5]:
            print(f'  {r["title"]}')
            print(f'  {r["snippet"][:200]}')
        time.sleep(2)  # ← CRITICAL: avoid silent rate-limiting
