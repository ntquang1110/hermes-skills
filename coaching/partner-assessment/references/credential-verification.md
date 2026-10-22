# Xác minh hồ sơ giấy tờ (CV, danh mục công bố, bằng cấp)

Khi đối tác / ứng viên là người có nền chuyên môn (nhà nghiên cứu, kỹ thuật, bác sĩ, chuyên gia)
và gửi CV hoặc danh mục công bố: **đừng đọc CV rồi tin**. Mọi thứ trên CV đều kiểm được trong
5 phút bằng registry công khai.

## 3 registry phải tra

| Registry | Endpoint | Xác minh được |
|---|---|---|
| **Crossref** | `https://api.crossref.org/works/<DOI>` | Bài có thật không, tạp chí nào, **thứ tự tác giả thật**, số tài liệu tham khảo, năm, NXB |
| **ORCID** | `https://pub.orcid.org/v3.0/<orcid-id>/record` (header `Accept: application/json`) | Danh mục công bố **đầy đủ** — thường lộ ra bài CV không ghi |
| **PubMed** | `esummary.fcgi?db=pubmed&id=<pmid>&retmode=json` | PMID có thật, tạp chí, năm |

Crossref đôi khi trả `403` cho DOI hợp lệ khi thiếu User-Agent. Luôn set User-Agent:

```python
import urllib.request, json
req = urllib.request.Request("https://api.crossref.org/works/10.xxxx/yyyy",
      headers={"User-Agent": "check/1.0 (mailto:you@example.com)"})
m = json.loads(urllib.request.urlopen(req, timeout=20).read())["message"]
authors = [f"{a.get('given','')} {a.get('family','')}".strip() for a in m.get("author", [])]
print(m["container-title"][0], m["published"]["date-parts"][0][0], f"{m['reference-count']} refs")
print(authors[:5])   # ← thứ tự tác giả THẬT, không phải như CV khai
```

ORCID trả cả bài chưa có tạp chí (`journal-title` = `"?"`), và cả `external-ids` chứa DOI —
đây là cách phát hiện bài CV che giấu hoặc ghi sai.

## 5 thứ phải kiểm, không được bỏ

1. **Thứ tự tác giả.** CV hay ghi "tác giả chính". Crossref trả mảng tác giả theo đúng thứ tự.
   **Đứng tên đầu ≠ làm chính** — vẫn phải hỏi trực tiếp vai trò cụ thể (làm phần nào, số liệu nào).
2. **Preprint hay đã bình duyệt.** DOI dạng `10.21203/rs.3.rs-...` (Research Square), bioRxiv,
   SSRN, medRxiv = **preprint, chưa qua peer review**. CV thường ghi như bài báo thật. Hạ giá trị
   đánh giá và nói rõ trong báo cáo.
3. **Tạp chí thật hay tạp chí săn mồi.** Kiểm `container-title` + nhà xuất bản. Nếu ORCID để trống
   tên tạp chí → bài đó chưa có nơi đăng chính thức.
4. **Lỗ hổng thời gian trong bảng học vấn.** Khoảng trống hoặc chồng lấn (VD 2 chương trình tiến sĩ
   liên tiếp) → ghi thành **câu hỏi cần hỏi**, không tự suy diễn lý do.
5. **Xung đột lợi ích.** Đọc mục "competing interests" cuối bài. Nếu người hướng dẫn hoặc đồng tác
   giả nằm trong ban điều hành công ty liên quan tới kết quả, ghi rõ khi trích số liệu.

## Cấu trúc báo cáo hồ sơ

Dùng đúng 3 tầng của skill này: **Mạnh / Còn thiếu / Phải xác minh**.
Tầng "phải xác minh" là phần giá trị nhất — liệt kê câu hỏi cụ thể, **không kết luận thay user**.

Với mỗi công bố, ghi rõ: tạp chí, năm, số đồng tác giả, vị trí tên, đã bình duyệt hay chưa,
số tài liệu tham khảo. Kèm đánh giá mạng lưới (giáo sư hướng dẫn là ai, cố vấn là ai).

## Khoảng cách phải nêu thẳng

Người có hồ sơ nghiên cứu tốt thường thiếu: **kinh nghiệm sản phẩm, bào chế, chi phí, thực địa,
thương mại**. Chứng minh cơ chế và phát triển sản phẩm là hai nghề khác nhau. Nói rõ người này
hợp vai nào, và nếu tuyển thì phải ghép với ai.

## Đã kiểm chứng

Session 10/2026: CV 2 trang gửi qua link viewer. Xác minh 4/4 DOI bằng Crossref → đủ 4 bài,
đúng 2 bài tác giả chính (một bài PNAS Nexus 17 tác giả, một bài Elsevier 16 tác giả), 1 bài chỉ
là preprint Research Square (CV ghi như bài báo), 1 bài đồng tác giả. ORCID trả 5 works → lộ thêm
bài thứ 5 CV không ghi. Phát hiện 2 chương trình tiến sĩ liên tiếp + xung đột lợi ích thương mại
của giáo sư hướng dẫn trong mục competing interests.
