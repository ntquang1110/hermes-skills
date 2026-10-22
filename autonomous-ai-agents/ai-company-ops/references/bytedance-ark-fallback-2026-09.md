# ByteDance Ark fallback — cứu team khi OpenCode Go hết sub (22/09/2026)

Khi OpenCode Go báo `server_error: An active OpenCode Go subscription is required`
hoặc `AuthError: Invalid API key`, `call_deepseek()` trong `hub/store.py` tự fallback
sang ByteDance Ark endpoint OpenAI-compatible:

- URL: `BYTEDANCE_URLS` = `["/api/v3/", "/api/coding/v3/"]` (thử lần lượt — xem mục quota bên dưới)
- Model: `deepseek-v4-flash-ga-260731`
- Key: `BYTEDANCE_ARK_API_KEY` trong `~/AppData/Local/hermes/.env` (prefix `ark-`)
- Code: `_call_bytedance()` + `_ensure_env_keys()` + 2 điểm fallback trong
  `call_deepseek()` (key thiếu + response non-200). Verify standup 22/09: 5/5 agent
  có báo cáo sau chuỗi None 11 ngày (09→21/09).

## ⚠️ QUOTA TÁCH RIÊNG TỪNG ENDPOINT — 429 KHÔNG PHẢI HẾT CÚNG (27/09, chết 5/5 agent)

`hub/store.py` từng hardcode 1 URL (`BYTEDANCE_URL`). Commit `ddb3046` (23/09) đổi
`/api/v3/` → `/api/coding/v3/`. Đến 27/09 endpoint đó **hết quota tuần**:

```
HTTP 429 {"error":{"code":"AccountQuotaExceeded",
  "message":"You have exceeded the weekly usage quota.
  It will reset at 2026-09-28 00:00:00 +0800 CST..."}}
```

→ standup 5/5 `(LLM trả None)` 2 lần liên tiếp (09:04 + 09:05), **không phải hết credit
toàn cung** — `/api/v3/` vẫn 200 (2.9s, len=179). Quota tính RIÊNG theo từng path.

**Fix (commit `06f3477`, verify thật):**
- `BYTEDANCE_URLS = ["/api/v3/", "/api/coding/v3/"]` — thử lần lượt, hết 1 sang cái 2.
- **Retry 3 lần mỗi endpoint** cho case `200` nhưng content rỗng (transient ~40-80%
  input dài, đã dính ở Content lúc 09:09). `429`/exception thì `break` sang endpoint kế,
  KHÔNG lặp vô ích. `time.sleep(2)` giữa lần retry.
- `add_activity` ghi endpoint + số lần retry để truy vết.

**Quy tắc chẩn đoán khi standup None mà ĐÃ CÓ fallback:**
1. Đọc `store/activity.json` → key là `d['activity']` (dict 1 cấp, KHÔNG phải `items`)
   → phân biệt 3 case: `[ERROR] ByteDance fallback thất bại hết N endpoint` (quota endpoint)
   vs `empty content` (transient) vs `[WARN] OpenCode API error` (chính OpenCode chết).
2. **Test TỪNG URL riêng** với payload thật (`format_system_prompt(agent)` + `max_tokens=2000`),
   không chỉ payload "noi ok" — payload nhỏ không lộ rate limit.
3. Đừng kết luận "hết credit" khi mới thấy 429. Đọc `resp.text` (body có `code` + `reset at`)
   chứ đừng in `str(exception)`.
4. Sau khi sửa, verify bằng **1 agent cụ thể** (`BaseAgent('Content').daily_standup()`)
   trước khi chạy lại cả standup 5 agent — tiết kiệm 5 phút/lượt.
5. **Cách verify fix fallback chain** (probe 2 tầng: mock transport + LLM thật; bẫy
   `requests.post` monkeypatch KHÔNG bị `importlib.reload` gỡ) → `references/verify-fallback-chain-2026-09.md`.

## Pitfall: log trùng sau khi thêm log endpoint (27/09)

Khi `_call_bytedance` bắt đầu log `[OK] ByteDance fallback thành công` kèm endpoint,
`call_deepseek` còn log `[OK] ByteDance fallback thành công` lần nữa ở **cả 2 call site**
→ mỗi lần fallback ra 2 dòng OK giống hệt nhau, đọc log không phân biệt được endpoint nào
thành công. Sửa: bỏ `add_activity` ở `call_deepseek`, để `_call_bytedance` (nơi biết endpoint
+ số lần retry) log một lần. Tương tự, `url.split("/api/")[1][:6]` chạy lặp mỗi dòng log →
tách 1 biến `tag` trước vòng lặp. Sau khi dọn code, verify lại từ đầu — bằng chứng cũ đã
không còn mô tả đúng code.

## Pitfall: worker 8100 chạy env khác `hub/` trực tiếp

`hub/store.py::_ensure_env_keys()` chỉ nạp key khi import trong process đó.
Server 8100 (`app/main.py::load_keys()`) là process riêng, khởi động từ
`tfo_launch.py` — nếu `load_keys()` chỉ nạp OPENCODE/GROQ mà quên BYTEDANCE,
fallback trong worker chết im: queue item `status=error`, thread task toàn
`⚠️ Lỗi: agent không trả về kết quả (provider transient)`, dù gọi `call_deepseek`
trực tiếp từ terminal vẫn OK (env terminal có key).

Fix: thêm vào `load_keys()` trong `app/main.py`:

```python
if line.startswith("BYTEDANCE_ARK_API_KEY=") and "..." not in line:
    os.environ["BYTEDANCE_ARK_API_KEY"] = line.split("=", 1)[1].strip()
```

## Recipe verify sau khi sửa key/fallback (đã chạy thật 22/09)

1. `python -m py_compile hub/store.py app/main.py` — cả 2 phải pass.
2. Kill 8100 cũ: `python -c "import os,signal; os.kill(<pid>,signal.SIGTERM)"`
   (taskkill qua git-bash/MSYS bị lỗi parse — xem pitfall taskkill trong skill chính).
3. Start mới: `terminal(background=true)` + `python .../tfo_launch.py`, chờ
   `Application startup complete`.
4. Wake thật: `python hub/wake_agent.py 8 "<nhiệm vụ>" "QA"` → chờ ~2-3 phút
   (worker retry flash→pro nhiều vòng) → đọc thread task #8 source=ai: phải có
   response agent thật, queue item `status=done`.
5. Đừng tin `call_deepseek` trực tiếp — nó chạy env terminal, không chứng minh
   worker 8100 đã có key.
6. Commit + push: `git add hub/store.py app/main.py briefing.md` (KHÔNG `git add -A`
   — `tfo_data/uploads/*.m4a`, `store/*.json` là local/gitignored).
