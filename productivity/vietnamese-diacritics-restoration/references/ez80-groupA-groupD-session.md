# Session note — ez80-direct groupA/groupD (2026-09-09)

Source session: restored dấu to 2 JSON files, 10 + 12 rows.
`D:/Hermes Proj/ez80-direct/data/groupA_minerals.json` and `groupD_interactions.json`;
`.raw.json` files are backups — never touch.

## Measured ratios (NFD Mark-strip method)

| File | VI-field before | VI-field after | Whole-file after |
|---|---|---|---|
| groupA_minerals.json | 0.000 (0/3131) | 0.599 (1874/3131) | 0.440 |
| groupD_interactions.json | 0.000 (0/3745) | 0.611 (2287/3745) | 0.438 |

Sibling already-accented files for calibration: groupB 0.509, groupC 0.417 whole-file.

## False-positive catalogue (do not "fix" these)

- `id` slugs: `fe-ket-tua-P-va-khu-H2S`, `tong-hop-lieu-thieu-hut-2025`,
  `D01-mg-ca-ph-struvite-hap-lieu-thuc`, `D11-tea-saponin-gioi-han-ngoai-suy`.
- Key `language`, `id`, `note`, `type`, `pmid`, `doi`.
- English/technical: `trong` ⊂ `control`, `air stripping`, `phase`, `change`,
  `nitrate`, `verified`, `zeolit`, `struvite`, `claim`, `biogas`, `saponin`.
- Units/formulas: `CaCO3` (contains `caco`), `g/L`, `mg/L`, `mmol/L`, `mgP/L`,
  `N-P`, `Fe-P`, `Ca-P`, `K-struvite`, `Fe-Mg`, `sub-MIC`, `Na>K>Ca>Mg`.
- Already-accented words matched by substring: `nhu cầu`, `quy hoạch`, `trực tiếp`.

## Verification queries used

```python
# word-boundary context check before editing any suspect
re.finditer(r'(?<![A-Za-zÀ-ỹ])' + word + r'(?![A-Za-zÀ-ỹ])', text)
# preservation: sorted extracts new-vs-raw for pmid, doi, pubmed_url,
# label/citation, and r'\d[\d.,]*' digit sequences — all must be equal
```

## Domain glossary (chăn nuôi / xử lý nước thải heo / QCVN 62:2025 Cột B)

thả trực tiếp, nước thải heo, nước lỏng sau tách rắn, liều thực 0,15 g/L,
liều thí nghiệm 1–5 g/L, kết tủa, kết tinh struvite, hiệu suất, thiếu hụt,
bổ sung Mg ngoài, hòa tan Mg nội sinh, vỏ hàu (CaCO3→CaO), đệm kiềm/alkalinity,
kéo tụ/lắng, sục khí/stripping, bùn kỵ khí, hầm biogas, đống ủ phân rắn,
qua thức ăn,bay hơi NH3, khóa mùi H2S/FeS, đồng kết tủa Fe-P, Cột B
(BOD5/COD/TSS/T-N/T-P/pH/Coliform), vô hiệu, ô nhiễm, suy luận, đánh giá,
tiêu chí, xử lý, chuẩn hóa saponin/COA.
