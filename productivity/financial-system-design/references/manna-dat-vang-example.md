# Manna Đất Vàng — Concrete Implementation Example

This is the actual sheet built for Vua Kiềm / Manna Đất Vàng. Use as a template for other companies.

## Company context

- **Công ty:** Manna Đất Vàng (Vua Kiềm)
- **MST:** 0109767318
- **Địa chỉ:** 1111 Ngô Gia Tự, Việt Hưng, Long Biên, Hà Nội
- **Sản phẩm:** EZ80 (bột), EZ67 (nước), Nguyên liệu Kiềm Khoáng Thảo Mộc, Virusto, Bột kiềm nhão, Kiềm thủy sản

## Sheet ID

`<SHEET_ID>`

## Tab structure

| Tab | SheetId | Purpose |
|-----|---------|---------|
| HDSD | 0 | Instructions |
| DOANHTHU | 1923499204 | Daily revenue |
| CHIPHI | 2119510230 | Daily expenses |
| CONGNO | 1241539106 | Receivables/payables |
| DASHBOARD | 941186403 | Auto-summary |
| KETOAN | 525391729 | For accountant |

## Column definitions

### DOANHTHU
A: Ngày, B: Mã đơn, C: Khách hàng, D: Sản phẩm, E: Nhóm SP (EZ80/EZ67/Kiềm KM/Virusto/Bột kiềm/Kiềm TS/Khác), F: SL, G: Đơn giá, H: Thành tiền, I: Đã thu (C/K), J: Ngày thu, K: Ghi chú

### CHIPHI
A: Ngày, B: Mô tả, C: Nhà cung cấp, D: Nhóm CP (NVL/Nhân công/Vận chuyển/Marketing/VP/Thuế/Khác), E: Số tiền, F: Hình thức (Tiền mặt/CK), G: Hóa đơn (C/K), H: Ngày TT, I: Ghi chú

### CONGNO
A: Đối tác, B: Loại (Phải thu/Phải trả), C: Số HĐ, D: Số tiền, E: Ngày PS, F: Hạn TT, G: Ngày TT, H: Trạng thái (Chưa TT/Đã TT/Quá hạn), I: Ghi chú

### DASHBOARD formulas (key ones)
- H5 (Doanh thu): `=SUM(DOANHTHU!H2:H501)`
- H6 (Đã thu): `=SUMIF(DOANHTHU!I2:I501,"Có",DOANHTHU!H2:H501)`
- H7 (Tổng chi phí): `=SUM(CHIPHI!E2:E501)`
- H10 (Lợi nhuận gộp): `=H5-H7`
- H13 (Phải thu): `=SUMIFS(CONGNO!D2:D501,CONGNO!B2:B501,"Phải thu",CONGNO!H2:H501,"Chưa TT")`
- H14 (Phải trả): `=SUMIFS(CONGNO!D2:D501,CONGNO!B2:B501,"Phải trả",CONGNO!H2:H501,"Chưa TT")`
- EZ80 revenue: `=SUMIF(DOANHTHU!E2:E501,"EZ80",DOANHTHU!H2:H501)`

## Formatting applied
- Header row: yellow background (#FFD700), bold, centered
- Freeze top row on all data tabs
- Dashboard: section headers in light yellow, number format #,##0
- Column widths: proportional to content (see build script for exact px)

## Build script
`C:\Users\NTQUANG_DELL\AppData\Local\hermes\scripts\build_manna_sheet.py`

To rebuild for a different company: copy the script, update company name + product categories + sheet title.
