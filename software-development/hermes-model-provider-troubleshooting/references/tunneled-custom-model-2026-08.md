# Tunneled custom model endpoint — test thật 2026-08 (Unsloth Studio gemma-4-12b)

Probe một model third-party sau Cloudflare tunnel (`*.trycloudflare.com`), OpenAI-compatible.
Kết quả đo thật để làm benchmark chuẩn cho lần sau.

## Setup

- Endpoint: `https://<tunnel>.trycloudflare.com/v1/chat/completions`
- Auth: `Authorization: Bearer sk-...` (Unsloth Studio key)
- Model: `unsloth/gemma-4-12b-it-GGUF:UD-Q2_K_XL`
- Server `/v1/models` KHÔNG cần auth (public) → HTTP 200 ko chứng minh key.
  Phải test `/chat/completions` mới biết key đúng. Key placeholder bị từ chối rõ ràng:
  `{"error":{"message":"This is the placeholder key from the example. Create an API key in Unsloth Studio under Settings > API..."}}`

## Số liệu đo thật

| Test | Kết quả |
|------|---------|
| Auth OK (key thật) | ✅ chat completion 200 |
| Non-stream, max_tokens 60 | 16s, `completion_tokens:60` nhưng `content:''`, `finish:length` — toàn bộ vào `reasoning_content` |
| Non-stream, max_tokens 900 | **HTTP 524 sau 125s** (Cloudflare timeout) |
| Non-stream, max_tokens 400 | 42s, content ra 3 câu nhưng bị cut (`length`), reasoning ~1256 chars |
| **stream:true**, max_tokens 600 | 42.5s, content ĐỦ 3 ý trọn vẹn, reasoning 1356 chars — không timeout |

## Kết luận vận hành

1. **SAU CF tunnel bắt buộc stream:true** — non-stream chờ full response bị 524.
   Stream tính timeout theo byte đầu → thoát timeout. Đây là điều kiện tiên quyết.
2. **Model reasoning tự sinh 1300+ chars trước đáp án** dù system prompt cấm.
   → content rỗng khi max_tokens nhỏ; phải kéo max_tokens cao; mỗi call tốn ~40s.
3. **Q2_K_XL quantize**: tiếng Việt ra tạm được nhưng bấp bênh dấu → vi phạm rule
   "Viet content MUST có dấu". Muốn chuẩn → Q4+ hoặc chỉ dùng cho output Anh/JSON.
4. **Tunnel trycloudflare là tạm** — tự tắt khi ngừng; không dùng làm prod endpoint.

## Lệnh curl mẫu (Windows bash, chuẩn để tránh lỗi dấu)

```bash
# Body ghi ra file UTF-8 bằng heredoc CÓ nháy (giữ dấu tiếng Việt)
cat > body.json <<'EOF'
{"model":"unsloth/gemma-4-12b-it-GGUF:UD-Q2_K_XL","stream":true,
 "messages":[{"role":"user","content":"Viết 3 câu giới thiệu con lợn, đủ dấu."}],
 "max_tokens":600}
EOF

# KHÔNG dùng /tmp (curl.exe Windows không thấy) — dùng C:/... thật
url="https://...trycloudflare.com"
curl -sS -N -m 170 "$url/v1/chat/completions" \
  -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" \
  --data-binary @C:/path/body.json -o C:/path/out.txt
```

Parse stream: đọc từng dòng `data: `, mỗi dòng JSON, cộng `choices[0].delta.content`
bỏ qua `delta.reasoning_content`; kết thúc ở `data: [DONE]`.

## Nếu model chậm — đừng cố đẩy mọi task

- Chỉ dùng cho bước tiền xử lý/nén (raw draft) hoặc output ngắn 1-call, chạy nền cron.
- Định giá mỗi call BẰNG reasoning (không chỉ đáp án) — token phình 2-3x.
- Nếu user có GPU, khuyên Ollama Qwen 7-8B Q4 (không reasoning-token giả, TTFB nhanh,
  tiếng Việt ổn) thay vì Q2 reasoning-model qua tunnel. 6GB VRAM không chạy nổi Qwen 27B.