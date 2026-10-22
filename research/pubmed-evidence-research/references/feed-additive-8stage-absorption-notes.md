# Lô nguyên liệu premix heo — ngân hàng bằng chứng theo khung 8 chặng

Nguồn: fixgby `D:/Hermes Proj/fixgby/docs/10-cong-thuc-23/batch-c.{md,json}` (19/10/2026), 7 nguyên liệu
premix trộn cám heo (2 kg/lô · 5 kg/tấn cám ⇒ 400 kg cám/lô), nhóm TĂBS — **cấm claim trị bệnh**.
**verified 61/61 PMID** (mỗi PMID mở `resultType=core`, đọc `title` + `abstractText` thật).

Ba khối dưới đây là phần **tái dùng được** (không phải toàn văn tài liệu): kỹ thuật tăng hấp thu,
khoáng hữu cơ vs vô cơ, và các con số chặng 7/8 (thải qua sữa, tồn lưu, độc).

---

## A. Kỹ thuật TĂNG HẤP THU (curcumin nano · vitamin E TPGS)

**Luật chung tìm được:** chất "tăng hấp thu" trong cùng một công thức thường tác động qua **bơm đẩy
(ABC)** — chặng 6 và chặng 2 ăn vào nhau. Đây là chỗ dễ nói sai nhất: phần lớn tài liệu mô tả
curcumin/TPGS *bị* P-gp thải, nhưng bằng chứng in-vitro/in-situ lại cho thấy chúng **ỨC CHẾ** P-gp.
Nếu không phân biệt được hai chiều này thì chặng 2 và chặng 6 sẽ tự mâu thuẫn.

| Chất | Số liệu chặng 2 (hấp thu) | PMID |
|---|---|---|
| Curcumin nano | hạt 264 nm, entrapment 76,9 %, sinh khả dụng uống **≥ 9 lần** so với curcumin+piperine | 19491009 |
| Curcumin nano-liposome | người: **AUC0-t ×23,2**, **Cmax ×53** (chuẩn liều) so với curcumin tự do | 42225688 |
| Curcumin (gốc) | chuột 500 mg/kg uống: Cmax **0,06 ± 0,01 µg/mL**, Tmax 41,7 ± 5,4 phút → nồng độ cực thấp | 17400527 |
| Curcumin + piperine | sinh khả dụng tăng **154 %** ở chuột/người — *không giải quyết được vấn đề gốc*: 2 g ở người cho nồng độ huyết tương "không đo được hoặc rất thấp" | 9619120 |
| Curcumin | ức chế **P-gp/ABCB1**; demethoxycurcumin ức chế ATPase P-gp người **IC50 = 1,56 ± 0,13 µM**, không đổi mức biểu hiện | 25594233 |
| Curcumin | in-situ ruột kết **chuột**: tăng độ thấm irinotecan qua ức chế P-gp | 24511364 |
| Curcumin | ức chế **UGT2B17 IC50 58 µM** (microsome ruột NGƯỜI) ⇒ có thể làm tăng nồng độ chất khác cùng premix nếu là cơ chất UGT2B17 | 40911949 |
| TPGS | EFSA: monoester > 82 % w/w, diester < 20 % w/w, **"poorly absorbed"** — TPGS **không** tăng α-tocopherol tự do | 40791650 |
| TPGS | chiều dài chuỗi PEG quyết định mức tác động lên bơm ra (**Caco-2**, TPGS 200→6000) | 16410030 |
| TPGS | ức chế P-gp màng đỉnh **Caco-2** | 17367162; 20205474 |

**Con số chặng 8 của vitamin E (đáng nhớ, dùng cho `o_lai`):** mô mỡ **1,53 µmol/g (657 µg/g)**;
tổng kho toàn cơ thể **25 900 ± 6 220 µmol (11 ± 3 g)**; t½ ngăn mô mỡ **184 ± 48 ngày**, thời gian lưu
**499 ± 702 ngày** (người, đồng vị 14C); sinh khả dụng RRR-α-tocopherol **81 ± 1 %**. Meta-analysis
trên **heo nái**: tăng α-tocopherol huyết thanh nái + heo con nhưng **KHÔNG tăng vitamin E trong sữa đầu**.
→ 23077194 · 41036371.

**Tương tác phải ghi trong `tuong_tac`:** TPGS ức chế P-gp ⇒ tăng hấp thu curcumin (17367162, 20205474);
nhưng cùng lúc curcumin cũng ức chế P-gp và UGT2B17 ⇒ tác động hai chiều lên các chất khác cùng premix.
Tương tác "TPGS ↔ α-tocopherol" **chưa có nguồn** đủ để khẳng định tăng hấp thu ⇒ tag H, đừng suy.

---

## B. Se hữu cơ vs Se vô cơ (điểm sống còn của lô)

**Khác biệt cốt lõi:** men giàu selen cung cấp **selenomethionine (SeMet) + selenocysteine (SeCys)**
(42572100, 41975998); Na-selenite là vô cơ. Khác biệt không nằm ở "hấp thu nhiều hơn" mà ở **tồn lưu mô**
và **cửa thải**.

| Phát biểu | Số / chi tiết | Loài | PMID |
|---|---|---|---|
| Se mô cao hơn ở dạng hữu cơ | HEO Tây Tạng (41,96 ± 6,91 kg, 72 con, 60 ngày), cùng **0,5 mg Se/kg**: Se ở thận, gan, tim, longissimus dorsi **cao hơn** ở nhóm men Se (SeY) so với selenite/SeSP/nano-Se (p < 0,05) | HEO | 42793988 |
| Se máu heo đực | 0,3 mg/kg: **107,5 ± 4,8** (hữu cơ) vs **114,7 ± 4,8** (selenite) vs **28,4 ± 4,8 µg/L** (đối chứng) | LỢN ĐỰC | 21948612 |
| **THẢI QUA SỮA (cửa sống còn của heo nái)** | 12 nái L×Y, 0,3 mg Se/kg, 60 ngày: Se trong **sữa đầu và sữa** cao hơn rõ ở nhóm **selenomethionine** so với Na-selenite (p < 0,05), kèm tăng khối lượng heo con từ sinh → cai sữa | HEO NÁI | 20717850 |
| Nái mang thai sớm + men Se | tăng số con/lứa (p < 0,05), tăng progesterone, tăng GPx/SOD/catalase, giảm MDA | HEO NÁI | 20740325; 42439553 |
| Cửa thải qua TRỨNG (minh hoạ, *không phải heo*) | gà Hy-Line Brown, liều 0–0,5 mg/kg: Se lòng đỏ **0,211 → 0,521 mg/kg** (p < 0,001) | GÀ (không phải heo) | 42651912 |
| Selenoprotein P (SEPP1) là điểm chững | EFSA dùng điểm SEPP1 chững lại để tính AI: **70 µg/ngày** người lớn; phụ nữ cho con bú **+15 µg/ngày** để bù lượng Se tiết vào sữa mẹ | NGƯỜI | 42087966 |

**Ngưỡng an toàn / độc (chặng 8 — phần quan trọng nhất):**
- NRC: **0,15 mg Se/kg cám** (nái, heo vỗ béo) · **0,30 mg/kg** (heo con tập ăn); EU giới hạn trên
  **0,5 mg Se/kg cám** (88 % DM).
- Sự cố **Na-uy 6/2023**: cám nhiễm **2,47–4,70 mg Se/kg** từ **Na-SELENITE**; theo dõi **516 nái / 895 lứa**
  → **KHÔNG** thấy selenosis lâm sàng, **không** ảnh hưởng sinh sản (p > 0,05). (42158037)
- Người nuốt **40,146 mg Se** → nhiễm độc đa cơ quan: bệnh não độc, mất thị lực/thính lực, rối loạn gan,
  rụng tóc. (42620727)
- Dải thiếu–độc **hẹp** ⇒ `tich_luy` của Se luôn là "CÓ", kèm ngưỡng. Không có t½ ở heo ⇒ tag H.

**Cảnh báo mô/loài:** PMID 42651912 (trứng) và 41514835 (ngỗng) chỉ dùng minh hoạ **cửa thải**, không suy
cho heo. Tên protein vận chuyển SeMet/selenite ở ruột heo **không có nguồn** ⇒ tag H (đừng lấy tên từ
bài về loài khác).

---

## C. MgO vs Mg chelate — bằng chứng ÂM TÍNH là kết luận đúng

Câu hỏi "chelate có hấp thu tốt hơn oxide không" — **nguồn đã đọc trả lời KHÔNG rõ ràng, và đó chính là
câu trả lời phải viết ra**, không phải chọn nguồn ủng hộ chelate.

| Phát biểu | Số / chi tiết | Loài | PMID |
|---|---|---|---|
| In-vivo: không tách được lợi thế | CHUỘT (60 ngày tuổi, 50 mg/kg/ngày Mg nguyên tố, 30 ngày gavage): Mg đa dạng vs Mg **oxide / citrate / glycinate** cho hiệu quả **so sánh được** trên chỉ số hệ thống, hành vi, phân tử, mô học gan–thận | CHUỘT | 42589240 |
| In-vitro: khác biệt phụ thuộc thức ăn | **Caco-2**: có thức ăn → Aquamin-Mg > bisglycinate 2 (p = 0,016); **không** thức ăn → **KHÔNG** khác biệt giữa các nguồn; TRPM6 giảm ở nhóm Aquamin (p < 0,001) | Caco-2 (ruột NGƯỜI) | 41599937 |
| Công thức quan trọng hơn loại muối | hai sản phẩm **bisglycinate cùng hàm lượng Mg**: Mg dialyzable **53 vs 39 mg** (p = 0,0009) — chênh **17 %** tổng lượng Mg khả dụng | mô phỏng tiêu hoá NGƯỜI (SHIME) | 42709016 |
| Thu hồi Mg thấp nhất | mô phỏng tiêu hoá INFOGEST + Caco-2: **MgO thu hồi Mg thấp nhất** trong 3 nguồn (MgO, Aquamin, MgCl2) | người/Caco-2 | 30018220; 29630135 |
| **Bằng chứng âm tính trên HEO (dùng cho `da_that_bai`)** | HEO SAU CAI SỮA 381 con (2 lô, Đan Mạch): Mg máu **GIẢM ở TẤT CẢ nhóm** sau 3 tuần (tuần 7 của đời heo), kèm tăng tổn thương đuôi — **rõ nhất ở nhóm bổ sung MgO** ⇒ bổ sung MgO KHÔNG giữ được Mg máu | HEO | 42277947 |
| Nái: Mg huyết thanh + miễn dịch | 120 nái Y×L (263,62 ± 3,60 kg), từ ngày 107 thai → cai sữa, 0,25/0,50/0,75 % kali-magie sulfat: Mg huyết thanh tăng, IgA/IgG/IL-10 tăng, giảm tiêu chảy (p < 0,05); **không có số Mg trong sữa** | HEO NÁI | 42339333 |
| Chốt giữ Mg = THẬN | CHUỘT: knockout **TRPM6 đặc hiệu ống lượn xa** giảm Mg2+ huyết tương ở khẩu phần 0,21 % và 0,08 % w/w; knockout **Kv1.1 ống thận thì KHÔNG** đổi Mg2+ | CHUỘT | 42572410 |
| Mg2+ chặn thụ thể NMDA | cryo-EM: Mg2+ giữ vỏ nước, bám **ngoài** bộ lọc chọn lọc → **chặn kênh** | cấu trúc tái tổ hợp (R) | 42086762 |

**Chặng 3 và 6 của Mg luôn là tag H** — Mg2+ là ion, KHÔNG bị CYP chuyển hoá, KHÔNG có bằng chứng bơm ABC.
Viết câu phủ định **tường minh** ("không có enzyme pha I — ion khoáng") thay vì bỏ trống ô.
Phần **glycine** giải phóng khỏi bisglycinate mới là chỗ có hoạt tính sinh học riêng (chất dẫn truyền ức chế);
tương tác glycine–NMDA **ở heo** chưa có nguồn ⇒ tag H.

---

## D. L-Tryptophan + Sodium ascorbyl phosphate — hai bẫy loài/mô đã chặn

**L-Tryptophan (heo):**
- Cửa vào + vi sinh: vi sinh ruột chuyển tryptophan dư thành **IPA (indole-3-propionic acid)** và
  **ILA (indole-3-lactic acid)** — ligand của **AhR** và **PXR** (42221959; 42237168).
- **HEO CON sơ sinh** (mô hình α-lactalbumin giàu Trp, GC-MS + NMR trên huyết thanh, nước tiểu, gan, não):
  tryptophan tuần hoàn tăng, **serotonin thể vân (striatum)** tăng; sản phẩm nhánh kynurenine và indole
  **"were predominantly excreted in urine"**; hoạt tính con đường kynurenine ở **GAN THẤP HƠN**. → 40610456
  (đây là nguồn hiếm hoi định lượng chặng 7 trực tiếp trên HEO — dùng làm xương sống).
- **HEO CON cai sữa** (27 heo Bama miniature, 6,200 ± 0,242 kg, 21 ngày, Trp ×0,5 và ×1,5): giảm tỷ lệ
  tiêu chảy (p = 0,012), cải thiện hình thái ruột (p < 0,05), tái cấu trúc vi sinh (metagenomics) → 42237168.
- **Cạnh tranh tại hệ L (LAT):** BCAA+Phe+Met hoặc BCAA+BCH ức chế cạnh tranh việc đưa tryptophan vào não
  → giảm mệt mỏi trung ương (người: hiệu quả **50 % vs 38 %** của BCAA đơn) → 42220619.
- **BẪY MÔ đã gặp:** nguồn **SLC7A5 (LAT1)** là về **HÀNG RÀO MÁU-NÃO**, KHÔNG phải hàng rào ruột. Ở ruột
  heo tên bơm cụ thể **không có nguồn** ⇒ tag H (41067390). Đây đúng là lỗi lớp 2 mà skill này cảnh báo.

**Sodium ascorbyl phosphate (dạng vitamin C ổn định):**
- **EFSA đã cấp phép** sodium ascorbyl phosphate (**3a311**) làm nguồn vitamin C cho **MỌI loài vật nuôi**;
  không gây kích ứng da/mắt, không gây dị ứng da. → 41158677 (nguồn chuẩn cho `dang_dung`).
- Bơm hấp thu: **SVCT1 (SLC23A1)** lo hấp thu ở **RUỘT**, **SVCT2 (SLC23A2)** ở mô. Người (257 người
  20–39 tuổi): biến thể **SLC23A1 rs6596473** liên quan tình trạng vitamin C huyết thanh → 42066640.
- **NGỖNG** (Yangzhou, 450 con cái, 16 tuần, 0–400 mg/kg): tăng SVCT1/SVCT2 ở ruột và buồng trứng, **ức chế
  GLO (L-gulonolactone oxidase)** ở gan/thận, tăng vitamin C huyết thanh và **lòng đỏ trứng** → 41514835.
  **Ghi rõ trong tài liệu: đây là NGỖNG, không phải heo.**
- **BẪY LOÀI đã chặn:** PMID **38683367** là về **LINH TRƯỞNG** và có nêu *"Brazilian guinea pig"* =
  **CHUỘT LANG (Cavia)**, KHÔNG phải heo (Sus scrofa). Heo có GULO hay không: **chưa có nguồn** ⇒ tag H.
  Trích nguồn này cho heo là lặp lại đúng lỗi gán loài mà skill này đã ghi nhận.
- Dược động (người): hấp thu **bão hoà mô**, **thanh thải thận nhanh**, t½ ngắn; liều cao chỉ tăng nhẹ
  nồng độ huyết tương và phải chia nhiều lần/ngày → 41304796.
- Tương tác có nguồn **trên HEO NÁI**: α-tocopherol-selenium + **acid ascorbic** giảm stress oxy hoá và
  cortisol, tăng IgG, giảm leptin ngày 7 sau đẻ (p < 0,05) — nhưng **KHÔNG** đổi khối lượng sơ sinh,
  khối lượng cai sữa, số con cai sữa → 31376718. Ascorbate tái sinh α-tocopherol: tag H (không có nguồn
  trong lô này).

---

## E. Quy trình đã dùng cho lô này (tái dùng)

1. Chia 7 chất thành **3 lượt `execute_code`** (2–3 chất/lượt), mỗi lượt ghi `_tmp_a/b/c.json` — thân code
   ngắn nên không bị cắt. **`execute_code` KHÔNG giữ state giữa các call** ⇒ biến `data` mất; phải persist
   ra file tạm rồi merge ở lượt cuối, rồi **xoá file tạm**.
2. Validate PMID: gọi `EXT_ID` **từng cái** — 50 call nhanh ⇒ **11 cái fail** (rate limit), retry với sleep
   ⇒ **đủ 61/61**. Chi tiết + luật đếm: xem pitfall trong SKILL.md.
3. Chạy `scripts/check_batch_schema.py <file.json>` trước khi ship (schema 20 khoá + `pmid` trong 8 chặng).
4. `python -c "import json;json.load(open(<file>,encoding='utf-8'))"` để chốt JSON hợp lệ.
5. Khối GIỚI HẠN cuối tài liệu phải nói rõ: `verified N/N` **chỉ chứng minh PMID tồn tại + title đúng**,
   KHÔNG chứng minh phát biểu khớp nguồn; kèm danh sách 4 bẫy mô/loài đã chặn (BBB≠ruột, linh trưởng/
   chuột lang≠heo, ngỗng≠heo, in-vitro≠in-vivo).
