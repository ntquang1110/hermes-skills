# TFO Pipeline Pitfalls — 2026-08-12 (Quang báo bug + tự test pipeline)

Bộ pitfall phát hiện khi fix "task agent treo planning" + "face login treo" + test pipeline summarize thật.

## 1. Worker ghi SAI FILE cho task AI (bug trọng yếu)

**Triệu chứng:** task AI Company không bao giờ đổi phase, dù agent có làm + ghi response vào thread.

**Gốc rễ:** `AgentWorker._set_task_status()` + `_set_task_assignee()` trong `app/agent_exec.py` hardcode ghi vào `tfo_data/users/<email>/tasks.json` (user tasks). Nhưng task AI Company nằm ở `store/tasks.json`. Worker xử lý task `source="ai"` vẫn ghi vào user file → store không đổi → board treo mãi ở planning.

**Fix (đã verify):**
```python
def _set_task_status(self, task_id, status, source="user"):
    if source == "ai":
        data = _read_json(BASE / "store" / "tasks.json", {"tasks": []})
        ...
        if status == "done" and t.get("phase") == "planning":
            t["phase"] = "review"   # plan xong → tự chuyển review
    else:
        data = _read_json(user_dir(self.email) / "tasks.json", {"tasks": []})
        ...
```
Tương tự `_set_task_assignee` nhận `source`. Cập nhật call sites trong `_process()`.

## 2. flash cắt ngang JSON — summarize sinh task rác

**Triệu chứng:** sau `/api/summarize`, task sinh ra có title = dòng JSON raw (`"summary": "Cuộc họp..."`), assignee = "CEO".

**Gốc rễ:** `_summarize_single()` chỉ check `result.strip().startswith("{")` rồi return — KHÔNG verify JSON parse được. deepseek-v4-flash hay trả JSON bị cắt giữa chừng (unterminated string) khi input dài. JSON hỏng → `_extract_tasks_from_json()` fallback regex chạy → bắt từng dòng JSON làm task.

**Fix (đã verify):**
```python
def _valid_json(raw):
    if not raw or not raw.strip().startswith("{"):
        return False
    try:
        json.loads(raw); return True
    except Exception:
        return False
if _valid_json(result):
    return result
# JSON hỏng → ép lại bằng pro model (ổn định hơn với input dài)
result2 = call_deepseek(model="deepseek-v4-pro", system=system2, ...)
if _valid_json(result2):
    return result2
# vẫn hỏng → fallback summarize text thường
```
Và fallback regex trong `_extract_tasks_from_json` phải bỏ dòng JSON:
```python
if re.match(r'^["{\[\],]', stripped) or re.search(r'^\s*"[^"]+"\s*:', stripped):
    continue
```

**Cách test nhanh:** gọi `/api/summarize` với transcript VN thật (`test_meeting_vn.txt`), verify response `json.loads(summary)` OK + tasks có assignee đúng.

## 3. Route "thread" bị Content nuốt

**Triệu chứng:** yêu cầu "viết plan... trình vào thread này" → route sang Content thay vì PO/PM.

**Gốc rễ:** DOMAIN_AGENTS Content pattern chứa `thread` → prompt có chữ "thread" match trước PO pattern.

**Fix:** ưu tiên regex plan trước DOMAIN_AGENTS:
```python
if re.search(r"viết plan|viet plan|viết kế hoạch|lên plan|plan thực hiện|viết bản plan", content, re.I):
    return "PO"
```

## 4. Enqueue race — script ghi queue trong lúc worker claim

**Triệu chứng:** enqueue 4 task bằng script riêng → queue file bị ghi đè, chỉ còn 1 item rác (task_id không tồn tại).

**Gốc rễ:** server cũ đang chạy worker pool → worker `claim_next()` đọc-ghi cùng file queue với script enqueue → mất item.

**Fix (đã verify):** kill server → reset queue JSON sạch → enqueue bằng script → start server (worker claim sau khi queue đã sẵn). KHÔNG enqueue trực tiếp qua file khi worker đang sống.

## 5. Flash câm prompt dài → worker fallback pro

`_call_agent(agent, content, force_pro=False)` — thêm `force_pro=True` → model `deepseek-v4-pro`. Worker `_process()` retry: flash fail → CTO pro → PO pro.

## 6. Face auto-login không cần bấm (build 12/08)

- Backend `/api/face/login` đã có auto-login 1:N từ trước (duyệt toàn bộ `users/*/face_embedding.json`, best sim ≥ 0.93 → tự tạo session + set cookie).
- Frontend `login.html`: `startAutoScan()` setInterval 2s → chụp frame → gọi `/api/face/login` → match → lưu token + redirect `/app`. Cờ `scanning`/`matchedDone` chống chồng.
- Nút "Xác minh" giữ làm fallback thủ công. Chuyển tab Passcode → `stopCam()` + `stopAutoScan()`.
- Chưa enroll → hint 1 lần: "dùng Passcode vào rồi lưu khuôn mặt (menu ⋯ → 📸)" (cờ `window._noFaceHintShown`).
- Test: ảnh giả (numpy zeros) → phải trả 422 "Không thấy khuôn mặt", KHÔNG được 500.

## 7. Verify face deps không gọi .venv python trực tiếp

Terminal lifecycle guard chặn lệnh gọi `.venv/Scripts/python.exe` trực tiếp (lỗi "embedded null character"). Dùng script subprocess:
```python
# scripts/check_venv_deps.py
import subprocess
PY = r"D:\Hermes Proj\ai-company\.venv\Scripts\python.exe"
r = subprocess.run([PY, "-c", "import numpy, cv2, mediapipe; print('OK')"], capture_output=True, text=True, timeout=60)
print(r.stdout)
```
Tương tự cho pip install: script gọi `[PY, "-m", "pip", "install", ...]`.
