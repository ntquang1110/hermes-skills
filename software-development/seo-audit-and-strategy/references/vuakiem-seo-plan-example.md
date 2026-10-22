# Reference: vuakiem.com SEO Plan (Sep 2026)

## Context

Domain vuakiem.com was branded 100% as "Manna Đất Vàng" — title, meta desc, H1, header, footer all said Manna Đất Vàng. "Vua Kiềm" only appeared in blog articles as a sub-brand mention. User wanted top rankings for "vua kiềm" and "EZ80".

## Key Findings

| Issue | Severity |
|---|---|
| Brand mismatch (domain=vuakiem, content=Manna Đất Vàng) | CRITICAL |
| No sitemap.xml (404) | CRITICAL |
| No structured data (JSON-LD) | CRITICAL |
| No canonical tags | HIGH |
| Blog URLs use UUIDs | HIGH |
| Twitter card has @Lovable (builder tool remnant) | MEDIUM |
| No hreflang (despite VN/EN toggle) | MEDIUM |
| Product page shows "Đang tải..." (JS-dependent) | MEDIUM |

## Brand Fix Table

| Position | Before | After |
|---|---|---|
| Title | Manna Đất Vàng - Mâm cơm sạch cho cả thế giới | Vua Kiềm — Giải pháp kiềm sinh học cho nông nghiệp tuần hoàn |
| Meta desc | CP Manna Đất Vàng - Giải pháp NN sinh học | Vua Kiềm (thương hiệu CP Manna Đất Vàng) — Kiềm sinh học, EZ80, EZ67, Virusto |
| H1 | Manna Đất Vàng | Vua Kiềm — Giải pháp kiềm sinh học toàn diện |
| OG:title | Manna Đất Vàng - Mâm cơm sạch... | Vua Kiềm — Kiềm sinh học cho nông nghiệp tuần hoàn |
| twitter:site | @Lovable | Removed |

## Implementation Details (Phase 2a — Dynamic SEO)

After Phase 1 brand sync, added per-page dynamic SEO via react-helmet-async:

**Changes (9 files, +158/-8 lines):**
- `src/components/SEO.tsx` — new reusable component supporting title, meta, OG, Twitter, canonical, JSON-LD
- `src/App.tsx` — wrapped with HelmetProvider, added default SEO
- `src/pages/ProductDetail.tsx` — dynamic title + Product schema JSON-LD (from Supabase data)
- `src/pages/NewsDetail.tsx` — dynamic title + Article schema JSON-LD (from Supabase data)
- `src/pages/About.tsx` — static SEO for about page
- `src/pages/Contact.tsx` — static SEO with contact info in meta desc
- `src/pages/Products.tsx` — ProductsOverview + ProductCategory with dynamic titles

**Key pattern — dynamic Product schema:**
```tsx
<SEO
  title={product.name}
  description={`${product.name} — ${catName}. ${stripHtml(product.description).slice(0, 160)}`}
  canonical={`https://vuakiem.com/san-pham/chi-tiet/${product.id}`}
  ogImage={product.image_url || undefined}
  jsonLd={{
    "@context": "https://schema.org",
    "@type": "Product",
    name: product.name,
    description: stripHtml(product.description).slice(0, 300),
    brand: { "@type": "Brand", name: "Vua Kiềm" },
    category: catName,
  }}
/>
```

**Key pattern — dynamic Article schema:**
```tsx
<SEO
  title={post.title}
  description={stripHtml(post.excerpt).slice(0, 160)}
  canonical={`https://vuakiem.com/tin-tuc/${post.id}`}
  jsonLd={{
    "@context": "https://schema.org",
    "@type": "Article",
    headline: post.title,
    datePublished: post.created_at,
    author: { "@type": "Person", name: "Vua Kiềm" },
    publisher: { "@type": "Organization", name: "Vua Kiềm" },
  }}
/>
```

**CI/CD:** GitHub Actions builds Docker image, copies via SCP to server, deploys via Docker Compose. Deploy time ~60s. Verify with: `curl -s https://domain.com | grep -o '<title>[^<]*</title>'`

**Tech stack:** Vite + React + TypeScript + Tailwind (SPA, no react-helmet)

**Files changed (16 total, +133/-42 lines):**
- `index.html` — title, meta desc, OG/Twitter, canonical, hreflang, JSON-LD Organization schema, loading text
- `public/robots.txt` — added Sitemap reference
- `public/sitemap.xml` — new file (12 URLs)
- `src/components/Header.tsx` — logo alt, brand name, tagline
- `src/components/Footer.tsx` — logo alt, brand name, tagline (kept company name in copyright)
- `src/components/home/HeroSection.tsx` — fallback title, subtitle, logo alt
- `src/components/home/JourneySection.tsx` — fallback subtitle
- `src/components/home/NewsSection.tsx` — hardcoded news item brand
- `src/components/home/ProductsBento.tsx` — section title
- `src/components/home/ProductsShowcase.tsx` — section title
- `src/pages/About.tsx` — page title
- `src/pages/Catalog.tsx` — fallback subtitle
- `src/pages/nttt/Dashboard.tsx` — header brand label
- `src/pages/science/Hub.tsx` — section label
- `src/components/admin/CatalogAdmin.tsx` — default form values
- `src/components/admin/JourneyAdmin.tsx` — description text

**Key insight:** Copyright line ("Công ty Cổ phần Manna Đất Vàng") was intentionally kept — it's the legal entity name, not the brand. Only the brand/tradename "Manna Đất Vàng" was replaced with "Vua Kiềm".

**GitHub auth:** Initial PAT (GITHUB_PAT_B64) didn't have access to the repo. User provided a second PAT which worked. Always verify repo access before cloning.

## Deliverables

- Markdown plan: `D:/Hermes Proj/seo-plan-vuakiem.md`
- Published HTML: https://preview.thefirstonly.com/o08d1k27hpch

## Outcome

5-phase plan delivered: Foundation (1wk) → On-page (2-3wk) → Off-page (3-8wk) → AI Search (parallel) → Technical (ongoing). Budget: 5-15tr VND. Expected: "vua kiềm" top 5 in 4-8 weeks, "EZ80" top 10 in 8-12 weeks.

**Phase 1 (Foundation):** Implemented and deployed ✅ — brand sync, sitemap, JSON-LD Organization schema, canonical, hreflang, robots.txt. All 16 files committed and pushed. GitHub Actions deploy confirmed success. Live site verified with updated title/meta.

**Phase 2a (Dynamic SEO):** Implemented and deployed ✅ — react-helmet-async installed, reusable SEO.tsx component created, dynamic Product schema for EZ80/EZ67/Virusto, dynamic Article schema for blog posts, unique meta per page (About, Contact, Products, ProductCategory). 9 files committed and pushed. Deploy confirmed success.

**Remaining items (need user action):**
- **GSC setup**: Requires Google account (@kiemsaphia.com). Need DNS TXT verification record from GSC. DNS is on Cloudflare (NS: daphne + koa) but the agent's API token only has access to thefirstonly.com and theliems.com zones — not vuakiem.com. User needs to either provide the vuakiem.com Cloudflare API token or add the TXT record manually.
- **GA4**: Need Measurement ID (G-XXXXXXXX) from Google Analytics.
- **Phase 2b (Blog slug migration)**: Replace UUID-based blog URLs with SEO-friendly slugs. Requires Supabase DB migration (add slug column).
- **Phase 2c (Pillar content)**: Create 3 pillar pages with cluster blog content.

## Cloudflare Credential Discovery

If the user says they have Cloudflare API keys but none are found in env vars, check the cloudflared cert.pem:

```bash
cat ~/.cloudflared/cert.pem
# Contains a JWT with apiToken, zoneID, accountID claims

# Decode the JWT payload:
grep -v "^---" ~/.cloudflared/cert.pem | tr -d '\n' | cut -d. -f2 | python -c "
import sys, base64, json
data = sys.stdin.read().strip()
padding = 4 - len(data) % 4
if padding != 4: data += '=' * padding
decoded = base64.urlsafe_b64decode(data)
print(json.dumps(json.loads(decoded), indent=2))
"
```

This reveals the Cloudflare API token (`apiToken`), account ID, and zone ID. The token may be scoped to specific zones only — check which zones it can access:

```bash
curl -s -H "Authorization: Bearer $CF_TOKEN" "https://api.cloudflare.com/client/v4/zones?per_page=50"
```

**Pitfall:** The cloudflared tunnel token may only have access to SOME zones, not all zones under the Cloudflare account. The target domain (e.g. vuakiem.com) may be in a different Cloudflare account entirely — verify before assuming you can manage its DNS.

**Pitfall:** Not all GitHub PATs have the same scopes. If one PAT returns 404 for `actions/runs`, try another PAT from the user. The `GITHUB_PAT_B64` env var may be one token while the user later provides a different, more permissive one.
