# Notion API Version Quirks

## Key Finding: 2022-06-28 is the most reliable version
Newer versions (`2025-09-03`) return `401: API token is invalid` for tokens that work fine with `2022-06-28`.

## Always verify against live API before assuming key is bad
1. Test with minimal call: `GET /users` — if 200, auth is fine
2. Test with `GET /databases/{id}` — if 200, integration has access
3. Only after both pass should you debug schema issues

## Schema Discovery Pattern
```python
# Get database schema
r = await client.get(f'/databases/{DB_ID}')
props = r.json().get('properties', {})
for name, p in props.items():
    print(f"  {name}: {p.get('type')}")
```

## Common Pitfalls
- Property types: `status` ≠ `select`, `title` ≠ `rich_text`
- The primary display column is always `"title"` type in properties, but the NAME varies per database
- API version `2025-09-03` requires token format that older Notion tokens don't support
- `POST /databases/{id}/query` needs a non-empty JSON body (`{"page_size": 1}` minimum)
- `POST /search` with filter `{"filter": {"value": "database", "property": "object"}}` discovers all accessible databases

## Error to Action Mapping
| Error | Likely Cause | Fix |
|-------|-------------|-----|
| 401 "API token is invalid" | Wrong API version for this token | Try `2022-06-28` |
| 401 "API token is invalid" | Token actually bad | Re-create integration |
| 400 "validation_error" | Property name/type mismatch | GET schema first |
| 400 "invalid_request_url" | Wrong endpoint format | Check path |
| 404 | Integration not shared with DB | Add connection in Notion |
