---
name: spray-dry-powder-formulation
description: Screen carriers/wall materials for spray-dried powders.
---

# Spray-dry powder formulation & carrier/wall-material screening

Trigger: evaluate/rank **chất mang / carrier / wall material / tá dược** for spray drying; feed liquid with extreme chemistry (pH ≥ 12 or ≤ 3, very high TDS, free alkali, Ca²⁺/Mg²⁺, Cl⁻); powder must survive 24 months at 30 °C/75% RH (VN climate zone IVB); "which material doesn't cake / doesn't brown / is legally a food additive in VN"; emit a `group*.json` dataset for the `say-phun-kiem` report builder.

## The 3-axis screen (never rank on one axis)
1. **Feed chemistry at process pH** — what survives: glycosidic/peptide bond cleavage, *peeling* from reducing ends, β-elimination, **loss of FUNCTIONAL groups**, ion interactions (Ca²⁺ + alginate/pectin → gel), alkaline dissolution of oxides/silicates/aluminosilicates.
2. **Thermal + moisture stability of the dry powder** — Tg dry AND Tg at working moisture, sorption isotherm, DRH vs storage RH.
3. **Legality** — VN additive list (TT 24/2019/TT-BYT, INS codes) cross-checked against Codex GSFA/EU; distinguish *food additive* vs *food ingredient* vs *pharma excipient*.
Optional 4th axis for corrosive feeds: **equipment material compatibility**.

**Key insight from practice:** with a few-seconds residence, polysaccharide backbones mostly SURVIVE pH 12–14 — what fails is the functional group (OSA ester saponified, pectin methyl ester → β-elimination, CMC carboxymethyl → depolymerisation) and the alkali reserve. Score "does it lose its function in alkali", not only "does the chain break".

## Scoring rubric (reusable; 0–5 per criterion, 5 = best/safest)
| criterion | key | weight | 5 means |
|---|---|---|---|
| Bền kiềm (mạch + nhóm chức) | kiem | 0.18 | inert / no functional loss |
| Nhiệt + Tg ở độ ẩm làm việc | nhiet | 0.18 | Tg high enough at 75% RH |
| Hút ẩm / DRH | am | 0.12 | no deliquescence, low uptake |
| Maillard safety | maillard | 0.10 | non-reducing, no free amine |
| Encapsulation / volatile retention | bao | 0.12 | film-forming + surface active |
| Giữ pH khi pha lại | giu_pH | 0.10 | supplies alkali reserve, no acid generation |
| Pháp lý VN | pl | 0.10 | permitted, INS code |
| Tương thích thiết bị | tb | 0.10 | inert, adds no stray ions |

`diem_tong_100 = Σ(score×weight)/5×100`; bands **A ≥75, B 60–74, C 45–59, D 30–44, E <30**; `rating = round(diem_tong/20)`.
Run `scripts/score_matrix.py` for totals/bands/ratings — do not hand-arithmetic 30 rows.

**Always apply an explicit OVERRIDE on top of the mechanical score** when one fact is decisive (melts at 32 °C; gelates on Ca²⁺; no legal status) and record why. A high mechanical score with one fatal flaw is still a NO — put that in `xep_loai`, keep `diem_tong_100` for transparency, and mark the row as overridden.

## Thresholds worth memorising
- No caking: **Tg at storage moisture ≥ T_storage + 20–30 °C** ⇒ at 30 °C, Tg ≈ 55–60 °C at 0.75 a_w. The 20–30 °C figure is an engineering rule of thumb — label it as such, never as a cited constant.
- Only crystalline solids have a **DRH**; amorphous carriers have none — they sorb water progressively and Tg slides. Report "vón/dính" for amorphous, "chảy nước" for crystalline.
- Free **NaOH/KOH is the #1 deliquescence risk** in a "pH ≥ 12" powder (DRH ~10% RH) → substitute a **carbonate/bicarbonate alkali reserve** (Na₂CO₃ DRH ≈ 84.5%, hydrates from ~72% RH) to keep pH ≥ 12 on reconstitution without liquefying at 75% RH.
- pH ≥ 12 is intrinsically pro-Maillard (amine deprotonation, pKa 9–10.5). "Keep pH high for the active" conflicts with "suppress Maillard" — state the trade-off instead of promising both.
- Aluminosilicates (kaolin, bentonite, zeolite) **dissolve in hot concentrated alkali** (zeolites are synthesised in 1–5 M NaOH) → release Al and exchange cations. Fumed silica/calcium silicate also dissolve in the feed at pH 12–14 → **dry-blend post-dry only**.
- Ester-type encapsulation aids (n-OSA starch) lose OSA by saponification → published retention figures do not transfer to an alkaline feed.
- Equipment: 316L fine for dilute caustic below ~80 °C (caustic SCC above); NOT 304, aluminium (oxide stable only pH 4–9), soda-lime glass (attacked pH > 9), or alumina ceramic nozzles.

## Verification discipline (non-negotiable for this class)
- Never invent a Tg, DRH, PMID, DOI or URL. Where a number has no source, write `note='chưa verify'` **at that field**, and list it in a per-question `chua_verify` array.
- Separate "value with a source" from "range from a trade/overview page" from "order of magnitude I recall". Only the first counts as verified.
- Routinely flag as unverified: Tg of maltodextrin DE10/DE20, gum arabic, β-CD/HP-β-CD, CMC, gelatin, n-OSA starch; DRH of KOH/NaOH, trehalose, alginate, CMC; the pH-acceleration factor for Maillard; the exact TT 24/2019 clause/row per INS.

## Output conventions
- Vietnamese **with full diacritics**. Every row's reason must name the concrete bond/reaction/mechanism — never generic filler.
- Deliver the machine-readable dataset AND a short ranking + recommendation block; open the final answer with file path, counts, top candidates, eliminations, and caveats.

## Project pipeline: `say-phun-kiem` dataset → HTML report
`D:/Hermes Proj/say-phun-kiem/` — `build.py` globs `data/group*.json`, `pick()`s the list under keys `items|rows|lines|compounds|data|list`, normalises, injects into `template.html` at the `__DATA__` marker → `say-phun-kiem.html`.
Non-obvious contract (details in `references/json-dataset-for-html-report-builder.md`):
- Fields consumed: `id, name_vi, name_en, cat, role, verdict, why, ph12, thermal, storage, evidence_level, verification, rating(0–5 int), references[{type,label,pmid,doi,number,note}]`.
- **Extra fields are silently dropped** by `normalize()` — anything a reader must see has to live inside a whitelisted field.
- `cat` must be the **group token** (`chat_mang` → chip "Chất mang"), not a chemistry category; keep the chemistry category in a separate key (`nhom_hoa_hoc`).
- Never leave stub rows with fake refs (`PMID 00000000`) in `data/` — they render as real data. Check for and report them.

## Pitfalls
- "Theo đúng schema bên dưới" with no schema attached: **do not guess** — `ls` the exact **output directory** for a sibling stub/sample (a `price_stub.json` next to the target file often *is* the schema; a project-wide `*schema*` grep misses it), then read the consumer code (`build.py`, `template.html`). Once found, conform on the core keys exactly (same names/types) and keep richer data in ADDITIVE keys — never rename a required key. Details + the `price_T2.json` case in `references/json-dataset-for-html-report-builder.md`.
- **No stub on disk ⇒ read the CONSUMER, not the sibling files.** When several sub-agents write `price_T1/T2/T3.json` in parallel, each invents a schema; the sibling files are guesses. The merge module (`price_lib.py`, or `build.py`) defines the accepted key names in its `ALIAS_*` tuples — that IS the authoritative schema. Read it top-to-bottom before writing a single row, and **trust the implementation over its comments**. Exact contract + 6 parser traps (3-decimal numbers silently read as thousands; per-item `ty_gia_vnd_usd` defaulting to 26300 via `meta` being ignored; numeric USD values tripping `can_xac_nhan_don_vi_gia` and being dropped from scoring) in `references/price-dataset-consumer-contract.md`.
- **Always re-read your own merged output for absurd values before declaring done** — e.g. a "bulk" price of 77.100 đ/kg that is really a lab-grade listing, or a 1000×-inflated number from the decimal trap. Run the consumer's own loader and eyeball every number; a clean parse is not the same as a correct value.
- Scoring insoluble materials (MCC, CaCO₃, silica) as if they were soluble carriers: split the verdict into "in-feed carrier" vs "dry-blend anti-caking/filler".
- Treating "food ingredient" (trehalose, inulin, WPI, gelatin) as equivalent to "permitted additive"; never cite an INS code you have not cross-checked.
- Trusting encapsulation efficiency measured in neutral media for a pH 12–14 feed.

## References
- `references/carrier-chemistry-alkaline-ph12.md` — sourced knowledge bank: Tg table, DRH, alkaline-degradation ranking, Maillard reducing/non-reducing lists, corrosion materials, INS/legality status.
- `references/json-dataset-for-html-report-builder.md` — reverse-engineering a schema from a project's builder script + the exact `say-phun-kiem` contract.
- `references/carrier-price-sourcing-vn.md` — sourcing GIÁ chất mang cho VN: kênh tra giá theo nhóm (Shopee/Kamereo vs nhà phân phối vs Tridge/E1450 vs lab), chiến lược **proxy** cho nhãn hiệu không có giá công khai (Hi-Cap 100, Capsul, Pure-Cote, HP-β-CD), bảng giá neo 22/10/2026, quy tắc ghi `do_tin_cay` + tỷ giá USD/VND.
- `references/price-dataset-consumer-contract.md` — hợp đồng key của consumer `price_lib.py` (module gộp mọi `data/price/price_*.json` vào bảng xếp hạng) + **6 bẫy parser đã trả giá thật**: số có đúng 3 chữ số thập phân bị đọc thành phân nghìn (`0.207` → 207, sai 1000×), `ty_gia` đọc theo TỪNG item (mặc định 26300), giá USD dạng số bị bật cờ `can_xac_nhan_don_vi_gia` và bị LOẠI khỏi điểm giá, `_spread` đọc `min`/`max` chứ không phải `price_vn_min`/`price_vn_max`, dict cho `thu_hoi_pct`/`ee_pct` mới mang được ghi chú + recipe verify bằng `price_lib.attach()`.
- `scripts/score_matrix.py` — compute diem_tong_100 / rating / band from a sub-score table.
