# Design System: Monad

> **Hermes Agent — Implementation Notes**
> 
> Uses ABC Diatype Mono (sub: JetBrains Mono, IBM Plex Mono) + Untitled Serif (sub: Georgia, Times New Roman).
> ```html
> <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&family=Playfair+Display:wght@400&display=swap" rel="stylesheet">
> ```

**Theme:** light | **Vibe:** Editorial tech journal on warm parchment

## Color Palette
- **Parchment** `#f6f3f1` — Page canvas
- **Lake Blue** `#2b59d1` — Single primary action fill
- **Periwinkle Mist** `#cfdaf5` — Muted UI surface, disabled controls
- **Off-Black** `#242424` — Primary text, action fills
- **Ink** `#000000` — Announcement bar
- **Graphite** `#4e4d4d` — Secondary text
- **Smoke** `#797776` — Muted helper text
- **Ash** `#cecac8` — Hairline borders
- **Pastels:** Sky Blue `#a0b5eb`, Mint `#a7fccd`, Coral `#ff9473`, Gold `#ecda98`, Crimson `#f37a0a` — decorative only

## Typography
- **Code/UI:** ABC Diatype Mono (sub: JetBrains Mono), weights 400, 500
- **Display:** Untitled Serif (sub: Playfair Display), weight 400 only
- **Scale:** Minor Third (1.2) from 16px base. Display up to 80px
- Negative letter-spacing on all text (-0.02em to -0.4px)

## Spacing & Shape
- **Base unit:** 8px | **Max width:** 1432px | **Section gap:** 64px
- **Card padding:** 40px | **Element gap:** 16px
- **Radius:** cards 40px, buttons 100px (pill), tags 9999px

## Key Rules
- Untitled Serif weight 400 for all headings — never bold
- ABC Diatype Mono for all body, buttons, nav, badges
- 100px pill buttons + 40px card radius
- Parchment canvas — never pure white
- Lake Blue for single primary action only
- 1px Ash borders, no drop shadows
- Uppercase + tight tracking on nav/buttons via mono
