# Lô A `10-cong-thuc-23` — 12 nguyên liệu theo khung 8 chặng

Trạng thái 20/10/2026: **ĐỦ 12/12 file nguồn `src/*.txt`, `python _build.py src a` chạy SẠCH**
(`ingredients=12  unique_pmids=110`, exit 0) — 5 chất đầu (19/10) + berberine/hoàng liên/ích mẫu + tannin
chestnut/quebracho + **huyết dụ + lá hẹ, chốt 20/10** (`src/huyet-du.txt` 56 dòng / 24 dòng bảng;
`src/la-he.txt` 61 dòng / 29 dòng bảng — cả hai: đủ 24 khoá bắt buộc, đủ 8 khối chặng, mọi dòng bảng đúng 6 cột).
`batch-a.md`/`batch-a.json` do parent chạy builder sinh — subagent KHÔNG tự viết.
Bank 2 nguyên liệu cuối ở §"Hai nguyên liệu cuối lô A" bên dưới.

## Trạng thái từng chất

| # | Chất | File nguồn | Trạng thái |
|---|---|---|---|
| 1 | Thymol | `src/thymol.txt` | ✅ 14,6 KB — 8/8 chặng |
| 2 | Carvacrol | `src/carvacrol.txt` | ✅ 12,5 KB — 8/8 chặng |
| 3 | Eucalyptol (1,8-cineole) | `src/eucalyptol.txt` | ✅ 13,5 KB — 8/8 chặng |
| 4 | Propolis | `src/propolis.txt` | ✅ 14,5 KB — 8/8 chặng |
| 5 | Glycyrrhizin | `src/glycyrrhizin.txt` | ✅ 17,1 KB — 8/8 chặng |
| 6 | Berberine | — | ❌ chưa viết |
| 7 | Hoàng liên (dược liệu thô — phải ghi RÕ khác Berberine HCl) | — | ❌ |
| 8 | Tannin Chestnut | — | ❌ |
| 9 | Tannin Quebracho | — | ❌ |
| 10 | Ích mẫu (*Leonurus japonicus*) | — | ❌ |
| 11 | Huyết dụ (*Cordyline terminalis*) | `src/huyet-du.txt` | ✅ 56 dòng / 24 dòng bảng — 8/8 chặng, 21 PMID |
| 12 | Dịch chiết lá hẹ (*Allium tuberosum*) | `src/la-he.txt` | ✅ 61 dòng / 29 dòng bảng — 8/8 chặng, 22 PMID |

## Bộ khung đã dựng trong thư mục (chưa chạy đầu-cuối)

`_epmc.py` (search + fetch abstract, có cache) · `_verify.py` (verify PMID theo `EXT_ID`) ·
`_build.py` (đọc `src/*.txt` → sinh `.md` + `.json`) · `_pmids.txt` (73 PMID).

**`_build.py` lint OK nhưng CHƯA CHẠY LẦN NÀO** → đó là lý do 0 byte. Xem
`pubmed-evidence-research/references/multi-item-deliverable-source-builder.md`.

File rác cần xoá: `_data_a.py` (51 KB, bị cắt), `_data_b.py` (260 byte, lint SyntaxError) — hai nỗ lực
"một write khổng lồ chứa cả lô" đều thất bại.

## Nguồn đã verify — điểm chốt của 5 chất đầu

### Thymol
- **Cửa vào = DẠ DÀY, không phải ruột** (ở heo): `24548668` — thymol 50 mg/kg thể trọng vào dạ dày heo,
  niêm mạc dạ dày là nơi hấp thu chủ yếu; gene set DIGESTION hạng 1 (môn vị) / 9 (oxyntic);
  **SLC15A1 (PEPT1) TĂNG** — bằng chứng gián tiếp duy nhất cho họ SLC.
- Người: `12092740` — **không phát hiện thymol TỰ DO** trong huyết tương/nước tiểu, chỉ có thymol sulfate;
  Cmax 93,1 ± 24,5 ng/mL; Tmax 2,0 ± 0,8 h; **t½ 10,2 h**; **16,2 ± 4,5 % liều ra nước tiểu 24 h**.
- Thỏ: `34573560` (thành ruột > huyết tương, rs = −1,000; phân > kết tràng p < 0,01) ·
  `41301947` (tích tụ ở **thận** p = 0,0182 và **mô mỡ** p = 0,0003; sau ngừng 7 ngày dưới LOQ ở huyết tương/lách/cơ).
- Heo in-vivo: `25049525` (96 heo cai sữa, E. coli ↓ manh/kết/trực tràng) · `42000567` (120 heo con,
  200/400/800 mg/kg + acid hữu cơ) · `33499989` (nái, giảm tử vong heo con).
- Trần độc: `42005330` — thymol > 1000 mg/kg, carvacrol > 2480 mg/kg.
- **tag H**: CYP pha I; bơm ABC; cửa sữa heo nái; t½ ở heo; protein chở trong máu.

### Carvacrol
- `32874282` — EFSA (Nimicoat) cho **heo cai sữa**: 250–1000 mg/kg feed = **100–400 mg carvacrol/kg**;
  tích luỹ sinh học thấp. **Suy ra cho premix 5 kg/tấn: ≤ 80 g carvacrol/kg premix.**
- `38799727` — chỉ **dạng vi nang (MEO)** mới hiệu quả, tinh dầu thường thì không; **KHÔNG đổi gene kháng
  tetracycline (p > 0,05)** → dùng làm `da_that_bai`/`bat_kha`.
- `41497464` — nái: 88,5 % vs 82,6 % heo con bán được.
- **tag H gần như toàn bộ chặng 3/4/6/7/8** — không có PK định lượng cho carvacrol trên heo.
- **BẪY ĐÃ LOẠI**: nguồn "carvacrol ức chế P-gp" chỉ có trên **MCF-7 (ung thư vú người)** → loại theo
  quy tắc audit mô, KHÔNG dùng cho ruột/gan.

### Eucalyptol (1,8-cineole)
- Người: `20425757` — pha I tạo 4 hydroxycineole (2-, 3-, 9-, 7-); Cmax **86** nmol/L (2-OH) vs **19** nmol/L
  (chất mẹ) → chuyển hoá rất mạnh; thải niệu 10 h: **20,9 / 17,2 / 10,6 / 3,8 %** liều.
- **Cửa MŨI/PHỔI có thật**: `23983963` — chỉ HÍT aroma hương thảo đã đo được cineole trong huyết thanh người
  ⇒ **cineole bay hơi mạnh, nguy cơ thất thoát khỏi premix bột + ô nhiễm chéo lô trộn**.
- **Cửa SỮA**: `24957890` — α2-hydroxy-1,8-cineole trong sữa mẹ **100–250 µg/kg** (người, KHÔNG phải heo).
- `36987546` = mô **NÃO chuột** + làm mở hàng rào **MÁU-NÃO** → chỉ dùng cho phát biểu về não, không mượn cho ruột.
- **tag H**: t½ (không có), cửa phổi/da, cửa mật→phân, mô đích ở heo, thụ thể (nguồn TRPM8/TRPA1 chưa mở abstract).

### Propolis
- Người: `42598803` — **63 chất chuyển hoá trong huyết tương / 85 trong nước tiểu**; Cmax 1,22 ± 0,20 µM
  (400 mg) và 4,80 ± 0,48 µM (1600 mg); Tmax **1 h**; thải niệu **< 3 h**;
  **net bioavailability 57,16 % → 43,82 % khi tăng 4× liều** (tăng liều KHÔNG tăng tỷ lệ hấp thu).
- `34449320` — chrysin bị **UGT/SULT** chuyển hoá ngay (KHÔNG phải CYP); BCRP/MRP2 đẩy ra;
  nhưng **tái tuần hoàn gan-ruột ⇒ nồng độ CAO ở hồi tràng/kết tràng** ⇒ mô đích.
- `25715997` — Ko143 ức chế BCRP giảm đẩy chrysin sulfate (Caco-2 + chuột nhắt Bcrp1−/−).
- `19732493` — **chrysin VỪA là cơ chất VỪA là CHẤT ỨC CHẾ BCRP** (chuột cống: nitrofurantoin ↑; chuột nhắt: không)
  ⇒ dùng làm ví dụ chuẩn cho khác biệt "bị bơm thải" vs "ức chế bơm".
- `27378517` — PCBG → aglycone pinocembrin trong hệ tiêu hoá; PCB/PCBG = 4× khi uống.
- `40732257` — **tương tác có nguồn**: propolis + enrofloxacin ở thỏ → AUC 26,11 → **48,91** µg·h/mL;
  t½ kháng sinh 5,93 → **11,75 h**. ⚠️ Đó là t½ của KHÁNG SINH, không phải của propolis.

### Glycyrrhizin
- **KHÔNG hấp thu được dạng nguyên vẹn** — `7742809` BA uống **~1 %** vs phúc mạc 65–90 %, mũi ~20 %;
  `14522122` AUC tĩnh mạch **cửa < ngoại vi** ⇒ first-pass gan có thật.
- Bắt buộc qua **VI SINH RUỘT**: `11145169` (chuyển **55–100 %** thành GA; tiếp đó 3-oxo-GA,
  3α-hydroxy-GA qua 3β-HSD) · `10836746` (Eubacterium sp. L-8 chủng chính; β-glucuronidase **2,7–6,8×**
  ở kết tràng viêm loét). Cả hai là **in-vitro vi sinh NGƯỜI** ⇒ ghi rõ loài.
- `31083444` — chuột cống: **t½ 23,1 ± 15,5 h** (dài nhất trong 4 marker) ⇒ **nguy cơ tích luỹ**.
- `29908072` — OATP1B1/1B3 (vào gan) + **MRP2/BCRP/BSEP/MDR1 đẩy ra mật**; gắn **albumin** mạnh;
  **rifampin ức chế OATP → TĂNG phơi nhiễm hệ thống** (can thiệp bước VÀO ngược chiều bước RA).
- `33481180` — khi MRP2 suy giảm: **3MGA tràn vào MÁU → thải NƯỚC TIỂU qua OAT1/OAT3**.
- `34604277` — 18β-glycyrrhetyl-3-O-sulfate là chất chuyển hoá chính ở người; **ức chế 11β-HSD2** (tác dụng
  phụ giả aldosterone — KHÔNG được claim như lợi ích).
- `35088789` — **mở tight junction** qua gắn vùng PDZ1 của ZO-1 (**Caco-2, biểu mô RUỘT người in-vitro**)
  ⇒ suy luận có thể làm TĂNG hấp thu mọi thành phần khác trong premix (tag H cho heo).

## Bẫy tương tác nội công thức đã ghi được

1. **Glycyrrhizin mở tight junction ruột** (`35088789`) ⇒ cộng hưởng hấp thu với thymol/carvacrol/
   eucalyptol/berberine (berberine BA chỉ 0,36 % nên đây là điểm đáng thử). Tag H cho heo.
2. **Vi sinh ruột là mắt xích sống còn của cam thảo**: nếu thymol/carvacrol/tannin diệt khuẩn mạnh thì
   chuyển glycyrrhizin → GA giảm ⇒ mất hiệu lực. Cơ chế vi sinh có nguồn (`11145169`), cặp trực tiếp tag H.
3. **Propolis ức chế chuyển hoá/thải thuốc khác** (`40732257`, thỏ) + ức chế BCRP ruột (`19732493`).
4. **Tannin kết tủa protein/enzyme** làm giảm tiêu hoá chất khô (`33105748`, `28004617`) ⇒ nguy cơ giảm hấp thu
   chung; đo trực tiếp trên heo tag H.
5. **Vi hạt/vi nang là điều kiện, không phải tuỳ chọn**: thymol vi hạt alginate nhả **73,7 %** ở dạ dày mô phỏng
   (`30141924`); carvacrol dạng MEO mới có hiệu quả còn EO thường thì không (`38799727`).
6. **Eucalyptol bay hơi** ⇒ thất thoát + ô nhiễm chéo lô trộn (`23983963`).

## Luật vận hành rút ra (đã ghi vào pitfall 23 của SKILL.md)

1. Chia lô **≤ 5–6 nguyên liệu / subagent** — 12 chất là vượt ngân sách tool-call.
2. **Chạy bộ dựng sau CHẤT THỨ NHẤT**, không phải sau chất cuối.
3. Nguồn dữ liệu = **một file nhỏ / một chất** (`src/<slug>.txt`, 12–17 KB), bộ dựng sinh CẢ `.md` và `.json`.
   Write ~51 KB bị cắt còn 260 byte; write ~12–17 KB qua sạch.

## Hai nguyên liệu cuối lô A (20/10/2026) — bank + bẫy

Cả hai **KHÔNG hấp thu hệ thống** ⇒ đích = **niêm mạc ruột / vi sinh ruột**; phần lớn chặng 3/4/6/7/8 là `tag H`.
Bằng chứng đã đọc abstract thật (35 PMID re-fetch trong lượt viết, thoả luật "không viết từ bản compaction"):
`git`-less verify qua Europe PMC `EXT_ID`, đối chiếu từng số trong bảng với `abstractText`.

### Huyết dụ — *Cordyline fruticosa* / *C. terminalis*, LÁ (dược liệu thô) — 21 PMID, MUC = **R**
- Hoá thực vật: `38136652` (98 hợp chất / 8 loài / 26 loài được chấp nhận; chất chính = **flavonoid + glycosid
  spirostan/furostan/cholestan** = saponin steroid) · `34624728` (giống VN "Fairchild red": **14 glycosid, 12 mới —
  10 từ RỄ, 4 từ phần trên mặt đất** ⇒ cảnh báo **lẫn bộ phận thu hái là đổi hoạt chất**) · `40901441` (70 % MeOH:
  **MIC 6,25 % *S. mutans* / 1,56 % *C. albicans***, 17 chất GC-MS, có saponin+flavonoid+triterpenoid+alkaloid) ·
  `22293491` (4 cholestan glycosid mới từ lá) · `31596585` (**LOÀI KHÁC** *C. manners-suttoniae*, mô **QUẢ**:
  suttonigenin F MIC75 ≈ chloramphenicol) · `9429320` (**LOÀI KHÁC** *C. stricta*, LÁ: spirostanol+furostanol,
  nhánh triglycosid gắn C-1) · `40685791` (**LOÀI KHÁC** *C. australis*: an toàn trên BJ-1 người — 0,6–8,5 % độc tính
  ở 100 µg/mL; vitexin rhamnosid IC50 **43,7 µg/mL** trên HOS) · `42666415` (414 đích chung, **in-silico**).
- Cửa vào = **miệng/ruột**: `35292376` (*C. fruticosa* = 1 trong **3 loài được nhắc nhiều nhất trị tiêu chảy**;
  133 người / 34 chuyên gia / 6 đảo French Polynesia) · `12628508` (LÁ + HẠT *C. terminalis* được ăn, người Maori) ·
  `38136652` (y văn cổ: ho ra máu, kiết lỵ, sốt cao). Mũi/phổi, da, tiêm, và **first-pass = tag H**.
- An toàn (chỉ in-vitro): `34445465` — aqCT trong gel: **DPPH 100 %**, sống tế bào **>85 %**, nhả polyphenol
  **110–350 nmol/mL** giờ đầu.
- Tham chiếu NHÓM HỢP CHẤT (KHÔNG phải Cordyline — phải ghi rõ): `41484883` (β-glucosidase EfD08 của *E. faecalis*
  D1 phân lập từ ruột **chuột cống**: trillin→diosgenin, cắt cả dioscin/deltonin/ginsenosid Rb1-Rc) ·
  `42124012` (anthocyanin → phenolic ở đại tràng, nồng độ huyết tương **×100** so chất gốc).
- **9 nguồn BỊ LOẠI** (đã ghi trong `DA_THAT_BAI`): 25415453 (bài thuốc **hỗn hợp** cổ Thái, không nêu Cordyline) ·
  33066411 (abstract chỉ có *Ageratum conyzoides* + *Ixora coccinea* — **đọc abstract mới dám kết luận**) ·
  35745988 (kháng khuẩn của **hạt nano bạc**, không phải của dịch chiết) · 28213142 / 25483560 / 33769150
  (pigment cho pin DSSC + nhuộm vải) · 30002597 / 40524191 (danh lục dân tộc dược học) · 1231125 (abstract TRỐNG).
- **KHÔNG tồn tại nghiên cứu Cordyline nào trên HEO.**

### Dịch chiết lá hẹ — *Allium tuberosum* — 22 PMID, MUC = **A** (nhưng trên chuột + gà thịt, KHÔNG phải heo)
- **Bằng chứng quyết định về cửa vào:** `11719943` — cùng dịch chiết, **uống ↓40 % di căn phổi B16-F10 (p<0,03)**,
  còn **tiêm IV KHÔNG hiệu quả** ⇒ tác dụng gắn với ĐƯỜNG TIÊU HOÁ, không phải nồng độ trong máu. Dùng câu này cho
  cả `CUA_VAO` (cửa = miệng/ruột) và `BAT_KHA` (không có bằng chứng tác dụng toàn thân).
- Cửa vào khác: `33308987` (ống thông dạ dày 27 ngày, chuột BALB/c hen) · `36290128` (3 % nước ép trộn cám/nước uống,
  800 gà Ross 308).
- Hoá học/độ bền: `20225897` (DART-MS — lá nghiền → thiosulfinate + thial S-oxide; **disulfane/polysulfane CHỈ xuất
  hiện khi ĐUN NÓNG**; sulfenic acid **t½ <1 giây**) · `23647469` (tinh dầu: allyl trisulfide **40,05 %**, MIC 250 ppm
  nhưng chỉ kháng **NẤM** *Aspergillus*) · `28216165` (40 hợp chất, 8 mới; **dịch chiết lá TƯƠI độc tế bào gan IAR20 /
  thận NRK chuột cống, mẫu HẤP thì an toàn** ⇒ premix phải dùng dạng đã xử lý nhiệt) · `25279760` (thiol/allicin/
  flavonoid/polyphenol, DPPH/FRAP — công nghệ lên men, không phải in-vivo).
- Đích ruột (mạnh nhất): `38953279` (nanovesicle từ hẹ, chuột DSS-colitis: ↓IL-1β/IL-6/TNF-α/NF-κB/SAA, **↑ZO-1 +
  occludin**, ↑IL-10, ↓tỷ lệ Firmicutes/Bacteroidetes, ↓Proteobacteria, ↑*Lactobacillus*, ↑acetic acid) ·
  `33308987` (Ruminococcaceae + Desulfovibrionaceae = biomarker; ILC giảm ở cả ruột và phổi) · `36290128`
  (↓vi khuẩn gây bệnh đường ruột **p<0,01**, ruột nặng hơn p<0,05, nhung mao/crypt **không đổi**).
- Kháng khuẩn tại chỗ: `11388483` (2 thiosulfinate tách từ lá vs *E. coli* O157:H7) · `41971187` (CCE **≥3 %** ức chế
  hoàn toàn, cả 10 °C và 35 °C) · `25836597` (**mô RỄ**: tuberoside O / shatavarin IV — MIC 16 µg/mL *E. coli*,
  32 µg/mL *B. subtilis*).
- PK của hẹ = **tag H toàn bộ**. Tham chiếu LOÀI KHÁC (tỏi *A. sativum*, luôn ghi rõ loài): `26764325`
  (SAC **F 98 %**, độ thanh thải thận 0,016 L/h/kg, 24 h: **2,9 % SAC + 80 % NAc-SAC + 11 % NAc-SACS**) ·
  `40171136` (F 88,0–95,8 % cho SAC/S1PC/SMC; SMC ~50 % thành lưu huỳnh vô cơ) · `29694836` (DAS ức chế CYP2E1) ·
  `42731716` (DAS → microbiota–tryptophan–AhR/IL-22/STAT3, chuột).
- Trên HEO chỉ có: `33800152` (chiết xuất Allium **loài KHÔNG XÁC ĐỊNH** — alpha diversity ↓ manh/kết tràng, nhưng
  BW/ADG/FCR tốt hơn đối chứng) · `41039193` (tỏi, heo 20 kg, 3 % w/w + apple pomace/blackcurrant: ↑Weissella/
  Catenibacterium/Holdemanella/Faecalibacterium, ↑butyrate, ↑SOD/GPx niêm mạc ruột non, ↓acid lactic/cadaverine,
  **KHÔNG đổi *E. coli*/*Lactobacillus***).
- Hạn chế dùng / loại: 25470273 (số liệu **gộp 6 loài** họ Alliaceae) · 23647469 (chỉ kháng nấm) · 35170391
  (tổng quan 6 loài, không tách số *A. tuberosum*) · 1231125 + 12628508 (không liên quan tới hẹ).

### Luật viết rút ra cho nguyên liệu THÔ không có PK (tái dùng cho lô sau)
1. Huyết dụ/hoàng liên/ích mẫu/tannin **không có PK** ⇒ mỗi chặng không nguồn ghi **đúng một dòng**
   `CHƯA CÓ NGUỒN (tag H)` — không được bỏ dòng, không được nâng thành suy luận.
2. Vẫn được thêm **dòng "tham chiếu LOÀI KHÁC"** để giữ cơ chế — nhưng **loài + mô của nguồn phải nằm ngay trong
   cột "mô & loài" VÀ trong ô mức bằng chứng** (`(R) in-vitro — LOÀI KHÁC: *C. stricta*, LÁ`). Không có nhãn đó thì
   dòng tham chiếu bị đọc thành số của nguyên liệu đang viết.
3. Với nguyên liệu thô, **`MUC` phải khai báo theo cấp cao nhất THẬT của chính loài đó** (huyết dụ = R; hẹ = A nhờ
   chuột + gà thịt) và **phải nói rõ chưa có cấp A trên HEO** — đừng để lô "có in-vivo" nghe như "có trên heo".
4. Cả hai file đều cần thêm cột nội dung **"dạng dùng"**: lá tươi vs đã đun nóng (hẹ) và **lẫn rễ/thân vào lá**
   (huyết dụ) là hai rủi ro thật của nguyên liệu thô, có nguồn, phải nằm trong `DANG_DUNG`.
5. Duyệt cuối: `python _build.py src a` → `ingredients=12  unique_pmids=110`, exit 0; tự kiểm thêm bằng script
   (đủ 24 khoá bắt buộc, 8 khối chặng, **mọi dòng bảng đúng 6 cột**) vì builder **không** kiểm số khoá hay số cột.
