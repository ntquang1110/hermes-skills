# HSNL (Hồ sơ năng lực) Brief — Pattern điền Google Sheets cho Marketing

Dùng khi Quang gửi link Google Sheets brief cho Marketing và yêu cầu đệ điền câu trả lời. Cấu trúc brief chuẩn: 14 câu hỏi, 5 section (THÔNG TIN CHUNG, VỀ NỘI DUNG, VỀ ĐỐI TƯỢNG, USP sản phẩm, VỀ HÌNH THỨC DESIGN), 5 cột (STT, Câu hỏi, Câu trả lời, Note, Link tài liệu).

## Các bước

1. **Probe sheet structure**: dùng `sheets_probe.py` (hoặc API) lấy tab names, sheetIds, row/col counts
2. **Read all rows**: đọc Brief!A1:E100 để lấy toàn bộ câu hỏi (có section headers xen kẽ)
3. **Xác định câu nào đã trả lời, câu nào chưa**: cột C (Câu trả lời) trống = cần điền, cột E (Link tài liệu) trống = có thể cần
4. **Điền câu trả lời từ nguồn dữ liệu**:
   - Thông tin công ty: trong skill `vua-kiem-corporate-strategy` (MST, địa chỉ, định giá, sản phẩm, đội ngũ)
   - Tài liệu preview: từ Files + link section của skill
   - Bằng chứng khoa học: VNUA 2022, research nội bộ
   - Thị trường: báo cáo bệnh lợn, Nghị định 211/2026, IMARC
   - Đối tượng: investor / đại lý / trại — xem phần "Khách mục tiêu" và "Chiến lược 24 tháng" trong skill

## Nội dung cốt lõi cho từng nhóm câu hỏi

### THÔNG TIN CHUNG (Q1-6)
- Q6 (Link folder): ghi các link preview có sẵn, đề nghị Quang tạo Google Drive folder. Đừng tự tạo folder.

### VỀ NỘI DUNG (Q7-8)
- Q7 (MUST HAVE): 9 hạng mục:
  1. Tổng quan công ty (Manna Đất Vàng CP JSC, MST, địa chỉ, vuakiem.com, tầm nhìn sứ mệnh)
  2. Sản phẩm cốt lõi (EZ80, EZ67, Nguyên liệu Kiềm Khoáng Thảo Mộc, Virusto)
  3. Cơ chế hoạt động (pH kiềm, giảm ETEC, khoáng điện giải, thảo dược kháng viêm)
  4. Bằng chứng khoa học (VNUA 2022, 15 PMID berberine, tỷ lệ phân thải)
  5. Thị trường (bệnh lợn VN, 195tr USD, Nghị định 211/2026 cấm AGP)
  6. Mô hình kinh doanh (Stage-Pack, giá 125k/kg, lãi gộp 70%)
  7. Đội ngũ (founder, chủ tịch danh dự, CCO, đối ngoại)
  8. Định hướng (EZ80-Start, EZ80-Sow, gói ASF)
  9. Kêu gọi đầu tư (định giá 112 tỷ, mục tiêu 24 tháng)
- Q8 (Outline tham khảo): link các tài liệu preview đã publish, gợi ý tham khảo HSNL đối thủ (GreenFeed, Dabaco, BaF)

### VỀ ĐỐI TƯỢNG (Q9-10)
- Q9 (Nhà đầu tư): impact fund, VC nông nghiệp, NĐT cá nhân hiểu ngành. Quan tâm: thị trường cấm AGP, bằng chứng VNUA, Stage-Pack 70%, founder đa ngành
- Q10 (Sale/Đại lý): đại lý cám, cửa hàng thú y, trại vừa. Rào cản: chưa tin hiệu quả → trải nghiệm miễn phí, giá cao → định vị bảo hiểm rủi ro chết, đọng vốn → Stage-Pack

### USP sản phẩm (Q11-12)
- Q11 (Bản Đầu tư): cơ hội thị trường cấm AGP, lợi thế độc quyền kiềm khoáng, Stage-Pack 70%, founder trẻ, định giá 112 tỷ
- Q12 (Bản Sale): ROI 156.250đ/con, bằng chứng VNUA, Stage-Pack không đọng vốn, đúng thời điểm cấm AGP

### VỀ HÌNH THỨC DESIGN (Q13-14)
- Q13 (Bộ nhận diện): logo Vua Kiềm/Kiềm Saphia, bảng màu B/W/Y (#0D0D0D/#1B1B1D/#FFD600), font system. Đề nghị Quang gửi file gốc logo
- Q14 (Hình ảnh thật): có thể chụp sản phẩm, trại thử, đội ngũ. Cần chụp mới hoặc dùng stock

## Technical pattern (Google Sheets API)

Read:
```
res = svc.spreadsheets().values().get(spreadsheetId=SID, range="Brief!A1:E100").execute()
```

Write single cell:
```
svc.spreadsheets().values().update(
    spreadsheetId=SID, range="Brief!C9",
    valueInputOption='RAW',
    body={'values': [["answer text"]]}
).execute()
```

Write many cells: loop through (row_num, answer, link) tuples, update column C and E separately.

## Lưu ý
- Không xoá section headers (THÔNG TIN CHUNG, VỀ NỘI DUNG...)
- Giữ nguyên câu trả lời đã có (Q1-5), chỉ điền câu trống
- Chỗ không biết: ghi "Cần anh cập nhật" thay vì bịa
- Verify sau khi write: đọc lại vài cell spot-check
- Factsheet tab thường trống (Marketing tự điền sau khi có brief)
