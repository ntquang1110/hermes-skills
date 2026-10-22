# Cron CONFIG GUARD giết Hermes desktop + ép config về model cũ (10/2026)

Case thật: Windows host `NTQUANG_DELL`, profile `default`, hermes-home = `C:\Users\NTQUANG_DELL\AppData\Local\hermes`.

## Triệu chứng user báo

- Hermes desktop tự tắt liên tục giữa phiên; các turn tool-use bị báo "interrupted".
- `config.yaml` tự quay về model cũ, không ai gõ lệnh nào.
- Session Telegram chạy model khác hẳn desktop (Telegram: `xiaomi/mimo-v2.5`, desktop: `deepseek/deepseek-v4-flash`).

## Nguyên nhân gốc

Cron job `config-guard-hermes` (id `7ce36552836e`, `*/15 * * * *`, mode **no_agent**, script `scripts/config_guard.py`, `deliver: local`, tạo 2026-10-07, đã chạy ~475 lần).

Script giữ dict `GOLDEN` hardcode (model.default = `xiaomi/mimo-v2.5`, provider `command-code`, fallback = 1 entry bytedance, `moa.enabled=false`, `agent.api_max_retries=0`). Mỗi lần chạy:

1. So config.yaml với GOLDEN. Lệch 1 check bất kỳ (`model.default`, `model.provider`, `model.base_url`, `providers.*.base_url`, `fallback_providers`, `moa.enabled`, `agent.api_max_retries`).
2. → copy `config.yaml.guard-<ts>.bak`, ghi lại config theo GOLDEN (xoá luôn mọi thay đổi của user).
3. → gọi `kill_desktop()`: `Get-Process Hermes | Stop-Process -Force` — giết TOÀN BỘ `Hermes.exe` nếu app đang mở.

Guard pin `xiaomi/mimo-v2.5`; user đổi model trong desktop sang `deepseek/deepseek-v4-flash` (desktop ghi lại `model.default` trong config). Tối đa 15 phút sau guard thấy lệch → revert config về mimo + kill desktop. Desktop auto-restart, user thấy đúng model cũ, lại đổi lại... Vòng lặp tự củng cố.

`deliver: local` nên report của guard không đi tới đâu → user chỉ thấy triệu chứng, không thấy nguyên nhân.

## Bằng chứng (đã dùng thật, đừng đoán)

```bash
# 1. Mỗi lần guard ghi config đều để lại backup, giờ trùng tick :00/:15/:30/:45
ls -lat ~/AppData/Local/hermes/config.yaml.guard-*.bak | head
#   → config.yaml.guard-20261012-223040.bak, -213047.bak  (2 lần kill trong ~1h)

# 2. Diff lấy lại setup "trước khi bị guard phá"
diff <(python -c "import yaml;d=yaml.safe_load(open('config.yaml.guard-20261012-223040.bak'));print(yaml.dump(d['model']))") ...

# 3. Desktop bị GIẾT chứ không crash
tail -5 ~/AppData/Local/hermes/logs/gui.log
#   → "auto-continue scheduled for session 20261012_212725_95d987 (attempt 2, interrupted 355s ago)"

# 4. Đọc job (jobs.json KHÔNG dùng read_file rồi json.loads, lấy raw)
python -c "import json;d=json.load(open('cron/jobs.json',encoding='utf-8'));[print(j['name'],j['id'],j['enabled'],j['last_run_at'],j['deliver']) for j in d['jobs'] if 'guard' in j['name'].lower()]"
```

## Fix đúng thứ tự (đã verify)

1. **`hermes cron pause <job_id>` TRƯỚC khi sửa.** Không pause thì guard kill desktop ngay giữa lúc đang sửa (turn chết giữa đường, rất dễ chẩn đoán sai thành lỗi mạng/agent). Case này turn bị interrupt 3 lần trước khi phát hiện.
2. Sửa `GOLDEN` trong `scripts/config_guard.py` cho khớp setup hiện tại, **và bỏ `kill_desktop()`** (thay bằng 1 dòng ghi chú trong report). Guard chỉ nên ghi config + log, không được giết app user đang dùng. Cũng bỏ branch else in cảnh báo mỗi 15 phút khi desktop đang mở (spam nếu đổi `deliver`).
3. Set config bằng CLI, không sửa tay: `hermes config set model.default <model>`; `hermes config set fallback_providers '<json array>'`. Sau đó `yaml.safe_load` verify: `type(fallback_providers).__name__ == 'list'` (CLI nhận JSON nhưng phải kiểm).
4. Chạy tay `python scripts/config_guard.py` → phải **im lặng, exit 0** = config khớp GOLDEN mới. Nếu nó in ra dòng "CONFIG BỊ THAY ĐỔI" thì GOLDEN sai chỗ nào đó.
5. `hermes cron resume <job_id>`, chờ tick kế tiếp rồi verify 3 thứ: `last_status=ok`, config không bị ghi lại, `@(Get-Process Hermes).Count` vẫn > 0.
6. `hermes fallback list` để xác nhận chain mà gateway thật sự đọc (chỉ top-level `fallback_providers`, xem `fallback-chain-hygiene-2026-10.md`).

## Model của session (Telegram/desktop) quyết ở đâu — đọc code, không đoán

- Model mỗi lượt = `config.yaml` đọc **live**. `sessions.model` chỉ là bản ghi sau lượt (`gateway/run.py: _sync_session_model_from_agent()`), và `model_config.gateway_runtime` chỉ ghi lại provider/base_url/api_mode/`fallback_active` của lượt vừa xong — **không được đọc lại để pin**.
- Ngoại lệ duy nhất: lệnh `/model` trong gateway → `SessionStore.set_model_override()` → lưu `entry_json.model_override` trong `gateway_routing` (state.db) + mirror `sessions.json`. Kiểm tra: `select session_key, entry_json from gateway_routing` rồi lọc key `model_override` (case này: 0 row).
- Vì vậy "chuyển session về model X" = (a) sửa `config.yaml` là đủ cho runtime, (b) UPDATE metadata `sessions.model / billing_provider / billing_base_url / model_config` để list + insights khỏi nói dối. **Đừng** sửa `session_model_usage` — đó là sổ lịch sử/billing thật.
- Đổi `platform_toolsets`/`model` trong desktop chỉ áp cho session MỚI; session Telegram đang mở ăn theo config live ở lượt kế tiếp.

## Chống lặp lại

- Guard no_agent mà `deliver: local` = hộp đen. Muốn giữ guard thì để nó canh provider/credential, đừng canh `model.default` — nếu không, mọi lần user đổi model trong desktop đều thành "config bị reset".
- Khi viết watchdog tự sửa config: cấm `Stop-Process` app của user. Muốn chống ghi đè thì log + báo, hoặc chỉ vá đúng key mình sở hữu.
