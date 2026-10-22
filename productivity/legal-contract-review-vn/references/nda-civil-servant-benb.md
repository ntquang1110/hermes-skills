# NDA với Bên B là cán bộ cơ quan quản lý nhà nước

## Bối cảnh

Bên A (doanh nghiệp KH&CN) ký NDA với Bên B — cá nhân tư vấn độc lập, nhưng thực tế Bên B **đang làm việc tại cơ quan quản lý nhà nước** trong lĩnh vực liên quan (KH&CN, doanh nghiệp KH&CN, đề tài/dự án cấp Bộ, cấp NN).

Đây là tình huống nhạy cảm vì NDA ghi nhận Bên B sẽ "kết nối, giới thiệu đầu mối cơ quan quản lý" — nếu văn bản lộ ra, cả hai bên đều gặp rủi ro về Luật Phòng chống tham nhũng 2018 (Điều 30) và Luật Cán bộ công chức 2008 (Điều 19).

## Nguyên tắc cốt lõi

NDA chỉ cần xác định phạm vi được phép sử dụng thông tin. Không nên ghi cụ thể công việc nhạy cảm. **Mục đích càng chung chung, rủi ro càng thấp.**

## Checklist điều chỉnh

### 1. Tiêu đề văn bản — bỏ mô tả chi tiết

Dòng mô tả dưới tiêu đề như:
```
(Dùng cho cá nhân tư vấn độc lập về đăng ký doanh nghiệp khoa học
và kết nối / xây dựng đề tài, dự án khoa học công nghệ cấp Bộ, cấp Nhà nước)
```

→ **Bỏ hẳn.** Hoặc thay bằng: `(Dùng cho cá nhân tư vấn độc lập)` — không gắn với lĩnh vực cụ thể.

### 2. XÉT RẰNG — bỏ từ "kết nối"

Đoạn mô tả Bên B như:
```
Bên B là cá nhân có năng lực tư vấn, hỗ trợ thủ tục hoặc kết nối
```

→ Sửa thành:
```
Bên B là cá nhân có năng lực, kiến thức chuyên môn trong lĩnh vực tư vấn thủ tục
```

Cũng bỏ "kết nối" khỏi phần liệt kê công việc:
```
(ii) xây dựng, kết nối, hoàn thiện hồ sơ đề tài
```
→
```
(ii) xây dựng, hoàn thiện hồ sơ đề tài
```

### 3. Điều 1.1 (Mục đích) — viết chung chung

Thay toàn bộ các khoản (a)-(e) chi tiết bằng một câu duy nhất:

> 1.1. Mục đích. Bên A tiết lộ Thông tin mật cho Bên B chỉ để Bên B thực hiện việc tư vấn, hỗ trợ các thủ tục pháp lý, hành chính và chuyên môn liên quan đến hoạt động đăng ký, quản lý, khai thác tài sản trí tuệ, doanh nghiệp khoa học và công nghệ, và các chương trình, đề tài, dự án khoa học công nghệ theo yêu cầu của Bên A (gọi chung là Mục đích).

**Không ghi:**
- "cấp Bộ, cấp Nhà nước" — gắn Bên B với quyền lực nhà nước
- "kết nối, giới thiệu đầu mối cơ quan quản lý" — chứng cứ Bên B dùng quan hệ công tác
- "chuyên gia phản biện, đơn vị phối hợp" — quá chi tiết

### 4. Điều 3(f) — cơ chế chia sẻ với bên thứ ba

Nếu giữ điều khoản cho phép Bên B chia sẻ thông tin để "kết nối, giới thiệu đầu mối", cần thêm:

> Bên B không sử dụng chức vụ, quan hệ công tác tại cơ quan quản lý nhà nước để thực hiện việc kết nối nêu trên.

## Lưu ý đặc thù

- **User có thể từ chối thêm compliance clause** (cam kết tuân thủ Luật PCTN, CBCC). Lý do: sợ làm to chuyện, sợ Bên B giật mình. Tôn trọng quyết định nhưng cần cảnh báo rủi ro.
- **Phạt 5 tỷ với cán bộ NN là vô dụng** — họ không có tài sản đó. Nhưng nếu user muốn giữ làm công cụ tâm lý, ok.
- **Điều 9.6** (bẫy "và Bên A chấp nhận") thường không được sửa vì user không muốn đàm phán thêm — ghi nhận rủi ro.
- **Ký danh nghĩa "Viện/Center..."** cần kiểm tra pháp nhân — nếu không có con dấu, người ký chịu trách nhiệm cá nhân.

## DOCX Editing — kỹ thuật

Khi python-docx không có sẵn (thiếu lxml/typing_extensions), dùng zipfile + xml.etree.ElementTree (stdlib):

```python
import zipfile, xml.etree.ElementTree as ET

W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'

with zipfile.ZipFile('input.docx') as zin:
    doc_xml = zin.read('word/document.xml')
    all_files = {n: zin.read(n) for n in zin.namelist()}

tree = ET.fromstring(doc_xml)
body = tree.find(W+'body')

def get_para_text(p):
    return ''.join(t.text or '' for t in p.iter(W+'t'))

def make_colored_run(text, color='003399'):
    r = ET.Element(W+'r')
    rPr = ET.SubElement(r, W+'rPr')
    sz = ET.SubElement(rPr, W+'sz'); sz.set(W+'val', '24')
    szCs = ET.SubElement(rPr, W+'szCs'); szCs.set(W+'val', '24')
    col = ET.SubElement(rPr, W+'color'); col.set(W+'val', color)
    t = ET.SubElement(r, W+'t')
    t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
    t.text = text
    return r

def set_para_colored(p, text, color='003399'):
    for r in list(p.findall(W+'r')): p.remove(r)
    p.append(make_colored_run(text, color))

# Tìm và thay thế text trong run (xử lý run splitting)
for p in body.iter(W+'p'):
    full = get_para_text(p)
    if 'cụm từ cần tìm' in full:
        for r in p.findall(W+'r'):
            for t in r.findall(W+'t'):
                if t.text and 'cụm từ cần tìm' in t.text:
                    t.text = t.text.replace('cũ', 'mới')
                    # Tô màu xanh
                    rPr = r.find(W+'rPr')
                    if rPr is None:
                        rPr = ET.Element(W+'rPr')
                        r.insert(0, rPr)
                    for c in rPr.findall(W+'color'): rPr.remove(c)
                    col = ET.SubElement(rPr, W+'color'); col.set(W+'val', '003399')

# Lưu
doc_xml_new = ET.tostring(tree, xml_declaration=True, encoding='UTF-8')
with zipfile.ZipFile('output.docx', 'w', zipfile.ZIP_DEFLATED) as zout:
    for name in all_files:
        zout.writestr(name, doc_xml_new if name == 'word/document.xml' else all_files[name])
```

**Xử lý run splitting (quan trọng):** Word có thể tách "kết nối, " thành một run riêng. Dùng `get_para_text()` để tìm paragraph, rồi dùng vòng lặp `for r in p.findall(W+'r')` + `for t in r.findall(W+'t')` để tìm run chứa từ cần sửa — không dùng `p.text` (chỉ trả về run đầu tiên).

## Tham khảo

- Luật Phòng, chống tham nhũng 2018, Điều 30
- Luật Cán bộ, công chức 2008 (sửa đổi 2019), Điều 19
- Case thực tế 09/2026: NDA Nguyễn Thị Chung × cán bộ cơ quan QLNN — file `17.09.26-THOA THUAN BAO MAT-MRN.MST_SELECTED.docx`
