# Giấy xác nhận đã nhận đủ tiền góp vốn — Capital Contribution Confirmation

**Cập nhật:** 2026-09-17 (từ case Trương Văn Thực + Khánh Ly — Manna Đất Vàng)

---

## Khi nào dùng

- Cá nhân/tổ chức góp vốn vào công ty cổ phần (JSC) hoặc công ty TNHH
- Cần văn bản xác nhận đã nhận đủ tiền góp vốn (không phải hợp đồng góp vốn)
- Dùng để làm căn cứ xác nhận tỷ lệ sở hữu vốn điều lệ

## Cấu trúc văn bản

| Phần | Nội dung | Ghi chú |
|------|----------|---------|
| **Quốc hiệu** | CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM / Độc lập – Tự do – Hạnh phúc | Tiêu đề chuẩn |
| **Tiêu đề** | GIẤY XÁC NHẬN ĐÃ NHẬN ĐỦ TIỀN GÓP VỐN | In đậm, căn giữa |
| **Căn cứ pháp lý** | Điều lệ Công ty + Hợp đồng góp vốn/Hợp đồng hợp tác kinh doanh + Biên bản họp HĐQT/quyết định ĐHĐCĐ | 2 căn cứ song song |
| **Bên nhận vốn (Công ty)** | Tên công ty, MST, địa chỉ, người đại diện PL | Để trống người đại diện nếu chưa xác định |
| **Bên góp vốn** | Họ tên, CCCD, ngày sinh, giới tính, dân tộc, tôn giáo, quê quán, thường trú | Map từ CCCD của bên góp |
| **Số tiền** | Số + chữ (VD: 1.000.000.000 đồng — Một tỷ đồng chẵn) | Ghi rõ bằng số và chữ |
| **Hình thức góp** | Tiền mặt / Chuyển khoản | Ghi cụ thể trong biên bản giao nhận kèm theo |
| **Ngày nhận** | ...../...../......... | Để trống nếu chưa xác định |
| **Tỷ lệ sở hữu** | ....% (tương ứng .... cổ phần) | Để trống nếu chưa xác định vốn điều lệ cuối cùng |
| **Cam kết** | Công ty cam kết sử dụng đúng mục đích, đúng pháp luật | Chuẩn |
| **Ký** | Bên góp vốn + Đại diện Công ty | 2 dòng ký riêng |

## CCCD field mapping

| CCCD field | Văn bản field | Ghi chú |
|------------|---------------|---------|
| Số định danh cá nhân | Số CCCD | 12 số |
| Họ, chữ đệm và tên | Họ và tên | Viết hoa đầy đủ từ CCCD |
| Ngày, tháng, năm sinh | Ngày sinh | Định dạng DD/MM/YYYY |
| Giới tính | Giới tính | Nam → "ông", Nữ → "bà" trong lời văn |
| Quê quán | Quê quán | Tỉnh/Thành phố đầy đủ |
| Dân tộc | Dân tộc | Ghi theo CCCD |
| Tôn giáo | Tôn giáo | "Không" nếu trống |
| Nơi thường trú | Nơi thường trú | Số nhà, phường, quận, TP đầy đủ |
| Ngày cấp | Ngày cấp CCCD | Format DD/MM/YYYY |

## Legal basis

- **Luật Doanh nghiệp 2020 (59/2020/QH14)** — Điều 112 (góp vốn thành lập), Điều 114 (xác nhận góp vốn)
- **Điều lệ Công ty** — quy định cụ thể về tỷ lệ, thời hạn, hình thức góp vốn
- **BLDS 2015 (91/2015/QH13)** — Điều 118 (góp vốn), Điều 119 (xác nhận thực hiện nghĩa vụ)

## Lưu ý khi soạn

1. **Người đại diện PL để trống** nếu chưa chốt — user tự điền sau
2. **Tỷ lệ sở hữu** cần biết vốn điều lệ chính thức để tính — nếu chưa xác định thì để trống
3. **Dùng giới tính** để chọn xưng hô trong lời văn: "ông" (Nam), "bà" (Nữ)
4. **2 bản riêng** cho mỗi bên góp vốn — không gộp chung dù cùng số tiền
5. Font: Times New Roman, size 13 (24 twip), căn lề chuẩn hành chính

## OCR CCCD → Văn bản workflow

1. User gửi ảnh CCCD (mặt trước, chip-based)
2. Dùng RapidOCR (venv python) extract text
3. Map fields theo bảng trên
4. Sinh .docx template bằng docx-js (npm)
5. Gửi file cho user + báo các trường còn trống cần điền
