# Group-JSON conformance to build.py (validated: say-phun-kiem group C, 52 rows, 22/10/2026)

Applies to every `D:/Hermes Proj/<project>/` catalog project that ships `build.py` + `template.html` + `data/group*.json`.

## 1. When the schema text is missing, derive it (do not invent)

Ask in this order — 2 file reads and you have the contract:

1. **`data/group0.json`** — the demo/placeholder file kept in these projects IS the schema documentation:

```json
{"meta": {"group": "..."},
 "lines": [{"id","name_vi","name_en","cat","role","rating" (int),
            "verdict","why","ph12","thermal","storage","evidence_level",
            "references" (list of strings), "verification"}]}
```

2. **`build.py`** — function `norm_row()` is the contract. It accepts `{"lines":[...]}` **or** `{"items":[...]}` **or** a bare list; anything else loads as 0 rows without error. Column mapping (`pick()` = first non-empty):

| HTML column | accepted JSON keys |
|---|---|
| name | `name_vi\|ten\|ten_vi\|name\|element_vi`, `name_en\|ten_en\|element` (at least one required, else row is dropped) |
| category chip | `cat\|nhom\|group`, must be in `ORDER` after `CAT_MAP` slugging, else falls back to a per-FILE `meta.group` keyword match (`KHOÁNG/MUỐI→Muối kiềm`, `HOẠT CHẤT→Hoạt chất`, `CHẤT MANG→Chất mang`, `THIẾT BỊ→Thiết bị`) — so a mixed group (actives + salts + packaging) **must** set `cat` per row. |
| verdict | `verdict\|ket_luan\|ly_do_ngan` |
| why | `why\|giai_thich\|mechanism` |
| ph12 / thermal / storage | `ph12\|o_ph12\|do_ben_ph12`, `thermal\|nhiet\|trong_buong_say`, `storage\|bao_quan\|luu_hanh` |
| extra block | whitelist only: `nhom_hoa_hoc, xep_loai, canh_bao, maillard, phap_ly_vn, legal_vn, tg_kho_C, hut_am_drh, trong_so_tinh_diem, ket_luan_1_dong, effect, mechanism, route, approval, ksp, side_effects, dosage_ref, element` |

`ORDER` (sort priority) = `Chất mang, Muối kiềm, Hoạt chất, Hóa học pH 12, Kim loại hiếm · thuốc người, Pháp lý, Bối cảnh VN, Thiết bị`. Use a valid `cat` for every row — that is what controls where the row lands.

`norm_refs()` turns references into strings by taking `url|doi|pmid|cite|title` from each dict and **drops dicts that only have `label`**. So always hand it pre-formatted strings (`"PMID 41140573 · <title>"`).

## 2. Write strategy for a large row set (fragments, then merge)

A single huge `write_file` can come back truncated mid-string. Robust pattern used here for 52 rich rows:

- Write rows as **JSON-array fragment files** (`data/_rows/B01.json`, `_partA.json`) kept ≤ ~6 KB each, and write them **one per tool call**.
- `.json` writes are lint-checked, so truncation is *self-detecting*: a cut file ends with a literal `[truncated]`-style token and fails JSON parse. If the lint reports `invalid control character` / unexpected end, re-emit that file smaller (split the row range). Non-JSON scratch files (`.py`) do **not** get that check — never trust one without running tail/grep.
- Before merging: `grep -rl "truncated" data/` must be empty; then `assert len(rows) == <expected>`, then merge.
- Merge with a transform script saved **inside the project** (`data/_build_<group>.py`) so the raw fragments stay reproducible. Note `build.py` globs only `group*.json`, so `_partA.json` / `_rows/` do not interfere.

## 3. Merge/transform skeleton (reusable)

```python
D = r"D:/Hermes Proj/<project>"; DATA = os.path.join(D, "data")   # never derive from __file__ when the script lives elsewhere
CAT  = {"A. Tannin": "Hoạt chất", "C. Muối kiềm — bảng": "Muối kiềm", "D. Bao bì & hạn dùng": "Thiết bị"}
SCORE = {"A01-...": 1, "C08-...": 5}          # explicit {id: int}; document the meaning
def ref_str(x):  # dict -> "PMID n · label" / "label · url"
def fmt_side(items):  # list[dict(type,label,note)] -> "(type) label · note  |  ..."  ← NEVER leave a raw Python dict in text fields
def dpick(d, *names, default=""):  # first non-empty of candidate source keys
line = {"id","name_vi","name_en","cat","role","rating","verdict","why","mechanism","ph12","thermal","storage",
        "evidence_level","references" (formatted strings), "verification", ...whitelisted extra keys...}
```

Then fill the display gaps honestly instead of leaving blanks — a short, true fallback beats an empty column:
`thermal` default = `"Giọt chịu 80-100 °C trong vài giây ở buồng sấy; hư hại thực tế xảy ra ở pha lỏng pH cao"`, `storage` default = `"Trong bột khô (aw <0,2) phản ứng bị hãm; bao bì quyết định"`. Rows with `""` in thermal/storage make the report look unfinished even when the JSON is right.

## 4. Conformance checklist before handing the file back

1. `json.load` + `len(lines) == meta.so_dong`.
2. `build.norm_row` on every row → 0 rows dropped, no empty `verdict/why/ph12/thermal/storage/evidence_level/verification`, ≥1 reference per row.
3. `extra` key histogram non-zero for the labels you intended (`Cơ chế`, `Xếp loại`, `Cảnh báo`, `Hút ẩm / DRH`, `Tích số tan`, `Kết luận`, `Liều tham chiếu`, `Tác dụng không mong muốn`).
4. No raw dict leak in text fields (`"{'" in json.dumps(extra)` == 0).
5. `python build.py` → row counts per file look right, `loi entity=0 | em-dash=0`; grep the HTML for 3–5 of your ids + a distinctive string.
6. Keep `note='chưa verify'` where a constant/PMID/URL could not be checked — the parent's reports rely on these markers being present rather than absent.
