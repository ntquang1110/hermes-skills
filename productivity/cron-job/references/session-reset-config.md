# session_reset Config — Session Lifecycle

Kiểm soát khi nào Hermes tự động reset session chat (Telegram, Discord, CLI...).

## Config

```yaml
session_reset:
  at_hour: 4          # Giờ reset hàng ngày (0-23). 4 = 4h sáng
  idle_minutes: 1440  # Idle timeout (phút). 1440 = 24h
  mode: both          # both | at_hour_only | idle_only | off
```

## Các mode

| mode | Hành vi |
|------|---------|
| `both` | Reset lúc `at_hour` HOẶC sau `idle_minutes` không tương tác |
| `at_hour_only` | Chỉ reset lúc `at_hour`, không reset vì idle |
| `idle_only` | Chỉ reset sau idle timeout, không reset theo giờ |
| `off` | Không bao giờ tự động reset session |

## Thay đổi

```bash
# Tắt hẳn auto-reset
hermes config set session_reset.mode off

# Bỏ daily reset, chỉ reset nếu idle 7 ngày
hermes config set session_reset.at_hour ""
hermes config set session_reset.idle_minutes 10080

# Reset sau 12h idle
hermes config set session_reset.idle_minutes 720
```

## Tác động

- `at_hour: 4` = mỗi sáng 4h, mọi session chat bị reset → context mới, không nhớ gì từ hôm trước
- `idle_minutes: 1440` = nếu không chat 24h, session tự reset
- Cron job sessions (ephemeral) không bị ảnh hưởng — chúng sống trong tick rồi chết
- Dấu hiệu nhận biết session vừa bị reset: system note *"The user's session was automatically reset by the daily schedule"*

## Use case

- Quang muốn giữ session không bị reset → set `mode: off` hoặc kéo dài `idle_minutes`
- Muốn reset mỗi sáng để context gọn → giữ default
- Muốn reset chỉ khi không dùng lâu → `at_hour_only` với idle cao
