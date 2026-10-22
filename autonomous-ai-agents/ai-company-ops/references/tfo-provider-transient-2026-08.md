# TFO Task Chat "provider transient" — root cause & fix (2026-08-07)

## Triệu chứng

Task chat trong TFO web (port 8100) trả về:
```
⚠️ Lỗi: agent không trả về kết quả (provider transient). Thử lại sau.
```

## Root cause — KHÔNG phải provider

`AgentWorker._process` (`app/agent_exec.py`) gọi `_call_agent` → `hub/store.py call_deepseek`.
Khi `call_deepseek` trả `None`, worker ghi message lỗi trên.

`call_deepseek` trả `None` khi:
1. `os.environ.get("OPENCODE_GO_API_KEY")` rỗng → log `[WARN] OpenCode API key not set — can't call <agent>`
2. Endpoint trả HTTP != 200
3. Endpoint trả 200 nhưng content rỗng sau 3 retry → log `[WARN] OpenCode empty response`

**Case 1 (2026-08-07): thiếu key.** `app/main.py load_keys()` chỉ đọc `GROQ_API_KEY` từ
`~/AppData/Local/hermes/.env`. Dòng:

```python
os.environ.setdefault("OPENCODE_GO_API_KEY", os.environ.get("OPENCODE_GO_API_KEY", ""))
```

là NO-OP: nếu env chưa có key thì set rỗng, KHÔNG đọc từ `.env`. Key thật nằm ở
`~/.bashrc` (chỉ áp dụng trong bash session) và `~/AppData/Local/hermes/.env`
(không được đọc). Server start bằng python trực tiếp (không qua bash) → process
không có key → mọi task chat fail với "provider transient".

## Case 2 (cùng ngày, sau khi fix key): flash trả rỗng hàng loạt với context dài

Sau khi load được key, task chat VẪN fail vì `deepseek-v4-flash` qua OpenCode
endpoint trả 200 + content rỗng **~80%** (đo 5 lần context 6k chars: flash 1/5 ok,
`deepseek-v4-pro` 5/5 ok). Context task chat luôn dài (task + project + history +
content) → flash fail đều.

**Đo benchmark trước khi chọn model/endpoint (kỹ thuật dùng được lại):**
```python
# Với context dài 6k chars, chạy 5 lần mỗi model, đếm số lần trả content != ""
# Kết quả thực tế: flash 1/5, pro 5/5 → chọn pro làm fallback.
```

**Fix trong `call_deepseek` (hub/store.py):** retry cùng model 3 lần → vẫn rỗng
thì fallback model khác (pro trước, vì ổn định hơn với input dài), mỗi model 2 lần:
```python
fallback_models = ["deepseek-v4-pro", "deepseek-v4-flash"]  # bỏ model đang gọi
fb_payload = dict(payload); fb_payload["model"] = fb
# gọi lại OPENCODE_URL, lấy content, nếu có content thì break
```

## Chẩn đoán nhanh

```bash
# Phân biệt thiếu key vs trả rỗng:
grep -E "OpenCode API key not set|OpenCode empty response" store/activity.json | tail -10
# "key not set" → thiếu key (fix loader + restart)
# "empty response" → key có nhưng retry hết vẫn rỗng (fallback model, không phải config)
```

## Fix tóm tắt

1. `load_keys()` trong `app/main.py` đọc thêm `OPENCODE_GO_API_KEY` từ `.env`
   (giống GROQ_API_KEY).
2. `call_deepseek` trong `hub/store.py` thêm fallback flash → pro khi content rỗng.
3. Restart server 8100 bằng `scripts/tfo_launch.py` (xem SKILL.md — uvicorn trực
   tiếp bị lifecycle guard chặn).
4. Verify bằng gọi task chat thật (POST message → chờ agent trả lời), không chỉ
   test hàm riêng lẻ.

## Bài học rộng

- Khi server/service start trực tiếp bằng python (không qua bash), KHÔNG có
  `~/.bashrc` exports. Key phải được load từ file (`.env`) trong code, hoặc set
  trong Windows env / service config. Đừng bao giờ tin `os.environ.setdefault(x, os.environ.get(x, ""))` — nó chỉ chống lỗi, không load key từ đâu.
- OpenCode endpoint: empty-response rate KHÁC NHAU theo model — flash yếu với
  input dài, pro ổn. Đừng kết luận "provider chết" khi chưa thử model khác;
  benchmark 5 lần trước khi đổi hạ tầng.
