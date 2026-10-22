## ⚠️ Inbox files PHẢI tracked trên git — đừng gitignore (pitfall 2026-08-06, suýt vỡ kênh)

- Cơ chế inbox Hermes↔Claw **đồng bộ QUA GIT**: `send()` tự commit+push, `read()` tự pull → 2 máy sync.
- **Lỗi đã mắc:** tưởng bỏ track `shared/to_claw.json` + `shared/to_hermes.json` để chống lộ token → nhưng chính điều đó LÀM VỠ KÊNH (file không còn push lên git → bên kia không nhận). **PHẢI track lại + commit.**
- **Hệ quả kép:**
  1. Inbox files GIỮ TRACKED (kênh hoạt động) — nhưng vì chúng nằm trên GitHub → **KHÔNG BAO GIỜ gửi token/credential qua inbox**. Token git → Claw tự lấy bằng `git remote get-url origin`.
  2. Nếu lỡ gửi token qua inbox → xóa token khỏi body message TRƯỚC khi commit lại, đừng commit file chứa token.
- Verify sau khi đổi gitignore: `git check-ignore shared/to_claw.json` phải trả non-zero (KHÔNG ignore).

### Meeting note JSON — LLM summarize KHÔNG ổn định giữa các lần chạy (2026-08-06, demo thật)

Cùng transcript v8 chạy `/api/summarize` 2 lần → lần 1 JSON chuẩn (2 task đủ assignee+deadline "thứ 7"), lần 2 ra 4 task, gán "Gọi cho mẹ → Anh Mão" (sai — phải Quang), 3/4 task thiếu deadline. LLM sinh nội dung không deterministic → kết quả là DRAFT, cần tầng stabilizer trước khi lưu/trình:

- **Heuristic fix sai người gán:** task chứa "gọi mẹ/thuyết phục mẹ/trao đổi mẹ" → assignee=Quang; "tìm trại" → anh Quân; "công thức/mẫu" → anh Dương.
- **Fallback deadline:** transcript có "chốt sáng thứ 7" → task thiếu deadline gán "Thứ 7".
- **Chạy 2 lần + chọn bản tốt hơn** (nhiều task đủ assignee+deadline) nếu pipeline quan trọng.
- **Cấu trúc lưu meeting note chốt:** `meetings.json` lưu `summary` (text) + `issues[]` + `decisions[]` + `tasks[]` (title/assignee/deadline) + `notes_url` — không chỉ 1 chuỗi summary text.
- **PITFALL JSON CẮT NGANG → task rác (12/08, test thật):** `_summarize_single()` chỉ check `startswith("{")` → deepseek-v4-flash trả JSON bị cắt giữa chừng (unterminated string) khi input dài → `json.loads` fail → `_extract_tasks_from_json()` fallback regex chạy → bắt từng dòng JSON raw làm task (title = `"summary": "Cuộc họp..."`, assignee = "CEO"). Fix 2 lớp:
  1. `_summarize_single`: define `_valid_json(raw)` = `json.loads` thật (không chỉ startswith), JSON hỏng → ép lại bằng `call_deepseek(model="deepseek-v4-pro", ...)` (pro ổn hơn) tối đa 3 lần, vẫn hỏng → fallback summarize text thường.
  2. `_extract_tasks_from_json` fallback regex: bỏ dòng JSON — `if re.match(r'^["{\[\],]', stripped) or re.search(r'^\s*"[^"]+"\s*:', stripped): continue`.
  - Dọn task rác đã sinh: lọc title bắt đầu bằng `"` hoặc chứa `"summary"`/`"tasks"`.
  - Chi tiết + code → `references/tfo-provider-transient-2026-08.md`.
  - **Credit exhaustion diagnosis + recovery:** xem `references/provider-credit-failure.md` (phân biệt 401 credit vs 400 MissingSessionID, link billing, provider fallback options).
