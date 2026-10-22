# Research JSON → 2-tab HTML (Visualize + Học thuật) — từ subagent JSON, không qua KFlow card

Dùng khi research KHÔNG xuất phát từ KFlow card mà từ subagents ghi JSON (WSSV 16/08/2026, crush ball 15/08/2026, REE, xử lý chất thải heo). Pipeline: 3 subagents song song → `group{N}.json` → generator script → 2-tab HTML → publish preview → KFlow.

## Schema JSON chuẩn từ subagents (nhất quán giữa các nhóm)

```json
{
  "group": "1",
  "note": "Mọi PMID đều đã verify bằng PubMed E-utilities (efetch abstract)...",
  "topics": [
    {
      "topic": "1. Phân loại WSSV (Taxonomy)",
      "summary": "1-2 câu tóm tắt",
      "facts": [
        {"fact": "sự kiện/số liệu cụ thể trích từ abstract", "reference": "tác giả năm tạp chí", "pmid": "30924764"}
      ],
      "mechanism": "giải thích cơ chế"
    }
  ]
}
```

- Mỗi nhóm research = 1 file `group{N}_*.json`. Load: `d['topics']` nếu dict, fallback list nếu array thẳng.
- Prompt subagent phải có: schema cố định, TIẾNG VIỆT có dấu, KHÔNG bịa PMID, yêu cầu `verification` field ghi rõ đã efetch cái nào, và **ghi file SỚM sau mỗi 2-3 topic** (chống hết iteration mất data).

## Generator script (thay vì viết HTML tay)

Viết `build_{project}.py` bằng write_file (KHÔNG heredoc — strip dấu tiếng Việt), chạy python. Script:
1. `load(f)` từng file JSON → gom `all_pmids` để đếm verified.
2. Hàm `topics_acad(grp)` render tab Học thuật: h2 = topic, p = summary, ul > li (fact + `<code>[PMID]</code>`), blockquote "Cơ chế".
3. Tab Visualize viết tay: hero (1 câu chủ đề + 3 stats nổi bật) + bản đồ dòng chảy 8 fnode + sections + card vàng Mục tiêu (goal) + 5 act.
4. CSS/HTML reuse Premium B/W/Y (SKILL.md chính): #0D0D0D/#1B1B1D/#FFD600, radius 28, `.fnode/.fnum/.evrow/.mflow/.goal/.act`, tabbar sticky 2 nút pill, `.tbl-wrap` overflow-x mobile.
5. Output `<project>/<name>.html` → publish → verify → KFlow (html-publishing skill).

Mẫu đã chạy OK: `D:/Hermes Proj/wssv-research/build_wssv.py` (68KB output, 21 topics, 73 PMID unique).

## Quy trình hoàn chỉnh (đã chạy 2 lần OK 15-16/08/2026)

1. Delegate 3 subagents song song, mỗi agent 1 nhóm, ghi `group{N}.json` + verify PMID (prompt schema + PMID gợi ý kèm trong context, subagent tự efetch lại).
2. Batch xong → `ls data/` + python check: topics count, PMID unique count, in từng topic + facts sample. **KHÔNG tin summary của subagent — đọc file thật**.
3. Build script → HTML.
4. Publish: payload json.dumps ra file tạm → `curl --data-binary @payload.json` (urllib bị 403 trên preview API; file >50KB tránh ARG_MAX).
5. Verify: `curl -o /dev/null -w "%{http_code}"` + `grep -c` markers ('Visualize','Học thuật', vài PMID, từ khóa chính).
6. KFlow: passcode login (<PASSCODE>) → POST /api/knowledge → báo link + ID card.

## Pitfalls

- **Subagent hết iteration trước khi ghi file** (api_calls=50 cap) — xảy ra 3/3 lần trong session 15/08 (giá thị trường). Recovery: dữ liệu nằm trong summary inline (`cache/delegation/subagent-summary-*.txt`) hoặc research_groupA script viết JSONL theo từng dòng sau mỗi item (mất thì chỉ mất item cuối). Prompt ngay từ đầu: "ghi file SỚM, mỗi 2-3 topic flush 1 lần".
- **Camofox nhiều query liên tiếp: KHÔNG dùng chung 1 tab** — tab chết sau 1-2 navigate (urls=0 cho các query sau). Pattern đúng: mỗi query tạo tab mới (POST /tabs) → navigate → evaluate → `DELETE /sessions/<userId>` reset giữa chừng (xem skill camofox-browser, đã patch 15/08).
- **Rate limit PubMed efetch** (HTTP 429, 3 req/s) → subagent retry sleep 2-4s; parent không cần đụng.
- **Số liệu gợi ý trong prompt KHÔNG phải verified** — subagent phải efetch từng PMID; parent verify lại vài PMID mẫu khi build. Nếu số liệu không tìm thấy trong abstract (vd dãy "70–167 × 210–380 nm" WSSV) → ghi số thay thế verified (275 × 120 nm) + note, không bịa.
