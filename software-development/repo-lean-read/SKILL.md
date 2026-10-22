---
name: repo-lean-read
description: "Low-token codebase reads that keep context for coding."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [codebase, reading, tokens, graft, context, efficient]
    related_skills: [repo-context-graph, codebase-context-graph, project-reconnaissance, graft]
---

# Repo Lean Read — đọc hiểu codebase ít token nhất

## Khi nào dùng
- Bắt đầu việc trong repo (bất kỳ dự án, session mới).
- "Đọc hiểu repo nhanh / ít token nhưng giữ context để code tiếp".
- Muốn orient + lấy surface + semantics mà KHÔNG mở nguyên file.

## Nguyên tắc cốt lõi
Phần tốn token nhất khi đọc repo là **tính thừa**: cùng 1 symbol đọc từ 5 file, hoặc mở nguyên file chỉ cần vài dòng. Luật ở đây:

1. **KHÔNG BAO GIỜ mở nguyên file để "hiểu".** Chỉ mở file ở đúng span cần sửa.
2. Tách 2 nhớ: **nhớ trong đầu** (map + surface gọn, dùng ngay) + **nhớ ngoài đầu** (graft graph / NOTE pointer ≤100 dòng, qua session nào đọc lại mà không tốn lại).
3. Orient trước, hỏi semantics sau, liệt kê surface bằng grep gọn, chỉ đọc file khi chạm code.

## Quy trình (THỨ TỰ TUYỆT ĐỐI)

### Bước 1 — Orient bằng map, không đọc file
Nếu repo có graft (`graft/`): `graft map` → dir clusters, file hubs, symbol với số incoming edges. Biết file nào nóng (hub nhiều caller) + hotspots, ~1,5KB.

### Bước 2 — Surface đầy đủ bằng MỘT grep gọn
Đừng phụ thuộc graft nếu graft còn tầng concept (không có skeleton sâu). Với Python/FastAPI:
```bash
grep -oE '@(app|router)\.(get|post|put|delete)\("[^"]+"' app/main.py
# 1,9KB → đủ 61 endpoint, thay cho mở nguyên file 73KB
```
Tương tự dùng với class/method của ngôn ngữ khác qua pattern sát cú pháp.

### Bước 3 — Hỏi semantics ĐÚNG needle
`graft ask "<câu gì làm gì / vì sao>" --source` → node kèm crux ≤8 dòng + file:line. Chỉ cần hiểu, không cần mọi chi tiết.

### Bước 4 — Edges (ai gọi ai) qua graph
`graft callers <symbol>` (precomputed, không grep). `--depth N` cho blast radius.

### Bước 5 — Mở file VẬT LÝ chỉ ở đúng span
`read_file(path, offset=<line>, limit=<số dòng>`) đúng file:line mà graft/grep đã trỏ. Không đọc nguyên file để tìm.

### Bước 6 — Flush vào state
Ghi kết luận + pointer file:line vào NOTE ≤100 dòng (theo state-file-protocol). Không ghi nguyên log. Đây là "context để code tiếp" — nhỏ, qua /new không mất.

## So sánh token (đo được, TFO trong ai-company)
| Cách | Input | Token ~ |
|---|---|---|
| Mở nguyên main.py 500 dòng | 73KB | ~20K |
| Lean (map + 1 grep routes + ask needle) | ~6KB | ~1,5K |

Chênh **12–15x**. Phần lớn từ bỏ "mở nguyên file".

## Pitfalls
- **Graft sâu ≠ graft có sẵn.** Graft ai-company/volden: ai-company là tầng concept (skeleton trả "no definitions"), volden sâu. Kiểm `graft skeleton <file>` trước khi tin; không sâu → grep gọn.
- `graft map` flag thay đổi theo version (vd v0.8.2 không có `-b`). Chạy `graft map` mặc định trước.
- Grep output để vào context trực tiếp là OK; đừng ném cả output vào NOTE.

## Verification
- [ ] Không mở nguyên file nào chỉ để "hiểu"
- [ ] Surface đầy đủ từ grep (đếm endpoint/symbol = con số khẳng định được)
- [ ] Biết file hub/hotspot (graft map) trước khi sửa
- [ ] NOTE ≤100 dòng có pointer file:line, đủ để session sau code tiếp