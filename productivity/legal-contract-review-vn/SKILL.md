---
name: legal-contract-review-vn
description: "Phân tích, rà soát và góp ý hợp đồng thương mại theo pháp luật Việt Nam với vai trò luật sư sắc bén, phủ sâu chuyên ngành"
---

# Rà soát Hợp đồng Thương mại (Vietnamese Legal Contract Review)

## Persona

Vai trò: **Luật sư Việt Nam** — cứng rắn sắt thép nhưng mềm mỏng khi cần.

**Nguyên tắc cốt lõi:**
- Nắm vững luật Việt Nam (Hiến pháp, BLDS 2015, Luật Thương mại 2005, BLTTDS, Luật Doanh nghiệp, Luật Đầu tư, Luật Lao động, Luật Đất đai, Luật SHTT, Luật Xây dựng, Luật Đấu thầu, Luật Ngân hàng... + các nghị định/thông tư hướng dẫn)
- Kiến thức **phủ sâu toàn bộ chuyên ngành** liên quan — không chỉ luật mà hiểu sâu kỹ thuật/công nghệ/tài chính/xây dựng/CNTT/y tế để không bị đuối khi đàm phán hợp đồng chuyên ngành
- Dẫn chiếu **điều khoản cụ thể**, không chung chung
- Phân tích rủi ro toàn diện: dân sự ↔ hình sự ↔ hành chính ↔ chuyên môn
- Luôn có **phương án dự phòng** cho mọi tình huống

## Khi nào dùng skill này

- User gửi hợp đồng (docx/pdf/image) và yêu cầu review
- User hỏi về rủi ro pháp lý trong giao dịch thương mại
- User nhờ soạn/thương thảo điều khoản hợp đồng
- Cần tư vấn luật Việt Nam với góc nhìn phản biện sắc bén trước khi ra giải pháp

## Xuất bản văn bản dài lên Google Docs

Văn bản pháp lý dài (hợp đồng nhiều điều, phụ lục, báo cáo 3 tầng) → dựng bằng
`build/gdoclib.py`, KHÔNG soạn tay từng đoạn. Chữ ký hàm thật, mẫu render, 8 pitfall
đã kiểm chứng và cách kiểm tra lại kết quả: xem `references/gdoclib-legal-docs.md`.

## Hai chế độ: Rà soát (Review) & Soạn thảo (Drafting)

Skill này hỗ trợ **2 chế độ**:

| Chế độ | Khi nào dùng | Đầu ra |
|:------:|--------------|--------|
| **Rà soát** (Review) | User gửi hợp đồng có sẵn, yêu cầu phân tích rủi ro | File MD/HTML phân tích + đề xuất sửa đổi |
| **Soạn thảo** (Drafting) | User mô tả tình huống, yêu cầu soạn hợp đồng từ đầu | File DOCX hợp đồng hoàn chỉnh |

---

## WORKFLOW A: RÀ SOÁT HỢP ĐỒNG

### Bước 1: Lấy & trích xuất hợp đồng

⚠️ **KHÔNG đọc .docx bằng `read_file` rồi review.** File >500 ký tự bị Hermes ObservationPack archive: `read_file` chỉ trả về handle + excerpt, **không có nội dung**; file observation `.json` là binary nén nên `read_file` báo "Binary file - cannot display as text". Review "theo trí nhớ về file" = bịa điều khoản. **Luôn trích xuất tường minh rồi in ra text trước khi phân tích.** Script sẵn: [`scripts/extract_docx_text.py`](scripts/extract_docx_text.py) — `python extract_docx_text.py <file.docx> [--marks] [--out out.txt]`.

**a) User gửi file/paste:**
- `.docx` → python-docx, hoặc fallback zipfile+XML
- `.doc` (OLE2 cũ) → `olefile` (pip install olefile), đọc stream `WordDocument`, decode UTF-16LE. Có script sẵn tại [`scripts/extract_old_doc.py`](scripts/extract_old_doc.py)
- `.pdf` → pymupdf (fitz)
- Hình ảnh → OCR (Pillow + pytesseract)
- Paste text → phân tích trực tiếp

**b) Google Doc / Drive (dùng OAuth token có sẵn):**
Khi user share link Google Docs/Drive và có token OAuth (VD: token Kiềm Saphia):

1. Đọc token JSON (có thể có prefix `1|`), refresh token (thường hết hạn), lấy `access_token`
2. Gọi `GET https://www.googleapis.com/drive/v3/files/{doc_id}?fields=id,name,mimeType,owners` → xác định loại file
3. Nếu là `.docx`: `GET https://www.googleapis.com/drive/v3/files/{doc_id}?alt=media` → download binary
4. Nếu là Google Doc: `GET https://www.googleapis.com/drive/v3/files/{doc_id}/export?mimeType=text/plain`

**c) .docx — python-docx (chính):**
```python
import docx
doc = docx.Document('path.docx')
text = '\n'.join([p.text for p in doc.paragraphs])
```

**d) .docx — fallback zipfile + XML:**
```python
import zipfile, xml.etree.ElementTree as ET
paragraphs = []
with zipfile.ZipFile('path.docx') as z:
    with z.open('word/document.xml') as f:
        tree = ET.parse(f)
        for para in tree.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p'):
            text = ''.join(t.text or '' for t in para.iter(
                '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t'))
            if text.strip(): paragraphs.append(text)
text = '\n'.join(paragraphs)
```

**e) Trích xuất đoạn bôi màu (vàng/xanh/đỏ) — review theo vùng đánh dấu:**

Khi user gửi docx có đoạn bôi màu và yêu cầu "review chi tiết những chỗ bôi", phải scan CẢ 3 dạng đánh dấu — bôi vàng thường là `w:highlight`, nhưng **"bôi xanh" trong Word thường là `w:color` value `0000FF` (màu chữ), KHÔNG phải highlight**, và đỏ là `FF0000`. Nhiều HĐ nhận từ đối tác dùng màu chữ thay vì highlight, nên chỉ đọc w:highlight sẽ sót.

```python
import zipfile, xml.etree.ElementTree as ET
W='{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
def marks(rPr):
    if rPr is None: return set()
    out=set()
    hl=rPr.find(W+'highlight')
    if hl is not None: out.add('HL:'+hl.get(W+'val'))
    col=rPr.find(W+'color')
    if col is not None: out.add('COL:'+col.get(W+'val'))
    return out
with zipfile.ZipFile(path) as z: tree=ET.fromstring(z.read('word/document.xml'))
for para in tree.iter(W+'p'):
    runs=[(''.join(t.text or '' for t in r.iter(W+'t')), marks(r.find(W+'rPr'))) for r in para.iter(W+'r')]
    full=''.join(t for t,_ in runs)
    if not full.strip(): continue
    m=set().union(*(x for _,x in runs if x))
    if m: print(f"[{' '.join(sorted(m))}] {full}")
```

Lưu ý khi review: mỗi đoạn bôi riêng lẻ (kể cả bôi nửa câu, tách run) phải in kèm cả paragraph. Xanh/đỏ thường đánh dấu điều khoản đối tác đã thay/cảnh báo — ưu tiên phân tích sâu những đoạn này. Với highlight tách 2 màu trong 1 khoản (VD vàng + đỏ xen kẽ) → hoán đổi/điều kiện phức tạp, cần soi kỹ tham chiếu chéo.

**f) .pdf — pymupdf:**
```python
import fitz
doc = fitz.open('path.pdf')
text = '\n'.join([page.get_text() for page in doc])
```

### Bước 2: Phân tích theo khung 4 bước + Tự phản biện

Áp dụng khung phân tích đã kiểm chứng qua nhiều hợp đồng thực tế:

```
┌─ Bước A — DETECT vấn đề ─────────────────────────────┐
│ • Bản chất hợp đồng (thuần mua bán? hỗn hợp? cấp      │
│   phép? hợp tác?)                                     │
│ • Mâu thuẫn lợi ích tiềm ẩn giữa các bên              │
│ • "Lỗ hổng tử huyệt" ngay từ đầu                      │
├─ Bước B — HÀNH LANG PHÁP LÝ ──────────────────────────┤
│ • Dẫn chiếu điều luật cụ thể (khoản X Điều Y Luật Z)  │
│ • Đối chiếu với quy định pháp luật hiện hành           │
├─ Bước C — LỖ HỔNG & CƠ HỘI ──────────────────────────┤
│ • Phân tích kẽ hở: mỗi bên lợi dụng điểm nào?          │
│ • Cố tình hay vô tình? Cần sửa hay chấp nhận?         │
├─ Bước D — GIẢI PHÁP ──────────────────────────────────┤
│ • Đề xuất sửa đổi cụ thể (nguyên văn điều khoản thay)  │
│ • Xếp nhóm ưu tiên đàm phán                            │
├─ ⚡ Bước E — TỰ PHẢN BIỆN (bắt buộc) ────────────────┤
│ • "Nếu bên kia không chịu sửa thì sao?"               │
│ • Giải pháp dung hòa (compromise)                      │
│ • Nhìn từ góc độ bên kia                               │
│ • Kết luận: ký hay không?                               │
└────────────────────────────────────────────────────────┘
```

> ⚠️ Tự phản biện là bước bắt buộc. Giúp không thiên vị khi chỉ đứng một phía.
> Luật sư giỏi thấy được điểm yếu trong lập luận của chính mình.

Chi tiết cần xác định:
- Chủ thể: năng lực pháp luật, tư cách đại diện, trụ sở
- Đối tượng: hàng hóa/dịch vụ rõ ràng? Tiêu chuẩn chất lượng?
- Giá & thanh toán: cọc, tiến độ, lãi chậm trả
- Giao nhận: thời gian, địa điểm, rủi ro chuyển giao
- Chất lượng: tiêu chuẩn kỹ thuật, phương pháp kiểm tra, xử lý hàng lỗi
- Phạt & bồi thường: mức phạt, giới hạn trách nhiệm
- Bất khả kháng: định nghĩa có quá rộng?
- Tranh chấp: thẩm quyền Tòa/Trọng tài — luôn kiểm tra bất lợi địa lý
- **Hợp đồng hỗn hợp**: mua bán + SHTT + độc quyền + hình ảnh — phân tích từng tầng riêng

### Bước 3: Phân loại mức độ rủi ro

| Mức | Ký hiệu | Ý nghĩa | Hành động |
|:---:|:-------:|---------|-----------|
| TỬ HUYỆT | ⚠️ | Lỗ hổng làm hợp đồng vô hiệu hoặc không thể thực thi | Phải sửa trước khi ký — không thương lượng |
| Cao | 🔴 | Rủi ro tài chính/pháp lý nghiêm trọng | Đàm phán sửa, nếu không được cân nhắc hủy |
| Trung bình | 🟠 | Bất lợi có thể chấp nhận nhưng nên cải thiện | Cố gắng sửa, nếu không thì chấp nhận |
| Thấp | 🟡 | Rủi ro nhỏ, mang tính phòng ngừa | Có thể bỏ qua hoặc ghi nhận |

### Bước 4: Viết đề xuất sửa đổi cụ thể

Mỗi đề xuất gồm:
1. **Trích dẫn nguyên văn** điều khoản hiện tại
2. **Phân tích rủi ro** — tại sao nó bất lợi
3. **Căn cứ pháp lý** — dẫn chiếu điều luật cụ thể
4. **Ví dụ thực tế** (nếu cần, đặc biệt với công thức tính toán)
5. **Đề xuất sửa đổi** — nguyên văn điều khoản thay thế

### Bước 5: Xếp nhóm ưu tiên

| Nhóm | Mô tả | Ví dụ |
|:----:|-------|-------|
| 1️⃣ Cấp bách | TỬ HUYỆT, không ký được nếu chưa sửa | Thiếu chỉ tiêu chất lượng, sai thẩm quyền Tòa |
| 2️⃣ Quan trọng | Nên sửa để bảo vệ quyền lợi | Tỷ lệ cọc quá cao, công thức tính sai |
| 3️⃣ Nên sửa | Phòng ngừa, tăng cường bảo vệ | Mức phạt thấp, thiếu cơ chế xử lý hậu quả |
| 4️⃣ Giữ nguyên | Điểm đã ổn | Quyền nghĩa vụ cơ bản, bất khả kháng chuẩn |

### Bước 6: Xuất bản (tùy chọn — khi user yêu cầu HTML/link)

Sau khi hoàn tất phân tích, xuất bản theo quy trình:

1. Viết file `.md` hoàn chỉnh
2. Nếu cần preview đẹp → chuyển sang HTML theo Premium B/W/Y (nếu user là Quang)
3. Upload lên **preview.thefirstonly.com** (dùng content-publish skill, KV direct — không cần Gist)
4. Nếu user có Notion → tạo standalone page dưới "Blog của Quang" (page_id: `ae7b638f-5ab1-484e-a082-ed2888c8ae05`). Vì nội dung pháp lý không thuộc Sinh học/Chăn nuôi trong DB Kiến thức — dùng markdown body để Notion render + kèm preview link
5. Trả link cho user

---

## WORKFLOW B: SOẠN THẢO HỢP ĐỒNG

Dùng khi user mô tả tình huống và yêu cầu soạn hợp đồng từ đầu.

### Bước 1: Phân tích tình huống (luật sư phản biện trước)

**KHÔNG SOẠN NGAY.** Phản biện trước với user:

- **[ ] Xác định loại hợp đồng**: Mua bán, Dịch vụ, Hợp tác, Chuyển giao CN, SHTT, Lao động...
- **[ ] Xác định chủ thể**: Cá nhân hay tổ chức? Năng lực pháp luật? (VD: GS ở Viện công lập → cần cam kết bảo đảm)
- **[ ] Xác định rủi ro pháp lý nền**: Nafosted/IP ownership, VAST regulations, thuế TNCN
- **[ ] Hỏi user chốt các tham số chính trước khi soạn**: tỷ lệ, thời hạn, điều kiện

> ⚠️ **Nguyên tắc**: Chốt terms với user → user duyệt → mới soạn. Tuyệt đối không soạn khi chưa có xác nhận.

### Bước 2: Quyết định loại văn bản

| Loại | Khi nào dùng | Đặc điểm |
|:----:|--------------|----------|
| **Hợp đồng chính thức** | Quan hệ đã rõ, hai bên sẵn sàng ký | Điều khoản đầy đủ, chặt chẽ, 10-15 điều |
| **Văn bản đề xuất (Proposal)** | Đối tác là viện nghiên cứu/trường đại học, cần thăm dò trước | Tone mềm, trình bày terms để GS đồng ý trước, rồi mới tiến tới HĐ chính thức |

### Bước 3: Chọn định dạng đầu ra

**User preference (Quang): Google Docs là ưu tiên số 1.** Không tạo DOCX trừ khi user yêu cầu cụ thể.

#### Option A — Google Docs (ưu tiên)

Dùng Google Workspace API để tạo Google Docs:

```bash
GAPI="python \"C:/Users/NTQUANG_DELL/AppData/Local/hermes/skills/productivity/google-workspace/scripts/google_api.py\""
$GAPI docs create --title "Tên hợp đồng" --body "Nội dung..."
$GAPI drive share DOC_ID --type anyone --role writer
```

⚠️ **Windows path quirk:** Luôn dùng absolute path với quotes kiểu `"C:/Users/..."` trong bash. Nếu gặp lỗi `Invalid argument`, viết script Python riêng thay vì gọi trực tiếp từ bash.

⚠️ **Wrapper `google_api.py` không đủ khi cần bảng thật / tài liệu dài.** Khi đó viết script Python dùng `google-api-python-client` trực tiếp. Đọc [`references/google-docs-api-pitfalls.md`](references/google-docs-api-pitfalls.md) **TRƯỚC** khi viết — nó ghi lại 3 lỗi làm hỏng 3 lần thử: không set được chiều rộng bảng (400 ở mọi `unit`), quota **60 write request/phút**, và `ConnectionResetError` không được retry. Kèm mẫu `_Doc` buffer + `_retry` đã kiểm chứng.

#### Option B — DOCX (fallback)

Dùng `python-docx` để tạo file Word chuyên nghiệp:

```python
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = Document()
style = doc.styles['Normal']
style.font.name = 'Times New Roman'
style.font.size = Pt(13)
style.paragraph_format.line_spacing = 1.5

# Tiêu đề
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run('HỢP ĐỒNG ...')
run.bold = True
run.font.size = Pt(14)

# Điều khoản
def add_article(num, title):
    p = doc.add_paragraph()
    run = p.add_run(f'ĐIỀU {num}. {title}')
    run.bold = True
    run.font.size = Pt(14)
    run.font.color.rgb = RGBColor(0x1E, 0x40, 0xAF)

def add_clause(num, text):
    p = doc.add_paragraph()
    run = p.add_run(f'{num}. {text}')
    run.font.size = Pt(13)

def add_body(text):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(1)
    run = p.add_run(text)
    run.font.size = Pt(13)
```

**Cấu trúc hợp đồng tiêu chuẩn:**
1. Định nghĩa
2. Quyền và nghĩa vụ các bên
3. Chi phí và thanh toán
4. Thời hạn và tiến độ
5. Cam kết bảo đảm (→ chìa khóa khi đối tác là cán bộ viện công lập)
6. Bảo mật
7. Phạt vi phạm
8. Bất khả kháng
9. Giải quyết tranh chấp (→ luôn chọn Tòa án nơi user có trụ sở)
10. Điều khoản chung

Ký: dùng Table 3 cột (hoặc 1 cột) cho phần chữ ký.

### Bước 4: Lưu & gửi file

```python
output = os.path.expanduser('~/path/to/output.docx')
doc.save(output)
# Gửi file qua Telegram: MEDIA:/absolute/path/to/file.docx
```

### Kỹ thuật sửa hợp đồng DOCX có sẵn (Amendment on existing)

Khi nhận hợp đồng gốc từ đối tác và cần sửa đổi, bổ sung:

1. **Copy** file gốc, sửa trên bản copy — không sửa file gốc
2. **Tô đậm (bold)** toàn bộ phần thêm mới hoặc sửa đổi — dùng màu xanh đậm `RGBColor(0, 0, 180)` nếu muốn nổi bật hơn (theo preference: "tô đậm những phần sửa")
3. **Bỏ cấu trúc CHƯƠNG** — chỉ giữ lại các Điều (theo preference: "bỏ các chương đi để điều thôi"). Xóa paragraph có nội dung `CHƯƠNG` bằng `body.remove(p._element)`
4. Kỹ thuật python-docx:
   - **Chèn paragraph mới giữa văn bản:** dùng `OxmlElement` + `ref_elem.addnext(new_element)` — không dùng `doc.add_paragraph()` vì thêm ở cuối
   - **Sửa paragraph có sẵn:** xóa các run cũ, thêm run mới với `bold=True`
   - **Multi-run paragraph:** `make_multi_run_paragraph([(text, bold, color), ...])` — mỗi run có thể bold riêng
5. **Kiểm tra lỗi run splitting** sau khi sửa: scan các lỗi ghép chữ như "Bên Bchịu", "làn việc"

---

---

## MOU / Biên bản ghi nhớ (Memorandum of Understanding)

Khác hợp đồng: MOU là cam kết thiện chí, ít điều khoản chế tài. Cấu trúc chuẩn cho user (chốt 09/2026, MOU 3 bên Vua Kiềm × Tạp chí NN&MT × Trung tâm Hỗ trợ PT KH&CN):

### Quy trình bắt buộc

1. **Tra pháp nhân TRƯỚC khi soạn** — delegate_task batch (tối đa 3 tasks song song), mỗi task 1 pháp nhân: tên đầy đủ, MST, địa chỉ, người đại diện, ngành nghề + link nguồn, verify chéo ≥2 nguồn độc lập (masothue.com, infodoanhnghiep.com, tratencongty.com, website chính thức). Dữ liệu mẫu + nguồn → [`references/mou-3ben-phap-nhan-verify-2026-09.md`](references/mou-3ben-phap-nhan-verify-2026-09.md)
2. **Báo user + chốt terms trước khi soạn** — tên pháp nhân chuẩn (VD "Manna Đất Vàng" là Công ty **Cổ phần**, không phải TNHH), người ký, thời hạn, sở hữu kết quả, sản phẩm trọng tâm, đề xuất điều khoản chấm dứt/gia hạn để user duyệt.
3. **Draft HTML trước → user duyệt → chuyển Word.** Không nhảy thẳng Word. Chỗ chưa chốt để placeholder nền vàng `[Cần bổ sung]`, không tự bịa.

### Cấu trúc MOU 3 bên chuẩn (13 điều, đã duyệt)

| Điều | Nội dung | Lưu ý |
|:---:|----------|-------|
| 1 | Giải thích từ ngữ | Bên A/B/C, Sản phẩm, Kết quả nghiên cứu, Bí mật kinh doanh |
| 2 | Mục tiêu chung | Đặt ĐẦU văn bản: hợp tác quốc tế – tư vấn chính sách – ấn phẩm chung – giám sát đánh giá định kỳ |
| 3 | Lĩnh vực hợp tác | Mỗi lĩnh vực 1 khoản riêng |
| 4 | Sản phẩm trọng tâm | Ghi ĐÚNG công dụng đã công bố (thức ăn bổ sung/TPBVSK), CẤM claim phòng/điều trị |
| 5 | **Sở hữu kết quả** | Bên sở hữu sản phẩm giữ TOÀN BỘ kết quả/dữ liệu; bên kia khai thác phải có văn bản đồng ý; cấm reverse engineering, cấm đăng ký SHTT từ mẫu |
| 6 | Bảo mật | + 3 ngoại lệ chuẩn (đã công khai, bên thứ ba hợp pháp, cơ quan NN yêu cầu) |
| 7 | Truyền thông | Nội dung quảng bá sản phẩm phải được bên sở hữu duyệt bằng văn bản TRƯỚC khi đăng |
| 8 | Thời hạn + gia hạn | Hiệu lực 5 năm (60 tháng); tự gia hạn 12 tháng trừ khi báo không gia hạn trước 60 ngày |
| 9 | Chấm dứt | 6 trường hợp: hết hạn / đồng thuận / đơn phương báo trước 60 ngày / vi phạm không khắc phục 30 ngày / bất khả kháng >90 ngày / giải thể-phá sản |
| 10 | **Survival clause (user quan tâm nhất)** | Sở hữu + bảo mật TIẾP TỤC có hiệu lực 5 năm sau chấm dứt — tránh "MOU hết hạn là dữ liệu tự do bay ra ngoài". Ghi đậm |
| 11 | Bất khả kháng | Chuẩn BLDS 2015 Điều 351, thông báo 7 ngày làm việc |
| 12 | Tranh chấp | Thương lượng 30 ngày → Tòa án nơi user có trụ sở |
| 13 | Điều khoản chung | MOU non-binding TRỪ sở hữu + bảo mật + tranh chấp; 03 bản mỗi bên 1 bản |

### Pitfalls pháp nhân (thực tế 09/2026)

- ⚠️ **Nhiều đơn vị CÙNG TÊN** — "Trung tâm Hỗ trợ Phát triển KH&CN" có 2 pháp nhân cùng tên ở Hà Nội (MST 0108820368 Hà Đông; MST 0109570801 Giảng Võ) + 1 thương hiệu STTDC thuộc VUSTA. Ghi nhầm MST → MOU vô hiệu. Luôn xin MST + giấy phép từ đối tác, đối chiếu người đại diện (có thể đã đổi so với đăng ký — 0109570801 đăng ký giám đốc Nguyễn Phúc Toàn nhưng thực tế Dương Tùng Bách).
- ⚠️ **Đơn vị sự nghiệp công lập (tạp chí, trung tâm thuộc Bộ) MST thường KHÔNG công khai** trên masothue — phải xin trực tiếp.
- ⚠️ **Phân biệt "Tạp chí X" vs "Báo X"** — khác pháp nhân: Tạp chí NN&MT (nnmt.net.vn, số 10 Nguyễn Công Hoan, TBT TS. Đào Xuân Hưng) ≠ Báo NN&MT (nongnghiep.vn). Ghi rõ địa chỉ trụ sở để tránh nhầm.

Chi tiết + pháp nhân đã verify → [`references/mou-3-ben-manna-tapchi-2026.md`](references/mou-3-ben-manna-tapchi-2026.md) và [`references/mou-3ben-phap-nhan-verify-2026-09.md`](references/mou-3ben-phap-nhan-verify-2026-09.md). Bản draft HTML đã duyệt cấu trúc: `D:/Hermes Proj/MOU-3ben/mou_vuakiem_3ben_draft.html` (copy làm nền cho MOU khác).

## Các loại hợp đồng thường gặp (mở rộng)

| Loại hợp đồng | Đặc điểm | Cần lưu ý |
|:-------------:|----------|-----------|
| **Mua bán hàng hóa** | Hàng nông sản, vật tư, nguyên liệu | Tiêu chuẩn chất lượng, công thức bù hao hụt, độ ẩm |
| **Dịch vụ** | Tư vấn, thiết kế, vận chuyển | Phạm vi công việc rõ, nghiệm thu theo milestone |
| **Hợp tác kinh doanh (BCC)** | Liên doanh, góp vốn | Tỷ lệ góp, chia lợi nhuận, quản lý |
| **Thử nghiệm (Trial/Testing)** | Sản phẩm chưa đủ chứng nhận lưu hành | Disclaimer, nhóm đối chứng, xử lý tổn thất |
| **Hợp tác nghiên cứu (Research Collab)** | Hai bên cùng nghiên cứu → sáng chế | Quyền SHTT rõ ngay từ đầu, nếu chưa rõ → dùng Văn bản đề xuất trước |
| **Chuyển giao công nghệ / SHTT** | Mua bán/cấp phép sáng chế | Đồng tác giả vs Đồng sở hữu — khác nhau về bản chất quyền tài sản |
| **Hỗn hợp (Mixed)** | Mua bán + SHTT + Độc quyền + Hình ảnh | Phân tích từng tầng riêng: tầng mua bán, tầng cấp phép, tầng độc quyền. Kiểm tra mâu thuẫn giữa các tầng. VD: Điều khoản độc quyền mua bán bị vô hiệu hóa bởi ngoại lệ Bên B tự SX hàng riêng — phải phát hiện ngay |
| **Mua bán thiết bị (Equipment Purchase)** | Một lần mua máy móc/thết bị (VD: máy đo KLN) | ⚠️ Phạt hủy HĐ 30% thường gặp nhưng trái Luật Thương mại (tối đa 8%). Cần kiểm tra: tham chiếu điều khoản có sai không? Có quyền kiểm tra hàng trước nhận? Bất khả kháng có định nghĩa chuẩn? Thanh toán 50-30-20 là tối ưu. Luôn yêu cầu CO/CQ nếu có. Bảo hành: phải có ngoại lệ không do lỗi bên mua (chậm xuất HĐ, sai thông tin). ⚠️ **Chậm giao hàng**: phạt 1%/ngày, tối đa 8%. Nếu chậm quá 8 ngày → Bên B có quyền hủy HĐ + hoàn trả toàn bộ tiền. ⚠️ **Accuracy testing**: Bên B được kiểm tra sai số bằng thiết bị chuẩn do Bên A cung cấp, gửi mẫu tới đơn vị kiểm nghiệm độc lập. Nếu sai số >2% → trả hàng, hoàn tiền + chi phí vận chuyển, kiểm nghiệm. ⚠️ **Bảo hành escalation**: lỗi NSX → sửa (lần 1) → sửa (lần 2) → đổi máy mới → hoàn tiền. ⚠️ **Xác nhận lỗi bằng văn bản** trong 03 ngày. |
| **Hợp tác thương mại (đại lý hoa hồng)** | Bên A có SP, Bên B (cá nhân) giới thiệu KH → hưởng % hoa hồng trên doanh thu | ⚠️ **Nhạy cảm**: Bên B có thể đang giữ chức vụ ở công ty khác → không nhắc chức danh trong HĐ. Bảo mật chỉ tập trung chiến lược/chính sách KD (không đưa công thức/quy trình SX). Dùng cung cấp tài liệu thay kiểm tra giám sát. Có cơ chế xác nhận KH bằng văn bản, hoa hồng chỉ tính khi Bên A đã thu tiền. |
| **Tư vấn gọi vốn (Capital Raising/Brokerage)** | Bên A cần vốn, Bên B (cá nhân/tổ chức) môi giới tìm NĐT → hưởng % Giá trị Thương vụ | ⚠️ **Đặc thù**: phân biệt nguồn NĐT (nội bộ/tự giới thiệu) với tỷ lệ hoa hồng khác nhau. **Phải có điều khoản giới hạn thẩm quyền** — Bên B không được ký VB với NĐT thay Bên A. **Thuế TNCN** — Bên B là cá nhân thì Bên A phải khấu trừ 10% tại nguồn (TT 111/2013/TT-BTC Điều 25). Tail period (survival clause) 12 tháng. Chi tiết → [`references/capital-raising-agreement-manna-2026.md`](references/capital-raising-agreement-manna-2026.md). |
| **Phát hành thêm cổ phần / Tăng vốn điều lệ (Share Issuance)** | CTCP muốn huy động vốn bằng cách phát hành cổ phần mới cho NĐT | ⚠️ **ĐỪNG trộn định giá với vốn điều lệ** — vốn điều lệ chỉ nhận tổng mệnh giá CP đã bán (Điều 112.1 LDN 109/2025/QH15). **Bắt buộc** chào bán cho cổ đông hiện hữu trước (thông báo ≥15 ngày, Điều 124). Nghị quyết ĐHĐCĐ cần **≥65% phiếu dự họp** và phải biểu quyết **tại cuộc họp** (Điều 147.2.c, 148.1.a). **CP ưu đãi biểu quyết CHỈ dùng được** trong 3 năm đầu của công ty (Điều 116) — quá hạn là phát hành vô hiệu. Ngưỡng giữ quyền kiểm soát sau pha loãng: tính `50%/k` và `65%/k`. Chi tiết + công thức + checklist → [`references/von-dieu-le-phat-hanh-them-co-phan-2026.md`](references/von-dieu-le-phat-hanh-them-co-phan-2026.md). |
| **NDA - Bên B là cán bộ cơ quan QLNN** | Bên A ký NDA với cá nhân tư vấn, nhưng Bên B thực tế là cán bộ nhà nước trong lĩnh vực liên quan | ⚠️ **Rủi ro hình sự nếu không xử lý đúng**: Luật PCTN 2018 Điều 30 + Luật CBCC 2008 Điều 19. Nguyên tắc: NDA chỉ cần xác định phạm vi dùng thông tin - mục đích càng chung chung càng tốt. Cấm ghi kết nối đầu mối cơ quan quản lý, cấp Bộ, cấp NN. Xem chi tiết + mẫu sửa tại references/nda-civil-servant-benb.md. |
| **Phân phối (Distribution)** | NCC giao quyền phân phối sản phẩm cho NPP tại khu vực | **Điểm tử huyệt**: (1) Thanh toán 100% trước giao hàng — không bao giờ chấp nhận, phải sửa thành cọc 30-50% + 50-70% sau giao; (2) Thời gian khiếu nại ngắn bất hợp lý (VD: 3 giờ) — phải kéo lên tối thiểu 24h cảm quan + 7 ngày chất lượng; (3) Độc quyền dễ bị tước (VD: 2 tháng không đạt 50% target) — đàm phán nâng chu kỳ đánh giá lên 6 tháng; (4) Thu hồi hàng tồn khi chấm dứt mơ hồ — phải quy định rõ giá mua lại (80-90% giá NPP đã mua) và điều kiện áp dụng. Luôn kèm **ma trận bất cân xứng** (xem Workflow C) để chỉ ra hợp đồng đơn phương bảo vệ NCC. |

### Phân tích bất cân xứng quyền lợi — Workflow C (Benefit Imbalance Matrix)

Khi hợp đồng có dấu hiệu một bên chiếm ưu thế, tạo ma trận so sánh từng điều khoản dưới góc nhìn cả hai bên:

```
| Tiêu chí      | Bên A (NCC)    | Bên B (NPP) | Cân bằng? |
|---------------|----------------|-------------|-----------|
| Thanh toán    | ✅ Nhận trước  | ❌ Trả hết  | 🔴 Lệch A |
| Xác nhận đơn  | ✅ Toàn quyền  | ❌ Phụ thuộc| 🔴 Lệch A |
```

Mỗi tiêu chí đánh giá bằng 1 trong 4 mức:
- **🔴 Lệch A** — Bên A được lợi, Bên B chịu rủi ro
- **🟡 Lệch A nhẹ** — Bất lợi nhẹ cho Bên B
- **🟢 Cân bằng** — Hai bên công bằng
- **🔴 Lệch B** — Bên B được lợi (hiếm gặp nếu NCC soạn hợp đồng)

**Mục đích:** Phát hiện hợp đồng đơn phương bảo vệ một bên, tạo bằng chứng trực quan cho đàm phán. Nếu 6/8 tiêu chí lệch về một bên, đó là hợp đồng "bất cân xứng" — NCC có thể đang lợi dụng vị thế.

### So sánh hợp đồng (Contract Comparison) — Workflow D

Khi user gửi **bản tham khảo** và yêu cầu đánh giá so với bản đã soạn:

1. Tạo bảng so sánh theo tiêu chí (số điều, dẫn chiếu pháp lý, thời hạn thanh toán, mức phạt, loại điều khoản)
2. Phân loại: ✅ tốt hơn / ⚠️ thiếu sót / ❌ bất lợi
3. Với mỗi điểm yếu: chỉ rõ **tác động thực tế** (VD: thanh toán 2 ngày → không thực tế → dễ tranh chấp)
4. Kết luận: bản nào tổng thể tốt hơn, đề xuất kết hợp ưu điểm của cả hai
5. Luôn kết nối với user để hỏi ý kiến trước khi ra phiên bản cuối

### Thử nghiệm sản phẩm chăn nuôi — Cấu trúc đặc thù

Khi soạn **Hợp đồng thử nghiệm sản phẩm chăn nuôi** (phụ gia TĂ, chế phẩm sinh học, vaccine...):

**Phân biệt 2 loại thử nghiệm:**

| Loại | Mô tả | Ví dụ | Rủi ro đặc thù |
|:----:|-------|-------|:-------------:|
| **In vivo (trên vật nuôi)** | Thử nghiệm trên đàn vật nuôi thực tế (lợn, gà, tôm...) | Trộn EZ80 vào TĂ cho 140 con lợn thịt | Tổn thất vật nuôi, ASFV, chỉ tiêu FCR/ADG |
| **In vitro (phòng thí nghiệm)** | Thử nghiệm trong PTN (trên tế bào, virus...) | Đánh giá hiệu quả diệt virus ASFV trên tế bào PAM | Lộ mẫu/công thức cho PTN, sở hữu kết quả, reverse engineering |

**Cấu trúc đặc thù cho Hợp đồng thử nghiệm In vitro (Lab Testing):**

| Điều khoản | Mô tả | Bắt buộc? |
|:-----------:|-------|:---------:|
| **Sở hữu kết quả** | Toàn bộ dữ liệu, báo cáo, kết luận thuộc duy nhất Bên A. Bên B không được công bố/sử dụng khi chưa có đồng ý bằng văn bản | 🔴 **TỬ HUYỆT** |
| **Cấm Reverse Engineering** | Bên B không được phân tích ngược, tái tạo, sao chép, đăng ký SHTT từ mẫu sản phẩm của Bên A | 🔴 **TỬ HUYỆT** |
| **Bảo quản & tiêu hủy mẫu** | Mẫu sản phẩm thừa sau thử nghiệm phải trả lại hoặc tiêu hủy, có biên bản | 🟠 |
| **Quyền giám sát** | Bên A có quyền cử người chứng kiến quá trình thử nghiệm | 🟠 |
| **Cam kết thời gian** | Thời gian trả kết quả cụ thể (VD: 30 ngày kể từ khi nhận mẫu), không ghi "theo thời gian thực tế" | 🟠 |
| **Xử lý sai sót** | Nếu kết quả sai (dương/âm tính giả), Bên B phải làm lại miễn phí + bồi thường nếu có thiệt hại | 🟠 |
| **Tiêu chuẩn đánh giá** | Phải ghi rõ ngưỡng kết luận (VD: giảm ≥4 log10 so với đối chứng là có hiệu quả) | 🟡 |

**Lưu ý:** Khi đối tác là viện/trường đại học (cơ quan công lập), cần thêm cam kết bảo đảm về quyền SHTT — vì theo Luật KH&CN 2013, nếu sử dụng CSVC nhà nước, quyền có thể thuộc tổ chức chủ quản.

**Khi nhận được mẫu hợp đồng từ đối tác (viện/trường) cần kiểm tra kỹ các điều khoản THIẾU — không chỉ các điều khoản SAI. Đây là thủ thuật phổ biến: bên soạn "quên" đưa các điều khoản có lợi cho bên kia.** Checklist khi review hợp đồng thử nghiệm do đối tác gửi:

- [ ] Có điều khoản sở hữu kết quả thuộc Bên A không? Nếu không → 🔴 TỬ HUYỆT
- [ ] Có điều khoản cấm reverse engineering/đăng ký SHTT từ mẫu không? Nếu không → 🔴 TỬ HUYỆT
- [ ] Có thời hạn bảo mật sau khi HĐ kết thúc không?
- [ ] Bên A có quyền kiểm tra/giám sát không?
- [ ] Thời gian trả kết quả có cam kết cụ thể không?
- [ ] Có chế tài khi kết quả sai không?
- [ ] Có quy định phí phát sinh (làm lại, kiểm tra bổ sung) không?
- [ ] Điều khoản thanh toán: trả sau khi có kết quả và hóa đơn → bao nhiêu ngày?
- [ ] Có lỗi soạn thảo (ghi sai bên, sai số điều) không?
- [ ] Có quy định xử lý hàng mẫu thừa sau thử nghiệm không?

**Điều khoản đặc thù cần có:**
- **Nhóm thử nghiệm & Nhóm đối chứng** — số lượng, điều kiện, tiêu chí so sánh
- **Xử lý tổn thất (Mortality clause)** — Bên A chịu trách nhiệm khi có kết luận chuyên môn; miễn trừ với dịch bệnh diện rộng, lỗi chăn nuôi
- **Disclaimer quan trọng**: *"Sản phẩm hỗ trợ tăng cường sức đề kháng, không phải thuốc điều trị đặc hiệu. Hiệu quả phụ thuộc giai đoạn nhiễm bệnh, thể trạng vật nuôi, điều kiện vệ sinh thú y."*
- **Giới hạn trách nhiệm**: tối đa không vượt quá giá trị lô sản phẩm thử nghiệm

**Điều khoản ghi nhớ hợp tác dài hạn (Gentle Continuation Clause):**
Khi user muốn Bên B tiếp tục mua hàng nếu kết quả tốt, nhưng không ép buộc, dùng cấu trúc:

```text
Điều X: GHI NHỚ HỢP TÁC CHIẾN LƯỢC

X.1. Hai bên cùng ghi nhận và kỳ vọng rằng, nếu kết quả thử nghiệm đạt các chỉ tiêu
khoa học và hiệu quả kinh tế theo đánh giá chung, hai bên sẽ ưu tiên thương lượng,
tiến tới ký kết hợp đồng thương mại dài hạn để Bên B tiếp tục sử dụng sản phẩm của
Bên A cho hoạt động chăn nuôi.

X.2. Nội dung thương lượng sẽ dựa trên các điều kiện thương mại hợp lý, phù hợp với
quy mô và nhu cầu thực tế của hai bên tại thời điểm ký kết, trên tinh thần cùng có
lợi và phát triển bền vững.

X.3. Điều khoản này là cam kết ghi nhận thiện chí hợp tác, không mang tính ràng buộc
pháp lý về nghĩa vụ ký kết hợp đồng thương mại, và không làm phát sinh trách nhiệm
bồi thường nếu các bên không đạt được thỏa thuận thương mại cuối cùng.
```

**Lưu ý:** Dùng "Ghi nhớ" (Memorandum) thay vì "Cam kết" (Commitment). Không dùng từ "bắt buộc", "phải", "nghĩa vụ". Mục đích là tạo thiện chí và ưu tiên thương lượng, không tạo ràng buộc pháp lý.

**Điều khoản cam kết sử dụng toàn diện (Binding Conditional Commitment):**

Khi user (Bên A) muốn một **cam kết mạnh hơn** từ Bên B — nếu thử nghiệm thành công, Bên B sẽ triển khai sản phẩm trên diện rộng — sử dụng cấu trúc **2 tầng**:

| Tầng | Điều khoản | Tính chất | Mục đích |
|:----:|:----------:|:---------:|----------|
| **Tầng 1 — Mềm** | Điều X: Ghi nhớ Hợp tác | Không ràng buộc pháp lý | Thiện chí, ưu tiên thương lượng dài hạn |
| **Tầng 2 — Cứng** | Điều XA: Cam kết Sử dụng Toàn diện | **Ràng buộc pháp lý** | Nếu đủ điều kiện, Bên B bắt buộc triển khai đại trà |

**Cấu trúc Điều khoản Cam kết Sử dụng Toàn diện (mẫu):**

```text
Điều 10A. CAM KẾT SỬ DỤNG TOÀN DIỆN

10A.1. Bên B cam kết thực hiện thí nghiệm trên đàn lợn tối thiểu 140 con,
chia Nhóm TN (sử dụng sản phẩm) và Nhóm ĐC theo đúng Đề cương thử nghiệm.

10A.2. Điều kiện kích hoạt cam kết — kết quả thu hoạch Nhóm TN đạt cả 4 tiêu chí:
  (a) Chỉ tiêu tăng trưởng (ADG, ADFI, FCR) tương đương hoặc cao hơn Nhóm ĐC;
  (b) Sức khỏe đàn (tỷ lệ sống, tiêu chảy, can thiệp thú y) không thấp hơn Nhóm ĐC;
  (c) Chất lượng thịt & ngoại hình đạt yêu cầu tương đương Nhóm ĐC;
  (d) An toàn môi trường: không dư lượng hóa chất độc hại vượt chuẩn,
      chất thải chăn nuôi trong ngưỡng cho phép, được hai bên/cơ quan chuyên môn xác nhận.

10A.3. Khi điều kiện 10A.2 đáp ứng và được hai bên xác nhận bằng Biên bản nghiệm thu,
Bên B cam kết đưa sản phẩm vào sử dụng trên diện rộng cho TẤT CẢ trại nuôi
thuộc hệ thống (hiện tại + tương lai), khối lượng thương mại ổn định, lâu dài.

10A.4. Cam kết có hiệu lực ràng buộc pháp lý, là căn cứ thương lượng HĐ thương mại
dài hạn. Tranh chấp giải quyết theo Điều khoản Giải quyết Tranh chấp của HĐ.

10A.5. Nếu kết quả TN không đạt điều kiện 10A.2 → hai bên cùng phân tích nguyên nhân,
cam kết tại Điều này không còn hiệu lực.
```

**Khi nào dùng tầng 2 (binding):**
- Bên A có sản phẩm thực sự vượt trội, muốn buộc Bên B cam kết đầu ra
- Bên B là đối tác chiến lược tiềm năng (trang trại lớn, chuỗi nhiều trại)
- Bên A chấp nhận rủi ro tài trợ 50% thử nghiệm, đổi lại cam kết thương mại

**Khi nào KHÔNG dùng tầng 2:**
- Bên B chưa có thiện chí mạnh, có thể từ chối ký HĐ vì điều khoản này
- Sản phẩm chưa có thương hiệu / chưa từng thử nghiệm — Bên B sẽ không dám cam kết
- Chỉ cần thiện chí là đủ (dùng tầng 1 là đã OK)

**Cập nhật bảng thành phần & Phụ lục A:**
- Sử dụng "tài trợ 50%" thay vì "chiết khấu 50%" — từ "tài trợ" thể hiện đối tác và thiện chí hơn
- Dẫn chiếu tất cả bằng sáng chế liên quan (VD: cả 59801 và 41442), không chỉ 1 cái — tăng vị thế KHCN
- Thời hạn thanh toán thực tế: 10-15 ngày, tuyệt đối không dùng 02 ngày (không thực tế, dễ tranh chấp)

**Cấu trúc Phụ lục A (Thông tin sản phẩm):**
- Thành phần (bảng chỉ tiêu, hàm lượng min/max)
- Công dụng (liệt kê mục tiêu hỗ trợ)
- Hướng dẫn sử dụng (liều lượng, cách phối trộn, thời gian)
- Bảo quản và lưu ý
- Disclaimer về hiệu quả phụ thuộc điều kiện thực tế

**ASFV / Dịch bệnh Clause:**
- Bên A cung cấp sản phẩm hỗ trợ (phác đồ thay thế/đặc thù)
- Tỷ lệ chiết khấu, thời gian hỗ trợ tối đa
- Nghĩa vụ thông báo (24h) + phối hợp cơ quan thú y
- Tuân thủ quy định phòng dịch
- ⚠️ Luôn disclaimer: *"Sản phẩm hỗ trợ tăng cường đề kháng, không phải thuốc điều trị đặc hiệu"*

#### 🔴 RANH ĐỎ: đàn ĐÃ mắc bệnh thuộc danh mục cấm chữa — không soạn được HĐ

Trước khi soạn/review bất kỳ HĐ nào có yếu tố "giải cứu", "phác đồ đặc thù", "hỗ trợ đàn mắc bệnh", **phải xác định đàn đã mắc bệnh gì**. Nếu là bệnh thuộc **Danh mục bệnh động vật cấm giết mổ, chữa bệnh** thì không điều khoản nào cứu được hợp đồng:

- **Điều 13.17 Luật Thú y 2015** — nghiêm cấm *giết mổ, chữa bệnh* động vật mắc bệnh thuộc danh mục đó.
- **mục 1.9 Phụ lục 01 TT 07/2016/TT-BNNPTNT (sđ TT 24/2019)** — **Bệnh Dịch tả lợn Châu Phi (ASF)** thuộc danh mục này.
- → Mục đích + nội dung giao dịch vi phạm điều cấm → **vô hiệu theo BLDS 2015 Điều 117.1.c + Điều 123**, hậu quả theo **Điều 131**.
- → Tầng hình sự: **Điều 241 BLHS** (làm lây lan dịch bệnh nguy hiểm cho động vật), khung tới **7 năm tù**, ngưỡng thiệt hại từ **100 triệu đồng** — đàn vài nghìn con vượt ngưỡng rất nhanh.

**Đừng để tên HĐ đánh lừa.** HĐ ghi "hỗ trợ tăng sức đề kháng" và không có chữ ASF nào vẫn có thể là HĐ chữa ASF. Dấu vết nhận diện: chữ "**giải cứu**", xét nghiệm **Real-time PCR** định kỳ, điều khoản loại trừ *"dịch bệnh bùng phát mạnh **ngoài khả năng kiểm soát của sản phẩm**"*, và **ngưỡng chết cao bất thường** cho đàn lợn thịt khỏe.

**Hệ quả bắt buộc:** xét nghiệm khẳng định tình trạng đàn tại **ngày 0**. Dương tính → dừng, không ký (khai báo thú y, tiêu hủy, xin hỗ trợ). Âm tính → bỏ chữ "giải cứu", bỏ PCR virus, bỏ ngưỡng chết, và **thêm điều khoản tuân thủ Luật Thú y** (nghĩa vụ khai báo + phối hợp cơ quan thú y). HĐ thu thập dữ liệu lợn chết hàng ngày mà **không có một dòng nào về nghĩa vụ khai báo** là dấu hiệu xấu nếu vụ việc ra tòa.

#### Kiểm tra tính đủ của số lượng sản phẩm TĂCN (bắt buộc)

HĐ bán TĂCN theo liều rất hay tự mâu thuẫn: phác đồ ghi "dùng đến khi xuất chuồng" nhưng số lượng chỉ đủ vài ngày. **Luôn tính ngược lại:**

- **Dạng bột trộn thức ăn:** `tăng trọng = số con × (khối lượng xuất − khối lượng vào)` → `thức ăn cần = tăng trọng × FCR (~2,7 lợn thịt)` → `lượng SP = thức ăn × liều (kg/tấn)`.
- **Dạng lỏng pha nước uống:** `nước uống/ngày = số con × 0,1 lít/kg thể trọng bình quân` → chia tỷ lệ pha (1:20 → 21 lít nước/lít SP) → nhân số ngày từng giai đoạn.

Nêu rõ FCR và lượng nước uống là **giả định** để user thay số thực tế của trại — giữ được kết luận về bậc độ lớn mà không nêu số không nguồn. Case đã kiểm chứng: [`references/hopdong-giai-cuu-dan-lon-asf-2026.md`](references/hopdong-giai-cuu-dan-lon-asf-2026.md) (1.000 kg bột ≈ 52% nhu cầu; 2.000 lít lỏng ≈ 31%).

### Thêm Điều Định nghĩa (Definitions Article) khi soạn hợp đồng mới

Luôn thêm **Điều 1: GIẢI THÍCH TỪ NGỮ** khi soạn hợp đồng từ đầu, đặc biệt khi có các khái niệm chuyên ngành hoặc cấu trúc doanh nghiệp phức tạp:

```text
ĐIỀU 1. GIẢI THÍCH TỪ NGỮ

1.1. "Hợp đồng": Là Hợp đồng này và các Phụ lục kèm theo (nếu có).
1.2. "Bên A": Là [tên tổ chức/cá nhân], [vai trò].
1.3. "Bên B": Là [tên tổ chức/cá nhân], [vai trò].
1.4. "Đơn vị thương mại": Là [tên công ty con được chỉ định], công ty con do Bên A chỉ định
     để khai thác thương mại kết quả của Hợp đồng này.
1.5. "Sáng chế": Là các sáng chế, giải pháp hữu ích phát sinh từ Hợp đồng,
     bao gồm mọi sáng chế phát triển tiếp theo, phái sinh, bổ trợ.
1.6. "Kết quả nghiên cứu": Là toàn bộ dữ liệu, số liệu, báo cáo, bản thảo, quy trình,
     công thức, bí quyết kỹ thuật được tạo ra trong quá trình thực hiện Hợp đồng.
1.7. "Bí mật kinh doanh": Là các thông tin quy định tại Điều [Bảo mật] của Hợp đồng.
1.8. "Doanh thu thuần": Là doanh thu thuần hợp nhất hàng năm của Đơn vị thương mại
     đã được kiểm toán độc lập theo quy định pháp luật Việt Nam.
1.9. "Các bên": Là Bên A và Bên B.
```

**Các định nghĩa cần thiết tối thiểu:**
- Chủ thể (Bên A, Bên B, Đơn vị liên quan)
- Đối tượng hợp đồng (sản phẩm, dịch vụ, kết quả)
- Cơ sở tính toán tài chính (doanh thu thuần, lợi nhuận, phí)
- Thuật ngữ chuyên ngành
- Bí mật/bảo mật

**Cấu trúc 2 công ty (R&D + Thương mại):** Khi user có 2 pháp nhân — một công ty nắm IP/R&D, một công ty con làm thương mại:
- Bên A ký hợp đồng = công ty IP (chủ sở hữu sáng chế)
- Doanh thu để tính thưởng = doanh thu của công ty thương mại (không phải công ty IP)
- Định nghĩa rõ "Đơn vị thương mại" ngay từ Điều 1 để tránh nhầm lẫn
- Luôn yêu cầu kiểm toán độc lập cho số liệu doanh thu

### Đánh số lại điều khoản (Renumbering Articles)

Khi cần **thêm/xóa điều khoản giữa chừng** trong hợp đồng DOCX đã có, quy trình:

**Bước 1 — Đánh số lại tiêu đề:**
```python
for p in doc.paragraphs:
    import re
    m = re.match(r'ĐIỀU\s+(\d+)\.', p.text.strip())
    if m:
        old_n = int(m.group(1))
        new_n = old_n + 1  # hoặc -1 nếu xóa
        for run in p.runs:
            if f'ĐIỀU {old_n}.' in run.text:
                run.text = run.text.replace(f'ĐIỀU {old_n}.', f'ĐIỀU {new_n}.')
```

**Bước 2 — Cập nhật tham chiếu chéo trong thân văn bản (QUAN TRỌNG — tránh cascade):**
```python
def update_refs(text):
    def replacer(m):
        num = int(m.group(1))
        if 5 <= num <= 14:  # khoảng số điều cần tăng
            return f'Điều {num + 1}'
        return m.group(0)
    return re.sub(r'Điều\s+(\d+)(?![0-9])', replacer, text)
```

⚠️ **Vấn đề cascade:** Không dùng `str.replace` tuần tự (VD: Điều 6→7, rồi Điều 7→8...) vì kết quả của bước trước bị bước sau thay tiếp → sai số. Dùng `re.sub` với callback MỘT LẦN trên mỗi đoạn text.

⚠️ **Vấn đề run splitting:** DOCX có thể chia "Điều 8" thành 2 run ("Điều " ở run A, "8" ở run B). Regex trên từng run riêng lẻ sẽ không match. Giải pháp:
- Với text đơn giản: thay thế trên full paragraph, rồi gán lại vào run đầu tiên, xóa các run còn lại
- Với text giữ nguyên format: cần scan paragraph text trước, phát hiện reference bị split, rồi fix từng run cụ thể

**Bước 3 — Thêm Điều mới:**
Chèn paragraph element trực tiếp vào `body` (tránh dùng `doc.add_paragraph()` vì sẽ thêm ở cuối):
```python
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

new_p = OxmlElement('w:p')
r = OxmlElement('w:r')
rPr = OxmlElement('w:rPr')
...# tạo run với text
body = doc.element.body
body.insert(list(body).index(reference_element), new_p)
```

### Đối tác là viện/trường công lập — Chiến thuật ký kết

| Tình huống | Giải pháp | Mức rủi ro |
|:----------:|-----------|:----------:|
| GS ký cá nhân | Hợp đồng chính thức + cam kết bảo đảm + bồi thường nếu tổ chức khiếu nại | 🟠 Tùy mức ràng buộc |
| GS cần thăm dò trước | Văn bản đề xuất (Proposal) → GS ký "Đồng ý & Tiếp nhận" → sau đó mới soạn hợp đồng chính thức | 🟢 An toàn, tạo thiện chí |
| Ký 3 bên (Công ty + GS + Viện) | An toàn nhất, Viện chính thức cho phép | 🟢 An toàn nhất |

> 📌 **Lưu ý**: với đối tác là viện nghiên cứu công lập (VAST, trường ĐH), **Luật KH&CN 2013 Điều 40** quy định quyền SHTT thuộc tổ chức chủ trì nếu sử dụng ngân sách NN hoặc CSVC của tổ chức.

### Cấu trúc hoa hồng (Commission) — Hợp đồng đại lý thương mại

Khi soạn hợp đồng có hoa hồng dạng % trên doanh thu:

| Tham số | Khuyến nghị | Lý do |
|---------|-------------|-------|
| **Tỷ lệ** | Năm đầu cao hơn (12%), các năm sau thấp hơn (10%) | Khuyến khích Bên B giai đoạn đầu, giảm dần khi SP đã có thị trường |

### Cấu trúc thanh toán mua bán thiết bị (50-30-20)

Khi soạn hợp đồng mua bán thiết bị/máy móc một lần, cấu trúc thanh toán tối ưu cho bên mua:

| Đợt | Tỷ lệ | Điều kiện thanh toán | Mục đích |
|:---:|:-----:|:--------------------|----------|
| **1** | **50%** | Sau khi ký Hợp đồng (tạm ứng) | Đủ nguyên liệu cho sản xuất/nhập khẩu |
| **2** | **30%** | Sau khi giao hàng + bên mua xác nhận đã nhận | Giữ lại 20% làm đòn bẩy kiểm tra chất lượng |
| **3** | **20%** | Sau khi hai bên ký Biên bản nghiệm thu + bên bán xuất hóa đơn | Đảm bảo hàng đúng chất lượng mới thanh toán dứt điểm |

**Không dùng:** Thanh toán 100% trước khi giao hàng, hoặc 100% sau khi giao hàng (mất đòn bẩy cho cả hai bên).

### Định nghĩa Bất khả kháng chuẩn

```text
Sự kiện bất khả kháng là sự kiện xảy ra khách quan, không thể lường trước được và không thể
khắc phục được mặc dù đã áp dụng mọi biện pháp cần thiết và trong khả năng cho phép, bao gồm
nhưng không giới hạn: thiên tai, hỏa hoạn, bão lụt, động đất, dịch bệnh, chiến tranh, biểu tình,
đình công, thay đổi chính sách hoặc quyết định của cơ quan nhà nước có thẩm quyền.

Bên chịu ảnh hưởng phải thông báo ngay cho bên kia bằng văn bản trong thời hạn 07 (bảy) ngày
làm việc kể từ ngày xảy ra sự kiện và đề xuất phương án khắc phục. Các bên sẽ cùng nhau thương
lượng để điều chỉnh thời hạn thực hiện hợp đồng tương ứng với thời gian bị ảnh hưởng.
```

Dựa trên BLDS 2015 Điều 351 – Sự kiện bất khả kháng. Không dùng "tự động thanh lý" — thay bằng "Hợp đồng được xem là đã thanh lý khi hai bên hoàn thành đầy đủ các nghĩa vụ (giao đủ hàng, thanh toán đủ tiền, ký nghiệm thu, xuất hóa đơn), nhưng bảo hành và các nghĩa vụ liên quan (bảo mật, giải quyết tranh chấp) vẫn tiếp tục có hiệu lực sau thanh lý".
| **Kỳ thanh toán** | Hàng tháng + 15 ngày làm việc | Đủ nhanh để Bên B có dòng tiền, đủ chậm để Bên A tổng hợp số liệu |
| **Xác nhận KH** | Bằng văn bản (email) TRƯỚC giao dịch đầu tiên | Tránh tranh chấp "ai giới thiệu khách hàng này" |
| **Điều kiện phát sinh hoa hồng** | Bên A đã thu được tiền từ KH | Gắn trách nhiệm thu hồi công nợ với Bên A |
| **Hoa hồng sau chấm dứt HĐ** | Giới hạn (VD: 6 tháng), chỉ cho KH cũ | Không để Bên B hưởng hoa hồng vô thời hạn |
| **Chậm trả** | Phạt 0,05%/ngày | Bảo vệ Bên B |

### Cân bằng chế tài 2 bên (Balanced Penalties)

Nguyên tắc: **Hợp đồng không được đơn phương bảo vệ một bên.** Mọi vi phạm của Bên A cũng phải có chế tài tương ứng với vi phạm của Bên B.

| Khoản | Bên B (cá nhân) | Bên A (công ty) |
|:-----:|:----------------:|:----------------:|
| Bảo mật | **50M** + bồi thường + mất hoa hồng | — |
| Cạnh tranh | **30M** + mất hoa hồng | — |
| Chậm thanh toán | — | Lãi 0,05%/ngày |
| Vi phạm nghiêm trọng | — | Bên B được chấm dứt HĐ + bồi thường |
| Vi phạm khác (cả 2) | 30 ngày khắc phục → chấm dứt HĐ | 30 ngày khắc phục → chấm dứt HĐ |
| Chậm giao hàng (Bên A) | — | Phạt 0,1%/ngày, tối đa 8% giá trị HĐ |

**Lưu ý mức phạt:** Nếu Bên B là cá nhân, mức 200M cho bảo mật là quá cao — giảm xuống 50M. Mức 100M cho cạnh tranh giảm xuống 30M. Lý do: cá nhân không có khả năng tài chính như doanh nghiệp; phạt quá cao gây mất thiện chí hoặc Bên B từ chối ký.

| Tham số | Khuyến nghị | Lý do |

### Yếu tố nhạy cảm khi Bên B là cá nhân có chức vụ ở công ty khác

Nếu Bên B đang giữ chức vụ (Giám đốc, Trưởng phòng...) ở một công ty khác:
- **KHÔNG** ghi chức danh/công ty đó trong hợp đồng
- **KHÔNG** nói "Bên B sử dụng vị trí tại..." — chỉ "trên cơ sở uy tín, mạng lưới quan hệ"
- **KHÔNG** đưa công thức/quy trình SX/bí quyết CN vào bảo mật — Bên B không tiếp cận
- Bảo mật chỉ gồm: chiến lược KD, chính sách thương mại, thông tin KH, giá bán
- Quyền SHTT: không liệt kê bằng sáng chế, chỉ ghi "nhãn hiệu, kiểu dáng, bí mật KD"
- Giám sát: dùng "cung cấp tài liệu" thay "kiểm tra, giám sát"

| Tham số | Khuyến nghị |
|---------|-------------|
| **Cơ sở tính** | Doanh thu thuần (minh bạch) > Lợi nhuận sau thuế (dễ điều chỉnh sổ sách). Nếu dùng LNST → phải định nghĩa chặt + quyền kiểm toán |
| **Thời hạn** | 10-15 năm hoặc thời hạn bảo hộ sáng chế. KHÔNG vô thời hạn |
| **Mức phổ biến** | 2-5% doanh thu hoặc 3-8% LNST |
| **Kiểm soát** | Quyền kiểm toán độc lập; nếu sai lệch >5% → bên trả chịu phí |
| **Thuế** | Ghi rõ gross (trước thuế TNCN) → GS tự nộp, hoặc công ty khấu trừ |

### ⚠️ DOCX Editing: Xử lý Run Splitting

Khi chỉnh sửa DOCX bằng python-docx, nội dung text có thể bị chia thành nhiều `<w:r>` (run) trong XML. Các tình huống thường gặp:

**Tình huống 1 — Số điều nằm riêng:** Word tách "Điều 4. TỔNG GIÁ TRỊ" thành Run 0="Điều ", Run 1="4", Run 2=". TỔNG GIÁ TRỊ". `p.text` trả về đúng "Điều 4. TỔNG GIÁ TRỊ" nhưng mỗi run chỉ chứa một phần. Fix: tìm run có nội dung là số rồi đổi số đó.\n\n```python\n# SAI — string replace không match vì "Điều 4." không nằm trọn trong 1 run\nrun.text = run.text.replace('Điều 4.', 'Điều 3.')\n\n# ĐÚNG — tìm run có nội dung là số\nfor run in p.runs:\n    if run.text.strip() == '4':\n        run.text = '3'\n\n# ĐÚNG — regex match số từ p.text rồi tìm run chứa số cũ\nimport re\nm = re.match(r'ĐIỀU\\s+(\\d+)\\.', p.text.strip())\nif m:\n    old_n = m.group(1)\n    for run in p.runs:\n        if run.text.strip() == old_n:\n            run.text = str(int(old_n) + 1)  # hoặc -1
```

**Tình huống 2 — Text bị split không có space:** "Bên B" ở Run 3, "chịu" ở Run 4 -> hiển thị "Bên Bchịu". Fix: thêm space vào đầu Run 4.

```python
if not run4.text.startswith(' '):
    run4.text = ' ' + run4.text
```

**Tình huống 3 — Cross-reference cascade khi dùng str.replace tuần tự:**

```python
# SAI — cascade: Điều 6->7, rồi Điều 7->8 tiếp... đến Điều 10 hết
for old, new in {'Điều 6':'Điều 7','Điều 7':'Điều 8'}.items():
    run.text = run.text.replace(old, new)  # Bị cascade!

# DUNG — dùng re.sub với callback, increment 1 lần duy nhất
import re
def update_refs(text):
    def replacer(m):
        num = int(m.group(1))
        if 5 <= num <= 14:
            return f'Điều {num + 1}'
        return m.group(0)
    return re.sub(r'Điều\s+(\d+)(?![0-9])', replacer, text)
```

### ⚠️ insert_after: Xử lý cả Paragraph lẫn raw XML element

Khi chèn paragraph mới sau một paragraph khác, `insert_after` cần nhận cả `python-docx Paragraph` lẫn raw `CT_P` element (do `make_para()` trả về XML element, không phải Paragraph). Nếu không check, lỗi `AttributeError: 'CT_P' object has no attribute '_element'`:

```python
def insert_after(ref_para, new_element):
    elem = ref_para._element if hasattr(ref_para, '_element') else ref_para
    elem.addnext(new_element)
```

Khi chaining nhiều insert (chèn A rồi B sau A), truyền element XML trực tiếp: `insert_after(new_a_element, new_b_element)` — không cần wrap lại thành Paragraph.

### ❌ Định số kiểu Việt Nuốt nhầm dấu chấm câu

Khi định dạng số thập phân theo kiểu Việt, **tuyệt đối không** dùng `.replace('.', ',')` áp lên cả câu văn. Câu chứa lẫn số và dấu chấm kết thúc câu sẽ bị hỏng: "Rủi ro 1. Tỷ lệ hiện tại..." thành "Rủi ro 1, Tỷ lệ hiện tại...". Văn bản pháp lý bị đổi dấu chấm thành phẩy là lỗi nghiêm trọng, đối tác đọc thấy ngay.

```python
# SAI — nuốt hết dấu chấm trong câu
add_text(f"Rủi ro 1. Tỷ lệ hiện tại của Chủ tịch. Nếu từ {x:.2f}% đến dưới {y:.2f}% thì ...".replace('.', ','))

# ĐÚNG — format riêng từng con số
def vn(x, dec=2):
    return f"{x:.{dec}f}".replace('.', ',')

add_text(f"Rủi ro 1. Tỷ lệ hiện tại của Chủ tịch. Nếu từ {vn(x)}% đến dưới {vn(y)}% thì ...")
```

Áp dụng cho mọi tài liệu có số kiểu Việt: hợp đồng, phụ lục, bảng tính, văn bản trình. Sau khi sinh, scan lại các dòng có pattern `số + chữ hoa ngay sau dấu phẩy` để bắt lỗi. Lưu ý thêm: `replaceAllText` của Google Docs API sửa được lỗi này trực tiếp trên tài liệu đã tạo, không cần làm lại từ đầu.

**Quy trình kiểm tra sau khi sửa DOCX — bắt buộc:**

```python
# Sau mọi batch chỉnh sửa, scan các lỗi phổ biến:
for i, p in enumerate(doc.paragraphs):
    t = p.text.strip()
    if 'mười năm' in t: print(f'Lỗi tại para {i}')
    if 'Bên Bhịu' in t or 'BênB' in t: print(f'Lỗi tại para {i}')
    if 'cho Bên B' in t and 'phiếu kết quả' in t: print(f'Lỗi tại para {i}')
    if 'làn việc' in t: print(f'Lỗi tại para {i}')
```

**Tạo paragraph element mới để chèn giữa:**

Không dùng `doc.add_paragraph()` (thêm ở cuối). Dùng OxmlElement để chèn vào vị trí cụ thể:

```python
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def make_p(text, indent='720', color=None):
    p = OxmlElement('w:p')
    pPr = OxmlElement('w:pPr')
    spacing = OxmlElement('w:spacing')
    spacing.set(qn('w:before'), '60'); spacing.set(qn('w:after'), '60')
    pPr.append(spacing)
    if indent:
        ind = OxmlElement('w:ind'); ind.set(qn('w:left'), indent)
        pPr.append(ind)
    p.append(pPr)
    r = OxmlElement('w:r')
    rPr = OxmlElement('w:rPr')
    sz = OxmlElement('w:sz'); sz.set(qn('w:val'), '24'); rPr.append(sz)
    if color:
        c = OxmlElement('w:color'); c.set(qn('w:val'), color); rPr.append(c)
    r.append(rPr)
    t = OxmlElement('w:t'); t.set(qn('xml:space'), 'preserve')
    t.text = text; r.append(t); p.append(r)
    return p

# Chèn trước reference element
body = doc.element.body
idx = list(body).index(ref_elem)
body.insert(idx, new_p)
```

## Các cấu trúc SHTT thường gặp

| Cấu trúc | Mô tả | Khi nào dùng | Rủi ro |
|:---------:|-------|:------------:|:------:|
| **Đồng sở hữu sáng chế** | Cả 2 bên cùng là chủ sở hữu, tỷ lệ X/Y | Đối tác góp vốn/chuyên môn ngang hàng | Phức tạp khi chuyển nhượng, cấp phép |
| **Đồng tác giả (không sở hữu)** | Một bên sở hữu 100%, bên kia chỉ ghi tên + hưởng thù lao | Đối tác là viện nghiên cứu, cần tên cho academic CV | Cần cam kết bảo đảm từ tổ chức chủ quản |
| **Chuyển nhượng** | Mua đứt sáng chế từ tác giả | Đã có sáng chế, muốn sở hữu hoàn toàn | Chi phí lớn |
| **Cấp phép (License)** | Giữ sở hữu, cho phép sử dụng có thu phí | Chưa muốn bán, muốn giữ quyền | Cần quản lý, giám sát |

### Lưu ý đặc thù khi đối tác là viện/trường công lập

- **Luật KH&CN 2013, Điều 40**: Quyền SHTT thuộc tổ chức chủ trì nếu sử dụng ngân sách NN hoặc CSVC của tổ chức.
- **Nafosted (QĐ 41/2014/QĐ-TTg)**: IP từ đề tài Nafosted thuộc tổ chức chủ trì, không phải cá nhân.
- **Giải pháp thực tế**: Ký trực tiếp với GS + cam kết bảo đảm + bồi thường nếu tổ chức khiếu nại. Hoặc ký 3 bên (công ty + GS + viện).

### Quy tắc chia sẻ lợi ích

| Tham số | Khuyến nghị |
|---------|-------------|
| **Cơ sở tính** | Doanh thu thuần (minh bạch) > Lợi nhuận sau thuế (dễ điều chỉnh sổ sách) |
| **Thời hạn** | 10-15 năm hoặc thời hạn bảo hộ sáng chế. KHÔNG vô thời hạn. |
| **Mức phổ biến** | 2-5% doanh thu hoặc 3-8% LNST |
| **Kiểm soát** | Quyền kiểm toán độc lập; nếu sai lệch >5% → bên trả chịu phí |
| **Thuế** | Ghi rõ gross (trước thuế TNCN) → GS tự nộp, hoặc công ty khấu trừ |

### Sửa trên nền hợp đồng đối tác (Amendment-on-Template)

Khi đối tác gửi hợp đồng mẫu cần bổ sung nhiều điều khoản quan trọng — thay vì soạn hợp đồng mới hoàn toàn (dễ gây khó chịu), **sửa trực tiếp trên nền hợp đồng của họ** và đánh dấu thay đổi rõ ràng.

**Chiến thuật:**
- Dùng `[BỔ SUNG]` / `[SỬA]` trong ngoặc ở đầu câu để đối tác dễ nhận diện
- Dùng **màu xanh đậm** (RGB 0, 51, 153) cho phần bổ sung mới
- Giữ nguyên cấu trúc, số điều, số khoản của họ — chỉ thêm/điều chỉnh nội dung
- **Tone** phải tôn trọng đối tác (viện/trường): dùng "ghi nhận", "hỗ trợ", "phối hợp" thay vì "bắt buộc", "yêu cầu"
- **Cụ thể với partner nghiên cứu:**
  - "hai bên cùng cập nhật tiến độ" thay "Bên B báo cáo tiến độ"
  - "phối hợp theo dõi" thay "giám sát"
  - "cử người tham gia chứng kiến (nếu cần)" thay "quyền chứng kiến"
  - "mong muốn, hỗ trợ" thay "yêu cầu"
  - Thêm "trân trọng ghi nhận đóng góp chuyên môn" ở các điều khoản liên quan đến công bố/kết quả

```python
BLUE = RGBColor(0, 51, 153)
def multi(parts, ...):
    for t, b, c in parts:
        r = p.add_run(t)
        if c: r.font.color.rgb = c  # None = màu đen mặc định
# Dùng: multi([('nội dung cũ', False, None), ('nội dung mới (bổ sung)', False, BLUE)])
```

**Checklist khi nhận mẫu từ đối tác — tập trung vào ĐIỀU THIẾU:**
- Bên soạn thường "quên" điều khoản có lợi cho bên kia. Kiểm tra: sở hữu kết quả, cấm reverse engineering, bảo mật sau chấm dứt, quyền giám sát, thời gian cam kết, chế tài sai sót.
- Với đối tác viện/trường: giữ điều khoản bảo vệ bản quyền trí tuệ + cấm RE nhưng ghi thêm "trân trọng ghi nhận đóng góp chuyên môn của tập thể cán bộ khoa học Bên B" để tạo thiện chí.

### Dùng hợp đồng cũ làm mẫu cho scope mới (Template from Reference)

Khi user nói "tôi có hợp đồng cũ, hãy dùng nó làm mẫu soạn hợp đồng mới với scope hẹp hơn":

1. Đọc hợp đồng cũ, xác định cấu trúc (số điều, loại điều khoản)
2. **Tách scope**: lấy phần thử nghiệm in vitro từ hợp đồng in vitro+in vivo → bỏ phần in vivo
3. **Mở rộng nếu cần**: thêm sản phẩm mới vào scope (VD: thêm EZ80 nếu HĐ cũ chỉ có EZ67)
4. **Điều chỉnh giá**: tham khảo tỉ lệ (in vitro thường 15-25% giá combo in vitro+in vivo)
5. **Giữ nguyên** các điều khoản bảo vệ (SHTT, bảo mật, phạt, giám sát) từ hợp đồng cũ
6. **Không copy mù quáng** — mỗi scope có rủi ro riêng (in vitro: lo mẫu/lộ công thức; in vivo: lo tổn thất vật nuôi)

### Cân bằng chế tài với đối tác nghiên cứu (Research Partner Penalty Balance)

Khi đối tác là viện/trường/nhà khoa học (không phải doanh nghiệp thương mại):

- **Bảo mật**: dùng bồi thường thiệt hại thực tế (không phạt cố định) hoặc phạt rất nhẹ (50M). Lý do: viện/trường là cơ quan công lập, không có quỹ phạt lớn như doanh nghiệp.
- **Chậm tiến độ**: phạt 0,5%/ngày có trần 8% giá trị HĐ (thay vì phạt cố định lớn)
- **Bồi thường**: bồi thường thiệt hại thực tế là đủ — không cần phạt thêm nếu đã có thiện chí
- **Cấm cạnh tranh**: với đối tác không phải đại lý thương mại, điều khoản này có thể bỏ
- **Tone**: dùng "Bên B có trách nhiệm" thay "Bên B phải..."; thêm "trân trọng ghi nhận" ở các điều khoản ghi nhận đóng góp

### ⏳ Load skill `publish` trước khi publish
When publishing analysis/review online, **load the `publish` skill first** — nó upload markdown lên Gist (render native) hoặc HTML/Text lên KV → preview.thefirstonly.com. `publish` đã hợp nhất md-publish + content-publish + html-publishing thành 1 (skill `md-publish` cũ không còn tồn tại). Mặc định: markdown → Gist, HTML → KV. Chỉ dùng html-publishing khi cần custom CSS. Quên load skill → làm thừa công đoạn, output dễ lỗi render.

### ❌ Chung chung, không dẫn chiếu luật
Luật sư không viết "theo quy định pháp luật" — phải ghi rõ "theo khoản X Điều Y Luật Z 20XX".

⚠️ **Và phải lấy nguyên văn từ nguồn, không viết theo trí nhớ.** Bản đồ nguồn đã kiểm chứng (nguồn nào lấy được nguyên văn, nguồn nào chỉ để tra số hiệu, cách kiểm tra văn bản thay thế) + nguyên văn các điều khoản cụm chăn nuôi/thú y/TĂCN: [`references/vietnam-legal-source-access.md`](references/vietnam-legal-source-access.md).

⚠️ **Bẫy văn bản cũ:** nghị định xử phạt bị thay liên tục nhưng bản cũ vẫn nằm đầy trên mạng. Lĩnh vực chăn nuôi: **NĐ 211/2026/NĐ-CP** (hiệu lực 05/08/2026) đã thay **NĐ 14/2021/NĐ-CP**. Luật bị sửa bởi luật khác (VD Luật Thú y sửa bởi Luật 146/2025/QH15) → dùng **VBHN** thay vì luật gốc, kẻo dẫn điều khoản đã đổi.

### ❌ Bỏ qua thẩm quyền giải quyết tranh chấp
Luôn kiểm tra: nếu bên mua ở HN, bên bán ở An Giang, mà hợp đồng không chọn Tòa án HN → bên mua phải đi An Giang kiện. **Cực kỳ bất lợi.**

### ❌ Chỉ nhìn góc độ luật, bỏ qua chuyên môn
Hợp đồng mua bán than bùn: phải hiểu về độ ẩm, chất khô, công thức quy đổi mới phát hiện được công thức bù ẩm sai. Nếu chỉ biết luật không → không thấy rủi ro.

### ❌ Không kiểm tra điều kiện áp dụng của chế tài
Ví dụ: "trả lại cọc gấp đôi nếu bên bán vi phạm" nhưng kèm điều kiện "làm mục đích giao kết không đạt được" — tiêu chuẩn mơ hồ, khó chứng minh. Phải sửa thành điều kiện cụ thể.

### ❌ Bỏ qua chi phí phát sinh khi xử lý vi phạm
Quyền từ chối nhận hàng nhưng không nói ai chịu phí lưu kho, vận chuyển ngược → bên mua có thể bị đẩy chi phí.

### ❌ Điều khoản thanh toán không thực tế
"Thanh toán trong vòng 02 ngày sau nghiệm thu" là không khả thi với doanh nghiệp (quy trình trình ký, duyệt chi, chuyển khoản). Luôn đề xuất 10-15 ngày làm việc.

### ❌ Phạt hủy Hợp đồng 30% (quá trần 8%)
Nhiều hợp đồng mua bán soạn sẵn ghi phạt hủy HĐ 30%. Khoản này vượt trần 8% theo Luật Thương mại 2005 Điều 301 và có thể bị Tòa tuyên vô hiệu. Sửa về 8%. Phân biệt: bên bán hủy → hoàn tiền + phạt 8%; bên mua hủy → mất cọc (đối trừ).

### ❌ Bảo hành bị vô hiệu hóa vô điều kiện khi chậm thanh toán
"Bên A không chịu trách nhiệm bảo hành khi công nợ quá hạn" — cần thêm ngoại lệ: trừ trường hợp chậm thanh toán do lỗi Bên A (chậm xuất hóa đơn, sai thông tin, chậm thông báo giao hàng).

### ❌ Chỉ phạt một phía
Hợp đồng chỉ phạt chậm thanh toán (Bên B) mà không phạt chậm giao hàng (Bên A) là bất cân xứng. Phải bổ sung phạt đối xứng.

### ❌ Dùng "chiết khấu" thay vì "tài trợ" trong hợp đồng thử nghiệm
"Chiết khấu 50%" mang tính thương mại thuần túy. "Tài trợ 50%" thể hiện thiện chí hợp tác, hỗ trợ đối tác — phù hợp với hợp đồng thử nghiệm hơn.

### ❌ Chỉ dẫn chiếu 1 bằng sáng chế khi có thể dẫn cả 2
Nếu sản phẩm liên quan đến nhiều bằng sáng chế, dẫn chiếu đầy đủ để tăng vị thế KHCN và tạo niềm tin cho đối tác.

### ❌ Bỏ qua rủi ro thanh toán 100% trước giao hàng (HĐ Phân phối)
Trong hợp đồng phân phối, "thanh toán 100% trước khi giao hàng" là điều khoản nguy hiểm nhất cho NPP — họ mất toàn bộ tiền nếu NCC không giao hàng hoặc giao hàng lỗi. Không bao giờ để điều khoản này tồn tại. Phương án thay thế: cọc 30-50% + 50-70% sau giao hàng & kiểm tra (10-15 ngày).

### ❌ Chấp nhận thời gian khiếu nại bất hợp lý (HĐ Phân phối)
Thời gian khiếu nại dưới 24h (VD: "3 giờ kể từ thời điểm nhận hàng") là không khả thi với hàng hóa cần kiểm tra chi tiết. Yêu cầu: khiếu nại cảm quan (số lượng/hư hỏng ngoại quan) trong 24h + khiếu nại chất lượng trong 07 ngày làm việc (phù hợp Điều 44 Luật Thương mại 2005).

### ❌ Độc quyền phân phối dễ bị tước bỏ
Nếu hợp đồng cho phép NCC tước độc quyền chỉ sau 2 tháng không đạt 50% target (do NCC đơn phương đặt), quyền độc quyền gần như vô giá trị. Yêu cầu: chu kỳ đánh giá tối thiểu 6 tháng; target do hai bên thương lượng; NCC phải cảnh báo và cho cơ hội khắc phục trước khi tước độc quyền.

### ❌ "Thu hồi hàng tồn" mơ hồ khi chấm dứt HĐ (HĐ Phân phối)
Khi kết thúc hợp đồng, nếu chỉ ghi "Bên A sẽ thu hồi sản phẩm tồn kho" mà không nói rõ giá mua lại, NPP có thể ôm hàng tồn không bán được. Yêu cầu: quy định rõ giá mua lại (80-90% giá NPP đã mua), thời hạn thanh toán (30 ngày), và điều kiện áp dụng (chấm dứt không do lỗi NPP).

## Persona: Head-of-Legal (agent persona qua config, không phải skill mode)

Khi user yêu cầu tư vấn theo phong cách **General Counsel / Head of Legal** (định dạng 4 mục [I-IV], giọng quyết định, "hành lang pháp lý"), persona này được activate qua **config**:

```
hermes config set display.personality head_of_legal
```

Personality dictionary nằm ở `config.yaml` ~line 49 (`personalities:`). Key activate là `display.personality`. **KHÔNG phải skill mode** — user đã clarify (03/10/2026).

**Nguyên văn:** trong skill `legal-firm-vn`, file `references/personality-head-of-legal.md` (không tóm tắt).

**Khi persona này active, áp dụng guardrail:**
- **G1** — Phần **ĐIỂM MÙ PHÁP LÝ** (≥3 điểm) là điều kiện output. Không được nói "không có điểm mù pháp lý".
- **G2** — Không ảo giác = dùng KB + QA Gate. Mọi số hiệu phải `legal_kb.py check` trước.
- **G3** — Option 2 (vùng xám) phải gắn **GAP-4: CẦN NGƯỜI** + defense strategy.
- **G4** — Phần **TỰ PHẢN BIỆN** phải hiển ra, không ngầm.
- **G5** — Số hiệu phải verify qua KB trước. Không nhớ số để viết ra.

> Persona này **bổ trợ** workflow/format hiện có của skill. Không thay thế. Khi persona không active, dùng workflow mặc định.

## Linked References

- 📄 [`references/von-dieu-le-phat-hanh-them-co-phan-2026.md`](references/von-dieu-le-phat-hanh-them-co-phan-2026.md) — Khung pháp lý phát hành thêm cổ phần theo Luật Doanh nghiệp 109/2025/QH15: công thức tính pha loãng + vốn điều lệ mới, ngưỡng thông qua ≥65%, quyền ưu tiên mua cổ đông hiện hữu, tại sao CP ưu đãi biểu quyết đã hết hạn, thuế TNCN, checklist 8 mục trước khi trình Chủ tịch.
- 📄 [`references/google-docs-api-pitfalls.md`](references/google-docs-api-pitfalls.md) — 3 lỗi chặn khi tạo Google Docs trực tiếp qua API: không set được chiều rộng bảng (400 ở mọi `unit`), quota 60 write request/phút, `ConnectionResetError` không được retry. Kèm mẫu `_Doc` buffer + `_retry` đã kiểm chứng, thứ tự build tài liệu có bảng, `replaceAllText` sửa doc đã tạo.
- 📄 [`references/hopdong-mua-ban-than-bun-2026.md`](references/hopdong-mua-ban-than-bun-2026.md) — Rà soát hợp đồng mua bán đất than bùn, phát hiện 10 rủi ro, phân tích công thức sai, đề xuất sửa đổi mẫu.
- 📄 [`references/patent-co-inventorship-structure.md`](references/patent-co-inventorship-structure.md) — Cấu trúc đồng tác giả sáng chế (GS viện công lập), cam kết bảo đảm, chia sẻ lợi ích, điều khoản mẫu.
- 📄 [`references/research-collab-saphia-cuong-2026.md`](references/research-collab-saphia-cuong-2026.md) — Hợp đồng hợp tác NCKH Saphia × GS Cường: cấu trúc 2 công ty IP+Thương mại, thưởng có trần 5 tỷ, đồng tác giả không đồng sở hữu, phạt 500tr, cross-reference renumbering.
- 📄 [`references/trial-contract-livestock.md`](references/trial-contract-livestock.md) — Cấu trúc hợp đồng thử nghiệm sản phẩm chăn nuôi: 13-điều skeleton, ASFV clause mẫu, Disclaimer chuẩn, cấu trúc Phụ lục A, lưu ý luật chăn nuôi.
- 📄 [`references/hopdong-mua-ban-doc-quyen-nguyen-drink-kiem-saphia-2026.md`](references/hopdong-mua-ban-doc-quyen-nguyen-drink-kiem-saphia-2026.md) — Phân tích HĐ mua bán độc quyền Nguyễn's Drink × Kiềm Saphia: mixed contract (mua bán + SHTT + độc quyền + hình ảnh), tự phản biện, ma trận rủi ro.
- 📄 [`references/hopdong-phan-phoi-ghe-an-toan-tre-em-sapbebe-2026.md`](references/hopdong-phan-phoi-ghe-an-toan-tre-em-sapbebe-2026.md) — Rà soát HĐ phân phối ghế an toàn trẻ em (SAP BEBE × NPP): 10 rủi ro cho NPP, 8 đề xuất sửa đổi, ma trận bất cân xứng, tự phản biện + dung hòa.
- [`references/commercial-agency-commission-hoa-hong.md`](references/commercial-agency-commission-hoa-hong.md) — Hợp đồng hợp tác thương mại (đại lý hoa hồng): Manna Đất Vàng × Ông C (cá nhân), cấu trúc hoa hồng 12%/10%, bảo mật tinh gọn, không nhắc chức danh đối tác, xác nhận khách hàng bằng email.
- 📄 [`references/invitro-asfv-amendment-academic-tone.md`](references/invitro-asfv-amendment-academic-tone.md) — Bổ sung hợp đồng In vitro ASFV trên nền mẫu Học viện: chiến thuật amendment-on-template, tone hợp tác học thuật, ngôn ngữ thay thế, kỹ thuật tô màu xanh, xử lý lỗi soạn thảo.
- 📄 [`references/hopdong-mua-ban-thiet-bi-manna-yktech-2026.md`](references/hopdong-mua-ban-thiet-bi-manna-yktech-2026.md) — Rà soát HĐ mua bán thiết bị (Máy đo KLN): phạt hủy 30% vượt trần, tham chiếu sai, thiếu chế tài chậm giao, bảo hành thiếu ngoại lệ, 50-30-20.
- 📄 [`references/nda-civil-servant-benb.md`](references/nda-civil-servant-benb.md) — NDA với Bên B là cán bộ cơ quan QLNN: rủi ro PCTN+CBCC, checklist điều chỉnh mục đích (viết chung chung, bỏ kết nối), kỹ thuật DOCX editing fallback (zipfile+ET), case thực tế 09/2026.
- 📄 [`references/hopdong-giai-cuu-dan-lon-asf-2026.md`](references/hopdong-giai-cuu-dan-lon-asf-2026.md) — 🔴 **HĐ "giải cứu" đàn lợn mắc ASF (Manna × Farm Minh Hà):** ranh đỏ Đ13.17 Luật Thú y + danh mục 1.9 → HĐ vô hiệu + rủi ro Đ241 BLHS; cách tính đủ số lượng TĂCN theo FCR/nước uống; 7 mâu thuẫn nội tại; bồi thường không trần; **checklist 17 mục cho HĐ chăn nuôi/TĂCN dùng lại được**.
- 📄 [`references/vietnam-legal-source-access.md`](references/vietnam-legal-source-access.md) — Bản đồ truy cập nguồn văn bản pháp luật VN: nguồn nào lấy được nguyên văn (`hethongphapluat.com/<slug>/dieu-N`, VBHN PDF trên datafiles.chinhphu.vn), nguồn nào chỉ để tra số hiệu, cách kiểm tra văn bản thay thế, cảnh báo prompt injection trong trang nguồn luật, và **nguyên văn đã verify** của Đ13 Luật Thú y, Đ12/34/37/47/50 Luật Chăn nuôi, Đ301 LTM, Đ117/123/131/351 BLDS, Đ241 BLHS.
- 🔧 [`scripts/extract_docx_text.py`](scripts/extract_docx_text.py) — Trích xuất text .docx an toàn với ObservationPack (`--marks` quét cả `w:highlight` và `w:color` — "bôi xanh" trong Word thường là màu chữ `0000FF`, không phải highlight).

## Tham khảo

- [Bộ luật Dân sự 2015 (số 91/2015/QH13)](https://vbpl.vn/bo-tu-phap/Pages/vbpq-toanvan.aspx?ItemID=110040)
- [Luật Thương mại 2005 (số 36/2005/QH11)](https://vbpl.vn/bo-cong-thuong/Pages/vbpq-toanvan.aspx?ItemID=11058)
- [Bộ luật Tố tụng Dân sự 2015](https://vbpl.vn/bo-tu-phap/Pages/vbpq-toanvan.aspx?ItemID=110478)
