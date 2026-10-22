---
name: hermes-skill-library-maintenance
description: "Use when a SKILL.md is oversized or skills overlap."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [skills, maintenance, refactor, token-efficiency, references]
    related_skills: [hermes-agent-skill-authoring, hermes-core-token-efficiency]
---

# Hermes Skill Library Maintenance

Giữ thư viện skill gọn và rẻ: tách SKILL.md quá khổ, gộp skill trùng, dọn skill chết.
Khác với authoring (viết skill mới) — đây là BẢO TRÌ thư viện đang có.

## When to use

- SKILL.md tiến sát / vượt hard cap 100,000 chars
- `skill_manage(action='patch')` bị từ chối: `SKILL.md content is N characters (limit: 100,000)`
- Skill load tốn token vì thân file quá dài so với tần suất dùng
- Hai skill phủ cùng một lớp việc → cần gộp
- Rà thư viện để prune skill không còn dùng

Không dùng cho: viết skill mới (→ `hermes-agent-skill-authoring`), giảm token ở
tầng source (→ `hermes-core-token-efficiency`).

## Luật nền: tách là MOVE, không phải rewrite

Chữ đã chuyển giữ **nguyên byte**. Không tóm tắt, không "viết lại cho gọn".
Mỗi câu bị rút gọn là một bước bị mất, và file sau khi tách vẫn đọc rất trôi chảy —
nên không ai phát hiện cho tới lúc cần đúng bước đó.

Ngoại lệ duy nhất được phép viết mới: **mục lục** trỏ tới các file vừa tách.

## Quy trình tách SKILL.md quá khổ

1. **Backup**: copy `SKILL.md` → `SKILL.md.bak-pre-split` trong chính thư mục skill.
   *Xong khi*: file backup tồn tại và cùng số byte với bản gốc.
2. **Parse thành section theo H1/H2 ONLY**, bỏ qua mọi dòng nằm trong ``` fence.
   Code block chứa `# comment` mà regex `^#` ngây thơ nhận nhầm là heading — parse
   sai bước này làm mất cả code block.
   *Xong khi*: số heading tìm được khớp với `grep` thủ công trên file gốc.
3. **Phân loại từng section**: KEEP (trigger + workflow + pitfall tần suất cao) hay
   MOVE → một `references/<chủ-đề>.md` theo chủ đề, không theo thứ tự xuất hiện.
   *Xong khi*: SKILL.md còn trong khoảng 25–50k chars.
4. **Ghi từng reference file** với các section nguyên văn, ngăn bằng `---`.
   *Xong khi*: mỗi file mới mở ra đọc được và có tiêu đề rõ.
5. **Viết lại SKILL.md** = frontmatter + section giữ lại + mục lục
   `## Chi tiết theo chủ đề` liệt kê từng file mới kèm 1 dòng "trong đó có gì".
   *Xong khi*: mỗi file references mới đều có đúng 1 dòng trỏ tới nó.
6. **Verify không mất mát** — xem mục dưới. *Xong khi*: cả hai diff RỖNG.

Script sẵn: `scripts/split_skill_md.py` — sửa bảng KEEP/MOVE rồi chạy.

## Verify — hai diff phải RỖNG

```python
old = headings(bak)                                  # heading ở bản gốc
now = set(headings(new_skill + all_new_refs))        # gom cả file mới
assert all(t in now for t in old)                    # 1. không mất heading

lost = {l.strip() for l in bak.split("\n") if l.strip() and l.strip() != "---"} \
     - {l.strip() for l in pool.split("\n") if l.strip() and l.strip() != "---"}
assert not lost                                      # 2. không mất dòng nội dung
```

- Diff heading bắt được **section bị bỏ quên**.
- Diff theo dòng bắt được **nội dung bị rút gọn bên trong section còn giữ** — thứ mà
  diff heading không thấy.
- "Đọc thấy ổn" KHÔNG phải bằng chứng.

## Pitfalls

1. **Byte ≠ char.** `wc -c` đếm byte UTF-8; tiếng Việt nhiều byte nên 25,498 chars đo ra
   28,486 B. **Cap 100,000 là chars.** So bằng chars, nếu không sẽ tưởng đã vượt trần
   trong khi thực ra chưa — hoặc ngược lại, tưởng đã an toàn.
2. **Quên bỏ qua code fence khi parse heading** → nuốt cả code block vào section sai.
3. **Loại `---` bạn tự thêm khỏi line-set diff**, nếu không chúng hiện ra như "mất".
4. **H3 tự đi theo H2 cha** khi chỉ tách ở H1/H2 — đúng ý muốn, không cần xử lý riêng.
   Đừng tách ở H3 rồi thắc mắc sao section vụn.
5. **Giao subagent tách nhiều skill thì phải TỰ VERIFY diff từng cái.** Child báo
   "done" là self-report, không phải bằng chứng. Đọc `SKILL.md.bak-pre-split` mà nó
   để lại và chạy lại hai diff.
6. **Kiểm tra protected trước khi hứa sửa.** `skill_manage` từ chối ghi vào skill
   bundled / pinned / user-owned, kèm thông báo rõ. Gặp refusal thì **dừng và báo
   user** (`hermes curator adopt <name>` nếu muốn tự quản), đừng tìm đường vòng.
   `hermes-agent`, `hermes-agent-skill-authoring` là bundled — không sửa được.

## Gộp skill trùng (consolidation)

Trước khi gộp: xác nhận hai skill thật sự phủ **cùng một lớp việc**, không phải hai
lớp gần nhau. Gộp sai làm mất trigger — skill gộp phải giữ được các cụm từ trigger
của cả hai bên trong `description`.

Khi gộp xong, dùng `skill_manage(action='delete', absorbed_into='<umbrella>')` để
curator biết đây là hợp nhất chứ không phải prune trơ. Umbrella phải **tồn tại trước**
khi delete — tạo/gia cố nó trước, xoá sau.

## TODO khi rà thư viện

- Đối chiếu mọi skill có `## Chi tiết theo chủ đề` xem file references nó trỏ tới có
  tồn tại thật không (tách xong đổi tên file là kiểu hỏng im lặng).
- Skill có `references/` ≥300 dòng thì reference phải có ToC ở đầu file.

## References

- `scripts/split_skill_md.py` — script tách deterministic: parse fence-aware, phân loại
  KEEP/MOVE, ghi references nguyên văn, chạy cả hai diff kiểm mất mát. Sửa bảng
  `KEEP_KEYS` / `MOVE_MAP` ở đầu file rồi chạy.
