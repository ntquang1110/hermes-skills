# Chain LLM của công ty — 4 chân, và cách chẩn khi standup 0/5 agent (14/10/2026)

Áp dụng khi `hub/run.py standup` trả `(LLM trả None)` cho mọi agent, hoặc khi sửa `hub/store.py::call_deepseek`.

## Trạng thái chain 14/10 (sau fix)

| Chân | Endpoint | Ghi chú |
|------|----------|---------|
| 1. OpenCode Go | `opencode.ai/zen/go/v1/chat/completions` | cần header `x-opencode-session` + `User-Agent`; **chết** vì hết subscription |
| 2. ByteDance Ark | 2 URL `bytepluses` (`/api/v3/` rồi `/api/coding/v3/`) | **thiếu key** trong `.env` |
| 3. OpenRouter | `openrouter.ai/api/v1/chat/completions` | **free tier 0 credit** — không bền |
| 4. Google Gemini | `generativelanguage.googleapis.com/v1beta/models/<model>:generateContent` | free tier có quota thật — chân bảo hiểm cuối |

Điều khiển bằng `_call_fallbacks()` trong `hub/store.py`; mọi call site của `call_deepseek` đi qua nó.
`_ensure_env_keys()` nạp `BYTEDANCE_ARK_API_KEY`, `OPENROUTER_API_KEY`, `GOOGLE_API_KEY` từ `~/AppData/Local/hermes/.env`.

**QUAN TRỌNG — chain này là CẦU TẠM.** Chân 3 là tài khoản free `total_credits: 0` (đã 402 ngay giữa
standup, agent thứ 4-5 phải nhờ Gemini). Công ty 13 agent cần provider có credit thật → phải Quang quyết
(nạp credit / cấp lại key Ark).

## 3 lỗi cấu trúc đã sửa (nguyên nhân khiến 9 ngày không ai chẩn ra)

1. **`_call_bytedance` thiếu key thì `return None` IM LẶNG.** Log chỉ hiện "fallback ByteDance cũng
   thất bại", không có dòng `ByteDance fallback error` (vì chưa hề gọi HTTP) → tưởng Ark chặn, thực ra key
   biến mất khỏi `.env`. Nay có `[WARN] ByteDance bỏ qua (<agent>): thiếu KEY trong env/.env`.
   → **Dấu hiệu nhận biết: log có "fallback X cũng thất bại" mà KHÔNG có "fallback error" = chết ở bước
   đọc key, không phải provider chặn.**
2. **OpenCode trả 200 nhưng content RỖNG** thì `call_deepseek` return `None` luôn, không thử chân dự phòng.
   Nay rơi xuống `_call_fallbacks()`.
3. **402/429/5xx bị coi là lỗi cứng** → bỏ chân ngay. Nay retry có backoff (5s×attempt, 3 lần) rồi mới bỏ.

## Bẫy khi chẩn đoán

- **Đừng tin "request 200 + có nội dung" là chân đó còn tiền.** OpenRouter 200 ở 3 call đầu rồi 402 ở
  call 4-5. Kiểm `/api/v1/credits` → `total_credits` + `is_free_tier` TRƯỚC khi coi là bền.
- **Model Google bị đổi tên âm thầm:** `gemini-2.5-flash` / `-flash-lite` → **404 "no longer available to
  new users"**; dùng `gemini-3.5-flash-lite` (200 OK). `gemini-3.8-flash` bị **timeout** — timeout ≠ model
  không tồn tại, đừng kết luận sai.
- **Command-code đã hết là phương án thay thế:** `deepseek-v4.1-flash` → `unsupported_model`. Provider
  chạy được hôm trước có thể không còn chạy hôm sau — luôn probe lại bằng model THẬT.
- **OpenCode đổi kiểu lỗi:** 13/10 là "subscription required", 14/10 là `MissingSessionID` (cần header
  `x-opencode-session`) — cùng nguyên nhân, khác thông báo.
- **Báo cáo agent ngắn ≠ chain chết.** Dev1 trả đúng 20 ký tự `'Dưới đây là bản phân'` dù `max_tokens=2000`
  (reasoning token ăn budget). Đọc `standup_results[].report`, đừng đếm.
- **`.env` mtime = thời điểm key bị xoá.** So với lần `ByteDance fallback thành công` cuối trong
  `store/activity.json`.

## Verify (probe, KHÔNG phải test suite)

`python docs/qa/probe_llm_chain.py` — 23 assertion, exit 0 = PASS. Cấu trúc:
- Tầng 1 mock `requests.post`, assert **số lần gọi từng chân** (không chỉ giá trị trả về): chain chính sống
  → không chạm chân dự phòng; Ark sống → không chạm OpenRouter/Gemini; 402 → retry đủ 3 lần; cả 4 chết → `None`.
- Tầng 2 E2E gọi LLM THẬT trong **subprocess sạch** (`env` bỏ `BYTEDANCE_ARK_API_KEY` + `OPENCODE_GO_API_KEY`).
- Mutation: tắt hết key → phải `None` (probe biết FAIL).

**Pitfall bắt buộc nhớ:**
- Mutation phải tắt `S._ensure_env_keys = lambda: None`, KHÔNG thì nó tự nạp lại key từ `.env` → mutation
  không FAIL = **PASS giả**.
- Khôi phục sau mutation phải kiểm bằng **subprocess sạch**, KHÔNG bằng `importlib.reload` (reload không gỡ
  monkeypatch `requests.post` → case E2E fail giả).

## Kết quả 14/10

- Trước fix: OpenCode chết + Ark mất key → `call_deepseek` trả `None` → **0/5 agent báo cáo**.
- Sau fix: **5/5 agent báo cáo thật**. Probe 23/23 PASS, mutation PASS, E2E thật OK.
- Guard STALE chạy trước/sau đều **21** → sửa code không che số (không bump `updated_at`).

## Việc kèm theo: `.gitignore` thiếu `.m4a`

`tfo_data/uploads/*.m4a` **không** được ignore (`git check-ignore` exit 1) → audio cuộc họp có thể lọt vào
git. Đã bổ sung `*.m4a/*.aac/*.flac/*.aiff` + `tfo_data/uploads/chunks/`. Kiểm lại:
`git check-ignore tfo_data/uploads/<file>.m4a` phải **exit 0**.
