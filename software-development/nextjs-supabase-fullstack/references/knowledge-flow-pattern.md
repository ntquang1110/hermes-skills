# Knowledge Flow — Multi-View Next.js Knowledge App

Concrete example of a Next.js 16 + Supabase knowledge management system with 3 views (Feed/Book/Research), cron auto-research, and mock-data fallback.

## Project Structure

```
~/knowledge-flow/
├── src/app/
│   ├── page.tsx                # Feed view (homepage, server component)
│   ├── feed-client.tsx          # Feed client (infinite scroll, filter, read-status)
│   ├── layout.tsx               # Root layout + JetBrains Mono + Inter
│   ├── globals.css              # Design System v1.0 tokens + table styles
│   ├── book/
│   │   ├── page.tsx             # Book server
│   │   └── book-client.tsx      # Sequential reader + TOC sidebar
│   ├── research/
│   │   └── page.tsx             # Research Queue UI
│   ├── card/
│   │   └── [id]/
│   │       ├── page.tsx         # Card detail server
│   │       └── card-detail-client.tsx  # Full markdown render + auto-read-mark
│   ├── search/
│   │   └── page.tsx             # Full-text search
│   └── api/
│       ├── cards/               # CRUD cards (GET, POST, DELETE, PATCH)
│       ├── topics/              # CRUD topics
│       ├── knowledge/           # Hermes auto-capture endpoint
│       ├── read-status/         # Read/unread state (file-backed JSON)
│       └── research-queue/      # Queue (file-backed JSON)
├── components/
│   └── TopBar.tsx               # Logo + view switcher + search
├── lib/supabase/
│   ├── client.ts                # Browser client
│   ├── server.ts                # Server client
│   └── api.ts                   # Data access functions
├── scripts/
│   ├── 001_knowledge_flow_schema.sql
│   ├── 002_seed_data.sql
│   └── import-notion.js
└── data/
    ├── research-queue.json
    └── read-status.json         # Local read/unread state
```

## Read/Unread Status Feature

### API: `/api/read-status`

File-backed (no DB migration needed). Stores card IDs in `data/read-status.json`.

```
GET  /api/read-status              → { readIds: [...] }
PATCH /api/read-status?id=X&action=read    → { isRead: true, count: N }
PATCH /api/read-status?id=X&action=unread  → { isRead: false, count: N }
PATCH /api/read-status?id=X&action=toggle  → { isRead: bool, count: N }
```

### Feed filter bar (default: unread only)

Three filter buttons at top of Feed, default active = "🔥 Chưa đọc":

```
[🔥 Chưa đọc] [📖 Đã đọc] [⚡ Tất cả]
```

Counter in header: `X / Y cards · 🔥 Z chưa đọc`

### Unread visual indicators

- **Unread cards:** yellow dot (`w-2 h-2 rounded-full bg-[--accent]`) before tags
- **Cards:** `opacity-60 hover:opacity-100` when read, subtle ✅ after title
- **Read badge** in card detail: `✅ Đã đọc` (clickable, toggle to unread)

### Auto-mark on view

When visiting `/card/[id]`, the `card-detail-client.tsx` automatically PATCHes the API to mark the card as read on initial load. Only fires once per card — skips if already marked. User can also manually toggle via the badge or the bottom button.

### Implementation Notes

- Use `useEffect` + `fetch` to load read IDs on Feed mount
- Use `Set<string>` for O(1) read/unread lookups in the filter
- Auto-mark only fires for cards not already read (check first)
- No loading state needed — unread filter gracefully shows "Bạn đã đọc hết" when empty
- Read state persists across sessions in `data/read-status.json`
- To reset: delete the file and restart the dev server

## Three View Patterns

### Feed View (Homepage `/`)
- **Infinite scroll** — show all cards, no pagination/prev-next
- **Topic filter** dropdown at top
- **Read-status filter** defaults to "Chưa đọc"
- Card preview: tags → title (link to detail) → summary → date → actions
- Actions: [🔖 Lưu] [📖 Đọc tiếp → /card/[id]] [🔗 Bản gốc → external URL]
- Content preview: first 300 chars, line-clamp-4, markdown rendered
- Sort: newest first (created_at DESC)
- No Library page — Feed IS the homepage

### Book View (`/book`)
- TOC sidebar (left desktop, collapsible overlay on mobile)
- Card ID-based state: `const [currentId, setCurrentId] = useState(cards[0]?.id)`
- Content rendered with `key={currentId}` for React force re-render
- Groups cards by first tag name (buildSections function)
- Progress: currentIdx / total + percentage
- Prev/Next buttons at bottom

### Research Queue (`/research`)
- Add form: topic, detail (optional), topic_slug (select)
- Lists grouped by status: pending → researching → done
- File-backed JSON API (data/research-queue.json)
- Cron (every 2h) picks pending → researches → imports → marks done

## Markdown Rendering — Table Support Required

The custom `renderMarkdown()` function must handle tables BEFORE the paragraph-wrapping section:

```javascript
// Tables — add before the paragraph section
h = h.replace(/\\|(.+)\\|/g, (_, row) => {
  const cols = row.split('|').filter(Boolean).map(c => c.trim());
  if (cols.every(c => /^[-:\\s]+$/.test(c))) return '';
  return `<tr>${cols.map(c => `<td>${c}</td>`).join('')}</tr>`;
});
h = h.replace(/(<tr>.*<\\/tr>\\n?)+/g, m => `<table>${m}</table>`);
h = h.replace(/<\\/table>\\n<table>/g, '');
```

CSS in globals.css:
```css
.markdown-content table { width: 100%; border-collapse: collapse; margin: 16px 0; }
.markdown-content td { border: 1px solid #2A2A2E; padding: 10px 12px; color: #8B8B8B; }
.markdown-content tr:nth-child(even) td { background: rgba(255,255,255,0.02); }
```

## Navigation: Use `<a>` Everywhere

Elements that navigate between pages MUST use `<a href>` not `<button onClick={router.push()}>`:

- Tab bar items (3 tabs: Feed/Book/Research)
- Card titles → detail page
- Topic cards → filtered feed
- Back buttons
- "Đọc tiếp" → detail page
- Search results

Reason: when accessed through a tunnel on mobile, React hydration can be delayed. Native `<a>` links work immediately without JS. Reserve `<button>` for non-navigation toggles (bookmark, like).

## Mock Data Fallback Pattern

```tsx
const cards = dbCards.length > 0 ? dbCards : MOCK_CARDS;
```

This ensures the app renders immediately even without a database. The mock data has the same shape as real data, so the UI is always functional. A banner indicates mock vs real data.

## Design System v1.0 Tokens

```css
--bg-dark: #0D0D0D;         --surface: #1B1B1D;
--accent: #FFD600;           --accent-dim: rgba(255,214,0,0.15);
--text-primary: #FFFFFF;     --text-secondary: #8B8B8B;
--text-tertiary: #5C5C5E;    --border: #2A2A2E;
--radius-lg: 28px;           --radius-full: 999px;
--font-heading: 'JetBrains Mono', monospace;
--font-body: 'Inter', sans-serif;
```

## Cron Auto-Research

Schedule: every 2h. Skills: web-research.

Flow:
1. GET /api/research-queue → check for pending items
2. If pending: PATCH `{status: "researching"}` → research → import → PATCH `{status: "done", card_id}`
3. If queue empty: auto-pick from focus topics (chan-nuoi, sinh-hoc, nghien-cuu → rotate)
4. Write card: Vietnamese diacritics + real emoji + source_url + citations
5. POST to http://localhost:3003/api/knowledge

**⚠️ CRITICAL: The cron model hallucinates the port (e.g. 6680 instead of 3003). State port 3 times in the prompt.**

**⚠️ DUPLICATE PREVENTION:** Cron prompts now include a mandatory check step:
- Before researching new topic → `curl -s http://localhost:3003/api/cards` to list existing cards
- Compare title and content for significant overlap (>60% keyword match)
- Skip if already exists in Knowledge Flow
- List of already-researched topics included in cron prompt to prevent re-research

## Vietnamese Encoding Requirements

Write_action: specify encoding in EVERY text step. "VIẾT TIẾNG VIỆT CÓ DẤU" — "Cơ chế tác dụng" NOT "co che tac dung". 

Use real emoji characters (🧬🐷🔬), NOT shortcodes (`:dna:` `:warning:`) which render as raw text.
