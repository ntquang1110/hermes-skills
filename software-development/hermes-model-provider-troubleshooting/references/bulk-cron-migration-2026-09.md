# Bulk Cron Migration khi Provider/Tunnel Chết — 2026-09-09

Case: 12 cron đang chạy (11× unsloth/Ministral qua pharma-llm.thefirstonly.com + 1× deepseek-v4-flash-ga-260731) đồng loạt `last_status: error` vì:
- `pharma-llm.thefirstonly.com` 502 — tunnel `pharma-duc-anh` (32f09491-56b2-...) còn 4 edge connections nhưng origin `localhost:8888` trên máy Đức Anh chết.
- `deepseek-v4-flash-ga-260731` 429 exhausted (500 RPM/1M TPM, burst +3M TPM/3p → RequestBurstTooFast).

Đồng thời `model.default` cũng bị 429, đốt 21M input trong 2 ngày do mỗi retry gửi lại full context (50-150K tokens).

## Fix ưu tiên — đổi MODEL trước, account mới sau (đã verify)

BytePlus limit theo ACCOUNT+MODEL → GA bị 429 không kéo model khác trên cùng key.
- `deepseek-v4-flash-ga-260731`: 500 RPM / 1M TPM
- `deepseek-v4-flash-260425`: **15K RPM / 1.5M TPM** (gấp 30× RPM, +50% TPM)

Đổi default + giảm retry trước khi bắt user tạo account mới:
```bash
hermes config set model.default deepseek-v4-flash-260425
hermes config set agent.api_max_retries 2   # 3→2 cắt ~25% input đốt khi provider chết
```

## Bulk migration 12 job — jobs.json trực tiếp

`cronjob action=update` KHÔNG nhận `model`/`provider` (trả `No updates provided`). Phải sửa `jobs.json` trực tiếp.

```python
import io, json, shutil
p = r"C:\Users\NTQUANG_DELL\AppData\Local\hermes\cron\jobs.json"  # D:/Hermes/hermes-home/cron/jobs.json là junction cùng file
import datetime
shutil.copy2(p, p + ".bak-" + datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
with io.open(p, encoding="utf-8") as f: d = json.load(f)
jobs = d if isinstance(d, list) else d.get("jobs", d)
for j in jobs:
    if j.get("provider") == "unsloth" and j.get("state") == "scheduled":
        j["provider"] = "bytedance"; j["model"] = "deepseek-v4-flash-260425"; j["base_url"] = None
    elif j.get("model") == "deepseek-v4-flash-ga-260731":
        j["model"] = "deepseek-v4-flash-260425"
with io.open(p, "w", encoding="utf-8") as f:
    json.dump(d if not isinstance(d, list) else jobs, f, ensure_ascii=False, separators=(",",":"))
```

Lưu ý: `read_file` tool chèn prefix `N|` làm `json.loads` fail — luôn `io.open` đường dẫn disk trực tiếp.
Verify: `cronjob action=list` → 12 job hiện `bytedance/deepseek-v4-flash-260425` ngay, không cần restart gateway (junction sync).

## Chạy bù sau migration

```bash
cronjob action=run job_id=<id>  # chạy lại từng job fail sáng nay
# Đã verify 09/09: 7 job chạy bù OK (Tâm lý 1/4, 2/4, KFlow Push, Auto Threads, Macro Daily, auto-post, ai-company standup, Auto-push research)
```

Output cron deliver=local → check `~/AppData/Local/hermes/cron/output/<job_id>/<timestamp>.md`, không phải chat.

## Bài học

- Khi primary provider chết, đừng tạo account mới ngay — check model khác trên cùng account có quota riêng không.
- Khi tunnel chết, mọi job trỏ vào tunnel đó phải rời ngay — không chờ origin sửa.
- Bulk edit qua jobs.json nhanh hơn 12 lần `hermes cron edit` (vốn cũng bị chặn cho vài job user-owned).
