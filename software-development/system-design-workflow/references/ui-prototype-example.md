# UI Prototype Example — Knowledge Flow

> **Context:** Session Jul 2026 — user wanted "TikTok for knowledge" web app.
> User said: *"dựng tạm thời html lên để tôi review design đã"*.

## What was built

A single static HTML file (`knowledge-flow-preview.html`) with **3 interactive views**:

| View | Tab | Content |
|------|-----|---------|
| Library | 🏛 | Grid of topic cards (emoji + title + card count + badges) |
| Feed | ⚡ | Infinite-scroll cards (progress bar, like/bookmark, prev/next) |
| Book | 📖 | TOC sidebar + sequential reader with chapter nav |

## Key patterns used

### 1. Design System tokens as :root CSS variables
```css
:root {
  --bg-dark: #0D0D0D;
  --surface: #1B1B1D;
  --accent: #FFD600;
  --text-primary: #FFFFFF;
  --text-secondary: #8B8B8B;
  --radius-lg: 28px;
  --btn-radius: 999px;
  --btn-height: 56px;
}
```

### 2. View switching with vanilla JS
```html
<div class="view-tabs">
  <button class="view-tab active" data-view="library">🏛 Library</button>
  <button class="view-tab" data-view="feed">⚡ Feed</button>
  <button class="view-tab" data-view="book">📖 Book</button>
</div>

<div class="view-section active" id="view-library">...</div>
<div class="view-section" id="view-feed">...</div>
<div class="view-section" id="view-book">...</div>

<script>
document.querySelectorAll('.view-tab').forEach(tab => {
  tab.addEventListener('click', () => {
    document.querySelectorAll('.view-tab').forEach(t => t.classList.remove('active'));
    tab.classList.add('active');
    document.querySelectorAll('.view-section').forEach(s => s.classList.remove('active'));
    document.getElementById('view-' + tab.dataset.view).classList.add('active');
  });
});
</script>
```

### 3. Realistic Vietnamese content (not Lorem ipsum)
- Used actual knowledge from Hermes sessions (Attention mechanism, Server/Client Components, Async/Await)
- Vietnamese headings, descriptions, and body text
- Real-looking metadata (dates, reading times, card counts)

### 4. Interactive elements
- Topic card click → switches to Feed view
- Like button toggle (heart filled/unfilled)
- TOC item click → highlights active section
- Progress bars showing reading progress

### 5. Delivery via localtunnel
```bash
cd ~/knowledge-flow/preview/
python -m http.server 3003
npx.cmd localtunnel --port 3003 --subdomain knowledge-flow-preview
# → https://knowledge-flow-preview.loca.lt
```

## File structure
```
<project>/preview/
  <project>-preview.html    # The interactive HTML mockup
```

## Full pipeline (from this session)

After user approved the design ("triển khai đi"), the build followed this pattern:

### Phase A — Project scaffold
1. `create-next-app` with TypeScript, Tailwind, App Router, src-dir
2. Install deps: `@supabase/supabase-js @supabase/ssr` (and markdown renderers if needed)
3. Set up `.env.local` with Supabase credentials
4. Create Supabase client libs (`lib/supabase/client.ts`, `lib/supabase/server.ts`)
5. Create data access layer (`lib/supabase/api.ts` — typed functions for all queries)

### Phase B — Database schema + seed
1. Write SQL migration in `scripts/001_<name>_schema.sql`
2. Write seed data in `scripts/002_seed_data.sql`
3. Run via Supabase dashboard SQL Editor (or direct psql if credentials available)

### Phase C — Components with mock fallback
Key pattern — every page/component has a **mock fallback** so the app works even before DB is connected:

```tsx
// page.tsx (server component)
export default async function Page() {
  try {
    const data = await getData();   // Supabase query
    return <ClientComponent data={data} />;
  } catch (e) {
    return <ClientComponent data={[]} error={e.message} />;
  }
}

// client.tsx (client component)
export default function Client({ data, error }) {
  const displayData = data.length > 0 ? data : MOCK_DATA;
  const showMock = data.length === 0;
  // ...render with displayData
  {showMock && <div>⚡ Dữ liệu mẫu — chạy migration SQL để kích hoạt DB</div>}
}
```

### Phase D — API routes for auto-capture
```tsx
// app/api/knowledge/route.ts — Hermes auto-capture
export async function POST(req: NextRequest) {
  const { title, content, summary, tags, topic_slug } = await req.json();
  // Basic auth check against env var
  // Find or create topic by slug
  // Insert card with reading_time_sec calculated from content length
  // Return created card
}
```

### Phase E — Serve + tunnel
```bash
# Dev
npx next dev -p 3002

# Tunnel preview
npx.cmd localtunnel --port 3002 --subdomain <project>-app
# → https://<project>-app.loca.lt
```

## Mock data fallback pattern
This pattern was critical because Supabase tables didn't exist yet (no direct DB access for migration):

1. **Server component** tries to fetch from Supabase, catches error
2. **Client component** receives `data: []` and `error: string | null`
3. If `error` or `data.length === 0`, render `MOCK_DATA` arrays defined in the client component
4. Show a banner: "⚡ Dữ liệu mẫu — chạy migration SQL trên Supabase dashboard để kích hoạt DB thật"
5. When migration runs and DB has data, app auto-switches from mock to real — no redeploy needed

**Mock data structure:** same TypeScript interface as real data, same shape, so rendering code is identical.

## What user reviewed
- Layout and spacing of each view mode
- Color scheme (Dark BG, Yellow accent)
- Content density (enough info per card?)
- Navigation between views
- Mobile responsiveness

## Common pitfalls
1. Arch diagram ≠ UI prototype — user needs to SEE the app, not the pipes
2. Don't use component libs for prototype — pure HTML+CSS is faster to iterate
3. Design System tokens must be EXACT — user notices wrong colors/radius immediately
4. Must be accessible from mobile — user reviews on phone, not desktop
5. Use real content from past sessions — placeholder text hides readability issues
