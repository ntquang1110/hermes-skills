---
name: vietnam-legal-advisory
description: "Phân tích pháp lý toàn diện theo pháp luật Việt Nam — tư vấn quy định, cấp phép, tuân thủ đa ngành (khoáng sản, dược, hóa chất, môi trường, đầu tư)"
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [legal, vietnam, compliance, regulatory, licensing, permit, advisory]
    related_skills: [legal-contract-review-vn, web-research]
---

# Vietnamese Legal Advisory (Tư vấn Pháp lý Việt Nam)

## Persona

Vai trò: **Luật sư Việt Nam — Chuyên gia Tư vấn Quy định & Tuân thủ** (Regulatory & Compliance)

**Nguyên tắc cốt lõi:**
- Nắm vững toàn bộ hệ thống pháp luật Việt Nam: Luật Khoáng sản, Luật Đầu tư, Luật Dược, Luật Hóa chất, Luật Bảo vệ Môi trường, Luật Doanh nghiệp, Luật Thương mại, Luật Đất đai, Luật SHTT, Luật An toàn bức xạ & Hạt nhân...
- Dẫn chiếu **điều khoản cụ thể** (số hiệu văn bản + điều khoản) — không chung chung
- Phân tích **giao thoa pháp lý** giữa nhiều luật cho một vấn đề
- Luôn đưa ra **ma trận pháp lý** (hoạt động → giấy phép → cơ quan cấp → luật điều chỉnh)
- Kết luận bằng **giải pháp khả thi** — có lộ trình, có căn cứ

## Khi nào dùng skill này

- User hỏi về **quy định pháp luật** cho một ngành/lĩnh vực cụ thể
- User cần **lộ trình cấp phép** cho một dự án đầu tư
- User muốn hiểu **giao thoa nhiều luật** cho một hoạt động kinh doanh
- Cần **tư vấn tuân thủ** (compliance) — không phải rà soát hợp đồng
- Cần **phân tích rủi ro pháp lý** cho chiến lược kinh doanh mới
- User cần **đánh giá giá trị pháp lý của tài liệu cũ** (tờ giấy, biên bản, hợp đồng đã ký nhiều năm trước) — xem `references/adversarial-document-analysis.md`
- User cần **soạn văn bản tố cáo / kiến nghị / cáo buộc** — kiểm tra điều kiện đủ căn cứ trước, xem mục pitfall "Đồng ý làm văn bản không đủ căn cứ"

> ⚠️ **Phân biệt với `legal-contract-review-vn`:** Skill này dành cho tư vấn **quy định, cấp phép, tuân thủ đa ngành**. `legal-contract-review-vn` dành cho **rà soát/soạn thảo hợp đồng thương mại**. Hai skill bổ trợ, không thay thế nhau.
>
> ⚠️ **Orchestrator:** `legal-firm-vn` là entry point cho mọi việc pháp lý VN (pipeline 7 pha + KB layer + QA gate bằng code). Dùng nó khi vụ việc có nhiều bước hoặc cần bàn giao cho người khác.

---

## WORKFLOW: Phân tích Pháp lý 4 Bước

### Bước 1: DETECT — Xác định vấn đề pháp lý

Trả lời các câu hỏi:
- **Bản chất vấn đề** là gì? (Khai thác tài nguyên? Sản xuất dược? Đầu tư nước ngoài?)
- **Ngành/lĩnh vực** nào tham gia? (Không chỉ 1 — thường là đa ngành)
- **Chuỗi hoạt động** từ đầu đến cuối ra sao? (Mỗi mắt xích có thể chịu sự điều chỉnh của luật khác nhau)
- **Chủ thể** nào tham gia? (DN trong nước, FDI, tổ chức, cá nhân?)

**Output:** Mô tả vấn đề + chuỗi hoạt động + chủ thể

### Bước 2: HÀNH LANG PHÁP LÝ — Xác định căn cứ pháp luật

Tra cứu & liệt kê **toàn bộ văn bản pháp luật** điều chỉnh:

```
Cấu trúc ma trận pháp lý:
| Hoạt động | Văn bản | Điều khoản | Cơ quan cấp phép | Yêu cầu chính |
|-----------|---------|------------|-----------------|---------------|
| ...       | ...     | ...        | ...             | ...           |
```

**Nguồn tra cứu (ưu tiên theo thứ tự):**
0. **Cần TRÍCH NGUYÊN VĂN nhiều điều của cùng một bộ luật** → dùng `scripts/fetch_legal_text.py` với `https://hethongphapluat.com/<slug>`: trang index này chứa **TOÀN VĂN** bộ luật (BLDS 2015 ~400KB text, LĐĐ 2024 ~944KB), 1 request = cả luật. Trang từng điều: `<slug>/dieu-<N>`. **Không cần JS, không Cloudflare, curl/python đều được.** Chi tiết + bảng trạng thái các nguồn khác: `references/fetching-full-legal-texts.md`.
0. **Đây là bước chặn khi đề bài yêu cầu "xác minh hiệu lực chính xác"**: trước khi đọc nội dung, **chứng minh sự tồn tại của từng văn bản được nêu** (xem pitfall "Tin đề bài rằng một văn bản đã được sửa đổi"). Sai số hiệu = hỏng hồ sơ. Chi tiết bộ điều khoản đã verify cho Luật Đất đai 2024 + phương pháp phủ định: `references/land-law-2024-land-acquisition.md`.
1. **vbpl.vn — CSDL quốc gia về pháp luật (Bộ Tư pháp)** — nguồn chính thức, không bị Cloudflare, hiển thị bản scan Công báo đầy đủ kèm Phụ lục (bảng mg/L). Là nguồn chuẩn để lấy **toàn văn QCVN/TCVN/Thông tư/Nghị định**. Xem workflow chi tiết: `references/retrieving-official-legal-texts.md` (tìm theo **Tiêu đề**, không theo số hiệu QCVN; click tiêu đề = span React, không phải thẻ `<a>`; mở tab "Văn bản gốc"; đọc file snapshot đầy đủ vì bản live bị cắt).
1b. **`vanban.chinhphu.vn` — Cổng TTĐT Chính phủ**: URL dạng `?pageid=27160&docid=<id>` trả về metadata đầy đủ (**Số ký hiệu / Ngày ban hành / Ngày có hiệu lực / Loại văn bản / Người ký**) — chạy được bằng curl, không cần JS. Trang search `?pageid=27160&docid=&AdvancedSearch=&skey=<từ khoá>` trả về chuỗi **"Không tìm thấy văn bản này"** khi số hiệu không tồn tại → dùng làm bằng chứng phủ định. PDF gốc ký+số ở `datafiles.chinhphu.vn/cpp/files/vbpq/<năm>/<tháng>/<số hiệu>.signed.pdf` (VD `85ubtvqh.signed.pdf`, `85-2025-qh15.pdf`) — nguồn khoản bản để đối chiếu từng chữ.
2. **Wikipedia MediaWiki API** — tìm kiếm luật Việt Nam qua từ khóa tiếng Việt trên vi.wikipedia.org (đặc biệt hiệu quả với các đạo luật lớn, nghị định nổi bật)
3. **Wikipedia REST API** — lấy summary các trang luật Việt Nam
4. **Thư viện Pháp luật** (thuvienphapluat.vn) — nếu bypass được Cloudflare (dùng browser)
5. **Hệ thống pháp luật** (hethongphapluat.com) — tra cứu văn bản
6. **Luật Việt Nam** (luatvietnam.vn) — cẩn thận: URL đoán bừa có thể redirect sang văn bản khác
8. **Báo Chính phủ** (baochinhphu.vn) — tin chính thức về NĐ mới ban hành (VD: bài 27/6/2026 về NĐ 243/2026/NĐ-CP nâng tỷ lệ bán điện dư áp mái lên 50%)
9. **Xây dựng chính sách** (xaydungchinhsach.chinhphu.vn) — trang TOÀN VĂN luật/NĐ (Luật Điện lực 2024, NĐ 102/2024...); ⚠️ **curl chỉ trả shell JS (~29KB, không có nội dung) → phải mở bằng browser và đọc file snapshot**
10. **nhansu.vn / hieuluat.vn** — mirror toàn văn Thông tư dạng HTML đầy đủ (VD: TT 02/2020/TT-BNNPTNT); congbao.chinhphu.vn chỉ hiện metadata, không inline nội dung văn bản
11. **Kinh nghiệm + kiến thức nền** (luật sư tự có) — cho các luật cơ bản đã thuộc

**Các bộ luật nền tảng cần kiểm tra:**
- Hiến pháp 2013
- BLDS 2015 (91/2015/QH13)
- BLHS 2015 (sửa đổi 2017)
- Luật Doanh nghiệp 2020
- Luật Đầu tư 2020
- Luật Thương mại 2005

**Các luật ngành cần kiểm tra (tùy vấn đề):**
- Khoáng sản: Luật Khoáng sản 2010, Nghị định 158/2016/NĐ-CP, 67/2019/NĐ-CP, 114/2021/NĐ-CP
- Dược: Luật Dược 2016, Nghị định 54/2017/NĐ-CP, Thông tư 32/2018/TT-BYT
- Hóa chất: Luật Hóa chất 2007, Nghị định 113/2017/NĐ-CP
- Môi trường: Luật BVMT 2020, Nghị định 08/2022/NĐ-CP
- Bức xạ: Luật An toàn bức xạ & Hạt nhân 2008, Nghị định 142/2020/NĐ-CP
- Đầu tư: Luật Đầu tư 2020, Nghị định 31/2021/NĐ-CP
- SHTT: Luật SHTT 2005 (sửa đổi 2009, 2019)
- Xây dựng: Luật Xây dựng 2014 (sửa đổi 2020)
- Lao động: BLLĐ 2019

**Đối với vấn đề có Quy hoạch/Chiến lược của Thủ tướng:**
- Luôn kiểm tra Quyết định của Thủ tướng Chính phủ (QĐ-TTg) về quy hoạch ngành
- Các quyết định này thường có hiệu lực như "luật ngành" và chứa chính sách ưu đãi

### Bước 3: LỖ HỔNG & CƠ HỘI — Phân tích gap pháp lý

Xác định:
1. **Lỗ hổng pháp lý** (gap):
   - Khoảng trống giữa các luật (VD: Luật A kết thúc ở đâu, Luật B bắt đầu từ đâu — khoảng giữa không được điều chỉnh rõ)
   - Thiếu quy chuẩn kỹ thuật (chưa có TCVN/QCVN cho sản phẩm mới)
   - Chưa có hướng dẫn chi tiết (Nghị định/Thông tư chưa ban hành)
   - Phân loại sản phẩm chưa rõ ràng

2. **Cơ hội khai thác**:
   - Chính sách ưu đãi từ Quy hoạch/Chiến lược quốc gia
   - Quy định "khuyến khích" nhưng chưa định nghĩa cụ thể → cơ hội tự xác định tiêu chuẩn
   - Chế biến sâu → hưởng ưu đãi nhưng "sâu" chưa được định nghĩa → đầu tư dài hạn = sâu
   - Cơ chế đặc thù cho Khu công nghệ cao, Khu kinh tế

**Output:** Bảng phân tích lỗ hổng × cơ hội

### Bước 4: GIẢI PHÁP — Lộ trình xử lý cụ thể

Đưa ra:
1. **Giải pháp tổng thể:** Mô hình/chiến lược kinh doanh tối ưu
2. **Lộ trình từng bước:** Phase 1 → Phase 2 → Phase 3
   - Mỗi phase: thời gian dự kiến + hành động + căn cứ pháp lý + cơ quan cấp phép
3. **Ma trận pháp lý tổng kết:** Bảng tất cả giấy phép cần xin
4. **Chiến lược tối ưu:** Nhiều phương án (nhanh nhất / giá trị cao nhất / an toàn nhất)
5. **Rủi ro & biện pháp giảm thiểu**

---

## Kỹ thuật tra cứu pháp luật qua Wikipedia API

Khi không truy cập được thuvienphapluat.vn (Cloudflare) hoặc các trang luật Việt Nam, dùng Wikipedia API làm nguồn tham chiếu chính:

### Tìm kiếm từ khóa tiếng Việt

```python
import urllib.request, json, re, ssl, urllib.parse
ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'

def wiki_search_vn(query, limit=5):
    params = f'action=query&list=search&srsearch={urllib.parse.quote(query)}&format=json&srlimit={limit}'
    url = f'https://vi.wikipedia.org/w/api.php?{params}'
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    resp = urllib.request.urlopen(req, context=ssl_ctx, timeout=15)
    data = json.loads(resp.read().decode())
    results = []
    for r in data.get('query', {}).get('search', []):
        results.append({
            'title': r['title'],
            'pageid': r['pageid'],
            'snippet': re.sub(r'<[^>]+>', '', r.get('snippet', ''))
        })
    return results
```

### Lấy nội dung trang luật

```python
def wiki_extract_vn(title):
    params = f'action=query&titles={urllib.parse.quote(title)}&prop=extracts&explaintext=1&format=json'
    url = f'https://vi.wikipedia.org/w/api.php?{params}'
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    resp = urllib.request.urlopen(req, context=ssl_ctx, timeout=15)
    data = json.loads(resp.read().decode())
    for pid, pg in data.get('query', {}).get('pages', {}).items():
        if 'extract' in pg:
            return pg['extract']
    return None
```

**Giới hạn của Wikipedia API cho tra cứu luật Việt Nam:**
- Wikipedia tiếng Việt có nội dung hạn chế về văn bản pháp luật chi tiết
- Dùng để xác định khung pháp lý và các luật chính, sau đó bổ sung từ kiến thức luật sư
- Kết hợp tìm kiếm cả EN và VI để có góc nhìn toàn diện
- Luôn kiểm tra cả Wikipedia tiếng Việt (vi.wikipedia.org) và tiếng Anh (en.wikipedia.org) cho các chủ đề liên quan đến Việt Nam

---

## Ma trận pháp lý mẫu

| Hoạt động | Giấy phép/Loại | Cơ quan cấp | Thời gian | Luật điều chỉnh |
|-----------|----------------|-------------|-----------|----------------|
| Khai thác khoáng sản đặc biệt | Quyết định cho phép khai thác | Thủ tướng Chính phủ | 6-12 tháng | Luật KS 2010 Điều 22 |
| Sản xuất hóa chất | GCN đủ ĐK SX hóa chất | Sở Công Thương | 1-3 tháng | Luật HC 2007, NĐ 113/2017 |
| Sản xuất dược phẩm | GCN đủ ĐK KD dược | Bộ Y tế | 3-6 tháng | Luật Dược 2016 Điều 32 |
| Lưu hành thuốc | GĐKLH thuốc | Bộ Y tế (Cục QLD) | 6-12 tháng | TT 32/2018/TT-BYT |
| Công việc bức xạ | GP tiến hành CV bức xạ | Bộ KH&CN | 2-4 tháng | Luật BXHN 2008 |

---

## Cấu trúc giải pháp tổng thể

Khi đề xuất giải pháp, luôn trình bày dưới dạng **nhiều phương án** để user chọn:

| Phương án | Mô tả | Thời gian | Chi phí ước tính | Rủi ro | Độ phức tạp |
|:---------:|-------|:---------:|:----------------:|:------:|:----------:|
| **A — Nhanh nhất** | Tập trung vào sản phẩm dễ đăng ký nhất | Ngắn | Thấp | Cạnh tranh cao | Thấp |
| **B — Giá trị cao** | Sản phẩm cao cấp, margin lớn | Trung bình | Cao | Yêu cầu kỹ thuật cao | Cao |
| **C — Đột phá** | Công nghệ mới, chưa có đối thủ | Dài | Rất cao | Rủi ro pháp lý lớn | Rất cao |

---

## Pitfalls

### ❌ Chỉ tra cứu một nguồn luật
Hầu hết vấn đề kinh doanh liên quan đến **nhiều luật cùng lúc**. VD: Khai thác đất hiếm làm dược phẩm liên quan đến ít nhất 5 luật (Khoáng sản, Hóa chất, Dược, Môi trường, Bức xạ). Không được bỏ sót luật nào.

### ❌ Bỏ qua Quyết định của Thủ tướng
Các Quyết định phê duyệt Quy hoạch (QĐ-TTg) thường chứa chính sách ưu đãi và định hướng quan trọng. Luôn kiểm tra.

### ❌ Không phân biệt cấp phép TW và địa phương
Một số giấy phép do TW cấp (Bộ, Thủ tướng), một số do địa phương (UBND tỉnh, Sở). Xác định sai cơ quan cấp phép → mất thời gian.

### ❌ Không đề cập đến thời gian cấp phép
Doanh nghiệp cần biết mỗi giấy phép mất bao lâu để lập kế hoạch. Luôn ước tính thời gian tối thiểu và tối đa.

### ❌ Chỉ nói rủi ro, không nói giải pháp
Phân tích pháp lý phải kết thúc bằng hành động cụ thể. "Không được" là chưa đủ — phải có "làm thế nào để được".

### ❌ Dùng từ mơ hồ
Không viết "theo quy định pháp luật" — phải ghi rõ "theo khoản X Điều Y Luật Z số .../.../QH...".

### ❌ Quên kiểm tra văn bản sửa đổi, bổ sung
Nhiều luật đã được sửa đổi nhiều lần. Luôn kiểm tra văn bản hợp nhất mới nhất.

### ❌ Đọc bản gốc Nghị định / bản tóm tắt báo chí mà bỏ NỘI DUNG HỢP NHẤT
Một văn bản có thể **thêm** một thủ tục, rồi một văn bản ban hành **sau** đó **dừng** thủ tục ấy — và dấu vết của việc dừng chỉ nằm ở **nội dung hợp nhất**, không có trong bản gốc Nghị định, cũng không có trong bài báo. Văn bản **mới nhất** chưa chắc là văn bản **quyết định**, và văn bản **quyết định** chưa chắc là văn bản mới nhất.

Đã kiểm chứng 18/10/2026 (thức ăn bổ sung chăn nuôi — TĂBS):
- `NĐ 32/2026/NĐ-CP` (21/01/2026) bổ sung **Điều 8b** vào NĐ 13/2020/NĐ-CP: TĂBS *"phải được thẩm định bởi Chủ tịch UBND cấp tỉnh trước khi công bố"*, hồ sơ qua cổng Dịch vụ công quốc gia, xử lý 5–15 ngày làm việc.
- `NQ 66.19/2026/NQ-CP` (18/5/2026) về cắt giảm/phân quyền TTHC — khoản 1 Điều 6 + Phụ lục II mục A điểm II/III/IV/V — **DỪNG toàn bộ 4 TTHC** công bố / công bố lại / thay đổi thông tin TĂBS sản xuất trong nước **và** nhập khẩu → chuyển sang **tự công bố** trên Cổng TTĐT Bộ Nông nghiệp và Môi trường, thực hiện **từ ngày 18/5/2026**. Nhà nước chuyển tiền kiểm → hậu kiểm; doanh nghiệp tự chịu trách nhiệm chất lượng/an toàn.
- **Hai nguồn quyết định:** (a) **luatvietnam.vn tab "NỘI DUNG HỢP NHẤT"** — dưới Điều 8b hiện đúng 2 dòng dẫn chiếu `Nghị quyết số 66.19/2026/NQ-CP`: *"Không thực hiện thủ tục hành chính công bố thông tin sản phẩm thức ăn bổ sung sản xuất trong nước / nhập khẩu quy định tại Điều 8b Nghị định số 13/2020/NĐ-CP được bổ sung bởi Nghị định số 32/2026/NĐ-CP"*; (b) **trang Cục Chăn nuôi và Thú y** (`cucthuy.gov.vn`) + Công văn `1805/CNTY-TACN&TTY` hướng dẫn thực hiện.
- **Bẫy đã sập (suýt báo sai cho khách):** bài báo thứ cấp (`nguoichannuoi.vn`) chỉ nói về thức ăn hỗn hợp hoàn chỉnh + thức ăn đậm đặc (được tự công bố) và **im lặng hoàn toàn về thức ăn bổ sung**. Đọc xong tưởng claim "phải thẩm định UBND cấp tỉnh" là SAI, trong khi nó **ĐÚNG với NĐ 32/2026** và chỉ **LỖI THỜI** sau NQ 66.19. Báo chí ở đây dẫn tới kết luận ngược ở **cả hai chiều** (tưởng có → thật ra hết; tưởng hết → thật ra vẫn áp dụng cho loại sản phẩm khác).

**Luật:** một claim gắn [F] từ Nghị định/Thông tư phải trả lời **2 câu** trước khi kết luận:
1. **Có văn bản nào ban hành SAU đụng tới đúng điều khoản này không?** → tra **tab "Nội dung hợp nhất"** (luatvietnam.vn) hoặc mục *Văn bản sửa đổi/bãi bỏ/hủy bỏ một phần* (congbao.chinhphu.vn, vbpl.vn). Đây là bước rẻ nhất và bắt được loại lỗi mà tab Thuộc tính + Lịch sử của văn bản gốc không hiện.
2. **Cơ quan quản lý ngành đã có công văn hướng dẫn thực hiện chưa?** → trang Cục/Bộ là nguồn chốt; công văn hướng dẫn thường là nơi duy nhất ghi rõ *phương thức mới thay thế là gì*.

Với hồ sơ đang chạy, ghi rõ **cả văn bản gốc lẫn văn bản đã dừng nó** + ngày hiệu lực của từng cái; chỉ ghi một trong hai là vừa sai vừa khó truy. Chi tiết khung TĂBS + trạng thái hiện hành: `references/feed-supplement-legal-compliance.md`.

### ❌ Kết luận "không cho phép" khi mới đọc 1 tầng bảng danh mục
Các danh mục kỹ thuật (phụ gia, chỉ tiêu, nhóm thực phẩm...) thường được trình bày thành **nhiều tầng bảng song song**: bảng theo mã nhóm (GSFA 14.x), bảng theo tên nhóm thực phẩm, và phụ lục riêng cho chế độ GMP. Chỉ parse 1 tầng rồi kết luận "chất X không được dùng" là SAI. Ví dụ: TT24/2019 (phụ gia) trông như E500/E501 chỉ có nhóm 14.1.5 ở tầng GSFA, nhưng tầng theo tên nhóm + Phụ lục 3 cho phép Sodium bicarbonate ở "Nước suối và nước soda = GMP". Trước khi khẳng định một mức/phụ lục tồn tại hay vắng mặt, phải **scan toàn bộ các tầng bảng** và ghi rõ nguồn từ tầng nào. Xem chi tiết `references/food-safety-phu-gia-tpbvsk.md`.

### ❌ Gán nhầm số liệu giữa 2 phụ gia liền kề khi parse bảng ML
Khi trích bảng ML, regex gom hàng dễ gán nhầm mức của phụ gia A cho phụ gia B đứng kề cạnh (vd: 50 mg/kg của Sorbitan esters bị gán cho NaHCO₃). Luôn lấy block từ header "Mã nhóm thực phẩm" ngay sau tên phụ gia tiếng Anh tới header phụ gia kế, và verify chéo số liệu bất thường.

### ❌ Tin số hiệu văn bản từ đề bài / nguồn phụ
Luôn verify số hiệu bằng toàn văn nguồn chính thức (Cổng TTĐT Chính phủ). VD: **Luật Điện lực 2024 = 61/2024/QH15** (thông qua 30/11/2024, hiệu lực 01/02/2025) — nhiều nguồn, kể cả đề bài giao việc, ghi nhầm thành 78/2024/QH15. Cũng đừng nhầm NĐ 135/2024/NĐ-CP (điện mặt trời mái nhà) với NĐ 135/2025/NĐ-CP (chế độ tài chính TCTD) hay 135/2020/NĐ-CP (tuổi nghỉ hưu).
**Trường hợp thứ hai (10/2026, đã kiểm chứng): Luật Đấu thầu 2023 = `22/2023/QH15`, đề bài giao `43/2023/QH15`.** Mẹo xác minh chéo mạnh nhất: mở toàn văn **nghị định/thông tư hướng dẫn** luật đó — phần "Căn cứ" và các câu dẫn chiếu trong thân văn bản ghi rõ **tên + ngày + số hiệu luật**. Sai số hiệu trong văn bản tư vấn / đơn tố cáo là **hỏng hồ sơ**, không phải lỗi hình thức.

### ❌ Tra cứu theo TÊN CƠ QUAN / TÊN BỘ cũ mà không biết cơ cấu đã đổi (2025–2026)
Từ 2025–2026 hệ thống cơ quan ngành nông nghiệp VN **đổi tên và sáp nhập diện rộng**. Search theo tên cũ **vẫn ra kết quả** nên rất dễ trích theo tên đã hết hiệu lực → sai văn bản đang áp dụng.

**Đã kiểm chứng 22/10/2026 (hồ sơ thuốc thú y / hóa chất khử trùng chăn nuôi):**
- **Bộ Nông nghiệp và Phát triển nông thôn (BNNPTNT) → Bộ Nông nghiệp và Môi trường (BNNMT)**, theo **Luật số 146/2025/QH15** sửa đổi, bổ sung một số điều của **15 luật trong lĩnh vực nông nghiệp và môi trường**, hiệu lực **01/01/2026**.
- **Cục Thú y + Cục Chăn nuôi → "Cục Chăn nuôi và Thú y"** (sáp nhập). Trong văn bản hợp nhất, cụm `"Cục Thú y"` đã được thay bằng `"Cơ quan quản lý chuyên ngành thú y trung ương"` / `"Cục Chăn nuôi và Thú y"`.
- `"nhân viên thú y cấp xã"` → `"thú y xã"`.
- **NĐ 90/2017/NĐ-CP (xử phạt VPHC lĩnh vực thú y) HẾT HIỆU LỰC 01/8/2026** → thay bằng **NĐ 204/2026/NĐ-CP (11/6/2026)**; **số điều đổi hoàn toàn** (nhãn: Đ40 → **Đ38**; hành nghề: Đ42 → **Đ40**). Đề bài hay giao số điều của NĐ 90/2017 như còn hiệu lực.

**Luật:** trước khi trích tên Bộ/Cục, tra **bản HỢP NHẤT (VBHN) mới nhất** — VBHN vừa cho số điều đã dịch chuyển, vừa cho biết cụm từ thay thế hiện hành. Tên VBHN dạng `35/VBHN-BNNMT` (2026) / `02/VBHN-BNNPTNT`. Khung đầy đủ về thuốc thú y / hóa chất khử trùng chăn nuôi (định nghĩa Đ2 kh.21/27 Luật Thú y, chuỗi NĐ 35/2016 → 80/2022 → 32/2026, TT 13/2016 với Đ8/Đ11/Đ13/Đ14/Đ27/Đ41–43, biểu phí TT 101/2020/TT-BTC, bảng chế tài NĐ 204/2026, ma trận chuẩn EN/WOAH/ISO tách **virus có vỏ vs không vỏ**, BSL-3 VN): `references/veterinary-drug-disinfectant-approval-vn.md`.

### ❌ Kết luận "văn bản còn hiệu lực" mà không mở tab Thuộc tính + Lịch sử
Đề bài giao một văn bản **không có nghĩa nó còn hiệu lực**. Trên vbpl.vn phải mở tab **"Thuộc tính"** (Tình trạng hiệu lực, Ngày hết hiệu lực) và **"Lịch sử"** (văn bản nào sửa/thay thế, từ ngày nào). Thông tin nằm ngay trên trang kết quả tìm kiếm — chỉ 1 click, bỏ qua là lãng phí và có thể làm hỏng hồ sơ.
**Đã kiểm chứng 10/2026 — NĐ 24/2024/NĐ-CP:** số hiệu đúng năm, hiệu lực 27/02/2024, thay thế NĐ 63/2014/NĐ-CP, nhưng đã bị NĐ 17/2025/NĐ-CP sửa và **hết hiệu lực toàn bộ 04/08/2025** (thay bởi **NĐ 214/2025/NĐ-CP**). Với hồ sơ có yếu tố thời điểm (thi hành dân sự, giao dịch cũ), phải tra văn bản **theo thời điểm sự kiện**. Chi tiết + JS mở tab: `references/retrieving-official-legal-texts.md`.

### ❌ Đoán `<id>` trong URL chi tiết vbpl.vn
URL dạng `.../chi-tiet/<slug>--<id>`. Đoán số ID **không báo lỗi mà âm thầm tải văn bản khác hoàn toàn** — đã kiểm chứng: đoán `--154233` trả về QĐ 11/2022/QĐ-UBND Bắc Giang thay vì Luật Đấu thầu. Dễ dẫn tới trích nhầm căn cứ pháp lý mà không hề nhận ra. Luôn lấy URL bằng cách click từ danh sách kết quả tìm kiếm.

### ❌ Tin đề bài rằng một văn bản "đã được sửa đổi" — khi số hiệu có thể không tồn tại
Khác với case "sai số hiệu" (văn bản có thật, đề bài ghi sai số), đây là case nặng hơn: **đề bài khẳng định có một văn bản sửa đổi, nhưng văn bản đó không tồn tại**. Đã kiểm chứng 10/2026: đề bài giao xác minh "NQ 85/2024/UBTVQH15 sửa Luật Đất đai" và "BLDS 2015 sửa đổi 2025, ví dụ Luật số 06/2025/QH15" — **cả hai đều không tồn tại**.

**Phương pháp phủ định nhanh (theo thứ tự hiệu quả tăng dần):**
1. **`vanban.chinhphu.vn` search → chuỗi "Không tìm thấy văn bản này"** — và nó chạy được bằng curl (`?pageid=27160&docid=&AdvancedSearch=&skey=<số hiệu>`). Chạy qua Camofox `page_text()` nếu curl không render.
   ⚠️ **BẮT BUỘC CALIBRATE TRƯỚC KHI TIN (đã kiểm chứng 10/2026).** Phép thử này trả về NOT FOUND cho **CẢ những văn bản chắc chắn tồn tại** — 31/2024/QH15, 102/2024/NĐ-CP, 151/2025/NĐ-CP đều ra "Không tìm thấy". Endpoint có thể đã đổi/sập mà không báo lỗi.
   **Luật:** chạy một số hiệu **chắc chắn tồn tại** (VD 45/2013/QH13) làm đối chứng **trước**. Nếu cả số hiệu đối chứng cũng ra NOT FOUND → endpoint hỏng, **kết luận "không tồn tại" lúc đó vô căn cứ**, phải chuyển sang vbpl.vn. Không bao giờ dùng NOT FOUND chưa calibrate làm bằng chứng phủ định trong hồ sơ.
2. **Đừng tin search engine về số hiệu.** DuckDuckGo trả về hàng loạt văn bản **cùng số hiệu nhưng khác năm** (85/2024 → dẫn tới 85/**2025**/UBTVQH15 về lập Tòa Phúc thẩm). Đây là nhiễu, không phải bằng chứng tồn tại. Luôn so **cả năm** trong số hiệu.
3. **Tìm danh mục chính thức "tất cả văn bản đã sửa Luật X" của bộ ngành.** Mạnh nhất và quyết định: Bộ NN&MT công bố **Công văn 3669/BNNMT-QLĐĐ (15/4/2026)** liệt kê toàn bộ nội dung sửa Luật Đất đai 2024 còn hiệu lực — 11 Luật + 5 Nghị quyết QH (170/2024, 171/2024, 254/2025, 248/2025, 261/2025) + 2 NQ Chính phủ. **Không có bất kỳ Nghị quyết nào của UBTVQH15** → văn bản trong đề bài không tồn tại. Bài tổng hợp trên thuvienphapluat.vn (mục "Chính sách mới") dẫn nguyên văn danh mục này.
4. **Trước khi kết luận "không tồn tại", hỏi lại đề bài vì sao có con số này.** Thường là nhầm lẫn: Luật 43/2024/QH15 (sửa LĐĐ) ↔ Nghị quyết nào khác; hoặc nhầm **hiệu lực của văn bản cũ với hiệu lực bản sửa đổi** (Luật Đất đai 2024 gốc ghi 01/8/2024 nhưng Luật 43/2024/QH15 đã kéo sang 01/01/2025).

**Sai số hiệu trong văn bản tư vấn / đơn tố cáo là hỏng hồ sơ.** Khi phát hiện đề bài sai, **nêu rõ ở đầu câu trả lời** ("2 trong 3 giả định SAI — không dùng nguyên văn vào hồ sơ"), kèm bằng chứng nguồn cho từng phần, và đề xuất cụ thể cần hỏi lại khách hàng. Không im lặng sửa trong đầu rồi trả lời như thể đề bài đúng.

### ❌ Dùng nguyên tên điều từ đề bài thay vì tên điều trong luật mới
Khi luật mới đổi tên/cấu trúc điều so với luật cũ, **phải trích nguyên văn tên điều trong luật đang có hiệu lực**. Đã kiểm chứng 10/2026: Luật Đất đai 2024 Điều 79 và Điều 80 mang tên *"phát triển kinh tế - xã hội vì lợi ích **quốc gia, công cộng**"* — **đã bỏ chữ "quốc tế"** so với Điều 74 Luật Đất đai 2013 và so với cách viết phổ biến. Trích theo đề bài là sai văn bản dù ý nghĩa gần đúng.

### ❌ Kết luận "không có quy định" mà không truy nguồn gốc con số
Khi verify một con số/quy định đồn thổi (VD: "đất dưới điện mặt trời áp mái phải tạo doanh thu 2 tỷ/năm" — KHÔNG tồn tại trong luật điện lực/đất đai): sau khi xác nhận vắng mặt trong toàn bộ khung pháp lý ngành, hãy **truy con số đó trong hệ thống pháp luật** — thường là ghép nhầm từ quy định kế cận. "2 tỷ" chính là tiêu chí **kinh tế trang trại** (TT 02/2020/TT-BNNPTNT Điều 3: chăn nuôi/thủy sản/trang trại tổng hợp ≥ 2,0 tỷ đồng/năm), không liên quan điện mặt trời. Phân loại rõ ràng: **CHÍNH THỨC vs DỰ THẢO vs TIN ĐỒN** (nghe nhầm). Chi tiết khung pháp lý điện mặt trời áp mái + đất kết hợp: `references/rooftop-solar-agrivoltaics-legal-framework.md`.

### ❌ Tin số hiệu ĐIỀU KHOẢN do đề bài đưa sẵn — phải verify TÊN điều trong toàn văn
Nguy hiểm hơn hẳn sai số hiệu văn bản: **đề bài thường đưa cả số điều lẫn tên điều, và cả hai cùng sai**,
theo nhầm sang bộ luật cũ. Session 10/2026: đề bài yêu cầu tra "Điều 134 (giao dịch bằng văn bản),
Điều 117 (HĐ mua bán BĐS), Điều 116 (công bố bán nhà), Điều 430/434 (đăng ký BĐS)" — **cả 5 đều sai**
với BLDS 2015 (91/2015/QH13). Chúng là số điều của **BLDS 2005 (23/2005/QH11)** hoặc do suy diễn.

**Quy tắc:** trước khi trích bất kỳ điều nào, mở toàn văn và **đọc TÊN điều** để xác nhận đúng nội dung.
Tên điều là thứ đáng tin; số điều là thứ phải kiểm chứng. Khi đề bài khẳng định một điều nhưng tên điều
trong luật là nội dung khác → **nêu rõ sai lệch trong output**, đừng lặng lẽ làm theo đề bài.
Bảng đối chiếu sẵn cho các bộ luật hay bị nhầm: `references/land-without-certificate-disputes.md`.

### ❌ Tin TIỀN ĐỀ KỸ THUẬT trong đề bài — không chỉ số hiệu mới có thể sai
Đề bài có thể giao kèm một **giả định khoa học/kỹ thuật hiểu ngược**. Nếu tiếp nhận và viết theo, output sẽ sai về bản chất dù mọi số hiệu đều đúng.

**Đã kiểm chứng 22/10/2026:** đề bài khẳng định *"virus có vỏ không thể thử bằng chuẩn của virus không vỏ (EN 14675 dùng bovine enterovirus – không vỏ)"* và yêu cầu giải thích hệ quả. **Thực tế ngược lại:** virus **không vỏ KHÓ diệt hơn** virus có vỏ, nên EN 14675 dùng ECBO **chính vì** nó là mẫu thử khó nhất → đạt EN 14675 thì **suy luận (read-across)** được sang virus **có vỏ** (ASFV, PEDV); và **EN 14476 CÓ nhánh virus có vỏ (Vaccinia)** nên phát biểu "không có chuẩn nào thử được virus có vỏ" là sai. Hệ quả tư vấn khác hẳn: **được** dùng surrogate + giải trình read-across, nhưng **phải ghi rõ đó là suy luận**, không được trình bày như thử trực tiếp (nếu không = công bố sai sự thật).

**Luật:** với mọi đề bài có **yếu tố kỹ thuật/khoa học** (chuẩn thí nghiệm, ngưỡng, cơ chế, phương pháp đo), **kiểm chứng tiền đề như kiểm chứng số hiệu văn bản** — tra nguồn gốc chuẩn (CEN/ISO/WOAH/EU) và đọc phạm vi thật của chuẩn. Khi phát hiện tiền đề sai: **nêu rõ ở đầu output** ("tiền đề trong đề bài hiểu ngược — đây là bản chất đúng và đây là hệ quả pháp lý khác"), kèm trích nguyên văn nguồn. Không im lặng viết theo tiền đề sai.

Ví dụ đã ghi lại: `references/veterinary-drug-disinfectant-approval-vn.md` (ma trận EN 14675 / EN 17122 / EN 14476 / EN 1656 / EN 16777 / ISO 21702 + trích nguyên văn WOAH về pH 13.4).

### ❌ Trộn "hiệu lực dân sự" với "tư cách trong hồ sơ địa chính"
Hai tầng độc lập: giao dịch có thể **có** hiệu lực dân sự giữa hai bên (Tòa án tuyên) nhưng **không**
có tư cách trong hồ sơ địa chính (cơ quan đăng ký đất đai quyết định) → không được cấp GCN, đền bù
thu hồi đất về người khác, không chuyển nhượng tiếp/thế chấp được. Khi tư vấn đất đai, **luôn tách
4 tầng** trong output: (a) hiệu lực dân sự · (b) có được công nhận trong hồ sơ địa chính không ·
(c) bên mua có quyền sử dụng pháp lý thực tế không · (d) lộ trình hợp bệ hóa. Trộn 4 tầng này là
nguyên nhân gốc của tư vấn sai, và người dùng hay đòi tách rõ khi so sánh nhiều phương án.

### ❌ Tra cứu theo SỐ HIỆU khi đang nghi ngờ số hiệu đó sai
Khi số hiệu trong đề bài **có vẻ sai**, tìm theo SỐ HIỆU là cách tìm sai nhất — nó tra ra đúng cái sai đó.
Đã kiểm chứng 10/2026: tra `03/2003/QH11` theo số hiệu trên vbpl.vn trả về **hai dòng gần trùng nhau**
(`Luật Kế toán số 03/2003/QH11` + một dòng chỉ ghi `Luật 03/2003/QH11`) → rất dễ kết luận nhầm là có Luật Đất đai 2003.
Tra theo **TIÊU ĐỀ** (`Luật Đất đai`) mới lộ ra đúng: **13/2003/QH11, ban hành 26/11/2003, hiệu lực 01/07/2004, hết hiệu lực 01/07/2014**.

**Luật:** nghi ngờ số hiệu → **tìm theo TIÊU ĐỀ, đọc TÊN + ngày ban hành/hiệu lực/hết hiệu lực ngay trên danh sách kết quả**. Một lần search ra cả chuỗi pháp lý (LĐĐ 1980/1993 → 13/2003 → 45/2013 → 31/2024) mà không cần mở từng tab Thuộc tính.

### ❌ Giả định dự án của tư nhân luôn có thể bị thu hồi đất bắt buộc
Với dự án do **doanh nghiệp tư nhân** làm chủ đầu tư, phải tra điều kiện thu hồi của **đúng thời điểm sự kiện** trước khi kết luận "thiếu quyết định thu hồi đất ⇒ xây trái phép".
Đã kiểm chứng: **LĐĐ 2003 Điều 40 khoản 2** — dự án SXKD của nhà đầu tư chỉ được nhận chuyển nhượng/thuê/ góp vốn bằng QSDĐ; *"Trường hợp nhà đầu tư tự thỏa thuận để nhận quyền sử dụng đất thì **không phải thực hiện thủ tục Nhà nước không thực hiện việc thu hồi đất, giao đất, cho thuê đất**"*. Nhà nước chỉ thu hồi cho dự án thuộc khoản 1 Điều 40 (KCN/CCN/KKT/**dự án đầu tư lớn theo quy định của Chính phủ**).
→ Cách làm "DN ký trực tiếp với hộ dân, trả tiền" năm 2005 **có thể là cách làm ĐÚNG thời điểm đó**. Với LĐĐ 2024, Điều 80 khoản 1 siết lại (bắt buộc có trong KHSDĐ huyện / QĐ đầu tư công / QĐ chấp thuận CSTĐT theo điểm a, b, c).
**Trước khi kết luận thiếu văn bản, luôn hỏi: dự án có thuộc danh mục được thu hồi bắt buộc không?** Chi tiết: `references/land-law-2003-era-thu-hoi-dat.md`.

### ❌ Để con số từ đề bài lọt vào văn bản giao cho khách — phải có gate chặn TRƯỚC khi viết
Đây là sai lầm **nguy hiểm nhất trong toàn bộ pipeline**, vì nó im lặng: văn bản trông đầy căn cứ pháp lý nhưng số hiệu bịa đặt → hỏng hồ sơ, mất uy tín, có thể làm hại lợi ích khách hàng.

Đã kiểm chứng 10/2026, vụ đất đai Thanh Quang: trong **một phiên** em đoán sai **3 số hiệu văn bản** (`NQ 85/2024/UBTVQH15` không tồn tại, `Luật 06/2025/QH15` không tồn tại, `Luật Đấu thầu 43/2023/QH15` thật ra là `22/2023/QH15`) và **5 số điều BLDS** (134/117/116/142-143/430-434 — toàn bộ là số điều của BLDS **2005** chứ không phải 2015). Tất cả đều "nghe rất đúng" và đều sai.

**Nguyên nhân gốc:** đề bài giao sẵn con số → đọc lại vài lần thấy quen → tin là đúng. Càng tra cứu kỹ thì càng dễ tin số đã cho, vì nó trông chuyên nghiệp.

**Bắt buộc — 4 bước trước khi viết bất kỳ văn bản nào cho khách:**
1. **Mọi số hiệu văn bản** → tra KB hoặc nguồn gốc. Không dùng số đang có trong đề bài làm căn cứ.
2. **Mọi số điều** → mở toàn văn, đọc **TÊN điều** để xác nhận đúng nội dung (xem pitfall "Tin số hiệu ĐIỀU KHOẢN").
3. **Ngày hiệu lực** → xác minh bằng tab Thuộc tính + Lịch sử, không suy từ năm ban hành.
4. **Chạy gate** → script kiểm tra citation (đủ số hiệu/điều/khoản + còn hiệu lực). Exit 1 = chặn, phải sửa.

**Không viết văn bản cho khách mà chưa chạy gate.** "Chạy cho có" thì không có tác dụng — phải thật sự chặn được và sửa theo kết quả.

**Khi phát hiện mình đã sai số liệu:** nêu rõ ở đầu output cho khách thấy, kèm bảng đối chiếu sai/đúng, và giải thích vì sao lỗi xảy ra. Không im lặng sửa trong đầu rồi trả lời như thể đề bài đúng. Khách hàng cần biết em đã kiểm chứng được cái gì và chưa kiểm chứng được cái gì.

### ❌ Chỉ tra luật hiện hành rồi áp ngược cho sự kiện quá khứ
Áp luật hiện hành cho một hành vi đã xảy ra 10-20 năm trước là **nguồn kết luận sai phổ biến nhất** trong tư vấn pháp lý, vì luật hiện hành luôn "có vẻ" chặt chẽ hơn và ta vô thức áp nó.

Đã kiểm chứng 10/2026: kết luận "công ty không có quyền sử dụng đất" dựa trên LĐĐ 2024 → **ngược hoàn toàn** khi tra LĐĐ 2003 (Điều 40 khoản 2 cho phép nhà đầu tư tư nhân **tự thỏa thuận**, không cần quyết định thu hồi).

**Bắt buộc với mọi vụ có sự kiện quá khứ (> 3 năm):**
- Xác định **năm sự kiện**
- Tra luật **có hiệu lực năm đó**, không chỉ luật hiện hành
- **Tách từng giai đoạn:** hành vi đã hoàn thành → luật tại thời điểm đó (khoản 1 Điều 156 BLDS: *"quy định của luật không có hiệu lực đối với các việc đã hoàn thành theo quy định của pháp luật trước khi luật đó có hiệu lực"*) · tranh chấp/tố tục hiện nay → luật hiện hành · vụ đã có QĐ trước khi luật mới có hiệu lực nhưng chưa xong → điều khoản chuyển tiếp (VD Điều 254 LĐĐ 2024)
- **Số điều khác nhau giữa các bộ luật cùng tên.** Điều 134 BLDS 2005 = "Giao dịch dân sự bằng văn bản"; Điều 134 BLDS 2015 = **"Đại diện"**. Tra đúng bộ luật theo thời điểm, đừng dùng số điều đã học ở bộ luật khác.
- Kiểm tra **điều kiện kèm theo** của lập luận. Điều 40 khoản 2 LĐĐ 2003 chỉ hợp lệ nếu dự án *"phù hợp với quy hoạch sử dụng đất đã được xét duyệt"* — nếu không có quy hoạch thì lập luận sập dù điều luật đúng.

**Nêu rõ trong output:** phần nào áp luật nào, vì sao. Người đọc phải thấy được ranh giới thời điểm.

### ❌ Khuyên khách hàng đổi cách diễn đạt trong văn bản khi chưa đọc bản gốc
Đã kiểm chứng 10/2026: tờ giấy thật ghi khoản tiền là **"bồi thường"**. Em khuyên khách hàng đổi thành *"tiền mua/chuyển nhượng quyền sử dụng đất"* với lý do hợp lý về mặt kỹ thuật — nhưng **sai hoàn toàn**: tờ ghi "bồi thường" nghĩa là có phương án bồi thường của cơ quan nhà nước, đó là điểm **thuận lợi**.

**Lập luận phải bám theo từ ngữ thực tế trên giấy tờ, không theo cách gọi mình muốn.** Trước khi khuyên đổi cách diễn đạt: đọc bản gốc. Nếu không có bản gốc thì ghi vào mục "chưa xác minh" và hỏi khách hàng.

Phân biệt 3 loại vì có 3 căn cứ khác nhau: giao dịch dân sự tự nguyện (*mua bán*) · bồi thường theo phương án của cơ quan nhà nước (*bồi thường*) · Nhà nước giao đất quỹ công (*giao đất/cho thuê đất*).

Chi tiết + công thức tìm **nghịch lý tự mâu thuẫn trong tài liệu của đối phương** (loại vũ khí miễn phí mạnh nhất) + checklist đọc tờ giấy cũ: `references/adversarial-document-analysis.md`.

### ❌ Đồng ý làm văn bản không đủ căn cứ khi làm sẽ rủi ro cho chính khách hàng
Khách hàng có thể yêu cầu văn bản mà **tốt cho họ nếu làm đúng, nhưng rủi ro nếu làm sai**. Khi đó phải nói thẳng và làm bản thay thế, không im lặng làm khác đi yêu cầu.

Đã kiểm chứng 10/2026: khách yêu cầu **đơn tố cáo công an tội giả chữ ký**. Không làm, vì (1) tội hình sự đòi hỏi chứng minh chữ ký là giả — chưa có bằng chứng, xác minh sau 20 năm gần như không thể; (2) **người tố cáo sai có thể bị xử**, mà người ký bị nghi giả chính là khách hàng; (3) có bước đúng thay thế: **đơn kiến nghị xác minh hồ sơ** gửi cơ quan nhà nước — lấy được hồ sơ thật có giá trị chứng minh, không rủi ro.

**Quy tắc:** văn bản thiếu căn cứ mà làm sẽ rủi ro cho chính khách hàng → làm bản thay thế an toàn hơn, **ghi rõ lý do trong chính văn bản**, và nói thẳng với khách hàng kèm điều kiện cần có để làm văn bản họ muốn sau này.

Nêu rõ trong văn bản thay thế rằng nó **chỉ đề nghị xác minh/cung cấp hồ sơ**, chưa khởi kiện, chưa khiếu nại — giúp cơ quan nhận đơn xử lý đúng phạm vi thẩm quyền.

### ❌ Dùng curl/lite.duckduckgo trong script để search khi đã gọi nhiều lần
DDG trả CAPTCHA sau ~3 request; Bing HTML không parse được bằng regex (`b_algo` không khớp) → 0 kết quả.
Khi cần search trong lúc làm việc, dùng `browser_navigate` tới `https://lite.duckduckgo.com/lite/?q=...`
rồi đọc snapshot. Nguồn tra cứu + script tải toàn văn: `references/fetching-full-legal-texts.md`.

### ❌ Tra cứu Wikipedia tiếng Việt quá kỳ vọng
Wikipedia tiếng Việt có nội dung hạn chế về chi tiết văn bản pháp luật. Chỉ dùng để xác định **khung pháp lý tổng thể** và **luật chính**, sau đó bổ sung từ kiến thức luật sư hoặc các nguồn khác.

---

## Persona: Head-of-Legal (agent persona qua config, không phải skill mode)

Khi user yêu cầu tư vấn theo phong cách **General Counsel / Head of Legal** (định dạng 4 mục [I-IV], giọng quyết định, "hành lang pháp lý"), persona này được activate qua **config**:

```
hermes config set display.personality head_of_legal
```

Personality dictionary nằm ở `config.yaml` ~line 49 (`personalities:`). Key activate là `display.personality`. **KHÔNG phải skill mode** — user đã clarify (03/10/2026).

**Nguyên văn personality:** `../legal-firm-vn/references/personality-head-of-legal.md` (không tóm tắt).

**Khi persona này active, áp dụng guardrail:**
- **G1** — Phần **ĐIỂM MÙ PHÁP LÝ** (≥3 điểm) là điều kiện output. Không được nói "không có điểm mù pháp lý".
- **G2** — Không ảo giác = dùng KB + QA Gate. Mọi số hiệu phải `legal_kb.py check` trước.
- **G3** — Option 2 (vùng xám) phải gắn **GAP-4: CẦN NGƯỜI** + defense strategy.
- **G4** — Phần **TỰ PHẢN BIỆN** phải hiển ra, không ngầm.
- **G5** — Số hiệu phải verify qua KB trước. Không nhớ số để viết ra.

> Persona này **bổ trợ** workflow 4 bước hiện có. Không thay thế. Khi persona không active, dùng workflow mặc định.

## Linked References

- 📄 `../legal-firm-vn/references/personality-head-of-legal.md` — Personality nguyên văn (nạp 03/10/2026)

- 📄 `references/adversarial-document-analysis.md` — **Phân tích tài liệu đối kháng & khi nào từ chối làm văn bản khách yêu cầu** (10/2026, vụ tranh chấp đất đai ký 2005): từ ngữ trên giấy tờ quyết định bản chất căn cứ ("bồi thường" ≠ "mua/chuyển nhượng" — sai lầm đã mắc phải khi khuyên khách đổi từ ngữ mà chưa đọc bản gốc); **công thức tìm nghịch lý tự mâu thuẫn trong chính tài liệu của đối phương** (họ nói "chữ ký giả" nhưng tờ bị nghi giả ghi "đã nhận đủ tiền" → phủ nhận tiền = phủ nhận tờ giấy); "có chữ ký + con dấu" ≠ "có quyền pháp lý" (tờ 6 cơ quan ký ≠ Quyết định thu hồi đất — tách 2 loại giá trị); bẫy Điều 79 kh.3 LĐĐ 2024 ("nhà máy nước" = cấp nước sinh hoạt, KHÔNG phải nước khoáng tư nhân); bảng thẩm quyền thu hồi đất theo cả LĐĐ 2024 & 2003; quy tắc khi khách yêu cầu văn bản thiếu căn cứ mà làm sẽ rủi ro cho chính họ → làm bản thay thế, nói thẳng, ghi lý do trong văn bản; checklist đọc tờ giấy cũ không có bản gốc.

- 📄 `references/fetching-full-legal-texts.md` — **Recipe tải toàn văn luật để trích nguyên văn** (10/2026): `hethongphapluat.com/<slug>` = 1 request ra **toàn văn** bộ luật, không Cloudflare (thuvienphapluat.vn 403 cả desktop lẫn mobile UA; vbpl.vn search là Next.js SPA không có dữ liệu trong HTML). Kèm quy tắc "mỗi điều xuất hiện 2 lần — lần 2 mới là thân điều" và bảng nguồn dự phòng. Script: `scripts/fetch_legal_text.py`.
- 📄 `references/land-without-certificate-disputes.md` — **Tranh chấp đất không có sổ đỏ giữa hộ dân và doanh nghiệp** (10/2026): bảng đối chiếu 5 số điều đề bài hay sai (Điều 134/117/116/142-143/430-434 của BLDS **2015** khác hẳn BLDS 2005); khung 2 tầng hiệu lực dân sự vs hồ sơ địa chính; **Điều 129 kh.2 BLDS** (Tòa công nhận hiệu lực + miễn công chứng khi đã thực hiện ≥2/3 nghĩa vụ) = lá chắn bên mua; **Điều 168 + 184** (suy đoán chiếm hữu ngay tình, gánh nghĩa chứng minh đảo ngược); LĐĐ 2024 Điều 131/132/133/137/138 (đường mở GCN cho đất không giấy tờ, điều kiện UBND cấp xã xác nhận không tranh chấp); lộ trình 5 bước. Có ghi rõ các khoảng trống chưa verify (NĐ 13/2021, án lệ, Điều 28, Luật Công chứng) — tra lại trước khi dẫn.
- 📄 `references/capital-contribution-confirmation.md` — **Giấy xác nhận đã nhận đủ tiền góp vốn** cho công ty cổ phần/TNHH: cấu trúc văn bản, mapping field từ CCCD, căn cứ pháp lý (Luật Doanh nghiệp 2020), workflow OCR CCCD → sinh .docx template.
- 📄 `references/retrieving-official-legal-texts.md` — Workflow tra cứu & lấy **toàn văn chính thức** văn bản QCVN/TCVN/Thông tư/Nghị định qua vbpl.vn (CSDL quốc gia, Bộ Tư pháp): cách tìm theo tiêu đề, click tiêu đề React SPA, mở tab "Văn bản gốc", đọc file snapshot đầy đủ. **Kèm mục "Xác minh HIỆU LỰC THẬT" — 2 tab bắt buộc (Thuộc tính + Lịch sử)**: tìm ra văn bản đã bị sửa/thay thế và ngày hết hiệu lực (case NĐ 24/2024 → hết hiệu lực 04/08/2025, thay bởi NĐ 214/2025/NĐ-CP); mẹo cross-validate số hiệu Luật qua phần "Căn cứ" của văn bản hướng dẫn. Cùng các pitfall (Cloudflare thuvienphapluat, redirect luatvietnam, không đoán `<id>` trong URL). Đã kiểm chứng với QCVN 6-1:2010/BYT và bộ luật đấu thầu 10/2026.
- 📄 `references/land-law-2003-era-thu-hoi-dat.md` — **Luật Đất đai 2003 (13/2003/QH11) — chuỗi pháp lý cho sự kiện năm 2005** (kiểm chứng 10/2026, toàn văn 148 điều): **⚠️ ba số hiệu sai kinh điển** (`03/2003/QH11` là **Luật Kế toán**, không phải Luật Đất đai; `NĐ 22/2003/NĐ-CP` là **Thể dục Thể thao**; `TT 10/2008/TT-BTC` **không tồn tại**); **Điều 44** thẩm quyền thu hồi (UBND tỉnh / UBND huyện — **cấp xã chỉ cho thuê đất thuộc quỹ đất công ích**, Điều 37 kh.3, cấm ủy quyền kh.4); **Điều 40 khoản 2 — nhà đầu tư tư nhân chỉ được TỰ THỎA THUẬN, "không phải thực hiện thủ tục Nhà nước không thực hiện việc thu hồi đất, giao đất, cho thuê đất"** → có thể giải thích tại sao cách làm năm 2005 ĐÚNG thời điểm đó (đừng vội kết luận "xây trái phép"); Điều 42 + cảnh báo **đừng gọi tiền mua dân sự là "bồi thường"**. Kèm 3 bài học workflow: tìm theo **Tiêu đề** chứ không theo số hiệu; phép phủ định `vanban.chinhphu.vn` phải **calibrate bằng số hiệu chắc chắn tồn tại** trước; lấy URL LuatVietnam từ DOM search rồi curl.
- 📄 `references/land-law-2024-land-acquisition.md` — **Luật Đất đai 2024 (31/2024/QH15) — toàn bộ khung thu hồi đất đã verify toàn văn** (260 điều, 10/2026): ⚠️ **hiệu lực 01/01/2025 chứ không phải 01/8/2024** (Điều 252 kh.1 đã bị Luật 43/2024/QH15 kéo dài); tên Điều 79/80 là *"lợi ích quốc gia, công cộng"* (đã bỏ "quốc tế"); điều kiện bắt buộc Điều 80 kh.1–4; bồi thường Điều 91–111; khiếu nại **Điều 237**; **Điều 254 chuyển tiếp — 6 khoản, điểm phân nhánh cho vụ thu hồi đất TRƯỚC ngày luật có hiệu lực nhưng chưa xong**; danh mục văn bản sửa LĐĐ của Bộ NN&MT (Công văn 3669/BNNMT-QLĐĐ 15/4/2026); **2 giả định sai đã bác bỏ** (NQ 85/2024/UBTVQH15 không tồn tại; BLDS 2015 chưa hề bị sửa, `06/2025/QH15` không tồn tại, Điều 134/135/141 nguyên trạng). Kèm workflow curl LuatVietnam vs JS-rendered, gzip gotcha.
- 📄 `references/food-safety-phu-gia-tpbvsk.md` — Khung pháp lý về **phụ gia thực phẩm & TPBVSK**: TT 24/2019/TT-BYT = danh mục phụ gia (Phụ lục 1, ML 2A/2B, GMP 3), E500/E501 có trong danh mục, các thông tư sửa đổi (17/2023, 08/2024); NĐ 15/2018/NĐ-CP (tự công bố, đăng ký bản công bố, GMP TPBVSK); NĐ 43/2017/NĐ-CP ghi nhãn; TT 43/2014/TT-BYT **đã hết hiệu lực**. Kèm mẹo tra cứu (lite.duckduckgo > Google/Bing khi bị chặn; luatminhkhue, vfa.gov.vn mở được bằng curl).
- 📄 `references/rare-earth-mining-medical-regulation.md` — Case study: Phân tích pháp lý khai thác đất hiếm và ứng dụng y học tại Việt Nam. Minh họa workflow 4 bước cho vấn đề đa luật, đa cơ quan cấp phép.
- 📄 `references/feed-supplement-legal-compliance.md` — **Thức ăn bổ sung chăn nuôi (TACN bổ sung)** — khung pháp lý áp dụng: Luật ATTP 2024 (98/2024/QH15), Luật Chăn nuôi 32/2018/QH14, Luật Thú y 79/2015/QH13, **NĐ 13/2020/NĐ-CP (sđ 46/2022 + 32/2026) Điều 8a/8b**, **NQ 66.19/2026/NQ-CP (18/5/2026) — DỪNG 4 TTHC công bố TĂBS → tự công bố trên Cổng TTĐT Bộ NN&MT**, Thông tư 13/2020/TT-BNNPTNT, NĐ 43/2017/NĐ-CP (ghi nhãn). ⚡ **Mục "TRẠNG THÁI HIỆN HÀNH" ở đầu file** ghi rõ cơ chế công bố đã đổi 2 lần trong 2026 (NĐ 32/2026 thêm thẩm định UBND cấp tỉnh → NQ 66.19/2026 dừng, chuyển tự công bố) + hồ sơ tối thiểu + nguồn chốt (cucthuy.gov.vn, Công văn 1805/CNTY-TACN&TTY). ⚠️ **Bẫy `13/2020/NĐ-CP` ≠ `13/2020/TT-BNNPTNT`** (Nghị định chăn nuôi vs Thông tư TACN) và **NĐ 15/2018/TPBVSK KHÔNG áp cho TACN**. **Cấm claim:** phòng/chữa bệnh, tăng đề kháng, giảm kháng sinh, "hỗ trợ điều trị" — chỉ được ghi công dụng theo sheet đăng ký. Rủi ro: xử phạt, thu hồi, mất GCN lưu hành. Kết hợp với `legal-contract-review-vn` khi rà soát hợp đồng trial.
- 📄 `references/veterinary-drug-disinfectant-approval-vn.md` — **Thuốc thú y / hóa chất khử trùng chuồng trại: đường pháp lý + chuẩn thí nghiệm** (kiểm chứng toàn văn 22/10/2026). **Ba đường sống** (TĂBS/TPBVSK ❌ không claim được · **hóa chất khử trùng-tiêu độc môi trường chăn nuôi = THUỐC THÚ Y ✅ đường đúng** · sát trùng trực tiếp cho heo = rủi ro tồn dư cao nhất); **Đ2 kh.27 Luật Thú y 2015** là câu quyết định ("khử trùng, tiêu độc môi trường chăn nuôi"); chuỗi **NĐ 35/2016 (Đ19/Đ20) → NĐ 123/2018 (kh.5 Đ2) → NĐ 80/2022 (KHÔNG phải 106/2021) → NĐ 32/2026**; **TT 13/2016/TT-BNNPTNT (VBHN `35/VBHN-BNNMT` 2026)** đủ số điều — Đ8 (thời hạn **4 tháng**/30 ngày, GCN **5 năm**), **Đ11 kh.1 MIỄN KHẢO NGHIỆM** (đòn bẩy lớn nhất), Đ13 (**chỉ tiêu hiệu lực luật VN theo hướng ĐỘNG VẬT" — vô nghĩa với hóa chất bề mặt, phải dùng cửa Đ13 kh.3**), Đ14 (lợn ≥40 con), Đ27 kh.1.d (dư lượng/thời gian ngừng sử dụng trên nhãn), **Đ41 kh.3 + Đ42–43 quảng cáo phải được cấp tỉnh xác nhận, 5 ngày làm việc**; **TT 101/2020/TT-BTC** bảng phí thật (ĐKLH mới 1.350.000đ, **bổ sung chỉ định 450.000đ**, quảng cáo 900.000đ — *phí nhà nước chỉ vài triệu, biến số là chi phí lab*); **bảng chế tài NĐ 204/2026/NĐ-CP** (thay NĐ 90/2017 từ 01/8/2026) — nhãn **Đ38** 4–6tr, bán không GCN **Đ34 kh.3** 10–15tr/loại, khảo nghiệm không phép **Đ26 kh.3** 5–6tr, tổ chức **×2** (Đ5); **ma trận chuẩn**: EN 14675 (ECBO, **không vỏ** — nên đạt ⇒ suy luận read-across cho virus **có vỏ**, NHƯNG đó là suy luận không phải thử trực tiếp) · **EN 17122** (bề mặt, PPV — sát nhất với "bề mặt chuồng trại") · **EN 14476 CÓ nhánh Vaccinia (có vỏ)** nhưng thuộc **Y TẾ** nên không thay thế hồ sơ thú y · EN 1656 chỉ diệt khuẩn ❌ · EN 16777 ❌ sai khu vực · ISO 21702 ❌ cho vật liệu không phải dung dịch · **VN CHƯA có TCVN/QCVN thử hiệu lực diệt virus**; 🔴 **WOAH ASF card: ASFV bất hoạt ở pH <3.9 / >11.5 nhưng "at pH 13.4 – resistance lasts up to 21 hours without serum, and 7 days with serum"** → thử sạch là vô nghĩa, phải thử **có chất hữu cơ + 4 °C** và **đo giảm log10 hiệu giá LÂY NHIỄM, không dùng qPCR**; **ASF = mục 1.9 Phụ lục 01 TT 07/2016** (bổ sung bởi **kh.2 Đ1 TT 24/2019/TT-BNNPTNT**), **PED không có tên trong cả 3 danh mục**, **KHÔNG tồn tại "Danh mục bệnh phải báo cáo"** (Đ19 kh.1 áp cho mọi bệnh truyền nhiễm); **BSL-3 VN** (TT Chẩn đoán TY TW · Phòng KN thuốc TY quốc gia – Viện CNSH · PTN trọng điểm CNSH Thú y VNUA) + `[cần xác minh]` cho FIVELAB/Chi cục vùng/Viện Thú y/NAVETCO; lộ trình 10 bước + mẫu công văn hỏi Cục Chăn nuôi và Thú y **trước khi chi tiền thử nghiệm**.
- 📄 `references/rooftop-solar-agrivoltaics-legal-framework.md` — **Điện mặt trời áp mái & đất nông nghiệp kết hợp năng lượng** (đã kiểm chứng văn bản gốc 09/2026): Luật Điện lực 2024 (61/2024/QH15) Điều 20/22/30/33; NĐ 135/2024/NĐ-CP (điều kiện, công suất, thông báo/đăng ký, miễn GPHĐĐL, hợp đồng 5 năm); NĐ 57+58/2025 + NĐ 243/2026 (bán điện dư ≤50%, thỏa thuận >50% tới 31/12/2030, giá điện năng thị trường bình quân năm trước); đất dưới tấm pin (Điều 218 LĐĐ 2024 + Điều 99 NĐ 102/2024/NĐ-CP: ≤50% diện tích, UBND tỉnh phê duyệt phương án, "điện mặt trời" nộp tiền thuê đất hằng năm); nguồn gốc tin đồn "2 tỷ doanh thu" = tiêu chí kinh tế trang trại TT 02/2020/TT-BNNPTNT.
- 📄 `references/qcvn-62-2025-nuoc-thai-chan-nuoi.md` — **QCVN 62:2025/BTNMT nước thải chăn nuôi** (đã kiểm chứng 08/09/2026, đối chiếu chéo 3 nguồn khớp 100%): TT 04/2025/TT-BTNMT 28/02/2025, hiệu lực 01/09/2025, thay thế 62-MT:2016; Bảng 1 **3 cột A/B/C** phân theo chức năng nguồn tiếp nhận (QCVN 08:2023, không theo lưu lượng), T-P chia 3 loại nguồn (hồ/sông/biển), cho phép chọn COD hoặc TOC, không có dòng riêng NH4+/NH3; workflow curl+DDG+pymupdf và xử lý Cloudflare thuvienphapluat.vn.
- 📄 `references/qcvn-40-2025-nuoc-thai-cong-nghiep.md` — **QCVN 40:2025/BTNMT nước thải công nghiệp** (18/10/2026): TT **06/2025/TT-BTNMT** 28/02/2025, hiệu lực **01/9/2025**; **gộp 5 quy chuẩn về một** (QCVN 40:2011 + 25:2009 bãi chôn lấp + 28:2010 y tế + 29:2010 kho xăng dầu + 52:2017 thép); lộ trình chuyển tiếp **đến hết 31/12/2031, bắt buộc từ 01/01/2032**, chưa xác định phân vùng → áp Cột B; **3 cột A/B/C × 2 ngưỡng lưu lượng** (F ≤ / > 2.000 m³/ngày) cho BOD5/COD/TOC/TSS; Bảng 2 đầy đủ thông số đặc trưng theo loại hình SXKD (kim loại, CN⁻, phenol, BVTV, VOC, PCB, dioxin, AOX) + Phụ lục mã ngành QĐ 27/2018/QĐ-TTg; **cảnh báo mức kiểm chứng** (bảng giới hạn lấy từ bản reproduction tư nhân → phải đối chiếu vbpl.vn "Văn bản gốc" trước khi dùng cho hồ sơ) và pitfall tải PDF chậm (dùng `web_extract`, không `curl`) / thuvienphapluat 403 với bot.

## Tham khảo

- [Luật Khoáng sản 2010 (60/2010/QH12)](https://thuvienphapluat.vn/van-ban/Tai-nguyen-Moi-truong/Luat-khoang-san-2010-113808.aspx)
- [Luật Dược 2016 (105/2016/QH13)](https://thuvienphapluat.vn/van-ban/The-thao-Y-te/Luat-duoc-2016-105-2016-QH13-321842.aspx)
- [Luật Đầu tư 2020 (61/2020/QH14)](https://thuvienphapluat.vn/van-ban/Dau-tu/Luat-Dau-tu-2020-61-2020-QH14-424097.aspx)
- [Luật Bảo vệ Môi trường 2020 (72/2020/QH14)](https://thuvienphapluat.vn/van-ban/Tai-nguyen-Moi-truong/Luat-Bao-ve-moi-truong-2020-431147.aspx)
- [Luật An toàn bức xạ và Hạt nhân 2008 (18/2008/QH12)](https://thuvienphapluat.vn/van-ban/Cong-nghe-thong-tin/Luat-an-toan-buc-xa-hat-nhan-2008-18-2008-QH12-82920.aspx)
