# Research Rotation Cron (8 bài/ngày, 4 tiếng/lần)

Recurring Hermes cron job for the user's Knowledge Flow (KF) instance at `localhost:3003`.
Runs 6x/day; each run produces exactly 1 card; ~8 cards/day across 4 topic groups (2-2-2-2).

## Run order (MANDATORY)

1. **Queue first:** `GET /api/research-queue` — if any item has `status: "pending"`, research + create card + `PATCH ?id=<id>&action=done` BEFORE rotation.
2. **Rotation file:** read `C:\Users\NTQUANG_DELL\knowledge-flow\data\research-rotation.json`:
   ```json
   { "last_index": 2, "created": "...", "updated": "..." }
   ```
   `last_index` = topic group used in the most recent run.
3. **Next group:** `(last_index + 1) % 4`:
   - 0 → 💰 Tài chính (CFA / Quant / M&A)
   - 1 → 🔧 Công nghệ — ưu tiên AI (AI/LLM papers, chip/semiconductor, robotics)
   - 2 → 🧬 Sinh học Heo+Người (miễn dịch & bệnh học heo: cytokine, PRRSV/ASFV/PEDV; dinh dưỡng & hệ vi sinh: probiotic/postbiotic, axit amin)
   - 3 → ⚗️ Hóa học & Dược (hợp chất thiên nhiên & dược lý: saponin, polyphenol, alkaloid, dược động học; hóa phân tích & xử lý môi trường: KLN As/Pb/Hg/Cd, biochar)
4. **Within group:** pick a subtopic NOT covered recently. Scan the card-title list for the group's already-covered subtopics; fill gaps. Ghost topics (concepts referenced by other cards but lacking dedicated coverage) have the highest connective value.
5. **Post card** (Pattern D, verify via re-fetch), then **update rotation file**: write whole JSON with `last_index` = group just used + fresh `updated` timestamp (file is tiny — use write_file).

## Quality gates (from the cron prompt — non-negotiable)
- EVERY card must cite real scientific papers (PubMed/DOI/trusted URL). No news-only research — if only news exists, skip the topic.
- Detailed analysis required: cơ chế, phương pháp, số liệu, kết quả, kết luận.
- Vietnamese output with diacritics, markdown, full PMID/DOI reference table at the end.
- Reading time target 300-900s (~5-15 min) — check `reading_time_sec` in POST response.

## Topic-selection heuristics that worked
- **Run the dedup scan IMMEDIATELY after picking a subtopic, BEFORE starting Wikipedia/PubMed research — not just before POST.** Tested 2026-08-03: picked Berberine for group 3 (alkaloid), did a full Wikipedia + PubMed research cycle, THEN the title scan revealed an existing card "🧪 Berberine — Alkaloid isoquinoline đa cơ chế..." → had to pivot to Resveratrol and redo all research. The one-line `curl /api/cards | python` keyword scan costs ~20s; a wasted research cycle costs 5+ tool calls. Scan both the class keyword (alkaloid, polyphenol) AND specific compound names (berberine, resveratrol).
- **Group 3 status (verified against live card list 2026-08-03):** covered = saponin (nhiều card), polyphenol chung, curcumin, quercetin, tannin, tinh dầu, dược động học, KLN/biochar (dense), **Berberine (đã có card — đừng chọn lại)**, **Resveratrol (DONE 2026-08-03, card `843029ae`, PMID bank: 41330231, 36139849, 34130737, 34303281, 37029412, 32514341, 36242589, 30449092)**. Open group-3 gaps as of now: rutin, apigenin, luteolin, genistein/isoflavone, phenolic acids (chlorogenic/ferulic), lignan, coumarin, anthraquinone, capsaicin, piperine, ellagic acid standalone, allicin/tỏi, anthocyanin. Group-3 card `topic_slug` used: `hoa-hoc-duoc`.
- **Group 2 status (verified against live card list 2026-08-03):** **ADE / Antibody-Dependent Enhancement (DONE 2026-08-03, card `c48ba9bd`, topic_slug `chan-nuoi-heo`)** — đừng chọn lại ADE/FcγR/CD16 làm topic đứng độc lập; PMID bank + queries đã test trong `references/ade-antibody-dependent-enhancement-swine-roadmap.md`. Open group-2 gaps as of now: M cells (microfold cells) của Peyer's patches, Kupffer cells / liver immunity, NFAT & calcium signaling trong T cells, bacteriophage therapy cho ETEC, feed enzymes (phytase/xylanase), nucleotides trong dinh dưỡng heo, metallothionein & chuyển hóa Zn, valine/isoleucine. Nhóm 2 có nhiều card cũ trùng nhau (hệ vi sinh vật đường ruột 4+ card, ZnO 3 card) — ưu tiên ghost topics để nối các card.
- **⚠️ `/api/cards` list dump không expose `topic_slug`** (trả `topic_id: null` cho mọi card, verified 2026-08-03). Không verify được slug từ list; chỉ cần dùng convention: group 2 → `chan-nuoi-heo`, group 3 → `hoa-hoc-duoc`.
- Run dedup keyword check against ALL card titles BEFORE research AND before final POST (multi-keyword variants: full name, abbreviation, Vietnamese name, genus/species).

## Classic-paper PMID retrieval
To cite a canonical paper when you only remember author/journal/year (e.g. Kong 2004 Nat Med on LDLR mRNA, Lee 2006 Diabetes on AMPK), search PubMed with `author + journal + year`:
`berberine cholesterol lowering Nature Medicine 2004` → esearch returns the exact canonical PMID (15531889, 16873688).
Never cite from memory — always confirm via esummary (title + DOI) that the PMID is the right paper.
