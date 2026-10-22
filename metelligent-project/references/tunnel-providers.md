# Tunnel Providers cho Vietnam Mobile (không WARP)

## Tested on this machine + Vietnamese mobile networks

| Provider | URL Pattern | Works in VN? | Notes |
|----------|------------|--------------|-------|
| **Cloudflare Tunnel** | `*.trycloudflare.com` | ✅ Yes | Cần tắt WARP tạm trên máy host. Domain không bị chặn. |
| **localtunnel (loca.lt)** | `*.loca.lt` | ⚠️ Thường bị chặn | Hay bị chặn trên Viettel/Mobifone/Vinaphone |
| **localtunnel (localtunnel.me)** | `*.localtunnel.me` | ❌ API server không reachable | `getaddrinfo failed` từ máy này |
| **serveo.net** | `*.serveo.net` (SSH) | ❌ Timeout | SSH connection timeout ở VN |
| **pinggy.io** | `*.pinggy.io` (SSH) | ❌ Timeout | SSH connection timeout ở VN |
| **ngrok** | `*.ngrok.io` | ⚠️ Tuỳ lúc | Chưa test — cần auth token |

## Cloudflare Tunnel — Chi tiết

**Cài đặt:** Đã có `cloudflared` tại `/c/Program Files (x86)/cloudflared/cloudflared`

**Chạy (cần tạm tắt WARP):**
```bash
warp-cli disconnect
cloudflared tunnel --url http://localhost:8767 --protocol http2
# -> URL: https://xxx-yyy-zzz.trycloudflare.com
warp-cli connect
```

**Lưu ý:**
- Dùng `--protocol http2` — QUIC timeout qua WARP
- URL random mỗi lần chạy
- tunnel chết khi cloudflared process tắt
- Cloudflare free tier không đảm bảo uptime cho quick tunnels

### Named Tunnel (URL cố định) — nếu có domain riêng
```bash
cloudflared tunnel create metelligent
cloudflared tunnel route dns metelligent api.metelligent.com
cloudflared tunnel run metelligent
```

## localtunnel — Chi tiết

**Install:** `npm install -g localtunnel`

**Chạy:**
```bash
npx localtunnel --port 8767 --subdomain metelligent-123
```

**Lưu ý:**
- Chạy được qua WARP (localtunnel không conflict với WARP)
- Subdomain cố định nhưng hay bị chặn ở VN
- Có thể thử server khác: `LOCAL_API=https://localtunnel.me npx localtunnel --port 8767`

## Troubleshooting kết nối từ điện thoại

1. **Test tunnel từ máy tính trước:**
   ```bash
   curl https://tunnel-url/api/health
   ```
   Nếu 200 OK → tunnel hoạt động. Vấn đề ở mạng điện thoại.

2. **Thử với browser trên điện thoại:**
   Mở `https://tunnel-url/api/health` trên Chrome/Safari của điện thoại.
   - Nếu hiện JSON → app có vấn đề, không phải mạng
   - Nếu timeout/ERR_CONNECTION_REFUSED → tunnel bị chặn bởi nhà mạng

3. **Nếu bị chặn:** Chuyển sang Cloudflare Tunnel (trycloudflare.com)
