# dithi Exam App — worked example (Aug 2026)

Full reference build of a self-hosted web app: timed multiple-choice exam for 30
candidates, deployed at `https://dithi.thefirstonly.com` (port 5100).

## Project layout

```
D:/Hermes Proj/dithi/
├── server.js              # Node http server (routes array, JSON store, exceljs export)
├── import_questions.py    # xlsx -> data/questions.json (uv run --with openpyxl)
├── add_ingress.py         # CF API merge+PUT (superseded by skill scripts)
├── add_dns.py             # CF CNAME create (superseded by skill scripts)
├── data/questions.json    # 121 câu: Cô Tâm 58 / Cô Minh 49 / Cô Dung 14
├── data/state.json        # runtime: contestants{}, admin_tokens[], exams[]
└── public/
    ├── index.html         # candidate SPA (enter → ready → exam → done)
    └── admin.html         # admin SPA (login → live table → detail → export)
```

## Exam generation

- 30 papers pre-generated at startup; each = 40 câu: Cô Tâm 20 / Cô Minh 15 /
  Cô Dung 5 (ratio config `TEACHER_RATIO` at top of server.js).
- Per question: shuffle [0,1,2,3] order for options, record `correct` as the new
  index. Dedup signature = sorted qids joined `,`; regenerate on collision (cap 200).
- STT 1-30 (STT = số thứ tự dự thi, no password — user rejected CCCD passcode in
  final spec; STT doubles as the candidate code).
- Assignment: first unused exam_id in a Set → unique paper per candidate.

## State machine

```
empty → assigned (enter, paper locked, 30-min hold) → in_progress (start) → submitted
```

- `enforceDeadline`: in_progress + now > started_at + 50min → submitted, auto=true,
  score from saved answers, submitted_at = deadline. Called from save/submit/overview.
- Admin login persists admin_tokens to state.json (this is why patching state.json
  while the server runs gets reverted — see umbrella skill pitfall).

## API surface

- POST /api/enter {stt, token?} — create/resume session, assign paper
- POST /api/start {token} — in_progress, started_at, returns exam payload + deadline
- POST /api/save {token, answers} — draft autosave (client every 15s)
- POST /api/submit {token, answers} — idempotent, score server-side, auto flag
- POST /api/admin/login {password} → token (default `dithi2026`, env ADMIN_PASSWORD)
- GET /api/admin/overview — 30 rows + KPI (done/active/assigned); polls every 5s
- GET /api/admin/detail?stt=N — per-question chosen/correct/is_correct/explain
- GET /api/admin/export — xlsx, 2 sheets: Tổng hợp (30 STT) + Chi tiết đáp án

## Candidate UX (as shipped)

1. Nhập STT 1-30 → Vào thi
2. Trang đệm "Bạn đã sẵn sàng chưa?" → "Vào thi" (bắt đầu countdown)
3. 40 câu, nav grid 1-40 (answered = blue), options A-D, prev/next
4. "Nộp bài" → confirm modal showing unanswered count → nộp luôn
5. Hết giờ → auto nộp (server-enforced)
6. Nộp xong → "Chúc mừng hoàn thành", NO score shown to candidate
7. Refresh/mất mạng → localStorage token resume; STT đang thi chặn người khác;
   STT đã nộp chặn vĩnh viễn

## Reset procedure (for a fresh exam)

```bash
# kill server → delete state → restart → 30 papers regenerate
rm D:/Hermes\ Proj/dithi/data/state.json
cd D:/Hermes\ Proj/dithi && node server.js
```

Test data backup convention: `cp data/state.json data/state_test_backup.json` before
resetting so admin review data survives.

## Deploy record

- Tunnel TQUANG-DELL (0ce9aa47-7d52-4d6a-9a16-13b48c508cff), service token-managed,
  `config_src: cloudflare`, zone `thefirstonly.com` (zone id 09a2d553b4c5ce037065260ea1feb732).
- Ingress v27→v28: `dithi.thefirstonly.com → http://localhost:5100` inserted before
  catch-all. CNAME id cd88b95a69a7fd738989c27592926632.
- Service BINARY_PATH_NAME: `cloudflared.exe tunnel run --token eyJ...` — API-managed,
  never edit local YAML for it.
- Server must be restarted after machine reboot (`cd D:/Hermes Proj/dithi && node server.js`).
