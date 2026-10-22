# Design System v1.0 — Premium Dashboard (Black / White / Yellow)

> Source: User's `design.md` specification.
> Áp dụng cho MỌI UI work liên quan đến dashboard, web app, business card.

---

## 1. Design Philosophy

**Keywords:** Premium · Minimal · Modern · High Contrast · Soft Rounded · Functional · Spacious · Focus Driven

Mỗi màn hình chỉ có:
- 1 Primary Action
- 2-3 Secondary Actions
- 1 vùng dữ liệu chính

---

## 2. Color System

| Token | Light | Dark |
|-------|-------|------|
| **Primary Yellow** | `#FFD600` | `#FFD600` |
| **Background** | `#F6F6F4` | `#0D0D0D` |
| **Surface** | `#FFFFFF` | `#1B1B1D` |
| **Text Primary** | `#111111` | `#FFFFFF` |
| **Text Secondary** | `#8B8B8B` | `#8B8B8B` |
| **Text Disabled** | `#BDBDBD` | `#BDBDBD` |
| **Border (Dark)** | — | `rgba(255,255,255,.05)` |
| **Success** | `#44C767` | `#44C767` |
| **Warning** | `#FFB800` | `#FFB800` |
| **Danger** | `#FF4B4B` | `#FF4B4B` |

Yellow (`#FFD600`) chỉ dùng cho: CTA, Active State, Highlight, Progress, Important Number. Không dùng cho dữ liệu thông thường.

---

## 3. Typography

| Level | Size | Weight | Line Height | Use |
|-------|------|--------|-------------|-----|
| **H1** | 32px | 700 | 40px | Hero / Primary Number |
| **H2** | 24px | 600 | auto | Section title |
| **Body** | 16px | 400-500 | auto | Content / Value |
| **Caption** | 12px | 400 | auto | Labels / Metadata |

Font: `Inter`, -apple-system, sans-serif.

---

## 4. Layout

**Grid:** 8pt system — spacing only: `4, 8, 12, 16, 24, 32, 40, 48, 64`

**Safe Area:** Top 24, Bottom 32, Horizontal 20-24

---

## 5. Border Radius

| Component | Radius |
|-----------|--------|
| **Card** | 28 |
| **Button** | 999 (pill) |
| **Chip** | 999 (pill) |
| **Input** | 18 |
| **Small Icon** | 16 |

Mọi component đều bo lớn. Không dùng góc vuông.

---

## 6. Shadow & Border

| Mode | Style |
|------|-------|
| Light | `0 8 20 rgba(0,0,0,.08)` |
| Dark | No shadow — use `border: 1px solid rgba(255,255,255,.05)` |

---

## 7. Card

- Padding: 24px
- Gap giữa các card: 16px
- Max 3 tầng thông tin: **Title** → **Value** → **CTA**
- Card chỉ phục vụ 1 mục đích duy nhất

---

## 8. Buttons

| Type | Style |
|------|-------|
| **Primary** | Yellow bg (#FFD600) · Black text |
| **Secondary** | White bg · No border |
| **Ghost** | Transparent · border .05 |

- Height: 56px
- Radius: 999
- Padding X: 24

---

## 9. Icon Style

- Style: **Outlined** (Material Symbols Outlined)
- Size: 20px · 24px
- `font-variation-settings: 'FILL' 0, 'wght' 300, 'GRAD' 0, 'opsz' 24`
- Không mix Outline và Fill

---

## 10. Data Hierarchy

```
Heading ↓ Primary Number ↓ Secondary Info ↓ Action
```

Không đảo ngược thứ tự.

---

## 11. White Space

- Mỗi section cách nhau 24px hoặc 32px
- Không dính sát nhau

---

## 12. Motion

- Duration: 200ms
- Easing: ease-out
- Không animation dài

---

## 13. Accessibility

- Min touch area: 48×48
- Contrast ≥ 4.5
- Không dùng màu để biểu đạt duy nhất — luôn kèm icon hoặc text

---

## 14. Responsive Breakpoints

| Device | Width |
|--------|-------|
| Mobile | 360+ |
| Tablet | 768+ |
| Desktop | 1280+ |

Không scale mọi thứ — chỉ tăng khoảng trắng.

---

## 15. UX Rules

1. **1 Hero per screen** — mọi thứ khác phải nhỏ hơn
2. **1 Primary CTA** — không hai nút vàng cùng khu vực
3. **Reading order:** Top → Left → Center → Bottom
4. **Card = 1 purpose** — Sales card không chứa Chart + Form + Notification
5. **Reduce cognitive load** — bỏ đường viền, icon, label nếu có thể

---

## 16. Component Standards

| Component | Spec |
|-----------|------|
| Card | Radius 28 · Padding 24 · Gap 16 |
| Button | Height 56 · Radius 999 · Padding X 24 |
| Chip | Height 44 · Radius 999 · Padding X 20 |
| Avatar | 40 / 48 / 64 |
| Input | Height 56 · Radius 18 |

---

## 17. Developer Checklist

- [ ] Sử dụng grid 8pt
- [ ] Chỉ dùng token màu trong Design System
- [ ] Không hardcode màu / spacing
- [ ] Border radius đúng chuẩn
- [ ] Button cao 56px
- [ ] Touch target ≥ 48px
- [ ] Contrast đạt WCAG
- [ ] Typography đúng scale
- [ ] Chỉ 1 Primary CTA mỗi section
- [ ] Khoảng trắng giữa section ≥ 24px
- [ ] Card chỉ phục vụ 1 mục đích
- [ ] Icon đồng bộ cùng style (outlined)
- [ ] Animation ≤ 200ms
- [ ] Dark mode sử dụng cùng token

---

## 18. Nguyên tắc vàng

> **Nếu phải lựa chọn giữa "đẹp hơn" và "dễ dùng hơn", luôn ưu tiên "dễ dùng hơn".**

Một giao diện cao cấp không đến từ nhiều hiệu ứng, mà từ:
- Nhất quán
- Khoảng trắng hợp lý
- Phân cấp thị giác rõ ràng
- Tốc độ thao tác nhanh
- Khả năng mở rộng và bảo trì lâu dài
