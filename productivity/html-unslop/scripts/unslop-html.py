#!/usr/bin/env python3
"""Unslop HTML — strip AI-isms from generated HTML designs.

Safely handles <script>, <style>, and HTML tags — only modifies visible text
and CSS values. Does NOT touch JavaScript code.

Usage:
  python unslop-html.py --file input.html --output output.html
  python unslop-html.py --file input.html --publish
"""

import re, sys, json, os, argparse, base64, hashlib


# ─── TEXT BAN LIST ──────────────────────────────────────
HIGH_WORDS = [
    r'\bdelve[sd]?\b', r'\btapestry\b', r'\btestament\b',
    r'\bbustling\b', r'\bvibrant\b', r'\brealm\b',
    r'\bnavigate\b(?![\w\s]*\([^)]*\))', r'\bharness\b', r'\bleverage\b',
    r'\bmultifaceted\b', r'\bparadigm shift\b', r'\btreasure trove\b',
    r'\bmyriad\b', r'\bplethora\b', r'\bever-evolving\b',
    r'\bgame[- ]chang(?:er|ing)\b', r'\bcrucial(?:ly)?\b(?!\.css)',
    r'\bpivotal\b', r'\bseamless(?:ly)?\b', r'\bunparalleled\b',
    r'\bcutting[- ]edge\b', r'\bstate[- ]of[- ]the[- ]art\b',
]

HIGH_PHRASES = [
    r"it'?s (?:important|worth|essential|crucial) (?:to|noting|mentioning)\b",
    r'\bin conclusion,?\b', r'\bin summary,?\b',
    r'\boverall,\s', r'\bwhen it comes to\b',
    r'\bdive into\b', r'\bunlock the power of\b',
    r'\bthe rise of\b', r'\ba deep dive into\b',
    r'\bgreat question!\b', r"\bi hope this helps\b",
    r'\bfeel free to ask\b',
]

MARKETING_VERBS = [
    r'\bfoster(?:s|ed|ing)?\b', r'\bfacilitat(?:e|es)\b',
    r'\boptimiz(?:e|es)\b(?!.{0,20}SEO)', r'\bstreamlin(?:e|es)\b',
    r'\brevolutioniz(?:e|es)\b', r'\bempower(?:s|ed)?\b',
    r'\belevat(?:e|es)\b(?!.{0,20}(?:altitude|height))',
    r'\bcurat(?:e|es)\b(?!.{0,20}(?:museum|gallery))',
]

# ─── CSS DESIGN TELLS ──────────────────────────────────
AI_CSS_PATTERNS = [
    (r'background:\s*linear-gradient\(135deg,\s*#[0-9a-fA-F]{6},\s*#[0-9a-fA-F]{6}\)', 'perfect-gradient'),
    (r'background:\s*#0[fb]1[0-9a-f]{2}2[0-9a-f]', 'ai-dark-bg'),
    (r'color:\s*#(?:e2e8f0|f1f5f9|94a3b8|64748b|475569)', 'ai-text-color'),
    (r'#38bdf8', 'ai-accent-blue'),
    (r'#818cf8', 'ai-accent-indigo'),
    (r'#(?:a78bfa|c084fc)', 'ai-accent-purple'),
    (r'#34d399', 'ai-accent-green'),
    (r'display:\s*grid;\s*grid-template-columns:\s*repeat\(auto-fit,\s*minmax\(\d+px,\s*1fr\)\)', 'ai-auto-grid'),
]

AI_CSS_COLORS = {
    '#0f172a': '#1a1a2e',    '#0b1120': '#1a1a2e',
    '#1e293b': '#2a2a3e',    '#334155': '#3a3a4e',
    '#e2e8f0': '#e8e0d8',    '#f1f5f9': '#f0ece4',
    '#94a3b8': '#a09890',    '#64748b': '#8a8078',
    '#475569': '#5a5a6a',    '#cbd5e1': '#c8c0b8',
    '#38bdf8': '#4a9eff',    '#818cf8': '#7c6cff',
    '#a78bfa': '#9a7ad8',    '#34d399': '#4ab87a',
    '#fbbf24': '#d4a030',    '#f87171': '#c85a5a',
    '#f472b6': '#c86090',
}

AI_FONTS = [
    ("'Inter', system-ui, -apple-system, sans-serif", "system-ui, 'Segoe UI', Roboto, sans-serif"),
    ("'JetBrains Mono', 'Fira Code', monospace", "'Cascadia Code', Consolas, monospace"),
]


def _replace_ai_word(m):
    word = m.group(0).lower()
    reps = {
        'delve': 'explore', 'tapestry': 'mix', 'testament': 'proof',
        'vibrant': 'rich', 'realm': 'field', 'navigate': 'work through',
        'harness': 'use', 'leverage': 'use', 'multifaceted': 'complex',
        'paradigm': 'model', 'myriad': 'many', 'plethora': 'many',
        'ever-evolving': 'changing', 'crucial': 'key', 'pivotal': 'key',
        'seamless': 'smooth', 'unparalleled': 'unique',
        'cutting-edge': 'latest', 'state-of-the-art': 'modern',
        'when it comes to': 'for', 'dive into': 'explore',
        'the rise of': 'the growth of',
        'in conclusion': 'so', 'in summary': 'so',
        'empower': 'help', 'facilitate': 'help', 'optimize': 'improve',
        'streamline': 'simplify', 'revolutionize': 'change',
        'elevate': 'improve', 'curate': 'pick',
    }
    r = reps.get(word)
    if r:
        if m.group(0)[0].isupper():
            r = r[0].upper() + r[1:] if len(r) > 1 else r
        return r
    return m.group(0)


def humanize_css(css_text):
    for old, new in AI_CSS_COLORS.items():
        css_text = css_text.replace(old, new)
    for old, new in AI_FONTS:
        css_text = css_text.replace(old, new)
    return css_text


def detect_ai_design_tells(html):
    findings = []
    for pattern, desc in AI_CSS_PATTERNS:
        matches = re.findall(pattern, html, re.IGNORECASE)
        if matches:
            findings.append(f'{desc} ({len(matches)}x)')
    return findings


# ─── SAFE HTML UNSLOP ───────────────────────────────────

def _protect_blocks(html):
    """Extract script blocks and replace with placeholders.
    Returns (safe_html, restore_list)."""
    blocks = []
    def _save_script(m):
        idx = len(blocks)
        blocks.append(m.group(0))
        return f'@@UNSLOP_SCRIPT_{idx}@@'
    safe = re.sub(r'<script[^>]*>.*?</script>', _save_script, html, flags=re.DOTALL | re.IGNORECASE)
    return safe, blocks


def _restore_blocks(html, blocks):
    for i, block in enumerate(blocks):
        html = html.replace(f'@@UNSLOP_SCRIPT_{i}@@', block)
    return html


def unslop_html(html):
    """Full pipeline: safely process text nodes + CSS, skip script blocks."""
    # 1. Protect <script> blocks
    safe, script_blocks = _protect_blocks(html)

    # 2. Humanize CSS in <style> blocks
    def _fix_style(m):
        return f'<style>{humanize_css(m.group(1))}</style>'
    safe = re.sub(r'<style>(.*?)</style>', _fix_style, safe, flags=re.DOTALL)

    # 3. Humanize inline styles
    def _fix_inline(m):
        return f'style="{humanize_css(m.group(1))}"'
    safe = re.sub(r'style="([^"]*)"', _fix_inline, safe)

    # 4. Process visible text nodes only
    # Match: > (text) <  but NOT inside HTML tags
    def _clean_text(m):
        text = m.group(1)
        # Skip if this is inside a tag (starts with <)
        if text.strip().startswith('<'):
            return m.group(0)
        # Skip if it looks like code/URL
        if re.match(r'^(https?://|//|#|[{};]|function|var |let |const |return|if\s*\()', text.strip()):
            return m.group(0)
        # Apply text replacements
        for pat in HIGH_WORDS + HIGH_PHRASES + MARKETING_VERBS:
            text = re.sub(pat, _replace_ai_word, text, flags=re.IGNORECASE)
        return f'>{text}<'

    safe = re.sub(r'>([^<]+)<', _clean_text, safe)

    # 5. Restore script blocks
    result = _restore_blocks(safe, script_blocks)

    # 6. Add random human comment (optional)
    import random
    random.seed(hashlib.md5(result.encode()).digest())
    comments = [
        '<!-- keep the spacing tight here -->',
        '<!-- this section took forever to get right -->',
        '<!-- TODO: revisit on mobile -->',
        '<!-- not my cleanest work but it works -->',
        '<!-- might refactor this later -->',
    ]
    if random.random() > 0.7:
        comment = random.choice(comments)
        result = result.replace('</body>', f'  {comment}\n</body>', 1)

    return result


# ─── MAIN ───────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description='Unslop HTML — make AI-generated HTML look human')
    parser.add_argument('--file', '-f', help='Input HTML file')
    parser.add_argument('--output', '-o', help='Output HTML file (default: stdout)')
    parser.add_argument('--check', action='store_true', help='Only scan for tells, dont fix')
    parser.add_argument('--publish', action='store_true', help='Upload result to preview')
    parser.add_argument('--title', '-t', default='Unslop HTML', help='Title for publish')
    args = parser.parse_args()

    if args.file:
        with open(args.file, encoding='utf-8') as f:
            html = f.read()
    elif not sys.stdin.isatty():
        html = sys.stdin.read()
    else:
        parser.print_help()
        sys.exit(1)

    tells = detect_ai_design_tells(html)
    if tells:
        print(f'AI design tells ({len(tells)}):', file=sys.stderr)
        for t in tells:
            print(f'  {t}', file=sys.stderr)
    else:
        print('No AI design tells detected', file=sys.stderr)

    if args.check:
        return

    result = unslop_html(html)
    tells_after = detect_ai_design_tells(result)
    print(f'Fixed: {len(tells) - len(tells_after)} tells removed', file=sys.stderr)

    # Validate: check for broken closing tags
    for tag in ['script', 'body', 'html']:
        open_count = result.count(f'<{tag}')
        close_count = result.count(f'</{tag}')
        if open_count != close_count:
            print(f'WARNING: <{tag}> mismatch: {open_count} opens vs {close_count} closes', file=sys.stderr)

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(result)
        print(f'Written to {args.output}', file=sys.stderr)
    else:
        print(result)

    if args.publish:
        try:
            import requests
            r = requests.post(
                'https://preview.thefirstonly.com/api/store',
                json={'content': result}, timeout=30
            )
            if r.status_code == 200:
                print(f'\nPublished: {r.json()["preview_url"]}')
            else:
                print(f'\nPublish failed: {r.text[:200]}', file=sys.stderr)
        except ImportError:
            print('\nInstall requests to use --publish: pip install requests', file=sys.stderr)


if __name__ == '__main__':
    main()
