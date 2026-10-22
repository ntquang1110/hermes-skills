---
name: application-forms
description: Fill external contest and grant forms end to end.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
---

# Application Forms

Điền hộ các form đăng ký bên ngoài: contest khởi nghiệp, grant, chương trình
tăng tốc, khảo sát dài. Nhận link form → trả bài dự kiến cho user duyệt →
mới fill/submit thật.

## Hard Rules (user đã chốt, không thương lượng)

1. **Dump TOÀN BỘ câu hỏi trước, không đoán mò.** Không publish draft khi mới
   xem được 1-2 page rồi tự bịa các section còn lại. User gọi đây là "form ảo"
   và sẽ reject.
2. **Trải phẳng (flatten) toàn bộ câu hỏi + đáp án dự kiến để user duyệt
   trước. Chỉ fill/submit sau khi user duyệt.** Không tự ý submit.
3. **Pick template trước khi dựng HTML.** Publish gallery, hỏi user chọn theme,
   rồi mới build (theo skill `design-template-selector`). Không tự chọn theme.

## Workflow

```
[Link form] → [Extract all questions] → [Flatten draft: Q + đáp án dự kiến]
→ [User review/comment] → [Pick template nếu dựng HTML] → [Fill form thật + submit]
```

### Step 1: Extract all questions

- Google Forms: đọc `references/google-forms-extraction.md`, dump toàn bộ items
  (sections, title, type, required, options, help text, giới hạn ký tự) qua
  `browser_console` trên session đã sign-in.
- Form khác (Typeform, web form thường): snapshot từng page, hoặc đọc HTML/JS.

### Step 2: Flatten draft

- Một file/MD/HTML duy nhất: mỗi câu hỏi + đáp án dự kiến + flag các chỗ cần
  user confirm (ngày thành lập, số liệu, documents...).
- Kèm self-assessment: điểm mạnh, điểm yếu, rủi ro, checklist tài liệu cần chuẩn bị.

### Step 3: User review

- Publish draft, gửi link. Đợi comment/duyệt. Không qua bước này.

### Step 4: Fill + submit (sau duyệt)

- Điền vào form thật theo draft đã duyệt, upload documents, submit trước deadline.
- Verify bằng snapshot sau mỗi page. Draft Google Forms tự lưu theo account —
  nói rõ với user đâu là draft thăm dò, đâu là submit thật.

## References

- `references/google-forms-extraction.md` — dump full cấu trúc Google Forms qua
  `FB_PUBLIC_LOAD_DATA_` (snippets đã verify, type map, pitfalls).
