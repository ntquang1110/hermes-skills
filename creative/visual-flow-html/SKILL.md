---
name: visual-flow-html
description: "Use when academic content needs a visual flow HTML."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [html, visual, flow, infographic, kflow, research, design, preview]
    related_skills: [dashboard-design-system, html-publishing, camofox-browser]
---

# Visual Flow HTML — học thuật → flow trực quan

Trigger: user đọc xong 1 bài học thuật (card KFlow, bài research, video) và muốn "nhìn flow, hiểu nhanh bằng hình ảnh, từng bước, ra mục tiêu". Đây là định dạng Quang yêu cầu bổ sung (chốt 10/08/2026) bên cạnh bài đọc thuần học thuật: **preview trước khi publish, luôn luôn**.

## Variant — 3-tầng giải thích "Dễ hiểu → Kỹ thuật → PhD" (chốt 09/09/2026)

Khi user yêu cầu "đọc thông tin, hiểu sâu tại sao họ làm thế, visualize, giải thích từ dễ hiểu đến trình độ PhD" cho 1 TÀI LIỆU KỸ THUẬT (báo cáo BVMT, quy trình XLNT, sơ đồ công nghệ) — không dùng flow 11 bước thuần, mà dùng cấu trúc 2 tab:

- **Tab 1 "Sơ đồ"**: 2+ flowchain dọc (mỗi hệ thống 1 chuỗi node), node có số thứ tự + mô tả 1 dòng, phân nhóm màu theo loại (input/step/chem/out/warn). Thêm stats hero (số cứng từ tài liệu) + dòng hóa chất tóm tắt.
- **Tab 2 "Tại sao họ làm thế"**: MỖI quyết định công nghệ = 1 thẻ, trong thẻ 3 block màu cố định:
  - `.lvl.easy` (blue) — analogy đời thường, 2-3 câu.
  - `.lvl.tech` (orange) — thông số, vận hành, cách làm thật.
  - `.lvl.phd` (green) — cơ chế gốc: phương trình hóa, động học (Monod, DLVO, SRT), first principle.
  - Kèm `.fnote` (purple) "Bài học cho sản phẩm của mình" — nối kiến thức tài liệu vào dự án đang làm. Đây là phần user giá trị nhất, đừng bỏ.
- Mẫu chuẩn đã duyệt: `D:/Hermes Proj/pig-waste-source/thanhnam-bvmt2023.html` (16 quyết định × 3 tầng, từ báo cáo BVMT 2023 nhà máy nước Thành Nam).
- Verify bằng DOM audit: đếm `.wsec`, `.lvl.easy/.tech/.phd`, `.fnote` — phải bằng nhau và bằng số quyết định.

### Variant — Bài báo khoa học → 3 món (glossary + flow cơ chế + gói 3 tầng) (chốt 12/10/2026)

Trigger: user gửi 1 bài báo (link / PMID / PDF) kèm than phiền "không biết thuật ngữ, không biết cây nào, phản ứng với chất nào, tác động đường nào, cái gì chặn nó".
KHÔNG giải thích suông, KHÔNG hỏi lại dàn trải: trả thẳng 3 món + 1 đoạn phê bình số liệu.

1. **Bảng thuật ngữ trung tâm — 8 mục là điểm ngọt.** Chọn: chất nghiên cứu, cây/nguồn gốc, dòng tế bào hay đối tượng thí nghiệm, thụ thể–enzyme đích, 2–3 marker, 1–2 chất công cụ (vd rapamycin), 1 thuật ngữ phương pháp (vd time-of-addition). Mỗi mục: tên → nghĩa tiếng Việt 1 câu → vai trò trong chuỗi. Nguyên tắc: 8 thuật ngữ lặp nhiều nhất là đủ hiểu 80% bài, đừng dịch cả bài.
2. **Flow cơ chế — bắt buộc có legend ký hiệu** (đúng convention user yêu cầu):
   `→` kích hoạt/tác động · `⊣` chặn/ức chế · `↑ ↓` tăng giảm · **đỏ = chặn, xanh = kích hoạt, vàng = mắt xích quyết định**.
   Mỗi node trong HTML trả lời đủ 3 câu: cái gì chặn nó, cái gì làm thay đổi nó, nó tác động ai tiếp.
3. **Thí nghiệm cứu vãn (rescue experiment) — nếu bài có, đây là mục giá trị nhất.** Node vàng + card 4 dòng: câu hỏi → cách kiểm → kết quả → kết luận. Gặp chữ "partially reversed" thì nói thẳng: cơ chế chỉ giải thích MỘT PHẦN, phần còn lại bài chưa mổ xẻ.
4. **Card phê bình số liệu — luôn có, không bỏ.** Ba điểm chuẩn: N nhỏ (66.7% = 2/3 hay 4/6 con), hiệu ứng trông kịch tính vì đối chứng chết 100%, khoảng cách giữa liều in vitro và nồng độ thật sự đạt được khi cho uống.
5. **Gói 3 tầng** 5 giây / 1 phút / deep dive theo logic `azu-easy`; deep dive nêu câu hỏi bỏ ngỏ thật (vd "cho uống thì máu có đạt nồng độ như trong đĩa?"), không tô hồng.

Recipe đầu-cuối từ PMID → HTML → publish → verify: `references/paper-to-flow-pipeline.md`.

## Workflow

0. **Bài báo khoa học cụ thể (glossary + cơ chế + phê bình số liệu)?** Dùng skill `paper-mechanism-map` trước, nó có workflow lấy abstract qua E-utilities, chuẩn ký hiệu ⊣/→, mục phê bình bắt buộc, và design pass playful.

1. **Xác định nguồn bài**
   - Card KFlow: `GET http://localhost:3003/api/cards` kèm Cookie `tfo_auth=<sha256 passcode>` (passcode xem memory). Tìm theo card ID hoặc title keyword.
   - Card có block `<!--OVERVIEW-->` chứa JSON `{what, why, mechanism[], players[], applications[], limits, analogy}` — parse JSON này là xương sống của flow. Không cần đọc lại cả content.
2. **Chốt bản đồ dòng chảy** (8 chặng điển hình):
   Phân tử/khái niệm → cơ chế 1 → cơ chế 2 → ... → kết quả thực tế → mục tiêu.
   Mỗi cơ chế = 1 bước riêng, kèm mini-flow (chip + arrow) dạng `CA → Keap1 → Nrf2 → HO-1`.
3. **Cấu trúc HTML 11 bước** (mẫu chuẩn: `D:/Hermes Proj/cinnamaldehyde-flow.html`):
   - Sticky progress bar: đếm % scroll qua các section (id s0..s11, JS update trên scroll)
   - Hero: tag nguồn bài + H1 + 3 stat nổi bật (số cứng từ bài)
   - Bản đồ dòng chảy: flowchain dọc, node số vàng, đường nối
   - Bước cơ chế: mỗi cơ chế 1 section, mini-flow chips, callout "ý nghĩa thực tế", evrow bằng chứng kèm PMID
   - Bước "Bằng chứng in vivo": card highlight thí nghiệm chính + evrow từng trial
   - Bước "Phối trộn/liều": combo cards + dose rows
   - Bước "Rào cản → Giải pháp": ps 2 cột với mũi tên
   - Bước chốt MỤC TIÊU: card vàng (#FFD600) + 3 hành động cụ thể (đánh số)
   - Footer: PMID chips + nguồn gốc card
4. **Design**: dùng tokens từ skill `dashboard-design-system` (dark #0D0D0D, surface #1B1B1D, yellow #FFD600, radius 28, mobile-first 360px). KHÔNG trộn màu ngẫu nhiên.
5. **Preview (bắt buộc trước khi publish)**:
   - Serve local: `cd <folder> && python -m http.server <port>` (background). **Camofox chặn `file://` URL (400 /tabs) → phải serve qua HTTP.**
   - `browser_navigate http://127.0.0.1:<port>/<file>.html`
   - Verify layout bằng `browser_console` DOM audit (hasHScroll, overflowing elements) — KHÔNG gọi browser_vision/vision_analyze nếu model active không có vision (lỗi `unknown variant image_url`).
   - Screenshot full-page qua Camofox API → `references/camofox-screenshots.md`
   - Gửi `MEDIA:<png>` cho user duyệt + báo path file HTML.
6. **Sau khi duyệt**: publish preview.thefirstonly.com (skill `html-publishing`), file gốc giữ ở `D:/Hermes Proj/`. Cập nhật state file chat.

## Pitfalls
- Tiếng Việt CÓ DẤU; ghi file bằng write_file (python heredoc strip dấu).
- Mọi số liệu/quote/PMID phải từ nguồn bài gốc (đã verify). Không bịa thêm, không thêm con số mới.
- **Rò rỉ ký tự lạ khi viết HTML tiếng Việt trong 1 lần `write_file` (verified 12/10/2026):** file dài dễ lọt token CJK/Hàn ("거의", "拭") và từ tiếng Anh ("also") ngay giữa câu tiếng Việt. Quét TRƯỚC khi publish:
  ```bash
  grep -nP '[\x{3000}-\x{9FFF}\x{FF00}-\x{FFEF}]' file.html   # CJK / Hàn / fullwidth
  grep -n -oE '\b(also|and|the|with|from)\b' file.html          # từ Anh lọt vào câu Việt
  ```
  Sửa bằng `patch` (không viết lại cả file). Sau khi publish, quét lại trên BẢN ĐÃ UPLOAD và probe từng chuỗi đặc trưng (kể cả ký hiệu `⊣`): HTTP 200 không chứng minh nội dung còn nguyên.
- **`curl -o /dev/null -w "%{size_download}"` trả 0 dù server serve đúng (Windows/MSYS, verified 12/10/2026):** false negative, dễ kết luận nhầm "server trả rỗng". Đo kích thước thật bằng pipe `curl -s URL | wc -c`. Kèm pitfall 2 http.server cùng bind 1 port (chi tiết ở skill `camofox-browser`): `netstat -ano | grep ":<port>" | grep -ic listen` phải = 1, nếu 2 thì kill hết PID cũ rồi đổi port.
- Mobile-first: kiểm tra overflow ở 390px, không chỉ desktop.
- Kill http.server sau khi xong preview (process kill).
- Model không vision → không gọi vision_analyze/browser_vision; dùng Camofox screenshot + DOM audit để verify.
- Sticky progress: nếu sections ít hơn, đảm bảo mảng labels khớp số section.

## References
- `references/camofox-screenshots.md` — recipe chụp full-page PNG qua Camofox API khi browser_vision không dùng được
- `references/paper-to-flow-pipeline.md` — recipe đầu-cuối "user gửi PMID/link bài báo → glossary + flow cơ chế + gói 3 tầng → publish → verify": lấy abstract qua E-utilities khi trang PubMed chặn cookie, 8 thuật ngữ mẫu, cấu trúc 7 phần, lệnh grep bắt ký tự lạ, publish `POST /api/store` kèm User-Agent, probe chuỗi trên bản đã upload.
