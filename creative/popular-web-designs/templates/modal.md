# Design System: Modal

> **Hermes Agent — Implementation Notes**
> 
> Uses Goga (sub: Inter Tight, Space Grotesk) + Inter Variable.
> ```html
> <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500&family=Space+Grotesk:wght@400;500&display=swap" rel="stylesheet">
> ```

**Theme:** dark | **Vibe:** Phosphor terminal in a darkened server room

## Color Palette
- **Void Black** `#000000` — Page canvas
- **Ground Iron** `#181818` — Button fill, card surface
- **Carbon Veil** `#212525` — Elevated surfaces, nav
- **Lime Pulse** `#7fee64` — Primary accent, hero CTA (one per viewport)
- **Phosphor White** `#ddffdc` — Primary text, headings
- **Sage 60** `#8cab87` — Body copy
- **Sage 40** `#677d64` — Muted text
- **Circuit Border** `#485346` — Outlined action border
- **Moss 70** `#9cbf93` — Eyebrow labels

## Typography
- **Display:** Goga (sub: Space Grotesk), weights 400, 500
- **UI:** Inter Variable, weights 400, 500
- **Scale:** Minor Third (1.2) from 14px base. Display up to 64px

## Spacing & Shape
- **Base unit:** 4px | **Max width:** 1280px | **Section gap:** 80px
- **Radius:** cards 8px, buttons 12px, pills 9999px

## Key Rules
- Lime Pulse on exactly one element per viewport
- Goga 'ss01' + Inter 'cv11' stylistic sets enabled
- Body text Sage 60 on black — 19:1 contrast
- No blue/purple — monochromatic green-on-black
- No shadows except nav bar
- 32px card padding — comfortable density
