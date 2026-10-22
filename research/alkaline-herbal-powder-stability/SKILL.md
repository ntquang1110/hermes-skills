---
name: alkaline-herbal-powder-stability
description: "Use when formulating/assessing pH 12-14 herbal powders."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [chemistry, alkaline, herbal, spray-drying, stability, pH, buffer, packaging, vietnamese]
    related_skills: [research-html-catalog, pubmed-evidence-research, livestock-product-lifecycle, vua-kiem-corporate-strategy, grounded-citations]
---

# Bột kiềm thảo dược (pH ≥ 12): độ bền hoạt chất, giữ pH, bao bì

Dùng khi câu hỏi thuộc lớp: *dịch chiết thảo dược ở pH 12–14 đem sấy phun thành bột* — hoạt chất nào
sống được, chọn muối kiềm nào để giữ pH ≥12 lâu dài, vì sao bột mất pH khi lưu hành, bao bì/hạn dùng.
Đã dùng cho: dự án `say-phun-kiem` (nhóm C), họ sản phẩm kiềm (Kiềm Saphia / Vua Kiềm).

Nguyên tắc chung: **pH cao không phá mọi thứ như nhau** — nó phá đúng những nhóm chức có pKa thấp hơn
pH môi trường, và **bền hóa học ≠ giữ được hàm lượng**. Luôn tách 3 câu hỏi: (a) hóa học ở pH 12–14,
(b) mất mát trong buồng sấy, (c) mất pH/hoạt chất trong 24 tháng lưu hành.

## Quy trình 5 bước

1. **Quy về pKa.** Nhóm chức nào có pKa < pH môi trường thì bị deprotonat, và dạng deprotonat là dạng
   phản ứng mạnh nhất (phenolat → quinon; ascorbat dianion → oxy hóa). Tốc độ phản ứng tăng **theo hàm
   mũ với pH**, nên 1 đơn vị pH quan trọng hơn 10 °C.
2. **Xếp hạng hoạt chất** (xem `references/ph12-active-stability.md`): alkaloid amoni bậc bốn ≈ bền nhất
   → alkaloid lactam/amin bậc ba → aglycon saponin → polyphenol/flavonoid/tanin ≈ kém nhất (tanin ngưng
   tụ oxy hóa–trùng hợp hóa nâu; tanin thủy phân còn bị cắt liên kết depside).
3. **Chọn kiềm theo pKa của cặp đệm so với pH mục tiêu, KHÔNG theo "độ mạnh base".** Chỉ cặp đệm có pKa
   trong ±1 đơn vị quanh pH đích mới giữ được pH khi bị CO₂ tấn công. Hệ cacbonat (pKa2 10,33) ⇒ trần
   ~11,5; muốn ≥12 phải dùng phosphate (pKa3 12,35) và/hoặc silicat. NaOH/KOH cho pH cao nhưng **không
   có đệm** ⇒ pH "không phanh", trôi tự do. Bảng đầy đủ: `references/alkali-salt-and-packaging.md`.
4. **Định lượng, đừng chỉ định tính.** Ba phép tính luôn phải có:
   - *Ngân sách CO₂*: 1 L khí 30 °C có ~0,017 mmol CO₂; tính lượng khí trao đổi qua 24 tháng rồi so với
     số mmol OH⁻ có trong bột. Vì pH là thang log, trong bao KÍN mất pH do CO₂ khí quyển rất nhỏ.
   - *Quan hệ pH ↔ liều kiềm*: pH 12 cần 10 mmol OH⁻/L; đo ở 1 % w/v (10 g bột/L) ⇒ bột phải chứa ~4 %
     NaOH-đương lượng hoặc ~7–8 % Na₃PO₄. Đo ở 5 % w/v thì yêu cầu giảm 5 lần.
   - *Dung lượng đệm, không chỉ pH*: Ca(OH)₂ đạt pH 12,4–12,6 nhưng độ tan 1,73 g/L ⇒ đệm ≈ 0, sụp ngay
     sau một lượng CO₂ nhỏ (CaCO₃ không tan).
5. **Dự đoán thất bại vật lý trước thất bại hóa học.** Chất chảy nước (deliquescence) là kẻ giết thật:
   NaOH rắn chảy ở RH ~10–15 %; khi có màng nước, cacbonat hóa nhanh gấp nhiều lần. Mục tiêu: aw ≤ 0,15–0,20,
   độ ẩm ≤ 1 %, màng nhôm nhiều lớp (Al ≥ 9 µm, WVTR < 0,1 g/m²·ngày).

## Bẫy đã gặp thật (đừng lặp lại)

- **KHÔNG đề xuất ascorbat làm chống oxy hóa cho hệ kiềm** — ở pH 12–14 nó nằm ở dạng dianion, chính là
  dạng bị O₂ oxy hóa nhanh nhất (tự phá trước, còn có thể thành pro-oxidant). Chống oxy hóa đúng cho hệ
  kiềm: **sulfit/metabisulfit** (còn khử quinon làm nhạt nâu, có trong tài liệu chống hóa nâu),
  **Na₄EDTA** (chelat kim loại, chú ý Ca/Mg cạnh tranh), **N₂ flush**. Tocopherol chỉ dùng cho pha dầu —
  phenolat tocopherol bị oxy hóa nhanh trong nước kiềm.
- **Rủi ro Maillard bị đánh giá thấp**: acid amin tự do + đường khử trong dịch chiết, ở pH > 10 phản ứng
  được base xúc tác mạnh (kèm caramel hóa đường và β-elimination của pectin). Hóa nâu trong sấy phun
  thường là Maillard/oxy hóa phenol, không phải "cháy".
- **Chỉ tiêu "pH ≥ 12" phải kèm nồng độ pha.** pH bột ≠ pH dung dịch 1 % ≠ 5 %. Thiếu nồng độ là nguyên
  nhân gốc của phần lớn tranh cãi "đạt/không đạt".
- **Độ bền hóa học ≠ giữ được hàm lượng.** Menthol/limonene bền về pH nhưng mất 50–95 % khi sấy nếu không
  có chất mang; thymol/carvacrol ở pH 12–14 chuyển thành phenolat (ít bay hơi hơn nhưng dễ oxy hóa hơn).
- **Đừng hứa "giữ pH 24 tháng" mà thiếu bộ ba**: đệm pKa≈12 (phosphate ± silicat) + bao kín (màng nhôm,
  hút ẩm) + aw thấp. Nếu người dùng mở gói nhiều lần, nói thẳng pH sẽ trôi về ~10,5–11,5 và đề xuất
  dạng 2 ngăn / gói liều đơn / dạng dung dịch.
- **Gói hút CO₂ gốc Ca(OH)₂ nhả NƯỚC** (Ca(OH)₂ + CO₂ → CaCO₃ + H₂O) ⇒ phải ghép với hút ẩm, không dùng
  một mình.
- **Đệm phosphate/silicat tủa với Ca²⁺/Mg²⁺** ⇒ kiểm độ cứng của nước/dịch trước khi chốt công thức.
- Kiểm tra tính tương thích: muốn đạt pH cao với lượng kiềm thấp thì phải giảm "trần" mong đợi — không có
  công thức nào vừa ít kiềm vừa pH ≥ 12 ở nồng độ pha loãng.

## Liêm chính nguồn (Quang, bắt buộc)

- Hằng số hóa học (pKa, Ksp, độ tan) lấy từ nguồn tra được và ghi rõ; giá trị thương mại/đại chúng
  (pH dung dịch của một muối) phải ghi `note='chưa verify'` nếu không có sổ tay/nguồn sơ cấp.
- Phân biệt rõ **dữ kiện tra được** vs **suy luận của báo cáo** (ví dụ: "phosphate là ứng viên số 1" là suy
  luận từ pKa3 + pH đo được ⇒ phải nêu là cần xác nhận thực nghiệm trong nền bột thảo dược).
- Mọi phép tính tự làm (ngân sách CO₂, liều kiềm theo nồng độ pha) ghi nhãn *tính toán*, không gán PMID.
- Xác minh PMID/DOI qua PubMed E-utilities trước khi trích (xem `pubmed-evidence-research`).

## Support files

- `references/ph12-active-stability.md` — ma trận độ bền từng nhóm hoạt chất ở pH 12–14 (cơ chế + PMID đã
  verify), nhóm chống oxy hóa thay thế, Maillard.
- `references/alkali-salt-table-and-packaging.md` — bảng 11 muối kiềm (pH 1 %/10 %, pKa đệm, dạng ngậm
  nước, độ hút ẩm), thang chẩn đoán pH khi pha lại, phép tính ngân sách CO₂, thông số bao bì và cách
  phân biệt lỗi bao bì vs lỗi công thức.
