---
name: dashboard-design-system
description: "Premium Dashboard design system — Black/White/Yellow color tokens, typography scale, 8pt grid, border radius, component specs, UX rules. Used for visit cards, dashboards, quotation pages, and landing pages by TheFirstOnly brand."
tags: [design, ui, dashboard, premium, black-white-yellow]
related_skills: [hermes-dashboard, sketch, excalidraw, popular-web-designs]
---

# Premium Dashboard Design System (Black / White / Yellow)

> Đây là tài liệu chuẩn để UI Designer, Frontend Developer và QA cùng follow.
> Mọi màn hình mới phải tuân thủ các quy tắc dưới đây.

Khi build HTML pages cho user này (visit card, dashboard, quotation, landing page), LUÔN dùng design tokens dưới đây. Không trộn màu ngẫu nhiên, không hardcode spacing.

---

## 1. Design Philosophy

- **Premium · Minimal · Modern · High Contrast**
- **Soft Rounded · Spacious · Focus Driven**
- Mỗi màn hình chỉ có: **1 Primary Action**, **2-3 Secondary Actions**, **1 vùng dữ liệu chính**

---

## 2. Color System

### Primary Yellow
`#FFD600` — dùng cho: CTA, Active State, Highlight, Progress, Important Number

### Background
- Light: `#F6F6F4`
- **Dark: `#0D0D0D`** (chính)

### Surface
- Light: `#FFFFFF`
- **Dark: `#1B1B1D`**

### Text
- Primary: `#111111` (light) / `#FFFFFF` (dark)
- Secondary: `#8B8B8B`
- Disabled: `#BDBDBD`

### Status
- Success: `#44C767`
- Warning: `#FFB800`
- Danger: `#FF4B4B`

---

## 3. Typography (chỉ 3 cấp)

| Style | Size | Weight | Line Height | Dùng cho |
|-------|------|--------|-------------|----------|
| **H1** | 32px | 700 | 40px | Hero number (VD: "245,243") |
| **H2** | 24px | 600 | — | Section title |
| **Body** | 16px | 400~500 | — | Nội dung chính |
| **Caption** | 12px | 400 | — | Label phụ |

---

## 4. Layout — 8pt Grid System

**Spacing chỉ được phép:** 4, 8, 12, 16, 24, 32, 40, 48, 64

Không dùng spacing ngẫu nhiên. Safe area: Top 24 · Bottom 32 · Horizontal 20~24

---

## 5. Border Radius

| Component | Radius |
|-----------|--------|
| **Card** | 28px |
| **Button** | 999px (pill) |
| **Chip** | 999px |
| **Input** | 18px |
| **Small Icon** | 16px |

Mọi component đều bo lớn. Không dùng góc vuông.

---

## 6. Shadow (Light Mode)
`0 8 20 rgba(0,0,0,.08)`

**Dark Mode:** KHÔNG dùng shadow. Dùng `border: rgba(255,255,255,.05)` thay thế.

---

## 7. Cards
- Padding: 24px
- Gap giữa các card: 16px
- Card không quá 3 tầng thông tin

**Sai:** Title → Subtitle → Description → Progress → Chart → Button → Footer  
**Đúng:** Title → Value → CTA

---

## 8. Buttons
| Style | Bg | Text | Border |
|-------|-----|------|--------|
| **Primary** | `#FFD600` | `#111111` | None |
| **Secondary** | `#FFFFFF` | `#111111` | None |
| **Ghost** | Transparent | `var(--text-primary)` | `var(--border)` |
| **Icon Button** | — | — | Circle 48x48 |

Button height: **56px** · Radius: **999px** · Padding X: 24px

---

## 9. Icons
- Style: **Outlined** (Material Symbols)
- Size: 20px hoặc 24px
- **Dashboard list items**: icon trong `.icon-wrap` xoay **45 độ** — thêm `transform: rotate(45deg)` cho `.mat-icon` bên trong
- Không mix Outline và Fill

---

## 10. Navigation
- Top AppBar: Title + Back + tối đa 2 actions
- Bottom Navigation: tối đa 5 tab (Home, Dashboard, Analytics, Profile)

---

## 11. Data Hierarchy
Thứ tự luôn là: **Heading → Primary Number → Secondary Info → Action**

---

## 12. White Space
Mỗi section phải có khoảng nghỉ 24px hoặc 32px. Không dính sát nhau.

---

## 13. Motion
- Duration: 200ms
- Easing: ease-out
- Không animation dài.

---

## 14. Accessibility
- Minimum touch area: 48×48px
- Contrast ≥ 4.5
- Không dùng màu để biểu đạt duy nhất (luôn kèm icon/text)

---

## 15. UX Rules

### Rule 1 — One Hero
Một màn hình chỉ có 1 Hero. VD: "245,243" là Hero — mọi thứ còn lại nhỏ hơn.

### Rule 2 — Single Primary CTA
Primary CTA luôn nổi bật. Không có hai nút vàng trên cùng một khu vực.

### Rule 3 — Reading Order
Top → Left → Center → Bottom

### Rule 4 — Single Purpose Card
VD: Sales Card không chứa Chart + Form + Notification cùng lúc.

### Rule 5 — Reduce Cognitive Load
Nếu có thể bỏ được một đường viền → bỏ. Một icon → bỏ. Một label → bỏ.

---

## 16. Component Standards

| Component | Value |
|-----------|-------|
| **Card** | radius: 28, padding: 24, gap: 16 |
| **Button** | height: 56, radius: 999, padding X: 24 |
| **Chip** | height: 44, radius: 999, padding X: 20 |
| **Avatar** | 40, 48, 64px |
| **Input** | height: 56, radius: 18 |

### Item List Overflow

Khi danh sách item có text dài (domain name, mô tả), dùng CSS text-overflow để tránh overlapping:

```css
.site-item .info { flex: 1; min-width: 0; overflow: hidden; }
.site-item .domain { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.site-item .desc { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
```

`.arrow` cần `flex-shrink: 0` + `min-width` để không bị đẩy khi text dài.

---

## 17. Responsive Breakpoints
- Mobile: 360+
- Tablet: 768+
- Desktop: 1280+

Không scale mọi thứ — chỉ tăng khoảng trắng.

### SVG / diagram trong HTML — chống chữ bị co

SVG có `viewBox` rộng hơn container thì **mọi chữ bị thu nhỏ theo**: `chữ thật = font-size × (containerWidth / viewBoxWidth)`. Đây là lỗi im lặng — không lỗi JS, `browser_snapshot` vẫn đủ element, mà không đọc được trên điện thoại.

- Giữ **viewBox width 600–700** (container nội dung ~650px) ⇒ scale ≈ 1. viewBox 900–1000+ cho một diagram nhỏ là lỗi.
- **Chữ nhỏ nhất SAU scale ≥ 12px** (Quang đọc bằng điện thoại).
- Nhiều nhãn → **layout dọc** (node xếp trên→dưới cùng `x`, cung quay về đi bên phải), KHÔNG xếp ngang.
- Verify bằng **ĐO** (`getBBox()` + `getBoundingClientRect()` → scale, chữ thật, va chạm nhãn). **Không tin vision model cho hình học** — nó bịa nhãn không tồn tại và báo node "lệch trục" trong khi cả ba cùng `cy`.
- Recipe đo đầy đủ + ngưỡng pass/fail: [`references/svg-diagram-legibility.md`](references/svg-diagram-legibility.md)

---

## 18. Nguyên tắc vàng

> **Nếu phải lựa chọn giữa "đẹp hơn" và "dễ dùng hơn", luôn ưu tiên "dễ dùng hơn".**

Một giao diện cao cấp đến từ: nhất quán · khoảng trắng hợp lý · phân cấp thị giác rõ ràng · tốc độ thao tác nhanh · khả năng mở rộng.

---

## 19. Partner One-Pager (poster cho đối tác / người không rành kỹ thuật)

Khi user yêu cầu "bản dễ nhìn dễ hiểu cho bác X, hiểu nhanh nhất, ít hỏi lại" → xem `references/partner-one-pager.md`: cấu trúc 7 block (hero → 3 chuyện ngắn → bản đồ zone → 4 phương án kèm con số tiền → hero number tổng → 3 bước → chốt), quy tắc chữ to ít chữ, trấn an trước đề xuất sau, design tokens B/W/Y, và cách verify bằng browser_console khi vision model lỗi. Case mẫu: `visual-bac-thuc.html` (đối tác Tây Nguyên, 09/2026).
