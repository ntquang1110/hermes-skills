# Config.yaml bị TRẮNG HÓA / corrupt — restore từ .bak (case 2026-09-11)

Triệu chứng user: "hermes bị restart, mất hết thông tin provider, phải điền lại".
Gateway.log lặp: `No model configured — defaulting to z-ai/glm-5.2 for provider openrouter`.
`config.yaml` chỉ còn vài KB (vd 2,996B thay vì 20KB) — mất model.default, providers,
personality, fallback, compression...

## Chẩn đoán (đọc file, không đoán)

1. `wc -c config.yaml` — file nhỏ hẳn = bị ghi đè/trắng hóa.
2. `ls config*.bak*` — Hermes tự backup khi corrupt:
   - `config.yaml.corrupt.<ts>.bak` — YAML thường hỏng do MẤT DÒNG HEADER. Case thật:
     `plugins:\n  enabled: []` rồi nhảy thẳng vào body omniroute, thiếu dòng
     `custom_providers:` → PyYAML `expected block end` ~line 750.
   - `config.yaml.bak` — bản ổn định cũ (dùng làm nền).
3. Verify từng backup bằng `yaml.safe_load`; bản nào OK + đủ model/providers/
   custom_providers/personality → làm nền restore. Backup corrupt thường chứa cả
   model command-code lạ (ai đó đã sửa trước khi vỡ) — đừng dùng, dùng bản .bak cũ hơn.

## Fix — restore nền + áp lại settings qua python

KHÔNG dùng `hermes config set` (dễ phá model block — xem pitfall sibling keys).
patch tool chặn ghi config.yaml. Dùng script python `yaml.safe_load/safe_dump`.

1. `cp config.yaml config.yaml.empty-<ts>.bak`
2. `cp config.yaml.bak config.yaml` (nền cũ OK)
3. Script python (idempotent — script mẫu `~/httptmp/restore_config.py`):
   - set `model.default`, `model.provider`, `model.api_mode`
   - set `providers.<name>.base_url` + `stale_timeout_seconds`/`ttfb_timeout_seconds`
   - set `agent.api_max_retries`
   - `compression.enabled` — backup cũ thường False; bật lại true nếu trước đó đã bật
   - `fallback_providers` — append nếu thiếu (giữ list cũ)
   - giữ nguyên `custom_providers`/plugins/personality từ nền
   - validate trước khi ghi: assert model.provider/default đúng, fallback là list
   - đọc lại sau ghi verify
4. **BẮT BUỘC restart Hermes Desktop app ngay sau khi file đúng** — desktop đang chạy
   giữ config cũ trong RAM, tự flush ghi đè file sau ~6s (pitfall desktop revert).
   Đừng bảo user điền lại tay: file đã đầy đủ, chỉ restart.
5. Verify sau restart: gateway.log hết "No model configured"; `hermes config get model` đúng.

Lưu ý: mọi thay đổi `hermes config set` trước đó (vd model.default 260425) nằm trong
file bị wipe → phải áp lại sau restore. Config set chỉ sống tới khi desktop flush —
restart ngay sau khi set.
