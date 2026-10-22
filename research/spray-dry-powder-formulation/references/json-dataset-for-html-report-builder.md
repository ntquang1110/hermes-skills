# Emitting a dataset JSON into an existing project report builder

Use when a task says "xuất ra <project>/data/groupX_*.json theo đúng schema" — especially when the schema is NOT actually attached, or is only implied.

## Step 1 — reverse-engineer the contract from the consumer code (do this before writing data)
Never guess the field names. The project's builder + template define them:
1. `search_files` / `read_file` the builder (`build.py`, `generate*.py`, `*.js`) — look for the glob pattern, the list-plucking helper, and the `normalize()`/mapping function.
2. Grep the template for field usage: `grep -o -E '\{\{[^}]{0,60}\}\}'`, then `grep -n -E "name_vi|rating|verdict|references|items|__DATA__"`.
3. Only then write the JSON with exactly those keys.

## Step 1b — scan the OUTPUT directory for a sibling stub (cheap, do it first)
Before reverse-engineering code, `ls` the **exact target directory** — a sample/stub JSON sitting
next to your output file often *is* the schema, and a project-wide `*schema*` search will miss it.

Real case (22/10/2026): `data/price/price_stub.json` (780 bytes, `meta.nguon`/`meta.ngay`, 4 rows)
defined the real per-item keys for `price_T2.json`:
`id, name_vi, gia_vn_vnd_kg (number), lieu_dung_pct_chat_kho (number), thu_hoi_pct (number|null), do_tin_cay (string), ngay ("dd/mm/yyyy")`.
A search for `*price*`/`*T1*`/`*T2*`/`*schema*` across the project root had returned nothing, so the
first pass had already designed a self-invented schema — which would have broken any consumer.

Rule once found: **conform on the core keys exactly** (same names, same types — e.g. keep
`gia_vn_vnd_kg` rather than `gia_vn_dkg`) and put richer data in **additive** keys
(`gia_nguon[]`, `ga_usd_kg`, `ee_pct`, `note`). Never rename or reshape a required key to "improve" it.
`do_tin_cay` is an enum-ish label describing the price kind: `báo giá thật` / `niêm yết web` /
`sàn B2B` / `ước lượng` — see `carrier-price-sourcing-vn.md`.

## Step 2 — the `say-phun-kiem` contract (verified this session)
- Location: `D:/Hermes Proj/say-phun-kiem/`; builder `build.py`; template `template.html` (contains the `__DATA__` marker); output `say-phun-kiem.html`.
- Loader: `glob.glob(data/group*.json)` → `pick(data)` returns the first list found under keys `items, rows, lines, compounds, data, list` → `normalize()` → `json.dumps(rows)` substituted into `__DATA__`.
- Item schema consumed (anything else is discarded):
  `id, name_vi, name_en, cat, role, verdict, why, ph12, thermal, storage, evidence_level, verification, rating (int 0–5), references[{type,label,pmid,doi,number,note}]`.
- `rating` is coerced with `int(float(...))`, clamped 0–5; non-numeric falls back to 3.
- `references` accepts a dict or a list; bare strings are wrapped as `{type:"", label:<string>}`. There is **no `url` field** — put the link inside `note`.
- `cat` goes through `norm_cat()` / `CAT_MAP`: the group token `chat_mang` renders as the chip **"Chất mang"**. Chemistry sub-categories (`Polysaccharid`, `Protein/sữa`, …) are NOT mapped and would appear as stray chips → keep the real category in a separate key such as `nhom_hoa_hoc`.
- Unmapped `cat` values sort to the end (`CAT_ORDER.index` fallback 99).

## Step 3 — verify integration without publishing
Simulate the loader instead of running the builder (which would overwrite the live HTML with a partial dataset):
```python
import sys; sys.path.insert(0, r'D:/Hermes Proj/say-phun-kiem')
import build
rows = build.normalize(build.load_groups())
print(len(rows), {r['cat'] for r in rows})
print([r['id'] for r in rows if not r['why'] or not r['references']])
```
Then `json.load` your own file and assert every required key exists in every item.

## Pitfalls
- Rich extra fields (Tg, DRH, sub-scores, legal status) are **silently dropped** by the builder. Keep them in the JSON for analysis, but also weave the essentials into the whitelisted fields (`why`, `ph12`, `thermal`, `storage`, `verdict`) or the rendered page will lose them.
- A stub/sample file left in `data/` (e.g. `group0.json` with `"PMID 00000000"`, `"doi doi"`-style placeholders) is loaded and rendered as if real. Detect placeholders and report them; do not treat them as evidence.
- Keep the generator script alongside the data (`data/_build_<group>.py`) so the JSON is reproducible — but do NOT name it `group*.json`, or the builder will try to parse it.
- Rating bands: if most rows land on 3–4, the page looks flat; the banding lives in the extra `xep_loai` field, so encode the A–E verdict text there (and in `verdict`) rather than expecting the 0–5 dots to carry the nuance.
