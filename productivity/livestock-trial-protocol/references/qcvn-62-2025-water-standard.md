# QCVN 62:2025/BTNMT — nước thải chăn nuôi (thay QCVN 62-MT:2016)

Cập nhật 08/09/2026 khi làm báo cáo CT888 Xuân Thiện. **Bắt buộc dùng chuẩn này cho MỌI báo cáo so ngưỡng xả thải chăn nuôi sau 01/09/2025** — không được dùng 2016 nữa.

## Thông tin văn bản
- Số hiệu: QCVN 62:2025/BTNMT (Quy chuẩn kỹ thuật quốc gia về nước thải chăn nuôi)
- Ban hành: Thông tư 28/02/2025 (Bộ TNMT), **hiệu lực 01/09/2025**
- Thay thế: QCVN 62-MT:2016/BTNMT
- Nguồn PDF chính thức: `D:/Hermes Proj/xuanthien/QCVN_62_2025.pdf` (7 trang, tải từ nguoichannuoi.vn/wp-content/uploads/2025/03/QCVN-62-2025-BTNMT-ve-nuoc-thai-chan-nuoi.pdf)

## Bảng 1 — Giá trị giới hạn (trang trại chăn nuôi)

| TT | Thông số | Đơn vị | Cột A | Cột B | Cột C |
|----|----------|--------|-------|-------|-------|
| 1 | pH | - | 6–9 | 6–9 | 6–9 |
| 2 | BOD5 (20°C) | mg/L | ≤40 | **≤60** | ≤100 |
| 3 | COD | mg/L | ≤65 | **≤150** | ≤250 |
| 3b | TOC (thay thế được COD) | mg/L | ≤35 | ≤70 | ≤130 |
| 4 | TSS | mg/L | ≤40 | **≤100** | ≤120 |
| 5 | Tổng N | mg/L | ≤20 | **≤60** | ≤120 |
| 6 | Tổng P — hồ/ao/đầm | mg/L | ≤2,0 | ≤3,0 | ≤4,0 |
| 6b | Tổng P — sông/suối/kênh/rạch | mg/L | ≤4,0 | ≤14 | ≤30 |
| 6c | Tổng P — vùng nước biển | mg/L | ≤4,0 | ≤14 | ≤40 |
| 7 | Tổng Coliform | MPN/CFU/100mL | ≤3.000 | ≤5.000 | ≤5.000 |

## So sánh Cột B 2016 → 2025 (mức siết)

| Chỉ tiêu | 2016 | 2025 | Giảm |
|----------|------|------|------|
| BOD5 | 100 | 60 | -40% |
| COD | 300 | 150 | -50% |
| TSS | 150 | 100 | -33% |
| Tổng N | 150 | 60 | -60% |
| pH | 5,5–9 | 6–9 | siết nhẹ |

**Hệ quả báo cáo CT888:** theo chuẩn 2016 thì M1 N15 đạt BOD5 (91≤100) + TN (145≤150); theo chuẩn 2025 **cả 4 chỉ tiêu vượt** (BOD5 ×1,5, COD ×8,2, TSS ×4,6, TN ×2,4). Mọi claim "ĐẠT" cũ phải re-baseline. Cách xử lý đã chốt với user: công khai chuẩn mới trước, đóng khung "thách thức chung của ngành sau 01/09/2025", đưa lộ trình chạm chuẩn mới (BOD5 ~N17-18, TSS ~19-21, TN ~22-24, COD ngoài khung 30 → bắt buộc xử lý lần 2 + tăng sục khí).

## Cách tìm chuẩn pháp lý VN khi SearXNG/Google/Bing chặn (đã verify 08/09/2026)
1. SearXNG local (8888) có thể TẮT → kiểm tra `curl -s http://127.0.0.1:8888/` trước, đừng giả định chạy.
2. DDG qua curl bị CAPTCHA; Bing qua curl trả rác (ADS/court records) → bỏ qua.
3. **Đường ra: Camofox browser** (start `node server.js` background) + `camsearch.py` (skill camofox-browser) search DDG → kết quả có PDF trực tiếp (nguoichannuoi.vn, scem.org.vn, scribd).
4. Tải PDF + trích bảng bằng `pymupdf`:
   ```python
   import pymupdf  # fitz deprecated
   doc = pymupdf.open(r"D:/Hermes Proj/xuanthien/QCVN_62_2025.pdf")
   text = doc[i].get_text()  # bảng nằm page 4 (index 3)
   ```
5. ⚠️ Lifecycle guard: command python có chuỗi `pymupdf.open('...')` inline bị báo lỗi "embedded null character" giả → **viết script ra file .py rồi chạy** mới OK.

## Claim khoa học đã sửa trong báo cáo CT888 (pH)
- SAI: "kiềm thuận lợi cho hệ vi sinh phân giải + thúc đẩy nitrat hóa" (pH 8,6–9,09 tại M1/M2).
- ĐÚNG: vi sinh ưa pH 6,5–8,5; nitrat hóa tối ưu ~7,5–8,5. pH cao 8,6–9 hỗ trợ **keo tụ + phân hủy hóa học** chất hữu cơ, giảm mùi. Khi pH về trung tính ở M3 (7,0–7,16), vi sinh + nitrat hóa mới hoạt động trở lại.
- Quy tắc: bất kỳ claim nào gắn pH với hoạt động sinh học phải kiểm tra ngưỡng pH của cơ chế đó trước khi viết.
