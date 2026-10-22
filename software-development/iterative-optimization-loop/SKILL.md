---
name: iterative-optimization-loop
description: "Optimization loop: measure, change, keep if better, stop."
version: 1.0.0
author: Hermes Agent (pattern drawn from Forward-Future/loopy)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [optimization, iteration, loop, performance, core-web-vitals, seo, verification]
    related_skills: [live-status-dashboard, test-driven-development, design-critique]
---

# Iterative Optimization Loop (Loopy)

For tasks like "tối ưu tốc độ website", "sửa test flaky", "dọn documentation", "SEO định kỳ" — anything improved by repeated, measurable passes. Instead of one vague prompt ("make it faster"), run a bounded loop with an explicit stop condition.

## The loop

```
1. Find the worst offender (page/test/doc) — measure first.
2. Pick ONE root cause you can actually change.
3. Make ONE change.
4. Re-measure the same metric.
5. Keep the change ONLY if it improved; else revert.
6. Repeat until: target met OR no meaningful improvement in one pass.
7. Human approval gate before shipping the batch.
```

## Rules that keep it safe

- **Measure before and after, same task, same metric.** No metric = no loop. Convert the task to a measurable target (Core Web Vitals LCP, flaky-test failure rate, outdated-doc count, keyword rank).
- **One change per iteration.** Two changes in one pass means you cannot attribute the result. Commit each pass separately, or stash-revert.
- **Keep only if better.** Improvement thresholds are explicit ("LCP < 2.5s", "0 flaky failures in 3 runs", "no 404 in crawl"). If a pass regresses, revert that change, log it, move on.
- **Stop condition is mandatory.** Reach the target, or a pass shows no meaningful gain → STOP and report. Do not loop forever chasing diminishing returns.
- **Every iteration leaves evidence.** Per-pass log: what changed, before-value, after-value, kept/reverted. This is what you hand the human for approval.

## Human approval gate

- End the run with a concise report: target, passes run, kept/reverted list, final metric.
- Do NOT batch-ship changes silently. Get approval before deploy.
- For destructive or large-blast-radius changes (schema, auth, deletes): get approval BEFORE starting, not just at the end.

## When NOT to use

- A single-shot, well-defined fix (one known bug) → just fix it.
- The metric cannot be measured reliably → no loop.
- "Improvement" is subjective with no proxy → agree a measurable proxy first or skip.

## Pitfalls

- Loop without a stop condition → runaway. Always set one.
- Measuring different things before/after → false conclusions.
- Optimizing without understanding the root cause → polishing symptoms.
- Reverting a good change because a later one regressed → evaluate each change independently.