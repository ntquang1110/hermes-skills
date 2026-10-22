---
name: nextjs-supabase-fullstack
title: Next.js + Supabase Full-Stack Workflow
description: Build full-stack features with Next.js 15/16, Supabase (PostgreSQL + Auth), and deploy via localtunnel or Cloudflare tunnel on Windows.
tags:
  - nextjs
  - supabase
  - postgresql
  - fullstack
  - migration
  - deployment
  - windows
domain: software-development
---

# Next.js + Supabase Full-Stack Workflow

Build and deploy full-stack features with Next.js App Router and Supabase (PostgreSQL + Auth) on this Windows machine.

## When to use

- You need to create a new feature requiring database schema changes + new pages + new API logic
- You set up a new Supabase project and need to run migrations
- You need to connect a local Next.js dev server to a Supabase backend
- You need to deploy the app via tunnel for preview or production

## Workflow overview

```
1. Reconnaissance — understand existing features, DB schema, env setup
2. Database Migration — design schema, write SQL, execute on Supabase
3. Environment — configure .env.local, verify connectivity
4. Feature Implementation — server pages → client components → update existing
5. Build Verification — pnpm build, check 0 errors
6. Deployment — start production server + tunnel (localtunnel or Cloudflare)
```

---

## 1. Reconnaissance

Before writing any code, understand the project structure:

```bash
# App structure
find ~/<project>/app -type f -name "*.tsx" -o -name "*.ts" | sort

# Supabase client setup
cat ~/<project>/lib/supabase/client.ts
cat ~/<project>/lib/supabase/server.ts

# Package dependencies
cat ~/<project>/package.json | grep -E "supabase|next|react"

# Check current env
cat ~/<project>/.env.local 2>/dev/null || echo "No .env.local"
```

## 2. Database Migration

### Write the migration

Create a SQL file in `~/<project>/scripts/` with sequential numbering:

```sql
-- scripts/NNN_feature_name.sql
-- Include in order:
-- 1. CREATE TABLE IF NOT EXISTS (new tables)
-- 2. ALTER TABLE (modify existing tables with new columns)
-- 3. ENABLE ROW LEVEL SECURITY
-- 4. RLS POLICIES (public read, auth insert, admin write patterns)
-- 5. INDEXES (for performance)
-- 6. TRIGGERS (auto-profile creation, counter updates)
-- 7. SEED DATA (categories, tags, sample content)

-- For pg_trgm indexes, install extension FIRST (separate step on Supabase)
CREATE EXTENSION IF NOT EXISTS pg_trgm;
-- Then create GIN trgm indexes:
CREATE INDEX IF NOT EXISTS idx_name ON public.table USING gin(column gin_trgm_ops);
```

### Execute the migration

Connect via the direct postgres connection string:

```bash
cat 'C:\Users\<user>\<project>\scripts\NNN_migration.sql' | python -c "
import sys, psycopg2
sql = sys.stdin.read()
conn = psycopg2.connect('postgresql://postgres:<password>@db.<project>.supabase.co:5432/postgres')
cur = conn.cursor()
cur.execute(sql)
conn.commit()
print('Migration OK!')
# Verify
cur.execute(\"\"\"SELECT table_name FROM information_schema.tables
               WHERE table_schema='public' AND table_type='BASE TABLE'
               ORDER BY table_name\"\"\")
print('Tables:', [r[0] for r in cur.fetchall()])
cur.close()
conn.close()
"
```

**Important:** If the migration uses pg_trgm, install the extension FIRST in a separate step, then run the migration. Otherwise the index creation fails.

### Common migration patterns

**Multi-table migration with foreign keys:**
```sql
CREATE TABLE IF NOT EXISTS public.parent_table (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL UNIQUE,
  slug TEXT NOT NULL UNIQUE,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS public.child_table (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  parent_id UUID REFERENCES public.parent_table(id) ON DELETE CASCADE,
  user_id UUID REFERENCES auth.users(id) ON DELETE SET NULL,
  some_value TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(parent_id, user_id)
);
```

**RLS pattern (public read, auth insert, admin write):**
```sql
ALTER TABLE public.my_table ENABLE ROW LEVEL SECURITY;

CREATE POLICY "select_all" ON public.my_table FOR SELECT USING (true);
CREATE POLICY "insert_auth" ON public.my_table FOR INSERT WITH CHECK (auth.uid() IS NOT NULL);
CREATE POLICY "update_admin" ON public.my_table FOR UPDATE 
  USING (EXISTS (SELECT 1 FROM public.profiles WHERE id = auth.uid() AND is_admin = true));
CREATE POLICY "delete_admin" ON public.my_table FOR DELETE 
  USING (EXISTS (SELECT 1 FROM public.profiles WHERE id = auth.uid() AND is_admin = true));
```

**Auto-increment counter via trigger:**
```sql
CREATE OR REPLACE FUNCTION public.update_counter()
RETURNS TRIGGER LANGUAGE plpgsql SECURITY DEFINER AS $$
BEGIN
  IF TG_OP = 'INSERT' THEN
    UPDATE public.parent_table SET count = count + 1 WHERE id = NEW.parent_id;
    RETURN NEW;
  ELSIF TG_OP = 'DELETE' THEN
    UPDATE public.parent_table SET count = count - 1 WHERE id = OLD.parent_id;
    RETURN OLD;
  END IF;
END;
$$;

CREATE TRIGGER on_change AFTER INSERT OR DELETE ON public.child_table
  FOR EACH ROW EXECUTE FUNCTION public.update_counter();
```

## 3. Environment Setup

After migrations, configure `.env.local`:

```bash
# ~/<project>/.env.local
NEXT_PUBLIC_SUPABASE_URL=https://<project>.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=<anon-key>

# Optional
NEXT_PUBLIC_DEV_SUPABASE_REDIRECT_URL=http://localhost:3000/auth/callback
```

**Test the key works:**
```bash
curl -s -H "apikey: <anon-key>" "https://<project>.supabase.co/rest/v1/categories?select=name"
# Expected: [{"name":"...", ...}]
```

## 4. Feature Implementation

### Pattern: Server page → Client component

**Server page** (handles data fetching, auth check, metadata):
```typescript
// app/<feature>/page.tsx
import { createClient } from "@/lib/supabase/server";
import FeatureClient from "./feature-client";

export const metadata = { title: "..." };

export default async function FeaturePage() {
  const supabase = await createClient();
  
  const { data: items } = await supabase
    .from("my_table")
    .select("*, related_table(*)")
    .order("created_at", { ascending: false });
    
  return <FeatureClient items={items || []} />;
}
```

**Client component** (handles interactivity, forms, state):
```typescript
"use client";
import React, { useState } from "react";
import { createClient } from "@/lib/supabase/client";

export default function FeatureClient({ items }: { items: Item[] }) {
  const supabase = createClient();
  // ... state, effects, handlers
}
```

### Local file-backed API pattern for single-user state

When you need **per-user state** (read status, bookmarks, preferences) in a single-user app, prefer a **local JSON file API** over a database migration. Benefits: no schema changes, no RLS policies, simple reset.

**Pattern — API route backed by JSON file:**

```typescript
// src/app/api/read-status/route.ts
import { NextRequest, NextResponse } from "next/server";
import * as fs from "fs";
import * as path from "path";

const STATUS_FILE = path.join(process.cwd(), "data", "read-status.json");

function getData(): string[] {
  try {
    if (fs.existsSync(STATUS_FILE)) {
      const data = JSON.parse(fs.readFileSync(STATUS_FILE, "utf-8"));
      return Array.isArray(data) ? data : [];
    }
  } catch {}
  return [];
}

function saveData(ids: string[]) {
  const dir = path.dirname(STATUS_FILE);
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(STATUS_FILE, JSON.stringify(ids), "utf-8");
}

export async function GET() {
  return NextResponse.json({ readIds: getData() });
}

export async function PATCH(req: NextRequest) {
  const { searchParams } = new URL(req.url);
  const id = searchParams.get("id");
  const action = searchParams.get("action") || "toggle"; // "toggle" | "read" | "unread"
  
  if (!id) return NextResponse.json({ error: "id required" }, { status: 400 });

  let ids = getData();
  const wasIn = ids.includes(id);

  if (action === "read" && !wasIn) ids.push(id);
  else if (action === "unread" && wasIn) ids = ids.filter(x => x !== id);
  else if (action === "toggle") ids = wasIn ? ids.filter(x => x !== id) : [...ids, id];

  saveData(ids);
  return NextResponse.json({ isRead: ids.includes(id), count: ids.length });
}
```

**Client consumption pattern (React):**

```tsx
"use client";
import { useState, useEffect } from "react";

function useReadStatus() {
  const [readIds, setReadIds] = useState<Set<string>>(new Set());

  useEffect(() => {
    fetch("/api/read-status")
      .then(r => r.json())
      .then(d => setReadIds(new Set(d.readIds)))
      .catch(() => {});
  }, []);

  const toggle = async (id: string) => {
    const res = await fetch(`/api/read-status?id=${id}&action=toggle`, { method: "PATCH" });
    const d = await res.json();
    setReadIds(prev => {
      const next = new Set(prev);
      if (d.isRead) next.add(id); else next.delete(id);
      return next;
    });
  };

  return { readIds, toggle };
}
```

**When to use:**
- ✅ Single-user app or prototype
- ✅ State that can be lost on server reset (dev only)
- ✅ Features that would otherwise require adding a column to an existing DB table
- ❌ Production multi-user data — use the database
- ❌ Data that must survive deployment restarts — use Supabase

### ⚠️ bfcache stale-state bug: read status (or any local state) is stale after browser Back

**Symptom:** User opens a card, it auto-marks as read (or they toggle it), they press the **browser Back button** to return to the feed, and the feed STILL shows the item as unread — even though the API confirms the state persisted.

**Root cause:** The browser's back-forward cache (bfcache) restores the previous page's DOM and React state **without re-running `useEffect`**. The feed mounted earlier, fetched read-status once with `useEffect([])`, and never re-fetches when restored from bfcache. Client-side `<Link>` navigation remounts the page (so it refetches correctly), but browser Back and tab-refocus do NOT.

**Fix — refetch on `pageshow` + `focus`:**

```tsx
"use client";
import { useState, useEffect } from "react";

export default function FeedClient() {
  const [readIds, setReadIds] = useState<Set<string>>(new Set());

  useEffect(() => {
    const load = () => {
      fetch("/api/read-status")
        .then((r) => r.json())
        .then((data) => {
          if (data.readIds) setReadIds(new Set(data.readIds));
        })
        .catch(() => {});
    };
    load();
    // bfcache restore (Back button) + tab refocus — both bypass useEffect([]) on remount
    window.addEventListener("pageshow", load);
    window.addEventListener("focus", load);
    return () => {
      window.removeEventListener("pageshow", load);
      window.removeEventListener("focus", load);
    };
  }, []);
  // ...
}
```

**When to apply:** ANY list/feed page whose displayed state is derived from a shared mutable source (read-status, bookmarks, likes, notifications) and that the user can navigate away from and return to via browser Back. The `pageshow` event fires on every bfcache restore; `focus` fires when the tab regains focus. Both are cheap — one small GET each.

### Adding DELETE and PATCH endpoints to existing Next.js API routes

To add new HTTP verbs to an existing Next.js App Router API route, export additional named functions in the same `route.ts` file:

```typescript
// src/app/api/cards/route.ts — add DELETE and PATCH alongside existing GET/POST

export async function DELETE(req: NextRequest) {
  const supabase = await createClient();
  const { searchParams } = new URL(req.url);
  const id = searchParams.get("id");
  const ids = searchParams.get("ids");   // comma-separated batch delete

  if (!id && !ids) {
    return NextResponse.json({ error: "id or ids param required" }, { status: 400 });
  }

  if (ids) {
    const idList = ids.split(",").filter(Boolean);
    const { error } = await supabase.from("knowledge_cards").delete().in("id", idList);
    if (error) return NextResponse.json({ error: error.message }, { status: 500 });
    return NextResponse.json({ deleted: idList.length });
  }

  const { error } = await supabase.from("knowledge_cards").delete().eq("id", id);
  if (error) return NextResponse.json({ error: error.message }, { status: 500 });
  return NextResponse.json({ deleted: 1 });
}

export async function PATCH(req: NextRequest) {
  const supabase = await createClient();
  const { searchParams } = new URL(req.url);
  const id = searchParams.get("id");

  if (!id) return NextResponse.json({ error: "id required" }, { status: 400 });

  const body = await req.json();
  const { error } = await supabase.from("knowledge_cards").update(body).eq("id", id);
  if (error) return NextResponse.json({ error: error.message }, { status: 500 });
  return NextResponse.json({ updated: 1 });
}
```

**Key details:**
- Each HTTP verb is a separate exported function (`GET`, `POST`, `PUT`, `PATCH`, `DELETE`)
- Query params from `searchParams` for DELETE ID targeting
- Request body from `req.json()` for PATCH update payload
- Batch delete via comma-separated `?ids=id1,id2,id3`
- RLS policy must allow the operation (or use service_role key)

### Updating existing pages

When adding features visible on existing pages (homepage, post detail, etc.), modify the server page first to fetch additional data, then update the client component:

1. **Server page** — add new `.from("new_table").select(...)` queries
2. **Pass new data** as props to the client component
3. **Client component** — add new props to the interface, display new data
4. **Build** — verify no errors

### Creating new routes within a section

For section-specific pages (e.g., `/thescam/tags`, `/thescam/faces`):

```
app/thescam/
├── page.tsx              # Hub page (server component)
├── thescam-hub-client.tsx # Hub client component
├── tags/
│   ├── page.tsx           # All tags (server)
│   ├── tags-browser-client.tsx
│   └── [slug]/
│       ├── page.tsx       # Posts by tag (server)
│       └── tag-detail-client.tsx
├── faces/
│   ├── page.tsx           # Face gallery (server)
│   └── faces-gallery-client.tsx
├── tracuu/
│   ├── page.tsx           # Search page (server)
│   └── tracuu-client.tsx
├── bao-cao/
    ├── page.tsx           # Report form (server)
    └── bao-cao-client.tsx
```

### Multi-tab page pattern (Overview + Detail)

For content-driven pages that need **two viewing modes** (e.g., an overview gallery and a detailed academic feed), use this pattern:

**Structure:**
```
app/
├── page.tsx              # Server page: fetches data, delegates to wrapper
├── feed-page-client.tsx   # Client wrapper: tab state + conditional render
├── feed-client.tsx        # Tab A: detailed view (current feed)
└── overview-client.tsx    # Tab B: visual overview (A-Z gallery)
```

**Wrapper component (tab bar + switching):**
```tsx
"use client";

import { useState } from "react";
import FeedClient from "./feed-client";
import OverviewClient from "./overview-client";

type Tab = "overview" | "detail";

export default function FeedPageClient({ cards }) {
  const [tab, setTab] = useState<Tab>("overview");

  return (
    <div>
      <div className="flex gap-1 mb-6 border-b border-[var(--color-border)] pb-3">
        <button
          onClick={() => setTab("overview")}
          className={`px-5 py-2 rounded-full text-sm font-medium transition-all ${
            tab === "overview"
              ? "bg-[var(--color-accent)] text-black"
              : "text-[var(--color-text-secondary)] hover:text-white"
          }`}
        >
          📚 Overview A-Z
        </button>
        <button
          onClick={() => setTab("detail")}
          className={`px-5 py-2 rounded-full text-sm font-medium transition-all ${
            tab === "detail"
              ? "bg-[var(--color-accent)] text-black"
              : "text-[var(--color-text-secondary)] hover:text-white"
          }`}
        >
          🎓 Học thuật
        </button>
      </div>

      {tab === "overview" ? <OverviewClient cards={cards} /> : <FeedClient cards={cards} />}
    </div>
  );
}
```

**Server page** (keeps fetching simple, passes everything to wrapper):
```tsx
// app/page.tsx
import { createClient } from "@/lib/supabase/server";
import FeedPageClient from "./feed-page-client";

export const dynamic = "force-dynamic";

export default async function FeedPage() {
  const supabase = await createClient();
  const { data: cards } = await supabase
    .from("knowledge_cards")
    .select("*, topics:knowledge_topics(*)")
    .order("created_at", { ascending: false });

  return <FeedPageClient cards={cards || []} />;
}
```

**Overview A-Z pattern** (grouping content by keywords/tags into visual sections):

```tsx
// Define categories with keywords for auto-classification
const CATEGORIES = [
  { name: "Immunology", emoji: "🛡️", keywords: ["prrsv", "cytokine", "nf-kb", "tlr"] },
  { name: "Molecular Biology", emoji: "🧬", keywords: ["autophagy", "apoptosis", "signaling"] },
  // ...
];

function categorizeCard(card: Card): string {
  const text = `${card.title} ${card.tags?.join(" ") || ""}`.toLowerCase();
  for (const cat of CATEGORIES) {
    for (const kw of cat.keywords) {
      if (text.includes(kw)) return cat.name;
    }
  }
  return "General";
}
```

**Key details:**
- Server page does one Supabase query, passes as prop — no `"use client"` in server page
- Tab state is local `useState` — simple, no routing needed
- Each tab component receives identical props but renders differently
- The overview tab groups cards by keyword matching into sections with KPIs + gloss-cards
- No extra DB queries — all grouping is client-side

## 5. Build Verification

```bash
cd ~/<project> && pnpm build
```

Expected output:
```
✓ Compiled successfully in X.Xs
✓ Generating static pages using N workers (M/M) in Xms
```

All routes should compile. Verify the route list shows both existing and new routes.

### 🛑 HARD RULE: Build THEN deliver

The user's explicit rule: **"Build trước, test xong mới hoàn thành."** Never declare a task done or say "xong rồi" until you have:

1. Run `npx next build` and verified **0 errors** (both compilation AND TypeScript)
2. **Restarted the dev server** and verified the page loads without console errors (no hydration mismatch, no runtime ReferenceError)
3. If the change added/showed new UI, **interacted with it in the browser** to confirm it renders correctly
4. Checked the browser console for any JS errors — even non-fatal ones (hydration warnings, import errors) count as failures

**Do NOT skip** — the build catches real TypeScript errors that the dev server tolerates (like `Property 'error' does not exist on type` or `useRouter is not defined`). A dev server showing "Compiled successfully" can still have TS errors that only surface in `next build`.

**Common post-build restart mistakes:**
- Forgetting to kill old PID on the port → `EADDRINUSE` → fail to start → timeout
- Forgetting the HMR tunnel config (if using tunnel domain) → hydration errors
- Loaded page from before restart still showing old code → need hard refresh (F5)

## 6. Deployment

### Content-driven card overview (auto-parsed from markdown)

For content cards that need **two viewing modes** at the *card level* (not the page level), use this pattern:

**Concept:** Parse the card's markdown content on the client-side to extract sections, key terms, and concepts, then render a visual overview (A-Z style) alongside the full academic content.

**Key parser outputs:**
- `essence` — first "Mô tả bản chất:" paragraph or first 200 chars
- `concepts` — `**term** — definition` patterns from bold markers
- `sections` — `## Heading` sections with their body text
- `terms` — bold phrases + tags, deduplicated
- `tldr` — summary or lines starting with "Tóm" / "Kết luận"

**Card detail client with 2 tabs (`card/[id]/card-detail-client.tsx`):**

```typescript
"use client";
import { useState, useEffect, useMemo } from "react";

type Tab = "overview" | "hoc-thuat";

export default function CardDetailClient({ card, error }: { card: Card | null; error: string | null }) {
  const [tab, setTab] = useState<Tab>("overview");
  const overview = useMemo(() => parseOverview(card), [card]);

  return (
    <div>
      {/* Tab bar */}
      <div className="flex gap-1 mb-5 border-b border-[var(--color-border)] pb-2">
        <button onClick={() => setTab("overview")}
          className={`px-4 py-1.5 rounded-full text-xs font-medium ${
            tab === "overview" ? "bg-[var(--color-accent)] text-black" : "text-[var(--color-text-secondary)]"
          }`}>📚 Overview</button>
        <button onClick={() => setTab("hoc-thuat")}
          className={`px-4 py-1.5 rounded-full text-xs font-medium ${
            tab === "hoc-thuat" ? "bg-[var(--color-accent)] text-black" : "text-[var(--color-text-secondary)]"
          }`}>🎓 Học thuật</button>
      </div>

      {tab === "overview" && overview && <OverviewContent overview={overview} card={card} />}
      {tab === "hoc-thuat" && <AcademicContent card={card} />}
    </div>
  );
}
```

**Parser implementation — place inside same file or import from utils:**

```typescript
function parseOverview(card: Card | null) {
  if (!card) return null;
  const content = card.content || "";
  const summary = card.summary || "";
  const tags = card.tags || [];

  const essence = (content.match(/\*\*Mô tả bản chất:\*\*\s*([^.]+\.)/)?.[1]
    || content.match(/Mô tả bản chất:\s*([^.]+\.)/)?.[1]
    || summary || content.slice(0, 200) + "…");

  const concepts: { term: string; def: string }[] = [];
  const boldPattern = /\*\*(.*?)\*\*\s*[—–\-:]\s*(.*?)(?:\.|$)/g;
  let m;
  while ((m = boldPattern.exec(content)) !== null) {
    if (m[1].trim() && m[2].trim() && m[2].length < 120 && concepts.length < 10)
      concepts.push({ term: m[1].trim(), def: m[2].trim() });
  }

  const sections: { title: string; body: string }[] = [];
  const sectionRegex = /##\s+(.+?)\n([\s\S]*?)(?=\n##\s|\n---|$)/g;
  while ((m = sectionRegex.exec(content)) !== null) {
    let title = m[1].replace(/\*+/g, "").trim();
    let body = m[2].trim().replace(/\|.*\|.*\n/g, "").replace(/\*+/g, "").slice(0, 300);
    if (title && body) sections.push({ title, body: body + (body.length >= 300 ? "…" : "") });
  }

  const termSet = new Set(tags);
  const termPattern = /\*\*(.{2,40}?)\*\*/g;
  while ((m = termPattern.exec(content)) !== null) {
    const t = m[1].trim();
    if (t.length > 2 && t.length < 40 && !t.includes("Mô tả") && termSet.size < 15) termSet.add(t);
  }

  const tldrLines = content.split("\n").filter(l => /^(Tóm|Kết luận|TL;DR)/.test(l.trim()));
  const tldr = tldrLines.length > 0
    ? tldrLines[0].replace(/^#{1,3}\s*/, "").replace(/\*+/g, "") : summary;

  return {
    essence, concepts: concepts.slice(0, 8), sections: sections.slice(0, 6),
    terms: [...termSet].slice(0, 15), tldr
  };
}
```

**Key design decisions:**
- Parse happens **client-side** via `useMemo` — no server round-trip
- Overview is **auto-generated** from existing markdown — no separate content needed
- Empty sections simply omitted — handles sparse data gracefully
- Each tab shares the same `card` prop — no extra API calls
- Separate `renderMarkdown()` function handles the academic tab's full formatting

### 🚨 Production server recovery (ChunkLoadError fix)

**Symptom:** Browser shows `ChunkLoadError: Failed to load chunk /_next/static/chunks/<hash>.js`. The site partially loads (HTML shell) but JS features break.

**Root cause:** The production server is running an old build. A `next build` was run (or the `.next/` cache regenerated) without restarting `next start`. The new build generates different chunk hashes, but the running server still serves the old HTML that references stale chunks. The browser fetches the new HTML (from a fresh page load), which references chunk names from the new build that don't exist because the old server process is still running.

**Fix — full recovery cycle:**

```bash
# Step 1: Rebuild production
cd ~/<project> && npx next build

# Step 2: Find the old node process — runs as Windows-native node.exe
cmd.exe /c "netstat -ano | findstr :<PORT>"
# The LISTENING line's last column is the PID. This is a Windows-native
# node.exe, NOT a bash child — git-bash `kill -9` silently fails on it.

# Step 3: Kill old process — MUST use taskkill, kill -9 won't work
cmd.exe /c "taskkill /F /PID <PID>"

# Step 4: Verify port is freed
curl -s --max-time 2 http://localhost:<PORT>/ -o /dev/null -w "%{http_code}"
# Expected: curl: (7) Failed to connect or 000 — port freed

# Step 5: Export env vars (next start does NOT read .env.local) + restart
cd ~/<project>
export NEXT_PUBLIC_SUPABASE_URL="https://<project>.supabase.co"
export NEXT_PUBLIC_SUPABASE_ANON_KEY="<key>"
npx next start -p <PORT>

# Step 6: Verify through tunnel
curl -s --max-time 10 https://<domain>/ -o /dev/null -w "%{http_code}"
FIRST_CHUNK=$(curl -s https://<domain>/ | grep -oP 'chunks/[^"]+\.js' | head -1)
SIZE=$(curl -s --max-time 5 "https://<domain>/_next/static/$FIRST_CHUNK" | wc -c)
echo "Chunk: $SIZE bytes"
# Expected: both 200, chunk > 0 bytes
```

**Why `kill -9` fails on Windows node.exe:** The PID from `netstat` is a Windows-native process. Git-bash's `kill -9` sends SIGKILL which MSYS2 translates to `TerminateProcess()`, but this only works for processes in the same MSYS2 process tree. A `node.exe` started independently (from another session, Task Scheduler, or `npx` directly) is outside that tree — `kill -9` reports success but the process stays alive. **Always use `cmd.exe /c "taskkill /F /PID <PID>"` for Windows-native node processes.**

### Verify the full stack works after restart

After any server restart or tunnel recovery, verify all layers independently:

```bash
# Layer 1: App server (local)
curl -s -o /dev/null -w "Layer 1 (app): %{http_code}\n" http://localhost:<PORT>/

# Layer 2: JS chunks load properly
FIRST_CHUNK=$(curl -s https://<domain>/ | grep -oP 'chunks/[^"]+\.js' | head -1)
SIZE=$(curl -s "https://<domain>/_next/static/$FIRST_CHUNK" | wc -c)
echo "Layer 2 (chunks): $SIZE bytes"

# Layer 3: API endpoints work (if applicable)
curl -s -o /dev/null -w "Layer 3 (API): %{http_code}\n" https://<domain>/api/health

# Layer 4: Tunnel connectivity
curl -s -o /dev/null -w "Layer 4 (tunnel): %{http_code}\n" --max-time 10 https://<domain>/
```

All four layers should return 200. If Layer 1 fails → server is down. If Layer 1 works but Layer 4 fails → tunnel is down. If Layers 1-3 work but Layer 2 shows 0 bytes → ChunkLoadError risk (old chunks referenced by new build).

### Start production server

```bash
# Port 3000 may be taken (e.g., by First Only). Check first:
netstat -ano | grep ":3000 " | grep LISTENING

# Use a different port if needed:
cd ~/<project>
PORT=3001 npx next start -p 3001
# Next.js does NOT support pnpm start -- --port X syntax
```

### Tunnel for preview (dev)

Use localtunnel for quick preview:
```bash
lt --port <PORT> --subdomain <unique-name>
# URL: https://<unique-name>.loca.lt
```

### Design preview before full build (HTML mockup first)

Before writing Next.js code, create a **static HTML preview** for mobile review. This enforces CRITIQUE BEFORE CODE at the UI level:

1. Write `preview/index.html` with all views as tab sections (``display:none`` + JS toggle)
2. Serve: ``cd preview && python -m http.server <PORT>``
3. Expose: ``npx.cmd localtunnel --port <PORT> --subdomain <name>``
4. User reviews on phone → gives feedback → only THEN build Next.js project

### Reuse existing Supabase project unless isolation required

For new features sharing data with an existing app, prefer adding tables to an **existing Supabase project** (e.g., theliems') rather than creating a new one. Benefits:
- No extra infra to manage (passwords, auth, billing)
- Single source of DB credentials
- Future cross-feature queries possible

Use distinct table names (``knowledge_topics``, ``knowledge_cards``, etc.) to avoid collisions. Only create a new project when strict data isolation is needed (multi-tenant, different environment).

### Tunnel for production (Cloudflare named tunnel)

```bash
# Pre-requisite: Cloudflare account with domain, cloudflared authenticated
cloudflared tunnel create <tunnel-name>
# Edit config at ~/.cloudflared/<name>-config.yml with native Windows paths
cloudflared tunnel route dns <tunnel-name> <domain.com>
# If DNS record already exists: error 1003. Delete existing records in CF Dashboard → DNS first.
cloudflared tunnel --config "C:\Users\<user>\.cloudflared\<name>-config.yml" run
```

## Pitfalls

### pg_trgm extension must be installed before GIN trgm indexes
**Error:** `operator class "gin_trgm_ops" does not exist for access method "gin"`
**Fix:** Create extension in a SEPARATE step before running the migration that creates trgm indexes.

### Next.js --port doesn't work with pnpm
**Wrong:** `pnpm start -- --port 3001` → "Invalid project directory provided"
**Correct:** `PORT=3001 npx next start -p 3001`

### `next start` doesn't load .env.local — export vars manually
**Symptom:** Production server (`next start`) returns 404 for dynamic routes that depend on Supabase data, even though `next dev` works fine and data exists in the DB.

**Root cause:** `next start` (production mode) does NOT read `.env.local`. Only `next dev` does. The Supabase client gets empty `NEXT_PUBLIC_SUPABASE_URL`/`NEXT_PUBLIC_SUPABASE_ANON_KEY` vars at runtime.

**Fix:** Export the environment variables before starting the production server:
```bash
cd ~/<project>
export NEXT_PUBLIC_SUPABASE_URL="https://<project>.supabase.co"
export NEXT_PUBLIC_SUPABASE_ANON_KEY="<key>"
npx next start -p <PORT>
```

Alternatively, rename `.env.local` to `.env.production` or `.env` (Next.js reads those in production too), but explicit export is more reliable during active development.

### Supabase nested select fails: "Could not find a relationship between 'posts' and 'profiles'"
**Symptom:** A query like `.from("posts").select("*, profiles(display_name)")` returns an error: `"Searched for a foreign key relationship between 'posts' and 'profiles' in the schema 'public', but no matches were found."` This causes the page to show a 404 (the `notFound()` call triggered by the supabase error).

**Root cause:** PostgREST (Supabase's REST API) resolves nested selects through foreign key constraints between the two tables. `posts.author_id → auth.users.id` and `profiles.id → auth.users.id` are both FKs to `auth.users`, but there's no direct FK between `posts` and `profiles`. PostgREST can't infer the relationship through the shared `auth.users` reference.

**Fix — add a direct FK from posts to profiles:**
```sql
ALTER TABLE public.posts 
  ADD CONSTRAINT posts_author_id_profiles_fkey 
  FOREIGN KEY (author_id) REFERENCES public.profiles(id) ON DELETE SET NULL;
```

Then reload the PostgREST schema cache (this tells Supabase to rebuild its foreign key relationship map):
```sql
NOTIFY pgrst, 'reload schema';
```

After that, the nested select works immediately — no need to restart any service.

**Alternative** (less invasive): Instead of a nested FK join, fetch posts and profiles separately in the server component, then merge them in code. This avoids the FK relationship requirement but requires more code.

### Vietnamese font support: Google Fonts that actually support Vietnamese
**Symptom:** Site uses a Google Font and Vietnamese characters (á, à, ả, ã, ạ, ê, ô, ơ, ư, ậ) display as boxes or missing glyphs. This applies even when `subsets: ['vietnamese']` is set.

**Root cause:** Many Google Fonts are listed with "vietnamese" subset support but their actual font files lack Vietnamese diacritic glyphs. Fonts like **Press Start 2P**, **VT323**, **Space Mono** are effectively Latin-only regardless of subset configuration. Even fonts that DO support Vietnamese (IBM Plex Mono, JetBrains Mono) may fail when loaded through `next/font/google` because the self-hosted font generation only downloads a subset.

**The most reliable approach — Google Fonts CDN `<link>` tag:**

Instead of `next/font/google`, load the font directly via Google Fonts CDN in the HTML `<head>`:

```tsx
// layout.tsx — remove next/font/google import, use CDN link instead
export default function RootLayout({ children }) {
  return (
    <html lang="vi">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link 
          href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&display=swap&subset=vietnamese,latin" 
          rel="stylesheet" 
        />
      </head>
      <body style={{ fontFamily: "'Space Grotesk', 'Noto Sans', 'Segoe UI', system-ui, sans-serif" }}>
        {children}
      </body>
    </html>
  )
}
```

**Key details:**
- Use `&subset=vietnamese,latin` (comma-separated, single parameter) in the Google Fonts URL
- Add `font-display=swap` for performance (already default in CDN mode)
- Set `<html lang="vi">` so browsers apply Vietnamese-specific typography rules
- Fallback chain should include `'Noto Sans'` as second choice — it's Google's universal font

**If using `next/font/google` (less reliable but works for some fonts):**

Only use fonts confirmed to have complete Vietnamese glyph coverage:
- **Space Grotesk** (sans-serif, modern) — ✅ confirmed working
- **JetBrains Mono** (monospace) — ✅ confirmed working
- **IBM Plex Mono** (monospace) — ✅ confirmed working
- **Noto Sans Mono** (monospace) — should work (Noto project)
- **Fira Code / Fira Mono** — should work

```typescript
import { Space_Grotesk } from 'next/font/google'
const spaceGrotesk = Space_Grotesk({ 
  weight: ['400', '500', '700'],
  subsets: ['latin', 'vietnamese'],
  variable: '--font-main'
})
```

**Test Vietnamese rendering:** Load a page with Vietnamese text and visually check:
- Characters like ư, ơ, ậ, ỗ, ỡ — do they show or are they boxes?
- If ANY Vietnamese character is missing, switch to CDN `<link>` approach immediately
- Do NOT trust Google Fonts' "vietnamese" subset tag alone — always verify visually on at least 3 Vietnamese-heavy pages

**Quick check command:**
```bash
# Fetch homepage and grep for Vietnamese character rendering in the HTML
curl -s http://localhost:3001/ | grep -oP '[àáảãạăằắẳẵặâầấẩẫậđèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵ]+' | head -10
# If this returns Vietnamese text, the HTML is correct — font is the issue
```

### Cloudflare named tunnel config needs native Windows paths
**Error:** `open /c/Users/...: The system cannot find the path specified`
**Fix:** Use `C:\\Users\\<user>\\.cloudflared\\config.yml` (backslashes in quotes)

### Anon key format
The Supabase anon key may include a `sb_publishable__` prefix. This works with both `apikey` and `Authorization: Bearer` headers. Test with:
```bash
curl -s -H "apikey: <key>" "https://<project>.supabase.co/rest/v1/..."
```

### Cloudflare quick tunnel returns 404 when an authenticated config exists

**Symptom:** `cloudflared tunnel --url http://localhost:<PORT>` succeeds at creating a quick tunnel URL but all requests return 404, even though the local server responds 200.

**Root cause:** cloudflared auto-loads `~/.cloudflared/config.yml` (or a similar credentials file) when it finds one. If that config has a catch-all ingress rule returning `http_status:404`, the quick tunnel is routed through that rule instead of the local origin.

**Fix — pass empty config to disable auto-loading:**
```bash
cloudflared tunnel --url http://localhost:<PORT> --protocol http2 --config ""
```
The `--config ""` flag tells cloudflared to not read any config file, forcing it to use the quick tunnel's default origin routing. Use `--protocol http2` to avoid QUIC protocol issues (Windows-specific).

**Check if a config is interfering:**
```bash
# If you see "Using existing config at ~/.cloudflared/config.yml" in logs,
# or the Settings map shows a cred-file path, config is being loaded.
# Add --config "" to disable it.
```

### Next.js dev server HMR blocked on tunnel domain — page keeps refreshing

**Symptom:** Accessing the Next.js dev server (`next dev`) through a Cloudflare/localtunnel domain (e.g., `kflow.thefirstonly.com`) causes the page to refresh every few seconds. The console shows `[HMR] connected` then disconnects repeatedly. The server log shows:

```
⚠ Blocked cross-origin request to Next.js dev resource /_next/webpack-hmr from "tunnel-domain.com".
Cross-origin access to Next.js dev resources is blocked by default for safety.
```

**Root cause:** Next.js 15+ blocks HMR (Hot Module Replacement) WebSocket connections from cross-origin domains by default. The tunnel domain is different from `localhost`, so the HMR WebSocket is rejected and the page enters a reload loop — it keeps trying to reconnect HMR, fails, then reloads the page to re-establish the connection.

**Fix — add `allowedDevOrigins` to `next.config.ts`:**

```typescript
// next.config.ts
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  allowedDevOrigins: [
    "kflow.thefirstonly.com",   // your tunnel domain
    "localhost",
    "127.0.0.1",
    // Add any other tunnel/preview domains here
  ],
};

export default nextConfig;
```

**IMPORTANT:** After changing `next.config.ts`, you MUST **restart the dev server** (`Ctrl+C` then re-run `next dev`). Next.js does NOT auto-reload config changes via HMR.

### Turbopack "Jest worker" crash — Next.js 16.2.10 on Windows

**Symptom:** Browser shows full-screen error overlay: `"Error: Jest worker encountered 2 child process exceptions, exceeding retry limit"`. Server log shows:
```
⨯ Failed to generate static paths for /card/[id]:
⨯ Error: Jest worker encountered 2 child process exceptions, exceeding retry limit
```
Followed by `write EPIPE` cascade. Server becomes unresponsive.

**Root cause:** Turbopack bug in Next.js 16.2.10 on Windows. Chain:
1. A client component throws a **hydration error** (old server HTML vs new client code after HMR)
2. The Next.js error overlay tries to **compile the card detail page** (dynamic route `[id]` without `generateStaticParams`)
3. Turbopack's internal worker crashes processing the dynamic route → `Jest worker` error
4. Cascade kills HMR WebSocket and the server

**Fix — three things together:**

**1. Add `export const dynamic = "force-dynamic"` to dynamic route pages:**
```typescript
// app/card/[id]/page.tsx
export const dynamic = "force-dynamic";
```
This prevents Turbopack from attempting static generation on dynamic routes.

**2. Clear `.next` cache and restart:**
```bash
rm -rf /c/Users/<user>/<project>/.next
npx next dev --port <PORT>
```

**3. Kill lingering processes on the port:**
```bash
netstat -ano | grep ":<PORT> " | grep LISTENING
taskkill /F /PID <pid>
```

**Prevention:** Add `dynamic = "force-dynamic"` to every route using Supabase data at request time. After editing `"use client"` components, do a hard refresh (F5) to force server recompile. If the error appears, full `.next` clean + restart is the only reliable fix.

### Navigation elements must work without JS — use `<a>` not `onClick + router.push()`
**Symptom:** Tabs, cards, and back buttons using `<button onClick={() => router.push(path)}>` render visually but do NOT respond to taps/clicks when accessed through a localtunnel/Cloudflare tunnel on mobile, or on slow connections where the Next.js client JS bundle hasn't finished loading/hydrating.

**Root cause:** `<button onClick={...}>` is inert until React hydrates the client component. If the JS bundle is delayed (tunnel latency, ad blocker, partial load), the element sits there unresponsive — the user sees it but can't tap.

**Fix — always use `<a href="...">` for navigation elements:**
```tsx
// ❌ BROKEN without JS — don't do this for navigation
<button onClick={() => router.push("/feed")}>Feed</button>

// ✅ WORKS always — native browser navigation
<a href="/feed" className="...">Feed</a>
```

**When you still need onClick (interactive toggles, not navigation):**
Reserve `<button onClick>` for genuine interactivity that has no URL destination (bookmark toggle, like button, expand/collapse). Every element whose primary purpose is "go to another page" should be `<a>`.

**Library card pattern (data-driven navigation):**
```tsx
// Instead of:
<button onClick={() => router.push(`/feed?topic=${topic.slug}`)}>
// Use:
<a href={`/feed?topic=${topic.slug}`}>
```

This applies to: tab switchers, topic cards, result list items, breadcrumbs, logo/back links — anywhere the user expects a navigation action.

### Localtunnel lifecycle management on Windows MSYS2
**Symptom:** Tunnel process (`npx.cmd localtunnel ...`) exits silently after a few hours. The background process shows `status: exited` with no error. Users get "Bad Gateway" or connection refused.

**Root cause:** Localtunnel processes (especially `npx.cmd`) are not durable — they can die from idle timeouts, network blips, or memory pressure.

**Workflow:**
1. Always check tunnel status after a session gap: `process(action='poll', session_id=...)`
2. If exited, re-launch with a fresh subdomain (old one may be taken):
   ```bash
   npx.cmd localtunnel --port <PORT> --subdomain <fresh-name>
   ```
3. Verify the tunnel returns 200: `curl -s -o /dev/null -w "%{http_code}" https://<subdomain>.loca.lt`

**Port cleanup on Windows MSYS2:**
When a dev server or tunnel won't start because `EADDRINUSE`, use `taskkill` with forward-slash syntax (MSYS2 Bash, not cmd.exe):
```bash
# Find the PID holding the port
netstat -ano | grep ":3002 " | grep LISTENING

# Kill it — use forward slash syntax in MSYS2
taskkill /F /PID 1944
```
Note: `taskkill //F //PID` (double-slash) does NOT work in MSYS2 bash. Use single forward slash.

### Python preferred over Node.js for data-import scripts on Windows MSYS2

**Symptom:** A Node.js script using `fetch()` to POST Vietnamese text (UTF-8) to a local API repeatedly fails with `"Empty or invalid json"` for some requests while others succeed with identical structure. The same data imported via `curl` or Python `urllib.request` works every time.

**Root cause:** Node.js `fetch` on Windows MSYS2 (git-bash) can mishandle Unicode/UTF-8 in certain edge cases — particularly when JSON bodies contain Vietnamese characters (ấ, ậ, ỗ, ỡ, etc.) combined with certain content-length calculations. The response from the API is valid JSON but Node.js cannot parse it, throwing "Empty or invalid json".

**Fix — use Python instead for batch data-import workflows:**
```python
import urllib.request, json

data = json.dumps({"title": "Xử lý đất", "content": "..."}).encode('utf-8')
req = urllib.request.Request(
    'http://localhost:3003/api/knowledge', data=data,
    headers={'Content-Type': 'application/json', 'Authorization': 'Bearer secret'},
    method='POST'
)
resp = urllib.request.urlopen(req, timeout=15)
result = json.loads(resp.read())  # Always works with Python
```

Python's `urllib.request` handles encoding deterministically — the Unicode characters are serialized as `\uXXXX` escapes in the JSON (via `json.dumps().encode()`), avoiding any MSYS2 pipeline corruption.

### Supabase DB migration blocked — no direct DB password
**Symptom:** Cannot run `001_schema.sql` migration because the Supabase project's direct PostgreSQL password is unknown. The anon key works for readonly REST API queries but cannot create tables.

**Workflow:**
1. If the project was created by another tool (Supabase dashboard, Vercel integration), the DB password may not be stored locally.
2. Check common locations: `.env`, `.env.local`, `supabase/config.toml`, `~/.supabase/projects.json`.
3. If not found, the fastest path is **Supabase Dashboard SQL Editor**:
   - Open: `https://supabase.com/dashboard/project/<REF>/sql/new`
   - Paste migration SQL → Run
   - Paste seed SQL → Run
4. The app can be developed and tested with mock data while waiting for the migration.
5. **Avoid** hardcoding the password in `.env.local` — use the anon key for client operations and only use direct DB access for migrations.

### Supabase DDL from REST is DEAD — use direct pg connection when you have the password
**Symptom:** Every remote-DDL attempt through the Supabase SDK/REST fails, even with the service_role key:
- `POST /pg/query` → **404** (endpoint deprecated by Supabase ~2024; not available on newer projects)
- RPC `exec_sql(sql)` → **404 PGRST202** (function does not exist — would need to be created manually, chicken-and-egg)

**Fix — connect directly to Postgres** (works whenever `SUPABASE_PASSWORD` is in `.env`, often stored under `SUPABASE_PASSWORD` alongside `SUPABASE_URL`):

```
postgresql://postgres:<SUPABASE_PASSWORD>@db.<project-ref>.supabase.co:5432/postgres
```
- `<project-ref>` is the subdomain of `SUPABASE_URL` (e.g. `https://wggluyflkdrgffugpidk.supabase.co` → `wggluyflkdrgffugpidk`)
- Use `pg` (Node) or `psycopg2` (Python); if connection times out (IPv6/network), try the pooler host: `db.<ref>.pooler.supabase.com:5432` or `aws-0-<region>.pooler.supabase.com:6543` (transaction) / `:5432` (session)
- Verify after applying: query `pg_proc` for RPCs, `information_schema.columns` for columns — don't trust "rows: undefined" as proof; confirm the objects exist
- DDL is not transactional per-statement the way a single `CREATE OR REPLACE` is — multi-object migrations should run fine as one `client.query(sql)` batch, but check each object after

**When you DON'T have the password:** Dashboard SQL Editor remains the only path (previous pitfall).

### SSR/client hydration mismatch: `toLocaleString` / `Date` formatting

**Symptom:** The card detail page shows "This page couldn't load" after a production build. The SSR HTML renders correctly, but the page crashes on client hydration. The browser console shows empty exceptions.

**Root cause:** `Date.toLocaleString("vi-VN", {hour:"2-digit", minute:"2-digit", ...})` produces different output on the server (Node.js) vs client (browser). Node.js may use 24-hour format while the browser's ICU data uses a different format. React detects the text-content mismatch during hydration and triggers an error.

**The specific failure chain:**
1. SSR (Node.js): `toLocaleString("vi-VN", {hour:"2-digit"})` → `"10:15 27/07/2026"`
2. Client (browser): Same call → `"10:15 SA 27/07/2026"` (with AM marker)
3. React sees `<span>10:15 27/07/2026</span>` (SSR) ≠ `<span>10:15 SA 27/07/2026</span>` (client) → hydration mismatch
4. Error Boundary catches the exception, shows "This page couldn't load"

**Fix — avoid locale-dependent methods that can differ between server and client:**

For **date + time** display that MUST match between SSR and client:

```tsx
// ❌ BROKEN — different output on Node.js vs browser
{new Date(date).toLocaleString("vi-VN", {day:"2-digit",month:"2-digit",year:"numeric",hour:"2-digit",minute:"2-digit"})}

// ✅ CORRECT — consistent between server and client
{new Date(date).toLocaleDateString("vi-VN")} {new Date(date).toISOString().slice(11,16)}
```

`toLocaleDateString("vi-VN")` is stable because it only uses the date part (no timezone-dependent hour formatting). `toISOString().slice(11,16)` gives UTC time (`HH:MM`) which is identical everywhere.

**If you need LOCAL time client-side without hydration mismatch:**

```tsx
// Use a state + useEffect pattern to render time only after hydration
const [mounted, setMounted] = useState(false);
useEffect(() => { setMounted(true); }, []);

return (
  <span>
    📅 {new Date(card.created_at).toLocaleDateString("vi-VN")}
    {mounted && ` ${new Date(card.created_at).toLocaleTimeString("vi-VN", {hour:"2-digit",minute:"2-digit"})}`}
  </span>
);
```

This avoids the hydration mismatch by rendering time only on the client side.

**Also affected:** Any use of `Intl.DateTimeFormat`, `toLocaleString`, `toLocaleTimeString`, or `toTimeString()` with options that differ between Node.js and browser ICU implementations. Test each format locally before shipping.

### CSS chunk cache invalidation

**Symptom:** Dashboard pages, topic grids, KPI badges, and other styled elements render as plain text / unstyled HTML. The browser loads a CSS chunk (`/_next/static/chunks/<hash>.css`) but the CSS classes (`.kpi-badge`, `.topic-grid`, etc.) are missing from that chunk.

**Root cause:** The `globals.css` file has all the classes, but the build process (when run without a clean `.next`) may serve a **stale CSS chunk** from the previous build. This typically happens when:
- You modified `globals.css` but ran `npx next build` without deleting `.next` first
- Or a previous build's CSS chunk had the same hash but different content (from partial caching)

**Fix:**

```bash
# ALWAYS clean .next before production builds, especially after CSS changes
cd ~/<project>
rm -rf .next
npx next build
```

**Why this happens:** Next.js uses CSS chunk hashing based on content. If you modify `globals.css` but the build tool's internal cache determines the content hasn't changed (or the old chunk is still referenced), the new classes are never emitted to the chunk file. A clean `.next` forces all chunks to be regenerated from scratch.

**Verification:**

```bash
# After build, check that your CSS classes exist in the emitted chunk
CHUNK=$(ls /c/Users/<user>/<project>/.next/static/chunks/*.css | head -1)
grep -c "kpi-badge\|topic-grid\|unread-row" "$CHUNK"
# Expected: > 0 (classes found)
```

If this returns 0, the CSS wasn't compiled — run a clean build.

### Live search dropdown in TopBar

**Pattern:** Add a debounced live search to the app's top navigation bar, with results appearing in a dropdown below the input. No navigation to a separate search page.

**Component structure:**

```tsx
"use client";
import { useState, useEffect, useRef, useMemo } from "react";

// Define a Card interface with id, title, summary, tags, etc.

export default function TopBar() {
  const [query, setQuery] = useState("");
  const [cards, setCards] = useState<Card[]>([]);
  const [cardsLoading, setCardsLoading] = useState(true);
  const [focused, setFocused] = useState(false);
  const mobileRef = useRef<HTMLDivElement>(null);
  const desktopRef = useRef<HTMLDivElement>(null);
  const dropRef = useRef<HTMLDivElement>(null);

  // 1. Fetch all cards once on mount
  useEffect(() => {
    fetch("/api/cards")
      .then(r => r.json())
      .then(data => { if (Array.isArray(data)) setCards(data); })
      .catch(() => {})
      .finally(() => setCardsLoading(false));
  }, []);

  // 2. Close dropdown on outside click (mouse + touch)
  useEffect(() => {
    const handler = (e: MouseEvent | TouchEvent) => {
      const target = e.target as Node;
      const isInside =
        (mobileRef.current?.contains(target)) ||
        (desktopRef.current?.contains(target)) ||
        (dropRef.current?.contains(target));
      if (!isInside) setFocused(false);
    };
    document.addEventListener("mousedown", handler);
    document.addEventListener("touchstart", handler);
    return () => {
      document.removeEventListener("mousedown", handler);
      document.removeEventListener("touchstart", handler);
    };
  }, []);

  // 3. Filter results synchronously (instant, no debounce needed since data is client-side)
  const results = useMemo(() => {
    if (!query.trim() || cardsLoading) return [];
    const q = query.toLowerCase();
    return cards
      .filter(c => c.title.toLowerCase().includes(q) || (c.summary || "").toLowerCase().includes(q))
      .slice(0, 10);
  }, [query, cards, cardsLoading]);

  // 4. JSX for the search bar + dropdown
  return (
    <header>
      <div className="relative">
        <input
          type="text"
          placeholder="Search..."
          value={query}
          onChange={e => setQuery(e.target.value)}
          onFocus={() => setFocused(true)}
          className="bg-[var(--color-surface)] pl-9 pr-4 py-1.5 rounded-full"
        />
        {focused && query.trim() && (
          <div
            ref={dropRef}
            className="absolute top-full left-0 right-0 mt-1 bg-[var(--color-bg-dark)] border rounded-xl shadow-2xl z-50 max-h-[360px] overflow-y-auto"
          >
            {cardsLoading ? (
              <div className="px-4 py-3 text-sm text-[var(--color-text-tertiary)] flex items-center gap-2">
                <span className="animate-spin" />
                Đang tải...
              </div>
            ) : results.length === 0 ? (
              <div className="px-4 py-3 text-sm text-[var(--color-text-tertiary)]">Không tìm thấy</div>
            ) : (
              results.map(c => (
                <Link
                  key={c.id}
                  href={`/card/${c.id}`}
                  onClick={() => { setQuery(""); setFocused(false); }}
                  className="block px-4 py-3 hover:bg-[var(--color-surface)] transition-colors no-underline"
                >
                  <div className="text-sm text-white line-clamp-1">{c.title}</div>
                  <div className="text-xs text-[var(--color-text-tertiary)]">{c.summary || c.tags?.join(" · ")}</div>
                </Link>
              ))
            )}
          </div>
        )}
      </div>
    </header>
  );
}
```

**Key design decisions:**
- **Client-side filtering** — fetch all cards once, filter locally via `useMemo` (instant, no debounce needed)
- **Loading state** — show spinner while `fetch("/api/cards")` is in progress, so user knows search will work
- **Both touch + mouse** — register both `mousedown` and `touchstart` for outside-click detection on mobile
- **Dual input support** — if the TopBar has separate mobile and desktop inputs, use separate refs (`mobileRef`, `desktopRef`) so clicking either input keeps the dropdown open
- **`line-clamp-1`** — prevents long titles from breaking the dropdown layout
- **Dropdown z-index** — `z-50` ensures the dropdown appears above sticky headers and feed content

**Mobile responsiveness:**
- The dropdown is `absolute top-full` relative to the search container, so it naturally positions below the search bar
- On mobile (small screens), the search container must NOT have `overflow: hidden` or the dropdown gets clipped
- `position: relative` on the parent div is critical for the dropdown to know where to anchor

### Next.js 16 route handler params change (async params)

**Symptom:** Build fails with:
```
Type error: Type 'typeof import("...route")' does not satisfy the constraint 'RouteHandlerConfig<"...">'.
  Types of property 'GET' are incompatible.
    Type '(_req: NextRequest, { params }: { params: { id: string; }; }) => ...'
    is not assignable to type '(request: NextRequest, context: { params: Promise<{ id: string; }>; }) => ...'
      Types of parameters '__1' and 'context' are incompatible.
        Type '{ params: Promise<{ id: string; }>; }' is not assignable to type '{ params: { id: string; }; }'.
```

**Root cause:** In Next.js 16.x, route handler `params` is now wrapped in a `Promise`. The old pattern `{ params }: { params: { id: string } }` is deprecated and fails the type checker.

**Fix — destructure with `await`:**

```typescript
// ❌ BROKEN in Next.js 16 — params is not a Promise in the old signature
export async function GET(
  _req: NextRequest,
  { params }: { params: { id: string } }
) {
  const id = params.id;
}

// ✅ CORRECT — params is a Promise, await it
export async function GET(
  _req: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params;
}
```

This applies to ALL route handlers (`GET`, `POST`, `PUT`, `PATCH`, `DELETE`) and server component pages (`page.tsx`). If you see a type error about `params` incompatibility, this is the fix.

### Next.js 16 proxy/auth gate behind Cloudflare tunnel — redirects go to `localhost` (absolute URL + X-Forwarded traps)

**Symptom:** A Next.js app behind a Cloudflare tunnel (e.g. `kflow.thefirstonly.com` → `localhost:3003`) implements an auth/passcode gate in `proxy.ts`. After entering the passcode, the browser redirects to `https://localhost:3003/` instead of staying on the tunnel domain. Users hit a dead end ("về localhost").

**Root cause chain (two independent traps):**
1. `NextResponse.redirect('/')` — a relative path — throws **500** with `Error: URL is malformed "/passcode?next=...". Please use only absolute URLs`. Next requires absolute redirect targets.
2. `new URL('/', request.url)` builds the wrong host: Next.js does **NOT** trust `X-Forwarded-*` headers by default, so behind the tunnel `request.url` is `http://localhost:3003/...` regardless of the Host header the tunnel forwarded. `experimental.trustHostHeader` exists in the runtime (`next/dist/server/config-shared.js` has `trustHostHeader: ex.trustHostHeader`) but the Next 16.2.10 `ExperimentalConfig` type does **not** declare it — adding it fails type-check. Manual header building is the reliable path.

**Fix — build the base URL from proxy headers explicitly:**

```typescript
// src/proxy.ts and any route handler that redirects
function getBaseUrl(request: NextRequest): string {
  const host = request.headers.get('x-forwarded-host') || request.headers.get('host') || 'localhost'
  const proto = request.headers.get('x-forwarded-proto') || 'http'
  return `${proto}://${host}`
}

// proxy.ts — redirect to passcode keeping the real domain
return NextResponse.redirect(new URL(`/passcode?next=${encodeURIComponent(pathname)}`, getBaseUrl(request)))

// api/passcode/route.ts — after verifying, redirect back to the real domain
const res = NextResponse.redirect(new URL(next, getBaseUrl(request)))
res.cookies.set('tfo_auth', PASSCODE_HASH, { path: '/', httpOnly: true, sameSite: 'lax', maxAge: 60*60*24*30 })
```

**Verification:** test through the **real tunnel domain**, not `curl -H "Host: ..."` against localhost. Check the `location:` header of the POST response:
- ✅ `location: https://kflow.thefirstonly.com/` — correct
- ❌ `location: https://localhost:3003/` — X-Forwarded base missing

**Passcode-gate pattern (Python `http.server` equivalent):** for a plain Python dashboard behind a tunnel, a relative `Location: /` redirect is fine — browsers resolve it against the URL in the address bar (the tunnel domain). The localhost trap only bites when the server itself builds an absolute URL. Server-side gate: check cookie (`tfo_auth=sha256(passcode)`) in `do_GET` before serving; `do_POST /_auth` verifies, sets `Set-Cookie: tfo_auth=<sha256>; Path=/; HttpOnly; SameSite=Lax; Max-Age=2592000`, and 302s to `/`. Store `sha256(passcode)` in code, never the plaintext.

### Next.js 16: middleware rewrite loses search params — host-based routing alternatives

**Symptom:** You write `middleware.ts` to route `preview.domain.com/card/:id` → `/api/preview?id=:id`, using `NextResponse.rewrite(url)` with search params set via `url.searchParams.set(...)` or `new URL('/api/preview?id=...', req.url)`. The target route handler receives the request but its `searchParams.get("id")` returns `null` → API responds "Missing id". The rewrite fires (you can confirm the route changed) but query params are NOT carried to the target handler.

**Also in Next.js 16.x:** the `middleware` file convention is deprecated — Next logs `⚠ The "middleware" file convention is deprecated. Please use "proxy" instead.` (Next 16 renamed the convention; a `proxy.ts` file is the new home for this logic).

**Second pitfall — page components cannot return a `Response`:** If you try to serve a clean HTML page directly from a `page.tsx` server component (host check → `return new Response(html)`), the build fails with:
```
Type 'Promise<Response | Element>' is not assignable to type 'ReactNode | Promise<ReactNode>'
```
Page components must return ReactNode. Raw `Response` is only valid from **route handlers** (`app/api/*/route.ts`) or `middleware`/`proxy`.

**Third pitfall — `headers().get("host")` is unreliable for host-based branching:** In a server component, `const hdrs = await headers(); hdrs.get("host")` does NOT reliably reflect a custom incoming Host header (curl `-H "Host: ..."`, or tunnel origin rewriting). You may get the server's own host instead, so host-conditional logic in `page.tsx` silently falls through to the wrong branch.

**Reliable patterns for host-based routing (serving different content per subdomain on the same server):**

1. **Dedicated API route + explicit share URL** (simplest, proven): keep the clean HTML in `app/api/preview/route.ts` and have the share button copy `https://preview.domain.com/api/preview?id=<id>` directly — no middleware, no host detection. Verify with `curl "http://localhost:3003/api/preview?id=<id>"`.
2. **`redirect()` from `next/navigation`** in the page component (type-safe — throws NEXT_REDIRECT instead of returning Response): works only if the Host header is reliably available in your deployment (tunnel origin preserves it); test with the real tunnel domain, not curl `-H`.
3. **Middleware/proxy rewrite** — avoid search-param passing through rewrite; if you must, pass the id as a request header (`x-preview-id`) or path segment (`/api/preview/<id>` route) instead of query params.

**Verification discipline:** always test the preview URL **through the real tunnel domain**, not with curl `-H "Host: ..."` against localhost — the Host header handling differs, and a localhost test that "works" can still fail in production (or vice versa).

### Share button + clean OG link preview (no platform branding)

When the user wants to share a content card to messaging apps (Zalo/Messenger/Telegram) but the preview must NOT reveal the hosting platform (no "Knowledge Flow" branding), use this two-part pattern:

**1. Share button (client component):** copy link, then try native share sheet on mobile, fall back to a desktop toast:

```tsx
const handleShare = async () => {
  if (!card) return;
  const url = `https://preview.yourdomain.com/card/${card.id}`; // clean preview URL
  try { await navigator.clipboard.writeText(url); } catch {}
  if (navigator.share) {
    try { await navigator.share({ title: card.title, url }); } catch {} // user cancel
  } else {
    // desktop: mutate button text as toast feedback
    const btn = document.activeElement as HTMLElement;
    if (btn) {
      const orig = btn.textContent;
      btn.textContent = "✅ Đã copy link";
      setTimeout(() => { btn.textContent = orig; }, 2000);
    }
  }
};
```

Place the button where the user is WHILE reading (next to the date line, top of the card) — not only in a bottom action bar. Users share content when they find it interesting mid-read.

**2. Clean preview page (route handler serving raw HTML):** `app/api/preview/route.ts` fetches the card from Supabase REST (`${SUPABASE_URL}/rest/v1/knowledge_cards?id=eq.${id}&select=*` with `apikey` + `Authorization: Bearer` headers, `cache: "no-store"`), then returns a `NextResponse(html)` with:

```html
<meta property="og:title" content="...">
<meta property="og:description" content="...">
<meta property="og:type" content="article">
<meta property="og:url" content="...">
<meta property="og:site_name" content="Chia sẻ kiến thức">  <!-- neutral, no platform name -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="...">
<meta name="twitter:description" content="...">
<meta http-equiv="refresh" content="0;url=<real page URL>">  <!-- old clients that ignore OG -->
```

Plus a minimal styled landing card (title + description + "Đọc bài viết" button) for humans who open the link directly. Escape all interpolated strings (`& < > " '`). `og:site_name` is the key lever for hiding platform identity — messaging apps render it as the preview's site name.

### Custom `renderMarkdown()` copied across client components — patch EVERY copy, verify in the browser

**Class of bug:** instead of using `react-markdown`/`remark`, the app hand-rolls a regex `renderMarkdown(md)`. That function gets **copy-pasted into every client component that renders content** (feed preview, book reader, detail page, dead tab component). Consequences: (a) fixing one copy makes the symptom vanish on ONE surface while the others stay broken, (b) the copies silently diverge, so a pitfall fixed in copy A was never applied to B/C/D.

**Mandatory first step — enumerate, don't guess:**
```bash
grep -rn "function renderMarkdown" src/
```
> Real case (2026-10-18): 4 copies. Two of them (`book-client.tsx`, `feed/feed-client.tsx`) were missing the table parser **and** the HTML-escape step entirely — the same bug had been fixed in the other two months earlier. Recommendation to make: extract to `src/lib/markdown.ts` (single source), delete orphaned components.

**Bug 1 — content containing raw HTML destroys the DOM. Fix = escape FIRST.**
```js
let h = md
  .replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;")   // ← must be the first replace
  .replace(/```(\w*)\n([\s\S]*?)```/g, (_, _l, c) => `<pre><code>${c.trim()}</code></pre>`)
  .replace(/`([^`]+)`/g, "<code>$1</code>")
  .replace(/^&gt;\s*(.*)$/gm, "<blockquote>$1</blockquote>")          // ← note &gt; after escaping
```
Symptom when missing: one card whose `content` is a whole `<!DOCTYPE html>…<style>…` document swallows the remainder of the page — only 1 card renders, every item shows "unread" (hydration never runs). Because only SOME copies had the escape, the breakage was surface-specific (feed OK, `/book` broken) — **test every surface, not just one**.

**Bug 2 — table separator row leaks into the output as data.** Filter it with a regex that survives multi-column tables:
- ❌ `^\|[-:\s]+\|$` — does **not** match `|---|---|---|` because `|` is inside the middle and is not in the char class `[-:\s]` → the separator row is emitted as `<td>---</td>` (observed: 10 such cells in a 5-table card).
- ✅ `^\|[-:\s]+(\|[-:\s]+)*\|$`

Tables also need a **block scan** (collect the whole table first), not per-line `|` splitting:
```js
h = h.replace(/((?:^\|.+\|\n?)+)/gm, (block: string) => {
  const rows = block.trim().split("\n")
    .filter((l: string) => l.trim() && !/^\|[-:\s]+(\|[-:\s]+)*\|$/.test(l.trim()));
  if (rows.length === 0) return "";
  return '<div class="table-wrap"><table>' + rows.map((row, i) => {
    const cols = row.split("|").filter(Boolean).map(c => c.trim());
    const tag = i === 0 ? "th" : "td";
    return `<tr>${cols.map(c => `<${tag}>${c}</${tag}>`).join("")}</tr>`;
  }).join("") + "</table></div>";
});
h = h.replace(/<\/table>\n<table>/g, "");
```
Place this after the `<li>`→`<ul>` block and before the `\n\n`→`</p><p>` conversion.

**Bug 3 — markdown links render as literal `[label](https://…)`.** A regex renderer has no link step; add both forms explicitly:
```js
h = h.replace(/\[([^\]]+)\]\((https?:\/\/[^\s)]+)\)/g, "<a href='$2' target='_blank' rel='noopener'>$1</a>");
h = h.replace(/(^|[\s(])(https?:\/\/[^\s<>'")]+)/gm, "$1<a href='$2' target='_blank' rel='noopener'>$2</a>");
```
Order matters: put these AFTER escaping (so `&`→`&amp;` in query strings stays valid inside `href`) and AFTER inline-code (so URLs inside `<code>` are skipped — their prefix is `>`, which the bare-URL regex does not accept). The bare-URL regex requires start-of-line/space/`(` before the URL, so it cannot re-wrap an `href='…'` just emitted.

**Bug 4 — dead route masquerading as a broken surface.** A client component in a folder with no `page.tsx` is never routed (e.g. `src/app/feed/` had only `feed-client.tsx` → `/feed` = 404). `next build` prints the route list — diff it against the directories under `src/app/`; a client-only folder is either imported by another page or dead code. Don't waste time "fixing" a 404 surface that has no route.

**Verification — all four steps, curl alone is NOT enough (the renderer runs client-side):**
1. `grep -rn "function renderMarkdown" src/` → patch every copy.
2. `npm run build` → exit 0 (also confirms no TS breakage).
3. `npx eslint <changed files> -f json` → assert **no lint message lands on the lines you inserted**; pre-existing errors elsewhere in the same file are expected — report the counts, do not "fix" unrelated lint in the same pass.
4. Browser assertions on EVERY surface that renders content (`/`, `/book`, `/card/<id>` tabs):
```js
const mc = document.querySelector('.markdown-content') || document.body;
({
  tables:    mc.querySelectorAll('table').length,                                                       // > 0
  dashCells: [...mc.querySelectorAll('td,th')].filter(c => /^[-|\s]+$/.test(c.textContent.trim())).length, // must be 0
  links:     mc.querySelectorAll('a').length,                                                           // > 0
  rawMdLink: /\]\(https?:/.test(mc.innerText),                                                          // false
  rawPipe:   /\|---/.test(mc.innerText),                                                                // false
})
```
Then **restart the production server** and hard-refresh — a rebuild without restart keeps serving the old bundle, which reads exactly like "my fix didn't work".

**CSS that must exist in `globals.css`** for the emitted HTML: `.markdown-content table` (with `display:block; overflow-x:auto` for mobile), `th` (accent colour + sticky), `tr:nth-child(even)` zebra, and `.markdown-content a` (accent colour + `word-break:break-word`).

### TypeScript strictness: API route pitfalls

When writing Next.js API routes (`src/app/api/*/route.ts`), the production build catches TypeScript strictness errors that the dev server tolerates.

**1. `catch (err)` clause — `err` is `unknown` in strict mode:**

```typescript
// ❌ BROKEN in production build — "err" is of type "unknown"
export async function GET() {
  try {
    // ...
  } catch (err) {
    return NextResponse.json({ error: err.message }, { status: 500 }); // ❌ err.message
  }
}

// ✅ CORRECT — cast or check type
export async function GET() {
  try {
    // ...
  } catch (err) {
    return NextResponse.json({ error: (err as Error).message }, { status: 500 });
  }
}
```

**2. `.filter()` / `.sort()` callbacks — implicit `any` on parameters:**

```typescript
// ❌ BROKEN in strict mode
queue.sort((a, b) => (a.scheduled_date || "").localeCompare(b.scheduled_date || ""));
//         ^ Parameter 'a' implicitly has an 'any' type
queue.filter((i) => i.status === "pending").length;
//           ^ Parameter 'i' implicitly has an 'any' type

// ✅ CORRECT — add explicit type
queue.sort((a: any, b: any) => (a.scheduled_date || "").localeCompare(b.scheduled_date || ""));
queue.filter((i: any) => i.status === "pending").length;
```

**3. `data.queue || []` — `queue` has type `any[]` when parsed from JSON:**

```typescript
const data = JSON.parse(raw);
const queue = data.queue || [];  // type: any[]
// Always add explicit annotations when chaining array methods
```

**Rule of thumb:** If the build fails with "Parameter implicitly has an 'any' type", the error is telling you to add a type annotation. If it fails with "'err' is of type 'unknown'", cast `err` to `Error` before accessing `.message`. These are always in YOUR code, not node_modules.

- See `local-tunnel` skill: `references/port-management.md` for port conflict resolution
- See `local-tunnel` skill: full tunnel workflow for localtunnel and Cloudflare
- `references/migration-patterns.md` — comprehensive migration template (10 tables, RLS, triggers, seed data, indexes)
- `references/knowledge-flow-pattern.md` — concrete example: multi-view Next.js app (Library/Feed/Book) with mock data fallback pattern, navigation resilience, and Design System v1.0 integration
- `references/cloudflare-tunnel-ingress-api.md` — managing tunnel subdomains via REST API
- `references/cross-bot-relay.md` — HTTP relay server for cross-agent communication when platform blocks bot-to-bot messages
- `references/infinite-scroll-pattern.md` — IntersectionObserver-based infinite scroll for feeds, with batch rendering, filter reset, and the critical `filtered-before-effect` ordering constraint
- `references/structured-overview-block.md` — embed AI-generated structured summaries inside card markdown (`<!--OVERVIEW-->{json}<!--/OVERVIEW-->`), parser extraction + fallback, cron prompt requirement, and resume-able LLM backfill script pattern

## Related skills

- `cloudflare-tunnel` — advanced tunnel management (API-based config, crash recovery, DNS, multi-tunnel)
- `local-tunnel` — exposing local servers via tunnel
- `system-design-workflow` — designing features before building
- `project-reconnaissance` — auditing existing codebases
