# Europe PMC — verify PMID theo LÔ (batch) + kiểm tra topic/loài

Dùng khi cần xác minh nhiều PMID cùng lúc, và phải chắc bài ĐÚNG chủ đề + ĐÚNG loài
chứ không chỉ "PMID tồn tại".

## 1. Discovery (tìm bài)
```
GET https://www.ebi.ac.uk/europepmc/webservices/rest/search
  ?query=<truy vấn>&format=json&pageSize=8&resultType=lite&sort=CITED desc
```
- Trường tìm kiếm: `TITLE_ABS:"cụm từ"` (title + abstract), `EXT_ID:<pmid>`, `AND/OR`.
- `sort=CITED desc` → bài kinh điển trước; bỏ `sort` → bài mới trước.
- `resultType=lite` không có abstract → chỉ để lọc thô bước đầu.

## 2. Verify batch — 1 request cho N PMID (cách nhanh nhất)
```
query = "EXT_ID:123 OR EXT_ID:456 OR ..."   # ≤ ~18–20 PMID/request
format=json & resultType=core & pageSize=40
```
- So `hitCount` với số PMID gửi đi; tập `pmid` trả về còn thiếu = PMID **không tồn tại**.
- `resultType=core` trả `abstractText` → **bắt buộc đọc title + abstract** để xác nhận:
  (a) đúng bệnh/mầm bệnh, (b) đúng **loài**, (c) có số liệu đo được (n, %, năm, MIC…).
- Chạy 2 pass (pass cuối in lại title của toàn bộ PMID) để chốt danh sách verify.

## 3. Snippet Python
```python
BASE = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
def core_batch(pmids, n=40):
    q = " OR ".join("EXT_ID:%s" % p for p in pmids)
    url = BASE + "?" + urllib.parse.urlencode(
        dict(query=q, format="json", pageSize=str(n), resultType="core"))
    with urllib.request.urlopen(url, timeout=60) as r:
        d = json.load(r)
    return d["hitCount"], d["resultList"]["result"]   # r["title"], r["abstractText"]
```
`clean()` hữu ích: bỏ thẻ XML, unescape HTML, gộp khoảng trắng — vì abstract core có `<i>`,
`&lt;` và `\r\n`.

## 4. Cạm bẫy đã gặp thật
- **"pig breeders" = NGƯỜI chăn nuôi heo**, không phải heo. Nếu gán nhãn loài "heo"
  cho bài về người mang trùng ở hầu họng thì sai loài hoàn toàn → phải đọc abstract
  để phân loại loài, đừng suy từ tiêu đề.
- Tiêu đề có thể khớp chủ đề nhưng đối tượng là mouse/chuột/cattle/người → hạ mức
  bằng chứng và ghi rõ loài trong trường mô tả loài.
- Đừng trích số liệu (n, %, MIC…) từ snippet của công cụ search; chỉ lấy từ
  `abstractText` của `resultType=core`.
- `hitCount` có thể lớn hơn số PMID gửi đi (query khớp thêm bài khác) → luôn map theo
  `pmid` cụ thể, không đếm `hitCount` để kết luận.

## 5. Ghi lại để không verify lại
Lưu `pmid` + trường `da_verify` (mô tả cách verify, ví dụ
"Europe PMC core, title + abstract khớp") vào file kết quả. Lần sau chỉ cần verify
phần mới thêm.
