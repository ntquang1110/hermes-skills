# Ví dụ hoàn chỉnh: Xe 1 tỷ — Thuê Lotte Rental vs Vay ngân hàng (08/2026)

Case mẫu đã chốt, dùng làm template cho các case thuê/mua sau.

## Dữ kiện gốc từ user

- Giá xe: 1.000.000.000đ
- **Option 1 Vay mua:** trả trước 30% = **300.6 triệu** (số lẻ thật từ quote, đừng làm tròn 300), vay 699.4 triệu, trả ~20 mấy triệu/tháng
- **Option 2 Thuê Lotte:** cọc **80 triệu** (trả lại cuối kỳ), thuê **20 triệu/tháng** × 36 tháng = 720 triệu, bảo dưỡng bên thuê trả

## Điều khoản Lotte đã hỏi (6 câu chuẩn)

1. Cọc trả lại cuối kỳ: CÓ → cọc chỉ là ký quỹ, thêm chi phí cơ hội
2. Quyền mua lại cuối kỳ: CÓ nhưng **giá theo thị trường** → vô nghĩa tài chính
3. Giới hạn km: **20.000 km/năm**, phạt vượt **2.000-5.000đ/km**
4. Bảo dưỡng/sửa chữa định kỳ: bên cho thuê trả
5. Chấm dứt sớm: phạt **15%**
6. Bảo hiểm vật chất: không bắt buộc mua qua bên cho thuê

## Dữ kiện sử dụng (quyết định tất cả)

- Chạy thực tế: **1.000 km/tuần = ~52.000 km/năm** (gấp 2.6 lần cap)
- Vượt: 32.000 km/năm × 3 năm = 96.000 km
- Phạt 3 năm: 96.000 × 2.000đ = **192 triệu** (min) đến 96.000 × 5.000đ = **480 triệu** (max)

## Script output (execute_code, amortization)

```
lai 9% / 36 thang: 22.2M/thang | tong tra 801M | lai 101M | tong chi 1101M
lai 10% / 36 thang: 22.6M/thang | tong tra 812M | lai 113M | tong chi 1113M
lai 12% / 36 thang: 23.2M/thang | tong tra 836M | lai 137M | tong chi 1137M
lai 10% / 48 thang: 17.7M/thang | tong tra 851M | lai 152M | tong chi 1152M
lai 10% / 60 thang: 14.9M/thang | tong tra 892M | lai 192M | tong chi 1192M
```

Base case: 10%/năm, 36 tháng → 22.6 triệu/tháng, tổng chi 1.113 triệu.

Lãi giảm dần: tháng 1 = 5.8 triệu, tháng 12 = 4.2, tháng 24 = 2.3, tháng 36 = 0.2 (dư nợ giảm dần).

## Chi phí thực (terminal value)

- **Residual:** xe chạy 156.000 km/3 năm → chỉ còn **45-50% = 450-500 triệu** (không dùng 55-65% của xe đi ít)
- **Thuê:** 720 (thuê) + 21 (cơ hội cọc 80M @8%/3 năm) + phạt 192-480 = **930-1.220 triệu**, terminal = 0
- **Mua:** 1.113 (trả góp) + 45 (bảo dưỡng) − 450-500 (bán xe) = **660-710 triệu**
- **Chênh: 220-560 triệu nghiêng về vay mua**

Opportunity cost thêm nếu tính: 220.6 triệu chênh trả trước @8%/3 năm = 57 triệu → mua vẫn thắng.

## P&L hàng tháng (góc kế toán)

Khấu hao 8 năm = 10.4 triệu/tháng. Mua: tháng 1 = 5.8 + 10.4 = 16.2M; tháng 36 = 0.2 + 10.4 = 10.6M. Thuê = 20M cố định. → Mua ghi nhận chi phí THẤP HƠN thuê dù dòng tiền cao hơn.

## Kết luận case

- **Chọn vay mua.** Rẻ hơn 220-560 triệu sau 3 năm + có tài sản trên sổ + không giới hạn km + không phạt chấm dứt sớm
- Thuê chỉ hợp khi: không có sẵn 300 triệu, hoặc vốn sinh lời > 20%/năm
- "Mua lại giá thị trường cuối kỳ": thuê 720 + mua lại 600 = 1.320 triệu vs mua thẳng 1.113 triệu → kém 207 triệu
- Lưu ý khi mua: xe tiêu hao thấp (diesel/hybrid) vì chạy 52k km/năm — chênh 1-2 lít/100km = 40-80 triệu/năm; chi phí vận hành 20-30 triệu/năm

## Cấu trúc HTML đã chốt (bản publish cuối: preview.thefirstonly.com/wm7y7ais2xj4)

- Header h1 + lead
- Section "Hai lựa chọn": grid 2 cột `.options`, mỗi cột `.option.buy` (viền vàng, tag vàng "Option 1") / `.option.lease` (tag xám "Option 2"), 9 metric ngang hàng + `.metric.total` chi phí thực + `.foot`
- Section "Vấn đề nằm ở số km": `.km-note` số to đỏ 32.000 km + phạt 192-480 triệu
- Section "Tổng chi phí thực sau 3 năm": `.chart` 2 bars (thuê 97.6% đỏ vs mua 56.8% vàng, scale 1.250) + `.diff` chênh 220-560 triệu
- Section "Tài sản và sổ sách": 2 `.point` cards
- `.verdict` card vàng: tag Kết luận + "Chọn vay mua" + lý do + bullets
- `.assume` chân trang: giả định (lãi 10%, residual 45-50%, phạt 2-5k/km, chưa gồm VAT/bảo hiểm/đăng ký)
- File gốc: `D:\Hermes Proj\so-sanh-xe-thue-vs-vay.html`
