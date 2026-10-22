# EZ80 khoáng thả TRỰC TIẾP vào nước thải heo — dose-to-water + struvite/HAP stoichiometry (verified 2026-09-09)

**Sản phẩm:** KIỀM EZ TÁI SINH 80 (TCCS 06:2025/MNĐV) — Ca ≥49.000, Fe 15.000, Mg 8.500, K 5.300, Mn 750, Zn 50 mg/kg; vỏ hàu (CaCO3) + cao lanh + diatomite + mùn khoáng + talc + zeolit. Liều thực 150 kg/1000 m³ = **0,15 g/L**; liều thí nghiệm 1–5 g/L. Mục tiêu QCVN 62:2025 Cột B: BOD5 ≤60, COD ≤150, TSS ≤100, T-N ≤60, T-P sông ≤14 (hồ ≤3), pH 6–9, coliform ≤5000 — verified PDF 7 trang `xuanthien/QCVN62_2025.pdf`.

## Công thức liều (đã dùng trong deliverable, verify bằng tính toán)

```
mg/L = (mg/kg trong sản phẩm) × (liều g/L) / 1000
mmol/L = mg/L / M (M: Mg 24.305, Ca 40.078, Fe 55.845, P 30.974)
```

| Liều | Mg mg/L (mmol) | Ca mg/L (mmol) | Fe mg/L (mmol) |
|------|---------------|---------------|---------------|
| 0,15 g/L (thực) | 1,28 (0,052) | 7,35 (0,183) | 2,25 (0,040) |
| 1,0 g/L | 8,5 (0,35) | 49 (1,22) | 15 (0,27) |
| 5,0 g/L | 42,5 (1,75) | 245 (6,11) | 75 (1,34) |

**Nhu cầu ion cho TP:** TP 60 mgP/L = 1,94 mmol/L → cần Mg 47 mg/L (1:1 struvite) hoặc Ca 130 mg/L (1,67:1 HAP Ca5(PO4)3OH). TP 150 mgP/L → 118 mg Mg hoặc 324 mg Ca. Vậy liều thực **thiếu 97% Mg, 94% Ca**; liều 1 g/L còn thiếu ~60%; liều 5 g/L đủ cho TP ≤60–80 mgP/L nếu pH 8,5–9 và N/P ≥2–3.

## Cơ chế đã verify (15 PMID, esummary+efetch 09/09/2026)

- **Mg → struvite MgNH4PO4·6H2O** (Mạnh): MgO 0,75 g/L (~455 mg Mg/L) ở 40°C + sục khí 0,48 m³/h·L 3h thu 88% NH4 + 96% TP (30632036); pH 7–9,5 đạt 80–95%, pH 6 chỉ ~50% (27208994); Langmuir 635 mgP/g trên vật liệu Mg-magnetic (38008222); 20 g/L zeolite Na-P1 + 4 mM Mg → 65% NH4/92% PO4 (27533361); FeCl3 tiền xử lý hòa tan Mg nội sinh → không cần Mg ngoài nhưng chỉ loại 15–17% NH4 (15974270).
- **Cạnh tranh ion:** Ca2+/Fe3+ ức chế P mạnh hơn Na+; propionate/glutamate/humate > tinh bột/tetracycline (41880949); hữu cơ làm chậm động học nhưng tăng cỡ tinh thể (26495935); tối ưu Mg:Ca ≥2,25:1, N:P ≥3:1, khuấy 45–90 rpm (23270959).
- **Ca vỏ hàu → Ca-P/HAP:** pH 9, 200 rpm 600s, Ca 207 + Mg 123 mg/L loại 92% P thành ACP + 1,65% struvite (32416395); OSP CaCO3 sống chỉ hấp phụ pH 5–7, nung 800–1000°C → CaO tan Ca vượt trội, cơ chế keo tụ (37532535).
- **Fe → FeS (-87% VSC) + FePO4:** FeCl3 -87% H2S, Al2(SO4)3 +920% H2S, Mg(OH)2 vô hiệu+gây bọt (26260964); review FeCl3 keo tụ COD/H2S, tăng BET biochar (36858210); CP/ATP 0,25 g/L + Fe 2mM (~112 mg Fe/L) loại P cao ít phụ thuộc pH (37229855); CIMBC Fe/Mg 1:2 nung 500°C 1 g/L pH7 → 95,7 mgN/g + 101 mgP/g (38183541).
- **K/Mn/Zn ở liều EZ80:** Không có bằng chứng trực tiếp — K tan, K-struvite chỉ khi NH4 thấp (32810833 gián tiếp); Mn2+ vô hoạt yếm khí, Zn 0,007–0,25 mg/L < ngưỡng ức chế 10 mg/L — ghi honest gap.

## Pitfalls mới (bổ sung cho SKILL.md)

1. **Đừng nhầm CaCO3 sống với CaO nung:** tan Ca và cơ chế khác nhau hoàn toàn — CaCO3 pH 5–7 hấp phụ, CaO pH 8,5–9 keo tụ; dùng sai liều tính thiếu 3–5 lần.
2. **Bài toán liều phải tính trước khi claim:** luôn tính mg/L và mmol/L từ TCCS ra nước thải và so với stoichiometry Mg:P 1:1 / Ca:P 1,67 — liều thực 0,15 g/L luôn thiếu >90% cho TP điển hình 60–150 mgP/L.
3. **Cạnh tranh Ca/Fe giết struvite:** nếu sản phẩm giàu Ca (vỏ hàu) mà không bổ sung Mg, P sẽ đi vào ACP/brushite không thu NH4 — phải kiểm Mg:Ca inline.
4. **TSS ảo sau thả:** khoáng mới thả làm TSS tăng 0,15–5 g/L trước lắng; phải lắng ≥2–4h mới đo TSS thực — không đo ngay sau thả.
5. **QCVN 62:2025 không có dòng NH4 riêng** — chỉ T-N; đừng thêm NH4 vào Bảng 1.

## Deliverable

`ez80-direct-mineral/data/group_mineral_direct.json` — 10 rows, 23 refs/15 PMID duy nhất, mỗi row = 1 khoáng × 1 cơ chế, evidence_level Mạnh/Vừa/Sơ bộ/Không có bằng chứng trực tiếp.

## Query pattern tái dùng

```
struvite+magnesium+swine+wastewater
dolomite+OR+calcium+AND+magnesium+AND+swine+wastewater
iron+chloride+hydrogen+sulfide+anaerobic+digester
oyster+shell+powder+AND+phosphate+removal
```
