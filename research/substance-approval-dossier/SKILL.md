---
name: substance-approval-dossier
description: "Use when verifying a substance's regulatory approvals."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [regulatory, FDA, openFDA, EMA, approval, dossier, evidence, citations, ingredients]
    related_skills: [pubmed-evidence-research, grounded-citations, vietnam-legal-advisory, research-reporting, research-html-catalog]
---

# Substance Approval Dossier (Hồ sơ phê duyệt chất)

## Mục đích

Trả lời câu hỏi dạng: *"Chất X đã được cơ quan quản lý nào phê duyệt, cho chỉ định/chức năng gì, đường dùng – liều bao nhiêu, ở dạng muối/phức nào — và điều đó nghĩa là gì với thị trường mục tiêu?"* — với **mỗi dòng phải có nguồn kiểm chứng được**.

Đây là lớp việc lặp lại trong các dự án nguyên liệu/sản phẩm (TPBVSK, phụ gia TĂCN, mỹ phẩm, thiết bị, khoáng chất): đã làm cho đất hiềm–heo (`rare-earth-pigs`), kim loại hiếm/đất hiềm–người (`say-phun-kiem`), phụ gia TĂCN.

## Khi nào dùng

- Cần biết **tiền lệ phê duyệt** của một chất/muối/phức trước khi đầu tư công bố sản phẩm.
- Cần **kết luận âm có căn cứ** ("không có đất hiếm nào trong 21 CFR Part 573"; "không phức ruthenium nào được phê duyệt").
- Cần bằng chứng "chất này đã dùng cho người/động vật ở liều nào, dạng nào".
- Xuất kết quả thành **JSON cho pipeline/report** của dự án (không phải bài luận).

## Stack xác minh 4 tầng — luôn đi từ nguồn quản lý → tài liệu → văn bản luật

| Tầng | Nguồn | Trả lời được gì |
|---|---|---|
| 1. Nhãn/hồ sơ phê duyệt | openFDA `drug/label.json` + `drug/drugsfda.json`, `accessdata.fda.gov` | số NDA/ANDA, biệt dược, đường dùng, **nguyên văn chỉ định + liều** |
| 2. Danh mục phụ gia/nguyên liệu | eCFR (`21 CFR 573` cho TĂCN), EU Register of Feed Additives, EFSA FEEDAP; VN: Phụ lục TT 24/2019/TT-BYT, TT 43/2014/TT-BYT | có/không có tên trong danh mục trắng + giới hạn liều |
| 3. Tiêu chuẩn quốc gia về giới hạn | QCVN 8-2:2011/BYT (VN), GB 2762 (TQ) | ngưỡng kim loại nặng/ô nhiễm — **phải kiểm bản mới nhất, xem pitfall** |
| 4. Tài liệu học thuật | PubMed E-utilities | cơ chế, dược động học, sinh khả dụng, RCT chủ chốt (xem `pubmed-evidence-research`) |

**Recipe truy vấn cụ thể + bẫy của từng nguồn:** `references/regulatory-source-recipes.md`.

## Workflow

### Bước 0 — Kế thừa schema TRƯỚC khi viết bất cứ dòng nào
Khi xuất file vào `data/` của một dự án đã có dữ liệu: **đọc một file anh em cùng thư mục trước** (`read_file` file `group*.json` gần nhất) và **copy đúng bộ key** của nó. Dự án thường có `build.py` normalize theo key cố định → sai key = dữ liệu bị bỏ qua âm thầm.

Kiểm tra luôn: thư mục đích có `_build_group*.py`, `group0.json`... không → nghĩa là các subagent khác đang ghi vào cùng chỗ; giữ đúng quy ước tên file được giao, đừng "cải tiến" tên.

### Bước 1 — Liệt kê chủ thể cần phủ, theo NHÓM không theo chất lẻ
Chia nhóm theo họ hoá học/khung pháp lý (vd: nhóm bạch kim; vàng; kim loại kiềm; kim loại phóng xạ; đất hiếm La/Ce/Gd/Lu). Nhóm giúp phát hiện chất bị bỏ sót và giúp kết luận theo cụm.

### Bước 2 — Xác minh từng chất bằng API, không bằng trí nhớ
Mọi số NDA/ANDA/PMID đều phải **lấy ra từ truy vấn**, không viết từ ký ức. Xem recipe ở references.

### Bước 3 — Chốt trạng thái pháp lý tại thị trường mục tiêu
Tách bạch 4 trạng thái và ghi rõ cái nào: (a) được phép dùng trong thực phẩm/TPBVSK · (b) bị cấm/hạn chế · (c) chỉ dùng như thuốc kê đơn · (d) **chưa có quy định nào**. Với VN: dùng `vietnam-legal-advisory` + `references/ree-rare-metals-human-medicine-vn.md` trong đó.

### Bước 4 — Xuất file + tự kiểm
Sau khi ghi JSON: `json.load()` lại và in ra (số dòng, key của dòng đầu, danh sách dòng thiếu `references`). Không báo "đã xong" mà chưa load lại file.

## Quy ước đầu ra (đã dùng cho các dự án này)

- **Tiếng Việt có dấu** trong mọi trường mô tả; giữ tên hoạt chất tiếng Anh ở trường `name_en`.
- **Mỗi dòng có `references[]`**, mỗi reference có `{type, label, pmid, doi, number, note}` — `type` ∈ `regulatory | legal | paper | gov | chemical`.
- **Chỗ chưa verify được: `number=''` + `note='chưa verify'`.** Không bịa PMID, số văn bản luật, số NDA, URL.
- **Kết luận âm phải ghi rõ là kết luận âm** ("KHÔNG có thuốc nào được phê duyệt", "esearch trả về rỗng") — kèm phương pháp để người đọc tự kiểm.
- Trường `verification` của mỗi dòng nói **cách** đã kiểm (API nào, ngày nào), không chỉ nói "đã kiểm".
- Giá trị hoá học/Ksp không có nguồn sơ cấp: ghi là **"giá trị tham chiếu"** + `note='chưa verify nguồn sơ cấp'`. Đừng để chúng trông như số liệu đã verify.
- Có mục **đính chính** khi phát hiện hồ sơ cũ/số liệu cũ sai (xem ví dụ GB 2762, USGS trong references).

## Pitfalls

### ❌ Tra số NDA bằng `brand_name` rồi kết luận "không tồn tại"
`openfda.brand_name:"FOSRENOL"` trả về rỗng dù thuốc có thật (đã ngừng bán / nhãn chuyển sang generic). **Luôn tra lại bằng `openfda.generic_name:"<HOẠT CHẤT>"`.** Kết quả rỗng sau khi đã thử cả hai → mới được coi là "đã ngừng lưu hành", và vẫn phải ghi `number='' note='chưa verify'` cho số NDA gốc.

### ❌ Để một PMID thật đứng thay cho một claim nó không chứng minh
Truy vấn theo chủ đề trả về **bài thật nhưng lệch**. Nếu không tìm được đúng bài chủ chốt → **bỏ trống trích dẫn**, đừng lấy bài gần chủ đề. Chi tiết + quy trình esearch→esummary: `pubmed-evidence-research` → `references/pmid-claim-verification.md`.

### ❌ Ghi "TQ giới hạn REE trong thực phẩm" mà không kiểm bản GB 2762
GB 2762-**2005/2012** có giới hạn `稀土`; **GB 2762-2017 đã XOÁ** ("删除了稀土限量要求"), các bản 2022/2025 cũng không có. Trích đúng bản, đúng năm — và nếu đang sửa một hồ sơ cũ thì **ghi rõ là đính chính**.

### ❌ Dùng số liệu trữ lượng/sản lượng cũ
USGS MCS các bản gần đây điều chỉnh mạnh số của VN (REE: 22 triệu tấn → **3,5 triệu tấn**; sản lượng 300 → 150 tấn). Luôn đọc bản MCS mới nhất, không chép lại con số từ hồ sơ dự án cũ.

### ❌ Suy ra "được phép" từ tính chất vật lý ("chất không tan nên vô hại/không tính là nguyên liệu")
Cơ quan quản lý phân loại theo **nguồn gốc/công dụng dùng cho thực phẩm**, không theo độ tan. Chất kết tủa hoàn toàn ở pH cao vẫn là "nguyên liệu không thuộc loại dùng cho thực phẩm". Kết luận pháp lý phải bám điều khoản, không bám hoá học.

### ❌ Trình bày chuỗi xác minh trước khi kiểm **hiệu lực văn bản**
Văn bản còn hiệu lực hay không là câu hỏi **độc lập** với việc nó có chứa điều khoản đúng. Với `vietnam-legal-advisory` phải mở tab **Thuộc tính + Lịch sử** trước khi trích số điều.

### ❌ Chạy script dài inline
Script dài (>~40 dòng) truyền thẳng vào tool chạy code có thể bị cắt giữa dòng → `SyntaxError` khó hiểu. **Fix: `write_file` script ra file rồi chạy bằng `terminal`** — nội dung không bị cắt, chạy lại được, và giữ làm bằng chứng cho lần sau.

### ❌ Sinh JSON lớn bằng Python literal với tiếng Việt
Dấu nháy kép **không escape** lọt vào giữa string nháy kép (rất hay xảy ra khi trích câu tiếng Việt có "…" hoặc tên sản phẩm trong ngoặc kép) → `SyntaxError` báo lệch dòng, và phép đếm nháy theo dòng **không** phát hiện được (số nháy vẫn chẵn).
**Fix khi build file dữ liệu:** dùng `'…'` (nháy đơn) cho mọi trích dẫn nằm trong string nháy kép; sau khi ghi file, debug bằng `compile()` rồi in đúng dòng lỗi:
```python
src = open(p, encoding='utf-8').read().split('\n')
try: compile('\n'.join(src), p, 'exec')
except SyntaxError as e: print(e.lineno, e.offset, src[e.lineno-1])
```
Luôn `json.load()` lại file sau khi ghi.

## Tham khảo

- 📄 `references/regulatory-source-recipes.md` — curl/web recipe cho openFDA `label.json` + `drugsfda.json`, `accessdata.fda.gov`, eCFR `21 CFR 573`, EU Register/EFSA, GB 2762; kèm bảng chủ thể × số phê duyệt đã verify ở 2 dự án.
- 📄 `vietnam-legal-advisory` → `references/ree-rare-metals-human-medicine-vn.md` — khung pháp lý VN cho TPBVSK + đất hiềm/kim loại hiếm (điều khoản cụ thể).
- 📄 `pubmed-evidence-research` → `references/pmid-claim-verification.md` — xác minh PMID ↔ claim.
