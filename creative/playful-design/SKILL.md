---
name: playful-design
description: "Playful Geometric — Memphis-style, hard shadows, pop colors."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows, web]
metadata:
  hermes:
    tags: [design, playful, geometric, memphis, pop, colorful, fun]
    related_skills: [claude-design, popular-web-designs, html-unslop]
---

# Playful Geometric Design System

## Design Philosophy

**Playful Geometric** is the antidote to sterile, corporate minimalism. It creates an emotional connection through **optimism, clarity, and tactile fun**.

The core concept is **"Stable Grid, Wild Decoration"**. The content itself (text, forms) lives in clean, readable areas, but the world around it is alive with movement and shape. It references the **Memphis Group** (80s) but cleans it up for modern digital screens — removing the chaos while keeping the energy.

### The Vibe
**Friendly. Tactile. Pop. Energetic.**
It feels like a playground or a well-organized sticker book. It invites clicking. It smiles at you.

### Visual Signatures
- **Primitive Shapes**: Circles, triangles, squares, pill shapes, and squiggles used as background elements, masks, or icons.
- **Hard Shadows**: Elements often have a hard, offset drop shadow (no blur) giving a sticker or cut-out paper feel.
- **Pattern Fills**: Polka dots, grid lines, and diagonal stripes used to fill shapes or backgrounds.
- **Varied Radii**: Mixing fully rounded corners with sharp ones to create "leaf" shapes or asymmetric blobs.

---

## Design Token System

### Colors (Light Mode)

| Token | Value | Usage |
|-------|-------|-------|
| Background | `#FFFDF5` | Warm Cream/Off-White — paper feel |
| Foreground | `#1E293B` | Slate 800 — softer than pure black |
| Muted | `#F1F5F9` | Slate 100 |
| MutedForeground | `#64748B` | Slate 500 |
| Accent | `#8B5CF6` | Vivid Violet — primary brand |
| AccentForeground | `#FFFFFF` | White |
| Secondary | `#F472B6` | Hot Pink — playful pop |
| Tertiary | `#FBBF24` | Amber/Yellow — optimism |
| Quaternary | `#34D399` | Emerald/Mint — freshness |
| Border | `#E2E8F0` | Slate 200 |
| Card | `#FFFFFF` | White |

**Usage Rule**: Use `accent` for primary actions. Use `secondary`, `tertiary`, `quaternary` rotationally for decorative shapes, icons, or emphasized words to create a "confetti" effect.

### Typography

| Role | Font | Weight |
|------|------|--------|
| Headings | `'Outfit', system-ui, sans-serif` | 700, 800 |
| Body | `'Plus Jakarta Sans', system-ui, sans-serif` | 400, 500 |

**Scale Ratio**: 1.25 (Major Third) — melodic and harmonious.

### Radius & Border

| Token | Value |
|-------|-------|
| radius-sm | `8px` |
| radius-md | `16px` |
| radius-lg | `24px` |
| radius-full | `9999px` |
| border-width | `2px` (chunky by default) |

**Special "Blob" Radius**: `rounded-tl-2xl rounded-tr-2xl rounded-br-2xl rounded-bl-none` (speech bubble) or `rounded-t-full rounded-b-none` (arch).

### Shadows & Effects

**The "Pop" Shadow (Hard Shadow):**
```css
box-shadow: 4px 4px 0px 0px #1E293B;  /* default */
box-shadow: 6px 6px 0px 0px #1E293B;  /* hover — lift */
box-shadow: 2px 2px 0px 0px #1E293B;  /* active — press */
```

No blur. Solid offset colors.

### Textures & Patterns
- **Dot Grid**: Small dots in strict formation as background
- **Squiggles**: SVG paths as section dividers or heading underlines
- **Confetti**: Small SVG shapes (triangles, circles) behind content

---

## Component Styling

### Buttons

**Primary ("The Candy Button"):**
- Bg: `#8B5CF6`, text: white, font-weight: 700
- Radius: `rounded-full`, Border: 2px solid `#1E293B`
- Shadow: 4px 4px 0px `#1E293B`
- Hover: `translate(-2px, -2px)`, shadow 6px 6px
- Active: `translate(2px, 2px)`, shadow 2px 2px

**Secondary:**
- Transparent bg, border 2px solid `#1E293B`
- Radius: `rounded-full`, hover fills yellow `#FBBF24`

### Cards ("The Sticker Card")
- Bg white, border 2px solid `#1E293B`, radius `rounded-xl`
- Shadow: 8px 8px 0px `#E2E8F0` (or pink for featured)
- Hover: rotate -1deg, scale 1.02
- Icon: floating circle half-in/half-out of top border

### Inputs
- Bg white, border 2px solid `#CBD5E1`, radius `rounded-lg`
- Focus: border accent + shadow 4px 4px 0px accent
- Label: bold, uppercase, tracking-wide

---

## Layout Strategy

- **Container:** `max-w-6xl`, spacing `py-24`
- **Grid:** 12-column, grouped into big blocks (6/6 or 4/4/4)

**Hero:** Text left, image right. Yellow circle behind text. Blob mask on image.
**Features:** Grid of 3, dashed SVG connector, alternating colors (Violet/Pink/Yellow).
**Pricing:** Middle card scaled 1.1x, "MOST POPULAR" badge rotated 15deg.

---

## Effects & Animation

**Feel:** Bouncy, Elastic, Fun.

- **Hover:** `transition-all duration-300 ease-[cubic-bezier(0.34,1.56,0.64,1)]`
- **Entrance:** Scale 0→1 with bounce
- **Marquee:** Infinite scrolling for logos/keywords
- **Wiggle:** `@keyframes wiggle { 0%,100%{rotate:0deg} 50%{rotate:3deg} }` on icon hover

---

## Iconography

- **Library:** Lucide React, stroke-width `2.5px`, round caps/joins
- **Usage:** Always enclosed in shapes — never floating alone

---

## Responsive

- Mobile: stack, reduce shadows to 2px, hide floating shapes
- Min 48px button height

---

## Accessibility

- Text `#1E293B` on `#FFFDF5`: AAA
- Never rely only on color — use shapes + text labels
- Respect `prefers-reduced-motion`
- Focus: thick colored border + hard shadow

---

## Implementation Checklist

1. Background `#FFFDF5`, foreground `#1E293B`
2. Import Outfit + Plus Jakarta Sans with `display=swap`
3. Define 4 accent colors (violet, pink, yellow, emerald)
4. Hard pop shadow utility (4px/6px/2px)
5. Dot grid pattern background
6. Blob/shape decorations (circles, triangles, squiggles)
7. Chunky 2px borders everywhere
8. Pill-shaped buttons with hard shadow
9. Sticker cards with wiggle hover
10. Bouncy transition (cubic-bezier 0.34,1.56,0.64,1)
11. `prefers-reduced-motion` fallback
12. Min 48px touch targets
