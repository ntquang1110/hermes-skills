---
name: executive-visual-report
description: "Turn trial/report data into formal executive visual HTML."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [html, visualize, report, executive, b2b, partner, corporate, trial]
    related_skills: [visual-academic-html, claude-design, publish, livestock-trial-protocol]
---

# Executive Visual Report (báo cáo visual gửi lãnh đạo/đối tác)

Dùng khi user có **kết quả thử nghiệm / số liệu đo đạc** (docx, pdf, sheet) và muốn dựng
bản visual trình bày cho **cấp lãnh đạo đối tác hoặc chủ tịch tập đoàn** — mục tiêu để họ
hiểu nhanh và quyết định, không phải để đọc chi tiết kỹ thuật. Phân biệt với
`visual-academic-html` (KFlow card, theme tối B/W/Y) — bài này dùng **formal corporate sáng**.

## Quy tắc cốt lõi (Quang chốt 07/09/2026, báo cáo EZ-CT888 tại Xuân Thiện Thanh Hóa)

1. **KẾT QUẢ TRƯỚC, quá trình sau, cơ chế cuối cùng.** "Đưa ra kết quả luôn, rồi mới bán ngược về
   quá trình và tại sao hiệu quả". Chủ tịch không đọc báo cáo — ông ấy đọc quyết định: 30 giây
   phải ra được câu chuyện.
2. **2 file, không 1**: File A = 1 trang A4 tổng kết (thứ duy nhất chủ tịch mở), File B = visual
   đầy đủ (cho cấp kỹ thuật / ban môi trường / khi hỏi sâu).
3. **Bố cục File A (1 trang A4):**
   - Header: 2 bên — trái CÔNG TY + địa chỉ, phải tên tài liệu + mốc thời gian
   - Badge giai đoạn + H1 nêu con số giảm lớn (vd "giảm tới 84–92% chỉ tiêu ô nhiễm chính")
   - 4 KPI cards (navy, số to): chỉ tiêu + vị trí + cặp giá trị (ngày 7 → 15)
   - Khối **kinh tế 3 cột**: chi phí hiện tại vs chi phí sản phẩm vs tiết kiệm % (nổi bật nhất)
   - Ý nghĩa với đối tác (4 bullet ✓)
   - Vì sao hiệu quả: 1 đoạn ngắn (cơ chế hoạt chất + tích lũy theo thời gian)
   - Footer: đơn vị thực hiện, cán bộ phụ trách, người viết, mã báo cáo
4. **Số liệu giữ NGUYÊN từ nguồn** — không bịa %, không làm tròn sai, không che yếu điểm.
   File B phải ghi rõ chỗ nào còn theo dõi (vd hồ air chưa giảm mạnh). Trung thực = tăng độ tin cậy
   với đối tác lớn, "báo % hallucination thật" (Quang yêu cầu).
5. **Tính toán kinh tế phải chốt đơn vị TRƯỚC khi tính.** Hỏi: giá theo kg hay theo bao? Chi phí
   hiện tại tính theo m³ hay tháng? Không suy đoán. Công thức mẫu đã chốt:
   `150 kg/1.000m³ × 180.000đ/kg = 27.000đ/m³` vs `>50.000đ/m³` → tiết kiệm ~46%.
6. **MỌI lô phải hiện đủ MỌI mốc đo** (Quang chốt 08/09): biểu đồ/bảng phải chứng minh từng công
   thức ĐC/CT1/CT2 được đo ở tất cả các ngày (N1, N7, N15...), không chỉ mốc cuối. Ngày 1 là mốc
   nền CHUNG (cùng nguồn nước đầu vào) → vẽ lặp cùng giá trị cho cả 3 lô để mắt thấy mỗi lô đều
   có cột ở N1, kèm chú thích "ngày 1 là nền chung của cả 3 công thức".
7. **So sánh chuẩn xả thải (cột B) + dự báo quán tính** — khối bắt buộc sau kết quả mốc hiện tại (08/09):
   - So với cột B (QCVN ngành nước thải chăn nuôi: BOD5 100, COD 300, TSS 150, Tổng N 150 mg/L,
     pH 5,5–9,0) từng chỉ tiêu tại vị trí chính (nơi rải sản phẩm).
   - **BIỂU ĐỒ CỘT NGANG, không bảng số**: mỗi chỉ tiêu một khối, thanh vàng = mốc cột B có GIÁ
     TRỊ in cạnh thanh, thanh xanh = đạt / đỏ = vượt kèm badge "VƯỢT ×N", số in ngay cạnh từng
     thanh. "Nhìn số đối chiếu được luôn, không cần dò số" (Quang chốt).
   - **Dự báo theo quán tính**: ngoại suy cửa sổ đo cuối (vd N7→N15 = 8 ngày), trình bày KHOẢNG
     giữa giả định tuyến tính (nhanh) và suy giảm chậm dần (thận trọng). Ghi rõ: chỉ tiêu đã đạt
     ngay mốc hiện tại · mốc dự kiến chạm chuẩn · điểm KHÔNG dự báo được (dãy số chưa có xu hướng
     giảm, vd hồ chứa nước tồn từ trước xử lý → chờ mốc kế tiếp xác nhận). Trung thực, không hứa quá mức.

## Style (formal corporate, KHÔNG dark/B/W/Y)

- Nền sáng: body `#F1F5F9` / `#F8FAFC`, surface trắng, border `#E2E8F0`
- Navy `#1F3B57` (header, tiêu đề, KPI cards, footer) + green `#15803D` (accent, số tốt, badge)
- Đỏ `#B91C1C` cho con số chi phí cũ, vàng `#FDE68A` cho điểm nhấn trên nền navy
- Bảng so sánh: th navy trắng, hàng chẵn `#F8FAFC`, ô "tốt hơn" green bold
- Bar chart: DC `#94A3B8`, CT1 `#7DD3FC`, CT2 `#15803D` (xanh lá = công thức tốt nhất)
- Font Segoe UI / system-ui. File A cố định A4: `.page{width:210mm;min-height:297mm}`, `@page{size:A4;margin:0}`
- File B responsive (max-width 1080px, cards 4 cột → 2 cột dưới 760px)

## File B — cấu trúc 8 khối

1. Header formal (giống File A)
2. Hero: badge + H2 câu chốt + sub mô tả thử nghiệm
3. 4 KPI cards (bổ sung chú thích ngày 7→15)
4. So sánh kinh tế 3 cột
5. Bối cảnh: vị trí lấy mẫu / công thức / chỉ tiêu / mốc đo + sơ đồ flow (Đầu vào → M1 → M2A/M2B → M3A/M3B → Đầu ra)
6. Kết quả theo từng chỉ tiêu: chart JS data-driven (nhóm N1 + N7 + N15, 3 bar DC/CT1/CT2 mỗi nhóm;
   N1 là mốc nền chung, lặp cùng giá trị cho 3 lô) — "càng thấp càng tốt" trừ pH
7. Bảng tần suất vượt đối chứng (vd CT2 26/40=65% vs CT1 16/40=40%) + kết luận công thức nào
8. So sánh cột B (bar chart ngang, thanh chuẩn vàng kèm số) + dự báo quán tính (xem Quy tắc #7)
9. Bước tiếp theo (3 card) + footer

Chart JS pattern đã chạy OK: đặt `.ch` container rỗng có `data-max`, script đọc CHARTS map
`{key: {groups: [['Ngày 1',[n,n,n]], ['N7',[dc,ct1,ct2]], ['N15',[dc,ct1,ct2]]]}}`, dựng bar theo %
của max, giá trị hiện trên đầu bar. Đổ giá trị TRỰC TIẾP từ báo cáo — không từ memory. Bar ngang
cho cột B dùng div CSS (`.hbar-track` + `.hbar.b/.ok/.no`), không cần SVG.

## Workflow

1. **Đọc nguồn đầy đủ** — docx dùng read_file (auto-extract), đọc hết cả phần sau truncate (offset tiếp).
2. Trích 4 KPI tốt nhất + bảng dữ liệu + bảng tần suất + kết luận + bước tiếp theo + người ký.
3. **Hỏi số liệu kinh tế trước khi dựng**: chi phí hiện tại (đơn vị?), giá sản phẩm (đ/kg hay đ/bao?), liều dùng. Chốt rồi mới tính tiết kiệm %.
4. Dựng File A + File B (write_file). Verify local: serve HTTP (`python -m http.server <port> --bind 127.0.0.1` background, camofox chặn file://), browser_navigate, check overflow `document.documentElement.scrollWidth == window.innerWidth`, chart bars count = 6/chart.
5. **Screenshot bằng playwright-core** khi vision model không có/chết (xem skill `camofox-browser` references/screenshot-local-html.md) — script .cjs trong camofox-browser, dùng chromium ms-playwright, chụp fullPage cả 2 file.
6. Publish cả 2 bằng `publish` skill → verify HTTP 200 + snapshot nội dung chính.

## Pitfalls

- **`/api/store` trả 403 khi gọi thẳng urllib/requests** — dùng `content-upload.py` của skill publish (nó gọi đúng và tự unslop; kiểm tra `unslopped:true` rồi verify layout sau publish vì unslop có thể đổi HTML).
- **Biểu đồ đường nhiều chuỗi phải dựng SVG nội tuyến, không dùng ảnh matplotlib** — và chữ trong SVG **co theo viewBox**, không phải px: đặt viewBox rộng bằng `max-width` desktop rồi font 19–20 đơn vị, và phải đo lại ở khung 280–300 px chứ không tin mắt trên desktop. Toàn bộ cách làm (nhãn trục số tròn, kiểu nét cho từng chuỗi, cách đo khi không resize được viewport): skill `inline-svg-charts`.
- **`tool_search` browser_vision báo 401 Invalid token payload** = vision model config hết hạn → đừng kẹt, chuyển playwright-core screenshot ngay.
- **port kẹt 2 process** khi start http.server nhiều lần → kill cả 2 PID qua `powershell Stop-Process -Id` trước khi start lại (git-bash taskkill bị path-conversion nuốt `/`).
- **Số liệu nguồn có thể nhập nhằng** (vd "giảm 59%" so với đầu vào hay so với ngày 7) — đối chiếu từng con số với bảng gốc, nếu mâu thuẫn ghi chú thích đầy đủ thay vì chọn bừa.
- **DOCX nhiều bảng/bảng sâu → read_file auto-extract có thể thiếu cấu trúc bảng** — decode thẳng `word/document.xml`: python `zipfile` + regex `w:tbl`/`w:tr`/`w:tc`/`w:t` ra từng bảng đầy đủ (đã dùng cho báo cáo CT888, 14 bảng gồm cả bảng Δ% và đối chứng). Lấy số liệu gốc từ đây, không từ memory.
- Model không nhận image (deepseek-flash `unknown variant image_url`) → browser_vision/vision_analyze fail; dùng DOM measure + screenshot cho user tự xem.
- Humanizer vẫn áp dụng: không em dash (—) trong nội dung, không emoji trang trí, không lạm dụng bold — bài formal càng phải sạch.

## References

- `references/xuanthien-ct888-trial.md` — hồ sơ thử nghiệm EZ-CT888 tại Xuân Thiện Thanh Hóa (thông số, kinh tế, KPI, mốc tiếp theo 21/30) — mẫu hoàn chỉnh cho bài đã dựng

## Verification Checklist

- [ ] Đã chốt đơn vị kinh tế (đ/kg hay đ/bao, đ/m³) trước khi tính %
- [ ] File A: pageH ≤ ~1123px (A4 @96dpi), không tràn trang 2
- [ ] Cả 2 file: `scrollWidth == innerWidth` trên desktop
- [ ] Số liệu từng bar/bảng đối chiếu đúng báo cáo gốc (không bịa)
- [ ] Publish 2 link, HTTP 200, snapshot xác nhận nội dung chính
- [ ] Screenshot đã gửi user kèm 2 link preview