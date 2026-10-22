---
name: html-catalogue-builder
description: "Build trang HTML lọc/tìm kiếm rồi publish preview."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [html, catalogue, dashboard, search, filter, preview, publish, vietnamese]
    related_skills: [publish, html-unslop, design-template-selector, legal-skill-porting]
---

# Dựng trang HTML danh mục rồi publish

Dùng khi kết quả một việc là **một danh sách dài** cần anh chọn/tra cứu:
skill pack vừa audit, danh sách model provider, menu tra cứu, kho tài liệu.
Không dùng cho báo cáo một trang hay dashboard số liệu thời gian.

Kết quả: một URL, mở trên điện thoại là xong.

## Quy tắc số 1: KHÔNG dựng HTML bằng f-string

Template có CSS và JavaScript. Mọi `{` trong đó phải nhân đôi, và sót một cái
là chết ngay. Lần này file 25 KB chết với:

```
SyntaxError: f-string: expecting '}' (line 516, column 11)
```

Dòng 516 là JavaScript, không phải Python — nhìn vào hoang đường.

Cách đúng: giữ template riêng dạng `.html` với token, generator Python thay thế.

```
templates/catalogue.html      ← CSS + JS + __TOKEN__
scripts/build_catalogue.py    ← .replace('__TOKEN__', ...)
```

Token phải đủ hiếm để không đụng nhầm: `__DATA_READY__`, `__N_TOTAL__`,
`__GCOLOR__`.

## Quy tắc số 2: nhúng JSON, vẽ bằng JS

Đừng dựng HTML thật ở Python. Nhúng `json.dumps(records, ensure_ascii=False)` vào
một hằng JS, để JS render. HTML nhỏ, tìm kiếm lọc chạy client-side, không cần
backend, không cần reload.

**Chốt số học trước khi ghi file** — lỗi này lộ ra muộn và khó truy:

```python
assert len(want) + len(skip) == len(denied), "partition does not add up"
```

Trang lần này: 126 + 18 + 45 = 189. Sai một cái là báo cáo bịa số liệu.

## Quy tắc số 3: tìm kiếm tiếng Việt trên nội dung tiếng Anh

Nội dung gốc (skill description, model list) viết tiếng Anh. Người dùng gõ
tiếng Việt. Trang không tìm được gì.

Thêm lớp từ khoá trong generator, không sửa nội dung gốc:

```python
VN_KEYWORDS = {
    "hợp đồng": "contract clause agreement redline term deal",
    "lao động": "employment labour workplace handbook disciplinary",
    "bảo vệ dữ liệu": "privacy data protection breach dpa gdpr",
    # ...
}

def vn_tags(name, desc):
    blob = (name + " " + desc).lower()
    hits = []
    for vi, en in VN_KEYWORDS.items():
        if vi in blob:
            hits.append(vi); continue
        for tok in en.split():
            if len(tok) < 4:
                continue
            if re.search(r"\b" + re.escape(tok) + r"\b", blob):
                hits.append(vi); break
    return hits
```

Rồi đưa `r.vi` vào chuỗi lọc của JS:

```js
.filter(r => !q || (r.name + ' ' + r.desc + ' ' + (r.vi||[]).join(' ') + ' ' + r.group)
         .toLowerCase().includes(q));
```

Và hiện 4 tag đầu lên card để anh thấy skill đó liên quan tới mấy chủ đề.

### Bẫy khớp chuỗi con

Bản đầu dùng `any(t in blob for t in en.split())`. Kết quả tìm "thuế" ra 41
thẻ, trong đó có `dpia-documenter` và `cap-table-analyst` — vì token `tax` khớp
bên trong từ khác, và token `ip` khớp gần như mọi từ chứa `ip`.

Sửa: **word-boundary `\b` + token dài tối thiểu 4 ký tự.** Xuống còn 38, sạch.

Luôn kiểm độ nhạy trước khi publish:

```js
['hợp đồng','lao động','thuế','bảo vệ dữ liệu','nhãn hiệu'].map(t => [t, test(t).length])
```

Số phải nhỏ vừa (vài chục trên 126 bản ghi), không phải 60% tập dữ liệu.

## Quy tắc số 4: QA bằng console, không cần mắt

Có lúc công cụ chụp ảnh trang không chạy. Đừng dừng lại — kiểm tra bố cục bằng
JavaScript trả về JSON. Xem `references/browser-qa-without-vision.md`.

Tối thiểu phải trả lời được: có tràn ngang không, mọi tab click được, mọi ô tìm
kiếm trả kết quả, trạng thái rỗng có hiện, dấu tiếng Việt không bị mất.

## Ngôn ngữ thị giác: Duolingo

Anh hay yêu cầu "dạng Duolingo" cho trang danh mục. Đặc trưng:

| Yếu tố | Cách làm |
|---------|----------|
| Thẻ | nền trắng, viền 2px `#e5e5e5`, viền dưới 4px, bo góc 12–16px |
| Nhấn | hover nhấc lên 1px, không đổi màu |
| Màu nhóm | 1 màu riêng mỗi nhóm, dùng cho chấm + badge nhạt |
| Số liệu | 4 thẻ to trên đầu, số 29px đậm, nhãn 11.5px xám |
| Tab | chữ 14.5px đậm, viền dưới 4px, đổi màu khi active, pill đếm số |
| Trạng thái | xanh lá = dùng được, vàng = viết tiếp, đỏ = bỏ |
| Nền | trắng, không gradient rốt ruột, chỉ header có gradient xanh→cyan |

Bảng dữ liệu dài thì gói trong `<details>` thay vì đổ dồ ra trang.

## Mobile

Trang này đọc trên điện thoại là tiêu chuẩn, không phải phụ:

```css
@media(max-width:640px){
  .stats{grid-template-columns:repeat(2,1fr)}
  header .wrap{flex-direction:column;text-align:center}
  h1{font-size:20px}
  .grid{grid-template-columns:1fr}
  .tab{padding:9px 10px;font-size:13.5px}
}
```

Kiểm tra: `document.documentElement.scrollWidth <= window.innerWidth + 2`.

## Publish rồi verify lại trên live

```bash
python skills/productivity/publish/scripts/content-upload.py \
  --file out.html --title "Tiêu đề"
```

Bước upload chạy `html-unslop` và **viết lại HTML**. Kiểm tra bản local không
đủ. Mở URL preview, chạy lại đúng probe console đó, xác nhận số card, số chip,
số dòng bảng, kết quả tìm kiếm.

## Chữ tiếng Việt trên web

Chữ tiếng Việt cần font có subset `vietnamese`. Mặc định hệ thông
(`-apple-system`, `Segoe UI`, `Roboto`, `Arial`) đều có nên an toàn. Nếu chọn
font trải nghiệm thì kiểm tra subset trước — Playfair Display, Lora, Inter,
Roboto Mono có; Antonio và JetBrains Mono không có, dùng là vỡ hết dấu.

## Liên quan

- `publish` — upload KV/Gist, xử lý lỗi preview domain
- `html-unslop` — dọn AI-ism, publish tự gọi
- `design-template-selector` — chọn nền tảng thị giác trước khi code
- `legal-skill-porting` — trường hợp dùng mẫu: audit rồi dựng catalogue chọn skill
