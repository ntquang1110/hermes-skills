---
name: multi-agent-council
category: software-development
description: >
  4-agent debate for evaluating ideas, papers, and deals.
trigger: |
  User says "đánh giá ý tưởng", "phản biện paper", "evaluate deal",
  "Claude Council", or asks multiple agents to debate a decision.
---

# Multi-Agent Council — Multi-Agent Debate for Decision Making

## Khi nào dùng

- User muốn đánh giá 1 ý tưởng kinh doanh / sản phẩm mới
- User muốn phản biện 1 bài báo khoa học / paper
- User muốn đánh giá 1 đối tác / deal / nhà đầu tư
- User muốn có nhiều góc nhìn khác nhau trước khi quyết định
- User nói "council" hoặc "multi-agent debate"

**KHÔNG dùng** khi user chỉ cần 1 câu trả lời đơn giản (tra cứu, tính toán, code).

## The Claude Council Pattern

Nguồn: TikTok @nateherkai (09/2026). Ý tưởng gốc: 4 Claude agent tranh luận về 1 ý tưởng kinh doanh, mỗi agent 1 góc nhìn khác nhau, Judge ra phán quyết cuối.

### 4 vai trò

| Vai trò | Góc nhìn | Prompt template |
|---------|----------|----------------|
| **Believer** | Lạc quan — tìm lý do ý tưởng thành công, ai sẽ mua, tại sao nó hoạt động | "Make the strongest case for why this idea could work and who would actually buy it." |
| **Skeptic** | Bi quan — công kích ý tưởng, tìm điểm yếu, lý do khách hàng không mua | "Attack the idea. Why customers won't pay and every weakness that hasn't been thought about." |
| **Investor** | Tài chính — phân tích dòng tiền, ROI, chi phí, rủi ro tài chính, cơ hội thị trường | "Look purely at whether this could actually make money and how realistic the opportunity is." |
| **Judge** | Trung lập — đọc 3 luồng tranh luận, tổng hợp, ra phán quyết cuối | "Read all three arguments and give a final verdict on whether to pursue this or not." |

### Cách hoạt động

```
User input (ý tưởng / paper / deal)
  ├── Believer → output
  ├── Skeptic  → output
  └── Investor → output
       └── Judge: đọc 3 outputs → verdict
```

**Luồng tuần tự:** 3 agent chạy song song (độc lập). Judge chạy sau khi có cả 3.

## Tích hợp với ai-company-v2

### Cách 1: delegate_task (nhanh, không cần agent registry)

```python
from hermes_tools import delegate_task

idea = "Sản phẩm TPBVSK hỗ trợ hô hấp cho heo..."

believer = delegate_task(goal="Believer: phân tích điểm mạnh của ý tưởng...", context=idea)
skeptic = delegate_task(goal="Skeptic: công kích ý tưởng, tìm điểm yếu...", context=idea)
investor = delegate_task(goal="Investor: phân tích tài chính, ROI...", context=idea)

# Chờ cả 3 xong, gửi Judge
judge_input = f"Believer: {believer}\nSkeptic: {skeptic}\nInvestor: {investor}"
verdict = delegate_task(goal="Judge: đọc 3 phân tích, ra phán quyết...", context=judge_input)
```

### Cách 2: Dùng ai-company-v2 registry (nếu đã setup agent roles)

```bash
# Tạo goal
python company.py goal add --type project --name "Product Council: RESP"

# Dispatch tuần tự
python company.py dispatch --to "Believer" --goal <ID> --context "..."
python company.py dispatch --to "Skeptic" --goal <ID> --context "..."
python company.py dispatch --to "Investor" --goal <ID> --context "..."
# CEO tự động chạy Judge sau khi có 3 outputs
```

### Cách 3: Một prompt duy nhất (gọn nhất)

Nếu không cần chạy song song, có thể dùng 1 prompt yêu cầu model tự đóng 4 vai:

```
Hãy đóng 4 vai để đánh giá ý tưởng sau:
1. Believer: điểm mạnh, ai sẽ mua
2. Skeptic: điểm yếu, tại sao không bán được
3. Investor: tài chính, ROI, chi phí
4. Judge: tổng hợp, phán quyết cuối

Ý tưởng: [nội dung]
```

Cách 3 nhanh nhất nhưng mất hiệu ứng "nhiều agent độc lập tranh luận".

## 3 Use Case chính

### Use Case 1: Product Council — đánh giá sản phẩm mới

Áp dụng cho Kiềm Saphia khi có ý tưởng TPBVSK mới (RESP, GUT, METRI, GROW...).

| Vai trò | Câu hỏi cụ thể |
|---------|----------------|
| Believer | Thị trường ngách nào? Ai cần sản phẩm này nhất? Tại sao họ mua? |
| Skeptic | Cạnh tranh thế nào? Giá cao hơn đối thủ? Chứng minh hiệu quả đủ mạnh? |
| Investor | Chi phí R&D? Giá vốn? Margin? Break-even? Scale được không? |
| Judge | Nên làm hay không? Nếu làm: ưu tiên gì trước? |

**Output:** HTML newsprint với 4 góc nhìn + verdict, publish lên preview.

### Use Case 2: Research Council — phản biện bài báo khoa học

Áp dụng cho Research Lab khi phân tích paper (như SpikingBrain analysis).

| Vai trò | Câu hỏi cụ thể |
|---------|----------------|
| Believer | Đóng góp khoa học là gì? Cái gì đáng học? Methodology có điểm mạnh? |
| Skeptic | Claim có thổi phồng không? Benchmark có fair không? Reproduce được không? |
| Investor | Chi phí áp dụng? Mất bao lâu? ROI nếu triển khai? |
| Judge | Nên tin bao nhiêu phần trăm? Có nên áp dụng không? |

### Use Case 3: Deal Council — đánh giá đối tác

Kết hợp với `business-deal-evaluation` skill.

| Vai trò | Câu hỏi cụ thể |
|---------|----------------|
| Believer | Điểm mạnh của đối tác? Cơ hội hợp tác? Tại sao nên ký? |
| Skeptic | Rủi ro? Cờ đỏ? Điều khoản bất lợi? Từng thất bại? |
| Investor | Dòng tiền? Margin? Scale được không? Cam kết tài chính? |
| Judge | Nên ký hay không? Nếu ký: điều kiện gì? |

## Output format

Mặc định: HTML dùng 1 trong 45 design system từ Template Gallery.

| Use case | Design gợi ý | Lý do |
|----------|-------------|-------|
| Product Council | Duolingo (light, playful) | Dễ đọc, màu sắc rõ |
| Research Council | Vellum (dark, scholarly) | Academic tone |
| Deal Council | Monochrome (restrained, archival) | Nghiêm túc, ledger feel |

## Lưu ý khi chạy Council

### Pitfall: Believer vs Skeptic bias
Mặc định model có xu hướng làm Believer tốt hơn Skeptic (vì RLHF alignment). Nếu Skeptic quá yếu, thêm prompt: "Be aggressive. Find every possible flaw."

### Pitfall: Judge bị ảnh hưởng bởi độ dài
Judge dễ bị thuyết phục bởi luồng dài hơn, không phải luồng đúng hơn. Cân nhắc: yêu cầu Judge tóm tắt từng luồng trước khi phán quyết.

### Pitfall: Cost
Council chạy 4 LLM calls cho 1 lần đánh giá. Với ByteDance DeepSeek v4-flash: ~20K tokens × 4 = 80K tokens ≈ 0.3s latency mỗi call. Chi phí ~2-3K VND/lần.

### Pitfall: Không có người thật
Council chỉ là AI đánh giá AI. Không thay thế được validation thực tế (pilot, phỏng vấn khách hàng). Dùng Council để sàng lọc trước, không thay thế quyết định cuối.

## Reference

- `references/claude-council-tiktok.md` — TikTok gốc từ @nateherkai, Claude Council 4-agent pattern
- `references/spikingbrain-analysis.md` — Ví dụ Research Council: phân tích SpikingBrain paper
- `references/product-council-kiem-saphia.md` — Mẫu Product Council cho Kiềm Saphia

## Related Skills

| Skill | Khi nào dùng |
|-------|-------------|
| `business-deal-evaluation` | Deal Council: bộ câu hỏi xuyên thấu + đánh giá đối tác |
| `design-critique` | Product Council: critique-first methodology |
| `system-design-workflow` | Kết hợp Council vào system design workflow |
| `ai-company-ops` | Chạy Council qua ai-company-v2 agent registry |
