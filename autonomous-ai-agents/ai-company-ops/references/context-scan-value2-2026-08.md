# Context Scan — value #2 (quét bối cảnh công ty → hỗ trợ quyết định)

Xây dựng 28/08: module đọc data THẬT từ workspace user (`tfo_data/users/<san_email>/`:
meetings/tasks/projects/goal) → DeepSeek tổng hợp thành `{headline, status, problems[], proposals[]}`
→ hiển thị Dashboard Company + push Telegram, chạy định kỳ bởi cron silent-watchdog.

## File

- `hub/context_scan.py` — CLI + thư viện: `read_workspace(workdir)` → `build_brief(ws)` →
  `synthesize(brief)` (deepseek-v4-pro, response JSON) → `run(email)`. Lưu `tfo_data/context_scan.json`.
- `hub/aggregate.py` — thêm `_read_context_scan()` đọc json trên → nối vào `generate_dashboard_data()["context_scan"]`.
- `dashboard/index.html` — card `🧭 Context Scan` (TÌNH HÌNH | VẤN ĐỀ | ĐẦU RA QUYẾT ĐỊNH).
- `app/tg_push.py` — `send_context_scan(headline, status, problems, proposals, source)`.
- `~/AppData/Local/hermes/scripts/context_scan_push.py` — cron entry (silent watchdog).
- Cron job `ai-company-context-scan` (mỗi 360m, no_agent=true, deliver origin).

## ĐIỂM MẤU CHỐT — dedup data nguồn, KHÔNG dedup synthesis (pitfall đã dính)

- **Sai (spam vô hạn):** so hash của `synthesis` (headline/status) làm "đã push chưa".
  → DeepSeek sinh headline KHÁC mỗi lần chạy dù data không đổi → hash luôn đổi → push mỗi tick.
- **Đúng:** hash **brief đầu vào** (data nguồn). Trước khi gọi LLM: đọc workspace → build_brief →
  `sha256(json.dumps(brief, ensure_ascii=False))` → so với state. Bằng nhau → return silent (không gọi LLM,
  không push). Khác → chạy LLM + push + lưu hash mới.

## Pitfall — `str.__hash__()` ngẫu nhiên hóa giữa các lần chạy

Python `X.__hash__()` cho str KHÔNG ổn định giữa các process (PYTHONHASHSEED random mỗi lần chạy)
→ dùng làm dedup key sẽ luôn khác → luôn push. **Bắt buộc dùng `hashlib.sha256(...).hexdigest()`.**
(Bug này đã suýt gây spam Telegram vô hạn.)

## Pitfall — Telegram parse_mode Markdown 400

Text từ LLM chứa `_`, `*`, dấu nháy → `parse_mode=Markdown` trả 400
`can't parse entities: Can't find end of the entity starting at byte offset 34`.
Fix: dùng `parse_mode="HTML"` + `html.escape(str(s or ""), quote=False)` cho MỌI nội dung động
(headline, status, problems, proposals), chỉ để thẻ `<b>` cố định. Verify bằng cả HTTP 200 lẫn `r.json().get("ok")`.

## Pitfall — MSYS path vào sys.path KHÔNG resolve trong Windows Python

`sys.path.insert(0, "/d/Hermes Proj/ai-company")` (MSYS style, có space) khi chạy script bằng
Windows Python qua route khác → `ModuleNotFoundError` dù file tồn tại. Fix:
`REPO = os.path.abspath("D:/Hermes Proj/ai-company")` rồi `sys.path.insert(0, REPO)` +
`os.path.join(REPO, "hub")` + `os.path.join(REPO, "app")`.

## Cron path — script phải relative

Khi tạo cron no_agent + script: path phải **relative tới** `~/AppData/Local/hermes/scripts/`
(ghi đúng filename, `context_scan_push.py`), KHÔNG absolute. Absolute bị reject
("Script path must be relative to ~/.hermes/scripts/").

## Dashboard server.py — không cần restart cho data mới

`server.py` gen `company-data.json` MỖI request bằng `importlib` (module load từ disk mỗi lần,
line ~60). Nên thêm key mới vào aggregate → dashboard có ngay, KHÔNG restart server.
Verify: curl login (passcode <PASSCODE>) → `company-data.json` chứa `context_scan`.

## Verify nhanh

1. `python hub/context_scan.py` → in headline/vấn đề/đầu ra (giọng người thật, bám data).
2. `python context_scan_push.py` lần 1 → push HTTP 200; lần 2 → **silent** (đó là bằng chứng dedup đúng).
3. `curl -s -b cookie localhost:8090/` → HTML chứa `contextScanBody`; `/company-data.json` chứa `context_scan`.
4. Trích `<script>` + `node --check`; đếm `<div` == `</div>` (142/142 sau build 28/08).