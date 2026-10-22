# Premix heo — Nhóm A: 8 cao thảo dược VN (verify 16/08/2026)

Ledger cho 8 loại đầu của công thức premix 16 thảo dược (nhóm B = `premix-heo-herbs-b.md`).
Deliverable: `D:/Hermes Proj/premix-heo-research/data/group2_herbs_a.json` (66 PMID verified, audit `data/_g2_abstracts.json` = 79 abstracts efetch).
Schema mỗi loại: id, name_vi, latin, active_compounds, category, summary, mechanisms[], pig_evidence[] (effect/type/evidence), diseases[], dosage, safety, references[], verification.

## Bảng evidence theo loài (type: in vivo heo / in vitro / loài khác; mức: Mạnh/Vừa/Sơ bộ)

| Loại (liều công thức) | Hoạt chất chính | Bằng chứng heo in vivo | PMID chốt |
|---|---|---|---|
| Xuyên tâm liên (50 mg/kg) | andrographolide | ✅ Nái 250–1000 ppm: ↑ IgG sữa đầu (lứa 6–9), ↑ sữa đầu heo con (lứa 3–5), ↓ mất cơ (Vừa). Heo vs aflatoxin B1 transcriptomics (Sơ bộ). ETEC = CHUỘT; PRRSV/S.suis/PEDV = in vitro/in silico | 38271976, 41535828, 41321521 (review, "cần thêm thử nghiệm heo"), 37727052 (chuột ETEC), 34704222, 39939878, 39553769 |
| Cát cánh (30 mg/kg) | platycodin D, polysaccharide PGP | ✅ MẠNH NHẤT NHÓM: PGP 1–2 g/kg heo con cai sữa 28 ngày: ADG↑, F/G↓, IL-1β/2/4↓, tight junction↑, Bacteroidota↑/Proteobacteria↓ (Vừa). CMH blend 0,1–0,3% gồm cát cánh trên 240 heo: ↓ điểm tiêu chảy, PMN↑, nhung mao↑ (Vừa). PCV2 (3D4/21), PRRSV-2 = in vitro | 41986952, 21535231, 38423406, 30469357 |
| Húng chanh (30 mg/kg) | thymol, carvacrol, rosmarinic acid | ❌ KHÔNG có heo — esearch `Plectranthus amboinicus AND (pig OR swine OR porcine)` = 1 hit (gà). Gà thịt PAE 100–200 mg/kg: GPx/SOD↑, MDA↓, coliform↓ (Vừa-loài khác). Salmonella biofilm, anti-QS = in vitro | 37457190, 37998800, 42334695, 42266885, 40430526 |
| Bách bộ (30 mg/kg) | Stemona alkaloid (tuberostemonine...), pectin polysaccharide | ❌ KHÔNG có heo — esearch `Stemona tuberosa AND (pig OR swine OR porcine)` = 7 hits toàn ho/côn trùng/cầu trùng gà. In vivo gà: chống Eimeria tenella (41807897). ⚠️ CẢNH BÁO: ức chế hô hấp TRUNG ƯƠNG (20219659) — alkaloid độc thần kinh tiềm tàng, cần độc tính heo trước khi dùng | 41807897, 20219659, 14648394, 19214944, 40713155 |
| Mạch môn (20 mg/kg) | ophiopogonin D, OP polysaccharide | ❌ KHÔNG có heo — esearch `Ophiopogon japonicus AND (pig OR swine OR porcine)` = 4 hits đều không phải heo. Gần nhất: OP liposome adjuvant vaccine parvovirus HEO trên CHUỘT (26529188: CD4/CD8↑, HI↑); thỏ thịt (42193829). ALI/xơ phổi/viêm ruột = chuột | 26529188, 39101149, 38824823, 39039348, 42193829 |
| Gừng (50 mg/kg) | 6-gingerol, shogaol, zingerone | ✅ 1 in vivo heo SƠ BỘ: oleoresin 0,05% heo vỗ béo KHÔNG đổi năng suất (22063669, "cần liều cao hơn"). Bê Holstein dịch chiết gừng: tăng trưởng+miễn dịch↑ (loài khác). In vitro vs E. coli/Salmonella PWD (29926714). ⚠️ KHÔNG TỒN TẠI meta-analysis gừng-heo trên PubMed (7 query, 0 hit) — meta gần nhất = tinh dầu chung 38359649 (31 study: ADFI/ADG↑, FCR/tiêu chảy↓) | 22063669, 38602560, 29926714, 21305447, 16849115, 16187193, 29328426, 38359649 |
| Bạc hà (30 mg/kg) | menthol, menthone, rosmarinic acid | ✅ Nái/gilt: mint oil top dress d110→cai sữa: ↑ năng suất heo con sau cai sữa (Vừa; 45 nái+481 con / 53 nái+605 con). Heo cai sữa: EO blend gồm M. piperita đổi hệ vi sinh ruột (Sơ bộ-blend). PAM heo ↓ IL-1β/TNF-α, kháng ETEC F18+ (in vitro tế bào heo). EFSA: peppermint tincture an toàn MỌI loài vật nuôi | 34322530, 32987688, 34201645, 40741364, 41619484 |
| Mộc hoa trắng (30 mg/kg) | chưa xác định | ⚠️ DANH TÍNH CHƯA XÁC ĐỊNH — cần COA nhà cung cấp. Ứng viên chính: Osmanthus fragrans (hoa mộc, f. leucanthus — Wikipedia vi: "hoa mộc"); phụ: Magnolia × alba (ngọc lan trắng, Michelia alba). Cả 2 đều 0 nghiên cứu heo. Osmanthus: acteoside/phenylethanoid glycoside chống oxy hóa-kháng viêm (chuột); Michelia: linalool 72–80%, sesquiterpenoid ức chế NO | 41951194, 37852338, 40603384, 35684387, 40193222 |

## Pitfalls / corrections phiên này

- **PMID gợi ý trong task brief SAI 100%** (thêm case vào pitfall chung): 30736495 = nuôi cấy phôi đu đủ Carica papaya; 29978730 = tế bào gốc mỡ người — đề bài gợi ý là "andrographolide kháng ETEC". Đã efetch xác nhận → loại. (Case sibling: 32221055/36108156 cho lá ổi.)
- **Bẫy title → loài sai**: PMID 32992929 "Effects of Dietary Andrographolide Levels on Growth Performance, Antioxidant Capacity, Intestinal Immune Function..." (Animals 2020) nghe như heo nhưng là CÁ CHÌNH ĐỒNG (Monopterus albus). Luôn đọc abstract xác nhận species trước khi xếp loại pig_evidence.
- **'Yellow ginger' mơ hồ**: PMID 25049522 (Exp 2, "yellow ginger" 1 g/kg trên heo) thường là NGHỆ (Curcuma longa) trong nghiên cứu Hàn — không dùng làm bằng chứng Zingiber officinale.
- **esearch 'không có hit heo' = bằng chứng thiếu dữ liệu** — dùng câu `X AND (pig OR swine OR porcine)` với retmax 15 làm thao tác chuẩn để ghi "thiếu dữ liệu heo trực tiếp" một cách kiểm chứng được (áp dụng cho húng chanh, bách bộ, mạch môn, mộc hoa).
- **Liều công thức vs liều nghiên cứu**: xuyên tâm liên công thức 50 mg/kg = 0,005% — thấp hơn 5–20× so với 250–1000 ppm trên nái (38271976); cát cánh 30 mg/kg vs PGP 1–2 g/kg (41986952). Ghi rõ khoảng cách liều trong field `dosage` để chủ trại thấy ngay.
- **Audit trail**: `_g2_abstracts.json` + assert trong build script (mọi pmid trong deliverable phải có abstract efetch) — assert đã bắt được PMID 37852338 chỉ mới esummary chưa efetch. Giữ pattern này.

## Query patterns đã chứng minh

- `"<Herb> AND (pig OR swine OR porcine OR weaned)"` retmax 15 (xuyên tâm liên, cát cánh)
- `"<Herb> AND (pig OR swine OR porcine)"` để chứng minh thiếu dữ liệu heo (húng chanh=1 hit gà, bách bộ=7 hits không heo, mạch môn=4 hits không heo)
- `"ginger AND (meta-analysis OR systematic review) AND (pig OR swine OR piglet OR weaned)"` → 0 hit (xác nhận không có meta)
- Mộc hoa trắng: Wikipedia vi opensearch "mộc hoa"/"hoa mộc"/"ngọc lan trắng" + action=raw → danh tính ứng viên
