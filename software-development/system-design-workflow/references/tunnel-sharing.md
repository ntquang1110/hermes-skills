# Tunnel — Share Local Server Publicly

Dùng khi cần cho user xem design / website từ điện thoại hoặc máy khác mà không cần deploy.

## localtunnel (khuyên dùng trên Windows)

**Ưu điểm:** Dùng npm, auto-download, không cần tài khoản, output URL capture được trên MSYS2.

```bash
# Foreground — lấy URL trước (timeout 25s)
npx.cmd localtunnel --port 8080
# Output: your url is: https://<random>.loca.lt

# Background — duy trì tunnel
npx.cmd localtunnel --port 8080
# Dùng terminal(background=true, notify_on_complete=true)
```

**Lưu ý:**
- ⚠️ **Dùng `npx.cmd`** (Windows native) — không dùng `npx` (MSYS2 fork lỗi)
- Lần đầu truy cập: localtunnel show interstitial "Click to Continue" — bấm qua
- Tunnel sống khi process còn chạy

## localhost.run (SSH — dùng khi localtunnel không available)

**Yêu cầu:** SSH client (có sẵn trên Windows 10+)

```bash
ssh -o StrictHostKeyChecking=no -o ServerAliveInterval=30 \
    -R 80:localhost:8080 nokey@localhost.run
```

**⚠️ Trên Windows/MSYS2:** SSH tunnel thường không capture được output trong background process. Nên dùng `pty=true` foreground để lấy URL, sau đó chạy background tunnel riêng.

## Khi nào dùng

| Tình huống | Nên dùng |
|------------|----------|
| User muốn xem từ điện thoại ngay trên Windows | ✅ **localtunnel** (npx.cmd localtunnel) |
| Cần share vĩnh viễn, ai cũng xem được | ✅ GitHub (push code lên — public repo) |
| Không có npm, chỉ có SSH | ✅ localhost.run (SSH tunnel) |
| Cần production-grade, custom domain | ❌ Cloudflare Tunnel / ngrok (trả phí) |

## Pitfalls

1. **localtunnel dùng `npx.cmd` không phải `npx`** — trên MSYS2, `npx` fork lỗi. Luôn dùng `npx.cmd`.
2. **EADDRINUSE** — port đã có process chiếm. Dùng `netstat -ano | grep ":PORT" | grep LISTENING` → `taskkill //F //PID <PID>`.
3. **SSH tunnel không capture output** trên Windows background process. Chạy `pty=true` foreground để lấy URL trước.
4. **Tunnel chết khi process chết** — cần maintain background tunnel process.
5. **localtunnel cần Node.js** — kiểm tra `node --version` trước.
6. **GitHub private repo** — raw.githubusercontent.com không serve được file. Cần set public hoặc dùng tunnel.
