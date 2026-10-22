# Khi web_extract fail: lấy nội dung từ JS-rendered document viewer

Áp dụng cho: Adobe Acrobat online (`acrobat.adobe.com/id/urn:aaid:sc:...`), Google Drive preview,
Scribd, và mọi viewer render trang thành ảnh thay vì serve HTML/text.

## Triệu chứng

- `web_extract([url])` trả `{"error": "target_unreachable"}` — viewer chỉ serve JS, không có HTML/text tĩnh.
- `browser_navigate` thành công nhưng snapshot chỉ có `img "Rendition 0"`, `img "Rendition 1"` — không có text node.
- `document.images` trả mảng `src="blob:https://..."` kích thước nhỏ (VD 902×294) — đây là **thumbnail**, không phải trang gốc. Đừng OCR chúng, chữ sẽ nát.

## Cách lấy file gốc: đọc network log

Viewer buộc phải tải file gốc về để render. URL đó nằm trong Resource Timing API:

```javascript
// browser_console
JSON.stringify(performance.getEntriesByType('resource')
  .filter(r => /\.pdf|download|blobstore|rendition|asset|content/.test(r.name))
  .map(r => r.name))
```

**Adobe Acrobat online** trả URL presigned S3 trỏ tới file gốc:

```
https://<id>.adobe.io/<uuid>?response-content-disposition=attachment%3B%20filename%3D%22CV_NAME.pdf%22
   &response-content-type=application/pdf&...&X-Amz-Signature=...
```

`filename` trong query string là tên file thật — dùng để xác nhận đúng tài liệu.

Biến thể thứ hai cũng xuất hiện, là ảnh trang độ phân giải cao:

```
https://cdn-sharing.adobecc.com/rendition/id/urn:aaid:sc:AP:<id>;page=0;size=1200;type=image%2Fjpeg?access_token=...
```

Chỉ dùng biến thể này khi file gốc là bản scan (không có text layer) và phải OCR.

## Tải và extract

```bash
curl -s -L -o doc.pdf "<URL presigned từ network log>"
file doc.pdf        # kỳ vọng: "PDF document, version 1.x, N page(s)"
```

URL presigned của Adobe hết hạn sau vài giờ (`X-Amz-Expires=14400`). **Tải ngay trong session**,
đừng lưu URL dùng lại sau.

```python
import pymupdf
doc = pymupdf.open("doc.pdf")
for i, page in enumerate(doc):
    print(f"===== PAGE {i+1} =====")
    print(page.get_text())
```

PDF 2 cột có thể ra thứ tự dòng lộn xộn. Với CV/hợp đồng nhiều cột,
`page.get_text("blocks")` rồi sort theo `(y, x)` thường sạch hơn `get_text()`.

## Pitfalls

- **Đừng OCR thumbnail blob.** 902×294 là ảnh thu nhỏ của cả trang. Luôn tìm file gốc.
- **Đừng kết luận "không đọc được"** khi `web_extract` fail. Fail đó do viewer, không phải tài liệu bị khóa.
- **Đừng dùng `document.body.innerText`** — viewer render vào shadow DOM/canvas, `innerText` gần như rỗng.
- Nếu `performance.getEntriesByType` không thấy URL file (buffer đã bị xoá), reload trang rồi chạy lại ngay.
- Prompt đăng nhập Google hiện ra không có nghĩa phải đăng nhập — tài liệu share public vẫn đọc được.
- Giữ lại bản PDF đã tải nếu còn cần dùng; URL hết hạn thì phải vào lại viewer.

## Xử lý web_extract fail nói chung — thứ tự thử

1. `web_extract` (nhanh nhất, đa số trường hợp đủ)
2. Fail với `target_unreachable` → **viewer render động** → network log → tải file gốc (recipe trên)
3. Fail với `bot_blocked` / CAPTCHA → xem `camofox-bypass-setup.md` ở skill `purchaser-pro`
4. Fail với 403 do thiếu User-Agent → curl với UA thật (xem `unsloth-cloudflare-403-fix`)
5. Vẫn fail → `browser_navigate` + `browser_console` để đọc DOM/network trực tiếp

## Đã kiểm chứng

Session 10/2026: link `acrobat.adobe.com/id/urn:aaid:sc:AP:c91f...` → `web_extract` trả
`target_unreachable` → network log cho URL presigned → curl về `cv_thu.pdf` (341KB, 2 trang,
`file` xác nhận) → pymupdf trích đủ toàn bộ text 2 trang: học vấn, dự án, kỹ năng, 4 công bố,
2 giáo sư liên hệ. Không cần OCR.
