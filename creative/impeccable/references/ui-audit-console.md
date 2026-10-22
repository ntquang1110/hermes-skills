# Browser Console UI Audit (detector without vision)

When the active model cannot process screenshots (vision provider rejects `image_url`), audit a page directly in the browser with a computed-styles probe. This is the deterministic half of the detector — it reads real computed values, not eyeballs. Run via `browser_console` with `expression=<the IIFE>` after `browser_navigate` to the page (set auth cookies / passcode first).

## What it checks

| Probe | AI-tell / rule |
|-------|----------------|
| `fonts` set from every element | `overused-font` — system-ui/Segoe everywhere = no display voice |
| emoji count in `button, .icon, [class*=icon], li` | `glyph-icons` — emoji standing in for an icon system |
| `radii` set across elements | radii chaos — more than ~4 steps (3/4/6/8/10/20/50) = no token system; canonical 8/12/16 + pill |
| `bodyBg` / `bodyColor` + contrast calc | `low-contrast` — note body-level check lies on card-based UIs (text lives on lighter cards); re-check the actual visible container |
| heading counts (h1/h2/h3) | `flat-type-hierarchy` — 0 h2 = no section hierarchy |
| `gradient-text` via `backgroundClip==='text'` | `gradient-text` |
| hard-offset shadows (`Npx Npx 0px` with N>2) | `hard-offset-shadow` |

## Script

```js
(() => {
  const res = {url: location.href, tells: [], fonts: new Set()};
  document.querySelectorAll('*').forEach(el => {
    const fs = getComputedStyle(el).fontFamily;
    if (fs) res.fonts.add(fs.split(',')[0].replace(/["']/g,'').trim());
    const bg = getComputedStyle(el).backgroundImage;
    if (bg && bg.includes('gradient') && getComputedStyle(el).webkitBackgroundClip === 'text') res.tells.push('gradient-text');
  });
  const emojiRe = /[\u{1F300}-\u{1FAFF}\u{2600}-\u{27BF}]/u;
  let emojiCount = 0;
  document.querySelectorAll('button, .icon, [class*=icon], li').forEach(el => { if (emojiRe.test(el.textContent)) emojiCount++; });
  if (emojiCount > 3) res.tells.push(`emoji-icons:${emojiCount}`);
  const radii = new Set();
  document.querySelectorAll('*').forEach(el => { const r = getComputedStyle(el).borderRadius; if (r && r !== '0px') radii.add(r); });
  res.radii = [...radii].slice(0,8);
  const b = getComputedStyle(document.body);
  res.bodyBg = b.backgroundColor; res.bodyColor = b.color;
  res.headings = {h1: document.querySelectorAll('h1').length, h2: document.querySelectorAll('h2').length, h3: document.querySelectorAll('h3').length};
  function lum(rgb){ const p = rgb.match(/\d+/g).slice(0,3).map(v => {v/=255; return v<=0.03928?v/12.92:Math.pow((v+0.055)/1.055,2.4)}); return 0.2126*p[0]+0.7152*p[1]+0.0722*p[2]; }
  try { const L1=lum(b.color),L2=lum(b.backgroundColor); res.bodyContrast=((Math.max(L1,L2)+0.05)/(Math.min(L1,L2)+0.05)).toFixed(2);} catch(e){res.bodyContrast='n/a';}
  res.tells=[...new Set(res.tells)]; res.fonts=[...res.fonts].slice(0,8);
  return JSON.stringify(res);
})()
```

## Interpreting results

- **fonts**: `system-ui`, `Segoe UI`, `Arial` first → no display face. Fix: add a real display face (Space Grotesk / Inter for body) via Google Fonts `<link>` in `<head>` + `font-family` on `h1,h2,h3,.card-header,...`. Keep one source of truth.
- **emoji-icons:N** — N>3 in controls/nav is a tell. Replace nav/tab icons with inline SVG (14-15px, `stroke="currentColor"` strokeWidth 1.8, 1 stroke weight). Keep emoji that are **content** (category tags, org-chart labels) and **data contract** (status strings matched against API responses like `'🔵 Working'` — changing them breaks filtering).
- **radii**: >4 distinct steps → normalize to 8/12/16 (sed in place: `border-radius: 3px`→`6px`→`8px`, `4px`→`6px`, `10px`→`12px`). `50%` and `999px` pills are fine.
- **headings h2=0**: card headers are often `<div class="card-header"><span>…</span></div>`. Convert to `<h2 class="card-header">` preserving the class — but then the FIRST `</div>` after the opening tag must become `</h2>` (do it positionally with a script, right-to-left, and re-check tag balance; a naive replace can corrupt nested divs like `.mc-label`).
- **bodyContrast** near 1.0 on a dark theme usually means the probe measured the wrong container (black body + black text) while real text sits on lighter cards — re-measure the actual visible element rather than declaring failure.

## Pitfalls

- `browser_console` blocks `navigator.*` by default (`sensitive browser JavaScript primitive`) — the audit above avoids navigator, fine.
- For pages behind a passcode gate, `browser_navigate` → `browser_type` the passcode → `browser_click` before running the audit.
- Tailwind v4: `rounded-sm` (2px) everywhere can be normalized globally by adding `--radius-sm: 8px; --radius-md: 12px; --radius-lg: 16px;` to the `@theme` block in `index.css` — one change, N usages.
- Verify after edits: re-run the same probe; emoji count 0 in nav, fonts show the new face, radii set shrinks.
