# Product Formulation Sheet Pattern

## Worked example: Pig health products (9 tabs, 14 formulas)

Created 21/09/2026 for Kiềm Saphia. Full sheet: https://docs.google.com/spreadsheets/d/<SHEET_ID>/edit

## Tab structure

| Tab | Purpose |
|---|---|
| Hướng dẫn | Guide for pharmaceutical professionals — structure, how to read, how to choose |
| Danh mục hoạt chất | 32 compounds master table (natural + synthetic), 9 columns |
| A1 — Sát khuẩn không khí | 2 formulas + 5-criteria analysis |
| A2 — Xử lý nước uống | 2 formulas + 5-criteria analysis |
| A3 — Tiêu hóa (FCR) | 2 formulas + 5-criteria analysis |
| A4 — Tiêu chảy | 2 formulas + 5-criteria analysis |
| A5 — Hô hấp | 2 formulas + 5-criteria analysis |
| B1 — Môi trường (dung dịch) | 2 formulas + usage guide + 5-criteria analysis |
| B2 — 3-trong-1 (bột) | 2 formulas + 5-criteria analysis |

## Option logic

- **Option A (5 products):** Each target has its own product. Higher per-target efficacy, but 5 products to manage.
- **Option B (2 products):** Environment (liquid, dual-use for air + water) + 3-in-1 powder (FCR + diarrhea + respiratory). Lower cost, easier compliance.

## 5-criteria analysis per formula

Each formula variant must be analyzed on:

1. **Tương thích** — Do ingredients react, separate, precipitate, or neutralize each other? Score: TỐT / KHÁ / TB
2. **Ổn định** — Shelf life? Storage conditions? What degrades it? Score: TỐT (≥6m) / KHÁ (3-6m) / TB (<3m)
3. **An toàn** — Interaction with pig body? LD50? Unsafe concentrations? Score: AN TOÀN / CẨN THẬN / CÓ RỦI RO
4. **Hiệu quả** — Expected disease reduction %? Evidence level? Score: CAO NHẤT (>70%) / CAO (50-70%) / KHÁ (30-50%)
5. **Rủi ro** — Specific side effects? Overdose risk? Production difficulty? Score: THẤP / TB / CÓ

## Google Sheets API workflow

1. `svc.spreadsheets().create()` → get SHEET_ID + URL
2. Rename Sheet1 + create tabs via `addSheet`
3. Populate Master Table with header + 32 rows via `values().update()` with `valueInputOption='RAW'`
4. Populate each product tab with formula tables + analysis tables
5. Format: freeze first row, bold + yellow header, set column widths (200-350px)
6. Guide tab: short, professional, for pharmaceutical professionals

## Key columns in product tabs

Formula table: Chất | % pha | Vai trò | Ghi chú
Analysis table: Tiêu chí | Đánh giá | Mức (score) | Chi tiết

## Compound source codes
- TN = Thiên nhiên (natural)
- TH = Tổng hợp (synthetic)
- TN+TH = Cả hai (both available)

## Target codes (Xử lý column)
- MT = Môi trường (environment)
- FCR = Tăng chuyển hóa (feed conversion)
- TC = Tiêu chảy (diarrhea)
- HH = Hô hấp (respiratory)
- ĐN = Đa năng (general)
