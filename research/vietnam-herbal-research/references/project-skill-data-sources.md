# Using Project Skills as Primary Data Sources

When web search engines (Google, Bing, DuckDuckGo) are blocked by CAPTCHA or bot detection, do NOT burn turns on workarounds immediately. First check whether the product/ingredient has an existing project skill with embedded data.

## Workflow (proven 09/2026, EZ80 competitor research)

1. **Identify the project umbrella**: Is the product from Kiềm Saphia, Vua Kiềm, or another project with a dedicated skill? Load the project skill first.

2. **Mine the skill for data**: Project skills like `kiem-saphia-product-docs` often contain:
   - Exact product specs (price, packaging, dosage, composition) from official catalogs
   - Patent numbers and legal status
   - Trial/verification results with real numbers
   - Competitor comparisons from past research tasks
   - Sheet/API data sources (Google Sheets IDs, Drive folders)

3. **Direct website crawl**: If the skill has gaps, crawl the company website directly (curl + User-Agent) — company websites rarely block curl. For Kiềm Saphia:
   - Homepage: `https://kiemsaphia.com` (WordPress, works with curl)
   - Product search: `https://kiemsaphia.com/?s=<product>` 
   - Product category: `https://kiemsaphia.com/san-pham/`

4. **Only then attempt workarounds**: If both skill and website lack data, fall back to:
   - Camofox browser (if running)
   - Hermes browser → DuckDuckGo direct (`browser_navigate` to DDG)
   - websosanh.vn (via curl, doesn't block)

## Pitfalls

- **EZ80 is NOT listed on kiemsaphia.com public site** — the search returns "Không tìm thấy kết quả". All EZ80 data lives in the project skill's catalog and sheet data, not on the public website. Don't assume a product has a public product page.
- **Don't re-search what's already in the skill**: Check the skill's linked files (`skill_view(name, file_path)`) before attempting web search. The `kiem-saphia-product-docs` skill has 9 reference files covering everything from TCCS criteria to detailed case studies.
- **SearXNG local search**: Often not running. Check once (`curl --connect-timeout 3 http://127.0.0.1:8888/search?q=test&format=json`), if HTTP 000 skip immediately.
- **Competitor pricing is rarely on company websites**: Use the skill's existing competitor data (zeolite 5-15K/kg, bentonite 4-12K/kg) rather than trying to scrape pricing from supplier sites.
