# Design System: monopo saigon

> **Hermes Agent — Implementation Notes**
> 
> The original site uses proprietary fonts (Roobert, Raleway). For self-contained HTML output, use these CDN substitutes:
> - **Primary:** `Inter` (substitute for Roobert) | **Display accent:** `Raleway`
> - **Font stack (CSS):** `font-family: 'Inter', ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;`
> ```html
> <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=Raleway:wght@400&display=swap" rel="stylesheet">
> ```
> Use `write_file` to create HTML. Verify visual accuracy with `browser_vision` after generating.

**Theme:** light | **Vibe:** Liquid iridescence behind editorial silence

## Color Palette
- **Obsidian** `#000000` — Primary text, SVG strokes, overlay fills
- **Inkstone** `#181818` — Footer body copy, secondary headings
- **Slate Pill** `#636363` — Filled neutral button background
- **Felt Gray** `#6d6d6d` — Muted helper text, address blocks
- **Pewter** `#808080` — Secondary mid-tone neutral
- **Ash Mist** `#9a9a9a` — Mid-tone neutral for disabled states
- **Paper** `#ffffff` — Light text on dark surfaces
- **Iridescent Fade** — Gradient (chromatic accent, hero only)

## Typography
- **Primary:** Roobert (sub: Inter), weights 300, 400, 600
- **Display accent:** Raleway weight 400 (sparing use)
- **Body:** system-ui for micro labels
- **Scale:** Minor Third (1.2) from 15px base. Display up to 225px weight 400

## Spacing & Shape
- **Density:** spacious | **Base unit:** 4px | **Max width:** 1078px
- **Section gap:** 46px | **Card padding:** 34px | **Element gap:** 14px
- **Radius:** tags 75px (pill), buttons 75px (pill) — everything else 0px

## Key Rules
- 75px pill radius for buttons/tags only, 0px everywhere else
- Monochrome interface only — iridescent gradient is hero media only
- No box-shadow, no elevation
- Weight 300 at 78px for atmospheric headlines
- `cubic-bezier(0.19, 1, 0.22, 1)` easing, 0.8-1.25s transitions
