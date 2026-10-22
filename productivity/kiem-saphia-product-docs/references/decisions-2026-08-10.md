# Quyết định 10/08/2026 — áp dụng cho HTML preview ASF V2.1

Bối cảnh: anh Quang duyệt demo, yêu cầu chỉnh theo từng vòng. Mọi quyết định dưới đây đã verify trong HTML `tai-lieu-san-pham-khoa-hoc-v2.html` (gist `3d581a3444296042579d49722d4d85fe`, preview https://preview.thefirstonly.com/3d581a3444296042579d49722d4d85fe).

## 1. BỎ TOÀN BỘ thông tin đất hiếm (anh: "bỏ toàn bộ thông tin liên quan đến đất hiếm đi")

- CẤM viết: CeO2, La2O3, Nd2O3, "đất hiếm", Ce trong tài liệu sản phẩm.
- Đã xóa: block "Đất hiếm xử lý" trong card Thành phần EZ80 (3 nhóm → **2 nhóm**: Khoáng vi lượng + Dược liệu).
- Đã xóa TOÀN BỘ card cơ chế "Bốn lớp áo giáp kháng ASF" (3/4 lớp dùng CeO2/Ce: Báo động toàn thân, Sát thủ tuần tra, Bảo vệ tế bào) → thay bằng note: "phần cơ chế giải thích đang chờ kết quả thử nghiệm InVitro/InVivo chính thức".
- Đã cập nhật nguồn [6]: "khoáng vi lượng, polyphenol, saponin" (bỏ "đất hiếm").
- Verify: `grep -n "đất hiếm\|CeO2\|La2O3\|Nd2O3"` = 0.
- LƯU Ý: catalog gốc (`catalog-vuakiem-29042026.md`) có nhắc đơn đất hiếm nộp 2022-2025 — là dữ liệu nội bộ, KHÔNG đưa vào tài liệu gửi đối tác.

## 2. BỎ "Công suất hiện tại" + "Doanh thu tiềm năng theo công suất"

- Đã xóa ở 2 chỗ: bảng Thông số kỹ thuật EZ80 (300 tấn/tháng · 3.600 tấn/năm · 450 tỷ đ/năm) + bảng Thị trường (6% nhu cầu, 450 tỷ).
- Đã bỏ ghi chú "Đạt 30% TAM tương đương gấp 5 lần công suất hiện tại" (chỉ giữ "Đây là con số dùng khi chào đối tác chiến lược").
- Đã cập nhật mô tả nguồn [7] (bỏ "công suất, doanh thu tiềm năng").
- Verify: `grep -n "Công suất\|công suất\|450 tỷ\|3.600"` = 0.

## 3. Công dụng ghi ĐÚNG theo sheet — CẤM claim "phòng, hỗ trợ điều trị"

- EZ80 + EZ67 công dụng = "Thức ăn bổ sung cho gia súc: hạn chế kháng sinh, tăng cường miễn dịch, cải thiện tiêu hóa" (nguồn [S]).
- Đối tượng = "Gia súc (lợn thịt, lợn trưởng thành)" — KHÔNG ghi "lợn chưa nhiễm/nghi nhiễm".
- Nút switcher: "EZ80 Thức ăn bổ sung · dạng bột" / "EZ67 Thức ăn bổ sung · dạng nước".
- Virusto = "Thức ăn bổ sung cho thủy sản: bổ sung khoáng, tôm lột xác đều, cứng vỏ, tăng đề kháng" + cách dùng 1 lít + 1 lít nước trộn 200kg thức ăn [S].

## 4. Ảnh sản phẩm EZ80

- Ảnh anh gửi `img_d484e571230e.jpg` (1280x1024) → copy `D:/Hermes Proj/kiem-saphia/assets/ez80-product.jpg`.
- Nhúng base64 data URI, vị trí đầu panel EZ80 dưới switcher, trước card Công dụng. CSS `.product-img{max-width:340px;margin:0 auto 16px;border-radius:12px;border:1px solid var(--border)}`.
- Base64 ~233KB → tổng HTML ~275KB (gist limit 1MB, OK).

## 5. PITFALL khi push gist (đã dính 2 lần)

- **`cat` qua terminal truncate ngầm ~52KB**: HTML ~275KB qua `terminal('cat ...')` → gist nhận thiếu (52882 bytes vs local 276369). FIX: trong execute_code đọc bằng `open(path, encoding='utf-8').read()` rồi PATCH gist trực tiếp. Verify sau push: so `len(content.encode('utf-8'))` với size API trả về.
- **Preview CDN cache ~vài phút**: sau PATCH, `preview.thefirstonly.com` có thể trả bản cũ. Verify bằng raw gist URL trực tiếp (luôn mới nhất). Raw URL mới có commit hash khác nhau — fetch đúng `raw_url` trong response của PATCH.
- **Preview đọc file `index.html` trong gist**: phải PATCH cả `index.html` + file tên dài (2 file trùng nội dung) chứ không chỉ file `tai-lieu-...html`.
