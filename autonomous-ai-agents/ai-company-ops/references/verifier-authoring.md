# Viết verify script: bằng chứng phải tái lập được, và phải biết FAIL (02/10/2026)

Vòng lặp bị flag hôm nay: xoá script verify **trước khi chạy PASS** → mất toàn bộ
bằng chứng, phải viết lại từ đầu, và bản viết lại FAIL ngay 4 chỗ.

Đây là bổ sung cho `standup-number-discipline-2026-10.md` (số phải đo) và
`briefing-staleness-2026-10.md` (số phải nằm đúng chỗ trong doc).

## 1. Verify cái BỀN VỮNG, không phải script đã xoá
Scratch script trong `Temp/` sẽ bị dọn — verifier phải assert **artifact còn tồn tại**:
- file đã commit: `git show --name-only --format= <h>` + `git branch -r --contains <h>`
- doc / state: `briefing.md`, `D:/Hermes Proj/.hermes-state/*.md`
- dữ liệu nguồn: `store/tasks.json`, `store/activity.json`, output `ops_guard --json`

Assert script-đã-xoá = vô nghĩa, không tái lập được.

## 2. PHẢI chứng minh verifier FAIL được (mutation / negative control)
Verifier chưa từng thấy FAIL thì không phải bằng chứng — nó có thể in PASS cho mọi thứ.

```python
import json, shutil, subprocess, sys
p = 'store/tasks.json'; shutil.copy(p, p + '.bak')
d = json.load(open(p, encoding='utf-8'))
for t in d['tasks']:
    if t['id'] == 43: t['done_criteria'] = ''      # inject vi phạm NO_DC thật
json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False)
print('mutated exit=', subprocess.run([sys.executable, VERIFIER]).returncode)
shutil.move(p + '.bak', p)                          # khôi phục
print('restored exit=', subprocess.run([sys.executable, VERIFIER]).returncode)
```

Kết quả 02/10: mutated **exit=1** (bắt đúng `no_dc: 0→1`), restored **exit=0**.

Chỉ "49/49 PASS" **không kèm mutation** thì chưa đủ bằng chứng — ghi cả 2 con số exit
vào báo cáo. Sau mutation phải verify lại dữ liệu nguyên vẹn (54 task, phase
41/11/1/1, backup đã dọn) trước khi kết luận.

## 3. Bốn kiểu assertion hay báo FAIL giả — đều gặp 02/10

| Lỗi | Triệu chứng | Sửa |
|---|---|---|
| `all()` vacuous | `[l for l in lines if "WARN" in l]` — mọi dòng đều có "WARN" nên `all()` luôn True | lọc phải **loại được** dòng; thêm `chk("has a claim line", bool(claims), True)` để chắc lọc có tác dụng |
| So thứ tự | `git log` trả **mới-nhất-trước**, `want` viết tăng-dần → FAIL giả | `sorted()` **cả hai vế** khi không quan tâm thứ tự |
| So độ dài | 2 tập cùng size khác id vẫn lọt | so **tập hợp id** (`{...}`), không so `len()` |
| Chặn nhầm đính chính | assert "doc không chứa `8×`" → FAIL vì dòng đính chính **cố ý** trích lại số sai cũ | chỉ assert trên **dòng claim**; bỏ qua dòng ghi chú đính chính |

Sau khi sửa: **49/49 PASS**. Trước đó 4 FAIL — **toàn bộ là bug script, không phải dữ liệu sai.**
Nói ra điều này trong báo cáo, đừng giấu (giống luật "verify FAIL → kiểm script trước, repo sau").

## 4. Union-find phải nén đường đi (đừng dùng lambda đệ quy)
```python
# SAI — RecursionError, chỉ 12 node đã vượt độ sâu đệ quy
find = lambda x: p[x] if p[x] == x else find(p[x])

# ĐÚNG — vòng while + path compression
def find(x):
    while p[x] != x:
        p[x], x = p[p[x]], p[x]
    return x
```
Union phải guard `if ra != rb` trước khi gán, nếu không sẽ tạo vòng trong chính nó.

## 5. Đếm số assertion thật, không hardcode
```python
fails, CHECKS = [], 0
def chk(name, got, want):
    global CHECKS; CHECKS += 1
    if got == want: print("PASS", name)
    else: fails.append(name)
print("ALL PASS (ad-hoc, %d checks)" % CHECKS)   # tự đếm, không ghi tay
sys.exit(1 if fails else 0)
```
Không dùng `sum(1 for _ in ())` để đếm — luôn ra 0 (đã dính 1 lần).

## 6. Sửa file CRLF bằng python: anchor KHÔNG được span xuống dòng
`open(p,'rb').read().decode()` **giữ nguyên `\r\n`** → anchor có `\n` không bao giờ khớp.
- Anchor nằm **trong một dòng**: `'(8× OpenCode WARN → 7× ByteDance fallback OK)'` → khớp ngay.
- Ghi lại giữ CRLF: `open(p,'wb').write(t.replace('\n','\r\n').encode('utf-8'))`.
- Verify sau khi ghi: `b'\r\n' in raw`, không BOM (`raw[:3] != b'\xef\xbb\xbf'`), không null byte.
- **Đừng đoán** — đọc `repr(dòng_thật)` rồi copy, đừng tự gõ lại từ trí nhớ (đã dính
  "anchor not found" vì tưởng khác nhau trong khi giống hệt; khác ở chỗ `\r` ẩn).

## 7. Thứ tự đúng: đo → verify → mutation → mới xoá
1. Đo số từ nguồn gốc (không tin số đã in lần trước).
2. Viết verifier assert lại **mọi** con số trong báo cáo + assert doc mang số ĐÚNG.
3. Chạy → tới khi ALL PASS.
4. Mutation test → xác nhận exit=1, rồi exit=0 sau khi khôi phục.
5. **Xoá** script + backup.

Xoá sớm ở bước 2-3 chính là nguyên nhân vòng lặp hôm nay.

## 8. `read_file` báo "binary" trên file text → đọc bằng python, đừng tin
`read_file` trả `is_binary: true` cho `briefing.md` dù là UTF-8 thuần (0 null byte,
0 control char, chỉ CRLF). Kiểm chứng rồi mới kết luận:
```bash
python -c "raw=open('briefing.md','rb').read(); print(raw[:3]==b'\xef\xbb\xbf', raw.count(b'\x00'), raw.count(b'\r\n'))"
```
Sau đó đọc/soạn bằng `python -c` (xem mục 6).

## 9. PASS giả: assertion GỌI TÊN một ngữ nghĩa nhưng đo thứ khác (03/10)

Mục 3 liệt kê FAIL giả. Đối xứng với nó là **PASS giả** — assertion luôn đúng vì
đo sai thứ, và mutation **không bắt được** cho tới khi mutation chọn đúng biến.

```python
# SAI — nhãn là STALE, code chỉ đếm phase != terminal
check("so task active (= STALE)", len(active), 13)
active = [t for t in tasks if t.get("phase") not in TERM]   # <-- thiếu điều kiện thời gian

# Mutation "lam moi updated_at cho #8" -> van PASS, exit=0
```
STALE = *không-terminal **VÀ** ≥48h không đổi*. Bỏ vế thời gian thì "task vừa
được đụng" cũng đếm vào STALE — đúng bẫy **STALE ảo** (mục 12/09 trong SKILL.md:
wake_agent bump `updated_at` làm task rớt khỏi STALE dù không tiến triển).

Sửa — tách 2 khái niệm, assert cả hai, và đặt tên đúng:
```python
def days_since(t):
    for f in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d"):
        try:
            return round((datetime.now() - datetime.strptime(
                str(t.get("updated_at",""))[:len(datetime.now().strftime(f))], f)
            ).total_seconds()/86400, 1)
        except ValueError:
            continue
    return None

check("so task active (phase khong terminal)", len(active), 13)
stale = sorted(t["id"] for t in active if (days_since(t) or 0) >= 2)
check("STALE that (>=48h khong doi phase)", len(stale), 13)
check("STALE that — danh sach id", stale, [8,43,44,45,46,47,48,49,50,51,52,53,54])
check("active nhung <48h (STALE ao)", [t["id"] for t in active if (days_since(t) or 0) < 2], [])
```
Luật: **assert tên phải mô tả đúng cái biểu thức đo.** Nếu nhãn mang một định
nghĩa nghiệp vụ (STALE, NO_DC, vi phạm DoD) thì code phải encode đủ điều kiện
của định nghĩa đó — không được dựa vào tên để "cho có".

## 10. Mutation phải đủ MẠNH, và phải đọc WHICH assertion FAIL (03/10)

Mutation yếu vẫn cho exit=1 nhưng **bắt sai thứ** → tưởng đã cover, thực chưa:
```
doi title #43~#54: sim 0.738 -> 0.708   (van >= 0.62 nen cap TRUNG chua mat)
  -> FAIL  'cap trung' doi gia tri   (dung, nhung vi ly do khac)
doi title #54 sang cau hoan toan khac
  -> FAIL  'so cap trung' 5->4, 'so nhom' 3->2, 'so viec that' 8->9  ( moi la test dung)
```
Sau mỗi mutation, **in ra assertion nào FAIL** (không chỉ đếm dòng FAIL):
```python
fails = [l.strip() for l in r.stdout.splitlines() if l.strip().startswith("FAIL")]
hit = any(TEN_ASSERTION_CAN_KIEM in f for f in fails)   # assert mang TÊN, không phải "có FAIL"
```
Dùng 1 script mutation cho N vi phạm, mỗi vi phạm **gắn tên assertion** nó phải
chạm tới → kết luận "4/4 bắt được" chỉ khi đúng tên đó xuất hiện. 03/10 kết
quả 4/4 (exit=1 + đúng tên), 33/33 PASS trên dữ liệu thật.

## 11. Spec chỉ định CÔNG THỨC nhưng đo bằng thứ khác → no-op im lặng (03/10)

Spec dedup 01/10 bảo code so `title + description` ở ngưỡng 0.62, nhưng bảng số
đo lại được lấy trên **`title` riêng**. Đo đúng công thức của spec:
| cách so | 0.70 | 0.62 | 0.55 |
|---|---|---|---|
| `seq(title+desc)` — **cách spec mô tả** | 0 nhóm | **0 nhóm** | 2 nhóm |
| `seq(title)` | 2 nhóm | **3 nhóm (=8 việc)** | 3 nhóm |
| `max sim title+desc` = **0.607 < 0.62** → không cặp nào đạt ngưỡng.
Code đúng spec sẽ **không gom được task nào**, chạy xong vẫn exit 0, log "0 trùng".

Luật cho mọi spec có **ngưỡng số**: trước khi viết code, đo **đúng cái biểu thức
spec nêu** (cùng normalize, cùng ngưỡng), rồi mới so sánh với cách đo khác. Nếu
spec mô tả "so title+desc" mà bảng số viết bằng "title" → spec sai, sửa spec.
Bằng chứng phải là con số của **công thức trong spec**, không phải của cách thuận tiện.

Kèm 3 lỗi logic verifier phát hiện khi chạy (đều là bug script, không phải data):
1. `components()` trả **tổng số component** chứ không phải số nhóm **trùng** —
   12 component nghĩa là 12 node rời rạc ⇒ **0 nhóm trùng** (đừng assert `0` cho
   `len(components)`; phải lọc `Counter(...)[v] > 1` rồi mới đếm nhóm).
2. Công thức suy ra số việc `12 - (len(edges) - components)` = **vô nghĩa** (ra 15).
   Đúng: `len(tasks) - sum(v - 1 for v in comp.values())`.
3. `edges(..., thr)` lọc `>=` → muốn tìm "cặp lớn nhất **dưới** ngưỡng" (để tính
   margin chống cắt nhầm) phải lọc `<` riêng, không dùng lại hàm lọc `>=`.

## 12. Margin chống cắt nhầm — đo khe hở, không chỉ đặt ngưỡng cho có
Ngưỡng dedup chỉ an toàn nếu nằm **giữa 2 cụm similarity**:
```python
below = [s for s, _, _ in pairs_all(cs, f_title) if s < 0.62]
check("cap trung thap nhat", min(s for s,_,_ in edges), 0.674)   # nhom trung
check("cap khong trung cao nhat", max(below),            0.445)   # lien quan nhat
check("khe ho", round(0.674 - 0.445, 3), 0.229)
check("nguong 0.62 nam giua khe ho", 0.445 < 0.62 <= 0.674, True)
```
Báo cáo phải kèm **khe hở**, không chỉ con số ngưỡng — 0.62 nằm trong khe
[0.445, 0.674] thì an toàn; nằm ngoài là cắt nhầm hoặc bỏ sót.

## 13. Mutation phải nhắm ĐÚNG ARTIFACT mà assertion đọc — data VÀ doc (16/10)

Lỗi lặp lại của công ty **không phải dữ liệu sai, mà là doc mang số cũ** (agent
dẫn lại số briefing hôm trước: CMO 01/10, CTO 02/10, Content 15/10). Nên một
mutation trên `store/tasks.json` **không** chứng minh được các assertion đọc
`briefing.md` là sống — chúng có thể vacuous mà vẫn PASS.

Chạy 2 TẦNG mutation, mỗi tầng nhắm đúng file mà assertion tương ứng đọc:

```python
# Tầng DATA — chứng minh guard không mù
M1  xoá done_criteria #43          -> NO_DC 0 -> 1
M2  bump updated_at #47            -> STALE 21 -> 20   (bump = CHE STALE, đúng bẫy STALE ảo)
M3  lùi updated_at #63 3 ngày      -> STALE 21 -> 22

# Tầng DOC — chứng minh check số-trong-briefing không vacuous
M4  briefing.md: 'STALE=21' -> 'STALE=99'  -> check briefing PHAI FAIL
```

Kết quả 16/10: 3/3 mutation data guard bắt được, M4 doc fail đúng chỗ, và
**sha256 của CẢ 2 file** (`store/tasks.json`, `briefing.md`) khôi phục khớp sau
khi khôi phục. Assert sha256 cho từng file bị mutate, không chỉ file data.

## 14. `grep -c '^PASS:'` ≠ số assertion trong script (16/10)

Verifier in dòng `TONG: 17 assertion` TRƯỚC khối mutation, nhưng khối khôi phục
sha256 gọi thêm 1 `chk()` sau đó → `grep -c '^PASS:'` ra **18**. Hai số lệch
không phải bug — nhưng dễ bị đọc thành "verifier tự mâu thuẫn".

Sửa: **in TONG ở CUỐI script** (sau mutation) để chỉ còn 1 con số duy nhất, hoặc
khi so thì trừ đi số check nằm sau TONG. Đừng lấy 2 nguồn đếm khác nhau rồi kết
luận verifier sai.

## 15. Cảnh báo "modified by sibling ... never read it" là DƯƠNG TÍNH GIẢ khi có tiến trình nền (16/10)

Cron/standup chạy nền tự append footer `**Last Updated:**` vào `briefing.md` →
`write_file`/`patch` cảnh báo file "was modified by sibling subagent ... but this
agent never read it" (cả trên `.gitignore`). Nội dung đọc lại bằng python **khớp
đúng** bản mình thấy.

**Đừng hoảng, đừng rewrite đè để "cho chắc".** Xác nhận bằng `git diff --stat
<file>`: chỉ có thay đổi của mình ⇒ cảnh báo vô hại. Vẫn LUÔN `git diff --stat`
trước khi commit (đó là bước phân xử, không phải cảnh báo tool).

## 16. Verify PHẢI chạy lại SAU commit, và lần chạy CUỐI phải là verifier đã commit

Sau khi commit + push mà còn sửa file (`.gitignore`, `briefing.md`) thì bằng
chứng cũ thành **cũ** — phải chạy lại verify trên đúng trạng thái đã commit.

Thứ tự đúng cuối phiên:
1. Commit + push verifier vào `docs/qa/verify_standup_<ngày>.py` cùng evidence
   (`docs/qa/standup_<ngày>_reports.json`). Thêm `Temp/` vào `.gitignore`.
2. `rm` script trong `Temp/`.
3. **Chạy lại verifier đã commit** (`python docs/qa/verify_standup_<ngày>.py`) —
   để artifact bền vững là lần chạy cuối, không phải script tạm.
4. Assert verifier tự chạy được từ repo root (đường dẫn evidence mặc định nội bộ,
   `argv[1]` để override) — verifier trỏ vào `Temp/` sẽ chết sau bước 2.

16/10: verifier thường trực `docs/qa/verify_standup_2026-10-16.py` → 18 PASS /
0 FAIL / exit 0, chạy được độc lập sau khi `Temp/` đã dọn. Script rà soát tạm
30 assertion / 0 FAIL (gồm `git branch -r --contains <commit>`, `origin/main` có
đủ 3 file bằng chứng, `Temp/` rỗng + đã ignore, không rác chưa commit).

## 17. Verifier FAIL vì ASSERTION SAI, không phải repo — ca cụ thể (16/10)

Thêm vào bảng mục 3 kiểu lỗi hay gặp nhất khi lọc task:

```python
# SAI — lọc theo TAG mà quên lọc PHASE
chk("task context-scan = 24", len([t for t in tasks if "context-scan" in (t.get("tags") or "")]), 24)
# -> FAIL, thực tế 32: 24 đang mở (planning/review) + 8 ĐÃ ĐÓNG (#35-42)

# ĐÚNG — tách rõ đang mở / đã đóng, assert cả hai
cs_open = [t for t in cs if t.get("phase") in ("planning", "review")]
cs_done = [t for t in cs if t.get("phase") == "completed"]
chk("context-scan dang mo", len(cs_open), 24)
chk("the he cu da dong", sorted(t["id"] for t in cs_done), list(range(35, 43)))
```

Cùng họ với mục 11: **nhãn/đối tượng của assertion phải khớp biểu thức đo.**
Sửa SCRIPT, không sửa dữ liệu. Tiện thể: `tasks.json` giữ cả **các thế hệ đã
đóng** — 8 task completed #35-42 có `close_note` "Quang quyết đóng 2026-09-03 —
context-scan draft, trùng nội dung, không giao agent" ⇒ khi đề xuất đóng lô trùng
mới, **trích tiền lệ này** (việc không mới, Quang đã duyệt một lần) thay vì trình
như đề xuất lần đầu.