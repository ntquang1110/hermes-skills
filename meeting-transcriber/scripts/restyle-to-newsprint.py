# -*- coding: utf-8 -*-
"""Restyle meeting HTML files (Slush/Antonio) -> Newsprint (Playfair/Lora/Roboto Mono).

All four web fonts used have a Vietnamese subset. Antonio and JetBrains Mono do not,
which is why Vietnamese diacritics rendered broken.
"""
import io, re

CSS = io.open(r"D:/Hermes Proj/_newsprint_style.css", encoding="utf-8").read()

FONT_LINK = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
             '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
             '<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400'
             '&family=Lora:ital,wght@0,400;0,600;1,400'
             '&family=Inter:wght@400;500;600;700'
             '&family=Roboto+Mono:wght@400;500;700&display=swap" rel="stylesheet">')

TICKER_ITEM = ('{pre} <i>{num}</i> /// 28 ng\u00e0y \u0111\u1ea7u <b>c\u1eeda s\u1ed5 v\u00e0ng ch\u1ee9ng minh hi\u1ec7u qu\u1ea3</b>')


def ticker(items):
    line = " /// ".join(items) + " /// "
    return ('<div class="ticker">\n  <div class="ticker-track">\n    ' + line + line + '\n  </div>\n</div>\n')


def masthead(title, meta):
    return ('<div class="masthead">\n  <div class="masthead-inner">\n    <h1>' + title + '</h1>\n'
            '    <div class="edition">\n'
            '      <span>Vol. 01 / Bi\u00ean b\u1ea3n h\u1ecdp n\u1ed9i b\u1ed9</span>\n'
            '      <span>' + meta + '</span>\n'
            '      <span>L\u01b0u h\u00e0nh n\u1ed9i b\u1ed9</span>\n'
            '    </div>\n  </div>\n</div>\n')


JOBS = [
    dict(
        path=r"D:/Hermes Proj/meeting_dinhhuong-sanpham-chan-nuoi.html",
        title="\u0110\u1ecbnh h\u01b0\u1edbng s\u1ea3n ph\u1ea9m ch\u0103n nu\u00f4i",
        meta="B\u1ee9c tranh th\u1ecb tr\u01b0\u1eddng t\u1eeb \u0111\u1ed1i t\u00e1c ph\u00e2n ph\u1ed1i",
        ticker_items=[
            "B\u1ee5 b\u00e9o <i>5 t\u1ea5n/th\u00e1ng</i> khi gi\u00e1 cao, c\u00f2n 2 t\u1ea5n khi gi\u00e1 xu\u1ed1ng",
            "Kh\u00e1ng sinh <i>1.000+ l\u1ecd/th\u00e1ng</i>",
            "Doanh thu <i>6 \u0111\u1ebfn 9 t\u1ef7/th\u00e1ng</i>, b\u00e1n l\u1ebb ti\u1ec1n t\u01b0\u01a1i",
            "T\u1ec7p kh\u00e1ch ch\u00ednh <i>50 n\u00e1i</i>",
            "\u0110i\u1ec1u tr\u1ecb h\u00f4 h\u1ea5p <i>50 \u0111\u1ebfn 100 ngh\u00ecn/con</i>",
            "R\u00fat ng\u1eafn nu\u00f4i <i>7 \u0111\u1ebfn 10 ng\u00e0y</i>",
        ],
        footer_anchor="\u1ee6y quy\u1ec1n",
    ),
    dict(
        path=r"D:/Hermes Proj/meeting_hop-tac-khcn-nong-nghiep.html",
        title="H\u1ee3p t\u00e1c khoa h\u1ecdc c\u00f4ng ngh\u1ec7 n\u00f4ng nghi\u1ec7p",
        meta="B\u1ed1n l\u0129nh v\u1ef1c bao tr\u1ecdn B\u1ed9 N\u00f4ng nghi\u1ec7p v\u00e0 M\u00f4i tr\u01b0\u1eddng",
        ticker_items=[
            "B\u1eb1ng s\u00e1ng ch\u1ebf <i>5</i>",
            "Nghi\u00ean c\u1ee9u <i>19 n\u0103m</i> ki\u1ec1m th\u1ea3o d\u01b0\u1ee3c",
            "Doanh thu k\u00eanh ng\u01b0\u1eddi <i>h\u01a1n 100 t\u1ef7/n\u0103m</i>",
            "Chi ph\u00ed <i>150.000\u0111/con l\u1ee3n</i> c\u1ea3 v\u00f2ng \u0111\u1eddi",
            "T\u1ef7 l\u1ec7 n\u1ea1p <i>86%</i> so v\u1edbi \u0111\u1ed1i ch\u1ee9ng 83%",
            "T\u00f4m s\u1ed1ng s\u00f3t <i>60%</i> so v\u1edbi \u0111\u1ed1i ch\u1ee9ng 31%",
        ],
        footer_anchor=None,
    ),
]

for j in JOBS:
    p = j["path"]
    h = io.open(p, encoding="utf-8").read()

    # 1. style
    h, n = re.subn(r"<style>.*?</style>", CSS, h, count=1, flags=re.S)
    assert n == 1, p

    # 2. remove every existing google-fonts link, insert the newsprint one
    h = re.sub(r'<link[^>]*fonts\.(googleapis|gstatic)[^>]*>\s*', "", h)
    h = h.replace("</title>", "</title>\n" + FONT_LINK, 1)

    # 3. masthead + ticker
    if 'class="masthead"' not in h:
        block = masthead(j["title"], j["meta"]) + ticker(j["ticker_items"])
        h = h.replace('<div class="tab-bar">', block + '<div class="tab-bar">', 1)

    # 4. drop cap on hero paragraph
    h = re.sub(r'(<div class="hero">\s*<h1>.*?</h1>\s*)<p>', r'\1<p class="dropcap">', h, count=1, flags=re.S)

    # 5. kill em/en dashes anywhere in markup text
    h = h.replace("\u2014", ":").replace("\u2013", "-")
    h = h.replace("Meeting: ", "Meeting: ")
    h = re.sub(r":\s*:", ":", h)

    io.open(p, "w", encoding="utf-8").write(h)

    lines = h.split("\n")
    bad = [i + 1 for i, l in enumerate(lines)
           if l.startswith('<div class="transcript-block">') and not l.rstrip().endswith("</div>")]
    print("---", p.split("/")[-1])
    print("  em dash:", h.count("\u2014"), "| en dash:", h.count("\u2013"))
    print("  div:", h.count("<div"), "/", h.count("</div>"),
          "| nested:", bad, "| masthead:", h.count("masthead") > 0,
          "| dropcap:", h.count("dropcap") > 0)
    print("  antonio:", h.count("Antonio"), "| jetbrains:", h.count("JetBrains"),
          "| playfair:", h.count("Playfair"))
