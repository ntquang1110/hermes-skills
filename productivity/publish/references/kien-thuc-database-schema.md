# Notion "Kiến thức" Database — Full Schema

*Captured 2026-07-01*

## IDs

| Type | ID |
|------|-----|
| Database ID | `38aee73e-673a-800e-b564-c2fc25c58097` |
| Data Source ID | `38aee73e-673a-8009-9e03-000bb99afbf8` |
| Database URL | `https://app.notion.com/p/38aee73e673a800eb564c2fc25c58097` |

## Properties

### Name (title)
- Property ID: `title`
- Type: title

### Chuyên ngành (select)
- Property ID: `ECoN`
- Options:

| Name | Option ID | Color |
|------|-----------|-------|
| Sinh học | `c423e881-680a-4aa8-b92e-0e7036647698` | orange |
| Chăn nuôi | `63263490-f27b-44e3-b12d-74bee3992c76` | default |

### Phân loại (select)
- Property ID: `WVA%7C`
- Options:

| Name | Option ID | Color |
|------|-----------|-------|
| Tên lửa | `868c75a2-58f7-4170-858a-9e9365aeaaf9` | default |
| Virus | `f753fe65-6a18-48e1-9b19-eafed87b8c06` | orange |
| Tế bào | `2abc77e1-c34a-4dc6-a6ed-0f0e92d8c069` | yellow |
| Sản xuất | `30b59d0a-7a7a-4c11-a18a-bfb4290ed648` | pink |
| Bệnh học | `895c21fa-1971-49c0-b023-3eb9152b96bd` | brown |

### Link (rich_text)
- Property ID: `eSbq`
- Type: rich_text (URL preview links)

## Current Entries (6)

| # | Name | Chuyên ngành | Phân loại |
|---|------|-------------|-----------|
| 1 | Phân đen trong lợn | Chăn nuôi | Bệnh học |
| 2 | Quy trình sản xuất cám | Chăn nuôi | Sản xuất |
| 3 | Tế bào | Sinh học | Tế bào |
| 4 | Cách thức tế bào tương tác với virus | Sinh học | Virus |
| 5 | H9N2 tương tác với tế bào | Sinh học | Virus |
| 6 | Tên lửa | — | Tên lửa |

## API Query Example

```python
import requests

headers = {
    'Authorization': f'Bearer {NOTION_API_KEY}',
    'Notion-Version': '2025-09-03',
    'Content-Type': 'application/json'
}

# Query all entries
resp = requests.post(
    'https://api.notion.com/v1/data_sources/38aee73e-673a-8009-9e03-000bb99afbf8/query',
    headers=headers, json={'page_size': 100}
)
```

## Create Entry Example

```python
payload = {
    'parent': {'database_id': '38aee73e-673a-800e-b564-c2fc25c58097'},
    'properties': {
        'Name': {'title': [{'text': {'content': 'Article Title'}}]},
        'Link': {'rich_text': [{'text': {'content': 'https://htmlpreview.github.io/?...'}}]},
        'Chuyên ngành': {'select': {'name': 'Sinh học'}},
        'Phân loại': {'select': {'name': 'Virus'}}
    }
}
resp = requests.post('https://api.notion.com/v1/pages', headers=headers, json=payload)
```
