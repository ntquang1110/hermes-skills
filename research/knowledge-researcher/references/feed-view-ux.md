## Feed View — UX Patterns

### Card preview (inline)
- Title → `<Link href="/card/[id]">` (hover yellow)
- Summary (italic) + date/reading time
- Content preview: first 300 chars, `line-clamp-4`
- **📖 Đọc tiếp** → links to detail page `/card/[id]`
- **🔗 Bản gốc** → external link to source_url (if exists)
- **🔖 Lưu** → local bookmark toggle
- Topic filter dropdown at top (all topics + each topic slug)

### Infinite Scroll (Feed)

**File:** `src/app/feed-client.tsx`

**Pattern:** Client-side batch rendering with IntersectionObserver.

- `BATCH_SIZE = 20` — initially renders 20 cards, loads more as user scrolls
- States: `visibleCount` (number, starts = BATCH_SIZE), `sentinelRef` (div at bottom)
- `IntersectionObserver` with `rootMargin: "200px"` triggers `setVisibleCount(prev => Math.min(prev + BATCH_SIZE, filtered.length))`
- Reset `visibleCount` on filter change: `useEffect(() => setVisibleCount(BATCH_SIZE), [topicFilter, readFilter])`

**Component structure:**
```typescript
const [visibleCount, setVisibleCount] = useState(BATCH_SIZE);
const sentinelRef = useRef<HTMLDivElement>(null);

const visibleCards = filtered.slice(0, visibleCount);
const hasMore = visibleCount < filtered.length;

// Observer
useEffect(() => {
  const el = sentinelRef.current;
  if (!el) return;
  const observer = new IntersectionObserver(
    (entries) => {
      if (entries[0].isIntersecting)
        setVisibleCount(prev => Math.min(prev + BATCH_SIZE, filtered.length));
    },
    { rootMargin: "200px" }
  );
  observer.observe(el);
  return () => observer.disconnect();
}, [filtered.length]);
```

**Sentinel JSX (after cards, before empty state):**
```tsx
{hasMore && (
  <div ref={sentinelRef} className="text-center py-6">
    <div className="inline-block w-5 h-5 border-2 border-[var(--color-accent)] border-t-transparent rounded-full animate-spin" />
    <p className="text-xs mt-2">Đang tải thêm...</p>
  </div>
)}
{!hasMore && filtered.length > BATCH_SIZE && (
  <div className="text-center py-6 text-xs">─ Đã hiển thị tất cả {filtered.length} bài ─</div>
)}
```

**IMPORTANT:** `filtered` must be computed via `useMemo` (not plain `const`) so the IntersectionObserver effect can depend on `filtered.length` without the ReferenceError "cannot access before initialization":

```typescript
const filtered = useMemo(() => topicFiltered.filter(c => {
  if (readFilter === "unread") return !readIds.has(c.id);
  if (readFilter === "read") return readIds.has(c.id);
  return true;
}), [topicFiltered, readFilter, readIds]);
```

### Read Status — đã đọc / chưa đọc (Feed + Card detail)

**Storage:** `data/read-status.json` — local JSON file, no DB migration needed. Safe to delete → resets all cards to unread.

**API (`/api/read-status`):**
```
GET              → { readIds: string[] }
PATCH ?id=X&action=read    → { isRead: true, count: N }
PATCH ?id=X&action=unread  → { isRead: false, count: N }
PATCH ?id=X&action=toggle  → { isRead: bool, count: N }
```

**Feed — filter bar (3 buttons, default: `🔥 Chưa đọc`):**
```
🔥 Chưa đọc  |  📖 Đã đọc  |  ⚡ Tất cả
```
- Counter header: `X / Y cards · 🔥 Z chưa đọc`
- Unread cards: **yellow dot** indicator (`w-2 h-2 rounded-full bg-[var(--color-accent)]`)
- Read cards: `opacity-60` on card container + `✅` after title

**Card detail — auto-mark on view:**
1. `useEffect` on mount fetches `/api/read-status` → checks if card is already read
2. If NOT read → PATCH `/api/read-status?id=X&action=read` (silent, no user action needed)
3. Shows **✅ Đã đọc** badge in topic/tag row (clickable to toggle)
4. Bottom nav includes toggle button: "✅ Đánh dấu đã đọc" / "↩ Đánh dấu chưa đọc"

**Flow:** Server page (`page.tsx`) fetches all cards once → passes to `FeedClient` (client component) → `useEffect` fetches read status → filters/sorts client-side. No polling, no extra server renders.

**PITFALL — back button (bfcache) giữ state cũ:** khi user đọc card rồi bấm nút Back trình duyệt, browser restore feed từ bfcache — `useEffect([])` KHÔNG chạy lại → readIds stale → bài vừa đọc vẫn hiện "chưa đọc". Fix: thêm `pageshow` + `focus` listeners refetch read-status (handle cả back button lẫn chuyển tab):
```js
useEffect(() => {
  const load = () => {
    fetch("/api/read-status")
      .then(r => r.json())
      .then(data => { if (data.readIds) setReadIds(new Set(data.readIds)); })
      .catch(() => {}).finally(() => setLoadingRead(false));
  };
  load();
  window.addEventListener("pageshow", load);
  window.addEventListener("focus", load);
  return () => {
    window.removeEventListener("pageshow", load);
    window.removeEventListener("focus", load);
  };
}, []);
```

### Live Search Dropdown (TopBar)

**File:** `src/components/TopBar.tsx`

The TopBar has a live search dropdown (`absolute top-full` dropdown) that shows results as the user types — no Enter key, no page navigation.

**Implementation:**

1. Fetch all cards once on mount via `fetch("/api/cards")` → store in `cards` state
2. Input `onChange` sets `query` state → `useMemo` filters matching cards (title + summary, `slice(0, 10)`)
3. On `onFocus` → set `focused = true` → dropdown appears (if `query.trim()` non-empty)
4. Click outside → close dropdown (via `document.addEventListener("mousedown", handler)`)
5. Each result is a `<Link href={/card/${c.id}}>` → click navigates to card and clears query

**Two instances (mobile + desktop) using separate refs for outside-click detection:**

```tsx
const mobileRef = useRef<HTMLDivElement>(null);
const desktopRef = useRef<HTMLDivElement>(null);
const dropRef = useRef<HTMLDivElement>(null);

// Outside-click handler
useEffect(() => {
  const handler = (e: MouseEvent) => {
    const isInside =
      (mobileRef.current && mobileRef.current.contains(e.target as Node)) ||
      (desktopRef.current && desktopRef.current.contains(e.target as Node)) ||
      (dropRef.current && dropRef.current.contains(e.target as Node));
    if (!isInside) setFocused(false);
  };
  document.addEventListener("mousedown", handler);
  return () => document.removeEventListener("mousedown", handler);
}, []);
```

**PITFALL:** Both mobile and desktop inputs share the same `query` + `results` state but need SEPARATE wrapper refs (`mobileRef` / `desktopRef`). If they share the same `inputRef`, clicking on the mobile input won't keep the dropdown open (the outside-click handler only checks the desktop input).

**Dropdown styling (desktop):**
```tsx
<div ref={dropRef} className="absolute top-full left-0 right-0 mt-1 bg-[var(--color-bg-dark)] border border-[var(--color-border)] rounded-xl shadow-2xl overflow-hidden z-50 max-h-[360px] overflow-y-auto">
  {results.map(c => (
    <Link key={c.id} href={`/card/${c.id}`} onClick={() => { setQuery(""); setFocused(false); }}
      className="block px-4 py-3 hover:bg-[var(--color-surface)] border-b border-[var(--color-border)] last:border-0">
      <div className="text-sm text-white line-clamp-1">{c.title}</div>
      <div className="text-xs text-[var(--color-text-tertiary)] line-clamp-1">{c.summary}</div>
    </Link>
  ))}
  <div className="px-4 py-2 text-[10px] text-[var(--color-text-tertiary)] text-center border-t">
    🔍 {results.length} kết quả · gõ tiếp để tìm thêm
  </div>
</div>
```

**Mobile:** Same logic, smaller padding/text, `sm:hidden`. Desktop: `hidden sm:flex`.

### Hydration-safe Time Display

**PITFALL:** `Date.toLocaleString("vi-VN", {hour:"2-digit", minute:"2-digit"})` causes SSR/client hydration mismatch. Node.js produces `"03:47 22/07/2026"` while the browser produces `"10:47 22/07/2026"` (timezone difference). React catches the text mismatch and throws 6+ silent exceptions per card page.

**Fix:** Use `toLocaleDateString("vi-VN")` (date only, same on server/client) + `toISOString().slice(11,16)` (UTC time, same on server/client):

```jsx
<span>📅 {new Date(card.created_at).toLocaleDateString("vi-VN")} {new Date(card.created_at).toISOString().slice(11,16)} · ⏱ 12 phút</span>
```

**Files affected:** `feed-client.tsx`, `card-detail-client.tsx`, `feed/feed-client.tsx`, `book/book-client.tsx`, `search/search-client.tsx`

### Delete card button

**File:** `src/app/card/[id]/card-detail-client.tsx`

Added at the bottom of card detail page (both tabs), next to the read-status toggle:

```tsx
const handleDelete = async () => {
  if (!card) return;
  if (!window.confirm(`Xoá \"${card.title.slice(0, 60)}\"? Hành động này không thể hoàn tác.`)) return;
  try {
    await fetch(`/api/cards?id=${card.id}`, { method: "DELETE" });
    window.location.href = "/";
  } catch {}
};
```

Button: `🗑 Xoá`, red border (`rgba(255,100,100,0.3)`), `color: #ff6464`, `cursor-pointer`.

Same row layout (flex gap-2): [✅ Đánh dấu đã đọc] [🗑 Xoá] ... [← Về Feed]

### Share Button — Native Share + Preview Link

**File:** `src/app/card/[id]/card-detail-client.tsx`

A **🔗 Share** button is placed in the card detail header (next to date/reading-time), visible immediately when the user opens a card.

**Implementation:**
```tsx
const handleShare = async () => {
  if (!card) return;
  const url = `https://preview.thefirstonly.com/card/${card.id}`;
  try {
    await navigator.clipboard.writeText(url); // always copy to clipboard
  } catch {}
  if (navigator.share) {
    // Mobile: native share sheet (Messenger, Zalo, Telegram...)
    try { await navigator.share({ title: card.title, url }); } catch {}
  } else {
    // Desktop: show "✅ Đã copy link" toast on the button itself
    const btn = document.activeElement as HTMLElement;
    if (btn) {
      const orig = btn.textContent;
      btn.textContent = "✅ Đã copy link";
      setTimeout(() => { btn.textContent = orig; }, 2000);
    }
  }
};
```

**Button position:** In the metadata row (📅 date · ⏱ read time · 🔗 Share), using `ml-auto` to right-align:
```tsx
<button onClick={handleShare}
  className="ml-auto px-3 py-1 rounded-full text-[10px] cursor-pointer flex items-center gap-1"
  style={{border: `1px solid ${AZU_STYLES.cobalt}33`, color: AZU_STYLES.cobalt}}>
  🔗 Share
</button>
```

**Share URL:** `https://preview.thefirstonly.com/card/{card.id}` — uses the clean preview domain, NOT `kflow.thefirstonly.com`.

### Preview URL — Clean OG Tags via Host-based Redirect

**Architecture:** When a request hits `preview.thefirstonly.com/card/{id}`, the page server component (`src/app/card/[id]/page.tsx`) detects the hostname via `headers()` from `next/headers` and redirects to `/api/preview?id={id}` which returns a clean HTML page with OG tags but NO "Knowledge Flow" branding.

**Card page — host-based redirect:**
```tsx
import { headers } from "next/headers";

export default async function CardPage({ params }) {
  const { id } = await params;
  const hdrs = await headers();
  if (hdrs.get("host") === "preview.thefirstonly.com") {
    redirect(`/api/preview?id=${id}`);
  }
  // ... normal KFlow rendering
}
```

**PITFALL:** `redirect()` from `next/navigation` in a server component throws a `NEXT_REDIRECT` that Next.js handles internally. Only `preview.thefirstonly.com` should trigger the redirect — NOT `localhost:3003`, NOT `kflow.thefirstonly.com`. The `headers().get("host")` check must be strict.

**Preview API route (`src/app/api/preview/route.ts`):**
```tsx
export async function GET(req: NextRequest) {
  const id = req.nextUrl.searchParams.get("id");
  if (!id) return new NextResponse("Missing id", { status: 400 });

  const SUPABASE_URL = process.env.NEXT_PUBLIC_SUPABASE_URL!;
  const SUPABASE_KEY = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!;

  // Fetch card from Supabase REST API
  const res = await fetch(
    `${SUPABASE_URL}/rest/v1/knowledge_cards?id=eq.${id}&select=*`,
    { headers: { apikey: SUPABASE_KEY, Authorization: `Bearer ${SUPABASE_KEY}` } }
  );
  const card = (await res.json())?.[0];
  if (!card) { /* render "not found" */ }

  // Render clean HTML with just title + description + OG tags
  return new NextResponse(`<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${escapedTitle}</title>
  <meta name="description" content="${escapedDesc}">
  <meta property="og:title" content="${escapedTitle}">
  <meta property="og:description" content="${escapedDesc}">
  <meta property="og:type" content="article">
  <meta property="og:url" content="https://preview.thefirstonly.com/card/${id}">
  <meta property="og:site_name" content="Chia sẻ kiến thức">
  <meta name="twitter:card" content="summary_large_image">
  ...
</head>
<body>...</body>
</html>`, { headers: { "Content-Type": "text/html; charset=utf-8" } });
}
```

**OG tags are deliberately NEUTRAL:** `og:site_name: "Chia sẻ kiến thức"` — no "Knowledge Flow" anywhere in the preview. The domain `preview.thefirstonly.com` doesn't reveal the platform either.

**Middleware rewrite (DEPRECATED — doesn't work in Next.js 16):**
Initial approach used `middleware.ts` with `NextResponse.rewrite()` to convert `/card/{id}` → `/api/preview?id={id}`. This failed because:
- `NextResponse.rewrite()` with modified `searchParams` on `req.nextUrl.clone()` does NOT preserve query params in the rewritten request
- Neither `url.searchParams.set()` nor `url.search = "?id=xxx"` nor `new URL(...)` approach worked
- The rewritten URL reaches the correct route handler but `req.nextUrl.searchParams.get("id")` returns `null`

**Verdict:** Use page-component host detection + `redirect()` instead. No middleware involved.

### Next.js 16 Route Handler — `params` is `Promise`

In Next.js 16, both page components and route handlers receive `params` wrapped in `Promise`:

```tsx
// Page component
export default async function Page({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  // ...
}

// Route handler
export async function GET(req: NextRequest, { params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  // ...
}
```

**Type error if omitted:** `Type '...' does not satisfy the constraint ... Types of property 'params' are incompatible. Type '...' is not assignable to type 'Promise<...>'`

### Schedule Page UI

**File:** `src/app/schedule/page.tsx` (server), `src/app/schedule/schedule-client.tsx` (client)

Replaced the bare API links with a proper UI:
- Filter tabs: ⏳ Chờ đăng / ✅ Đã đăng / 📋 Tất cả (with counts)
- Search input for filtering by title
- Grouped by month with date cards
- Each card: date column · title link · status badge · scheduled date · ↗ external link
- Footer: total count + last posted date

**Data:** `GET /api/schedule` → `{ queue: [{id, title, url, scheduled_date, posted_date, status}], total, pending, posted }`

### Card page returns Response — NOT Allowed

**PITFALL:** You CANNOT return `new Response(...)` directly from a page component in Next.js 16. The page component must return `ReactNode`. Attempting to return `Response` causes:
```
Type 'Promise<Response | Element>' is not assignable to type 'ReactNode | Promise<ReactNode>'
```

**Fix:** Use `redirect()` for preview mode (which throws an internal NEXT_REDIRECT error handled by the framework), OR create a separate route handler at `/api/...` for non-HTML responses.

### Card detail 2-tab system
- Full content render with markdown
- If `source_url` exists → prominent **📂 Xem bản đầy đủ** button + content below
- If no source_url → notice: "không có link bản gốc — nội dung đã hiển thị đầy đủ"
- ← Về Feed link
- Topic badge + tags + summary highlight box

### Mobile responsive rules
- Header: Logo+Search on row 1, tabs on row 2 (wrap via `flex-col sm:flex-row`)
- Book TOC: hidden on mobile, hamburger button bottom-right, opens fullscreen overlay
- No horizontal scroll — everything wraps

