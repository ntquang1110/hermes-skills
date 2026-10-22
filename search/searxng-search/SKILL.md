---
name: searxng-search
description: "Self-hosted SearXNG search engine — dùng API search local, không qua Google/Bing"
category: search
---

# SearXNG Search

SearXNG is a privacy-respecting metasearch engine that you can run locally. It aggregates results from multiple search engines and package repositories, returning clean JSON output.

## Quick Start

API_KEY="sk-sea...92f0"

SEARXNG_URL="http://127.0.0.1:8888"

## Quick Reference

Check searxng instant
```
curl -s -w "HTTP Status: %{http_code}" \
  -H "X-API-Key: *** \
  "${SEARXNG_URL}/search?q=orange+pi&format=json"
```

## JSON Response Structure

```json
{
  "query": "search term",
  "number_of_results": 0,
  "results": [
    {
      "url": "https://example.com",
      "title": "Result Title",
      "content": "Snippet of content...",
      "publishedDate": "2025-01-01T00:00:00",
      "engine": "duckduckgo",
      "engines": ["duckduckgo", "startpage"],
      "score": 3.0,
      "category": "general"
    }
  ],
  "answers": [],
  "suggestions": [],
  "corrections": [],
  "infoboxes": [],
  "unresponsive_engines": []
}
```

## Common Usage Patterns

### 1. Package Repository Searches

**Cargo/Rust crates:**
```bash
curl -s "http://localhost:8888/search?q=tokio&format=json&categories=cargo" | \
  jq '.results[] | {title, url, content}'
```

**npm packages:**
```bash
curl -s "http://localhost:8888/search?q=express&format=json&categories=packages" | \
  jq '.results[] | select(.engines[] == "npm") | {title, url, content}'
```

### 2. Web Search with Filtering

**IT/Tech search:**
```bash
curl -s "http://localhost:8888/search?q=rust+async&format=json&categories=it" | \
  jq '.results[0:5] | .[] | {title, url, engines}'
```

**GitHub repositories:**
```bash
curl -s "http://localhost:8888/search?q=machine+learning&format=json&categories=repos" | \
  jq '.results[] | select(.engines[] == "github") | {title, url}'
```

### 3. Extracting Specific Information

**Get top 3 results:**
```bash
curl -s "http://localhost:8888/search?q=rust+ownership&format=json" | \
  jq '.results[0:3] | .[] | {title, url, content}'
```

## Debugging

**Check SearXNG config:**
```bash
curl -s "http://localhost:8888/config" | jq '.engines[] | select(.name == "pypi")'
```

**Check for engine errors:**
```bash
curl -s "http://localhost:8888/search?q=test&format=json" | jq '.unresponsive_engines'
```
