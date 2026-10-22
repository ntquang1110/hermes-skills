# Premix định mức tab — pattern tính cân được (added 21/10/2026)

Case thật: 6 công thức premix heo con (fixgby) đổ vào **tab mới `CT heo (fixgby)`** của sheet
`VK – RnD + Lab` (id `<SHEET_ID>`, gid `1534069869`) — thêm tab, KHÔNG tạo file,
KHÔNG chèn dòng vào block `Định mức & Lượng mua` của user (xem pitfall 22 trong SKILL.md).

## Bộ 3 cột bắt buộc — để đứng ở cân là cân được

| Công thức | Nhóm bệnh | Nguyên liệu | kg/tấn cám | % trong premix | Gram cho 1 kg premix | Cửa chặn | Bậc bằng chứng | Ghi chú |
|---|---|---|---|---|---|---|---|---|

- **kg/tấn cám** = liều trong cám thành phẩm (thứ khách mua).
- **% trong premix** = tỷ lệ khi phối trộn (thứ xưởng cân). Ghi rõ khác nhau ở dòng chú thích ngay dưới tiêu đề —
  người đọc rất dễ lẫn hai đơn vị này.
- **Gram cho 1 kg premix** = % × 10, con số công nhân thật sự đọc.

Đơn vị gốc trong data có thể khác (`ct` × 10 = kg/tấn là quy ước thật của dự án fixgby — đọc builder trước khi
đổi). Luôn tính hai cột còn lại bằng code, không tính tay.

## Phép kiểm bắt buộc (cả hai phải đạt mới được báo xong)

1. Mỗi công thức kết bằng dòng `TỔNG` → **% cộng đúng 100,0** và **gram cộng đúng 1000**.
2. Phải có dòng `Chất mang` — công thức mà phần hoạt chất nhỏ hơn liều thì chỉ đủ khi có chất mang bù:
   TC-1 = 1,667 tanin + 0,433 thymol = 2,10 hoạt chất + 0,40 chất mang = 2,50 kg/tấn.
3. In bảng đối chiếu ra stdout (`TC-1 2.5 kg/tấn | 100 % | 1000 g`). Công thức cộng ra 97% là loại lỗi không ai
   bắt được bằng mắt.

## Bố cục 4 phần — đọc giống tab của user

`PHẦN 1 — ĐỊNH MỨC TỪNG NGUYÊN LIỆU` · `PHẦN 2 — ĐIỂM VÀ SO SÁNH` (mỗi công thức 1 dòng: liều, tổng điểm, trục
hiệu quả, trục ổn định, số nguyên liệu, ghi chú) · `PHẦN 3 — ĐÓNG GÓI VÀ CẢNH BÁO` (không chung bao · nhiệt ép
viên · độ ẩm · CV phân tầng) · `PHẦN 4 — VIỆC CÒN NỢ` (khớp đúng danh sách trên trang HTML công khai).

## Format

Tiêu đề merge + nền xanh `#1a3300` chữ trắng đậm · dòng `PHẦN n` nền vàng `#FFE95C` · dòng `TỔNG` nền kem
`#FCFAF5` đậm · cột số căn phải · `frozenRowCount` tới hết dòng tiêu đề.
**`numberFormat.pattern` phải là `General`** — `#,##0.###` render số nguyên kèm dấu chấm cuối (pitfall 19).
