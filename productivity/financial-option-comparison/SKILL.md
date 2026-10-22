---
name: financial-option-comparison
description: "Compare financial options (lease vs buy). Then build HTML."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [finance, comparison, lease, buy, decision, html, presentation, tài chính]
    related_skills: [content-publish, impeccable, html-unslop, business-deal-evaluation]
---

# Financial Option Comparison (so sánh phương án tài chính)

Dùng khi user đưa 2+ phương án mua/thuê/vay cho 1 quyết định (xe, máy móc, thiết bị, bất động sản) và muốn "phân tích sâu để chốt". Flow chuẩn: **số thật → kết luận → HTML trái/phải → publish**.

## Bước 1. Chốt số gốc — hỏi đủ trước khi tính

Đừng phân tích trên số mơ hồ. Hỏi/đòi đủ:

1. Giá trị tài sản, % trả trước, số tiền trả trước chính xác
2. Lãi suất vay, kỳ hạn (36/48/60 tháng), trả gốc lãi đều hay dư nợ giảm dần
3. Điều khoản bên cho thuê (6 câu chuẩn):
   - Cọc có trả lại cuối kỳ không?
   - Quyền mua lại cuối kỳ? Giá theo thị trường hay giá chốt trước?
   - Giới hạn km/năm? Phạt bao nhiêu/km vượt?
   - Bảo dưỡng, sửa chữa ai trả, bắt buộc ở đâu?
   - Chấm dứt sớm phạt bao nhiêu %?
   - Bảo hiểm vật chất có bắt buộc mua qua bên cho thuê không?
4. **Số km/giờ sử dụng thực tế mỗi tuần** — quyết định phạt km. Hỏi sớm, vì nó đổi kết luận.
5. Xe/thiết bị dùng cho công ty hay cá nhân (góc kế toán khác nhau)

## Bước 2. Tính toán chính xác bằng execute_code — không đoán số

Viết script amortization (công thức gốc lãi đều: `P*r*(1+r)^n / ((1+r)^n - 1)`), output bảng:

- Khoản trả mỗi tháng × lãi suất (9/10/12%) × kỳ hạn (36/48/60 tháng)
- Tổng trả = gốc + lãi; tổng chi = trả trước + tổng trả
- Lãi tháng đầu vs tháng cuối (dư nợ giảm dần) — dùng cho góc P&L

Mọi con số đưa lên trình bày phải từ kết quả script, không ước lượng mồm.

## Bước 3. Chi phí thực = tổng chi − giá trị còn lại (terminal value)

Lỗi phổ biến: so tổng chi thuần. Phải trừ giá trị tài sản còn lại cuối kỳ:

- Thuê: terminal value = 0 (trả xe) — nếu cọc trả lại thì cộng thêm chi phí cơ hội cọc (cọc × lãi suất cơ hội × số năm)
- Mua: terminal value = giá bán lại. **Residual giảm theo km**: xe chạy 156.000 km/3 năm chỉ còn 45-50% (không phải 55-65% như xe đi ít)
- Thêm chi phí cơ hội của khoản vốn bỏ ra thêm (chênh trả trước × ~8%/năm × số năm)
- So sánh chi phí thực 2 bên, ra con số chênh lệch dứt khoát

## Bước 4. Lượng hóa rủi ro điều khoản thành tiền

"Khắc khe về hợp đồng" phải thành con số:

- Phạt vượt km: (km thực tế − km giới hạn) × phạt/km × số năm. Chạy 52k km/năm với cap 20k = phạt 192-480 triệu/3 năm → nuốt sạch lợi thế dòng tiền của thuê
- Chấm dứt sớm %, phạt trả xe trễ, bảo hiểm bắt buộc đắt hơn thị trường

## Bước 5. Góc kế toán / sổ sách

- Thuê (operating lease): chi phí hàng tháng vào P&L, bảng cân đối không có tài sản, không thế chấp được
- Mua: TSCĐ ghi sổ, khấu hao (ô tô 6-10 năm, thường 8 năm → 10.4 triệu/tháng cho xe 1 tỷ), lãi vay là chi phí tài chính. Điểm hay: **chi phí P&L hàng tháng của mua (khấu hao + lãi giảm dần) thường THẤP HƠN tiền thuê** dù dòng tiền cao hơn
- Quyền mua lại "giá thị trường" cuối kỳ = vô nghĩa về tài chính: thuê 3 năm + mua lại giá thị trường luôn đắt hơn mua thẳng (chênh ~200 triệu)

## Bước 6. Rule quyết định rõ

Đưa threshold, không nói chung chung:

- Mua thắng khi có sẵn tiền trả trước VÀ vốn đó sinh lời < ~15-20%/năm
- Thuê chỉ hợp khi: thiếu vốn ban đầu, hoặc vốn sinh lời > threshold, hoặc dùng ngắn hạn đúng kỳ hạn
- Nếu phạt theo mức sử dụng cao → mua gần như luôn thắng

## Trình bày HTML — format trái/phải (user đã duyệt, bắt buộc)

Quang yêu cầu: **so sánh trái/phải, mỗi option 1 card riêng, nhìn ngang thấy chênh lệch, kết luận cuối trang**:

- Option 1 (trái) vs Option 2 (phải), mỗi bên 1 card riêng biệt với tag "Option 1"/"Option 2"
- Các metric xếp **cùng thứ tự, ngang hàng** giữa 2 cột: vốn ban đầu, trả tháng, tổng kỳ hạn, cuối kỳ, giới hạn sử dụng, phạt, sổ sách, chi phí thực
- Winner: viền + tag vàng; loser: đỏ cho điểm bất lợi, xám cho trung tính
- Số lớn, sub-note nhỏ (small) giải thích
- Kết luận: card vàng full width cuối trang (tag "Kết luận" + heading "Chọn X" + lý do + bullets)
- Chân trang: mục "Giả định" (lãi suất, residual, phạt, chưa gồm VAT/bảo hiểm/đăng ký) — trình bày minh bạch
- Mobile: 2 cột xếp dọc (media query ≤700px)
- Theme B/W/Y đã duyệt: nền #0D0D0D, surface #1B1B1D, viền #2D2D32, vàng #FFD600, đỏ #FF6B6B, system-ui font. Không emoji, không em dash, tiếng Việt có dấu
- Thêm section "Vấn đề nằm ở X" (con số rủi ro to đỏ) nếu có 1 yếu tố quyết định

## Publish pipeline

1. Viết HTML → `python .../html-unslop/scripts/unslop-html.py --file X.html --check` (phải ra "No AI design tells detected")
2. `python .../content-publish/scripts/content-upload.py --file X.html --title "..."` → lấy preview_url (KV backend, không cần PAT)
3. Verify: browser_navigate preview URL → đọc snapshot đủ nội dung → chạy ui-audit.js qua browser_console (vision model qua opencode-go hay fail với `image_url` → dùng detector DOM, đã được impeccable ghi chú)
4. Trả link + tóm tắt + nhắc giả định cần xác nhận (lãi suất thật của ngân hàng) để cập nhật số

## Pitfalls

1. **Đừng so tổng chi thuần** — luôn trừ terminal value. Chênh lệch sau trừ thường đổi hẳn kết luận
2. **Residual theo km thực tế**, không theo khung mặc định
3. **Hỏi km/tuần sớm** — phạt km là cái bẫy chí mạng của hợp đồng thuê
4. Số lẻ user đưa (300.6 triệu) thường là số thật từ quote — đừng làm tròn thành 300, dùng đúng
5. Kết luận phải có con số chênh lệch (220-560 triệu), không nói "rẻ hơn đáng kể"
6. Chưa bao giờ giả định user muốn bảng hàng ngang — format trái/phải là chuẩn đã duyệt

## Support files

- `references/lease-vs-buy-car-2026.md` — ví dụ đầy đủ: xe 1 tỷ, Lotte Rental vs vay ngân hàng, toàn bộ số liệu + script output + cấu trúc HTML đã chốt
