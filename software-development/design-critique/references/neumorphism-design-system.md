# Neumorphism (Soft UI) Design System — Cool Grey

A complete neumorphism design system reference. Use when user requests "neumorphism", "soft UI", or "cool grey" aesthetic.

## Tokens

Background: #E0E5EC, Foreground: #3D4852 (7.5:1), Muted: #6B7280 (4.6:1)
Accent: #6C63FF (violet), Accent Secondary: #38B2AC (teal)

## Shadow System (RGBA only — no hard hex)

Extruded: `9px 9px 16px rgb(163,177,198,0.6), -9px -9px 16px rgba(255,255,255,0.5)`
Extruded Hover: `12px 12px 20px rgb(163,177,198,0.7), -12px -12px 20px rgba(255,255,255,0.6)`
Extruded Small: `5px 5px 10px rgb(163,177,198,0.6), -5px -5px 10px rgba(255,255,255,0.5)`
Inset: `inset 6px 6px 10px rgb(163,177,198,0.6), inset -6px -6px 10px rgba(255,255,255,0.5)`
Inset Deep: `inset 10px 10px 20px rgb(163,177,198,0.7), inset -10px -10px 20px rgba(255,255,255,0.6)`
Inset Small: `inset 3px 3px 6px rgb(163,177,198,0.6), inset -3px -3px 6px rgba(255,255,255,0.5)`

## Radius

Container 32px, Base/Button 16px, Inner 16px min, Pills 9999px

## Typography

Display: Plus Jakarta Sans (500-800), Body: DM Sans (400, 500, 700)

## Interactions

Buttons: translateY(-1px) hover / translateY(0.5px) active
Cards: translateY(-2px) hover
300ms cubic-bezier(0.34, 1.56, 0.64, 1)

## Anti-Patterns

1. Hard hex shadows — use rgb() with alpha
2. White backgrounds — match #E0E5EC
3. Flat buttons — always shadow depth
4. Sharp corners — minimum 16px radius
5. Poor contrast — never #8B95A5 for body
6. Missing focus states — 2px accent ring on all interactive
7. display=block fonts — use display=swap
