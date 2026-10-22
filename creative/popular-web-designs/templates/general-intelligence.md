# Design System: General Intelligence Company

> **Hermes Agent — Implementation Notes**
> 
> Uses ppmondwest (sub: Fraunces, Recoleta, GT Sectra) + af (sub: Inter, Geist, Söhne).
> ```html
> <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Fraunces:opsz,wght@9..144,400;9..144,500&display=swap" rel="stylesheet">
> ```

**Theme:** light | **Vibe:** Literary journal beside a bonfire

## Color Palette
- **Parchment** `#fefffc` — Page canvas (warm off-white)
- **Paper** `#ffffff` — Card surfaces, footer
- **Linen** `#f9faf7` — Input fields, subtle wash
- **Ink Black** `#171717` — Primary foreground
- **Graphite** `#2c2c2c` — Headlines, key body text
- **Charcoal** `#444141` — Secondary text, button text
- **Ash** `#646464` — Muted helper text
- **Fog** `#b4b8b4` — Tertiary borders, disabled
- **Mist** `#dee2de` — Hairline borders (green-tinted signature)
- **Signal Blue** `#41a1cf` — Outlined action border only
- **Cerulean** `#0081c0` — Singular saturated card surface

## Typography
- **Display:** ppmondwest serif (sub: Fraunces), weights 400, 500
- **UI:** af sans (sub: Inter), weights 400-700
- **Scale:** Major Second (1.125) from 16px base. Display up to 54px

## Spacing & Shape
- **Base unit:** 4px | **Max width:** 1200px | **Section gap:** 32-64px
- **Radius:** nav 50px (pill), cards 12-16px, buttons 4-8px, large 24px

## Key Rules
- ppmondwest for headings 27px+ — never sans for display
- Weight 400 on serif — never 600+
- 1px solid #dee2de borders on cards — green-tinted signature
- Signal Blue as border-only accent — no filled chromatic buttons
- No box-shadow on buttons — borders + backdrop-blur instead
