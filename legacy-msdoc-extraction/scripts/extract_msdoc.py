# -*- coding: utf-8 -*-
"""Extract element header + numeric table values from legacy binary .doc files.

Use when antiword/LibreOffice drop the multi-column table values: this reads the
WordDocument OLE stream, decodes UTF-16LE, and splits on the \\x07 cell delimiter
so per-cell values come back in document order, alongside the element/column names.

Usage:
    python extract_msdoc.py file.doc [file2.doc ...]

Pair the counted values against the header line (Ca Mg Fe K Mn Si Zn ...) BEFORE
using them. Values at piece-table boundaries may lose a final digit — verify
against the original before trusting a reconstructed figure.
"""
import sys, re, olefile

NUM = re.compile(r'<?\s*\d+(?:,\d+)?')

def extract(doc):
    ole = olefile.OleFileIO(doc)
    wd = ole.openstream('WordDocument').read()
    ole.close()
    t = wd.decode('utf-16-le', errors='ignore')
    # collapse control-run garbage so header labels & values are readable
    cells = [c for c in t.split('\x07')]
    def clean(s):
        s = re.sub(r'[\x00-\x1f\x7f]', ' ', s)
        return re.sub(r'\s+', ' ', s).strip()
    header = []
    for c in cells:
        cc = clean(c)
        m = re.fullmatch(r'(?:Ca|Mg|Fe|K|Mn|Si|Zn|Cu|Sc|Y|La|Ce|Pr|Nd|Sm|Eu|Gd|Tb|Dy|Ho|Er|Tm|Yb|Lu|U|Th|As|Pb|Cd|Hg)\s*', cc)
        if m:
            header.append(m.group(0).strip())
    vals = [cc for cc in (clean(c) for c in cells) if NUM.fullmatch(cc or '<0,1') or cc in ('<0,1',)]
    vals = [cc for cc in (clean(c) for c in cells) if re.fullmatch(r'<\s*0,1|<0,1|<?\s*\d+(?:,\d+)?', cc)]
    pp = t.find('ppm (mg/kg)')
    win = t[pp:pp + 220] if pp >= 0 else ''
    win = re.sub(r'[\x00-\x1f\x7f]', ' ', win)
    return doc, header, vals, re.sub(r'\s+', ' ', win).strip()

def main():
    if len(sys.argv) < 2:
        print(__doc__); return
    for doc in sys.argv[1:]:
        d, header, vals, win = extract(doc)
        print('=' * 15, d, '=' * 15)
        print('HEADER elems:', header)
        print('ppm context :', win[:220])
        print('values (%d):' % len(vals), vals)
        print()

if __name__ == '__main__':
    main()