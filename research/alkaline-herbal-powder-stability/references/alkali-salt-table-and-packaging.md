# Bảng muối kiềm + giữ pH ≥ 12 trong bột 24 tháng + bao bì

## 1. Bảng muối kiềm (chọn theo pKa cặp đệm, không theo "độ mạnh base")

| Muối | pH 1 % w/v | pH 10 % | Cặp đệm (pKa) | Dạng | Hút ẩm / deliquescence | Giữ pH ≥12? |
|---|---|---|---|---|---|---|
| **Na₃PO₄** (TSP) | ~11,8–12,1 đo / 12,6 lý thuyết | 12,3–13,0 | PO₄³⁻/HPO₄²⁻ **pKa3 12,35** | khan (hút ẩm TB) / 12H₂O (phong hóa) | Không deliquescent như NaOH | **Có — ứng viên số 1** (đệm đúng vùng 11,3–13,3) |
| **Na₂SiO₃ / nước thủy tinh** | ~12,7 (nguồn thương mại, chưa verify) | ~13 | silicic pKa1 9,8 (verify) / pKa2 ~11,8–12,5 (chưa verify) | khan / dung dịch | TB, tạo màng cứng khi ẩm | **Có — số 2**; CO₂ + silicat → SiO₂ gel **tự niêm phong** giảm khuếch tán |
| NaOH | 13,0–13,4 | ~14 | không đệm | rắn, deliquescent, CRH ~10–15 % | rất mạnh (chảy nước) | Chỉ khi bao kín tuyệt đối; thực tế KÉM |
| KOH | ~13,2 | ~14 | không đệm | rắn, deliquescent | rất mạnh, ít tạo lớp vỏ cản | KÉM hơn NaOH |
| Na₂CO₃ | ~11,4–11,6 | ~11,8–12,1 | HCO₃⁻/CO₃²⁻ pKa2 10,33 | khan (hút ẩm) / 10H₂O (phong hóa) / 1H₂O | TB | **Không đạt trần** (trần ~11,6 ở 1 %) |
| K₂CO₃ | ~11,6 | ~12,1 | pKa2 10,33 | rất tan, hút ẩm mạnh | mạnh | Không đạt trần; tệ hơn Na₂CO₃ về bảo quản |
| NaHCO₃ | ~8,3 | ~8,3 | lưỡng tính (6,35/10,33) | bền | thấp | Không — nhưng là "xương sống" của đệm cacbonat |
| Na₂HPO₄ | ~9,8 | ~10 | lưỡng tính (7,20/12,35) | 12H₂O/7H₂O/khan | TB | Không (chỉ dùng chỉnh pH) |
| Ca(OH)₂ | 12,4–12,6 | ~12,6 | độ tan giới hạn 1,73 g/L ⇒ **đệm ≈ 0** | bột | hút ẩm → CaCO₃ | Đạt pH ban đầu, **không giữ được** |
| CaO | — | — | nguồn kiềm sau khi tôi | bột | hút ẩm rất mạnh (dùng làm hút ẩm) | Không nên cho vào phần pha trực tiếp (bỏng nhiệt + kiềm) |
| MgO / Mg(OH)₂ | ~10,4–10,5 (bão hòa) | ~10,5 | Ksp ≈ 5,6×10⁻¹² | bột | MgO hút ẩm nhẹ | Không đạt 12 — chỉ chống vón/hút ẩm |

**Kết luận cấp bảng:** chỉ nhóm có pKa ≈ 12–12,4 (**phosphate, silicat**) vừa đạt pH ≥ 12 vừa **giữ được**
pH khi bị CO₂ tấn công. Mọi hệ cacbonat có trần ~11,4–12,1. NaOH/KOH đạt pH nhưng không có phanh.

## 2. Thang chẩn đoán pH khi pha lại (đọc ra dạng tồn tại của kiềm)

```
1 % NaOH   13,0–13,4   → hydroxide còn nguyên
1 % Na₂CO₃ 11,4–11,6   → đã chuyển thành cacbonat (mất ~1,5–2 đơn vị pH)
1 % NaHCO₃  8,3        → đã bicacbonat hóa (pH sụp)
```
Đo pH thấp ở 1 % mà bột vẫn còn kiềm dư ⇒ **cacbonat hóa**, không phải "hết kiềm". Đối chiếu thêm bằng
**độ kiềm tổng** (chuẩn độ bằng HCl): độ kiềm tổng còn cao nhưng pH thấp = đã bị CO₂ chuyển hóa.

## 3. Ngân sách CO₂ (phép tính phải trình bày, không chỉ nói định tính)

Nguồn số: CO₂ khí quyển 2024 = 422,8 ppm (climate.gov, verify).

```
n_khi(1 L, 30 °C, 1 atm) = PV/RT = 101325 · 0,001 / (8,314 · 303,15) ≈ 0,0402 mol
CO₂ trong 1 L            = 0,0402 · 422,8e-6 ≈ 1,7e-5 mol = 0,017 mmol
CO₂ + 2 OH⁻ → CO₃²⁻ + H₂O   (1 mol CO₂ trung hòa 2 mol OH⁻)

Trao đổi khí kiểu "hô hấp bao bì" (headspace 5 L, ΔT ngày/đêm 30→22 °C ⇒ ΔV/V ≈ 2,6 %):
  2 chu kỳ/ngày × 730 ngày × 0,13 L ≈ 190 L khí / 24 tháng
  CO₂ ≈ 190 × 0,017 ≈ 3,2 mmol ⇒ trung hòa ≈ 6,4 mmol OH⁻ ≈ 0,26 g NaOH
Nếu 100 g bột chứa 5 g NaOH (125 mmol OH⁻) ⇒ mất ~5 % kiềm ⇒ ΔpH chỉ ~0,1–0,3 (pH là thang LOG).
```
**Hệ quả thực chiến (ngược trực giác, đã kiểm tra):** trong bao KÍN, CO₂ khí quyển KHÔNG phải thủ phạm
làm mất pH. Thủ phạm thật là **ẨM**: khi bột hút ẩm/deliquesce, tạo màng nước → CO₂ liên tục hòa tan và
cacbonat hóa nhanh, đồng thời pH cục bộ lớp bề mặt sụp. Vì vậy ưu tiên thiết kế: **aw < 0,2 + rào cản
ẩm**, không phải "chống CO₂".

## 4. Quan hệ pH ↔ liều kiềm ↔ nồng độ pha (gốc rễ nhiều tranh cãi đạt/không đạt)

```
pH 12  ⇒ [OH⁻] = 10 mmol/L;  pH 11,5 ⇒ ≈ 3,2 mmol/L;  pH 12,5 ⇒ ≈ 31,6 mmol/L
Đo ở 1 % w/v (10 g bột/L): cần ~10 mmol OH⁻/L = 1 mmol/g bột = 40 mg NaOH-đương lượng/g ⇒ ~4 % kl
                           (với Na₃PO₄: cần ≈ 0,0045 M trong dung dịch ⇒ ~7–8 % kl bột)
Đo ở 5 % w/v (50 g bột/L): yêu cầu GIẢM 5 lần ⇒ ~0,9 % NaOH-đương lượng, ~1,5 % Na₃PO₄
⇒ LUÔN ghi kèm nồng độ pha trong chỉ tiêu pH, và ghi cả pH 0 phút và 30 phút (nước đã đun loại CO₂).
```

## 5. Bao bì & hạn dùng

| Hạng mục | Mục tiêu | Ghi chú |
|---|---|---|
| Độ ẩm bột | ≤ 1 % (nhắm 0,5 %) | dạng khô cũng cần điểm hoạt độ thấp |
| aw | ≤ 0,15–0,20 | ngưỡng quyết định: trên ngưỡng này mọi phản ứng chạy lại |
| Vật liệu | màng nhôm ≥ 4 lớp (PET/Al/PA/PE), **Al ≥ 9 µm** | WVTR < 0,1 g/m²·ngày vs PE đơn lớp ~5 ⇒ chênh 50× |
| Gói 2 lớp Al / có tráng | khi cần chống lỗ kim | màng 1 lớp Al dễ thủng ở mép hàn |
| Hút ẩm | silica gel (yếu ở RH thấp) / rây phân tử (tốt ở RH thấp) / CaO | cân tính theo thể tích headspace + độ ẩm xâm nhập |
| Hút CO₂ | vôi Ca(OH)₂ **nhưng nhả H₂O** | phải ghép hút ẩm khi dùng |
| N₂ flush | giảm O₂/ẩm headspace | thứ tự ưu tiên: hút ẩm > N₂ > hút CO₂ |
| Thử | 24 tháng 30 °C / 75 % RH (điều kiện IVb) + **in-use** mở 2 lần/tuần × 4 tuần | mốc 0/3/6/12/18/24; n ≥ 3 gói/mốc; để cả đứng và nằm |

### Phân biệt LỖI BAO BÌ vs LỖI CÔNG THỨC (bắt buộc lấy mẫu phân tầng)

| Dấu hiệu | Kết luận | Hành động |
|---|---|---|
| pH giảm **chỉ lớp bề mặt** (1 cm đầu), lõi vẫn ≥12; khối lượng gói TĂNG; vón cứng trên mặt | **Lỗi bao bì** (hàn lỗi, lỗ kim, thiếu hút ẩm) | dye penetration ASTM F1929, bubble ASTM D3078, seal strength ASTM F88; soi mép hàn |
| pH giảm **đều mọi lớp, ngay từ T0** | **Lỗi công thức/quy trình** (thiếu liều kiềm theo nồng độ pha, mất kiềm khi phối trộn) | tính lại theo mục 4; so pH dịch trước sấy vs bột tái pha |
| Chỉ vài gói trong lô bị | lỗi hàn theo lô | kiểm seal trên đúng gói bị |
| pH ổn nhưng độ kiềm tổng giảm | đã cacbonat hóa một phần (đệm đang làm việc) | chấp nhận nếu pH còn ≥ chỉ tiêu; kiểm tra lại rào cản ẩm |
| Bột màu nâu, A420 tăng, mùi khét | oxy hóa phenol / Maillard, không phải lỗi bao bì | xem `references/ph12-active-stability.md` |

## 6. Phương án khi không thể giữ pH ≥ 12 (nói thẳng, đừng hứa)

1. **Dạng 2 ngăn**: bột thảo dược bảo quản ở pH thấp (ổn định hơn nhiều) + kiềm (bột/viên nén) pha ngay
   trước dùng — tốt nhất cho việc *giữ hoạt chất*, đổi lại thao tác 2 bước.
2. **Gói liều đơn** (stick/sachet 1 lần mở) — cắt trao đổi khí nhiều lần mở.
3. **Dạng dung dịch** chai HDPE/PP kín (tránh PET/PETG và nhôm trần ở pH cao) — nặng, tốn vận chuyển.
4. **Viên kiềm nén** (giảm diện tích bề mặt) trong ống kín có hút ẩm.
5. **Hạ chỉ tiêu** xuống pH 10,5–11,5 hoặc chuyển sang chỉ tiêu "độ kiềm tổng" / "pH huyền phù 10 %".
6. Dạng **khan/không nước** (phân tán trong pha dầu) khi công thức cho phép.

Giá trị chưa verify (ghi `note='chưa verify'` khi dùng): pKa2 acid silicic, pH 1 % thực đo của Na₂CO₃ và
natri metasilicat (nguồn thương mại), pH 10 % của vài muối, giá trị MDRH định lượng của hỗn hợp muối
(hiệu ứng làm giảm RH deliquescence so với từng muối riêng — định tính thì đã rõ).
