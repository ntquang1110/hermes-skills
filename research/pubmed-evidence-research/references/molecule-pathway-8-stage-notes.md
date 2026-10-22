# Khung 8 chặng "đường đi phân tử" (fixgby `09-tra-cuu-duong-di`) — shape thứ ba + bank bằng chứng

Deliverable dạng này KHÁC row-JSON và Q&A-markdown: **mỗi CHẤT là một khối 8 mục a→h, mỗi dòng một
sự kiện, KHÔNG viết văn.** Dùng khi câu hỏi là *"chất này đi đường nào trong cơ thể"* chứ không phải
*"chất này có tác dụng gì"*.

## 8 khoá (đúng thứ tự, đúng tên — sai tên là phải làm lại)

| # | khoá | nội dung | cặp dễ lẫn |
|---|---|---|---|
| 1 | `cua_vao` | cửa vào trong **4 cửa**: mũi/phổi · miệng/ruột · da · tiêm + có qua gan lần đầu không (`first_pass`: `có`/`không`/`một phần`) | — |
| 2 | `qua_hang_rao` | bơm/họ vận chuyển đưa chất **VÀO** trong tế bào (họ **SLC**, OATP…) | **2 ≠ 6**: 2 = vào, 6 = ra |
| 3 | `gan_lan_dau` | enzyme **pha I** (họ **CYP** + enzyme khác) sửa chất thành gì | **3 ≠ 4**: 3 = CYP, 4 = UGT/SULT |
| 4 | `gan_de_di` | liên hợp **pha II** gắn nhóm gì **+** chất bám protein chở nào (albumin/lipoprotein/globulin) | — |
| 5 | `toi_mo` | tới mô/cơ quan nào, gõ vào **thụ thể** hay hệ nào | **thụ thể ≠ enzyme** (xem dưới) |
| 6 | `ra_khoi_te_bao` | bơm **ĐẨY RA** khỏi tế bào (họ **ABC**, MATE…) | — |
| 7 | `thai` | **5 cửa ra**: thận→nước tiểu · mật→phân · phổi→hơi thở · da→mồ hôi · sữa (ghi **%** nếu nguồn có) | — |
| 8 | `o_lai` | **t½** + **có tích luỹ không** | — |

**Luật "thụ thể ≠ enzyme":** đa số chất KHÔNG gõ GPCR. Statin đích là **enzyme HMG-CoA reductase**;
metformin đích là **complex I ty thể + AMPK**. Chỉ melatonin (MT1/MT2) và omega-3 (GPR120) mới có
GPCR thật trong lô C. Ô `thu_the` phải ghi thẳng "không qua GPCR — đích là enzyme X", **đừng bịa
thụ thể** cho chất không có.

## Schema JSON (khoá tiếng Anh, giá trị tiếng Việt **CÓ DẤU**)
`chat`, `ten_vi`, `cong_thuc`, `nhom`, `cua_vao{mo_ta,first_pass,pmid}`, `qua_hang_rao{phan_tu,chi_tiet,pmid}`,
`gan_lan_dau{enzyme,san_pham,chi_tiet,pmid}`, `gan_de_di{lien_hop,bam_protein,chi_tiet,pmid}`,
`toi_mo{mo_dich,thu_the,chi_tiet,pmid}`, `ra_khoi_te_bao{bom,chi_tiet,pmid}`, `thai{co_quan,ty_le,chi_tiet,pmid}`,
`o_lai{t_half,tich_luy,chi_tiet,pmid}`, `bat_kha`, `da_that_bai`, `chi_dau_do_duoc`, `muc_bang_chung`, `tag_H[]`, `pmids[]`.

File `batch-*.json` = **MẢNG** các object này (mỗi chất 1 object) — `json.load()` hợp lệ với mảng.
Khối markdown đi kèm: mỗi chặng một bảng, đúng cột
`| phát biểu | số/chi tiết | đường vào | mức bằng chứng | mô & loài | PMID |`.

Ba khoá "đời": `bat_kha` = chất **không** làm được gì; `da_that_bai` = **bằng chứng ÂM TÍNH thật**
(KO làm mất tác dụng, giả thuyết bị bác bỏ) — luôn điền, đừng để trống; `chi_dau_do_duoc` = chỉ số
đo được lặp lại trên **cùng một cá thể**.

## Bẫy vận hành đã dính thật (19/10/2026)

### 1. QC script glob CẢ THƯ MỤC ⇒ report là số TỔNG, không phải số của lô bạn
`qc-pmid-batch.py <dir>` quét **mọi** `batch-*.json` trong thư mục, không phải chỉ file vừa viết.
Ca thật: chạy trên `09-tra-cuu-duong-di` bắt luôn lô A/B (sat, canxi, curcumin, paracetamol,
ibuprofen) → `_qc-report.json` là số của **10 chất**, không phải 5 chất của lô C.
**Luật: con số `verified N/N` ký nhận phải chạy RIÊNG trên file của mình** — loop `unique(pmid)` đọc
từ chính file đó, fetch `EXT_ID:<pmid>` từng cái, đếm thật. Không trích `_qc-report.json` làm số của lô.

### 2. `·` (U+00B7 middle dot) là DẤU THẬP PHÂN, không phải dấu ngăn cách
Abstract của **Lancet** và nhiều nhà xuất bản in số thập phân bằng `·`: `3·5 mg` = **3.5**.
Tra số trong abstract **phải `replace("·", ".")` TRƯỚC khi grep**, nếu không sẽ tưởng "nguồn không có
con số đó" rồi đi tìm nguồn khác vô ích. Và **đừng mang `·` vào `value` của JSON** — người đọc sau
sẽ hiểu thành dấu ngăn cách.

### 3. `read_file` báo `is_binary:true` / 0 dòng trên file UTF-8 **HỢP LỆ**
Ca thật: `batch-c.md` 37.261 ký tự (tiếng Việt có dấu + `·` + `≥`) bị `read_file` trả
`is_binary: true, total_lines: 0, file_size: 43368`. File **không** hỏng — `bytes_written` đã đúng.
**Fix: verify bằng Python, đừng viết lại file vì tưởng nó hỏng:**
```python
t = open(p, encoding='utf-8').read()
print(len(t), len(re.findall(r'^#{1,3} ', t, re.M)))   # độ dài + số heading
```
Viết lại theo cảm giác "file hỏng" sẽ tốn công và dễ tạo bản kém hơn bản gốc.

### 4. Deliverable DÀI → ghi bằng `write_file` thẳng, đừng build trong `execute_code`
Lô C: build dict trong `execute_code` bị cắt thân code **4 lần** (vẫn trả về "1 lines output").
Ghi `batch-c.json` (25 KB) và `batch-c.md` (37 KB) **trực tiếp bằng `write_file`** thì qua ngay.
Với deliverable dài: `write_file` là đường chính, `execute_code` chỉ để fetch/validate.

## Bank bằng chứng 5 chất (19/10/2026 · 46 PMID · verified 46/46)

Chặng nào có nguồn, chặng nào **KHÔNG** — để lô sau biết ngay chỗ nào phải tag H:

| chất | chặng CÓ nguồn | chặng KHÔNG có nguồn (tag H thật) |
|---|---|---|
| atorvastatin | 1,2,3,4,5,6,7,8 | bơm đẩy cụ thể ở gan (MRP2/BCRP) · tích luỹ khi dùng liều lặp lại |
| metformin | 1,2,3(không có),4(không có),5,6,7,8 | tỷ lệ % thải theo từng cửa · tích luỹ khi chức năng thận bình thường |
| vitamin C | 1,2,3(không có),5,7,8 | enzyme liên hợp pha II · protein chở trong máu · bơm ABC đẩy ra · % theo từng cửa · **chặng 4 trống hoàn toàn** |
| omega-3 EPA/DHA | 1,2,3,4,5,8 | **chặng 6 (bơm đẩy) trống** · **chặng 7 (cửa thải + %) trống** · enzyme CYP cụ thể · liên hợp pha II · PPAR |
| melatonin | 1,3,4,5,7,8 | bơm SLC hấp thu (chặng 2) · bơm ABC đẩy ra (chặng 6) · bám protein chở · % theo từng cửa |

**Chặng 6 (bơm đẩy) là chặng TRỐNG NHIỀU NHẤT** — chỉ atorvastatin (P-gp) và metformin (MATE1/MATE2-K)
có nguồn thật. Đừng suy từ chất này sang chất khác; tag H.

### Nguồn dễ gán sai MÔ — audit lại từng cái trước khi dùng

| PMID | title thật | MÔ/LOÀI thật | gán được cho ⚠ |
|---|---|---|---|
| 24828044 | Mfsd2a is a transporter for DHA | chuột KO · **hàng rào MÁU-NÃO** | chặng 2/5 omega-3 — **KHÔNG** dùng cho hàng rào **RUỘT** |
| 40126401 | MFSD2A in Focus: the Molecular Mechanism of Omega-3 FA Transport | người/chuột · **máu-não** | như trên |
| 39382087 | … Regulating the Hypoxic Pathway in Cultured **Glioblastoma** Cells | tế bào **U NÃO nuôi cấy** | cơ chế SVCT2/HIF — **KHÔNG** dùng cho não in-vivo, ruột, gan, thận |
| 16150108 | Biotransformation of melatonin in human **breast cancer cell lines**: SULT1A1 | tế bào **UNG THƯ VÚ nuôi cấy** | chỉ dùng cho **TÊN ENZYME SULT1A1** — **KHÔNG** dùng cho mô gan |
| 40858268 | The curious family of cytochrome P450 4F fatty acid ω-hydroxylases | tổng quan · nói về **acid arachidonic** | **KHÔNG nêu EPA/DHA** ⇒ đánh tag H cho enzyme CYP của EPA/DHA, không gán bừa |
| 42805149 | A herb-drug interaction: transporters … atorvastatin absorption | **chuột + Caco-2** | efflux ratio 39,32 là **Caco-2**, không phải người in-vivo → chấm (A)+(R) |
| 10631088 | Human vitamin C (L-ascorbic acid) transporter SVCT1 | người · cRNA→oocyte **Xenopus** | chỉ dùng **định vị mô + K0,5** — abstract ghi **NHẦM ký hiệu gene** (SLC23A2 = SVCT1); không chép ký hiệu gene |
| 17568749 | Resolvin E1 and protectin D1 activate inflammation-resolution programmes | chuột (exudate) | chặng 3 omega-3 (COX/LOX) — title **không có chữ "omega"** nhưng abstract có "omega-3 PUFA-derived" ⇒ đọc abstract mới dám dùng |
| 19785645 | Impact of OATP transporters on pharmacokinetics | người · màng xoang tế bào gan | title generic — abstract có OATP1B1/1B3/2B1 + "many statins are substrates of OATP1B1" ⇒ **hợp lệ**, nhưng số c.521T>C 145 % là của 38493369 (atorvastatin GWAS), **không** của bài này |
| 42564851 | hepato-specific mechanisms of statins in MASLD | người (chủ yếu quan sát) | chặng 5 — chấm **hỗn hợp**, không phải RCT |

### Con số chặng 8 đáng nhớ (đã đọc abstract thật, không lấy từ snippet)
- **atorvastatin** t½ ≈ 7 h · F 14 % · Vd 381 L · thanh thải 625 mL/phút · bám protein 97,62 ± 1,96 % (suy thận 86,58 ± 2,04 %) · thận < 1 %
- **metformin** t½ ≈ 5 h (liều lặp lại) / 4,0–8,7 h (đơn) · F 55 ± 16 % · CLR 510 ± 130 mL/phút · **KHÔNG chất chuyển hoá nào**, KHÔNG bám protein
- **vitamin C** t½ **nghịch** với liều · pool tới ≈ 20 mg/kg · bạch cầu bão hoà ở 100 mg/ngày · thận bắt đầu thải ở liều ≥ 500 mg
- **omega-3** t½ tính bằng **NGÀY**: EPA 3,4 ± 2,7 · n-3 DPA 6,4 ± 5,3 · DHA 6,3 ± 8,9 (δ¹³C, n=12)
- **melatonin** t½ 53,7 ± 7,0 phút (uống) / 39,4 ± 3,6 (TM) · F **2,5 %** (1,7–4,7) · Vd 1,2 L/kg

**Chất duy nhất tích luỹ THẬT là omega-3** (t½ ngày, vào phospholipid màng tim/gan/não). Bốn chất
còn lại t½ giờ→phút; metformin chỉ "tích luỹ" khi suy thận (t½ tăng theo creatinin) — viết đúng
điều kiện, đừng viết "không tích luỹ" trống không.

## Bằng chứng ÂM TÍNH đã dùng cho `da_that_bai` (mẫu tốt, tái dùng được)
- metformin: "**không phát hiện chất chuyển hoá nào**" (8743335) giết giả thuyết "bị CYP phá huỷ";
  40098288 bác giả thuyết "OCT2 thận là cơ chế chính của tương tác cimetidin" (thật ra là OCT1 gan +
  ức chế MATE).
- vitamin C: 24400138 chứng minh SLC23A1 **và** SLC23A2 đều **KHÔNG** trung gian thải ascorbate ra ở
  tế bào ống thận gần → giết giả thuyết "một bơm đóng hai vai trò vào/ra".
- omega-3: GPR120-KO làm **MẤT hoàn toàn** tác dụng kháng viêm/tăng nhạy insulin (20813258) ⇒ GPR120
  là **bắt buộc**, không chỉ tương quan.
- melatonin: in-vitro chỉ 1 µM melatonin cho **< 1 %** 6-OHMelS so với dùng thẳng 6-OH-MEL (16150108)
  ⇒ giết giả thuyết "melatonin bị sulfat hoá ngay"; và aMT6s niệu **KHÔNG** tương quan với máu sau
  khi uống (r = 0,02) ⇒ không dùng aMT6s làm chỉ dấu SAU KHI UỐNG (10690873).

---

## LÔ B — bank 5 chất (19/10/2026 · **71 PMID · verified 71/71**)

`sắt (Fe) · canxi (Ca) · curcumin · paracetamol (APAP) · ibuprofen` — file `batch-b.json` / `batch-b.md`.
Cùng thư mục với lô C ⇒ nhớ luật **QC script glob cả thư mục** (mục 1 ở trên): `qc-pmid-batch.py` trên
thư mục này báo **117/117** (lô A+B+C), KHÔNG phải 71 của lô B. Số ký nhận phải loop riêng trên file.

| chất | chặng CÓ nguồn | chặng KHÔNG có nguồn (tag H thật) |
|---|---|---|
| sắt | 1,2,3,4,5,6,7(mồ hôi),8 | **không có đường thải chủ động** — mật→phân · nước tiểu · sữa · pha II liên hợp (không có) · bơm họ ABC |
| canxi | 1,2,5,6,7(mồ hôi),8 | **pha I và pha II ở gan (ion khoáng, không có)** · ~99 % canxi ở xương · % theo từng cửa · t½ huyết tương · PMCA/NCX · bơm ABC |
| curcumin | 1,2,3,4,5,6,7,8 | t½ ở NGƯỜI · % chính xác qua nước tiểu · cửa mũi/phổi · sữa/hơi thở · **thụ thể đặc hiệu trên mô đích** |
| paracetamol | 1,2,3,4,5,6,7,8 | t½ ở người · % liều qua nước tiểu · albumin · cửa mũi/phổi · da/sữa/hơi thở · họ SLC màng ruột |
| ibuprofen | 1,2,3,4,5,7,8 | **t½ ở người (giá trị số)** · % liều qua nước tiểu ở NGƯỜI · **bơm họ ABC đẩy ra (trống)** · kênh SLC · cửa mụi/phổi/da/sữa/mật |

**SỬA LẠI KẾT LUẬN Ở LÔ C: "chặng 6 (bơm đẩy) là chặng TRỐNG NHẤT" KHÔNG còn đúng sau lô B.**
Chặng 6 **có** nguồn thật cho 3/5 chất lô B — và chúng đi theo một quy luật dùng lại được:
**chất CÓ pha II liên hợp rõ thì thường CÓ bơm đẩy có tên** (curcumin → MRP2 · BCRP/ABCG2 · MRP4/ABCC4;
paracetamol → MRP4/ABCC4 · MRP3/ABCC3 · MRP2 · P-gp; sắt → ferroportin **SLC40A1**, bơm xuất sắt duy nhất).
Chặng 6 trống ở **chất vô cơ/ion** (canxi — ion, không có bơm ABC) và **NSAID** (ibuprofen).
Luật rút ra: **bơm đẩy bám theo con đường liên hợp, không bám theo "họ thuốc"** — nên tra chặng 4 trước
khi kết luận chặng 6 trống.

### Curcumin — HAI ĐIỂM BẮT BUỘC (đã đòi nguồn thật cho cả hai, không suy đoán)
Đây là mẫu cho lớp yêu cầu *"chất X có vấn đề đã biết là A và B — tìm nguồn thật cho cả hai"*:
1. **Sinh khả dụng rất thấp** — `22930441` kết luận **nguyên văn** *"the systemic bioavailability of CUR
   from the intestine after oral intake must be expected to be **virtually zero**"*; `21147222` Papp (A→B)
   chỉ **2,93 ± 0,94 × 10⁻⁶ cm/s**, **11,78 %** chuyển hoá NGAY khi vận chuyển, **> 20 %** tích trong tế bào;
   `40732360` công thức tan nước đạt AUC **> 7 lần** viên thường (chứng minh gián tiếp bằng RCT người n=12).
2. **Bất ổn trong môi trường kiềm / pH cao** — `9278892`: pH 7,2 / 37 °C trong đệm phosphate,
   **~90 % phân huỷ trong 30 phút**; *"decomposition was pH-dependent and occurred **faster at
   neutral-basic conditions**"* (dải thử pH 3→10). Sản phẩm chính
   trans-6-(4'-hydroxy-3'-methoxyphenyl)-2,4-dioxo-5-hexenal; phụ vanillin, acid ferulic, feruloylmethane.
   **Ổn định HƠN trong máu người / môi trường 10 % huyết thanh bò** (< 20 % phân huỷ trong 1 h, ~50 % còn sau 8 h).

Bẫy ghép số: **đừng hoán vị hai con số của hai điểm này.** "90 % trong 30 phút" là **độ bất ổn pH**
(9278892), còn "60–66 % hấp thụ" là **tỷ lệ hấp thụ [³H] ở chuột** (7342372). Hai đơn vị khác nhau,
hai câu hỏi khác nhau — gán lẫn là lỗi im lặng vì cả hai đều "đúng loại số".

Con số chặng 8 đã đọc abstract thật: chuột i.v. 20 mg/kg t½z CUR **32,4 ± 10,8 phút**, DHC 6,4, THC 5,6;
AUC₀₋∞ **107,0 / 6,0 / 12,0** (mg/L)·phút; **chỉ curcumin nguyên vẹn vào NÃO**, DHC ở thận, CUR ở gan;
chuột cống t½β tự do **3,15 ± 1,37 h** / nano **25,79 ± 0,87 h**; liều 400 mg [³H] còn hoạt độ trong mô
**12 NGÀY** ⇒ **có tích luỹ ở liều cao**, liều 10–80 mg thì không (72 h).

### Bằng chứng ÂM TÍNH mới cho `da_that_bai` (mẫu tốt)
- **canxi**: `19073913` — TRPV6 **KHÔNG bắt buộc** cho hấp thụ canxi do 1,25(OH)₂D₃ cảm ứng ⇒ giết giả
  thuyết "một kênh duy nhất giải thích hết"; `12566470` chuột KO thụ thể vitamin D cho hấp thụ tá tràng
  **↓ 71 %**, CaBP mRNA **↓ 55 %**, ECaC2 mRNA **↓ 95 %** ⇒ trục VDR/calbindin là bắt buộc.
- **paracetamol**: `40065514` **NAPQI VẮNG MẶT trong NÃO chuột** ⇒ giết giả thuyết "độc tính thần kinh
  do NAPQI" (và cảnh báo: đây là nguồn về **NÃO**, không dùng cho gan); `34901318` gọi cơ chế là
  *"unexplained mechanism of action"* ⇒ đừng viết "paracetamol ức chế COX trung ương" như sự thật đã chốt.
- **sắt**: `39814221` *"no active pathway for iron excretion"* ⇒ không được viết "sắt thải qua thận/mật";
  cảnh báo `41403447`-kiểu "t½" cho sắt là **sai khái niệm** — dùng **plasma iron turnover**, không dùng t½.

### Bảng gán sai MÔ / sai CHẤT của lô B — audit lại trước khi dùng
| PMID | title thật | MÔ/LOÀI thật | gán được cho ⚠ |
|---|---|---|---|
| **30562214** | …self-adjusted **ibuprofen** dose in the Coriell Personalized Medicine Collaborative | người · **n=445** | ⚠️ **LÀ BÀI VỀ IBUPROFEN, KHÔNG PHẢI PARACETAMOL.** Đã bị gán nhầm vào chặng 8 của *paracetamol* khi viết lô B. Câu *"no early signs of acute kidney injury"* cũng thuộc bài này ⇒ thuộc ibuprofen |
| 40065514 | **NAPQI is absent in the mouse brain** | **NÃO** chuột | chặng 5 paracetamol — phủ định; **KHÔNG** dùng cho gan (gan dùng 41034397/41685192) |
| 41034397 | …amplifies NAPQI in acetaminophen-induced **LIVER INJURY** | **GAN** chuột + tế bào L02 người | chặng 3/5 paracetamol — không dùng cho não |
| 41685192 | NAPQI adducts in **patients** with selective hypersensitivity | **huyết thanh** người | chặng 5 paracetamol — không dùng cho gan in-vivo |
| 42511236 | A **Rice Protein Peptide-Calcium Complex** Enhances Intestinal Calcium Absorption and Bone Formation via the **TRPV6-Calbindin9k** Axis | **ruột + xương** · Caco-2 + chuột thiếu canxi (Foods 2026) | chặng 2/5 canxi — nhưng nhớ đây là **phức peptide gạo-canxi**, KHÔNG phải canxi vô cơ ⇒ đừng dùng để nói về canxi carbonat/citrat |
| 30472169 | Ex vivo detection of calcium phosphate and calcium carbonate in **rat blood serum** | huyết thanh · **CHUỘT CỐNG** (ex vivo, XANES) | chặng 4 canxi — chia tCa = fCa + prCa + cCa; **không phải người** |
| 32507433 | Calcium loss in **sweat** does not stimulate PTH release: Bikram hot yoga | mồ hôi · người | chặng 7 canxi — mồ hôi 2,9 ± 1,7 mg/dL, mất 41,3 ± 16,4 mg/buổi |
| 24434184 | FGF23 promotes **renal** calcium reabsorption through the TRPV5 channel | **ống thận** chuột | chặng 5/7 canxi — **KHÔNG** dùng cho ruột; cũng đừng dùng làm nguồn cho chặng 3 ("không chuyển hoá ở gan") — chặng 3 canxi phải tag H |
| 17487259 | pig **colon and duodenum** for luminal iron absorption | **ruột** · **LỢN** | chặng 1/2 sắt — 14 % hấp thụ ở ruột già; lợi thế là **động vật lớn** (A) |
| 42826159 | DMT1 Facilitates **Heme-iron Absorption** in **Rats and Mice** | **ruột** chuột cống + chuột nhắt | chặng 1/2 sắt heme — 10,8 % vs 1,4 %; **KHÔNG** phải nguồn về máu-não |
| 29453024 | ibuprofen and its metabolites in complex **equine** urine | **nước tiểu** · **NGỰA** | chặng 3/7 ibuprofen — **phải ghi rõ loài NGỰA**, không gán cho người |
| 18043697 | Upregulation of **MRP3** … (paracetamol) | người | chặng 6 paracetamol — **`NO ABSTRACT`** (bài không có abstractText) ⇒ chỉ verify được title+DOI, phải nói rõ trong deliverable |

### Con số chặng 7–8 lô B đáng nhớ (đã đọc abstract thật)
- **sắt**: **KHÔNG có đường thải chủ động** — điều hoà ở khâu HẤP THỤ. Mất mồ hôi 0,08 mg/m²/h (tập) vs
  0,039 (nghỉ); runner 0,276 ± 0,140 mg/h (nữ) / 0,21 ± 0,13 (nam). Nhịp ngày/đêm: giải phóng lưới nội mô
  6 h = **54,1 % (sáng) vs 25,9 % (tối)**; sắt huyết tương ↓ 62 % (nam)/47 % (nữ) lúc 18 h. Serum ferritin
  **> 1000 µg/L** gắn tăng tử vong (gan). t½ = **không áp dụng** ⇒ dùng plasma iron turnover.
- **canxi**: nhiều chặng **không có khái niệm** t½/pha I/pha II (ion khoáng) — ghi thẳng tag H, đừng mượn
  số của chất hữu cơ.
- **paracetamol**: Tmax **0,66 h** (người Hoa) / **1,06 h** (da trắng); nồng độ đỉnh 23,8 / 18,7 µg/mL;
  liều thử 20 mg/kg. Người Hoa bài tiết **+6 % sulfate / −5 % glucuronid** so với da trắng. t½ người = tag H.
- **ibuprofen**: CL_**S** 3,98 mL/h (RSE 8 %) vs CL_**R** 18 mL/h (RSE 24 %) ở trẻ sơ sinh ⇒ **R thải nhanh
  gấp ~4,5 lần**; số mũ 2,25 (PNA) / 5,81 (GA); nhỏ so với tuổi thai **CL_S ×3,11**. HSA: Ka(R) = 5,3 × 10⁵
  M⁻¹ > Ka(S) = 1,1–1,2 × 10⁵ M⁻¹. Glucuronid hoá **YẾU**: Vmax/Km **1,6** (so với 45,4 và 8,0 của 2 thuốc khác).
  KHÔNG có khác biệt t½ giữa 2 enantiomer ở người khoẻ — nhưng **giá trị số t½ vẫn là tag H**.

---

## LÔ A — bank 5 chất (19/10/2026 · fixgby `10-cong-thuc-23` · **73 PMID verified 73/73**)

`thymol · carvacrol · eucalyptol (1,8-cineole) · propolis · glycyrrhizin` (lô A giao 12 chất, mới xong 5).
**`batch-a.{md,json}` CHƯA ĐƯỢC GHI** — 4 lần liên tiếp lô này hết ngân sách tool-call trước khi ghi byte nào.
Chi tiết đầy đủ + định dạng file nguồn + bộ dựng: `references/multi-item-deliverable-source-builder.md`.

| chất | chặng CÓ nguồn | chặng KHÔNG có nguồn (tag H thật) |
|---|---|---|
| thymol | 1,2(gián tiếp),3(không CYP),4,5,7,8 | **bơm họ ABC** · CYP pha I · protein chở trong máu · **cửa SỮA ở heo nái** · cửa phổi/da · t½ ở HEO |
| carvacrol | 1,5,6(chỉ "tích luỹ sinh học thấp") | **gần như toàn bộ 2,3,4,6,7,8** — không có PK định lượng nào cho carvacrol trên HEO |
| eucalyptol | 1(miệng + **mũi/phổi**),3,4,5(NÃO chuột + SỮA người),7,8 | **t½ (không có ở bất kỳ loài nào)** · cửa phổi/da · cửa mật→phân · mô đích ở HEO · thụ thể · bơm ABC |
| propolis | 1,2,3(không CYP),4,5,6,7,8 | t½ của propolis · PK trên HEO · cửa SỮA heo nái · % thải theo cửa · thụ thể |
| glycyrrhizin | 1,2,3(glucuronidase vi sinh, **không CYP**),4,5,6,7,8 | CYP ở HEO · kênh vận chuyển ở ruột HEO · % thải theo cửa · t½ ở HEO · cửa SỮA heo nái · dư lượng mô HEO |

### Điểm chốt đáng nhớ (số đã đọc abstract thật)
- **thymol**: `24548668` (HEO, 50 mg/kg vào DẠ DÀY) — **cửa vào là DẠ DÀY, không phải ruột**; `SLC15A1`
  (PEPT1) TĂNG; TRPA1 hạng 1072/128. `12092740` (người) — **không có thymol TỰ DO trong huyết tương**,
  chỉ thymol sulfate; Cmax 93,1 ± 24,5 ng/mL; Tmax 2,0 ± 0,8 h; **t½ 10,2 h**; **16,2 ± 4,5 % liều/24 h**
  ra nước tiểu. `34573560` (thỏ) IW > plasma, rs = −1,000. `41301947` (thỏ) tích tụ **thận** p = 0,0182 /
  **mô mỡ** p = 0,0003, sau ngừng 7 ngày dưới LOQ. Trần độc `42005330`: thymol > **1000** mg/kg, carvacrol > **2480** mg/kg.
- **carvacrol**: `32874282` (EFSA, **HEO CAI SỮA**) 250–1000 mg/kg feed = **100–400 mg carvacrol/kg**
  → quy ra premix 5 kg/tấn = **≤ 80 g/kg premix**; `38799727` chỉ **dạng vi nang (MEO)** mới hiệu quả,
  tinh dầu thường thì không; `41497464` nái 88,5 % vs 82,6 % heo con bán được.
- **eucalyptol**: `20425757` (người) **86** nmol/L (2-OH) vs **19** nmol/L (chất mẹ) ⇒ chuyển hoá rất mạnh;
  thải niệu 10 h **20,9 / 17,2 / 10,6 / 3,8 %**; `23983963` **chỉ HÍT aroma** đã vào huyết thanh
  ⇒ bay hơi mạnh, thất thoát khỏi premix bột + ô nhiễm chéo lô trộn; `24957890` α2-hydroxy-1,8-cineole
  trong **sữa mẹ 100–250 µg/kg** (người).
- **propolis**: `42598803` (người) **63 chất chuyển hoá huyết tương / 85 nước tiểu**; Tmax **1 h**;
  thải niệu **< 3 h**; **net bioavailability 57,16 % → 43,82 % khi tăng 4× liều** (tăng liều KHÔNG tăng hấp thu);
  `34449320` chrysin bị **UGT/SULT** (không CYP) + BCRP/MRP2 đẩy ra, nhưng **tái tuần hoàn gan-ruột làm
  nồng độ CAO ở hồi tràng/kết tràng** ⇒ mô đích.
- **glycyrrhizin**: `7742809` BA uống **~1 %** vs phúc mạc 65–90 %; `14522122` AUC tĩnh mạch **cửa < ngoại vi**
  ⇒ first-pass gan có thật; `11145169` + `10836746` (**in-vitro vi sinh NGƯỜI**) chuyển **55–100 %** thành GA,
  β-glucuronidase **2,7–6,8×**; `31083444` **t½ 23,1 ± 15,5 h** ⇒ nguy cơ tích luỹ;
  `29908072` OATP1B1/1B3 vào + **MRP2/BCRP/BSEP/MDR1 ra mật**, **rifampin ức chế OATP → TĂNG phơi nhiễm**
  (can thiệp bước VÀO ngược chiều bước RA); `33481180` MRP2 suy giảm → **3MGA tràn máu → nước tiểu qua
  OAT1/OAT3**; `34604277` 18β-glycyrrhetyl-3-O-sulfate **ức chế 11β-HSD2**.

### Lớp lỗi "bị BƠM THẢI RA" vs "ỨC CHẾ BƠM" — ví dụ chuẩn để dạy lại
`19732493`: **chrysin (flavonoid propolis) VỪA là cơ chất VỪA là CHẤT ỨC CHẾ BCRP** — cho **chuột cống**
uống làm TĂNG nồng độ nitrofurantoin (cơ chất BCRP), nhưng **KHÔNG** xảy ra ở **chuột nhắt** vì ruột non
chuột nhắt biểu hiện Bcrp thấp hơn. `25715997`: Ko143 ức chế BCRP làm GIẢM đẩy chrysin sulfate (Caco-2 +
chuột nhắt Bcrp1⁻/⁻). ⇒ Chặng 6 phải ghi **hai chiều khác nhau**, không gộp thành "tương tác BCRP".

### Bẫy MÔ/LOÀI của lô A — audit lại trước khi dùng
| PMID | title/mô thật | gán được cho ⚠ |
|---|---|---|
| (nguồn "carvacrol ức chế P-gp") | **MCF-7 = dòng tế bào UNG THƯ VÚ người** | **LOẠI** theo quy tắc audit mô — KHÔNG dùng cho ruột/gan |
| 36987546 | eucalyptol · **NÃO CHUỘT + hàng rào MÁU-NÃO** (thoát Evans blue ↑) | chỉ dùng cho phát biểu về **não**; **KHÔNG** mượn cho hàng rào ruột |
| 24957890 | cineole trong **SỮA MẸ người** | ghi rõ **người**, KHÔNG phải sữa heo (cửa sữa heo nái vẫn tag H) |
| 35088789 | glycyrrhizin mở tight junction · **Caco-2 (biểu mô RUỘT người, in-vitro)** | hợp lệ cho ruột, nhưng chấm **(R)** — không phải heo in-vivo |
| 11145169 · 10836746 | **in-vitro VI SINH RUỘT NGƯỜI** (Eubacterium sp. L-8, Streptococcus sp. LJ-22) | dùng cho cơ chế chung, **KHÔNG** trình bày như vi sinh ruột heo |
| 40732257 | propolis + enrofloxacin ở **THỎ** | t½ **11,75 h là của KHÁNG SINH**, không phải của propolis — không dùng lẫn |
| 42005330 · 10985073 · 40153080 | **tổng quan** (không nêu mô) | chỉ dùng để đánh dấu hướng / ngưỡng, không gánh số định lượng |

### Tương tác nội công thức đã có nguồn (mẫu tốt cho khoá `tuong_tac`)
1. **glycyrrhizin MỞ tight junction** (`35088789`) ⇒ cộng hưởng hấp thu với mọi thành phần khác trong premix
   (berberine BA 0,36 % là ứng viên đáng thử). Suy luận từ Caco-2 ⇒ **tag H cho heo**.
2. **Vi sinh ruột là mắt xích bắt buộc của cam thảo**: thymol/carvacrol/tannin diệt khuẩn mạnh ⇒ giảm
   chuyển glycyrrhizin → GA ⇒ **mất hiệu lực**. Cơ chế vi sinh có nguồn; **cặp trực tiếp tag H**.
3. **propolis ức chế chuyển hoá/thải thuốc khác** (`40732257` thỏ) + ức chế BCRP ruột (`19732493`).
4. **tannin kết tủa protein/enzyme** ⇒ giảm tiêu hoá chất khô (`33105748`, `28004617`) ⇒ giảm hấp thu chung.
5. **vi hạt/vi nang là ĐIỀU KIỆN, không phải tuỳ chọn**: thymol vi hạt alginate nhả **73,7 %** trong dịch dạ
   dày mô phỏng (`30141924`); carvacrol chỉ hiệu quả ở dạng MEO (`38799727`).
6. **eucalyptol bay hơi** (`23983963`) ⇒ thất thoát + ô nhiễm chéo.

### LUẬT VẬN HÀNH — vì sao lô này thất bại 4 lần
1. **Chia lô ≤ 5–6 chất / subagent.** 12 chất × 8 chặng × 6 trường + audit tiêu đề là vượt ngân sách tool-call.
2. **CHẠY BỘ DỰNG SAU CHẤT THỨ NHẤT, KHÔNG PHẢI SAU CHẤT CUỐI.** Ca này `_build.py` đã viết nhưng **chưa
   chạy lần nào** ⇒ 0 byte đầu ra. Chạy sớm giữ file đích LUÔN tồn tại và hợp lệ.
3. **Một write = một đơn vị công việc.** Write ~12–17 KB (một chất/file) qua sạch; write ~51 KB (data cả lô
   trong một file `.py`) **bị cắt còn 260 byte** + lint `SyntaxError: unterminated string literal`.
4. Nguồn dữ liệu = `src/<slug>.txt` một chất/file; bộ dựng sinh **CẢ** `.md` **và** `.json` từ cùng nguồn
   ⇒ hai bản không thể lệch nhau, và session bị ngắt chỉ cần viết tiếp file nguồn còn thiếu.
