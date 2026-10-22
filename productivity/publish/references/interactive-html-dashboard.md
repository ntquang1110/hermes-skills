# Interactive HTML Dashboard Pattern (self-contained, no backend)

Pattern used for the Leadership Hub — a single HTML file that works standalone on mobile/desktop, persists data in browser, and lets the agent/user exchange data via JSON export/import. No server needed.

## Architecture

```
Single .html file:
  <style>  → dark theme, responsive, tabs
  <script> → data model + localStorage + render functions
```

### Data persistence (3 layers)
1. **localStorage** — auto-save on every input: `localStorage.setItem(key, JSON.stringify(data))`
2. **Export JSON** — button downloads full state: `new Blob([JSON.stringify(data)], {type:'application/json'})` + `<a download>`
3. **Import JSON** — `<input type="file" accept=".json">` → FileReader → `JSON.parse` → overwrite state → re-render

**Versioned storage keys:** use `_v2` suffix when evolving schema so old corrupted data doesn't break new code. On load, merge old key into new structure (migration), never just overwrite.

### Tab system (no router needed)
```js
const TABS = [{id:'canvas', icon:'📋', label:'Canvas'}, ...];
function switchTab(id){ currentTab=id; renderTabs(); renderContent(id); }
function renderContent(id){ const m = {canvas:renderCanvas, journal:renderJournal, ...}; m[id](el); }
```

### Interactive links — ALWAYS button + addEventListener, NEVER inline onclick with template-literal escaping
```js
// ✅ SAFE
`<button data-tab="${s.tabId}" ...>${s.linkLabel}</button>`
// after innerHTML:
el.querySelectorAll('[data-tab]').forEach(b => b.addEventListener('click', () => switchTab(b.dataset.tab)));

// ❌ BROKEN (3 failures this session)
`<a onclick="switchTab('${s.tabId}')">`  // `\"` inside backtick = literal backslash, not quote
`<a href="javascript:switchTab('x')">`   // javascript: hrefs blocked in some contexts
```
External links (real URLs) can use `<a href target="_blank" rel="noopener">` — that's fine.

### Data structure pattern (each "module" = one tab)
```js
const DEFAULT_DATA = {
  canvas: {...}, journal: [], actions: [],
  timeline: [...], focus: {...},
  progress: {}   // keyed by date or id
};
```

## Verification workflow (BEFORE telling user it works)
User explicitly demanded: simulate the user before claiming done.
1. `browser_navigate(preview_url)` → check title: `document.title`
2. Count elements: `document.querySelectorAll('.tab-btn').length`
3. Click real buttons via console: `el.click()` then assert `document.querySelector('.tab-btn.active').textContent`
4. Check `browser_console` with `clear=true` → returns `js_errors: []`
5. Only then report "✅ hoạt động" — with exact test results as evidence

## Pitfalls
- **`read_file` line numbers corrupt HTML** — read via `terminal('cat file')` when building payloads
- **htmlpreview cache** — user sees stale version; test via browser tools first; if browser tools pass, tell user hard-refresh/incognito
- **Emoji in sheet/tab names** — Google Sheets API range needs quoted name: `"'📋 Dự án'!A1:I1"`
- Keep the file self-contained (inline CSS/JS, no CDN except fonts) so it works on phone + in htmlpreview sandbox
