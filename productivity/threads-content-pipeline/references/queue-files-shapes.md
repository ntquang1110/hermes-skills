# Queue files — shape thật + recipe thêm bài (đã verify 2026-10-18)

Hai file ở `~/AppData/Local/hermes/cache/`:

## 1. `youtube-schedule.json`

```json
{
  "last_posted_date": "2026-10-21",
  "queue": [
    {
      "id": "63FPhjGWjvk-20270131",
      "video_id": "63FPhjGWjvk",
      "scheduled_date": "2027-01-31",
      "scheduled_time": "20:00",
      "status": "pending",
      "title": "Beyond Limits - Dương Quý Chi: Nghiện học bằng ba cỗ máy của mạng xã hội",
      "channel": "Beyond Limits",
      "chars": 5820,
      "draft_path": "C:\\Users\\NTQUANG_DELL\\hermes-temp\\draft_xxx.txt",
      "added_at": "2026-10-18T22:41:02",
      "content": "<toàn bộ bài đăng>"
    }
  ]
}
```

- `id` = `f"{video_id}-{YYYYMMDD}"` (ngày đăng, không có gạch).
- `queue` là LIST, sắp theo `(scheduled_date, id)` sau mỗi lần thêm.
- `status`: `pending` | `posted`.

## 2. `youtube-processed.json`

```json
{
  "video_ids": ["...", "63FPhjGWjvk"],
  "urls": ["https://www.youtube.com/watch?v=63FPhjGWjvk"],
  "items": [
    {"id": "63FPhjGWjvk-20270131", "video_id": "63FPhjGWjvk",
     "title": "...", "url": "https://www.youtube.com/watch?v=63FPhjGWjvk",
     "date": "2027-01-31"}
  ],
  "last_updated": "2026-10-18",
  "tiktok_urls": [],
  "notes": [],
  "by_source": {},
  "topics_posted": []
}
```

## 🔴 Pitfall đã sập thật: `items` là LIST, không phải dict

```python
p["items"][VID] = {...}          # TypeError: list indices must be integers or slices, not str
p["items"].append({...})         # ĐÚNG
```

`video_ids` là list riêng để check duplicate nhanh; `items` là list bản ghi đầy đủ. Hai chỗ phải cập nhật cùng lúc.

🔴 **Lỗi này đã SẬP LẦN 2 (2026-10-19)** — không phải vì không có tài liệu, mà vì agent tự viết script add-queue mới thay vì dùng cái có sẵn. Quy tắc: **KHÔNG viết lại script add-queue**, chạy template:

```bash
python "C:/Users/NTQUANG_DELL/AppData/Local/hermes/skills/productivity/threads-content-pipeline/templates/add_queue_item.py" \
  --video-id <ID> --draft "C:/Users/NTQUANG_DELL/hermes-temp/draft_x.txt" \
  --title "<tiêu đề>" --channel "<kênh>"
```

Template làm sẵn mọi thứ dưới đây (ngày kế tiếp, guard id/ngày trùng, nhúng `content`, append vào `items`, tự audit). Chỉ tự viết script khi bài toán khác hẳn (vd sửa hàng loạt item cũ), và khi đó chép logic từ template.

Nếu đã lỡ viết tay và sập giữa chừng: phần schedule thường ĐÃ ghi xong trước khi lỗi xảy ra — đừng xoá item khỏi queue, chỉ vá `youtube-processed.json` (`video_ids.append`, `items.append`) rồi chạy lại audit.

## Pitfall: ghi schedule trước rồi mới ghi processed → nửa đường sập là lệch trạng thái

Script kiểu này từng ném lỗi SAU khi queue đã ghi xong. Hệ quả: item có trong queue nhưng chưa có trong processed, và lần chạy lại chết ở guard "ALREADY EXISTS" rồi bỏ luôn phần processed.

Recipe chống: ghi schedule → ghi processed trong `try`, và **luôn để bước processed chạy lại được** (check `if VID not in p["video_ids"]` rồi append). Nếu đã lỡ lệch, chạy một đoạn chỉ vá processed, đừng xoá item khỏi queue.

## Pitfall: thiếu `content` = poster im lặng không đăng

`youtube-scheduler.py` đọc `next_item.get("content", "")` rồi `if not content: return`. Không log, không báo. Mọi item `pending` phải có `content` (nhúng nguyên văn từ file draft, không chỉ để `draft_path`).

## Verify sau khi thêm (bắt buộc)

```python
q = json.load(open(SCHED, encoding="utf-8"))["queue"]
assert len({i["id"] for i in q}) == len(q)                       # 0 id trùng
assert len({i["scheduled_date"] for i in q}) == len(q)           # 0 ngày trùng
empty = [i["id"] for i in q if i.get("status") == "pending" and not (i.get("content") or "").strip()]
print("pending thiếu content:", len(empty))                      # phải = 0
```

## Snippet thêm bài

```python
DRAFT = r"C:\Users\NTQUANG_DELL\hermes-temp\draft_xxx.txt"
VID, DATE = "63FPhjGWjvk", "2027-01-31"
ITEM_ID = f"{VID}-{DATE.replace('-', '')}"
content = open(DRAFT, encoding="utf-8").read().strip()

d = json.load(open(SCHED, encoding="utf-8")); q = d["queue"]
assert not any(i.get("id") == ITEM_ID for i in q), "đã có"
assert not any(i.get("scheduled_date") == DATE for i in q), "ngày đã bị chiếm"
q.append({..., "status": "pending", "chars": len(content), "content": content})
q.sort(key=lambda i: (i.get("scheduled_date") or "", i.get("id") or ""))
json.dump(d, open(SCHED, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
```

Ngày đăng luôn là **ngày kế tiếp sau item cuối trong queue**, không phải ngày hiện tại.
