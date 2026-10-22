# Web Content Cleaning (Defuddle pattern)

Use when a target page is cluttered (menus, cookie banners, sidebars, ad widgets)
and you only need the main article body before feeding it to a summarizer or
saving to Obsidian/Notion/research notes.

## Steps

1. If an `article` or `main` element exists, restrict extraction to it on the
   mounted DOM. Drop `nav`, `header`, `footer`, `aside`, `#cookie-banner`,
   `[class*="ad"]`, `[class*="popup"]`, `[class*="modal"]`.
2. For saved-for-later content, output clean Markdown: keep headings, paragraphs,
   lists, tables, links. Drop scripts, iframes, filler images.
3. When HTML is malformed or JS-rendered, fall back to Jina Reader
   `https://r.jina.ai/<url>` or a DOM snapshot (`document.body.innerText` /
   browser snapshot) rather than raw HTML.
4. Feed the cleaned text, not raw HTML, to any summarizer or index — raw chrome
   inflates tokens and pollutes matches.

## Net effect

URL or messy HTML → clean article text in one step, ready for research notes or
an agent pipeline.