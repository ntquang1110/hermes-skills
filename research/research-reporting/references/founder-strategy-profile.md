# Founder-Strategy Profile (research EN → output VI)

Dùng khi founder VN yêu cầu "mổ xẻ" chiến lược đổi mới/sản phẩm của một founder/CEO nổi tiếng (Musk, Jobs, Bezos, BYD...) — cần sự thật không tô hồng, ví dụ có nguồn, và bài học áp dụng cho nông nghiệp/tech/sản xuất VN.

## Cấu trúc mỗi chiều phân tích (bắt buộc 4 khối)

1. **Cơ chế (mechanism):** quy tắc vận hành, điều kiện áp dụng, quote gốc nếu có.
2. **Ví dụ cụ thể có nguồn:** tên sự kiện + năm + con số + nguồn (tiểu sử, SEC filing, phỏng vấn, lời kể nhân viên có tên).
3. **Điểm mù / thất bại:** nơi chính công thức đó phản tác dụng; số liệu thiệt hại nếu có.
4. **Bài học cho founder Việt:** 1-2 câu hành động, gắn với vốn mỏng / lao động VN / tuân thủ.

## Khung 8 chiều dùng cho Musk (tái dùng được cho founder khác)

1. Lọc vấn đề quan trọng — 2. Tích hợp dọc build-vs-buy — 3. Vòng lặp phản hồi nhanh —
4. Deadline bất khả thi — 5. Quản trị rủi ro (liều ở đâu, hedge ở đâu) —
6. Ứng xử đối thủ (mặc kệ / đè / mua) — 7. Tổ chức phẳng + hardcore —
8. Nghịch lý tốc độ vs an toàn sinh mạng.

Với founder khác, giữ khung 4-khối/chiều, thay danh sách chiều cho phù hợp.

## Quy tắc nguồn

- Thứ tự ưu tiên: tiểu sử chính thống (Vance 2015, Isaacson 2023 cho Musk) → hồ sơ pháp lý (SEC, NHTSA, tòa Delaware) → báo chí điều tra (Reuters/NYT) + lời kể nhân viên nêu tên (Mueller, Shotwell, Cantrell) → Wikipedia CHỈ làm chỉ mục, không phải nguồn duy nhất.
- Mỗi chiều ≥ 1 nguồn định danh được. Thất bại/blind spot là mục bắt buộc — thiếu thì profile chưa xong.
- Không dùng PMID/chủ quan từ trí nhớ cho con số (giá, năm, %): verify qua API/page text thật.

## Quy tắc song ngữ

- Research bằng tiếng Anh (từ khóa EN, nguồn EN), output tiếng Việt.
- Giữ nguyên thuật ngữ EN lần đầu xuất hiện kèm dịch: "vertical integration (tích hợp dọc)", "test-to-failure".
- Thông điệp xuyên suốt 1 đoạn cuối: học cái gì, tránh cái gì.

## Thu thập đã verify OK (Wikipedia-heavy subject)

- `action=query&prop=extracts` nhẹ hơn `prop=wikitext`; gắn `User-Agent` riêng, dính 429 → sleep 10s rồi retry, đừng spam parse full page.
- Jina Reader `https://r.jina.ai/<wikipedia-url>` trả markdown sạch, tốt để trích đoạn founding/vertical-integration/hardcore; strip `[!Image...]` trước khi tìm keyword.
- Case Musk 09/2026: trích được vụ Nga–Dnepr/Mars Oasis, vertical integration + COTS, ultimatum "hardcore" 16/11/2022, sa thải ~1/2 nhân sự 4/11/2022, "funding secured" 2018, production hell — đủ dựng 8 chiều.
