---
name: image-document-ocr
description: "Use when OCRing image/doc scans with no vision model."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [OCR, Image, Vietnamese, Scans, Tables, Extraction]
    related_skills: [ocr-and-documents]
---

# Image Document OCR (no vision model needed)

When the source is **image files** (photo/scan of a report, table, Vietnamese trial sheet) and you have **no vision model** — `vision_analyze` missing/refused, `browser_vision` returns 401 (misconfigured auxiliary model), or the active model simply lacks native vision — do NOT burn turns on vision tooling. **RapidOCR (PaddleOCR/onnx) runs fully local on CPU, is a light install, and reads Vietnamese well.**

Also relevant when a vision model exists but is slow/misconfigured; RapidOCR is deterministic and iterable. (The bundled `ocr-and-documents` skill covers PDFs via pymupdf/marker-pdf; this one is for raw image files.)

## Install

```bash
pip install rapidocr_onnxruntime pillow   # onnxruntime models, light
```

## Core usage

```python
from rapidocr_onnxruntime import RapidOCR
e = RapidOCR()
result, elapse = e("scan.png")          # each result item = [box, text, score]
for item in (result or []):
    print(item[1])                       # box = item[0], text = item[1]
```

## Pitfalls (verified on real VN trial reports 08/2026)

1. **`execute_code` has a 300s timeout and kills multi-image OCR.** RapidOCR init + inference is ~30-40s/small or 100s+ per large image, so a batch of several large PNGs exceeds it. Run batches as a **background terminal process** (`terminal(background=true)`), writing each image's text to its own file as it finishes (`flush=True`), then poll/wait and read the saved files. Never OCR >2 large images synchronously in `execute_code`.
2. **Multi-column tables scramble columns.** OCR emits rows but interleaves left/right column text (esp. tables with 2+ treatment groups, e.g. Đối chứng vs Khảo nghiệm). Reconstruct by reading each item's **bounding-box x-centroid** (`cx = mean of the 4 box x-coords`), sort by y, then group values by which column centroid (left/mid/right) they fall in. Never trust naive line order for a table.
3. **Attribute values to rows by matching y-range to the label.** Column-crossed numbers get pulled up into the wrong row (e.g. adverse-reaction counts landing under "phù thũng"). When a dense bottom table stays genuinely ambiguous after re-cropping + upscaling, **report the raw numbers with an explicit "cannot unambiguously attribute to each group" caveat rather than guessing which column/row owns them**.
4. **Duplicate/scanned pages often pair up** — identical file sizes (e.g. `A1=A2`, `B4=B5`) usually = same page scanned twice. Detect via `search_files`/`ls -la`/`stat` sizes and skip re-OCR.
5. **Crop-and-upscale disambiguates a dense bottom region**: `PIL.Image.crop((0, H*pct, W, H))` of the lower N%, resize 1.5x with LANCZOS, re-OCR. Repeat with tighter y-slices until a row reads clean.
6. **Never fabricate illegible handwriting.** Conclusion/signature blocks are frequently handwritten and unreadable. State honestly (e.g. "kết luận viết tay mờ, OCR không đọc được") instead of inventing content. Same for any number you actually cannot read.

## Reporting structure (Vietnamese report summaries)

For scanned trial/feed-test reports being organized, summarize each image set in Vietnamese with: customer info (name/address/phone), species/count, trial design (dosage), key results (weight gain, FCR, mortality, disease, conclusion) — and flag which cells could not be read reliably.

## Verification

- Flag genuinely ambiguous cells rather than asserting them.
- If re-OCR of the same region keeps giving a different reading, note "needs cross-check against original image".