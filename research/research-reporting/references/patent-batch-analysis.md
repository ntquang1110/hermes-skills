# Patent Batch Analysis Workflow

Used in the 24-patent soil remediation analysis session (July 2026). After each patent research batch, creates an overview page linking to individual deep-dive pages.

## Workflow

1. **Create overview table** listing ALL patents in the batch with columns: patent#, name, process, efficiency, country
2. **Create individual HTML page** for EACH patent following the Patent Deep-Dive pattern (Overview → Flow → Deep Dive → Checklist)
3. **Link step:** add `<a href="URL">📄 Phân tích</a>` to the patent# cell in the overview table
4. **Publish overview** to `preview.thefirstonly.com` via POST /api/store
5. **Publish each individual page** to preview service
6. **Update overview** by adding links to all individual pages, then re-publish
7. **Save to KFlow** with summary of all patents

## Batch Execution

When doing 20+ patents, batch them by category (e.g., EKR, soil washing, chemical, biological, thermal). Process each patent fast: ~3-5KB HTML per compact page, publish one by one. Use a shared minified CSS template to save space.

## HTML Structure for Individual Compact Patent Pages

```html
<!DOCTYPE html>
<html lang="vi">
<head>
  <title>Patent #N: ...</title>
  <style>/* compact CSS — reuse same vars */</style>
</head>
<body>
<div class="header"><h1>Patent #N: Name</h1><div class="sub">Tagline</div>
  <div><span class="pat-num">PATENT</span><span class="badge-country">🌐 Country</span></div></div>
<div class="container">
  <div class="card"><h2>I. TỔNG QUAN</h2>
    <div class="stats-grid">4 boxes: year, cost/m³, days, efficiency</div>
    <p>Description of patent innovation</p>
    <div class="ref-box"><p>🔗 Patent link</p></div>
  </div>
  <div class="card"><h2>II. FLOW</h2>
    <div class="flow-step">3-5 steps with: title, detail, cost, easy/hard</div>
  </div>
  <div class="card"><h2>III. DEEP DIVE</h2>
    <div class="deep-box">1-3 key innovations with specs</div>
  </div>
  <div class="card"><h2>IV. CHECKLIST</h2>
    <p>What to buy / budget / timeline</p>
  </div>
</div></body></html>
```

## Key Tips

- **File naming convention:** `patent{N}-{countrycode}{patentnumberfirstchars}.html` (e.g., `patent1-cn112517626b.html`)
- **Publish format:** JSON payload `{"content": "<html>...", "title": "Patent #N: Name"}`
- **Cost per patent page:** ~5-7KB HTML, consistent template reuse
- **Batch publishing:** for efficiency, prepare all payloads first then publish sequentially
