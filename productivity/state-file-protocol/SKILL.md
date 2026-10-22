---
name: state-file-protocol
title: State File Protocol (SFP)
description: "Keep agent context short by storing long-horizon project state in external STATE files instead of letting the conversation grow unbounded. Read at session start, flush at turn end, /new anytime."
version: 1.0.0
author: agent
created_by: agent
tags: [hermes, context-management, state-files, workflow, multi-session, projects]
---

# State File Protocol (SFP)

User-requested workflow (Quang, 2026-08-04): **never throw the whole conversation at the
model.** Everything long-horizon lives in a compact STATE file per project; the conversation
context stays small (system prompt + STATE + current turn + recent tool output).

Why it exists: an unbounded conversation hit 266K tokens on a custom LAN provider that
silently returns empty above ~200K (see `hermes-telegram-gateway` skill →
`references/empty-response-fallback-config.md`, Cause 3). SFP is the structural fix:
context never grows big enough to trigger provider dead zones.

## Trigger

- Work in any project under `D:/Hermes Proj/` (volden-ops-web, ai-company, meTelligent,
  TFO, KFlow, threads-schedule, ...) — read the project's STATE file at session start and
  flush at turn end.
- **Any chat session (Telegram DM/group, Feishu, CLI)** — read the chat STATE file at
  session start and flush at turn end. Auto-load enforced via `D:/Hermes Proj/AGENTS.md`
  (injected into every session whose cwd resolves there; `terminal.cwd` is set to
  `D:/Hermes Proj` for the gateway).

## Protocol (5 rules, mandatory)

1. **Start session** → read `D:/Hermes Proj/.hermes-state/chat/_INDEX.md` to map the
   current chat, then read the chat's STATE file
   (`D:/Hermes Proj/.hermes-state/chat/<platform>-<name>.md`). If the chat maps to a
   project, also read `D:/Hermes Proj/.hermes-state/<project>.md`. Do NOT rely on chat history.
2. **Done with a piece of work** → update STATE immediately (overwrite, keep <100 lines).
3. **End of turn** → flush STATE: update "Tiến độ" and "Bước tiếp theo".
4. **Long tool output** (logs, diffs) → never copy into STATE; write conclusion + file path only.
5. **/new anytime** — reading STATE gives full context; nothing is lost.

## File layout

```
D:/Hermes Proj/.hermes-state/
├── README.md          # protocol definition (source of truth)
├── TEMPLATE.md        # blank template to copy per project
├── <project>.md       # one STATE file per project
└── chat/              # chat-level STATE files (added 2026-08-05)
    ├── _INDEX.md      # map chat name → file + project
    ├── TEMPLATE.md    # blank template for chat state
    └── <platform>-<name>.md  # e.g. telegram-dm-quang.md, telegram-group-volden.md
```

### Chat STATE file (add to layout above)

```markdown
# STATE: Chat <Tên hiển thị / chat ID>
Cập nhật: <YYYY-MM-DD HH:MM>

## Ngữ cảnh
- <ai chat, mục đích cuộc chat>

## Project liên quan (nếu có)
- <tên project> → đọc thêm .hermes-state/<project>.md

## Đang bàn
- <topic hiện tại, 1-3 dòng>

## Đã chốt
- <quyết định + lý do ngắn>

## Bước tiếp theo
- <việc kế, 1 dòng>
```

Rules for chat STATE files:
- Name by platform + display name (`telegram-dm-<name>.md`, `telegram-group-<name>.md`, `feishu-<name>.md`); write the real chat ID inside `## Ngữ cảnh` (display names can collide).
- **Do NOT create an empty file for a new chat** — only create when there is content worth remembering (work discussion, partner, decision). Empty files are noise.
- Chat maps to a project → reference it in `## Project liên quan` so the agent reads both files.
- Update `_INDEX.md` whenever a chat file is created.

STATE file structure (keep each section ≤5 bullets, Vietnamese with diacritics):

```markdown
# STATE: <Tên dự án>
Cập nhật: <YYYY-MM-DD HH:MM>

## Mục tiêu
- <1 dòng>

## Tiến độ
- [x] <việc đã xong, 1 dòng>
- [ ] <việc đang làm>

## Quyết định đã chốt
- <quyết định + lý do ngắn>

## Đang chờ / Blockers
- <cái gì đang chặn>

## Bước tiếp theo
- <việc kế tiếp, 1 dòng>
```

## Install into a new project

1. Copy `TEMPLATE.md` → `.hermes-state/<project>.md`, fill from real data (git log, memory, docs — never invent).
2. Add a `## 0. STATE FILE PROTOCOL (BẮT BUỘC)` section at the top of the project's
   `AGENTS.md` / `agents.md` / `briefing.md` with the 5 rules + pointer to the README.
3. Already installed (2026-08-04): volden-ops-web (`agents.md` §0.0), ai-company (`briefing.md` §0), meTelligent (`AGENTS.md` §0).
4. Chat-level auto-load (2026-08-05): `D:/Hermes Proj/AGENTS.md` (cấp cha) + `terminal.cwd: D:/Hermes Proj` — mọi session gateway (Telegram/Feishu/CLI) tự đọc chat STATE. Nếu gateway chạy với cwd khác, file này không auto-load → kiểm tra lại `terminal.cwd`.

## Bảo trì: tạo state files cho toàn bộ chat từ state.db

Khi user yêu cầu "đọc toàn bộ chat, tổng hợp context, lưu state files" — KHÔNG đoán từ log gateway (log chỉ có chat ID, thiếu tên). Làm theo trình tự:

1. **Enumerate chat từ `state.db`** (bảng `sessions` có `chat_id`, `display_name`, `chat_type`, `message_count`, `last_activity_at`):
   ```sql
   SELECT chat_id, chat_type, display_name, COUNT(DISTINCT id) n_sessions,
          MAX(last_activity_at) last_activity, SUM(message_count) total_msgs
   FROM sessions WHERE chat_id IS NOT NULL
   GROUP BY chat_id, chat_type, display_name ORDER BY last_activity DESC
   ```
   DB path: `C:\Users\NTQUANG_DELL\AppData\Local\hermes\state.db`. `sessions.json` là mirror LEGACY chỉ có chat đang active — không đủ.

2. **Dump context từng chat** bằng script `scripts/dump_chat_context.py <chat_id>` (in 12 sessions gần nhất + messages user/assistant của session mới nhất). Script đọc trực tiếp DB, không cần gateway.

3. **Spawn subagents song song** chia theo nhóm chat (3-6 chat/task): mỗi đứa dump → tổng hợp → ghi `chat/<platform>-<name>.md` theo TEMPLATE + cập nhật `_INDEX.md`. Truyền đủ context: DB path, script path, template, quy tắc (tiếng Việt có dấu, không file rỗng, <15 dòng).

4. **Verify**: đọc lại từng file mới tạo (không tin self-report của subagent), check đúng template + không rỗng.

## Verify auto-load (sau khi set terminal.cwd + tạo AGENTS.md)

Test bằng session thật, không chỉ `build_context_files_prompt`:
```bash
cd "D:/Hermes Proj" && hermes chat -q "Bắt đầu session theo STATE FILE PROTOCOL. 1) Em có đọc AGENTS.md không? 2) Đọc chat/_INDEX.md liệt kê chat state files?"
```
Pass khi agent trả lời: đã load AGENTS.md + đọc đúng _INDEX.md + nắm context cũ. Nếu fail → check `terminal.cwd` trong config (phải là `D:/Hermes Proj`, gateway bridge thành `TERMINAL_CWD`).

## Resume việc dở khi câu hỏi mơ hồ ("check xem được chưa", "tiếp tục đi")

Khi user hỏi kiểu "em check xem được chưa" mà không nói check cái gì (desktop session, không
có chat state file riêng): xác định việc đang dở bằng trình tự, KHÔNG hỏi lại nếu có thể suy ra:

1. `session_search()` (browse, không query) → session gần nhất + title + last_active. Session
   đó là nguồn việc đang dở.
2. Đọc session: `session_search(session_id=...)` trả first 20 + last 10 messages; nếu output
   >100K bị persisted → `tail -c 12000 <file>` xem message cuối (patch/verify gì vừa chạy).
3. `ls -lt` folder project nghi vấn → file mtime gần nhất khớp last_active session = artifact
   đang dở. Đối chiếu size file với size trong verify log cuối (lệch = có sửa sau verify).
4. Verify artifact bằng python (HTML: `<div` vs `</div>`, số section, em dash, emoji, marker
   còn sót, dấu VN). Mở `open_preview` cho user xem trực tiếp.
5. Báo trạng thái + hỏi xác nhận 1 câu ngắn nếu vẫn có nhiều ứng viên ("đang hỏi việc A hay B?").

Rule: luôn kiểm tra state files + session_search TRƯỚC, hỏi lại CHỈ khi có ≥2 ứng viên khả dĩ.

## Pitfalls

- STATE files are project-wide, shared by multiple agents → one file per project prevents conflicts; never put per-session noise in them.
- Don't let STATE grow past ~100 lines — that defeats the purpose. If a section exceeds 5 bullets, condense.
- Ghi tiếng Việt có dấu (user rule: all Vietnamese output must have diacritics).
- STATE is a pointer + conclusion store, NOT a log: raw tool output stays in session DB, not in the file.
- **SAFE FILE EDITING — use `patch`, not `write_file`, for multi-section files.** When editing a large file with multiple independently-maintained sections (e.g. a combined briefs file with Research, EZ80-Start, EZ80-Sow sections), `write_file` overwrites the ENTIRE file — truncating every section you didn't explicitly include. This is catastrophic for 100K+ char files. Instead: (a) use `skill_manage(action='patch')` or the direct `patch` tool for find-and-replace on only the targeted section, (b) if you must use `write_file`, first re-read the full file with `read_file(path, offset=1, limit=999999)` to confirm you have the complete content in context, (c) for section-level edits, extract the old section content via `read_file`, modify it in isolation, then patch-replace it. The `write_file` tool warns "was last read with offset/limit pagination (partial view). Re-read the whole file before overwriting it." — **never ignore this warning.**
- **read_file báo "Binary file" cho .md state:** file có thể bị nhiễm UTF-16 BOM từ lần ghi trước (đã gặp với `chat/telegram-group-hermes-meeting-note.md` 15/08). Đừng bỏ qua — đọc bằng terminal: `head -c 3000 file | iconv -f UTF-16 -t UTF-8 2>/dev/null || head -c 3000 file` (fallback về UTF-8 plain nếu iconv fail). Nội dung vẫn đọc được, chỉ là encoding quirk. **Nhánh thứ hai (gặp 18/10/2026 với `docs/05-plan-do-trung-khop-co-quan.md`): file là UTF-8 THUẦN** (kiểm bằng `python -c "d=open(p,'rb').read(); print(d.count(b'\x00'))"` → 0 null, không control char, lệnh `file` cũng báo "UTF-8 text") nhưng `read_file` vẫn trả `is_binary: true`. Nhánh này **đừng dùng iconv** (sẽ làm hỏng dấu) — đọc bằng python:
  ```bash
  python -c "import sys; sys.stdout.reconfigure(encoding='utf-8'); print(open('<file>',encoding='utf-8').read())"
  ```
  và khi **append** vào file đó thì khớp line-ending bằng `open(p,'w',encoding='utf-8',newline='')` + `\r\n`, rồi verify bằng `git diff --numstat` (cột deletions phải = 0).
- **Script path của skill có thể đã sang ổ D** (junction từ 10/08/2026): path C: trong skill cũ có thể fail. Trước khi báo "không có script", chạy `find D:/Hermes/hermes-home/skills -name '<tên script>'` — rất nhiều script (unslop-html.py, content-upload.py...) đã nằm ở D: qua junction.
