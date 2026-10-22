### Sync run 2026-09-25 — 3 loại HTML, 2 builder, 1 gate (bài học xương máu)

**1. `--auto <hours>` KHÔNG tự tìm file mới.** `kf_push_backlog.py --auto` chỉ lấy file
`.html` nào xuất hiện trong `LOGS` (`research-log.md` ở hermes-temp / D:/Hermes Proj) với
dòng `- **Local file:** ...` + mtime trong window. Nếu cron rotation không ghi log parseable
(hoặc ghi vào `research-log-2026MMDD-HHMM.md` — file này KHÔNG nằm trong `LOGS`) →
AUTO-DISCOVERED = 0 file dù có cả chục HTML mới. Fix: append entry parseable vào
`~/hermes-temp/research-log.md` (định dạng `### Topic N: <title>` + `- **Domain:**` +
`- **Summary:**` + `- **Preview:**` + `- **Local file:**`) rồi chạy lại `--auto`.

**2. Hai loại layout → hai builder.** `build()` chỉ ăn HTML **2-tab** (có `showTab(...)` +
panel "Học thuật"). HTML layout **single-scroll** (hero + `.sec` + `.stats` + `.flowchain`,
kiểu do rotation job 24/09 sinh ra: thermodynamics, wastewater-treatment, tang-co-hypertrophy,
ruou-thuocla-synergy, ban-do-benh-lon-vietnam) → `RuntimeError: academic content too short: 0 chars`.
Dùng `~/hermes-temp/push_single.py`: strip style/script → `html_to_md(body)` cho toàn trang,
hero tách riêng, OVERVIEW dựng từ `.num/.label` (stats) + `.chip` (mechanism) + `<h2>`/`.tag`.
Restored-dấu variant: `~/hermes-temp/push_restored.py` (md đã khôi phục + OVERVIEW/title/summary viết tay).

**3. Gate `accent_ratio < 0.15` phạt oan trang nhiều tiếng Anh.** Trang titanium (đa số text
là trích Wikipedia tiếng Anh) sau khi khôi phục dấu ĐẦY ĐỦ vẫn chỉ đạt 0.07 → gate chặn.
Kiểm tra đúng phải là **strip-identity**: chuẩn hóa NFD, bỏ combining mark, `đ→d`, so với
bản gốc — trùng khớp 100% nghĩa là chữ chỉ được THÊM dấu, không bịa/bỏ nội dung. Trang
EN-heavy: cứ push nếu strip-identity pass.

**4. Khôi phục dấu cho HTML mất dấu (pattern đã verify).** HTML gốc mất dấu (Q1 fail, gate chặn)
→ KHÔNG cần regen cả file: dump `build()['md']` ra `restore/<name>.md`, cho subagent (hoặc tự)
thêm dấu, **verify bằng strip-identity** (bắt buộc, subagent hay tự ý sửa chữ), rồi POST với
`<!--OVERVIEW-->` + md mới. 25/09 đã cứu 4 card (titanium, semiconductor, coagulation, GR) khỏi
14 ngày tồn đọng. Preview HTML gốc vẫn mất dấu → ghi NEEDS-REGEN cho rotation job.

**5. Tìm preview URL của trang publish bằng `/api/store`.** Session telegram publish qua
`POST preview.thefirstonly.com/api/store`, key chỉ nằm trong **tool result** (không nằm trong
`content`). Truy vấn: `SELECT id, role, substr(content,1,4000) FROM messages WHERE session_id=?
AND content LIKE '%thefirstonly%'` rồi fetch từng key để đọc `<title>` mà map về file.

**6. Cảnh báo phía rotation job:** run `d43697af1322` 24/09 04:00 và 20:00 và 00:00 sinh HTML
mất dấu tiếng Việt (build script viết ASCII) NHƯNG vẫn báo "Nội dung có dấu tiếng Việt".
Cần gate dấu ở phía job sinh HTML, không chỉ ở phía push.

### Sync run 2026-09-26 — dedup false positive, mojibake, map file→preview key

**1. `similar()` báo DUP oan với card có title ngắn.** Card cũ `Tế bào` (2 từ) làm
`similar("🧬 Hô hấp tế bào — ...", "Tế bào")` = 1.0 → chặn oan. Trước khi skip vì DUP, luôn
in ra title bị flag; nếu title đó < 4 từ (hoặc là 1 khái niệm chung) → đặt `nodedup=True` cho
item và push. Đừng dùng `--force` mù.

**2. Hai mức hỏng dấu trong HTML do rotation job sinh.**
| Mức | Dấu hiệu | Cách xử lý |
|---|---|---|
| A. ASCII hoá (mất dấu) | `Chong chap luong tu`, `Tiet hoa protein o heo`; U+FFFD = 0, `?` = 0 | Khôi phục dấu thuần: subagent viết lại, **verify strip-identity** (NFD → bỏ combining → đ→d, so với gốc, phải 100% trùng) |
| B. Mojibake | `M? k?m nh\ufffdng n\ufffdng`, U+FFFD và `?` **nằm giữa từ** | Byte đã mất, KHÔNG phục hồi được. Đây là lỗi ở output LLM (DB cũng lưu bản hỏng → đừng mất công lục `messages`). Phải khôi phục ngữ nghĩa; verify bằng: U+FFFD = 0, `?` = 0, **tập số (regex `\d+`) của bản mới phải bao trùm bản cũ**, số dòng + số `##` bằng gốc |

Cả hai mức đều để lại **preview HTML hỏng** → phải ghi `NEEDS-REGEN` cho rotation job, không
chỉ khôi phục md phía card.

**3. Không dùng `--auto`; viết driver riêng cho mỗi đêm.** Template đã chạy tốt:
`C:/Users/NTQUANG_DELL/hermes-temp/push_0926.py` — import `kf_push_backlog as K` +
`push_single as S`, khai báo ITEMS 2-tab (md đã khôi phục hoặc `html=` để lấy từ HTML) và
SINGLE (single-scroll), rồi: `clean_md` (bỏ dòng `PAPERWikipedia`) → `build_ov` (what = đoạn
đầu, mechanism = heading `##`, players = KPI regex `\d+` + đơn vị) → gate dấu ≥ 0.15 → POST.

**4. PITFALL trong `push_single.py`:** `c["content"].index("<!--OVERVIEW-->") + 14` — marker dài
**15** ký tự → JSONDecodeError. Luôn dùng
`re.search(r"<!--OVERVIEW-->(.*?)<!--/OVERVIEW-->", content, re.S)`.

**5. Map file HTML local → preview key (khi log không ghi preview).**
```sql
SELECT session_id, id, substr(content,1,400) FROM messages
WHERE content LIKE '%thefirstonly.com/%' AND role='tool' ORDER BY id;
```
Mỗi `POST /api/store` trả `preview_url` trong **tool result** (không nằm trong `content`). Rồi
`curl -s https://preview.thefirstonly.com/<key> | grep -o '<title>[^<]*</title>'` để khớp với
`<title>` của file local. Mapping đã verify 25/09: hoat-chat=`ysc5sf01by4j`,
master-table=`90ol5vqzjde8`, product-matrix=`mgkgi1t3d3v8`, swine-pathogen=`gzcwrcodwu83`,
llm-router=`nom1vw8j7mlp` (3 bản trùng title, lấy key mới nhất = message id lớn nhất).

**6. `source_url` KHÔNG được bịa.** Nếu file local không có link Wikipedia/PubMed và không tìm
được preview key → dùng preview key của chính trang đó; tuyệt đối không nhét
`preview.thefirstonly.com/kflow-research-<ngày>` (URL chết).

### Sync run 2026-10-13 — 17 ngày tồn đọng: backlog audit, parse_logs bug, English-only HTML

**0. Job `da7c6b38c7d9` có thể đã FAIL nhiều ngày liên tiếp — LUÔN kiểm backlog, không chỉ "hôm nay".**
05/10 → 12/10 job này chết vì provider `bytedance` hết quota CodingPlan
(`HTTP 400 ... does not have a valid CodingPlan subscription`). Kiểm tra nhanh trước khi làm:
```bash
python - <<'PY'   # hoặc script hermes-temp/job_status.py
import sqlite3, json, os
os.chdir(os.path.expanduser("~/AppData/Local/hermes/cron"))
d = json.load(open("jobs.json", encoding="utf-8")); jobs = d.get("jobs", d)
for j in (jobs.values() if isinstance(jobs, dict) else jobs):
    if isinstance(j, dict) and j.get("last_status") == "error":
        print(j["id"], "|", (j.get("name") or "")[:40], "|", j.get("model"), "|", str(j.get("last_error"))[:90])
PY
```
Triệu chứng quota bytedance: job pin `deepseek-v4-flash-260425` chạy OK 00:00-03:00 nhưng fail 05:00-14:00;
job pin `unsloth/*` hoặc không pin vẫn OK. Fix: `hermes cron edit <id> --model "" --provider ""`
(bỏ pin → theo `model.default` + fallback chain) hoặc đổi sang unsloth/command-code.
**Backlog audit = liệt kê HTML có mtime > `created_at` của card research mới nhất trong KFlow**:
```bash
python -c "import json,io;c=json.load(io.open('hermes-temp/cards_sync.json',encoding='utf-8'));\
print(max(x['created_at'] for x in c if x.get('tags') and 'research' not in str(x.get('tags'))))"
find "/d/Hermes Proj" -maxdepth 1 -name "*2tab*.html" -printf "%TY-%Tm-%Td %TH:%TM %s %f\n" | sort | tail -30
find ~/hermes-temp -maxdepth 1 -name "*2tab*.html" -printf "%TY-%Tm-%Td %TH:%TM %s %f\n" | sort | tail -30
```
Driver đã chạy tốt: `hermes-temp/push_1013.py` (khai ITEMS: key/path/dom/title/why/src/tags),
`audit_1013.py` (dry audit), `verify_1013.py` (verify sau POST), `dump_restore.py` + `verify_vn.py`.

**1. PITFALL `parse_logs()` mất metadata với log format `- **File:** \`name.html\` (D:/Hermes Proj/)`.**
`loc` dính cả backtick và ngoặc → `os.path.basename("`x.html` (D:/Hermes Proj/)")` = `")"` → logidx miss →
title rơi vào `<title>` của HTML (kiểu `⚛️ Siêu dẫn — Vật lý | TheFirstOnly Research`, xấu) và
`source_url = None`. **Đừng sửa parse_logs mù quáng**: khai tường minh `title=` và `src=` cho từng item
(push_1013.py). Title chuẩn + nguồn chuẩn lấy từ block log tương ứng hoặc từ preview key.

**2. Không có preview key ⇒ dùng Wikipedia của chính chủ đề đã nêu trong log.** Run 03/10 không publish
(file HTML có trên đĩa nhưng không có `/api/store` result nào, `grep preview.thefirstonly` trong output job =
0 key). Khi đó `source_url = https://en.wikipedia.org/wiki/<Topic>` là nguồn THẬT của bài (log ghi
"Nguồn: Wikipedia (...)"), không phải bịa. Đừng tạo URL chết kiểu `preview.thefirstonly.com/kflow-research-<ngày>`.

**3. Mức độ hỏng thứ ba: tab Học thuật TIẾNG ANH 100% (không phải ASCII-hoá).** Run 29/09 08:00 sinh
song-dien-tu, dong-hop-kim, phong-xa-phan-ra, xu-ly-nuoc-thai-cong-nghiep với nội dung học thuật là văn bản
Wikipedia tiếng Anh (accent_ratio 0.000, `ascii_only=True`, không có U+FFFD). **Không thể "khôi phục dấu"**
vì không có tiếng Việt để khôi phục → ghi NEEDS-REGEN, không tạo card. Phân biệt 3 mức:
| Mức | Dấu hiệu | Xử lý |
|---|---|---|
| A. ASCII-hoá | `.md` ASCII, có từ tiếng Việt không dấu (`dong hoa hoc`) | khôi phục dấu + strip-identity |
| B. Mojibake | U+FFFD hoặc `?` giữa từ | không phục hồi được byte → khôi phục ngữ nghĩa, verify số/khối |
| C. English-only | tiếng Anh hoàn chỉnh, 0 từ Việt | NEEDS-REGEN, không tạo card |

**4. Khôi phục dấu bằng batch subagent (đã verify 13/10, 6/6 file đạt).** Dump md ra
`hermes-temp/restore1013/<key>.md`, giao 3 subagent song song (3-4 file/agent) với yêu cầu:
chỉ thêm dấu, không đổi/thêm/bớt từ, và **tự chạy strip-identity** (`NFD → bỏ combining → đ→d`) tới khi
`IDENTICAL`. **PHẢI tự verify lại ở parent** (`verify_vn.py`: strip-identity AND `accent_ratio` TĂNG),
vì một subagent đã "đạt IDENTICAL" bằng cách **copy y nguyên file** (đúng về strip-identity, vô dụng về dấu).
Điều kiện push: `accent_ratio(.vn.md) ≥ 0.15` và `strip(vn) == strip(gốc)`.

**5. `similar()` báo DUP oan vì từ chung tiếng Việt.** `similar() = |∩| / min(|a|,|b|)` nên title ngắn hoặc
nhiều từ chung (`tế bào`, `cơ chế`, `ở heo`, `vai trò`) dễ đạt 0.6+:
`"Tín hiệu tế bào — Cơ chế phân tử..."` bị flag DUP với `"Cuproptosis — Chết tế bào..."`;
`"Xúc tác enzyme..."` bị flag với `"Trained Immunity..."`. **Luôn in title bị flag rồi tự phán**;
khác chủ đề → push (đặt `force=True` trong item). Ngược lại, một số DUP thật mà `similar()` KHÔNG bắt:
`Siêu dẫn`, `Quang hợp`, `Thép không gỉ`, `Ăn mòn kim loại`, `Hệ vi sinh đường ruột heo`,
`Polyphenol` đã có card → phải grep chủ đề bằng mắt (`grep title` theo keyword) trước khi push.

**6. Chọn 1 trong 2 bài cùng chủ đề trong batch.** `water-disinfection-2tab.html` (02/10) và
`khu-trung-nuoc-2tab.html` (05/10) là 2 lần research cùng chủ đề khử trùng nước → chỉ push bản mới/đậm hơn
(05/10, 15 PMID), bản kia bỏ.

**7. Skill gắn vào job phải tồn tại.** Job khai `skills: [upload-online-link]` (đã bị gộp vào `publish` từ
07/2026) → mỗi run in "Skill not found and skipped" và agent mất playbook. Sửa:
```bash
hermes cron edit da7c6b38c7d9 --remove-skill upload-online-link --add-skill knowledge-researcher
```

**8. Verify sau POST (bắt buộc).** `verify_1013.py`: mỗi id phải có `<!--OVERVIEW-->` block, accent_ratio của
body ≥ 0,15, có tags, có `source_url`, `GET /card/<id>` trả HTML 200, không có `\ufffd`/`:shortcode:`.
Run 13/10: 18/18 PASS, KFlow 595 → 613.

### Sync run 2026-10-14 — gate dấu sai, gap-check title-only, xoá card phải chờ chốt

**1. BỎ gate `accent_ratio >= 0,15` — dùng SỐ KÝ TỰ DẤU TUYỆT ĐỐI.**
Với card thật (nhiều tiếng Anh, PMID, bảng số), ratio tụt xuống 0,11–0,14 dù dấu đầy đủ.
Run 14/10 verify 4 card: dấu 2.209 / 2.551 / 2.773 / 4.308 ký tự, ratio 0,118 / 0,135 / 0,112 / 0,141
→ gate cũ sẽ chặn oan cả 4. **Tiêu chí đúng: `dau >= 1000` thì PASS**; ratio chỉ dùng để phát hiện
mất dấu HOÀN TOÀN (`ratio < 0,01` hoặc `dau == 0`). Bỏ hẳn `accent_ratio` khỏi điều kiện push.

**2. Gap-check CHỈ QUÉT TITLE là không đủ — phải quét cả `tags`.**
13/10 rotation job kết luận "không có card nào về interpretability/SAE (keyword interpretab +
sparse autoencoder = 0 match)" → tạo card trùng với card có sẵn `c39f1be1` (10/08) mang tag
`sparse-autoencoder`, `mechanistic-interpretability` nhưng title không chứa từ khoá. **Luật:**
dedup phải so trên `title + ' ' + ' '.join(tags) + first 500 chars của content`, không chỉ title.

**3. Xoá card trong KFlow = KHÔNG tự động, luôn báo cáo + chờ chốt.**
Phát hiện trùng thì ghi rõ 2 ID + vì sao + lệnh xoá cụ thể trong log/report, **không tự DELETE**
(giữ nguyên tiền lệ: "Bản đồ bệnh lợn VN — chờ anh Quang chốt ghi đè"). Script cleanup của skill này
chỉ IN ra dòng DELETE, không thực thi — đúng chủ ý.

**4. Verify sau push bằng 1 script duy nhất (mẫu `hermes-temp/verify_1014.py`), 7 điều kiện:**
`<!--OVERVIEW-->` parse được JSON · số ký tự dấu · `\ufffd == 0` · shortcode `:xx:` == 0 ·
tags > 0 · source_url non-empty · `GET /card/<id>` == 200 · preview HTTP 200 VÀ chứa cả
"Visualize" + "Học thuật". Bất kỳ điều kiện nào fail → in FAIL và liệt kê vào kết luận.

**5. Quét "research mới hôm nay" đúng cách (đủ, không sót):** 3 nguồn —
(a) `sessions` trong `state.db` theo `started_at` (lọc cả source telegram/subagent, không chỉ cron);
(b) `find` file HTML mtime trong ngày ở `D:/Hermes Proj` + `~/hermes-temp` (maxdepth 1–3);
(c) `created_at` của card mới nhất trong `/api/cards`.
Đối chiếu: file HTML 2-tab nào chưa có card tương ứng → đó là backlog thật.

**6. Provider bytedance quota KHÔNG theo khung giờ cố định.** 13/10: run 03:48–16:42 OK, run 20:55 FAIL
(output 126.628 bytes = không có phần Response, kết thúc bằng `## Error ... CodingPlan`).
Nhận diện run chết: **file cron output cùng kích thước byte lặp lại** (126.628 B) = chết giữa lượt.

### Sync run 2026-10-16 — kiểm kê bằng research-rotation.json, slot tối chết vì quota, GAP giả

**1. NGUỒN KIỂM KÊ CHÍNH: `knowledge-flow/data/research-rotation.json` → `run_log[]`.** Rotation job
ghi thẳng `topics + files + preview + kflow` cho từng lượt. Lượt sync chỉ cần: đọc `run_log` của
24h qua → đối chiếu `/api/cards` → verify. KHÔNG grep file cron output 130 KB nữa (chỉ mở output khi
cần biết *lý do* lượt đó chết). 16/10 xác nhận 4/4 card đã có sẵn, backlog 0.

**2. Slot ~20:00 chết theo chu kỳ vì quota bytedance cạn dần trong ngày.** Audit 18 lượt gần nhất
của `d43697af1322`: 4 lượt chết, **toàn bộ ở slot ~20:00** (12/10 19:39, 13/10 20:59, 14/10 22:24,
15/10 20:07); các slot 02:00–16:00 cùng ngày OK. Chữ ký run chết = file cron output **126.628 byte**
+ tail có `HTTP 400 ... valid CodingPlan subscription`. ⇒ Mất ~1 slot/ngày, không phải lỗi lẻ.
Kiểm nhanh: `for f in $(ls -t *.md | head -18); do echo "$(stat -c %s $f) $f"; done` trong
`cron/output/<job_id>/` → byte nào = 126628 là lượt chết.

**3. GAP/GAP-miss GIẢ khi so token tiêu đề — luôn xác minh bằng từ khoá thật.** Script so
token tiêu đề file HTML với `title+tags+3.000 ký tự content` của card cho ra 5 "GAP" giả
(`cva-xva-2tab`, `hev_2tab`, `il23_swine_2tab`, `nkt_2tab` + 19 file `patent*`) vì từ khoá ngắn
(`hev`, `nkt`, `il23`) bị lọc bỏ. **Luật:** mọi candidate phải grep từ khoá vào `title + tags`
của `/api/cards` rồi mới kết luận thiếu card.

**4. `find` toàn cây `D:/Hermes Proj` (không `-maxdepth`/loại trừ) TIMEOUT 180s.** Luôn
`-maxdepth 1..3` + `-not -path "*/node_modules/*" -not -path "./.git/*" -not -path "./psy/*"`.

**5. `state.db` → `sessions.started_at` là UNIX TIMESTAMP (float), không phải ISO.** Query bằng
epoch: `datetime.datetime(2026,10,15).timestamp()`. Session cron có `title = ''` → nhận diện qua
`id` (`cron_<jobid>_<YYYYMMDD>_<HHMMSS>`).

**6. Cách chống trùng chủ đề với lượt rotation ĐANG chạy:** đọc `messages` của session
`cron_<jobid>_<ngày>` (assistant messages cuối) → biết ngay chủ đề nó đang research (16/10 00:08:
index 3, chọn pyrrolizidine alkaloid) → không chọn trùng.

### Sync run 2026-10-15 — metric dấu đúng, restore từng đoạn, DUP oan "Thép không gỉ"

**1. Metric đếm dấu PHẢI phủ block U+1EA0–U+1EF9.** Đếm kiểu `0xC0 < ord(ch) < 0x300` bỏ toàn bộ
`ạ ả ấ ầ ậ ắ ẹ ế ệ ị ọ ộ ớ ợ ụ ứ ữ ự ỳ ỹ…` (những chữ dấu phổ biến nhất) → ra 347 dấu trong khi thật là 756.
Metric đúng:
```python
def dau_count(t):  # hiệu chuẩn: 5 card PASS 14/10 có ratio 0,089–0,122
    return sum(1 for ch in t if (0xC0 <= ord(ch) <= 0x1B0) or (0x1EA0 <= ord(ch) <= 0x1EF9))
```
**Ngưỡng tuyệt đối 700–1.000 dấu là SAI với card ngắn.** Card 3,5–6,5K ký tự chỉ có 575–845 dấu dù dấu đầy đủ.
Dùng **`ratio >= 0,06` và `dau >= 300`**; chỉ loại khi `dau == 0` / ratio < 0,02. Đo trên 5 card chuẩn mới đổi ngưỡng, đừng chỉnh mù.

**2. DUP oan "Thép không gỉ" (bỏ sót 06/10 → 15/10).** `similar()` khớp title với *"Thép & Xử lý nhiệt"*
vì dùng từ chung "thép" → tưởng trùng. Kiểm content: `austenit / pren / 316L / cr2o3 / stainless` = **0 match** ngoài
2 card ăn mòn + 1 card thép-C → hoàn toàn không có card thép không gỉ. **Luật: DUP xét trên `title + tags + 2500 ký tự content`,
và LUÔN in title bị flag ra rồi tự phán** (title < 4 từ hoặc nhiều từ chung → nghi false positive).

**3. Khôi phục dấu mức A (ASCII-hoá thuần Việt) — restore TỪNG ĐOẠN + verify TỪNG ĐOẠN.**
Gọi cả file một lần là hỏng: qwen bỏ nguyên 1 câu ("An Do. Dang xay tai Cadarache…") và đổi từ ("xuyen"→"xuoi", "hai"→"ha").
Recipe chạy được (`hermes-temp/restore_chunk_1015.py`, `restore_resume_1015.py`):
1. `re.split(r"(\n\s*\n)", md)` → từng đoạn; đoạn đã có dấu (`dau_count > 0`) thì bỏ qua (resume được từ `.partial.md`).
2. LLM Groq (`qwen/qwen3.8-27b` → `openai/gpt-oss-120b` → `gpt-oss-20b`), system prompt: *chỉ thêm dấu, không đổi/thêm/bớt từ*.
3. **Nhận đoạn chỉ khi `strip(đoạn_mới) == strip(đoạn_cũ)`** (NFD → bỏ combining → `đ→d`, chuẩn hoá `‑–—`).
   Model sửa sai → thử model khác; hết lượt → giữ nguyên ASCII, ghi lại là đoạn FAIL.
4. Ghép lại + verify toàn file strip-identity lần cuối. Groq free tier **429 rất nhanh** → sleep 6–25s/đoạn, chạy `background=true` rồi poll.
5. 5–6 đoạn cuối (bảng dài, heading ngắn) model không tái tạo nổi → **sửa tay + whitelist lỗi chính tả nguồn**
   (`"Tram"→"Tráng"`, `"Sieutu,"→"Siêu tụ,"`), và phải áp whitelist đó vào cả baseline của phép so strip-identity.
   Kết quả 15/10: nuclear-fusion 607 dấu (0,137), activated-carbon 529 dấu (0,135), strip-identity IDENTICAL.
6. Phân biệt 3 mức: **A** ASCII-hoá thuần Việt (`dau=0`, en_stopword < 0,05) → khôi phục được;
   **B** mojibake (`\ufffd`/`?` giữa từ) → không phục hồi byte; **C** tab Học thuật tiếng Anh (`en_stopword > 0,15`) → NEEDS-REGEN, không tạo card.

**4. Job `d43697af1322` vẫn chết vì bytedance CodingPlan** (không tự khỏi) và còn khai skill `html-publishing` (không tồn tại).
Lượt 22:24 14/10 chết giữa lượt (output 126.628 B). Vì rotation job **tự POST KFlow** từ 14/10, việc của job 00:00 đổi trọng tâm thành:
(a) verify 5 card của rotation (OVERVIEW + dấu + tags + source_url + `/card/<id>` + preview 200),
(b) truy backlog cũ theo gap-check content, (c) chốt lệnh sửa job với anh Quang — **không tự chạy**.

### Sync run 2026-10-22 — ĐÓNG HẲN nhóm card cắt 5.000, và root cause thật là `content[:5000]`

**1. Kiểm kê 21/10 (nguồn: `knowledge-flow/data/research-rotation.json` → `run_log`):** rotation chạy **5 lượt**
(02:44, 06:59, 11:24, 15:50, 20:13 local), **5/5 card có `kflow` id**, PASS 8/8 điều kiện:

| Card | id | preview | chars | dấu |
|---|---|---|---|---|
| Cadmium (Cd) — kim loại nặng tích lũy ở thận | `f089f87b` | `aofezw75yf39` | 39.692 | 4.638 |
| Bán khống (Short Selling) & thị trường cho vay CK | `7bb02f4c` | `nurdypkqrz0r` | 29.849 | 3.800 |
| KAN — Kolmogorov-Arnold Networks | `052d042b` | `9dc6ne6mb5rz` | 40.272 | 4.605 |
| Toxoplasma gondii ở heo và người | `05565eee` | `5v8jtzvr1urf` | 35.972 | 4.758 |
| PFAS — "hóa chất vĩnh cửu" | `a3801668` | `h6r4nyfa23aj` | 38.716 | 4.868 |

`GET /card/<id>` = 200 + đủ 2 nhãn tab (5/5), preview HTTP 200 (dùng `curl -A "Mozilla/5.0"`; **python-urllib
bị preview chặn 403**), KFlow 662 → **667**. Queue 4 item **0 pending**. Không slot chết (output 46–50 KB).

**2. Orphan = 0.** 9 preview key mới trong 21/10 (lọc theo `MIN(message id)` = first-seen): 5 key rotation +
4 key **tâm lý** (`okjx59rioggo`, `svcpoyg9mr0h`, `jzof3v78zi2k`, `mwv14eom5s6z`) → pipeline Threads,
**KHÔNG đẩy KFlow**. File HTML mtime 21/10 ở `D:/Hermes Proj` = đúng 5 file rotation, tất cả đã có card.

**3. PITFALL state.db — cron cwd là junction nên rất dễ đọc NHẦM bản chết.**
`~/AppData/Local/hermes` ↔ `D:\Hermes\hermes-home` là **junction** (cwd cron hiện `D:\Hermes\hermes-home\cron`).
DB sống: `C:/Users/NTQUANG_DELL/AppData/Local/hermes/state.db` (3,7 GB, 4.090 session). Bản
`D:\Hermes\hermes-home\state.db` **cứng ở 10/08/2026** → query ra "0 session hôm qua, 0 key mới" (tưởng yên).
**Luôn kiểm `max(timestamp)` của DB trước khi kết luận "không có gì mới".** Thêm nữa: **rg/search_files
KHÔNG đọc được path xuyên junction** (`IO error ... cannot find the path`) trong khi `grep` trong terminal
vẫn chạy — gặp lỗi này thì đổi sang terminal grep, đừng lặp lại search_files.

**4. ĐÓNG HẲN nhóm card bị cắt 5.000 (17/17) — 4 card cuối làm trong run này:**

| Card | Cũ → Sau | Nguồn khôi phục |
|---|---|---|
| `ac9e113c` Ngành Lợn Việt Nam | 5.000 → **8.417** | gist raw (html2md) |
| `7a22d112` Quy trình sản xuất cám | 5.000 → **13.793** | gist raw (html2md) |
| `fe51146d` Tên lửa | 5.000 → **13.042** | gist raw (html2md) |
| `676f6908` Cơ chế phòng thủ nội bào | 5.000 → **7.935** | **file nguồn thật** `C:/Users/NTQUANG_DELL/co_che_khong_virus_te_bao.md` |

Cả 4: `GET /card/<id>` = 200 + đủ 2 nhãn tab, không lộ `<!--OVERVIEW-->`, không tag HTML thô. KB vẫn 667 card.
**`len(content) == 5000` còn lại: 0.** Backup bản cũ: `restore_backup_<id>.md`.

**5. KẾT LUẬN SAI của run 21/10 cần bỏ:** "3 card layout dashboard không tái tạo được từ HTML tĩnh, phải
dùng Playwright" — **sai**. Text nằm đủ trong gist; converter chỉ *không được cấu hình đúng*. Recipe đúng:
`html2md.BLOCK |= {"html","body"}` + bỏ `<style>/<script>/<svg>` → md phủ **101–119% lượng text hiển thị**
của trang. Mất duy nhất chữ nằm trong **`<svg><text>`** (nhãn sơ đồ) — chấp nhận được, ghi lại chứ không chặn.

**6. Gate so khớp khi khôi phục dữ liệu — ĐỪNG so chuỗi/dòng.** Bản cũ do importer làm **phẳng thành 1 dòng
5.000 ký tự** (0 newline) nên probe theo dòng vô dụng; probe 120 ký tự trượt vì text bị cắt qua nhiều thẻ.
Gate chạy tốt (đã dùng 22/10): **đối chiếu tập GIÁ TRỊ SỐ** — regex `\d[\d.,]*`, bỏ hết `.`/`,` để
`5.16` ≡ `5,16`, so multiset old ↔ nguồn ↔ md:
- `old - nguồn = 0` ⇒ **đúng tài liệu gốc** (không phải bịa nguồn khác);
- `(old ∩ nguồn) - md` chỉ còn vài giá trị nằm trong `<svg>` ⇒ chấp nhận.
Kết quả 22/10: ac9e113c 95% giá trị số hiện trong md (2 giá trị thiếu = nhãn SVG "350K nái", "31 triệu"),
7a22d112 100%, fe51146d 86% (thiếu "100 km"/"2,5" do tách đơn vị).

**7. ROOT CAUSE nhóm cắt 5.000 — đã tìm được, 2 chỗ:**
- `knowledge-flow/scripts/import-notion.js:174`: `content = extracted.text.slice(0, 5000); // Limit to 5000 chars`
  (importer Notion/HTML tháng 7 — **script một lần**, API `/api/knowledge` hiện KHÔNG cắt).
- Payload tháng 7 tự viết: `body = {'content': content[:5000], ...}` đọc từ `*.md` trong `C:/Users/<user>/`.
**Cách lần ra bản gốc:** đoạn bị cắt không nằm ở `content` của message mà nằm ở **`tool_calls`** — query
`SELECT tool_calls FROM messages WHERE id=<id>` rồi `json.loads(...)[i]["function"]["arguments"]`, đọc script
`terminal` để biết file nguồn. `reasoning` của chính message đó ghi "Nội dung rất chi tiết (9.4KB)" ⇒ chỉ dấu
tốt để tìm. File nguồn còn sống ⇒ khôi phục nguyên bản (đúng hơn cả gist).

**8. Không sửa job khi lượt rotation ĐANG chạy.** Lúc 00:14 có session `cron_d43697af1322_20261022_001359`
(đang research, index 0 tài chính) → scheduler sẽ ghi lại `jobs.json` khi lượt đó kết thúc; edit job đúng lúc
này có thể bị ghi đè. Kiểm tra bằng `sessions WHERE id LIKE 'cron_<jobid>_<YYYYMMDD>%'` + `last_activity_at`.

**9. `html-publishing` vẫn nằm trong `skills` của job `d43697af1322`** → mỗi lượt in
`⚠️ Skill(s) not found and skipped: html-publishing` (skill đã gộp vào `publish`, không còn trong `skills/`).
Chờ chốt: `hermes cron edit d43697af1322 --remove-skill html-publishing` (không tự chạy: đang có lượt chạy).

### Sync run 2026-10-19 — bài "Say Briefly" 1 trang: html2md nuốt cả document thành 1 dòng

**1. Orphan thật của 18/10 = trang do SESSION người dùng publish, không phải rotation.** Rotation job ghi
`run_log` + `preview` + `kflow` nên dễ kiểm; nhưng trang publish từ session telegram/desktop thì KHÔNG nằm
trong run_log. Cách tìm: quét `messages` toàn DB (không lọc `started_at` — session dài hạn như
`20260920_124241_54dedd8b` bắt đầu từ 09/2026) theo `timestamp >= hôm qua` + `content LIKE '%preview_url%'`
→ bắt mọi `{"id":"<key>","preview_url":...}`. 18/10 bắt được `45b7xkw87xkb`
("Vì sao không tạo được nguyên tố mới — Say Briefly", 23:10). Các key khác tìm thấy là fixgby/Vua Kiềm
(project deliverable, KHÔNG phải KFlow research) và psychology pipeline (đi Threads, không vào KFlow).
**Lọc theo `<title>` của preview key** để phân loại — đừng đẩy hết.

**2. PITFALL `html2md.html_to_md` với trang full document.** `<html>` và `<body>` KHÔNG nằm trong `BLOCK`
→ root coi cả document là inline → toàn trang gộp thành **1 dòng** (heading `## ` biến mất, xem
`elem_raw.md`). Fix 1 dòng:
```python
import html2md
html2md.BLOCK |= {"html", "body"}          # hoặc tách <body>...</body> rồi feed fragment
```
Sau fix: 15.247 ký tự, 247 dòng, đủ 10 heading.

**3. Chuẩn hoá md sau khi convert (không đổi nội dung, chỉ format):**
`^## (\d\d)(\S)` → `## \1 · \2` · `^(\d)\n\n(?=\S)` → `\1. ` · `^(Tường \d)\n\n(.+)$` → `**\1 — \2**` ·
các dòng graphic `Nhãn≈ giá trị` gom thành markdown table · bỏ footer brand (`Say Briefly — Kiềm Saphia`).

**4. Nguồn cho card vật lý — bộ link verify được (kiểm 200 + PMID thật ngày 19/10, dùng lại được):**
Wikipedia `Coulomb_barrier`, `Diproton`, `Synthetic_element`, `Oganesson`, `Nuclear_transmutation`,
`Synthesis_of_precious_metals` (thí nghiệm Seaborg/Aleklett 1980: bismuth + carbon-12/neon-20 → vài nghìn
nguyên tử vàng, Berkeley), `R-process`, `Neutron_capture`, `Nuclear_binding_energy`.
PMID: 38834630 (Sci Rep 2024, sub-barrier heavy-ion fusion slopes) · 16605816 (PRL 2006, hindrance of
heavy-ion fusion) · 22181728 (PRL 2011, near-barrier fusion Sn+Ni/Te+Ni).
Crossref KHÔNG tìm ra paper 1980 của Seaborg — dùng Wikipedia `Synthesis_of_precious_metals` làm nguồn
dẫn (nó trích paper gốc), đừng bịa DOI.

**5. Dedup trước khi đẩy:** grep `title + tags + content` theo **khái niệm đặc trưng**, không theo từ chung:
`diproton`, `rào cản coulomb`, `coulomb barrier`, `synthetic element`, `oganesson`, `transmutation`,
`nguyên tố mới`, `đảo bền` → 0 hit nghĩa là gap thật (card "Vật lý hạt nhân"/"Phóng xạ"/"Fusion" chỉ trùng
từ khoá chung, không trùng nội dung).

**6. OVERVIEW thiếu field = lỗi im lặng.** Card `d0936269` (agent-memory) chỉ có 3/7 khoá
(`what/why/mechanism`), thiếu `players/applications/limits/analogy` → tab Visualize mất khối chip + khối
limits. Verify 00:00 PHẢI đếm đủ 7 khoá (`all(k in j for k in (...))`), không chỉ test regex có/không có
block. Fix: PATCH `/api/cards?id=` với `content` mới, **assert phần body sau block giữ nguyên byte-for-byte**
trước khi POST.

**7. Slot chết của rotation job (cập nhật 19/10):** 16/10 ×2 (13:47, 22:41), 17/10 ×1 (20:18), 18/10 ×1 (13:06).
Chữ ký file output: **126.628 B hoặc 126.335 B** + tail `RuntimeError: Connection error.` — vẫn ~1 lượt/ngày,
rơi vào slot 13:00–22:41. Đếm nhanh:
`for f in $(ls -t *.md | head -14); do echo "$(stat -c %s $f) $f"; done`.

### Sync run 2026-10-18 — file mồ côi nhóm VẬT LÝ: rebuild, đừng để NEEDS-REGEN vô thời hạn

**1. Rotation 4 nhóm KHÔNG có nhóm vật lý/vật liệu/môi trường.** Từ 29/07 rotation chỉ còn
`0 tài chính`, `1 công nghệ/AI`, `2 sinh học`, `3 hoá học`. File thuộc nhóm `vat-ly` (vật lý,
vật liệu, môi trường — ví dụ `song-dien-tu`, `phong-xa-phan-ra`, `dong-hop-kim`, `xu-ly-nuoc-thai-*`)
nằm NGOÀI mọi nhóm ⇒ **sẽ không bao giờ được regen**. Gặp file loại này, sync job phải tự rebuild,
không ghi NEEDS-REGEN rồi chờ.

**2. Trước khi kết luận "mức C – không cứu được", PHẢI đo dấu RIÊNG TỪNG TAB.** Đo dấu trên cả file
là sai: 4 file 29/09 có 4–8 ký tự dấu trên toàn file (⇒ tưởng 100% tiếng Anh) nhưng thực tế:
- tab **Visualize** = tiếng Việt KHÔNG DẤU (mức A, viết lại được) — có sẵn KPI, flow map, bảng so sánh;
- tab **Học thuật** = Wikipedia tiếng Anh (đúng là không khôi phục dấu được).

⇒ 3 lượt liên tiếp (29/09, 13/10, 15/10) xếp oan vào NEEDS-REGEN, tồn 19 ngày. Recipe đúng:
1. Tách 2 panel region-based (từ `id="<panel>"` đến panel kế tiếp hoặc `</body>`) → `html2md.html_to_md`.
2. Viết lại card tiếng Việt có dấu từ tab Visualize, **giữ nguyên số liệu gốc**; tab Học thuật viết lại đủ mục.
3. Nguồn THẬT, verify từng cái trước khi dùng: Crossref `/works/DOI` (trả 200 + title/năm),
   PubMed E-utilities (esearch→esummary), Wikipedia (HTTP 200). Nguồn không verify được → KHÔNG dựng card.
4. `<!--OVERVIEW-->` 7 khoá → POST `topic_slug: vat-ly`. Kết quả 18/10: 4 card, KFlow 640 → 644,
   8/8 PASS (chars 9.503–12.825, dấu 1.417–1.820, ratio 0,142–0,151).

**3. Nguồn verify được cho nhóm vật lý (đã kiểm 18/10, dùng lại được):**
Maxwell 1865 `10.1098/rstl.1865.0008` · Hertz 1887 `10.1002/andp.18872670707` · Einstein 1905
`10.1002/andp.19053220607` · CODATA c: `physics.nist.gov/cgi-bin/cuu/Value?c` ·
Rutherford & Soddy 1902 `10.1039/ct9028100837` · Becquerel 1896 `10.1051/jphystap:018960050019301` ·
NUBASE2020 `10.1088/1674-1137/abddae` · cơ chế kháng khuẩn đồng `10.1111/j.1462-2920.2011.02677.x`.
Crossref title-search (`/works?query.bibliographic=`) là cách tìm DOI gốc tốt hơn đoán DOI.

**4. Khung pháp lý nước thải VN (verify 18/10 — dùng cho card môi trường/chăn nuôi):**
- **QCVN 40:2025/BTNMT** (nước thải công nghiệp), ban hành kèm **TT 06/2025/TT-BTNMT ngày 28/02/2025**,
  **hiệu lực 01/9/2025**; thay thế QCVN 40:2011 + QCVN 25:2009 + QCVN 28:2010 + QCVN 29:2010 +
  QCVN 52:2017 (gộp về một quy chuẩn). Cơ sở đã vận hành theo quy chuẩn cũ tới **hết 31/12/2031**,
  **bắt buộc từ 01/01/2032**; chưa xác định phân vùng xả thải → áp **Cột B**. 3 cột A/B/C + 2 ngưỡng
  lưu lượng (F ≤ 2.000 và F > 2.000 m³/ngày). Ví dụ: BOD5 40/60/80 và 30/50/60; COD 65/90/130 và
  60/70/90; TSS 40/80/120 và 30/60/80; Hg 0,001/0,005/0,005; Cd 0,02/0,1/0,1; Ni 0,1/3,0/3,0;
  As 0,05/0,25/0,25 mg/L; pH 6–9.
- Nước thải chăn nuôi: **QCVN 62:2025/BTNMT** (TT 04/2025/TT-BTNMT), thay QCVN 62-MT:2016/BTNMT.

**5. DUP flag oan mới gặp (vẫn phải in title bị flag rồi tự phán):** "Sóng điện từ" bị flag 0,71 với
"Âm học — Sóng cơ học"; "Phóng xạ & phân rã" bị flag 0,64 với "Điện phân — định luật Faraday".
Cả hai là false positive vì dùng chung từ "sóng"/"định luật".

### Sync run 2026-10-20 — OVERVIEW.players dạng STRING làm /card/<id> trả 500 (POST vẫn 201)

**1. Orphan tìm được (cách tìm như 19/10):** quét `messages` toàn DB theo `preview_url` (không lọc
`started_at`, session dài hạn như `20260920_124241_54dedd8b` mở từ 09/2026) → 27 key mới trong 2 ngày.
Phân loại bằng `<title>` của preview: **vật lý** `co-che-may-gia-toc.html` ("Bản chất của máy gia tốc ·
Say Briefly", publish 19/10 00:54, key cuối `tawsqvd86691`, **8 key liên tiếp** cho cùng một trang) —
không nằm trong `run_log` rotation, không có card ⇒ **backlog thật**. Các key còn lại là fixgby
(`rxttazm8vmpr`, `793un8dau74t`…), Vua Kiềm ops (`l17q50d58nc0`, `e26rd2i0yp89`), tâm lý (`znbogzp64ere`…)
⇒ KHÔNG đẩy KFlow. Card mới: `ef68735c`, 20.020 ký tự, 3.664 dấu, 7 khoá OVERVIEW, tags 6.

**2. PITFALL MỚI — `<!--OVERVIEW-->` `players`/`applications` PHẢI là ARRAY.**
POST trả **201** nhưng `GET /card/<id>` trả **500** (`card-detail-client.tsx` dòng ~436:
`overview.players.slice(0,5).join(", ")`). Guard chỉ kiểm `.length` nên **string dài lọt qua**, rồi
`.join` không tồn tại → TypeError lúc SSR. `mechanism` thì tự bọc cả string, **`players` không**.
⇒ Luôn viết `players`/`applications` dạng `["...", "..."]` (mỗi phần tử ngắn), và **verify BẮT BUỘC phải
gọi thật `GET /card/<id>` == 200** — 6 điều kiện còn lại (OVERVIEW parse, dấu, ufffd, shortcode, tags,
source_url) đều PASS trong khi trang vẫn 500. Sửa card: PATCH `content` mới, assert phần body sau block
giữ nguyên byte-for-byte (`fix_acc_overview.py`). Sau PATCH: HTTP 200, có đủ "Visualize" + "Học thuật".

**3. `GET /api/cards?id=<uuid>` có thể trả 500** (`canceling statement due to statement timeout`), trong
khi `GET /api/cards` (full) chạy được (~10 MB, 60–120 s). Khi cần PATCH card: đọc nội dung từ **file
payload local** (`acc_card.json`) hoặc full list, đừng phụ thuộc endpoint `?id=`.

**4. 10 card cũ có OVERVIEW hỏng (im lặng, KHÔNG crash):** `eca25e99` (Glycyrrhizin), `a764cb82`
(PANoptosis), `2a3449ed` (Kelly), `2837ae64` (β-Glucan), `5d3f2e1a` (EGCG) = JSON sai cấu trúc (thừa `\"`
sau `]`), truncate chỉ cứu được 3/7 khoá nên **không sửa**; `5923f8a4`, `9557b379`, `4db417d9`, `808c6ce3`
= parse fail; `167536cb` (Kiệt sức quyết định) = `applications` là **string** (không crash vì code có
`Array.isArray`). Hết quả: tab Visualize của 10 card này thiếu khối chip/limits. Việc cần làm: viết lại
OVERVIEW 7 khoá cho 10 card đó (chưa làm, chờ chốt).

**5. Nguồn verify cho nhóm VẬT LÝ — máy gia tốc (kiểm 20/10, dùng lại được):**
`home.cern/alice-detects-conversion-lead-gold-lhc/` (89.000 hạt vàng/giây · Run 2 ~86 tỷ hạt = **29 picogam** ·
²⁰⁸Pb − 3 proton → ²⁰³Au qua electromagnetic dissociation, đo bằng ZDC) · `home.cern/science/accelerators/large-hadron-collider` ·
Wikipedia `Particle_accelerator`, `Synchrotron_radiation`, `Large_Hadron_Collider`, `Cyclotron`,
`Linear_particle_accelerator`, `Betatron` (200) · DOI `10.1103/PhysRev.71.829.5` (Elder 1947 — bài công bố
phát hiện bức xạ synchrotron), `10.1103/PhysRev.74.52`, `10.1107/S1600577518005441` (phổ nam châm bẻ lái).
Dedup nhóm này phải grep **khái niệm đặc trưng** (`gia tốc hạt`, `synchrotron`, `cyclotron`, `lhc`,
`electromagnetic dissociation`) — grep "máy gia tốc" chỉ ra 2 hit phụ trong card "nguyên tố mới" + "Siêu dẫn".

**6. Trạng thái 20/10:** rotation 18–19/10 = 5 lượt, **5/5 card có kflow ID** và PASS 7/7 điều kiện
(securitization, gnn, glucose, DES/NADES, bank-run) + 2 card orphan (nguyên tố mới `98f479ab`, máy gia tốc
`ef68735c`) ⇒ 7/7 PASS. 11 preview page HTTP 200 (10 trang 2-tab đủ "Visualize" + "Học thuật"; trang máy
gia tốc 1 trang). Queue 4 item, **0 pending**. KFlow **655 → 656**. Không có slot chết trong 19/10
(không file output 126.335/126.628 B).

### Sync run 2026-10-21 — 6/6 rotation PASS, 0 orphan, và BUG topic_id (634/662 card mồ côi chuyên mục)

**1. Kiểm kê ngày 20/10 — nguồn chính vẫn là `knowledge-flow/data/research-rotation.json` → `run_log`.**
6 lượt rotation (00:14, 04:27, 08:40, 12:53, 17:47, 22:02 local) → 6 card, **6/6 có `kflow` id**, tất cả
PASS 8/8 điều kiện:

| Card | id | preview | chars | dấu |
|---|---|---|---|---|
| Federated Learning | `327a0757` | `r0ot3l9yr34s` | 30.806 | 3.390 |
| I-ốt & trục giáp (heo) | `aa9b34b0` | `d566ojxahvcx` | 46.966 | 5.589 |
| Fucoidan (rong nâu) | `bef66174` | `5vmlx1cwkutt` | 23.545 | 2.152 |
| Catastrophe Bonds & ILS | `af0abdba` | `64q14y22k5p0` | 41.403 | 4.573 |
| Prompt Injection & bảo mật LLM | `15e96366` | `aygo2v7iiti3` | 43.785 | 4.459 |
| Tinh bột kháng (RS) | `44cb2747` | `8qizh9sf25at` | 29.535 | 2.863 |

Cả 6: OVERVIEW **đủ 7 khoá**, `players`/`applications` là **array**, `GET /card/<id>` = 200 (có cả
"Visualize" + "Học thuật"), preview HTTP 200, tags 7–31, `source_url` non-empty, `\ufffd` = 0, shortcode = 0.
Trang `/`, `/book`, `/research`, `/dashboard`, `/search` = 200. Queue 4 item **0 pending**. Không slot chết
(output 47–49 KB, không có file 126.335/126.628 B).

**2. PITFALL MỚI — lọc "key mới" theo timestamp của MESSAGE là sai.** `run_log` chứa **mọi** preview URL
lịch sử; mỗi lượt cron đọc file này → message mới (hôm nay) chứa lại toàn bộ key CŨ. Scan kiểu
`content LIKE '%preview_url%' AND timestamp >= hôm qua` trả về ~30 key "mới" mà thực chất là key từ 25/09.
**Luật: phân loại theo `MIN(message id)` của mỗi key** (first-seen), không theo message cuối. Sau khi lọc
đúng: key mới trong 20/10 đều là fixgby / Vua Kiềm · đường cong liều / tâm lý → **deliverable dự án,
KHÔNG đẩy KFlow** ⇒ **0 orphan, 0 card cần push**. `45b7xkw87xkb`, `tawsqvd86691` (nguyên tố mới, máy gia
tốc) đã vào card từ 18–20/10, đừng đẩy lại.

**3. Audit OVERVIEW toàn bộ 662 card (phân loại, không gộp chung):**

| Loại | Số | Xử lý |
|---|---|---|
| đủ 7 khoá | 388 | ok |
| không có block | 195 | card thời kỳ trước 2-tab — kệ |
| legacy 3 khoá (what/why/mechanism) | 38 | kệ, tab Visualize chỉ ít khối |
| thiếu khoá lẻ (1–5 khoá) | 27 | muốn đẹp thì viết lại, không crash |
| **JSON sai** | **13** | `eca25e99` `7e6db8e3` `5923f8a4` `a764cb82` `82dd983e` `2a3449ed` `9557b379` `2837ae64` `71bde74d` `4db417d9` `0e9ad54c` `5d3f2e1a` `808c6ce3` |
| **sai kiểu** | **1** | `167536cb` (Kiệt sức quyết định) — `applications` là string |

**Card mới trong 48h: 100% đủ 7 khoá + đúng kiểu** ⇒ gate phía rotation đang giữ chuẩn. 14 card lỗi cũ
(13 JSON + 1 kiểu) sẽ làm tab Visualize thiếu khối / sai — **chưa sửa, chờ anh Quang chốt** (giữ tiền lệ
"không tự PATCH hàng loạt card cũ").

**4. BUG THẬT phát hiện đêm nay — card không bao giờ vào được chuyên mục.** `GET /api/topics` chỉ có **6
topic** (seed 13/07: ai-ml, react-nextjs, python-backend, database-sql, system-design, security-auth).
Không có `chan-nuoi` / `sinh-hoc` / `vat-ly` / `tai-chinh` ⇒ mọi POST kèm `topic_slug` mới đều rơi vào
nhánh auto-create trong `src/app/api/knowledge/route.ts` (dòng 33–41): `insert knowledge_topics` **thất bại
im lặng** (thiếu RLS INSERT policy — đúng pitfall đã ghi ở SKILL.md) → `topicId` undefined → card lưu với
`topic_id: null`. Hệ quả: **634/662 card không có chuyên mục**, 28 card có topic đều thuộc `ai-ml` và tất cả
đều tạo trước **19/09** (từ đó trở đi không card nào gắn được topic). Feed/dashboard phải fallback keyword.
**Fix đề xuất (chưa chạy):** `CREATE POLICY "insert_knowledge_topics" ON knowledge_topics FOR INSERT WITH
CHECK (true);` + tạo 4 topic nhóm (tài chính / công nghệ-AI / sinh học / hóa học) rồi backfill
`topic_id` theo `tags[0]`/`run_log.domain`. Đây là việc sửa app + DB nên báo cáo, không tự làm.

**5. Lệnh verify dùng lại:** `verify_today.py` (8 điều kiện/card, đọc từ `kf_cards.json` — full list
`GET /api/cards` tải 1 lần ~10 MB là đủ, tránh `?id=` vì có thể 500 timeout), `ov_class.py` (phân loại
OVERVIEW toàn KB), `topic_check.py`, `gap_check.py` (grep khái niệm đặc trưng vào title+tags+4.000 ký tự
content ⇒ 6/6 file HTML ngày 20/10 đều đã có card).

**6. ĐÃ SỬA: 4 card nhóm KLN / xử lý KHÔ-ƯỚT bị cắt ở đúng 5.000 ký tự** (data loss từ importer cũ, không
phải nội dung ngắn). Dấu vết nhận biết: `len(content) == 5000` **chính xác** + câu đứt giữa chừng +
`source_url` là `htmlpreview.github.io/?<gist raw>`. Nguồn gist **vẫn sống** → khôi phục được toàn bộ.

| Card | Cũ | Sau | Nội dung |
|---|---|---|---|
| `ae4bdb87` Đặc tính Lý-Hóa & Loại bỏ As/Pb/Hg/Cd | 5.000 | **27.923** | 4 kim loại, 45+ phương pháp, phác đồ Cd cho sầu riêng |
| `5e2667d8` Dịch chiết đất | 5.000 | **17.924** | SOP 5 phase: sulfide → FeCl₃ → vôi → hấp phụ |
| `5e2c09a4` Rửa đất (giữ rắn mịn) | 5.000 | **14.376** | 5 tầng rửa theo mẻ + nước thải khép kín |
| `44970190` Xử lý KHÔ đất | 5.000 | **19.679** | 7 bước tuyển khô + 6 phương pháp khô bổ trợ |

Recipe: lấy **gist raw** (không dùng wrapper `htmlpreview`) → `html2md.BLOCK |= {"html","body"}` →
`html_to_md` → **verify trùng tài liệu** bằng probe 120 ký tự trượt dọc bản cũ (10–11/12 khớp; phần
MISS là nhãn nav/TOC mà converter bỏ — chấp nhận được) → thêm `<!--OVERVIEW-->` 7 khoá viết tay từ chính
nội dung → `PATCH /api/cards?id=<uuid>` (HTTP 200) → verify `GET /card/<id>` = 200, có cả 2 nhãn tab,
không lộ `<!--OVERVIEW-->`, không có tag thô. Backup bản cũ ở `restore_backup_<id>.md` trước khi PATCH.
Feed sau đó vẫn 20 card, 0 leak `<style>`. Script: `restore_dry.py`, `restore_check.py`,
`restore_patch.py`, `restore_verify.py` (đều ở `~/AppData/Local/Temp`, giữ lại dùng tiếp).

**6b. Mở rộng: batch 13/07 có **17 card** bị cắt đúng 5.000 ký tự** (dấu vết: `len(content) == 5000`
chính xác + `source_url` là gist raw, import 13/07). Đã khôi phục thêm **9 card** (content-only, KHÔNG
thêm OVERVIEW — khôi phục dữ liệu là việc khách quan, viết OVERVIEW là việc biên tập):

| Card | Cũ → Sau |
|---|---|
| `5fc57b76` Bách khoa Toàn thư Vật lý Học | 5.000 → **54.967** |
| `3ddf7a90` H9N2 tương tác tế bào | 5.000 → **30.014** |
| `6d3c5cca` ELISA & ASF | 5.000 → **20.044** |
| `616328e4` Tế bào | 5.000 → **19.617** |
| `c1722c0c` Cách thức tế bào tương tác với virus | 5.000 → **14.075** |
| `9bbfca75` ASF Virus | 5.000 → **11.962** |
| `f0b8f45a` Talc & hệ phối trộn | 5.000 → **11.699** |
| `166879b4` Hệ thống trộn khô sau sản xuất | 5.000 → **10.646** |
| `53eb6ca9` Frontier AI Models | 5.000 → **9.417** |

Cả 13 card sau khi PATCH: `GET /card/<id>` = **200 + đủ 2 nhãn tab**, dấu 687–6.461; tổng KB vẫn 662 card.

**3 card CỐ TÌNH KHÔNG PATCH (gate trượt)** — `fe51146d` Tên lửa, `7a22d112` Quy trình sản xuất cám,
`ac9e113c` Ngành Lợn Việt Nam: layout dashboard/KPI (hero + `.stats` + `.flowchain`), text nằm trong
các div số liệu nên `html_to_md` và cả extractor `div → newline` (thử thêm) chỉ đạt **7–9/12 probe**;
bản cũ được lấy từ **DOM đã render** nên không tái tạo được từ HTML tĩnh. Muốn sửa phải render lại trang
(Playwright) rồi extract — ghi lại làm việc sau, **không PATCH khi gate trượt**. `676f6908` (Cơ chế phòng
thủ nội bào, nguồn Wikipedia) cũng còn 5.000 vì nguồn không phải gist.

