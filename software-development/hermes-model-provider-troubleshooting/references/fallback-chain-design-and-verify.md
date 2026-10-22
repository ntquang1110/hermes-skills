# Thiết kế & verify chuỗi fallback provider (case 18/10/2026)

Case gốc: phiên Telegram nhóm beFounder + 22 cron job chết hàng loạt vì "fallback không áp dụng".
Triệu chứng bề mặt: `hermes fallback list` → *"No fallback providers configured"* dù config có khai báo.

## 1. Bẫy chết người: `hermes config set` ghi LIST thành STRING

`hermes config set fallback_providers '[{"provider":"x","model":"y"}]'` → config.yaml nhận **một chuỗi JSON**
(1 dòng, bọc nháy đơn). Loader không parse string:

- Code thật: `hermes_cli/fallback_config.py` → `get_fallback_chain()` → `_iter_fallback_entries()`
  chỉ nhận `dict` hoặc `list`; `str` → `return []`. Không warning, không log.

⇒ Chuỗi fallback **chết im lặng**. Phát hiện:
```bash
hermes fallback list         # "No fallback providers configured" = chuỗi chết
grep -n -A3 "^fallback_providers" ~/AppData/Local/hermes/config.yaml   # thấy 1 dòng bọc '...' = string
```
Đúng format phải là list YAML thật:
```yaml
fallback_providers:
  - provider: custom:ark-v3
    model: deepseek-v4-1-flash-260910
    base_url: https://ark.ap-southeast.bytepluses.com/api/v3
  - provider: command-code
    model: deepseek/deepseek-v4.1-flash
```
Entry nhận thêm `base_url`, `api_key`, `key_env` (xem `resolve_entry_api_key()`); `agent/agent_init.py`
dùng `explicit_base_url=` + `explicit_api_key=` nên **entry fallback có thể tự khai endpoint/key riêng** —
không cần đăng ký provider mới, nhưng nếu muốn pool exhaustion độc lập thì nên tạo custom provider riêng.

`hermes config set` KHÔNG có flag `--json`/typed (kiểm tra `hermes config set --help`), `hermes fallback add`
là interactive picker (cần TTY). Muốn ghi list bằng script: sửa text YAML trực tiếp rồi `os.replace` (atomic),
kèm retry `PermissionError` 1–2s (config.yaml bị process khác giữ lock tạm thời khi desktop/gateway đọc).

## 2. Luật thiết kế chuỗi

1. **Khác provider VÀ khác bucket quota.** 429 của command-code là *"5-hour usage limit for your plan"* →
   quét sạch mọi hop cùng nhà. Chuỗi cũ (primary + 2 hop đều command-code) chết 100%.
2. **Hermes tự nối thêm model cùng provider** (log: `Fallback activated: deepseek/deepseek-v4.1-flash → moonshotai/Kimi-K3 (command-code)`)
   ⇒ limit theo *plan* giết cả chuỗi dù chỉ khai 1 hop. Đừng tin "nhiều hop = an toàn" nếu cùng nhà.
3. **Khi primary fail, Hermes clear credential pool của primary** (log: `Fallback to X: clearing primary
   credential pool (pool_provider=openrouter)`) ⇒ hop nào **cùng provider với primary** sẽ bị SKIP
   ("no available entries (all exhausted or empty)"). Vì vậy test fallback bằng cách làm hỏng primary
   trên provider khác cũng sẽ cho kết quả sai lệch.
4. **Quota riêng cùng nhà vẫn là hop thật.** ByteDance Ark: `…/api/coding/v3` (subscription) và `…/api/v3`
   (pay-per-token) **cùng key, quota riêng** → coding plan cạn vẫn sống bằng /api/v3. Đây là cách rẻ nhất
   để có redundancy thật: tạo custom provider thứ hai trỏ endpoint khác bucket.
5. Mỗi hop phải **probe sống trước khi tin** (mục 4). Chain đẹp trên giấy ≠ chain chạy.

## 3. Credential pool — đọc để biết hop nào đang bị loại

State: `~/AppData/Local/hermes/auth.json` → key `credential_pool.<provider hoặc custom:NAME>` = **list** entry:
`label`, `last_status` (`ok|exhausted`), `last_error_code`, `last_error_reset_at`, `base_url`, `api_key`, `priority`.
Ngoài ra `suppressed_sources` (env key bị suppress) và `providers` (thường rỗng).

- Pool không có entry cho provider mới → chưa từng gọi, không phải lỗi.
- TTL cooldown theo error code: `_exhausted_ttl()` → 401/429/default khác nhau; `reset_at` = None thì
  dùng TTL mặc định từ `last_status_at`.
- `402 "This request requires more credits, or fewer max_tokens. You requested up to N tokens"` = **cost 1 request
  vượt balance**, KHÔNG phải hết sạch credit: cùng key gọi `max_tokens: 16` vẫn 200. ⇒ hop đó vô dụng cho agent
  thật (turn cần hàng nghìn token) nhưng vẫn "sống" trong probe.
- Log `credential pool: no available entries (all exhausted or empty)` lặp 15s = có process đang probe pool
  đã cạn (thường do primary đang trỏ provider 402). Đổi primary khỏi provider đó là hết loop.

## 4. Probe từng hop (bằng chứng sống)

Dùng `scripts/probe_provider_hops.py` (kèm skill này): đọc config, in bảng candidate + HTTP status,
key được mask. Lưu ý: một số endpoint sau Cloudflare trả **403 error code 1010** với UA lạ
(probe thô thấy chết nhưng agent chạy được) → đừng kết luận provider chết từ probe thô nếu mã là 1010.
Kết quả cuối cùng phải là "agent thật gọi được", không phải "curl trả 200".

## 5. Verify chuỗi end-to-end (cách chắc chắn nhất)

Chạy một lượt thật với primary bị làm hỏng, rồi đọc **hop nào đã phục vụ** từ DB:

```bash
hermes -z "Trả lời đúng một từ: FALLBACK_OK" -t hermes-cli --provider '<provider primary>' -m 'model-khong-ton-tai'
```
```sql
select id, model, billing_provider, billing_base_url, started_at
from sessions order by started_at desc limit 3;
```
`billing_provider` / `billing_base_url` của session = **hop đã phục vụ**.
Case 18/10: `model=deepseek-v4-1-flash-260910`, `billing_provider=custom:ark-v3`,
`billing_base_url=https://ark.ap-southeast.bytepluses.com/api/v3/` → hop 1 đã cứu, chuỗi đúng.

Verify đường cron (khác code path): chờ 1 job thật chạy và grep log:
```bash
grep -E "cron_<jobid>" logs/agent.log | grep -E "API call|Turn ended|Fallback"
```
Case 18/10: cron `KFlow Push Tâm lý` pin `deepseek/deepseek-v4-flash @ command-code` fail 18:00 (429),
**thành công 18:30** với `provider=custom:ark-v3` + `Turn ended: reason=text_response(stop)`.
⇒ Job cron **pin model chết vẫn được chuỗi top-level cứu**, chạy được, chỉ tốn 1 call fail mỗi lượt.

## 6. Model của một session đến từ đâu

- Model đọc **live từ config mỗi lượt** (đổi config xong lượt sau ăn ngay, không cần restart gateway).
- `gateway_routing` (`state.db`) key dạng `agent:main:telegram:group:<chat_id>`, `entry_json` chứa
  `model_override` — **None = session ăn theo config**. Không có dòng nào chứa `model_override` ⇒ chưa ai `/model`.
- `sessions.model` / `billing_provider` / `model_config.gateway_runtime.fallback_active` chỉ là **bản ghi**.
  Muốn "chuyển session X về model hiện tại": sửa config primary (ảnh hưởng mọi kênh) hoặc set override
  trong chính session đó; sửa cột DB chỉ để hiển thị đúng, không đổi hành vi.

## 7. Pitfall

- Đổi model/fallback mà **không sync GOLDEN của guard** → lần guard chạy sẽ revert (xem
  `references/config-guard-desktop-kill-2026-10.md`). Verify bằng cách import script guard, so 8 key GOLDEN
  với config (drift phải = 0) và mô phỏng `fix_config()` ra file tạm trước khi tin.
- Đổi primary xong **đừng quên cron/phiên khác**: 22 job pin provider cũ vẫn "chạy được" nhờ chuỗi nhưng
  mỗi lượt trả giá 1 call fail. Muốn sạch thì repoint pin.
- Form Settings của desktop có thể ghi lại `model.default` + `fallback_providers` (case 18/10: bị ghi thành
  `openrouter` + chuỗi 1 hop, đúng lúc desktop đổi model). Sửa config xong phải nói user biết: đừng bấm Save
  ở tab model nếu không muốn ghi đè.
- `hermes config set model.provider custom:<tên>` hoạt động; tên custom provider có thể lệch hoa/thường so với
  `custom_providers[].name` mà vẫn resolve.
