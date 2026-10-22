# Vietnamese draft length budget (measured)

Numbers below come from a real long-form Vietnamese Threads draft pass (2026-10), trimming
10,524 chars down to 6,999 chars for a 3-7K window.

## The conversion factors

| Measure | Value |
|---|---|
| bytes per char, full Vietnamese diacritics | **≈1.32** |
| chars per byte | ≈0.757 |
| avg chars per accent character | ~0.21 (1,465 accents in 6,999 chars) |
| avg paragraph length (2 sentences, diacritics) | **200-230 chars** |

Free checks this gives you:

- `write_file` → `bytes_written` ÷ 1.32 ≈ char count. No extra call needed.
- `read_file` → `file_size` is **bytes**, not chars. Never read it as the char count.
- Byte targets: 7,000 chars ≈ **9,200 bytes** · 6,500 chars ≈ 8,600 bytes · 3,000 chars ≈ 4,000 bytes.

## Paragraph budget by target window

| Char window | Paragraphs (~2 sentences each) |
|---|---|
| 3,000 | 14-15 |
| 5,000 | 22-25 |
| 6,500 | 29-32 |
| 7,000 (hard ceiling) | **30-35** |

A 45-block outline lands around 10,000 chars. Outline-level cutting is free; text-level
cutting costs multiple tool calls.

## Skeleton that lands in 3-7K

Roughly 30 blocks, this order:

1. Hook quote, verbatim in source language (1 block)
2. One-line Vietnamese gloss of the hook (1 block)
3. Author credibility / why they are not a theorist (1 block)
4. Source-honesty note: is this research or personal notes? does the video end in a CTA/upsell? (1 block)
5. The problem, told as the author's own story (2-3 blocks)
6. The author's key line, verbatim + one gloss (1 block)
7. Mechanism / the numbers, with the concrete figures kept exact (3-5 blocks)
8. The reusable framework, named (2-3 blocks)
9. Concrete worked example (1-2 blocks)
10. Best single insight, called out as such (1-2 blocks)
11. Second-order insight / hardest truth (1-2 blocks)
12. "If you only do N things" numbered actions (4-5 blocks)
13. Local-context bridge: how this lands for the reader's own market (1 block)
14. Closing question addressed to the reader (1 block)

If the outline exceeds ~35 blocks, something in 5, 7 or 11 must shrink before you write a word.

## Ranked cut candidates (delete in this order)

When over the ceiling, delete whole blocks. Proven payoff, best first:

1. **Transition filler** — "Rồi ông vào phần tiền, và đây là chỗ nhiều người chưa từng nghe." Pure signposting, ~80-100 chars. Always first.
2. **Side observations / secondary statistics** — a whole block that is interesting but not load-bearing.
3. **Caveats and self-qualifications** — "if you only have one thing in you and want to own it forever, holding may be right."
4. **Redundant gloss of a quote you already glossed** — keep the quote, keep one gloss, drop the second.
5. **Timing/motivational asides** — "people who say 'after this quarter' never do it." Feels good, adds no mechanism.
6. **Second sentence of a two-sentence definition** — the first is usually the definition, the second is elaboration.
7. **Price/process trivia inside a list** — keep the number, drop the surrounding procedure.

Do NOT cut: verbatim quotes, hard numbers, source attributions, the source-honesty note, the
local-context bridge, the closing question.

## Order of operations that actually converged

```
write full draft        -> 10,524   (over by 3,500)
5x reword passes        -> 10,091   (~10% total, 5 tool calls)   <- poor return
delete 3 whole blocks   ->  7,773   (~25% in ONE move)           <- this is the lever
3x targeted trims       ->  7,341
4x micro-trims          ->  7,250 / 7,106
2x more block trims     ->  6,999   (in window)
```

Lesson: reword passes cost a call and return ~5-10% each. Block deletion returns 25% in one
move. Spend the first three moves on deletion.

## Accidental-quote-loss recovery

Cutting a block can take a pull-quote with it. Recover in one small patch: re-insert the quote
plus a single lead-in clause (~185 chars including the quote). Cheaper than reworking a paragraph.
