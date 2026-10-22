---
name: web-research
description: "Multi-strategy web research: search engine workarounds, market/supplier research, Vietnamese domain research, and fallback patterns when direct HTTP search is blocked."
version: 2.2.4
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [research, search, web, vietnam, supplier, market-research, scrape, fallback]
    related_skills: [spike, plan]
---

# Web Research

Use this skill when you need to gather information from the web — especially when standard search engines (Google, Bing, DuckDuckGo) block your direct HTTP requests with CAPTCHAs or bot detection.

## When to use

- Market research (pricing, suppliers, competitors)
- Finding Vietnamese companies and their contact info
- Product sourcing research
- Any situation where search engines return blocked/obfuscated content from direct `curl`, `urllib`, or `requests` calls

## Core challenge: search engine blocking

**Reference**: `references/scientific-literature-retrieval.md` — verified scientific citations via PubMed eutils curl + Wikipedia `--compressed`+UA workaround.
**Reference**: `references/vietnam-price-research.md` — VN giá thị trường: DDG HTML qua Camofox + curl site hóa chất VN; site sống/chết; regex trích giá; worked examples 8/2026.

**Reference**: `references/blocked-article-retrieval-patterns.md` — Cloudflare/JS-SPA fallbacks (Jina Reader, Bing News, Wayback CDX, VN gov originals). **Reference**: `references/vietnam-food-water-standards.md` — verified VN water/food QCVNs, WHO/NIH stats, PMIDs.

**Reference**: `references/kf-large-kb-and-pubmed-pitfalls.md` — large-KF `/api/cards` timeout workaround (background fetch), NCBI `RemoteDisconnected` backoff, topic-selection `esearch` count probe, ghost-topic content-mention scan, f-string backslash SyntaxError fix. Script: `scripts/kf_md_to_html.py` converts a KF card payload JSON to the Premium B/W/Y HTML for the delivery pipeline.

**Reference**: `references/vietnam-supplier-blocking.md` — blocking patterns specific to Vietnamese e-commerce, supplier, and search engine sites (Shopee, Tiki, Alibaba, Bing VN mistranslation, Google CAPTCHA) with tested workarounds and reporting templates.
**Reference**: `references/vietnam-search-blocking.md` — Vietnamese search/e-commerce blocking patterns (Google, Bing, Shopee, Tiki, Alibaba), and the honest-reporting fallback when all methods fail.



Google, Bing, and DuckDuckGo's main pages **all detect and block** non-browser HTTP requests coming from tool environments. Common symptoms:
- Return obfuscated JavaScript instead of search results
- CAPTCHA challenges ("select all squares with a duck")
- Empty HTML with `<noscript>` tags
- JSON responses with no actual results
- Bing matching dictionary definitions of query words instead of actual search results (e.g. "best" query returns dictionary entries for "best")

**Do not** retry the same search engine more than twice with different user agents — it won't help.

**DuckDuckGo Lite (lite.duckduckgo.com) is now consistently blocked by CAPTCHA** in most automated environments. As of mid-2026, queries to `lite.duckduckgo.com/lite/` from a tool environment return a "select all squares containing a duck" CAPTCHA, resulting in 0 results with no error. Treat DDG Lite as a **first probe only** — skip directly to **Level 2 (Wikipedia API)** at the first sign of CAPTCHA HTML.

### Scientific/medical shortcut: skip straight to APIs

For **scientific, medical, biological, or veterinary research**, skip all Level 1 approaches (DDG Lite, Bing, Playwright) and go directly to:

1. **Level 2a (Wikipedia MediaWiki Action API)** — search by keyword, get structured plain-text extracts from any Wikipedia language
2. **Level 2b (Wikipedia REST API)** — fetch page summaries and full HTML by known title
3. **Level 2c (PubMed NCBI E-utilities API)** — search peer-reviewed papers, fetch titles/authors/DOIs/abstracts with structured JSON

This combined approach is faster and more reliable than any search engine workaround for scientific topics. The Wikipedia API provides broad context; PubMed provides specific citations. Use them together — fetch Wikipedia summaries for background, then search PubMed for recent primary literature. See `references/pubmed-wikipedia-scientific-workflow.md` for the tested workflow pattern.

**Why skip DDG Lite for scientific topics?** Even when DDG Lite works (rare), its results for technical queries are shallow — it surfaces blog posts and news summaries, not peer-reviewed papers. PubMed returns structured citation data with DOIs, journals, and author lists that DDG cannot match.

## Strategy hierarchy (try in order)

**Level 1 — search engines (delegate_task → DDG Lite → curl → Bing → Playwright).** Full code, the tested Playwright platform matrix (YouTube/Bing News/Reddit work; TikTok/Facebook/X/DDG blocked), YouTube/Bing-News/Reddit extraction patterns, DDG query limits, site-coverage gaps, and pitfalls: `references/strategy-level-1-search-engines.md`
### Level 2: Direct site access

If you know specific websites, access them directly:

```python
# Python with urllib (works on many sites)
import urllib.request, ssl
ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE
headers = {"User-Agent": "Mozilla/5.0 ...", "Accept-Language": "vi-VN,vi;q=0.9"}
req = urllib.request.Request(url, headers=headers)
resp = urllib.request.urlopen(req, context=ssl_ctx, timeout=20)
html = resp.read().decode('utf-8', errors='replace')
```

**Anti-bot sites that DON'T work** with direct HTTP: most Vietnamese sites use Cloudflare/anti-bot too. Can try multiple domain variations.

**Level 2a/2b — Wikipedia APIs (BEST for topic discovery; never CAPTCHA-blocked).** Full code library — multi-language search, batch extract, `wiki_extract_by_pageid`/`wiki_extract_multi`, `find_deals_in_page`, deal/transaction context, Vietnamese Wikipedia queries — plus every pitfall (`exlimit` silently capped to 1, Greek/Unicode `titles=` failure, disambiguation/0-char extracts, shared Action+REST 429 bucket, stale pages): `references/strategy-level-2-wikipedia-apis.md`
Supporting: `references/wikipedia-mediawiki-api-research.md`, `references/wikipedia-api-research.md`, `references/wikipedia-parse-table-extraction.md` (structured `action=parse` + `section=` wikitable extraction).

**Level 2c — PubMed NCBI E-utilities (BEST for peer-reviewed literature; skip Level 1 for scientific topics).** Full three-endpoint workflow (esearch/esummary/efetch + scoped-abstract regex), multi-query-angle pattern, broad-topic noise trap, "no-review" disease-specific workaround, verified-PMID discipline, finance/economics Crossref DOI bank, sparse-literature triple fallback, the `scripts/kf-gap-analysis.py` DETECT/CHECK usage, and the complete E-utilities pitfall list (`RemoteDisconnected` backoff, field-tag bracket crash, f-string/`join()` SyntaxError, bash-loop variable scoping): `references/strategy-level-2c-pubmed-eutils.md`
Supporting: `references/pubmed-eutils-research.md`, `references/pubmed-wikipedia-scientific-workflow.md`, `references/pubmed-evidence-research.md`, `references/immunology-research-worked-example.md`, `references/porcine-sparse-literature-triple-fallback.md`, `references/crossref-finance-doi-bank.md`, `references/grpo-rl-llm-reasoning-roadmap.md`, `references/arxiv-pdf-fulltext-extraction.md`.

**Condensed reference bank index** (all files below `references/` directory):

| Roadmap file | PMIDs | Focus |
|-------------|-------|-------|
| `tgf-beta-smad-swine-roadmap.md` | 13 | TGF-β/SMAD in swine: pathway, SMAD family, feed additives, post-weaning |
| `nk-cell-swine-roadmap.md` | 13 | Porcine NK: CD16⁺CD8α⁺perforin⁺CD3⁻, Ly49/KIR, ADCC, PRRSV/ASFV |
| `porcine-amp-roadmap.md` | 18 | AMPs: cathelicidin, β-defensin pBD2/3/5, PR-39, protegrin, butyrate induction |
| `neutrophil-swine-roadmap.md` | 13 | Porcine neutrophils: CD markers, NETosis, S. suis, APP, Zn/butyrate |
| `bile-acid-fxr-tgr5-swine-roadmap.md` | 16 | Bile acids: hyocholic acid, FXR/TGR5, BSH-microbiota, VDR crosstalk |
| `vdr-swine-roadmap.md` | 14 | VDR: genomic/non-genomic, VDR-FXR heterodimer, PRV/PEDV/rotavirus |
| `tnf-tnfr-swine-roadmap.md` | 15 | TNF/TNFR: TNFR1→apoptosis, TNFR2→Treg, PRRSV/ASFV/PEDV/ETEC |
| `zearalenone-swine-roadmap.md` | 19 | ZEA: ERα, ER-phagy, ferroptosis, autophagy, 6-pathway diagram |
| `wnt-beta-catenin-swine-roadmap.md` | 16 | Wnt: destruction complex, ISC, glutamate→FZD7, TGEV/PEDV interactions |
| `notch-signaling-swine-roadmap.md` | 15 | Notch: juxtacrine, fringe, Atoh1/HES1, PEDV/TGEV, benzoic acid |
| `il1-family-swine-roadmap.md` | 22 | IL-1 family: 11 members, two-signal model, NLRP3, ETEC, PRRSV |
| `kynurenine-pathway-swine-roadmap.md` | 10 | KP: IDO1, CSFV/PRRSV hijacking, Trp→CaSR→defensin |
| `nod1-nod2-swine-roadmap.md` | 15 | NOD1/2: peptidoglycan sensing, RIPK2, 10 feed additive modulators |
| `immune-checkpoint-swine-roadmap.md` | 15 | PD-1/CTLA-4/CD28: T cell exhaustion, PRRSV, LEA29Y xenotransplant |
| `il17-family-swine-roadmap.md` | 8 | IL-17 family: IL-17A/F/C/D/E/25, Act1/TRAF6, ETEC/weaning |
| `tight-junction-swine-roadmap.md` | 21 | TJ: claudin, occludin, ZO-1, MLCK, 15 additives, 7 pathogens |
| `interferon-gamma-swine-roadmap.md` | 17 | IFN-γ: JAK-STAT/GAS, γδ T cells, M1, PRRSV/CSFV evasion |
| `ho-1-swine-roadmap.md` | 13 | HO-1: Nrf2/KEAP1, Bach1, biliverdin/CO/ferritin, rosemary/butyrate |
| `paneth-cell-swine-roadmap.md` | 16 | Paneth: AMP factory, ISC niche, TGEV/PEDV/DON, EGF/Zn |
| `goblet-cell-swine-roadmap.md` | 12 | Goblet cells: MUC2, PEDV/PDCoV, tryptophan→ILA→AHR, GOS |
| `hippo-yap-taz-swine-roadmap.md` | 20 | Hippo/YAP/TAZ: organ size, mechanotransduction, revSCs, GPR43→YAP |
| `swine-antigen-presentation-research.md` | 18 | Antigen presentation: MHC-I/II, SLA, TAP, PLC, NLRC5, CIITA, evasion |
| `porcine-rotavirus-swine-roadmap.md` | 32 | PoRVA: NSP4 enterotoxin, NSP1-IRF, G/P, CRISPR, vaccine; 0-hit query fix |
| `curcumin-phytochemical-roadmap.md` | 20 | Curcumin: 6 mechanisms (Nrf2, TLR4/NF-κB, TJ, Rho/ROCK, microbiota), IPEC-J2 + pig trials, ZnO alternative, piperine PK, 8 tested queries |
| `glycyrrhizin-phytochemical-roadmap.md` | 18 | Glycyrrhizin (cam thảo): HMGB1/TLR4, PRRSV penetration (in vitro ✓ / in vivo ✗ matrine), DON+GAP piglets, nursery 2026, coronavirus spike-RBD, pseudoaldosteronism 11β-HSD2, PK |
| `isg-swine-roadmap.md` | 22 | ISG effectors: Mx1, OAS/RNase L, PKR, ISG15, Viperin, BST2, CH25H; PRRSV/ASFV/PEDV/PDCoV evasion (Nsp11/Nsp1β/L11L); therapy (ISG15-IFN-λ3, 25HC, baicalin, probiotic→STING) |
| `eicosanoid-prostaglandin-swine-roadmap.md` | 36 | Eicosanoids: COX-2/PGE2, EP1-4 (EP3=sốt, EP4=bảo vệ ruột), 5-LOX/LTB4, ω-3/ω-6, POA-EP3R fever, PGI2+PGE2 gut barrier, NSAIDs, resolvin; queries + VN terms |

Each starts with a summary table, tested PubMed queries, PMID table with mechanisms, pathway diagrams, Vietnamese terminology, and feed additive modulation matrix.

### Level 3: Extract phone/email from raw HTML

When a page loads, extract contact info from raw text:

```python
phones = re.findall(r'(0[0-9]{2,4}[-\\s]?[0-9]{3}[-\\s]?[0-9]{3}[-\\s]?[0-9]{2,4})', text)
phones += re.findall(r'(\\+84[-\\s]?[0-9]{1,3}[-\\s]?[0-9]{3,4}[-\\s]?[0-9]{3,4}[-\\s]?[0-9]{2,4})', text)
emails = re.findall(r'[\\w.]+@[\\w.]+\\.\\w+', text)
hotlines = re.findall(r'[Hh]otline[:\\s]*([0-9\\s\\.\\+]+)', text)
```

Then deduplicate and format.

## Vietnamese-specific research patterns

### Finding Vietnamese suppliers

When searching for Vietnamese suppliers of industrial/chemical products:

1. **Search terms in Vietnamese:**
   - "[product name] thức ăn chăn nuôi"
   - "[product name] giá bán Việt Nam"
   - "phụ gia [product name]"
   - "công ty [product name]"
   - "hóa chất [product name]"

2. **Known Vietnamese supplier website naming patterns:**
   - hoachat[companyname].vn or .com
   - phugia[brand].com
   - [company]hoachat.com
   - Often hosted on WordPress/WooCommerce — API endpoints may exist

3. **Types of Vietnamese suppliers for feed additives:**
   - Chemical trading companies (Hóa chất Đại Việt, Phương Đông, Việt Mỹ)
   - Feed additive specialized companies (Phụ gia Thành Hóa, etc.)
   - International trading companies (Á Âu AIC, etc.)
   - Byproduct sources (paper mills for lignosulfonate)

4. **Contact methods:**
   - Phone/Zalo: Vietnamese businesses respond fastest to calls (not email)
   - Hotline numbers on websites
   - Zalo OA (Official Account) buttons on most Vietnamese business sites

### Vietnamese scam/security research

When the user asks to scan the internet for scam reports (on Twitter/X, Telegram, Threads, news sites):

1. Use DDG Lite with the search terms listed in `references/vietnamese-scam-research.md`
2. Pace queries with `time.sleep(2)` every 4 searches to avoid DDG rate limits
3. Auto-categorize results via snippet keywords (see reference file)
4. Compile into a Google Sheet using the `google-workspace` skill
5. Accept that scraping full articles is blocked by Cloudflare on Vietnamese news sites — extract what you can from snippets

**Data compilation workflow:**
1. Collect results with DDG Lite (paced queries)
2. Fetch article text for data-rich URLs (phone number lists, news reports)
3. Extract entities (phones, bank accounts, websites) via regex from fetched text
4. Import entities into the project DB (e.g., Supabase `scam_entities` table)
5. Create curated posts for notable scam cases
6. Export stats back to Google Sheet for synced reporting

**See** `references/vietnamese-scam-research.md` for search terms, categorization keywords, and platform coverage.

### What to collect per company

| Field | Example |
|-------|---------|
| Company name | Hóa chất Đại Việt (DVC) |
| Phone | 0976 938 801 |
| Email | lienhe@hoachatdaiviet.com |
| Website | hoachatdaiviet.vn |
| Address | Tầng lửng, Tòa nhà B2 Topaz City, 39 Cao Lỗ, P. Chánh Hưng, TP.HCM |

## Dedicated social-media scraping tools (expected 2025-2026)

When the user asks to scan social media for content (scam reports, brand mentions, sentiment), **do not** reach for tools like `snscrape`, `twint`, `twscrape`, or `facebook-scraper` as a first instinct. As of 2025-2026, all major platforms have locked down their APIs and web endpoints enough that general-purpose open-source scrapers fail consistently:

| Tool | Platform | Status in 2025-2026 | Failure mode |
|------|----------|---------------------|--------------|
| **snscrape** | Twitter/X | Dead | Twitter GraphQL API returns 404 to unauthenticated requests. Old v1.1 endpoint gone. |
| **snscrape** | Reddit | Dead | Relies on PushShift.io, which stopped serving public search queries. |
| **snscrape** | Telegram | Very limited | Only works for channels with public post list enabled. Cannot search by keyword. |
| **twscrape** | Twitter/X | Dead | Same GraphQL blocking as snscrape for unauthenticated pools. |
| **facebook-scraper** | Facebook | Brittle | Requires Selenium/Playwright + logged-in session. Facebook actively detects and bans. |
| **TikTok-Api** | TikTok | Brittle | Internal API changes frequently. Breaks every few weeks. |
| **social-analyzer** | Multiple | Not useful for content search | Only finds profiles by username, not content search. 23k stars but wrong tool for the job. |
| **URS** | Reddit | Large repo, may timeout | PRAW-based. If URS clone fails, use PRAW directly (same engine, simpler). |

**Use Playwright (Level 1d) instead.** It automates a real browser and works for YouTube, Bing News, and Reddit without login credentials. See Level 1d above for setup and platform coverage.

### When scraping genuinely works (rare cases)

- **Telegram public channels** — Only if you know the exact channel username AND it has search indexing enabled. Use `snscrape.modules.telegram.TelegramChannelScraper(channel_name)`.
- **Wikipedia APIs** — Always works (see Level 2a / 2b). Not social media, but useful for background research.
- **Self-hosted social listening** — Tools like OpenMagpie can monitor RSS feeds and Reddit, but require dedicated infrastructure.

## Pitfalls

The full pitfall list — DDG Lite CAPTCHA / silent rate-limit / >80-char query limits, Bing relevance pollution, Windows git-bash `python3` + MSYS path-conversion traps, Vietnamese anti-bot / partial-JS-load / phone-normalisation, subagent result lag, Vietnam international-domain blocking (+ TELEGRAM_PROXY / WARP), same-company-many-domains, `/api/knowledge` vs `/api/cards`, raw card list exceeding the 50KB stdout cap and the `/api/cards` large-KB timeout workaround, Wikipedia extract stdout truncation + the combined Pattern A+B workflow, cron topic-rotation via `session_search`, `execute_code` BLOCKED in cron mode, missing `import time`, and the cron-mode data patterns 0/A/B/C/D with their heredoc/MSYS caveats — is in `references/pitfalls-and-cron-data-patterns.md`.
Supporting: `references/windows-urllib-dns-quirk.md` (urllib 403/DNS while curl works), `references/kf-large-kb-and-pubmed-pitfalls.md`.

## Compiling and delivering research findings

After gathering raw information, structure the output for clarity and authority. This workflow was validated on a comprehensive physics encyclopedia (12 branches, 500+ terms, 93KB HTML with full citations).
- **Default pipeline (Research → HTML → Publish → KFlow), the "từ ngu đến PhD" 6-level explanation pattern, scientific evidence table format, the "Lead Researcher" delivery persona, and the "Sườn → Phê duyệt → Chi tiết" workflow** — including the `preview.thefirstonly.com` 403-with-urllib pitfall: `references/delivery-pipeline-html-publish.md` (also `references/research-quality-gates.md`, `references/physics-encyclopedia-case-study.md`).
- **Knowledge Flow card creation pipeline** — Steps 0–6 (research queue, KF passcode gate, mandatory existing-card check, novel-topic selection, gap-finding heuristics, research, card structure, dedup + word-boundary fix, POST via Pattern D/C, post-landing verification) and every KF pitfall: `references/knowledge-flow-card-pipeline.md` (also `references/research-rotation-cron.md`, `references/kf-passcode-gate-cron.md`, `references/gap-finding-ghost-topics.md`, `references/gap-prioritization-heuristics.md`, `references/kf-duplicate-card-removal.md`, `references/kf-unreachable-fallback.md`, and the card templates `references/{virus-pathogen,bacterial-pathogen,pathway,feed-additive,toxic-agent}-card-template.md`).
- **Output format matrix, HTML knowledge-base recipe (section skeleton + CSS colour tokens), citation standards, deliverable pitfalls, multi-pass protocol refinement pattern, budget/Sheet delivery pattern**: `references/delivery-formats-and-citation-standards.md` (also `references/heavy-metals-soil-remediation.md`, `references/output-requirements.md`).

## Verification

When researching suppliers:
1. Confirm website is real (loads meaningful content, not parked domain)
2. Phone number should match format: 0XX XXX XXXX or +84 XX XXX XXXX
3. Cross-reference: does the company list any products relevant to the search?
4. For Vietnamese companies: check if they have a Zalo button on their website