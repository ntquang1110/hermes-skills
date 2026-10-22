# Design System: Duolingo

> **Hermes Agent — Implementation Notes**
> 
> Uses feather (sub: Nunito Black) + duolingo-sans (sub: Inter, Nunito Sans).
> ```html
> <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@700;800;900&family=Inter:wght@500;700&display=swap" rel="stylesheet">
> ```

**Theme:** light | **Vibe:** Playful classroom mascot on white paper

## Color Palette
- **Eager Green** `#58cc02` — Headings, CTA fills, footer band
- **Storybook Green** `#d7ffb8` — Soft highlight wash
- **Spark Blue** `#1cb0f6` — Interactive links, outlined CTAs
- **Fresh Leaf** `#a5ed6e` — Green accent
- **Night Ink** `#000437` — Violet accent
- **Paper White** `#ffffff` — Page canvas
- **Charcoal** `#4b4b4b` — Hero headings
- **Pencil Gray** `#777777` — Body text
- **Faded Gray** `#afafaf` — Disabled/button borders

## Typography
- **Display:** feather (sub: Nunito Black), weight 700 only
- **Body:** duolingo-sans (sub: Inter), weights 500, 700
- **Scale:** Minor Third (1.2) from 16px base. Display up to 64px

## Spacing & Shape
- **Base unit:** 4px | **Max width:** 1200px | **Section gap:** 80-120px
- **Radius:** All 12px (links, buttons, nav-items)

## Key Rules
- 12px radius everywhere — no sharp corners
- 2px solid #afafaf borders on outlined buttons
- Uppercase 15px with 0.053em tracking for nav only
- Body stays #777777 17px/500 — mid-gray default
- No gradients, shadows, or glass effects
- Feather only at 48px+ — display face only
