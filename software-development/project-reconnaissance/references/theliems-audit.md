# Project Reconnaissance — Worked Example: TheLiem

This is the output of applying the `project-reconnaissance` process to the [theliems](https://github.com/ntquang1110/theliems) project (July 2026). Use as a template for future audits.

## Phase 1: Find & Clone

```bash
# Token in .env as GITHUB_PAT_B64 (base64), gh CLI had stale token
# Workaround: use HTTPS with PAT directly
git clone https://ntquang1110:${TOKEN}@github.com/ntquang1110/theliems.git ~/theliems
```

**Key lesson:** Always check gh auth scopes vs .env token separately. The old token had only `gist` scope; the new one had full `repo` scope but gh didn't know about it.

## Phase 2: Structure Scan

```
theliems/
├── app/
│   ├── page.tsx                    ← Homepage (SSR)
│   ├── layout.tsx                  ← Root layout + metadata
│   ├── globals.css                 ← Dark retro pixel theme
│   ├── bai-viet/[slug]/
│   │   ├── page.tsx                ← Post detail (SSR)
│   │   └── post-detail-client.tsx  ← Comments, likes, share
│   ├── dang-nhap/page.tsx          ← Login form
│   ├── dang-ky/page.tsx            ← Register form
│   └── auth/callback/route.ts      ← OAuth callback
├── components/
│   ├── home-client.tsx             ← Home UI (client component)
│   ├── theme-provider.tsx
│   └── ui/                         ← shadcn components
├── lib/supabase/
│   ├── client.ts                   ← Browser Supabase client
│   ├── server.ts                   ← SSR Supabase client
│   └── middleware.ts               ← Auth middleware
├── hooks/                          ← use-mobile, use-toast
├── scripts/                        ← SQL migrations
│   ├── 001_create_tables.sql       ← Full schema + RLS
│   ├── 002_seed_posts.sql
│   └── 003_create_admin_user.sql
└── styles/globals.css              ← Pixel art CSS
```

## Phase 3: Key Sources

### README
- **Title:** TheLiem
- **Stack:** Next.js + v0.dev
- **Setup:** `pnpm dev` → localhost:3000

### Layout Metadata
- **Title:** "TheLiem - Pixel Wisdom"
- **Description:** "Cộng đồng liêm chính Việt Nam"

### Tech Stack (from package.json)
- Next.js 15 (App Router), React 19, TypeScript
- 51 dependencies (shadcn/ui: Radix accordion, dialog, dropdown, etc.)
- Supabase SSR (@supabase/ssr)
- Tailwind CSS 4
- Vercel Analytics
- Fonts: Press Start 2P + VT323 (pixel retro)

### DB Schema (from 001_create_tables.sql)
```sql
profiles    (id PK, display_name, avatar_url, is_admin)
categories  (id PK, name, slug, color) → Theliems(cyan) + TheScam(red)
posts       (id PK, title, slug, content, excerpt, is_anonymous, views, likes, status)
            FK: category_id→categories, author_id→auth.users
comments    (id PK, content, is_anonymous)
            FK: post_id→posts, author_id→auth.users
post_likes  (id PK, UNIQUE post_id+user_id)
```
- Full RLS on all tables
- Auto-create profile on signup (trigger)
- GIN indexes for Vietnamese full-text search

## Phase 4: Feature Audit

| Feature | Status | Location |
|---------|--------|----------|
| Homepage + Hero | ✅ | `app/page.tsx` + `components/home-client.tsx` |
| Post cards with excerpt | ✅ | `PostCard` component |
| Two-column layout (Theliems/TheScam) | ✅ | `home-client.tsx` |
| Realtime search (debounce) | ✅ | `searchPosts` + `SearchResultCard` |
| Post detail with comments | ✅ | `app/bai-viet/[slug]/` |
| Like/Unlike | ✅ | `post-detail-client.tsx` handles like + DB sync |
| Comment submission | ✅ | `post-detail-client.tsx` |
| Related posts | ✅ | Same category, limit 3 |
| View counter | ✅ | Increment on page load |
| Login (email + password) | ✅ | `app/dang-nhap/page.tsx` |
| Register (name + email + password) | ✅ | `app/dang-ky/page.tsx` |
| Email confirmation flow | ✅ | "Check your email" screen |
| Dark/Light theme toggle | ✅ | `home-client.tsx` sun/moon switch |
| Pixel art design (CRT, scanlines) | ✅ | `globals.css` + pixel fonts |
| Auth middleware | ✅ | `lib/supabase/middleware.ts` |
| SEO metadata per post | ✅ | `generateMetadata` |
| Category system | ✅ | Supabase `categories` table |
| RLS policies | ✅ | All tables, user/admin separation |
| **/dang-bai** (Create Post) | 🔴 | CTA button exists but page not found |
| **/tai-khoan** (Account page) | 🔴 | User icon links there but not implemented |
| Admin dashboard | 🔴 | `is_admin` flag + RLS ready but no UI |
| Password reset flow | 🔴 | Not implemented |
| `.env.local` on this machine | ❌ | Missing → can't `pnpm dev` yet |

## Phase 5: Mission Mapping

**Mission:** *"Sự thật là liêm chính — Cộng đồng liêm chính Việt Nam"*

Two pillars:
- **Theliems** (cyan) — Share integrity stories, real experiences, life lessons
- **TheScam** (red) — Scam alerts, fraud warnings, protect the community

Implied by mission but not yet built:
- Anyone should be able to **post** (Theliems story or TheScam alert) → `/dang-bai` missing
- Community should be able to **report** violations → report system missing
- Trustworthy content needs **moderation** → admin workflow missing

## Phase 6: Suggestions

| Tier | Feature | Rationale |
|------|---------|-----------|
| 🔥 | **/dang-bai — Create Post** | Core mission enabler — users can't share without it |
| 🔥 | **Setup .env.local + Supabase** | Prerequisite to run locally |
| 🔥 | **Admin moderation dashboard** | Mission requires trustworthy, reviewed content |
| ⚡ | **Comment/Report system** | Community building, self-policing |
| ⚡ | **Social sharing** | "Share to Facebook/Zalo" — spreads the mission |
| 📈 | **Bookmark/Save posts** | Engagement metric |
| 📈 | **User reputation/badges** | Incentivize quality contributions |
| 🔐 | **Password reset flow** | Basic UX requirement |
| 🔐 | **Deploy to Vercel** | CI/CD + public access |

## Raw Output Delivered

For reference: this audit was delivered to the user in a ~200-line message with markdown tables covering all 6 phases. The key was **systematic coverage**: every page checked, every DB table noted, every navigation link clicked (mentally) to see if the target page existed.

## Mistakes to Avoid

1. **Don't assume `gh repo clone` works** — always check the actual token scopes against what gh has cached
2. **Don't skip SQL migration files** — they show the intended data model even when no data exists yet
3. **Don't trust the README alone** — cross-reference with actual pages found in the app/ directory
4. **Every CTA button in the UI should link to an existing page** — if it doesn't, that's a missing feature (🔴)
