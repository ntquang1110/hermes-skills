---
name: design-template-selector
description: "Use when publishing HTML. Gallery->pick theme->apply tokens."
version: 1.0.0
author: Hermes Agent
license: MIT
tags: [design, template, gallery, selector, workflow]
platforms: [linux, macos, windows]
triggers:
  - publish
  - create html
  - build a page
  - design a page
  - tao html
  - tao trang
  - publish html
  - chon design
  - chon theme
---

# Design Template Selector

## Workflow

When the user wants to create/publish any HTML page, follow this workflow:

### Step 1: Show Gallery

Publish the gallery page so the user can browse designs. Load the gallery HTML from the popular-web-designs skill:

```
skill_view(name="popular-web-designs", file_path="templates/design-gallery.html")
```

Publish it, then send the link and ask: **"Anh chọn theme nào?"**

### Step 2: Load Selected Design

Once user picks a theme name, load the template:

```
skill_view(name="popular-web-designs", file_path="templates/<theme-name>.md")
```

### Step 3: Build with Design Tokens

Use the template's tokens when building:
1. Set CSS custom properties from the template
2. Apply font CDN substitutes from Hermes notes
3. Follow component specs for buttons, cards, nav, hero
4. Apply Do's and Don'ts

### Step 4: Verify

Write with `write_file`, publish with `publish` skill, verify with `browser_vision`.

## Available Themes

### Fintech & Crypto
| Theme Name | Site | Style |
|---|---|---|
| `mercury` | Mercury | Alpine banking, near-black canvas, cobalt accent |
| `slash` | Slash | Midnight vault, didone serif, copper accent |
| `slush` | Slush | Inflatable sticker universe, 6-color palette |

### Editorial & Creative
| Theme Name | Site | Style |
|---|---|---|
| `monad` | Monad | Editorial tech journal, mono body + serif display |
| `general-intelligence` | G.I. Company | Literary journal, serif headlines |
| `gsap` | GSAP | Dark chalkboard, 224px display |
| `monopo-saigon` | Monopo Saigon | 225px display, 75px pills |
| `oryzo-ai` | ORYZO AI | Darkroom product editorial |
| `say-briefly` | Say Briefly | Creative sketchbook, forest green |
| `duolingo` | Duolingo | Playful classroom, green accent |

### AI & Developer Tools
| Theme Name | Site | Style |
|---|---|---|
| `modal` | Modal | Phosphor terminal, green-on-black |

Plus 54 more existing designs in `popular-web-designs` skill.

## Design Token Patterns

Every template follows this structure:
1. Hermes Implementation Notes (font CDN substitutes)
2. Color Palette (hex values with roles)
3. Typography (faces, weights, scale)
4. Spacing & Shape (base unit, gaps, radius)
5. Key Rules (Do's and Don'ts)

## Publishing Gallery

Gallery at `templates/design-gallery.html` inside `popular-web-designs` skill.
Use `publish` skill to deploy it.
