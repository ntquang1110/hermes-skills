# Patent Deep-Dive Analysis Format

This reference documents the exact patent analysis format used across 24 patents in the July 2025 session. Each patent got its own HTML page following this structure.

## Page Structure

```
I. TỔNG QUAN (Overview)
II. FLOW TỔNG QUAN (7-Bước Process)  
III. DEEP DIVE — PhD (Chi tiết như PhD)
IV. CHECKLIST (Triển khai)
V. Liên kết & Tài liệu tham khảo
```

## I. TỔNG QUAN

Top of page:
- Patent number badge + country badge
- Stats grid (5 boxes: year, cost/m³, duration days, efficiency %, and 1 custom)
- 2-paragraph description: (1) what it does, (2) key innovation/differentiation
- Link to patent gốc (patents.google.com)
- "Dễ nhất" vs "Khó nhất" comparison card (2-column)

### Color Coding per Method

| Method | Tag class | Accent color |
|--------|-----------|-------------|
| EKR (điện động học) | `tag-elek` | Blue #448AFF |
| Rửa đất | `tag-wash` | Orange #FF9100 |
| Cố định hóa học | `tag-chem` | Red #FF4B4B |
| Sinh học | `tag-bio` | Green #44C767 |
| Thực vật | `tag-phyto` | Teal #64FFDA |
| Nhiệt | `tag-therm` | Purple #B388FF |

## II. FLOW

Two parts:
1. **Arrow diagram** (ASCII art in `<pre>`): Show all steps with arrows
2. **Flow steps** (individual `flow-step` divs): Each step has:
   - `<div class="step-title">` — B1: Name
   - `<div class="step-detail">` — What to do
   - `<div class="step-detail">` — Requirements 
   - `<span class="step-easy">` or `<span class="step-hard">`
   - `<span class="step-cost">` — Cost estimate

## III. DEEP DIVE (Deep Dive boxes)

- Each key concept gets a `deep-box` div with blue left border
- Label + detailed explanation with specs, prices, chemical formulas
- 3-5 boxes per patent page

## IV. CHECKLIST

- Budget summary (total $ estimate, timeline, personnel)
- Shopping list: what specific items to buy (with prices)
- Links to suppliers (Alibaba, Amazon, local options)

## V. Pattern for Batch Analysis

When analyzing multiple patents in a category:
1. **Overview page**: Table with all patents (5 columns: patent#, name, process, efficiency, country)
2. **Detail pages**: One per patent following I-IV above
3. **Link each row** in overview table → detail page
4. Each detail page links back to the overview page

## HTML Implementation Notes

- Each page is self-contained (no external CSS/JS dependencies)
- Single-file HTML with inline `<style>`
- All styles use the Premium B/W/Y design system root variables
- Font size: compact mode for batch patents (0.85em body), standard for single patents (0.92em)
- Responsive breakpoint at 768px
