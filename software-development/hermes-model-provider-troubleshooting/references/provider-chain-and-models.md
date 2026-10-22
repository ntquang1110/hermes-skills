# Provider / fallback chain / model — chi tiết

> Tách từ `SKILL.md` ngày 19/10/2026. Nội dung giữ nguyên văn.


---

## Thêm provider MỚI làm fallback — tạo plugin model-provider (case ByteDance Ark, 2026-09)

Khi user cấp endpoint OpenAI-compatible của một provider CHƯA có profile (vd
ByteDance Ark/Volcano `ark.ap-southeast.bytepluses.com` serve
`deepseek-v4-flash-ga-260731`), đừng chỉ đặt `providers.<name>.base_url` — Hermes
KHÔNG nhận `--provider <tên>` nếu không có plugin profile → session ghi
`provider=opencode-zen` (default) dù trả lời đúng. Đủ trọn quy trình:

1. **Test endpoint trực tiếp TRƯỚC** (curl): chat, tool calling, streaming, JSON
   mode. DeepSeek V4 → trả `reasoning_content` (thinking) — lưu ý khi parse.
2. **Key vào `.env`**: `BYTEDANCE_ARK_API_KEY=ark-...` (không nháy, không bọc).
3. **Tạo plugin profile** tại `plugins/model-providers/<name>/` (Hermes data đã
   junction → `D:/Hermes/hermes-home/plugins/model-providers/<name>/`):
   - `plugin.yaml`: `name: <name>-provider`, `kind: model-provider`, description.
   - `__init__.py`: copy shape `deepseek/__init__.py` rồi đổi name/env_vars/
     base_url/model. **Bắt buộc giữ `build_api_kwargs_extras` bơm
     `extra_body["thinking"]={"type":"enabled"|"disabled"}` + top-level
     `reasoning_effort`** — DeepSeek V4 yêu cầu bật/tắt thinking tường minh,
     thiếu sẽ dính lỗi echo `reasoning_content must be passed back` (HTTP 400)
     sau tool call đầu tiên (#15700/#17212/#17825).
4. **Cấu hình provider**: `hermes config set providers.<name>.base_url <url>` (+
   `stale_timeout_seconds`/`ttfb_timeout_seconds`).
5. **Thêm fallback**: `hermes config set fallback_providers '[...]'` lưu STRING —
   KHÔNG hợp lệ (xem pitfall fallback string). Sửa file qua python text-line
   (patch tool chặn ghi config.yaml; desktop app đang chạy sẽ revert — xem pitfall
   desktop revert), rồi verify:
   ```python
   import yaml; d=yaml.safe_load(open(r'<home>/config.yaml',encoding='utf-8'))
   assert isinstance(d['fallback_providers'], list)
   ```
6. **Verify thật**: `hermes chat -q "..." --provider bytedance --model
   deepseek-v4-flash-ga-260731` → kết quả + `python` check session mới nhất trong
   state.db ghi `billing_provider=bytedance`, `model=deepseek-v4-flash-ga-260731`
   (không phải default). Test direct API bằng `urllib` đã đủ chứng minh endpoint;
   test qua Hermes chứng minh plugin profile được nạp.
7. `hermes fallback list` → thấy provider mới ở vị trí đã thêm.

Latency đo thật (2026-09): tool-call 1.5s, streaming 2s, câu dài có reasoning
~12s — chấp nhận làm fallback.

#### PITFALL — ByteDance Ark `key_env` fails with coding-plan key format (JWT-like, not `ark-*`)

**Triệu chứng:** trên Hermes git-install mới, `custom_providers` dùng `key_env: BYTEDANCE_ARK_API_KEY` với key coding plan (dạng `VxCgNvLTE.Ch...` — dài ~180-200 ký tự, 3 đoạn cách dấu chấm). Direct API call qua curl/Invoke-RestMethod **200 OK**, nhưng Hermes gọi ra **401**:
```
openai.AuthenticationError: Error code: 401
{'error': {'code': 'AuthenticationError', 'message': 'The API key format is incorrect.'}}
```

**Nguyên nhân:** `key_env` có thể thêm ký tự đặc biệt (whitespace, BOM, newline) hoặc provider custom plugin xử lý key khác so với native `bytedance` provider. Key coding plan ByteDance dạng JWT (`VxCg...`) không giống key truyền thống (`ark-...`) và có thể không tương thích với `key_env` ở một số phiên bản Hermes.

**Fix — dùng `api_key` trực tiếp thay vì `key_env`:**
```yaml
custom_providers:
  - name: Ark.ap-southeast.bytepluses.com
    base_url: https://ark.ap-southeast.bytepluses.com/api/coding/v3
    model: deepseek-v4.1-flash
    api_key: VxCgNvLTE...   # <-- ghi thẳng key, KHÔNG dùng key_env
```
Hoặc qua CLI (cẩn thận vì `hermes config set` có thể không nhận diện được key path trong custom_providers):
```bash
hermes config set custom_providers[0].api_key "<key>" --force
```
(Nếu cách trên tạo block rác `custom_providers[0]:` cuối file, sửa bằng python text-line.)

**Kiểm tra:** `hermes -z "say hi"` → phải trả lời, không 401.

**Lưu ý:** `.env` phải được ghi bằng UTF-8-NoBOM (dùng `System.IO.StreamWriter` trong PowerShell, không dùng `Set-Content -Encoding UTF8` vì thêm BOM). Nếu dùng PowerShell:
```powershell
$sw = New-Object System.IO.StreamWriter($envFile, $false, [System.Text.UTF8Encoding]::new($false))
$sw.WriteLine("BYTEDANCE_ARK_API_KEY=$key")
$sw.Close()
```


---

## ByteDance Ark — scan model list trước khi chọn (chỉ 5/13 text model chạy được)

Endpoint `/v1/models` trả 55 model (kể cả vision/embedding/audio/3d). Không phải model
nào cũng call được — test thật 2026-09, chỉ **5 text model trả 200**:

| Model | Kết quả |
|---|---|
| `deepseek-v4-flash-ga-260731` | ✅ 1.5s (dùng làm primary/fallback) |
| `deepseek-v4-pro-ga-260813` | ✅ 2.0s |
| `deepseek-v4-flash-260425` | ✅ 1.4s |
| `deepseek-v4-pro-260425` | ✅ 1.7s (trả `OK.</think>OK` — bỏ tag think khi parse) |
| `seed-2-0-code-preview-260328` | ✅ 1.1s |
| `deepseek-v3-2/3-1/r1-250528`, `kimi-k2*`, `glm-5-2/4-7`, `gpt-oss-120b` | ❌ HTTP 404 (không được serve) |

→ scan `/v1/models` + probe từng model TRƯỚC khi set làm fallback; đừng chọn model
đẹp trên giấy. Code probe mẫu: loop `chat/completions` max_tokens=20, đếm OK/FAIL.


---

## Dựng FALLBACK CHAIN đầy đủ từ catalog provider ("list hết model ra fallback")

Khi user đòi một chain dài ("cắm hết model vào fallback, ưu tiên model lớn trước"), quy trình
4 bước — chi tiết + script probe chạy được + bảng model NVIDIA NIM →
`references/nvidia-nim-fallback-chain-2026-09.md`:

1. **Provider NATIVE trước, custom sau.** NVIDIA NIM có sẵn id `nvidia` trong Hermes → chỉ cần
   `fallback_providers: [- provider: nvidia / model: X]` + `NVIDIA_API_KEY`. Dạng
   `provider: custom` + `base_url` + `key_env` chỉ dùng cho endpoint KHÔNG có profile native.
2. **Probe catalog, đừng tin catalog.** `/v1/models` liệt kê cả model account không được serve.
   Đo thật NVIDIA free tier: 63 ứng viên chat → **chỉ 14 chạy được**; 49 model trả
   `404 Function '<uuid>': Not found for account`, 3 model timeout 240s. Lọc tên non-chat
   (embed/reward/safety/guard/parse/asr/clip/ocr/detector...) trước, rồi probe `max_tokens=8`
   từng model (concurrency 6), và **retry riêng tuần tự** những model timeout trước khi loại —
   kẻo loại oan model chỉ chậm cold start. Model reasoning trả `content: ''` +
   `reasoning_content` = VẪN TỐT, đừng kết luận chết.
3. **Xếp hạng theo KHẢ NĂNG AGENT, không theo size.** Đo thật 2026-09: model to nhất chain
   (`moonshotai/kimi-k3`, 1T) pass probe "hi" nhưng **đẻ `!!!!!!!!` ở lượt sau tool-call** → mọi
   lần fallback đều hỏng. Thứ tự đúng: (a) model đã verify tool round-trip OK, xếp size giảm dần;
   (b) model chưa verify đủ / intermittent; (c) model hỏng hoặc chuyên dụng (NMT/code/calibration)
   xuống CUỐI. Bảng khả năng agent từng model + cách verify →
   `references/fallback-model-agent-capability-2026-09.md`, script `scripts/probe_agent_capability.py`.
   Vẫn cần bảng bù size tay cho tên không chứa số tham số (`yi-large`, `dbrx`, `mixtral-8x22b`,
   `kimi-k3`, `glm-5.3`) — nếu không chúng rơi về 0.0B rồi xếp bừa.
4. **Lọc entry chết khỏi config.** Mỗi entry 404 tốn 1 vòng request mới nhảy tiếp — nhồi 49 entry
   chết vào chain là cộng hàng chục giây trước khi tới model sống. 404 account-scoped KHÔNG tự khỏi.
5. **Retry TUẦN TỰ trước khi loại model timeout.** 3 model timeout ở probe song song (240s) — retry
   riêng thì **2 trong 3 chạy được thật** (`openai/gpt-oss-20b`,
   `meta/llama-3.2-11b-vision-instruct`); chỉ `meta/llama-3.2-90b-vision-instruct` chết thật
   (timeout cả khi retry 240s). Roster cuối thực tế là **16 model**, không phải 14 — nếu không retry
   tuần tự là loại oan model dùng được.

### PITFALL — sửa block YAML top-level bằng regex `(?s)` sẽ NUỐT cả file

Xóa block cũ bằng `re.sub(r"(?ms)^fallback_providers:\n(?:[ \t]+.*\n|\n)*?(?=^\S)", "", cfg)`:
với DOTALL, `.*` ăn xuyên dòng rồi backtrack tới `\n` cuối file → nuốt luôn `platforms:` trở
xuống → bước chèn trước anchor fail `ERROR: no 'platforms:' anchor`. **Sửa config theo DÒNG**
(bỏ dòng top-level + các dòng thụt/trống theo sau, chèn lại trước anchor top-level), giữ `\r\n`,
đọc `utf-8-sig`. Code mẫu → reference trên. Nguyên tắc an toàn: **`raise` TRƯỚC khi ghi file** để
regex sai không phá config.

### PITFALL — model lớn nhất chain trả `!!!!` ở LƯỢT TOOL-RESULT (không phải lỗi hiển thị)

Triệu chứng: output là `!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!` (32 dấu `!`) thay vì câu trả lời. Đây
KHÔNG phải artifact render, KHÔNG phải lỗi harness — model thật sự sinh ra nó, và nó chỉ xuất hiện
khi primary đã fail (đang chạy fallback).

**Chẩn đoán quyết định — đọc `state.db`, đừng đoán từ stdout.** Bảng `messages` lưu TÁCH RIÊNG
`content`, `reasoning_content`, `finish_reason`, `tool_calls`; join `sessions.model` để biết model nào:

```python
import sqlite3
con = sqlite3.connect(r"<HERMES_HOME>\state.db"); con.row_factory = sqlite3.Row
for r in con.execute("""
  SELECT session_id, role, substr(content,1,80) c, finish_reason, reasoning_content, tool_calls
  FROM messages WHERE session_id IN (
      SELECT id FROM sessions ORDER BY started_at DESC LIMIT 8)
  ORDER BY session_id DESC, rowid ASC"""):
    print(dict(r))
# model của từng session: SELECT id, model, billing_provider FROM sessions ORDER BY started_at DESC LIMIT 12
```

Đo thật: model gọi `terminal` → tool trả `{"output":"30"}` → lượt kế tiếp assistant có
`content=''` + `reasoning_content='!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'`. Đối chiếu ngược:
`SELECT reasoning_content FROM messages WHERE session_id=...` — thấy `!` nằm ở đây là chốt.
Cùng model trả lời **đúng** cho câu hỏi KHÔNG cần tool (vd "thủ đô Việt Nam") → bug CHỈ lộ ở lượt
tool-result. Đừng kết luận "model chết" khi test bằng câu hỏi kiến thức.

**Vì sao probe "hi" / probe chat 1 lượt KHÔNG bắt được:** probe thường không có tool schema +
system prompt ~15K token như session agent thật. Bug chỉ hiện sau khi model nhận tool-result.
Verify phải chạy trong CHÍNH harness Hermes, với prompt BUỘC gọi tool:

```powershell
hermes --provider <provider> -m <model> -z "Dung lenh terminal de tinh 5 nhan 6, roi tra loi ngan gon."
# OK   -> "5 × 6 = 30"
# HỎNG -> "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
```

**Fix:** đẩy model đó xuống CUỐI chain (hoặc bỏ hẳn) — đừng để ở vị trí đầu. Chain hỏng ở entry #1
thì mọi lần fallback đều vô dụng dù 16 entry sau đều tốt: user thấy "model provider failed" hoặc rác.
Đây chính là lý do thứ tự chain phải theo khả năng agent, không theo size (mục "Dựng FALLBACK CHAIN"
bước 3). Script probe cả chain → `scripts/probe_agent_capability.py`.

### Quản Hermes host Windows TỪ XA (paramiko) — 2 mẹo bắt buộc

**Tiên quyết — kiểm tra ĐƯỜNG VÀO trước khi hứa "để em SSH vào setup".** Máy Windows từ xa thường
KHÔNG sẵn SSH. Quét cổng trước bằng `socket.connect_ex` lần lượt 22 / 2222 / 3389 / 5985 / 5986 /
443 / 80 — **`3389` mở KHÔNG có nghĩa SSH dùng được** (RDP ≠ SSH, và agent không lái được RDP).
Nếu `22` đóng, bật OpenSSH Server trên máy đích (PowerShell **Admin**):

```powershell
Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0
Start-Service sshd; Set-Service -Name sshd -StartupType Automatic
netsh advfirewall firewall add rule name="OpenSSH" dir=in action=allow protocol=TCP localport=22 profile=any
```

`profile=any` là bắt buộc — rule mặc định không áp cho profile Public (và `Enable-PSRemoting` fail
với `network connection types ... set to Public`). Rồi xác nhận service đang nghe:
`Get-Service sshd` + `netstat -ano | findstr :22` → LISTENING.

**Nếu service đã listen mà vẫn `Unable to connect to port 22`** → cổng chưa được forward ở
router/modem. Port forward là việc của user, không làm được từ xa — nói thẳng và chuyển phương án B
(hướng dẫn user tự chạy lệnh trong PowerShell). Đừng thử WinRM như đường vòng: 5985/5986 phải qua
đúng cái router đó nên cũng tắc y hệt.

- **PowerShell qua SSH → base64 `-EncodedCommand`**: `base64.b64encode(script.encode("utf-16-le"))`
  rồi `powershell -NoProfile -EncodedCommand <b64>`. Nhồi path Windows vào
  `powershell -Command "..."` qua bash SSH bị ăn dấu `\` lẫn nhau.
- **Sửa config/.env → SFTP**, không dựng chuỗi trong shell: `sftp.open(path,"r").read().decode("utf-8-sig")`
  và `sftp.open(path,"w").write(text)`. Giữ nguyên nội dung, không phải escape.
- **PITFALL `python -c` inline với path Windows** → `SyntaxError: (unicode error) 'unicodeescape'
  codec can't decode bytes ... truncated \UXXXXXXXX escape`. Ghi script ra file rồi chạy; đúng cho
  mọi thao tác paramiko nhiều bước (dễ sửa và chạy lại).

### PITFALL — ByteDance Ark free có TPM limit (HTTP 429), không phải vô hạn

Triệu chứng: cron chạy song song (vd `knowledge-researcher-4h-rotation` + `KFlow Push
Tâm lý` 30 phút/lần) đụng nhau → job fail:
```
RuntimeError: HTTP 429: TPM (Tokens Per Minute) limit of the model deepseek-v4-flash-ga is exceeded.
```
→ Token free BytePlus KHÔNG vô hạn: vượt ngưỡng tokens/phút là 429, retry không cứu
nếu load liên tục. Chiến lược: đẩy cron nhẹ về model local (unsloth) để giữ quota
ByteDance cho chat chính + job research nặng; đừng trông cậy ByteDance gánh mọi thứ.


---

## PITFALL — Key provider "exhausted" trong credential pool: chẩn đoán 429 + đổi MODEL thay vì account mới (case BytePlus 2026-09-08)

Triệu chứng user: "mất 21 triệu input", "retry liên tục", "chưa làm được gì đã hết token". System vẫn chạy nhưng mọi thứ rơi vào fallback chain vì key chính chết.

**Chẩn đoán 4 bước (theo thứ tự, đều đọc file, không đoán):**
1. **auth.json → credential_pool** — đọc `last_status` + `last_error_code` của TỪNG provider:
   ```python
   import json; d=json.load(open(r'C:\Users\NTQUANG_DELL\AppData\Local\hermes\auth.json',encoding='utf-8'))
   for prov, ents in d['credential_pool'].items():
       for e in ents: print(prov, e.get('last_status'), e.get('last_error_code'), e.get('last_error_reason'))
   ```
   `last_status: "exhausted"` + `429` = key chết vì rate limit/quota; `401` = key sai/hết hạn. Đo thật 08/09: bytedance 429 exhausted + opencode-zen 401 exhausted cùng lúc → cả primary lẫn fallback đều chết.
   **PHÂN BIỆT 429 vs 401 (đo 2026-09-14):** 429 TPM là TẠM THỜI (reset theo phút) —
   key CHƯA chết, nhưng pool đánh dấu exhausted làm Hermes NÉ primary ngay tick sau →
   mọi request rơi vào fallback → user tưởng "provider bị reset/đổi" dù config đúng.
   Fix nhanh: backup auth.json, xóa `last_status`/`last_error_code`/`last_error_reason`
   của entry bytedance → Hermes thử lại ngay, KHÔNG cần đổi model/account. Chỉ 401/402
   mới là key chết thật (đừng reset những code đó).
2. **state.db usage** (skill `hermes-usage-stats`): input tokens theo ngày/model — xác nhận mức đốt thật (vd 16.9M/ngày + 5.1M = đúng "21M" user thấy, không phải bug).
3. **config.yaml**: `model.default`, `agent.api_max_retries`, `providers.<name>.stale_timeout_seconds`/`ttfb_timeout_seconds`.
4. **Hermes retry KHÔNG nóng** — verify `agent/retry_utils.py`: jittered backoff chuẩn (base 5s → max 120s, jitter 0.5). Nhưng **mỗi lần retry = gửi lại FULL context** (50-150K tokens) → retry là nguồn đốt input chính khi provider chết.

**Fix ưu tiên — đổi model trước, account mới sau:** BytePlus limit theo ACCOUNT+MODEL → model GA bị 429 KHÔNG kéo model khác trên CÙNG key (vd `deepseek-v4-flash-260425` 15K RPM/1.5M TPM vs GA 500 RPM/1M TPM, xem reference). Đổi `model.default` + giảm retry trước khi bắt user tạo account mới:
```bash
hermes config set model.default deepseek-v4-flash-260425
hermes config set agent.api_max_retries 2   # 3→2 cắt ~25% input đốt khi provider chết
```
Verify: `python -c "import yaml;c=yaml.safe_load(open(r'<home>/config.yaml',encoding='utf-8'));print(c['model']['default'], c['agent']['api_max_retries'])"`.
Lưu ý: config đổi chỉ áp dụng session MỚI (session đang chạy giữ model cũ trong prompt cache).


---

## PITFALL — Cron "unsloth" chạy ra model KHÁC: endpoint local chết + credential pool trỏ sai → fallback im lặng

Cron job để `provider: unsloth, model: unsloth/Ministral-3-8B-Instruct-2512-GGUF`
nhưng output thực tế là deepseek/nemotron (opencode-zen/bytedance) — user tưởng chạy
local. Đo thật 2026-09: **unsloth "local" thật sự nằm trên tunnel
`https://pharma-llm.thefirstonly.com/v1`** (có `UNSLOTH_API_KEY`), KHÔNG phải
`127.0.0.1:18888` — nhưng credential pool `custom:unsloth` trong `auth.json` vẫn trỏ
`http://127.0.0.1:18888` (chết). Hermes resolve base_url từ credential pool → request
fail → rơi vào fallback chain → session ghi `provider=opencode-zen/bytedance` dù job
cấu hình unsloth.

**Chẩn đoán — 2 chỗ kiểm tra:**
1. `python` đọc `auth.json` → `credential_pool['custom:unsloth'][0]['base_url']` có phải địa chỉ chết?
2. Session thực tế của cron: `SELECT billing_provider FROM sessions WHERE id LIKE 'cron_%' ORDER BY started_at DESC` → provider KHÁC provider job = fallback im lặng.

**Fix — sửa CẢ HAI nơi:**
1. `hermes config set providers.unsloth.base_url "https://pharma-llm.thefirstonly.com/v1"` (config provider).
2. Sửa trực tiếp `auth.json` credential_pool `custom:unsloth[].base_url` → cùng URL
   (`hermes auth add --inference-url` KHÔNG ăn cho custom provider — chỉ dành Nous portal).
3. Test xuyên suốt: curl trực tiếp tunnel (`/v1/chat/completions` + `User-Agent: curl/8.0`,
   vì `OpenAI/Python` UA bị chặn 403 — xem pitfall UA-block) → OK, rồi
   `hermes chat -q "..." --model unsloth/Ministral-... --provider unsloth` → check
   session mới nhất trong state.db ghi đúng provider.

Cùng chủ đề: provider "unsloth" KHÔNG có trong `hermes model list` picker — nó không
phải plugin model-provider riêng; test `--provider unsloth` dễ rơi về default. Muốn
verify thật phải đọc `billing_provider` session, không tin reply text.


---

## PITFALL — Lỗi 402 OpenRouter (`z-ai/glm-5.2` hết credit) dù config KHÔNG dùng OpenRouter: nguồn là MOA aggregator

Triệu chứng (2026-09-11): user báo "Anh có dùng openrouter đâu" — request_dump cho
session Telegram ghi `model=z-ai/glm-5.2`, `url=https://openrouter.ai/api/v1/chat/completions`,
HTTP 402 "requires more credits". Nhưng `fallback_providers` trong config KHÔNG có
openrouter — tra không ra nguồn.

**Nguồn thật: MOA (Mixture of Agents) đang enabled.** Khi desktop app ghi đè config
bản cũ, `moa.enabled: true` được khôi phục với `aggregator.provider: openrouter` +
`reference_models` chứa openrouter → Hermes gọi OpenRouter cho aggregator/reference
dù fallback chain sạch. Tra trong config: `python -c "import yaml; d=yaml.safe_load(open(r'<home>/config.yaml',encoding='utf-8')); print(d.get('moa'))"`.

**Fix (3 chỗ, làm cùng lúc):**
1. `moa.enabled: false`
2. `moa.aggregator` → đổi provider openrouter → bytedance (hoặc provider đang dùng)
3. Mọi `moa.reference_models[].provider == openrouter` → `enabled: false`
Sửa qua python yaml dump (patch tool chặn config.yaml), rồi verify
`yaml.safe_load` → `moa.enabled == False`. Config đổi chỉ áp dụng session mới.

### PITFALL — nguồn 402 OpenRouter thứ HAI: `model.fallback_providers` (không chỉ MOA)

Case 2026-10-05: user báo "anh có dùng openrouter đâu" khi Hermes trả
`HTTP 402: This request requires more credits ... for deepseek/deepseek-chat` +
"OpenRouter reported that billing...". `moa.enabled` = false → KHÔNG phải MOA.
Nguồn thật nằm ngay trong **`model.fallback_providers`** — block CON của `model:`,
trùng tên với `fallback_providers` top-level nên rất dễ bỏ sót khi đi tra:

```yaml
model:
  provider: command-code
  fallback_providers:          # ← block con, KHÁC top-level
    - provider: openrouter     # ← 402 khi hết credit OpenRouter
      model: deepseek/deepseek-chat
```

**Thứ tự tra khi thấy 402/403 OpenRouter dù "không dùng OpenRouter":**
1. `model.fallback_providers` (block con `model:` — nghi phạm số 1, hay bị quên)
2. `fallback_providers` (top-level)
3. `moa.aggregator` / `moa.reference_models`
4. `model_aliases.*.provider`

Chốt nhanh bằng 1 dòng python:
```python
import yaml; c = yaml.safe_load(open(r'<home>/config.yaml', encoding='utf-8'))
print(any('openrouter' in str(x) for x in c['model'].get('fallback_providers', [])))
```

**Fix:** thay list con bằng provider đang dùng thật (command-code trước, custom
bytedance sau). Nếu user nói "bỏ openrouter", bỏ ở CẢ 4 chỗ trên, không chỉ 1.

### PITFALL — `hermes fallback add|clear|remove` là INTERACTIVE, KHÔNG script được

`hermes fallback` chỉ có 3 việc dùng được không tương tác: `list`/`ls` (xem chain).
Còn `add` mở **picker chọn provider + model**, `clear` hỏi `[y/N]`, `remove` cũng
picker — truyền thẳng `model --provider` vào là lỗi ngay:

```
hermes fallback add deepseek/deepseek-chat --provider openrouter
→ hermes: error: unrecognized arguments: deepseek/deepseek-chat --provider openrouter
hermes fallback clear
→ Clear all entries? [y/N]:  (treo chờ nhập, hoặc "Cancelled." nếu bị pipe)
```

→ **Muốn set chain theo kịch bản (agent tự làm) thì ghi thẳng config.yaml bằng
python**, đừng gọi CLI `fallback add`. `hermes config set fallback_providers '[...]'`
cũng KHÔNG dùng được (stringify list — xem pitfall Fallback config ở trên). Đúng
nhất: `yaml.safe_load` → gán list → `yaml.safe_dump(cfg, allow_unicode=True,
sort_keys=False)` (patch/write_file bị chặn ghi config.yaml).

### PITFALL — `hermes fallback list` và RUNTIME có thể đọc HAI vị trí KHÁC NHAU

Đo thật 2026-10-05: ghi chain mới vào `model.fallback_providers` rồi chạy
`hermes fallback` → vẫn in chain CŨ (bytedance + command-code), tức khớp đúng
**`fallback_providers` top-level**; còn `hermes chat` lúc đó cũng nhảy fallback
theo chain top-level (`→ stealth/space-bunny-alpha via command-code`). Sau khi xoá
top-level, chain con mới là thứ chạy.

Nguồn code: `hermes_cli/fallback_config.py::get_fallback_chain()` đọc
`config["fallback_providers"]` RỒI MỚI tới legacy `config["fallback_model"]` —
**không hề nhắc `model.fallback_providers`**. Chain này truyền vào
`agent/agent_init.py:1401` để dựng `agent._fallback_chain`.

**CHỐT (verify lại toàn bộ source 2026-10-05, loại venv/tests):** KHÔNG một dòng
Python nào đọc `model.fallback_providers`. Nó là **CONFIG CHẾT** — Hermes im lặng
bỏ qua, không cảnh báo. `hermes fallback ls`, runtime, và `get_fallback_chain()`
đều chỉ đọc top-level; kiểm chứng bằng cách đặt hai giá trị KHÁC NHAU ở hai vị trí
rồi so kết quả (top-level thắng tuyệt đối, con bị bỏ hoàn toàn). Sửa lại kết luận
cũ trong file này: **chain chỉ có MỘT nguồn sự thật — `fallback_providers`
top-level** (legacy: `fallback_model`). `model.fallback_providers` KHÔNG phải
nguồn thứ hai.

Block con này thường mang thêm field lạ `max_retries` (không có trong schema docs
và cũng không được parse) — dấu hiệu nhận biết nhanh là config rác, không phải chain
thật. Đo thật: list con tự đổi giá trị giữa các lần đọc khi Desktop app đang chạy
(từng thấy `stealth/space-bunny-alpha`, `poolside/laguna-s-2.1-free` xuất hiện rồi
biến mất) → nghi phạm ghi nó là UI/app, nhưng **dù ai ghi thì engine vẫn không đọc**.
Đừng tốn thời gian truy nguồn ghi trước khi xác nhận engine bỏ qua nó.

**Luật chẩn đoán: `hermes fallback ls` là nguồn chân lý.** Chain chạy khác chain
hiển thị → gần như chắc chắn còn sót block `model.fallback_providers` gây rối. Đọc
cả hai để phát hiện, nhưng **xoá vị trí CHẾT, không xoá top-level:**

```python
import yaml, json
c = yaml.safe_load(open(r'<home>/config.yaml', encoding='utf-8'))
print("top-level (THẬT):", json.dumps(c.get('fallback_providers'), ensure_ascii=False))
print("model.*  (CHẾT):", json.dumps(c.get('model', {}).get('fallback_providers'), ensure_ascii=False))
print("legacy          :", repr(c.get('fallback_model')))
```

Trước khi bàn giao, giữ **đúng một nguồn sự thật**: xoá block con
(`del c["model"]["fallback_providers"]`) — ⚠️ TUYỆT ĐỐI KHÔNG xoá
`c["fallback_providers"]`, đó chính là chain thật. Verify bằng `hermes fallback ls`
(phải khớp số entry mong đợi) rồi `hermes chat -q "..."`: im lặng = primary tự trả
lời, đúng như mong đợi.

### PITFALL — model sống ≠ provider dùng được: probe TỪNG HOP của chain

Đo thật 2026-10-05, cùng lúc, key đều có trong `.env`:

| Hop | Kết quả |
|---|---|
| `opencode-zen` + `deepseek-v4-flash` | `402 Insufficient account funds` |
| `opencode-zen` + bất kỳ `*-free` | `403 FreeTierError: ...free tier can only be used from within OpenCode` |
| `opencode-go` + `deepseek-v4-flash` | `403 An active OpenCode Go subscription is required` |
| `custom:ark...` / `deepseek-v4-flash-260425` | `429 AccountQuotaExceeded` (kèm ngày reset) |
| `openrouter`, `gemini-flash-latest`, Groq `openai/gpt-oss-120b` | `OK` |

→ **`opencode-zen` / `opencode-go` KHÔNG dùng được làm hop trong Hermes** dù
`OPENCODE_ZEN_API_KEY` / `OPENCODE_GO_API_KEY` có sẵn trong `.env`: free tier gắn với
app OpenCode, Go cần subscription riêng. **Key tồn tại KHÔNG có nghĩa gọi được** — và
`/v1/models` trả 403 trong khi lỗi thật chỉ lộ ở `/chat/completions`.
→ **Bắt buộc smoke test TỪNG hop** (`scripts/smoke_fallback_chain.py`): chain đẹp
trong config vẫn có thể 0 hop sống.

**Model id cũng bị gỡ theo thời gian:** `gemini-2.5-flash` → `404 no longer available
to new users` (VĨNH VIỄN cho account mới) trong khi `gemini-flash-latest` → `OK`;
`gemini-3-flash-preview` → `503 high demand` (TẠM THỜI, đừng loại vĩnh viễn). → Ưu
tiên alias `-latest` trong chain dài hạn, probe lại id trước khi ghi config.

Chi tiết + bảng đầy đủ + chain chốt → `references/fallback-chain-hygiene-2026-10.md`.

### PITFALL — quét block YAML theo dòng: sequence cùng indent với key cha → cắt hụt, phá config

Bẫy mới, khác bẫy regex `(?s)` ở trên. YAML cho phép sequence item **thụt ĐÚNG BẰNG
key cha**, và `model.fallback_providers` được ghi đúng kiểu đó:

```yaml
model:
  fallback_providers:        # key cha, indent 2
  - provider: command-code   # item CŨNG indent 2 (không phải 4!)
    model: deepseek/deepseek-v4-flash
```

Hàm dò kiểu `end = dòng đầu tiên có indent <= parent_indent` → dừng NGAY ở item đầu
→ chỉ xoá được 1 dòng, các item còn lại mồ côi → `yaml.safe_load` chết
(`expected <block end>, but found '-'`). Đã xảy ra thật, phải restore từ backup.

**Điều kiện dừng ĐÚNG:** bỏ qua dòng trống; dừng ở dòng KHÔNG trống, **không bắt đầu
bằng `- `**, và có indent `<= parent_indent`.

```python
def block_end(lines, start, parent_indent):
    j = start + 1
    while j < len(lines):
        b = lines[j].rstrip("\r")
        if not b.strip():
            j += 1; continue
        s = b.lstrip(" ")
        ind = len(b) - len(s)
        if ind <= parent_indent and not s.startswith("- "):
            return j
        j += 1
    return len(lines)
```

Quy trình an toàn bắt buộc khi sửa block YAML trong config.yaml:
1. `cp config.yaml config.yaml.bak-<ts>` TRƯỚC.
2. **`raise`/`sys.exit` TRƯỚC khi ghi** nếu anchor không khớp hoặc không duy nhất
   (đếm anchor: `sum(1 for l in lines if l.rstrip()=="  fallback_providers:")`).
3. Ghi xong → `yaml.safe_load` lại NGAY. Fail → `cp <backup> config.yaml` ngay lập tức.
4. Verify chức năng bằng `hermes fallback ls`, không chỉ YAML parse.

Ghi kèm `newline=""` và giữ `\r` của từng dòng để không đổi CRLF→LF cả file.

### PITFALL — `hermes config set` GHI LẠI TOÀN BỘ config.yaml (mất comment, thêm default)

Ngoài việc biến list thành string (mục "Fallback config — PITFALL NGHIÊM TRỌNG"),
`hermes config set <bất kỳ key>` còn **normalize cả file**. Đo thật 2026-10-05:
`hermes config set model.fallback_providers '[...]'` làm config từ **24.991 bytes /
926 dòng → 23.606 bytes / 886 dòng**: comment bị bỏ, key default chưa có được chèn
thêm (`agent.personalities`, `agent.environment_hint`, `agent.coding_context`...).
User phản ứng khi thấy file khác bản gốc.

→ **Luôn `cp config.yaml config.yaml.bak-<ts>` TRƯỚC khi `config set`.** Nếu file
user tự sắp xếp / có comment quan trọng → **dùng text-line patch**, không `config set`.

Recovery đã chạy thật (khi `config set` vừa stringify vừa normalize):
1. `cp config.yaml.bak-<ts> config.yaml` — về bản gốc.
2. Thay block theo DÒNG bằng python, giữ nguyên phần còn lại:
   ```python
   # tìm start = dòng '  fallback_providers:' (2 space, không phải top-level)
   # end = dòng đầu tiên không còn thụt '    -'/'      '
   out = lines[:start] + new_block + lines[end:]
   open(path, "w", encoding="utf-8", newline="").write("\n".join(out))
   ```
3. Verify: `yaml.safe_load` parse OK + `wc -l` khớp kỳ vọng (926 - 9 = 917) +
   `any('openrouter' ...)` = False.
Lưu ý `patch`/`write_file` CHẶN ghi config.yaml → phải đi qua python trong terminal
(thao tác này cần user approve).


---

## PITFALL — `model.provider: custom:<host>` là BASE_URL TRỰC TIẾP, KHÔNG lookup custom_providers

**Đây là lý do sửa `custom_providers` cả buổi mà Hermes vẫn gọi thẳng endpoint cũ.** Đo thật
2026-09 (Mac + pharma-llm.thefirstonly.com): khi `model.default.provider` có dạng
`custom:pharma-llm.thefirstonly.com`, Hermes hiểu cụm **sau dấu `:` chính là base_url trực
tiếp** và gọi thẳng host đó, **KHÔNG đọc** entry `custom_providers[].base_url` dù tên entry
giống hệt. Vì vậy đổi base_url trong entry `custom_providers` (dù đúng) không có tác dụng
cho model default — request vẫn gửi tới host cũ.

Dấu hiệu nhìn thấy: trong `~/.hermes/sessions/request_dump_*.json`, dòng `"url"` sau khi
restart vẫn ghi `https://pharma-llm.thefirstonly.com/v1/chat/completions` dù config đã đổi
điểm vào → chứng minh Hermes chưa bao giờ dùng entry custom_providers.

**Fix — sửa MODEL BLOCK (không phải custom_providers):**
```yaml
model:
  default: unsloth/Ministral-3-8B-Instruct-2512-GGUF
  provider: custom            # ← bỏ phần ":<host>"
  base_url: http://127.0.0.1:18888   # ← proxy/endpoint đích, KHÔNG /v1
  api_key: sk-...
```
Chuẩn nhất qua `hermes config set` (xử lý đúng cấu trúc, không phá indent):
```bash
hermes config set model.provider custom
hermes config set model.base_url "http://127.0.0.1:18888"
hermes config set --force model.api_key "$KEY"
```
Và **restart Hermes bắt buộc** — process `serve` giữ config cũ trong bộ nhớ; đổi config riêng
vô tác dụng (không hot-reload). Nhận biết config chưa được đọc lại: request_dump/agent.log
vẫn ghi URL cũ.

Cùng insight cho alias: chỉ sửa `custom_providers` khi bạn trỏ vào một entry CĨ name riêng
và gọi bằng `--provider <tên>`; nhưng với model default, cứ handle trực tiếp qua model block.

PITFALL phụ — **macOS sed khác GNU:** `sed -i.bak3 's/.../\1/' file` trên macOS hiểu
`.bak3` là label → lỗi `sed: 1: "...": undefined label 'quang/.hermes/config.yaml'`.
Không phải syntax lỗi, là BSD sed không có GNU `-i<SUFFIX>`. Dùng `sed -i '' 's/.../' file`
(BSD) hoặc sửa qua python `hermes config set`/script text-line. Tương tự Windows git-bash
sed là GNU nên `-i.bak` chạy — khác biệt platform tiêu diệt script port.


---

## PITFALL — cùng 1 endpoint nhưng API key LỆCH giữa env / custom_providers / watchdog (403 vs 401 vs im lặng)

Khi một endpoint Unsloth/tunnel xuất hiện ở nhiều nơi config (xem mục trước), nó
còn mang theo **nhiều bản API key** có thể KHÁC nhau — mỗi nơi một key. Đo thật
2026-09 (pharma-llm.thefirstonly.com): env `$UNSLOTH_API_KEY` = `sk-uns...4815`
(đúng, call 200), còn key trong entry `custom_providers[].api_key` = `sk-uns...b8a9`
(invalid, call `HTTP 401 Invalid or expired API key`), còn watchdog script hardcode
key thứ ba. Kết quả: **curl với env key = 200, Hermes (đọc key config) = fail** —
trông như base_url sai nhưng thật ra key sai.

**Chẩn đoán — test TỪNG key độc lập, đừng đoán:**
```bash
# env key
curl -s -o /dev/null -w "%{http_code}\n" -H "Authorization: Bearer $UNSLOTH_API_KEY" \
  -H "Content-Type: application/json" -d @body.json <base>/v1/chat/completions
# key trong config entry (dòng api_key) — đọc qua python yaml, không qua grep
CFGKEY=$(python -c "import yaml;print(yaml.safe_load(open('.../config.yaml'))['custom_providers'][0]['api_key'])")
curl -s -o /dev/null -w "%{http_code}\n" -H "Authorization: Bearer $CFGKEY" \
  -H "Content-Type: application/json" -d @body.json <base>/v1/chat/completions
```
`200` (env) vs `401` (config key) → chốt key lệch, không phải base_url sai.

**Fix — thống nhất 1 nguồn key duy nhất là `${ENV}`**, KHÔNG hardcode ở bất kỳ chỗ nào:
1. Entry `custom_providers[].api_key` → dùng `${UNSLOTH_API_KEY}` (Hermes resolve env
   trong config) như `model_aliases` đang làm, thay vì key chuỗi thật.
2. Watchdog script → `KEY = os.environ.get("UNSLOTH_API_KEY","")` (đã sửa đúng cách
   như vậy), không ghi key thật vào script (key sẽ thối theo thời gian).
3. Verify `python watchdog-unsloth.py; echo $?` → stdout rỗng + exit 0.

**Cẩn thận khi đọc key từ config qua shell:** `grep`/`awk` dòng `api_key:` giữ
**leading whitespace** dính vào giá trị → prefix thấy `    sk-unslo`. Strip
`tr -d ' \t'` trước khi test, và dùng python `yaml.safe_load` (tự bỏ whitespace)
là an toàn nhất. Một key "invalid" do dính space sẽ làm nhiều công đoạn chẩn đoán sai.


---

## PITFALL — cron chết IM LẶNG khi tunnel/provider local tạm tắt → cần watchdog

Model local sau tunnel (trycloudflare) hay endpoint LAN không ổn định: khi tunnel
rớt, cron job dùng provider đó **fail im lặng** (không deliver, không tự báo) —
user chỉ phát hiện khi không nhận bài. Các job chạy gateway đều phụ thuộc 1 URL
tunnel tạm (`*.trycloudflare.com` đổi mỗi lần server restart).

**Giải pháp — cron watchdog `no_agent`:** script tự probe endpoint `/v1/models`
bằng `urllib`/`requests`, `print` RỖNG khi OK (im lặng → cron không deliver) và
`print` cảnh báo rõ khi endpoint chết (→ cron gửi cảnh báo vào chat). Cre thức:
một watchdog no_agent với stdout rỗng = không có gì gửi đi, stdout có text =
cảnh báo tới chat. Mẫu ở `~/AppData/Local/hermes/scripts/watchdog-unsloth.py`.
Khởi tạo cron `every 30m`, no_agent=true, deliver=origin, widget:
`cronjob(action=create, no_agent=true, script="watchdog-unsloth.py", schedule="every 30m", deliver="origin")`.
**LƯU Ý:** khi URL tunnel đổi, phải update CẢ config lẫn watchdog script — 2 khối,
đừng bỏ sót. Và **một endpoint Unsloth/tunnel xuất hiện ở NHIỀU vị trí config**
(đo thật 2026-09, máy mở rộng pharma-llm.thefirstonly.com): `auxiliary.vision.base_url`,
entry `custom_providers[].base_url`, VÀ `model_aliases.*.base_url` (alias
unsloth-qwen/unsloth-min). Sửa sót 1 chỗ → job đó vẫn trỏ endpoint chết dù phần khác đã OK.

**Trước khi khởi động lại đổi endpoint, dọn đồng bộ đầy đủ:**
1. `grep -nE "base_url" <config>` — liệt kê MỌI nơi trỏ endpoint cũ.
2. `grep -niE "trycloudflare|racial-clarke|<endpoint-cũ>" <config>` — tìm sót dấu vết cũ.
3. `hermes config set` cho key NHẬN DIỆN được (`auxiliary.vision.base_url` OK).
   Key KHÔNG nhận diện (`model_aliases.*.base_url`) → báo "not a recognized config
   key — it was saved anyway"; thêm `--force` để bỏ warning, hoặc sửa qua python
   `load_config/save_config`. **patch tool CHẶN ghi config.yaml** (security-sensitive).
4. Update watchdog script tương ứng.
5. Verify script: `python watchdog-unsloth.py; echo $?` — stdout rỗng + exit 0 = OK.


---

## PITFALL — cùng 1 endpoint Unsloth/tunnel trên NHIỀU Hermes host — phải đồng bộ từng máy

Một endpoint chia sẻ (`pharma-llm.thefirstonly.com`) không chỉ xuất hiện ở nhiều vị trí
trong 1 config (`auxiliary.vision.base_url`, `custom_providers`, `model_aliases` — xem
mục cron im lặng) mà còn **trên nhiều Hermes host riêng biệt**: máy làm việc (Windows) +
máy Mac chạy cron tâm lý (`/Users/tquang/.hermes`). **Fix config máy này KHÔNG đụng máy
kia.** Nếu user báo "Hermes <máy khác> vẫn 403/401/4096" mà chỉ sửa máy đang ngồi → lặp
đúng cụm lỗi trên host kia.

Chẩn đoán nhanh: hỏi user *chỉ một máy hay tất cả Hermes host* bị lỗi; mở log host đích
(`~/AppData/Local/hermes/config.yaml` mỗi máy) để xem base_url trỏ đâu.

Quản lý host từ xa trên LAN qua SSH/paramiko (tìm IP bằng ARP + scan port 22, deploy
proxy, sửa base_url/context_length, verify YAML bằng hermes venv vì system python3 3.9
thiếu yaml), lưu ý đổi config bắt buộc restart Hermes host đích mới có hiệu lực; cách
restart Hermes **Desktop app** từ xa (`osascript quit` + `pkill hermes_cli.main serve` +
`open` bundle) đã đo thành công → `references/remote-hermes-host-config-2026-09.md`.


---

## Quy tắc model router cho workflow (từ quyết định 2026-08)

Tách theo nhu cầu reasoning, không theo "local vs API" cứng:
- **Nặng** (research sâu + citation, legal, code phức tạp, orchestration) → API strong (deepseek-v4-pro). KHÔNG local.
- **Nhẹ** (tóm tắt raw, format, tiêu đề, dialog ngắn) → local ngựa thồ NẾU đủ VRAM + không reasoning + Q4; else API rẻ.
- **Cơ học** (watchdog, STT, move card, format file) → code/script thuần, 0 LLM (nơi cắt token nhiều nhất).
- Rule này đặt trong router/config, không để model tự chọn. Setup bằng tay từng job trước khi auto-route.


---

## OpenCode/DeepSeek endpoint — quirk khi gọi trực tiếp qua API (không qua Hermes)

Khi code gọi `https://opencode.ai/zen/go/v1/chat/completions` trực tiếp
(call_deepseek trong hub/store.py, summarize TFO...), có 4 quirk:

1. **HTTP 200 nhưng content rỗng ~40-80% số lần** với input dài (>~5000 chars tổng).
   Không phải timeout, không phải network. Bắt buộc retry loop khi content rỗng,
   không chỉ khi status != 200.
   **Tỷ lệ rỗng KHÁC NHAU theo model (đo thật 2026-08-07, context 6k):** `deepseek-v4-flash`
   rỗng ~80% (1/5 ok), `deepseek-v4-pro` ổn 100% (5/5 ok). → trước khi kết luận
   "provider chết", benchmark 5 lần mỗi model; dùng pro (hoặc fallback flash→pro)
   cho prompt dài. Benchmark code mẫu → `references/opencode-empty-json-quirks.md`.
2. **`response_format={"type":"json_object"}` → LUÔN trả rỗng.** Bỏ response_format,
   ép JSON bằng prompt: "OUTPUT: CHỈ JSON thuần, bắt đầu bằng {." → model comply.
3. **Tổng prompt (system + input) vượt ngưỡng → rỗng.** Chunk input nhỏ
   (~3500 chars), system prompt NGẮN cho bước trung gian.
4. **Input dài → model trả markdown thay vì JSON.** Xử lý 2 bước: summarize text
   ngắn trước, ép JSON lại trên output ngắn đó (retry 4x, check startswith("{")).
5. **timeout=60 không đủ** cho prompt dài + model lớn → tăng 180.

Chi tiết test + code mẫu + pattern tóm tắt dài → `references/opencode-empty-json-quirks.md`.


---

## PA A — Groq llama là JSON extractor đáng tin khi DeepSeek/OpenCode fail

Khi cần output JSON ổn định (summarize meeting → summary/issues/decisions/tasks),
**ưu tiên gọi Groq llama-3.3-70b-versatile + `response_format={"type":"json_object"}`**
thay vì DeepSeek qua OpenCode:

```python
r = requests.post("https://api.groq.com/openai/v1/chat/completions",
    headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
    json={"model": "llama-3.3-70b-versatile",
          "messages": [...], "temperature": 0.1, "max_tokens": 2500,
          "response_format": {"type": "json_object"}}, timeout=180)
```

Kinh nghiệm thực tế (08/2026, TFO summarize):
- Groq trả JSON chuẩn **ngay lần đầu**, không bao giờ trả rỗng → không cần retry loop.
- Điều kiện: input nên NGẮN (~<8000 chars). Với transcript dài → chunk-summarize
  trước bằng DeepSeek flash (giữ số liệu/tên), rồi bước ép JSON cuối giao cho Groq.
- Groq có context rộng hơn DeepSeek qua OpenCode → ít gặp ngưỡng trả rỗng.
- Fallback chain: Groq JSON → (nếu fail) DeepSeek 2 bước (summarize → ép JSON).

Cùng GROQ_API_KEY đang dùng cho Whisper STT → không cần credential mới.


---

## LLM summarize KHÔNG deterministic — chạy 2 lần chọn bản tốt (2026-08, demo meeting note)

Cùng 1 transcript, chạy summarize 2 lần → kết quả KHÁC NHAU: lần 1 ra 2 task đủ assignee+deadline chuẩn, lần 2 ra 4 task, gán sai người ("Gọi cho mẹ → Anh Mão" thay vì Quang), 3/4 thiếu deadline. Đây là bản chất LLM sinh nội dung — không phải bug pipeline.

**Khi output cần ổn định (tasks/issues/decisions cho meeting note), áp dụng:**
1. **Chạy 2 lần** (cùng input, temperature thấp), chọn bản tốt hơn theo heuristic: nhiều task có đủ assignee + deadline hơn, hoặc issue/decision nhiều và có ý nghĩa.
2. **Heuristic sửa lỗi gán người sau LLM:** pattern "gọi mẹ/thuyết phục mẹ" → assignee = Quang (người họp chính), không tin LLM gán ngẫu nhiên.
3. **Deadline fallback:** task thiếu deadline → nếu transcript chứa "chốt sáng thứ 7"/mốc chung → gán mốc đó.
4. Trình user xem DEMO kết quả thật trước khi chốt pipeline (anh Quang yêu cầu "em làm demo trước, được thì mới chốt") — không báo "xong" dựa trên 1 lần chạy may mắn.


---

## Session lifecycle — session bị reset theo daily schedule / inactivity

**Triệu chứng:** user vào Telegram/Discord thấy context mới tinh, system note
"automatically reset by the daily schedule". Mọi context cũ biến mất.

**Nguyên nhân gốc:** `restart_after_turn_timeout` trong config.yaml — mặc định
21600 giây (6 tiếng). Nếu user không nhắn gì trong 6h+ giữa các turn, Hermes tự
reset session. Các job cron chạy trong khoảng lặng đó không cứu được — timeout
tính theo turn gap, không tính cron activity.

**Các tham số liên quan trong config (agent section):**
- `restart_after_turn_timeout: 21600` — **thủ phạm chính.** 21600s = 6h không
  nhắn → session reset. Set 0 để tắt hẳn (không bao giờ auto reset), hoặc tăng
  lên 86400 (24h) / 172800 (48h).
- `session_stall_timeout: 300` — timeout 5 phút cho stall, KHÔNG reset session.
- `gateway_timeout: 1800` — gateway timeout (30 phút), KHÔNG reset session.

**Kiểm tra nhanh:**
```bash
hermes config get agent.restart_after_turn_timeout
# → 21600 (6h) = đang bật
```

**Fix — 3 lựa chọn:**
1. **Tắt hẳn** (không bao giờ auto reset):
   ```bash
   hermes config set agent.restart_after_turn_timeout 0
   ```
2. **Tăng lên 24h:**
   ```bash
   hermes config set agent.restart_after_turn_timeout 86400
   ```
3. **Tăng lên 48h:**
   ```bash
   hermes config set agent.restart_after_turn_timeout 172800
   ```

**Lưu ý quan trọng:**
- Đổi config chỉ áp dụng cho **session mới** (`/new`) — session đang chạy giữ
  giá trị cũ vì nó nằm trong prompt cache.
- Nếu Hermes Desktop app đang chạy, nó có thể **revert config sau ~6s** (xem
  pitfall Desktop revert ở trên). Cần restart Desktop app để config mới có hiệu
  lực, hoặc kill Desktop an toàn (xem section kill an toàn ở trên).
- Config guard (`config_guard.py`) nếu đang chạy có thể giữ giá trị cũ trong
  golden snapshot → phải update golden của guard sau khi đổi.

**Theo docs chính thức:** gateway conversations KHÔNG reset sau inactivity hoặc
daily boundary. `restart_after_turn_timeout` là cơ chế cleanup cho cached agent
instance (giải phóng tài nguyên), không phải session reset — nhưng trên thực tế
nó gây reset session cho messaging platform. Set 0 để đúng behavior docs.
