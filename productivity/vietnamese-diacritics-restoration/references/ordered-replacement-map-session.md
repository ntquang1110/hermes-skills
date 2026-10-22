# Ordered replacement map — session notes (2026-10-13)

Batch: 3 markdown research notes (chemical kinetics / cast iron metallurgy / feed enzymes)
in `C:/Users/NTQUANG_DELL/hermes-temp/restore1013/`, ASCII-stripped Vietnamese, each needing
a `.vn.md` twin that differs from the input ONLY by diacritics.

Result: `chemkin`, `castiron`, `enzymecat` all `IDENTICAL` (strip-identity), with base-letter
counts 4679 / 3637 / 3673 matching the sources exactly.

## Source layout facts (measure in BINARY before writing)

| file | bytes | CRLF | trailing NL | lines |
|---|---|---|---|---|
| chemkin | 4769 | 89 | none | 90 |
| castiron | 3712 | 68 | none | 69 |
| enzymecat | 3738 | 55 | none | 56 |

Outputs keep CRLF count + no-final-newline and the same line count; only UTF-8 dấu bytes are
added. Read/write with `io.open(..., encoding='utf-8', newline='')`. Note `strip()` never
touches `\r`, so an EOL change would have printed MISMATCH.

Non-ASCII chars present in the sources (worth enumerating first): `°` (chemkin, castiron),
one literal `đ` (castiron, in `đai bac` → `đại bác`), `—` em dash (enzymecat citations).
The surviving literal `đ` proves the stripper folded `đ→d` but did not reach every occurrence.

## Ambiguity map (both readings strip identically — choose by sense)

| base | readings | resolution used |
|---|---|---|
| `do` | độ / đo | `độ` (độ thay đổi), but `duoc do bang` → "được **đo** bằng" |
| `dong` | động / đông | động (hóa học, năng, học, cơ, nhân tố); đông (đông đặc) |
| `co` | cơ / có | cơ (bản, chế, chất, tính); có (thể, hại, năng lượng) |
| `duoc` | được / dược | `duoc pham` → **dược** phẩm; else được |
| `roi` | rời / rồi | `roi khoi` → **rời** khỏi; `roi bi tieu hao` → **rồi** bị |
| `su` | sự / sử | sự (phụ thuộc, hư hỏng, gia cố); `lich su` → lịch **sử** |
| `bi` | bị / bi | `bi tieu hao` → **bị** tiêu hào; `bi nghien` → **bi** nghiền (grinding balls) |
| `nghien` | nghiên / nghiền | nghiên (cứu); nghiền (máy nghiền, bi nghiền) |
| `cung` | cùng / cũng / cứng | cùng (pha); cũng (nào cũng); cứng (rất cứng, độ cứng, carbide cứng) |
| `tinh` | tính / tinh | tính (chất, đặc hiệu, đúc); `tinh bot` → **tinh** bột |
| `mat` | mất / mặt | `be mat` → bề **mặt**; `mat hang trieu nam` → **mất** |
| `dan` | dẫn / dần | dẫn (nhiệt, đến); `tang dan` → tăng **dần** |
| `dai` | đại / dai | `dai phan tu` → **đại** phân tử; `Deo dai`, `do dai` → **dai** |
| `dien` | diện / diễn / điển / điện | diện tích; diễn ra; điển hình; phụ kiện **điện** |
| `khi` | khí / khi | khí (chất khí, khí thải); **khi** as conjunction (khi gang đông đặc) |
| `the` | thế / thể | thế (năng, kỷ, giới, thay thế); thể (đồng thể, dị thể, có thể) |
| `khoi` | khối / khỏi | khối (động cơ); `roi khoi` → rời **khỏi** |
| `qua` | quả / quá | hiệu **quả**; **quá** (trình, cao) |
| `gia` | giá / già / gia | giá (rẻ, thành); già cỗi(**vetoed**, see below); `gia co` → **gia cố** |
| `ban` | bản / bán / ban | cơ **bản**; chu kỳ **bán**; **ban** đầu (no mark) |
| `bao` | bảo / bão | bảo (quản); **bão** hòa |
| `moi` | mỗi / mới / mọi / môi | mỗi, mới (mới có hiệu quả), mọi (mọi chất xúc tác), môi trường |
| `tam` | tâm / tạm | tâm (xúc tác, trung tâm); **tạm** thời |
| `chinh`/`doc` | chính / độc | khác biệt chính; ba chiều **độc** nhất (độc nhất) |

## Letter-count veto (real case)

Source `su gia co cua polymer`. Semantically nicest = `sự già cỗi của polymer`, but `cỗi`
strips to `coi` → base becomes `gia coi`, one letter too many → MISMATCH. Correct answer was
`sự gia cố của polymer` (`gia cố` = reinforcement). **Count base letters of the candidate
before committing it.**

Also source-anomaly kept as-is: `nghanh` (chemkin) → `nghành`, the only form that strips back
to `nghanh`; the source itself carries an extra `h`. Per the contract we do not "fix" it.

## Ordering-collision catalogue (silent IDENTICAL failures)

Longer phrase must precede any shorter phrase that is its substring:

- `dong hoa hoc` before `hoa hoc` (else `Dong hoa hoc` → `Dong hóa học`)
- `co dong nang` / `co nhiet do` / `co nang luong` before `dong nang` / `nhiet do`
- `dai phan tu`, `so phan tu` before `phan tu`
- `hieu qua` before `qua cao` (else `hieu qua cao` → `hiệu quá cao`)
- `muc bo sung` before `bo sung`
- `chu ky ban` before `chu ky`; `hang so khi` before `hang so`
- `dung moi co hieu qua` before `moi co hieu qua` before `hieu qua`

Phrase OUTPUT re-mangled by a later bare rule (needs a POSTFIX pass):

- `va cham` → `va chạm`, then bare `va`→`và` ⇒ `và chạm` → POSTFIX `('và chạm','va chạm')`
- `tinh bot` → `tinh bột`, then bare `tinh`→`tính` ⇒ `tính bột` → POSTFIX `('tính bột','tinh bột')`
- same class avoided by simply **not** having a bare rule for `cung` (kept `cung va gion`,
  `rat cung`, `do cung`, `cung pha`, `cung cap` as phrases instead).

## English / identifier casualties (why some tokens must stay phrase-only)

| bare rule | would corrupt | fix |
|---|---|---|
| `doi` → `đổi` | `DOI: 10.1093/jas/skaf043` → `Đổi:` | phrase `thay doi`, `tuyet doi` only |
| `co` → `có` | `Synergistic Cu-Co Bimetallic Catalysts` | phrases `co che`, `co ban`, `co nang luong`… |
| `to` → `tố` | English "to" in `Technologies ... to improve` | phrases `yeu to`, `o to` |
| `U` → `Ủ` | `1000-2000 U/kg` | literal `str.replace('U (Annealing)', 'Ủ (Annealing)')` |
| `the` → `thế` | English article "the" | phrases `the ky`, `the nang`, `co the`… |

Practical rule applied to the whole batch: **no bare rule for any token that also occurs in
English or identifiers** — `the, so, do, dai, dien, dong, mo, nong, dung, ban, to, doi, khi,
co, duoc, phan` were all handled phrase-first or scope-limited.

## QA sweep allowlist (surviving ASCII that is CORRECT)

`tinh bột`, `va chạm`, `ban đầu`, `bi nghiền`, `nghiên cứu`, `trung tâm`, `trong`, `so sánh`
("so" carries no mark), `Trung Quốc`, `Anh` (England), plus chemical/units `Si`, `Mn`, `S`,
`P`, `Mg`, `Fe3C`, `Cu-Co`, `U/kg`, `FTU/kg`.

Known prefix-substring false positives from the boundary regex: `quy` in `quyết`, `khu` in
`khuỷu`, `kho` in `khoảng`, `so` in `soát`, `thuy` in `thuyết`, `tu` in `tuân`.

## Verification stdout (as reported)

```
chemkin IDENTICAL 4679 4679
castiron IDENTICAL 3637 3637
enzymecat IDENTICAL 3673 3673
```

Reproducer kept next to the data: `restore_vn.py` (PHRASES → BARE → POSTFIX pipeline) and
`verify_restore2.py` (mandated strip-identity check with first-diff position reporting).
