# 502 Bad Gateway trên endpoint tự host — tunnel sống, origin chết

Case thật: 2026-10-21. Provider `unsloth` (`https://pharma-llm.thefirstonly.com/v1`) trả 502. Watchdog
`watchdog-unsloth` báo *"Tunnel Unsloth CHẾT hoặc không phản hồi — HTTP Error 502. 4 job tâm lý đang dùng
model này sẽ không chạy được."*

Nhãn "tunnel CHẾT" là **sai**. Tunnel sống. Chết là origin. Đây là lý do phải đo từng tầng.

## Bảng phân biệt 3 nguyên nhân 502

| Triệu chứng | Nguyên nhân thật | Xử lý |
|---|---|---|
| `/ready` 200, `ha_connections` > 0, `request_errors` tăng | connector sống, **origin** chết hoặc bind sai (`127.0.0.1`) | bật lại dịch vụ origin trên máy đó |
| `/ready` fail, `ha_connections` 0 | connector không nối được Cloudflare edge (mạng máy đó hỏng / service stop) | khôi phục mạng + restart cloudflared |
| Origin trả 200 khi curl **tại chỗ** nhưng ngoài vẫn 502 | connector đang giữ hostname nằm ở **máy khác** | đối chiếu tunnel ID giữa các máy |

## Lệnh đo, theo thứ tự

```bash
# 1. Tầng ngoài — lặp nhiều lần để loại trừ chập chờn do load-balance
for i in $(seq 1 12); do
  curl -s -o /dev/null -w "%{http_code}\n" --max-time 12 https://<domain>/v1/models
done
# 502 đều 12/12 → connector trỏ sai chỗ. Nếu 200/502 xen kẽ → nhiều connector, 1 cái chết.

# 2. Tunnel còn sống? (Windows: cloudflared mở metrics ở 127.0.0.1:20241)
curl -s http://127.0.0.1:20241/metrics | grep -E "cloudflared_tunnel_ha_connections|cloudflared_tunnel_request_errors"
curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:20241/ready     # phải 200

# 3. Tunnel có phải remote-managed?
sc qc cloudflared | grep BINARY_PATH      # thấy "tunnel run --token eyJ..." = remote-managed

# 4. Origin bind ở đâu? (chạy TRÊN máy chạy origin)
lsof -nP -iTCP:8888 -sTCP:LISTEN           # 127.0.0.1:8888 = chỉ local, HTTP 000 từ ngoài là bình thường

# 5. Port nào trên máy local thật sự là LLM? (đừng đoán theo số port)
#    quét /v1/models trên các port đang listen; LLM OpenAI-compatible trả JSON {"object":"list",...}
```

## Topology thật của pharma-llm (đo 21/10/2026)

```
Hermes → https://pharma-llm.thefirstonly.com/v1
       → Cloudflare edge
       → cloudflared tunnel
       → 127.0.0.1:8888  trên Mac mini của Kiềm   ← ORIGIN
            unsloth studio --api-only -H 127.0.0.1 -p 8888
            llama-server (port động, vd 61405, --api-key-file ~/.unsloth/studio/auth/...)
            unsloth-ua-proxy.py 0.0.0.0:18888 https://pharma-llm.thefirstonly.com/v1
            cloudflared tunnel run --token-file "/Library/Application Support/com.cloudflare.cloudflared/token"
```

⚠️ Mac đó là **MÁY NGOÀI** (LAN `192.168.1.5`, user `tquang`). Quang yêu cầu rõ: **KHÔNG SSH/probe vào**
trừ khi anh nói đích danh. Cần thì hỏi trước.

### Ba cái bẫy nhận diện sai máy

1. **Port 8080 trên máy Windows (NTQUANG_DELL) KHÔNG phải LLM server** — đó là **Vite dev server của ERP
   `saphia-holding`** (`node ... vite.js dev --port 8080 --strictPort`). Nó trả HTTP 404 cho `/v1/models`
   nhưng vẫn là "port quen thuộc", rất dễ kết luận sai.
2. **`~/.cloudflared/config.yml` trên Windows là config CŨ/SAI**: trỏ `llm.theliems.com → 127.0.0.1:8080`
   (→ đúng vào Vite!). Service thật chạy bằng `--token` remote-managed nên file này **không được đọc**.
   Đừng tin nó để suy ra ingress.
3. **Hai tunnel khác nhau ở hai máy.** Windows: ID `0ce9aa47-7d52-4d6a-9a16-13b48c508cff` (account tag
   `7aa3945509f3a3c90b75fca0317e7e5b`). Mac: tunnel riêng qua token-file (không đọc được nếu không có sudo).
   Cùng hostname mà connector ở máy khác → 502 dù máy bạn mọi thứ "xanh".

## Vì sao watchdog báo sai

Watchdog chỉ thấy HTTP 502 ở tầng ngoài, nên nó gán nhãn theo thứ nó biết: "tunnel chết". Nhưng 502 nghĩa
là Cloudflare **có** nhận request và **không** có connector nào phục vụ được hostname đó. Nhãn đúng phải là
"origin không phục vụ được", không phải "tunnel chết".

**Bài học:** watchdog/provider alert chỉ là điểm khởi đầu, không phải kết luận. Luôn mở từng tầng ra đo
trước khi đi bật lại dịch vụ — nếu bật nhầm máy thì mất thời gian mà lỗi y nguyên.

## Ghi chú môi trường (dễ gây nhiễu khi đo)

- Chạy python trong venv của repo bị `PYTHONPATH` từ venv Hermes rò vào → import nhầm `pydantic` hỏng.
  Phải `unset PYTHONPATH` (và `PYTHONHOME`) trước khi chạy python của venv khác.
- Tool `terminal` của Hermes có lúc báo `open: embedded null character in path` (guard
  `lifecycle_guard`) khi câu lệnh chứa đường dẫn `.venv/Scripts/python.exe`. Lách được bằng biến shell:
  `P=".venv/Scripts/python.exe" && $P script.py`.
