# Session: diacritic-only restore of 3 markdown research notes (2026-10-13)

Task class: astronaut-style "restore dấu, verify with a strip-identity check" on
`C:/Users/NTQUANG_DELL/hermes-temp/restore1013/{polyphenol,gutmicro,cellsignal}.md`
→ twins `*.vn.md` in the same folder.  Topics: polyphenol antioxidants, swine gut
microbiota, cell signalling.

## What the check actually constrains

`strip()` = NFD → drop combining marks → NFC → `đ→d`, `Đ→D`.  Consequences:

- Any tone/hook/horn/breve disappears; `đ` is folded.  So `dau`→`đậu` passes.
- `\r` is NOT touched → line endings are part of the contract.
- Final-newline presence is part of the contract.

Source layouts on this host (Windows/git-bash, files written by a generator):
- polyphenol: 52 CRLF, no trailing newline, 53 lines, 3697 B
- gutmicro:   54 CRLF, no trailing newline, 55 lines, 3750 B
- cellsignal: 60 CRLF, no trailing newline, 61 lines, 4763 B

Output after dấu: 4196 / 4293 / 5445 bytes — growth is UTF-8 multibyte only.
Result: all three IDENTICAL (`len(a) == len(b)`: 3635 / 3684 / 4659 with universal
newlines on read).

## Two mismatches the checker caught (and their real cause)

1. **gutmicro line 37** — source 2-column table separator is `|---|---|` while line 12
   (3-column table) is `|---|---|---|`.  I had "normalized" it to 3 columns.
   Lesson: copy the separator verbatim; a source can mix column counts between tables.
2. **cellsignal** — source says `ban sinh`, not `bam sinh`.  `miễn dịch bẩm sinh`
   (intended) strips to `mien dich bam sinh` ≠ input.  Correct restore = `bản sinh`.

## Substring trap that cost a run

`'|---|---|---|'.count('|---|---|') == 1` — the 3-group separator CONTAINS the 2-group
one, and `'|---|---|---|\r\n'.count('|---|---|\r\n') == 1` too (the match starts at the
second `|`).  So `s.count('|---|---|\r\n')` returned 2, and `s.replace(old, new, 1)`
without a unique anchor rewrites the FIRST table.  Fix: anchor on the header line
(`'| Thành phần \| Tác động lên hệ VSV |\r\n|---|---|---|\r\n'`) and assert on
`split('\r\n')[i]` afterwards.  Nothing was written because the assert fired first —
assert before write.

## Source-text anomalies (restored literally, reported, NOT corrected)

The ASCII source itself was malformed in places; only dấu could be added, so these
read oddly but are strip-exact.  Worth reporting to the requester:

- `Khain niem co ban` → `Kháin niệm cơ bản` (stray `n`; intended `Khái niệm`)
- `thu te bao` → `thụ tế bào` (file elsewhere uses `thụ thể` / `nội bào`)
- `gap sot nhiet` → `gặp sốt nhiệt` (likely intended `sốc nhiệt`)
- `nguy co` → `nguy cơ` (contextually likely `ngũ cốc`); `dau tat` → `đậu tắt`
- `Tan axit tannic` → `Tấn axit tannic`; `bia hoa tan (hop)` → `bia hòa tan (hợp)`
- `Bui sua (7-21 ngay)` → `Búi sữa` (likely intended `Bú sữa`; extra `i`)

Corollary: several restorations were ambiguous between two strip-identical readings
(`loại` vs `loai`, `Chế`/`Chẹn`, `sốt`/`sốc`).  Pick by domain sense, note the
ambiguity in the report — the checker cannot arbitrate it.

## Token audit (proves "nothing added / removed / reordered")

Whitespace-split token counts must be equal; then list tokens identical in input and
output and confirm each is legitimately unaccented.  Legit hits this session:
`the` (only inside English titles/refs), `Da` (Dalton), `vi sinh`, `heo`, `gen`,
`axit`, `tan` (`hòa tan`, `tanin`), `hoa quả`, `gan` (liver), `sinh`, `cạnh tranh`,
`con đường`, `vi`, `trong`, `khi`, `qua`, `ty thể`, `tinh trùng`'s `tinh`, plus all
`DOI:`/PMID/URL/`H2O2`/`Ca2+`/`NF-kB` tokens.

## Workflow that worked

1. Inspect layout in binary (`\r\n` count, `endswith(b'\n')`) before writing anything.
2. Write the accented twin with the `write_file` tool (never echo/heredoc).
3. `scripts/normalize_eol.py` to force the source's EOL/trailing-newline state.
4. `scripts/strip_identity_check.py` (all-diff reporting) → patch the twin → re-run.
5. Finish with the mandated pure verifier and report its raw stdout; delete scratch
   scripts, keep the verifier.
