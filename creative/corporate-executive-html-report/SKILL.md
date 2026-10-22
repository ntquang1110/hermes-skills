---
name: corporate-executive-html-report
description: "Formal Vietnamese HTML report for execs and partners."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [html, report, executive, corporate, vietnamese, design, qcvn]
    related_skills: [impeccable, visual-academic-html, publish, claude-design]
---

# Corporate / Executive Report HTML (VN formal)

HTML báo cáo formal gửi **chủ tịch / lãnh đạo tập đoàn / đối tác lớn**: báo cáo thử nghiệm
khảo nghiệm, tổng kết dự án, đề xuất hợp tác, tài liệu bán hàng B2B.

## Trigger

- User đưa file báo cáo (docx/pdf) hoặc số liệu thử nghiệm → muốn "bản Visualize dễ hiểu + formal để gửi chủ tịch".
- User nói "gửi cho Chủ tịch tập đoàn X", "đối tác lớn", "bán ngược", "chủ tịch hiểu nhanh".
- User nhờ **hướng dẫn nghiệp vụ cho bộ phận** (kế toán, pháp lý, vận hành) — xem mục *Audience contract* bên dưới.
- KHÁC bài academic KFlow (thứ đó vẫn là 2-tab B/W/Y tối, skill `visual-academic-html`).

## Lịch sử xác nhận (bắt buộc đọc)

Báo cáo EZ-CT888 xử lý nước phân thải gửi Chủ tịch Xuân Thiện (09/2026): bản đầu
(nền trắng + card xám + viền+shadow chồng, Segoe UI, kicker, số section 01/02/03,
checkmark "✓", text 9.5px) bị user chê **"trông xấu quá"**. Bản được duyệt theo pattern
dưới. Đừng lặp lại sai lầm bản đầu.

## Design tokens (đã chốt)

| Token | Giá trị | Ghi chú |
|---|---|---|
| Nền giấy | `#FBFBF8` | light paper, KHÔNG dark |
| Ink | `#16211C` | body text |
| Muted | `#5C6B63` | phụ |
| Accent chính | `#1D5C3E` (forest) | thương hiệu/ngành |
| Accent nhấn | `#C89B3C` (gold) | điểm nhấn "tiết kiệm", số nổi |
| Hairline | `#E5E7E0` / `#D3D8D2` | elevation = hairline, KHÔNG shadow |
| Font | Be Vietnam Pro (Google Fonts) | display 800, body 400/500, đủ dấu tiếng Việt |
| Radius | 12px | gom ramp |

Elevation rule: 1px border HOẶC shadow, không cả hai (ghost card bị chê).

## Cấu trúc "kết quả trước" (chủ tịch đọc quyết định, không đọc quy trình)

1. **Masthead**: tên công ty + loại tài liệu + mốc thời gian, hairline dưới.
2. **Statement 1 dòng**: kết quả to nhất, KHÔNG kicker trên heading.
3. **KPI strip**: 4 ô số lớn (30px+) kẻ hairline giữa — chỉ tiêu + vị trí + % (sup) + cặp trước→sau.
4. **So sánh kinh tế**: bảng 3 ô (hiện trạng / sản phẩm / tiết kiệm) — đổi ra đ/m³, đ/kg. Tiền nhanh hơn mg/L với chủ tịch.
5. **Ý nghĩa với họ**: 4 check SVG tròn xanh (KHÔNG checkmark text, KHÔNG emoji).
6. **Vì sao hiệu quả**: 1 đoạn ngắn + flow chips `A → B → C → D` (mũi tên gold).
7. **Footer**: đơn vị thực hiện, cán bộ phụ trách, người viết.

File A = 1 trang A4 chốt nhanh; File B = báo cáo đầy đủ (kèm chart, bảng pH, tần suất).
Publish cả 2 lên preview.thefirstonly.com bằng script `publish` skill (KHÔNG tự POST urllib — 403).

## Claims trung thực (tránh bị bắt bài)

- Số liệu GIỮ NGUYÊN nguồn, không bịa %.
- Nói "giảm X% tải ô nhiễm ở đầu hệ thống" chứ KHÔNG "đạt chuẩn xả thải" nếu chưa đạt QCVN.
- Cơ chế chưa công bố (vd kim loại hiếm/đất hiếm): ghi "cần kiểm chứng", không hứa với khách.
- Phân loại độ tin cậy cơ chế: 🟢 Đã chứng minh / 🟡 Khả dĩ / 🔴 Cần kiểm chứng.

## Bộ 5 trang cho 1 chiến dịch đối tác (đã chốt 09/2026, Xuân Thiện)

Khi user muốn thuyết phục chủ tịch + cấp kỹ thuật + bản thân hiểu sâu, đừng dồn 1 trang.
Chia vai trò thành 5 file HTML riêng, mỗi file 1 mục đích, publish từng link:

1. **File A** — 1 trang A4 "chốt nhanh" (statement + 4 KPI + kinh tế). Thứ gửi chủ tịch.
2. **File B** — báo cáo đầy đủ (9 khối: tóm tắt → kinh tế → bối cảnh → charts từng chỉ tiêu → pH → tần suất CT1/CT2 → ý nghĩa → vì sao → bước tiếp). Thứ gửi cấp kỹ thuật/ban môi trường.
3. **Trang giải thích chỉ số** — BOD/COD/TSS là gì, vì sao cao là hại, bảng QCVN 62, đối chiếu với số liệu trial (đọc "dưới chuẩn / trên chuẩn" cột nào). Giúp user tự tin phát biểu.
4. **Trang cơ chế sâu** — từng thành phần sản phẩm đóng góp gì + phân loại tin cậy 🟢/🟡/🔴 + đòn bẩy tối ưu không hóa chất (sục khí / bioaugmentation EM-bacillus / lắng thêm bậc / phối trộn đúng vị trí).
5. **Trang đề xuất thí nghiệm** — kế hoạch kiểm chứng (xem mục bên dưới).

Kèm 1 trang **visualize cơ chế** kiểu "chuyện gì xảy ra khi đổ bột vào bể": big-flow 3 bước
(Nước bẩn → Rắc EZ-CT888 → Nước sạch hơn) + 5 thẻ thành phần icon SVG + hộp chốt "bản chất 1 câu".
Trang visual này đúng skill impeccable (0 tells), dùng SVG thay CSS bar.

## Đề xuất thí nghiệm tiếp theo (4 bể song song, 30 ngày)

Sau báo cáo giai đoạn 1 thành công, pattern chốt tiến độ với đối tác lớn: thí nghiệm so sánh
4 công thức song song, cùng nguồn nước/volume/thời điểm, chỉ khác 1 biến mỗi bể:

| Bể | Công thức | Kiểm chứng |
|---|---|---|
| A | Liều cũ (150kg/1.000m³) | đối chứng, xác nhận lặp lại |
| B | Liều cũ + **sục khí tăng cường** | "kiềm + khí" (Arkansas 2023) |
| C | Liều cũ + **vi sinh bổ sung** (EM/bacillus sau khi pH về 7-9) | "kiềm dọn nhà, vi sinh ăn sau" |
| D | **Liều cao hơn** (200kg/1.000m³) | tăng liều tuyệt đối có đáng chi phí |

Nguyên tắc: cố định mọi thứ khác, lấy mẫu sau **lắng 60 phút** (tránh nhiễu sinh khối hồ air),
mốc đo 0/7/15/30, chụp ảnh mỗi mốc. Tiêu chí quyết định theo kịch bản: B/C vượt A → đầu tư
khí+vi sinh không phải liều; D giảm đáng kể → tính điểm cân bằng chi phí–hiệu quả; cả 4 tương
đương → giới hạn ở hạ tầng (thời gian lưu, tải trọng). Đề xuất này tránh cạm bẫy "cứ tăng liều"
khi giới hạn thật của hệ thống là sục khí + hệ vi sinh.

## Chart recipe

SVG inline render bằng JS: gridline 4 mức + axis mg/L + bar 3 nhóm (ĐC/CT1/CT2) × 2 mốc,
giá trị trên bar. Màu: `#9DA89F` ĐC, `#8FBBA4` CT1, `#1D5C3E` CT2. Legend 3 ô đầu chart.
KHÔNG dùng CSS bar tay (nhìn amateur).

## Kiến thức miền bắt buộc (nước thải chăn nuôi — research 09/2026)

- **BOD5**: oxy vi sinh tiêu thụ phân hủy chất hữu cơ (5 ngày, 20°C). Cao → nguồn tiếp nhận cạn oxy → cá chết, kỵ khí → H₂S/metan hôi. BOD cao = tốn điện sục khí, bể to.
- **COD**: oxy oxy hóa TOÀN BỘ hữu cơ bằng hóa chất, luôn ≥ BOD5. Tỷ lệ BOD/COD quyết định chọn công nghệ.
- **TSS**: hạt >2µm (hữu cơ, sét, vi khuẩn, tảo). Hại: cản khử trùng (vi khuẩn ẩn trong hạt khỏi clo/UV), chặn ánh sáng quang hợp, bồi lắng, mang N/P/kim loại nặng.
- **QCVN 62-MT:2016/BTNMT** (nước thải chăn nuôi, Bảng 1): BOD5 40/100, COD 100/300, TSS 50/150, Tổng N 50/150, pH 6-9/5,5-9, Coliform 3000/5000. Cột A = nguồn cấp nước sinh hoạt, cột B = nguồn không cấp nước sinh hoạt.
- **Hồ sục khí (M3) COD/TSS đi ngang ≠ sản phẩm kém**: sinh khối vi sinh + tảo "sống" làm mẫu đo cao; quy trình chuẩn có bể lắng cuối trước khi đo/xả. Mốc sau: đo ở bể lắng sau hồ air hoặc lắng 30-60 phút trước lấy mẫu.
- **Cơ chế sản phẩm kiềm khoáng**: kiềm pH>12 thủy phân hữu cơ + Ca/Mg keo tụ TSS (đã chứng minh); saponin = bio-surfactant mở đường vi sinh (khả dĩ); polyphenol/alkaloid ức chế vi khuẩn hôi (khả dĩ, thận trọng liều cao); kim loại hiếm La/Ce (cần kiểm chứng). Tối ưu không hóa chất: sục khí + bioaugmentation EM/bacillus + lắng thêm bậc + phối trộn đúng vị trí.
- **Nguồn research**: ccep.vn, moitruonghopnhat.com, primer.vn; QCVN qua hoabinhxanh.vn (thuvienphapluat 403); PMC (polyphenol), phys.org (alkaline pretreatment + air mixing Arkansas 2023).

## Audience contract: tài liệu BỘ PHẬN phải thực thi được

Khác với báo cáo lãnh đạo (kết quả trước), có một dạng tài liệu khác: **hướng dẫn nghiệp vụ nội bộ** —
kế toán, pháp lý, vận hành, sản xuất — bộ phận dưới đọc để LÀM, không phải để DUYỆT.

Khi brief có câu kiểu *"để bộ phận X hiểu bối cảnh để thực thi được toàn bộ nghiệp vụ và không phải
thắc mắc tại sao"*, đó là **audience contract**, không phải gợi ý. Ràng buộc cứng:

1. **ĐỦ ĐỂ LÀM** — có số liệu, thứ tự thao tác, tên chứng từ, số hiệu tài khoản / điều luật.
2. **MỖI BƯỚC MỘT LÝ DO** — "tại sao làm thế" nằm ngay tại chỗ, không dồn cuối bài.

Sai lầm phổ biến: viết cả loạt bước chỉ có "Làm gì" rồi kết bằng "hiểu rồi thì làm được".
Bộ phận kỹ thuật vẫn phải hỏi lại, và tài liệu mất tác dụng.

Bộ khung cho tài liệu nghiệp vụ:

| Mục | Nội dung |
|---|---|
| Bối cảnh | Bảng thông số đầu vào — bao nhiêu, ai, loại hình gì |
| Vì sao phải làm | Nguyên tắc luật + bảng so sánh phương án sai/đúng, lý do định lượng |
| Tính toán | Từng bước ra con số, tự kiểm lại được bằng máy tính |
| Nghiệp vụ | Bút toán / thao tác + "Tại sao" cho TỪNG bước, kèm chứng từ đi kèm |
| Thủ tục | B1..Bn, mỗi bước "Làm gì" + "Tại sao" |
| Kiểm soát | Checklist kiểm toán / rủi ro / trường hợp biệt lệ |
| FAQ | Câu bộ phận dưới hay hỏi nhất — trả lời thẳng |

### Bẻ cong số: luôn khai báo phần chênh

Tự làm tròn lại mọi con số ví dụ và nêu phần chênh + giải thích nó đi đâu. Ví dụ
`71.428 cp × 70.000 đ = 4.999.960.000 đ`, chênh 40.000 đ so với "5 tỷ" nêu ở brief: ghi rõ phần
chênh hấp thụ vào thặng dư vốn, chấp nhận được. Giấu đi thì bộ phận kế toán tự tính lại, thấy lệch,
và mất niềm tin vào cả tài liệu.

### Tự phản biện trước khi gửi

Quang hay yêu cầu *"tự phản biện xem có sai sót gì, nếu không sai thì chứng minh"*. Trả lời theo
bảng hạng mục (đúng / thiếu gì / mức rủi ro), kết bằng câu hỏi **có sửa publish lại không**.
Đừng tự sửa ngầm — anh muốn thấy phản biện trước khi duyệt.

### Design cho tài liệu kế toán / pháp lý

Không dùng design sticker/ngộ ngữ (Slush, Bold Poster) cho tài liệu bộ phận kế toán phải đọc để
làm việc thật — anh đã chê thẳng là "mát hết tiếng Việt rồi". Dùng thiết kế nghiêm túc: nhiều
khoảng thở, accent một màu, bảng số rõ. Theme **Blue Professional**: cream `#fdfae7`, accent
`#1e2bfa`, Inter 400–700 (không serif/mono), card bo 12px, section gạch chân 2px, step có left
rule 4px. Token đầy đủ: `references/professional-doc-tokens.md`.

### Sai tên thực thể

Tên công ty rất dễ trượt âm (anh đọc "Vô Kiềm" thành "Vua Kiềm"). Trước khi build, grep tên sẽ viết
vào mọi heading + footer, đối chiếu với nguồn. Một homophone sai lặp ở hero + footer làm cả tài liệu
trông như chưa ai duyệt.

### Publish

Skill `publish`, backend KV → `preview.thefirstonly.com/<id>`.
**Lưu ý path:** script upload chạy Python nên cần Windows-style path `"C:/Users/<user>/<file>.html"`,
không phải `/c/Users/...` (sẽ `FileNotFoundError` dù shell thấy file).

## Support files

- `references/sop-documentation-pattern.md` — Pattern chuyển đổi bộ SOP văn bản thành HTML tương tác: tabbed navigation, visual flow diagrams, checklist kiểm tra, kịch bản hỏi đáp mô phỏng thanh tra. Dùng kết hợp newsprint-design.
- `references/professional-doc-tokens.md` — Token 2 design nghiêm túc cho tài liệu bộ phận (Blue Professional) + gallery-token extraction khi không có file template.
- `references/equity-raise-accounting-vn.md` — Case học gọi vốn CTCP VN: 4111/4112, luật, thuế, bẫy làm tròn.
- `references/budget-limit-proposal-report.md` — Variant **đề xuất hạn mức ngân sách trình Chủ tịch** dựng từ budget sheet có sẵn: thứ tự 8 khối (masthead → H1 + lede → KPI strip 4 ô → 01 hạn mức theo phòng ban theo tháng + bảng dòng tiền → 02 nhóm chi phí + bar chart + 2 card đòn bẩy → 03 trần phê duyệt + flow chips hòa vốn → 04 rủi ro/kiến nghị → footer nêu tên tab nguồn), luật cứng (không bịa preview URL, mọi số truy về tab nguồn, nêu chênh lệch liên tab ra callout thay vì tự chọn một con), và bộ verify sau mỗi lần patch HTML (cân thẻ `div`, f-string không chứa backslash, assert live qua `browser_console`: jsErrors 0, không overflow ngang, 0 em dash). Dùng khi Quang hỏi "đề xuất hạn mức với chủ tịch".

## Verify

- Detector impeccable ui-audit: 0 tells, bodyContrast ≥ 4.5, radius gom 8/12/16.
- A4: `.page` offsetHeight ~1123px (297mm), không tràn trang 2.
- Preview HTTP 200 + đối chiếu từng con số với nguồn gốc.