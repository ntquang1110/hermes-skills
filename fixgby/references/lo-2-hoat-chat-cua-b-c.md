# Lô 2 — Cửa B + Cửa C (hoạt chất ngoài 26 nguyên liệu)

Giao 20/10/2026. File đích: `docs/12-hoat-chat-mo-rong/batch-lo-2-kinh-te-va-tai-thai.{md,json}`.
Phạm vi: **Cửa B** (chặng `7_hau_qua`, giữ heo ăn / chịu đựng, 22 dòng) + **Cửa C** (chặng
`8_thai_lay`, cắt tải thải, 16 dòng, chỉ nhóm tiêu chảy). Không chạm A/D/E.

**Số chốt:** 19 hoạt chất (15 chạm B, 5 chạm C, 1 dùng chung) · **17 `in_vivo_heo`** · 2 `in_vitro`
(chất sát trùng môi trường) · **20 PMID verify Europe PMC 20/20** (`hitCount==1` + pmid trả về đúng) ·
40/40 spot-check số nằm trong `abstractText` → **8/38 dòng điểm cắt** được dùng · 5 trùng 26 nguyên liệu ·
`tag_H` 21 ở cấp lô + 26 ô cấp chất.

---

## 1. Cửa C nghèo vì CẤU TRÚC, không vì thiếu tìm — phân loại 16 dòng

| Loại | Số dòng | Dòng | Hệ quả |
|---|---|---|---|
| Hoạt chất chạm được **và** đã có PMID trên heo | **4** | `etec` · `salmonella` · `ascaris` · `pedv` | chỉ 4 dòng này sinh được chất |
| Hoạt chất có thể chạm nhưng **chưa có PMID nào đứng được** | **7** | `isospora` · `rota-a` · `rota-c` · `trichuris` · `pdcov` · `crypto` · `cperf` | chỉ có hướng (làm khô, vôi, sát trùng), chưa có số |
| Điểm cắt của **quy trình**, không phải của hoạt chất | **5** | `brachy-h` · `brachy-p` · `lawsonia` · `yersinia` · `cdiff` | đều là "phát hiện sớm bằng qPCR và tách heo thải" — một chất cho vào miệng heo không làm được việc của que qPCR |

Cửa B ngược lại: **18/22 dòng mở đầu bằng "bù nước"** ⇒ Cửa B phần lớn là chỗ **bán đúng** một sản
phẩm bù nước cho đúng tác nhân, không phải chỗ tìm chất mới.

---

## 2. Bank 19 hoạt chất (số lấy từ `abstractText` của chính PMID ghi cạnh)

### Cửa B

| Hoạt chất | PMID | Liều trong bài | Số trích được | Dòng cắt | Ghi chú quyết định |
|---|---|---|---|---|---|
| ORS (bù nước–điện giải) | 29718928 | 70 mL/kg/ngày, 48 h | nước tiểu **47,3 ± 9,0** vs **16,1 ± 2,5** (chỉ nước) vs **24,5 ± 1,7** mL/kg (không uống) | `brachy-h` | **Mô hình BỎNG trên heo Yorkshire, không phải tiêu chảy** — `in_vivo_heo` đúng luật nhưng phải nói rõ; `tag_H` cho hiệu quả trên tiêu chảy heo con |
| Glycyl-glutamine | 40941369 (+ đối chứng âm 40453319) | 0,25–0,50% khẩu phần; **0,25% = liều tối thiểu có hiệu lực** | ADG/ADFI/khối lượng cuối ↑ (P<0,05); CP digestibility ↑ ở 0,375–0,5% | `isospora` | dipeptide ổn định; glutamine **tự do** trong khẩu phần **lỏng** cho kết quả **NGƯỢC** (40453319: ADG ngày 14–21 ↓ P<0,05, tiêu chảy xu hướng ↑ P=0,09) |
| L-glutamate | 41029389 | 1% glutamate; 1–2% aspartate | ADG & G:F ↑ (P<0,05) ngày 0–5 sau gây nhiễm; thải β-hemolysin ↓ ngày 14 | `etec` | khớp **cả tác nhân** (ETEC F18) lẫn chặng; carbadox chỉ là đối chứng của bài |
| L-arginine | 42450709 | 400 mg/kg thể trọng/ngày uống, ngày 5–11 | phục hồi T-SOD/CAT/GSH-Px, MDA ↓; ISG (MX1/OASL/ISG15/IFITM3) ↑; IL-6/CXCL2 ↓ | `pedv` | **TÁC DỤNG NGƯỢC: làm TĂNG biểu hiện gen cấu trúc M/N/S của PEDV.** "disease tolerance", KHÔNG phải "ức chế PEDV" |
| Huyết tương sấy phun (SDP) | 41473098 | SDP tích luỹ 85–610 g/con trong nursery | độ nặng tiêu chảy ↓ (p<0,05); can thiệp y tế ↓; **chỉ số viêm phổi ↓ (p<0,001)**; FBW tăng tuyến tính (p=0,037) | `lawsonia` | **không** cải thiện ADG/ADFI/FCR trong nursery — đừng bán "tăng trọng ngay"; tăng mỡ lưng, giảm nạc (p=0,039–0,052) |
| ZnO cơ học hóa | 42602773 | **400 mg Zn/kg** vs 1600 mg ZnO thường | ADG ↑ ngày 1–14; F:G ↓; tỷ lệ tiêu chảy ↓ (**P=0,001**); tương đương 1600 mg | `lawsonia` | 1152 heo con. Mạnh nhất về số, **rủi ro nhất về quy định** (EU cấm liều dược lý từ 2022) ⇒ giải pháp chuyển tiếp |
| Sodium butyrate **bọc lipid** | 39978008 | 0,05% khẩu phần | **G:F +16%**; FITC-dextran flux **−32%**; short-circuit current −52% | `lawsonia` | nhà đang có **calcium** butyrate — khác muối, khác độ bọc, khác điểm giải phóng ⇒ **không thay 1:1** |
| Tannin chestnut | 42662228 | **0,75%** khẩu phần, 4 tuần | tiêu chảy **41,7% → 0%** (n=12/nhóm); độ ẩm phân ↓ | `brachy-p` | **đổi lấy:** ADG ↓ có ý nghĩa + RBC/Hb/WBC ↓ (thiếu máu). **KHÔNG kháng E. coli/Salmonella trong ruột** |
| Tannin quebracho (MGM-P) | 34828046 | 0,2–0,3%, 20 ngày | 0,3% cải thiện tỷ lệ tiêu chảy (p<0,05); villus height ↑, crypt depth ↓; **ADG/ADFI/FCR không đổi** | `brachy-h` | **hai loại tanin không đổi liều cho nhau** (0,75% chestnut có hại, 0,3% quebracho thì không) |
| Berberine | 41716830 | **50 mg/kg**, 28 ngày | ADG P=0,024; ADFI P=0,020; chỉ số tiêu chảy P=0,003; **AQP8 P<0,001 · SLC9A3 P<0,001** | `brachy-p` | chất **duy nhất** trong lô có số trực tiếp trên **kênh hấp thu nước** (AQP1/8/10/11 · NHE3 · NKCC1); vị đắng ⇒ nghịch lý với "giữ heo ăn" |
| Attapulgite | 36288170 | 7 kg/tấn (0,7%) | ADFI ↑, FCR tốt hơn (p<0,05) trên **1890 heo**, 6 tháng, 3 trại | `lawsonia` | bài **KHÔNG đo tiêu chảy** và **không nêu cơ chế** ⇒ cấm viết "hấp phụ độc tố" |
| Chitosan | 42816880 | 100 mg/kg | FCR ↓ ngày 6–14 (P<0,05); ADG xu hướng ↑ (0,05<P<0,10); **thải E. coli chỉ P=0,085** | `etec` | thải mầm là **xu hướng**, không được ghi "giảm thải" |
| Hương liệu hương kem sữa | 41695671 | 0,05%, 42 ngày | ADG ↑ mọi khoảng (p<0,05); ADFI xu hướng ↑ (p<0,10); tần suất tiêu chảy ngày 8–14 ↓ (p<0,05) | `lawsonia` | gần nghĩa đen "giữ heo ăn" nhất |
| Protease bọc | 42651943 | abstract **không nêu liều** | nitơ urê ↓ (p<0,01); tiêu hoá mỡ thô ↑; D-lactate & DAO ↓ (p<0,05) | `lawsonia` | so theo **hoạt độ U/kg**, không theo %; kiểm hoạt độ **sau ép viên** |

### Cửa C

| Hoạt chất | PMID | Liều | Số trích được | Dòng cắt | Ghi chú |
|---|---|---|---|---|---|
| Sodium chlorate | 17803134 | chlorate–nitrat–lactat uống/ngày × 5 ngày | giảm tỷ lệ + nồng độ Salmonella trong phân, dịch manh tràng, hạch lympho hồi-manh tràng; kéo đến 14 ngày sau cai sữa (9 ngày sau liều cuối) | `salmonella` | **KHÔNG mua được** (`da_ban_o = chua_co`) — giữ để biết cơ chế: Salmonella khử chlorate thành chlorite |
| Acid formic ester hóa, nước uống | 37760214 | 10 kg/1000 L (chế phẩm 30%), **5 ngày trước giết mổ** | nhiễm **50% vs 20%** (p<0,001); **OR 5,63** (2,92–10,8); **82,2%** ca thải được ngăn; 240 heo × 3 trại | `salmonella` | can thiệp Cửa C **rẻ nhất có số thật**; nhưng chỉ 5 ngày trước giết mổ, acid ăn mòn |
| Acid hữu cơ + monoglyceride | 39838409 | abstract không nêu | tần suất tiêu chảy ↓ (P<0,05); **coliform dung huyết β trong phân ↓ ngày 10** (P<0,05); chuyển vị hạch mạc treo ↓ | `etec` | dòng C duy nhất nói thẳng "giảm tải thải" cho một mầm; **không** cải thiện tăng trọng |
| Chlorine dioxide | 39437589 | **0,5–2%**, 15 ngày ở 22–25 °C | ức chế **hoàn toàn** phát triển trứng *A. suum* đến L2 | `ascaris` | chỉ **in_vitro** trên trứng; 0,5–2% là nồng độ sát trùng bề mặt, không dùng cho nước uống |
| Potassium peroxymonosulfate (Virkon S) | 41361821 | PPMS 0,5–2% · NaOH 1–3% · ethanol 80% | giảm **≥4 log10 TCID50/mL** với TGEV & PRCV; acetic acid/H₂O₂/phenol **KHÔNG đạt** | `pedv` | **bằng chứng là TGEV/PRCV, KHÔNG phải PEDV** ⇒ `tag_H` bắt buộc |

---

## 3. Ba phát hiện ngược (đáng giá hơn cả bảng)

1. **Tanin KHÔNG thuộc Cửa C.** Brief chỉ định tanin cho "giảm tải Salmonella"; `42662228` nói thẳng
   tanin **không có tác dụng kháng E. coli hay Salmonella trong ruột**. Cái nó làm được là giảm độ ẩm
   phân + tỷ lệ tiêu chảy ⇒ **Cửa B**. Ai đang bán tanin như "giảm Salmonella trong phân" thì câu đó
   không có nguồn.
2. **Tanin chestnut 0,75% phải trả giá bằng tăng trọng và hồng cầu** (ADG ↓, RBC/Hb/WBC ↓), trong khi
   quebracho 0,2–0,3% không hại tăng trọng nhưng yếu hơn ⇒ hai loại trong nhà **không đổi liều cho nhau**.
3. **Arginine làm tăng lượng virus PEDV** (gen M/N/S ↑) — đúng cho "giữ heo chịu đựng", tuyệt đối không
   được trình bày là "ức chế PEDV". Cùng họ cảnh báo với glutamine: **dạng bào chế quyết định chiều kết quả**.

---

## 4. Bảy khoảng trống đã xác nhận

| Dòng cắt | Vì sao trống |
|---|---|
| `rota-a` · chặng 7 — "…và **giảm tải lactose**" | không tìm được PMID thí nghiệm trên heo cho lactase / khẩu phần giảm lactose ở heo con tiêu chảy. **Dòng hấp dẫn nhất còn trống của Cửa B** |
| `cdiff` · chặng 7 — "hỗ trợ tuần hoàn" | không có hoạt chất đường uống nào có PMID đo được |
| `salmonella`/`yersinia` · chặng 7 — "hạ sốt" | không có ứng viên không-kháng-sinh, không-NSAID có PMID trên heo |
| `app`/`cperf` · chặng 7 — "cứu trong vài giờ" | bản đồ đã ghi can thiệp tới muộn |
| 5 dòng quy trình của Cửa C | qPCR + tách heo, không phải hoạt chất |
| 7 dòng Cửa C còn lại | chỉ có hướng (làm khô/vôi/sát trùng), chưa có số trên heo |
| `pedv`/`pdcov` · chặng 8 — "**làm khô nền**" | `39437589` **có** thử vôi sống nhưng abstract **không báo cáo** tỷ lệ bất hoạt của vôi ⇒ không được trích số |

---

## 5. Mẫu truy vấn đã cứu lượt này

`sort=''` (relevance) + trường `TITLE:` là tổ hợp hiệu quả nhất; `CITED desc` trả về review tổng
(không số) cho hầu hết truy vấn lô này.

```
'tannin AND (pig OR piglet) AND (Salmonella OR shedding OR diarrhea)'
'TITLE:tannin AND (piglet OR "weaned pig")'          -> ra đúng 42662228 / 34828046
'sodium chlorate AND (pig OR swine) AND Salmonella'   -> ra 17803134
'zeolite AND (piglet OR "weaned pig") AND (diarrhea OR ammonia)'
'chlorine dioxide OR "peracetic acid" AND pig AND drinking water'
'TITLE:flavor AND (weaned pigs OR piglet) AND (growth OR intake)'
'bioconversion' không dùng; thay bằng tên chất cụ thể + (pig OR piglet)
```

**Bẫy đã dính:** query rộng `'pig'` nuốt cả `guinea pig`; `hitCount` 300–1000 là dấu query chưa hẹp,
không phải "lĩnh vực nhiều bài".

---

## 6. Việc còn lại của `docs/12`

- Lô 1 (Cửa A) và Lô 3 (Cửa D+E) do 2 subagent khác — **parent ráp trang**, không subagent nào viết
  file tổng hợp.
- `00-cua-mo.md` **nên được bổ sung** dòng *"Giảm tải thải và tách heo đang thải khỏi nhóm"* cho
  `salmonella` ở chặng 8 (hiện chỉ có dòng giám sát + cách ly) — nếu không, lô sau lại phải khớp lỏng.
- Trước khi ráp trang: chạy `scripts/check-cut-lines.py` trên **từng** `batch-*.json`.
