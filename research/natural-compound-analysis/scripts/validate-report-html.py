#!/usr/bin/env python3
"""
validate-report-html.py — pre-publish gate cho report HTML sinh bằng script.

Bắt đúng những bug mà "page load + 0 JS error" KHÔNG phát hiện được:

  * tag không cân đối / crossed (ví dụ `</td>` đóng nhầm khối `<dd>`)
  * citation superscript trỏ quá cuối reference list
  * reference list có mục không được trích dẫn ở thân bài
  * artifact generator sót lại (None / undefined / NaN / placeholder f-string)

Dùng:
    python validate-report-html.py report.html
    python validate-report-html.py report.html --strict

Exit: 0 = sạch, 1 = có error, 2 = chỉ warning (kèm --strict)
"""
import argparse
import re
import sys
from html.parser import HTMLParser

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input",
        "link", "meta", "param", "source", "track", "wbr"}


class Balance(HTMLParser):
    """Tag-balance checker, báo vị trí dòng của lỗi đầu tiên."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.errors = []

    def handle_starttag(self, tag, attrs):
        if tag not in VOID:
            self.stack.append((tag, self.getpos()))

    def handle_startendtag(self, tag, attrs):
        pass  # tự đóng, không cần theo dõi

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack:
            self.errors.append(f"stray </{tag}> at line {self.getpos()[0]}")
            return
        if self.stack[-1][0] != tag:
            opened = self.stack[-1]
            self.errors.append(
                f"crossed tags: <{opened[0]}> opened line {opened[1][0]} "
                f"but </{tag}> closed at line {self.getpos()[0]}"
            )
            for i in range(len(self.stack) - 1, -1, -1):
                if self.stack[i][0] == tag:
                    del self.stack[i:]
                    return
            return
        self.stack.pop()


# PHẢI dùng word boundary — "morphinan" chứa "nan", prose có "undefined".
# Quét substring thuần sẽ báo động giả.
ARTIFACTS = [
    (r"\bNone\b", "python None leaked into output"),
    (r"\bundefined\b", "JS undefined leaked into output"),
    (r"\bNaN\b", "NaN leaked into output"),
    (r"\{[A-Za-z_][\w\.]*\}", "unrendered f-string placeholder"),
    (r"&lt;/?[a-z]+&gt;", "double-escaped tag (html.escape applied twice)"),
]


def check_citations(html: str):
    errors, warnings = [], []
    cited = [int(n) for n in re.findall(r'<sup class="refmark">\[(\d+)\]</sup>', html)]
    refs = re.findall(r"<li><b>", html.split('class="refs"')[-1]) if 'class="refs"' in html else []
    n_refs = len(refs)

    if cited and not n_refs:
        warnings.append('citations present but no reference list (thiếu class="refs"?)')
    for n in sorted(set(cited)):
        if n < 1 or n > n_refs:
            errors.append(f"citation [{n}] out of range (reference list có {n_refs} mục)")
    if n_refs:
        for i in range(1, n_refs + 1):
            if i not in set(cited):
                warnings.append(f"reference [{i}] không được trích dẫn ở thân bài")
    return errors, warnings, len(set(cited)), n_refs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--strict", action="store_true")
    args = ap.parse_args()

    with open(args.file, encoding="utf-8") as fh:
        html = fh.read()

    errors, warnings = [], []

    bal = Balance()
    bal.feed(html)
    errors += bal.errors
    errors += [f"unclosed <{t}> opened line {p[0]}" for t, p in bal.stack]

    for pat, msg in ARTIFACTS:
        hits = re.findall(pat, html)
        if hits:
            warnings.append(f"{msg}: {len(hits)} hit(s), first={hits[0]!r}")

    cite_err, cite_warn, n_cited, n_refs = check_citations(html)
    errors += cite_err
    warnings += cite_warn

    n_sections = len(re.findall(r"<section id=", html))
    n_tables = len(re.findall(r"<table", html))
    n_rows = len(re.findall(r"<tr data-", html))
    if n_sections == 0:
        warnings.append("không tìm thấy <section id=...>")
    if n_tables and n_rows == 0:
        warnings.append("có table nhưng không có data row (<tr data-...>)")

    for label, items in (("ERROR", errors), ("WARN", warnings)):
        for it in items:
            print(f"[{label}] {it}")

    print(f"\nsections={n_sections} tables={n_tables} rows={n_rows} "
          f"citations={n_cited} refs={n_refs} size={len(html) // 1024}KB")
    print(f"errors={len(errors)} warnings={len(warnings)}")

    if errors:
        return 1
    if warnings and args.strict:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())