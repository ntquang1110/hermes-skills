# Lô B — premix heo: enzyme · vi sinh · acid hữu cơ · betaine (khung 8 chặng)

**Ngữ cảnh:** fixgby `docs/10-cong-thuc-23/batch-b` (Nguyễn Thành Quang / TheFirstOnly + Vua Kiềm).
Sản phẩm: premix bột trộn cám heo, 2 kg/lô, trộn 5 kg/tấn cám → 400 kg cám/lô. Đây là TĂBS — **cấm claim
trị bệnh**, chỉ mô tả CƠ CHẾ + CHỈ SỐ.

**7 nguyên liệu:** Phytase (coated) · Xylanase (coated) · Protease (coated) · *Bacillus subtilis* (bào tử) ·
Calcium butyrate · Acid citric · Betaine HCl 98 %.

> **TRẠNG THÁI GHI FILE — CẬP NHẬT 19/10/2026 (lô enzyme đã xong).** `batch-b.md` (59.765 ký tự) +
> `batch-b.json` (63.860 byte) **ĐÃ TỒN TẠI**, sinh từ `src-b/{phytase,xylanase,protease}.txt` bằng
> `python _build.py src-b b` → `ingredients=3  unique_pmids=26`.
> **CẬP NHẬT 20/10/2026 — LÔ B ĐÃ ĐỦ 7/7.** 3 nguyên liệu enzyme + *B. subtilis* bào tử + calcium butyrate
> đã có `src-b/<slug>.txt`; acid citric + betaine HCl 98 % do các con song song viết trong cùng lượt.
> `python _build.py src-b b` → **`ingredients=7  unique_pmids=80`**, exit 0; `batch-b.md` = **56 khối**
> (`## a)`…`## h)` × 7 chất). Bank §2.1–2.7 dùng được ngay; **phần BỔ SUNG của 2 chất chốt 20/10 ở §2.9**
> (*B. subtilis* + calcium butyrate — ~41 abstract đọc thật trong lượt, 33 ID loại/giới hạn verify 33/33).
> Số liệu cho 3 enzyme đã được **bổ sung và verify trong chính lượt đó** → xem **§2.8** (mới) và các dòng
> chèn thêm ở **§3**; cách làm đã kiểm chứng end-to-end:
> `references/multi-item-deliverable-source-builder.md`.
> Kho bằng chứng thô còn ở `C:/Users/NTQUANG_DELL/epmc_work/work1.json` (tag `PHY-*`, `XYL-*`, `PRT-*`,
> `CB-*`/`BUT-*`, `ACID-*`/`CIT-*`, `BET-*`, `TAN-*`, `ENZ-*`).

---

## 1. PHÁN QUYẾT VỀ "CẢNH BÁO ĐIỂM SỐNG CÒN" CỦA SHEET DỰ ÁN

Sheet dự án ghi: *"Enzyme Phytase / Xylanase / Protease bắt buộc dạng coated hoặc chịu kiềm. Dạng thường
mất 50–80 % hoạt tính ở pH 8–9."*

**Kết luận trung thực: con số "50–80 % ở pH 8–9" KHÔNG có nguồn → `CHƯA CÓ NGUỒN (tag H)`. KHÔNG suy đoán.**
Ba lý do, đều có nguồn thật:

1. **pH 8–9 không tồn tại ở đoạn ruột nơi enzyme tác động (HEO).** `42462087` đo trực tiếp trên heo con
   cai sữa: dạ dày **4.0** · jejunum gần **6.0** · jejunum xa **5.9** · manh tràng **5.5** (p<0.05). Nghĩa là
   stress thật là **pH 2–4 + pepsin ở dạ dày**, không phải kiềm.
2. **Có nguồn ĐO Ở pH 8 và hoạt tính vẫn còn >50 %.** `30088242` — AppA (E. coli phytase) display trên bào tử
   *B. subtilis* bằng CotG: **giữ >50 % hoạt tính sau 12 h ở pH 2,0 / 4,0 / 7,0 / 8,0**; hoạt tính cực đại ở
   pH 4,5 và 55 °C. ⇒ pH 8 một mình **không** giết phytase.
3. **pH optimum thì thấp thật, nhưng đó là "hoạt tính tương đối", không phải "% mất do kiềm".** `11195907` —
   pH optimum 4,5–5,5 (4 phytase nấm), E. coli 4,5, **Bacillus 7,0**. `23594993` / `38819952`: phytase Bacillus
   pH optimum 7–8, giữ >70 % hoạt tính trong dải pH 5–10 ⇒ **"chịu kiềm" tồn tại thật ở nhóm Bacillus phytase**,
   nhưng con số 50–80 % phải bỏ khỏi tài liệu.

**Cái THAY THẾ được — stress thật, có số:**

| Stress | Số thật | PMID | Mô & loài |
|---|---|---|---|
| Ép viên 84 °C | P tự do sau ép chỉ còn **53 %** so với mash | 9795986 | HEO (in vitro trong cám + in vivo) |
| Conditioner 70 °C | nhóm bền nhiệt nhất giữ **~70 %**, nhóm còn lại **~30 %** | 11195907 | in vitro, 6 phytase thương mại |
| T½ nhiệt | **T½ = 1 h ở 70 °C** (P. oxalicum, pH opt 3,0, kháng trypsin+pepsin) | 40655371 | in vitro |
| Dịch vị | *P. lycii* bền nhiệt NHẤT nhưng **kém bền dịch vị NHẤT**; *A. niger* + *E. coli* bền dịch vị nhất | 25562369 | in vitro (mô phỏng dạ dày) |
| Pepsin/pancreatin | **chỉ** E. coli phytase không bị ức chế bởi pepsin + pancreatin | 11195907 | in vitro |
| Dịch dạ dày | phytase giữ **76 và 80 %** hoạt tính qua tiêu hoá dạ dày; Ca cao làm giảm hydrolysis | 20836179 | in vitro mô hình GI HEO |
| Tồn trữ 23 °C | ≥**85 %** (nguyên chất) / **73 %** (premix vitamin) / **60 %** (premix VTM) ở 180 ngày; coated > uncoated **mọi** mốc | 21890502 | 360 d, 3 nguồn phytase thương mại |
| Xylanase nhiệt | Tm **87,2 °C**; bền dải **pH 2,0–10,0 tới 4 h**; kháng TAXI-IB/TAXI-IIA/XIP | 39522348 | in vitro (bài trên gà) |
| Xylanase acid | hoạt tính còn lại pH 4,0/4,5/5,0 = **53,07 / 69,8 / 82,4 %** (WT) | 38670187 | in vitro (làm trong) |

**Hệ quả cho công thức:** premix của lô là dạng **trộn bột** ⇒ rủi ro thật là **TỒN TRỮ** (đúng ô
"VTM premix" của `21890502`: chỉ còn 60 % sau 180 ngày) — chứ không phải pH 8–9. Betaine HCl 98 % + acid
citric trong cùng premix là **tải acid**, nên đây là luận điểm nên đưa vào `tuong_tac`.

---

## 2. BANK THEO CHẤT (số liệu đã đọc abstract thật, mức (I)/(A)/(R))

### 2.1 Phytase (coated)
| PMID | Số liệu thật | Mức | Mô & loài |
|---|---|---|---|
| 31769698 | meta-analysis **88 thí nghiệm / 74 bài / 547 dòng số**: tiêu hoá P **+25,6 điểm %** (SE 1,54) lên bình nguyên **64,9 %**; P tiêu hoá **+1,01 g/kg** (SE 0,102) → **2,62 g/kg**; R²=0,780 | A | HEO (meta) |
| 9795986 | AFP 500 U/kg: tiêu hoá P biểu kiến **52,8 % vs 30,8 %**; P phân **−13…−33 %**; ép hơi ~84 °C → free P = 53 % của mash | A | HEO non + vỗ béo |
| 23148255 | coated (C) vs uncoated (U) ở heo cai sữa, ép viên 80/90 °C: C ép viên ↑ATTD P + năng lượng vs C mash; **kết luận: bioefficacy sau ép viên KHÔNG bị ảnh hưởng bởi lớp coating** | A | HEO (n=56) |
| 8463857 | phân giải phytate dạ dày+ruột non **35–45 %** (khẩu phần không phytase) vs **65 %** (khẩu phần có phytase nội tại); toàn ống tiêu hoá **97 / 77 / 42 %** khi Ca 4,5 / 9,9 / 15 g/ngày | A | HEO đực thiến, fistula hồi tràng |
| 12357589 | phytase nội tại của cám lái phân giải phytate ở DẠ DÀY; ruột non + ruột già: **alkaline phosphatase cao, phytase thấp** bất kể khẩu phần; phân giải toàn ống gần như hoàn toàn | A | HEO |
| 38819952 / 23594993 | phytase Bacillus pH optimum **7–8**; >70 % hoạt tính dải pH 5–10; 80 %/62 % sau 70 °C 10/30 phút | R | in vitro |
| 27336313 | rPhyPt4 (peat-soil): T½ dịch vị **dài hơn mọi phytase "gastric-stable" đã báo**; dải pH 1,5–5,0; opt pH 2,5 = 2.790 µmol/min/mg ở 37 °C | R | in vitro |
| 24315971 | Y. mollaretii tiến hoá định hướng: M1 giữ **993 U/mg = 93 %** hoạt tính WT; T50 +1,5 °C ở 58 °C | R | in vitro |

### 2.2 Xylanase (coated) — **bằng chứng HỖN HỢP, phải ghi cả hai chiều**
| PMID | Số liệu thật | Mức | Mô & loài |
|---|---|---|---|
| 29766982 | heo 17,6 kg, 0→1400 LXU/kg: tiêu hoá hồi tràng **NDF 27,9→40,3 %**, **DM 55,4→64,6 %**, **OM 59,2→67,7 %**, **năng lượng 58,8→68,0 %** (tuyến tính); độ nhớt dịch jejunum **2,9→2,5 cP** (phi tuyến) | A | HEO đực thiến |
| 39595308 | 312 heo cai sữa 5,1 kg, 900–7200 U: **KHÔNG cải thiện tăng trưởng**; ↓ tỉ lệ phân điểm 3–4 (tiêu chảy) tuần 2–3; ↑ATTD NDF/ADF; ↓ độ nhớt manh tràng | A | HEO cai sữa |
| 29508681 | 512 heo grower tới **32.000 BXU/kg**: **KHÔNG** ảnh hưởng tăng trưởng, ATTD, VFA, peptide YY (chỉ xu hướng tăng pH hồi tràng) | A | HEO grower |
| 25049899 | complex amylase+protease+xylanase 100/150 ppm: ↑khối lượng, G:F, tiêu hoá GE (tuyến tính); ↑acetic/propionic/butyric manh tràng + kết tràng; ↑Lactobacilli, ↓E. coli | A | HEO cai sữa |
| 31532988 | xylanase *B. subtilis* XynA vs **chất ức chế nội tại lúa mì** (TAXI/XIP/TLXI): nhạy cảm hơn ⇒ cần **gấp 7 và 53 lần** liều enzyme để đạt hiệu quả tối đa | R | in vitro (làm bánh mì) |
| 36499321 | review 3 họ xylanase inhibitor thực vật: TAXI / XIP / TLXI | R | review |
| 11424701 | 5 chế phẩm feed enzyme: polysaccharidase **bền** trong dịch dạ cỏ sau cho ăn; pepsin pH 3 / pancreatin pH 7 | R | **DẠ CỎ bò sữa** — KHÔNG phải heo |

### 2.3 Protease (coated)
| PMID | Số liệu thật | Mức | Mô & loài |
|---|---|---|---|
| 39506561 | 10 heo fistula 21 kg, SBM, 0/15.000/30.000/45.000 NFP/kg (=0/25/50/75 g/tấn ProAct 360): pha I tăng **tuyến tính SID của 7/11 AA không thay thế được**; tốt nhất ở **30.000 NFP/kg (50 g/tấn)**; heo NON có SID CP + 15/18 AA cao hơn **~5,6 %** AA không thay thế so heo lớn | A | HEO (cannulated) |
| 38181459 | 96 heo 20,66 kg, khẩu phần sorghum 66,98 %, **400 mg/kg** protease: ↑BW d21/28, ↑ADG, ↑ATTD GE/CP/DM; ↓globulin, ↑albumin, ↑IgG, ↑ALB/GLB | A | HEO grower |
| 40519622 | 24 heo cai sữa 10,94 kg, CP 18,78 vs 16,92 % × PT 0/0,1 %: tuần 2 ↑ATTD CP ở PT10 vs PT0 | A | HEO cai sữa |
| 42526864 | β-mannanase 0,05 % (400 U/kg), 5 heo fistula 20,25 kg: ↑tiêu hoá DM+CP; ↑SID Arg, Lys, Thr; ↑ hoạt tính trypsin, protease, amylase | A | HEO grower sớm |
| 12097670 | ngũ cốc họ đậu làm tăng mất protein nội sinh ở hồi tràng: band 25/27/30 kDa = **trypsin heo**, chymotrypsin | A | HEO cai sữa |

### 2.4 *Bacillus subtilis* (bào tử) — **mạnh nhất trong lô về phía HEO**
| PMID | Số liệu thật | Mức | Mô & loài |
|---|---|---|---|
| 41813752 | 384 heo cai sữa 28 d → 30 kg, BS = 0,1 % **bào tử *B. subtilis* 87Y**, 72 d: N phân **−32 %**, N nước tiểu **−29 %** (6,6→4,5 g/con/ngày); tổng P thải **−39 %** (3,05→1,85); **Ca tồn lưu +187 %**; Zn phân **−63 %**, Cu **−39 %**; **AID của P 47→70 %** | A | HEO cai sữa (Y×L) |
| 36949225 | 96 heo con nursery, BS9 2×10⁷ / 2×10⁹ CFU/con vs ZnO 3.000 mg/kg: ↓FCR pha 2 + toàn kỳ; ↓ tỉ lệ tiêu chảy; ↓E. coli + coliform phân, ↑LAB + Bacillus; ↓mRNA IL-8, **↑MUC-1, occludin, TJP-1** | A | HEO con nursery |
| 35158640 | 150 heo con cai sữa 7,53 kg, *B. subtilis* C-3102 **300 g/tấn**, 6 tuần: ↑BW, ADG, G:F | A | HEO con |
| 37583344 | 320 heo con cai sữa, QST713 100/200 mg/kg ± β-mannanase: ↑ăn vào (BS100 d1–21); ↓FCR (BS100XT); ↓E. coli + *C. perfringens* d21 | A | HEO con |
| 39965290 | 78 NÁI đa sản (L×Y), QST713 1,5×10⁹ CFU/kg từ d85 thai → d21 tiết sữa: ↓thời gian đẻ, ↓thai chết lưu, ↓heo con không hợp lệ; **↑protein sữa đầu + IgM** | A | NÁI (sữa đầu) |
| 33005761 | 32 nái L×Y d90 thai, *B. subtilis* PB6 0,2 % (4,0×10⁸ CFU/kg): ↑ổ đẻ (tổng + sống, P<0,01); ↓MDA, ↑T-AOC huyết thanh | A | NÁI |
| 16547057 | bào tử **nảy mầm VÀ tái tạo bào tử trong ruột chuột**; chủng phân lập tự nhiên tồn tại lâu hơn chủng phòng thí nghiệm ⇒ "không phải khách quá cảnh" | A | **CHUỘT** |
| 34408741 | 11 người ileostomy: bào tử + tế bào sinh dưỡng **xuất hiện ở hồi tràng từ 3 h**; 9,7×10⁷ ± 8,1×10⁷ CFU/g dịch ở 6 h | I | NGƯỜI |
| 22968412 | *B. subtilis* C-3102 trong TIM-1: sống sót **99 %**, nảy mầm **8 %**; dịch ra làm ↑một số Bifidobacterium, ↓một số Clostridium | R | in vitro mô phỏng NGƯỜI |
| 34925306 | nảy mầm **theo chủng + theo chất cảm ứng**; **L-ALANINE** thúc đẩy rõ các chủng có tiềm năng nảy mầm; gen nảy mầm tăng biểu hiện | R | in vitro + in vivo |

### 2.5 Calcium butyrate
| PMID | Số liệu thật | Mức | Mô & loài |
|---|---|---|---|
| 34237915 | **nguồn calcium-butyrate ĐÚNG của lô**: 72 heo con cai sữa 7,17 kg, Ca-butyrate + tanin 0,15 %/0,075 % vs colistin 40 mg/kg: ↓tỉ lệ tiêu chảy d1–14 và d1–35; ↓độ sâu crypt tá tràng d14; ↓COX-2 (d14) và **TNF-α (d35)** tá tràng | A | HEO con |
| 34605248 | 12 heo đặt catheter đa cơ quan 25,6 kg: **PDV là nguồn phóng thích chính** của acetate/propionate/butyrate/isovalerate/valerate (P=0,001); gan hấp thu mạnh mọi SCFA (trừ acetate); **butyrate: chỉ 42 % [23; 60]** phóng thích từ PDV thoát khỏi vùng splanchnic; **cơ và thận** là cơ quan chuyển hoá ngoại vi chính | A | **HEO** (mô hình dịch chuyển) |
| 20050950 | heo 97 kg, inulin-coated butyrate ~150 g/ngày (81 g butyrate), 6 ngày: coating được tiêu hoá bởi VSV **ở hồi tràng**; **↑mRNA MCT1 ở hồi tràng**; ↓apoptosis; **lông nhung dài +~25 %** | A | HEO |
| 18313333 | ruột HEO: mRNA MCT1 ở ruột già **cao gấp 20 lần** ruột non; protein 41 kDa; ruột non = tế bào miễn dịch lamina propria/nang lympho; **kết tràng = tế bào biểu mô là nguồn chính** | A | HEO |
| 9824713 | túi màng bề mặt lòng ruột kết HEO + NGƯỜI: MCT1 vận chuyển **L-lactate và butyrate**, kiểu proton-activated/anion exchange | A/R | HEO + người |
| 29845774 | **heo con**, tributyrin = **chất ức chế HDAC**: thay đổi tiềm năng sinh cơ của tế bào vệ tinh; **tỉ lệ DNA:protein +~40 %** sau 21 ngày | A | HEO con |
| 26491121 | heo con cai sữa 28 d, 1.000 mg SB bao vi nang/kg + kháng sinh giảm liều: ↑khối lượng, G:F; ↓tiêu chảy; **lactulose:mannitol nước tiểu −25 %**; ↑occludin jejunum + kết tràng; MDA **−42 %**, TNF-α **−63 %** | A | HEO con |
| 39978008 | 96 heo cai sữa 6,60 kg, NaB bao lipid 0,05 %: **G:F +16 %**; thông lượng FD4 jejunum **−32 %**; dòng ngắn mạch **−52 %** | A | HEO nursery |
| 32048746 / 2100936 | 0,2 % Na-butyrate heo vỗ béo: ↑BW cuối, ↑tăng trọng/ngày, ↑khối lượng thân thịt | A | HEO 27,4 kg / 7–102 kg (ADG **+23,5 %**) |
| 35968955 | butyrate + acid mật thứ cấp **CẢM ỨNG** biểu hiện **P-gp chức năng** ở biểu mô ruột (vai trò HNF4α) ⇒ butyrate **TĂNG** bơm thải, **KHÔNG ức chế** | A/R | biểu mô ruột (chuột + dòng tế bào) |
| 38073487 | SCFA (butyrate) kích thích thông lượng Ca ở manh tràng **~2 lần**; **NHE3 + TRPV6** tham gia một phần | R | **CHUỘT** |

### 2.6 Acid citric — **bằng chứng YẾU trên heo, phải nói thẳng**
| PMID | Số liệu thật | Mức | Mô & loài |
|---|---|---|---|
| 9690644 | heo con cai sữa 7,4/9,6 kg, 3×4 (CA 0/1,5/3,0 % × phytase 0/250/500/750 U/kg): **CA hạ pH khẩu phần VÀ pH dịch dạ dày (P<0,05)**; CA ↑ADG, hiệu quả thức ăn, tiêu hoá Ca (Exp1) nhưng Exp2 không; **KHÔNG có tương tác cộng hợp (synergy) giữa CA và phytase** | A | HEO con |
| 10764076 | gà + **heo 10–11 kg**: gà đáp ứng mạnh (tibia ash +43 %, tăng trọng +22 % ở 6 % citrate) và CA tác động chủ yếu lên **sử dụng phytate-P, KHÔNG phải Ca**; ở HEO phản ứng **nhỏ hơn nhiều** — phytase cải thiện mọi chỉ tiêu | A | GÀ + HEO |
| 3198539 | 192 heo cai sữa 4 tuần: **CA KHÔNG cải thiện ADG** qua 4 tuần; còn giảm lượng ăn tuần 1 (P<0,05) | A | HEO cai sữa |
| 42462087 | 144 + 540 heo nursery: **pH dịch dạ dày 4,0 · jejunum gần 6,0 · jejunum xa 5,9 · manh tràng 5,5**; **giảm ABC khẩu phần 40–50 meq/kg bằng acidifier KHÔNG đủ** để hạ pH dịch dạ dày | A | HEO nursery |
| 39935381 | **ABC-4 200 meq/kg (d0–10) và 250 meq/kg (d10–24)** cải thiện tăng trưởng + DM phân so nhóm ABC-4 cao | A | HEO cai sữa |
| 39508819 | **SLC35G1** = transporter màng basolateral cho hấp thu citrate ở ruột non; màng đỉnh = **NaDC1/SLC13A2**; SLC35G1 bị **ức chế bởi ion Cl⁻ ở nồng độ sinh lý** | R | tế bào biểu mô ruột (hệ tế bào NGƯỜI) |
| 10192253 | **cùng** Na⁺/dicarboxylate cotransporter ở màng vi nhung mao tế bào ruột và ống thận gần; NaDC-1/hNaDC-1 từ thận thỏ/người | R | review (thận + ruột) |
| 2595270 | người, tưới jejunum: **citrate 355 ± 87 µmol/cm/h**; betaine **313 ± 125 µmol/cm/h**; 46 mmol/l citrate hoặc 36 mmol/l betaine KHÔNG ảnh hưởng hấp thu nước | I | NGƯỜI (jejunum) |

### 2.7 Betaine HCl 98 %
| PMID | Số liệu thật | Mức | Mô & loài |
|---|---|---|---|
| 23980906 | 6 tình nguyện viên, ức chế tiết acid bằng rabeprazole, **1.500 mg betaine HCl** hạ pH dịch dạ dày **4,5 ± 0,5 đơn vị: 5,2 → 0,6** | I | NGƯỜI |
| 12534635 | 12 nam + 3 bệnh nhân: **t½ hấp thu 0,28 h**, phân bố 0,59 h, **Cmax 0,94 mmol/L ở tmax 0,90 h**, **t½ thải trừ 14,38 h**; **lặp liều: t½,z tăng lên 41,17 h ⇒ CÓ TÍCH LUỸ**; DMG tích luỹ tương tự; **thải niệu = 4 % liều**; chủ yếu thải bằng CHUYỂN HOÁ | I | NGƯỜI |
| 1657504 | **BHMT VẮNG HOÀN TOÀN ở NÃO** của người, heo, chuột; có ở **gan + thận** người và heo (chuột chỉ gan) | A | NGƯỜI + HEO + chuột |
| 9281325 | mô HEO: chỉ **gan + thận** có BHMT; **vỏ thận** chứ không phải tuỷ; tuỵ, não, tim, phổi, lách đều âm tính; gen người 5q13.1-q15 | A | HEO + người |
| 21156199 / 23948084 / 11516176 | BHMT + BHMT-2 heo đã clone (407/363 aa, 78 % tương đồng); biểu hiện từ G45; **gen ống thận gần vỏ thận** — tế bào chất | A | HEO |
| 24795654 | **BGT1 = SLC6A12**, đồng vận chuyển Na⁺/Cl⁻, nhận betaine + GABA; nghiên cứu kỹ nhất ở **TUỶ THẬN** (MDCK), điều hoà bởi TonEBP/NFAT5 ⇒ **đừng dùng cho ruột** | R | thận (bài review) |
| 11223388 | **GÀ THỊT**: hấp thu betaine đồng vận chuyển Na⁺ **tá tràng > không tràng**; betaine vào máu **nhanh hơn và nồng độ cao hơn** choline/methionine; **betaine ở dạng TỰ DO trong huyết tương** còn choline/methionine gắn **lipoprotein**; 24 h phần lớn nhãn betaine ở **PHA NƯỚC trong CƠ** | A | **GÀ THỊT** |
| 22307525 / 34944185 / 41096440 | heo Alentejano 1 g/kg 20 tuần: ↑lipid nội cơ ở longissimus dorsi + biceps femoris (không đổi mỡ toàn thân); heo Ningxiang 0,2 %: **↓dày mỡ lưng, ↓tỉ lệ mỡ, ↑tỉ lệ nạc**; mảnh mô mỡ heo Iberian + betaine 200 µM: **↑lypolysis không kích thích +73 %**, bù lại tác dụng của sốc nhiệt (−47 %) | A | HEO |
| 40372560 / 27733523 | **SỮA**: nái 0,2 % betaine ↓nhiệt độ cổ; nái >5 lứa ↑sản lượng sữa; **nồng độ betaine trong sữa nái nhạy với choline khẩu phần mẹ và ngày tiết sữa (P<0,001)** | A | NÁI |

### 2.8 BỔ SUNG 19/10/2026 — nguồn **HEO in-vivo** cho 3 enzyme (đã đọc abstract thật, dùng trực tiếp)

Đây là bank đã đi vào `src-b/{phytase,xylanase,protease}.txt` (67 / 65 / 68 dòng; union **26 PMID** trong
dòng bảng, verify **29/29** tồn tại + title khớp). Ưu tiên bảng này khi làm lại: **gần như toàn bộ là HEO**,
khác hẳn §2.1–2.3 vốn nặng in-vitro.

**Phytase (coated)**

| PMID | Số liệu thật | Mức | Mô & loài |
|---|---|---|---|
| 25382707 | **NEO của cả 3 chặng "không hấp thu"**: hoạt tính phytase bổ sung **KHÔNG thu hồi được ở HỒI TRÀNG heo** ⇒ không vượt hết ruột non, không vào máu ⇒ first_pass KHÔNG, chặng 6 n/a, t½ huyết tương tag H. Cũng là nguồn cho "độ đề kháng protease nội sinh là yếu tố quyết định hiệu lực" | A | HEO + non-ruminant (review) |
| 40585274 | **SỐ DUY NHẤT tìm được cho "coated chịu nhiệt viên nén"**: RR (thu hồi hoạt tính) sau steam conditioning–pelleting–cooling **giảm khi 75 → 85 °C**; **coating thế hệ 2 tăng RR và giảm mất hoạt tính so với phytase KHÔNG bọc ở CẢ 75 và 85 °C (p<0,05)** | R | mô phỏng quy trình ép viên (đích heo/gia cầm) |
| 40919030 | 6-phytase sinh học mới **500 FTU/kg**: ATTD P **+13,5 điểm %** (heo con cai sữa) / **+24,6 điểm %** (heo lớn); **bone ash +27,6 % / +9,3 %**; **bone P +29,3 % / +7,0 %** | A | **HEO** — xương metacarpal |
| 40808565 | liều **0/500/750/1000/1500 FTU/kg** → **myo-inositol huyết tương tăng TUYẾN TÍNH theo liều (p<0,01, pha 2)** ⇒ cạnh "chỉ SẢN PHẨM mới vào máu" | A | **HEO CON cai sữa** |
| 41301988 | **2.500 vs 5.000 FTU/kg**, 375 heo ~94,6 kg: plasma inositol ↑, glucose huyết thanh ↑, AST ↓ (p<0,05) ⇒ chưa bão hoà trong dải đã thử | A | **HEO VỖ BÉO** |
| 41227420 | **NÁI**: Ca huyết thanh **+73 %** (500–1500 FTU/kg) và **+140 %** (2500); P **+55 / +59 / +118 %** lúc cai sữa; **thời gian đẻ −24,2 / −23,8 / −14,8 phút**; KL cai sữa ổ **+6,1–8,2 %**. **KHÔNG đo phytase trong sữa** ⇒ cửa SỮA vẫn tag H | A | **HEO NÁI** |
| 41566379 | mẫu **RUỘT HEO** (culturomics): ~**30 % loài** vi khuẩn phân giải myo-inositol; chủng CÓ phytase **nuôi chéo** cho chủng KHÔNG có, **kể cả *Salmonella* Typhimurium** | A | **VI SINH RUỘT HEO** |
| 42791756 | bỏ **hoàn toàn** phosphate vô cơ, chỉ 6-phytase lai, cai sữa → giết mổ: tăng trọng + khoáng hoá xương **tương đương** đối chứng ⇒ hiệu ứng "có nhớ" ở mô KHOÁNG (dùng cho chặng 8, KHÔNG phải t½) | A | **HEO** — xương |
| 42278145 | meta heo: ADG **+0,068 kg/ngày**, DFI **+0,106 kg/ngày**, FW **+4,630 kg**, FC **−0,115** | A | **HEO** (meta) |

**Xylanase (coated)**

| PMID | Số liệu thật | Mức | Mô & loài |
|---|---|---|---|
| 38254395 | review Carbohydrases and Phytase in Poultry/Pig — nguồn neo cho "carbohydrase ngoại sinh tác động nền NSP + hệ vi sinh/niêm mạc ruột, **không** qua chuyển hoá gan" (chặng 1 và 3) | A | HEO + gia cầm (review) |
| 42291120 | heo cai sữa, cám NSP cao: ↑ADG + G:F d1–7 và d1–14 (p<0,05); ↑ATTD DM, ↑AID DM d28; **↓TNF-α niêm mạc hỗng tràng** (p<0,05), ↓IgG (p=0,066), ↓MDA (p=0,070) | A | **HEO cai sữa** |
| 38280204 | 192 heo 8,7 kg; cám thiếu ME 3.300 kcal làm **↑độ nhớt dịch hỗng tràng + ↓AID DM/GE**; xylanase **1.200/2.400/3.600 XU/kg** ↓độ nhớt, ↑AID DM+GE, ↑*Prevotella*, ↓*Helicobacter*, ↓protein carbonyl | A | **HEO nursery** |
| 38704593 | 40 heo 6,5 kg, xylanase+β-glucanase **280–1.120 TXU/kg**: độ nhớt dịch hỗng tràng giảm theo **hàm bậc hai, tối thiểu 1,74 mPa.s ở 751/335 TXU/TGU per kg**; Lactobacillaceae **tối đa 40,3 %**, Prevotellaceae **tối thiểu 0,6 %**, Helicobacteraceae **tối thiểu 1,6 %**; VH:CD tối đa **2,62** | A | **HEO nursery** |
| 37991108 | 20 heo nái chưa sinh 30,6 kg, cannula hỗng tràng + hồi tràng, 3 giai đoạn 17 ngày, Econase XT 25P **100 mg/kg**: **AJD chất khô P1 = 6,3 % vs đối chứng ít xơ 15,5 %; P3 = 15,3 % vs đối chứng nhiều xơ 11,7 %** ⇒ CẦN THỜI GIAN THÍCH NGHI. Đồng thời là nguồn cho "**độ nhớt KHÔNG giảm** ở cám ngô nhiều xơ (p>0,10)" | A | **HEO** (cannulated) |
| 39595308 | 312 heo cai sữa 5,1 kg, 900–7.200 U: **không cải thiện tăng trọng**; ↓độ nhớt **KẾT TRÀNG**; ↑ATTD NDF/ADF; **↓ tổng VFA + acetic/propionic/butyric/valeric ở MANH TRÀNG** ⇒ hướng VFA **KHÔNG nhất quán**, ghi cả hai chiều | A | **HEO cai sữa** |
| 39930968 | in-vitro tiêu hoá **mô hình HEO**: xylanase+cellulase 20.000 U/kg ↓arabinoxylan chất chứa không tiêu hoá của **LÚA MÌ 53→46 g/kg (p<0,05)** nhưng **KHÔNG đổi trên NGÔ (42→44 g/kg, p>0,05)** | R | mô hình in-vitro HEO |
| 40096523 | 12 heo cannula hồi tràng 31,7 kg: AID **Ile 77,3→80,0 %**, Thr 73,8→77,8 %, Trp 83,2→86,6 %, CP 71,1→75,9 %, GE 61,5→67,6 %, NDF 22,0→29,1 %, TDF 29,2→37,1 %, cellulose 12,5→22,0 %; ATTD DM 75,4→78,9 %, CP 80,8→85,7 %, GE 76,5→79,4 % | A | **HEO grower** (cannulated) |
| 40375102 | nái tiết sữa **16.000 BXU/kg** → heo con từ nái có xylanase **KHÔNG khác gì** nhóm đối chứng (không có tương tác nái × heo con) ⇒ **BẰNG CHỨNG ÂM TÍNH cho cửa SỮA** | A | **HEO NÁI + HEO CON** |
| 40453315 | heo 7,2 kg, 6-phytase + xylanase **2.440 XU/kg** + β-glucanase 304 U/kg: BW **+1,82 kg** (starter II), **+5,11 kg** (grower I) (p<0,05); chi phí thức ăn/kg tăng trọng **−7,3 %** | A | **HEO** |

**Protease (coated)**

| PMID | Số liệu thật | Mức | Mô & loài |
|---|---|---|---|
| 41153964 | 90 heo đực 13,52 kg, khô dầu đậu nành: protease **AXIT** P2 **0,01 %** ↑AID+SID của **Lys, Met, Phe, Ala, Cys, Glu 7,5–22 %**; **KHÔNG cải thiện trên NGÔ (p>0,05)** ⇒ chặng 2 phải nêu rõ cơ chất | A | **HEO CON** (hồi tràng, pp chỉ số) |
| 40519622 | 24 heo đực 10,94 kg, CP 18,78 vs 16,92 % × PT 0/0,1 %: PT0,1 ↑ATTD CP **tuần 2** (không tuần 1), ↑ATTD Thr/Ile/Leu/Arg/Met, ↓BUN, ↓H₂S, ↓tổng N bài tiết, ↑tỷ lệ giữ N; **không đổi tăng trưởng** | A | **HEO cai sữa** |
| 42651943 | 96 heo con 26 ngày, protease ± amylase: protease ↓BUN (p<0,01), ↑GPx, ↓**D-lactate + diamine oxidase** (chỉ dấu tổn thương hàng rào ruột), ↑acetic + valeric acid phân, làm giàu **Anaerovoracaceae + Blautia**. Tác dụng lên ĐẠM chỉ rõ khi phối **amylase** | A | **HEO CON** |
| 42450685 | 160 heo 33,0 kg, nền cám đa dạng + enzyme 0,02 % **có protease**: ↑ATTD DM/OM/CP/GE, ↑G:F d15–28, ↑hoạt tính **chymotrypsin + amylase** hỗng tràng, ↑Chlamydiaceae | A | **HEO grower** |
| 42282997 | 355 + 356 heo, blend carbohydrase + protease ở **0 / 0,01 / 0,02 / 0,03 %** → **KẾT QUẢ ÂM**: không cải thiện tăng trưởng/tiêu hoá, còn **↓chiều cao nhung mao tá tràng (p=0,017)** | A | **HEO nursery** |
| 42514626 | 200 heo con 6,01 kg; hạ **2 % CP** làm ↓BW d7/19/31 + ↓ADG; protease **0,1 g/kg** phục hồi MỘT PHẦN; ADFI/FCR/tiêu hoá DM-N-E/điểm phân **KHÔNG đổi** (p>0,05) | A | **HEO CON cai sữa** |
| 42373590 | INFOGEST in-vitro, khô dầu đậu nành: tiêu hoá protein **83–89 % → 90–96 %** (Protease I) và **91–92 %** (Protease II); giảm một số epitope gây dị ứng ⇒ dùng cho **CƠ CHẾ** (peptide + epitope), **KHÔNG** phải số trên heo | R | in-vitro (không phải heo) |
| 41746456 | **CHỈ dùng cho PHƯƠNG PHÁP cân bằng nitơ** (lồng trao đổi chất, thu trọn phân + nước tiểu 4 ngày). Thiết kế gộp probiotic *B. subtilis* + đa enzyme CÓ protease, và một nhánh gộp cả kháng sinh (lincomycin + colistin) ⇒ **KHÔNG tách được** đóng góp của protease — không trích số tác dụng | A | **HEO CON** (phương pháp) |

**Ba luật rút ra cho lô enzyme (áp cho cả 3 chất, không chỉ chất đang viết):**
1. Chặng **3 / 4 / 6** và **t½ huyết tương** của CẢ BA enzyme = **KHÔNG / tag H**, neo bằng `25382707`
   ("hoạt tính bổ sung không thu hồi được ở hồi tràng heo") + `38254395`. **Cấm suy diễn** CYP · SLC · ABC
   cho một protein ngoại sinh nằm trong lòng ruột.
2. Chặng 2 **phải nêu CƠ CHẤT + cơ chế tăng tiêu hoá**, không được để trống: phytate → inositol phosphate +
   P vô cơ + **myo-inositol** (`40808565`, `41301988`) · arabinoxylan → **XOS** + ↓độ nhớt (`38704593`,
   `38280204`) · protein → peptide/AA (`41153964`, `42373590`).
3. Số về **coated chịu nhiệt viên nén CHỈ có thật với phytase** (`40585274`). Với xylanase và protease phải
   ghi thẳng **CHƯA CÓ NGUỒN (tag H)**; chỉ được dùng `41419619` như **proxy DẠNG VI NANG có gắn cờ**
   chủng/bộ enzyme (xem §3) — không được lấy số của nó làm số của xylanase.

---

## 3. BẪY MÔ / LOÀI CỦA LÔ B (bắt buộc kiểm trước khi gán)

| PMID | Bẫy | Dùng cho |
|---|---|---|
| 11223388 | betaine = **GÀ THỊT**, không phải heo | cơ chế hấp thu betaine (bắc cầu) |
| 23246691 | betaine trên **tế bào biểu mô GIÁC MẠC người** — KHÔNG phải ruột | **loại** |
| 32733389 | *Bacillus **clausii*** — không phải *B. subtilis* | sống sót bào tử (chủng khác) |
| 30694101 / 21831748 | *Bacillus **coagulans*** GBI-30 | sống sót bào tử (chủng khác) |
| 38547603 | *B. subtilis* ở **CÁ BƠN** | **loại** |
| 42099934 | Bacillus đa chủng, **GÀ ĐẺ** | **loại** khỏi khối heo |
| 11424701 | dịch **DẠ CỎ bò sữa** | chỉ dùng cho "enzyme bị protease tiêu hoá" |
| 38073487 | **CHUỘT** | cạnh SCFA→Ca, phải ghi rõ loài |
| 16547057 | **CHUỘT** | vòng đời bào tử trong ruột |
| 24795654 | **THẬN** (không phải ruột) | BGT1 → chặng 2/6 của betaine ở thận |
| 39508819 | hệ tế bào **NGƯỜI** | transporter citrate (bắc cầu sang heo) |
| 11195907 | in vitro, dịch **GÀ MÁI** cho phần "digesta supernatant" | phần pepsin/pelleting dùng được, phần digesta phải ghi loài |
| 11424701 / 39522348 / 38670187 / 41716179 / 41202731 / 41543593 / 38227704 / 40729810 | **GÀ** (broiler/layer) | chỉ đối chiếu, không thay bằng chứng heo |
| 41419619 | **bẫy chủng + bẫy tên**: vi nang alginate đa enzyme *B. subtilis* = **protease, lipase, cellulase, amylase — KHÔNG có xylanase**; thí nghiệm **in-vitro**, định hướng thức ăn **GIA CẦM** | chỉ dùng làm tham chiếu **DẠNG BÀO CHẾ**, phải ghi rõ chủng + bộ enzyme. Đã xuất hiện ở CẢ file xylanase lẫn protease trong cùng lượt → dễ bị "tái sử dụng" thành số của xylanase |
| 42514643 / 42736212 / 42514119 | enzyme/thuỷ phân trên **GÀ BROILER** | loại khỏi khối heo |
| 41939266 | xylanase (?), **GÀ ĐẺ** | loại |
| 42795684 | **CÁ HỒI** rainbow trout (định giá phụ phẩm tảo) | loại |
| 42749412 | phytase khai thác genome từ **PHÂN NGỰA** | loại |
| 42636573 | phytase + lên men sorghum, **VỊT THỊT** | loại |
| 34225796 / 32403458 | tinh dầu oregano **gà đẻ** / curcumin — trả về khi tìm `microencapsulated phytase AND pig` | loại (sai chất **và** sai loài) |
| 41657984 / 41283320 | xylanase metagenome suối nước nóng / endoxylanase *C. acetobutylicum* cho XOS từ **lignocellulose công nghiệp** | loại (không phải dinh dưỡng heo) |
| 39682426 | **β-mannanase** (không phải xylanase) | loại khỏi khối xylanase |
| 42602577 / 42360547 | L-lysine vi nang **gà broiler** / protein động vật chế biến **gia cầm** | loại |
| 42598592 | protease ở đây là **CÔNG CỤ** vi nang hoá carvacrol, không phải nguyên liệu | loại |
| 40002107 / 41409194 | glucose oxidase / whey peptide cho đồ uống thể thao | loại |
| 42714699 | nấm men + tannin + enzyme amylolytic trên **CỪU** | loại |
| 42511011 / 41301996 | enzyme **XỬ LÝ TRƯỚC** nguyên liệu (đùn + thuỷ phân khô dầu hạt cải; sấy khô dầu đậu **đã xử lý enzyme**) | loại khỏi khối "enzyme TRỘN vào cám" — khác hẳn về mặt công thức |
| 42221496 / 42795656 | probiotic / nấm men trả về khi tìm `phytase AND simulated gastric fluid` | loại (sai chất) |

**Luật rút ra cho lô này:** ở nhóm enzyme/vi sinh, nguồn GÀ nhiều hơn heo rất nhiều ⇒ cột "mô & loài" phải
ghi `GÀ` ở mọi dòng dùng nguồn gia cầm; và các ca "cùng chi, khác loài" (*B. clausii*, *B. coagulans*,
*B. safensis*) **không** được gán cho *B. subtilis* — đây là **lớp 3 (sai chất anh em)** ở cấp loài/chủng.

---

## 4. TƯƠNG TÁC NỘI CÔNG THỨC (`tuong_tac`, bắt buộc cho mọi nguyên liệu lô này)

- **Betaine HCl + enzyme (tải acid):** betaine HCl 1.500 mg hạ pH dạ dày 4,5 đơn vị (`23980906`); acid citric
  cũng hạ pH khẩu phần + dịch dạ dày (`9690644`) ⇒ trong cùng premix đây là **cộng dồn acid**, và theo
  `42462087` giảm ABC 40–50 meq/kg **vẫn không đủ** hạ pH dịch dạ dày ⇒ đừng hứa "hạ pH để enzyme hoạt động".
- **Acid citric × phytase:** **KHÔNG synergy trên heo** (`9690644`); acid hữu cơ giúp phytate-P rõ ở **GÀ**
  chứ không phải heo (`10764076`) ⇒ ghi là "lợi riêng, không cộng hợp".
- **Acidifier × multienzyme (HEO):** `40433456` — 240 heo cai sữa, khẩu phần SBM cao + multienzyme ± acidifier:
  ↑ADG pha 2 ~12,5 % (xu hướng), ↓tiêu chảy, ↑AID AA (trừ Gly, Pro) ⇒ **dùng được** làm nguồn "phối hợp enzyme
  + acidifier có lợi" trên heo.
- **Acidifier × butyrate bao:** `40233213` — 315 heo nursery, canola meal 40 %: acidifier ↑BW cuối + ADG; phối
  **acidifier + encapsulated butyrate** ↓khối lượng ruột già, ↑*Lactobacillus amylovorus* manh tràng.
- **Tanin × enzyme (HEO):** `37100756` — dịch tiêu hoá heo mô phỏng: tanin sorghum (30 mg/g) giảm tiêu hoá
  **bởi pepsin và pepsin-pancreatin**; `36075205` — sorghum tanin cao giảm tiêu hoá DM/GE/CP; `33105748`
  chestnut+quebracho 120 heo con cai sữa. ⇒ nguồn cho luật "tanin kết tủa protein/enzyme".
- **Berberine / thảo dược × *Bacillus* (ức chế chéo, có định lượng):** `22878842` — **20 µg/mL berberine KÍCH
  THÍCH *B. subtilis* nhưng ỨC CHẾ *E. coli*; trên 100 µg/mL mới ức chế *B. subtilis*; *E. coli* làm GIẢM sức
  chịu berberine của *B. subtilis*`; `26636757` — 25 µg/mL berberine + 20 µg/mL INF55 (ức chế bơm) chặn **~99 %**
  tạo khuẩn lạc từ bào tử *B. subtilis*, còn **200 µg/mL berberine một mình KHÔNG có tác dụng** (bào tử chủ
  động tống ra); `35303184` — carvacrol 25 µg/mL là **chất ức chế bơm thải yếu** ở *B. subtilis*; `36786641` —
  berberine ức chế **MdfA** (MFS) của *E. coli*.
- **Ca × phytase:** `8463857` (Ca 4,5→15 g/ngày đẩy phân giải phytate toàn ống 97→42 %) + `20836179`
  (Ca cao giảm hydrolysis in vitro) ⇒ cặp tương tác mạnh nhất trong lô.
- **Sinh khả dụng tổng:** `42510536` (review 2026) — butyric acid có hạn chế mùi + hiệu suất hấp thu thấp nên
  phải dùng dạng bền: sodium butyrate, coated butyrate, butyrate glycerides.

---

## 5. KHUNG 8 CHẶNG ÁP CHO CHẤT **KHÔNG** HẤP THU (enzyme / bào tử vi sinh)

Khi vật chủ là HEO mà chất là enzyme hoặc vi sinh, phần lớn chặng là **KHÔNG** — và cái phải ghi rõ là
**"vào" nghĩa là gì**. Bản đồ đã kiểm:

| Chặng | Enzyme (phytase/xylanase/protease) | *B. subtilis* bào tử |
|---|---|---|
| 1 `cua_vao` | Miệng/thức ăn; `first_pass: **không**` — enzyme **không hấp thu nguyên dạng**, tác động trong **lòng ruột** (`12357589`, `20836179`) | Miệng; bào tử đi qua dạ dày nguyên vẹn |
| 2 `qua_hang_rao` | **Không vượt màng** — "vào" = **tiếp cận cơ chất**; điều kiện sống còn = sống sót pepsin + pH dạ dày (`25562369`, `11195907`, `20836179` giữ 76–80 %) | **Nảy mầm ở RUỘT NON** — đo trên người từ **3 h ở hồi tràng** (`34408741`), `16547057` (chuột), `22968412` (8 %), `34925306` (**L-alanine**, theo chủng) |
| 3 `gan_lan_dau` | **KHÔNG** (không CYP; hoạt tính đo trong chyme chứ không trong tuần hoàn — `12357589`) | **KHÔNG** |
| 4 `gan_de_di` | **KHÔNG** liên hợp, **KHÔNG** protein chở | **KHÔNG** |
| 5 `toi_mo` | Đích = **CƠ CHẤT TRONG THỨC ĂN**: phytate/InsP6 (`31769698`, `8463857`) · arabinoxylan (`29766982`) · protein khẩu phần (`39506561`) | Niêm mạc ruột + hệ vi sinh: ↓IL-8, ↑MUC-1/occludin/TJP-1 (`36949225`), ↓E. coli/coliforms (`35158640`, `37583344`) |
| 6 `ra_khoi_te_bao` | **KHÔNG áp dụng** — không có tế bào đích. P vô cơ giải phóng được hấp thu qua NaPi-IIb ở ruột non: **CHƯA CÓ NGUỒN (tag H)** cho heo | **KHÔNG áp dụng** (tag H) |
| 7 `thai` | **PHÂN** (enzyme bị tiêu hoá thành acid amin; P dùng rồi thải theo phân — P phân ↓13–33 % `9795986`; phân giải phytate toàn ống gần 100 % `12357589`). **Sữa: tag H** | **PHÂN** — bào tử đào thải theo phân; *"sữa"* chỉ có **gián tiếp** (sữa đầu ↑protein + IgM ở nái được bổ sung — `39965290`), **không** phải vi khuẩn vào sữa |
| 8 `o_lai` | **t½ = độ bền trong đường tiêu hoá + nhiệt ép viên**: T½ 1 h ở 70 °C (`40655371`); 53 % P tự do sau ép 84 °C (`9795986`); ~70 % vs ~30 % ở conditioner 70 °C (`11195907`); coating giữ tốt hơn khi TỒN TRỮ (`21890502`) — và `23148255` cho thấy **coating KHÔNG tạo khác biệt bioefficacy sau ép viên 80/90 °C** | Tồn tại dưới dạng bào tử; sống sót dịch vị 70–100 % (`21831748`, `22968412`, `32733389`) |

**Ba khoá đời của lô này:**
- `bat_kha`: phytase **không** hấp thu, **không** vào máu/sữa; enzyme **không** cứu được khẩu phần thiếu Ca/P
  đúng mức; xylanase **không** cải thiện tăng trưởng trong 2 thí nghiệm heo lớn (`39595308`, `29508681`);
  citric acid **không** cải thiện ADG heo cai sữa (`3198539`); *B. subtilis* **không** thay được ZnO ở heo con
  (`36949225`).
- `da_that_bai`: `29508681` (32.000 BXU/kg, không hiệu quả), `3198539` (citric acid không hiệu quả), `10764076`
  (citric acid nhỏ hơn nhiều ở heo so gà), `23148255` (coating không tạo khác biệt sau ép viên),
  `22878842`/`26636757` (berberine không diệt được bào tử *B. subtilis* khi bơm còn hoạt động).
- `chi_dau_do_duoc`: AID/ATTD của P (`31769698`, `41813752` AID P 47→70 %), độ nhớt dịch ruột (`29766982`
  2,9→2,5 cP), ATTD NDF/ADF (`39595308`), tỉ lệ tiêu chảy/phân điểm, G:F, MCT1 mRNA ở hồi tràng (`20050950`),
  pH dịch dạ dày (`42462087`, `9690644`), ABC/ABC-4 khẩu phần (`39935381`), lactulose:mannitol nước tiểu
  (`26491121`).

### 2.9 BỔ SUNG 20/10/2026 — *B. subtilis* + calcium butyrate (2 chất chốt lô B)

Đi vào `src-b/bacillus-subtilis.txt` (**70 dòng**) và `src-b/ca-butyrate.txt` (**77 dòng**), cả hai 8/8 khối.
~41 PMID mở `abstractText` thật trong lượt. Trùng §2.4/§2.5 thì KHÔNG lặp lại; dưới đây chỉ là phần MỚI.

**Bacillus subtilis — bổ sung §2.4**

| PMID | Số liệu thật | Mức | Mô & loài (chủng) |
|---|---|---|---|
| 34071231 | BioPlus YC **400 g/tấn**, 83.838 heo vỗ béo / 4 đợt: B. subtilis đếm được ở **NIÊM MẠC + CHẤT CHỨA ĐẠI TRÀNG/TRỰC TRÀNG** (cao hơn đối chứng); Enterobacteriaceae/Enterococcus/Clostridium ↓, LAB ↑ | A | HEO — DSM 5750 (+ DSM 5749) |
| 35630380 | ức chế bám *E. coli* K88/ETEC + *Salmonella* Typhimurium trên **IPEC-J2**, trước/đồng/sau xử lý. ⚠️ thí nghiệm có **cả** *B. licheniformis* ⇒ phải ghi rõ | R | IPEC-J2 — biểu mô ruột non HEO |
| 42651854 | **59 chủng** Bacillus phân lập từ GIT heo; chủng tốt nhất bám niêm mạc mạnh + sống qua pH acid/muối mật; **4 cụm gen: surfactin · fengycin · bacillaene · subtilosin A** | R | GIT HEO → in-vitro (1BP1Co1) |
| 42240379 | **C17 fengycin B** là phân tử ức chế ETEC; **có ở DB9011, KHÔNG có ở chủng tham chiếu NBRC13719**; tăng cường khi phối colistin | R | dịch nổi DB9011 vs ETEC phân lập heo |
| 39203378 | 6,5×10⁸ CFU/kg cám, 480 heo 8,13 kg: **VH hỗng tràng ↑ p<0,01**, **crypt hồi tràng ↓ p<0,05**, tế bào hình đài ↑, occludin ↑ | A | hỗng tràng + hồi tràng HEO |
| 34473279 | **2×10⁹ CFU/kg thể trọng/ngày** heo sơ sinh IUGR: VH/CD hỗng tràng ↑ p<0,05, **DAO huyết tương ↓**, ZO-1/occludin/claudin-1 ↑ | A | hỗng tràng HEO sơ sinh |
| 40431582 | nái ăn 35 ngày cuối thai kỳ: heo con **VH + crypt hỗng tràng ↑**, tế bào hình đài ↑, MUC2/Lyz-1 ↑, IL-4/IFN-γ/CD3⁺ T | A | hỗng tràng heo con (B.S-Dia) |
| 41976011 | nái + heo con: **MUC2 ↑ + sIgA ↑**, *Lactobacillus* ↑, ***C. perfringens* type A ↓**, CRP/IL-1β/IFN-γ ↓ ⇒ nguồn chính cho nhánh (d) miễn dịch niêm mạc | A | ruột + niêm mạc nái (PB6) |
| 36548829 | sIgA hỗng tràng + kết tràng ↑, host defense peptides ↑ | A | ruột HEO |
| 37630670 | *Listeria* **gan −67 %, lách −49 %** (p<0,001) — thuần MIỄN DỊCH, **KHÔNG phải vi khuẩn có mặt ở gan** ⇒ dòng dễ viết sai nhất của chất này | A | gan + lách heo 3 tuần (MB40) |
| 41316334 | 10⁹ CFU bào tử/kg cám: sIgA, ZO-1, occludin, hệ vi sinh | A | ruột heo con |
| 42450761 | tổng quan hệ thống PRISMA/PICOS: **619 bản ghi 2000–2025 / 29 nghiên cứu** ⇒ đáp ứng phụ thuộc chủng + liều + khẩu phần + thiết kế (`BAT_KHA`) | A | HEO cai sữa |
| 36077989 | meta heo vỗ béo: liều trung vị **486 mg/ngày** | A | HEO |
| 41295738 | chất chuyển hoá probiotic nguồn heo = **SCFA + bacteriocin + exopolysaccharide**; ADG +18–22 %, F:G −12–15 %, tiêu chảy ↓40–45 % ⇒ neo cho nhánh (c) acid hữu cơ | R | review HEO |
| 35197953 · 41472814 · 36417387 | Bacillus ở heo/gia cầm; **bào tử bền qua chế biến cám + dạ dày/muối mật rồi nảy mầm** ⇒ luận cứ kỹ thuật cho dạng bào tử; tuyển chọn chủng sinh surfactin + cảnh báo nhạy cảm kháng sinh | R | review |
| 42324599 | đột biến `sinR` tăng biofilm ⇒ sống sót vượt trội qua dịch dạ dày/mật + bám nhiều hơn. **Chỉ dùng cho "sống qua dạ dày", ghi rõ mô hình** | A | **C. elegans** — KHÔNG phải heo |

**Calcium butyrate — bổ sung §2.5**

| PMID | Số liệu thật | Mức | Mô & loài |
|---|---|---|---|
| 34359944 | MCT1 + SMCT1 hấp thu → **β-oxy hoá NHANH để sinh năng lượng cho colonocyte**; **butyrate paradox** (tăng sinh ngược chiều ở tế bào biệt hoá vs chưa biệt hoá); HDAC/histone | R | biểu mô đại tràng (chủ yếu người/dòng tế bào) |
| 41596106 | **MCT1 (SLC16A1) + SMCT1 (SLC5A8)** = hấp thu; **BCRP (ABCG2) + MCT4 (SLC16A3)** = ĐẨY RA ⇒ nguyên liệu **hiếm hoi của lô B có dữ liệu BƠM RA thật** (chặng 6 KHÔNG phải tag H). Điều hoà bởi stress oxy hoá/viêm: "scarce and inconsistent" | R | biểu mô đại tràng |
| 41643415 | NÁI NaB 0,2 % ngày 30–114 thai kỳ: heo con cai sữa **VH hỗng tràng ↑ + VH/crypt ↑ p<0,05**, khối lượng tương đối hỗng tràng ↑; claudin-1 ↑; **GPR41/FFAR3 ↑**; IL-6/TNF-α/MDA ↓. ⚠️ CYP1A1 mRNA **nhau thai** chỉ là **xu hướng p = 0,051** — KHÔNG phải gan | A | hỗng tràng heo con (nái Landrace × Yorkshire) |
| 38789563 | 180 heo 21 ngày / 5,17 kg, 24 ngày: **VH hồi tràng ↑**, mảng Peyer ↓, **mRNA MCT1/SGLT1/PepT1 ↑** hỗng tràng, OCL/ZO-1/GPX/SOD ↑ | A | hồi tràng + hỗng tràng HEO |
| 42510536 | acid butyric tự do = **"pungent odor" + "low absorption efficiency in the digestive tract"** ⇒ LUẬN CỨ GỐC cho **mùi** và lý do phải dùng dạng muối/bao (sodium butyrate · coated butyrate · butyrate glycerides) | R | heo con cai sữa (review) |
| 42791758 | vật liệu mang bảo vệ hoạt chất khỏi phân huỷ khi chế biến/thông qua ống tiêu hoá + **điều hoà động học NHẢ**; có in-vitro tiêu hoá mô phỏng | R | nhiều loài — gồm HEO |
| 39795009 | **muối butyrate = lợi ích TỨC THÌ; prebiotic/probiotic = sản xuất butyrate BỀN VỮNG** ⇒ câu chốt cho `TUONG_TAC` Ca-butyrate × *B. subtilis* | R | heo cai sữa |
| 40557239 | uống butyrate **có thể tăng butyrate tuần hoàn**; "butyrate kinetics and dynamics remain poorly understood" ⇒ lý do chính đáng để `t½` = tag H | R | review (đa loài) |
| 40518439 | 300 heo 5,5 kg, mono-tributyrin: **butyrate MANH TRÀNG ↑ p<0,05**, G:F ↑, hematocrit/hemoglobin ↑ | A | chất chứa manh tràng HEO |
| 36161319 | 32 heo DSS + TBCD 8,3 g/kg sữa: butyrate **manh tràng + đại tràng gần ↑ p<0,05**, niêm mạc đại tràng xa dày lên; **TBCD lại làm tăng cân KÉM** | A | manh tràng + đại tràng heo |
| 35573094 | NH3 · butyrate · acetate · H₂S · p-cresol tác động lên **chuyển hoá NĂNG LƯỢNG của tế bào biểu mô đại tràng heo** ⇒ hiệu quả butyrate phụ thuộc **NỀN KHẨU PHẦN** (protein thô cao = đối kháng) | R | niêm mạc + crypt + colonocyte **HEO** (ex-vivo) |
| 34681598 | **PHẢN CHỨNG trung thực**: trên tế bào nuôi cấy butyrate **KHÔNG bị oxy hoá** mà làm tăng dòng pyruvate vào ty thể + tích tụ giọt lipid; chặn MPC thì mất tác dụng | R | **HT29 + Caco-2 = dòng ung thư đại tràng NGƯỜI** |
| 40635319 | **Ca-butyrate đúng muối canxi**: trẻ 4–17 tuổi IBS, n=51, **500 mg/ngày × 8 tuần** (NCT04566679): thành công **73 % vs 3,8 % placebo** (p<0,0001); **giữ hiệu ứng sau 4 tuần washout** | I | đường tiêu hoá + phân NGƯỜI |
| 38473146 | phối **acid hữu cơ + tinh dầu** thay kháng sinh sinh trưởng ⇒ neo cho `TUONG_TAC` với Lô A | R | heo |

**Bẫy loài/chủng của 2 chất này — verify 33/33, KHÔNG dùng cho phát biểu heo:**
*B. subtilis:* 42510706 (gà broiler) · **41008601 + 42123979 (*Alkalihalobacillus clausii*)** · 42806832
(*B. coagulans* + *L. acidophilus*) · **41597768 + 40572135 + 42278110 (*B. velezensis*)** ·
42736181 + 42634836 + 42061257 (gia cầm) · 42514093 (B. subtilis M2 ở **gà mái đẻ**) · 41466115
(*Apis mellifera*) · 42104959 (bào tử display kháng nguyên PRRSV ở **chuột**) · 42221496 (meconium **người**) ·
40678151 (B. subtilis hoang dã niêm mạc **mũi chuột**).
*Ca-butyrate:* 39923452 + 39447330 (gà broiler + phytase) · 38362518 (gà mái đẻ) · **37727053 (chim cút Nhật
— dính đúng bẫy betaine gia cầm cũ)** · 37796385 (bê Holstein bao) · IND607138702 (cừu non) · 42655764
(bồ câu) · 40861197 (*Penaeus vannamei*) · 41856080 (cừu, rumen) · 40876116 + IND609297823 (meta gà broiler) ·
42736188 (gà broiler *Salmonella*) · 40681595 (gà broiler NaB vs tributyrin) · 41547414 (chuột đột quỵ) ·
**41628665 (Ca-butyrate nhả chậm ở người — đích là KHỚP bàn tay, không phải ruột)** · 42791718 (heo Tây Tạng,
khác chủ đề). **38892647 = butyrate NỘI SINH từ xơ dinh dưỡng ở heo con** — xoá khỏi mọi phát biểu về
butyrate NGOẠI SINH dù nó đúng loài.

**4 luật rút ra của lượt 20/10 (tái dùng cho mọi lô sau):**
1. **`sort=relevance` trả bài MỚI, không phải bài ĐÚNG.** Với yêu cầu "ưu tiên HEO", truy vấn trần chôn bài
   heo in-vivo dưới review 2025. Dùng **loài trong ngoặc** + **trường title**:
   `"<chất>" (pig OR piglet OR swine OR porcine)` · `TITLE:"calcium butyrate"` ·
   `TITLE:butyrate AND (pig OR piglet OR swine) AND (villus OR crypt)`. Chính 2 truy vấn sau tìm ra
   `34237915` và `42510536` — thứ mà truy vấn thường **không** bao giờ trả về.
2. **Tìm theo CẶP ghép lô, không chỉ từng chất.** Nguồn quyết định cho `TUONG_TAC` Lô A × Lô B chỉ lộ ra khi
   truy vấn chính cặp đó (`calcium butyrate` **và** `tannin`).
3. **Với vi sinh, chặng 6 và 8 KHÔNG tồn tại về cơ chế** — ghi `CHƯA CÓ NGUỒN (tag H)` kèm 1 câu nêu LÝ DO,
   đừng suy diễn. Và phân biệt **bơm xuất bacteriocin của VI KHUẨN** với **bơm ABC của tế bào ruột HEO**;
   gán lẫn hai cái là lỗi mô. Ngược lại, **calcium butyrate CÓ bơm ra thật** (`41596106`) — đừng mặc định
   cả lô là tag H.
4. **Loài anh em cấp CHỦNG là lớp bẫy thứ ba** (*B. clausii* · *B. coagulans* · *B. velezensis* ·
   *Alkalihalobacillus clausii*) — grep tên loài trong **title** trước khi đọc abstract, và **ghi chủng ở
   MỌI dòng** của chất vi sinh.
