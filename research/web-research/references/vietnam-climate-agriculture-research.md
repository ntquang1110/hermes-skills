# Vietnam climate / soil / agriculture research — verified recipe + data bank

Use when researching Vietnamese regional climate, soil, or crop/livestock feasibility
(agrivoltaics "đất dưới tấm pin", vùng miền khí hậu, đất đai) and the answer must carry
real numbers with sources. Validated 2026-09 on the Tây Nguyên agrivoltaics study.

## Recipe (order matters)

1. **Wikipedia weather box = best free structured climate data.**
   Fetch wikitext, parse the `{{Weather box}}` template:
   ```
   curl -s "https://en.wikipedia.org/w/api.php?action=parse&page=<Title>&prop=wikitext&format=json&formatversion=2"
   ```
   Extract lines like `|Jan high C =`, `|Jan mean C =`, `|Jan low C =`,
   `|Jan rain mm =`, `|Jan sun =`, `|Jan humidity =`, `|year rain mm =`.
   Origin is NOAA / Vietnam IBST — credible for planning. If no `year` row for rain,
   sum the 12 months yourself. Pitfalls:
   - Diacritic redirects: `Buon_Ma_Thuot` → `Bu%C3%B4n_Ma_Thu%E1%BB%99t`. On en.wiki the
     title must carry exact diacritics.
   - vi.wiki redirects: `Tây Nguyên` → `Duyên hải Nam Trung Bộ và Tây Nguyên` (combined
     region article). Follow redirect targets in the parse response.
2. **Vietnamese Wikipedia province articles** (`Đắk Lắk`, `Gia Lai`, `Lâm Đồng`...) carry
   Khí hậu / Đất đai / Kinh tế sections with local, citable numbers. Fetch wikitext and
   strip `{{...}}`, `[[...]]`, `<ref>` to get readable prose; grep keywords. Note: the
   `extracts` API sometimes returns empty for vi.wiki — use `action=parse` instead.
3. **Search engines:** curl to `html.duckduckgo.com` and Bing returns bot-challenge/garbage
   pages. Workaround that works: `browser_navigate` to
   `https://html.duckduckgo.com/html/?q=<urlencoded>` — the snapshot returns parsed result
   headings + snippet text, perfect for Vietnamese-language queries. Extract target URLs
   from the `//duckduckgo.com/l/?uddg=` links.
4. **Verify every number before citing:** curl the actual target pages (VN agri sites
   baokhuyennong.com, nongnghiep.farmvina.com, thuysanvietnam.com.vn, caycanhflora.com,
   asahinhatban.com, giathe.vn; FAO static HTML like
   `fao.org/fishery/docs/DOCUMENT/aquaculture/CulturedSpecies/file/en/*.htm`) and grep the
   exact sentence carrying the claim. Only then attached quote→source.
5. **Citation ledger:** use grounded-citations `sources.py`. `add` takes ONE url per call
   with `--title` (multi-url invocation errors). Loop it. `render --replace-in` at the end.

## Data bank — Tây Nguyên (verified, 2026-09)

Sources: en.wiki weather boxes (NOAA/IBST), vi.wiki region+province articles, PVGIS via
Tạp chí Công Thương, Báo Công Thương, FAO.

- **Elevation:** Kon Tum ~500 m; Pleiku ~800 m; Buôn Ma Thuột ~500 m; Mơ Nông 800–1000 m;
  Lâm Viên (Đà Lạt) ~1500 m; Di Linh/Bảo Lộc 900–1000 m. Trung Tây Nguyên (Đắk Lắk) =
  warmest subregion.
- **Temp TB năm:** BMT 23,7 °C | Pleiku 21,9 °C | Kon Tum 23,8 °C | Đà Lạt 18,0 °C.
  Day-night amplitude mùa khô ~12–13 °C, mùa mưa ~6–8 °C. Đà Lạt record low −0,6 °C.
- **Rain:** 1 784 (BMT) / 2 180 (Pleiku) / 1 855 (Kon Tum) / ~1 809 (Đà Lạt) mm/yr.
  Mùa mưa T5–T10 = 80–90% of year; mùa khô T11–T4 (T1–T2 gần như không mưa, khô hạn
  nghiêm trọng). Gia Lai: Đông Trường Sơn 1200–1750 mm, Tây Trường Sơn 2200–2500 mm.
- **Sun & GHI:** 2 000–2 600 h/năm; bức xạ 4,9–5,7 kWh/m²/ngày (PVGIS-CMSAF: 5,1–5,3).
- **Soil:** đất đỏ bazan = Rhodic Ferralsols (nhóm đất đỏ vàng). pH <4,5 (rất chua),
  base saturation <50%, mùn tầng A 4–8%, độ xốp 60–65%, tầng dày, thoát nước nhanh,
  dễ bạc màu/xói mòn → luôn bón vôi khi canh tác. Phổ biến ở độ cao 500–600 m.

## Agrivoltaics / "dưới tấm pin" key facts (with sources)

- Panels che 40–70% nắng → cây nhận ~30–60% ánh sáng. Mưa rơi theo mép mái → dễ trữ nước.
- Giảm bốc hơi 14–29% (California), có nghiên cứu ghi 50% (Arizona) → tiết kiệm tưới.
- Xà lách dưới panel: giữ mát hơn 20 °C, khối lượng tươi +400% so với đối chứng (nắng nóng
  Canada). Rau ăn lá + gia vị (gừng, nghệ) hưởng lợi từ bóng; lúa/đậu giảm năng suất.
- Solar grazing (cừu/dê) là chuẩn quốc tế; bò ít dùng do nguy cơ hư hại trụ/cáp.
- Shade needs per crop (dùng để đối chiếu với độ che của pin):
  - Nấm sò: tối (<5–10% sáng), nhóm lạnh 13–20 °C / nhóm nhiệt 24–28 °C, ẩm kk ≥80%.
  - Gừng: che 25–50% TĂNG năng suất (agriculturereview); mưa 1500–3000 mm, tới 1500 m.
  - Xạ đen: cần bóng râm 30–50%, kỵ nắng gắt (caycanhflora); Gia Lai là vùng phân bố.
  - Đinh lăng: chịu bóng, ưa ẩm, kỵ úng (asahinhatban).
  - Sả, cỏ voi (C4): ưa nắng — chỉ vùng sáng/khe giữa dãy pin; cỏ voi 25–30 °C, đất sâu giàu mùn.
  - Ếch Thái Lan: nước 25–32 °C (tối ưu 28–30 °C), pH 6,5–8,5 (Tạp chí Thủy sản VN).
  - Lươn: ao cần che mát mùa hè (farmvina) — mái pin làm sẵn vai trò này.
  - Cá rô phi: ưa 31–36 °C, chết <11–12 °C (FAO).
- Mọi mô hình thủy sản ở Tây Nguyên gặp ràng buộc số 1: nước cho 5–6 tháng mùa khô.