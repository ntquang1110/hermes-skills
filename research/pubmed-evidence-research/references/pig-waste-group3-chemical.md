# Pig wastewater treatment — Group 3 chemical research (verified source bank)

Captured 2026-08-12 from the pig-waste-treatment Group 3 session (ammonia stripping /
struvite / H2SO4 neutralization / QCVN 62 / H2S biogas / patents).
**Deliverable `D:/Hermes Proj/pig-waste-treatment/data/group3_chemical.json` was NOT
written** (agent hit the tool-iteration limit right before assembly). All data below IS
verified — a future session can finish the JSON without re-verifying. Schema in the
skill's SKILL.md; `evidence_level` values `Mạnh|Vừa|Sơ bộ`.

## Verified PMIDs + DOIs (esearch → esummary → efetch, all efetch-confirmed)

| Topic | PMID | Year/J | DOI | What the abstract showed |
|---|---|---|---|---|
| Ammonia stripping + struvite combo | 30632036 | 2019 ESPR | 10.1007/s11356-019-04153-x | MgO as struvite precipitant + pH adjuster; 40 °C, 0.48 m³ h⁻¹ L⁻¹ aeration, 3 h; N/P/COD removal rises with MgO dose |
| Air stripping optimisation | 32721283 | 2020 J Environ Manage | 10.1016/j.jenvman.2020.110692 | 27 batch tests on real swine wastewater; pH 8/10, 40/60 °C, air 0/1/5 L L⁻¹ min⁻¹; >80% TAN removed in ~50% of tests; (NH4)2SO4 recovered |
| Stripping + anaerobic digestion | 34516343 | 2021 Environ Technol | 10.1080/09593330.2021.1980826 | Microwave-irradiation-assisted ammonia stripping improves mesophilic AD of swine wastewater |
| P+NH4 removal (magnesium-loaded) | 38008222 | 2024 Bioresour Technol | 10.1016/j.biortech.2023.130103 | Simultaneous phosphate+ammonium removal from swine wastewater |
| Pilot pig-slurry N recovery | 39303586 | 2024 J Environ Manage | 10.1016/j.jenvman.2024.122597 | 2-yr on-farm pilot: microfiltration + membrane stripping + RO; up to 56% N as ammonium sulphate; 12.49 kWh/kg NH3 |
| Struvite chemical-addition order | 27208994 | 2016 J Environ Manage | 10.1016/j.jenvman.2016.05.009 | Optimising Mg/P/NH4 addition sequence for struvite P recovery |
| Struvite electrochemical | 34436357 | 2021 Membranes | 10.3390/membranes11080594 | Organic substances effect on electrochemical struvite precipitation |
| Livestock effluent → water quality | 33959840 | 2021 ESPR | 10.1007/s11356-021-14284-9 | Pig/cow/poultry farm effluent impacts on receiving water |
| FeCl3 + biochar, biogas | 36858210 | 2023 Sci Total Environ | 10.1016/j.scitotenv.2023.162437 | Biochar + iron chloride for contaminant removal + biogas production (H2S context) |
| Chlorine + UV disinfection | 35162659 | 2022 IJERPH | 10.3390/ijerph19031636 | Conventional disinfection vs antibiotic-resistance control in wastewater |
| Ammonia → ammonium sulphate (membrane) | 39997688 | 2025 Membranes | 10.3390/membranes15020062 | Membrane contactor recovery of ammonia as ammonium citrate/sulphate |

Working keyword queries: `ammonia stripping swine wastewater`, `struvite recovery
livestock wastewater`, `struvite swine wastewater ammonium`, `NaOH pH ammonia removal
wastewater` (noisy — prefer the first two), `hydrogen sulfide biogas removal` (257 hits,
title-screen), `livestock wastewater UV disinfection`.

## QCVN 62 — verified tables (both sourced from primary text)

**QCVN 62-MT:2016/BTNMT, Bảng 1** (Thông tư 04/2016/TT-BTNMT; verified from the official
English translation on english.luatvietnam.vn). NOTE: **no Tổng P (phosphorus) column in
2016**. A=6-9 pH, B=5.5-9 pH; BOD5 40/100; COD 100/300; TSS 50/150; Tổng N 50/150; Tổng
Coliform 3,000/5,000 MPN-100mL (all mg/L except pH/coliform).

**QCVN 62:2025/BTNMT, Bảng 1** (Thông tư 04/2025/TT-BTNMT — **replaced 2016**; verified
from the signed PDF `QCVN62_2025_BTNMT_921506.doc`/pdf mirror, 7 pages, extracted with
pymupdf). 3 columns A/B/C, trang trại scale: pH 6-9 all; BOD5 ≤40/≤60/≤100; COD ≤65/≤150/
≤250 (or TOC ≤35/70/130); TSS ≤40/100/120; T-N ≤20/60/120; **T-P (NEW in 2025) — depends
on receiving water**: hồ/ao/đầm ≤2.0/3.0/4.0, sông/suối/kênh/mương ≤4.0/14/30, biển
≤4.0/14/40; Tổng Coliform ≤3000/5000/5000.

## Retrieval paths (what worked / what blocked) — Vietnamese regulatory docs

WORKED:
- **english.luatvietnam.vn** — official English translations of Circulars (incl. the
  QCVN-carrying Thông tư) fetch fine with plain urllib/curl; full parameter tables in the
  HTML. Fastest path to QCVN values.
- **Bing search in browser + `browser_console` DOM extraction** of organic results:
  `Array.from(document.querySelectorAll('#b_results > li.b_algo')).map(li => ...)` — the
  compact snapshot hides results; this extracts title+url+snippet reliably. Compact
  `browser_snapshot` shows only the header nav.
- **Gov/mirror PDFs** found via Bing (xulymoitruong.com, sonnmt.langson.gov.vn,
  cdn.thuvienphapluat.vn ...) download via curl; extract text with pymupdf:
  the hermes venv `python` has no pip → use the interpreter that does (`pip install
  pymupdf`, run with `python3.14` / `py -0` to list interpreters). `import fitz` works.

BLOCKED (plan around these):
- thuvienphapluat.vn → Cloudflare challenge (403), even in the browser.
- vanban.chinhphu.vn → HTTP 200 but JS-only shell, no document text in static HTML.
- luatvietnam.vn deep URLs → 404 unless the exact slug from a search engine is used.
- Direct `curl` of Google Patents XHR → HTTP 503; browser → "Sorry... automated queries"
  page. FreePatentsOnline → connection reset; Espacenet → 403; WIPO Patentscope
  `result.jsf` returned HTTP 200 (parse not completed; body may be brotli-encoded —
  `pip install brotli`). **No patent number was verified → all patent fields in the
  deliverable must be `"number":"", "note":"chưa verify — Google Patents 503"`.**

## Chemistry core facts for the deliverable (from abstracts read; textbook parts flagged)

- NH3 stripping: NH4+ ⇌ NH3 + H+ (pKa ≈ 9.25); NaOH → pH 10-11 drives >90% to free NH3;
  aeration + 40-60 °C raises mass transfer; scrub with H2SO4 → (NH4)2SO4 fertiliser.
  NaOH vs Ca(OH)2/KOH trade-off is textbook knowledge [unverified in this session]:
  Ca(OH)2 cheaper but slow pH rise, CaCO3/Ca3(PO4)2 scale, hard to hold pH ≥10; KOH
  expensive, K+ surplus harms soil; NaOH = standard choice.
- Struvite: Mg2+ + NH4+ + PO4 3- → MgNH4PO4·6H2O, optimum pH 8.5-9.5, Mg source MgO/MgCl2,
  slow-release N+P fertiliser.
- Final H2SO4 step: neutralises excess NaOH to pH 6-9 (QCVN) and can double as
  (NH4)2SO4 recovery; HCl more corrosive/expensive, CO2 too weak for the buffered liquor.
- H2S in biogas: FeCl3/FeCl2 dosing precipitates FeS in digester; bio-trickling filter as
  polishing step. Disinfection: UV or chlorine (PMID 35162659).
