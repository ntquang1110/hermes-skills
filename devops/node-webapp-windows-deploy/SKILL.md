---
name: node-webapp-windows-deploy
description: "Reset/deploy Node web app trên Windows (dithi, tfo, kflow)."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [windows, node, deploy, process, cloudflare, tunnel, selfhosted, reset]
---

# Node Web App Windows Deploy

Vận hành Node web app chạy trên máy Windows của Quang, phía sau Cloudflare tunnel.
Áp dụng cho: dithi (5100), tfo (8100), kflow (3003), metelligent (8766), v.v.
Không phải skill deploy Docker — đây là node thuần / process nền.

## 1. Process lifecycle — QUAN TRỌNG NHẤT

**TRAP: `process(action='kill')` trên Hermes KHÔNG giết được node.exe thật.**

Hermes background terminal chạy qua bash wrapper. PID trả về là wrapper, KHÔNG phải node.
Kill wrapper → node.exe vẫn sống, vẫn giữ port + state trong RAM. Sau đó:
- start server mới → `EADDRINUSE` hoặc log vẫn ghi "running" nhưng request chạy vào server CŨ
- reset state (xóa file) → server cũ persist lại dữ liệu RAM cũ lên file → tưởng reset mà không reset
- triệu chứng người dùng thấy: "STT đang được sử dụng" / "dữ liệu cũ vẫn còn" / "đã reset mà không sạch"

**Quy trình kill đúng (luôn dùng PID thật từ netstat):**

```bash
# 1. Tìm PID thật đang listen
netstat -ano | grep ":PORT" | grep LISTEN
# 1b. KHÔNG dừng ở PID đầu tiên — kiểm tra MỌI node.exe liên quan port (thường có 2):
#     - npx wrapper (npx-cli.js next start) → process trung gian dễ sót
#     - next/bin/next thật → process giữ port thật, kẻ báo LISTENING
#     `wmic process where "name='node.exe'" get ProcessId,CommandLine | grep :PORT`
#     TODO: quét hết, kill tất cả. Sót 1 cái → port vẫn bị giữ, start mới EADDRINUSE
#     hoặc log vẫn "running" nhưng request chạy vào server cũ.
# 2. Kill từng PID (bash kill -9 FAIL SILENTLY trên Windows-native process)
powershell -Command "Stop-Process -Id <PID> -Force"
#    (cách khác hoạt động: MSYS_NO_PATHCONV=1 taskkill /F /PID <PID> — thêm MSYS_NO_PATHCONV=1
#     để /F không bị MSYS biến thành path; //F double-dash thì taskkill báo "Invalid argument/option".)
# 3. Verify port free
netstat -ano | grep ":PORT" | grep LISTEN || echo "port free"
```

## Start lại từ Hermes background terminal

Ở đây KHÔNG dùng `nohup ... &` — bash không job control sẽ lỗi `bash: no job control in this shell / syntax error near unexpected token`. Đúng cách: chạy server TRỰC TIẾP làm lệnh background, dùng `exec` để thay thế wrapper shell:

```bash
terminal(background=true, command="cd <project> && exec node node_modules/next/dist/bin/next start --port <PORT>")
```

Kill wrapper trước đó thì không cần — `exec` chắc chắn lệnh thật chiếm PID background process.

Không dùng `taskkill //F //PID` trong git-bash (MSYS mangle `//` thành path).
`taskkill -F -PID <PID>` single-dash OK, nhưng `powershell Stop-Process` là đáng tin nhất.

## 2. Reset state hygiene

Thứ tự BẮT BUỘC: **kill server thật TRƯỚC, xóa state file SAU, verify port free, mới start lại.**

Server giữ state trong RAM, chỉ persist khi có request gây thay đổi (enter/save/submit/login).
Nếu server còn sống mà xóa state.json → request kế tiếp ghi đè file với dữ liệu RAM cũ.
Luôn backup state trước khi xóa: `cp data/state.json data/state_backup_<mô tả>.json`.

Sau khi start lại, verify bằng 1 request thật (không chỉ đọc log):
```bash
curl -s -X POST http://localhost:PORT/api/admin/login -H "Content-Type: application/json" -d '{"password":"..."}'
# rồi gọi endpoint overview/danh sách — nếu response 0 record là sạch
```

## 2b. Server LISTENING nhưng 0 bytes (busy-loop deadlock)

**Khác với "kill không chết" — đây là server SỐNG nhưng treo logic, vẫn giữ port, không trả byte nào.** KF (Next.js `next start --port 3003`) từng dính: mọi route (kể cả `/`) treo vài giây → `HTTP:000` size 0, dính ở **cả IPv4 (`127.0.0.1`) lẫn IPv6 (`::1`)** — nếu còn dính một IP thì là network stack, nếu cả hai cùng 0 byte thì là server treo.

Chẩn đoán phân biệt với tạm quá tải:
```bash
curl -s -m 8 http://localhost:PORT/ -o /dev/null -w '%{http_code}'   # HTTP:000, 0 bytes
netstat -ano | grep ":PORT" | grep LISTEN                            # vẫn LISTENING
# xác nhận busy-loop: CPU delta ~= wall time nghĩa là full 1 core, không recover tự nhiên.
# PowerShell có biến $ qua bash: viết file .ps1 rồi chạy (bash nuốt `$a/$b` trong double-quote -> parse error)
# nội dung: $a=(Get-Process -Id <pid>).CPU; Start-Sleep 4; $b=(Get-Process -Id <pid>).CPU; ($b-$a)
```

CPU delta ≈ 4s sau 4s ngủ = đang cháy trọn 1 core (busy-loop/deadlock). Server như vậy KHÔNG tự hết — `EADDRINUSE` ở trên hoặc knowledge-researcher/hron cùng push đều fail. Fix là **restart** bằng đúng quy trình ở mục 1 (Stop-Process → verify port free) rồi `cd <project> && node node_modules/next/dist/bin/next start --port <PORT>`, sau đó verify `curl -b "tfo_auth=<hash>" http://localhost:PORT/api/cards` trả `HTTP:200`. Production `next start` không cần compile → restart nhanh & an toàn.

## 3. Health check 4 tầng

```bash
# Layer 1: process
netstat -ano | grep ":PORT" | grep LISTEN
# Layer 2: local origin
curl -s -o /dev/null -w "%{http_code}" http://localhost:PORT/
# Layer 3: qua tunnel
curl -s -o /dev/null -w "%{http_code}" --max-time 25 https://sub.domain/
# Layer 4: DNS
nslookup sub.domain 2>/dev/null | grep -E "Address"
```

Localhost 200 + tunnel 404 = tunnel config thiếu ingress. Localhost 200 + tunnel 200 + user báo chậm 30s = xem mục 5 (Google Fonts) hoặc benchmark: `curl -w "TTFB %{time_starttransfer}s | Total %{time_total}s"`.

## 4. Cloudflare tunnel (tóm tắt — chi tiết xem skill cloudflare-tunnel)

- Service token-managed (`sc qc cloudflared` → `--token`) → `config_src: cloudflare` → **local YAML bị IGNORE**. Sửa qua API:
  1. GET `accounts/{ACCOUNT}/cfd_tunnel/{TUNNEL}/configurations`
  2. Chèn rule trước catch-all `http_status:404` (bắt buộc cuối cùng)
  3. PUT, verify version tăng + đọc lại config
- Thêm CNAME: resolve ZONE_ID cho EXACT domain (không dùng zoneID trong cert.pem — có thể thuộc domain khác!), POST dns_records `{type:CNAME, name:sub, content:"<TUNNEL_ID>.cfargotunnel.com", proxied:true}`
- Token lấy từ `~/.cloudflared/cert.pem` (decode base64, field `apiToken`)
- API call luôn wrap `--retry 5 --retry-delay 3` (mạng VN hay rớt, trả body rỗng)
- Sau PUT ingress mới ~30s tự load, KHÔNG restart.

## 5. VN network pitfalls

**Google Fonts = render-blocking = 30 giây delay.** `<link href="https://fonts.googleapis.com/...">` trong `<head>` bắt buộc browser chờ stylesheet xong mới render. Ở VN googleapis bị chặn/chậm → user thấy "bấm xong 30s sau mới đổi" — thực ra là trang chưa render.

**Fix: BỎ Google Fonts hoàn toàn, dùng system-ui.** Kiểm tra: `grep -c googleapis public/*.html` phải = 0, và `performance.getEntriesByType('resource')` không có font external. Font display đẹp (Space Grotesk...) không đáng 30s trễ — nhất là app thi/dashboard thí sinh.

Khác: cloudflared bị WARP cạnh tranh, 2 process cùng tunnel gây TLS chậm — xem skill cloudflare-tunnel.

## Pitfalls

1. **process(action='kill') tin cậy ~0 trên Windows cho node** — luôn netstat → Stop-Process.
2. **"Đã reset mà vẫn còn dữ liệu"** = server cũ còn sống, gần như chắc chắn.
3. **Đọc state file bằng python khi server đang chạy** — nội dung có thể là bản cũ; server chỉ persist khi có request.
4. **Lint sau patch báo "Cannot find module D:\d\..."** — là lỗi MSYS path của linter, KHÔNG phải file hỏng. Verify bằng `node --check file.js` thật.
5. **Không bao giờ viết file nặng vào C:/Users** — project để D:/Hermes Proj/ (disk policy, xem AGENTS.md).
6. **Xác nhận reset bằng dữ liệu thật** (gọi overview thấy 0 record), không chỉ nhìn log "running".
7. **Browser tool KHÔNG phải nơi verify thay đổi UI** — nó cache bundle cũ client-side (sau rebuild vẫn show DOM cũ: class/placeholder cũ). Verify server-render TRỰC TIẾP: `curl -s http://localhost:PORT/ | grep -c "placeholder=\"…mới…\""` phải khớp bản mới, và curl kiểm tra bản cũ phải = 0. Đã chắc server đúng rồi mới để user reload trình duyệt của họ.
8. **Chạy `taskkill` từ MSYS** — `/F` bị biến thành path → wrap `MSYS_NO_PATHCONV=1 taskkill /F /PID <PID>`, không dùng `//F` (lỗi "Invalid argument/option").

## References

- `references/exam-app-dithi.md` — hồ sơ vận hành app thi dithi (port, pass, reset, cấu trúc data, link)
- `references/quiz-exam-patterns.md` — pattern tái sử dụng cho hệ thống thi trắc nghiệm (gen đề, auto-submit, resume, lock STT, import Excel)

## Related skills

- `cloudflare-tunnel` — tunnel sâu: ingress API, DNS, crash recovery, WARP conflict
- `html-unslop` / `impeccable` — design UI, audit AI-tells
- `systematic-debugging` — khi health check các tầng không ra
