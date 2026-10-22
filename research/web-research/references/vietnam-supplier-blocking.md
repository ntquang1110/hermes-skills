# Vietnamese Supplier & E-commerce Site Blocking Patterns

Case study from session 2026-07-27: researching handheld heavy metal soil analyzers (Hach DR1900, XRF, ASV) for a Vietnamese buyer. Budget 50tr VND, deadline 1 week.

## Blocking Test Results

| Site | Method Used | Result | Mechanism |
|------|-------------|--------|-----------|
| Google (search) | `browser_navigate`, `r.jina.ai` | ❌ CAPTCHA blocked | IP-based JS challenge |
| Bing (web search) | `browser_navigate`, `r.jina.ai` | ❌ Wrong results (Vietnamese "máy" → "May" month; "portable" → PortableApps; "heavy metal" → sports site) | Intent matching failure for VN technical terms |
| Bing News | `browser_navigate` | ⚠️ Sparse, no relevant results | Not blocked but useless for technical VN queries |
| Bing Shopping | `browser_navigate` | ❌ No results found | Bot detection |
| DuckDuckGo (html) | `browser_navigate` | ❌ CAPTCHA checkbox | IP-based |
| DuckDuckGo (lite) | `browser_navigate` | ❌ CAPTCHA checkbox | IP-based |
| Shopee | `browser_navigate` | ❌ Empty page | Browser fingerprinting + IP reputation |
| Tiki | `browser_navigate` | ❌ Empty page | Bot detection |
| Lazada | Not tested | Likely blocked | Assumed same |
| Alibaba | `r.jina.ai` | ❌ 403 AbuseAlleviationError | Cloudflare + IP block |
| AliExpress | `r.jina.ai` | ❌ "Captcha Interception" | Slide verification |
| eBay | `browser_navigate` | ⚠️ Error page | Understood but limited |
| 1688.com | Not tested | Likely blocked | Assumed same |
| LabVIETCHEM (VN site) | `r.jina.ai` | ✅ Homepage accessible | Static Laravel site, search returns 404 |
| maydochuyendung.com | `r.jina.ai` | ✅ Homepage + search accessible | Static site, but doesn't carry analytical equipment |
| thietbikhoahoc.com.vn | `r.jina.ai` | ⚠️ 404 for product pages | Site-specific URL structure unknown |
| harpersurveying.com | `r.jina.ai` | ✅ Full article retrieved | Cloudflare bypassed by Jina |

## Bing Mistranslation Pattern

Bing's query understanding for Vietnamese technical terms is fundamentally broken:

| Vietnamese query | What Bing returns | Root cause |
|-----------------|-------------------|------------|
| "máy XRF" → "May XRF" | Wikipedia page for month of May | "máy" (machine) → "May" (month) |
| "máy đo kim loại nặng" | Online calculators, Điện máy Xanh | "máy" → calculator/electronics |
| "portable heavy metal analyzer" | PortableApps.com, gaming handhelds | "portable" → portable software |
| "heavy metal" + "soil" | Heavy.com sports news | "heavy" → sports brand |

**Lesson:** Do NOT use Bing for Vietnamese technical or product research. Results will be useless.

## Jina AI Reader Behavior

- `r.jina.ai/<URL>` bypasses Cloudflare on many static sites
- Gets 403 from Google properties, Alibaba, and any site using Cloudflare bot management
- Returns "Captcha Interception" from AliExpress
- Cannot render JS SPAs (Vue/React)
- Has rate limits for Google
- **Works on:** Static company websites, English-language tech articles, news sites
- **Fails on:** E-commerce sites, search engines, Chinese platforms

## Browser Tool Behavior

The Hermes `browser_navigate` tool runs a real Chromium instance with:

- `stealth_features: ["local"]` — basic evasion (navigator.webdriver=false, etc.)
- **No residential proxy** — datacenter IP detected by most bot protection
- Browserbase provider with upgradable stealth

**Limitation:** Even a real browser with basic stealth gets blocked by Shopee/Tiki/Alibaba because:
1. Datacenter IP triggers CAPTCHA
2. Missing cookies/localStorage (no browsing history)
3. Suspicious behavior (no mouse movements, instant navigation)

## Solutions (in priority order)

### 1. Enable Browserbase Residential Proxy (config change)

```yaml
# In ~/.hermes/config.yaml
browser:
  provider: browserbase  # default
  # proxy: residential   ← UNCOMMENT to enable
  # stealth: full        ← UNCOMMENT to enable full stealth mode
```

Apply with:
```bash
hermes config set browser.stealth full
hermes config set browser.proxy residential
```

**Effect:** Residential IP → bypass most CAPTCHAs. Full stealth → hide fingerprint. Requires paid Browserbase plan (~$20-50/mo).

### 2. SERP APIs (paid, reliable)

| API | Cost | Query volume | Notes |
|-----|------|-------------|-------|
| Serper.dev (Google) | $50/mo | 50k queries | Returns real Google results via API |
| Azure Bing Search | ~$7/1k calls | Pay as you go | Official API, not blocked |
| ScrapingBee | $49/mo | Handle proxy+CAPTCHA | Full scraping, not just search |
| ScraperAPI | $49/mo | 5k API credits | Proxy rotation included |

### 3. Direct Site Access Strategy

Instead of searching (which is blocked), go straight to known sources:

1. **Find NCC website URLs** from previous research or user-provided links
2. **Navigate directly** with `browser_navigate` to product/category pages
3. **Use Google Cached** pages: `https://webcache.googleusercontent.com/search?q=cache:<URL>`
4. **Ask user for specific links** they found themselves

### 4. Facebook / Social Media

Many Vietnamese suppliers sell through Facebook groups. To search:
- Ask user: "Anh có biết group Facebook nào về [ngành] không?"
- Search on Facebook directly (if accessible)

## Reporting When Blocked

Template format when a research target is blocked:

```
🔴 [Site] bị chặn — [reason]

[Site] trả về CAPTCHA/trang trống do [mechanism].
Em không lấy được [giá/thông số] từ kênh này.

Giải pháp:
- Anh tự check trên [Shopee/Tiki/website] với từ khóa "[keyword]"
- Hoặc gọi [NCC] theo số [phone]
- Hoặc nếu anh có link cụ thể, em vào thẳng link đó
```
