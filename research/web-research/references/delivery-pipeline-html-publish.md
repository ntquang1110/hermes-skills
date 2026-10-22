# Delivery pipeline: Research → HTML → Publish → KFlow (+ multi-level pattern, persona, Sườn workflow)

### Default delivery pipeline: Research → HTML → Publish → KFlow

**This is the user's default expectation.** Unless the user explicitly asks for a different format, follow this pipeline after every research session:

```
Phase 1: RESEARCH
  → Wikipedia API (Level 2a) + PubMed E-utilities (Level 2c)
  → Gather structured data with citations (PMID, DOI, journal)

Phase 2: HTML OUTPUT
  → Format as comprehensive single-file HTML with Premium B/W/Y design system
    (var(--yellow): #FFD600, var(--black): #0D0D0D, var(--bg): #1B1B1D, var(--card): #242428)
  → Use: cards with rounded corners (28px), tables with alternating rows, reference boxes,
    summary quote boxes with left yellow border, responsive grid, stat boxes
  → Every scientific claim gets a citation in a ref-box (blue left border, PMID/DOI)
  → For complex topics: multi-level explanation (cơ bản → nâng cao)

Phase 3: PUBLISH
  → POST file content to https://preview.thefirstonly.com/api/store
  → curl -s -X POST "https://preview.thefirstonly.com/api/store" \
      -H "Content-Type: application/json" \
      -d '{"content":"<html>...</html>","title":"Research Title"}'
  → Get preview_url from response → share with user

  **⚠️ Pitfall — Python `urllib` returns 403 Forbidden on preview service:** The `preview.thefirstonly.com` API endpoint rejects Python `urllib.request` (HTTP 403) even with a standard browser User-Agent header. The same request from `curl` succeeds. **Fix:** always use `curl` (not Python `urllib`) for this endpoint. If you need processing logic, write the JSON payload with `write_file` and POST via `curl -d @path`, or use `curl | python -c` to parse the response:

  ```bash
  curl -s -X POST "https://preview.thefirstonly.com/api/store" \
    -H "Content-Type: application/json" \
    -d @C:/Users/<user>/hermes-temp/payload.json | python -c "import sys,json; d=json.load(sys.stdin); print(d.get('preview_url',''))"
  ```

Phase 4: KFLOW SAVE
  → If topic fits KFlow (knowledge management), POST summary to:
    POST http://localhost:3003/api/knowledge
    Authorization: Bearer hermes-knowledge-secret
    Body: { title, content, summary, tags, topic_slug, source_url }
  → Use Python urllib (Pattern D) for reliable Unicode/Vietnamese handling
```

**Tagline to remember:** "mặc định là yêu cầu research xong sẽ xuất ra html nhé"

**Reference**: `references/research-quality-gates.md` — mandatory quality gates for all research tasks (paper-first, no news, traceable citations, cron workflow).

### Multi-level explanation pattern ("từ ngu đến PhD")

For topics where the user wants graduated understanding, use this 6-level structure in the HTML:

| Level | Name | Style | Content depth |
|-------|------|-------|---------------|
| 0 | **Ngu (Dumb)** | Everyday analogies, no jargon | "DNA = bản thiết kế gốc, RNA = copy tạm đi làm" |
| 1 | **Cấp 3** | Comparison tables, structure diagrams | 3 differences, basic chemistry |
| 2 | **Đại học** | Central Dogma, types, processes | Transcription, translation, 8 RNA types |
| 3 | **Master** | Enzymatic mechanisms, chemical detail | 2'-OH chemistry, ribozyme, telomerase |
| 4 | **PhD** | Cutting-edge tech | RNAi, alternative splicing, mRNA vaccine |
| 5 | **Nobel** | Origin of life, fundamental discoveries | RNA World hypothesis, evidence timelines |

Use this pattern when the user asks for layered understanding or says "từ ngu đến..." / "giải thích dễ hiểu".

### Scientific evidence table format

When the user requests structured comparison data (e.g. "các cột: Tên - Tác dụng - Nguồn tham khảo"), use this format in the HTML:

```html
<table>
  <thead><tr><th>Tên</th><th>Tác dụng & Cơ chế</th><th>Nguồn tham khảo</th></tr></thead>
  <tbody>
    <tr><td><strong>Element/Compound</strong></td>
        <td>Mechanism description with <span class="hl-yellow">highlighted key terms</span></td>
        <td><strong>Author, Journal Year.</strong> PMID: XXXXXXXX</td></tr>
  </tbody>
</table>
```

Every claim in the table must have a corresponding citation. Use PMID as the primary identifier for biomedical research, DOI for general science.

### The "Lead Researcher" delivery persona

When the user assigns a research role (e.g. "lead researcher, doctor-level, multi-field, sharp critical thinking, no bias, truth-first with evidence"), adopt:

| Principle | Practice |
|-----------|----------|
| **No bias** | State both sides of contested claims. Flag speculation vs. consensus explicitly. |
| **Evidence-first** | Every factual claim needs a citation (Author, Year, Publication). |
| **Critical thinking** | Point out methodological limits, statistical significance, sample sizes. |
| **Structured output** | Tables, hierarchies, formulas in blockquotes, milestone timelines, banner callouts. |
| **Always cite** | Format: [Author(s), Year, Pub]. Include a References section at the end. |

### The "Sườn → Phê duyệt → Chi tiết" workflow

For any broad research topic, follow this research-equivalent of critique-first:

```
Phase 1: SƯỜN (Outline)
  → Present structured skeleton (branches, keywords) to user
  → Wait for approval / corrections
Phase 2: CHI TIẾT (Depth)
  → Expand each node with:
     • Thuật ngữ + Định nghĩa
     • Bảng (term | definition | evidence/source)
     • Công thức (nếu có)
     • Mốc lịch sử (milestones)
Phase 3: OUTPUT (Deliverable)
  → Produce final artifact (see format matrix below)
```

**Apply this when:** user asks "tổng quan ngành X", "cho tôi sườn trước", or the topic spans 5+ subtrees.

