---
name: legacy-doc-extraction
description: "Use when extracting legacy binary .doc/.rtf Word files."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [doc, docx, word, extraction, antiword, legacy, windows]
---

# Legacy MS document extraction (.doc / .rtf / pre-docx)

Extracting text from OLD binary formats that `python-docx`, pymupdf and
`web_extract` cannot open. `.docx` is a ZIP of XML (use `python-docx`). Legacy
`.doc` is an OLE2 compound document and needs different tooling.

Trigger: user sends a `.doc` (not `.docx`) file, or a lab/scanned report in old
Word format, and you need its text/table values.

## Tool set (Windows git-bash verified)

- `antiword` v0.37 ships with MSYS/git-bash — works for paragraphs and simple
  tables, but see the table limitation below. Detect with `which antiword`.
- `pip install olefile` — read the OLE `WordDocument` stream and parse the FIB
  piece table for text (route for table cells antiword drops).
- MS Word COM (`win32com`) and LibreOffice (`soffice`) only if actually
  installed — don't assume; check `which soffice` / probe COM first.

## Working antiword recipe (VERIFIED on Windows)

```bash
# 1) Rename inputs to ASCII-safe names first — Vietnamese diacritics in the
#    filename break antiword's open.
cp <orig>.doc fileN.doc

# 2) Install the character mapping where antiword looks by default. It checks
#    ~/.antiword and /usr/share/antiword, NOT the mingw64 share.
mkdir -p ~/.antiword
cp "D:/Program Files/Git/mingw64/share/antiword/UTF-8.txt" ~/.antiword/UTF-8.txt
#    Do NOT pass -m with a path containing a space — "Program Files" gets
#    truncated and antiword errors: "can't open your mapping file (…/sha.txt)".

# 3) Input MUST be a native Windows path (D:/…) — NOT MSYS /d/… or /tmp; the
#    Windows antiword binary cannot open MSYS-style paths.
antiword -t "D:/path/fileN.doc" > out.txt
```

Output lands in `out.txt`. Batch loop each file.

## Pitfall — antiword drops multi-column table cells

antiword 0.37 reads paragraph text reliably (dates, sample names, descriptions)
and small result tables, but **drops wide multi-column value grids**. A lab
results table with 7–18 numeric columns comes back as the table stub with the
cells missing. If the values you need are in a wide grid:

1. **Verified route**: decode the ENTIRE `WordDocument` stream as UTF-16LE and
   split on the `\x07` byte — that is the table-cell delimiter, so each segment
   is one cell and values come out in exact column order. Works for 7–18 column
   grids. Full recipe + code: `references/antiword-table-cell-recovery.md`.
   (A "correct" FIB/piece-table parser returns only the main narrative prose,
   NOT the table-body cells — the naive whole-stream decode + `\x07` split is
   the reliable route for these value grids.)
2. Or `soffice --headless --convert-to txt file.doc` if LibreOffice is present.
3. **Values can split across a piece boundary**: a cell's last digit may read as
   its own `\x07` token (e.g. `32,9` then bare `1` = Y 32,91). Cross-check by
   matching value-count to the header element count; if the last digit is
   genuinely ambiguous, leave it empty rather than guess.
4. **Never fabricate missing values** — leave the cell/field empty and report
   exactly which ones could not be recovered. Fabricated lab numbers are worse
   than a blank.

## Verification

After extraction, spot-check: (a) the header/meta lines made it through, (b)
any known single-table values are present, (c) cross-check filename → content
mapping (a batch copy loop preserves `ls` order — keep the mapping straight or
you'll label the wrong file's data).