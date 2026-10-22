# Verify một fix fallback chain — probe có mục đích, KHÔNG phải test suite (27/09/2026)

Áp dụng sau khi sửa `hub/store.py::call_deepseek` / `_call_bytedance` (fallback chain nhà cung cấp LLM).
Bối cảnh: fix quota Ark 2-endpoint (`06f3477`) → hệ thống yêu cầu bằng chứng verify mới, bằng chứng cũ
đã stale (trỏ vào probe trước khi thêm retry). Repo **không có test harness nào** — đừng bịa lệnh
`pytest`/`make test`. Tự viết probe.

## Nguyên tắc

- **Đây là probe có mục đích, không phải test suite.** Ghi rõ điều này trong báo cáo, đừng gọi
  nó là "test suite pass" — người đọc sẽ tưởng có regression protection mà thực tế không có.
- Script tạm phải nằm **ngoài repo** (`~/AppData/Local/Temp/hermes-verify-*.py`) và **xoá ngay**
  sau khi chạy. Trong repo thì nó gây nhiễu `git status` / `git pull --rebase` (xem
  `references/cron-mode-scripts-2026-09.md`).
- Chạy 1 lần rồi xoá. Không lưu lại thành test.
- Exit code phải phản ánh FAIL (`sys.exit(1)`) để evidence tool đọc được, đừng chỉ in PASS.

## Cấu trúc probe 2 tầng

**Tầng 1 — mock transport, khởi động nhanh, phủ từng nhánh hành vi.**
Monkeypatch `requests.post` để mô phỏng đúng từng tình huống:

```python
class Resp:
    def __init__(self, code, content):
        self.status_code, self.text = code, json.dumps({"e": code})
        self._c = content
    def json(self):
        return {"choices": [{"message": {"content": self._c}}]}

REAL_SLEEP, REAL_POST = time.sleep, requests.post   # GIỮ LẠI để gỡ mock

def fake_post(url, **kw):
    log.append(url.split("/api/")[1][:6])   # tag phân biệt endpoint
    i, state[url] = state[url], state[url] + 1
    item = seq[url][i] if i < len(seq[url]) else seq[url][-1]
    if isinstance(item, Exception):
        raise item
    return item
```

Nên phủ 5 nhánh cho một chain N-endpoint có retry:
1. `200` rỗng rồi `200` thật → retry **cùng endpoint**, KHÔNG nhảy sang endpoint sau
2. `429` endpoint đầu → `break` sang endpoint sau, đúng 1 lần mỗi endpoint
3. Cả N endpoint `429` → `None` với đúng N calls (chứng minh **không lặp vô ích** khi lỗi quota)
4. Rỗng hết retry ở cả N → `None` với N × số lần retry
5. Network exception → `break` sang endpoint sau

Assert **cả số lần gọi từng endpoint** (`log.count(tag)`), không chỉ assert giá trị trả về —
"số lần gọi" mới là thứ phân biệt retry-đúng với retry-vô-ich.

Chặn `time.sleep` trong lúc mock cho probe chạy nhanh, **nhưng khôi phục trong `finally`**
không thì các case sau (và case LLM thật) bị treo/ngủ thừa.

**Tầng 2 — 1 call LLM thật, không mock.** Chứng minh end-to-end trên đúng code đã sửa:

```python
res = S.call_deepseek("deepseek-v4-flash", "Bạn là trợ lý.",
                      [{"role": "user", "content": "Trả lời đúng 1 từ: ok"}],
                      temperature=0.1, max_tokens=10, agent_name="verify-e2e")
assert res and res.strip()
```

`max_tokens` nhỏ, prompt ngắn → gần như miễn phí. Tầng 1 bắt logic, tầng 2 bắt tích hợp thật.

## ⚠️ BẪY — `importlib.reload` KHÔNG gỡ monkeypatch trên module khác

Sau khi monkeypatch `requests.post`, `importlib.reload(hub.store)` **không** khôi phục
`requests.post` — `reload` chỉ nạp lại module được chỉ định, `requests` vẫn giữ hàm giả.
Case E2E fail **giả**, dễ dẫn tới debug nhầm hướng vào code thật.

```python
requests.post = REAL_POST        # phải gán LẠI thủ công, TRƯỚC reload
importlib.reload(S)              # nạp lại hub.store sạch
assert requests.post is REAL_POST
```

Tương tự: `time.sleep`, `add_activity` — mọi thứ đã patch đều phải gán lại tay.

## Cảnh báo khác trong lúc verify

- **Đừng dùng payload tầm thường để test rate limit.** `"noi ok"` với `max_tokens=8` không lộ
  quota/rate limit. Test từng URL riêng với **payload thật** (`format_system_prompt(agent)` +
  `max_tokens=2000`). Ở case này payload nhỏ trả 200 cho cả 2 endpoint — chỉ payload thật mới
  lộ ra endpoint nào hết quota.
- **Sửa code thì nhìn lại chính dòng vừa sửa.** Ở lượt verify này phát hiện 2 vấn đề KISS/DRY
  ngay trong diff: `add_activity("[OK] ...")` bị log trùng 2 lần (`_call_bytedance` đã log,
  `call_deepseek` lại log lần 2 ở cả 2 call site), và `url.split("/api/")[1][:6]` chạy lặp
  5 lần mỗi dòng log thay vì tính 1 lần ra biến `tag`. Sửa xong **phải verify lại từ đầu** —
  bằng chứng cũ đã không còn mô tả đúng code.
- Sau khi dọn code, chạy lại **tác vụ thật** (`python hub/run.py standup`) chứ không chỉ probe.
  Kết quả mong đợi: 5/5 agent có báo cáo.

## Verify bằng chứng đã commit

```bash
python hub/verify_done.py --claim "<short-hash>"   # ACCEPT = đã push origin/main
python -m py_compile hub/store.py                 # luôn, sau mỗi patch .py
git status --porcelain                            # KHÔNG còn file tạm do em tạo
```

Bảo đảm working tree chỉ còn untracked file runtime đã biết (`tfo_data/uploads/*.m4a`,
`tfo_data/context_scan.json`, `store/tasks.json.bak_*`) — không file `.standup_*.txt` /
`.json` do probe để lại.
