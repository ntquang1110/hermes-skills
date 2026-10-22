---
name: neumor-design
description: "Neumorphism Soft UI — Cool Grey, dual RGBA shadows, depth."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows, web]
metadata:
  hermes:
    tags: [design, neumorphism, soft-ui, ui, css, design-system]
    related_skills: [claude-design, popular-web-designs, html-unslop]
---

# Neumorphism (Soft UI) Design System

## Design Philosophy

Core Principles: Neumorphism creates the illusion of physical depth through carefully balanced dual shadows — one light source from the top-left, one dark shadow falling bottom-right — on monochromatic backgrounds. Elements appear to either extrude from the surface (convex/raised) or be pressed into it (concave/inset). The effect mimics soft, pillowed physical objects with realistic lighting, creating a "molded from the same material" aesthetic. Every element feels like it's part of the same continuous surface, either raised or pressed, never flat.

Vibe: Tactile, calm, modern, and physically grounded. This is UI that feels like cooler matte plastic or soft ceramic. It is satisfying and tangible. The aesthetic is deliberately restrained, utilizing a cooler grey palette to feel fresh and distinct from "warm" legacy neumorphism. The design prioritizes accessibility with WCAG AA compliant contrast ratios while maintaining the soft aesthetic.

## Visual Signatures

- Dual opposing RGB shadows (top-left light, bottom-right dark) using alpha transparency for smoother, more realistic blending than solid hex shadows.
- Monochromatic "Cool Grey" discipline (#E0E5EC) where shadows and highlights do all the visual heavy lifting. No flat backgrounds.
- Same-surface illusion: Elements appear to be part of the same material as the background — molded, not placed.
- Deep Inset States: Wells for icons and inputs that feel significantly deeper (insetDeep) than standard pressed states, creating true 3D depth.
- Soft, Hyper-Rounded Corners: 32px for containers and 16px for smaller elements, reinforcing the pillowed, organic aesthetic.
- Complex Nested Depth: Visuals formed by nesting elements (Extruded → Inset → Extruded) to showcase the physics of the system.
- Smooth Micro-interactions: 300ms transitions with translateY, shadow depth changes, and nested circle rotation. Floating animations for ambient motion.
- Mobile-First Responsive: Fully responsive with touch-friendly targets (44px minimum) and maintained neumorphic aesthetic on all screen sizes.

## Anti-Patterns (Do Not Do)

- Hard Hex Shadows: Do not use opaque hex codes for shadows (e.g., #A3B1C6). Use `rgb(... 0.6)` for transparency and blending.
- White Backgrounds: Never use `bg-white` for cards. They must match the body background `#E0E5EC`.
- Flat Buttons: Buttons must have depth (shadows). No flat designs.
- Sharp Corners: `rounded-lg` is too sharp. Use `rounded-2xl` (16px) or `rounded-3xl` (24px) minimum.
- Poor Contrast: Never use `#8B95A5` or `#A0AEC0` for body text. Use `#6B7280` or darker for WCAG compliance.
- Missing Focus States: All interactive elements must have visible focus indicators.
- Block Display for Fonts: Use `display=swap` in Google Fonts URL, not `display=block`.

## Design Token System (The DNA)

### Colors (Light Mode - Cool Monochromatic)

| Token | Value | Usage |
|-------|-------|-------|
| Background | `#E0E5EC` | The base "cool clay" surface. Everything is molded from this. |
| Foreground | `#3D4852` | Dark blue-grey for primary text. 7.5:1 contrast (WCAG AAA). |
| Muted | `#6B7280` | Cool grey for secondary text. 4.6:1 contrast (WCAG AA). |
| Accent | `#6C63FF` | Soft violet for interactive highlights. Used sparingly for CTAs and focus states. |
| Accent Light | `#8B84FF` | Lighter violet for gradients and hover states. |
| Accent Secondary | `#38B2AC` | Teal for success states, checkmarks, and positive indicators. |
| Border | transparent | Neumorphism never uses borders; shadows define all edges. |
| Muted Light | `#A0AEC0` | Placeholder text color. |

**Shadow Colors (CRITICAL - RGBA for Smoothness):**
- Shadow Light: `rgba(255, 255, 255, 0.5-0.6)` — top-left light source.
- Shadow Dark: `rgb(163, 177, 198, 0.6-0.7)` — bottom-right dark shadow.

### Typography

- **Display Font:** "Plus Jakarta Sans" (500, 600, 700, 800) for headlines.
- **Body Font:** "DM Sans" (400, 500, 700) for all body text and UI elements.
- **Weights:** Display headings 800 with letter-spacing -0.02em. Headings 700. Body 400-500.
- **Colors:** Primary `#3D4852`, Muted `#6B7280`.

### Radius

| Level | Value |
|-------|-------|
| Container / Card | `32px` |
| Base / Button | `16px` |
| Inner Elements | `16px` |
| Pill / Tag | `9999px` |

### Shadow System

All shadows use rgba for smooth blending. Never use hard hex shadow colors.

| Name | Value |
|------|-------|
| Extruded | `9px 9px 16px rgb(163,177,198,0.6), -9px -9px 16px rgba(255,255,255,0.5)` |
| Extruded Hover | `12px 12px 20px rgb(163,177,198,0.7), -12px -12px 20px rgba(255,255,255,0.6)` |
| Extruded Small | `5px 5px 10px rgb(163,177,198,0.6), -5px -5px 10px rgba(255,255,255,0.5)` |
| Inset (Pressed) | `inset 6px 6px 10px rgb(163,177,198,0.6), inset -6px -6px 10px rgba(255,255,255,0.5)` |
| Inset Deep | `inset 10px 10px 20px rgb(163,177,198,0.7), inset -10px -10px 20px rgba(255,255,255,0.6)` |
| Inset Small | `inset 3px 3px 6px rgb(163,177,198,0.6), inset -3px -3px 6px rgba(255,255,255,0.5)` |

## Component Styling

### Tab Bar
- Background `#E0E5EC`, inset shadow. Tabs: transparent default, extruded when active.
- Min height 44px. Focus-visible: 2px accent ring.

### Buttons
- `border-radius: 16px`, min height 48px.
- Default: Extruded Small. Hover: `translateY(-1px)` + Extruded Hover. Active: `translateY(0.5px)` + Inset Small.
- Primary: Background `#6C63FF`, white text.

### Cards
- `border-radius: 32px`, background `#E0E5EC`.
- Default: Extruded. Hover: `translateY(-2px)` + Extruded Hover.
- Feature: Nested depth (Extruded → Inset Deep → Extruded).

### Inputs
- `border-radius: 16px`, background `#E0E5EC`.
- Default: Inset. Focus: Inset Deep + accent ring (2px offset).

### Tables
- Wrapped in inset well (16px radius). Cells separated by subtle border.

### Pills / Tags
- Inset Small shadow, `border-radius: 9999px`. Tinted backgrounds at 0.12 opacity.

## Nested Depth Pattern

```
Extruded (outer container)
  └── Inset (mid layer)
       └── Extruded (inner core)
```

Used for decorative elements, mechanism flow containers, and card icon wells.

## Animation

| Element | Duration | Properties |
|---------|----------|------------|
| UI elements | 300ms ease-out | box-shadow, transform |
| Nested circles | 500ms ease-out | scale(1.05), rotate(180deg) |
| Floating decoration | 3s ease-in-out infinite | translateY(0 to -6px) |

## Accessibility

- Primary text #3D4852 on #E0E5EC: 7.5:1 (WCAG AAA)
- Muted text #6B7280 on #E0E5EC: 4.6:1 (WCAG AA)
- Focus: 2px accent ring + 2px offset on ALL interactive elements
- Touch targets: min 44px

## CSS Variables

```css
:root {
  --bg: #E0E5EC;
  --fg: #3D4852;
  --muted: #6B7280;
  --muted-light: #A0AEC0;
  --accent: #6C63FF;
  --accent-light: #8B84FF;
  --accent-secondary: #38B2AC;
  --shadow-light: rgba(255,255,255,0.55);
  --shadow-dark: rgb(163,177,198,0.65);
  --shadow-dark-hover: rgb(163,177,198,0.75);
  --shadow-light-hover: rgba(255,255,255,0.65);
  --radius-container: 32px;
  --radius-base: 16px;
  --radius-inner: 16px;
  --radius-full: 9999px;
  --transition: 300ms cubic-bezier(0.34, 1.56, 0.64, 1);
}
```

## Implementation Checklist

1. Body background `#E0E5EC`
2. Load Plus Jakarta Sans + DM Sans with `display=swap`
3. Define all CSS variables
4. Define all 6 shadow classes
5. `:focus-visible` on ALL interactive
6. min-height 44-48px on interactive
7. translateY (NOT scale) for hover/active
8. 32px containers, 16px minimum everywhere
9. `rgb()` with alpha for ALL shadows
10. No `bg-white`
11. Floating animation for decoration
12. Nested depth in at least one section
