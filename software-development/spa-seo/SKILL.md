---
name: spa-seo
description: "Use when auditing SEO for React SPA web apps."
version: 1.0.0
author: Hermes Agent
---

# SPA SEO Optimization

SEO for Single Page Applications requires a multi-layer approach. Static HTML meta handles the initial load; dynamic meta (react-helmet) handles per-page; structured data feeds Google/AI search; sitemaps ensure discovery.

## Audit Flow

```
index.html static meta → dynamic per-page SEO → structured data → sitemap → canonical/hreflang → brand consistency → GSC setup
```

## Layer 1 — Static Meta (index.html)

The `index.html` is what Googlebot and social crawlers see first. Always start here.

| Element | What to check |
|---------|--------------|
| `<title>` | Must contain brand + primary keyword. 55-60 chars |
| `<meta name="description">` | 150-160 chars, include keywords + brand |
| `<meta name="author">` | Set to brand name |
| `<meta property="og:title">` | Match title |
| `<meta property="og:description">` | Match description |
| `<meta name="twitter:card">` | Set to `summary_large_image` |
| `<meta name="twitter:site">` | Remove if from builder tool (e.g. @Lovable) |
| `<link rel="canonical">` | Add for every page |
| `<link rel="alternate" hreflang="">` | Add vi/en/x-default |
| `<script type="application/ld+json">` | Add Organization schema |
| Loading text | Should match brand name, not generic |

## Layer 2 — Dynamic Per-Page SEO

Install `react-helmet-async` for dynamic meta tags per route.

```bash
npm install react-helmet-async
```

### Setup

Wrap app with `HelmetProvider` in App.tsx:

```tsx
import { HelmetProvider } from "react-helmet-async";

const App = () => (
  <HelmetProvider>
    {/* rest of app */}
  </HelmetProvider>
);
```

### SEO Component

Create `src/components/SEO.tsx` with `Helmet` from react-helmet-async. Accept props: `title`, `description`, `canonical`, `ogImage`, `jsonLd`. Format title as `"${title} — ${SITE_NAME}"`.

### Usage Per Page

- **Product page**: dynamic title + Product schema JSON-LD
- **Article page**: dynamic title + Article schema JSON-LD (headline, datePublished, author, publisher)
- **Static pages**: fixed title + description + canonical

## Layer 3 — Structured Data (JSON-LD)

| Schema | Where | Why |
|--------|-------|------|
| Organization | index.html (all pages) | Knowledge Panel |
| Product | Product detail pages | Rich results |
| Article | Blog posts | Google News, SGE |
| BreadcrumbList | Navigation | Breadcrumb rich result |
| FAQ | Product/Q&A pages | FAQ rich result, AI citation |

## Layer 4 — Sitemap

Create `public/sitemap.xml` with all URLs. Update `robots.txt` to reference it.

## Layer 5 — Canonical + Hreflang

- Canonical: every page needs `<link rel="canonical">`
- Hreflang: add vi/en/x-default if site has language toggle

## Layer 6 — Brand Consistency

Search across codebase for old brand name. Check: index.html (title, meta, OG, Twitter, loading text), Header.tsx (logo alt, brand text), Footer.tsx (keep legal entity in copyright), HeroSection.tsx (fallback title), all page components, admin UI strings.

## Layer 7 — Google Search Console + GA4

Register domain in GSC (verify via DNS TXT record). Submit sitemap. Add GA4 tracking tag to index.html.

## SPA Gotchas

1. Dynamic meta only after JS executes — static index.html meta is critical for initial crawl.
2. UUID URLs are not SEO-friendly. Add `slug` column, query by `.or("slug.eq.${id},id.eq.${id}")` for backward compatibility.
3. If no react-helmet, install and set up before anything else.

## Pitfalls

- Keep legal entity name in footer copyright.
- Remove twitter:site="@Lovable" (Lovable.dev builder artifact).
- Use `alternateName` in schema for brand transitions.
- UUID → slug migration: keep backward compatibility, don't break existing URLs.
