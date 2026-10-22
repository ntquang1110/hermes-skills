# Dựng fallback chain đầy đủ từ catalog provider + sửa config host từ xa (2026-09)

Case: user yêu cầu "cắm fallback cho máy Hermes mới, list hết model ra fallback lần lượt,
ưu tiên model lớn lên đầu". Host đích: Windows từ xa (lqremote), quản qua paramiko SSH.

## 1. Provider NATIVE vs custom — chọn native khi có

Hermes có sẵn provider id `nvidia` (NVIDIA NIM). Fallback chỉ cần:

```yaml
fallback_providers:
  - provider: nvidia
    model: nvidia/nemotron-3-ultra-550b-a55b
```
+ `.env`: `NVIDIA_API_KEY=nvapi-...`

**KHÔNG cần** `provider: custom` + `base_url` + `key_env` cho NVIDIA — dạng custom chỉ dùng khi
provider không có profile native. Danh sách provider native đầy đủ (nvidia, zai, kimi-coding,
minimax, groq?, stepfun, nebius-token-factory, alibaba, ...) ở docs
`/docs/user-guide/features/fallback-providers`; custom endpoint mới cần
`provider: custom` + `base_url` + `key_env`.

Verify chain: `hermes fallback list` → in `Fallback chain (N entries)` kèm `(via <provider>)`.

**Fallback trigger** (để biết khi nào chain thực sự chạy): 429 / 500 / 502 / 503 sau khi hết
retry; 401 / 403 / 404 ngay lập tức; response 200 nhưng content rỗng lặp lại. Auth fail lúc
khởi động CLI cũng nhảy fallback ngay.

## 2. Catalog KHÔNG bằng khả dụng thật — phải probe từng model

`GET /v1/models` liệt kê model mà **tài khoản không có quyền gọi**. Đo thật NVIDIA NIM free tier
(2026-09): 82 model trong catalog, sau khi lọc tên non-chat (embed / reward / safety / guard /
parse / rerank / asr / tts / clip / diffusion / ocr / detector / segmentation) còn **63 ứng viên**,
probe thật thì **chỉ 14 chạy được**:

- **49 model → HTTP 404** `{"status":404,"title":"Not Found","detail":"Function '<uuid>': Not found for account '<acc>'"}`
  = catalog có nhưng account không được serve. Bao gồm model cũ quen thuộc: llama-3.1-nemotron-70b,
  nemotron-4-340b, mixtral-8x22b, dbrx, mistral-large, yi-large, gemma-2b/3-12b, phi-3.5-moe,
  mistral-7b, codellama-70b, sea-lion-7b...
- **3 model timeout** ở 240s trong lần probe SONG SONG (llama-3.2-90b-vision, llama-3.2-11b-vision,
  gpt-oss-20b) — **chỉ 1 trong 3 thật sự chết.** Retry riêng, tuần tự: `openai/gpt-oss-20b` ✅ và
  `meta/llama-3.2-11b-vision-instruct` ✅ chạy được; `meta/llama-3.2-90b-vision-instruct` ❌ timeout
  cả khi retry 240s. → **roster thật là 16 model, không phải 14.** Đây là lý do bắt buộc retry tuần
  tự trước khi loại: probe song song timeout vì nghẽn/cold-start, không phải model chết.
- **1 model HTTP 500** (llama-3.2-11b-vision) ở lần probe song song — retry riêng thì PASS.

**Model chạy được (16)** — toàn dòng mới, xếp theo size giảm dần (sau khi retry tuần tự 3 model
timeout ở trên):

| Size | Model |
|---|---|
| 1T | `moonshotai/kimi-k3` |
| 550B | `nvidia/nemotron-3-ultra-550b-a55b` |
| 355B | `z-ai/glm-5.3` |
| ~200B | `deepseek-ai/deepseek-v4.1-flash` |
| 123B | `mistralai/mistral-nemotron` |
| 120B | `nvidia/nemotron-3-super-120b-a12b` |
| ~100B | `z-ai/glm-5.3-flash` |
| 31B | `google/gemma-4-31b-it` |
| 31B | `nvidia/ising-calibration-1.5-31b` |
| 30B | `meta/muse-glimmer-30b` |
| 30B | `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning` |
| 30B | `nvidia/nemotron-3.5-lightning-30b-a3b` |
| 20B | `openai/gpt-oss-20b` (chỉ chạy khi retry TUẦN TỰ) |
| 11B | `meta/llama-3.2-11b-vision-instruct` (chỉ chạy khi retry TUẦN TỰ) |
| 4B | `nvidia/riva-translate-4b-instruct-v1.1` (dịch thuật) |
| 4B | `nvidia/riva-translate-4b-instruct-v2` (dịch thuật) |
| 3B | `poolside/laguna-xs-2.1` (code) |

**Cảnh báo khi đưa hết vào chain:** 3 model cuối là model chuyên dụng (NMT / code) — trong agent
loop có tool schema chúng không gọi tool được. Cứ để cuối chain (size nhỏ tự xếp cuối) nhưng nói
rõ với user, đừng im lặng coi như model general.

## 3. Probe script (chạy được ngay, thay KEY)

```python
import json, re, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed

KEY  = "nvapi-..."
BASE = "https://integrate.api.nvidia.com/v1"
EXCLUDE = ["embed","reward","safety","guard","parse","rerank","retriever","asr","tts",
           "vision-encode","clip","diffusion","flux","sdxl","deplot","grounding","ocr",
           "detector","segmentation","biomedclip"]

def is_chat(m):  return not any(k in m.lower() for k in EXCLUDE)
def size_of(m):
    mm = re.search(r"-(\d+(?:\.\d+)?)b(?:-|$)", m.lower()) or re.search(r"-(\d+)b", m.lower())
    return float(mm.group(1)) if mm else 0.0

ids = [m["id"] for m in json.loads(urllib.request.urlopen(
    urllib.request.Request(f"{BASE}/models",
        headers={"Authorization": f"Bearer {KEY}"}), timeout=30).read())["data"]]
chat = sorted([m for m in ids if is_chat(m)], key=lambda x: -size_of(x))

def probe(mid):
    body = json.dumps({"model": mid, "messages":[{"role":"user","content":"hi"}],
                       "max_tokens": 8, "temperature": 0.1}).encode()
    try:
        d = json.loads(urllib.request.urlopen(urllib.request.Request(
            f"{BASE}/chat/completions", data=body,
            headers={"Authorization": f"Bearer {KEY}", "Content-Type":"application/json"},
            method="POST"), timeout=90).read())
        ch = d.get("choices") or []
        if not ch: return (mid, False, "no choices")
        msg = ch[0].get("message", {})
        txt = (msg.get("content") or "") + (msg.get("reasoning_content") or "")
        return (mid, bool(txt.strip()), txt.strip()[:60])
    except urllib.error.HTTPError as e:
        return (mid, False, f"HTTP {e.code}: {e.read().decode()[:120]}")
    except Exception as e:
        return (mid, False, f"{type(e).__name__}")

with ThreadPoolExecutor(max_workers=6) as ex:
    for f in as_completed([ex.submit(probe, m) for m in chat]):
        mid, ok, info = f.result()
        print(("OK " if ok else "XX "), mid, "|", info)
```

Lưu ý khi probe:
- `max_tokens=8` là đủ để biết model sống, nhưng model reasoning sẽ trả `content: ''` +
  `reasoning_content` có nội dung → **coi như OK** (đừng kết luận chết vì content rỗng).
- Concurrency 6 là an toàn; đẩy cao hơn dễ dính pool 503 của free tier (xem
  `references/nvidia-nim-endpoint-2026-09.md`).
- Model timeout ở lần chạy song song phải **retry riêng, tuần tự, timeout dài** trước khi loại
  hẳn — tránh loại oan model chỉ chậm cold start.
- Sort theo size cần bảng bù cho tên không chứa số tham số (`yi-large`, `dbrx`,
  `mixtral-8x22b`, `kimi-k3`, `glm-5.3`, `laguna-xs`): map tay, đừng để 0.0B rồi xếp bừa.

## 4. Ghi `fallback_providers` vào config — theo DÒNG, không dùng regex DOTALL

`hermes config set fallback_providers ...` lưu thành string → vô hiệu (xem pitfall fallback
string trong SKILL.md). Phải sửa file.

**Bẫy đã dính thật:** dùng regex `(?ms)^fallback_providers:\n(?:[ \t]+.*\n|\n)*?(?=^\S)` để xóa
block cũ — với `(?s)` DOTALL, `.*` ăn xuyên dòng, backtracking rồi match luôn tới `\n` cuối file
→ nuốt hết cả `platforms:` trở xuống → bước "chèn trước `platforms:`" fail với
`ERROR: no 'platforms:' anchor`. (Lần đó script raise trước khi write nên file còn nguyên — luôn
`raise` trước khi ghi để regex sai không phá file.)

**Cách đúng — xử lý theo dòng:**

```python
text  = open(cfg, encoding="utf-8-sig").read()
lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")

# 1. bỏ block cũ: dòng top-level + các dòng thụt/trống theo sau
out, i = [], 0
while i < len(lines):
    if lines[i] == "fallback_providers:":
        i += 1
        while i < len(lines) and (lines[i].startswith((" ", "\t")) or lines[i].strip() == ""):
            i += 1
        continue
    out.append(lines[i]); i += 1

# 2. block mới
block = ["fallback_providers:"]
for m in CHAIN:
    block += ["  - provider: nvidia", f"    model: {m}"]

# 3. chèn trước anchor top-level
idx = out.index("platforms:")          # ValueError = anchor mất -> thoát, KHÔNG ghi
new = "\r\n".join(out[:idx] + block + out[idx:])
open(cfg, "w", encoding="utf-8", newline="").write(new)
```

Giữ `\r\n` cho cả file để không trộn line-ending, và đọc bằng `utf-8-sig` để nuốt BOM
(`Set-Content -Encoding UTF8` của PowerShell thêm BOM → `platforms:` đầu file có thể dính
`\ufeff` làm `out.index("platforms:")` fail).

## 5. Quản host Windows từ xa bằng paramiko — 2 mẹo bắt buộc

**(a) PowerShell qua SSH: base64 `-EncodedCommand`, đừng nhồi dấu nháy.**

```python
import base64
def ps(client, script, timeout=300):
    enc = base64.b64encode(script.encode("utf-16-le")).decode()
    _, out, _ = client.exec_command(f"powershell -NoProfile -EncodedCommand {enc}", timeout=timeout)
    return out.read().decode("utf-8", "replace").strip()
```
Lý do: nhồi path Windows (`C:\Users\...`) vào `powershell -Command "..."` qua bash SSH → dấu
`\` bị bash/PowerShell ăn lẫn nhau, lỗi khó đọc. Base64 UTF-16LE né sạch.

**(b) Sửa file config/.env: dùng SFTP, đừng dựng chuỗi trong shell.**

```python
sftp = client.open_sftp()
text = sftp.open(CFG, "r").read().decode("utf-8-sig")   # đọc
with sftp.open(CFG, "w") as f: f.write(new_text)         # ghi
```
Nhanh, giữ nguyên nội dung, không phải escape. `cat`/`Get-Content` chỉ dùng để *hiển thị* kết quả.

**PITFALL — đừng viết `python -c "..."` inline với path Windows.** Backslash trong chuỗi Python
inline bị hiểu là escape:
```
SyntaxError: (unicode error) 'unicodeescape' codec can't decode bytes in position 38-39: truncated \UXXXXXXXX escape
```
Luôn ghi script ra file (`write_file`) rồi `python script.py`. Cũng đúng cho mọi thao tác
paramiko nhiều bước — script file dễ sửa và chạy lại, `-c` một dòng thì vỡ ở lần chỉnh thứ hai.

## 6. Verify chain thật (đừng chỉ tin `fallback list`)

1. `hermes fallback list` → đủ N entries, đúng thứ tự.
2. Ép primary fail để chain chạy thật: khi primary đang 429 quota, chạy
   `hermes -z "<câu hỏi tiếng Việt ngắn>"` → phải trả lời đúng (nghĩa là fallback đã phục vụ).
3. Đối chiếu `logs/errors.log` xem 429/401 có đúng là của primary không, và
   `logs/gateway.log` tìm `Gateway running with N platform(s)`.
4. **Verify KHẢ NĂNG AGENT, không chỉ "model sống".** Model top chain (`moonshotai/kimi-k3`, 1T)
   pass probe "hi" và trả lời đúng câu hỏi kiến thức, nhưng **đẻ `!!!!!!!!` ở lượt sau tool-call**
   → mọi lần fallback hỏng. Prompt buộc gọi tool, chạy trong chính harness:
   ```powershell
   hermes --provider nvidia -m <model> -z "Dung lenh terminal de tinh 5 nhan 6, roi tra loi ngan gon."
   # "5 × 6 = **30**" = tốt   |   "!!!!..." = hỏng, đẩy xuống cuối chain
   ```
   Chẩn đoán khi đã thấy rác: đọc `state.db` (`messages.content` / `reasoning_content` /
   `finish_reason` + `sessions.model`) để biết model nào sinh ra nó. Chi tiết, ma trận khả năng
   agent từng model, và thứ tự chain đúng → `fallback-model-agent-capability-2026-09.md`.
   Script probe → `../scripts/probe_agent_capability.py`.

## 7. Nếu chain có nhiều entry chết (404)

Mỗi entry 404 tốn 1 vòng request rồi mới nhảy tiếp — chain 15 entry mà 49 entry chết chèn vào
sẽ cộng thêm hàng chục giây trước khi tới model sống. **Lọc model chết khỏi config**, đừng
"cho đủ danh sách cho oai": 404 là lỗi account-scoped, không tự khỏi.
