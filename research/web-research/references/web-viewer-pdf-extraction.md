# Lấy PDF từ web viewer (Adobe Acrobat, Google Drive, share links)

Kỹ thuật đã chạy thành công 07/10/2026 trên link CV `acrobat.adobe.com/id/urn:aaid:sc:AP:<uuid>` mà user gửi.

Khi user gửi link **xem** PDF (không phải link .pdf trực tiếp): `web_extract` trả `target_unreachable`, `browser_navigate` chỉ đọc được **ảnh render**. Đừng dừng ở đó.

## Nguyên tắc

Web viewer **đã tải PDF thật về trình duyệt**. Không cần reverse-engineer API — chỉ cần đọc resource đã fetch và tải thẳng file.

## Bước 1 — Tìm URL PDF thật

Mở viewer bằng `browser_navigate`, rồi:

```javascript
performance.getEntriesByType('resource')
  .filter(r => r.name.includes('pdf') || r.name.includes('blobstore') ||
               r.name.includes('attachment'))
  .map(r => r.name)
```

**Dấu hiệu URL đúng:**
- Adobe Acrobat: host `acp-aep-cs-blobstore-prod-*.adobe.io`, query chứa `response-content-disposition=attachment` + `response-content-type=application%2Fpdf` + tên file URL-encoded
- Có `X-Amz-Security-Token` + `X-Amz-Signature` → **URL có thời hạn** (thường 14400 s), phải tải ngay, không cache lại

**Fallback** nếu filter trên rỗng: lấy rendition ảnh thay vì PDF gốc.

```javascript
// vd: https://cdn-sharing.adobecc.com/rendition/id/urn:aaid:sc:AP:<uuid>;page=0;size=1200;type=image%2Fjpeg?access_token=...
```

Ảnh 1200 px/page đọc được bằng `vision_analyze`, nhưng **không dùng được pymupdf**. Chỉ nên dùng cho tài liệu ngắn.

## Bước 2 — Tải và trích text

```bash
curl -s -L -o cv.pdf "<URL bước 1>" && file cv.pdf   # phải trả "PDF document, version 1.5, N page(s)"
```

```python
import pymupdf
doc = pymupdf.open("cv.pdf")
for i, page in enumerate(doc):
    print(f"===== PAGE {i+1} =====")
    print(page.get_text())
```

## Cạm bẫy

- **`import fitz` deprecated** → dùng `import pymupdf`.
- Viewer render **blob images 902×294** — đó là thumbnail, KHÔNG đọc được, đừng dùng.
- Tên file trong `response-content-disposition` hay bị escape kép `%2520`. Đọc lại để xác nhận tải đúng tài liệu (`CV_THU%2520HA%2520NGUYEN.pdf` → `CV_THU HA NGUYEN.pdf`).

## Thứ tự ưu tiên khi gặp link xem PDF

1. `web_extract(url)` — cho URL PDF trực tiếp hoặc arxiv
2. Fail → `browser_navigate` + bước 1 ở trên
3. Vẫn fail → `browser_vision` đọc từng trang (chỉ nên dùng cho tài liệu ngắn)
