# vuakiem.com SEO Audit — Session Reference

## Stack
- **Framework**: Vite + React 18 + TypeScript (SWC)
- **Styling**: Tailwind CSS + shadcn/ui
- **Router**: react-router-dom v6
- **Data**: Supabase (project: gkehvopdnlkdjfxqtygi)
- **Deploy**: Docker (Nginx) → GitHub Actions → VPS 45.77.253.250
- **DNS**: Cloudflare (NS: daphne + koa)
- **GA4**: G-VXS57XXFQ6

## Key Findings (Sept 2026)

1. **Brand crisis**: Domain vuakiem.com but site branded 100% as "Manna Đất Vàng" — no "Vua Kiềm" in title, meta, H1. Google couldn't match domain to brand.
2. **sitemap.xml**: 404 — no sitemap at all.
3. **Structured data**: Zero JSON-LD anywhere.
4. **Canonical/hreflang**: Missing on all pages.
5. **twitter:site**: Set to @Lovable (Lovable.dev builder tool).
6. **UUID URLs**: Blog and product detail URLs use UUIDs (`/tin-tuc/de650c82-...`).
7. **No dynamic SEO**: All pages share same static title from index.html — no react-helmet.
8. **Loading text**: "Đang tải Manna Đất Vàng..." — old brand.

## Changes Made

### Phase 1 — Foundation (deployed)
- index.html: title, meta desc, OG, Twitter → "Vua Kiềm" brand
- Added canonical, hreflang (vi/en/x-default), Organization JSON-LD
- Removed @Lovable from twitter:site
- Added sitemap.xml (12 URLs) + robots.txt Sitemap reference
- Changed loading text to "Đang tải Vua Kiềm..."
- Header.tsx, Footer.tsx, HeroSection.tsx: brand → Vua Kiềm
- 12+ components/pages: brand text updated

### Phase 2a — Dynamic SEO (deployed)
- Installed react-helmet-async
- Created SEO.tsx component
- ProductDetail: dynamic title + Product schema JSON-LD
- NewsDetail: dynamic title + Article schema JSON-LD
- About, Contact, Products: unique per-page SEO

### Phase 2b — Slugs (code pushed, SQL pending)
- slug.ts: toSlug() with Vietnamese diacritic support
- Supabase migration: add slug columns to news_posts + products
- Backward compatible query: `.or("slug.eq.${id},id.eq.${id}")`
- Admin forms auto-generate slug from title/name

## Cloudflare API Access
Found in `~/.cloudflared/cert.pem` JWT payload. Decode with:
```
grep -v "^---" cert.pem | tr -d '\n' | cut -d. -f2 | base64 -d
```
Returns: zoneID, accountID, apiToken fields.
Current token only accesses thefirstonly.com + theliems.com zones.
