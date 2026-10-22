# Design System: ORYZO AI

> **Hermes Agent — Implementation Notes**
> 
> Uses halyard-display-variable (sub: Inter, Söhne). For HTML, use Inter with uppercase weight 500 for most text.
> ```html
> <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500&display=swap" rel="stylesheet">
> ```

**Theme:** dark | **Vibe:** Darkroom product editorial, lone object in warm darkness

## Color Palette
- **Ember Accent** `#dc5000` — Orange text for links, tags, emphasized short phrases only
- **Pure Black** `#000000` — SVG icon fills only
- **Walnut Shadow** `#100904` — Page canvas, deepest background
- **Bark Brown** `#382416` — Elevated surface, filled button background
- **Cork Border** `#40372e` — Hairline dividers, dashed separators
- **Driftwood** `#6c5f51` — Mid-tone warm gray for dividers
- **Warm Cream** `#ffedd7` — Light text, high-contrast captions

## Typography
- **Single face:** halyard-display-variable (sub: Inter), weights 400, 500
- **Scale:** Minor Third (1.2) from 16px base. Display up to 51px weight 500
- All UI text uppercase weight 500. Only body copy (29px) is mixed-case weight 400

## Spacing & Shape
- **Density:** comfortable | **Card padding:** 24px | **Element gap:** 18px
- **Radius:** cards 12px, buttons-outlined 22.5px, buttons-pill 36px

## Key Rules
- All text in #ffedd7 Warm Cream — never pure #fff
- Ember #dc5000 for credit lines/links only — never for buttons
- Uppercase weight 500 across interface, except 29px body
- Section gaps at 100vh — each section is one viewport
- 1px dashed #40372e dividers
- No drop shadows — depth from two-step surface stack
