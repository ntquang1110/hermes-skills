---
name: personal-coaching
description: >
  Design and deliver multi-session structured coaching programs for users who
  want to learn complex topics (leadership, management, strategy, etc.).
  Covers needs assessment, curriculum design, interactive lesson delivery,
  reflection analysis, progress tracking, and persistent knowledge base.
platforms: [windows, macos, linux]
---

# Personal Coaching: Structured Multi-Session Learning

Use this skill when a user asks to **learn a complex topic** from A-Z, or says
"teach me X", "I want to master Y", or "guide me through Z step by step".
The method turns a broad request into a trackable, interactive, personalized
learning program with persistent artifacts.

## Trigger Topics

Leadership, management, strategy, communication, personal effectiveness,
domain knowledge (business, technical, creative), or any skill a user wants
to build over multiple sessions.

## Workflow

### Step 1: Needs Assessment (3 clarifying questions max)

Ask the user about:
1. **Current level** — beginner, intermediate, experienced?
2. **Primary goal** — what do they want to achieve by the end?
3. **Priority area** — what's their biggest struggle/challenge right now?

> Use `clarify` with choices to keep this fast. 1-2 rounds only.

### Step 2: Curriculum Design

Design 3-10 modules covering the topic. Each module has a 4-part structure:

```
1. 📖 Core Theory     — Framework, model, concept (concise, memorable)
2. 🎯 Real Case Study — Concrete example from known leader/company
3. ✍️ Reflection       — Questions that make the user apply it to themselves
4. ✅ Action Tasks     — Specific things they must DO before next session
```

Save the full curriculum as a reference file under
`~/AppData/Local/hermes/<topic>/00-curriculum.md`.

### Step 3: Set Up Progress Tracking

Use **three persistence layers**:
- **Todo list** (`todo()`) — track each module as a checklist item
- **File system** (`write_file()`) — full module content under
  `~/AppData/Local/hermes/<topic>/` for permanent library
- **Memory** (`memory()`) — brief summary of the project + user profile for
  cross-session continuity

### Step 4: Deliver Each Module

Deliver the module content **conversationally**, not as a wall of text.
On Telegram, use Markdown tables, bullet lists, bold for key terms, and
collapsible sections where appropriate.

End each module with a clear **"khi nào xong action tasks thì bảo em"**
invitation so the user drives the pace.

### Step 5: Collect & Analyze Reflection

When the user returns their reflection answers:

1. **Explicitly save** their raw answers to a reflection file
   (`01-module-reflection.md`).
2. **Analyze for patterns** — connect their answers to:
   - Their stated priority / pain point
   - Implicit root causes (e.g. "team weak → I do everything → no time to lead")
   - Contradictions or tensions (e.g. values autonomy but not decisive)
3. **Give 2-3 sharp insights** in plain language — what this reveals about
   them as a learner/leader.
4. **Re-prioritize remaining modules** if their reflection changes what
   they need first.

### Step 6: Persist the Project

Create a `PROJECT.md` file under the topic directory containing:
- Goal and definition of done
- User profile summary (from reflection)
- File structure overview
- Progress status

## Pitfalls to Avoid

- **Don't design 20+ modules** — the user will never finish. 5-10 is ideal.
- **Don't skip reflection analysis** — the value is in connecting their
  answers to their goals, not just recording them.
- **Don't deliver everything in one go** — let the user complete action
  tasks before the next module. Momentum > volume.
- **Don't use only text** — include frameworks, tables, case studies,
  actionable templates to make it interactive.
- **Don't default to English when user speaks Vietnamese** — match the
  user's language throughout.

## Chốt NGHĨA của chủ đề trước khi thiết kế

Nhiều thuật ngữ coaching có 3-4 nghĩa hoàn toàn khác nhau, mỗi nghĩa cho ra chương
trình khác hẳn. Ví dụ "articulation training" = (1) luyện nói rõ cho người đi làm,
(2) trị liệu âm ngữ lâm sàng, (3) kỹ thuật articulation trên nhạc cụ, (4) diễn đạt
chiến lược trong họp.

**Đừng đoán.** Nêu 2-4 nghĩa ra, chỉ rõ mình đi theo nghĩa nào và vì sao, rồi mới
thiết kế. Đoán sai nghĩa thì cả chương trình vô dụng và user phải nói lại.

## Phân tầng bằng chứng: mạnh / cơ chế / lời vendor

Khi chủ đề có nền khoa học, tách rõ 3 tầng trong curriculum:

1. **Mạnh** — peer-reviewed, có PMID/số liệu. Ghi rõ thiết kế + liều lượng.
2. **Cơ chế** — nghiên cứu giải thích TẠI SAO phương pháp hoạt động.
3. **Lời vendor** — con số marketing không có nguồn bình duyệt.

**Không trộn tầng 3 vào tầng 1.** Nếu thị trường bán một liều lượng chưa được
chứng minh, nói thẳng ra — đó thường là phát hiện giá trị nhất cho user, và nếu user
đang làm sản phẩm thì đó chính là chỗ trống thị trường.

Đối chiếu liều lượng thật, đừng lặp lại con số marketing. Ví dụ: nghiên cứu lâm sàng
dùng 16-20 giờ trong 4 tuần, còn app bán "9 phút/ngày" → nói rõ khoảng cách đó thay
vì thiết kế theo con số của app.

## Deliverable: công cụ HTML tương tác, không chỉ bài giảng chữ

Với chương trình LUYỆN TẬP (thể chất, giọng nói, thói quen, kỹ năng), bài giảng chữ
không đủ. User cần thứ mở ra dùng hằng ngày. Dựng **một file HTML tự chứa** gồm:
timer/checklist theo buổi · bảng tự chấm điểm · biểu đồ tiến độ so với đường cơ sở ·
localStorage lưu trên máy · nút xuất dữ liệu.

Rồi publish preview để mở trên điện thoại. Xem `html-interactive-dashboard` cho kiến
trúc + các bẫy wiring (guard `NaN` khi dữ liệu thiếu, không gate trạng thái user sau
cờ runtime, gọi `render()` ngay khi state đổi).

**Bàn giao cả hai:** link HTML để tập hằng ngày + file curriculum gốc để tra cứu.

## Supporting Files

- `references/leadership-curriculum-example.md` — Full 10-module leadership
  curriculum from a real session, usable as a template for similar requests.
- `references/articulation-training-evidence.md` — Knowledge bank luyện nói rõ:
  7 PMID đã verify (RCT LSVT LOUD / PD COMM BMJ 2024, chất xám-chất trắng Exp
  Gerontol 2024, random-vs-blocked practice, checkpoint theo tuổi), phân tầng
  bằng chứng mạnh/cơ chế/vendor, đặc điểm tiếng Việt (thanh điệu, âm cuối, phụ âm
  đầu hay lẫn), cấu trúc buổi 12 phút, thang chấm 5 chỉ số, khảo sát thị trường.

## Verification

After creating a coaching program:
- [ ] Curriculum file exists at `~/leadership/00-curriculum.md`
- [ ] Module content files exist (01-, 02-, etc.)
- [ ] Todo list shows all modules
- [ ] Memory stores project summary
- [ ] User's reflection is saved and analyzed
- [ ] PROJECT.md exists with full context
