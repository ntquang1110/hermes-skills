# Premix Heo Research — Group 3B (8 cao thảo dược VN) — verified PMID ledger

Project: `D:/Hermes Proj/premix-heo-research/data/group3_herbs_b.json` (đã viết 16/08/2026).
52 PMID verified (efetch + đọc abstract, audit trail `_g3b_abstracts.json` trong thư mục data).
Schema giống piglet-diarrhea catalog: id, name_vi, latin, active_compounds, category, summary, mechanisms[], pig_evidence[], diseases[], dosage, safety, references[], verification.

## Bảng PMID verified theo loại (kèm mức bằng chứng heo)

| Loại (latin) | Bằng chứng heo | PMID chính + phát hiện cốt lõi |
|---|---|---|
| vằng đắng (Coptosapelta flavescens) | KHÔNG có heo | 35243058 (Cao Khai kháng viêm/oxy hóa trên chuột, VN), 25735817 (CFQ kháng Giardia), 24689295 (hóa thực vật đầu tiên: anthraquinone/naphthoquinone) |
| lá ổi (Psidium guajava) | MẠNH — heo cai sữa ETEC | 33140438 (GE 50–200 mg/kg: ↓ tiêu chảy, ↑ SOD/GPx/T-AOC, ↓ IL-1β/6/TNF-α, ↑ villus), 34109234 (↑ ZO-1/occludin/claudin-1, NHE3), 38420856 (hỗn hợp GE+PSE 200 mg/kg, 200 heo con, microbiome), 32193047 (chống oxy hóa xúc xích heo, không phải heo sống) |
| rau má (Centella asiatica) | Chỉ in vitro heo | 32949562 (BBB tế bào nội mô não heo), 34174755 + 31574397 (asiatic acid cải thiện oocyte/phôi heo in vitro), 33022343 (chống viêm đại tràng DSS chuột), 37304601 (phôi thiếu oxy, loài khác) |
| cam thảo (Glycyrrhiza uralensis/glabra) | MẠNH NHẤT — 9 in vivo heo | 23244491 (chữa tiêu chảy rotavirus heo con), 38471043 (PEDV: sống 80% vs 0%), 42298622 (GA 0,65–2,6 g/kg, 225 heo: ↓ tiêu chảy, ↑ IgG/IgM, ↓ vi khuẩn hô hấp), 41325968 (18β-GA 100 mg/kg: ↑ ADFI 21,5%/ADG 64%), 36548753 (GA+probiotics chống DON), 42424652 (cao cam thảo 500 mg/kg heo nái: ↑ tăng khối lượng ổ + IUGR), 42250709 (liquiritin hỗn hợp CP-GU 1%), 40966589 (18β-GA chống oxy hóa thận), 40046304 (GA uống + vaccine FMD heo), 38965549 (matrine+GA kháng PRRSV in vitro), 21535231 (hỗn hợp CMH 0,1–0,3%) |
| atiso (Cynara scolymus) | VỪA — 2 in vivo heo | 31890916 (CSE 15 mg/kg BW heo cai sữa, factorial FOS×CSE×DON: ↓ E:L, ↑ butyrate), 34689664 (bã ép hạt cardoon C. cardunculus: ↓ IMF/MUFA, ↑ PUFA), 15863902 (cynaropicrin chống co thắt ≈ papaverine, chuột lang), 31286388 (cao lá atiso chống oxy hóa), 40555873 (cá rô phi, loài khác) |
| rau đắng đất (Glinus oppositifolius) | KHÔNG có heo | 37049664 (triterpenoid mới spergulagenin B/C/D + ức chế NO), 38838506 (saponin chống tạo mỡ), 38460574 (MEGO 200–400 mg/kg chuột viêm khớp CFA: ↓ TNF-α/IL-6/IL-1β), 40953343 (acyamino acid + flavonoid ức chế XO/α-glucosidase), 37532557 (Traphaco Tox-off/Biovip chứa loài này, AMPK/ACC, HepG2) |
| diếp cá (Houttuynia cordata) | VỪA–MẠNH — 3 in vivo heo | 25049522 (1 g/kg, 150 heo cai sữa: ↑ ADG/ADFI/G:F, ↓ điểm tiêu chảy), 25049500 (1 g/kg: KHÔNG cải thiện tăng trưởng nhưng ↓ E. coli phân — ghi trung thực), 35924249 (HC50 uống + vaccine PRRSV-1 MLV: ↓ viremia HP-PRRSV-2, ↑ IRF3), 20942608 (kháng PrV in vitro), 42273260 (review cơ chế Nrf2/NF-κB/NLRP3), 40339260 (THỎ không phải heo!), 42433689 (gà broiler) |
| hương nhu (Ocimum gratissimum / Elsholtzia ciliata) | KHÔNG có heo trực tiếp | 12780522 (EO O. gratissimum kháng độc lực Shigella + hiệp đồng kháng sinh), 12020920 + 16008129 (chống co thắt hồi tràng, eugenol/cineole), 40412777 (E. ciliata kháng viêm RAW264.7: NF-κB/TBK1-IRF3/MAPK/COX-2), 40432966 (nhuận tràng chuột), 40460336 (luteolin-7-O-glucoside kháng HCoV-OC43 IC50 2 µM), 40603548 (EO carvone 31,6% kháng khuẩn viêm vú, phá màng), 37895935 (dehydroelsholtzia ketone giãn cơ trơn), 25382222 (O. sanctum vi nang cho heo), 41237583 (E. cypriani vịt Muscovy), 40741360 (EFSA basil = O. basilicum, KHÔNG phải O. gratissimum) |

## Cảnh báo/corrections đã phát hiện trong phiên này (quan trọng cho các nhóm sau)

1. **PMID gợi ý TRONG task brief cũng có thể sai** — task gợi ý 32221055 + 36108156 cho lá ổi-heo nhưng efetch ra "Ocular tumors in children" (Indian Pediatr 2020) và "ctDNA profiling" (Cancer Discov 2022), sai chủ đề hoàn toàn. PMID đúng: 33140438 + 34109234 (tìm qua esearch `Psidium guajava leaf pig`). Quy tắc: efetch MỌI PMID gợi ý trước khi dùng, bất kể nguồn gợi ý.
2. **Bẫy tên "artichoke" trên PubMed**: phần lớn hit là Helianthus tuberosus (atisô Jerusalem, TĂ prebiotic inulin) — KHÁC atiso VN (Cynara scolymus). Kiểm tra latin name trong title trước khi dùng. Tương tự: EFSA "basil tincture" = O. basilicum, không phải O. gratissimum.
3. **Title gây hiểu nhầm loài vật**: 40339260 (Meat Sci) nghe như heo nhưng là THỎ; 40555873 (Trop Anim Health Prod) là cá rô phi. Luôn đọc METHODS của abstract để xác nhận loài.
4. **Lô bài Trung Quốc cùng dải PMID (4260xxxx)**: chạy qua nhiều query khác nhau đều trả về bài không liên quan (Animal Nutrition/Poultry Science special issues) — esummary triage loại sạch.
5. **Liều công thức (25–30 mg/kg TĂ) thấp hơn ngưỡng nghiên cứu** ở hầu hết loại: ổi 50–200, GA 100–2600, Houttuynia 1000, Cynara 15 mg/kg BW — đã note khuyến nghị trong file JSON.
6. **Tên VN ↔ latin**: hương nhu trắng = O. gratissimum, hương nhu tía = E. ciliata; atiso = Cynara scolymus; vằng đắng = Coptosapelta flavescens ("Cao Khai", dân tộc Ninh Thuận); rau đắng đất = Glinus oppositifolius; diếp cá = Houttuynia cordata.
7. Wikipedia vi cho các loài này là stub (không có công dụng dân gian) — không mất thời gian; cần UA header nếu gọi API (403 nếu thiếu).
