# Design System v1.0 — Premium Dashboard

User's authoritative design spec for all UI work. Every new UI component MUST follow these tokens — no deviations.

## Color tokens
| Token | Hex | Usage |
|-------|-----|-------|
| Dark BG | `#0D0D0D` | Body, page backgrounds |
| Surface | `#1B1B1D` | Cards, sidebars, modals, dropdowns |
| Surface Hover | `#252529` | Card hover state |
| Surface Light | `#2A2A2E` | Subtle dividers, code blocks |
| Accent Yellow | `#FFD600` | Primary CTA, highlights, active states, progress bars |
| Accent Dim | `rgba(255, 214, 0, 0.15)` | Badge backgrounds, active tab backgrounds |
| Accent Glow | `rgba(255, 214, 0, 0.08)` | Subtle halo effects |
| Text Primary | `#FFFFFF` | Headings, body text |
| Text Secondary | `#8B8B8B` | Descriptions, meta data |
| Text Tertiary | `#5C5C5E` | Placeholders, timestamps, disabled |
| Border | `#2A2A2E` | Dividers, card borders |
| Danger | `#FF4444` | Error states, destructive actions |
| Success | `#44CC88` | Success states, completion |

## Spacing (8pt grid)
| Token | Value |
|-------|-------|
| Space 1 | 8px |
| Space 2 | 16px |
| Space 3 | 24px |
| Space 4 | 32px |
| Space 5 | 40px |
| Space 6 | 48px |

## Radius
| Token | Value |
|-------|-------|
| Card radius | 28px |
| Button radius | 999px (pill) |
| Small radius | 8px |
| Medium radius | 16px |
| XLarge radius | 40px |

## Button
| Property | Value |
|----------|-------|
| Height | 56px |
| Border radius | 999px |
| Primary | Yellow bg #FFD600, text black |
| Secondary | Border + transparent bg |

## Typography
| Role | Font | Size | Weight |
|------|------|------|--------|
| Heading | JetBrains Mono | 18-28px | 700 |
| Body | Inter | 13-15px | 400 |
| Small/Meta | Inter | 11-12px | 400-500 |
| Code | JetBrains Mono | 12px | 400 |

## Animation
- Duration: 200ms
- Easing: cubic-bezier(0.16, 1, 0.3, 1)
- Only on: hover, active, enter/exit

## Icons
- Style: Outlined
- Size: 16px (inline), 24px (standalone)

## Application in Tailwind v4
```css
@theme inline {
  --color-bg-dark: #0D0D0D;
  --color-surface: #1B1B1D;
  --color-surface-hover: #252529;
  --color-surface-light: #2A2A2E;
  --color-accent: #FFD600;
  --color-accent-dim: rgba(255, 214, 0, 0.15);
  --color-text-primary: #FFFFFF;
  --color-text-secondary: #8B8B8B;
  --color-text-tertiary: #5C5C5E;
  --color-border: #2A2A2E;
  --color-danger: #FF4444;
  --color-success: #44CC88;
  --font-heading: 'JetBrains Mono', monospace;
  --font-body: 'Inter', -apple-system, sans-serif;
}
```
