# Threads Comment Review (post-engagement monitoring)

Use when user asks "xem bài post hôm qua, mọi người comment gì, phản hồi tiêu cực gì, tại sao, và comment đó có đúng không" cho một bài đã đăng.

## 1. Tìm bài post đã đăng

- Đọc `youtube-schedule.json` (`C:/Users/NTQUANG_DELL/AppData/Local/hermes/cache/`) → tìm item theo title/url, check `status=posted` + `posted_date`.
- Queue item KHÔNG lưu post URL → phải tìm trên profile Threads.

## 2. Đọc profile để lấy post link (Playwright + session cookies)

Session cookies: `C:/Users/NTQUANG_DELL/.hermes/threads_state.json` — dạng list cookies. Pattern đã verify:

```python
import json
from playwright.sync_api import sync_playwright

with open('C:/Users/NTQUANG_DELL/.hermes/threads_state.json', encoding='utf-8') as f:
    state = json.load(f)
cookies = state.get('cookies', state if isinstance(state, list) else [])

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
        viewport={"width": 1280, "height": 900}
    )
    ctx.add_cookies(cookies)
    page = ctx.new_page()
    page.goto("https://www.threads.com/@ntquang1110", timeout=45000)
    page.wait_for_timeout(8000)
    # Lấy link bài: a[href*='/post/'] — bài mới nhất prefix code gần nhất
```

- Nếu bị redirect sang login → session hết hạn, chạy `threads_login.py`.
- Bài mới nhất (post hôm nay/3h trước) có post-id prefix mới nhất; đối chiếu nội dung đầu bài với queue title để chắc chắn đúng bài.

## 3. Đọc comments (scroll + expand)

- Mở post URL trực tiếp: `https://www.threads.com/@ntquang1110/post/<POST_ID>`
- **Scroll nhiều lần** (`page.mouse.wheel(0, 1200)` x 6-8, wait 2s mỗi lần) — comments load theo scroll, không có sẵn ngay.
- **Click "Show replies"** (`page.locator("text=Show replies")`) để mở reply ẩn — nếu không click sẽ bỏ sót comment.
- Comments nằm trong cùng selector `div[data-pressable-container="true"]` với main post. Container đầu = main post (text bắt đầu bằng username + giờ), các container sau = comments. Mỗi container: `username | giờ | nội dung | Translate | N likes | N replies`.
- Stats ở cuối main post dạng `12 | 5 | 2` = likes | comments | reposts.

## 4. Fact-check comment (bắt buộc)

- Mọi claim tiêu cực trong comment phải verify bằng nguồn (Wikipedia API, trang chính thức, tin tức) trước khi kết luận "comment sai".
- Dùng Wikipedia REST: `https://en.wikipedia.org/w/api.php?action=query&titles=<Title>&prop=extracts&exintro=1&explaintext=1&format=json`
- Phân loại: comment ĐÚNG (lỗi từ bài), comment đáng tranh luận (có cơ sở), comment công kích vô cớ.

## 5. Báo cáo

Cấu trúc báo cáo đã anh duyệt:
1. Bài post + stats (likes/comments/reposts)
2. Bảng toàn bộ comment (user | giờ | nội dung)
3. Tại sao phản hồi tiêu cực — **chỉ ra lỗi của bài trước**, không đổ lỗi cho commenter
4. Fact-check từng comment: đúng/sai/tranh luận được
5. Đánh giá + đề xuất xử lý (trả lời đính chính / xóa đăng lại / để nguyên) + câu trả lời mẫu nếu chọn trả lời

## 6. Xử lý bài sai: KHÔNG xóa, đính chính bằng reply (user chốt 2026-08-09)

Quyết định của user khi bài đã đăng bị lỗi sự thật (case Techcombank 09-08):
- **KHÔNG xóa bài đã đăng** — user chốt "bài đã viết rồi thì không xóa đi".
- **KHÔNG edit được** — Threads KHÔNG có nút Edit cho post đã đăng quá ~15 phút (verified: mở menu More trên cả desktop và mobile web, menu chỉ có Insights/Save/Pin/Archive/Hide counts/Reply options/Delete/Copy link/Get embed code — không có Edit). Đừng hứa edit bài cũ; báo thẳng user giới hạn này.
- **Cách xử lý đúng**: reply đính chính ngay dưới post, thừa nhận nhanh không chống chế, rồi dừng.

### Reply đính chính (verified 2026-08-09)
```python
# 1. Mở post URL, scroll xuống comments
# 2. Tìm container comment muốn reply (chứa username + đoạn text)
idx = page.evaluate("""() => {
    const cs = document.querySelectorAll('div[data-pressable-container="true"]');
    for (let i = 0; i < cs.length; i++)
        if ((cs[i].innerText||'').includes('<username>')) return i;
    return -1;
}""")
# 3. Click icon Reply trong container đó
containers.nth(idx).locator('svg[aria-label="Reply"]').first.click()
# 4. Gõ vào textbox CUỐI cùng bằng keyboard.type có delay (Lexical editor bỏ qua fill())
tb = page.locator('[contenteditable="true"], [role="textbox"]').last
tb.type(REPLY_TEXT, delay=12)
page.keyboard.press("Control+Enter")
# 5. VERIFY bắt buộc: dump lại containers, reply phải hiện dưới comment với tag "Author"
```
- Reply 1 comment duy nhất (người hỏi lịch sự nhất) — đủ để mọi người thấy đính chính, trả lời từng comment riêng lẻ dễ thành drama.
- Reply editor KHÔNG dùng fill() (Lexical bỏ qua im lặng) — chỉ keyboard.type có delay.

## Pitfalls

- **Đừng chạy script bằng `venv/Scripts/python "C:/full/path.py"` khi lifecycle guard báo "embedded null character in path"** — workaround: `cd` vào thư mục chứa script rồi gọi tên file tương đối:
  `cd /c/Users/NTQUANG_DELL/hermes-temp && /c/Users/NTQUANG_DELL/AppData/Local/hermes/hermes-agent/venv/Scripts/python.exe script.py`
- Viết script mới bằng write_file vào `~/hermes-temp/`, không dùng heredoc (dấu TV bị strip).
- Playwright venv: `~/AppData/Local/hermes/hermes-agent/venv/Scripts/python.exe`.
