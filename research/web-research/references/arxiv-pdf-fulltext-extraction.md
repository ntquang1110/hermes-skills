# arXiv full-text extraction for AI/tech research cards (tested Jul 2026)

When the research rotation lands on an AI/tech/CS topic, PubMed has no coverage —
use arXiv. The recipe below gets the **full paper text** (not just the abstract) so
the KF card can cite exact table numbers, confidence intervals and p-values,
which is what pushes cards to the 5–15 min reading-time target.

## 1. Find fresh papers by category (not keyword relevance)

```bash
curl -s --max-time 30 "https://export.arxiv.org/api/query?search_query=cat:cs.CL+AND+cat:cs.LG&sortBy=submittedDate&sortOrder=descending&max_results=30" | python -c "
import sys, xml.etree.ElementTree as ET
ns = {'a': 'http://www.w3.org/2005/Atom'}
root = ET.parse(sys.stdin).getroot()
for i, entry in enumerate(root.findall('a:entry', ns)):
    title = entry.find('a:title', ns).text.strip().replace('\n', ' ')
    arxiv_id = entry.find('a:id', ns).text.strip().split('/abs/')[-1]
    published = entry.find('a:published', ns).text[:10]
    print(f'{i+1}. [{arxiv_id}] ({published}) {title[:130]}')
"
```

- Use `cat:cs.CL AND cat:cs.LG` for LLM papers, `cat:cs.AI`, `cat:cs.CV` for other areas.
- Pick candidates whose abstract has concrete numbers (benchmark scores, budgets,
  effect sizes) — those make the richest cards.
- Fetch the full abstract for the shortlist with `id_list=<id>` before committing:

```bash
# Batch-fetch abstracts for a known shortlist in ONE call (comma-separated ids)
curl -s --max-time 30 "https://export.arxiv.org/api/query?id_list=2401.04088,2401.06066,2412.19437" | python -c "
import sys, xml.etree.ElementTree as ET, re
ns = {'a': 'http://www.w3.org/2005/Atom'}
root = ET.parse(sys.stdin).getroot()
for e in root.findall('a:entry', ns):
    aid = e.find('a:id', ns).text.strip().split('/abs/')[-1]
    title = re.sub(r'\s+', ' ', e.find('a:title', ns).text.strip())
    summ = re.sub(r'\s+', ' ', e.find('a:summary', ns).text.strip())
    print(f'=== [{aid}] {title}')
    print(f'Abstract: {summ[:900]}')
"
```

**Read extracted text by keyword slices, not whole chunks:** for 100K+ char extractions (DeepSeek-V3 = 150K), do NOT read the .txt in full chunks — locate key sections with `python -c` using `text.find('Auxiliary-Loss-Free')` / `re.finditer` and print ±150-300 char windows around each hit (e.g. `print(text[max(0,i-100):i+600])`). This pulls exact formulas, hyper-parameters, and benchmark numbers into context at a fraction of the cost.

## 2. ⚠️ HTML version often missing

`https://arxiv.org/html/<id>` frequently returns a small page saying
`No HTML for '<id>'` (source is LaTeX-only, conversion not available).
This does NOT mean the paper is unavailable — the PDF is always there.

## 3. PDF + pypdf extraction (no OCR needed for text-based PDFs)

```bash
mkdir -p "C:/Users/<user>/hermes-temp"
curl -sL --max-time 90 "https://arxiv.org/pdf/<id>" -H "User-Agent: Mozilla/5.0" \
  -o "C:/Users/<user>/hermes-temp/paper.pdf"
pip install pypdf -q
python -c "
from pypdf import PdfReader
r = PdfReader(r'C:/Users/<user>/hermes-temp/paper.pdf')
text = '\n'.join((p.extract_text() or '') for p in r.pages)
open(r'C:/Users/<user>/hermes-temp/paper_text.txt','w',encoding='utf-8').write(text)
print('PAGES:', len(r.pages), 'CHARS:', len(text))
"
```

Then `read_file` the `.txt` in chunks (offset/limit) and quote exact numbers.

Pitfalls:
- `pypdf`'s `extract_text()` can return `None` for some pages — always `or ''`.
- LaTeX `\boxed{...}`/math renders as plain text; numbers come through fine.
- Tables may lose column alignment in extraction — cross-check numbers against
  prose mentions in the text.
- Do NOT use this for scanned/image PDFs — those need `ocr-and-documents`.
- Papers may contain honest self-reporting of bugs (e.g. a scoring bug that changed
  headline numbers). Quote the corrected numbers and note the fix — it makes the
  card more credible, not less.
- Always check `withdrawn` notices in the abstract before citing.

## 4. Card quality bar

A full-paper card typically runs 11–15K chars of content and lands ~700–900 s
reading time. Reference-table rows should be keyed by arXiv ID
(e.g. `Mirzaei 2026, arXiv:2607.28576`) plus 10–15 supporting refs from the
paper's own bibliography (they are already curated — reuse them).
