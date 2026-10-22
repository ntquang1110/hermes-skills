#!/usr/bin/env python3
"""Convert markdown to a styled HTML document.

Usage:
  python md-to-html.py --file doc.md --output doc.html
  cat doc.md | python md-to-html.py --output doc.html

Requires: markdown (pip install markdown)
"""

import os, sys, webbrowser
try:
    import markdown as md_lib
except ImportError:
    print("Install: pip install markdown", file=sys.stderr)
    sys.exit(1)

HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/5.5.1/github-markdown.min.css">
<style>
  body{{ font-family: system-ui, 'Segoe UI', Roboto, sans-serif;
        background: #fff; color: #1f2937; line-height: 1.7; }}
  .markdown-body{{ max-width: 860px; margin: 40px auto; padding: 0 28px; }}
  @media (max-width: 600px){{ .markdown-body{{ margin: 20px auto; padding: 0 15px; }} }}
</style>
</head>
<body class="markdown-body">
{body}
</body>
</html>'''


def md_to_html(md_content, title=''):
    body = md_lib.markdown(md_content, extensions=['fenced_code', 'tables', 'codehilite', 'sane_lists', 'toc'])
    return HTML_TEMPLATE.format(title=title or 'Document', body=body)


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Convert markdown to styled HTML')
    parser.add_argument('--file', '-f', default='-', help='Markdown file (default: stdin)')
    parser.add_argument('--output', '-o', default=None, help='Output HTML file')
    parser.add_argument('--title', '-t', default='', help='Page title')
    args = parser.parse_args()

    if args.file == '-':
        md_content = sys.stdin.read()
    else:
        with open(args.file, encoding='utf-8') as f:
            md_content = f.read()

    html = md_to_html(md_content, args.title)

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f'Written to {args.output}', file=sys.stderr)
    else:
        print(html)


if __name__ == '__main__':
    main()