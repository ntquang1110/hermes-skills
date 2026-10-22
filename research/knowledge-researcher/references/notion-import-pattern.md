# Notion → Knowledge Flow Import Pattern  

## DB Structure  

Database "Kiến thức" (ID: `38aee73e-673a-800e-b564-c2fc25c58097`):  

- **Name** (title) — title (may have emoji prefix)  
- **Chuyên ngành** (select) → maps to `topic_slug`  
- **Phân loại** (select) — Phương pháp, Định nghĩa, Sản xuất, Bệnh học...  
- **Link** (rich_text) — HTML preview URL (GitHub Gist)  

## Import Steps  

1. `POST /v1/databases/{id}/query` page_size=100 → get all items  
2. Map Chuyên ngành → topic_slug:  

   Vật lý → `vat-ly`, Chăn nuôi → `chan-nuoi`, AI → `ai-ml`  
   Nghiên cứu → `nghien-cuu`, Sinh học → `sinh-hoc`, Xét nghiệm → `xet-nghiem`  
   (empty) → `tong-hop`  

3. Fetch HTML từ Link nếu có, extract text content (5000 chars max)  
4. POST `/api/knowledge` với `{title, content, summary, topic_slug, tags, source_url}`  

## Content Extraction from GitHub Gist HTML  

Link format: `https://htmlpreview.github.io/?https://gist.githubusercontent.com/{user}/{gist_id}/raw/{hash}/index.html`  

Extract raw URL via regex: `(https://gist\.githubusercontent\.com[^#?]+)`.  

```python
import re, urllib.request
resp = urllib.request.urlopen(raw_url, timeout=15)
html = resp.read().decode('utf-8', errors='replace')
text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
text = re.sub(r'<[^>]+>', ' ', text)
text = re.sub(r'\s+', ' ', text).strip()[:5000]
```

## Research Queue Integration  

After import, items can also be queued for deeper research via `/api/research-queue`:  

- `POST` with `{topic, detail, topic_slug}` → status `pending`  
- Cron (9am daily) picks pending item → research → import card → status `done`  

## Pitfalls  

### Vietnamese Encoding  

**Symptom:** Card created with missing diacritics: "Co che tac dung" instead of "Cơ chế tác dụng".  

**Cause:** LLM output defaults to ASCII-only Vietnamese. The cron prompt must explicitly require diacritics.  

**Fix:**  
1. Add to cron prompt: `VIẾT TIẾNG VIỆT CÓ DẤU ĐẦY ĐỦ. Title, summary, content đều phải có dấu.`  
2. Use Python for import scripts — it handles Unicode via `json.dumps().encode('utf-8')` deterministically  

### Node.js fetch Unicode Bug  

Node.js `fetch()` on MSYS2/Git Bash mishandles Vietnamese characters in JSON responses → "Empty or invalid json".  

**Fix:** Use Python `urllib.request` instead.  

### RLS Blocks INSERT/DELETE  

New tables need EXPLICIT RLS policies:  

```sql
CREATE POLICY "insert_{table}" ON {table} FOR INSERT WITH CHECK (true);
CREATE POLICY "delete_{table}" ON {table} FOR DELETE USING (true);
```

Missing DELETE policy → cleanup scripts silently fail (200 response but no rows deleted).  

### Duplicate Prevention  

Import script running twice → 18 duplicate cards on 23 items.  

**Fix:**  
1. Query Supabase REST to find duplicates (group by title, keep newest)  
2. DELETE older duplicates via `DELETE /rest/v1/knowledge_cards?id=eq.{id}`  
3. Need DELETE RLS policy first  

### Card Topic Linking  

Cards from Notion have `topic_id: null` because topics aren't in DB.  

**Workaround:** Filter by `tags` column instead of FK join:  
```tsx
.contains("tags", ["Vật lý"])   // Supabase filter
```

Book view groups by `c.tags[0]` when `c.topics` join = null.
