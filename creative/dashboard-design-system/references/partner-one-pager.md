# Poster-style One-Pager cho đối tác / người không rành kỹ thuật

Khi user yêu cầu "visualize bản dễ nhìn dễ hiểu cho bác X, để họ hiểu nhanh nhất và ít phải hỏi lại nhất" — đây là class riêng, KHÔNG phải dashboard, KHÔNG phải landing bán hàng. Là **Read/Persuade hybrid cho 1 người cụ thể**: poster cuộn dọc, chữ to, ít chữ, đập vào mắt là hiểu.

Case đã chứng minh: bác Thực (đối tác góp vốn, công ty thiết bị điện, Tây Nguyên) — file `visual-bac-thuc.html`, preview https://preview.thefirstonly.com/8jp5tmscyosq (09/2026).

## Cấu trúc chuẩn (7 block, theo thứ tự)

1. **Hero** — tag pill vàng "GỬI BÁC X" + H1 34–64px 1–2 dòng + 1 đoạn "kể chuyện" ≤ 60ch + dòng diện tích/quy mô nhỏ.
2. **3 card "chuyện" ngắn** — mỗi card 1 câu chốt: chuyện pháp lý (trấn an) / chuyện làm ăn (cơ hội) / chuyện dòng tiền (con số). Đây là phần user băn khoăn nhất → gỡ ngay ở đầu, trước khi trình phương án.
3. **Bản đồ khu/zone** — visual chia theo yếu tố quyết định (vd: độ che nắng). Mỗi zone: tên + diện tích + 1–3 plan card nhỏ. Không dùng bảng dữ liệu — dùng grid box.
4. **4 card phương án** — icon SVG 1-stroke + H3 + 1 dòng "chỗ nào dùng" + đoạn ngắn + **dòng tiền nổi bật cuối card** (con số + span).
5. **Hero number tổng** — block nền vàng lớn: "1,5–3 tỷ / năm" + 2 stat nhỏ bên dưới (card đen).
6. **3 bước triển khai** — bước 1 khảo sát / 2 pilot / 3 scale. Mỗi bước: số to + H3 + đoạn ngắn.
7. **Cảm ơn / chốt** — box trung tâm: 1 đoạn tóm + 1 câu chốt kiểu "Không cần bác tự làm — thuê HTX làm, bác giữ đất và điện" + footer disclaimer nhỏ.

## Quy tắc bắt buộc

- **Chữ to, ít chữ**: H1 ≥ 34px, số tiền dùng Space Grotesk đậm, body 15–17px. Không bao giờ để một block quá 2 câu.
- **Kể bằng cấu trúc, không kể bằng đoạn dài**: grid > paragraph. Nếu block đó là 3 dòng text liền → tách thành card/box.
- **Trấn an trước, đề xuất sau**: nếu có tin đồn/pháp lý gây lo (vd "luật bắt 2 tỷ"), block đầu tiên là gỡ nó, kèm 1 dòng khẳng định. Không để sự lo lắng đè lên đến hết trang.
- **Mỗi phương án phải có con số tiền** — đối tác quyết định bằng tiền, không bằng mô tả.
- **Disclaimer nhỏ cuối trang**: "số liệu ước tính, cần kiểm chứng thực địa" — 13px muted, không cần nổi bật.
- **Design tokens B/W/Y** (dashboard-design-system): nền `#0D0D0D`, surface `#1B1B1D`, surface2 `#242428`, vàng `#FFD600`, border `#2D2D32`. Radius 12–16, elevation = 1px border (không shadow ở dark mode).
- **Responsive 1 cột** ở mobile (≤840px) — bác X đọc bằng điện thoại là chính.

## Verify trước khi giao

- `browser_navigate(preview_url)` — snapshot trả đủ heading (1 H1, các H2), đếm `.zone`, `.pa`, `.step`, `.t-big`.
- `browser_console` expression: `({h1:..., h2:..., cards:..., zones:..., steps:..., total:..., bodyBg:..., errors:[]})` — check bodyBg = rgb(13,13,13), total có con số đúng.
- Vision model có thể lỗi 401 (invalid token payload) → KHÔNG bỏ dở; browser_snapshot + console đủ để verify cấu trúc.

## Lưu ý khác

- Publish qua skill `publish`: `md-to-html.py` → `content-upload.py --file X.html --title "..."` → preview.thefirstonly.com/<id>. Scripts nằm trong skill dir (không phải project cwd); khi cwd ở ổ D dùng path dạng `C:/Users/...` chứ không `/c/...` (MSYS biến thành `D:\c\...`).
- Source markdown đầy đủ (báo cáo dài) và bản visual là 2 deliverable riêng: user gửi đối tác bản visual, giữ bản chi tiết làm tài liệu nội bộ.