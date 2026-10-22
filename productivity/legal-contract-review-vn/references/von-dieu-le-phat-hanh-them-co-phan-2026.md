# Phát hành thêm cổ phần để tăng vốn điều lệ — Khung pháp lý Việt Nam

Nguồn: **Luật Doanh nghiệp số 109/2025/QH15** (thay thế Luật Doanh nghiệp 2020 số 59/2020/QH14), hiệu lực 01/7/2026.
Verify qua 2 nguồn độc lập: vietnamthuvien.com + CSDL văn bản Quốc gia (vanban.chinhphu.vn).

> ⚠️ **Không trộn định giá với vốn điều lệ.** Định giá pre-money là thỏa thuận thương mại giữa các bên. Vốn điều lệ chỉ nhận **tổng mệnh giá cổ phần đã bán** (Điều 112.1). Hai con số khác nhau về bản chất.

---

## 1. Công thức tính số liệu

```
CHO:   V0  = vốn điều lệ hiện tại
       P   = mệnh giá cổ phần (thường 10.000, XEM ĐIỀU LỆ — không phải luật đặt sẵn)
       N0  = tổng số cổ phần hiện tại = V0 / P
       Vpre= định giá trước phát hành (pre-money)
       I   = số tiền nhà đầu tư góp
       Vpost = Vpre + I

TÍNH:
1.  Giá mỗi cổ phần          g  = Vpre / N0
2.  Số cổ phần mới           n  = I // g          (làm tròn XUÔNG)
3.  Giá trị mệnh giá mới     Vm = n × P           → VÀO VỐN ĐIỀU LỆ
4.  Thặng dư vốn cổ phần     Ts = I − Vm          → KHÔNG vào vốn điều lệ
5.  Vốn điều lệ mới          V1 = V0 + Vm
6.  Tổng số cổ phần mới      N1 = N0 + n
7.  Tỷ lệ nhà đầu tư mới     rN = n / N1          (≈ I / Vpost)
8.  Tỷ lệ cổ đông hiện hữu   rO = N0 / N1
9.  Hệ số pha loãng          k  = N0 / N1
10. Giá trị sổ sách/cổ phần  = Tổng vốn chủ sở hữu / N1
```

**Kiểm tra chéo (bắt buộc):**
- `Vpre + I = Vpost` — đúng tuyệt đối
- `Vm + Ts = I` — đúng tuyệt đối
- `V0 + Vm = V1` — đúng tuyệt đối
- `rN + rO = 1` — đúng tuyệt đối
- `n / (N0 + n) = I / Vpost` — **chỉ xấp xỉ**, sai số do làm tròn. Chấp nhận dưới 0,0001 phần trăm. Ghi rõ sai số vào tài liệu.

**Ngưỡng của người sáng lập sau pha loãng:**
- Giữ **>50%** sau pha loãng: cần hiện sở hữu **> 50% / k**
- Giữ **≥65%** (đủ tự thông qua nghị quyết quan trọng nếu cổ đông khác không dự họp): cần hiện sở hữu **≥ 65% / k**

**Case Manna Đất Vàng (16 tỷ → phát hành 5 tỷ, định giá 112 tỷ):**
- g = 112.000.000.000 / 1.600.000 = **70.000 VNĐ/cổ phần**
- n = 5.000.000.000 // 70.000 = **71.428** (làm tròn xuống, sai số 40.000 VNĐ)
- Vm = **714.280.000** · Ts = **4.285.720.000**
- V1 = **16.714.280.000** (chỉ tăng ~714 triệu, KHÔNG phải 112 tỷ)
- N1 = 1.671.428 · rN = **4,2735%** · rO = **95,7265%**
- k = 0,957265 → ngưỡng >50%: **52,23%**; ngưỡng ≥65%: **67,90%**

---

## 2. Hình thức phát hành

| Hình thức | Căn cứ | Điều kiện |
|:---------:|:------:|:----------|
| Chào bán cho cổ đông hiện hữu (**bắt buộc trước**) | Điều 124 | Thông báo **trước ít nhất 15 ngày** so với hạn cuối đăng ký mua |
| Chào bán riêng lẻ | Điều 125.1.b | Dưới **100 nhà đầu tư**, hoặc chỉ cho NĐT chứng khoán chuyên nghiệp |
| Chào bán qua Sở Giao dịch | Điều 125.1.a | Tuân thủ Luật Chứng khoán |

**Điều 125.2.c:** Chỉ bán phần **chưa được cổ đông hiện hữu mua hết**, với điều kiện **không bất lợi hơn**. Bỏ qua bước này → NĐT cũ có thể kiện yêu cầu hủy giao dịch.

---

## 3. Thẩm quyền quyết định

| Nội dung | Cơ quan | Căn cứ |
|:--------:|:-------:|:------:|
| Loại cổ phần và **tổng số cổ phần của từng loại** được quyền chào bán | ĐHĐCĐ | Điều 138.2.b |
| Giá bán cổ phần | HĐQT | Điều 153.2.d |
| Kiến nghị loại CP và tổng số CP được quyền chào bán | HĐQT | Điều 153.2.b |
| Toàn quyền quản lý, trừ quyền thuộc ĐHĐCĐ | HĐQT | Điều 153.1 |
| Người đại diện theo pháp luật | Chủ tịch HĐQT (hoặc GĐ/TGĐ nếu Điều lệ ghi) | Điều 137.2 |

**⚠️ Nghị quyết ĐHĐCĐ phải biểu quyết TẠI CUỘC HỌP** (Điều 147.2.c), trừ khi Điều lệ có quy định khác. Không lấy ý kiến bằng văn bản cho nội dung quan trọng.

**Ngưỡng thông qua:**
- Nghị quyết **thông thường**: > 50% tổng số phiếu biểu quyết của cổ đông dự họp (Điều 148.2)
- Nghị quyết **quan trọng** (bao gồm "loại CP và tổng số CP của từng loại"): **≥ 65%** (Điều 148.1.a)

> Nếu Chủ tịch sở hữu ≥ 67,90% (khi k ≈ 0,957) → tự thông qua được nếu cổ đông khác không dự họp. Dưới mức đó → phải vận động đạt ≥ 65% phiếu của cổ đông dự họp.

---

## 4. Quyền của cổ đông mới — tại sao 0,8% không có gì

| Quyền | Ngưỡng | Căn cứ |
|:-----:|:------:|:------:|
| Quyền biểu quyết | 1 cổ phần phổ thông = **1 phiếu**, không thể tước | Điều 115.1.a |
| Tra cứu BCTC, yêu cầu triệu tập ĐHĐCĐ, yêu cầu Ban kiểm soát kiểm tra | ≥ **5%** tổng số CP phổ thông | Điều 115.2 |
| Quyền ưu tiên mua cổ phần phát hành thêm | Cổ đông hiện hữu, theo tỷ lệ sở hữu | Điều 124 |

→ Cổ đông sở hữu 0,85% **không có quyền kiểm soát nào**. Không thể đề cử HĐQT, không thể yêu cầu triệu tập ĐHĐCĐ, không thể tra cứu BCTC.

---

## 5. Cổ phần ưu đãi — KHÔNG dùng được để giữ quyền kiểm soát

| Loại | Quyền biểu quyết | Điều kiện |
|:----:|:----------------:|:----------:|
| **Ưu đãi biểu quyết** (Điều 116) | Có, tối đa **3 lần**/cổ phần, tổng ≤ 20% tổng số CP có quyền biểu quyết | **CHỈ** tổ chức được bởi: (a) doanh nghiệp Nhà nước được Chính phủ ủy quyền, (b) **cổ đông sáng lập** trong thời hạn **3 năm** kể từ ngày cấp GCNĐKDN |
| **Ưu đãi cổ tức** (Điều 117) | **KHÔNG có** quyền biểu quyết, dự họp, đề cử vào HĐQT/Ban kiểm soát | ĐHĐCĐ quyết định; phải trả cổ tức **cao hơn** CP phổ thông |

**⚠️ LỖ HỔNG NGHIÊM TRỌNG:** Một công ty thành lập từ **06/10/2021** sẽ hết hạn dùng CP ưu đãi biểu quyết từ **06/10/2024**. Sau đó **không còn cơ sở pháp lý** để phát hành loại này. Kiểm tra ngày cấp GCNĐKDN trước khi đề xuất.

**⚠️ Điều 114.5:** Cổ phần phổ thông **không thể chuyển đổi** thành cổ phần ưu đãi. Không có đường vòng.

---

## 6. Thuế TNCN với người nhận cổ phần

- **Luật Thuế TNCN số 109/2025/QH15**, hiệu lực **01/7/2026**, kèm **Nghị định 253/2026/NĐ-CP**.
- **Đầu tư vốn** (cổ tức): **5%**
- **Chuyển nhượng vốn / chứng khoán**: theo Nghị định 253/2026 — cần kế toán thuế xác nhận tỷ lệ và cơ sở tính **tại thời điểm giao dịch**.
- **Phát hành thêm cổ phần cho NĐT = góp vốn, KHÔNG phải chuyển nhượng.** Chênh lệch giá phát hành so với mệnh giá hạch toán vào **thặng dư vốn cổ phần (TK 4112)**, không phải thu nhập chịu thuế TNCN tại thời điểm đăng ký mua.
- ⚠️ NĐ 253/2026 còn mới, cần tra lại văn bản gốc trước khi tư vấn con số cụ thể cho khách hàng.

---

## 7. Thủ tục sau phát hành

1. NĐT chuyển đủ tiền vào tài khoản công ty
2. Hạch toán: Dr Tiền mặt/Tiền gửi → Cr Vốn điều lệ (Vm) → Cr Thặng dư vốn cổ phần (Ts)
3. **Cổ phần được coi là đã bán** khi thanh toán đủ và thông tin NĐT được ghi đầy đủ vào **sổ đăng ký cổ đông** (Điều 124.4)
4. Cập nhật sổ đăng ký cổ đông (Điều 122)
5. **Đăng ký thay đổi nội dung ĐKKD** (vốn điều lệ mới, cổ đông mới) **trong vòng 10 ngày** kể từ ngày hoàn thành đợt bán (Điều 123.4)
6. Sửa Điều lệ nếu Điều lệ ghi rõ vốn điều lệ

---

## 8. Lỗ hổng thường gặp

| # | Lỗ hổng | Hệ quả | Cách xử lý |
|:-:|:---------|:-------|:-----------|
| 1 | Tăng vốn điều lệ lên mức định giá | Vốn điều lệ ảo, không có căn cứ pháp lý | Chỉ tăng theo mệnh giá × số CP bán |
| 2 | Bỏ qua quyền ưu tiên mua của cổ đông hiện hữu | Nghị quyết có thể bị khiếu nại, Tòa hủy giao dịch | Thông báo ≥15 ngày, xin từ chối quyền ưu tiên bằng văn bản |
| 3 | Nghị quyết không đủ ≥65% | Bị khiếu nại, bị Tòa hủy (Điều 151) | Thu thập phiếu thuận ≥65% tại cuộc họp |
| 4 | Giá phát hành < giá trị sổ sách/cổ phần | Vi phạm Điều 126 | Tra BCTC gần nhất trước khi chốt giá |
| 5 | ≥100 NĐT trong một đợt chào bán riêng lẻ | Chuyển sang hình thức khác, có thể phải tuân thủ Luật Chứng khoán | Giới hạn <100 NĐT |
| 6 | Quá hạn 10 ngày đăng ký thay đổi ĐKKD | Xử phạt hành chính | Đặt deadline ngay khi hoàn thành đợt bán |
| 7 | Dùng CP ưu đãi biểu quyết khi đã quá 3 năm | Phát hành vô hiệu | Kiểm tra ngày cấp GCNĐKDN |
| 8 | Làm tròn sai số cổ phần không ghi nhận | Tranh chấp về tỷ lệ sở hữu | Làm tròn xuống + ghi rõ sai số trong HĐ đăng ký mua |

---

## 9. Checklist trước khi trình Chủ tịch / Hội đồng

- [ ] Xác minh pháp nhân: tên đúng, MST, người đại diện, trụ sở (≥2 nguồn độc lập)
- [ ] Đọc Điều lệ: mệnh giá CP, ngưỡng thông qua nghị quyết, điều kiện dùng CP ưu đãi
- [ ] Lấy BCTC gần nhất: giá trị sổ sách/cổ phần, lợi nhuận giữ lại, quỹ dự phòng
- [ ] Xác định tỷ lệ sở hữu **HIỆN TẠI** của từng cổ đông (đặc biệt Chủ tịch)
- [ ] Tính ngưỡng giữ >50% và ≥65% sau pha loãng
- [ ] Kiểm tra ngày cấp GCNĐKDN (CP ưu đãi biểu quyết)
- [ ] Danh sách NĐT: tổng số người có vượt 100 không
- [ ] Xác định thuế TNCN áp dụng tại thời điểm giao dịch
