# Lark / Feishu Calendar API

Tạo sự kiện lịch trên Lark (Feishu) sử dụng tenant access token.

## Authentication

```python
import requests

APP_ID = '<LARK_APP_ID>'
APP_SECRET = '<LARK_APP_SECRET>'

r = requests.post('https://open.larksuite.com/open-apis/auth/v3/tenant_access_token/internal',
    json={'app_id': APP_ID, 'app_secret': APP_SECRET})
token = r.json().get('tenant_access_token')
```

## Create Calendar Event

```python
headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}

# Tính timestamp (UTC): 2026-07-18 14:00 UTC+7 = 2026-07-18 07:00 UTC
import time, calendar
start_ts = int(time.mktime(time.strptime('2026-07-18 14:00', '%Y-%m-%d %H:%M'))) - 7*3600
end_ts = start_ts + 3600

event = {
    'summary': 'Gặp ông ABC',
    'start_time': {'timestamp': str(start_ts), 'timezone': 'Asia/Ho_Chi_Minh'},
    'end_time': {'timestamp': str(end_ts), 'timezone': 'Asia/Ho_Chi_Minh'}
}

r = requests.post('https://open.larksuite.com/open-apis/calendar/v4/calendars/primary/events',
    headers=headers, json=event)
# Response: 200 + event_id
```

## Add Attendees (Guests)

```python
headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
event_id = '...'  # from create response

payload = {
    'attendees': [{'type': 'user', 'user_id': 'USER_OPEN_ID', 'is_optional': False}],
    'need_notification': True
}
r = requests.post(f'https://open.larksuite.com/open-apis/calendar/v4/calendars/primary/events/{event_id}/attendees',
    headers=headers, json=payload)
```

### Lưu ý về User ID
- `user_id` phải là **Open ID** (dạng `ou_xxx`), **không phải** email hay tên tài khoản
- Cách lấy Open ID của user: user nhắn tin cho bot → kiểm tra log gateway để capture open_id
- Hoặc user copy từ Lark Profile → Copy Member ID
- Nếu không có Open ID: bot tạo event trên calendar của bot, user không thấy được
- User cần là guest (attendee) với Open ID đúng mới thấy event trong calendar của họ

## Notes
- `start_time.timestamp` là Unix timestamp (seconds since epoch) — **cần UTC**, không phải local time
- `timezone` set `Asia/Ho_Chi_Minh` để Lark hiển thị đúng múi giờ
- Endpoint: `POST /open-apis/calendar/v4/calendars/primary/events`
- API version: v4
- Lark domain: `open.larksuite.com` (international), `open.feishu.cn` (China)
