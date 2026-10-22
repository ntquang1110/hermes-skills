# Fallback chain hygiene + `model.fallback_providers` là config CHẾT (2026-10-05)

Case: user hỏi *"làm sao để khi apply model trong Hermes desktop thì các session sẽ
apply, hoặc khi hết limit thì tự fallback?"* — và tưởng mình đang có chain 3 entry.
Sự thật: chain hiệu lực chỉ **1 entry**, 3 entry kia nằm ở vị trí engine **không đọc**.

## 1. Chốt bằng source: chỉ TOP-LEVEL được đọc

Khảo sát toàn bộ `hermes-agent/**/*.py` (loại `venv/`, `tests/`) — mọi tham chiếu
`fallback_providers` đều là top-level:

| Nơi | Vai trò |
|---|---|
| `hermes_cli/fallback_config.py:80` `get_fallback_chain()` | đọc `config["fallback_providers"]` rồi `config["fallback_model"]`. **Không nhắc `model.fallback_providers`.** |
| `agent/agent_init.py:1401` | nhận `fallback_model`, dựng `agent._fallback_chain`; `isinstance(..., list)` mới nhận |
| `hermes_cli/config_defaults.py:10` | default `"fallback_providers": []` (top-level) |
| `hermes_cli/fallback_cmd.py:44` | `config["fallback_providers"] = chain` khi ghi |
| `gateway/run.py:8281` | merge top-level + legacy để agent create/reuse |

Grep cho truy cập lồng (`model.*fallback_providers`, `["model"].get("fallback`) →
**0 kết quả**. Kết luận: `model.fallback_providers` là config chết, engine bỏ qua im
lặng.

### Kiểm chứng chức năng (không chỉ đọc code)

```bash
hermes fallback ls     # nguồn chân lý: in chain engine THẬT SỰ dùng
```

Trước khi sửa: `Fallback chain (1 entry): deepseek-v4-flash-260425 (via custom:ark...)`
— dù config có 3 entry ở block con. Sau khi chuyển sang top-level: hiện đủ số entry
mới. Thêm một lớp xác nhận bằng chính hàm runtime:

```python
import sys; sys.path.insert(0, "<HERMES_HOME>/hermes-agent")
from hermes_cli.fallback_config import get_fallback_chain
print(get_fallback_chain(cfg))   # phải khớp `hermes fallback ls`
```

## 2. Block con trông như thế nào (dấu hiệu nhận biết)

```yaml
model:
  default: deepseek/deepseek-v4-flash
  provider: command-code
  fallback_providers:                    # ← block CON của model:, KHÔNG được đọc
  - provider: command-code               # ← item cùng indent với key cha (bẫy quét dòng)
    model: deepseek/deepseek-v4-flash
    max_retries: 2                       # ← field lạ, không nằm trong schema docs
  - provider: command-code
    model: meta/muse-spark-1.3-contributor
    max_retries: 2
```

Hai dấu hiệu: (a) `max_retries` trong entry fallback — không được parse ở đâu cả
(chỉ `kanban` có `max_retries` riêng); (b) giá trị **tự đổi giữa các lần đọc** khi
Desktop app đang chạy — quan sát thật trong case này: list con lần lượt chứa
`meta/muse-spark-1.3-contributor` → rồi `stealth/space-bunny-alpha` +
`poolside/laguna-s-2.1-free`. Nghi phạm ghi là UI/app, nhưng **không cần truy nguồn
trước khi xử lý** — dù ai ghi, engine vẫn không đọc.

Hệ quả độc hại: entry toàn `provider: command-code` — **cùng provider với primary**.
Dù có đọc được thì một 429 của command-code cũng kéo chết cả chain. Chain đúng phải
KHÁC provider giữa các hop.

## 3. Smoke test từng hop — kết quả thật

Chạy `scripts/smoke_fallback_chain.py` (1 token/hop). Bảng đo 2026-10-05:

| Hop | Kết quả | Ghi chú |
|---|---|---|
| `opencode-zen` / `deepseek-v4-flash` | `402 Insufficient account funds` | hết tiền |
| `opencode-zen` / `mimo-v2.5-free`, `nemotron-3.5-lightning-free`, `jev-1.13-free` | `403 FreeTierError: OpenCode's free tier can only be used from within OpenCode` | free tier khóa ngoài app |
| `opencode-go` / `deepseek-v4-flash` | `403 An active OpenCode Go subscription is required` | cần sub riêng |
| `custom:ark...` / `deepseek-v4-flash-260425` | `429 AccountQuotaExceeded ... reset at 2026-10-08` | quota tháng, tự hồi |
| `openrouter` / `deepseek/deepseek-v4-flash` | `OK` | ✅ |
| `gemini` / `gemini-flash-latest` | `OK` | ✅ |
| `gemini` / `gemini-2.5-flash` | `404 no longer available to new users` | id đã bị gỡ |
| `gemini` / `gemini-3-flash-preview` | `503 high demand` | tạm thời |
| `custom` (Groq) / `openai/gpt-oss-120b` | `OK` | ✅ |

Chain chốt (cross-provider, xếp live trước, dead/hồi-phục sau):

```yaml
fallback_providers:
  - provider: openrouter
    model: deepseek/deepseek-v4-flash          # cùng họ với primary -> hành vi agent ổn định
  - provider: gemini
    model: gemini-flash-latest                 # khác hạ tầng
  - provider: custom
    model: openai/gpt-oss-120b                 # Groq: dùng dạng custom+base_url vì an toàn hơn
    base_url: https://api.groq.com/openai/v1
    key_env: GROQ_API_KEY
  - provider: custom:ark.ap-southeast.bytepluses.com
    model: deepseek-v4-flash-260425            # quota reset 08/10 -> để cuối
```

Lưu ý Groq: có trong `_MODELS_DEV_PREFERRED` (`hermes_cli/models.py`) nên
`provider: groq` cũng chạy, nhưng dạng `custom` + `base_url` + `key_env` là dạng docs
bless chắc chắn nhất → dùng nó. Không đưa `opencode-zen`/`opencode-go` vào chain dù
key `.env` có sẵn: key tồn tại ≠ gọi được.

## 4. Bẫy quét block theo dòng: sequence cùng indent với key cha

`model.fallback_providers` được ghi với item **cùng indent** (2) với key cha:

```yaml
  fallback_providers:        # indent 2
  - provider: command-code   # indent 2, không phải 4
```

Hàm dò `end = dòng đầu tiên có indent <= parent_indent` → dừng ngay tại item đầu →
chỉ xoá 1 dòng, các item còn lại mồ côi → `yaml.safe_load` chết:

```
yaml.parser.ParserError: expected <block end>, but found '-'
  in "config.yaml", line 5, column 3
```

Đã xảy ra thật và phải restore backup. Vì file chỉ bị hỏng SAU khi ghi, phải luôn có
backup trước + verify YAML sau + đường lùi tức thì:

```bash
cp -f config.yaml.bak-<ts> config.yaml && \
python -c "import io,yaml;yaml.safe_load(io.open(r'<cfg>',encoding='utf-8'));print('RESTORED OK')"
```

Điều kiện dừng đúng (chạy được, đã dùng):

```python
def block_end(lines, start, parent_indent):
    j = start + 1
    while j < len(lines):
        b = lines[j].rstrip("\r")
        if not b.strip():
            j += 1; continue
        s = b.lstrip(" ")
        if (len(b) - len(s)) <= parent_indent and not s.startswith("- "):
            return j
        j += 1
    return len(lines)
```

Ghi file giữ `\r` của từng dòng + `newline=""` để không biến CRLF thành LF cả file.
Đếm anchor trước khi sửa để chắc khớp duy nhất:

```python
n = sum(1 for l in lines if l.rstrip("\r") == "  fallback_providers:")
assert n == 1, n
```

## 5. Semantics của fallback (từ docs chính thức, để trả lời user cho đúng)

- Trigger: 429 (sau khi hết retry), 5xx (sau retry), 401/403 (**ngay**), 404 (**ngay**),
  response rỗng/malformed.
- **Turn-scoped:** mỗi message mới khôi phục primary; trong 1 turn activate tối đa
  **1 lần** — tránh cascade loop.
- Rate-limit aware: provider báo reset time → primary bị bench tới đúng lúc đó;
  không báo → backoff 60s → 4h. Tinh chỉnh `fallback.min_switch_reset_seconds`
  (0 = luôn switch).
- Giá phải trả: mỗi lần switch phá prompt cache → request kế đọc lại TOÀN BỘ history
  giá full. Session dài nhảy qua nhảy lại tốn hơn hẳn.
- Cron **unpinned** thừa hưởng chain; cron pin provider/model riêng thì **không**.
- Auxiliary `provider: auto` cũng đi qua chain này.

## 6. Model apply trong Desktop — phạm vi (câu hỏi gốc của user)

- Desktop Settings → Model → Change → Switch ghi `model.provider` + `model.default`
  → **chỉ áp dụng cho session MỚI**. Chat tab đang mở giữ model cũ. Muốn chúng ăn
  theo: `/new` (hay `/reset`) từng chat, hoặc restart gateway.
- Trong 1 chat: composer picker / `/model <x>` = session-scoped; `--global` mới persist.
- Cron unpinned ăn model global ở lần chạy kế; cron pin riêng thì không.
- Bug đã biết: desktop picker có lúc ghi thẳng vào global config thay vì session
  (issue #56058), và live session giữ override cũ không có surface list/clear
  (issue #102658) → đừng kỳ vọng "đổi 1 chat thôi".
- **Field "Fallback Models" trong Desktop Settings trỏ top-level
  `fallback_providers`** (i18n bundle: section `model` khai báo key
  `fallback_providers`) — nhưng vì đã thấy block con `model.fallback_providers`
  sinh ra và tự đổi giá trị, **khuyên user đừng set fallback qua UI; để agent ghi
  top-level** rồi verify bằng `hermes fallback ls`.

## 7. Gotcha phụ đã gặp trong case này

- `hermes config set plugins.disabled '[]'` → ghi **string** `'[]'` (không parse
  JSON). Key không nhận diện thì báo "not a recognized config key — saved anyway".
  Với list: sửa bằng python, đừng `config set`.
- `patch` / `write_file` **từ chối** ghi `config.yaml` ("Refusing to write to Hermes
  config file"). Phải đi qua terminal + python (cần user approve) hoặc `hermes config`.
- Hermes **tự normalize** config.yaml: sắp lại top-level key theo alphabet và **xoá
  comment**. Nên đừng tin "file bị đổi" là do ai phá — engine tự viết lại. Muốn giữ
  comment/thứ tự thì text-line patch và chấp nhận nó có thể bị normalize sau đó.
- `hermes plugins remove <name>` có thể fail giữa đường trên `.git/objects/pack/*.idx`
  (`PermissionError: [WinError 5]` do read-only) → plugin vẫn `enabled` trong config
  dù folder đã xoá một phần. Fix: `hermes plugins disable <name>` trước (đường chuẩn,
  ghi config), rồi xoá folder bằng python `shutil.rmtree(..., onerror=chmod)`.
