# Resolve context window thật của model + guard không được xoá key mới

Case gốc: 2026-10-19, model `deepseek-v4-1-flash-260910` @ BytePlus Ark coding/v3.

## 1. Triệu chứng

`logs/agent.log` ghi `ctx 128,000` / `context=128,000` cho mọi request.
Ngưỡng auto-compress = 96.000 (75%). Session dài bị nén liên tục dù model còn thừa chỗ.

## 2. Nguyên nhân — Hermes lấy NHẦM con số

Bảng model chính thức BytePlus ModelArk (`deepseek-v4-1-flash-260910`):

| Trường | Giá trị |
|---|---|
| Context length | **1024K** ← cửa sổ thật |
| Max input | 1024K |
| Max output (incl. CoT) | 384K, default 4K |
| Max CoT | **128K** ← Hermes lấy số này |
| Rate limit | 0.5K RPM, 1000K TPM |

Hermes resolve ra **128.000 = đúng bằng Max CoT**, không phải context window. Sai 8,2 lần.
Với model Hermes không có trong registry nội bộ, nó rơi về một hằng số mặc định —
và ở đây hằng số đó tình cờ bằng Max CoT. **Không được tin `ctx` trong log là cửa sổ thật.**

## 3. Cách tra cửa sổ thật (theo thứ tự, cách 1–2 KHÔNG hiệu quả)

1. **`GET /api/v3/models`** — KHÔNG dùng được. Trả về danh sách `id` (59 model) nhưng
   **không có field `context_length`**. Không suy ra được gì.
2. **Probe bằng `max_tokens` khổng lồ** — KHÔNG dùng được. Gửi `max_tokens: 1000000`
   vẫn trả HTTP 200 bình thường, API âm thầm tự cắt về trần thật. Không lộ giới hạn.
3. **Trang model-list của provider** — ĐÚNG. Đây mới là nguồn có số.
   - BytePlus: `https://docs.byteplus.com/en/docs/modelark/deepseek-v4-1-flash`
     và `.../modelark/model-list`
   - Trang **render bằng JS** → `web_extract` chỉ trả về phần nav, **không thấy bảng**.
     Phải mở bằng browser tool mới đọc được spec.
4. Nếu vẫn không có: đọc thẳng trang spec trên console của provider, hoặc docs của bản
   base model (HuggingFace card) — nhưng nhớ bản host thường khác bản base.

## 4. Fix

```bash
hermes config set model.context_length 1048576     # 1024K
```

Hiệu quả (đo thật):

| Chỉ số | Trước | Sau |
|---|---|---|
| context window | 128.000 | **1.048.576** |
| ngưỡng auto-compress (75%) | 96.000 | **786.432** |
| ngưỡng session hygiene (85%) | 108.800 | **891.289** |

Cần **restart gateway** mới có hiệu lực — `model.context_length` được đọc lúc session
khởi tạo. Xem pitfall restart trong SKILL.md.

## 5. PITFALL — guard "phục hồi config" sẽ XOÁ key bạn vừa thêm

Đây là cái bẫy chính của case này. `config_guard.py` V4 (cron `config-guard-hermes`,
chạy `*/15 * * * *`) **phát hiện drift theo từng key** nhưng **sửa bằng cách thay
nguyên khối**:

```python
# V4 — SAI
cfg["model"]      = GOLDEN["model"]        # xoá mọi key không có trong GOLDEN
cfg["providers"]  = GOLDEN["providers"]    # trả providers.unsloth.base_url về IP chết
```

Hệ quả:

- `model.context_length` (không có trong GOLDEN) **bị xoá trắng** ngay khi BẤT KỲ
  key nào trong danh sách `checks` lệch — không cần chính nó lệch.
- `providers` bị thay cả khối → `unsloth.base_url` bị trả về `192.168.1.3:18888`
  (đã chết), đè mất endpoint thật `pharma-llm.thefirstonly.com`.

Chẩn đoán nhanh: đọc `CHECKS` trong guard. Nếu danh sách `checks` là per-key mà
`fix_*()` lại gán cả khối, đó là bẫy.

**Sửa đúng (V5)** — hai việc, phải làm CẢ HAI:

1. Thêm key mới vào `GOLDEN` **và** vào danh sách `CHECKS`, để nó được bảo vệ
   và được phục hồi nếu bị sửa.
2. Đổi hàm sửa thành **targeted per-key**, không gán cả khối:

```python
def set_path(cfg, key, value):        # 'a.b.c'
    parts = key.split(".")
    cur = cfg
    for p in parts[:-1]:
        nxt = cur.get(p)
        if not isinstance(nxt, dict):
            nxt = {}; cur[p] = nxt
        cur = nxt
    cur[parts[-1]] = value

def fix_config(deviated):             # chỉ sửa đúng key bị lệch
    cfg = load_conf()
    for key, _got, want in deviated:
        set_path(cfg, key, want)
    # backup rồi ghi
```

## 6. Verify BẮT BUỘC — test đường PHỤC HỒI, không chỉ đường im lặng

Chạy guard khi config đúng chỉ chứng minh nó không phá. Phải phá thử:

```bash
# 1. đặt sai giá trị (giả lập drift)
python -c "import yaml;p='config.yaml';d=yaml.safe_load(open(p,encoding='utf-8'));\
d['model']['context_length']=128000;yaml.safe_dump(d,open(p,'w',encoding='utf-8'),allow_unicode=True,sort_keys=False)"
# 2. chạy guard
python scripts/config_guard.py
# 3. khẳng định đã cứu về 1048576
```

Kỳ vọng: guard in ra dòng drift + `ĐÃ KHÔI PHỤC THÀNH CÔNG`, giá trị về `1048576`.
Sau đó kiểm tra toàn vẹn các phần KHÁC (fallback chain, `providers.*.base_url`,
`kanban.dispatch_in_gateway`) — guard ghi lại cả file nên phải xác nhận không mất gì.

## 7. Lưu ý khi mở rộng cửa sổ

- **Chi phí:** mỗi call bill toàn bộ input. Cửa sổ 786K nghĩa là session có thể phình
  tới 786K token trước khi nén. Cache hit 98–99% làm phần đọc lại rẻ, nhưng khối lượng
  vẫn lớn hơn nhiều so với 70K/call. Cân nhắc soft-cap thực dụng (~256K) thay vì để trần.
- **Chất lượng ở độ dài cực lớn chưa kiểm chứng.** Có báo cáo người dùng nói chất lượng
  giảm quanh ~125K input. Chưa tự verify → đừng trích như sự thật. Nếu cần dùng session
  rất dài, đo lại trước.
- `hermes config set` ghi lại TOÀN BỘ `config.yaml` (mất comment). Sao lưu trước khi set.

## 8. Model mới hơn trên cùng endpoint

Cùng lúc phát hiện `deepseek-v4-1-flash-261017` (bản 17/10, cùng spec 1024K) —
mới hơn bản `260910` đang chạy. `glm-5-3-flash-260828` cũng 1024K.
Quét `/api/v3/models` để phát hiện bản mới thay vì dùng mãi một snapshot.
