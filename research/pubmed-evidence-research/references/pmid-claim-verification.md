# Xác minh PMID ↔ claim (không để bài "gần chủ đề" đứng thay bài chủ chốt)

Bổ sung cho workflow E-utilities của skill này. Đã kiểm chứng 10/2026 khi dựng hồ sơ kim loại hiếm/đất hiềm dùng cho người.

## Vòng lặp bắt buộc: esearch → esummary → so TIÊU ĐỀ

`esearch` trả về PMID; **PMID là thật nhưng có thể là bài sai chủ đề**. Luôn gọi `esummary` cho các ID vừa tìm được và in ra `title / source / pubdate` rồi tự đối chiếu với claim.

```python
def esearch(term, n=2):
    u = ("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
         "?db=pubmed&retmode=json&retmax=%d&term=%s" % (n, urllib.parse.quote(term)))
    return json.loads(curl(u))["esearchresult"].get("idlist", [])

def esummary(ids):
    u = ("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
         "?db=pubmed&retmode=json&id=" + ",".join(ids))
    d = json.loads(curl(u))["result"]
    return [(i, d[i].get("title", "")[:140], d[i].get("source", ""), d[i].get("pubdate", "")) for i in ids]
```

`curl -s` qua `terminal` chạy ổn định; không cần API key cho esearch/esummary ở mức dùng này.

## Bẫy lớn nhất: truy vấn mô tả trả về bài THẬT nhưng LỆCH

Truy vấn theo cụm mô tả ("ALSYMPCA radium-223 overall survival phase 3", "VISION 177Lu-PSMA-617 phase 3",
"platinum anticancer mechanism Lippard") **không** trả về bài gốc. Kết quả thực tế nhận được:

- "ALSYMPCA …" → `35428207` (Sn-117m-DTPA) và `31479407` (bất bình đẳng chủng tộc với ²²³Ra) — **không phải** thử nghiệm ALSYMPCA.
- "VISION 177Lu-PSMA-617 …" → `41854638` (dosimetry) và `40723235` (phase 2 thuần) — **không phải** thử nghiệm VISION.
- "Cellular processing of platinum anticancer drugs" → `15789122` ✔ (khớp tiêu đề) — **thử tiêu đề chính xác thì ra**.

**Quy tắc:** ưu tiên **tiêu đề chính xác của bài muốn trích**; nếu sau 1–2 lần thử vẫn không ra → **bỏ trống trích dẫn** cho claim đó (ghi `pmid=''`, `note='chưa verify'`), tuyệt đối không lấy bài gần chủ đề làm "đại diện". Một PMID thật gán sai claim là lỗi nặng hơn một ô trống — người đọc không thể phát hiện.

Cách chấp nhận được khi không có bài gốc: trích **nhãn/hồ sơ phê duyệt** (số NDA) làm căn cứ cho hiệu lực, và dùng bài **khác** cho một claim **khác** đúng với nó (vd `31479407` chỉ để minh hoạ việc ²²³Ra được dùng trên lâm sàng).

## Kết luận âm là kết quả hợp lệ — nếu nêu rõ phương pháp

Ví dụ đã dùng: "các phức ruthenium **chưa** có thuốc nào được phê duyệt" — căn cứ là `esearch` trả rỗng cho tiêu đề giai đoạn III/đã phê duyệt **và** không có trong `openFDA drug/label.json`. Ghi kèm câu "esearch trả về NONE với truy vấn …" để người đọc tự tái lập phép kiểm.

## Định dạng tham chiếu trong hồ sơ dự án

Mỗi dòng dữ liệu có mảng `references[]`, phần tử dạng:

```json
{"type": "paper", "label": "Wang D, Lippard SJ. Cellular processing of platinum anticancer drugs. Nat Rev Drug Discov 2005;4(4):307-20",
 "pmid": "15789122", "doi": "10.1038/nrd1691", "note": "PMID verify qua esearch/esummary"}
```

`note` ghi **cách** đã kiểm. DOI chỉ điền khi lấy được từ nguồn (esummary/Crossref) — không suy DOI từ tên tạp chí.
