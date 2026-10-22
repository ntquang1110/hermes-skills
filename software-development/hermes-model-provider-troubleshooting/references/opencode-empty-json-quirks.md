# OpenCode endpoint quirks — empty 200 + JSON (2026-08)

Nguồn: debug summarize pipeline TFO (app/main.py → hub/store.call_deepseek
→ https://opencode.ai/zen/go/v1/chat/completions, model deepseek-v4-flash/pro).

## Quirk 1: HTTP 200 nhưng content RỖNG (~40-50% số lần)

- Với input dài (hệ thống + user content tổng > ~5000 chars), endpoint trả
  `status=200` với `choices[0].message.content = ''` — KHÔNG phải timeout,
  không phải network error. Không theo quy luật độ dài rõ ràng: test 1000-4000
  chars rỗng, 5000 chars OK ở lần khác.
- Kết quả đo: content ngắn (1 dòng) → 5/5 OK. Content 2000 chars → 3/5 OK,
  2/5 rỗng. Content 5000 chars + system dài → thường rỗng.
- → **Bắt buộc retry loop** khi content rỗng (không chỉ khi HTTP != 200):
  ```python
  content = data["choices"][0]["message"]["content"]
  if not content or not content.strip():
      for attempt in range(3):
          resp2 = requests.post(URL, json=payload, timeout=180)
          if resp2.status_code == 200:
              content = resp2.json()["choices"][0]["message"]["content"]
              if content and content.strip():
                  break
  ```
- Retry ở tầng gọi riêng (4 lần) vẫn cần nếu lỗi xuất hiện ở bước thứ cấp.

## Quirk 2: `response_format={"type":"json_object"}` → LUÔN trả rỗng

- Test thực tế: cùng input, bật response_format json_object → content rỗng
  (cả retry). Bỏ response_format, chỉ ép JSON bằng prompt → model trả JSON
  chuẩn (1308 chars, đủ summary/issues/decisions/tasks).
- → **KHÔNG dùng response_format với endpoint này.** Ép JSON bằng prompt:
  "OUTPUT: CHỈ JSON thuần, KHÔNG markdown, KHÔNG code fence. Bắt đầu bằng {."

## Quirk 3: tổng prompt (system + input) vượt ngưỡng → rỗng

- System dài + input 5000 chars → rỗng. System ngắn + input 5000 → OK.
- → Chunk input nhỏ (3500 chars/đoạn), system prompt NGẮN gọn cho bước trung
  gian; bước JSON cuối chỉ nhận output ngắn (< 4000 chars).

## Quirk 4: model trả markdown thay vì JSON khi input dài

- Khi input dài, model đôi khi trả markdown dù prompt yêu cầu JSON.
- → Xử lý 2 bước: (1) summarize ra text ngắn, (2) ép JSON lại trên chính
  output ngắn đó với retry loop tối đa 4 lần, kiểm tra `result.strip().startswith("{")`.

## Pattern tóm tắt dài (đã chạy OK)

```
transcript dài → chunk 3500 chars + overlap 200 → summarize từng chunk (system NGẮN)
→ gom partials (cắt ≤ 4000) → _summarize_single:
    call JSON-prompt (không response_format) → nếu bắt đầu "{" return
    nếu markdown → ép lại với output ngắn (retry 4x) → nếu vẫn không: return markdown
```

## Pitfall: timeout

- requests timeout=60 không đủ cho prompt dài + pro model → tăng 180.
