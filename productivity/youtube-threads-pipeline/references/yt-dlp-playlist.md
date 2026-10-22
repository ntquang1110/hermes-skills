# Lấy danh sách video một YouTube playlist (Windows / Quang)

## Cấu hình
- **yt-dlp KHÔNG nằm trong venv python** (`python` = Hermes venv 3.11 → `import yt_dlp` = ModuleNotFoundError).
- yt-dlp cài trong user Python 3.14 site-packages. Gọi thẳng interpreter Python 3.14:
  ```
  /c/Python314/python -m yt_dlp ...
  ```
- `pip show yt-dlp` → `Location: C:\Users\NTQUANG_DELL\AppData\Roaming\Python\Python314\site-packages` (xác nhận 3.14).

## Dump playlist (flat, không tải video)
```bash
/c/Python314/python -m yt_dlp --flat-playlist -J \
  "https://www.youtube.com/playlist?list=<PLAYLIST_ID>" --no-warnings \
  2>/dev/null | /c/Python314/python -c "
import sys, json
data = json.load(sys.stdin)
print('TOTAL:', len(data['entries']))
for i, e in enumerate(data['entries'], 1):
    print(f\"{i}|{e.get('id')}|{e.get('title')}|{e.get('duration', '?')//60 if e.get('duration') else '?'}m\")
"
```
- `--flat-playlist` chỉ lấy metadata (id, title, duration), nhanh, không cần tải.
- `-J` xuất toàn bộ dưới dạng 1 JSON — pipe trực tiếp vào python để parse + in bảng, tránh ngập terminal bằng raw JSON.
- duration trả về giây; `//60` đổi ra phút.

## Tìm playlist từ tên
Cách rẻ nhất: curl trang kết quả tìm kiếm, grep `playlist?list=`:
```bash
curl -sL --max-time 20 "https://www.youtube.com/results?search_query=<tên+có+dấu+cộng>" \
  -H "User-Agent: Mozilla/5.0" | grep -oE 'playlist\?list=[A-Za-z0-9_-]+' | sort -u
```
Trả về nhiều playlist — xác minh đúng bằng title: curl `playlist?list=<ID>` rồi grep `"title":"..."`.

## Case đã dùng
- MIT 14.02 Principles of Macroeconomics, Spring 2023 (MIT OpenCourseWare):
  `PLUl4u3cNGP62EXoZ4B3_Ob7lRRwpGQxkb`, 25 lecture ~44-52 phút/bài, video IDs `heBErnN3ZPk` (L1) ... `spY5kl_EYDU` (L25).
- How Leaders Lead (channel, @HowLeadersLead): dump qua `https://www.youtube.com/@HowLeadersLead/videos` — channel dùng cùng flat-playlist JSON, mỗi entry sẵn `duration` (giây) để lọc clips <30 phút. 282 tổng → 109 giữ. Chi tiết: `podcast-channel-ingest.md`.

## Sai lầm tránh
- `python -m yt_dlp` (venv) → `ERROR: No module named yt_dlp` / exit 0 rỗng. Dùng `/c/Python314/python` (Python 3.14 win, ổ cứng đủ).
- Đừng dùng `--flat-playlist` với `-o`/`--write-info-json` — không cần cho mục tiêu lấy id+title.