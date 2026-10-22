# Triệu chứng "provider/model tự reset về X" — check config_guard GOLDEN + cron DB

Case gốc: user hỏi *"tại sao lại reset về openrouter?"* (2026-10-07). Config hiện tại ĐÚNG (không có openrouter),
nhưng vài ngày trước nó từng quay về openrouter. Đây là 2 nguyên nhân thật đã xác minh, KHÔNG phải "config tự reset".

## 1. `config_guard.py` — GOLDEN literal bị cũ (nguyên nhân chính)

`~/AppData/Local/hermes/scripts/config_guard.py` (guard chạy qua cron `no_agent` mỗi 15 phút) giữ một dict `GOLDEN`
**hard-code cứng** gồm cả `model.default`, `model.provider`, `model.base_url` và **toàn bộ `fallback_providers`**.
`fix_config()` GHI ĐÈ nguyên khối các field đó bằng GOLDEN mỗi khi phát hiện config "lệch".

⇒ Đổi model chính mà **không sửa GOLDEN** thì guard sẽ kéo config về model cũ ở lần chạy kế tiếp.
Đây chính là cảm giác "provider tự reset". Trong case này GOLDEN vẫn còn entry
`{"provider": "openrouter", "model": "deepseek/deepseek-chat"}` ở cuối fallback chain + primary vẫn là
`bytedance / deepseek-v4-flash` dù thực tế đã đổi sang `command-code / xiaomi/mimo-v2.5`.

### Cách chẩn đoán

```bash
grep -n "openrouter" ~/AppData/Local/hermes/scripts/config_guard.py     # tìm literal trong GOLDEN
sed -n '12,45p' ~/AppData/Local/hermes/scripts/config_guard.py          # xem cả dict GOLDEN
```

So `GOLDEN["model"]` + `GOLDEN["fallback_providers"]` với config.yaml thật. Lệch = đây là thủ phạm.

Đối chiếu chéo bằng backup `.guard-<ts>.bak` do chính guard tạo trước mỗi lần sửa — file backup có
fallback chain cũ (5 entries, có openrouter) là bằng chứng guard đã ghi đè.

### Cách sửa

Sửa `GOLDEN` trong `config_guard.py` cho khớp config mong muốn, rồi chạy guard 1 lần để xác nhận nó IM LẶNG
(không in dòng "CONFIG BỊ THAY ĐỔI / guardian tự phục hồi"):

```bash
python "C:/Users/NTQUANG_DELL/AppData/Local/hermes/scripts/config_guard.py"
```

Chạy đúng được thì output chỉ còn cảnh báo (nếu có) `config chuẩn nhưng desktop Hermes.exe ĐANG CHẠY — nên đóng để tránh ghi đè.`
Exit 0 + không có dòng phục hồi = GOLDEN khớp.

**Quy tắc durable:** mỗi lần đổi model/provider/fallback chính trên máy này, phải sửa GOLDEN của guard
TRONG CÙNG lượt. Nếu không, guard 15 phút sau sẽ revert.

## 2. `cron/jobs.json` hỏng → chết TOÀN BỘ cron (kể cả guard)

Gặp cùng lượt: `~/AppData/Local/hermes/cron/jobs.json` chỉ còn **1 byte** (nội dung `x`). Log lặp:

```
RuntimeError: Cron database corrupted and unrepairable: Expecting value: line 1 column 1 (char 0)
ERROR cron.jobs: Failed to auto-repair jobs.json: Expecting value: line 1 column 1 (char 0)
```

Hệ quả kép: (a) guard không chạy nữa nên không ai revert config — vô tình "che" lỗi GOLDEN;
(b) mọi job khác im lặng không chạy. `hermes cron list` không in gì.

### Chẩn đoán

```bash
ls -la ~/AppData/Local/hermes/cron/jobs.json          # size 1 byte = hỏng
head -c 200 ~/AppData/Local/hermes/cron/jobs.json | xxd | head -5
ls -lt ~/AppData/Local/hermes/cron/jobs.json.bak*     # tìm bản backup
```

### Cách sửa

1. Sao lưu file hỏng trước: `cp jobs.json jobs.json.corrupt-$(date +%Y%m%d-%H%M%S)`
2. Restore từ backup mới nhất: `cp jobs.json.bak-<ts> jobs.json`
3. Verify parse: `python -c "import json;d=json.load(open(r'C:\\Users\\NTQUANG_DELL\\AppData\\Local\\hermes\\cron\\jobs.json',encoding='utf-8'));jobs=d if isinstance(d,list) else d.get('jobs',[]);print(len(jobs),'jobs')"`
4. **Tạo lại bằng tool những job không có trong backup** — backup cũ thiếu job tạo sau đó. Dùng
   `cronjob(action='create', ...)` chứ KHÔNG sửa jobs.json bằng tay (scheduler ghi đè, xem pitfall
   "sửa prompt cron bằng TOOL" trong skill `threads-content-pipeline`).

## 3. Nguồn reset khác cần loại trừ

- **Credential pool đánh dấu provider `exhausted`** (vd bytedance 429, openrouter 402) → engine né primary và
  nhảy fallback ⇒ user tưởng "provider bị đổi". Kiểm tra `auth.json` → `credential_pool.<provider>.last_status`.
- **Desktop app `Hermes.exe` đang chạy** ghi đè config.yaml. Đếm process: `ps -W | grep -i "Hermes.exe"`.
  Guard có `kill_desktop()` cho việc này.

## Thứ tự kiểm tra khi user báo "provider tự reset"

1. Config.yaml thật đang là gì? (`model.default/provider/base_url` + `fallback_providers`)
2. `cron/jobs.json` có parse được không? (nếu hỏng, guard chưa chạy → fix cron trước)
3. `config_guard.py` GOLDEN có khớp config thật không? (nghi phạm số 1)
4. Backup `.guard-*.bak` để xem guard đã ghi đè gì
5. `auth.json` credential_pool có entry nào `exhausted`?
6. `Hermes.exe` có đang chạy không?
7. Log `logs/gateway.log` grep `No model configured — defaulting to` (dấu hiệu model trống → engine tự chọn default)
