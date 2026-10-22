# Recovering table cells antiword drops (verified recipe)

Context: antiword 0.37 drops wide multi-column result-grid cells. This recipe
successfully recovered **all** numeric cells from a set of lab TEST REPORT
.doc files (7–18 numeric columns each: mineral 7CT/8CT, heavy-metal 4CT,
rare-earth 18CT). It produced real values, verified legible in the stream.

## Core idea

The table body text lives in the `WordDocument` stream as **UTF-16LE**, with each
cell delimited by the bytes `\x07` (`0x07`, Form Feed — the classic Word table
cell/text-run separator). So instead of parsing the FIB piece table precisely:

1. `pip install olefile`
2. Read the whole `WordDocument` stream, decode `utf-16-le` (errors='ignore').
3. Split on the `\x07` character — each segment is one table cell (or prose run).
4. `re.findall(r'\d+,\d+', ...)` the numeric cells in order.

The result reproduces the source's on-page order: element/label cells, then the
unit cell `ppm (mg/kg)`, then the value cells in column order.

```python
import olefile, re
ole = olefile.OleFileIO('file.doc')
wd  = ole.openstream('WordDocument').read(); ole.close()
t   = wd.decode('utf-16-le', errors='ignore')
cells = t.split('\x07')
vals = [c for c in cells if re.fullmatch(r'\d+,\d+', c.strip())]  # in order
```

Sanity-check by mapping the element header row to the value positions: a row
beginning `Ca Mg Fe K Mn Si Zn` with values `2072 2600 20797 26239 24,87
96084 50,25` means Ca=2072, Mg=2600, … in that exact header order.

## Why not a full FIB/piece-table parser

A "correct" CLX/piece-table parser (FibRgFcLcb → fcClx → Pcdt → PlcPcd) returns
only the **main narrative text** (file5 yielded just 3 pieces / the prose 0–1789),
NOT the table-body cells. The lab values live in the wider raw stream. So the
naive whole-stream UTF-16LE decode + `\x07` split is the *reliable* route — the
piece parser is for clean prose, not for these value grids.

## Pitfall — a value can split across a piece boundary

A single cell's last digit may sit in the next text piece and read as its own
`\x07` token. e.g. after `19,20` you may see `32,9` then a bare digit token `1`
then the next full value `69,83`. That bare `1` completes the previous cell →
`Y = 32,91`. Decide with evidence:
- Confirm the bare digit by examining raw bytes around the truncated value
  (`wd[i:i+16].hex()`), and by matching the expected *count* of values to the
  header's element count (9 elements ⇒ 9 values; split tokens collapse to 9).
- If the last digit is genuinely ambiguous (a `\x07` piece boundary with binary
  after, and no corroborating digit), **leave the cell empty** and report the
  element+sample as "not fully recovered" rather than guessing.

## Vietnamese number format

Values are comma-decimal (`23,48`, `<0,1`). Keep them in this string form when
filling downstream (they are lab readings, not computed quantities).