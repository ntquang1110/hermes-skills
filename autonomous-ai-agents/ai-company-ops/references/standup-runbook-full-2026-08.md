## Standup cron — runbook chạy + verify (2026-08-14, áp dụng từ 14/08)

Chạy standup KHÔNG chỉ là `python hub/run.py standup` — phải verify từng claim trước khi báo Quang:

1. **git pull --rebase trước.** Nếu bị chặn "unstaged changes" → KHÔNG stash đại trà. Commit riêng file code/docs (hub/*, shared/*, briefing.md) với message rõ, `git push origin HEAD:main`. TUYỆT ĐỐI không `git add -A` (tfo_data/, store/*.json runtime, .watchdog_state.json, lan_chat/ là local/gitignored — commit nhầm = lộ data/token).
2. Chạy `python hub/run.py standup` (python mặc định, không cần .venv cho hub/).
3. **Verify 4 nguồn bằng chứng trước khi tin báo cáo:**
   - `git log --format="%h %ad %s" --date=format:"%Y-%m-%d %H:%M" --all | head -15` — agent nào báo "đã commit/xong" phải có commit tương ứng.
   - `find . -iname "*gtm*" -o -iname "*playbook*" ...` / `grep -rli` — file được nhắc phải tồn tại.
   - `store/tasks.json` (⚠️ là dict `{tasks:[...], next_id}`, KHÔNG phải list — đọc `data['tasks']`) — đối chiếu phase/done_criteria/deadline từng task.
   - Inbox `shared/to_claw.json` + `to_hermes.json` lọc từ ngày standup trước — tin mới nào.
4. **4 pattern lặp lại cần bắt (đều đã dính 14/08):**
   - **Báo done không bằng chứng:** CMO báo "GTM Playbook đã commit" nhưng 0 file/commit trong repo → đánh dấu ⚠️ vi phạm DoD, đòi link/file.
   - **Báo chốt/bàn không bằng chứng:** CTO báo "chốt kiến trúc" nhưng không commit/workspace update → KHÔNG tính là đóng.
   - **Report lệch ngày:** QA ghi "hôm qua 12/08" trong khi standup 14/08 → agent dùng template cũ → nhắc cập nhật đúng ngày. **ROOT CAUSE + FIX (verify 22/08):** `agents/base_agent.py::daily_standup()` + `status_report()` chạy prompt CỨNG `self.think("Hôm qua làm gì? Hôm nay làm gì?")` — **KHÔNG inject ngày hệ thống** → agent tự bịa/giữ nguyên mốc cũ (thực tế dính chuỗi 3 ngày ghi 19/08 dù hôm nay 22/08). Fix: `today = now()` (đã import sẵn từ `hub.store`) rồi `self.think(f"NGÀY HÔM NAY LÀ: {today}...KHÔNG copy report cũ. Kèm bằng chứng commit/file/task_id", temperature=0.2)`. **Patch CẢ `daily_standup()` lẫn `status_report()`** (cùng kiểu lỗi). Verify: `python -c "from agents.base_agent import BaseAgent; print(BaseAgent('CTO').daily_standup())"` phải in đúng ngày hôm nay. Mốc 19/08 cứ tái diễn theo ngày = agent báo mốc quá khứ → chính là dấu hiệu prompt thiếu inject ngày, SỬA CODE chứ đừng chỉ nhắc agent.
   5. **Task xong nhưng phase chưa đóng:** task #15 "Tạo mail" còn planning dù việc đã xong (commit 7c0c410 12/08) → cross-check task phase với git history, đề xuất đóng. **Kiểm tra CẢ việc chưa push (verify 22/08):** task SPIN #21 "Chống lỗi mạng" có commit code xong từ 17/08 (`0069193` retry chunk + queue, verify `git show <hash> -- <file> | grep retry`) nhưng **`git branch -r --contains <hash>` rỗng = chưa push** + phase còn `planning`. Xử lý: `git push origin HEAD:main` → verify `git branch -r --contains <hash>` ra `origin/main` → cập nhật `store/tasks.json` phase → `testing` kèm bằng chứng. Task con SPIN cần "test thật máy Android/cuộc họp" (E2E, mạng yếu thật) thì Hermes KHÔNG bịa bằng chứng — đẩy tới `testing` + ghi rõ cần Quang test, KHÔNG tự đóng `completed`.

   6. **⚠️ Standup None cho TẤT CẢ agents — đọc `store/activity.json` (key `d['activity']`), đọc `resp.text` chứ đừng in `str(e)`:**
      - `401 CreditsError` = **hết credit** → escalate Quang link billing, đừng wake agent.
      - **`429` KHÔNG mặc định hết cung** — có thể chỉ hết quota MỘT endpoint (27/09: `/api/coding/v3/` 429 còn `/api/v3/` 200) → test từng URL riêng, payload THẬT (payload "ok" nhỏ không lộ rate limit). `models 401` = key hỏng; `empty content` = transient, retry cùng endpoint. Bẫy 403: thiếu browser headers (UA/Origin/Referer).
      - → `references/standup-credit-diagnosis-2026-09.md` + `references/bytedance-ark-fallback-2026-09.md` + `references/verify-fallback-chain-2026-09.md` (probe 2 tầng verify fix, bẫy monkeypatch `requests.post` không bị `importlib.reload` gỡ).
- ⏱ Cơ chế chạy standup trong CRON (timeout → background, wake kanban đổi phase, số STALE agent lệch guard, claim bịa) → `references/standup-cron-runbook-2026-09.md`
- 🧮 Dedup 15/10: ngưỡng chuỗi KHÔNG đủ (cùng 1 việc sim 0.30-0.60; khe hở 0.021 mà cả 2 đầu đều trùng thật) → nhóm theo CHỦ ĐỀ; mutation phải nhắm task ĐANG stale, không hardcode kỳ vọng: `references/dedup-threshold-insufficient-2026-10.md`.
- 🔎 Verify wake (ai THỰC SỰ xử lý) + biến output agent thành artifact đã commit/verify_done + agent echo số liệu briefing cũ → `references/standup-agent-output-to-artifact.md`.
5. Flush state file `D:/Hermes Proj/.hermes-state/ai-company.md` + commit briefing.md timestamp (`git add briefing.md && git commit && git push`).

### 🚨 "Cron có chạy không?" + "Chain LLM có sống không?" — chẩn đoán 13/10/2026 (9 ngày 0 commit)

Triệu chứng: guard bình thường, activity.json vẫn có entry mỗi ngày, **nhưng 0 commit suốt 9 ngày** và state file đóng băng.

- **`executions.db` KHÔNG đáng tin** — nó có thể bị reset (13/10 chỉ còn 2 ngày lịch sử; kèm `jobs.json.corrupt-<ts>` trong `~/AppData/Local/hermes/cron/`). Đừng kết luận "cron không chạy" từ DB rỗng.
- **Nguồn thật = file output:** `D:/Hermes/hermes-home/cron/output/<job_id>/<YYYY-MM-DD>_*.md`.
  - File **tồn tại** = cron ĐÃ chạy (kể cả khi chết giữa chừng).
  - Cuối file có khối **`## Error`** = crash ở tầng gọi model → **không bước nào trong prompt được thực thi** (không guard, không standup, không commit). Đây chính là cơ chế "cron chạy mà 9 ngày không commit".
  - Duyệt nhanh cả dải ngày: `for f in $(ls -1 | tail -12); do echo "--- $f"; grep -A3 "^## Error" "$f" | cut -c1-150; done`
- **Đừng tin dòng `Daily standup hoàn thành: N agents báo cáo`** trong `store/activity.json` — nó ĐẾM SỐ AGENT, không đếm báo cáo thật. Phải đọc `standup_results[].report`: nếu là `(LLM trả None)` thì chain chết, báo cáo rỗng. Dòng này còn xuất hiện cả khi 5/5 agent trả None.
- **Chain công ty (`hub/store.py`) có 2 chân, chết độc lập:** OpenCode Go (hết subscription) + ByteDance Ark (fallback).
  - Nếu log CHỈ có `OpenCode API error (...)` rồi `(ByteDance fallback cũng thất bại)` mà **KHÔNG có dòng `[WARN] ByteDance fallback error`** → `_call_bytedance` return None ngay ở bước đọc key (line ~372-374), **chưa hề gọi HTTP**. Nguyên nhân = **`BYTEDANCE_ARK_API_KEY` mất khỏi `.env`**, không phải Ark chặn.
  - Key mất không lấy lại được: `auth.json` chỉ giữ `secret_fingerprint` (sha256). `auth.json → suppressed_sources` ghi `bytedance: ["env:BYTEDANCE_ARK_API_KEY"]` = nguồn key là env và đang bị suppress → dấu hiệu env var đã biến mất.
  - So `.env` mtime với lần fallback OK cuối cùng trong `store/activity.json` (grep `ByteDance fallback thành công`) để tìm thời điểm key bị xoá.
- **command-code là provider CHẠY ĐƯỢC** (`https://api.commandcode.ai/provider/v1`, key env `HERMES_CUSTOM_COMMAND_CODE_API_KEY`). Test tay: thiếu browser headers → **403 Cloudflare code 1010**; `max_tokens` nhỏ (20) → **content rỗng vì reasoning_tokens ăn hết budget** (dùng ≥600 mới thấy nội dung). Cần headers UA + Origin + Referer như bẫy Groq.
- **Guard NO_DC: backfill ngay nhưng TUYỆT ĐỐI không bump `updated_at`** — assert trong script (`assert t["updated_at"] == before`) để chứng minh không che STALE. Verify sau backfill: NO_DC 8→0 **và STALE giữ nguyên 21**.
- **Đo dedup toàn bộ:** `docs/qa/measure_dedup.py` **hardcode 12 task #43-54** → chạy ra số cũ, không thấy thế hệ mới. Dùng `docs/qa/measure_dedup_active.py` (đo mọi draft đang mở) + `docs/qa/mutation_dedup_active.py` (7 check, phải `TONG FAIL = 0`). **Báo MARGIN, không chỉ ngưỡng:** 13/10 khe hở co còn 0.067 (0.625 vs 0.558) so với 0.229 của lô cũ → ngưỡng 0.62 sát mép.

### ⚠️ SỐ ĐI VÀO TÀI LIỆU PHẢI ĐO (01/10 + 02/10/2026)
- **Log đã lọc ≠ log đầy đủ.** Số vào spec/state/briefing phải do script **in ra trực tiếp**, không cộng tay trong đầu từ output một phần. Muốn nói "ở threshold khác ra mấy" → **chạy lại script ở threshold đó**.
- **Đừng vội kết luôn "phiên trước sai"** — chạy lại phép đo trên **cả hai mốc**, và **≥2 phương pháp** rồi mới kết luận. 02/10: sim 0.87 trong briefing 30/09 không khớp cả 3 cách đo (title/desc/ghép) → số cũ thổi phồng, đã sửa.
- **Verify script FAIL → kiểm tra script trước, repo sau**, báo cáo trung thực các FAIL đó.
- **`echo "EXIT=$?"` sau pipe là exit của `tail`** → dùng `${PIPESTATUS[0]}` nếu không sẽ pass giả.
- **Không viết hash commit trước khi commit:** commit → `git rev-parse --short HEAD` → mới patch hash vào tài liệu.
- `store/activity.json` schema phẳng: field **`time`** + **`message`** (không có `ts`/`agent`/`ok`) → tách agent bằng regex trong `message`.
- Chi tiết: `references/standup-number-discipline-2026-10.md`
6. Trong `python -c` script đọc JSON: tránh f-string lồng dấu nháy kép (`f"...{'CÓ' if ...}..."` fail SyntaxError) — dùng `%` formatting hoặc biến trung gian.
7. **⚠️ `briefing.md` body đóng băng nhưng footer tự nhảy mỗi standup → agent dẫn số cũ (lỗi lặp 3 ngày: CMO 01/10, CTO 02/10 dẫn "#8 = 4 ngày" trong khi guard đo 6.0).** Sửa DATA, không nhắc agent. Mỗi standup phải viết lại TOÀN BỘ body bằng số guard hôm nay + thêm dòng "số ở đây là ảnh chụp, muốn số thật tự chạy ops_guard --json". Fix triệt để (chờ duyệt): inject `ops_guard --json` vào `daily_standup()`. Chi tiết + `read_file` báo binary sai + giữ CRLF + schema `activity.json` phẳng + bảng sim đo 3 phương pháp: `references/briefing-staleness-2026-10.md`.
