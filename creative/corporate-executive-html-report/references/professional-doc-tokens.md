# Design tokens cho tài liệu bộ phận (formal, nghiêm túc)

Dùng khi tài liệu để kế toán / pháp lý / vận hành ĐỌC ĐỂ LÀM — không phải để lãnh đạo duyệt.
Quang đã chê thẳng design sticker ("mát hết tiếng Việt rồi") cho loại tài liệu này.

## Blue Professional (đã dùng & duyệt, 09/2026)

| Token | Giá trị |
|---|---|
| Canvas | `#fdfae7` warm cream |
| Ink | `#111111` |
| Muted | `#6b6b6b`, tertiary `#9a9a9a` |
| Accent | `#1e2bfa` royal blue |
| Wash | `rgba(30,43,250,.04 / .08 / .15 / .20)` |
| Font | Inter 400/500/600/700 — KHÔNG serif, KHÔNG mono |
| Card | nền `#fff`, border `rgba(30,43,250,.2)`, radius 12px |
| Section title | 700, gạch chân 2px `#1e2bfa`, `display:inline-block` |
| Step | border-left 4px `#1e2bfa`, radius 12px |
| Table head | `rgba(30,43,250,.08)` + border-bottom 2px accent |
| Radius gom | 4px (badge) / 8px / 12px — KHÔNG pill |
| Deco | quote block (border-left 3px), paper wash, KHÔNG gradient/shadow |

Màu nhấn phụ (cho callout lưu ý / rủi ro): `#fb4903` — dùng rất tiết chế, chỉ cho cảnh báo.

Vibe: "blueprint nghiệp vụ". Rộng rãi, nhiều khoảng thở, số liệu nổi bật.

## Trích token từ gallery khi KHÔNG có file template

`popular-web-designs/templates/` có **ít hơn** số theme trong gallery. User chọn theme chưa có file
→ `skill_view` trả `File 'templates/<name>.md' not found`. Đừng đổi theme khác, đừng bắt user chọn lại.
Token nằm ngay trong HTML gallery:

```bash
curl -sL "https://preview.thefirstonly.com/<gallery_id>" | grep -i "<tên theme>" -A 50
```

Trong block đó:
- `palette` → `swatch` `style="background:#hex"` — thứ tự: canvas trước, rồi ink, rồi accent
- `fonts` → `font-row` có `font-label` (serif/sans/mono) + `font-name` (family thật, hoặc `—` = không có)
- `deco` → chip `deco-badge`: quote / shape / paper / grain / ribbon / pill → đọc như design rule
- `scheme-badge` = light | dark → quyết định canvas sáng hay tối

## Nguyên tắc chọn design theo đối tượng đọc

| Đối tượng | Theme |
|---|---|
| Kế toán, pháp lý, vận hành — đọc để làm | **Blue Professional** |
| Chủ tịch / lãnh đạo — đọc để duyệt | tokens forest+gold trong SKILL.md |
| Bài học thuật / nghiên cứu | `visual-academic-html` (B/W/Y) |
| Bán hàng B2B, thuyết phục | file A/B 5-trang trong SKILL.md |
| Social / bắt trend | Slush, GSAP — KHÔNG dùng cho tài liệu nghiệp vụ |
