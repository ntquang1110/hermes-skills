# Dịch bài báo open-access sang tiếng Việt

Dùng khi user muốn "bản dịch toàn văn" một bài báo. Đây là workflow đã chạy thành công 12/10/2026, publish được 2 link.

## 1. Quyết định được phép dịch hay không

**Bản dịch là tác phẩm phái sinh.** Chỉ dịch và đăng lại bài **CC BY** (hoặc Public Domain / CC0). Không dịch bài paywalled, author-manuscript, hay "text mining / fair use" rồi publish link công khai — đó là tái bản có bản quyền.

Cách đọc license nhanh nhất là **esummary**, không cần fetch全文:

```python
S.get(BASE+"esummary.fcgi", params={"db":"pubmed","id":"8801435","retmode":"json"})
# -> it["articleids"] chứa doi; license không nằm đây
```

License nằm trong **BioC XML của PMC**: `<infon key="license">CC BY</infon>`. Nó xuất hiện ở ngay đầu response, nên fetch thử 1 cái rồi dừng là đủ để quyết định.

Nếu bài user muốn KHÔNG phải CC BY: **đừng dịch và publish.** Thay vào đó nói thẳng "bài này có bản quyền, mình tổng hợp nội dung thay vì dịch", rồi chọn bài CC BY gần nhất cùng chủ đề để dịch.

## 2. Lấy toàn văn

```
https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pmcoa.cgi/BioC_xml/<PMCID>/unicode
```

- **Không dùng PMC website HTML**: `pmc.ncbi.nlm.nih.gov` trả reCAPTCHA ~20KB rỗng.
- **Không dùng EuropePMC fullTextXML** cho bài ngoài OA subset: HTTP 500.
- Nếu `pmcoa.cgi` trả `"No result can be found"` → bài KHÔNG nằm trong OA subset, dù vẫn mở đọc được trên PMC. Chuyển bài khác.

## 3. Đọc cấu trúc XML

BioC XML là **mảng phẳng các `<passage>`**, KHÔNG có thẻ `<section>` lồng nhau (regex `'<section\b...` trả 0 kết quả, đừng mất thời gian). Mỗi passage có:

```xml
<passage>
  <infon key="section_type">INTRO</infon>   <!-- TITLE/ABSTRACT/INTRO/CONCL/REF/FIG -->
  <infon key="type">paragraph</infon>       <!-- paragraph/title_1/title_2/ref/abstract/fig_caption -->
  <infon key="license">CC BY</infon>
  <text>...</text>
</passage>
```

Parse: regex `<passage>(.*?)</passage>` + regex `<infon key="([^"]*)">(.*?)</infon>` + `<text>(.*?)</text>`, strip tag, `html.unescape`.

**Lọc `section_type != "REF"`** để lấy thân bài. Với bài Molecules 2010 artemisinin: 166 passage, trong đó 115 là reference, còn lại 51 passage / 37.192 ký tự thân bài. Đó là thứ phải dịch.

## 4. Chiến lược viết bản dịch

- **Chia thành 3 file con** (`-part1.md`, `-part2.md`, `-part3.md`) rồi gộp. Lý do là tool-call token cap (~8K) sẽ cắt một write_file khổng lồ.
- **Sau mỗi part, chạy kiểm tra rò rỉ ngôn ngữ**: quét token Anh còn sót (`further`, `strongly`, `however`, `rearrangement`, `potency`) và ký tự Trung (`[\u4e00-\u9fff]`). Lỗi này xảy ra thật trong session: "further được làm sáng tỏ", "kị nước亲 nước", "several sách". Sửa ngay part đó trước khi viết part sau, không dồn cuối.
- **Giữ nguyên thuật ngữ gốc** khi dịch ngược sẽ sai nghĩa: `in vitro`, `in vivo`, `IC50`, `Ki`, `MIC`, `PMID`. Chỉ dịch khi có tương đương chuẩn (hằng số ức chế, nồng độ ức chế tối thiểu).
- **Tiêu đề mục số theo bản gốc** (1. Giới thiệu, 6.1. ...) để user đối chiếu được với bản Anh.

## 5. Convert markdown → HTML

Không cần thư viện ngoài. Parser ~40 dòng xử lý: `##`/`###` → h2/h3, `> ` → `<div class="note">`, `- `/`* ` → ul, `1. ` → ol, còn lại gộp thành p.

**Bẫy Python 3.11:** f-string không được chứa backslash trong biểu thức. Lỗi thật:
```python
out.append(f'<li>{inline(re.sub(r"^\d+\.\s+","", s))}</li>')   # SyntaxError
```
Sửa: tính `item = inline(pat.sub('', s))` trước, rồi `f'<li>{item}</li>'`.

**Validate tag balance** bằng regex đếm open/close cho p, h2, h3, ul, li, section, table. Trường hợp `<div class="note">` bị báo lệch là báo động giả, vì regex `<div>` không khớp `<div class=...>`.

## 6. Verify sau khi publish

HTTP 200 là chưa đủ. Check thêm 3 thứ trên HTML đã upload:

```python
has_dia = bool(re.search(r'[ăâđêôơưáàảãạấầẩẫậéèẻẽẹíìỉĩịóòỏõọúùủũụýỳỷỹỵ]', plain, re.I))
moji   = len(re.findall(r'Ã.|â€|Ä.|ï¿½', plain))
```

- `has_dia` phải True. **Không có dấu = không được gửi.** Đây là standing rule của user.
- `moji` phải 0.
- Đếm `<h1>`, `<section>`, `<table>` khớp với bản local trước khi báo xong.

Playwright verify nếu Camofox chết: script `.cjs` dùng `playwright-core` + `C:/Users/NTQUANG_DELL/AppData/Local/ms-playwright/chromium-1228/chrome-win64/chrome.exe`. `browser_vision` có thể fail với deepseek-v4-flash (không nhận image) — dùng DOM check thay vision.

## 7. Case đã chạy

| Link | Nội dung |
|---|---|
| `preview.thefirstonly.com/rgjd6ciohgqt` | Tổng quan + hình hoạ, 9 phần, 4 bảng |
| `preview.thefirstonly.com/ok2535gevuvg` | Dịch toàn văn Molecules 2010, 15(3):1378-1397, CC BY, 13 mục |

Bài được chọn: Li J., Zhou B., *Biological Actions of Artemisinin*, doi:10.3390/molecules15031378, PMID 20335987, PMC6257283.
