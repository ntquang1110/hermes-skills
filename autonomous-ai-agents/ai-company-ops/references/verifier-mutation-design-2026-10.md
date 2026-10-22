# Verifier: thiết kế mutation + verify chính verifier (standup 17/10/2026)

Bối cảnh: standup cron 17/10 — guard STALE=25 / NO_DC=0 / WAKE=0, 0 task đóng, 0 commit mới.
Verifier: `docs/qa/verify_standup_2026-10-17.py` (21 assertion, 0 FAIL, 3/3 mutation bắt được).
Bài học áp dụng cho MỌI standup sau, không riêng ngày này.

## 1. Mutation phải ĐỔI TRẠNG THÁI PHÂN LOẠI (mutation yếu = PASS giả)

- ❌ Sai (đã dính 17/10): lùi `updated_at` của **#64** (task ĐANG stale, 2.9 ngày) thêm 5 ngày → guard vẫn trả `stale=25` → script báo "guard MÙ". Thực ra phép thử **không đổi được phân loại nào**: #64 vốn đã nằm trong tập stale, già thêm không thêm id mới.
- ✅ Đúng: muốn test "thêm 1 id vào STALE" → **mở lại một task `completed`** thành `planning` + `updated_at` = now−5d → `stale 25→26`.
  ```python
  M3_ID = sorted(t["id"] for t in load_raw()["tasks"] if t.get("phase") == "completed")[0]
  def reopen_old(d):
      for t in d["tasks"]:
          if t["id"] == M3_ID:
              t["phase"] = "planning"
              t["updated_at"] = (datetime.datetime.now() - datetime.timedelta(days=5)).strftime("%Y-%m-%d %H:%M:%S")
  ```
- Bộ 3 mutation chuẩn (đo 17/10, cả 3 bắt được):
  1. **M1** xoá `done_criteria` #43 → `no_dc 0→1`
  2. **M2** bump `updated_at` #47 (đang stale) lên now → `stale 25→24` (chứng minh bump = che STALE)
  3. **M3** mở lại task `completed` → `planning` cũ 5 ngày → `stale 25→26`
- Nguyên tắc chung: mutation chỉ có giá trị khi nó **dịch chuyển tập id** hoặc **đổi cờ**. Mutation trên phần tử đã thuộc tập = no-op.

## 2. Assertion đếm LOG phải đếm SET AGENT, không đếm số dòng

- Tình huống 17/10: chạy `python hub/run.py standup` **2 lần** (lần 2 để lưu artifact `docs/qa/standup_20261017_reports.json` vào git) → `store/activity.json` có **10 dòng** `[OK] Gemini fallback thành công` và 10 dòng `thiếu BYTEDANCE_ARK_API_KEY`.
- ❌ `len(ok_gem) == 5` → **FAIL giả** (got 10). Đây là lỗi của SCRIPT, không phải repo.
- ✅ Đếm agent distinct:
  ```python
  import re
  def _agents(msgs):
      out = set()
      for a in msgs:
          m = re.search(r"\(([A-Za-z0-9 ]+)\)", a.get("message", ""))
          if m: out.add(m.group(1))
      return out
  ok_gem = _agents([a for a in today if "[OK] Gemini fallback thành công" in a["message"]])
  chk("5/5 agent gánh bằng Gemini", ok_gem == {"CTO","Dev1","QA","CMO","Content"}, sorted(ok_gem))
  ```
- Quy tắc rộng: assertion dạng `== 5` gắn với **số lần chạy** sẽ vỡ ngay khi một bước chạy lại (retry, lưu artifact, chạy tay + cron). Assert trên **tập đối tượng** hoặc trên `>=`.

## 3. Verify CHÍNH verifier (script tạm `%TEMP%/hermes-verify-*.py`)

Chưa từng thấy FAIL = chưa phải bằng chứng. Verifier phải được chứng minh là **biết FAIL** ở tầng ngoài, không chỉ tự khai mutation nội bộ.

Các bước (đã chạy thật 17/10 — 8/8 PASS, exit 0):

1. Backup **bytes gốc**: `shutil.copy2(TASKS, bak)` — KHÔNG `json.dump` (sẽ đổi CRLF/format).
2. **(a)** chạy verifier trên dữ liệu thật → assert `rc == 0`, stdout chứa `"21 assertion, 0 FAIL"` và `"0 mutation guard MU"`.
3. **(b)** mutation ở **tầng NGOÀI**: sửa `store/tasks.json` (vd mở lại 1 task completed giữa danh sách thành stale) → chạy verifier → phải `rc == 1` **và** stdout chứa ĐÚNG TÊN assertion sai (`FAIL: stale: so luong == 25 ... got 26`). Chỉ assert exit code là chưa đủ — phải thấy tên.
4. **(c)** `finally: shutil.copy2(bak, TASKS)` → assert `sha256 == sha0`.
5. Chạy xong **xoá ngay** script tạm.

⚠️ **Bẫy thứ tự khôi phục:** verifier tự mutate rồi tự restore `store/tasks.json` bằng `ORIG_RAW` của chính nó. Khi ta đã inject mutation ngoài, bản `ORIG_RAW` đó là **bản đã mutate** → verifier sẽ "khôi phục" về bản hỏng. Vì vậy backup bytes ở tầng ngoài là bắt buộc, và restore phải nằm trong `finally`. Đo lại sha256 ngay sau khi chạy để chắc chắn repo không bị bỏ quên ở trạng thái mutate.

## 4. Đếm lone LF cho file CRLF

- ❌ `raw.replace(b'\r\n', b'\n').count(b'\n')` → đếm luôn phần vừa convert → báo "CRLF 87 / lone LF 87" (vô nghĩa, gây hoảng loạn giả).
- ✅ `raw.count(b'\n') == raw.count(b'\r\n')` ⇒ mọi LF thuộc CRLF, không có lone LF.
- `write_file` trên `briefing.md` **giữ CRLF** (17/10: 8580 bytes, 87 CRLF) — không cần convert tay.

## 5. Chạy lệnh: exit code sau pipe

- `python docs/qa/verify_...py | tail -30; echo "EXIT=$?"` → `$?` là exit của `tail`, luôn 0.
- Dùng `echo "EXIT=${PIPESTATUS[0]}"` (bash) — 17/10 dùng cách này nên bắt được exit 1 đúng lúc verifier còn 2 FAIL.

## 6. Commit evidence (đừng để trong Temp)

`git add` **đúng file mình tạo**: `briefing.md` + `docs/qa/verify_standup_<ngày>.py` + `docs/qa/standup_<ngày>_reports.json` + `docs/qa/guard_<ngày>.json`.
Untracked rác KHÔNG được đụng: `store/tasks.json.bak_backfill_dc_20260925`, `tfo_data/context_scan.json`, `tfo_data/uploads/*.transcript.txt` — tuyệt đối không `git add -A`.
Xác nhận push: `git branch -r --contains HEAD` phải ra `origin/main` (17/10: `c1cf85c`).
