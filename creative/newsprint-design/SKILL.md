---
name: newsprint-design
description: "Newsprint — serif, zero radius, ink-on-paper grid."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows, web]
metadata:
  hermes:
    tags: [design, editorial, newspaper, typography, grid, print]
    related_skills: [claude-design, popular-web-designs, html-unslop]
---

# Design Style: Newsprint

## 1. Design Philosophy

**"All the News That's Fit to Print."**

This style is an ode to the golden age of print journalism, reimagined for the web. It embodies **absolute clarity, hierarchy, and structure** through its unwavering commitment to high-contrast typography, grid-based layouts, and sharp geometric precision.

### Core DNA
The newsprint aesthetic rejects modern web trends of soft shadows, blurred backgrounds, and rounded corners. Instead, it embraces:

- **Stark Geometry**: Zero border radius. Every element is a perfect rectangle with sharp 90-degree corners.
- **High Information Density**: Tight padding, collapsed grid borders, and efficient use of space mimic newspaper column layouts.
- **Typographic Drama**: Massive serif headlines (up to 9xl on desktop) paired with smaller, highly legible body text create extreme hierarchy.
- **Visible Structure**: Grid lines aren't hidden — they're celebrated. Borders between columns and sections are explicit and prominent.
- **Editorial Authority**: The design feels serious, timeless, and trustworthy — like a publication of record.
- **Paper Texture**: Subtle grain overlays and line patterns simulate the tactile quality of newsprint without being overly skeuomorphic.

### Vibe
Authoritative, intellectual, urgent, timeless. It feels like holding a fresh morning newspaper — crisp, organized, and information-rich. The design exudes confidence and credibility.

## 2. Design Token System

### Colors (Light Mode Only — No Dark Mode)

| Token | Value | Usage |
|-------|-------|-------|
| Background | `#F9F9F7` | Newsprint Off-White — warm, mimics aged paper, reduces eye strain |
| Foreground | `#111111` | Ink Black — very deep black, used for all text and borders |
| Muted | `#E5E5E0` | Divider Grey — light grey for secondary borders and subtle backgrounds |
| Accent | `#CC0000` | Editorial Red — extremely sparing, only for breaking news badges, CTAs, hover states |
| Border | `#111111` | Ink Black — primary structural element, defines grid and creates visual rhythm |
| Neutral-100 | `#F5F5F5` | Hover backgrounds |
| Neutral-200 | `#E5E5E5` | Image placeholders |
| Neutral-400 | `#A3A3A3` | Muted text in dark sections |
| Neutral-500 | `#737373` | Metadata, captions |
| Neutral-600 | `#525252` | Body text variations |
| Neutral-700 | `#404040` | Secondary headings |

### Typography

**Font Stack:**

| Role | Font | Fallback |
|------|------|----------|
| Serif (Headlines & Display) | `'Playfair Display'` | `'Times New Roman', serif` |
| Serif (Body) | `'Lora'` | `Georgia, serif` |
| Sans-Serif (UI) | `'Inter'` | `'Helvetica Neue', sans-serif` |
| Monospace (Data) | `'JetBrains Mono'` | `'Courier New', monospace` |

**Scale Strategy:**
- H1 (Hero): `text-5xl sm:text-6xl lg:text-9xl` (80px → 128px), `leading-[0.9]`, `tracking-tighter`
- H2 (Section): `text-4xl lg:text-5xl`, `font-black`, uppercase or sentence case
- H3 (Card Titles): `text-2xl lg:text-3xl`, `font-bold`, serif
- Body: `text-sm` to `text-lg` (14px → 18px), Lora, `leading-relaxed`
- Metadata/Labels: `text-xs` (12px), uppercase, `tracking-widest`, monospace or sans

**Text Transform:** Uppercase for nav, labels, metadata, badges. Sentence case for headlines, body.

### Radius & Border

- **Border Radius:** `0px` everywhere. No exceptions.
- **Border Width:** 1px solid black standard. `border-b-4` or `border-4` (4px) for major dividers.
- **Border Style:** Always solid. Never dashed/dotted except rare decorative elements.
- **Collapsed grids:** Adjacent elements share borders to avoid double lines.

### Shadows/Effects

- **No soft drop shadows.** Flat design.
- **Hover — Hard Offset Shadow:** `box-shadow: 4px 4px 0px 0px #111111` + `translate(-2px, -2px)`
- **No blur, no inner shadows, no gradient overlays.**

### Textures & Patterns (Critical for Depth)

**1. Dot Grid Pattern (Body Background):**
```css
background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='4' height='4' viewBox='0 0 4 4'%3E%3Cpath fill='%23111111' fill-opacity='0.04' d='M1 3h1v1H1V3zm2-2h1v1H3V1z'%3E%3C/path%3E%3C/svg%3E");
```

**2. Line Grid Overlay (Section Texture):**
```css
.newsprint-texture::before {
  content: '';
  position: absolute; inset: 0;
  background-image:
    linear-gradient(0deg, transparent 98%, rgba(0,0,0,0.02) 100%),
    linear-gradient(90deg, transparent 98%, rgba(0,0,0,0.02) 100%);
  background-size: 3px 3px;
  pointer-events: none; opacity: 0.5;
}
```

**3. Radial Dot Pattern (Image Placeholders):**
```css
background-image: radial-gradient(#000 1px, transparent 1px);
background-size: 16px 16px; opacity: 0.1;
```

**4. Ornamental Dividers:**
```html
<div class="py-8 text-center font-serif text-2xl text-neutral-400 tracking-[1em]">
  &#x2727; &#x2727; &#x2727;
</div>
```

## 3. Component Styling

### Buttons

| Variant | Default | Hover |
|---------|---------|-------|
| Primary | `bg-[#111111] text-[#F9F9F7]` | Invert: `bg-white text-[#111111] border-[#111111]` |
| Secondary (Outline) | `border border-[#111111] bg-transparent` | `bg-[#111111] text-[#F9F9F7]` |
| Ghost | No border | `hover:bg-[#E5E5E0]` |
| Link | Text only | Red underline (`decoration-[#CC0000] decoration-2`) |

- Sharp corners. Uppercase, `tracking-widest`, sans-serif.
- `transition-all duration-200`
- Min 44px touch target.

### Cards/Containers
- `border border-[#111111] bg-[#F9F9F7] p-6`
- Hover: `hover:bg-neutral-100` or `.hard-shadow-hover`
- Collapsed grid borders using `border-r` + `border-b`

### Inputs
- `border-b-2 border-[#111111] bg-transparent px-3 py-2 font-mono text-sm`
- Focus: `focus-visible:bg-[#F0F0F0] focus-visible:outline-none`
- No radius. No ring.

### Icons
- Library: `lucide-react`, `stroke-width={1.5}`, color `#111111`
- Icon containers: `border border-black h-12 w-12 flex items-center justify-center`
- Hover: `hover:bg-black hover:text-white`

## 4. Non-Generic Bold Choices

1. **Vertical Grid Dividers** — Use `border-r` for strict vertical columns like newspaper
2. **Drop Caps** — `text-7xl float-left` on first letter of key paragraphs
3. **Marquee Ticker** — Horizontal scrolling stats, black bg, white text, red badges
4. **Edition Metadata** — "Vol. 1 | Date | Edition" in header/footer
5. **Justified Text** — `text-justify` for multi-column body text
6. **Grayscale Images** — `grayscale` default, `sepia-[50%]` on hover
7. **Asymmetric Layouts** — 8-col/4-col, 5-col/7-col splits, not 50/50
8. **Uppercase Labels** — `uppercase tracking-widest text-xs font-mono` everywhere
9. **Inverted Sections** — At least one black-bg section with white text + red accent

## 5. Layout

- **Container:** `max-w-screen-xl` (1280px), centered `mx-auto`
- **Grid:** 12-column (`grid-cols-12`), collapsed borders
- **Spacing:** High density. `py-16` sections, `p-6` to `p-8` cards, `gap-6` to `gap-8`
- **Mobile:** Reduce one step, collapse to single column, remove `border-r`

## 6. Animation

- **Duration:** 200ms, `ease-out` — fast and snappy
- **Hover:** Color inversion, hard shadow offset, underline, scale(1.05) on images
- **No floating, no bouncy easing.**
- **Accordion:** `grid transition-all duration-300 ease-in-out`

## 7. Responsive

| Breakpoint | Width |
|------------|-------|
| Mobile (default) | < 768px |
| Tablet `md:` | 768px+ |
| Desktop `lg:` | 1024px+ |

**Mobile adaptations:** Single column, remove `border-r`, shrink headlines, reduce padding, full-width CTAs, hamburger nav.

## 8. Accessibility

- Black `#111111` on Off-White `#F9F9F7`: >17:1 (AAA)
- Red `#CC0000` on Off-White: >5:1 (AA)
- Never red on black
- Focus: `focus-visible:ring-2 focus-visible:ring-neutral-950 focus-visible:ring-offset-2`
- Semantic HTML, ARIA labels, keyboard navigation

## 9. CSS Utilities

```css
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&family=Playfair+Display:ital,wght@0,400;0,600;0,700;0,900;1,400&family=Lora:ital,wght@0,400;0,600;1,400&display=swap');

.font-serif { font-family: 'Playfair Display', serif; }
.font-body { font-family: 'Lora', serif; }
.font-sans { font-family: 'Inter', sans-serif; }
.font-mono { font-family: 'JetBrains Mono', monospace; }

.sharp-corners { border-radius: 0px !important; }

.hard-shadow-hover:hover {
  box-shadow: 4px 4px 0px 0px #111111;
  transform: translate(-2px, -2px);
}
```

## 10. Implementation Checklist

1. Background `#F9F9F7` with dot grid SVG texture
2. Import Playfair Display + Lora + Inter + JetBrains Mono with `display=swap`
3. Define font classes (.font-serif, .font-body, .font-sans, .font-mono)
4. Zero border radius everywhere — `.sharp-corners` utility
5. Hard shadow hover utility
6. Newsprint line-grid texture for major sections
7. 12-column grid with collapsed borders (border-r + border-b pattern)
8. Red accent `#CC0000` used sparingly
9. Inverted section (black bg, white text) in at least one section
10. Grayscale images with sepia hover
11. Marquee ticker for stats
12. Drop cap on first paragraph
13. Edition metadata in header/footer
14. Min 44px touch targets
15. `focus-visible` ring on all interactive
