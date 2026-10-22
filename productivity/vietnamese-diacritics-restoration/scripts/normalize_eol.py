"""Force output files to match the SOURCE file's line-ending / trailing-newline state.

strip() does not touch \\r, so a CRLF->LF or an added final newline makes a
perfectly accented output print MISMATCH.  Windows-generated files here are
usually CRLF with NO trailing newline.

Run:
    python normalize_eol.py SRC.md OUT.vn.md [OUT2.vn.md ...]

Prints the source layout (crlf count / trailing newline) and normalizes each
output to it, writing in binary so no text-mode translation can re-introduce
\\r\\r\\n.
"""
import sys


def layout(p):
    b = open(p, 'rb').read()
    return dict(crlf=b.count(b'\r\n'), lf=b.count(b'\n'), trailing_nl=b.endswith(b'\n'))


def normalize(path, crlf=True, trailing_nl=False):
    b = open(path, 'rb').read()
    b = b.replace(b'\r\n', b'\n')          # collapse to LF
    while b.endswith(b'\n'):
        b = b[:-1]                          # no trailing newline
    if trailing_nl:
        b += b'\n'
    if crlf:
        b = b.replace(b'\n', b'\r\n')
    with open(path, 'wb') as f:
        f.write(b)
    return len(b)


def main():
    src, outs = sys.argv[1], sys.argv[2:]
    lay = layout(src)
    print('source layout:', lay)
    for p in outs:
        n = normalize(p, crlf=lay['crlf'] > 0, trailing_nl=lay['trailing_nl'])
        print('normalized', p, '->', n, 'bytes', layout(p))


if __name__ == '__main__':
    main()
