# Tạo Standalone Page & Embed Gist Preview

Use when the user wants a **new Notion page** (not a database entry) with markdown content + embedded Gist preview links.

## Workflow

```
Bước 1: Xác định parent page (hoặc workspace root → dùng page_id của root page)
Bước 2: Tạo page với POST /v1/pages + markdown body
Bước 3: Update content với PATCH /v1/pages/{id}/markdown (nếu cần sửa)
```

## 1. Create a new page with markdown

```python
payload = {
    "parent": {"page_id": "parent_page_uuid"},
    "properties": {
        "title": {"title": [{"text": {"content": "Page Title"}}]}
    },
    "markdown": "# Heading\n\nContent..."
}

POST /v1/pages
```

**Note:** `parent: {"type": "workspace"}` does NOT work — must use a real `page_id`.

## 2. Update page content (PATCH markdown)

The endpoint `PATCH /v1/pages/{page_id}/markdown` has strict validation. The **working format** (tested with Notion-Version: 2022-06-28):

```python
payload = {
    "type": "insert_content",
    "insert_content": {
        "position": {"type": "start"},   # MUST be object, not string "start"
        "content": "## New Section\n\nContent..."  # key is "content", NOT "markdown"
    }
}
```

### Accepted `type` values
| Type | Purpose |
|------|---------|
| `insert_content` | Insert at position (start/end) |
| `update_content` | Replace with `content_updates` array |
| `replace_content_range` | Replace a range |

### Common mistakes
- ❌ `position: "start"` (string) → should be `position: {"type": "start"}` (object)
- ❌ `"markdown": "..."` inside insert_content → should be `"content": "..."`
- ❌ `type: "replace_content"` → not available in v2022-06-28; use `update_content`

## 3. Embedding Gist preview links

After uploading HTML to a Gist, add the preview URL to the Notion page:

```markdown
🔗 **Preview:** https://htmlpreview.github.io/?https://gist.githubusercontent.com/USER/GIST_ID/raw/COMMIT/index.html
📁 **Gist gốc:** https://gist.github.com/USER/GIST_ID
```

Notion's markdown auto-converts bare URLs to clickable links, or you can use markdown link syntax.

## Parent page discovery

List root-level pages to find a parent:

```python
POST /v1/search
{"query": "", "page_size": 50}
# Filter results where parent.type == "workspace"
```
