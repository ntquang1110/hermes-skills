# Piglet Diarrhea (PWD) Compound Catalog — verification ledger & schema

Project: `D:/Hermes Proj/piglet-diarrhea-compounds/data/` — catalog hoạt chất trị/ngừa tiêu chảy heo con (post-weaning diarrhea, PWD) cho chủ trại + nhà sản xuất hoạt chất tại VN. Output: JSON tiếng Việt có dấu, mỗi chất 1 object theo schema dưới. Đã hoàn thành: `groupA_botanicals.json`, `groupB_microbes_acids.json`, `groupC_minerals_immune.json`.

## JSON schema (bắt buộc đủ key)
```json
{"id":"slug","name_vi":"...","name_en":"...","latin":"...","category":"Khoáng|Clay hấp phụ|Kháng thể|Phi dược|Thảo dược",
 "summary":"1-2 câu","mechanism":["..."],"evidence_level":"Mạnh|Vừa|Sơ bộ","dosage_ref":"liều",
 "side_effects":["..."],"production":{"method":"...","stability":"...","risks":["..."],"quality_control":"..."},
 "references":[{"type":"paper","label":"Tác giả, Tạp chí, Năm","pmid":"","doi":"","note":"phát hiện chính"},
               {"type":"patent","number":"","title":"","note":""}],
 "verification":"đã verify gì"}
```

## PMID verified (nhóm C, 08/2026 — đã efetch đọc abstract, lưu `_abstracts.json` làm bằng chứng)
- ZnO liều cao: 33670980 (Bonetti 2021, EU cấm 6/2022), 10784192 (Hill 2000: 3000 ppm Zn / 250 ppm Cu)
- Zn hữu cơ/nano: 41922685 (Zn-glycine heo nái), 38200877 (nano-ZnO), 33375418 (Zn-Met vs ZnSO4)
- CuSO4: 37392143 (tỷ lệ Zn/Cu); montmorillonite: 38066981, 22539019, 33793003
- Diosmectite: 23308387 (DS-ZnO 500 mg Zn/kg ≈ ZnO 2250 mg Zn/kg) — KHÔNG dùng 42503678 (sai chủ đề, xem pitfall)
- Zeolite: 14659725; attapulgite/kaolin/than hoạt: 37071083, 36822096, 35517287, 36447022
- IgY: 31286936, 12854815; patent ES2742734T3 (Pantheryx, verify OK qua Google Patents)
- Sữa non bò: 25743486, 34444709; chitosan: 33256856; ORS: 16969915
- Mannose/MOS: 37696080, 3526703; thảo dược tannin: 37170987, 34634977, 41056411, 36098087, 24668769

## Cảnh báo khoa học bắt buộc ghi trong file
- **ZnO**: EU cấm liều 2500-3000 ppm từ tháng 6/2022 (ô nhiễm môi trường + kháng chéo AMR) — ghi trong side_effects/risks, không né.
- **Mannose/MOS**: fimbriae K88 (F4), F18 của ETEC heo là mannose-KHÁNG → mannose chỉ tác động chủng type-1 fimbriae + qua điều hòa microbiota, không phải vạn năng.
- **α-mangostin (măng cụt)**: 24668769 cho thấy làm NẶNG viêm đại tràng chuột → ghi cảnh báo liều.
- Patent không verify được → `number=''` + `note='chưa verify'` (Google Patents hay 503 sau vài query).
