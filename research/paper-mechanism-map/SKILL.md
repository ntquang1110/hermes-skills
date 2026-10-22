---
name: paper-mechanism-map
description: "Use when đọc bài báo khoa học cần bản đồ cơ chế."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [research, paper, mechanism, pathway, html, playful-design, impeccable, publish, verify]
    related_skills: [visual-flow-html, playful-design, impeccable, camofox-browser, grounded-citations, pubmed-evidence-research]
---

# Paper Mechanism Map — bài báo khoa học thành bản đồ cơ chế

Trigger: user gửi link bài báo (PubMed/DOI/PDF) hoặc nói "anh không hiểu bài này, dựng bản đồ cho anh".
Mục tiêu: một trang HTML để người không chuyên đọc 30 giây là nắm được chất gì, đi đâu, chặn ở đâu, hậu quả gì. Chi tiết chỉ để tra khi cần.

Nguyên tắc nền: người đọc cần **bản đồ dòng chảy trước, chi tiết sau**. Không bao giờ đưa một bản dịch abstract dài rồi gọi đó là bản đồ.

## Workflow

### 1. Lấy nguồn, không cào HTML PubMed
Trang `pubmed.ncbi.nlm.nih.gov` trả "Cookies must be enabled" khi fetch. Dùng E-utilities (plain text, không cần key):
```bash
curl -s "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=<PMID>&rettype=abstract&retmode=text"
```
Lấy đủ: tên bài, tác giả, tạp chí, năm, DOI, PMID, toàn bộ abstract. Cần full text thì tìm bản open-access (PMC) trước khi kết luận là không có.

### 2. Xác định chất gốc và cây mẹ
Chất thực vật thì **tra cây mẹ rồi mới viết**, không đoán theo tên. Search một câu dạng "`<compound>` isolated from which plant", lấy nguồn học thuật (PMC/PubMed/Frontiers). Người đọc mất niềm tin ngay ở dòng đầu nếu tên cây sai.

### 3. Chọn 5 đến 8 thuật ngữ trung tâm
Tiêu chí: chất đang nghiên cứu, đích tác động, 1 đến 2 con đường tín hiệu, các chỉ dấu đo lường, cách làm đặc thù của bài.
Mỗi thuật ngữ một câu: nó là gì, vai trò trong lập luận. Không tra hết glossary của bài.
Gắn nhãn phân loại (tác nhân, chất thử, chỉ dấu, cơ chế, công cụ, cách làm) để người đọc biết đâu là vật, đâu là thước đo.

### 4. Dựng flow theo chuẩn ký hiệu
```
→   kích hoạt / tác động tới / làm tăng
⊣   chặn / ức chế
↑↓  tăng giảm
```
Màu cố định: **hồng = bị chặn**, **mint = kích hoạt hoặc bị làm giảm**, **vàng = điểm quyết định**, **tím = bước trung tính**. Luôn có legend giải thích ký hiệu.
Mỗi node trả lời đủ 4 câu: cái gì chặn nó, cái gì làm thay đổi nó, nó tác động tới ai, hậu quả cuối là gì.
Chuỗi điển hình: tác nhân xâm nhập, vào tế bào, con đường bị trục lợi, nhân lên, hệ quả thực tế. Kết bằng hậu quả nhìn thấy được (chết, tiêu chảy, tổn thương mô).

### 5. Ba tầng đọc, phân biệt bằng cỡ chữ chứ không bằng card
- 5 giây: một câu, chữ lớn nhất.
- 1 phút: hai đoạn, chữ vừa.
- Deep dive: cơ chế phân tử, câu hỏi còn bỏ ngỏ, chữ nhỏ và nhạt hơn.
Ba tầng khác nhau bằng type scale, không phải ba card giống nhau (impeccable cấm repeated container).

### 6. Luôn có mục phê bình số liệu
Bắt buộc kiểm: cỡ mẫu suy ra từ phần trăm, các chữ tự giới hạn của tác giả ("partially reversed", "adjunctive"), khoảng cách giữa nồng độ in vitro và nồng độ đạt được in vivo. Người đọc cần biết chỗ nào bài tự giới hạn, không cần lời khen.
Thêm một câu hỏi tác giả chưa trả lời, và ghi rõ đó là chỗ bỏ ngỏ, không suy diễn thành kết luận.

### 7. Design pass: Playful Geometric
Design system mặc định cho loại trang này là **playful** (skill `playful-design`), nền sáng. Không mặc định dark dashboard.

Tokens:
```
paper #FFFDF5 · ink #1E293B · ink-soft #475569 · muted #64748B
violet #8B5CF6 · pink #F472B6 · amber #FBBF24 · mint #34D399
card #FFFFFF · hairline #E2E8F0
radius 8 / 16 / 24 · border 2px solid ink
hard shadow 6px 6px 0 ink, mobile 3px 3px, không blur
font: Outfit 700/800 cho display + Plus Jakarta Sans cho body
nền: dot grid radial-gradient(#CBD5E1 1px), nhịp 22px
```
Đặc trưng bắt buộc: primitive shapes (tròn, tam giác, vuông bo) làm decoration ở header và ẩn hết dưới 640px; card kiểu sticker; pill có hard shadow; đúng một khoảnh khắc chuyển động có chủ đích (stagger reveal cho các node, ease-out, tôn trọng `prefers-reduced-motion`).
Tương phản: chữ trên nền màu dùng ink hoặc trắng đậm, tuyệt đối không xám. Violet không dùng làm nền chữ thường, chỉ heading, viền, decoration.

### 8. Impeccable gate: bỏ hết dấu vết AI
Chạy checklist cùng một lượt render:
- Không eyebrow/kicker chip trên heading. Nguồn bài để ở byline dưới h1.
- Không hero-metric template (số to cộng label nhỏ thành grid). Ba con số then chốt đưa vào đoạn lede dạng chữ.
- Không đánh số section 01/02/03 trang trí. Số chỉ dùng khi là thứ tự thật (các bước thí nghiệm) hoặc list thật.
- Không em dash và en dash. Dùng dấu phẩy, hai chấm, hoặc tách câu.
- Không emoji làm icon. Ký hiệu ⊣ → ↑↓ là **dữ liệu**, được giữ, nhưng phải có legend.
- Không gradient text, không glassmorphism, không colored side border trên card, không nested card, không marquee, không bounce easing cho UI.
- Hard shadow hợp lệ vì thế giới này là neobrutalist/Memphis. Không trộn soft shadow vào.
- Không dùng một font hệ thống cho tất cả, phải có display face riêng.
- Copy tiếng Việt **có dấu đầy đủ**, số dùng chữ số.
Quét máy bằng `impeccable/scripts/ui-audit.js` qua browser_console, hoặc grep raw HTML.

### 9. Verify render trước khi publish
```bash
cp "C:/Users/NTQUANG_DELL/AppData/Local/hermes/skills/devops/camofox-browser/scripts/verify-html-render.cjs" \
   "/d/Hermes Proj/camofox-browser/verify-html-render.cjs"
cd "/d/Hermes Proj/camofox-browser" && node verify-html-render.cjs "http://127.0.0.1:<port>/<file>.html" "./shots"
```
Điều kiện qua: `base.hOverflow === false` và `mobile.hOverflow === false`, `brokenImgs` rỗng, `overflowingTextNodes` rỗng, title khớp, và có dòng `DONE`.
Kèm audit tĩnh: grep em dash, grep emoji/CJK, grep gradient/backdrop-filter.

### 10. Publish và verify trên server
```
POST https://preview.thefirstonly.com/api/store
headers: Content-Type application/json, User-Agent (bắt buộc, thiếu thì Cloudflare 1010)
body: {"content": "<html>"}
```
Có `preview_url` rồi thì fetch lại, kiểm vài cụm tiếng Việt có dấu và kiểm ký tự lạ còn sót. Không báo xong trước bước này.
Gửi user: link, kèm MEDIA screenshot desktop và mobile.

## Pitfalls

1. **PubMed HTML bị cookie wall** → luôn dùng E-utilities `efetch`. Không kết luận "không lấy được bài".
2. **`curl -o /dev/null` báo bytes=0 dù HTTP 200** trên MSYS Windows là lỗi path, không phải lỗi server. Kiểm size bằng `curl -s <url> | wc -c`.
3. **Hai http.server cùng bind một port** làm request rơi vào server cũ serve thư mục khác (file mới 404 dù có thật). Check `netstat -ano | grep ":<port>" | grep -i listen | wc -l` phải bằng 1; thấy 2 thì kill hết rồi đổi port.
4. **Ký tự lạ lọt vào bản thảo** (chữ Hàn/Trung, từ tiếng Anh lẫn vào câu Việt) khi soạn nhanh. Grep trước publish:
   `grep -nP '[\x{3000}-\x{9FFF}\x{AC00}-\x{D7AF}]' <file>` và `grep -nE '\b(also|and|the|with|from)\b' <file>`.
5. **Camofox trả 500 ở `/tabs` lần navigate đầu** (session cũ bị reaper) → retry một lần. Hoặc đi thẳng đường playwright của `verify-html-render.cjs`, không cần Camofox cho việc verify.
6. **`file://` bị Camofox chặn** → serve qua `python -m http.server <port> --bind 127.0.0.1` ở background, kill server sau khi xong.
7. **MEDIA path có dấu cách** dễ vỡ khi gửi Telegram → copy screenshot sang `$HOME/httptmp/` tên không dấu cách rồi mới gửi.
8. **Không bịa số, PMID, tên cây, tên đường tín hiệu.** Thiếu dữ liệu thì ghi rõ "bài tóm tắt chưa nêu" trong mục phê bình.
9. **Số trong bài sống sót nguyên vẹn**: dùng chữ số, giữ đúng đơn vị và khoảng (≤120 μM, 40 mg/kg/ngày, 66,7%).
10. **Không tự QA vô hạn**: build, verify một lượt desktop cộng mobile, fix một batch, xác nhận một lượt nữa, dừng.

## File tham chiếu
- Biến thể dark B/W/Y cùng nội dung: skill `visual-flow-html`.
- Screenshot local HTML khi model không có vision: `camofox-browser/references/screenshot-local-html.md`.
- Bản nháp playful tại chỗ (dùng làm điểm khởi đầu cho design pass mục 7, chưa verify render): `D:/Hermes Proj/berberine-pedv-playful.html`.
