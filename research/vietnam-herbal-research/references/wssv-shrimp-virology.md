# WSSV (White Spot Syndrome Virus) — Virus đốm trắng tôm — knowledge bank

Ledger 73 PMID verified (16/08/2026) qua PubMed E-utilities (esearch → esummary → efetch abstract).
Deliverable: `D:/Hermes Proj/wssv-research/wssv.html` (2-tab Visualize + Học thuật) + preview https://preview.thefirstonly.com/thq01psq6wna + KFlow 8b0a8bc7-30bb-41bc-9e50-225779223d01.
Data: `D:/Hermes Proj/wssv-research/data/group{1,2,3}_{virology,infection,survival}.json`.

Dùng khi: user hỏi về bệnh tôm (đốm trắng, WSSV), virus giáp xác, kiểm soát dịch ao tôm, hoặc sản phẩm Kiềm thủy sản liên quan.

## Virology cơ bản (group1)
- **Phân loại**: WSSV là loài duy nhất họ Nimaviridae, giống Whispovirus. Virus dsDNA vòng khổng lồ. PMID 30924764 (ICTV profile), 19216439 (Leu 2009 review).
- **Virion**: 275 × 120 nm, hình elip→trụ, có đuôi (PMID 10639309). Cryo-EM 2023: capsid ring-stacked, oval→rod (PMID 36812312, 37108688).
- **Genome**: 292.967 nt / 184 ORF (van Hulten 2001, PMID 11448154); 305.107 bp / 181 ORF (Yang 2001, PMID 11689662); ICTV: 280–307 kb, 531 ORF (PMID 30924764).
- **Protein chính**: VP28 + VP19 (envelope), VP26/VP24/VP15 (nucleocapsid), VP664 = protein virus LỚN NHẤT từng biết (6.077 aa, ORF 18.234 nt) (PMID 15596810). VP28 trung hòa xâm nhiễm (PMID 11437657).
- **3 lớp**: envelope–tegument–nucleocapsid; VP24 là lõi liên kết VP26/VP28/VP38A/VP51A (PMID 20502662); tách bằng Triton X-100 (PMID 16501111).
- **Chủng**: TW/CN/TH đồng nhất 99,32%, khác vùng mất đoạn (PMID 15045557). VN isolate miền Trung mất ~8,5 kb (PMID 15557233). Mexico 255–290 kb (PMID 30184198).

## Cơ chế nhiễm + nhân lên + miễn dịch (group2)
- **Đường vào**: nước qua mang + antennal gland (không cuticle, PMID 33097672), vết thương/lột xác (PMID 19201551), đường miệng chết 78h (PMID 37766231), ăn mô nhiễm (PMID 31019127).
- **Entry**: VP28 bám PmRab7 (Kd 22,5 nM, PMID 39537865), clathrin-mediated endocytosis (PMID 26397221), cần cholesterol/MβCD (PMID 23747417), đa đường nội bào (PMID 27385304), AP-2 σ (PMID 26988289).
- **Nhân lên**: trong nhân, importin α1/β1 + Ran (PMID 35638850), DNA polymerase/rr2/ie1/ie3/vp26/vp28 (PMID 19596390), lytic (PMID 19216439).
- **VP28 vaccine/RNAi**: dsRNA vp28 → LT50 765h (PMID 21345339); oral vaccine RPS 61% (PMID 14747570); rSHRV-VP28 chết 30% vs 100% (PMID 40414471).
- **Miễn dịch tôm**: KHÔNG có adaptive immunity (PMID 41305485), chỉ innate Toll/Imd/AMP (PMID 28501515, 23059654), RNAi quan trọng (PMID 19596390), viral accommodation/EVE (PMID 16970989, 19725947).
- **Bệnh tích**: đốm trắng do WSSV cảm ứng chitinase Chi2 giảm chitin vỏ (PMID 38739679), chết ≤100% (PMID 38793694), ngưỡng thải G1 3,1×10³ copies/mg (PMID 37238106).
- **Stress**: sốc nhiệt 94% chết vs 28% (behavioral fever, PMID 37865676), lột xác tăng mẫn cảm (PMID 19201551), nhiệt độ nước ảnh hưởng PL25 (PMID 39370017).

## Khả năng sống sót + lây truyền (group3)
- **Môi trường**: DNA trong bùn đáy tới 10 tháng, nước ao dịch ~10² copies/mL.
- **Nhiệt**: đông lạnh KHÔNG diệt (tôm mồi đông lạnh gây chết 100% khi tiêm). Con số "50–60°C/x phút" KHÔNG verify được từ abstract — đừng bịa, ghi "chưa xác nhận".
- **Hóa chất**: clo 100 ppm/10 phút bất hoạt (nguồn review Islam 2023 PMC OA; không phải PMID abstract).
- **Host range**: 90+ loài giáp xác theo OIE/WOAH (không PMID — ghi nguồn OIE), 16/20 loài cua, copepod, Artemia, cua Scylla.
- **Lây ngang**: nước là đường chính (nguy cơ 1.0 vs phân 0.2), thải virus 6h sau khởi phát, liều tối thiểu 10¹ copies/mL.
- **Lây dọc**: 58% tôm bố mẹ hoang dã mang WSSV; TEM thấy virus trong buồng trứng/spermatophore (bằng chứng đầu tiên 2024).
- **Dịch sử**: 1992–1993 châu Á (Đài Loan), thiệt hại >3 tỷ USD/năm.
- **Carrier**: tôm sống sót mang virus tiềm ẩn, tải lượng thấp hơn nhiều log.

## 5 điểm kiểm soát trại (đã chốt trong trang)
1. Chlorine nước 100 ppm/10 phút + xử lý bùn đáy (10 tháng)
2. Giống PCR sạch (58% bố mẹ hoang dã mang WSSV)
3. Ổn định nhiệt, chống stress (94% chết khi sốc nhiệt)
4. Chặn vector cua/ghẹ/copepod/Artemia + chim
5. Không tái dùng tôm carrier sau dịch
