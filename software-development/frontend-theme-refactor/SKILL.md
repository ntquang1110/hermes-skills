---
name: frontend-theme-refactor
description: "Refactor an HTML app's theme without breaking its JS."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [frontend, theme, redesign, refactor, html, css, javascript, verification, design-system]
    related_skills: [impeccable, design-md, design-critique, dashboard-design-system, html-unslop, html-publishing]
---

# Frontend Theme Refactor

Áp design system/theme đã duyệt lên app HTML hiện hữu (thường là 1 file `index.html` lớn, CSS + JS inline) mà KHÔNG phá logic. Bổ trợ cho `impeccable` (chất lượng design) — skill này lo phần **triển khai an toàn + verify**.

## When to use

- User chốt 1 phương án theme/design (từ mockup PA1/PA2/PA3) và yêu cầu triển khai trên app thật
- App là single-file HTML (CSS inline + JS inline + template literals render HTML)
- Cần đổi bộ token màu/font/radius + xoá emoji chrome + semantic heading mà giữ nguyên 100% hành vi JS

## Nguyên tắc sống còn

- **Đọc toàn bộ file trước** (kể cả JS template literals) trước khi sửa. Grep mọi `class` CSS mà JS tham chiếu (`getElementById`, `classList`, template strings) — giữ NGUYÊN tên class/id, chỉ đổi style.
- **Backup trước:** `cp index.html index.html.bak-<theme>` (xoá khi user duyệt ổn vài ngày).
- **Data contract emoji:** trước khi thay emoji, grep `status === 'emoji'` / map keyed by emoji (`{ on_track: '🟢', ... }[p.status]`). Chỉ đổi VALUE hiển thị, GIỮ key/logic. Map key → màu: `{ on_track: 'var(--green)', ... }` + `<span class="dot" style="background:...">`.
- **Static app không cần rebuild:** FastAPI/StaticFiles serve từ disk — sửa xong reload là áp dụng.

## Workflow (đã verify trên TFO 150KB, 2643 dòng)

1. **Backup** cả index.html + login.html (`.bak-<theme>`).
2. **Map toàn bộ**: đọc hết file; liệt kê class CSS dùng trong JS; ghi chú vị trí emoji chrome (static HTML + JS template) và emoji data contract.
3. **CSS swap**: viết CSS block mới (giữ NGUYÊN tên token `--black/--surface/--surface2/--border/--text/--text2/--yellow/--yellow-dim/--green/--red/--blue/--orange` vì JS inline style tham chiếu). Thêm class mới (`.dot`, `.pd`, `.stats-row-4`, checkbox `.task-check.checked`...).
4. **Transform bằng Python script viết qua write_file** (KHÔNG heredoc — strip dấu tiếng Việt):
   - Mỗi replacement khai báo expect count, in warning `!! EXPECT N got M` khi lệch
   - Thay emoji chrome → SVG 1-stroke; data-contract emoji → dot màu
   - Global strip list cho emoji 'X ' (emoji + space) — chạy SAU các replace cụ thể
   - Cuối script: đếm emoji còn lại bằng regex `[\U0001F300-\U0001FAFF\u2600-\u27BF\u2B00-\u2BFF\uFE0F]`, in ra để soát
5. **Semantic heading** (div.card-header → h2) bằng depth-scan — xem Pitfalls.
6. **Verify** theo checklist dưới — bounded, tối đa 2 lượt fix.

## Verify checklist (chạy đủ trước khi báo "xong")

1. **Detector audit** (script `ui-audit.js` trong skill `impeccable`): kỳ vọng emoji-icons=0 (chấp nhận ✕ close glyph), radii ∈ ramp {8,12,16,999,50%,tab-top}, headings h1=1 + h2=N, contrast ≥4.5.
2. **JS không vỡ:** `typeof window.<fn>` cho MỌI function ở mọi `<script>` block (25+ hàm). 1 hàm missing = syntax error trong block đó.
3. **Switch tab / view:** gọi từng `switchTab(...)`, không exception.
4. **Template render thật:** stub `window.fetch` trả fake data → gọi `loadKanban()` / `renderProjects()` / `loadTasks()` → kiểm tra HTML output: dot/checkbox class đúng, không emoji, onclick giữ nguyên.
5. **Mobile:** inline `grid-template-columns` phá media query — đưa vào class + `!important` override. Check KPI 2x2 trên phone.
6. **App thật:** curl app đang chạy xác nhận serve file mới; login page render; auth guard /app còn nguyên.
7. Xoá file audit tạm; giữ backup tới khi user duyệt.

## Multi-PA proposal (user preference — Quang)

Khi user muốn CHỌN hướng theme/style (chưa chốt): đừng hỏi tả trừu tượng. Dựng 2-3 phương án khác biệt RÕ thành **1 file HTML so sánh**: mỗi PA 1 tab + tab "So sánh + đề xuất" (bảng trade-off + box recommendation) + banner mô tả PA. Mockup phải render skeleton dashboard thật (header, tabs, KPI, kanban, thread) để user hình dung. Publish URL (upload server 8899 hoặc preview.thefirstonly.com) rồi đưa link — user chọn 1 PA, rồi mới triển khai. Anti-reference mặc định: gradient tím-xanh, glow tràn, grid nền, scanline, neon text.

## Pitfalls (đã vấp thật)

1. **Auth guard gây navigation loop khi audit.** Page có `if (!token) { window.location.href = '/'; return false; }` → browser_console 500 `Execution context was destroyed... navigation`, snapshot rỗng. Tạo bản copy tạm bỏ guard (`sed` đổi thành `return false`), serve static port khác, audit bản đó, xoá sau. Nếu vẫn redirect, tìm `location.href = '/'` khác trong `checkAuth()`.
2. **CRLF + emoji qua shell (Windows).** (a) File Windows có thể CRLF — pattern `\n` không match; check `repr(s[i-6:i+12])` thấy `\r\n` thì dùng `\r\n`. (b) Emoji literal qua `python -c "..."` trong MSYS bash bị mangle → count 0 vô cớ; dùng `\U0001F3A4` escape. (c) Script viết bằng write_file, không heredoc.
3. **Detector hard-offset-shadow false positive.** Regex match giá trị spread (số thứ 4) của shadow blur thật: `0 8px 24px 0px` bị flag dù blur 24px hợp lệ. Verify element trước khi sửa.
4. **Inline `grid-template-columns` phá media query.** Inline `repeat(4,1fr)` thắng media query → mobile vỡ. Đưa vào class + media `!important` override.
5. **card-header div → h2: đừng dùng "tìm `</div>` đầu tiên" thô** — card-header có thể chứa div con (flex buttons). Cách verify: đổi thẻ mở trước; với mỗi `<h2 class="card-header">` quét tới, đếm depth `<div`(+1)/`</div>`(-1), đổi `</div>` đầu tiên đưa depth về 0 thành `</h2>`; cuối cùng đếm `<h2` == `</h2>` (16/16 pass).
6. **JS set `textContent` lên element có SVG icon sẽ xoá icon.** Nút record: đặt `<span id="recordLabel">` riêng, JS chỉ sửa label, SVG giữ nguyên. Check mọi chỗ JS `textContent =` trỏ vào element mà bạn vừa thêm icon.

## Support Files

- `references/frontend-transform-verify.md` — chi tiết verify + skeleton script transform có assertion (TFO làm mẫu)
