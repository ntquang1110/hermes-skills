# Bộ chấm điểm công thức — công thức toán và cách đọc

## Hai trục

```
Tổng = 0,5 × E + 0,5 × S
```

Hai trục ngang nhau vì sản phẩm kém ổn định thì hiệu quả bằng 0 sau 3 tháng nằm kho.

## E — hiệu quả trên vật chủ (0–100)

Mỗi cửa lấy ứng viên mạnh nhất, cộng thêm phần dự phòng từ **cơ chế khác**:

```
giá trị 1 chất tại 1 cửa = 0,45 × min(1, bậc_bằng_chứng / 3)
                        + 0,30 × min(1, liều_dùng / liều_đã_thử_max)
                        + 0,25 × min(1, nồng_độ_đạt_được / MIC)     ← 1,0 nếu không phải kháng khuẩn

điểm_cửa = 100 × trọng_số_cửa × min(0,95 ; mạnh_nhất + 0,25 × mạnh_nhất_ở_cơ_chế_khác)
E = Σ điểm_cửa
```

- Bậc bằng chứng chia 3 chứ không chia 4: bậc 2 (`in vivo` đúng loài) đã đạt 0,67, bậc 3 trở lên = 1,0.
  Lý do: khác biệt giữa "thử trên heo" và "thử trên heo nhiều trại" nhỏ hơn khác biệt giữa "có thử trên
  heo" và "chỉ in vitro".
- Hệ số 0,45 / 0,30 / 0,25 là **do người dựng đặt**. Ghi rõ trong báo cáo. Đổi là đổi công thức.
- Liều vượt `liều_đã_thử_max` bị trừ, không được thưởng: `dn = max(0,4 ; 1 − (liều/max − 1))`.
- Trần 0,95: không công thức nào đáng điểm tuyệt đối, luôn còn phần chưa biết.

### Trọng số cửa

Tiêu chảy (4 cửa): chặn mầm trong cám–nước 20 · qua hàng rào ruột 35 · hậu quả/giữ ăn 30 ·
miễn dịch niêm mạc 15.

Hô hấp (không có cửa chặn mầm vào, vì mầm vào bằng không khí): hàng rào hô hấp 35 · bám cư trú 30 ·
giữ ăn 20 · mầm trong cám 15.

Hệ quả cần nhớ: **công thức hô hấp yếu hơn công thức tiêu chảy về mặt lý thuyết.** Không hứa hai công
thức ngang nhau.

### Cửa trống là lỗ hổng lớn nhất

Nếu một cửa có trọng số 15–35% mà không nguyên liệu nào chấm được (chưa có bằng chứng trên loài đích),
điểm cửa = 0 và đó là **trần của cả công thức**.

### Chẩn đoán trần — đọc điểm từng cửa, không chỉ đọc tổng

Sau mỗi lần tối ưu, in **điểm từng cửa** rồi tự hỏi: *cửa nào đã chạm trần 0,95?*

Kết quả thật đo được: TC-1 đạt D 19,0/20 · A 33,2/35 · B 28,5/30 · **C 0/15**, và tăng ngân sách từ
10 lên 20 kg/tấn **không đổi một điểm nào**.

Câu phải nói với khách: **mọi cửa đã có chất đều đã chạm trần — thêm nguyên liệu thứ bảy, thứ tám vào
cửa A hay B là đổ tiền xuống sông. Tiền đó dồn vào tìm một chất cho cửa trống.** Đây là kết luận có giá
trị nhất trong cả báo cáo, và nó chỉ hiện ra khi đọc điểm theo từng cửa.

Hệ quả phụ: nếu tổng điểm ở ngân sách 10 và 20 kg/tấn giống hệt nhau, **đừng bán bản 20 kg/tấn** cho
khách vì nó không mua thêm hiệu quả, chỉ mua thêm giá vốn.

## Kiểm nồng độ đạt được so với MIC — phép kiểm lộ ra cơ chế thật

Mọi chất được quảng cáo là "kháng khuẩn" phải qua phép kiểm này trước khi vào công thức. Ba số phải đi
liền nhau: **liều trộn · nồng độ đạt được · MIC**.

```
nồng độ trong lòng ruột (µg/mL) = liều trong cám (mg/kg) × lượng cám ăn (kg/ngày)
                                  ÷ thể tích dịch ruột (L)

tỉ lệ = nồng độ đạt được / MIC          ← < 1 nghĩa là không đủ diệt khuẩn tại chỗ
```

Giả định phải ghi rõ khi báo cáo (không phải số nguồn): heo con cai sữa 20 kg ăn 1,0 kg cám/ngày, thể
tích dịch ruột non 1,5–2,5 L; heo 8 kg ăn 0,35 kg/ngày.

**Ca thật đã gặp — berberine:** liều dùng trong bài 50 mg/kg cám, MIC đo trên APP là 312,5 µg/mL
⇒ nồng độ đạt được ~25 µg/mL, **thiếu 12,5 lần**. Nhưng bài đó vẫn đo được hiệu quả thật (ADG P=0,024,
chỉ số tiêu chảy P=0,003) và đo kèm AQP8 (P<0,001) với SLC9A3 (P<0,001) — kênh nước và bơm Na⁺/H⁺ của
biểu mô ruột.

Kết luận ghép từ hai số đã đo: **berberine không diệt khuẩn ở liều trộn cám, nó điều hoà vận chuyển nước
và điện giải của biểu mô ruột.** Vì thế nó phải xếp cùng nhóm ORS ở cửa hậu quả, **không** xếp vào nhóm
kháng khuẩn. Xếp sai nhóm là chồng ba bốn chất lên cùng một cửa và hở sạch cửa khác.

Ba hệ quả dùng ngay:
- Chất nào `nồng độ/MIC < 1` thì **cấm ghi cơ chế kháng khuẩn** trong hồ sơ, kể cả khi bài báo nói vậy.
- Muốn đủ MIC thì phải tính ngược liều, và kiểm liều đó có nằm trong dải đã thử trên loài đích không.
  Ví dụ protoberberin: MIC 8–32 µg/mL ⇒ cần **≥50 mg/kg cám** mới có cơ sở.
- Chỉ chất nào có `nồng độ/MIC ≥ 1` mới được tính điểm đầy ở phần MIC. Chất chưa có MIC thì để trống và
  nói rõ đó là **ân hạn**, không phải bằng chứng.

## S — ổn định sản phẩm (0–100)

`S = 100 − Σ hình phạt`. Các hình phạt dùng được ngay:

| Hình phạt | Điểm | Gỡ được bằng | Mức bằng chứng |
|---|---|---|---|
| Acid tự do + nền kiềm/carbonat (trung hoà, sủi CO₂, vón cục) | 25 | chỉ bằng cách bỏ một trong hai; tách gói gỡ 30% | có PMID |
| Khoáng sét mạnh + hoạt chất hữu cơ (hấp phụ) | 20 | tách gói gỡ 60%, còn 8 tồn dư | có PMID |
| Acid tự do + khoáng sét aluminosilicat | 8 | tách gói | chưa có nguồn |
| Acid tự do + humate | 8 | tách gói | chưa có nguồn |
| Humate + hoạt chất hữu cơ | 8 | tách gói | chưa có nguồn |
| **Acid tự do + bào tử Bacillus** | **5** (không phải 14) | tách gói | cặp ghi `chua_co_nguon`, đánh giá trung tính |
| **Acid tự do + muối kẽm hữu cơ** | **0** | — | `in_vitro`: trung tính |
| Acid tự do hút ẩm / ăn mòn thiết bị | 5 | dùng muối acid | có PMID (gián tiếp) |
| Tanin + protein huyết tương (kết tủa) | 14 | bỏ một trong hai | `in_vivo_heo` |
| Tanin + IgY (kết tủa kháng thể) | 10 | bỏ một trong hai | chưa có nguồn |
| Tanin + enzyme | 10 | bọc enzyme | chưa có nguồn |
| Tanin + oligosaccharide (MOS/GOS) | 6 | tách gói | chưa có nguồn |
| Tanin + khoáng sét | 6 | tách gói | chưa có nguồn |
| **Tanin + ion kim loại** | **0** | — | `in_vivo_heo`: trung tính |
| **Kẽm tan + phytate khẩu phần** | **8, luôn áp dụng** | chỉ bằng phytase hoặc ZnO cơ học hoá | `in_vitro` + 42/24/27% sinh khả dụng |
| Khoáng sét + tinh dầu | 10 | bọc tinh dầu; hoặc intercalate chủ đích thì đảo thành hiệp lực | `in_vitro` |
| Khoáng sét + oligosaccharide | 6 | tách gói | chưa có nguồn |
| Đất hiếm + phytate khẩu phần | 10 | không gỡ được | `in_vivo_heo` |
| Đất hiếm + khoáng sét / acid hữu cơ / tanin | 10 / 6 / 8 | tách gói một phần | chưa có nguồn |
| **Cam thảo (glycyrrhizin) + alkaloid (berberine, protoberberin)** | **12** | bỏ một trong hai, không tách gói được | `in_vivo_loài_khác` |
| **IgY không bọc (pH dạ dày 2–4 + pepsin phá)** | **8, luôn áp dụng** | chỉ bằng bao tan trong ruột | `in_vivo_heo`, 2 PMID |
| Acid tự do + IgY (biến tính ngay trong bao) | 12 | tách gói | `in_vivo_heo` (gián tiếp) |
| **1-monolaurin/GML + Ca²⁺/Mg²⁺ (xà phòng)** | **4** | tránh nguồn Ca dễ tan | chưa có nguồn |
| **Monoglyceride MCFA C8–C10 + Ca²⁺** | **0** | — | `in_vivo_heo`: trung tính |
| Kiềm + butyrate bọc (nhả sớm) | 8 | bọc chịu kiềm | chưa có nguồn |
| Kiềm + flavonoid / tinh dầu phenol | 4 / 8 | bọc | chưa có nguồn |
| Kiềm + IgY (mất hoạt tính) | 10 | bỏ một trong hai | chưa có nguồn |
| Nhiệt ép viên 70–90 °C trên tinh dầu / men / enzyme / butyrate / **peptide ngắn (Gly-Gln)** | 0 nếu đã bọc · 7 nếu không rõ · 15 nếu không bọc | bọc (trần tổng 30) | `in_vivo_heo` + loài khác |
| Trộn trên 5 nguyên liệu (phân tầng, khó đều) | 1,5 mỗi nguyên liệu vượt, trần 9 | giảm số nguyên liệu | suy luận |

### Điểm cộng hiệp lực — bắt buộc phải có

Chỉ trừ mà không cộng thì bộ tối ưu luôn ra công thức mỏng, dễ sụp khi một cơ chế hỏng:

| Cặp | Điểm | Mức bằng chứng |
|---|---|---|
| Acid hữu cơ tự do + tinh dầu phenol (thymol, carvacrol) | **+8** | `in_vivo_heo` |
| Oligosaccharide + men vi sinh (Bacillus) | +6 | chưa có nguồn |
| Humate + kẽm | +5 | `in_vivo_loài_khác` |

`S = min(100 ; 100 − Σ phạt + Σ thưởng)`. Sau khi sửa theo bằng chứng, S của công thức tốt rơi vào
**95–98,5** — không còn 100. Nếu bảng vẫn cho ra toàn 100 thì bảng đó sai, không phải công thức hoàn hảo.

**Mọi hình phạt tự nghĩ ra phải đối chiếu bản đồ có PMID trước khi dùng để chốt công thức.** Sáu cặp
đoán ban đầu đã bị bác bỏ và danh sách nằm ở `incompatibility-map.md`.

Tách gói **không bao giờ gỡ 100%**: acid và kiềm, khoáng sét và thảo dược vẫn gặp nhau trong lòng ruột.

## Leo dốc tối ưu

```
seed → sửa cho khả thi (≤ ngân sách, ≤ liều max)
lặp:
  thử đổi liều từng nguyên liệu (4 mức trong dải đã thử)
  thử thêm 1 nguyên liệu (chỉ nguyên liệu có nhãn đúng bệnh)
  thử bỏ 1 nguyên liệu (trừ nhóm bị ép)
  giữ thay đổi tốt nhất; nếu không có → DỪNG
```

Mỗi vòng một thay đổi, ghi log `(vòng, hành động, điểm sau)`. Log này là bằng chứng của việc tối ưu,
kèm vào báo cáo.

## Chấm biến thể bị ép

Khi khách yêu cầu một biến thể có thêm nhóm cố định (ví dụ kiềm + khoáng + đất hiếm), để bộ tối ưu tự
do thì nó sẽ **loại sạch** nhóm đó vì chỉ thêm hình phạt. Phải chạy chế độ **ép buộc** (không được bỏ
các nguyên liệu bị ép) rồi báo **Δ điểm so với bản không ép**.

Δ thực tế đo được **sau khi sửa luật theo bằng chứng** (hô hấp): −44,2 (0,5% một bao) · −29,7 (1% một
bao) · −20,7 (1% hai gói) · −16,0 (2% hai gói). Tiêu chảy: −29,2 · −20,1 (1% hai gói) · −15,2 (2% hai gói).

Chú ý: khi bảng hình phạt còn dùng luật đoán, Δ chỉ khoảng −41; sau khi thay bằng luật có bằng chứng,
Δ xấu đi thành −44,2. **Công thức bị ép luôn đắt hơn khi chấm bằng bằng chứng thật — đừng chốt giá
bán dựa trên con số từ bảng luật đoán.**

Hai câu phải nói:
- *Nếu mục tiêu là hiệu quả thì đừng làm bản ép; nếu mục tiêu là câu chuyện sản phẩm thì làm nhưng đừng
  quảng cáo nó mạnh hơn.*
- *Bản ép bắt buộc dùng **muối/ester acid** (K-diformat) thay acid tự do, và phải tách 2 gói — tách gói
  gỡ lại 8–14 điểm.*

Kiểm tra bộ tối ưu có tự chọn đúng không: khi để tự do, nó phải chọn K-diformat chứ không chọn acid
benzoic trong bản ép. Nếu nó chọn acid tự do thì bảng hình phạt đang thiếu cặp acid tự do ↔ carbonat.

## Đọc kết quả cho đúng

- Điểm chênh dưới 2 điểm là **nhiễu**, đừng kết luận thắng thua.
- Trùng điểm ở nhiều ngân sách nghĩa là công thức đã bão hoà theo mô hình, không phải đã tối ưu thật.
- Nếu bộ tối ưu liên tục chọn đúng một chất cho một cửa, kiểm lại xem đã thưởng cơ chế dự phòng chưa.
