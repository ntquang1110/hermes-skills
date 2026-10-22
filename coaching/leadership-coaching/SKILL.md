---
name: leadership-coaching
description: Design & deliver personalized leadership development programs — curriculum building, interactive coaching materials (reflection, case studies, action tasks), Leadership Canvas tool, daily accountability check-ins via cron, and publishing to Gist+Notion.
---

# Leadership Coaching

Use this skill when the user wants to become a better leader, build a leadership curriculum, or get personalized coaching on leadership skills.

## Workflow

### Phase 1: Assessment
1. **Ask current level:** never led / leading small team / several years / aspiring with vision
2. **Ask top priority:** people management, vision/strategy, communication, decision-making/conflict
3. **Ask about context:** team size, industry, biggest pain point
4. **Have them do a reflection exercise** across 5 questions (triggers, values, gaps, EQ, team reality)
5. **Analyze reflection** to find patterns and connect dots to their priority

### Phase 2: Curriculum Design
Design 10 modules covering the full leadership spectrum:

| # | Module | Focus |
|---|--------|-------|
| 1 | Self-Mastery | EQ, self-awareness, mindset |
| 2 | Building Trust | Trust Equation, psychological safety |
| 3 | Communication & Influence | Storytelling, active listening, Golden Circle |
| 4 | People Management & Talent Retention | Coaching (GROW), stay interviews, retention toolkit |
| 5 | High-Performance Teams | Tuckman stages, delegation matrix |
| 6 | Vision, Strategy & Execution | OKRs, 4 Disciplines of Execution |
| 7 | Difficult Conversations | SBI feedback, Radical Candor, underperformers |
| 8 | Resilience & Change | Change curve, 4 pillars of resilience |
| 9 | Scaling Leadership & Culture | Multiplier vs Diminisher, culture layers |
| 10 | Legacy & Growth | Mentorship flywheel, growth mindset |

Each module always includes: theory → case study → reflection exercise → action tasks.

### Phase 3: Materials Creation

**HTML tools:**
- Full curriculum → index.html with sidebar navigation, dark theme, all 10 modules embedded
- Leadership Canvas → leader-canvas.html (9-block editable canvas, localStorage auto-save, Ctrl+S)
- Use `write_file` to create HTML, then upload to GitHub Gist via curl+API PATCH

**Upload to Gist:**
```bash
# Build JSON payload via Python, then curl PATCH
python -c "import json; ..."  # write payload to temp file
curl -s -X PATCH "https://api.github.com/gists/{GIST_ID}" \
  -H "Authorization: token $PAT" \
  -H "Content-Type: application/json" \
  -d @payload.json
```

**Local Canvas Server** (for saving to file on "Save" click instead of just localStorage):
Use the reusable script under this skill:

```bash
cd ~/AppData/Local/hermes/skills/coaching/leadership-coaching/scripts
python canvas-server.py
```

This starts a local HTTP server at `http://localhost:2345` that:
- Serves the canvas HTML
- Accepts `POST /save` with JSON body → writes to `canvas-data.json` + `canvas-data.md`
- `GET /data` returns current saved data
- Same-origin → no CORS issues

**Hub Dashboard** (recommended — single-page 8-tab app):
Build one unified HTML (`hub.html`) with auto-saving localStorage. Tabs:

| Tab | Purpose | Key features |
|-----|---------|-------------|
| 📋 Canvas | 9-box Leader Canvas | Editable, auto-save, copy-text |
| 📓 Journal | Daily learning log | Date + free-text entry, delete |
| ✅ Actions | Action tracker | Tick-to-complete, module filter, timeline logging |
| 📈 Timeline | Visual progress | Milestones, action completions, notes |
| 🎯 Focus | Weekly/monthly goals | Editable cards, auto-save |
| 📖 Learning Lab | Deep-dive study | Concepts with research + case study + counter-point + application |
| 🎴 Q&A | Flashcard quiz | 25+ questions, difficulty/module filters, Daily 5 mode, "Learned it" progress |
| ⚙️ Storage | Export/Import JSON | Download full data → send to mentor, upload to restore |

**Learning Lab concept format** (for the 📖 tab):
```
📖 CORE — 2-3 sentence definition
🔬 RESEARCH — cited study with numbers/statistics
📖 CASE STUDY A — startup/small-team context
🏢 CASE STUDY B — enterprise/billion-dollar context
⚠️ COUNTER-POINT — when NOT to use this framework
💡 APPLICATION — specific to this user's situation
```

**Q&A Flashcard system** (for the 🎴 tab):
- 25+ questions across Modules 1-2 (expand as user progresses)
- 3 difficulty levels: 🟢 Easy, 🟡 Medium, 🔴 Hard
- 4 study modes: All / By Module 1 / By Module 2 / Daily 5 (prioritizes unseen cards)
- Each card: question → reveal answer → explanation → case study → "Đã nhớ" / "Học lại" buttons
- Progress stored in localStorage, displayed as progress bar + stat cards

**⚠️ Gist preview vs Local server:** htmlpreview.github.io pages CANNOT POST to localhost (cross-origin). The user MUST open `http://localhost:PORT` directly for the Save-to-file feature to work. If they use the Gist preview, they'll need a fallback. Best fallback strategy for Gist-hosted HTML: add a "📋 Copy gửi cho Mentor" button that copies formatted text to clipboard, plus a "⬇️ Tải JSON" download button.

**Notion page:** Create standalone page under user's root page (e.g. "Blog của Quang") with overview + Gist preview links embedded in markdown.

**Project files:** Store everything under `~/leadership/`:
- `00-curriculum.md` — full curriculum overview
- `01-{module-name}.md` — per-module detailed content
- `01-{module-name}-reflection.md` — user's reflection data + analysis
- `PROJECT.md` — project context, progress, links
- `{name}.html` — interactive HTML tools

### Phase 4: Daily Accountability

Create 2 cron jobs with `attach_to_session: true`:
- **11:30 AM** — Midday check-in (lighter: what did you learn this morning?)
- **5:30 PM** — End-of-day review (deeper: lessons, action tasks, tomorrow's focus)

Both cron prompts should:
- Reference user's profile (values, triggers, gaps)
- Reference current module and its action tasks
- Use coaching mindset (Radical Candor, direct but supportive)
- End with an open question for reflection

### Phase 4b: Cron Prompt Evolution (CRITICAL)

**Stale prompts cause user frustration.** The user will correct you if the prompt references completed tasks or outdated state. Common signal: *"sao canvas đã làm rồi mà cứ nhắc lại thế, nói lại về X và Y đi"*.

To avoid this:

1. **Update cron prompts after every milestone.** When user completes a module's action tasks, update BOTH cron prompts to:
   - Remove references to completed tasks
   - Add references to new module and its action tasks
   - Reflect any new tools/hub tabs they now have access to

2. **Never mention completed items.** If Canvas is done, don't ask about it. The prompt must reflect current reality, not the template.

3. **State-scan before composing.** The cron should check the hub state (browser) or sheet before responding. Don't trust the static prompt alone — verify what's actually done vs pending. If the sheet/hub is unreadable (see tracker-sheet pitfall below), fall back to `session_search` on past sessions (previous check-in content, user's last reported issue) and compose the check-in from that + direct questions. A check-in grounded in conversation history is better than one blocked on data access.

   **Data access reality (verified 08-2026):** `curl` hub.html → static HTML only; user progress (journal entries, daily ticks) lives in browser localStorage, NOT readable server-side. The hardcoded `DAILY_STEPS` array (5 bước: Check Sheet Tracker, Học 1 Concept, Quiz 5 Câu, Viết Nhật Ký, Làm 1 Action Task) reveals what the daily guide asks, not what the user did. Sheet gviz export (`/gviz/tq?tqx=out:csv`) → HTML login page (shared drive, blocked). So the ONLY reliable state signal is `session_search`: pull the last leadership interaction (e.g. SBI explanation → Feedback Friday still pending), then compose the check-in as direct questions + that context. Don't burn time parsing hub.html for progress — use it only for structure (what today's guide asks).

4. **When user complains about stale info**, fix immediately and redirect to what they asked about. Don't explain, don't justify, don't apologize more than once.

**Update method:**
```bash
hermes cron list            # get job IDs
hermes cron update --job-id <ID> --prompt "## Updated context with current module..."
```

### Phase 4c: Stalled User Recovery Pattern

When user hasn't touched action tasks for 3+ days (hub shows 0/5 daily steps, empty journal, no actions created):

| ❌ Don't | ✅ Do |
|----------|-------|
| Repeat same reminders louder | Change framing — connect new module content to stalled tasks |
| Accuse "you haven't done anything" | Name stall factually, then offer a new angle |
| Keep using same framework | Introduce a fresh concept for perspective |
| Ignore the stall | Address directly — "5 ngày 0/5 — có chuyện gì?" |

**Techniques:**
- **Hook with new module content**: Deploy a new module even if current tasks aren't done. Fresh concepts often give the insight that unsticks the user.
- **Connect concept → stalled task**: E.g. "Self-Determination Theory says team needs Autonomy, Competence, Relatedness. That Feedback Friday task? It's the gateway to Relatedness."
- **Shrink the ask**: Instead of "do 3 tasks", suggest "1 concept đọc + 1 journal entry + 1 câu hỏi với team" — micro-commitments rebuild momentum.
- **Use the 0/5 tracker as neutral reference**: "Cả tuần 0/5. Có thể bận. Ngày mai chỉ cần 1/5 là khác."

**When to advance despite stalled tasks:**
If Module 1 action tasks (e.g. Feedback Friday, EQ Journal) stall >7 days, introduce Module 3 content anyway. The psychology concepts often provide the insight that unsticks the user. Follow the engagement curve, not the curriculum rigidly.

Also see `references/psychology-of-leadership-concepts.md` for the 7-concept Module 3 content that works well as a re-engagement hook.

### Phase 5: Coaching Style

- **Radical Candor** — care personally + challenge directly
- **Framework-first** — give them mental models (Trust Equation, GROW, SBI, Golden Circle) not just advice
- **Case studies** — real examples (Nadella, Jobs, Netflix, Ferguson, Buffett)
- **Action-oriented** — every session ends with a concrete task
- **Profile-driven** — use the learner's reflection data to personalize every interaction
- **Clarity over cleverness** — when a user says your question is "mơ hồ" or unclear, rephrase it immediately with concrete examples. Never defend the original wording. Use the pattern: vague question → restate with 3 concrete options (e.g. "If X happens, does team learn A, B, or C?").
- **Lead Through Structure** (see `references/lead-through-structure.md`) — when the user manages people who are 5-10+ years older, traditional authority doesn't work. Shift from command-based leadership to structure-based: shared trackers, experience-respecting language, self-committed deadlines.

### Persona Script for Role-Play

When user wants you to act as an experienced leader, use this exact framing:

> "Từ giờ ở group này, em đóng vai leader đã từng:
> - **Startup 3 người** → làm mọi thứ, học cách hire & fire, xây văn hoá từ con số 0
> - **Growth-stage (50-200 người)** → xây quy trình, delegation, giữ chân nhân tài khi công ty lớn nhanh
> - **Enterprise (tỷ đô)** → chiến lược, M&A, leader of leaders, văn hoá ở scale
>
> **Cách em coach:** không lý thuyết suông — em đưa framework + tình huống thực tế em đã trải qua + câu hỏi để anh tự tìm ra đáp án."

### Reflection Analysis Patterns

After the user completes Module 1 reflection, look for these patterns:

| User Says | Underlying Issue | Coaching Direction |
|-----------|-----------------|-------------------|
| "Người giỏi nhất chuyên môn yếu" | Team quality gap → leader does everything → no time to lead | Recruiting, development, or tough conversations to upgrade team |
| "Phản ứng nhiều hơn đáp ứng" | Low self-regulation EQ | Pause 6 seconds before responding; EQ Journal practice |
| Output không đạt → tự làm | Perfectionism leading to micromanagement | Shift from "I'll do it right" to "I'll teach them to do it right" |
| "Quyết đoán chưa đủ" | Low confidence or fear of wrong decisions | Build decision-making frameworks; start with small irreversible calls |
| "Chưa làm cùng mọi người nhiều" | Leader disconnected from team | Increase 1:1 frequency; practice servant leadership |

## Founder/Chủ tịch ôm việc — Delegation Bottleneck (intervention playbook)

Khi user báo sếp/chủ tịch (thường là cha/mẹ) tự làm việc nhỏ vận hành (gọi kho, gọi vận chuyển, giao việc vụn) thay vì tập trung R&D/đối tác, và "bảo rồi giao được 1 thời gian vẫn tự làm lại":

- KHÔNG phải "ham việc" — 4 cơ chế: negative reinforcement (lo âu được giải tỏa = thưởng), negativity bias (nhớ lần hỏng quên lần ngon), bản năng gia đình (bảo bọc vô thức), sợ vô dụng (ngày trống → nhặt việc vụn).
- KHÔNG cấm — cấm = đụng giá trị bản thân → tự ái → bám chặt. Thay thế bằng hệ thống (kênh báo cáo, SOP, case mẫu) + việc lớn đủ đầy có deadline. Lo âu chuyển hướng, không bị xóa.
- Dùng plan 12 tuần 3 giai đoạn + câu nói chuẩn ("Việc này con giao X rồi. Mẹ làm thì X không học được. Lần sau để X, mẹ duyệt giúp con nhé") + KPI (giảm 50% việc nhỏ sau 4 tuần, hết đụng việc vụn sau 8 tuần, ≥1 sản phẩm/đối tác mới sau 12 tuần).

Chi tiết đầy đủ: `references/founder-delegation-intervention.md`

## Founder Identity Transition — Từ "nhà khoa học" sang "người sáng lập" (intervention playbook)

Khi user báo sếp/chủ tịch (thường là cha/mẹ) tự nhận danh xưng khoa học ("nhà khoa học", "người phát hiện") nhưng phát ngôn thiếu cơ sở, không nghe góp ý, gây rủi ro uy tín công ty.

**Khác với delegation bottleneck:** đây không phải chuyện ôm việc nhỏ, mà là identity crisis. Danh "nhà khoa học" là lớp áo bảo vệ giá trị bản thân. Đụng vào = đụng vào lý do tồn tại.

- 4 cơ chế: identity anchoring, Dunning-Kruger + confirmation bias, backfire effect, loss aversion.
- KHÔNG cấm, KHÔNG đối đầu. Xây danh mới cao hơn ("người sáng lập") để họ tự nguyện bỏ cái cũ.
- Cần người thứ 3 (Scientific Officer) — vừa đá vừa thổi còi = "con dạy mẹ" → nổi đóa.
- Briefing 5 phút trước mọi cuộc gặp: 3 ý chính, kỹ thuật để team lo.
- Lộ trình 14 tuần 4 phase: nền tảng → chuyển narrative → củng cố → duy trì.

Chi tiết đầy đủ: `references/founder-identity-transition.md`

## Key Frameworks

| Framework | Application |
|-----------|-------------|
| LEADER FROM WITHIN | L=Limiting Beliefs, E=Emotional Triggers, A=Authentic Values, D=Daily Habits, E=Energy Management, R=Reflection |
| EQ (Goleman) | Self-Awareness, Self-Regulation, Motivation, Empathy, Social Skills |
| Trust Equation | (Credibility + Reliability + Intimacy) / Self-Orientation |
| Golden Circle (Sinek) | WHY → HOW → WHAT |
| GROW Model | Goal → Reality → Options → Will |
| SBI Feedback | Situation → Behavior → Impact |
| Radical Candor | Care Personally + Challenge Directly |
| Tuckman Stages | Forming → Storming → Norming → Performing → Adjourning |
| Change Curve | Shock → Denial → Frustration → Depression → Experiment → Decision → Integration |

## Common Pitfalls

- ❌ Don't use `read_file` for HTML upload — it adds line numbers (1|, 2|...). Use `terminal('cat <path>')` to get raw content.
- ❌ Notion markdown PATCH requires `old_str` field — easier to archive old page and create new one.
- ❌ Avoid overly long theory — keep each module focused on 2-3 frameworks max.
- ❌ Don't skip the reflection phase — it's where personalization happens.
- ⚠️ Cron `attach_to_session: true` works best on Telegram with topic support.
- ⚠️ **Gist preview can't POST to localhost** — htmlpreview.github.io is cross-origin. The Save button on a Gist-previewed page CANNOT send data to a local Python server. Solutions: (a) user opens `http://localhost:PORT` directly (same origin), (b) add a "Download JSON" fallback button that creates a downloadable file, (c) add a "Copy all" button that copies formatted text to clipboard.
- ⚠️ **Re-order modules after reflection** — the initial curriculum order is generic. After the user completes reflection (Module 1), analyze their answers and re-prioritize modules to match their real gaps. E.g. "team yếu" → move Module 4 (People) and Module 7 (Difficult Conversations) earlier.
- ⚠️ **Vòng lặp tiêu cực phổ biến**: "Output không đạt kỳ vọng → tự làm → càng ít lead → càng ít ảnh hưởng". Khi thấy pattern này, coaching hướng đến delegation + people development trước.
- ⚠️ **Nếu reset Gist HTML**: khi upload lại Gist với PATCH, raw_url thay đổi → preview URL cũng đổi. Cập nhật ngay Notion page + báo cho user.
- ⚠️ **Tracker sheet API quirks (Leadership)**: sheet `<SHEET_ID>` (⚡ Tracker — Kết quả, Công việc) nằm trong shared drive, owner `<EMAIL>`. Drive `files.get` by ID có thể trả 404 và Sheets API trả `400 INVALID_ARGUMENT` cho hầu hết range — trong khi Drive `files.list` search vẫn thấy file. Không kết luận "file mất". Tab thật: `'Task'`, `'📋 Dự án'`, `'🎯 Mục tiêu & KQ'` (KHÔNG phải `Tuần` như cron prompt cũ). Nếu không đọc được, dùng `session_search` để dựng lại trạng thái từ các check-in trước. Chi tiết: `references/tracker-sheet-access.md`.

## User Preferences for This Task

- Vietnamese language preferred
- Dark theme HTML (#0a0a0f bg, #e2e2f0 text, #f0c040 accent)
- No AI-looking design — avoid Inter/JetBrains Mono combo, use natural colors
- Practical over theoretical — 70-20-10 rule (70% practice, 20% others, 10% theory)
