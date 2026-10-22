---
name: research-overview
description: "Deep-root research: 3 verified layers + routing."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [research, first-principle, routing, evidence, overview]
    category: research
    related_skills: [web-research, pubmed-evidence-research, research-reporting, research-html-catalog, content-publish, grounded-citations]
---

# Research Overview (First Principle)

Khung tư duy cho bất kỳ bài nghiên cứu nào. ĐI SÂU VÀO GỐC vấn đề theo first principle:
hiểu bản chất → triển khai ra hiện hữu → nêu vướng mắc khoa học. Mỗi tầng BẮT ĐỀN bằng bằng chứng (PMID/DOI/tài liệu gốc), KHÔNG có chỗ cho lý luận suông.

## When to use

- Bất kỳ yêu cầu nghiên cứu nào: phân tích sâu, so sánh, brief, review, "đi vào gốc vấn đề", "hiểu bản chất".
- Đặc biệt khi user nói "follow first principle", "đào tận gốc", "hiểu bản chất".

## ⚠️ Cạm bẫy chính (chặn trước)

First principle không = viết lý thuyết trừu tượng. Bản chất phải được **bắt đền bằng bằng chứng**, không phải lý luận đẹp. Nếu một phát biểu bản chất không gắn được nguồn verify → phải nói rõ "chưa có bằng chứng trực tiếp", KHÔNG bịa PMID. Đây là điểm quyết định chất lượng.

## 3 tầng bắt buộc (mỗi bài nghiên cứu phải qua đủ)

### Tầng 1. First principle — hiểu bản chất
Câu hỏi khởi động: **"Điều gì thật sự đang xảy ra ở mức cơ chế?"**

- Bóc hiện tượng về nguyên lý nền: cơ chế vật lý/hóa học/sinh học thật đằng sau.
- Trả lời bằng gốc khoa học (cơ quan/chuỗi phản ứng/định luật), KHÔNG bằng thuật ngữ marketing.
- QUY TẮC: mỗi phát biểu bản chất phải gắn sẵn PMID/DOI/tài liệu gốc.
- Xác định thuật ngữ chính xác trước (vd "kháng thể không đặc hiệu" thực chất là natural IgM polyreactive — phải chuẩn hoá thuật ngữ trước khi phân tích).

### Tầng 2. Hiện hữu — triển khai ra thực tế
- Bản chất đã hiểu → nó thể hiện ra sao trong sản phẩm/hệ thống đang tồn tại.
- Nối điểm: nguyên lý nền → thiết kế/mô hình đang dùng → TẠI SAO được làm vậy.
- QUY TẮC: khẳng định "X làm thế này" phải có trích nguồn thực tế (spec, trial, tài liệu), không tự suy diễn từ bản chất.

### Tầng 3. Vướng mắc khoa học hiện tại
- Bản chất đã hiểu, hiện hữu đã triển khai → chỗ nào khoa học CHƯA trả lời được.
- Nêu giới hạn bằng chứng, khoảng trống dữ liệu, ngưỡng chưa xác định.
- Đây là phần tạo giá trị: chỉ ra cái "chưa ai biết", không lặp cái đã biết.
- QUY TẮC: vướng mắc phải ghi rõ "chưa có bằng chứng trực tiếp" khi đó là sự thật (theo đúng quy tắc không bịa PMID).

## Routing — skill con đảm nhiệm phần nào

Khung này làm bản đồ TƯ DUY. Đạn dược do các skill con cung cấp. KHÔNG lặp lại chi tiết kỹ thuật của chúng ở đây — chỉ trỏ.

| Giai đoạn | Skill chịu trách nhiệm |
|-----------|------------------------|
| Gom nguồn, xử lý search engine chặn | `web-research` |
| Verify PMID/DOI, không bịa nguồn, tra cứu cho từng tầng | `pubmed-evidence-research` |
| Dẫn nguồn kiểm chứng được (grounded) | `grounded-citations` |
| Bày kết quả thành HTML có cấu trúc | `research-reporting` |
| Output dạng catalog/bảng | `research-html-catalog` |
| Xuất link preview.thefirstonly.com | `content-publish` |

## Quy trình làm bài

1. **Nhận diện kiểu** bài (phân tích sâu / so sánh / brief / review / đánh giá sản phẩm).
2. **Chạy Tầng 1 trước tiên**: chuẩn hoá thuật ngữ + gom nguyên lý nền kèm nguồn. Không nhảy sang hiện hữu khi bản chất còn mơ hồ.
3. **Xác định khoảng trống** của Tầng 1 (chưa có bằng chứng trực tiếp chỗ nào) → ghi sẵn để dùng lại ở Tầng 3.
4. **Chạy Tầng 2**: nối bản chất với sản phẩm/hệ thống thực, kèm nguồn thực tế.
5. **Chạy Tầng 3**: tổng hợp vướng mắc khoa học + giới hạn bằng chứng.
6. **Verify toàn bộ**: mọi PMID đã efetch thật trong phiên này, không có PMID bịa, thuật ngữ đã chuẩn.
7. **Bày + xuất bản**: theo skill routing. Nếu user chỉ định đăng Threads kênh cụ thể thì mới sang pipeline Threads; mặc định là link preview.

## Deliverable shape

Mọi bài nghiên cứu hoàn chỉnh phải có đủ 3 phần theo cấu trúc trên, kèm:
- Phần **Nguồn đã verify** ở cuối (PMID + note ngắn nội dung thật của từng bài).
- Ghi rõ ngày verify + phương pháp (theo `pubmed-evidence-research`).

## Pitfalls

- Đừng để Tầng 1 thành bài giảng trừu tượng — mỗi câu bản chất phải mang nguồn.
- Đừng bỏ Tầng 3 — phần "chưa ai biết" mới là giá trị; nếu bỏ, bài chỉ là lặp lại kiến thức.
- Thuật ngữ chuẩn hoá trước khi phân tích, nếu không cả 3 tầng đều đi trên nền sai.
- KHÔNG tự suy luận hiện hữu từ bản chất — cần nguồn thực tế riêng cho Tầng 2.