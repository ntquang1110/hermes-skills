# QCVN 62-MT:2016/BTNMT + cơ chế BOD/COD/TSS (research 09/2026, có nguồn)

Áp dụng khi: báo cáo thử nghiệm xử lý nước thải chăn nuôi, cần giải thích "vì sao phải giảm
BOD/COD/TSS" hoặc đối chiếu kết quả với chuẩn pháp lý VN.

## 1. Bảng chuẩn QCVN 62-MT:2016/BTNMT (nước thải chăn nuôi) — Bảng 1, giá trị C

| Chỉ tiêu | Cột A (nguồn cấp nước sinh hoạt) | Cột B (nguồn không dùng cấp nước sinh hoạt) |
|---|---|---|
| BOD5 | 40 mg/L | 100 mg/L |
| COD | 100 mg/L | 300 mg/L |
| TSS | 50 mg/L | 150 mg/L |
| Tổng Nitơ (theo N) | 50 mg/L | 150 mg/L |
| pH | 6–9 | 5,5–9 |
| Coliform | 3.000 /100ml | 5.000 /100ml |

Lưu ý: giá trị tối đa cho phép còn nhân hệ số Kq (đặc điểm nguồn tiếp nhận: sông/hồ/biển,
0,6–1,3) và Kf (lưu lượng nguồn thải). Nguồn: trích Bảng 1 qua hoabinhxanh.vn (= hoabinhxanh.vn/qcvn-62-mt2016btnmt-nuoc-thai-chan-nuoi/), văn bản gốc trên thuvienphapluat.vn (403 qua curl, dùng bản trích).

## 2. Cơ chế: vì sao BOD/COD/TSS cao là vấn đề

### BOD5 (Nhu cầu oxy sinh hóa, 5 ngày, 20°C)
- = lượng oxy vi sinh vật tiêu thụ để phân hủy chất hữu cơ. BOD cao = nước giàu "thức ăn" hữu cơ.
- Cơ chế hại: xả ra ao/hồ/sông → vi sinh trong nguồn tiếp nhận ăn + tiêu thụ oxy hòa tan (DO)
  → DO cạn kiệt → cá/tôm/thủy sinh chết ngạt; hết oxy → chuyển kỵ khí → đen, hôi, sinh H₂S/metan/amoniac.
- Góc kinh tế: BOD cao = hệ thống phải bơm thêm oxy, tốn điện, bể sinh học phải to hơn.

### COD (Nhu cầu oxy hóa học, oxy hóa bằng kali bicromat)
- = oxy cần để oxy hóa TOÀN BỘ chất hữu cơ (kể cả phần vi sinh không ăn được). COD luôn ≥ BOD5.
- Chênh lệch COD−BOD = phần khó phân hủy sinh học (hóa chất, thuốc, hợp chất bền).
- Tỷ lệ BOD/COD quyết định công nghệ: cao → xử lý sinh học là chính; thấp → phải thêm công đoạn
  hóa lý trước bể sinh học, không thì không bao giờ đạt chuẩn.
- Đo COD chỉ mất vài giờ (BOD chờ 5 ngày) → dùng để giám sát hàng ngày.

### TSS (Tổng chất rắn lơ lửng, hạt > 2 micron)
- = hạt rắn không lắng: hạt hữu cơ, đất sét, phù sa, vi khuẩn, tảo. Nước càng đục TSS càng cao.
- 4 tác hại:
  1. Cản trở khử trùng: vi khuẩn ẩn TRONG hạt rắn không tiếp xúc clo/UV → nước tưởng xử lý vẫn chứa mầm bệnh.
  2. Chặn ánh sáng: ngăn quang hợp thực vật thủy sinh, tăng nhiệt độ nước → rối loạn hệ sinh thái.
  3. Bồi lắng: tích tụ trong đường ống, bể, kênh mương → tắc nghẽn, phải nạo vét.
  4. Vận chuyển chất bẩn: hạt rắn là chỗ bám của vi khuẩn, kim loại nặng, N/P.

## 3. Cách đọc kết quả thử nghiệm khi đối chiếu chuẩn (bài học CT888)

- M1 (sau tách phân) là vị trí ĐẦU hệ thống, nước đậm đặc nhất — đối chiếu "còn trên chuẩn"
  ở M1 KHÔNG có nghĩa hệ thống xử lý thất bại; phải phân biệt đầu nguồn vs đầu ra.
- Ví dụ CT888 ngày 15 tại Xuân Thiện: BOD5 M1 = 91 mg/L < chuẩn Cột B (100) ✓; Tổng N M2A =
  65 mg/L < 150 ✓; nhưng TSS 455 và COD 1.236 còn trên chuẩn → kết luận trung thực:
  "giảm 84–92% tải ô nhiễm ở đầu hệ thống, cần xử lý lần 2 + liều cao hơn để về sát chuẩn".
- Khi gửi lãnh đạo: nói "giảm tải ô nhiễm đầu hệ thống", KHÔNG nói "đạt chuẩn xả thải" khi chưa.

## 4. Nguồn tham khảo (đã fetch được trong session 09/2026)

- CCEP.vn — "BOD, COD, TSS, Amoni là gì": ccep.vn/chi-tieu-o-nhiem-nuoc-thai/ (BOD/COD/TSS cơ chế, rõ nhất)
- Môi Trường Hợp Nhất — "Chỉ tiêu BOD, COD, TSS trong xử lý nước thải": moitruonghopnhat.com
  (TSS định nghĩa, tác hại, phương pháp xử lý; tham khảo GS. Lâm Minh Triết)
- Primer.vn — "BOD5 là gì": primer.vn/bod5-la-gi/ (định nghĩa BOD5 chuẩn)
- hoabinhxanh.vn — Bảng 1 QCVN 62-MT:2016/BTNMT (giá trị Cột A/B)