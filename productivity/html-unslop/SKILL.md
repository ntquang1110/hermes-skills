---
name: html-unslop
description: "Strip AI-isms from generated HTML designs — humanize text content, soften AI color palettes, add character to CSS, remove generic patterns. Makes AI-generated HTML look hand-crafted by a real designer."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [html, design, humanize, ai-detection, css, anti-slop]
    related_skills: [content-publish, field-map, md-publish]
---

# HTML Unslop (html-unslop)

Làm HTML "hết AI" — cả nội dung lẫn CSS/design.

## When to Use

- Sau khi agent generate HTML design → muốn output trông chân thực, không generic
- HTML có text chứa AI-isms ("delve", "testament", "leveraging", ...)
- CSS dùng color palette AI-signature (dark blue #0f172a, accent #38bdf8, ...)
- Layout quá hoàn hảo, thiếu "cá tính"
- Muốn publish HTML mà không bị nhận ra là AI tạo

**Không dùng cho:**
- HTML đã được humanize sẵn
- Code thuần (PHP, JS, Python) — unslop chỉ xử lý HTML text + CSS
- Khi cần giữ nguyên AI style vì lý do thương hiệu

## What It Fixes

### Text AI-isms (từ unslop project)
| Loại | Ví dụ | Thay bằng |
|------|-------|-----------|
| Từ cấm | delve, tapestry, paradigm | explore, mix, model |
| Cụm AI | dive into, unlock the power of, great question! | explore, bỏ, (không nói) |
| Marketing speak | empower, revolutionize, streamline | help, change, simplify |
| Over-perfect | overall, in conclusion | bỏ hoặc "so" |

### CSS Design Tells
| Tell | Mô tả | Fix |
|------|-------|-----|
| Color palette AI-signature | `#0f172a`, `#38bdf8`, `#e2e8f0` | Warm hơn: `#1a1a2e`, `#4a9eff`, `#e8e0d8` |
| Font stack AI | `'Inter', system-ui, -apple-system` | `system-ui, 'Segoe UI', Roboto` |
| Perfect border-radius | all `8px`, `12px`, `14px` uniform | Vary ±1-3px |
| Over-perfect grid | `repeat(auto-fit, minmax(...))` | Giữ nhưng thêm spacing quirks |
| Card pattern | `rgba(255,255,255,0.03)` + `border-radius` | Giảm uniformity |
| Generic blur | `backdrop-filter: blur()` | Giữ nếu cần, bỏ decoration thừa |
| Comment | Không có human comment | Thêm comment "mộc" ngẫu nhiên |

## Usage

### CLI

```bash
# Scan HTML for AI tells
python scripts/unslop-html.py --file input.html --check

# Fix + output file
python scripts/unslop-html.py --file input.html --output output.html

# Fix + publish trực tiếp
python scripts/unslop-html.py --file input.html --publish --title "My Page"

# Pipe
cat generated.html | python scripts/unslop-html.py > human.html
```

### Trong Agent Flow

```python
from hermes_tools import terminal

# Generate HTML → unslop → publish
terminal('python scripts/unslop-html.py --file design.html --publish --title "Design"')
```

## Script

- `scripts/unslop-html.py` — main processor (scan + fix + publish)

## Common Pitfalls

1. **Không over-humanize.** Giữ lại technical precision. Chỉ thay AI-isms thực sự.
2. **Color thay đổi có thể phá design.** Kiểm tra visual sau khi chạy. Có thể skip color replace nếu cần.
3. **Comment thêm vào có thể outdated.** Dùng comment chung chung, không hardcode chi tiết.
4. **Chạy --check trước** để biết mức độ AI trước khi quyết định có unslop hay không.
5. **Nội dung tiếng Việt** — AI-isms tiếng Việt khác tiếng Anh. Xem section "Vietnamese AI-isms" bên dưới để biết pattern cần thay.

## Vietnamese AI-isms (Knowledge Flow adaptation)

### Text tells (thay thế khi unslop card content)

| AI-ism | Thay bằng |
|--------|-----------|
| "đi sâu vào", "đào sâu" | "tìm hiểu", "phân tích" |
| "mở ra cánh cửa" | "giúp", "cho phép" |
| "không thể phủ nhận" | bỏ |
| "một trong những... nhất" | "là" |
| "đóng vai trò quan trọng" | "là", "quyết định" |
| "có thể thấy rằng" | bỏ |
| "tuy nhiên" | "Nhưng" |
| "bên cạnh đó" | "Ngoài ra" |
| "nhìn chung", "tóm lại" | bỏ, kết luận cụ thể |
| "được coi là" | "là" |
| "cụ thể là" | bỏ, dùng ":" |
| "có nghĩa là" | "— tức là" |

### CSS tells for dark dashboard (Knowledge Flow specific)

- **Nền**: `#0D0D0D` → `#0f0f0f` (AI-signature pure black)
- **Surface**: `#1B1B1D` → `#1a1a1e` (slightly muted)
- **Accent dim**: `rgba(255,214,0,0.15)` → `rgba(255,214,0,0.12)`
- **Text secondary**: `#8B8B8B` → `#888` (số lẻ bớt "thiết kế")
- **Font body**: dùng `system-ui` đầu tiên, bỏ `'Inter'` khỏi vị trí ưu tiên
- **Comment**: thay "Design System v1.0 — Premium Dashboard" bằng "tối màu + vàng, cap nhat linh tinh :v"
- **Border-radius**: tránh dãy hoàn hảo `4px 8px 12px 16px` → `7px 11px 14px 24px`
- **Transition**: `all 0.2s` → `border-color 0.15s ease`, `opacity 0.12s`
- **Surface border**: `rgba(255,255,255,0.08)` → `rgba(255,255,255,0.06)`

## React / Next.js App Adaptation

When unslopping a **React/Next.js app** (not standalone HTML), the technique differs from running the CLI script:

### What to target

| Target | What to change | Example |
|--------|---------------|---------|
| **CSS variables** in `globals.css` | Round values to slightly non-perfect numbers. Soften pure `#000`/`#fff`. | `#0D0D0D` → `#0f0f0f`, `#1B1B1D` → `#1a1a1e`, `#8B8B8B` → `#888` |
| **Font stack** in `@theme` | Move away from pure `'Inter', system-ui`. Use `system-ui` first, drop `-apple-system`. | `'Inter', -apple-system, sans-serif` → `system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif` |
| **Border-radius** | Avoid perfectly ascending values (`4px, 8px, 12px, 16px`). Pick slightly odd values. | `8px` → `7px`, `10px` → `11px`, `12px` → `14px` |
| **Transitions** | Vary `all 0.2s` to specific properties with different timing. | `all 0.2s` → `border-color 0.15s ease`, `opacity 0.12s` |
| **Border patterns** | AI loves `rgba(255,255,255,0.08)` or `rgba(255,255,255,0.03)`. Vary opacity and surface color. | `rgba(255,255,255,0.08)` → `rgba(255,255,255,0.06)`, background `#242424` → `#1a1a1e` |
| **Color variables names** | AI groups them neatly (`--color-*`). Keep but add human-sounding comment. | `/* Design System v1.0 */` → `/* cap nhat linh tinh, khong theo design system nao :v */` |
| **Card shadows/effects** | AI-perfect cards use `hover:brightness-110`, `card-surface`, `transition-all`. Reduce uniformity. | `padding: 1rem` → `padding: 1rem 0.75rem` (not symmetrical), `gap: 4px` → `gap: 3px` |

### Component-level patterns to vary

- **Inline `style={{...}}` in JSX**: AI defaults to perfect hex codes. Shift hue slightly or use `#555` instead of `#6C757D`.
- **Button radii**: `rounded-full` is AI's goto. Accept it for pills, but make other radii slightly non-standard.
- **Hover effects**: AI loves `hover:opacity-80` or `hover:brightness-110`. Use `hover:opacity-85` or `hover:border-color` instead.
- **Font sizes**: Instead of perfect step scale (`0.75rem, 0.85rem, 1rem, 1.1rem`), pick slightly irregular: `0.65rem, 0.8rem, 0.95rem, 1.05rem`.

### What NOT to change in React apps

- **Component logic** (useState, useEffect, fetch) — unslop is visual/text only
- **Accessibility attributes** (aria-*, role) — keep them perfect
- **API response contracts** — unslop the display, not the data shape
- **Tailwind utility classes** — change them at the CSS variable level, not per-element

### Deployment pitfall: EADDRINUSE / stale server

After unslopping CSS in a Next.js production app (`next start`), the server often serves the OLD build even after `next build`. Root cause: `process(action='kill')` in Hermes targets the WRONG PID, while the real server stays alive. Always:

1. `netstat -ano | grep ":3003" | grep LISTENING` to find ALL PIDs
2. `taskkill /F /PID $PID` for each
3. `rm -rf .next node_modules/.cache`
4. `npx next build && npx next start --port 3003`

Without this sequence, unslop changes appear compiled but the browser shows stale design.

## Verification Checklist

- [ ] `--check` trả về 0 tells (hoặc chấp nhận được)
- [ ] Text không còn "delve", "testament", "crucial", "seamless"...
- [ ] CSS color palette không còn AI-signature colors
- [ ] Design vẫn đẹp — unslop không phá layout
- [ ] HTML valid (w3c check)
- [ ] Preview URL hoạt động

## Related Skills

- `content-publish` — upload kết quả lên preview.thefirstonly.com
- `field-map` — tạo knowledge map (thường cần unslop sau khi sinh HTML)
- `md-publish` — markdown publishing
