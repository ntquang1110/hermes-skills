---
name: seo-audit-and-strategy
description: "Use when a user needs a full SEO audit and ranking strategy."
version: 1.0.0
author: Hermes Agent
tags: [seo, audit, strategy, planning, website, google-search, ai-search, structured-data]
---

# SEO Audit & Strategy Planning

Use when the user asks to analyze a website's SEO readiness and build a ranking strategy for Google + AI search (SGE, ChatGPT, Perplexity).

## Workflow

### Phase A: Audit

1. **Browse the site** — `browser_navigate` homepage + key pages (gioi-thieu, san-pham, tin-tuc, khoa-hoc, lien-he)
2. **Extract meta** via `browser_console`:
   - `document.title`
   - `document.querySelector('meta[name="description"]')?.content`
   - All meta tags: `JSON.stringify([...document.querySelectorAll('meta')].map(m=>({name:m.getAttribute('name'),property:m.getAttribute('property'),content:m.getAttribute('content')})))`
   - `document.querySelector('link[rel="canonical"]')?.href`
   - `document.querySelector('script[type="application/ld+json"]')?.innerHTML`
   - `document.querySelector('html')?.getAttribute('lang')`
   - `document.querySelector('link[rel="alternate"][hreflang]')?.outerHTML`
3. **Check sitemap.xml** — `/sitemap.xml`
4. **Check robots.txt** — `/robots.txt`
5. **Check product/blog pages** — verify content, H1 count, JS loading behavior
6. **Identify brand mismatch** — compare domain name vs actual title/meta/H1 content

### Phase B: Analysis

Document findings in a structured table:

| Category | Status | Detail |
|---|---|---|
| Brand alignment | ✅/❌ | Domain vs title/meta/H1 match |
| Title tags | ✅/❌ | Keyword presence, length 55-60 |
| Meta description | ✅/❌ | Keyword presence, length 150-160 |
| H1 tags | ✅/❌ | Unique per page, contains keyword |
| Structured data | ✅/❌ | Organization, Product, Article, FAQ, BreadcrumbList |
| Sitemap | ✅/❌ | Exists, contains all pages |
| Canonical | ✅/❌ | Present on all pages |
| Hreflang | ✅/❌ | For multi-language sites |
| robots.txt | ✅/❌ | Allows crawling, references sitemap |
| Open Graph | ✅/❌ | og:title, og:description, og:image |
| Twitter Card | ✅/❌ | Check twitter:site is not from builder tool |
| Page speed | ⚠️ | Note if SPA/heavy JS |
| Mobile friendly | ⚠️ | Has viewport meta |
| Blog URLs | ✅/❌ | Uses slug vs UUID |
| Image alt text | ✅/❌ | Present with keywords |

### Phase C: Strategy Plan

Structure the plan in 5 phases:

| Phase | Focus | Time | Priority |
|---|---|---|---|
| **P1 — Foundation** | Brand sync, sitemap, structured data, GSC, canonical, hreflang | Week 1 | 🔴 Highest |
| **P2 — On-page** | Product landing pages, blog slug fix, pillar content, image alt | Weeks 2-3 | 🔴 High |
| **P3 — Off-page** | Google Business Profile, backlink outreach, social strategy | Weeks 3-8 | 🟡 Medium |
| **P4 — AI Search** | FAQ schema, glossary, E-E-A-T, content freshness | Parallel P2 | 🟡 Medium |
| **P5 — Technical** | Core Web Vitals, mobile, crawl budget, security | Ongoing | 🟢 Low |

#### P1 — Foundation Details

**Brand alignment:** For each position (title, meta desc, H1, OG:title, header logo, twitter:site), document current vs target values in a comparison table.

**Structured data to add:**
- Organization (every page) — with `alternateName` for brand
- Product (product pages) — with `alternateName` for product codes (e.g. EZ80)
- Article (blog posts) — with author, datePublished, publisher
- BreadcrumbList (every page)
- FAQ (product/Q&A pages)
- HowTo (instructional pages)

**Sitemap:** Generate comprehensive list of all URLs with `<lastmod>`, `<changefreq>`, `<priority>`.

**Canonical + Hreflang:** Add to `<head>` of every page.

#### P2 — On-page Details

**Product landing pages:** Each main product needs unique title, meta desc, H1, Product schema, BreadcrumbList, images with alt text, internal links to related blog posts, CTA.

For each product, document in a card format:
- Product name + alternate name (e.g. Kiềm EZ Tái Sinh 80 / EZ80)
- Target slug (e.g. `/san-pham/kiem-ez-tai-sinh-80`)
- Target keywords (e.g. EZ80, thức ăn bổ sung gia súc, thay thế kháng sinh)

**Blog optimization:**
- Replace UUID slugs with keyword-rich slugs
- Add Article schema
- Add internal links to product pages
- Add author attribution

**Pillar content:** Create 3 content hubs:

1. **Core topic definition** (e.g. "What is X?")
   - Cluster: mechanism, comparison with alternatives, applications in different sectors
   - URL: `/kien-thuc/<topic-slug>`

2. **Industry solution** (e.g. "Replace antibiotics in livestock")
   - Cluster: specific product applications, case studies, trial results, expert insights
   - URL: `/kien-thuc/<solution-slug>`

3. **Broader concept** (e.g. "Circular agriculture")
   - Cluster: system overview, sub-models (VACB), economic/environmental impact
   - URL: `/kien-thuc/<concept-slug>`

Each pillar page links to cluster blog posts. Each cluster blog links back to the pillar page.

#### P4 — AI Search Details (Google SGE, ChatGPT, Perplexity)

**E-E-A-T signals:**
- Create author page for subject matter experts (name, credentials, publications)
- Cite specific research sources (university studies, partner trials) with links
- Display real data from dashboards (not hand-entered)
- Show certifications/awards prominently
- Full contact info on every page

**FAQ schema:** Add to product pages. AI search engines frequently extract FAQ in answers.
- Question-answer pairs for: "What is [product]?", "How to use [product]?", "Difference between X and Y?"

**Glossary page:** Create `/thuat-ngu` with definitions of industry terms. AI loves glossary content.

**Content freshness:**
- New blog posts weekly (case studies, trial results)
- Update product pages when new data arrives
- Dynamic sitemap with accurate `<lastmod>`

**Multi-language:** Ensure product info in both VN and EN for bilingual AI queries.

### Phase D: Deliverable

1. **Write detailed markdown plan** to `.md` file
2. **Convert to HTML** — use `md-to-html.py` from publish skill, or build custom consulting-grade HTML with:
   - Dark header with summary (target keywords, timeline, budget)
   - Sticky nav with phase links
   - Phase cards with color coding (red=highest, amber=high, blue=medium, purple=parallel, green=low)
   - Product cards grid for P2 landing pages
   - Pillar cards grid for content strategy
   - Timeline visualization with week markers
   - KPI table with baseline + 3-month targets
   - Cost estimate summary grid
   - Risk/mitigation table
3. **Publish** via `content-upload.py` from publish skill
4. **Verify** preview URL returns HTTP 200 via `curl -s -o /dev/null -w "%{http_code}"`

## KPI & Tracking

Include a KPI table in the deliverable:

| Metric | Tool | Baseline (est.) | Target (3 months) |
|---|---|---|---|
| Indexed pages | GSC | ~current count | 2-3x increase |
| Primary keyword rank | GSC / Ahrefs | Outside top 50 | Top 5 |
| Secondary keyword rank | GSC / Ahrefs | Outside top 50 | Top 10 |
| Organic traffic | GA4 | ~current | 500+/month |
| Backlinks | Ahrefs | ~0 | 20+ |
| Core Web Vitals | GSC | Unknown | Pass all |
| CTR from search | GSC | Unknown | 5%+ |

## Risk & Mitigation

Include a risk table in the deliverable:

| Risk | Impact | Mitigation |
|---|---|---|
| Brand conflict (domain vs content) | High | Use `alternateName` in Organization schema, keep legal name in footer |
| SPA hard to index | High | Recommend SSR or pre-render for critical pages |
| UUID URLs cannot change | Medium | Add slug field to DB, 301 redirect from UUID |
| Competitors | Medium | Focus on unique case studies and research data |
| Thin content for AI search | Low | Pillar content + glossary + FAQ schema |

## Budget Estimate

| Item | Cost | Note |
|---|---|---|
| Google Business Profile | 0đ | Self-register |
| GSC + GA4 | 0đ | Free |
| Backlink outreach | 5-15tr VND | Guest posts, PR |
| SEO tools | 0đ | Use GSC + free tier |
| **Total** | **5-15tr VND** | Mostly backlinks |

## Implementation — Phase E: Deploy P1 Changes

After the plan is approved and the user provides repo access, implement Phase 1 directly.

### E.1 Clone & Inspect

Check GitHub credentials first, then clone:

```bash
env | grep GITHUB  # check for PAT (may be base64-encoded)
```

**Pitfall: Verify repo exists and PAT has access.** Always check before cloning:
```bash
PAT="ghp_..." && curl -s -H "Authorization: token $PAT" "https://api.github.com/repos/<owner>/<repo>"
```
The user may have multiple accounts and multiple PATs. The first PAT found may not have access to the repo they named. If you get 404, ask the user to provide the correct PAT or check which account owns the repo:
```bash
curl -s -H "Authorization: token $PAT" "https://api.github.com/user/repos?per_page=100&type=all" | python -c "import sys,json; [print(r['full_name']) for r in json.load(sys.stdin)]"
```

**Pitfall: PAT may lack `actions:read` scope for CI/CD verification.** If the first PAT gives a 404 when checking workflow runs, try a different PAT from the user. Not all tokens have the same scopes:
```bash
curl -s -H "Authorization: token $PAT" "https://api.github.com/repos/<owner>/<repo>/actions/runs?per_page=1&branch=main"
```

**Pitfall: SSH key for deployment may be in GitHub secrets only.** The deploy key may be stored as `secrets.SSH_KEY` in GitHub Actions and not accessible locally. Check `env | grep -i GITHUB` and `ls ~/.ssh/`. You won't be able to SSH into the deploy server directly.

**Server host discovery from GitHub Actions:** When the deploy target is unknown, check GitHub Actions variables:
```bash
curl -s -H "Authorization: token $PAT" "https://api.github.com/repos/<owner>/<repo>/actions/variables" | python -c "import sys,json; [print(f'{v[\"name\"]}: {v[\"value\"]}') for v in json.load(sys.stdin).get('variables',[])]"
```
This reveals the deployment server IP/hostname and SSH user.

Then clone:
```bash
git clone --depth 1 https://<user>:<pat>@github.com/<owner>/<repo>.git
```

### E.2 Find All Brand References

```bash
grep -rn "OldBrand\|OLD BRAND" src/ --include="*.tsx" --include="*.ts"
```

### E.3 Prioritize Changes

| Priority | Files | Why |
|---|---|---|
| Critical | `index.html` | SEO metadata — title, meta, OG, Twitter, canonical, hreflang, JSON-LD, loading text |
| High | Header, Footer, HeroSection | User-facing brand on every page |
| Medium | About, Catalog, Dashboard, Science Hub | Content pages with brand text |
| Low | Admin components | Internal UI |

### E.4 index.html Changes (Vite/React SPA)

For a Vite/React SPA without react-helmet, ALL SEO metadata is in `index.html`:

1. **Title** — primary keyword + brand (55-60 chars)
2. **Meta description** — brand + key products + keywords (150-160 chars)
3. **Canonical** — `<link rel="canonical" href="https://domain.com/">`
4. **Hreflang** — vi, en, x-default for multi-language sites
5. **JSON-LD Organization schema** — legal name + `alternateName` for brand
6. **OG/Twitter** — match new brand, remove builder tool remnants (e.g. `@Lovable`)
7. **Loading text** — update spinner text

### E.5 Component Brand Changes

- **Logo alt** — `alt="OldBrand"` → `alt="NewBrand"`
- **Brand name text** — hardcoded strings in JSX
- **Fallback values** — `data?.title || "OldBrand"` patterns
- **Copyright** — KEEP legal entity name in footer (registered company, not brand)

### E.6 Sitemap & Robots

Create `public/sitemap.xml` with all URLs, `<lastmod>`, `<changefreq>`, `<priority>`.
Update `public/robots.txt` — add `Sitemap: https://domain.com/sitemap.xml`.

### E.7 Commit & Push

```bash
git add -A && git commit -m "Phase 1 SEO: brand sync, sitemap, schema, canonical, hreflang"
git push origin main
```

### E.8 Verify After Deploy

- `browser_navigate` to site → check title/meta in console
- `curl -s -o /dev/null -w "%{http_code}" https://domain.com/sitemap.xml` → 200
- Check structured data in browser console
- Verify GitHub Actions deploy completed: `curl -H "Authorization: token $PAT" "https://api.github.com/repos/<owner>/<repo>/actions/runs?per_page=1&branch=main"` → `conclusion: success`
- After deploy confirmed, curl the live site to verify meta changes landed:
  ```bash
  curl -s https://domain.com | grep -o '<title>[^<]*</title>'
  curl -s https://domain.com/sitemap.xml | head -5
  curl -s https://domain.com/robots.txt | grep -i sitemap
  ```

### E.9 — Dynamic SEO for React SPAs (Phase 2)

For React SPAs (Vite, CRA) where all SEO meta is static in `index.html`, implement per-page dynamic meta:

**1. Install react-helmet-async:**
```bash
npm install react-helmet-async
```

**2. Create reusable SEO component (`src/components/SEO.tsx`):**
```tsx
import { Helmet } from "react-helmet-async";

interface SEOProps {
  title: string;
  description?: string;
  ogTitle?: string;
  ogDescription?: string;
  ogImage?: string;
  canonical?: string;
  jsonLd?: Record<string, unknown>;
}

const SITE_NAME = "Brand Name";
const DEFAULT_DESC = "Default meta description...";

const SEO = ({ title, description = DEFAULT_DESC, ogTitle, ogDescription, ogImage, canonical, jsonLd }: SEOProps) => {
  const fullTitle = `${title} — ${SITE_NAME}`;
  const url = canonical || "https://domain.com";

  return (
    <Helmet>
      <title>{fullTitle}</title>
      <meta name="description" content={description} />
      <meta property="og:title" content={ogTitle || fullTitle} />
      <meta property="og:description" content={ogDescription || description} />
      <meta property="og:url" content={url} />
      <meta name="twitter:title" content={ogTitle || fullTitle} />
      <meta name="twitter:description" content={ogDescription || description} />
      <link rel="canonical" href={url} />
      {ogImage && <meta property="og:image" content={ogImage} />}
      {ogImage && <meta name="twitter:image" content={ogImage} />}
      {jsonLd && <script type="application/ld+json">{JSON.stringify(jsonLd)}</script>}
    </Helmet>
  );
};
```

**3. Wrap App with HelmetProvider (`src/App.tsx`):**
```tsx
import { HelmetProvider } from "react-helmet-async";
import SEO from "@/components/SEO";

const App = () => (
  <HelmetProvider>
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <SEO title="Homepage title" canonical="https://domain.com/" />
        <Routes>...</Routes>
      </BrowserRouter>
    </QueryClientProvider>
  </HelmetProvider>
);
```

**4. Per-page SEO with dynamic JSON-LD:**

For product pages (dynamic Product schema):
```tsx
<SEO
  title={product.name}
  description={`${product.name} — category. ${plainText.slice(0, 160)}`}
  canonical={`https://domain.com/san-pham/${product.id}`}
  ogImage={product.image_url}
  jsonLd={{
    "@context": "https://schema.org",
    "@type": "Product",
    name: product.name,
    description: product.description?.slice(0, 300),
    brand: { "@type": "Brand", name: "Brand Name" },
    category: catName,
  }}
/>
```

For blog posts (dynamic Article schema):
```tsx
<SEO
  title={post.title}
  description={post.excerpt?.slice(0, 160)}
  canonical={`https://domain.com/tin-tuc/${post.id}`}
  jsonLd={{
    "@context": "https://schema.org",
    "@type": "Article",
    headline: post.title,
    datePublished: post.created_at,
    author: { "@type": "Person", name: "Author" },
    publisher: { "@type": "Organization", name: "Brand Name" },
  }}
/>
```

**Important SPA limitation:** Dynamic meta from react-helmet-async only updates AFTER JavaScript loads and renders. Googlebot does execute JS but with delays. For critical pages, consider SSR (Next.js) or prerendering. The react-helmet approach is still valuable because:
- Googlebot's modern crawler executes JS (though slower)
- Each page gets unique canonical + JSON-LD (Google's structured data validator sees these)
- Social media crawlers (Facebook, Twitter) may execute JS

## Pitfalls

- **Brand mismatch is the #1 killer**: Domain name ≠ brand on page = Google doesn't know what the site is about. Always check title + meta desc + H1 first.
- **UUID blog URLs**: Google can't infer topic from `/tin-tuc/uuid`. Always recommend slug migration with 301 redirects.
- **SPA loading**: If products page shows "Đang tải..." (JS-dependent), Googlebot may not index product content. Flag for SSR/pre-rendering.
- **Builder tool remnants**: Check twitter:site, generator meta tags, etc. for Lovable.dev / Webflow / other builder artifacts.
- **No structured data = invisible to AI search**: ChatGPT, Perplexity, Google SGE all rely heavily on JSON-LD schema.
- **Cost is mostly backlink outreach**: Technical SEO is free (GSC, GA4, schema, sitemap). Budget goes to guest posts and PR.
- **Cloudflare API token discovery**: If the user says they have Cloudflare access but no token is in env vars, decode the cloudflared cert.pem JWT: `grep -v "^---" ~/.cloudflared/cert.pem | tr -d '\n' | cut -d. -f2 | python -c "import sys,base64,json; print(json.dumps(json.loads(base64.urlsafe_b64decode(sys.stdin.read().strip()+'==')), indent=2))"`. The resulting `apiToken` may be scoped to specific zones only — verify with `curl -s -H "Authorization: Bearer $TOKEN" "https://api.cloudflare.com/client/v4/zones?per_page=50"`.
- **GSC setup requires DNS TXT record**: For domain property verification, Google provides a `google-site-verification=xxxxx` TXT value. The agent needs either Cloudflare API access to the target domain's zone or the user to add it manually. Check DNS provider via `nslookup -type=NS domain.com`.
- **GA4 setup needs user action**: The agent cannot create Google Analytics properties. Ask for the Measurement ID (G-XXXXXXXX) and inject it into the site.

## Related Skills

- `publish` — upload HTML/MD/TXT to preview.thefirstonly.com
- `html-unslop` — pre-processor for AI-generated HTML
- `design-critique` — critique-first design methodology (similar audit-before-build approach)
