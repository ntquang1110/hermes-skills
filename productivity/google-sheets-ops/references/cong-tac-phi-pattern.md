# Công tác phí — pattern sheet theo định mức công ty (Manna Đất Vàng)

Dùng khi Quang yêu cầu dựng bảng theo dõi công tác phí / chi phí đi lại / tạm ứng.
Workflow bắt buộc: **draft trên chat → Quang duyệt → mới tạo Google Sheet thật**. Không tạo trước khi duyệt. Draft theo cấu trúc 4 sheet dưới đây, trích định mức từ quy định công ty, nêu rõ mâu thuẫn nếu có, chốt câu hỏi trước khi tạo.

## Lấy nội dung quy định (Google Doc public, không cần OAuth)

```bash
curl -sSL "https://docs.google.com/document/d/<DOC_ID>/export?format=txt" -o dmct.txt
```

- DOC_ID ví dụ: `<SHEET_ID>` (QUY ĐỊNH CÔNG TÁC PHÍ Manna Đất Vàng, QĐ-…/2026)
- **Pitfall Windows/MSYS:** `/tmp` không dùng được (curl exit 23, file không tạo ra). Ghi vào `C:/Users/NTQUANG_DELL/AppData/Local/hermes/tmp/`, và `cd` vào thư mục trước khi curl với `-o` relative.
- Cách khác nếu doc private: `google-workspace` skill (`$GAPI docs get DOC_ID`), cần OAuth.

## Định mức Manna Đất Vàng (chốt 14/09/2026, nguồn: quy định trên)

- **Đi lại:** xe máy cá nhân 2.000đ/km · ô tô cá nhân 4.000đ/km · xe công ty = thanh toán hóa đơn xăng dầu thực (hóa đơn ghi đúng biển số + tên/MST công ty)
- **Nguyên tắc đầu xe:** 01 xe = 01 lần tính cho toàn hành trình, KHÔNG nhân theo số người đi cùng
- **Cầu đường:** nạp VETC 2.000.000đ/tháng (không nhập từng lần)
- **Nhiên liệu:** xăng chuẩn 23.000đ/lít, dầu 28.000đ/lít, biên độ ±10% (trong biên độ giữ định mức, vượt thì lập bảng mới), tiêu hao trung bình 8,5 lít/100km
- **Tạm ứng đầu tháng:** xăng dầu 5.600.000 (26 ngày × 100km/ngày × 8,5 lít/100km × 25.500đ) + VETC 2.000.000 + ăn uống tiếp khách 5.000.000 = **12.600.000đ**
- **MÂU THUẪN CHƯA CHỐT:** ăn uống tiếp khách — mục VI.3 ghi 5.000.000đ/tháng, mục VIII.1 ghi 10.000.000đ/tháng. Phải hỏi Quang con số chuẩn trước khi tạo.
- **Lưu trú:** 450.000đ/phòng/đêm 1 người; 2 người chung phòng cùng giới (nam-nam, nữ-nữ) tối đa 600.000đ/phòng/đêm
- **Phụ cấp công tác:** 130.000đ/người/ngày, khi làm ngoài trụ sở ≥8 giờ hoặc đi qua đêm, chỉ khi được chỉ định/đề xuất được duyệt
- **Chứng từ & thanh toán:** trong 5 ngày làm việc sau chuyến gửi bảng kê + hóa đơn cho kế toán; kế toán kiểm tra hợp lệ, đối chiếu định mức; cuối tháng đối soát tạm ứng, thực chi ít hơn → hoàn lại hoặc trừ kỳ sau

## Cấu trúc 4 sheet (draft đã duyệt)

1. **Nhật ký công tác** (nhập liệu): Ngày | Tên nhân viên (dropdown) | Mục đích/địa điểm/kết quả | Loại chi phí (dropdown: Xe máy / Ô tô cá nhân / Xăng dầu xe công ty / Lưu trú 1 người / Lưu trú 2 người / Ăn uống tiếp khách / Phụ cấp công tác / Khác) | Số lượng (km / đêm / ngày / lít) | Đơn giá (lookup từ Sheet Định mức) | Thành tiền (= SL × ĐG) | Chứng từ (Có/Không/N/A) | Ghi chú (biển số, hóa đơn số)
2. **Định mức** (config, Quang sửa được — đổi khi giá xăng vượt ±10%): mỗi loại một dòng, là nguồn lookup
3. **Tạm ứng & đối soát cuối tháng**: tạm ứng (12.600.000) vs thực chi = SUMIFS theo tháng từ Sheet 1 → chênh lệch dương = hoàn lại, âm = chi thêm; cột xử lý (hoàn lại / trừ kỳ sau)
4. **Báo cáo tổng hợp** (tự động): tổng tháng × nhân viên, tổng theo loại chi phí, số dòng thiếu chứng từ/chưa duyệt, tô đỏ dòng vượt định mức

## Công thức mẫu

- Đơn giá lookup: `=VLOOKUP(E2, 'Định mức'!$A:$C, 3, FALSE)` (loại chi phí → đơn giá)
- Thành tiền: `=F2*G2` (SL × đơn giá)
- Thực chi tháng: `=SUMIFS('Nhật ký'!$H:$H, 'Nhật ký'!$A:$A, ">="&DATE(2026,9,1), 'Nhật ký'!$A:$A, "<"&DATE(2026,10,1))`
- Dropdown: data validation từ một sheet/danh sách Danh mục (nhân viên, loại chi phí) — tránh gõ tay lệch chuẩn
- Cảnh báo vượt định mức: `=IF(H2>VLOOKUP(...), "VƯỢT", "")` kèm conditional formatting tô đỏ

## Câu hỏi chốt trước khi tạo (hỏi Quang, đừng tự đoán)

1. Tạm ứng ăn uống tiếp khách: 5tr hay 10tr/tháng (quy định đang ghi 2 chỗ khác nhau)
2. Tạm ứng 12.600.000 tính cho mỗi người đi công tác hay một mức chung cả team
3. Ai nhập liệu: nhân viên tự nhập hay kế toán gõ chung
