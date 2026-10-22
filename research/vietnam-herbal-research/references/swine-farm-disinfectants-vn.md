# Thuốc sát trùng trại heo (swine-farm disinfectants) — knowledge bank VN

Nguồn verify: 25/09/2026. 30 PMID đã efetch + đọc abstract trong phiên; giá/liều
từ trang nhà cung cấp VN (crawl trực tiếp, HTTP 200). Dùng khi được hỏi về:
sát trùng chuồng trại, NaOH/xút, vôi bột/Ca(OH)2, cơ chế diệt khuẩn-virus,
chi phí tiêu độc theo lứa, ASF/PEDV/PRRS phòng chống bằng hóa chất.

## 1. High-pH — cơ chế + ngưỡng theo nhóm mầm bệnh

**NaOH**: OH⁻ xà phòng hóa lipid màng + thủy phân liên kết peptide (alkaline
hydrolysis) → biến tính protein vỏ/envelope. 1% ≈ pH 13.0; 2% ≈ pH 13.5.

**Ca(OH)2**: CaO + H2O → Ca(OH)2 + nhiệt (slaking, tỏa nhiệt). Dung dịch bão hòa
pH ~12.4–12.6. Tác động = pH cao + hút ẩm/desiccation + nhiệt khi tôi vôi.

| Mầm bệnh | Ngưỡng / thời gian tiếp xúc | PMID |
|---|---|---|
| ASFV (có envelope) | 1% NaOH **hoặc** Ca(OH)2 → diệt trong **150 s ở 4 °C**; 0.5% cần 30 min | 10432596 |
| ASFV trong đất/bùn | 10% vôi (vôi tôi, nước vôi, vôi sống) → **≥4 log**, cả khi tải hữu cơ cao, không phụ thuộc độ ẩm đất (1–10% đã test) | 35458464 |
| ASFV trong đất | Ca(OH)2 **hoặc** citric acid → bất hoạt hoàn toàn | 33238521 |
| ASFV + nhiệt + kiềm + peroxide | 48 °C + pH 10.2 + 20.6–102.9 mM H2O2 / 10 min → 3.35–4.17 log (có plasma); 6.99 log/5 min (không plasma) | 29778187 |
| **SVDV (enterovirus, không envelope)** | 1% NaOH/Ca(OH)2 **KHÔNG hiệu quả** ở 22 °C/30 min; phải **1.5%** mới diệt | 10432596 |
| SVDV + QAC | DDAC + **0.1% NaOH** hiệu quả ở pH ~11, tác dụng sau **1 min**; NaOH một mình vô hiệu | 9192351 |
| PCV2 (không envelope, circovirus) | NaOH giảm 1.61 log ở 30 min/20 °C; NaOCl, KMPS, QAC-aldehyde cũng hiệu quả | 17851101 |
| Salmonella (Gram−) | 0.1–0.2% Ca(OH)2 (pH 12.6) → **>3 log trong 1–3 min**, vẫn hiệu quả với 5% huyết thanh; **150 ppm NaOCl thất bại** | 29944400 |
| Virus không envelope nói chung | cần **pH ~9.5 + 60 °C/10 h** (HAV, SV40, CPV) — pH cao ở nhiệt độ thường KHÔNG đủ | 21333548 |
| FMDV | capsid **acid-labile** (phân ly ở pH acid) → kiềm kém hiệu quả hơn, dùng acid/oxidizer | 29183342 |
| Bào tử | 2% alkaline glutaraldehyde là chuẩn sporicide; NaOH/vôi KHÔNG diệt bào tử đáng tin | 2125592 |

**Ba điểm chết phải nói rõ với người dùng:**
1. **Chất hữu cơ đánh bại kiềm.** 2% NaOH ở pH cao **KHÔNG** diệt được ASFV trong
   huyết-lách giàu protein sau 1 h ở 22–25 °C (PMID 4631432). Phải làm sạch trước.
2. **Độ bền của vôi rất ngắn**: Ca(OH)2 20% trong độn chuồng **mất hiệu lực sau 3 ngày**
   (PMID 28321028) → phải rắc lại ~2 lần/tuần. Vôi là dụng cụ cho nền/lối đi/hố tiêu hủy,
   KHÔNG thay thế sát trùng terminal tường-trần.
3. **Virus không envelope là giới hạn của mọi phương án pH**: phải tăng nồng độ
   (1.5%), hoặc kết hợp QAC, hoặc dùng oxidizer/aldehyde.

## 2. Cơ chế theo nhóm hoạt chất (khuẩn vs virus)

| Nhóm | Diệt khuẩn | Diệt virus | Điểm yếu |
|---|---|---|---|
| Glutaraldehyde / formaldehyde | cross-link protein + alkyl hóa DNA, sporicide | mạnh, **cả không envelope** | kích ứng hô hấp; cần bề mặt sạch; glutaraldehyde phải **alkalin hóa** mới hoạt động (pH 7.5–8.5, PMID 2125592, 6780502) |
| QAC (benzalkonium, DDAC) | cationic surfactant phá màng lipid, rò tế bào chất (PMID 41824921, 27452423) | yếu với không-envelope; **hiệp lực với 0.1% NaOH** | bị chất hữu cơ/nước cứng vô hiệu |
| Peroxide / peracetic (POA) | POA **xuyên màng nguyên vẹn** → oxidative stress nội bào; chlorine thì phá bề mặt + ly giải nhanh (PMID 36995048) | **kém** — chỉ ~1 log cho MS2 và Φ6 sau 30 min | mùi, ăn mòn; PAA bền hơn ở pH acid |
| Chlorine (NaOCl, chloramine, NaDCC) | HOCl oxy hóa –SH, **nhiều đích cấu trúc**: đầu/đuôi phage + vỏ capsid, giải phóng genome (PMID 9871311) | rộng, cả không-envelope | hết tác dụng khi pH >8; bị hữu cơ hấp thụ mạnh; ASFV cần **≥500 mg/L Cl khả dụng** cho >4 log (PMID 41955653) |
| Iodine / PVP-I | oxy hóa –SH, tyrosine | rộng nhưng **hiệp lực mới mạnh**: 0.13% iodine phức hợp (0.0065% I hiệu dụng) diệt hết 10⁴ TCID50 ASFV; 1.0% cho 10⁶ (PMID 35588273) | **PVP-I thường KHÔNG giảm PCV2** (PMID 17851101) |
| Phenolic | hấp phụ–bất hoạt protein (PMID 5657532, 14123964) | mạnh với **có envelope** (1% o-phenylphenol diệt ASFV trong 60 min, kể cả trong huyết, PMID 4631432; >4 log ASFV 4–20 °C, PMID 37513703) | **kém với PCV2** (PMID 17851101); độc, ăn mòn |

**Mạnh ở pH cao**: NaOH, Ca(OH)2/CaO; glutaraldehyde cần alkalin hóa; NaDCC.
**Mất hiệu lực khi pH tăng**: HOCl/bleach (HOCl → OCl⁻ trên pH 7–8), iodophor;
peracetic ổn định/hoạt động tốt hơn ở pH acid. QAC tương đối ổn định pH.

## 3. Sản phẩm thương mại + liều dùng VN (đã crawl)

| SP | Nhà SX | Thành phần | Liều | Giá tham khảo |
|---|---|---|---|---|
| **Bencocid** | Navetco | glutaraldehyde 150 g + benzalkonium chloride 150 g + amyl acetate 0.1 mL / L | 20–25 mL/10 L định kỳ; 33–40 mL/10 L khi có dịch; 100 mL/10 L xác chết. 1 L pha phun 4–5 m² (dịch: 2–3 m²) | 85.000 ₫ |
| **Omnicide** | Goovet | glutaraldehyde 150 g/L + cocobenzyl dimethyl ammonium chloride 100 g/L | 2–3 mL/L, 10 L/100 m²; dịch 1 mL/1.5 L | ~850.000 ₫ |
| **Good Farm L** | — | glutaraldehyde 15% + benzalkonium chloride 10% | 20–25 mL/10 L; dịch 33–40 mL/10 L | 120.000 ₫ |
| **TH4** | — | glutaraldehyde + QAC + pine oil + terpineol | 1:200; 1 L pha phun 3–5 m² | 350.000 ₫ |
| **Benkona** | — | benzalkonium chloride + amyl acetate glutaraldehyde | 5 mL/L | 250.000 ₫ |
| **Bioxide** | — | glutaraldehyde + alkylbenzyldimethylammonium chloride | 20–25 mL/10 L | 50.000 ₫ |
| **Virkon / Virkon S** | — | potassium peroxymonosulfate + NaCl + citric acid | 25 g/L bề mặt; 10 g/L nước uống; 50 g/10 L xác | 30.000–130.000 ₫ |
| **Vimekon** | Vemedim | potassium monopersulfate triple salt 494 g/kg + sodium hexametaphosphate 224 g + Na dodecylbenzene sulfonate 131.7 g + malic acid 89 g | 1:200 (100 g/20 L); **300 mL dd/m²**; 1–2 tuần/lần | — |
| **HAN-IODINE 10%** | Hanvet | PVP-iodine 10.000 mg + glycerin 10.000 mg/100 mL | 1 L / 100–250 L nước; 1–2 lần/tuần × 2–3 tuần | — |
| **Vemedim-Iodine** | Vemedim | phức iodine | 4 mL/L chuồng; 2.5 mL/L trên thú | — |
| **Formol** | — | formaldehyde 37–40% | 1 L/10–15 L; 1:10 dụng cụ; **chỉ chuồng trống** | 100.000 ₫ |
| **Cloramin B** | — | chloramine-B dạng bột | 3–5 g/L; 250 L/1.000 m²; tiếp xúc 3–5 h rồi rửa | 50.000–200.000 ₫ |
| **Donacide** | Greenfeed | — | 2,5 mL/L định kỳ; 3,5 mL/L có dịch; 10 mL/L hố tiêu độc | — |
| **ALTAcid** | Vemedim | tinh dầu thông | 1 L pha phun 2–3 m² bề mặt; 2 L/10 m³ phun sương | — |
| **Vôi bột** | nhiều nhà máy | CaO >80% hoặc Ca(OH)2, mịn 60–90 µm | **100 g/m²** rắc nền; **150–200 g/m³** chuồng heo; nước vôi 5% hoặc 20% quét tường, 2 lần/tuần | xem §4 |

⚠️ Cột giá là **giá tham khảo trên trang bán/thú y**, **quy cách đóng gói không phải
lúc nào cũng ghi rõ** (Virkon 30.000 ₫ vs 130.000 ₫ = khác gói). Ghi rõ "giá tham
khảo, chưa xác nhận quy cách" khi đưa vào tài liệu đối tác.

## 4. Giá gốc nguyên liệu (verify 09/2026)

- **Xút vảy NaOH 99%**: 23.000–34.000 ₫/kg (bán lẻ VN, bao 25 kg — ghgroup.com.vn);
  hàng Trung Quốc nhập số lượng lớn **9.800–13.500 ₫/kg**.
- **Xút lỏng**: 32% (d=1.348), 45% (d=1.478), 50% (d=1.52). IBC 1000 L rẻ hơn
  phuy 200 L ~8–12%; xe bồn rẻ hơn IBC ~15–20% (hoachatlocthien.com).
  ⚠️ Bảng giá của Lộc Thiên ghi "Liên hệ" — không có số, đừng trích như có giá.
- **Vôi**: vôi bột CaO 50–90% **800.000–2.500.000 ₫/tấn**; vôi cục CaO >80%
  1.800.000–2.300.000 ₫/tấn (khoangsandavoi.vn — nhà máy Hà Nam); vôi khử trùng
  chuyên dụng ~1.200.000 ₫/tấn (soidasanvuon.vn). Bán lẻ: vôi nông nghiệp
  400–1.000 ₫/kg, thủy sản 800–1.500 ₫/kg, xây dựng 700–1.500 ₫/kg.
- Giao sỉ: bao 30 kg, nguyên chuyến xe tải (VinaTap — không công bố giá).

## 5. Kinh tế — tính cho trại 1.000 con (per cycle)

**Giả định phải nêu rõ**: 1.000 heo thịt; 1,1 m²/con → ~1.100 m² nền; tổng bề mặt
xử lý (tường + trần + lối đi) ~2.200 m²; phun 0,4 L dd/m² → ~880 L dd/lứa.

| Phương án | Nguyên liệu/lứa | Chi phí |
|---|---|---|
| NaOH 2% | ~17,6 kg NaOH | **~440.000 ₫** (25.000 ₫/kg) hoặc **~200.000 ₫** (xút TQ 11.500 ₫/kg) |
| Vôi bột 100 g/m² | 220 kg | **~264.000 ₫** (1.200 ₫/kg) — chỉ nền/lối đi |
| Glutaraldehyde+QAC (Bencocid) | 2,5 mL/L × 880 L = 2,2 L cốt | **~187.000 ₫** (85.000 ₫/L) |
| Omnicide | 2,2 L cốt | **~374.000 ₫** |

→ **Khoảng cách chi phí NaOH vs sản phẩm thương mại nhỏ hơn nhiều so với cảm tính**;
NaOH còn phải cộng PPE + công rửa lại + ăn mòn nhôm/kẽm/bê tông.

**Nhân công & thiết bị**: 2 người × 1–1,5 ngày/lứa (rửa ướt → khô → sát trùng → khô);
máy rửa áp lực, bình phun/máy phun sương; PPE bắt buộc (găng, kính, khẩu trang/mặt nạ,
ủng) — đặc biệt NaOH và formaldehyde.

**Tần suất theo mầm bệnh**: ASF → terminal mỗi lứa + liên tục hố sát trùng/xe/nước
(tồn tại >42 ngày trong nước, PMID 41955653); vôi rắc lại ~2 lần/tuần.
PEDV → ủng/hố sát trùng mỗi ngày, **bột khô hiệu quả hơn dạng ướt** (PMID 36519006);
AHP cần 40–60 min tiếp xúc (PMID 29191202). S. suis → bị diệt bởi thuốc thường ở
nồng độ **thấp hơn khuyến cáo**, tồn tại 8 ngày trong phân ở nhiệt độ phòng
(PMID 6464322) → định kỳ tuần là đủ. Salmonella → phải **xoay vòng hoạt chất**
(PMID 28532805).

**Cảnh báo trung thực (đừng bán giải pháp)**: phân tích chi phí–lợi ích trên heo
Anh cho thấy **không** chiến lược nào (kể cả tăng cường vệ sinh–sát trùng) có lãi
ròng; cần giảm chi phí tới 96% mới hòa vốn, acid hữu cơ cần giảm 22,7% (PMID 30388998).
Tăng cường C&D + định tuyến xe làm số lần C&D tăng tới 81% và quãng đường 54%
(PMID 40784160).

## 6. Khoảng trống bằng chứng (phải ghi rõ khi báo cáo)

- **Không** tìm thấy nghiên cứu công bố nào về chi phí sát trùng/lứa cho trại 1.000 con ở VN
  → mọi con số ở §5 là **tính toán từ giá nguyên liệu đã verify**, không phải số khảo sát.
- Giá trị pH ngưỡng cho virus không-envelope ở nhiệt độ thường chưa thống nhất trong
  tài liệu (mỗi nghiên cứu dùng hệ đệm/virus khác nhau).
- Peroxyacid diệt virus kém (PMID 36995048) nhưng PAA 0,1% (5 L/m²) lại diệt được
  ASFV trong đất (PMID 34834979) → hiệu lực phụ thuộc nền, chưa có mô hình dự đoán.

## 7. PMID đã verify trong phiên

10432596, 4631432, 9192351, 17851101, 29778187, 33238521, 35458464, 34834979,
29944400, 28321028, 37513703, 35588273, 41955653, 29191202, 28408777, 36519006,
27886439, 21333548, 29183342, 36995048, 9871311, 2125592, 6780502, 6464322,
30388998, 40784160, 40368283, 29636911, 27452423, 5657532.

Mọi PMID đều đã efetch + đọc abstract. Các PMID "gợi ý trong brief" KHÔNG được tin;
tên/khái niệm lạc loài trong pool tìm kiếm bị loại (vd bài "Escherichia coli membrane
protein biogenesis" — không liên quan sát trùng).
