# gdoclib — dựng Google Docs pháp lý (hợp đồng, phụ lục, báo cáo)

Thư viện: `~/AppData/Local/hermes/build/gdoclib.py` (Windows). Dùng lại cho mọi văn bản
pháp lý dài. Đã kiểm chứng với hợp đồng 274 đoạn + 7 bảng, và báo cáo 45 đoạn + 6 bảng.

## Chữ ký hàm THẬT (đọc kỹ, đây là chỗ mất thời gian nhất)

```python
from gdoclib import Doc, new_doc, svc

did = new_doc("Tên tài liệu")      # CHỈ trả doc_id (str), KHÔNG trả (doc, url)
doc = Doc(did)
url = f"https://docs.google.com/document/d/{did}/edit"

doc.margins(top=42, bottom=42, left=48, right=48)      # PT
doc.base(family="Times New Roman", size=11, justify=True, spacing=118)  # 1 lượt, toàn văn
doc.end()                                              # -> index để chèn
doc.text_block(items, at=None)                         # items=[(text, kind)]; trả (marks, cur)
doc.add_table(rows, at=None)                           # trả (startIndex, endIndex, rows) — 3 giá trị
doc.style(s, e, bold=None, size=None, italic=None,
          align=None, space_before=None, keep_next=None)   # TỰ GỌI batch, trả None
doc.style_table(start, size=9, header_bold=True)
doc.share(role="writer")                               # trả URL
```

Tham số SAI sẽ TypeError: không có `spacing`, `sb`, `sa`, `keep` trong `style()`.
`align` chỉ nhận `"START" | "CENTER" | "END" | "JUSTIFIED"` (KHÔNG dùng `"JUSTIFY"` → 400).

## Mẫu render đúng

```python
marks, tbls = [], []
buf, cur = [], None

def flush(idx):
    if not buf:
        return idx
    if idx is None:
        idx = doc.end()          # tài liệu mới: end() == 1
    items = list(buf)
    doc.text_block(items, at=idx)
    c = idx
    for t, k in items:
        marks.append((c, c + len(t), k))
        c += len(t) + 1
    buf.clear()
    return c

for blk in BLOCKS:               # ("p"|"h1"|"h2"|"b"|"italic"|"center"|"title"|"gap", text) | ("table", rows)
    if blk[0] == "table":
        cur = flush(cur)
        s, e, _ = doc.add_table(blk[1], at=cur)
        tbls.append(s)
        cur = doc.end()
    elif blk[0] == "gap":
        buf.append(("", "gap"))
    else:
        buf.append((blk[1], blk[0]))
flush(cur if cur is not None else doc.end())

doc.base(size=10, justify=True, spacing=115)
for s, e, kind in marks:
    if kind == "h1":
        doc.style(s, e, bold=True, size=12.5, align="START", space_before=14, keep_next=True)
    # ... KHÔNG cộng dồn reqs — style() tự batch
```

## Pitfalls

1. **`new_doc` chỉ trả id.** Viết `doc, url = new_doc(...)` → `ValueError: too many values to unpack`.
2. **`add_table` trả 3 giá trị.** `s, e = doc.add_table(...)` → ValueError. Dùng `s, e, _ =`.
3. **`style()` tự batch và trả `None`.** `reqs += doc.style(...)` → `TypeError: unsupported operand`. Gọi trực tiếp.
4. **Chèn gộp để né trần 60 write request/phút.** `text_block` gộp cả lô đoạn thành 1 `insertText`. Tuyệt đối không lặp `insertText` từng đoạn.
5. **Bảng: chèn text ô theo index GIẢM DẦN** (`sorted(cells, key=lambda x: -x[0])`), nếu không text dồn hết vào ô đầu.
6. **`updateTableColumnProperties` bị 400** → để width mặc định.
7. **Chỉ số paragraph style phải phủ newline**: range `s..e+1`. `gdoclib.style` đã xử lý.
8. **Kiểm chứng sau khi dựng**: đếm paragraph/table và soi ô nào >400 ký tự (nghi dồn text). Xem script kiểm tra trong phần Verification.

## Verification

```python
d = Doc(did).get()
ntab = sum(1 for el in d["body"]["content"] if "table" in el)
npar = sum(1 for el in d["body"]["content"] if "paragraph" in el)
# ô dài bất thường = dấu hiệu text dồn vào một ô
```

**Pitfall đã sập một lần:** script kiểm tra chỉ gom dòng TIÊU ĐỀ của bảng
(`rows[0]`) thì mọi mỏ neo nằm trong ô thân bảng đều báo `THIẾU` sai — bảng biểu
thuế, bảng văn bản dẫn chiếu, bảng đối chiếu 30 điểm. Phải duyệt **toàn bộ ô của
mọi dòng** rồi mới ghép chuỗi để tra mỏ neo:

```python
parts = []
for el in d["body"]["content"]:
    if "paragraph" in el:
        parts.append("".join(r["textRun"]["content"]
                             for r in el["paragraph"].get("elements", [])
                             if "textRun" in r))
    elif "table" in el:
        for row in el["table"]["tableRows"]:
            for cell in row["tableCells"]:
                parts.append(" ".join(
                    "".join(r["textRun"]["content"]
                            for r in cc["paragraph"].get("elements", [])
                            if "textRun" in r)
                    for cc in cell["content"] if "paragraph" in cc))
body = "\n".join(parts)
```

Kiểm mỏ neo theo từng cặp `(số hiệu văn bản, tên văn bản)` VÀ theo số mục cuối
cùng của từng danh mục dài (ví dụ `mục 70`, `mục 100`). Cách này bắt được cả lỗi
mất đuôi khi chèn danh mục vài trăm dòng.

Rồi in tuần tự nhãn đoạn + tiêu đề bảng để xác nhận ĐÚNG THỨ TỰ. Không tin kết quả
`exit 0` — phải đọc lại nội dung trên Docs.

## Nội dung pháp lý — quy ước

- Ô cần anh chốt số liệu: ghi `..............` tại chỗ, KHÔNG tự bịa số.
- Mọi số tiền phải có phần bằng chữ.
- Bảng phải là `<table>` thật, không dùng dấu `|`.
- Không đưa nội dung khoa học/kỹ thuật vào văn bản pháp lý.
