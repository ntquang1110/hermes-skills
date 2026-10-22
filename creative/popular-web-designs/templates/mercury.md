# Design System: Mercury

> **Hermes Agent — Implementation Notes**
>
> The original site uses proprietary fonts (Arcadia, ArcadiaDisplay). For self-contained HTML output, use these CDN substitutes:
> - **Primary:** `Inter` | **Display:** `Space Grotesk` (closest substitute for ArcadiaDisplay's wide-set architectural quality)
> - **Font stack (CSS):** `font-family: 'Inter', ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;`
> - **Display stack (CSS):** `font-family: 'Space Grotesk', ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;`
> ```html
> <link href="https://fonts.googleapis.com/css2?family=Inter:wght@360;400;420;480&family=Space+Grotesk:wght@360;480;530&display=swap" rel="stylesheet">
> ```
> Use `write_file` to create HTML. Serve via the `publish` skill (preview.thefirstonly.com).
> Verify visual accuracy with `browser_vision` after generating.

## 1. Visual Theme & Atmosphere

Mercury operates in an alpine banking aesthetic: a near-black canvas (#171721) sets a cinematic, observatory-like atmosphere where content surfaces float as subtly lighter graphite cards. The interface is overwhelmingly monochromatic — ivory text on onyx, with a single vivid cobalt (#5266eb) acting as the only chromatic punctuation, reserved exclusively for the primary "Open account" action.

Typography carries the weight of expression: a custom display face at intermediate weight 480 (neither bold nor light) paired with a refined body face at weight 400, creating a voice that is confident but never loud. Components are flat and borderless, relying on the 12px-radius graphite card lift and pill-shaped controls to define structure rather than shadows.

The full-bleed photographic hero — misty mountains with a solitary desk — establishes aspiration before the product UI takes over, and every subsequent surface maintains that hushed, premium darkness.

**Key Characteristics:**
- Near-black `#171721` canvas — cinematic, observatory-like atmosphere
- Single chromatic accent: Cobalt `#5266eb` — reserved for the one primary action per page
- Custom intermediate-weight typefaces (weights 360, 420, 480, 530) — never bold, never thin
- Flat, borderless components — separation through value contrast, not shadows
- Pill-shaped controls (32px–40px radius) for all interactive elements
- Graphite card lift (`#1e1e2a` on `#171721`) — one step lighter, no drop shadows
- Spacious density — 72px vertical section rhythm, 32px card padding
- Full-bleed cinematic photography in hero, dark surfaces everywhere else

## 2. Color Palette & Roles

### Brand Accent
- **Cobalt** (`#5266eb`): `--color-cobalt` — the sole chromatic note. Used exclusively for the single primary CTA per page (filled buttons, selected nav states, focused conversion moments). Never decorative.

### Neutrals — Surfaces
| Name | Value | Token | Role |
|------|-------|-------|------|
| Onyx Canvas | `#171721` | `--color-onyx-canvas` | Dominant page background, hero overlay base, footer and section canvases |
| Graphite Card | `#1e1e2a` | `--color-graphite-card` | Elevated card and section surfaces — one step lighter than the canvas to create quiet separation |
| Obsidian Button | `#272735` | `--color-obsidian-button` | Secondary button fills, inline form backgrounds, subtle interactive surfaces |

### Neutrals — Text & Borders
| Name | Value | Token | Role |
|------|-------|-------|------|
| Ivory Text | `#ededf3` | `--color-ivory-text` | Primary text, icons, nav items, ghost-button strokes and text — the dominant foreground color |
| Ash Text | `#c3c3cc` | `--color-ash-text` | Muted body copy, helper text, secondary labels — reduced hierarchy without losing legibility |
| Slate Border | `#70707d` | `--color-slate-border` | Medium-weight dividers and structural borders between content blocks |
| Mist Border | `#e2e3ed` | `--color-mist-border` | Light hairline borders, ghost-button outlines, input edges — light-on-dark border |
| Pure White | `#ffffff` | `--color-pure-white` | Text and icon fills on cobalt primary buttons for maximum contrast |

### Surface Levels
| Level | Name | Value | Purpose |
|-------|------|-------|---------|
| 0 | Onyx Canvas | `#171721` | Base page background — hero overlay, section canvases, footer |
| 1 | Graphite Card | `#1e1e2a` | Elevated content surface — product cards, feature blocks, form containers |
| 2 | Obsidian Button | `#272735` | Interactive surface — secondary button fills, inline form attachments |

## 3. Typography Rules

### Font Family
- **Body/UI:** `arcadia` (substitute: `Inter`) — handles navigation, body copy, buttons, inputs, labels, and supporting text
- **Display:** `arcadiaDisplay` (substitute: `Space Grotesk`) — headlines and display copy from 28px through 65px
- **Intermediate weight axis:** 360, 400, 420, 480, 530 — instead of standard 300/400/600/700
- **Fallback:** `Inter` for body, `Söhne Breit` for display

### Type Scale

| Role | Size | Weight | Line Height | Letter Spacing | Token |
|------|------|--------|-------------|----------------|-------|
| caption | 12px | 480 | 1.00 | 0.12px | `--text-caption` |
| body-sm | 14px | 480 | 1.00 | 0.07px | `--text-body-sm` |
| body | 16px | 400 | 1.50 | — | `--text-body` |
| body-lg | 18px | 480 | 1.35 | — | `--text-body-lg` |
| subheading | 21px | 360 | 1.35 | — | `--text-subheading` |
| heading-sm | 28px | 480 | 1.20 | 0.42px | `--text-heading-sm` |
| heading | 32px | 480 | 1.15 | 0.48px | `--text-heading` |
| heading-lg | 42px | 480 | 1.15 | 0.42px | `--text-heading-lg` |
| display | 65px | 480 | 1.10 | — | `--text-display` |

### Principles
- **Weight 480 is the signature** — heavier than regular but distinctly lighter than semibold. Used for all headings from 28px through 65px. This intermediate weight creates a voice that asserts without shouting.
- **Tight line-heights on display** (1.1–1.15) with positive letter-spacing (0.01–0.02em) give large text an architectural, wide-set quality.
- **Generous body line-height** at 1.5 (16px weight 400) keeps reading comfortable against the dark canvas.
- **No bold (700+) anywhere** — weight 480 is the ceiling. The intermediate weight scale (360, 420, 480, 530) replaces the conventional bold/light binary.
- **Letter-spacing is positive** on headings (0.42–0.48px) — not compressed like Vercel. Mercury's text breathes.

## 4. Component Stylings

### Primary CTA Button (Cobalt)
**Role:** The sole chromatic action in the system — reserved for the most important conversion
- Background: `#5266eb` Cobalt
- Text: `#ffffff` Pure White, 16px arcadia weight 400
- Border-radius: 32px (pill)
- Padding: 0px vertical, 20px horizontal (inline); 40px vertical when standalone
- No border, no shadow
- The vivid blue against the dark canvas makes this the gravitational center of any page

### Ghost Outline Button
**Role:** Secondary or tertiary action on dark backgrounds
- Background: transparent
- Border: 1px solid `#ededf3` Ivory
- Text: `#ededf3` Ivory, 16px arcadia weight 400
- Border-radius: 40px (pill)
- Padding: 0px vertical, 20px horizontal
- Used for navigation links and secondary CTAs

### Navigation Pill Link
**Role:** Top-bar navigation items with optional dropdown caret
- Background: transparent
- No border
- Text: `#ededf3` Ivory, 16px arcadia weight 400
- Border-radius: 40px
- Padding: 0px vertical, 20px horizontal
- Floats over hero image, transitions to solid dark fill on scroll via backdrop-blur

### Graphite Card
**Role:** Content grouping surface — product features, feature blocks, section containers
- Background: `#1e1e2a` Graphite
- Border-radius: 12px
- Padding: 32px all sides
- No shadow, no border
- Separation through value contrast alone — the one-step lift from `#171721` canvas

### Email Capture Input (Pill, Left-Half)
**Role:** Hero email input with attached submit button
- Background: transparent
- Border: 1px solid `#ededf3` Ivory on left + top + bottom only
- Text: `#ededf3` Ivory, 16px arcadia weight 400
- Placeholder: `#c3c3cc` Ash
- Border-radius: 32px 0px 0px 32px (left-side pill, flat right edge)
- Padding: 14px vertical, 20px left padding

### Full-Bleed Hero Section
**Role:** Above-the-fold brand statement with photographic atmosphere
- 100vw x ~100vh, centered content stack
- Headline: 65px arcadiaDisplay weight 480, line-height 1.1, `#ffffff`
- Subtext: 18px arcadia weight 480, `#ededf3` Ivory, centered, max-width 520px
- Full-bleed photographic background with subtle dark overlay
- Content max-width ~640px centered vertically and horizontally

### Transparent Top Navigation Bar
**Role:** Primary site navigation overlaid on hero
- Full-width, fixed/sticky, transparent over hero
- Brand mark left, nav links centered (Products, Solutions, Resources, About, Pricing)
- "Log in" text link and Cobalt "Open account" pill button on the right
- Uses `backdrop-blur(8px–20px)` on scroll for frosted-glass separation

### Disclaimer Banner
**Role:** Legal/regulatory footnote strip at page bottom
- Dark background (matches canvas or slightly lighter)
- 12px arcadia weight 480, 0.01em letter-spacing
- Ivory or Ash text color
- Minimal visual weight — present but never distracting

### Section Container
**Role:** Horizontal content wrapper between hero and footer
- Full-width dark canvas (`#171721`)
- Inner content constrained to 1200px max-width
- 72px vertical padding
- Contains 2- or 3-column grids of Graphite Cards or text+image splits

## 5. Layout Principles

### Spacing System
- **Base unit:** 4px
- **Density:** spacious
- **Page max-width:** 1200px
- **Section gap:** 72px
- **Card padding:** 32px
- **Element gap:** 12px

### Spacing Scale
| Name | Value | Token |
|------|-------|-------|
| 4 | 4px | `--spacing-4` |
| 8 | 8px | `--spacing-8` |
| 12 | 12px | `--spacing-12` |
| 16 | 16px | `--spacing-16` |
| 20 | 20px | `--spacing-20` |
| 24 | 24px | `--spacing-24` |
| 32 | 32px | `--spacing-32` |
| 40 | 40px | `--spacing-40` |
| 56 | 56px | `--spacing-56` |
| 72 | 72px | `--spacing-72` |
| 112 | 112px | `--spacing-112` |
| 128 | 128px | `--spacing-128` |

### Border Radius
| Element | Value |
|---------|-------|
| nav | 40px |
| tags | 40px |
| cards | 12px |
| inputs | 32px |
| buttons | 32px |
| default | 4px |

### Whitespace Philosophy
- **Dark gallery**: The near-black canvas creates infinite depth. Cards float as lighter islands in the dark.
- **Spacious rhythm**: 72px between sections gives content room to breathe. Mercury is not dense — it's luxurious.
- **Flat separation**: No shadows means every element's position is defined by its value contrast against the canvas.
- **Centered hero**: Single-column centered content with full-bleed photography behind — the only section that breaks the grid.

## 6. Depth & Elevation

Mercury deliberately avoids shadows. All elevation is communicated through value contrast alone:

| Level | Name | Value | Use |
|-------|------|-------|-----|
| 0 | Onyx Canvas | `#171721` | Base background |
| 1 | Graphite Card | `#1e1e2a` | Elevated surface — one step lighter |

The graphite card sits one step lighter than the onyx canvas, creating perceptible separation without any drop shadow. This flat aesthetic keeps the interface feeling modern, digital, and weightless, letting the photographic hero imagery and cobalt accent do the emotional work.

**No shadows. No elevation layers. Just value contrast.**

## 7. Do's and Don'ts

### Do
- Use Cobalt `#5266eb` exclusively for the single primary action per page — never as a decorative accent, icon fill, or secondary button
- Set all cards to `#1e1e2a` with 12px radius and 32px padding — rely on the one-step value lift from the canvas, not shadows, for separation
- Apply arcadiaDisplay weight 480 (not 600/700) for all headings — the intermediate weight is Mercury's signature restraint
- Use 32px or 40px pill radius for all interactive controls (buttons, inputs, nav items) — sharp 4px corners are reserved for structural elements only
- Set body text at 16px arcadia weight 400 with 1.5 line-height — this is the density baseline for all content
- Maintain 72px vertical rhythm between major sections — spacious density is part of the premium feel
- Use ivory `#ededf3` on ghost/outline buttons for both border and text — never use a chromatic color for secondary actions

### Don't
- Do not use multiple bright accent colors — Cobalt is the only chromatic note; introducing greens, reds, or oranges breaks the monochrome discipline
- Do not add drop shadows to cards or components — separation comes from the graphite-on-onyx value difference alone
- Do not use bold weights (700+) for headings — arcadiaDisplay at 480 is the ceiling
- Do not use sharp corners (0–4px) on buttons, inputs, or nav items — the pill shape is non-negotiable
- Do not use `#ffffff` for body text — always `#ededf3` Ivory; pure white on dark creates harsh, cold contrast
- Do not place Cobalt-filled elements next to each other without at least 32px gap — the vivid color creates visual competition when clustered
- Do not use bright or saturated backgrounds for sections — every surface is either `#171721` (canvas) or `#1e1e2a` (card); no mid-gray or colored bands

## 8. Responsive Behavior

### Breakpoints
| Name | Width | Key Changes |
|------|-------|-------------|
| Mobile | <768px | Single column, reduced padding, stacked hero |
| Tablet | 768–1024px | 2-column grids, maintain pill shapes |
| Desktop | 1024px+ | Full 1200px layout, 3-column card grids |

### Collapsing Strategy
- Hero: full-bleed becomes centered stack with reduced headline (65px → 42px)
- Navigation: transparent top bar becomes hamburger on mobile
- Feature cards: 3-column → 2-column → single column stacked
- Section spacing: 72px → 48px on mobile
- Card padding: 32px → 24px on mobile

## 9. Agent Prompt Guide

### Quick Color Reference
- Background (canvas): `#171721` Onyx
- Card surface: `#1e1e2a` Graphite
- Primary text: `#ededf3` Ivory
- Muted text: `#c3c3cc` Ash
- Border: `#e2e3ed` Mist
- Primary action: `#5266eb` Cobalt (filled action)

### Example Component Prompts

1. "Create a product feature card: background #1e1e2a Graphite, 12px border-radius, 32px padding all sides, no shadow. Heading at 28px arcadiaDisplay weight 480, letter-spacing 0.015em, color #ededf3 Ivory. Body text at 16px arcadia weight 400, line-height 1.5, color #ededf3 Ivory."

2. "Create a primary CTA button: background #5266eb Cobalt, white text at 16px arcadia weight 400, 32px border-radius (pill), no border, no shadow, 12px vertical / 24px horizontal padding. Text is 'Open account' or equivalent action label."

3. "Create a ghost/outline button: transparent background, 1px solid #ededf3 Ivory border, #ededf3 text at 16px arcadia weight 400, 40px border-radius, 10px vertical / 20px horizontal padding."

4. "Create a hero section: full-bleed (100vw), full-viewport height, photographic landscape background with dark overlay. Headline at 65px arcadiaDisplay weight 480, line-height 1.1, color #ffffff, centered. Subtext at 18px arcadia weight 480, color #ededf3 Ivory, centered, max-width 520px."

5. "Create an inline email capture form: flex row, no gap. Input — transparent background, 1px solid #ededf3 Ivory border (left + top + bottom only), #ededf3 text at 16px arcadia weight 400, placeholder in #c3c3cc Ash, border-radius 32px 0 0 32px, 14px vertical / 20px horizontal padding. Button — #5266eb Cobalt fill, white text at 16px arcadia weight 400, border-radius 0 32px 32px 0, 14px vertical / 24px horizontal padding, no border."

### CSS Custom Properties

```css
:root {
  /* Colors */
  --color-onyx-canvas: #171721;
  --color-graphite-card: #1e1e2a;
  --color-obsidian-button: #272735;
  --color-slate-border: #70707d;
  --color-mist-border: #e2e3ed;
  --color-ash-text: #c3c3cc;
  --color-ivory-text: #ededf3;
  --color-cobalt: #5266eb;
  --color-pure-white: #ffffff;

  /* Typography — Font Families */
  --font-arcadia: 'Inter', ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --font-arcadiadisplay: 'Space Grotesk', ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;

  /* Typography — Scale */
  --text-caption: 12px;
  --leading-caption: 1;
  --tracking-caption: 0.12px;
  --text-body-sm: 14px;
  --leading-body-sm: 1;
  --tracking-body-sm: 0.07px;
  --text-body: 16px;
  --leading-body: 1.5;
  --text-body-lg: 18px;
  --leading-body-lg: 1.35;
  --text-subheading: 21px;
  --leading-subheading: 1.35;
  --text-heading-sm: 28px;
  --leading-heading-sm: 1.2;
  --tracking-heading-sm: 0.42px;
  --text-heading: 32px;
  --leading-heading: 1.15;
  --tracking-heading: 0.48px;
  --text-heading-lg: 42px;
  --leading-heading-lg: 1.15;
  --tracking-heading-lg: 0.42px;
  --text-display: 65px;
  --leading-display: 1.1;

  /* Typography — Weights */
  --font-weight-w360: 360;
  --font-weight-regular: 400;
  --font-weight-w420: 420;
  --font-weight-w480: 480;
  --font-weight-w530: 530;

  /* Spacing */
  --spacing-unit: 4px;
  --spacing-4: 4px;
  --spacing-8: 8px;
  --spacing-12: 12px;
  --spacing-16: 16px;
  --spacing-20: 20px;
  --spacing-24: 24px;
  --spacing-32: 32px;
  --spacing-40: 40px;
  --spacing-56: 56px;
  --spacing-72: 72px;
  --spacing-112: 112px;
  --spacing-128: 128px;

  /* Layout */
  --page-max-width: 1200px;
  --section-gap: 72px;
  --card-padding: 32px;
  --element-gap: 12px;

  /* Border Radius */
  --radius-nav: 40px;
  --radius-tags: 40px;
  --radius-cards: 12px;
  --radius-inputs: 32px;
  --radius-buttons: 32px;
  --radius-default: 4px;

  /* Surfaces */
  --surface-onyx-canvas: #171721;
  --surface-graphite-card: #1e1e2a;
  --surface-obsidian-button: #272735;
}
```

### Tailwind v4

```css
@theme {
  --color-onyx-canvas: #171721;
  --color-graphite-card: #1e1e2a;
  --color-obsidian-button: #272735;
  --color-slate-border: #70707d;
  --color-mist-border: #e2e3ed;
  --color-ash-text: #c3c3cc;
  --color-ivory-text: #ededf3;
  --color-cobalt: #5266eb;
  --color-pure-white: #ffffff;

  --font-arcadia: 'Inter', ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --font-arcadiadisplay: 'Space Grotesk', ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;

  --text-caption: 12px;
  --leading-caption: 1;
  --tracking-caption: 0.12px;
  --text-body-sm: 14px;
  --leading-body-sm: 1;
  --tracking-body-sm: 0.07px;
  --text-body: 16px;
  --leading-body: 1.5;
  --text-body-lg: 18px;
  --leading-body-lg: 1.35;
  --text-subheading: 21px;
  --leading-subheading: 1.35;
  --text-heading-sm: 28px;
  --leading-heading-sm: 1.2;
  --tracking-heading-sm: 0.42px;
  --text-heading: 32px;
  --leading-heading: 1.15;
  --tracking-heading: 0.48px;
  --text-heading-lg: 42px;
  --leading-heading-lg: 1.15;
  --tracking-heading-lg: 0.42px;
  --text-display: 65px;
  --leading-display: 1.1;

  --spacing-4: 4px;
  --spacing-8: 8px;
  --spacing-12: 12px;
  --spacing-16: 16px;
  --spacing-20: 20px;
  --spacing-24: 24px;
  --spacing-32: 32px;
  --spacing-40: 40px;
  --spacing-56: 56px;
  --spacing-72: 72px;
  --spacing-112: 112px;
  --spacing-128: 128px;

  --radius-md: 4px;
  --radius-lg: 8px;
  --radius-xl: 12px;
  --radius-3xl: 32px;
  --radius-3xl-2: 40px;
}
```
