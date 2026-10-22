# Verify STALE tự viết lại logic + 3 lỗi assert git (29/09)

Bài học từ standup 29/09: script ad-hoc verify FAIL 2 vòng liên tiếp trong khi `ops_guard.py` thật đã PASS. Toàn bộ lỗi nằm ở script verify, không phải dữ liệu.

## 1. `store/tasks.json` lưu `updated_at` KHÔNG phải ISO-8601

Format thật: `"%Y-%m-%d %H:%M:%S"` — **không có chữ `T`**.

```python
# SAI -> parse fail moi task -> STALE=0 (guard that bao 13)
datetime.strptime(s[:19], "%Y-%m-%dT%H:%M:%S")

# DUNG: copy logic _parse() cua hub/ops_guard.py (thu nhieu format + fallback created_at)
def parse(s):
    for f in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S"):
        try:
            return datetime.strptime(s[:19], f).replace(tzinfo=timezone.utc)
        except ValueError:
            pass
    return None

dt = parse(t.get("updated_at") or t.get("created_at") or "")
if dt is None:
    unparsed.append(t["id"])   # LUON check unparsed rong — im lang bo qua task la FAIL im
```

Assert thêm: `check("moi task parse duoc updated_at", not unparsed)`. Không có assert này thì task parse hỏng biến mất khỏi cả STALE lẫn NO_DC → verify "xanh" trong khi bỏ sót.

**Nguyên tắc:** khi script verify FAIL mà guard thật PASS → **nghi script trước, đừng nghi dữ liệu**. Rẻ hơn nhiều so với sửa `hub/ops_guard.py` oan.

## 2. `git branch -r --contains <hash>` trả TÊN NHÁNH, không phải hash

```
$ git branch -r --contains 48fab1e
  origin/HEAD -> origin/main
  origin/main
```

Check `hash in output.split()` → **FAIL giả** dù commit đã push thật. Cách so đúng:

```python
HEAD = git("rev-parse", "HEAD")
check("HEAD nam tren origin/main", "origin/main" in git("branch", "-r", "--contains", HEAD).split())
check("origin/main tro toi HEAD", git("rev-parse", "origin/main") == HEAD)   # so chuan nhat
```

## 3. `git log --since=<ngay>` lech múi giờ commit (+0700)

Commit lúc 09:06 +0700. `git log --since=2026-09-29` có thể rỗng vì so sánh theo UTC. So bằng text thay vì `--since`:

```python
commits_today = [c for c in git("log", "--format=%h|%ad", "--date=format:%Y-%m-%d", "--all").splitlines()
                 if c.endswith("|2026-09-29")]
check("chi 1 commit hom nay", commits_today == [f"{short}|2026-09-29"])
```

## 4. So khớp chuỗi tiếng Việt có dấu — copy nguyên văn, đừng gõ lại

`check("briefing chua '0 task `mode=agent` active'")` FAIL vì file ghi `"0 task `mode=agent` **đang** active"`. Thiếu 1 từ là FAIL giả.

Cách an toàn: assert ngắn, tránh backtick + dấu tiếng Việt dài.

```python
for s in ["STALE=13", "NO_DC=0", "WAKE=0", "0 task đóng hôm nay"]:
    check(f"briefing chua {s!r}", s in b)
```

Nếu cần khớp dài, **copy paste nguyên văn từ output git**, không gõ tay.

## 5. Verify `Temp/` đã dọn + không rò data

Sau khi xoá script phân tích trong repo, phải assert không còn sót:

```python
check("khong con script rac", (not os.path.isdir(tmp)) or not os.listdir(tmp))
```

Và check `git status --porcelain` chỉ còn file gitignored/derived (tfo_data/, store/*.bak, Temp/) — không có data/token lọt lên tracking.
