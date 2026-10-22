# Lô A premix heo — berberine · hoàng liên · ích mẫu (khung 8 chặng)

Nguồn: fixgby `docs/10-cong-thuc-23/src/{berberine,hoang-lien,ich-mau}.txt`, 19/10/2026.
**42 PMID, verified 42/42 tồn tại + 42/42 đã đọc `abstractText` thật** (`_verify.py` + `_epmc.py a`).
Mọi số dưới đây đều lấy từ abstract đã đọc, không phải từ title.

Bối cảnh sản phẩm: premix trộn cám heo, 2 kg/lô, 5 kg/tấn cám → 400 kg cám/lô.
Đích cuối là người, bước đệm là HEO ⇒ ưu tiên bằng chứng trên heo/lợn.

---

## 0. Ba kỹ thuật rút ra từ lô này (đã đưa vào SKILL.md)

1. **Cache JSON dùng chung + 2 tool-call song song = cache hỏng** (`Extra data: line 4223`). Chạy tuần tự.
2. **Spec khoá (`S_THAI_TY_LY`) ≠ builder `SCALARS` (`S_THAI_TY_LE`)** ⇒ builder exit 0 mà field rỗng.
   Phát **cả hai** khoá; assert scalar non-empty sau build.
3. **`sort=''` cho truy vấn PK, `CITED desc` cho tổng quan**; search n=20–25 rồi lọc abstract tại chỗ
   theo `(từ khoá PK) AND (\d)`, in **câu** chứ không in cả abstract.

---

## 1. Berberine (berberine chloride)

| điểm | số | PMID | mô & loài |
|---|---|---|---|
| Sinh khả dụng uống tuyệt đối | **0,26 %** | 37914368 | chuột cống (10 mg/kg PO vs 1 mg/kg IV) |
| Sinh khả dụng uống tuyệt đối | **0,37 ± 0,11 %** | 33584274 | chuột cống (48,2 / 120 / 240 mg/kg PO vs 4,0 mg/kg IV) |
| Sinh khả dụng uống | **0,68 %** | 42653808 | chuột cống (review) |
| Sinh khả dụng TRỰC TRÀNG | **17,0 % / 24,3 % / 12,3 %** (1/3/10 mg/kg) | 37914368 | chuột cống |
| OCT1 (SLC22A1) | **KM 7,0 µM; CLint 306 ± 29 µL/min/mg**; allele *3–*6 giảm uptake ≥65 %; Oct1/2-KO AUC gan **3,2×** | 39488825 | tế bào người in-vitro + chuột nhắt KO |
| OCT1 ở người | kiểu gene giảm chức năng **KHÔNG** đổi PK berberine | 39488825 | huyết tương người (NCT05463003) |
| Pha I | CYP2D6 chính → CYP1A2 > 3A4 > 2E1 > 2C19 | 21787170 | HLM + gan chuột nhắt |
| 4 chất pha I | berberrubine (M1), thalifendine (M2), demethyleneberberine (M3), jatrorrhizine (M4) | 21569619 | gan chuột cống + CYP tái tổ hợp người |
| Pha II | **glucuronide + sulfate**; AUC0-48h pha II **>** pha I ⇒ dạng liên hợp là dạng lưu hành chính | 33584274 | huyết tương chuột cống |
| 6 chất liên hợp | M4 jatrorrhizine-3-O-GlcA · M5 jatrorrhizine-3-O-sulfate · M6 thalifendine-10-O-GlcA · M7 berberrubine-9-O-GlcA · M8 demethyleneberberine-2-O-sulfate · M9 demethyleneberberine-2-O-GlcA | 33584274 | chuột cống |
| Cân bằng khối lượng | tổng thu hồi (nước tiểu + mật + phân) **41,2 %** liều; **18,6 %** liều ở PHÂN dạng berberrubine | 33584274 | chuột cống 48,2 mg/kg |
| t½ | **5,77 h** (MRT 20,74 h) | 42228594 | huyết tương chuột cống |
| Phơi nhiễm tuyệt đối | Cmax **12,32 ng/mL**; AUC0-8 **68,28 ng·h/mL** ở liều **200 mg/kg** | 42367479 | chuột cống |
| HEO — chuyển hoá | heo con ăn **30 mg/kg cám** 14 ngày → định lượng được BBR + chất pha I **và** pha II trong **dịch ruột + huyết tương** | 40867778 | HEO CON cai sữa (60 con, 4 tuần) |
| HEO — niêm mạc | **50 mg/kg cám**, 28 ngày: VH p=0,026; VH/CD p=0,002; goblet p=0,023; crypt p=0,022; TJP1 p=0,031; MUC2 p=0,045; AQP1 p=0,019; AQP8 p<0,001; AQP10 p=0,018; AQP11 p=0,004; **SLC9A3 p<0,001**; **SLC12A2 p=0,018**; ADG p=0,024; ADFI p=0,020; tiêu chảy p=0,003 | 41716830 | NIÊM MẠC HỖNG TRÀNG HEO CON (90 con) |
| HEO — vi sinh | tăng Bacteroidota hỗng tràng | 41716830 | HEO CON |
| HEO — BBR + ellagic acid | 10 mg/kg BW + 10 mg/kg EA, 14 ngày: tăng Lactobacillus, Phascolarctobacterium, Parabacteroides; tăng propionate/butyrate | 37317228 | HEO CON (63 con Landrace × Yorkshire) |
| HEO — DON challenge | 40 mg/kg BBR + 4 mg/kg DON, 21 ngày: tăng ZO-1/Occludin/Claudin-1 ở hồi tràng + hỗng tràng; giảm ERK/JNK/NF-κB | 34358871 | HEO CON (180 con) |
| **Cơ chế hấp thu then chốt** | vi sinh ruột khử BBR → **dihydroberberine (dhBBR)**, hấp thu **gấp 5 lần** BBR; dhBBR tự oxy hoá ngược lại thành BBR trong mô ruột; **kháng sinh làm mất chuyển hoá này và giảm BBR trong máu** | 26174047 | chuột KK-Ay + vi sinh ruột |
| Bơm đẩy | **P-gp (ABCB1) thải BBR**; ức chế P-gp (P85 + tween 80) làm tăng AUC | 32957491 | chuột cống 50 mg/kg |
| Bơm đẩy (trực tiếp) | BBR bị P-gp đẩy trong **túi ruột chuột** và **MDCK-MDR1** | 34552326 | MDCK-MDR1 + Caco-2 + túi ruột chuột |
| BBR **ức chế** bơm | ức chế BCRP (ABCG2) → AUC rhein **~2×** | 41901337 | chuột cống + MDCKII-BCRP |
| BBR **ức chế** P-gp | cao Oregon grape 0,1–1 mg/mL ức chế efflux digoxin/CsA theo bậc liều | 38304488 | Caco-2 + LS-180 (dòng ung thư đại tràng NGƯỜI) |

**Câu chốt cho chặng 6 (phân biệt rất dễ lẫn):** berberine **VỪA là cơ chất VỪA là chất ức chế** P-gp và BCRP.
Đây là ngoại lệ của luật "chặng 6 trống" — phải viết rõ hai chiều, không được chỉ ghi "bị bơm thải".

---

## 2. Hoàng liên (thân rễ *Coptis chinensis* / *C. teeta*) — dược liệu THÔ

Khác berberine ở 3 điểm: (a) nhiều alkaloid cùng lúc, (b) có polysaccharide, (c) ma trận dược liệu
quyết định hấp thu. **Không được suy số của berberine tinh khiết sang dược liệu thô mà không ghi rõ.**

| điểm | số | PMID | mô & loài |
|---|---|---|---|
| Loài | *C. chinensis* có tổng alkaloid và **berberine + palmatine cao hơn rõ** *C. teeta* và *C. deltoidea* ⇒ phải chuẩn hoá theo lô | 39701727 | rhizome 3 loài (widely-targeted metabolomics, 658 chất) |
| Chất đánh dấu | 10 alkaloid định lượng trên 4 loài; **jatrorrhizine, columbamine, magnoflorine** là chất khác biệt giữa loài; vị đắng tương quan **berberrubine**; vị chát tương quan coptisine/epiberberine/berberine/palmatine | 39574447 | rhizome 4 loài *Coptis* |
| PK toàn cao | 5 alkaloid (BBR, jatrorrhizine, palmatine, epiberberine, coptisine) + **7 chất chuyển hoá** định lượng in vivo | 34111890 | huyết tương chuột cống |
| Pha II | **dạng tồn tại in vivo LÀ chất liên hợp pha II, chủ yếu glucuronidation** (không phải aglycone) | 34111890 | huyết tương chuột cống |
| 5 chất liên hợp | jatrorrhizine-3-O-GlcA · thalifendine-10-O-GlcA · berberrubine-9-O-GlcA · demethyleneberberine-2-O-sulfate · demethyleneberberine-2-O-GlcA | 34111890 | chuột cống |
| Phân bố mô | **Kp mô/huyết tương > 1** với BBR, palmatine, coptisine; phơi nhiễm **cao nhất ở mô dạ dày–ruột** (thấm trực tiếp qua niêm mạc); ngoài GI thì **BBR và coptisine vào GAN mạnh**, ít bị trạng thái bệnh làm đổi | 40089197 | chuột cống (Zuojin Pill; DESI-MSI dạ dày + gan) |
| HEO | **lợn mini Bama** uống Baitouweng thang (có hoàng liên): coptisine, berberine, columbamine, phellodendrine, obacunone đều **Cmax THẤP**; LLOQ 0,60–2,01 ng/mL; 11 hoạt chất | 38766522 | huyết tương LỢN MINI BAMA |
| Hấp thu phụ thuộc ma trận | 5 alkaloid hấp thu tốt hơn khi ở viên Shuanghua Baihe so với cao Rhizoma Coptidis đơn | 28871816 | chuột cống (túi ruột lật ngược) |
| Kháng khuẩn | cao *C. chinensis* mạnh nhất trong **20 dược liệu** thử trên **14 chủng ESBL-Enterobacterales** (7 loài); berberine là hoạt chất chính, phytochemical khác cộng lực; UAE tăng hiệu suất alkaloid 80,9 %, berberine 75,4 % | 41302392 | chủng phân lập lâm sàng (KHÔNG phải heo) |
| MIC | 4 protoberberine alkaloid (epiberberine, jatrorrhizine, BBR, coptisine) với *M. hyopneumoniae* ES-2: **MIC 8–32 µg/mL** | 41575198 | in-vitro + HEO lai Chang Da (mô hình thử thách bệnh — KHÔNG dùng làm claim) |

### ⚠️ Tương tác QUYẾT ĐỊNH cho công thức: Coptis × Cam thảo (glycyrrhizin)

`32087732` — chuột nhắt ICR, dịch chiết nước, berberine làm marker PK:

| chỉ số | không có cam thảo → có cam thảo | giảm |
|---|---|---|
| AUC tuần hoàn CỬA | 425,8 → **270,4** ng·h/mL | ~36 % |
| AUC GAN | 29.500,8 → **15.422,4** ng·h/mL | ~48 % |
| Cmax cửa | 104,3 → **76,5** | ~27 % |
| Cmax gan | 4.926,1 → **2.642,8** | ~46 % |
| lượng berberine chiết được | −**32 %** | |
| độ tan berberine | còn **34,7 %** so với control | |
| hoà tan 15 phút | **88,7 % → 66,1 %** (đệm acid) · 68 % → 51,8 % (đệm phosphate) | |

Cơ chế: **tạo tủa (sediment)** ⇒ giảm chiết, giảm tan, giảm hoà tan.
**Hệ quả cho premix:** batch A có `glycyrrhizin` ⇒ nếu ghép hoàng liên với cam thảo trong cùng premix
thì phần lớn berberine có thể mất trước khi tới ruột. **Phải tách bao/granulation hoặc kiểm tra lại liều.**
Đây là con số mạnh nhất trong cả lô — dùng làm ví dụ chuẩn cho "tương tác nội công thức".

---

## 3. Ích mẫu (*Leonurus japonicus* Houtt.) — dược liệu THÔ, phần trên mặt đất

| điểm | số | PMID | mô & loài |
|---|---|---|---|
| Chất đánh dấu | **leonurine, stachydrine (= proline betaine), trigonelline** — 3 alkaloid được đề xuất làm Q-marker | 35272128 | huyết tương chuột cống |
| Độ phức tạp | **131 thành phần** in vitro; **21 chất nguyên vẹn** hấp thu + **72 chất chuyển hoá** in vivo | 35272128 | chuột cống |
| Sinh khả dụng leonurine | **F(PO) = 0,14 %**; **F(IP) = 66,6 %**; **CL = 152 mL/min/kg**; **t½ = 2,48 h** (IV) | 42357401 | huyết tương chuột cống |
| Thải | thu hồi leonurine **NGUYÊN VẸN** ở nước tiểu + phân **< 6 %** liều ở CẢ 3 đường (IV/PO/IP) ⇒ **thải qua CHUYỂN HOÁ, không qua thận dạng nguyên chất** | 42357401 | nước tiểu + phân chuột cống |
| Pha II | **12 glucuronide + 12 sulfate**; tổng **30 thành phần** liên quan leonurine, **24 chất chưa từng công bố** | 42357401 | chuột cống |
| Bước biến đổi đầu | **THUỶ PHÂN CẮT LIÊN KẾT ESTER** (không phải oxy hoá CYP); mảnh thuỷ phân sau đó mới bị liên hợp | 42357401 | chuột cống |
| Ruột | leonurine tăng **claudin-1 + occludin**, giảm **TNF-α + IL-1β**, cải thiện tính thấm ruột | 41079267 | KẾT TRÀNG CHUỘT NHẮT |
| Vi sinh | giảm Rikenellaceae_RC9, UBA1819, *Enterococcus*, *Oscillibacter* | 41079267 | chuột nhắt |
| Tử cung — coumarin | 8 coumarin trên **mảnh cơ tử cung chuột cống KHÔNG MANG THAI**: **bergapten** tăng Ca²⁺ nội bào (kênh Ca²⁺ type L + thụ thể α); **osthole** đối kháng α, giảm Ca²⁺, giãn cơ do oxytocin | 39337649 | in-vitro, cơ tử cung chuột cống |
| Tử cung — stachydrine | 10⁻⁶·⁵–10⁻⁴ mol/L ức chế co **47,1 %** (tự phát) / **40,4 %** (oxytocin); đảo ngược bởi **L-NAME** và **indomethacin** ⇒ qua NO + prostaglandin; giảm **COX-2** và **PGF2α**; in vivo 20/10/5 mg/kg | 41296465 | in-vitro + chuột nhắt |

**Điểm phải viết thẳng:** ích mẫu là ví dụ điển hình của **dược liệu KHÔNG hấp thu** — mô đích thực tế khi
cho ăn là **NIÊM MẠC RUỘT + VI SINH RUỘT** (99,86 % liều không vào tuần hoàn), còn tác dụng tử cung chỉ
chứng minh trên chuột. **Không có một nghiên cứu nào trên HEO** (PK, mô, sữa, t½) ⇒ `tag H` toàn bộ phần heo.
Cũng vì tác động tử cung hai chiều ⇒ ghi rõ **không dùng cho nái đang chửa** như một lý do loại trừ an toàn,
không phải claim điều trị.

---

## 4. Bảng nguồn BỊ LOẠI (audit mô/loài) — dùng lại được

| PMID | Vì sao loại |
|---|---|
| 42652033 | **Cortex Phellodendri** (hoàng bá, *Phellodendron*) — KHÔNG phải *Coptis*, dù cùng chứa berberine |
| 42770040 | "compound Chinese herbal preparations" — abstract không nêu thành phần hoàng liên |
| 38136904 | "fermented Chinese herbs" trên heo — abstract không liệt kê ích mẫu (đã đọc abstract để xác nhận) |
| 38587649 | epiberberine ức chế urease vi sinh **DẠ CỎ** — sai loài, không gán cho heo |
| 40536902 | palmatine tiêm bắp ở **GÀ** — sai loài |
| 40527062 | motherwort + oxytocin trên **SẢN PHỤ NGƯỜI** (51.312 ca mổ lấy thai) — không gán cho heo |
| 42394984 | cao ích mẫu trên **CHUỘT VIÊM ĐƯỜNG THỞ** — sai mô đích |
| 39205203 | chỉ network pharmacology + docking (in-silico) |
| 42178826 | chỉ dự đoán ADME in-silico ("renal excretion", "HIA 100 %") — không phải số đo |
| 42367479 | t½ **8,63 h** là của dạng bào chế Metaberine™, KHÔNG phải berberine thường (nhưng Cmax 12,32 ng/mL của berberine thường thì dùng được) |
| 42070023 | tổng quan OCTN1 chỉ xác lập ergothioneine; **KHÔNG** nêu stachydrine ⇒ không được nói stachydrine là cơ chất OCTN1 |
| 36160869 | OATP1B1/1B3 trên tế bào CHO, abstract **không nêu berberine** |
| 38304488 | Caco-2/LS-180 = dòng **ung thư đại tràng người** + **cao rễ Oregon grape**, không phải berberine tinh khiết ⇒ chỉ dùng cho phát biểu "cao chứa berberine ức chế P-gp", không dùng định lượng |

---

## 5. Truy vấn đã hiệu quả (relevance sort)

```
berberine pharmacokinetics oral bioavailability
berberine urinary fecal excretion rats
berberine P-glycoprotein substrate efflux intestinal absorption
berberine organic cation transporter OCT1 SLC22A1 uptake intestinal
berberine bile duct cannulated                     ← lôi ra bài cân bằng khối lượng 33584274
berberine weaned piglets jejunal intestinal barrier
Coptidis Rhizoma pharmacokinetics alkaloids rat plasma
comparative pharmacokinetics berberine palmatine coptisine epiberberine rats
Pharmacokinetic incompatibility of the Huanglian-Gancao herb pair   ← tương tác glycyrrhizin
leonurine pharmacokinetics bioavailability rats
Leonurus japonicus chemical constituents alkaloids stachydrine leonurine
```

Truy vấn **KHÔNG** hiệu quả (trả review/noise): `berberine absolute bioavailability percent rats oral
intravenous`, `berberine mass balance excretion radiolabeled rats recovery`, `Coptis chinensis berberine
content percent rhizome`, `Huanglian Coptis pig feed additive` (0 hit).
