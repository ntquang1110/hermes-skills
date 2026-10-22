# Unsloth Studio served models — đo thật 2026-08 (gemma/Qwen/Ministral/LFM)

Bối cảnh: user muốn tối ưu token bằng cách đẩy tác vụ nhẹ sang model local (qua
Unsloth Studio, 1 máy GPU 6GB VRAM GTX 1660 Super, expose qua trycloudflare
tunnel). Mục tiêu tiết kiệm chi phí OpenCode/DeepSeek API vốn bị run-out-limit.

## Điểm quyết định: hardware 6GB không chạy nổi 27B

- Qwen 27B Q4 cần ~16GB VRAM. Máy 6GB → offload gần hết CPU → 1-3 tok/s, không đáng.
- Model đáng dùng cho 6GB: 7-8B Q4 (~5GB) hoặc 4B (~3GB). Gemma 12B Q4 (~7GB) hơi tràn.
- Kiểm tra GPU thật bằng `wmic path win32_VideoController get name,AdapterRAM`
  (nvidia-smi không luôn tồn tại trên máy này). Đừng tin lời user về model card —
  đo /v1/models mới chuẩn.

## Test 4 model qua cùng tunnel (stream:true, prompt tiếng Việt giới thiệu Kiềm Saphia)

| Model | TTFB/thời gian | Reasoning | Tiếng Việt | Context serve | Qua Hermes? |
|-------|---------------|-----------|------------|---------------|-------------|
| gemma-4-12b (UD-Q2_K_XL) | 42-215s | 1300-6600 ký tự | sai "Kiềm"→"Kiêm" | — | ❌ (chậm + sai dấu) |
| Qwen3-VL-8B (Q3_K_S) | ~10s | 0 | chuẩn, gọn | **4096** | ❌ (<64K) |
| Ministral-3-8B | ~14s | 0 | chuẩn, trôi | không báo | ⏳ |
| LFM2.5-8B-A1B | ~14s | 1597 | ok nhưng sáo rỗng | không báo | ⏳ |

Rút ra:
- Model "reasoning" (gemma-4) sinh reasoning_content dài trước đáp án → content
  rỗng khi max_tokens nhỏ, token/độ trễ phình. Bỏ max_tokens hẳn (stream) để
  content hoàn chỉnh, nhưng call ~3.5 phút cho tóm tắt 1 transcript ngắn.
- Q2_K_XL quantize SAI tiếng Việt đồng âm: "Kiềm Saphia"→"Kiêm Saphia",
  "bò và gia cầm"→"bô và giá cam". → không dùng cho content tiếng Việt chính chủ.
- Qwen3-VL-8B nhanh nhất + tiếng Việt sạch, nhưng Unsloth báo context 4096
  (native 262144 nhưng serve limit 4096) → Hermes hard-chặn (<64K).
- `switch by request` đã bật nhưng các model chưa nạp vẫn trả model_not_found.

Kết luận truyền cho user: đa số model Unsloth qua tunnel KHÔNG đạt 64K Hermes
cần, và quantize thấp hỏng tiếng Việt. Đường thật: Ollama local chạy Qwen3 8B
(báo context 128K) hoặc giữ API + chia thớ task (local nén/format, API viết final
+ citation). Tốc độ/chi phí phải đo thật, không tin ergo.

## Lệnh test mẫu (Windows bash + curl)

```bash
# body phải file UTF-8 heredoc CÓ nháy, --data-binary @C:/path (không /tmp)
cat > body.json <<'EOF'
{"model":"unsloth/Qwen3-VL-8B-Instruct-GGUF","stream":true,
 "messages":[{"role":"user","content":"Viết 2 câu giới thiệu công ty Kiềm Saphia."}]}
EOF
curl -sS -N -m 170 "$URL/v1/chat/completions" \
  -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" \
  --data-binary @body.json -o out.txt
# đo thời gian: s=$(date +%s%3N) ... e=$(date +%s%3N); echo $((e-s))ms
```

Chú ý: gemma-4-12b là reasoning model — phải stream (non-stream bị CF 524) và
đừng set max_tokens nhỏ nếu muốn content. Đo TTFB + token/s + reasoning_chars
trước khi quyết định chấp nhận model.

## Follow-up: chọn Ministral, domain ỔN ĐỊNH qua HTTP, và chia 4 cron

Sau vòng đo đầu, tiến xa hơn — kết quả chốt (đo thật 2026-08):

**1. So sánh bài tâm lý sâu 5 phần (cùng prompt, 3 model):** Ministral thắng — tiếng
Việt GẦN NHƯ 100% chuẩn (không lỗi dấu), gọi đúng thuật ngữ khoa học (burnout,
social comparison, FOMO, fight-or-flight, neural fatigue, dopamine depletion),
giải pháp gắn vào cơ chế. QwenVL chuẩn dấu nhưng lặp ý ("trình diễn"×5). LFM nhanh
nhất (20s) nhưng SAI tiếng Việt nhiều ("taymi", "choáng nản", "trớt mất"). → **chọn
Ministral cho content tiếng Việt.** QwenVL = backup, LFM = loại.

**2. Domain ổn định ≠ tunnel tạm.** User cấp `pharma.llm.thefirstonly.com` (trỏ cùng
Unsloth server) — **phải gọi qua HTTP, KHÔNG HTTPS**: HTTPS bị `SEC_E_ILLEGAL_MESSAGE`
(handshake fail) vì service bind HTTP. `http://pharma.llm.thefirstonly.com/v1` →
200. Đây là endpoint bền (địa chỉ cố định), thay thế `*.trycloudflare.com` đổi mỗi
lần. Chuyển `custom_providers` + `model_aliases` + watchdog URL về đây.

**3. Ministral serve context vẫn 4096** (native 262144) — như skill body đã ghi:
override context_length trong config qua được rào 64K Hermes, nhưng server vẫn
reject lúc call ("Message too long: 22040 tokens exceeds 4096"). Must nâng context
serve trên Unsloth Studio cho đúng model đang load.

**4. Cloudflare chặn UA `OpenAI/Python` → 403.** Fix: `extra_headers: {User-Agent:
curl/8.0}` trong entry custom_providers. Chi tiết → skill body.

**5. Chia cron đúng hướng "từng bài 1".** Job tâm lý local: bỏ hết skill nặng
(web-research/visual-academic-html/html-publishing/dashboard-design-system) — chúng
làm prompt dài → overflow. Cấu trúc 5 phần chuẩn của user: **ví dụ → nêu vấn đề →
gốc rễ → first principle → giải pháp**, mỗi phần 1 đoạn, gọi tên cơ chế khoa học
(dopamine, cortisol, PFC, amygdala). Tách **4 job nhỏ lệch giờ** (6h/10h/14h/18h),
mỗi job 1 bài, model Ministral, text thuần (không HTML). Job cũ 6 bài deepseek +
4 skill → PAUSE.