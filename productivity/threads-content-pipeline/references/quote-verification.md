# Kiểm chứng quote nguyên văn với transcript raw

Vấp phải 2026-08-08 khi xử lý video Stanford CS329A (draft_cs329a_p1_overview.txt) — quote trích trong draft bị check `quote in transcript` trả **False oan** dù quote ĐÚNG nguyên văn.

## Nguyên nhân

Transcript `fetch_transcript.py --text-only` xuống dòng GIỮA câu (mỗi dòng 1-2 từ, kết thúc bằng `\r\n`). Substring check trực tiếp fail vì quote có khoảng trắng đơn trong khi transcript có `\r\n`.

## Cách check đúng

```python
import re
with open(path, encoding='utf-8') as f:
    t = f.read()
tnorm = re.sub(r"\s+", " ", t).strip()   # BẮT BUỘC normalize trước
assert q in tnorm, f"quote KHÔNG nguyên văn: {q}"
```

## Chỉnh sửa biên tập được phép khi trích (không phải bịa quote)

1. **Viết hoa chữ đầu quote** nếu transcript viết thường giữa câu (vd transcript: "it was not baked in by design. It was basically discovered." → draft: "It was not baked in by design..."). Chuẩn biên tập, các từ vẫn nguyên văn.
2. **Lược bỏ false-start disfluency** trong lời nói — transcript giữ nguyên "the correct--" kiểu nói lắp giữa chừng. Lược phần đó được phép:
   - transcript: "wait, the correct-- there's something wrong, maybe. And maybe I need to fix that."
   - draft: "wait, there's something wrong, maybe. And maybe I need to fix that."
   - Miễn các từ còn lại nguyên văn, đúng thứ tự.

## CẤM

- Thêm/sửa/bịa từ, số liệu, tên người không có trong transcript.
- Ghép hai câu cách xa nhau thành một quote.
- Giữ nguyên dấu "–"/"—" bị cắt trong false start (sẽ phá luật 0 em dash của draft).
