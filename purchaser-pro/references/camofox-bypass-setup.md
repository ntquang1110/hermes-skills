# Camofox Bypass — Chống chặn bot cho browser research tại VN
> Cập nhật sau session 2026-07-27: đã test thành công Google, Shopee, EMIN.vn, YKTech

> Kỹ thuật phát hiện và xác nhận hoạt động trong session 2026-07-27.
> Google Search, Shopee, EMIN.vn, YKTech đều qua được sau khi setup.

## Vấn đề

Các search engine và sàn TMĐT tại VN chặn hầu hết request từ bot:
- **Google:** CAPTCHA ngay (IP datacenter)
- **Bing:** kết quả sai hoàn toàn (từ "máy" → "May" tháng)
- **Shopee / Tiki / Lazada:** bot-detection → empty page
- **Alibaba / AliExpress:** CAPTCHA + Cloudflare
- **DuckDuckGo:** CAPTCHA

**Căn nguyên:** Browser chạy ở chế độ `stealth_features: ["local"]` — không có residential proxy, không có fingerprint spoofing mạnh.

## Giải pháp: Camofox (Camoufox-based Firefox)

Camoufox là Firefox fork có C++ fingerprint spoofing — browser thật, không phải headless Chromium bị phát hiện. Camofox-browser là REST API server wrapping Camoufox, tương thích với Hermes.

### Cài đặt

```bash
# Clone
git clone https://github.com/jo-inc/camofox-browser.git
cd camofox-browser

# Install dependencies
npm install

# Download Camoufox browser binary + GeoIP database
npx camoufox-js fetch

# Start server (port 9377 mặc định)
node --max-old-space-size=256 server.js
```

Kiểm tra: `curl http://localhost:9377/` → `{"ok":true,"engine":"camoufox",...}`

### Cấu hình Hermes dùng Camofox

```bash
# 1. Set env var (uncomment trong .env)
# ~/.hermes/.env
CAMOFOX_URL=http://localhost:9377

# 2. Set browser engine trong config.yaml
# ~/.hermes/config.yaml
browser:
  engine: camofox
```

Hoặc dùng CLI:
```bash
hermes config set browser.engine camofox
```

**Lưu ý:** Config chỉ có hiệu lực sau khi session restart (`/reset` hoặc khởi động lại Hermes).

### Xác nhận hoạt động

Dấu hiệu Camofox đang hoạt động:
- **Không còn** dòng `"Running WITHOUT residential proxies"` trong output của `browser_navigate`
- `stealth_features` không còn là `["local"]`
- Google Search trả về kết quả thay vì CAPTCHA
- Shopee trả về trang thật thay vì empty page

### Xử lý

- Server chạy ngầm, cần đảm bảo auto-restart khi reboot (systemd / Task Scheduler)
- Nếu cần chạy trên port khác: `CAMOFOX_PORT=3000 node server.js`
- Memory: `--max-old-space-size=256` là đủ, idle ~40MB

## Giải pháp thay thế (nếu Camofox không đủ)

| Phương án | Chi phí | Ghi chú |
|-----------|---------|---------|
| Browserbase Pro | $29-99/tháng | Residential proxy + CAPTCHA solving, config: `browser.stealth: full` |
| Serper.dev API | $50/tháng | Google search API, không CAPTCHA |
| Azure Bing Search | ~$7/1k calls | Bing thật, không block |
| ScrapingBee | $49/tháng | Handle proxy + CAPTCHA tự động |

## Lưu ý

- Camofox dùng Firefox engine, khác biệt nhẹ so với Chromium trong render
- Cookie/session không persist qua restart server trừ khi bật `managed_persistence`
- GeoIP database download lần đầu ~66MB
