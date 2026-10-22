# Berberine Extraction — Verified Knowledge Bank (17/08/2026)

Bối cảnh: dự án `berberine-tannin-extraction` (group 1 = berberine) — chủ DN sản xuất TĂCN + chiết xuất thảo dược tại VN, phát triển sản phẩm berberine cho heo. Mọi PMID đã efetch abstract trong phiên; mọi patent xuất hiện trên Espacenet. Deliverable: `D:/Hermes Proj/berberine-tannin-extraction/data/group1_berberine.json` (schema: topic/summary/facts/method_detail/verification).

## 1. Nguồn nguyên liệu + hàm lượng (verified)
- Coptis chinensis (Hoàng Liên): tổng alkaloid thân rễ 15,97% (907 m) → 17,82% (1698 m), tăng theo độ cao — HPLC+UV-Vis, 9 alkaloid (PMID 41809628). Vùng trồng chính: Shizhu, Trùng Khánh TQ.
- Berberis spp rễ: 1,6–4,3% (review 40661201); Berberis integerrima rễ 6,26 mg/g DW ≈ 0,63%, tập trung vỏ rễ (40388442).
- Coscinium fenestratum thân: 2,67–3,37% w/w tùy phương pháp (16888396).
- Phellodendron chinense (Hoàng Bá): N/P đất điều hòa sinh tổng hợp berberine (41451276); kháng H. pylori in vitro (38823658).
- Fibraurea tinctoria (Hoàng đằng, Menispermaceae, có ở VN): protoberberine gồm berberine/palmatine/jatrorrhizine (review 36770960); palmatine phân lập bằng silica gel CC từ cao methanol (39109327).
- Mahonia napaulensis vỏ (40087695); cành Berberis cảnh nguồn rẻ (39590381); Berberis aristata LD50 >5000 mg/kg (20738174).
- Task-brief ghi "2–8% berberine trong thân rễ Coptis" — CHƯA có nguồn verified trực tiếp; dùng số verified thay thế (ở trên) và ghi rõ.

## 2. Hóa học (verified)
- Berberine: C20H18NO4+ (cation), MW 336,4 (PubChem CID 2353); HCl salt C20H18ClNO4, MW 371,8 (CID 12456). Verify: PubChem REST `/rest/pug/compound/cid/<CID>/property/MolecularFormula,MolecularWeight,IUPACName/JSON`.
- pKa 2,47 và 15,7 → muối tan nước, bền acid/trung tính; dạng base tan dung môi hữu cơ (full-text review 40661201 / PMC12257298).
- Berberine sulfate tan tốt trong nước; hydrochloride gần như không tan → nguyên tắc chiết H2SO4 loãng + kết tinh HCl (40661201). Berberine sulphate có bài dược lý riêng (42551178).

## 3. Chiết cổ điển (verified)
- 4 nhóm: nước (sắc), nước acid, nước vôi (lime milk), ethanol (reflux/siêu âm/vi sóng) (40661201).
- Quy trình công nghiệp TQ "nước chua + nước vôi": ngâm 24 h, H2SO4 0,4%, rắn:lỏng 1:16, nước vôi pH 12, HCl pH 5, NaCl 25% → hiệu suất 8,4%, tinh khiết thô 7,27% (40661201 full-text).
- Maceration ethanol 80% > percolation > Soxhlet (Coscinium: 3,37/3,08/2,67%) (16888396); ethanol 80% + 2% acid acetic, 25°C, 72 h tối ưu cho Berberis integerrima (40388442); reflux ethanol tối ưu RSM Box-Behnken (41611957).
- Sắc nước tạo kết tủa siêu phân tử — công nghiệp hiện đại tách riêng (41865144, 42469858).

## 4. Chiết hiện đại (verified)
- UAE dung môi xanh (ĐH Y Dược Huế, VN): lactic 96%, 30 mL/g, 60°C → 139,6 mg/g; pyruvic 88%, 30 mL/g, 75°C → 146,3 mg/g tổng alkaloid (40286019). UAE vỏ Hoàng Bá: ethanol 81%, 500 W, 80°C, 23 min, 25 mL/g (36177459). UAE chung: ethanol 70%, 1:25, 180 W, 50°C, 30 min → 8,12% (40661201).
- MAE: công suất > thời gian > nhiệt độ (Taguchi L9, HPTLC quant) (39916620); Tinospora 1,66% trong 3 phút vs Soxhlet 3 h 1,04% vs ngâm 7 ngày 0,28% (40661201).
- SFE: scCO2 + 1,2-propanediol 6,91% (200 bar) → 7,53% (500 bar), 3 h; ethanol modifier kém 0,15–0,19%; Tween 80 vô ích (16500064).
- Kết hợp siêu âm+vi sóng: H2SO4 0,05 M, 10 min US + 3 min MW 600 W → 11,43% (40661201). Ionic liquid USE 40 min (40661201).
- Enzyme-assisted: KHÔNG có PMID chuyên biệt (`"enzyme-assisted extraction" AND berberine` = 0); chỉ có mô tả trong review 40661201 (enzyme thủy phân + siêu âm, HPLC định lượng).
- NADES + UAE Thalictrum: berberine 11,91 mg/g DW, AB-8 resin tốt nhất (39241417).

## 5. Tinh chế (verified)
- Chuỗi: chiết acid → kiềm hóa pH 12 kết tủa base → hòa tan HCl → kết tinh lạnh (muối HCl kém tan) → kết tinh lại 2–3 lần (ethanol/nước) → >95–97%; ≥99% cần nhựa macroporous/sắc ký.
- Nhựa macroporous: XAD-8 80,11%, AB-8 79,00%, LSA-40 95,58/89,86%, HPD-400 79,52% (40286019); tổ hợp X-5/S-8/HPD100/AB-8 hấp phụ ~100% (22066439); than mesoporous OMC hấp phụ 450 mg/g (23953651).
- Kết tinh chọn lọc từ cao thô bằng crystalline mate — nghiên cứu, chưa công nghiệp (41875085).

## 6. QC (verified)
- HPLC-PDA: 347 nm, acetonitril/0,1% H3PO4, 20 min, LOD 0,019 mg/L, thu hồi 97,2–107,4% (37818260).
- HPTLC GF254: ethyl acetate:methanol:diethylamine 6,5:1:0,3, 350 nm, Rf 0,22, ICH Q2(R1) (42360317).
- TLC-densitometry: butanol:AcOH:nước 14:3:4, 415 nm (16888396). UV-Vis ~345–350 nm cho sàng lọc nhanh.
- Kết hợp DNA barcoding + HPTLC chống hàng giả (40945162); HPLC coptisine+berberine cao nước (40943623).

## 7. Công nghiệp (verified + gap)
- TQ dẫn đầu sản xuất (nguồn Coptis Tứ Xuyên/Trùng Khánh; Phellodendron). Quy trình chủ lực: nước acid + nước vôi (rẻ, dễ vận hành) (40661201). Chiết cồn hiệu suất cao nhưng không hợp đại trà (chi phí dung môi/năng lượng/an toàn).
- Nhà sản xuất/đơn vị patent: Jiangxi Fushine Pharmaceutical (CN111100121A tinh khiết ≥99,8%, CN111205285A), Guilin Layn Natural Ingredients (CN118005628A: 95% berberine HCl từ vỏ Hoàng Bá), Chongqing Univ of Education (CN117050071A).
- Giá thành/chi phí sản xuất: CHƯA VERIFY (không bịa số). Nếu cần giá VN: dùng pipeline `references/vn-market-prices.md` (Camofox + DDG).

## 8. Patent (Espacenet-verified 17/08/2026, query 'berberine extraction' + 'berberine purification crystallization')
- Chiết xuất: CN117050071A (đã đọc abstract), CN119613395A, CN110746417A (B), CN104435194A, CN108707149A (B), CN110540537A, CN107955000A, CN106518863A (film extraction), CN114230566A, CN121850998A (Nandina domestica), CN109942573A (Berberis julianae).
- Tinh chế: CN111100121A (B) (tạp ≤0,2%, đã đọc abstract), CN111205285A (B) (tinh chế + dạng tinh thể), CN111704609A (B) (BaCl2).
- Thiết bị: CN120827746A (B), CN216457009U (chiết-kết tinh), CN216320085U, CN214913546U (siêu âm).
- Muối mới: WO2016110250A1 (mangiferin-6-O-berberine, Changzhou Deze). Bào chế (không phải chiết): WO2021090214A2 (Sucrosomial), US11786513B2.
- Lưu ý: WO2014042426A1 (CJ CheilJedang) là patent COMPOSITION trị bệnh dạ dày, không phải chiết xuất — đừng nhầm.

## Query patterns đã chạy được
- PubMed: `berberine AND (ultrasonic OR ultrasound) AND extraction`, `berberine AND microwave AND extraction`, `berberine AND (supercritical OR "supercritical fluid")`, `macroporous resin AND berberine`, `berberine AND (TLC OR HPTLC OR thin-layer)`, `Fibraurea tinctoria AND berberine`, `berberine AND (pKa OR protonation OR ionization OR cation)` (ít hit hữu ích — pKa lấy từ review full-text).
- Full-text review: PMC OA REST `https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pmcoa.cgi/BioC_xml/PMC12257298/unicode` rồi grep `pKa|solubility|lime milk|sulfuric acid|purity` — lấy được số công nghiệp + pKa mà abstract không có.
- Espacenet: browser + browser_console span extraction (xem SKILL.md phần Espacenet).
- PubChem: CID 2353 (berberine), 12456 (berberine chloride).

## Gap trung thực
- Giá thành berberine HCl, chi phí sản xuất quy mô: chưa verify.
- Hàm lượng "2–8%" Coptis: chưa verify nguồn gốc.
- Enzyme-assisted berberine: không có PMID chuyên biệt.
- Google Patents chặn 503 → toàn bộ patent verify qua Espacenet.
