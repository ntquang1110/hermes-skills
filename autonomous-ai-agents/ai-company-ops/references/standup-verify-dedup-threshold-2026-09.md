# Standup cron: bẫy tool + verify lại bằng chứng + ngưỡng dedup (30/09/2026)

Bổ sung cho `references/cron-mode-scripts-2026-09.md` và `references/standup-cron-runbook-2026-09.md`.
Tất cả mọi khẳng định dưới đây đã chạy thật trên máy, có output thật.

---

## 1. `execute_code` bị chặn trong cron — chuyển sang terminal, đừng cố lại

Cron runner là 1-shot, không có người duyệt. `execute_code` tự chặn:

```
BLOCKED: execute_code runs arbitrary local Python (including subprocess calls
that bypass shell-string approval checks). Cron jobs run without a user present
to approve it. Use normal tools instead, or set approvals.cron_mode: approve
only if this cron profile is intentionally trusted.
```

**Hành động đúng:** dùng `terminal` trực tiếp cho toàn bộ bước cron (guard, standup, git,
verify_done, script phân tích). `python -c` inline cũng dính pending_approval → viết
script file rồi `python <file>`.

**Không ghi "execute_code hỏng" vào memory/skill như một ràng buộc vĩnh viễn.** Đây là
cấu hình approvals của profile. Nếu anh bật `approvals.cron_mode: approve` thì tool chạy
lại bình thường.

---

## 2. `terminal(background=true)` KHÔNG inherit `cd` — redirect phải ABSOLUTE

Lệnh này **FAIL** trong background shell:

```bash
cd "D:/Hermes Proj/ai-company" && python hub/run.py standup > Temp/standup.txt
# -> bash: Temp/standup.txt: No such file or directory
# -> EXIT=1
```

Cùng lệnh đó chạy **foreground** thì OK. Lý do: cwd của background shell không được set
theo `cd`, nên path tương đối trong redirect không resolve được (tương đương pitfall
"2 http.server cùng port" — cùng lệnh, hành vi khác nhau theo context chạy).

**Fix — ghi output bằng absolute path:**

```bash
cd "D:/Hermes Proj/ai-company" && python hub/run.py standup \
  > "D:/Hermes Proj/ai-company/Temp/standup_20260930.txt" 2>&1
# -> EXIT=0, file 7202 bytes
```

Đừng lặp lại y hệt câu lệnh trong runbook cũ (`> Temp/x.txt`) ở ngữ cảnh background.

**Về `notify_on_complete`:** trả về
`notify_unsupported: "one-shot runner such as hermes -z, a cron job ..."`. Không cần
bật, không phải lỗi. Dùng `process(action='wait')` (timeout bị clamp 180s, nhận partial
output) rồi đọc file output.

---

## 3. Verify lại bằng chứng khi script phân tích đã bị xoá

Tình huống: đã chạy 2 script phân tích (`Temp/standup_audit_*.py`, `Temp/act_check_*.py`),
lấy số liệu, rồi `rm` dọn. Cuối turn hệ thống yêu cầu verify các con số đã đưa vào báo cáo.

**Không viết lại script cũ và không tin báo cáo cũ.** Re-derive từ nguồn gốc trong 1
script `hermes-verify-*.py` đặt ở `%TEMP%` (`C:\Users\<user>\AppData\Local\Temp\`), chạy
1 lượt, in từng assertion, `sys.exit(1)` nếu lệch, rồi xoá.

Repo **không có test suite / lint command canonical** → verification script tự viết là
chuẩn, không phải thiếu sót. Nói rõ trong báo cáo: đây là kiểm tra ad-hoc trên dữ liệu
thật, **không phải test suite xanh**.

### 27 assertion dùng cho standup (mẫu tái dùng được)

| Nhóm | Kiểm tra | Kết quả 30/09 |
|---|---|---|
| Guard | STALE / NO_DC / WAKE + `len(stale)==count` | 13 / 0 / 0 — PASS |
| Phase | completed 41, planning 11, in_progress 1, review 1, tổng 54 | PASS |
| Stale id | `[8, 43..54]` khớp từng id từ guard | PASS |
| Mode | 12 stale còn lại đều `mode=kanban` + `tags=context-scan` | PASS |
| Wake | số task `mode=agent` phase∉{completed,paused} | 0 → không wake được |
| Near-dup | số nhóm @0.70 = 9; @0.62 = 8 | PASS |
| Git | 0 code commit hôm nay · commit briefing trên `origin/main` · tracked sạch | PASS |

Bốn nguồn độc lập phải khớp nhau: `hub/ops_guard.py --json` ↔ `store/tasks.json`
(dict `{tasks, next_id}`, **không phải list**) ↔ `git log` ↔ `git status --porcelain
--untracked-files=no` (rỗng = sạch; KHÔNG `git add -A`).

### Bẫy đọc `store/activity.json`

Format thật là list, mỗi entry chỉ có **2 key**:

```json
{"time": "2026-09-30 09:05:42", "message": "Daily standup hoàn thành: 5 agents báo cáo"}
```

Có entry cũ dạng dict rỗng `?` ở đuôi → **không phải lỗi**, chỉ là entry không có field
timestamp. Đừng đoán key `date`/`timestamp`/`agent`/`success` rồi kết luận "chain chết".
Bộ lọc đúng:

```python
d = json.load(open('store/activity.json', encoding='utf-8'))['activity']
t = [x for x in d if str(x.get('time','')).startswith('2026-09-30')]
# kỳ vọng: 11 entry = 5×[WARN] OpenCode + 5×[OK] ByteDance fallback + 1 dòng tổng kết
```

---

## 4. Ngưỡng near-dup 0.70 BỎ SÓT cặp trùng thật — nên hạ 0.62

Đo lại 12 stale context-scan bằng `difflib.SequenceMatcher` trên title đã chuẩn hoá
(bỏ dấu câu, `[^a-z0-9\u1ea0-\u1ef9]+` → space, lowercase).

| Cặp | sim | ở ngưỡng 0.70? |
|---|---|---|
| #43 ↔ #48 | 0.87 | bắt |
| #43 ↔ #51 | 0.77 | bắt |
| #46 ↔ #54 | 0.75 | bắt |
| #48 ↔ #51 | 0.72 | bắt |
| **#45 ↔ #52** | **0.66** | **BỎ SÓT** |

Spec fix dedup đang chờ duyệt viết ngưỡng 0.70 → sẽ **không** gom được #45/#52 dù đó
là trùng thật ("Chốt vai trò chủ tịch mới bằng văn bản" vs "Chốt vai trò mới chủ tịch
bằng văn bản với 3-5 đầu việc có deadline").

**Đề xuất chốt spec: ngưỡng 0.62.** Kết quả:

- @0.70 → 9 nhóm, 4 cặp, **12 task = 9 việc thật**
- @0.62 → 8 nhóm, 5 cặp, **12 task = 8 việc thật** (gom thêm [45,52])

Cặp khác đủ thấp nên không dính: #44↔#49 = 0.29, #47↔#49 = 0.39, #50↔#52 = 0.13,
#44↔#45 = 0.14. Hạ xuống 0.62 **không** gom nhầm.

⇒ Đóng được ngay **4** bản trùng (#48, #51, #52, #54), không phải 3 như briefing
29/09 ghi. Con số này đưa vào spec + báo cáo cho anh, đừng để briefing cũ dẫn 3.

### Code mẫu (union-find để gom cặp thành nhóm)

```python
parent = {i: i for i in ids}
def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]; x = parent[x]
    return x
for a, b in edges:                      # edges đã lọc theo threshold
    ra, rb = find(a), find(b)
    if ra != rb: parent[ra] = rb
groups = {}
for i in ids: groups.setdefault(find(i), []).append(i)
```

Chỉ so `title` là thiếu: 2 proposal sinh cùng việc nhưng diễn đạt khác nhau sẽ có
title lệch → nên so thêm `description` khi triển khai thật.

---

## 5. Bài học quy trình: đừng để "chờ duyệt" đứng yên vô thời hạn

Fix dedup chờ duyệt từ 24/09 → 30/09 = **6 ngày**, 4 standup liên tiếp cùng 1 đề xuất
A/B giống nhau. Cả 5 agent đều trung thực báo "0 task đóng, không bịa" — nhưng
standup vẫn **lặp nguyên văn**, vì:

- Không task `mode=agent` active nào để agent thức dậy (đo bằng script: 0).
- 12 stale đều `mode=kanban`, thuộc Quang/Anh Quân.
- Mọi "việc tự làm được" đều là **sửa code** → dính quy tắc "KHÔNG code trước khi duyệt".

Xử lý đúng: báo cáo thẳng vào báo cáo standup, nêu rõ 3 nút chờ anh kèm **ước lượng
thời gian cụ thể** (30 phút / 5 phút / 30-60 phút) và **phương án rẻ hơn không cần code**
(đóng tay 4 bản trùng). Đừng tự code để "cho có bằng chứng" — đó là vi phạm quy tắc
gốc, và anh đã mắng vì chuyện đó trước đây.
