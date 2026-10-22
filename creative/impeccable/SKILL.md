---
name: impeccable
description: "Design language cho AI-generated frontend — nâng chất lượng HTML lên mức craft. Trích từ impeccable (pbakaus/impeccable, 54k stars): 4 visitor modes, craft-floor Verify/Refuse checklist, ~25 detector rules deterministic bắt AI-tells, DESIGN.md token template B/W/Y, và 3 lightweight commands (shape → critique → polish). Dùng cho mọi design task: landing, dashboard, research page, HTML artifact. KHÔNG dùng cho backend/non-UI."
version: 1.0.0
author: Hermes Agent
license: Apache 2.0
metadata:
  hermes:
    tags: [design, ui, craft, anti-patterns, checklist, html, frontend, design-system]
    related_skills: [html-publishing, content-publish, html-unslop, design-md, design-critique, dashboard-design-system, claude-design]
---

# Impeccable Design (bản rút gọn cho HTML)

Design language giúp AI tạo frontend **không giống AI**: production-grade, có POV, đúng brand. Nguồn: `pbakaus/impeccable` (Apache-2.0).

## Core Principles

- **Go all out.** Không hedge, không shortcut. Deliverable phải hoàn chỉnh.
- **Brief wins.** Honor brand đã pin (màu, font, palette) — kể cả khi xung đột với pattern thông thường. Đổi brief theo ý mình là fail.
- **Refinement preserves; redesign replaces.** Chỉnh = giữ identity cũ. Redesign = giữ product truth nhưng thay world cũ.
- **Verify in bounded passes, not a loop.** Build → inspect 1 lượt (desktop + mobile) → fix 1 batch → confirm tối đa 1 lượt nữa → dừng. Không tự QA vô hạn.

## Modes (chọn TRƯỚC khi design)

| Mode | Visitor làm gì | Áp dụng cho | Ưu tiên |
|------|---------------|-------------|---------|
| **Persuade** | Quyết định + hành động | Landing, marketing, pricing | Attention & action. Design là sản phẩm. |
| **Operate** | Hoàn thành task | Dashboard, app UI, admin, settings | Scanability, consistency, native expectations. Brand nằm ở chi tiết. |
| **Read** | Hiểu nội dung | Docs, articles, research page | Cấu trúc cho comprehension, rồi làm trải nghiệm đọc đáng ở lại. |
| **Experience** | Ở trong tác phẩm | Portfolio, showcase | Artifact dẫn dắt từ viewport đầu. |

Chọn theo surface, không theo product: tool landing vẫn là Persuade; fashion docs vẫn là Read; research page = Read.

## Craft Floor — VERIFY (check trên kết quả build, không phải ý định)

Chạy tất cả cùng 1 lượt render (desktop + mobile chung):

- [ ] **Contrast:** body/placeholder text ≥ 4.5:1, large text ≥ 3:1. Trên nền màu, tint secondary text từ hue đó hoặc foreground — KHÔNG bao giờ xám.
- [ ] **Depth:** shadow có offset + blur thật. Zero-offset colored halo = decoration, không phải depth.
- [ ] **Spacing:** nhóm chặt, phân cách rộng, nhiều space trên heading hơn dưới. Đọc computed values.
- [ ] **Type:** body measure 65–75ch, display max 6rem, tracking floor -0.04em, scale + weight steps rõ ràng. Chạy copy thật ở mọi breakpoint, fix overflow.
- [ ] **Motion:** 1 authored moment, không rải rác. Ease-out từ trạng thái visible. Có thể dùng blur/backdrop-filter/clip-path/mask nếu mượt.
- [ ] **States:** hover, disabled, loading, error, empty. + real content, working controls, responsive, keyboard focus.
- [ ] **Copy:** ngôn ngữ của product. Control đặt tên hành động; error nêu vấn đề + cách khôi phục.
- [ ] **Coverage:** mọi yêu cầu brief hiện diện, tìm được trong vài giây.

## Craft Floor — REFUSE (pattern AI hay dùng — mặc định cấm, trừ khi brief ghi rõ)

**Page scaffolds:**
- Cards đồng dạng (icon + heading + text) làm cấu trúc trang — cards là container lười; nested cards luôn sai
- Hero-metric template (số to, label nhỏ, supporting stats, accent)
- Eyebrow/kicker trên heading — **ban tuyệt đối**: heading tự nói, xoá label đi
- Số section 01/02/03 trừ khi sequence mang thông tin cần thiết
- Modal cho task không cần focus bảo vệ

**Surface habits:**
- Gradient text — emphasis từ weight/size, không phải gradient
- Glassmorphism/blur trang trí (không phải hiệu ứng cụ thể)
- Colored border-left/right > 1px trên card/list/callout
- Hard offset shadow (4px 4px 0) ngoài world neobrutalist thật
- Sparklines, progress rings, soft-shadowed rounded rect đứng thay content
- Monospace làm "costume technical" (chỉ dùng cho code/data/measurement)
- System display face (Impact, Arial Black) làm display voice — source + self-host face hợp character
- Unicode glyph/emoji thay icon system — icon phải vẽ, 1 stroke + weight nhất quán
- Light/dark chọn theo category — chọn theo use scene: ai, ở đâu, ánh sáng nào

**Codex-level (thêm cho HTML tĩnh):**
- Tracking dừng ở -0.04em (-0.02 đến -0.03 thường đọc tốt hơn)
- Khai báo elevation 1 lần: border HOẶC shadow. 1px border dưới soft shadow = ghost card. Card radius 12–16px; pill chỉ cho control nhỏ
- Illustration thật hoặc không: SVG sketch-style/doodle/feTurbulence grain = amateur. SVG geometry (vector, diagram, animated linework) thì OK
- Background là surface: repeating-linear-gradient stripes + grid overlay cần canvas/map/blueprint thật bên dưới
- Claims/config từ dữ liệu thật; label illustrative values trung thực
- Không animate image khi hover (qua parent cũng vậy) — feedback cho container, không phải image

## Detector Rules — AI-tells phổ biến (check nhanh trước publish)

Các dấu hiệu "AI made this" dễ bắt nhất:

> ⚡ **Tự động hoá:** `scripts/ui-audit.js` — detector chạy trong browser (browser_navigate → browser_console với expression = nội dung file). Trả về JSON: tells (gradient-text, glassmorphism, hard-offset-shadow, emoji-icons, flat-type-hierarchy, overused-font, low-contrast-body...), fonts, radii, headings, bodyContrast. Dùng khi audit nhiều trang — đỡ phải đọc từng rule bằng mắt. Lưu ý: bodyContrast chỉ đo body; text nằm trong card có nền khác thì contrast thực tế khác (thường tốt hơn).

**Workflow audit browser (Camofox):**
1. Start browser TRƯỚC: `cd /d/Hermes Proj/camofox-browser && npm start` (background) → verify `curl http://localhost:9377/health` trả `{"ok":true}`
2. `browser_navigate` tới trang (localhost hoặc qua tunnel)
3. Trang có passcode → `browser_type` + `browser_click` để vào
4. `browser_console` với expression = nội dung scripts/ui-audit.js → đọc JSON
5. Fix 1 batch → verify lại 1 lượt → dừng (bounded passes)

| # | Rule | Dấu hiệu |
|---|------|----------|
| 1 | `gray-on-color` | Text xám trên nền màu |
| 2 | `low-contrast` | Contrast < 4.5:1 |
| 3 | `ai-color-palette` | Tím → xanh gradient, neon trên đen, cyan glow |
| 4 | `gradient-text` | Text gradient |
| 5 | `icon-tile-stack` | Icon tile tròn/vuông trên heading (rounded-square icon tile) |
| 6 | `kicker-above-heading` | Eyebrow/kicker trên mọi heading |
| 7 | `hero-eyebrow-chip` | Chip "Introducing..." trên hero |
| 8 | `hero-metric` | Số to + label nhỏ làm hero |
| 9 | `nested-cards` | Card trong card |
| 10 | `repeated-container-text` | Cùng layout card lặp 3+ lần |
| 11 | `side-tab` | Colored side border/stripe trên item |
| 12 | `dark-glow` / `radial-halo` | Glow halo sau element |
| 13 | `repeating-stripes-gradient` | Stripes gradient nền |
| 14 | `codex-grid-background` | Grid overlay nền không có lý do |
| 15 | `overused-font` | Inter/System font cho mọi thứ (không có display face riêng) |
| 16 | `flat-type-hierarchy` | Không có scale/weight steps rõ |
| 17 | `tiny-text` / `undersized-ui-text` | Text < 12px cho UI |
| 18 | `tight-leading` | Line-height < 1.3 cho body |
| 19 | `line-length` | Measure > 75ch |
| 20 | `cramped-padding` | Padding < 16px toàn cục |
| 21 | `bounce-easing` | Bounce easing cho UI chuyển động |
| 22 | `marquee` | Marquee/scrolling ticker không cần thiết |
| 23 | `pulsing-dot` | Dot nhấp nháy |
| 24 | `numbered-section-labels` | 01/02/03 decorative |
| 25 | `em-dash-overuse` | Em-dash (—) lạm dụng trong copy |
| 26 | `image-hover-transform` | Scale/transform image khi hover |
| 27 | `italic-serif-display` | Serif italic cho display (AI tell) |
| 28 | `cream-palette` | Beige/cream background mặc định |

## DESIGN.md — Token Template (B/W/Y — brand TFO)

Mỗi project HTML giữ 1 file DESIGN.md (hoặc section tokens trong code) — mọi giá trị đúng 1 nguồn:

```yaml
name: <project>
description: <tagline>
colors:
  brand-yellow: "#FFD600"          # primary accent / CTA
  ink-black: "#0D0D0D"             # page ground
  surface-dark: "#1B1B1D"          # panels, cards
  surface-2: "#242428"             # raised
  border: "#2D2D32"                # hairlines
  text-primary: "#F5F5F5"          # headings
  text-body: "#E0E0E2"             # body
  text-muted: "#9E9EA4"            # meta, captions
  text-disabled: "#6B6B70"         # disabled
typography:
  font-display: "Space Grotesk, system-ui, sans-serif"   # display voice — self-host nếu offline
  font-body: "Inter, system-ui, sans-serif"
  scale: [12, 13, 14, 16, 18, 20, 24, 28, 32, 40, 48, 56, 64, 72, 80]
  measure: 65-75ch
spacing:
  base: 4
  rhythm: [4, 8, 12, 16, 24, 32, 48, 64, 96]
  radius: [8, 12, 16]
  elevation: "1px border hoặc shadow — không cả 2"
```

**Quy tắc token:**
- Mọi literal color/font-size/spacing trong code phải nằm trên ramp — không invent giá trị mới
- Thêm step là quyết định design, không phải tiện lợi (ramp 86 sizes = 6 bước gần giống nhau = fail)
- Vietnamese content bắt buộc có dấu; font subset vietnamese

## Lightweight Commands (nhúng vào quy trình)

### shape — trước khi code (khi task design rõ ràng)
1. Xác định mode (Persuade/Operate/Read/Experience)
2. Hỏi 2-3 câu liên quan, đợi. Không dump questionnaire
3. Chốt brief: audience, mục tiêu, brand constraints, anti-references
4. Mới design → chạy tiếp critique ngay sau build

### critique — sau khi build
1. Đánh giá A: design review theo craft-floor Verify (contrast, depth, spacing, type, motion, states, copy, coverage)
2. Đánh giá B: chạy Detector Rules checklist (~28 rules trên)
3. Tổng hợp: điểm mạnh, điểm yếu, fix list ưu tiên
4. Sửa 1 batch → confirm 1 lượt → dừng

### polish — trước khi ship
1. Chạy Verify checklist lần cuối
2. Kiểm tra drift với DESIGN.md: missing token? one-off implementation?
3. Kiểm tra states + responsive + keyboard focus
4. Xác nhận brief coverage
5. Chỉ refine, không đổi world — concept sai thì nói thẳng cần redesign

## Không áp dụng (cần infrastructure khác)

- `live` — cần dev server HMR + browser extension
- `audit` full — cần detect.mjs CLI quét code
- `overdrive`, `onboard`, `optimize` — cho app SPA phức tạp
- `init`/`document`/`extract` — cần PROJECT/DESIGN.md system đầy đủ (dùng khi làm design system riêng)

## Pitfalls

1. **Không tự chấm "đẹp"** — chạy checklist deterministic, đọc computed values thật (không eyeballing)
2. **Brief wins** — brand B/W/Y pin rồi thì không đổi màu vì "đẹp hơn"
3. **Bounded passes** — tối đa 2 lượt fix rồi dừng, không tự QA vô hạn (tốn tiền, không tốt hơn)
4. **Vietnamese có dấu** — copy tiếng Việt bắt buộc full diacritics
5. **Một element một công việc** — không nhồi decoration vào control
6. **Vision không sẵn → dùng detector DOM.** Khi `vision_analyze`/`browser_vision` lỗi (provider không nhận `image_url` — ví dụ model qua opencode-go/Console Go trả `unknown variant image_url`), KHÔNG bỏ dở audit. Chạy `scripts/ui-audit.js` qua browser_console (hoặc grep raw HTML cho emoji/svg) — deterministic, đủ phát hiện AI-tells chính. Screenshot/Playwright vẫn dùng được để chụp tài liệu, nhưng đừng phụ thuộc vision model cho audit.
7. **Emoji cleanup — phân biệt UI glyph vs DATA CONTRACT.** Khi thay emoji thay icon bằng SVG (rule `glyph-icons`), CHỈ đổi emoji trong UI chrome: nav, tab bar, buttons, card headers, filters. GIỮ NGUYÊN emoji là dữ liệu/contract:
   - Status string từ API: `a.status === '🔵 Working'` / `'⚪ Idle'` — đổi sẽ phá logic filter (Company 8090)
   - Emoji content/tags người dùng quen: category labels (🔬🧬🐷), org chart nodes (👑🛡📦) — giữ làm symbol nhỏ
   - CSS class name chứa emoji: `.dot-🔵` → đổi thành `.dot-blue` PHẢI sửa cả định nghĩa CSS lẫn mọi usage trong HTML/JS (đừng sed 1 chỗ)
   - Cách sạch cho status phase: thay emoji bằng `<span class="dot" style="background:#HEX"></span>` (8px circle) — phase → màu, không cần icon glyph
8. **Thêm display font cho HTML tĩnh**: link Google Fonts trong `<head>` (`<link href="https://fonts.googleapis.com/css2?family=Inter...&family=Space+Grotesk...">`) + CSS: body = Inter, `h1,h2,h3,.card-header,.tab-btn` = Space Grotesk. Radii lộn xộn: `sed -i 's/border-radius: 3px;/border-radius: 6px;/g'` theo hướng gom về ramp 8/12/16 (3px→6px, 4px→6px, 6px→8px, 10px→12px) — 3 bước là đủ.
9. **Tailwind v4 radius override 1 chỗ:** thêm vào `@theme`: `--radius-sm: 8px; --radius-md: 12px; --radius-lg: 16px;` — override toàn cục mọi `rounded-sm` (2px) mà không cần sửa từng class. Đặc biệt hữu ích khi source có hàng chục `rounded-sm` (React + Tailwind v4 không có tailwind.config — config nằm trong CSS `@theme`).
10. **Đổi `div.card-header` → `h2` semantic bằng regex Python:** pitfall — `</div>` đầu tiên sau `<h2>` có thể là đóng của element CON (không phải đóng card-header). Đã gặp khi đổi nhầm `mc-label` thành `</h2>`. Cách an toàn: đổi thẻ mở trước, rồi với mỗi h2 mở tìm `</div>` đầu tiên và đổi thành `</h2>`; SAU ĐÓ đếm `<h2` mở vs `</h2>` đóng phải cân bằng (9 mở = 9 đóng). Browser tự sửa thẻ sai nhưng HTML không chuẩn.
11. **Phân biệt Vite dev server vs static server:** cùng 1 app có thể chạy 2 port khác nhau serve bản KHÁC NHAU (Vite dev 3000 với HMR + python http.server 5099 serve file tĩnh riêng). Sửa source React chỉ ảnh hưởng Vite; bản static cần sửa file HTML khác. Xác định process thật của từng port (netstat PID → command line) trước khi sửa — tránh sửa nhầm file.

## Related Skills

- `html-publishing` / `content-publish` — publish sau khi qua quality gate này
- `html-unslop` — strip AI-isms text/CSS (bổ trợ, chạy trước publish)
- `design-md` — DESIGN.md spec chuẩn Google (token format chuẩn hơn)
- `design-critique` — critique-first workflow
- `dashboard-design-system` — Premium B/W/Y dashboard cụ thể

## Support Files

- `scripts/ui-audit.js` — detector JS chạy qua browser_console (audit UI trong Chrome thật)
- `references/ui-audit-console.md` — full IIFE + cách đọc kết quả + pitfalls khi sửa (radii, headings, emoji vs data contract) khi không xem được screenshot
- `references/svg-icon-set.md` — bộ SVG icons 1 stroke (dashboard, calendar, bolt, list, search, target, gear) dùng thay emoji nav/tab — copy-paste sẵn
