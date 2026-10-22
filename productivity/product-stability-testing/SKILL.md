---
name: product-stability-testing
description: "Use when đo độ ổn định/hạn dùng sản phẩm."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [stability, shelf-life, han-dung, ich, tcn, tpbvsk, premix, vung-khi-hau, do-on-dinh]
---

# Thử độ ổn định / hạn dùng sản phẩm (Việt Nam)

Dùng khi: soạn đề cương thử độ ổn định, xin báo giá phòng kiểm nghiệm, trả lời "sản phẩm để được bao lâu",
hoặc khi một mô hình/điểm số nội bộ đang được dùng như bằng chứng ổn định (nó không phải).

Áp dụng cho: premix/thức ăn bổ sung chăn nuôi · TPBVSK · dung dịch & bột thảo dược.

## Rule 0 — Điểm ổn định của model KHÔNG phải độ ổn định của sản phẩm

Dự án premix từng có điểm ổn định **S = 100** trên mọi công thức. Con số đó chỉ nghĩa là **engine không tìm ra
cặp tương kỵ nào trong tổ hợp**; nó KHÔNG đo được thoái hoá theo thời gian. Bằng chứng thật: khi ép thêm nền
kiềm + nền khoáng, S rơi 88 → 70 → 82 — tức con số chỉ phản ánh dữ liệu tương kỵ đã biết. **Muốn nói "ổn định"
với khách thì phải có thử gia tốc + dài hạn thật.** Nói thẳng câu này khi ai đó trích S=100 như bằng chứng.

## Điều kiện chuẩn — Việt Nam là vùng khí hậu IVB

| Việc | Điều kiện | Nguồn |
|---|---|---|
| Dài hạn (đúng khí hậu VN) | **30 °C ± 2 °C / 75% RH ± 5%** | ASEAN Guideline on Stability Study of Drug Product — vùng ASEAN dùng điều kiện **IVB (30 °C/75% RH)**; VN là IVB (nóng, rất ẩm) |
| Gia tốc | **40 °C ± 2 °C / 75% RH ± 5%**, tối thiểu **6 tháng** | ICH Q1A(R2); bảng điều kiện theo vùng của WHO (TRS 953 Phụ lục 2) để IVB gia tốc ở 40/75 |
| Số lô | tối thiểu **3 lô** mỗi công thức | ICH Q1A(R2) — chọn lô phải từ ≥3 lô |
| Khi gia tốc có thay đổi đáng kể | chạy thêm trung gian **30 °C/65% RH** + tiếp tục dài hạn | ICH Q1A(R2) |

**Bẫy vùng khí hậu (đã dính):** dùng **25 °C/60% RH** vì "theo ICH" — đó là điều kiện vùng I–II. Bảo quản ở
Việt Nam mà đo ở 25/60 là đo sai chỗ; sản phẩm đạt 25/60 vẫn có thể gãy ở 30/75.

## Thiết kế thử — tối thiểu nhưng không cãi được

- **3 lô TRỘN RIÊNG** mỗi công thức. Một mẻ lớn chia ba thì chỉ đo độ lặp của máy trộn, không đo được công thức.
- **2 kiểu bao chạy song song**: (1) bao thật đúng như bao sẽ bán; (2) **bao hở cố ý** (hàn không kín 1 góc).
  Nhánh hở là cách duy nhất biết sản phẩm chết vì **ẩm** hay vì **công thức** — không có nó thì kết quả xấu cũng
  không biết sửa bao hay sửa công thức.
- Mốc: **T0 · gia tốc 1/3/6 tháng · dài hạn 3/6/12 tháng**.
- Có Bacillus/men vi sinh thì **bắt buộc** thử riêng ở dạng bào tử — đây là chỗ dễ chết nhất.
- Giữ **mẫu đối chiếu T0 đủ nhiều**; hết mẫu T0 là mất mốc so sánh vĩnh viễn.

## Chỉ tiêu và ngưỡng (đề xuất nội bộ — ghi rõ, đừng gọi là ngưỡng cơ quan ban hành)

| Chỉ tiêu | Phương pháp | Ngưỡng |
|---|---|---|
| Cảm quan, vón, màu, mùi | quan sát | không vón/mốc, mùi không lệch T0 |
| Độ ẩm | sấy 105 °C | ≤ 8–10%, tăng ≤ 2 điểm % so T0 |
| Hoạt độ nước aw | đo aw | ≤ 0,60 (cảnh báo 0,65) |
| pH dịch 10% | điện cực | lệch ≤ 0,5 đơn vị |
| Marker hoá học (tanin · glycyrrhizin · baicalin) | Folin–Ciocalteu / HPLC-UV | ≥ **90%** so T0 |
| Chất BAY HƠI (thymol, carvacrol) | GC-FID headspace | ≥ **85%** so T0 — ngưỡng thấp hơn vì bay hơi |
| Hoạt lực vi sinh | đếm khuẩn lạc CFU/g | ≥ 10⁶ CFU/g, giảm ≤ 1 log |
| Hoạt độ enzyme | U/g | ≥ 80% so T0 |
| Vệ sinh vi sinh | theo TCVN hiện hành cho TĂCN | **chốt số trước khi in tiêu chuẩn cơ sở** — không tự bịa |
| Phân tầng trong bao 25 kg | 8–10 điểm trên–giữa–dưới | **CV < 5%** |

## Cách đọc kết quả

| Kết quả ở 6 tháng gia tốc | Kết luận | Việc làm |
|---|---|---|
| Marker ≥90%, vi sinh giảm <1 log | hạn **24 tháng** | tiếp tục dài hạn để dọn bằng chứng |
| Marker 80–90%, vi sinh giảm 1–2 log | hạn **12 tháng** | thêm vi nang 2 lớp, giữ bao |
| Marker <80% hoặc vi sinh giảm >2 log | hạn **3–6 tháng** | đổi **bao** trước, đổi công thức sau |
| Độ ẩm +>2 điểm % / aw >0,65 mà marker vẫn tốt | **lỗi bao**, không phải lỗi công thức | bao nhôm 2 lớp, hút ẩm, kiểm mép hàn |
| Nhánh hở chết, nhánh kín sống | bao là biến số lớn nhất | nâng cấp bao thành điểm bắt buộc |
| CV phân tầng >5% | lỗi trộn/gói, không phải bảo quản | tách gói nhẹ–nặng, kiểm thời gian trộn |

**Không dùng Q10 để suy hạn dùng** khi ẩm là biến chính (premix, TPBVSK ẩm): Q10 chỉ đúng khi nhiệt là biến
chính. Có hạn dùng thì phải có số dài hạn thật.

## Bảng xin báo giá — gửi đúng cái này, đừng hỏi trống "giá bao nhiêu"

Quy đổi mọi thứ thành **số phép × số lượng** rồi mới xin giá. Ví dụ thật (4 công thức × 3 lô × 2 kiểu bao × 7 mốc
= 168 điểm mẫu): buồng 40/75 chạy 6 tháng · buồng 30/75 chạy 12 tháng · GC-FID 60 lần · HPLC-UV 60 lần ·
Folin 30 lần · đếm khuẩn lạc 15 lần · hoạt độ enzyme 18 lần · độ ẩm+aw 168 · vi sinh an toàn 84 (rút còn 24
được) · CV phân tầng 24. Thời gian không rút ngắn được: **gia tốc = 6 tháng + 2–3 tuần báo cáo**.

## Pitfalls

1. **Đo 25/60 rồi kết luận cho Việt Nam.** Sai vùng khí hậu (xem bảng trên).
2. **Một mẻ chia ba lô.** Ba lô phải trộn riêng.
3. **Lấy mẫu không đại diện.** Premix phân tầng: một muỗng mặt bao khác hẳn muỗng đáy bao. Lấy sai thì thử
   nghiệm vô giá trị và không cứu được bằng thống kê.
4. **Kết luận sớm ở mốc 3 tháng.** Nhiều nền ẩm chỉ gãy sau tháng thứ 4.
5. **Trích điểm ổn định của model làm bằng chứng.** Xem Rule 0.
6. **Bịa ngưỡng vi sinh khi chưa có số TCVN.** Ghi thẳng "chốt số trước khi in tiêu chuẩn cơ sở".
7. **Đặt ngưỡng rồi gọi nó là ngưỡng luật.** 90%/85% là ngưỡng nội bộ đề xuất.
8. **Thiếu nhánh bao hở.** Không có nó thì không phân biệt được lỗi bao với lỗi công thức.

## Liên quan

- `livestock-trial-protocol` — đề cương thử nghiệm TRÊN ĐỘNG VẬT (khác: thử ổn định là thử trên SẢN PHẨM).
- `google-sheets-ops/references/product-formulation-sheet-pattern.md` — đổ định mức/điểm công thức ra Sheet.
- `fixgby` — dự án premix heo con đã dùng đề cương này (`docs/14-cong-thuc-co-ban/10-thu-on-dinh-gia-toc.md`).
