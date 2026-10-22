# Briefing staleness + số liệu sai lặp lại (02/10/2026)

Bài học từ 3 ngày liên tiếp agent dẫn số liệu cũ (CMO 01/10, CTO 02/10).

## 1. ROOT CAUSE: `briefing.md` body đóng băng, footer tự nhảy

`cmd_standup()` (và script standup) chỉ update **footer**:
```
**Standup (last):** 2026-10-02 09:03:42
**Last Updated:** 2026-10-02 09:03:42
```
**KHÔNG viết lại body.** Agent đọc `briefing.md` → thấy timestamp MỚI → tưởng số trong đó
cũng mới → dẫn số cũ.

Thực tế 02/10: CTO viết "#8 chờ Quang — 4 ngày rồi" (số của 30/09) trong khi
`ops_guard` đo **6.0 ngày**. Cùng lỗi CMO mắc 2 ngày liên tiếp 01/10.

→ **Nhắc agent không được. Phải fix data.**

### Fix mỗi standup (bắt buộc)
Viết lại **TOÀN BỘ** body `briefing.md` bằng số guard đo hôm nay (KHÔNG copy body cũ),
rồi thêm dòng cảnh báo ở đầu:

```markdown
## ⚠️ ĐỌC SỐ Ở ĐÂY NHƯ ẢNH CHỤP, KHÔNG PHẢI SỐ MỚI
File này ghi lúc 09:05 mỗi standup. Số "ngày stale" là ảnh chụp tại thời điểm đó.
**Agent KHÔNG được dẫn lại số trong file này.** Muốn số thật phải tự chạy
`python hub/ops_guard.py --json`.
```

### Fix triệt để (CẦN QUANG DUYỆT — đụng code)
Inject output `ops_guard --json` vào prompt `daily_standup()` trong `agents/base_agent.py`
→ agent đọc số thật mỗi ngày thay vì đọc số trong briefing.

## 2. Đo lại số phiên trước bằng NHIỀU cách trước khi kết luôn "sai"

Sim dedup trong briefing 30/09: `0.87 / 0.77 / 0.75 / 0.72 / 0.66`.
Đo lại 02/10 bằng **3 phương pháp**:

| pair | title | desc | title+desc ghép | briefing 30/09 |
|---|---|---|---|---|
| #43↔#48 | 0.801 | 0.786 | 0.284 | **0.87** |
| #43↔#51 | 0.775 | 0.352 | 0.571 | 0.77 |
| #46↔#54 | 0.737 | 0.416 | 0.513 | 0.75 |
| #48↔#51 | 0.715 | 0.394 | 0.560 | 0.72 |
| #45↔#52 | 0.650 | 0.287 | 0.416 | 0.66 |

→ Không cách nào ra 0.87 → số 30/09 bị **thổi phồng**. Đã sửa → commit `fb3b500`.
Kết luận "9 việc" vẫn ĐÚNG (@0.70 = 9 nhóm, @0.62 = 8 nhóm) → chỉ số sai, không phải kết luận sai.

**Quy tắc:** đo ≥2 phương pháp rồi mới kết luôn "phiên trước sai". Tháng trước suýt ghi
"30/09 sai" — hóa ra 30/09 đúng và bản spec hôm đó sai. Sim là tham số quyết định ngưỡng
dedup, lệch 0.07 là đổi cả quyết định.

## 3. `read_file` trên `briefing.md` trả "binary file"

File là text UTF-8 thuần (verify: 0 null byte, 0 control char, chỉ CRLF).
`read_file` vẫn báo `is_binary: true` → phải đọc bằng:
```bash
python -c "t=open('briefing.md','rb').read().decode('utf-8'); print(t)"
```
Kiểm chứng trước khi tin `is_binary`:
```bash
python -c "raw=open('briefing.md','rb').read(); print('BOM',raw[:3]==b'\xef\xbb\xbf','null',raw.count(b'\x00'),'crlf',raw.count(b'\r\n'))"
```

## 4. Ghi `briefing.md` phải giữ CRLF

`write_file` (Hermes tool) ghi LF → git diff toàn file + file có thể bị đánh dấu binary.
Ghi bằng python bytes:
```python
open('briefing.md','wb').write(body.replace('\n','\r\n').encode('utf-8'))
```
Verify sau khi ghi: đọc lại bằng `python -c`, check `b'\r\n'` còn, check các số cần thiết có mặt.

## 5. `store/activity.json` schema phẳng

```json
{"time": "2026-10-02 09:01:53", "message": "[WARN] OpenCode API error (Dev1): {...} — fallback ByteDance"}
```
Field = `time` + `message`. **KHÔNG có** `ts` / `agent` / `ok` / `model`.
Phải regex trong `message` để tách agent + trạng thái:
```python
warn = sum("[WARN]" in e["message"] for e in recent)
ok   = sum("[OK]" in e["message"] for e in recent)
agent = re.search(r"\(([^)]+)\)", e["message"]).group(1)
```

## 6. Trạng thái ngày 02/10 (baseline để so sánh)
- Guard: STALE=13 / NO_DC=0 / WAKE=0. Phase: completed 41, planning 11, in_progress 1 (#8), review 1 (#47).
- 5/5 agent sống. OpenCode Go hết sub → ByteDance fallback, 8 WARN → 7 OK.
- 0 task `mode=agent` active → **không wake được** (đo bằng script, không suy đoán).
- 3 agent dẫn sai số cũ (CTO 4 ngày, CMO sim 0.87), Dev1/QA/Content nói đúng.
- `git pull --rebase` FAIL "unstaged changes" khi briefing vừa sửa → commit file trước, rồi pull.