# Nghiên cứu chủ đề không nằm trong PubMed (lịch sử, văn hóa, tín ngưỡng, nhân vật, sự kiện) qua Wikipedia MediaWiki API

Dùng khi đề tài research thuộc lĩnh vực nhân văn/xã hội/lịch sử tôn giáo/tiểu sử mà PubMed không index. Vẫn phải publish kết quả lên preview.thefirstonly.com theo `## Publish rule` của skill này — rule đó áp dụng cho MỌI deliverable nghiên cứu, không chỉ khoa học.

## Vì sao dùng Wikipedia API thay vì fetch trang HTML
- Trang HTML nặng (thẻ, script, nội dung quanh co) — API `prop=extracts&explaintext=1` trả **plain text sạch** theo section, tiết kiệm token và không bị nhiễu.
- API cho snippet tìm kiếm để triage nhanh như `esearch`/`esummary` của PubMed.

## Cách gọi (curl/python urllib, luôn kèm User-Agent)
```python
import urllib.request, urllib.parse, json
def get(url):
    req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read().decode("utf-8","ignore")
```

### 1. Tìm kiếm + lấy pageid (triage — tương đương esearch)
```
action=query&list=search&srsearch=<urlencode>&format=json&srlimit=N&srnamespace=0
```
Response: `query.search[]` với `title`, `pageid`, `snippet` (snippet có thẻ `<span>` — strip tags nếu cần). Dùng snippet để loại hit nhiễu (từ khóa trùng tên người/tên địa danh khác).

### 2. Lấy nội dung (tương đương efetch) — DÙNG pageid, KHÔNG dùng title
```
action=query&pageids=<pageid>&prop=extracts&explaintext=1&format=json&redirects=1&exsectionformat=plain
```
**Trap quan trọng:** nếu nhét title trực tiếp vào URL path với ký tự có dấu (Đền Bảo Hà, Ông Hoàng Bảy…), curl có thể ghi file 0 byte / server không match đúng do Unicode bị nhà mạng/trình bao gồm làm hỏng. **Luôn resolve pageid từ bước search trước, rồi query bằng `pageids=` — tránh hẳn encoded title trong URL.** Nếu title ASCII thuần không dấu vẫn OK, nhưng chuẩn là qua pageid.

Plain text trả về kèm marker `== Section ==` → regex/giữ nguyên để chia section khi đọc.

### 3. Mẹo đọc nhanh
- `redirects=1` để tự nối trang đổi hướng.
- Khi chỉ cần một đoạn (vd từ khóa xuất hiện ở đâu), `.find("từ khóa")` trên extract rồi in quanh vị trí đó thay vì đổ cả bài.
- Hàng loạt từ khóa → vòng lặp các `list=search`, `time.sleep(0.7)` giữa mỗi gọi như PubMed.

## Ví dụ đã chạy tốt (03/09/2026 — Ông Hoàng Bảy / Đền Bảo Hà, Lào Cai)
- Search "Hoàng Bảy Bảo Hà Lào Cai" → hit "Đền Bảo Hà" (pageid 19778483) + "Bảo Hà" (1242465).
- `pageids=19778483&prop=extracts&explaintext=1` → full lịch sử đền (di tích quốc gia 1997, thờ Thần vệ quốc Nguyễn Hoàng Bảy, gốc tướng nhà Lê Cảnh Hưng, sắc phong "Trấn an hiển liệt"/"Thần Vệ quốc", hiện tượng "đền số má" + cúng thuốc phiện).
- Đó là toàn bộ chất liệu factual cho deliverable; phần phân tích hai lăng kính (tâm linh vs logic) là reasoning của agent, không cần nguồn.