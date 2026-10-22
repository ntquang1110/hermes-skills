# Cron job chết `HTTP 401: Model is not supported` vì pin provider/model lỗi thời

Case đo thật 2026-08-24: job `knowledge-researcher-4h-rotation` (id `d43697af1322`).

## Triệu chứng

- Telegram nhận tin: `⚠️ Cron '...' failed: provider authentication error`.
- `cronjob action=list` cho job đó: `last_status: "error"`, `model: "deepseek-v4-pro"`, `provider: "opencode-zen"`.
- Cron output cuối file (mục `## Error`):
  ```
  RuntimeError: HTTP 401: Model  is not supported
  ```

## Nguyên nhân

Job tạo 13/07 pin `provider: opencode-zen` + `model: deepseek-v4-pro`. Giữa chừng provider
bị rename/repin model. Config hiện tại (`~/AppData/Local/hermes/config.yaml`):
```yaml
fallback_providers:
  - provider: opencode-zen
    model: deepseek-v4-flash-free
  - provider: opencode-zen
    model: nemotron-3-ultra-free
  - provider: opencode-go
    model: deepseek-v4-flash
  - provider: opencode-go
    model: deepseek-v4-pro   # ← deepseek-v4-pro thuộc opencode-go, KHÔNG phải zen
```
Gọi `opencode-zen` + `deepseek-v4-pro` → provider không serve model đó → 401
"Model is not supported". Không phải key hết hạn.

## Chẩn đoán

1. `cronjob action=list` → đọc model + provider của job lỗi.
2. `grep -nE "opencode|zen|deepseek" config.yaml` → lập bảng (provider → model) tồn tại.
3. Model của job không nằm trong list model provider đó serve = kết luận.

## Fix — sửa `jobs.json` trực tiếp

Tool `cronjob` KHÔNG expose model/provider params → `cronjob(action=update, model=..., provider=...)`
trả `{"error": "No updates provided."}`. Phải sửa file.

Path (Hermes data đã junction sang D): `D:/Hermes/hermes-home/cron/jobs.json`.

```python
import json, io
path = r"D:\Hermes\hermes-home\cron\jobs.json"
with io.open(path, encoding="utf-8") as f:
    raw = f.read()
d = json.loads(raw)                      # d là list (hoặc dict có khóa 'jobs')
jobs = d if isinstance(d, list) else d.get("jobs", d)
t = [j for j in jobs if j.get("id") == "d43697af1322"][0]
t["provider"] = "opencode-go"            # đổi sang provider chứa model hiện tại
t["base_url"] = None
out = json.dumps(d, ensure_ascii=False, separators=(",", ":"))
with io.open(path, "w", encoding="utf-8", newline="\n") as f:
    f.write(out)
```

Lưu ý bắt buộc:
- **Đọc/ghi bằng `io.open` đường dẫn disk trực tiếp, KHÔNG qua `read_file` tool.** read_file
  thêm prefix line-number + re-escape `\uXXXX` → `json.dumps`/`json.loads` fail với
  `JSONDecodeError: Invalid \uXXXX escape`. Đọc thẳng từ disk tránh được.
- Ghi với `ensure_ascii=False` để giữ dấu tiếng Việt trong prompt job.

## Verify

- `cronjob action=list` → job giờ `provider: "opencode-go"`, `model: "deepseek-v4-pro"`.
- `last_status` vẫn `"error"` là của lần chạy cũ → không phải lỗi. Lần chạy kế tới mới tính.

## Quy tắc phòng

- Khi tạo cron gắn model: xác minh cặp (provider, model) khớp config hiện tại NGAY lúc tạo.
- Sau bất kỳ lần provider bị rename/repin model: rà lại các job cron pin cặp cũ bằng
  `cronjob action=list` đối chiếu với config.yaml.