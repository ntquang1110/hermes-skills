---
name: field-map
description: "Build a comprehensive field knowledge map with KPI cards: break any domain into specialties, topics, terms, current frontier, and scientific challenges. Renders as interactive HTML with expandable tree + KPI metrics."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [knowledge, kpi, tree-map, mind-map, field-analysis, research]
    related_skills: [publish, html-unslop]
---

# Field Map (field-map)

Vẽ bản đồ toàn cảnh của một lĩnh vực — từ tổng quan đến chuyên sâu, kèm KPI cho mỗi nhánh.

## When to Use

- User muốn hiểu **một ngành từ gốc** — cấu trúc cây, chuyên ngành, chủ đề
- User muốn **KPI định lượng** cho từng chuyên ngành (bao nhiêu chủ đề, thuật ngữ)
- User muốn biết **frontier research** và **rào cản khoa học** của từng chuyên đề
- User muốn học một lĩnh vực mới nhưng có hệ thống, không học vẹt

## Output Format

Một HTML page với:

```
🏠 Hero: tổng quan + KPI toàn ngành
├── 📊 KPI global: số chuyên ngành, chủ đề, thuật ngữ
│
├── 🛡️ Chuyên ngành 1
│   ├── 📊 KPI card: số chủ đề, số thuật ngữ
│   ├── 🎯 Mục đích của chuyên ngành
│   ├── 📖 Hiểu cơ bản (basic concept)
│   ├── 🚀 Frontier research hiện tại
│   ├── 🧱 Rào cản khoa học
│   └── 📌 Chủ đề con (expandable)
│       ├── Tổng quan
│       ├── Nghiên cứu sâu nhất
│       └── Rào cản khoa học
│
├── ⚠️  Chuyên ngành 2 (tương tự)
└── ...
```

## Workflow

### Bước 1: Agent phân tích field

Dựa trên kiến thức của agent, xây dựng cấu trúc JSON:

```json
{
  "field": "Tên lĩnh vực",
  "root_definition": "Định nghĩa gốc — bản chất của ngành này là gì?",
  "total_specialties": 6,
  "total_topics": 25,
  "total_terms": 128,
  "specialties": [
    {
      "id": "unique-id",
      "name": "Tên chuyên ngành",
      "icon": "🛡️",
      "color": "#38bdf8",
      "topic_count": 5,
      "term_count": 28,
      "purpose": "Mục đích — tại sao có chuyên ngành này?",
      "basic_concept": "Cốt lõi cần hiểu — 2-3 câu",
      "current_frontier": "Nghiên cứu sâu nhất hiện tại là gì? Có gì mới?",
      "challenges": "Vấn đề lớn chưa giải quyết được",
      "subtopics": [
        {
          "name": "Tên chủ đề con",
          "term_count": 6,
          "overview": "Tổng quan chủ đề",
          "current_research": "Frontier của chủ đề này",
          "challenges": "Rào cản riêng"
        }
      ]
    }
  ]
}
```

### Bước 2: Render HTML

```bash
python scripts/render-field-map.py --data data.json --output map.html
```

Script sinh HTML với:
- KPI banner cho toàn field
- Card cho từng chuyên ngành (click để mở)
- Sub-topic expandable bên trong
- Màu sắc phân biệt từng ngành

### Bước 3: Unslop + Upload + Preview

Sau khi render, tự động strip AI-isms rồi upload qua skill `publish`:

```bash
# Hoặc qua publish skill (auto unslop + KV upload)
python scripts/content-upload.py --file map.html --title "Field Map"
# → https://preview.thefirstonly.com/<id>
```

## Quick Reference — Các trường JSON

| Trường | Bắt buộc | Ý nghĩa |
|--------|----------|---------|
| `field` | ✅ | Tên lĩnh vực (rõ ràng) |
| `root_definition` | ✅ | Bản chất cốt lõi — 1-2 câu |
| `specialties[].name` | ✅ | Tên chuyên ngành |
| `specialties[].purpose` | ✅ | Tại sao có chuyên ngành này? |
| `specialties[].basic_concept` | ✅ | Cốt lõi cần hiểu |
| `specialties[].current_frontier` | ✅ | Đi sâu nhất hiện tại |
| `specialties[].challenges` | ✅ | Rào cản khoa học |
| `subtopics[].overview` | ✅ | Tổng quan chủ đề |
| `subtopics[].current_research` | ✅ | Frontier của chủ đề |
| `subtopics[].challenges` | ✅ | Rào cản riêng |
| `topic_count`, `term_count` | ✅ | Số liệu KPI |

## Scripts

- `scripts/render-field-map.py` — render JSON → HTML interactive page
- `references/immunology-data.json` — example: miễn dịch học

## Common Pitfalls

1. **Dữ liệu không đủ depth.** Mỗi chuyên ngành cần ít nhất 3-5 chủ đề con. Agent cần tự fill đầy dựa trên domain knowledge.
2. **Term count ước lượng.** Không cần chính xác tuyệt đối — mục đích là cho perspective về khối lượng.
3. **Frontier quá chung chung.** Cần research cụ thể: tên paper, công nghệ, kết quả clinical trial. Tránh "đang được nghiên cứu".
4. **JSON syntax error.** Validate kỹ trước khi render. Dùng `json.dumps(data, indent=2, ensure_ascii=False)`.
5. **HTML >1MB.** Gist giới hạn. Nếu field quá lớn, chia làm nhiều page.
6. **Icon + color.** Chọn icon và color phù hợp với bản chất từng chuyên ngành để dễ phân biệt.

## Verification Checklist

- [ ] JSON có đủ `field`, `root_definition`, `specialties[]`
- [ ] Mỗi specialty có đủ purpose, basic_concept, frontier, challenges
- [ ] Mỗi subtopic có overview, research, challenges
- [ ] Topic/term count khớp với thực tế
- [ ] HTML render không lỗi
- [ ] Preview URL hoạt động trên mobile
- [ ] Từng specialty card click mở/đóng được
- [ ] Từng subtopic click mở/đóng được

## Related Skills

- `content-publish` — upload HTML lên preview.thefirstonly.com
- `md-publish` — tạo tree map dạng markdown trước
