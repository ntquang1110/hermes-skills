# Chẩn đoán input token cao (bloat) trong Hermes

Khi user kêu "input token rất cao, request nào cũng 200k": không đoán, chẩn đoán theo thứ tự.

## 1. Nguồn dữ liệu: state.db (bảng session_model_usage)

- **DB ACTIVE:** `C:/Users/NTQUANG_DELL/AppData/Local/hermes/state.db` (1.7GB+).
  ⚠️ Bản `D:/Hermes/hermes-home/state.db` chỉ là bản cũ (junction pha 1, dừng cập nhật từ 10/08/2026) — đọc bản này sẽ ra số liệu thiếu tháng gần.
- `session_model_usage`: `api_call_count`, `input_tokens`, `output_tokens`, `estimated_cost_usd`, `first_seen` (epoch float).
- `sessions`: `message_count`, `tool_call_count`, `api_call_count`, `started_at` (epoch).

### Thống kê request theo tháng
```python
import sqlite3, datetime
conn = sqlite3.connect(r'C:\Users\NTQUANG_DELL\AppData\Local\hermes\state.db')
cur = conn.cursor()
rows = cur.execute('''SELECT first_seen, api_call_count, input_tokens, output_tokens, estimated_cost_usd
FROM session_model_usage WHERE first_seen IS NOT NULL''').fetchall()
from collections import defaultdict
bym = defaultdict(lambda: [0,0,0,0,0.0])
for ts, req, it, ot, cost in rows:
    m = datetime.datetime.fromtimestamp(int(ts)).strftime('%Y-%m')
    d = bym[m]; d[0]+=1; d[1]+=req or 0; d[2]+=it or 0; d[3]+=ot or 0; d[4]+=cost or 0
for m in sorted(bym):
    d = bym[m]
    print(m, 'req=', d[1], 'in=', f'{d[2]:,}', 'out=', f'{d[3]:,}')
```

### Tìm session có input/request cao nhất (200k+)
```python
rows = cur.execute('''SELECT s.started_at, s.title, u.api_call_count, u.input_tokens, u.output_tokens
FROM session_model_usage u LEFT JOIN sessions s ON s.id = u.session_id
WHERE u.api_call_count > 0 AND u.input_tokens IS NOT NULL
ORDER BY u.input_tokens*1.0/NULLIF(u.api_call_count,0) DESC LIMIT 20''').fetchall()
```
Session "1 request = 249k input" kiểu này = context bị phình, không phải nhiệm vụ nặng.

## 2. Root cause #1: compression TẮT (thủ phạm chính)

Check `config.yaml`:
```yaml
compression:
  enabled: false   # ← nếu false: không bao giờ nén history
  threshold: 0.5
  target_ratio: 0.2
```
- `enabled: false` → context không nén, session dài (300–400 messages) mỗi turn gửi **toàn bộ history** → input phình tới 200k+.
- Fix: `hermes config set compression.enabled true`. Cơ chế: context đạt 50% → nén còn 20%, giữ `protect_last_n: 20` tin cuối + `protect_first_n: 3` tin đầu. Giảm input 5–10x cho session dài.

## 3. Root cause #2: session quá dài không reset

- Turn chat thường có `history=290–380` messages trong agent.log → mỗi turn tốn = tổng context cũ.
- Pattern trong log: dòng `agent.turn_context ... history=339` lặp lại với model khác nhau = context đang phình.
- USER đã đề xuất hướng này ("tóm tắt conversation mỗi turn thay vì full history") — câu trả lời đúng là **bật compression + /new khi đổi task + STATE file protocol** (state files chứa kết luận + pointer, đọc lại là hiểu ngay).
- ⚠️ Cấm "tóm tắt chồng tóm tắt" — tóm tắt của tóm tắt mất chi tiết + hallucination. Compression tự động tránh được vì chỉ nén 1 lần + giữ phần gần.

## 4. Ngưỡng tham khảo

- System prompt nền ~12k tokens/request (skills + memory + AGENTS.md) — phần này cố định, không phải bloat.
- Input/request trung bình khoẻ mạnh: 5–16k. Vượt 100k+ với request thường = bloat.
- Tháng research nặng (delegate + tool output dài) → history phình nhanh → ảnh hưởng các turn sau.