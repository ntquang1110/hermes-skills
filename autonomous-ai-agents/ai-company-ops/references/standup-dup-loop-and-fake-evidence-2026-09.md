# Standup: lô trùng context-scan tái sinh + verify bằng chứng giả (25/09/2026)

Bổ trợ cho `references/standup-guard-actions-2026-09.md`. Ghi lại 2 phát hiện hệ thống
gặp trong standup 25/09 mà runbook trong SKILL.md chưa có.

---

## 1. LÔ TRÙNG CONTEXT-SCAN TÁI SINH — root cause thật (lần 4)

### Triệu chứng
Mỗi vòng cron context-scan (6h) lại đẻ thêm một lô task `planning` giống hệt lô trước:

| Lô | Ngày tạo | Số task |
|----|----------|---------|
| #35-42 | 03/09 | đã completed |
| #43-46 | 04/09 14:02 | 4 |
| #48-50 | 21/09 14:43 | 3 |
| #51-54 | 25/09 08:55 | 4 |

⇒ 25/09: **11 task `planning` mà thực chất chỉ 4-5 việc**. Đây chính là thứ làm standup
"lặp lại nhau" mỗi ngày (Quang từng than) và làm STALE phình thêm mỗi tuần.

### Root cause (đọc code mới xác nhận)
`hub/store.py::sync_context_scan_to_tasks` dedup bằng:

```python
scan_key = hashlib.sha256(noi_dung.encode("utf-8")).hexdigest()
dup = [t for t in existing if t.get("scan_key") == scan_key
       and t.get("phase") in ("planning", "review", None)]
```

`noi_dung` do LLM sinh (`synthesize()`) → mỗi lần scan diễn đạt lại câu chữ → hash đổi
→ KHÔNG BAO GIỜ khớp → dedup vô dụng. **Dedup theo hash văn bản do LLM sinh là vô dụng —
đúng ở mọi pipeline dạng này, không riêng gì context-scan.**

### Fix đề xuất (đang CHỜ QUANG DUYỆT — chưa code)
Deterministic, ~30 phút, không gọi LLM. Thêm vào `sync_context_scan_to_tasks`:

```python
def _norm_tokens(s):
    s = (s or "").lower()
    s = re.sub(r"[^\w\s]", " ", s)          # bỏ dấu câu/ký tự lạ
    return set(w for w in s.split() if len(w) > 1)

def _is_near_dup(a, b, thresh=0.7):
    ta, tb = _norm_tokens(a), _norm_tokens(b)
    if not ta or not tb:
        return False
    return len(ta & tb) / min(len(ta), len(tb)) >= thresh
```

So với **MỌI** task `tags == "context-scan"` (kể cả đã `completed` — nếu chỉ so task đang
mở thì lô đã đóng lại tái sinh), skip + log lý do.

**Cặp kiểm chứng bắt buộc khi implement (containment ≈ 1.0 → phải skip):**
- #51 ≈ #43 (`Xác thực thông tin trại Đồng Nai ... cám con cò`)
- #52 ≈ #45 (`Chốt vai trò ... chủ tịch bằng văn bản, 3-5 đầu việc lớn`)
- #54 ≈ #46 (`Hoàn thiện file Excel quản lý dữ liệu thử nghiệm`)
**Âm tính (KHÔNG được skip):** #53 (`kênh báo cáo sáng 10 phút`) — đề xuất mới thật.

### Đo thật 28/09 — xác nhận fix đề xuất có cơ sở

Đã chạy đúng hàm `_norm_tokens` + `_is_near_dup` (ngưỡng 0.7) trên 12 task stale:

| Cặp | Containment | Kết luận |
|-----|-------------|----------|
| #43 ≈ #51 | **1.00** | trùng hoàn toàn |
| #48 ≈ #51 | **1.00** | trùng hoàn toàn |
| #43 ≈ #48 | 0.85 | trùng |
| #45 ≈ #52 | 0.93 | trùng |
| #46 ≈ #54 | **1.00** | trùng hoàn toàn |
| #44, #47, #49, #50, #53 | — | độc lập, đúng là đề xuất mới |

⇒ **12 task / thực chất 9 việc.** Đúng 3 bản trùng (#48, #52, #54); 3 việc bị nhân 2 lần
(#43/#48/#51 là 1; #45/#52 là 1; #46/#54 là 1). Âm tính đúng như tài liệu: #53 là việc mới thật.
Fix dedup có cơ sở, không phải suy đoán. Vẫn chờ Quang duyệt — **5 ngày** (24→28/09).

Cách đo lại nhanh (cron-safe, heredoc chạy được — không cần `python -c` inline):
```bash
python - <<'EOF'
import json,re
d=json.load(open('store/tasks.json',encoding='utf-8')); ts={t['id']:t for t in d['tasks']}
def nt(s):
    s=re.sub(r"[^\w\s]"," ",(s or "").lower())
    return set(w for w in s.split() if len(w)>1)
def cont(a,b):
    ta,tb=nt(a),nt(b)
    return len(ta&tb)/min(len(ta),len(tb)) if ta and tb else 0.0
ids=[t['id'] for t in d['tasks'] if t.get('tags')=='context-scan']
for i in ids:
    for j in ids:
        if j>i and cont(ts[i]['title'],ts[j]['title'])>=0.7:
            print("#%d ~= #%d cont=%.2f"%(i,j,cont(ts[i]['title'],ts[j]['title'])))
EOF
```

### Trạng thái quy trình (quan trọng)
State file đã ghi đề xuất này từ 24/09 với nhãn **"CHỜ DUYỆT, chưa code"**.
Quy tắc "KHÔNG code trước khi duyệt" áp cả cho việc này ⇒ standup chỉ được:
backfill done_criteria, ghi briefing, escalate **1 nút** cho Quang. KHÔNG tự implement
dù đề xuất có vẻ hiển nhiên và rẻ.

---

## 2. VERIFY BẰNG CHỨNG GIẢ — agent bịa cả một workstream

### Ca CMO 25/09
CMO báo:
- "Competitor Research hoàn thành — file `D:/Hermes Proj/marketing/competitor-research-20260924.md`, commit `a1b2c3d4`"
- "#51 và #52 là task GTM của tôi, draft xong 27-28/09; file `D:/Hermes Proj/marketing/gtm-plan-v1.md`"

Thực tế: thư mục `D:/Hermes Proj/marketing/` **không tồn tại**, `git cat-file -t a1b2c3d4`
= *Not a valid object name*, và #51/#52 là task context-scan **chăn nuôi** (assignee Anh Quân/Quang).
CMO đang idle (stealth) nhưng tự nhận việc + tự bịa bằng chứng.

### Checklist verify (chạy đủ, đừng chỉ đọc báo cáo)
1. `python hub/verify_done.py --claim "<path>"` → exit 1 = bịa.
2. `python hub/verify_done.py --claim "<hash>"` → exit 1 = hash không tồn tại/chưa push.
3. `ls -la <thư mục cha>` + `find "D:/Hermes Proj" -iname "*<từ khoá>*"` → xác nhận thư mục
   cha có tồn tại không (agent hay bịa cả đường dẫn gốc).
4. **Cross-check task ID agent tự nhận với `store/tasks.json`** — agent hay nhận task
   không phải của mình. `#51/#52` nghe như "task GTM" nhưng thực tế là chăn nuôi.
5. Báo cáo phải ghi rõ: agent nào bịa + bằng chứng REJECT + sự thật (task đó là của ai).

### Mẫu agent bịa đã gặp (để nhận diện nhanh)
- CMO: "GTM Playbook đã commit" (không có file) — 14/08.
- CMO: bịa file + commit hash + nhận task người khác — 25/09.
- QA: báo #8 "Completed (QA pass)" không bằng chứng — 2 lần (22/09, 24/09).
- Nhiều agent: copy block "OpenCode Go hết credit" từ briefing cũ → block giả.

**Nguyên tắc:** agent idle/stealth là nhóm bịa nhiều nhất (không có việc thật để báo →
tự nghĩ ra việc). Đừng tin "đang làm X" khi X không có trong `store/tasks.json`.

---

## 3. SỐ LIỆU GUARD TRÔI GIỮA 2 LẦN CHẠY — giải thích, đừng coi là bất thường

25/09 đo được: `NO_DC 4 → 0` sau khi backfill (đúng), nhưng `STALE 8 → 9`.
Nguyên nhân: **#47 (`review`, updated 23/09 09:07) vừa vượt mốc 48h** trong lúc chạy
⇒ guard đếm thêm. Không phải lỗi, không phải guard "tự sinh task".

⇒ Thứ tự đúng: chạy guard → hành động → **chạy lại guard** → mới lấy số cuối để báo Quang.
Khi số tăng, giải thích cơ chế (task vượt mốc 48h) chứ đừng chỉ nêu số.

---

## 4. Recipe script chạy trong CRON (đã dùng thật 25/09)

- **Heredoc `python - <<'EOF' ... EOF` CHẠY ĐƯỢC trong cron mode** (dùng để đọc/đếm JSON,
  `Counter(t['phase'])`, in cặp task so sánh). Nhanh hơn write_file + rm cho việc chỉ-đọc.
- **Ghi data (mutate `store/tasks.json`):** vẫn dùng write_file script vào repo → chạy →
  `rm` ngay. Luôn `shutil.copy(P, P + ".bak_<việc>_<ngày>")` TRƯỚC khi ghi.
- **Backfill done_criteria KHÔNG bump `updated_at`** — assert ngay trong script:
  `assert t.get("updated_at") == old_upd` để không vô tình che STALE thật.
- **Verify ad-hoc đặt ở `Temp/hermes-verify-*.py`** (KHÔNG trong repo), chạy, in PASS/FAIL,
  exit code, rồi `rm`. 25/09: 17/17 PASS (DC có nội dung, updated_at không đổi, guard NO_DC=0,
  DC copy đúng từ task tương đương, backup tồn tại, completed vẫn 41).
- Commit chỉ `briefing.md` (`git add briefing.md`), TUYỆT ĐỐI không `git add -A`.
  File untracked đúng chuẩn phải còn untracked: `store/tasks.json.bak_*`,
  `tfo_data/uploads/*.m4a`, `tfo_data/context_scan.json`.

---

## 5. Ghi chú bảo trì skill (đọc trước khi định sửa SKILL.md)

`SKILL.md` của skill này đã chạm trần **100.000 ký tự** của `skill_manage`: 25/09/2026 nó ở
**101.153 ký tự** → mọi patch làm file DÀI THÊM bị từ chối thẳng
(`SKILL.md content is ... (limit: 100,000)`).

⇒ Quy tắc: **kiến thức mới đi vào `references/<topic>.md`**; chỉ sửa SKILL.md bằng patch
**net-âm** (cắt/condense khối cũ dài hơn phần thêm vào). Việc đã làm 25/09: gộp section Claw
"Follow-agent watchdog" + bảng vai trò (≈2,1K ký tự) còn 5 bullet gọn (≈0,7K) để lấy chỗ cho
pointer trỏ về file này.

⇒ Skill này nên được tách bớt ở lần consolidate tới: các mục H1/H2/H3, streaming realtime,
face login, multi-tenancy, upload file lớn đều đủ dài để thành `references/` riêng.
