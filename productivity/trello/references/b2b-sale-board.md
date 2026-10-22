# B2B Sale board (Trello) — cấu trúc pipeline đề xuất + đã dựng 07/09/2026

Board: **B2B Sale** · `https://trello.com/b/jdP0O9AQ/b2b-sale`
- id: `6a9e30aa11891777725b9a0e`
- Thuộc workspace `tqws` của tài khoản Tee Kwang (ntquang1110). Bước đầu `GET /boards/jdP0O9AQ` trả 401 vì chưa được add — chờ user add rồi check lại, KHÔNG kết luận "board chết".

## Lists (7, thứ tự pipeline bán hàng Kiềm Saphia)

1. Lead / Khách tiềm năng
2. Đã liên hệ
3. Đã báo giá
4. Đàm phán
5. Chốt đơn
6. Thất bại
7. Chờ quyết định (optional: khách chờ phê duyệt nội bộ)

## Labels (6) — phân loại nhanh

- Loại vật nuôi: **Lợn** (blue) · **Gia cầm** (yellow) · **Thủy sản** (orange) · **Trâu bò** (purple)
- Kênh: **Đại lý/NPP** (red) · **Trại trực tiếp** (green)

## Card title rule

```
[Khách hàng] - [Sản phẩm] - [SL dự kiến] - [Loại]
VD: Trại Xuân Thiện - EZ80 - 50 bao - Cty
```

## Template desc (paste vào mỗi card)

```
📍 Khách: _______________
👤 Người liên hệ: ________
📞 SĐT/Zalo: ________
🏠 Loại khách: [Trại trực tiếp | Đại lý | NPP]
🐖 Vật nuôi: _______ SL chuồng: _______
📦 Sản phẩm quan tâm: EZ80 / EZ67 / Kiềm kháng / Virusto / khác
🛒 Số lượng dự kiến: _______
💵 Đơn giá TS/đề xuất: _______
📝 Nhu cầu/băn khoăn: _______
📎 Link báo cáo/khảo nghiệm đã gửi: _____
🗓 Next step + ngày: _______
```

## Lý do KHÔNG dùng Custom Fields

Custom Fields là tính năng trả phí (Standard trở lên). Bản Free dùng được nhưng rủi ro giới hạn — quyết định 07/09/2026: đóng gói thông tin trong tiêu đề + labels + template desc, không phụ thuộc Custom Fields. Tránh kẹt khi board bị hạ gói hoặc chủ board không trả phí.

## Thẻ mẫu đã tạo trong Lead (làm ví dụ/template)

- `Trại Xuân Thiện - EZ80 - 50 bao - Cty` (labels: Lợn + Đại lý/NPP, desc đầy đủ)
- `Tên khách - Sản phẩm - SL - Loại (template mẫu)` (template trống để copy)