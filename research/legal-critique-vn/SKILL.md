---
name: legal-critique-vn
description: "Use when: critiquing a VN law, case, or argument."
version: 1.0.0
author: Nguyễn Thành Quang / Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [legal, vietnam, critique, self-critique, gap-hunt, adversarial, risk]
    category: research
    related_skills: [legal-firm-vn, legal-contract-review-vn, vietnam-legal-advisory]
---

# Legal Critique VN — Phản biện luật & case

Skill này trả lời **2 câu hỏi** anh đặt ra:

1. Luật này / case này có vấn đề không? Hình hưởng đến ai, mức độ ra sao?
2. Trong luật có lỗ hổng nào đi được hợp pháp không? Rủi ro của mỗi hành lang?

**Đây là Pha 6 của `legal-firm-vn`.** Pha này bắt buộc, không output nào bỏ qua.

---

## Nguyên lý: phản biện không phải phần trang trí

Phản biện là **điều kiện để kết luận đáng tin**, không phải đoạn kết thêm cho có.

Luật sư giỏi và LLM khác nhau ở đúng một chỗ: **luật sư biết tự tìm lỗi trong lập luận của chính mình trước khi khách hỏi**. Nếu output của anh không tự nói ra điểm yếu của mình thì khách sẽ hỏi — và lúc đó mất uy tín.

---

## Cấu trúc output — 6 phần, đúng thứ tự

### Phần 1 — Bản chất vấn đề

- Văn bản / case này thuộc lĩnh vực nào, điều chỉnh cái gì
- Ai chịu ảnh hưởng trực tiếp, ai gián tiếp
- Đây là **điểm khoảng** luật hay điểm cụ thể

Nêu số hiệu và điều khoản cụ thể, đã chạy qua `legal_kb.py check` ở Pha 2.

### Phần 2 — Vấn đề luật (có hay không)

**4 mức đánh giá, phải chọn 1:**

| Mức | Dấu hiệu | Ví dụ |
|------|-----------|-------|
| **Không có vấn đề** | Văn bản rõ, nhất quán, có hướng dẫn | TT ghi rõ liều, đo được, kiểm chứng được |
| **Khoảng trống kỹ thuật** | Luật đúng nhưng thiếu chỉ tiêu đo lường | "Xử lý nước thải đạt chuẩn" mà không có QCVN cho loại nước đó |
| **Xung đột / chồng lấn** | Hai văn bản cùng điều chỉnh, yêu cầu xung đột | NĐ yêu cầu A, TT yêu cầu B không thể đồng thời |
| **Lỗi kỹ thuật thật** | Văn bản viết sai, mâu thuẫn nội tại, không dùng được | Cùng một khái niệm định nghĩa 2 khác nhau trong 2 điều |

Với mỗi vấn đề tìm thấy, chỉ ra **cơ chế** gây ra:
- Do không có hướng dẫn dưới?
- Do mâu thuẫn giữa 2 văn bản?
- Do điều khoản viết chung chung đến mức không dùng được?
- Do lịch sử sửa đổi chưa cập nhật?

### Phần 3 — Mức ảnh hưởng

Với mỗi vấn đề:

| Chiều | Câu hỏi |
|-------|---------|
| **Ai chịu** | Doanh nghiệp / người dân / cơ quan quản lý / tất cả |
| **Trong tầm tay** | Xử lý được trong phạm vi doanh nghiệp không, hay phải chờ văn bản dưới |
| **Chi phí** | Nếu phải thích nghi — bao nhiêu, đo bằng gì |
| **Thời gian** | Xử lý ngay, hay kho 3-6 tháng, hay kho không giải quyết được |
| **Mức chắc chắn** | Chắc / khá chắc / suy đoán — nói thẳng mức nào |

Bắt buộc dùng tag mức chắc chắn. "Vấn đề này chắc chắn ảnh hưởng" là cách nói của người không biết.

### Phần 4 — Bốn loại kẽ hở (bắt buộc đủ 4)

Đây là phần **giá trị nhất** của skill. Phải phân loại rõ, không trộn.

| Loại | Đặc điểm | Hành lang | Khai báo |
|------|-----------|----------|---------|
| **GAP-1 · Khoảng trống luật** | Luật không điều chỉnh trường hợp X | Đi hành lang hợp pháp hiện có | `GAP-1: AN TOÀN` |
| **GAP-2 · Chưa có hướng dẫn** | Luật có, NĐ/TT chưa ban hành chi tiết | Tự xác định tiêu chuẩn, cứu hồ sơ trước, ghi rõ lý do | `GAP-2: LÀM ĐƯỢC` |
| **GAP-3 · Thiếu quy chuẩn kỹ thuật** | Có luật, chưa có QCVN/TCVN | Đề xuất ban hành, tự công bố trong khoảng trống | `GAP-3: LÀM ĐƯỢC` |
| **GAP-4 · Đại lý hiểu sai** | Văn bản nghĩa A, thực tế áp dụng B | **NGUY HIỂM** — dừng, cần luật sư người xác nhận | `GAP-4: CẦN NGƯỜI` |

**Loại 4 bắt buộc hiện dạng callout đỏ**, không được để lọt xuống footnote. Đây là loại lỗi không cố ý mà vẫn phạt, và là loại đáng tin nhất khi người tư vấn không nói ra.

Với mỗi GAP tìm được, phải ghi rõ:
- Chỗ nào trong luật (điều/khoản)
- Ai có thể khai thác
- Nếu khai thác sai thì hậu quả

### Phần 5 — Giải pháp + phản biện giải pháp

Với mỗi kẽ hở, đưa **2-3 phương án**, mỗi phương án có:

| | Phương án A | Phương án B |
|---|---|---|
| Cách làm | | |
| Thời gian | | |
| Chi phí | | |
| Rủi ro | | |
| Điều kiện để chọn | | |

Sau đó **phản biện chính các phương án đã đưa ra**:
- Phương án nào yếu nhất, tại sao
- Nếu đối phương (cơ quan quản lý / bên kia) phản biện thì đứng vững không
- Điều gì có thể khiến cả phương án tốt nhất sập

### Phần 6 — Tự phản biện (bắt buộc)

Đây là phần **QA Gate chặn**. Skill `legal_qa_gate.py` với mode `critique` sẽ FAIL nếu thiếu phần này.

Phải có ít nhất 3 trong 4 dạng:

1. **Rủi ro của chính lập luận** — "Tôi phân tích X dựa trên giả định Y. Nếu Y sai thì toàn bộ kết luận đổi."
2. **Đối thủ phản biện thế nào** — "Cơ quan quản lý có thể lập luận ngược lại rằng..."
3. **Nếu bên kia không chịu** — "Trường hợp đối tác không chịu sửa điều khoản thì phương án dự phòng là..."
4. **Phạm vi giới hạn của phân tích** — "Tôi chưa tra cập nhật văn bản sau ngày X, vì vậy..."

Sau phần 6, chốt bằng câu:
> "Đã check đến [ngày] với các văn bản liệt kê. Văn bản sửa đổi sau ngày đó có thể tạo rủi ro mới."

Không dùng "đảm bảo hợp pháp" / "không vi phạm" ở bất kỳ đâu.

---

## Workflow

```
1. Xác định văn bản / case, chạy legal_kb.py check
2. Phần 1 — bản chất
3. Phần 2 — có vấn đề không (4 mức)
4. Phần 3 — mức ảnh hưởng (có tag chắc chắn)
5. Phần 4 — đủ 4 loại GAP, loại 4 callout đỏ
6. Phần 5 — 2-3 phương án + phản biện phương án
7. Phần 6 — tự phản biện (>= 3/4 dạng)
8. Chạy legal_qa_gate.py --mode critique
9. Publish
```

---

## Pitfalls

1. **Bỏ phần 6** — QA Gate chặn, và đây là lý do skill này tồn tại.
2. **Trộn GAP-2 với GAP-4** — nghe giống nhau nhưng hậu quả ngược nhau. GAP-2 làm được, GAP-4 là bẫy.
3. **Viết "chắc chắn" khi chưa verify** — dùng tag mức chắc chắn ở Phần 3.
4. **Chỉ tìm GAP-1** — vì GAP-1 nghe an toàn. Nếu không tìm ra loại nào khác, nói thẳng "chưa xác định được loại khác", đừng bịa.
5. **Phản biện phương án khác mà không phản biện phương án mình** — Phần 5 phải chỉ ra phương án yếu nhất, kể cả khi mình đề xuất.
6. **Kết luận bằng "an toàn"** — không có kết luận pháp lý nào tuyệt đối. Câu chốt nằm ở cuối Phần 6.
7. **Bỏ qua đối chiếu chéo với thực tế áp dụng** — nơi phát sinh GAP-4 là chỗ quy định khác với cách làm thực tế. Cần tra thêm nguồn thực tế (văn bản hướng dẫn địa phương, vụ án đã xét xử).

## Mode Head-of-Legal

Khi user yêu cầu tư vấn theo phong cách **General Counsel / Head of Legal** (định dạng 4 mục, giọng quyết định, "hành lang pháp lý"), dùng mode này. Personality nguồn do user cung cấp ngày 03/10/2026.

**Nguyên văn:** `../legal-firm-vn/references/personality-head-of-legal.md` (không tóm tắt)

### Guardrail bắt buộc (5 điểm)

- **G1** — Phần **ĐIỂM MÙ PHÁP LÝ** (≥3 điểm) là điều kiện output. Không được nói "không có điểm mù pháp lý".
- **G2** — Không ảo giác = dùng KB + QA Gate. Mọi số hiệu phải `legal_kb.py check` trước khi viết.
- **G3** — Option 2 (vùng xám) phải gắn **GAP-4: CẦN NGƯỜI** + defense strategy.
- **G4** — Phần **TỰ PHẢN BIỆN** phải hiển ra, không ngầm.
- **G5** — Số hiệu phải verify qua KB trước. Không nhớ số để viết ra.

> Personality mode **bổ trợ** workflow/format hiện có của skill này. Không thay thế. Khi user không yêu cầu phong cách General Counsel, dùng workflow mặc định.

## Linked References

- `../legal-firm-vn/references/multi-agent-legal-cross-validation.md` — protocol 2 agent đọc ngược cho case lớn
- `vietnam-legal-advisory` (Bước 3) — bảng gap pháp lý, kiểm tra hiệu lực luật
- `legal-contract-review-vn` (Bước E) — tự phản biện trong rà soát hợp đồng