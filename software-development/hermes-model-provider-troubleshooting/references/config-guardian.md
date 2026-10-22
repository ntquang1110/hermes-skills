# Config guardian — lịch sử & pitfall

> Tách từ `SKILL.md` ngày 19/10/2026. Nội dung giữ nguyên văn.


---

## CONFIG GUARDIAN — "ép cứng" config khỏi reset, không cần canh tay (2026-09-13)

Khi user yêu cầu **"ép cứng để không bị reset nữa"** (không muốn mỗi lần desktop
mở lại là phải set lại config), đừng chỉ kill desktop 1 lần — dựng watchdog tự
sửa. Pattern đã triển khai + test thật:

**Cron no_agent + script kiểm tra/re-apply:**
1. Script `config_guard.py` (đã deploy tại `~/AppData/Local/hermes/scripts/config_guard.py`,
   bản template trong skill: `scripts/config_guard.py`):
   - Đọc config.yaml bằng `yaml.safe_load`, so 5 key quan trọng:
     `model.default` (deepseek-v4-flash-ga-260731), `model.provider` (bytedance),
     `agent.api_max_retries` (0), `moa.enabled` (False),
     `moa.aggregator.provider`/`.model` (bytedance/deepseek-v4-flash-ga-260731).
   - Key lệch → **re-apply bằng `hermes config set` qua subprocess** (đúng luồng,
     không sửa tay file), kill Hermes.exe desktop (nguồn reset) nếu đang chạy, in
     báo cáo → cron deliver cảnh báo vào chat.
   - Desktop chạy nhưng config OK → in cảnh báo rủi ro.
   - Mọi thứ OK → stdout RỖNG = im lặng (watchdog pattern chuẩn).
2. Tạo cron: `cronjob(action=create, no_agent=true, script="config_guard.py",
   schedule="every 15m", deliver="origin")`.
3. **Test thật trước khi bàn giao:** `hermes config set moa.enabled true` (bẻ
   config) → chạy `python config_guard.py` → phải thấy "CONFIG BỊ RESET — guardian
   tự sửa" + giá trị về đúng. Rồi `cronjob(action=run)` chạy 1 tick xác nhận OK.
   Nếu cron chạy xong không deliver gì = đúng (im lặng khi OK).

**Lưu ý:** `moa.*` là custom key → `hermes config set` báo "not a recognized
config key — saved anyway" (warning vô hại, vẫn lưu). Guardian chỉ re-apply khi
LỆCH — nếu user chủ động đổi model có chủ đích, guard sẽ revert + báo (đúng ý
"ép cứng", user biết qua cảnh báo).
