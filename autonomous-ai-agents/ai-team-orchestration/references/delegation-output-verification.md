# Verify deliverable của subagent trước khi relay cho user

**Bắt buộc từ 18/10/2026.** Summary của subagent là **SELF-REPORT** — nó mô tả việc subagent *tin* là mình đã làm, không phải việc đã xảy ra trên đĩa. Parent là người chịu trách nhiệm cuối trước user.

---

## Ca thật (18/10/2026) — suýt relay 1 kết luận sai

Batch 2 subagent: (A) research cơ chế heo↔người, (B) market gap analysis.

Summary A tự khai:

> "Deliverable complete and verified. 84 KB, ~460 dòng, **102 PMID riêng biệt**, đã **đọc abstract thật cho 100% PMID** được trích (resultType=core), phát hiện + loại bỏ bẫy guinea pig."

Summary B tự khai:

> "Done. File written and verified. 145 KB, ~130 tag F/E/I/H/INT."

Parent verify → cả hai artifact **có thật và đúng size**. 14/14 PMID spot-check **thật, title khớp claim**. Nhưng bước 4 (săn cái sai) lộ ra: tài liệu B gắn **[F]** cho một kết luận pháp lý **đã lỗi thời** — nó viện đúng NĐ 32/2026 nhưng bỏ qua NQ 66.19/2026/NQ-CP đã **dừng** thủ tục đó. Subagent không sai nguồn; nó sai **thời điểm hiệu lực**, và tag [F] khiến lỗi trông như đã kiểm chứng.

Kết quả: parent tự tra văn bản hợp nhất, sửa 9 chỗ trong tài liệu, thêm banner ĐÍNH CHÍNH. Nếu relay thẳng, founder đã nhận kết luận pháp lý ngược.

---

## Checklist 4 bước

### 1. Kiểm artifact vật lý (trước khi tin bất cứ con số nào)

```python
import os
base = r"D:\path\to\project"
for root, dirs, files in os.walk(base):
    dirs[:] = [d for d in dirs if d != ".git"]
    for f in files:
        p = os.path.join(root, f)
        print(f"{os.path.getsize(p):>9}  {os.path.relpath(p, base)}")
```

- So **số byte** với con số trong summary (bytes ≠ chars với tiếng Việt: 83,916 bytes ≈ 75,031 chars).
- Summary nói "đã ghi file X" mà `os.walk` không thấy → **bịa**. Dừng ngay, đừng relay.
- `read_file` báo "binary file" cho một `.md` là dấu hiệu encoding lạ → đọc lại bằng `open(p, encoding="utf-8")` trong `execute_code`, đừng kết luận file hỏng.

> **Bẫy phụ:** `search_files` đôi khi trả `IO error os error 2/3` với đường dẫn **có dấu cách** (`D:/Hermes Proj/...`). Dùng `terminal` (`ls`) hoặc `os.walk` trong `execute_code` thay thế — đừng kết luận thư mục không tồn tại.

### 2. Spot-check citation trên nguồn gốc

Không đọc lại toàn bộ. Lấy **10–15 citation quan trọng nhất** (những cái chống đỡ claim chính) và mở trên API gốc:

```
https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:<pmid>&format=json&pageSize=1&resultType=lite
```

- Đối chiếu **title** với claim mà citation supposedly chống đỡ. Title khớp claim là **điều kiện tối thiểu**, không phải điều kiện đủ.
- `resultType=lite` cho payload nhỏ; `core` kéo cả abstract → stdout dễ bị cắt, phải ghi ra file.
- `json.loads(s, strict=False)` vì abstract chứa control character.
- Script sẵn: `pubmed-evidence-research/scripts/verify_pmids.py <file.md>` — quét mọi PMID trong file, in title thật, exit 1 nếu có PMID không tồn tại.
- Citation là **DOI/preprint** (`10.1101/...`) thì verify riêng và kiểm xem subagent có gắn cờ "chưa bình duyệt" chưa.

### 3. Đọc phần summary bị cắt

Summary dài bị Hermes chèn:

```
[... middle omitted — see footer ...]
Full subagent output saved to: C:\Users\...\cache\delegation\subagent-summary-N-<ts>.txt
```

- **Luôn đọc lại file đó.** Phần bị cắt thường chứa đúng danh sách **điểm yếu / rủi ro / khoảng trống** — thứ quan trọng nhất cho quyết định của user.
- File summary đôi khi là UTF-16/CP1258 → decode thử nhiều encoding trước khi kết luận "file rỗng".
- Live transcript đầy đủ: `...\cache\delegation\live\<delegation_id>\task-N.log`.

### 4. Săn cái SAI, đừng săn cái đúng

Chọn **claim quyết định nhất** trong deliverable và tự tra nguồn gốc. Câu hỏi để chọn:

- Claim nào, nếu sai, làm **đảo kết luận** của cả tài liệu? → ưu tiên số 1.
- Claim nào được gắn tag mạnh nhất ([F] / "verified" / "cực kỳ quan trọng")? → tag mạnh là chỗ dễ ngủ quên nhất, vì nó *trông* đã được kiểm.
- Với claim pháp lý/quy định: **văn bản ban hành SAU có dừng/sửa điều khoản đó không?** Tra **văn bản hợp nhất** (nội dung hợp nhất) và **trang cơ quan quản lý ngành** — nơi duy nhất ghi phương thức mới thay thế.
- Với claim số liệu: con số đó lấy từ đâu, có phải đang **suy từ loài/mô hình khác** không?

---

## Cách báo cho user

Nói rõ **đã verify được gì và bằng cách nào**, không chỉ nói "đã kiểm tra":

```
| Kiểm | Kết quả |
|---|---|
| File tồn tại | ✅ 03a = 83,916 bytes · 04 = 148,732 bytes (khớp claim) |
| PMID mở lại trên Europe PMC | ✅ 14/14 thật, title khớp claim |
| Tổng citation | 101 PMID riêng biệt · 35 chỗ ghi thẳng "KHÔNG CÓ NGUỒN" |
```

Nếu tìm ra lỗi → sửa **tại chỗ trong artifact** (patch + banner đính chính đầu file + nguồn), commit, rồi mới báo. Đừng chỉ ghi chú trong chat: lần sau ai đọc file sẽ đọc bản sai.

---

## Khi nào bỏ qua checklist này

- Subagent chỉ trả lời câu hỏi đọc-hiểu (không tạo artifact lưu lại).
- Deliverable không chứa con số/citation nào (thuần văn xuôi/ý tưởng).
- Task mang tính thăm dò, user biết là bản nháp.

Còn lại: **verify rồi hãy relay.**
