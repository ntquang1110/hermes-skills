# Standup dài ngày khi hết credit + fix briefing.md trong cron (2026-09-20)

Trích từ standup cron 20/09 — ngày thứ 10 OpenCode Go hết credit liên tiếp (09/09 → 20/09).

## Tín hiệu
- `python hub/ops_guard.py --json` → STALE 5 (#8 QA 10.0d có DC + #43-46 planning 15.8d NO DC), NO_DC 4, WAKE 0. Đếm tăng đều 0.8-1.0d/ngày.
- `python hub/run.py standup` → 5/5 agent `(LLM trả None)`. `BaseAgent("CTO").think("OK")` cũng None → credit hết thật, không phải transient.
- HEAD `6d368af` briefing 20/09, commit mới nhất `92f84df` pivot 15/09 — không có code mới 5 ngày.

## Pitfall: cập nhật briefing.md timestamp trong cron

**Thử `sed -i "s/^> Standup timestamp:.*/…/" briefing.md` → FAIL** `unknown option to s` vì dòng mới chứa URL `https://opencode.ai/...` có nhiều `/` làm vỡ delimiter `s///`.

**Thử `python replace(old_substring, new, 1)` trên substring `> Standup timestamp: 2026-09-15 (cron).` → patch nửa vời**: `t.split("\n")[2]` là dòng dài 400 ký tự, replace substring chỉ đổi đầu dòng → đuôi cũ (mô tả 15/09) còn dính lại, tạo dòng lai 2 timestamp.

**Fix đúng — ghi đè nguyên dòng `lines[2]`:**
```python
import pathlib
p = pathlib.Path(r"D:/Hermes Proj/ai-company/briefing.md")
lines = p.read_text(encoding="utf-8").splitlines()
lines[2] = "> Standup timestamp: 2026-09-20 (cron). ⚠️ OpenCode Go VẪN HẾT CREDIT ngày thứ 10 liên tiếp (09/09 → 20/09, think() None 5/5) — STALE=5 (#8 QA 10.0d có DC + #43-46 planning 15.8d NO DC), NO_DC=4. HEAD 5732150 (briefing 19/09), commit mới nhất 92f84df pivot 15/09. Chờ Quang nạp credit: https://opencode.ai/workspace/wrk_01KS52FWVYXBS15WZAJRJFVB34/billing. Đọc state file mới nhất: D:/Hermes Proj/.hermes-state/ai-company.md"
p.write_text("\n".join(lines), encoding="utf-8")
```
Chạy qua `write_file` + `python Temp/fix.py` (không dùng `sed`, không dùng `execute_code` trong cron).

## Quy tắc verify áp dụng
- Script verify đặt ở `C:\Users\...\AppData\Local\Temp\hermes-verify-*.py` (cron mode), không đặt trong repo `Temp/` hay `/tmp` (Windows/MSYS path mismatch).
- 13/13 PASS = briefing/state/git HEAD/ops_guard khớp — chỉ là ad-hoc focused verification, chưa phải suite green.
