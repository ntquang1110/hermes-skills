# BytePlus ModelArk — Rate Limits (research 2026-09-08, đọc từ docs chính thức)

Khi user hỏi về rate limit BytePlus/Volcengine ModelArk, hoặc Hermes dính HTTP 429
trên provider bytedance (`deepseek-v4-flash-ga-260731` etc.), đây là chính sách thật.

## Nguồn chính thức
- Burst traffic best practices: https://docs.byteplus.com/en/docs/ModelArk/1848593
- Model list + rate limit từng model: https://docs.byteplus.com/en/docs/ModelArk/1330310
- Error codes (đầy đủ 429): https://docs.byteplus.com/en/docs/ModelArk/1299023
- Activation Management (xem limit account thật): https://docs.byteplus.com/en/docs/ModelArk/1159200
- FAQ tăng limit: https://ai.byteplus.com/en/help/article/how-do-i-increase-my-rate-limit-qps-concurrency-or-resolve-throttling-and-queueing

## Cấu trúc limit — ĐỌC KỸ
- Limit theo **PRIMARY ACCOUNT + MODEL**, không theo API key. Mọi endpoint/account
  của cùng model chia chung 1 resource pool → **xoay API key trong cùng account KHÔNG
  thoát rate limit**. Muốn thoát phải dùng account khác.
- Metric: **RPM** (requests/phút), **TPM** (tokens/phút, input+output), **Inflight
  Batchsize** (concurrency, span cả queue+compute), IPM (ảnh/phút), TPD (batch).
- **Model rate limits do ModelArk set, KHÔNG tự chỉnh** → tăng phải mở ticket support.
  Endpoint (EP) limits thì user adjust được trong console.
- Số trong Model list là *theoretical max, không đảm bảo* — tùy tải nền tảng.

## Rate limits DeepSeek trên BytePlus (bảng thật từ Model list 1330310)

| Model | RPM | TPM |
|---|---|---|
| `deepseek-v4-flash-ga-260731` | **500** | 1M (1000K) |
| `deepseek-v4-pro-ga-260813` | **500** | 1M |
| `deepseek-v4-flash-260425` | 15K | 1.5M |
| `deepseek-v4-pro-260425` | 15K | 1.5M |
| `seed-2-0-lite-260428` | 30K | 1.5M |

→ Bản GA (260731/260813) RPM thấp hơn **30x** bản 260425. Workload nhiều request
nhỏ (cron chat, tool-call dày) → cân nhắc `deepseek-v4-flash-260425` hoặc
`seed-2-0-lite` thay vì GA.

## Burst traffic (nguyên nhân 429 hay gặp khi Hermes chạy cron song song)
- Ngưỡng nhận diện: tăng **+3M TPM so phút trước** HOẶC **+20% trong 3 phút**.
- Trả 429: `RequestBurstTooFast` (model seed-2.0 trở đi), `ServerOverloaded`
  (seed-1.8 trở về trước). Platform tự hồi phục sau vài phút khi mở rộng cluster.
- **Failed requests VẪN ĐẾM vào RPM** → retry nóng càng chết nhanh hơn.

## Taxonomy 429 — phân biệt để xử lý đúng
| Error code | Ý nghĩa | Xử lý |
|---|---|---|
| `ModelAccountRpmRateLimitExceeded` / `ModelAccountTpmRateLimitExceeded` | vượt limit model trên account | backoff + giảm tải |
| `RateLimitExceeded.EndpointRPMExceeded` / `EndpointTPMExceeded` | limit endpoint | chỉnh trong console (endpoint limit adjust được) |
| `APIAccountRpmRateLimitExceeded` | limit RPM API account | backoff |
| `QuotaExceeded` | hết free trial quota model | vào Activation page bật model |
| `SetLimitExceeded` | Safe Experience Mode chạm ngưỡng | chỉnh/off trên Activation Management |
| `InflightBatchsizeExceeded` | vượt concurrency theo số tiền nạp | nạp thêm mới mở |
| `ServerOverloaded` / `RequestBurstTooFast` | burst traffic | ramp-up chậm lại |

## Cách áp dụng (từ doc best practices 1848593)
1. **429 → exponential backoff + jitter**: tenacity
   `@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))`.
2. **Ramp-up chậm**: 5 QPS → +2 QPS mỗi 5s → max 30 QPS (slope 0.4 QPS/s). Có thể
   dùng token bucket client-side (golang.org/x/time/rate pattern trong doc).
3. **Chia tải qua model KHÁC** (pool độc lập giữa các model). Chia qua nhiều
   endpoint/key cùng model vô ích (chung pool).
4. Peak predictable (scheduled jobs) → **mua Model Unit TRƯỚC 15 phút** để mở rộng pool.
5. Muốn tăng limit cố định → ticket support (model limit không tự chỉnh được).
6. Base URL ap-southeast-1: `https://ark.ap-southeast.bytepluses.com/api/v3`.

## Lưu ý research — docs BytePlus là JS-render
- curl tới `docs.byteplus.com` trả HTTP 200 nhưng **0 byte** (Next.js SPA) → phải
  dùng browser (Camofox).
- Trang error codes (1299023): snapshot accessibility tree KHÔNG chứa nội dung
  bảng → phải `browser_console` evaluate `document.body.innerText` rồi slice quanh
  `429`/`TooManyRequests`.
- Google/Bing chặn từ IP VN → DuckDuckGo qua Camofox là đường search chuẩn.
