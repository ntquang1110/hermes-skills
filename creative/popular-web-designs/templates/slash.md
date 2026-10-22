# Design System: Slash

> **Hermes Agent — Implementation Notes**
> 
> Uses Ivy Presto (sub: Playfair Display, DM Serif Display) + Inter.
> ```html
> <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:ital,wght@0,400;0,500;1,400&display=swap" rel="stylesheet">
> ```

**Theme:** dark | **Vibe:** Midnight vault with gilded ledger lines

## Color Palette
- **Obsidian** `#08080a` — Page canvas
- **Onyx** `#040406` — Card surface
- **Carbon** `#121317` — Elevated panels
- **Graphite** `#1c1d22` — Hairline borders
- **Bone** `#e2e3e9` — Default body text
- **Paper White** `#ffffff` — Headings, primary action
- **Copper** `#cc9166` — Only chromatic accent
- **Gilded Gradient** — Chart line accent

## Typography
- **Display:** Ivy Presto serif (sub: Playfair Display), weights 400, 500
- **UI:** Inter, weights 300-700
- **Scale:** Minor Third (1.2) from 14px base. Display up to 88px

## Spacing & Shape
- **Density:** compact | **Max width:** 1216px | **Section gap:** 160px
- **Radius:** nav 2px, cards 10px, buttons/tags/inputs 9999px

## Key Rules
- Ivy Presto for headings 28px+ — never for body
- White filled button used once per viewport max
- Copper only for category labels — never buttons
- 1px borders, no drop shadows
- Gilded gradient for data viz only
