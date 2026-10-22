# Open Code Review (OCR) — Alibaba Group

**Repo:** github.com/alibaba/open-code-review (Apache-2.0)
**Paper:** arXiv 2609.20519 (Sep 17, 2026)
**Stars:** 37.8k | **Forks:** 2.7k | **Language:** Go 1.25.5
**CLI:** `npm install -g @alibaba-group/open-code-review`
**Site:** open-codereview.ai

## Key Architecture Insight

OCR uses a **hybrid architecture**: deterministic engineering pipeline + LLM agent.

**Deterministic (engineering code, not LLM):**
- `selectFiles()` — pure function: binary/path/extension/size gates, no LLM call
- `groupDiffs()` — LLM-assisted file grouping with fallback to 1-file-per-group
- `sniffer.go` — rule matching engine, template-based
- Positioning + reflection modules in `llmloop/`

**LLM Agent:**
- Scenario-tuned prompts for code review
- Scenario-tuned toolset (distilled from production traces)
- Dynamic context retrieval

## Results

- AACR-Bench (self-reported by Alibaba): 50 repos, 200 PRs, 10 languages, 1,505 annotations
- ~1/9 tokens vs general-purpose agents
- Higher Precision + F1, lower Recall (deliberate trade-off)
- Delegation mode: let coding agent run review, OCR handles file selection + rules

## Lesson for Agent Design

The core insight from OCR: "việc nào có đáp án đúng thì để code tất định lo, việc nào cần suy xét thì mới gọi model." Applied to Quang's systems:
- meTelligent: deterministic task parser replaces 2nd LLM call
- Content pipeline: deterministic transcript extractor feeds structured data to LLM
- AI Company: structured inter-agent contracts replace NL communication drift

## Files on Disk

`C:\Users\NTQUANG_DELL\deterministic/` — Python implementation of deterministic layer:
- `metelligent/parser.py` — task parser
- `content/extractor.py` — transcript extractor  
- `aicompany/contract.py` — inter-agent contracts
