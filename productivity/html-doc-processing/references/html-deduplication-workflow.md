# HTML Document Deduplication Workflow

Phát hiện và loại bỏ section trùng lặp trong tài liệu HTML nhiều section.

## Khi nào dùng

- Document HTML có 10-30 section riêng biệt (ngăn bằng § hoặc `<hr>`)
- Nghi ngờ một số section là expanded version của section khác
- Cần gọn mà không mất thông tin

## Workflow

### 1. Lấy text để phân tích

```python
# Dùng browser_console lấy innerText toàn bộ page
# Hoặc curl HTML → parse text
import re, json
from collections import Counter

# Parse HTML sections
section_headers = list(re.finditer(
    r'<div class="section">\s*\n\s*<div class="section-header">'
    r'<span class="section-number">§</span>'
    r'<h[23] class="section-title">(.*?)</h[23]></div>',
    html
))

# Mỗi section: từ header này tới header kế
sections = []
for i, m in enumerate(section_headers):
    start = m.start()
    end = section_headers[i+1].start() if i+1 < len(section_headers) else len(html)
    sections.append((start, end, m.group(1)))
```

### 2. So sánh nội dung giữa các section

```python
# Đếm section content trùng
# Pattern phổ biến: Executive Summary có mục X ngắn,
# sau đó có section riêng expanded version của X
long_lines = [l.strip() for l in text.split('\n') if len(l.strip()) > 60]
para_counts = Counter(long_lines)

# Tìm section title overlap
# Nếu Executive Summary có "9.3 3 việc KHÔNG được làm"
# và có section riêng "3 việc KHÔNG được làm" → duplicate
```

### 3. Dấu hiệu nhận biết section trùng

| Dấu hiệu | Ví dụ |
|---|---|
| Section có title giống sub-heading trong section khác | Exec Summary có "5. Điều kiện tiên quyết", section riêng "Điều kiện tiên quyết" |
| Section nhỏ hơn nhiều so với các section khác nhưng cùng chủ đề | 12K vs 20-30K trung bình |
| Bảng nguồn tham khảo lặp lại nguyên văn | [S1] xuất hiện dạng table row 5+ lần |
| Content overlap >60% với sub-section của Exec Summary | So sánh Jaccard similarity |

### 4. Xoá section khỏi HTML

```python
# Biết vị trí section cần xoá (start, end)
# Cắt chuỗi: html[:remove_start] + html[remove_end:]
new_html = html[:section_start] + html[section_end:]

# Verify số section còn lại
remaining = len(re.findall(
    r'<div class="section-header"><span class="section-number">§</span>',
    new_html
))
```

### 5. Verify

- `browser_navigate(preview_url)` — check page load
- `browser_snapshot()` — đếm số section heading còn lại
- Scroll qua chỗ transition (sau section cuối cùng giữ lại, trước section đầu tiên của phần tiếp theo)
- Không cần re-check từng section không bị ảnh hưởng

## Lưu ý

- **Section boundary bằng regex:** Dùng `re.finditer` với pattern section-header. Mỗi section = từ header này tới header kế. Không dùng div-balancing (dễ sai với HTML lồng nhau).
- **Chỉ xoá section dạng §-header.** Không xoá sub-heading bên trong section khác (ví dụ "9.3 3 việc KHÔNG được làm" bên trong Exec Summary là sub-section, không phải section riêng).
- **Source table cuối mỗi section** là redundancy chấp nhận được nếu mỗi section muốn đứng độc lập. Chỉ gộp khi user yêu cầu.
- **Giữ nguyên `<hr>` trước section đầu tiên được giữ lại** để transition mượt.
