# Board B2B Sale — Kiềm Saphia (ví dụ đã publish 07/09/2026)

Ví dụ hoàn chỉnh của quy trình trello-board-publish: dựng trang HTML bán hàng B2B từ board Trello thật.

## Board
- Tên: B2B Sale
- Board ID: `6a9e30aa11891777725b9a0e`
- URL: https://trello.com/b/jdP0O9AQ/b2b-sale
- Short link: `jdP0O9AQ`
- Kết quả publish: https://preview.thefirstonly.com/dgf6spk4bap3
- File nguồn: `D:/Hermes Proj/.hermes-state/b2b_data.json` (fetch API thật), HTML `b2b-sale-publish.html`

## Lists (thứ tự pipeline chuẩn — sort by pos, API trả về lộn xộn nếu không sort)
1. Lead / Khách tiềm năng — `6a9e32a0f7c2547676d17f36`
2. Đã liên hệ — `6a9e32a2f8b2cfda11976cfa`
3. Đã báo giá — `6a9e32a3b72cdffd2e42ee13`
4. Đàm phán — `6a9e32a44995ba043a119e24`
5. Chốt đơn — `6a9e32a792fe88a60e90a8c1`
6. Thất bại — `6a9e32e985688e0897865a95`
7. Chờ quyết định — `6a9e32eaa9f5e36a31aa2965`

## Labels (8)
| Tên | Color | Hex |
|-----|-------|-----|
| Lợn | blue | `#0079bf` |
| Trại trực tiếp | green | `#61bd4f` |
| Tập đoàn | green_dark | `#4b8f3c` |
| Thủy sản | orange | `#ff9f1a` |
| Cty Cám | pink_light | `#ff78cb` |
| Gia cầm | yellow | `#f2d600` |
| Trâu bò | purple | `#c377e0` |
| Đại lý/NPP | red | `#eb5a46` |

## Cards (4, tất cả ở Lead lúc publish)
1. **Trại Xuân Thiện - EZ80 - 50 bao - Cty** (card `77SCSVbs`) — label Lợn + Tập đoàn — desc: anh Hiếu, Đại lý/NPP, ~500 nái + lợn thịt, EZ80 bột, 50 bao 10kg, 1.250.000đ/bao
2. **Cty Công Danh** (card `PnL2dgxi`) — label Lợn + Trại trực tiếp — cô Dung, 3000 con, quan tâm EZ80/EZ67
3. **Cám Vina Ez80** (card `LdJrW9Or`) — label Cty Cám + Gia cầm + Thủy sản + Lợn — Ms Hương (phòng thu mua), <PHONE>
4. **Tên khách - Sản phẩm - SL - Loại (template mẫu)** (card `UPGeZ5f1`) — template trống để copy

## Ghi chú triển khai
- Dùng `execute_code` fetch (urllib + json, creds `~/AppData/Local/hermes/.env` strip `\r`) — bash heredoc qua terminal bị chặn consent gate.
- Board này do session "Thêm sheet track công thức mới" (07/09, session `20260907_102304_cbdfd2e1`) dựng: tạo 7 lists theo ORDER + xóa 6 label trống tên + sửa pos list (nhân 65536) + 2 thẻ mẫu.
- Cấu trúc desc thẻ: `📍 Khách | 👤 Người liên hệ | 📞 SĐT/Zalo | 🏠 Loại khách | 🐖 Vật nuôi | 📦 Sản phẩm quan tâm | 🛒 Số lượng | 💵 Đơn giá | 📝 next step`.