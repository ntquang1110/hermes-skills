# User Design System — Premium Dashboard (Black / White / Yellow)

**Source:** User-provided `design.md` on 2026-07-12. This is the authoritative style reference for all web projects for this user.

## Philosophy

- Premium · Minimal · Modern · High Contrast · Soft Rounded · Functional · Spacious · Focus Driven
- 1 Primary Action, 2-3 Secondary Actions, 1 main data zone per screen
- **Rule: "Nếu phải lựa chọn giữa 'đẹp hơn' và 'dễ dùng hơn', luôn ưu tiên 'dễ dùng hơn'"**

## Color System

| Token | Value | Usage |
|-------|-------|-------|
| `--yellow` | `#FFD600` | CTA, Active, Highlight, Progress, Important numbers |
| `--bg` (dark) | `#0D0D0D` | Background |
| `--surface` (dark) | `#1B1B1D` | Card/container surface |
| `--text-primary` | `#FFFFFF` (dark) / `#111111` (light) | Main text |
| `--text-secondary` | `#8B8B8B` | Labels, secondary info |
| `--text-disabled` | `#BDBDBD` | Disabled state |
| `--border` (dark) | `rgba(255,255,255,.05)` | Card borders (dark mode: NO shadow, use border) |
| `--success` | `#44C767` | Positive status |
| `--warning` | `#FFB800` | Warning |
| `--danger` | `#FF4B4B` | Error/danger |

## Typography

| Level | Size | Weight | Line-Height |
|-------|------|--------|-------------|
| H1 | 32px | 700 | 40px |
| H2 | 24px | 600 | — |
| Body | 16px | 400–500 | — |
| Caption | 12px | 400 | — |

All sub-labels use Caption.

## Layout — 8pt Grid System

**Allowed spacing:** 4, 8, 12, 16, 24, 32, 40, 48, 64 — no random spacing.

| Context | Value |
|---------|-------|
| Safe area top | 24 |
| Safe area bottom | 32 |
| Safe area horizontal | 20–24 |
| Card padding | 24 |
| Card gap | 16 |
| Section spacing | 24 or 32 |
| Button padding X | 24 |

## Border Radius

| Component | Radius |
|-----------|--------|
| Card | 28 |
| Button | 999 (pill) |
| Chip | 999 |
| Input | 18 |
| Small Icon bg | 16 |

Every component has rounded corners. No sharp corners.

## Cards

- Max 3 levels of information: Title → Value → CTA (never more)
- ✅ Title, Value, CTA
- ❌ Title, Subtitle, Description, Progress, Chart, Button, Footer

## Buttons

| Type | Style | Height | Radius |
|------|-------|--------|--------|
| Primary | Yellow bg (#FFD600) + Black text | 56 | 999 |
| Secondary | White bg + no border | 56 | 999 |
| Ghost | Transparent | 56 | 999 |

- Icon button: Circle, 48×48

## Icons

- Outlined style only (FILL=0 in Material Symbols)
- Size: 20 or 24px
- Never mix outlined and fill icons
- Use `Material Symbols Outlined` from Google Fonts

## Shadows / Borders

| Mode | Style |
|------|-------|
| Light | `0 8 20 rgba(0,0,0,.08)` — very subtle |
| Dark | **NO shadow** — use `border: rgba(255,255,255,.05)` |

## Animation

- Duration: 200ms
- Easing: `ease-out`
- No animation longer than 200ms

## Accessibility

- Minimum touch area: 48×48px
- Contrast ratio ≥ 4.5:1
- Never use color alone to convey meaning — always pair with icon or text

## Data Hierarchy

Always: **Heading → Primary Number → Secondary Info → Action**
Never reverse this order.

## Chart Hierarchy

**Value → Trend → Chart** — chart must never be more prominent than the number.

## UX Rules

1. **One Hero per screen** — one standout number/element, everything else smaller
2. **Only one Primary CTA per section** — never two yellow buttons in the same area
3. **Reading order:** Top → Left → Center → Bottom
4. **One purpose per card** — Sales card doesn't contain Chart + Form + Notification
5. **Reduce cognitive load** — if you can remove a border, icon, or label, do it

## Navigation

- Top AppBar: Title + Back + max 2 actions
- Bottom nav (if present): max 5 tabs — Home, Dashboard, Analytics, Profile

## Responsive Breakpoints

| Device | Min width |
|--------|-----------|
| Mobile | 360+ |
| Tablet | 768+ |
| Desktop | 1280+ |

Don't scale everything — only increase whitespace.

## Developer Checklist (from design.md §19)

- [ ] 8pt grid used
- [ ] Only token colors used (no hardcoded colors)
- [ ] No hardcoded spacing
- [ ] Correct border radius per component spec
- [ ] Button height = 56px
- [ ] Touch target ≥ 48px
- [ ] Contrast meets WCAG
- [ ] Typography follows scale
- [ ] 1 Primary CTA per section
- [ ] Section spacing ≥ 24px
- [ ] Card serves 1 purpose
- [ ] Icons consistent style (all outlined)
- [ ] Animation ≤ 200ms
- [ ] Dark mode uses same tokens
