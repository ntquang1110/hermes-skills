# WordPress REST API Content Extraction

Extract structured content from WordPress websites using their native REST API. Bypasses HTML parsing of Elementor/block markup by fetching clean JSON data.

## When to Use

- User gives you a WordPress URL and asks you to scan/extract all content
- Need to separate knowledge content from company/press content
- Need to compile a site's knowledge base into a structured file (MD/HTML)
- CMS is WordPress (detect via `wp-json`, `wp-content`, generator meta tag)

## Workflow

### 1. Discover all URLs via sitemap

```bash
# WordPress generates wp-sitemap.xml automatically (Yoast SEO)
curl -sL "https://example.com/wp-sitemap.xml"

# Parse sitemap index to find per-type sitemaps
# Each sitemap has: <loc>https://example.com/wp-sitemap-posts-post-1.xml</loc>

# Extract all URLs from a sitemap
curl -sL "https://example.com/wp-sitemap-posts-post-1.xml" | grep -oP '<loc>\K[^<]+'
```

Sitemap categories to look for:
- `wp-sitemap-posts-post-1.xml` — blog/news posts
- `wp-sitemap-posts-page-1.xml` — pages
- `wp-sitemap-posts-{custom_type}-1.xml` — custom post types (cases, tips, jobs, etc.)
- `wp-sitemap-taxonomies-{taxonomy}-1.xml` — category/tag archives

### 2. Use REST API for clean data (NOT HTML scraping)

```bash
# API root
curl -sL "https://example.com/wp-json/wp/v2/"

# Available endpoints (check for custom post types)
curl -sL "https://example.com/wp-json/wp/v2/types"

# Fetch pages with minimal fields (faster, less bandwidth)
curl -sL "https://example.com/wp-json/wp/v2/pages?per_page=100&_fields=id,title,slug,link,date,content,excerpt"

# Fetch posts with pagination
curl -sL "https://example.com/wp-json/wp/v2/posts?per_page=100&page=1&_fields=id,title,slug,link,date,content,excerpt"

# Fetch custom post types
curl -sL "https://example.com/wp-json/wp/v2/cases?per_page=50&_fields=id,title,slug,link,content"
curl -sL "https://example.com/wp-json/wp/v2/tips-and-insights?per_page=50"
```

### 3. Filter company/press content from knowledge content

Build a keyword blocklist for press releases and company news:

```python
company_keywords = [
    'subsidiary', 'appoints new', 'establishes', 'strengthens position',
    'enters', 'delivers significant growth', 'shuts down',
    'expands in', 'opens a.i.', 'exports', 'ceo', 'cfo',
    'pressrelease', 'press-release', 'joint venture',
    'award', 'board of directors', 'new hq',
]

def is_company_content(post):
    text_check = (post['title']['rendered'] + ' ' + post['slug']).lower()
    return any(kw in text_check for kw in company_keywords)
```

### 4. Strip Elementor/Block HTML markup

WordPress REST API returns raw HTML including full Elementor markup. Strip it:

```python
import re, html

def strip_html(content):
    text = re.sub(r'<[^>]+>', ' ', content)
    text = html.unescape(text)
    text = re.sub(r'&nbsp;', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text
```

### 5. Handle multilingual sites (Polylang)

Many WP sites use Polylang for i18n. Add `&lang=en` to API calls:

```bash
curl -sL "https://example.com/wp-json/wp/v2/pages?slug=about-us&lang=en"
```

Without `&lang`, the API may return a random language version.

### 6. Token estimation

```python
# Rough estimate: 1 char ≈ 0.25-0.3 tokens for English
total_tokens = len(stripped_text) // 4

# But REST API returns ~50-100x more chars as raw HTML
# Strip first, then estimate
```

## Real Example: danbred.com

**Scale:** 1,277 URLs across 7 languages (EN: 533)

**Process:**
1. Get sitemap → find 76 sub-sitemaps
2. Identify custom post types: `cases`, `fact_sheets`, `webinars`, `tips-and-insights`, `jobs`, `herds`, `offices`, `link_cards`
3. Fetch EN pages (25) + breeds (4) = 29 key pages
4. Fetch EN posts (209) → filter to 174 knowledge articles (35 company posts skipped)
5. Fetch cases (12), fact sheets (5), tips (17)
6. Strip HTML, truncate long posts to 2,500 chars
7. Output: MD file (581 KB, ~147K tokens)
8. Optional: build Vietnamese HTML with SVG diagrams for visual summary

**Key numbers:**
- 209 total EN posts → 174 knowledge + 35 company/press
- ~450K chars stripped text (EN only)
- 6 languages other than EN (~744 URLs) — skip unless needed, content is translated

## Pitfalls

1. **REST API timeout:** Individual calls can be slow. Set `--max-time 15` on curl. Use short timeouts per post.
2. **Custom post types:** Not always exposed in the REST API by default. Check `/wp-json/wp/v2/types` first.
3. **Elementor markup:** Can be 50-100x the actual text content. Always strip before saving.
4. **Rate limiting:** Some WP hosts limit API calls. Add small delays between batch requests.
5. **Polylang slug collision:** The same slug may exist in multiple languages. Always specify `&lang=en`.
6. **Protected content:** Some pages may return empty content (password-protected, private). Check `protected: false` in response.
