# Eicosanoids ở heo — Roadmap nghiên cứu (COX-2/PGE2, 5-LOX, ω-3/ω-6)

Chủ đề: Eicosanoids là lipid truyền tín hiệu từ oxy hóa arachidonic acid (ω-6) hoặc EPA/DHA (ω-3) qua COX (prostaglandin/thromboxane), LOX (leukotriene/lipoxin), CYP450 (EET). Trung tâm của viêm, sốt, đau, hàng rào ruột. Tỷ lệ ω-6/ω-3 trong thức ăn quyết định hướng dòng eicosanoid (động vật có vú KHÔNG chuyển ω-6 → ω-3).

## Tóm tắt nhanh

| Khía cạnh | Nội dung |
|-----------|----------|
| Enzyme mở khóa | cPLA2α — ROS kích hoạt, giải phóng AA khỏi màng phospholipid |
| Nhánh COX | COX-1 (nền) / COX-2 (cảm ứng) → PGH2 → mPGES-1 → PGE2; PGIS → PGI2; TXS → TXA2 |
| Nhánh LOX | 5-LOX (+FLAP) → LTA4 → LTB4 (hóa ứng động bạch cầu) / LTC4→LTD4→LTE4 |
| Thụ thể PGE2 | EP1 (Gq), EP2 (Gs, ức chế miễn dịch/MDSC), EP3 (Gi, GÂY SỐT), EP4 (Gs, bảo vệ niêm mạc ruột) |
| Tắt tín hiệu | 15-PGDH phân giải PGE2 — ức chế 15-PGDH (SW033291) làm tăng PGE2, phục hồi mô |
| Công tắc dinh dưỡng | ω-3 (EPA/DHA) cạnh tranh AA → eicosanoid ít viêm + resolvin/lipoxin (SPM chống viêm) |
| Bệnh heo | S. suis, M. hyopneumoniae, APP, Metastrongylus đều tăng COX-2/5-LOX + PGE2/LTB4 |

## Sơ đồ cascade

```
Màng phospholipid → cPLA2α (ROS kích hoạt) → Arachidonic acid (AA)
  ├─ COX-1/COX-2 → PGG2 → PGH2 → mPGES-1 → PGE2 (sốt qua EP3, bảo vệ ruột qua EP4)
  │                             ├─ PGIS → PGI2 (giãn mạch, bảo vệ niêm mạc — cộng hưởng với PGE2)
  │                             └─ TXS → TXA2 (ngưng tập tiểu cầu)
  ├─ 5-LOX → LTA4 → LTB4 (hóa ứng động) / cysteinyl-LT (LTC4/LTD4/LTE4, co thắt phế quản)
  └─ CYP450 → EETs (giãn mạch) / 20-HETE (co mạch)
```

## Query PubMed đã test (Aug 2026)

| Query | Kết quả |
|-------|---------|
| `COX-2 cyclooxygenase porcine inflammation lung` | ✅ 6 PMIDs |
| `omega-3 PUFA pig immune response eicosanoid` | ✅ 6 PMIDs |
| `leukotriene swine lung inflammation` | ✅ 6 PMIDs |
| `prostaglandin E2 fever hypothalamus EP3` | ✅ 6 PMIDs |
| `prostaglandin E2 immunomodulation EP2 EP4 dendritic cell T cell` | ✅ 6 PMIDs |
| `15-hydroxyprostaglandin dehydrogenase PGE2 catabolism inflammation` | ✅ 6 PMIDs |
| `prostaglandin E2 intestinal barrier permeability epithelial repair` | ✅ 5 PMIDs |
| `flunixin meglumine pig prostaglandin inflammation` | ✅ 2 PMIDs |
| `prostaglandin E2 secretory diarrhea CFTR chloride intestinal epithelium` | ✅ 1 PMID |
| `specialized pro-resolving mediators swine` | ✅ (1-2 dùng được) |
| `prostaglandin E2 ETEC pig diarrhea intestinal secretion` | ❌ 0 — dùng `prostaglandin E2 secretory diarrhea` thay thế |
| `eicosanoid prostaglandin pig intestinal barrier weaning` | ❌ 0 |
| `prostaglandin E2 IPEC-J2 intestinal epithelial tight junction` | ❌ 0 — dùng `n-3 PUFA IPEC-J2 LPS` thay thế |
| `enterotoxigenic Escherichia coli prostaglandin E2 pig intestine chloride secretion` | ❌ 0 |
| `resolvin lipoxin specialized pro-resolving mediators pig inflammation` | ❌ 0 — dùng `resolvin D1 pig` + `SPM swine` tách riêng |
| `omega6 pig growth` / `linoleic acid arachidonic acid pig immune growth eicosanoid` | ❌ 0 |
| `nsaid_pig` (flunixin meloxicam) | ❌ 0 — dùng `flunixin meglumine pig` |

Bài học: query PGE2+ETEC trực tiếp không ra trên PubMed — chuyển sang cơ chế chung (secretory diarrhea, CFTR, iNOS/COX-2 trong Gastroenterology PMID 11910358) và suy luận từ ETEC LT→cAMP→CFTR.

## Bảng PMID chính (36 PMIDs)

| PMID | Nguồn (Năm) | Đóng góp |
|------|-------------|----------|
| 33673302 | Microorganisms (2021) | S. suis cảm ứng COX-2/PGE2 ở phổi heo (PCLS), vai trò suilysin |
| 24925603 | J Comp Pathol (2014) | COX-2 trong viêm phổi M. hyopneumoniae ở heo |
| 22341869 | Res Vet Sci (2012) | 5-LOX + COX-2 tăng ở phổi heo (Mh + APP), kèm LTB4/PGE2 |
| 19906385 | J Comp Pathol (2010) | 5-LOX/COX-2 trong viêm phế quản phổi giun Metastrongylus |
| 18565553 | Res Vet Sci (2009) | AEC II heo giải phóng LTC4 khi LTB4/LPS, tăng MCP-1 |
| 29156155 | PLEFA (2017) | LTB4 chỉ điểm tổn thương phổi heo đa chấn thương |
| 9329955 | J Clin Invest (1997) | PGI2+PGE2 cộng hưởng phục hồi hàng rào hồi tràng heo (Ussing) |
| 11927615 | J Clin Invest (2002) | EP4 bảo vệ niêm mạc đại tràng (DSS colitis); chủ vận EP4 chữa lành |
| 39172154 | J Mol Med (2024) | EP4R tiết Cl- ruột; NSAID-enteropathy |
| 11910358 | Gastroenterology (2002) | iNOS/COX-2 trong tiêu chảy do vi khuẩn xâm lấn |
| 31865463 | J Gastroenterol (2020) | NSAID gây tổn thương ruột non: ức chế PG + ty thể → TLR4/NLRP3; ~50% người dùng mãn tính |
| 34157367 | Gastroenterol Hepatol (2022) | Độc tính tiêu hóa NSAIDs; COX-2 chọn lọc an toàn hơn |
| 36563142 | Sci Adv (2022) | Neuron POA-EP3R điều khiển thân nhiệt 2 chiều; PGE2 ức chế → sốt |
| 39352065 | Acta Physiol (2024) | Sốt phụ thuộc PGE2 từ tế bào nội mô não + EP3 |
| 41664914 | J Physiol (2026) | PGE2-EP3 ở LPB gây hành vi tìm hơi ấm (warmth-seeking) |
| 38702500 | Acta Pharmacol Sin (2024) | PGE2 nội LPBN gây sốt qua EP3 + đường LPBN-POA |
| 20051652 | J Pharmacol Sci (2010) | PGE2 thúc đẩy Th17/Th1 qua EP2/EP4 — "immunoactivator" (đảo chiều quan điểm cũ) |
| 37315536 | Immunity (2023) | PGE2-EP2/EP4 làm cDC1 rối loạn (mất IRF8) → thoát miễn dịch ung thư |
| 21972293 | Blood (2011) | Vòng hồi tiếp PGE2-COX2 tạo MDSC |
| 28630103 | J Leukoc Biol (2017) | EP2/EP3 tăng trên DC dung nạp (tol-DC) |
| 35126344 | Front Immunol (2021) | Biểu mô miệng tiết PGE2 ức chế T cell |
| 34794096 | Animal (2021) | Dầu cá EPA/DHA cho nái (36 nái) đổi oxylipin sữa đầu/sữa |
| 33445698 | Nutrients (2021) | Nhũ tương dầu cá 100% (FO100) heo non tháng: EPA 0,1→9,7; DHA 2,5→13,6; giảm đáp ứng LPS |
| 36463585 | Vet Immunol Immunopathol (2022) | DHA/EPA điều biến monocyte heo CD14+ (25-100 µM không độc) |
| 38062040 | Sci Rep (2023) | n-3 PUFA giảm rối loạn chuyển hóa IPEC-J2 do LPS (proteomics + RNA-seq) |
| 32759853 | Nutrients (2020) | Ăn DHA cao: giảm AA máu, tăng Resolvin D1 phổi, chống bụi chuồng heo |
| 32080063 | Shock (2020) | Resolvin D1 (0,3-0,6 µg/kg IV) bảo vệ tim/não heo sau ngừng tim |
| 39456882 | Int J Mol Sci (2024) | FA transporters CD36/SLC27A ở nội mạc tử cung heo; AA kích thích IL1B |
| 22648045 | Vet Immunol Immunopathol (2012) | Flunixin meglumine giảm PGE2 huyết tương heo sau LPS; bộ 5 gene biomarker |
| 39047790 | Am J Vet Res (2024) | ⚠️ PGE2 KHÔNG đáng tin làm biomarker đau thiến heo (RCT) |
| 41722697 | Pharmacol Res (2026) | Master switch eicosanoid-ROS; ferroptosis qua 15-LOX/PE peroxid hóa |
| 41240885 | BBRC (2025) | Ức chế mPGES-1 chọn lọc (pharmacophore) |
| 41042969 | Mol Pharm (2025) | Ức chế mPGES-1 AGU661 |
| 39971253 | Pharmacol Ther (2025) | 15-PGDH ức chế khối u, điều hòa biểu sinh |
| 39952309 | Exp Gerontol (2025) | Ức chế 15-PGDH (SW033291) chữa suy tim tuổi già |
| 25039419 | J Anim Physiol Anim Nutr (2015) | Kẽm và vận chuyển biểu mô ruột heo cai sữa (Ussing) |

## Thuật ngữ tiếng Việt

| Thuật ngữ | Tiếng Việt |
|-----------|-----------|
| Eicosanoid | Eicosanoid (lipid truyền tín hiệu từ axit arachidonic) |
| Prostaglandin E2 (PGE2) | Prostaglandin E2 — trung gian sốt/viêm |
| Cyclooxygenase (COX) | Cyclooxygenase — enzyme tạo prostaglandin, đích của NSAIDs |
| Leukotriene B4 (LTB4) | Leukotriene B4 — chất hóa ứng động bạch cầu trung tính |
| Arachidonic acid (AA) | Axit arachidonic (ω-6, 20 carbon) |
| Resolvin | Resolvin — phân tử chấm dứt viêm từ DHA/EPA |
| 15-PGDH | Enzyme phân giải PGE2, "tắt công tắc" |
| mPGES-1 | Synthase chuyển PGH2 thành PGE2 |
| Sốt (fever) | Sốt — do PGE2-EP3 ở vùng tiền thị (POA) |
| Hàng rào ruột | Intestinal barrier — PGE2/PGI2 bảo vệ qua EP4 |

## Ma trận điều biến dinh dưỡng

| Can thiệp | Cơ chế eicosanoid | PMID |
|-----------|-------------------|------|
| Dầu cá (EPA/DHA) cho nái | Đổi oxylipin sữa đầu sang hướng chống viêm | 34794096 |
| n-3 PUFA cai sữa / IPEC-J2 | Giảm rối loạn chuyển hóa do LPS | 38062040 |
| DHA diet + bụi chuồng | Tăng RvD1 phổi, giảm AA | 32759853 |
| Nhũ tương lipid IV dầu cá | Tăng EPA/DHA huyết tương, giảm đáp ứng LPS | 33445698 |
| Flunixin (NSAID) | Giảm PGE2 huyết tương sau LPS | 22648045 |
| ⚠️ Tránh NSAIDs dài ngày | Mất PGE2/PGI2 bảo vệ ruột → enteropathy | 31865463, 9329955 |
| Polyphenol (curcumin/quercetin) | Ức chế COX-2/LOX (cross-ref card Curcumin, Quercetin) | — |

## Card đã tạo (Aug 2026)

- Title: `🧬 Eicosanoids ở heo — Hệ lipid điều khiển viêm, sốt và sửa chữa mô: COX-2/PGE2, 5-LOX/Leukotriene & công tắc ω-3/ω-6`
- ID: `8dae3641-6051-4830-a5ec-e191315b96f4` (201, reading time 1080s)
- 28 tags, overview block `<!--OVERVIEW-->` ở đầu content
