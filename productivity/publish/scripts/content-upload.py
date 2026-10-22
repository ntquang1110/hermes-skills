#!/usr/bin/env python3
"""Upload any content (HTML, markdown, text) to preview online.

Two backends:
  --kv      (default) Store directly in Cloudflare KV — no Gist needed, instant.
  --gist    Store in GitHub Gist (fallback, requires PAT).

Auto-applies html-unslop to HTML content before uploading.

Usage:
  python content-upload.py --content "<h1>Hello</h1>" --title "Page"
  python content-upload.py --file doc.html --title "Report"
  cat note.md | python content-upload.py --title "Note"
"""

import os, sys, json, argparse, base64, re
import requests

PREVIEW_DOMAIN = 'https://preview.thefirstonly.com'

# Cloudflare WAF on preview.thefirstonly.com blocks non-browser User-Agents
# with `error code: 1010` (403). Default python-requests UA gets blocked, so
# always send a browser-like UA. Symptom before fix: HTTP 403 "error code: 1010",
# or ConnectionResetError(10054) on large payloads.
UA_HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
        '(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    ),
}


def apply_unslop(content):
    """Auto-apply html-unslop to HTML content. Returns (content, applied)."""
    if not re.match(r'^\s*<(?:!DOCTYPE\s+html|html|head|body|div|h[1-6]|p|span|table|ul|ol|form|a|img|script|style|section|article|nav|header|footer|main|aside)\b', content.strip(), re.IGNORECASE):
        return content, False
    try:
        here = os.path.dirname(os.path.abspath(__file__))
        # Script lives in publish/scripts/, unslop in sibling html-unslop/scripts/
        candidates = [
            os.path.join(here, 'unslop-html.py'),
            os.path.join(here, '..', '..', 'html-unslop', 'scripts', 'unslop-html.py'),
        ]
        for cand in candidates:
            if os.path.exists(cand):
                import subprocess
                r = subprocess.run(['python', cand], input=content,
                                   capture_output=True, text=True, timeout=20)
                if r.returncode == 0 and r.stdout.strip():
                    return r.stdout, True
    except Exception as e:
        sys.stderr.write(f'  ⚠️ unslop skipped: {e}\n')
    return content, False


# ─── KV Backend (default) ──────────────────────────────

def upload_to_kv(content, title=''):
    content, unslopped = apply_unslop(content)
    resp = requests.post(
        f'{PREVIEW_DOMAIN}/api/store',
        json={'content': content},
        headers=UA_HEADERS,
        timeout=180   # file HTML lớn (600KB-1MB) upload mất 40-90s; 30s là lỗi hay gặp
    )
    if resp.status_code != 200:
        raise RuntimeError(f'KV store failed (HTTP {resp.status_code}): {resp.text[:200]}')
    data = resp.json()
    return {
        'preview_url': data['preview_url'],
        'gist_url': None,
        'raw_url': None,
        'gist_id': data['id'],
        'filename': 'index.html',
        'type': 'html',
        'unslopped': unslopped,
    }


# ─── Gist Backend ──────────────────────────────────────

def get_pat():
    pat = os.environ.get('GITHUB_PAT', '')
    if pat:
        return pat
    for env_path in [
        os.path.expanduser('~/.hermes/.env'),
        os.path.expanduser('~/AppData/Local/hermes/.env'),
        '.env',
    ]:
        if not os.path.exists(env_path):
            continue
        with open(env_path, encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith('GITHUB_PAT='):
                    return line.split('=', 1)[1].strip()
                if line.startswith('GITHUB_PAT_B64='):
                    b64 = line.split('=', 1)[1].strip()
                    return base64.b64decode(b64).decode()
    raise RuntimeError('GitHub PAT not found. Use --kv (default) instead.')


def detect_type(content):
    stripped = content.strip()
    if re.match(r'^\s*<(?:!DOCTYPE\s+html|html|head|body|div|h[1-6]|p|span|table|ul|ol|form|a|img|script|style|section|article|nav|header|footer|main|aside)\b', stripped, re.IGNORECASE):
        return 'index.html', False
    md_signals = [
        r'^#{1,6}\s', r'^\*{1,3}\s', r'^- {0,3}\[', r'^```',
        r'^\|.+\|', r'^>\s', r'^---\s*$', r'^\[.+\]\(.+\)',
        r'^!\[.+\]\(.+\)', r'\*\*.+\*\*', r'__.+__',
    ]
    for pattern in md_signals:
        if re.search(pattern, stripped, re.MULTILINE):
            return 'document.md', True
    return 'note.txt', False


def upload_to_gist(content, title='', filename=None):
    if filename is None:
        filename, is_md = detect_type(content)
    else:
        is_md = filename.endswith('.md')

    pat = get_pat()
    headers = {'Authorization': f'token {pat}', 'Content-Type': 'application/json'}
    payload = {'description': title or 'Uploaded Content', 'public': False,
               'files': {filename: {'content': content}}}
    resp = requests.post('https://api.github.com/gists', headers=headers,
                         json=payload, timeout=30)
    if resp.status_code != 201:
        raise RuntimeError(f'Gist upload failed (HTTP {resp.status_code}):\n{resp.text}')
    data = resp.json()
    gist_id = data['id']
    gist_url = data['html_url']
    file_key = filename
    if file_key not in data.get('files', {}):
        for fname in data['files']:
            if fname.endswith('.md') or fname == filename:
                file_key = fname
                break
        else:
            file_key = list(data['files'].keys())[0]
    raw_url = data['files'][file_key]['raw_url']
    preview_url = gist_url if is_md else f'{PREVIEW_DOMAIN}/{gist_id}'
    return {
        'preview_url': preview_url,
        'gist_url': gist_url,
        'raw_url': raw_url,
        'gist_id': gist_id,
        'filename': file_key,
        'type': 'markdown' if is_md else ('html' if filename.endswith('.html') else 'text'),
    }


# ─── MAIN ──────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description='Upload content and get a preview URL')
    parser.add_argument('--content', '-c', help='Content string to upload')
    parser.add_argument('--file', '-f', help='Path to file to upload')
    parser.add_argument('--title', '-t', default='', help='Title/description')
    parser.add_argument('--name', '-n', help='Force filename (only with --gist)')
    parser.add_argument('--gist', action='store_true', help='Use GitHub Gist (requires PAT)')
    args = parser.parse_args()

    if args.file:
        with open(args.file, encoding='utf-8') as f:
            content = f.read()
    elif args.content:
        content = args.content
    elif not sys.stdin.isatty():
        content = sys.stdin.read()
    else:
        parser.print_help()
        sys.exit(1)

    try:
        if args.gist:
            result = upload_to_gist(content, args.title, args.name)
        else:
            result = upload_to_kv(content, args.title)
    except RuntimeError as e:
        print(f'Error: {e}', file=sys.stderr)
        sys.exit(1)

    print(json.dumps(result, indent=2, ensure_ascii=False))
    method = 'KV' if not args.gist else 'Gist'
    print(f'\nPreview: {result["preview_url"]}')
    if result.get('gist_url'):
        print(f'Gist:    {result["gist_url"]}')
    print(f'Method:  {method}')


if __name__ == '__main__':
    main()
