# Embedding Favicon as Base64 Data URI

When building standalone HTML files (prototypes, visit cards, single-page designs), embed the favicon inline rather than linking to an external file. This keeps the page fully self-contained.

## Process

### 1. Resize image to 48×48 PNG

Use Python PIL/Pillow:

```python
from PIL import Image
import io, base64

img = Image.open("source.jpg")
favicon = img.resize((48, 48), Image.LANCZOS)

buf = io.BytesIO()
favicon.save(buf, format='PNG', optimize=True)
png_data = buf.getvalue()
```

**Why 48×48?** Standard favicon sizes are 16×16, 32×32, 48×48. 48px is sharp on retina displays while still small.

### 2. Convert to base64 data URI

```python
b64 = base64.b64encode(png_data).decode()
favicon_uri = f'data:image/png;base64,{b64}'
```

### 3. Inject into HTML

```html
<link rel="icon" type="image/png" sizes="48x48" href="data:image/png;base64,...">
```

Add after `</title>` in the `<head>` section.

## Results

| Source | After |
|--------|-------|
| 1024×1024 JPEG ~88KB | 48×48 PNG ~4.6KB |
| External file needed | Inline, zero network request |

## Pitfalls

- **File too large:** If source is >200KB, resizing to 48×48 may still produce a large PNG (>10KB). Try JPEG instead of PNG for the inline format, or compress with `optimize=True`.
- **Transparency:** If source has transparency, use `PNG` format (supports alpha). JPEG does not — white background will appear.
- **Browser support:** All modern browsers support data URI favicons. Some older browsers may ignore them.
