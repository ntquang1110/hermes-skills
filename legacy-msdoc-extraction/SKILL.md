---
name: legacy-msdoc-extraction
description: "Extract text and tables from legacy binary .doc files."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [doc, extraction, olefile, antiword, word, legacy, office]
    category: productivity
    related_skills: [ocr-and-documents, docx]
---

# Legacy MSDOC (.doc binary) Text & Table Extraction

Old Word `.doc` is an OLE2 compound container and is NOT a zip like `.docx` — `python-docx` won't open it. This skill covers getting readable text AND table values out of them, including the case where the value tables are silently dropped by the usual extractors.

## When to use

- A `.doc` (not `.docx`) arrives (EMR, lab results, invoices, scanned Word) and you must read its content or enter its figures into a spreadsheet.
- `read_file` can't inline it; `antiword`/`soffice` produced partial text with the numbers missing.

## Recommended order

1. **LibreOffice** (if installed) is the most faithful: `soffice --headless --convert-to txt:Text file.doc` or convert to `.docx` then `read_file`. Try it first.
2. **antiword** for quick text (see pitfalls — it drops large tables).
3. **Raw OLE recovery** (below) when the tables are missing — this recovered 53/54 values from 9 old laboratory phiếu that antiword truncated.

## antiword on Windows/git-bash (pitfalls, all hit in real sessions)

- `antiword.exe` (mingw) can't open MSYS/forward-slash paths: `/d/...`, `/tmp` → `I can't open for reading`. Pass a native `D:/path/file.doc`.
- The `-m <mapping>` argument path must have NO spaces. `"D:/Program Files/Git/.../UTF-8.txt"` is truncated at the space (`.../AntiWord/sha.txt`). Fix: copy the mapping into a default search dir and omit `-m`:
  ```bash
  mkdir -p ~/.antiword && cp <mingw>/share/antiword/UTF-8.txt ~/.antiword/UTF-8.txt
  ```
- `antiword -t` extracts simple single-row tables fine (e.g. a 4-column As/Pb/Cd/Hg row). It **silently drops large multi-column grids** (7-column mineral rows, 18-column rare-earth tables) — the value row simply vanishes. `antiword -x db` (DocBook XML) does NOT recover them either.

## Raw OLE value recovery (the reliable fallback)

When a table's values are missing, read the `WordDocument` stream directly. Word stores each table cell's text as a run; cells are delimited by `\x07` (bell). Combined with the element names that are in the same stream, this recovers the values antiword cut.

```python
import olefile, re
ole = olefile.OleFileIO('file.doc')
wd = ole.openstream('WordDocument').read(); ole.close()
t = wd.decode('utf-16-le', errors='ignore')
# numeric cell values, in document order (VN comma decimals):
cells = t.split('\x07')
vals = [c.strip() for c in cells if re.fullmatch(r'<?\s*\d+(?:,\d+)?|<0,1', c.strip())]
```

Then VERIFY before trusting:

- **Pair by position, not guess.** Print a window around `t.find('ppm (mg/kg)')` (+~200 chars) and eyeball the element header line (Ca Mg Fe K Mn Si Zn …) followed by the value row so you don't mis-pair element↔value.
- **Check the count** of recovered numerics against the number of elements in the header.
- **Boundary-fused last digit:** a value at a piece-table boundary can lose its final digit into the next chunk's formatting garbage (e.g. reads `32,9` then glyphs). That digit is often the char just before the next value's `\x07` fence — recoverable, but treat as *reconstructed; verify against the original*.
- **Never fabricate.** If a value can't be confirmed from the stream, leave the cell blank and report it rather than inventing a number. This matters for real lab/soil data.

## Full-text extraction (beyond the numeric-cell script)

`scripts/extract_msdoc.py` only extracts TABLES (element header + numeric value cells) — it does NOT return prose. When you need the full report text (process descriptions, context, flow diagrams, waste tables) read the `WordDocument` stream directly:

```python
import olefile, re
ole = olefile.OleFileIO(src)
wd = ole.openstream('WordDocument').read()
ole.close()
t = wd.decode('utf-16-le', errors='ignore')
t = t.replace('\x07', '\n')                          # \x07 = cell/paragraph marker
t = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', t)   # strip control garbage
t = re.sub(r'\n{3,}', '\n\n', t)
```

- The stream starts with binary header (thousands of garbage glyphs) — the real text begins after; locate the first line matching accented ALL-CAPS (e.g. `CÔNG TY`, `CỘNG HÒA`).
- The tail contains table/format garbage (CJK + control chars) — accept it; only the middle matters.
- Verified 09/2026 on `bvmt 2023.doc` (9-page BVMT report, ~11K chars → ~22K extracted): chemical tables, process flow diagrams, waste tables all land in the text as labeled lines.
- If `olefile` is missing: `pip install olefile` first.

## Support scripts

- `scripts/extract_msdoc.py` — run against one or more `.doc` paths: prints the element header + numeric value cells together (position-paired), so you can enter them into a sheet or review them at a glance.