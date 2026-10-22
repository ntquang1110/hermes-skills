# Newsprint Design for Livestock Product Briefs

Captured 16/09/2026 — after EZ80-Start/Sow/Grow/Repro Master Briefs.

## Design decision

The user approved **newsprint design** (light mode, serif fonts) for livestock product briefs, NOT the B/W/Y dark design previously specified in the livestock-product-lifecycle skill.

**Approved design tokens:**
- Background: `#F9F9F7` (off-white)
- Font stack: `Playfair Display` (headings), `Lora` (body), `Inter` (UI), `JetBrains Mono` (data)
- Border radius: `0px` everywhere
- Blockquotes: `4px solid #111111` left border + `#F5F5F5` bg
- Hard shadow hover: `box-shadow: 4px 4px 0px 0px #111111`
- Dot grid texture: SVG background on body
- Accent: `#CC0000` (editorial red, sparingly)
- Inverted section: black bg `#111111`, white text, red accent for GO Decision
- Marquee ticker: black bg, white text, red badges for key stats
- Tables: uppercase sans-serif headers, collapsed borders, hover rows
- Responsive: collapse to single column on mobile

## Content structure (verified 21-section pattern)

Each livestock product brief has these sections:
1. Executive Summary + GO Decision
2. Executive Research Framework (10 câu hỏi)
3. Quy mô vấn đề / Dịch tễ
4. Market Sizing — TAM/SAM/SOM (riêng cho từng giai đoạn)
5. Phân khúc khách hàng & Chấm điểm
6. Customer Pain & Jobs To Be Done
7. Competitive Landscape
8. Market Gap & Opportunity
9. Opportunity Scorecard
10. Đối chiếu nền tảng Kiềm Thảo Dược
11. Công thức MoSCoW
12. Công thức & Liều
13. An toàn & Pháp lý
14. Product Development Brief / RFI
15. Lộ trình G1-G7
16. Devil's Advocate & Risk Mitigation
17. Danh mục nguồn tham khảo

## Duplicate detection (important)

When generating multi-section briefs, the auto-merge can produce 3 sections that duplicate Executive Summary content:
- **"5–7 Kết Luận Cốt Lõi"** — duplicates the conclusions in Executive Summary
- **"3 việc KHÔNG được làm"** — duplicates section 9.3 in Executive Summary
- **"Điều kiện tiên quyết"** — duplicates section 5 in Executive Summary

These 3 sections should be REMOVED from the master doc. The Executive Summary already contains this content.

## Design verification checklist

After building HTML, verify via browser console:
```js
// Check key design elements
const bs = getComputedStyle(document.body);
{
  bg: bs.backgroundColor,                          // should be rgb(249, 249, 247)
  font: bs.fontFamily,                             // should include 'Lora'
  dotGrid: bs.backgroundImage.includes('svg'),      // should be true
  maxRadius: max radius of any element,             // should be 0
  fontsLoaded: check Google Fonts links,            // Playfair, Lora, Inter, JetBrains
  hardShadowCSS: check style for '4px 4px 0px',     // should be true
  blockquoteBorder: check blockquote borderLeft,     // should be '4px solid rgb(17, 17, 17)'
  invertedSection: check for .inverted element,      // should be true
  ticker: check for .ticker element,                 // should be true
}
```

## Parallel generation pattern

For N product briefs, dispatch one subagent per product via `delegate_task` (max 3 parallel). Each agent:
1. Loads newsprint-design, publish, and saphia-product-brief-factory skills
2. Writes its own HTML with 21-section structure
3. Publishes to preview.thefirstonly.com
4. Returns the preview URL

After all agents complete, collect URLs and present to user.
