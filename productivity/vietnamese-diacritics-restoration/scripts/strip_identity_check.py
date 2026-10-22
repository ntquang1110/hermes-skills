"""Pure strip-identity verifier for diacritic-only restoration tasks.

Contract: the output may differ from the input by diacritics ONLY
(and d <-> đ).  strip(a) == strip(b) on the full file text, including
line endings and trailing-newline state.

Run:
    python strip_identity_check.py DIR key1 key2 key3
    # checks DIR/key1.md  vs  DIR/key1.vn.md  ...

No side effects: this script never writes.  Keep it that way so its stdout
can be reported verbatim as evidence.
"""
import os
import sys
import unicodedata


def strip(s):
    s = unicodedata.normalize('NFD', s)
    s = ''.join(c for c in s if not unicodedata.combining(c))
    s = unicodedata.normalize('NFC', s)
    return s.replace('\u0111', 'd').replace('\u0110', 'D')


def read(p):
    with open(p, 'rb') as f:
        return f.read().decode('utf-8')


def layout(p):
    """Byte-level facts that strip() does NOT normalize."""
    b = open(p, 'rb').read()
    return dict(crlf=b.count(b'\r\n'), lf=b.count(b'\n'),
                trailing_nl=b.endswith(b'\n'), bytes=len(b))


def main():
    d = sys.argv[1]
    keys = sys.argv[2:]
    for key in keys:
        src = os.path.join(d, key + '.md')
        out = os.path.join(d, key + '.vn.md')
        a, b = read(src), read(out)
        sa, sb = strip(a), strip(b)
        if sa == sb:
            print(key, 'IDENTICAL', len(a), len(b))
            continue
        print(key, 'MISMATCH', len(a), len(b), 'stripped len', len(sa), len(sb))
        la, lb = layout(src), layout(out)
        if la['crlf'] != lb['crlf'] or la['trailing_nl'] != lb['trailing_nl']:
            print('  LAYOUT DIFF (fix EOL first, it masks every diacritic diff):')
            print('   in :', la)
            print('   out:', lb)
        # report ALL differing positions grouped, with line numbers
        diffs = [i for i in range(min(len(sa), len(sb))) if sa[i] != sb[i]]
        groups = []
        for i in diffs:
            if groups and i - groups[-1][-1] <= 3:
                groups[-1].append(i)
            else:
                groups.append([i])
        for g in groups:
            i = g[0]
            ln = sa[:i].count('\n') + 1
            print('  line %d idx %d  IN:%r  OUT:%r'
                  % (ln, i, sa[max(0, i - 25):i + 25], sb[max(0, i - 25):i + 25]))


if __name__ == '__main__':
    main()
