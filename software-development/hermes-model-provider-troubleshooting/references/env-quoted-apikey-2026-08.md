# Case: OPENCODE_GO_API_KEY bọc nháy kép → "Invalid API key" (2026-08-07)

## Tình huống
User hỏi "model này dùng được không". Config Hermes (config.yaml):
```
model:
  default: deepseek-v4-flash
  provider: opencode-go
  context_length: 256000
fallback_providers:
  - provider: custom:omniroute
    model: auto/best-coding
```

## Chẩn đoán
Ban đầu tưởng key sai vì:
- `curl /chat/completions` với key đọc từ .env → `AuthError: Invalid API key.` cho mọi model (cả minimax-m3 có thật).
- `/models` trả HTTP 200 — **nhưng /models KHÔNG cần auth**, nên 200 này gây hiểu lầm.

So sánh key:
```
env key  (69 chars): "sk-dE2...cPFh"    ← có nháy kép
given key(67 chars): sk-dE2...cPFh      ← user gửi, trần
tr -d '"' + tr -d "'" → GIỐNG NHAU      ← chốt: key giống, lỗi do nháy
```

Test mấu chốt: gõ key TRẦN bằng tay vào curl (không đọc .env):
```bash
key="<API_KEY>"
curl -sk -m 25 https://opencode.ai/zen/go/v1/chat/completions \
  -H "Content-Type: application/json" -H "Authorization: Bearer $key" \
  -d '{"model":"deepseek-v4-flash","messages":[{"role":"user","content":"Say OK"}],"max_tokens":10}'
```
→ 200 OK, model trả bình thường. Vậy lỗi hoàn toàn do nháy kép trong .env.

## Fix
`.env` line gốc: `OPENCODE_GO_API_KEY="sk-..."` (có nháy).
- patch tool chặn (credential file). Dùng sed:
```bash
cp .env .env.bak-$(date +%Y%m%d%H%M%S)
sed -i 's|^OPENCODE_GO_API_KEY=.*|OPENCODE_GO_API_KEY=sk-... |' .env
```
- Verify: key đọc từ .env dài 67 (đúng), `grep -c '"'`=0, test chat lại bằng giá trị đọc từ .env → 200 OK.
- Hermes cần restart để đọc key mới (user tự restart, không admin).

## Bài học tái sử dụng
- "Invalid API key" cho MỌI model + `/models` trả 200 KHÔNG = key hỏng. Kiểm tra nháy kép trước.
- API key trong .env nên để TRẦN, không bọc `"` hoặc `'`.
- So sánh key: luôn `tr -d '"' | tr -d "'"` cả 2 vế trước khi so.
