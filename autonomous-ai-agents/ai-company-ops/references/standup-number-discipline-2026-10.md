# Standup: đo trước khi viết số vào tài liệu (01/10/2026)

Bài học từ 1 lỗi tự bắt được trong standup 01/10/2026. Áp dụng cho **mọi con số**
viết vào spec / state / briefing / báo cáo Quang — không riêng standup.

## Lỗi gốc: suy diễn số từ log ĐÃ LỌC

**Việc đã xảy ra:**
- Script đo similarity chỉ in cặp có sim ≥ 0.66. Từ output đó em **đếm tay** số nhóm
  ở ngưỡng 0.70 → ghi vào spec "**10 nhóm**", commit `216416d`.
- Verify script đo độc lập → ra **9 nhóm**. Sai 1 nhóm, ngay trong tài liệu anh đọc để duyệt.

**Vì sao lỗi này nguy hiểm:** script KHÔNG hỏng. Nó in đúng những gì được hỏi. Nhưng
em đọc output đã lọc rồi đoán số chưa được in → nhân bản sai nội dung của log vào
tài liệu quyết định. **Log đã lọc không phải log đầy đủ — đừng suy số chưa được in từ log đó.**

**Luật:**
- Số đi vào tài liệu commit → phải do script **in ra trực tiếp**, không phải em cộng
  trong đầu từ output một phần.
- Script chỉ in threshold cụ thể thì muốn nói "ở threshold khác ra mấy nhóm" → **chạy lại
  script ở threshold đó**, đừng suy.
- Nghi ngờ số mình đang ghi → chạy script lấy đúng số đó, không dùng trí nhớ phiên trước.

## Đính chính sai hướng: đừng vội kết luôn "phiên trước sai"

Sau khi bắt lỗi 10 → 9, em viết vào state: *"30/09 báo 9 nhóm là SAI, hôm nay xác nhận"*.
Đo lại: 30/09 ghi 9 ở ngưỡng 0.70 → **hôm nay đo lại đúng 9. 30/09 không sai. Bản spec
hôm nay mới sai.**

**Luật:** khi định "đính chính" một con số của phiên trước, hãy **chạy lại phép đo trên
cả hai mốc** và so. Mặc định nghi ngờ chính bản mới vừa viết — cảm giác "vừa phát hiện
lỗi nghiêm trọng" thường làm em tìm thêm lỗi ở chỗ khác để hợp thức hoá cảm giác đó.
Phiên 01/10 đã suýt ghi một lỗi sai vào state theo đúng kiểu đó.

## Verify script FAIL: kiểm tra script trước, repo sau

Lần chạy đầu FAIL 2 assertion. **Cả 2 là bug của script verify, không phải lỗi repo:**

| Assertion FAIL | Nguyên nhân thật |
|---|---|
| "files in commit" → có cả dòng `2 files changed, 65 insertions(+)` | `git show --stat` in dòng summary; phải lọc `if "\|" in ln` mới lấy đúng tên file |
| "commit pushed" → False | `git branch -r --contains <hash>` trả **tên branch**, không trả hash → phải check `"origin/main" in output` |

**Luật:** FAIL đầu tiên → đọc xem assertion sai hay dữ liệu sai. Đừng sửa repo cho khớp
script vừa viết. Sửa assertion, chạy lại, và **báo cáo trung thực** trong báo cáo
rằng 2 FAIL đầu là bug script chứ không giấu luận điện.

## Bẫy `EXIT=$?` sau pipe (Windows git-bash)

```bash
python verify.py | tail -14; echo "EXIT=$?"     # SAI: $? của tail, luôn 0
python verify.py | tail -14; echo "EXIT=${PIPESTATUS[0]}"   # ĐÚNG
```
Script có `exit(1)` khi fail mà `EXIT=0` vẫn in ra → tưởng pass. Lần này đã dùng
`${PIPESTATUS[0]}` nên bắt được; không dùng thì verification pass giả.

## Lọc log theo NGÀY: đừng dùng `>= "YYYY-MM-DD 00:00"` rồi cộng tay (02/10)

**Việc đã xảy ra:** state + briefing ghi "02/10: 8× `[WARN]` → 7× `[OK]` ByteDance".
Script lọc `e["time"] >= "2026-10-02 00:00"`. Đo lại **theo ngày** (`e["time"][:10]`):

| ngày | entries | WARN | OK |
|---|---|---|---|
| 29/09 | 17 | 8 | 8 |
| 30/09 | 11 | 5 | 5 |
| 01/10 | 11 | 5 | 5 |
| **02/10** | **11** | **5** | **5** |

→ "8" là của **29/09**, không phải 02/10. Con số 02/10 đúng là **5 WARN → 5 OK**,
đúng **1 cặp/agent** (5 agent). Đã sửa briefing + state → commit `9bc0c0f`.

**Luật:**
- Muốn số của MỘT ngày → so sánh `e["time"][:10] == "2026-10-02"`. Đừng dùng mốc
  `>= "… 00:00"` rồi cộng đầu-cuối bằng tay — dễ nuốt entry chưa flush của hôm trước.
- **In bảng theo ngày trước khi trích con số** (4 dòng, 5 giây) — nhìn thấy ngay mình
  đang lẫn ngày. Không cần tin trí nhớ.
- Cặp WARN/OK phải **bằng nhau** = số agent. Lệch → đang đếm sai phạm vi.
- Đây là lỗi **tự làm**, không phải agent bịa. Sửa data + ghi đính chính vào state
  (kèm bảng số đo được), đừng xoá dấu vết.

## `git --grep` với tiếng Việt: `-i` KHÔNG fold dấu (02/10)

`git log --grep="lô trùng"` → **không match** (git grep theo byte, không strip dấu).
`--grep=trùng` cũng rỗng. Dùng **từ không dấu**: `--grep="tai sinh"`, `--grep=context-scan`.

Ngoài ra:
- `-iE` **không hợp lệ** → `fatal: unrecognized argument: -iE`. Dùng `-i` + `--perl-regexp` tách riêng.
- Nhiều `--grep` là **OR**: `--grep=dedup --grep=trung --grep=dup` — nhưng dễ match nhầm
  việc khác (grep "dup" ra commit 01/08 "duplicate mediaRecorder", không phải task trùng).
  → grep rộng rồi **lọc lại theo ngữ nghĩa**, hoặc grep từ đặc thù.
- Chạy thử `git log ... | head` trước khi tin kết quả rỗng — rỗng thường do sai flag, không phải do không có lịch sử.

## Verify script bằng `subprocess` chạy git: so sánh set, không so thứ tự

Bài học từ chính script hôm nay: `chk("…", sorted(got), ["fb3b500", "9bc0c0f"])` FAIL vì
`git log` trả **mới nhất trước** (`['9bc0c0f','fb3b500']`) còn `want` viết tăng dần.
→ **`sorted()` cả hai vế** khi so danh sách không quan tâm thứ tự. Sắp xếp một vế là
FAIL giả, dễ bị nhầm là dữ liệu sai.

Tương tự: so **tập hợp id** (set) chứ không so độ dài — 2 tập cùng size khác id vẫn lọt.

## Mẫu verify 02/10: 77/77 pass
Script `%TEMP%/hermes-verify-ai-company-standup-20261002.py` — assert lại **mọi con số**
trong báo cáo từ nguồn gốc (ops_guard --json, store/tasks.json, difflib, git, verify_done,
activity.json) + assert chính các doc (briefing/state) **không còn chứa số sai**.
Bắt được 2 lỗi của chính em: LLM chain 8→5, dedup origin 2026-08-01 vs 25/09.

## Đừng xoá script verify trước khi chạy lại được (02/10)
Lần trước em xoá hết script trong `Temp/` ngay sau khi đọc số → không còn cách nào
kiểm lại báo cáo, phải viết lại từ đầu. **Giữ script verify cho tới khi chạy PASS**,
rồi mới xoá. Verify phải **tái lập được từ nguồn**, không phải lưu con số đã in.

## Không được viết hash commit trước khi commit

Em ghi `→ \`d5c1f7a\`` vào state khi commit chưa tồn tại (placeholder trong đầu), rồi phải
commit xong mới quay lại patch hash thật (`ecb5217`).

**Luật:** **commit trước, rồi mới viết hash vào tài liệu.** Muốn ghi "đã sửa ở commit X"
mà X chưa có → commit trước, lấy `git rev-parse --short HEAD`, rồi patch. Tài liệu
chứa hash bịa là tài liệu sai theo đúng nghĩa.

## Gotcha nhỏ: field của `store/activity.json`

`store/activity.json` dùng key **`time`** (không phải `ts`/`timestamp`). Grep sai field →
thấy 0 entry → tưởng log trống/hỏng. Đọc `entry["message"]` để đếm WARN / fallback.
Muốn xác nhận LLM chain sống mỗi standup: 5× WARN OpenCode → 5× OK ByteDance, 0 None.

## Verify ad-hoc đúng cách (không có test suite canonical)

Repo **không có** test suite — script tự viết là chuẩn, gọi nó là "kiểm tra ad-hoc",
KHÔNG gọi "test xanh". Pattern hôm nay (đo độc lập `ops_guard`, không tin guard):

1. Đọc `store/tasks.json` thẳng, tự tính lại phase counter / STALE / dedup groups.
2. `assert` set id STALE **trùng khớp từng phần tử** với output `ops_guard --json` — so
   tập hợp, không so độ dài (2 tập cùng size khác id vẫn lọt).
3. Check commit chỉ chứa file cần thiết + `git ls-files` không lọt audio/env/face.
4. Xoá script sau khi chạy (`Temp/` là local, không commit).

## Mẫu lần này: 16/16 pass, 0 file rác

Sau khi sửa 2 assertion: **16/16 pass**. Commit `216416d` + `ecb5217` chỉ chứa
`briefing.md` + `shared/spec-dedup-context-scan-2026-10.md`; `git ls-files` không có
`.webm/.mp3/.opus/.m4a/.env/face_embedding/tg_env`.