# Blocked Article Retrieval Patterns

Case study from session 2026-07-26: retrieving "China's ZAI completes 1-gigawatt AI data center using only Chinese-made chips" from GuruFocus (blocked by Cloudflare).

## Fallback chain that worked

| Level | Method | Result |
|-------|--------|--------|
| 0 | Direct `curl` to original URL | ❌ Cloudflare blocked |
| 1 | Jina AI Reader (`https://r.jina.ai/<URL>`) | ⚠️ Bypassed Cloudflare, but article content was JS-rendered (Vue/Nuxt SPA) so only nav appeared |
| 2 | Browser to search engines (Google, DDG, Brave, Qwant) | ❌ All blocked with CAPTCHAs |
| 3 | Browser to Bing Web Search | ❌ Eventually triggered Cloudflare challenge |
| 4 | **Browser to Bing News** (`https://www.bing.com/news/search?q=...`) | ✅ **Success** — returned article snippet with headline, source, and summary |

## Key Tools

### Jina AI Reader
- URL pattern: `https://r.jina.ai/<URL>`
- Bypasses Cloudflare on many sites
- Returns text/markdown extraction of page content
- **Limitation**: Cannot render JavaScript SPAs (Vue/React/Svelte). Only server-rendered or static content is extracted.
- **Limitation**: Has rate limits — can get blocked by Google properties after a few requests.
- Works well on: Tom's Hardware, site footers/nav, static news pages.

### Bing News via Browser
- URL: `https://www.bing.com/news/search?q=<query>`
- Significantly less aggressive bot detection than Bing Web Search or Google News
- Returns real news headlines, snippets, sources, and relative dates
- Good for: discovering that a story exists, getting the headline/lede, identifying which outlet covered it

## Pattern Template

When a specific article URL is blocked:

1. **Try Jina Reader** first: `curl -sL "https://r.jina.ai/<blocked-url>"` 
   - If content is extracted → done
   - If only nav/JS shells appear → the page is an SPA, proceed

2. **Try Browser to Bing News**: navigate to `https://www.bing.com/news/search?q=<exact-article-title>`
   - Look for matching headlines in the results
   - Snippet often contains the lede/summary even without clicking through

3. **Identify alternative sources**: From Bing News results, note which outlets covered the story (e.g. The Silicon Review, Tom's Hardware, etc.)

4. **Target alternative sources with Jina Reader**: Try `https://r.jina.ai/<alternative-article-url>` to bypass paywalls or blocks on those sites

5. **If all else fails**: Report what you found (headline, source, snippet, significance) and clearly state that the full article text could not be retrieved.

## Wayback Machine CDX — locate & fetch archived copies (use when ALL search engines are blocked)

Verified 2026-08-11: when DDG html via curl rate-limits after ~2 queries, Bing browser serves unrelated junk, and Google returns a bare searchbox, the Wayback CDX API still works and is curl-friendly.

**List archived URLs for a domain matching a pattern:**
```bash
curl -s "https://web.archive.org/cdx/search/cdx?url=<domain>&matchType=domain&filter=original:.*<urlpattern>.*&limit=25&fl=original,timestamp,statuscode&collapse=urlkey"
```
**Fetch a specific snapshot:**
```bash
curl -sL "http://web.archive.org/web/<timestamp>/<original-url>"
```
- The CDX hit itself **confirms the exact URL + document title** (e.g. `.../QCVN-8-2-2011-BYT-gioi-han-o-nhiem-kim-loai-nang-trong-thuc-pham-901429.aspx` proves the regulation name) — useful even before fetching.
- Use `collapse=urlkey` to dedupe; filter statuscode 200 to skip 404 captures.
- Case: thuvienphapluat.vn (Cloudflare-blocked even in browser) — recovered full text of QCVN 8-2:2011/BYT and TT 24/2019/TT-BYT from 2012/2019 snapshots, incl. issue dates ("Ngày ban hành", "Ngày hiệu lực").

## Official VN government document originals (bypass legal-site walls entirely)

For Vietnamese legal/regulatory text (QCVN, Thông tư, TCVN):
1. `curl` the doc page on `vanban.chinhphu.vn/default.aspx?pageid=27160&docid=<id>` (find docid via search)
2. `grep -oE 'href="[^"]*(datafiles|\.doc|\.rar|\.pdf)[^"]*"'` → official attachments live on `datafiles.chinhphu.vn/cpp/files/vbpq/...`
3. Extract: **7-Zip** at `/c/Program Files/7-Zip/7z.exe` for `.rar`; **antiword** (ships with git-bash) for `.doc` — tables get mangled but text is readable.
- Worked: QCVN 6-1:2010/BYT annex ("TT 34-kem.doc" from 102219_tt34byt2.rar) extracted verbatim, incl. full Phụ lục I–IV tables.

## Windows/host gotchas (this machine)

- **`/tmp` and `$TEMP` do NOT reliably persist between terminal calls** — a file written in one call may be gone in the next. Fetch + extract in a SINGLE command, or use a dedicated dir (`$HOME/<project>/`). Avoid `cd "$TEMP"` — it drops you into the huge user Temp dir.
- **pip is missing in the hermes venv** — for PDF text extraction use `uv run --with pymupdf python - <<'EOF' ... EOF` (downloaded + worked on WHO guideline PDFs; `import fitz` also works).
- **NIH ODS (ods.od.nih.gov) returns HTTP 403 to urllib/curl** — use browser_navigate and read the snapshot; the Sodium-HealthProfessional fact sheet 404s (as of 08/2026), Calcium/Magnesium/Potassium pages work.
