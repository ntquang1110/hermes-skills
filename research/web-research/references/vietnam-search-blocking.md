# Vietnamese-Domain Search Blocking Patterns

Case study from session 2026-07-27: researching heavy metal analyzers in soil — pricing and supplier info for Vietnamese market.

## The Problem

Standard search engines and e-commerce platforms block most automated requests when searching for Vietnamese-market technical/industrial products.

## Blocking Matrix

| Target | Method | Result | Notes |
|--------|--------|--------|-------|
| Google (`google.com/search?q=...`) | curl / Jina / Browser | ❌ CAPTCHA (google.com/sorry) | Most aggressive. Blocks anonymous IPs instantly. |
| Bing Web Search | Browser / curl | ❌ CAPTCHA / irrelevant results | Returns "PortableApps" for "portable heavy metal analyzer", "May" (month) for "máy", "heavy.com" (sports) for "heavy metal". Intent matching broken for technical queries. |
| DuckDuckGo (lite/html) | Browser | ❌ CAPTCHA checkbox | DDG lite triggers checkbox challenge after a few queries. |
| Shopee.vn | Browser | ⚠️ Empty page | Blocks automated browser sessions. No search results rendered. |
| Tiki.vn | Browser | ❌ Empty page | Full JS SPA, blocks headless browsers. |
| Lazada.vn | Browser | ❌ (not tested) | Likely similar protection. |
| Alibaba.com | curl / Jina | ❌ CAPTCHA / 403 | Abusive traffic detection. |
| AliExpress.com | curl / Jina | ❌ CAPTCHA | "Please slide to verify" slider. |
| 1688.com | Browser | ❌ (likely blocked) | Chinese CAPTCHA (滑块验证). |

## What Partially Works

| Approach | Notes |
|----------|-------|
| **Direct URL via Jina AI Reader** (`r.jina.ai/<known-supplier-site>`) | Bypasses if you already know the domain and URL path. Cannot discover new suppliers this way — only read content from URLs you already have. |
| **Bing News** (`bing.com/news/search?q=...`) | Works for news articles (less aggressive blocking). Useless for product pricing. |
| **Direct browser to known supplier homepage** | May render — depends on the site's JS complexity and anti-bot measures. |
| **User-provided URLs** | Most reliable. If user gives a specific Shopee/Tiki/product page URL, Jina or browser can often read it. |

## The Honest-Reporting Rule

When ALL search methods are blocked and no real pricing data can be obtained:

1. **DO NOT fabricate or estimate prices** from general knowledge, international articles, or "industry average"
2. **DO NOT use "~X-Y triệu" ranges** without a verifiable source link
3. **Clearly separate** what was verified (technology comparisons, specs, trade-offs) vs what could not be verified (pricing, availability, stock)
4. **Tell the user explicitly**: which sites blocked you, what you couldn't retrieve, and recommend they check directly (Shopee, call suppliers, etc.)
5. **The final output should contain only data with source links** for everything — fewer items with verified sources is better than more items with fabricated data

## Pattern Template

When the user asks you to research Vietnamese-market pricing/suppliers:

1. Try direct approach first: known supplier websites via Jina (`r.jina.ai/https://<known-site>`)
2. If no known URLs: try Bing Search — if it returns irrelevant results (sports/months/gaming) → Bing is broken for this query, abandon
3. Try Shopee/Tiki via browser — if empty page → e-commerce blocks, abandon
4. **Stop here.** Report the blocking to the user. Do NOT substitute fabricated data.
5. Offer to analyze the user's own findings (links they provide) against technical specs instead.
