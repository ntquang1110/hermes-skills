# Case study: OmniRoute trả empty response (2026-08-04)

## Bối cảnh

- Hermes gateway chạy Telegram + Feishu. Model default: `auto/best-coding` qua `custom:omniroute` (base_url `http://192.168.1.110:20128/v1`).
- 02:57 test tool-calling với `auto/best-coding` → OK (context nhỏ).
- 03:08–03:10: CẢ 2 session (DM `6277220574` + group `-1004368353156`) cùng báo "Empty response from model — retrying" rồi "No fallback providers configured".

## Log bằng chứng (agent.log)

Session kẹt (`20260804_025555_08e955`), model=auto/best-coding provider=custom:

```
03:08:52 API call #1: in=266776 out=0 total=266776 latency=16.6s
03:08:57 Empty response (no content or reasoning) — retry 1/3
03:09:04 API call #3: in=266826 out=0 latency=6.9s   ← retry 2/3
03:09:09 API call #4: in=266826 out=0 latency=5.0s   ← retry 3/3
03:09:15 Turn ended: reason=empty_response_exhausted tool_turns=293
```

Sau restart gateway (03:15), session vẫn kẹt với cùng context 266K:

```
03:15:49 API call #1: in=266831 out=0 latency=5.2s   ← vẫn rỗng
03:16:31 API call #4: in=174343 out=10 latency=35.0s ← context giảm → trả được 10 tokens
```

→ Ngưỡng lỗi quanh ~200K tokens. Context càng nhỏ, model càng trả lời được.

## Vì sao không phải Hermes

- Session khác (`20260804_031036_1de976`) cùng lúc chạy `deepseek-v4-flash` qua `opencode-go` → OK (latency 5-6s, đầy đủ content). Đường riêng, không qua OmniRoute.
- Test độc lập qua OmniRoute: `auto/best-coding` với text thuần 266K tokens + tool-call pattern → vẫn trả "OK". Nên không phải context size đơn thuần.
- Điểm khác biệt còn lại: session thật gửi kèm system prompt khổng lồ + 100+ tool schemas. Với request cỡ đó, OmniRoute/upstream (claude-opus-4-6-thinking) chết im, trả **HTTP 200 với content rỗng** thay vì 4xx/5xx.

## Lỗi thứ 2: fallback config sai format

Config ban đầu:

```yaml
fallback_providers: '[{"provider": "opencode-go", "model": "deepseek-v4-flash"}]'
```

→ YAML parse ra **string**, code cần **list** → fallback chain rỗng → "No fallback available".

## Fix (python, vì patch tool bị chặn trên config.yaml)

```python
import io
p = r'C:\Users\NTQUANG_DELL\AppData\Local\hermes\config.yaml'
with io.open(p, 'r', encoding='utf-8-sig', newline='') as f:
    content = f.read()
old = "fallback_providers: '[{\"provider\": \"opencode-go\", \"model\": \"deepseek-v4-flash\"}]'"
new = """fallback_providers:
- provider: opencode-go
  model: deepseek-v4-flash"""
content = content.replace(old, new)
with io.open(p, 'w', encoding='utf-8', newline='') as f:
    f.write(content)
```

Verify:

```python
import yaml
cfg = yaml.safe_load(open(r'C:\Users\NTQUANG_DELL\AppData\Local\hermes\config.yaml', encoding='utf-8'))
fb = cfg.get('fallback_providers')
assert isinstance(fb, list) and all(isinstance(x, dict) and x.get('provider') and x.get('model') for x in fb)
```

Lưu ý: `hermes config set fallback_providers '[...]'` lưu dạng string → vẫn sai. Phải sửa file trực tiếp.

## Bài học rút ra

1. Fallback chain mặc định: `opencode-go` / `deepseek-v4-flash` — nên luôn verify là list thật sau mọi thay đổi config.
2. OmniRoute `auto/best-coding` (→ claude-opus-4-6-thinking) yếu với context > ~200K tokens kèm tool schemas lớn. Phòng thủ: fallback chain hoạt động, hoặc ép compression giữ context < 180K (config `model.context_length`).
3. Khi cả 2 session cùng empty trong cùng vài phút → check server/provider trước, đừng đổ lỗi Hermes.
