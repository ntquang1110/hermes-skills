# Đề cương thử ổn định premix heo con (fixgby, 21/10/2026)

Bản gốc trong repo: `D:/Hermes Proj/fixgby/docs/14-cong-thuc-co-ban/10-thu-on-dinh-gia-toc.md`
Trang công khai của nhánh: https://preview.thefirstonly.com/gyegd6p0w9y8

## Bối cảnh đã dẫn tới đề cương này

Bốn việc còn nợ treo trên trang công khai, ba trong số đó là câu hỏi "số thật là bao nhiêu":

1. Cửa C (miễn dịch niêm mạc) chưa có chất nào → *Bacillus subtilis* có đo IgA tiết trong phân không (nợ dài, cần tra cứu).
2. Hàm lượng tannin hạt dẻ thật của lô hàng (giả định 65–75%, phải có spec lô thật).
3. Bảng giá nhà cung cấp → giá vốn VND (cột giá trong engine chỉ là thứ bậc, không dùng để định giá).
4. **Thử ổn định gia tốc 3 và 6 tháng** ← đề cương này.

Nợ 4 là thứ duy nhất trả lời được câu "sản phẩm để được bao lâu", nên làm trước.

## Thiết kế đã chốt

- 4 công thức: TC-1 · 2,5 kg/tấn (đỉnh 90,40) · HH-1 · 4,5 kg/tấn (95,75) · SÀN-TC · 0,70 kg/tấn (có Bacillus,
  phải đo riêng vì bào tử là chỗ dễ chết nhất) · SÀN-HH · 1,80 kg/tấn.
- 3 lô TRỘN RIÊNG mỗi công thức = 12 lô 2 kg.
- Mỗi công thức 2 kiểu bao: bao nhôm/PA-PE hàn kín (bao thật) + **bao hở cố ý 1 góc**.
- Mốc: T0 · gia tốc 40/75 ở 1/3/6 tháng · dài hạn 30/75 ở 3/6/12 tháng.
- Tổng: 4 × 3 × 2 × 7 = **168 điểm mẫu** (cắt còn 84 nếu bỏ nhánh hở, còn 48 nếu giữ 4 mốc 0/3/6/12).

## Bảng xin báo giá (gửi nguyên bảng này cho lab)

| Hạng mục | Số lượng | Ghi chú |
|---|---|---|
| Buồng 40 °C/75% RH | 6 tháng | 12 lô × 2 kiểu bao |
| Buồng 30 °C/75% RH | 12 tháng | chạy song song |
| GC-FID headspace (thymol) | 60 lần chạy | 2 CT × 3 lô × 2 bao × 5 mốc |
| HPLC-UV (glycyrrhizin, baicalin) | 60 lần chạy | như trên |
| Folin–Ciocalteu (tanin) | 30 lần chạy | 2 CT × 3 lô × 5 mốc |
| Đếm khuẩn lạc Bacillus | 15 lần | chỉ SÀN-TC |
| Hoạt độ protease | 18 lần | 3 CT có protease × 3 lô × 2 mốc |
| Độ ẩm + aw | 168 | mọi điểm mẫu |
| Vi sinh an toàn | 84 | rút còn 24 được |
| CV phân tầng | 24 | 12 lô × 2 lần |

Thời gian: chuẩn bị + trộn 2 tuần → mốc 1 · 3 · 6 tháng → báo cáo cuối 2 tuần = **6 tháng 3 tuần** cho phần gia tốc.

## Ngưỡng dùng cho lô này

- Tanin (Folin–Ciocalteu) ≥ 90% T0 · acid glycyrrhizic HPLC 254 nm ≥ 90% T0 · baicalin HPLC 280 nm ≥ 90% T0.
- Thymol/carvacrol GC-FID ≥ **85%** T0 (bay hơi — cố ý đặt ngưỡng thấp hơn).
- *Bacillus subtilis* ≥ 10⁶ CFU/g và mất ≤ 1 log.
- Protease ≥ 80% hoạt độ T0 · độ ẩm ≤ 8–10% · aw ≤ 0,60 · CV phân tầng < 5%.
- Vi sinh an toàn: theo TCVN hiện hành cho TĂCN — **số chưa chốt, ghi thẳng là còn nợ**, không tự đặt.

## Chỗ dễ sai nhất của lô này

- Bao nhôm hàn kín là **biến số lớn hơn cả nhiệt**; nhánh bao hở chính là để chứng minh điều đó.
- Lấy mẫu trong bao 25 kg phải theo 8–10 điểm trên–giữa–dưới; premix phân tầng nên lấy sai là vô giá trị.
- Không đo ở 25 °C/60% RH (vùng I–II) rồi kết luận cho Việt Nam.
- Giữ đủ mẫu T0 — hết mẫu T0 là mất mốc so sánh, không mua lại được.
