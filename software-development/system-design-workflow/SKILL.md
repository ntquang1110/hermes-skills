---
name: system-design-workflow
category: software-development
description: >
  Full-cycle system design: requirements → architecture → critique → 
  dependency mapping → priority → then code. Enforces the user's 
  "critique before code" principle. Optimized for Vietnamese-language 
  projects and real-time AI systems.
trigger: |
  User starts a new software project, asks to design a system, or says
  "tạo dự án mới" / "thiết kế hệ thống" / "kiến trúc".
---

# 🏗️ System Design Workflow

## Khi nào dùng skill này
- User nói "tạo dự án mới" hoặc "thiết kế hệ thống"
- User muốn phân tích kiến trúc trước khi code
- User yêu cầu so sánh competitor để rút ra design decisions
- Có dấu hiệu user muốn làm kỹ lưỡng thay vì code ngay

**KHÔNG dùng** khi user muốn code ngay một tính năng nhỏ hoặc fix bug.

---

## ⚠️ Nguyên tắc vàng (từ user correction)

> **CRITIQUE BEFORE CODE** — Không bao giờ code trước khi:
> 1. Đã có architecture document
> 2. Đã tạo UI prototype (HTML mockup) cho user review design
> 3. Đã phản biện design để tìm gap
> 4. Đã xác định task priority dựa trên dependency thực tế
> 5. User đã duyệt design và nói "triển khai đi"

User đã từng nói: *"Đừng code trước — thu thập thông tin dự án và phản biện trước để sắc nét những việc cần làm"*
User cũng nói: *"dựng tạm thời html lên để tôi review design đã"* — UI prototype là bước bắt buộc, không skip.

---

## 🔄 Workflow

### Bước 0: Phân tích Competitor (khi có)
Khi user đề cập đến một hệ thống có sẵn (Claude, ChatGPT, v.v.) **và muốn xây hệ thống thay thế**:
- Liệt kê toàn bộ điểm mạnh của đối thủ, phân loại: **model quality**, **app features**, **ecosystem**
- Vẽ bảng so sánh với hệ thống dự định xây (3 cột: Claude | Hermes/ours | Mức độ)
- Xác định đâu là lợi thế **cốt lõi** (khó sao chép) vs **có thể thay thế**
- Output: HTML (render đẹp cho user đọc) hoặc markdown
- **Pitfall:** Đừng chỉ liệt kê — phải kèm đánh giá "có replicable không?" và "cần ưu tiên thay thế không?"

### Bước 0.5: Pattern rút ra từ review competitor (đã duyệt Aug 2026)

Khi review agent harness khác (DeepSeek Harness/dsh), chỉ lấy pattern đã duyệt, không đu theo hype. 2 pattern đã duyệt:

1. **Layered patch config** — config là các layer đè nhau (profile → bundle → patch file → --patch). Layer sau override layer trước, mọi row config thay được bằng patch mà không đụng file gốc. Áp dụng cho Volden/TFO/AI Company config thay vì sed file.
2. **Session log là nguồn sự thật** — invariant: "model-visible means logged". Thứ gì model thấy phải tái tạo được từ log; fork, resume, telemetry, replay đều derive từ 1 luồng log duy nhất. Củng cố state-file protocol: quyết định quan trọng phải ghi state, không giữ trong đầu.

**Đã loại:** Capability seams + E2B remote sandbox — user không dùng (chạy Windows local, không cần remote Linux sandbox).

### Bước 1: Architecture Design
- Vẽ architecture diagram (dùng text-art, excalidraw, hoặc HTML/SVG)
- Xác định: modules, data flow, tech stack, storage
- Bao gồm **cả real-time path và batch/after-process path**
- Ghi rõ: mỗi module dùng công nghệ gì, lý do

**Checklist cho architecture:**

### Bước 3: User-System Interaction Flow
Vẽ ít nhất **3 scenario** cụ thể với **timeline format**:

**Format chuẩn (kèm latency tracking):**
```
THỜI GIAN   USER                      SYSTEM
─────────   ────                      ──────
T+0s        👤 Bắt đầu nói
                                     🎤 Mic capture ON
T+2s        👤 "Nội dung..."         ⚙️ VAD detect → Whisper
T+4s                                  📝 Interim transcript push
T+5s                                  📊 Analyzer: intent, entities
                                     ⚡ Critique check vs memory
T+6s                                  📌 Push critique đến UI
```

Vẽ các scenario:
- **Scenario A**: Real-time (user đang nói, hệ thống phản hồi) — kèm critique push
- **Scenario B**: Batch/After-process (sau cuộc họp — transcript → summary → tasks → profile)
- **Scenario C**: Search/Recall (tra cứu thông tin cũ trong memory)

Mỗi scenario phải verify:
1. **Happy path** — mọi thứ hoạt động
2. **Degraded path** — mạng chậm, audio kém, model lỗi
3. **Edge cases** — im lặng, nhiều người nói, code-switching ngôn ngữ

### Bước 4: Phản biện Design (CRITIQUE)
Đây là bước quan trọng nhất — tự phản biện design trước khi code.

**Các loại gap cần tìm:**
| Loại | Ví dụ |
|------|-------|
| **Architecture gap** | Pipeline tuần tự → không real-time |
| **Missing module** | Không có speaker diarization cho multi-user |
| **Wrong dependency order** | Core engine phụ thuộc STT, STT phụ thuộc audio capture |
| **Over-engineered** | SQLAlchemy cho 1 bảng tasks |
| **Under-engineered** | Regex-only critique → không đủ thông minh |
| **Tech mismatch** | Thư viện tiếng Anh cho data tiếng Việt |
| **Privacy gap** | Audio data không được bảo vệ |

**Output:** Markdown document với sections:
- Vấn đề kiến trúc (kèm severity: 🔴 🟡 🟢)
- Vấn đề module cụ thể (kèm solution)
- Vấn đề roadmap/priority

### Bước 5: Dependency-based Prioritization
Không dùng phase ngẫu nhiên. Xác định **dependency graph thực tế**:

```
Module A (không phụ thuộc)
  └── Module B (phụ thuộc A)
       └── Module C (phụ thuộc B)
            └── Module D (phụ thuộc B + C)
```

**Matrix:**
```
                  HIGH VALUE          LOWER VALUE
HIGH URGENCY     P0: nền tảng         P1: nice-to-have
(không có →      (audio, STT,         (diarization,
không chạy được)  memory, models)      dashboard)
LOW URGENCY      P1: core logic       P2+: tương lai
(có thể delay)   (analyzer, critique,  (plugins, TTS,
                  tasks, API)          notifications)
```

## Design Pattern: Deterministic + LLM Hybrid Architecture

Inspired by Alibaba's Open Code Review (ocr) and applied to Quang's systems in Sep 2026.

### The principle

Việc nào có đáp án đúng thì code tất định lo. LLM chỉ làm việc cần phán đoán.

A well-designed system splits work by what each layer does best:

| Layer | What it handles | Examples |
|-------|----------------|----------|
| Deterministic | Things with a right answer | File selection, grouping, parsing dates, extracting quotes, validating schema, sorting tasks |
| LLM | Things needing judgment | Summarizing, writing draft, resolving ambiguity, critiquing intent |

### When to apply

- Data extraction: regex + rules beats LLM for pulling structured data from text (timestamps, numbers, quotes, dates)
- Schema validation: never trust LLM output format. Always validate + coerce deterministically
- Preprocessing: extract building blocks before LLM writes from them. LLM reads structured data, not raw input
- Inter-agent communication: agents should pass JSON with validated schemas, not natural language. Each decode of NL loses information

### When NOT to apply

- One-shot tasks where setup cost exceeds LLM cost
- The deterministic parser would be as complex as the LLM call
- Input format is unpredictable and rules can't cover it

### Three implementations from this session

All in `C:\Users\NTQUANG_DELL\deterministic\`:

1. meTelligent task parser (metelligent/parser.py): LLM outputs structured JSON to deterministic parse_date/parse_priority/validate to sorted task list. Replaces the second LLM call for task extraction.
2. Content pipeline extractor (content/extractor.py): Transcript to deterministic extract topics/quotes/numbers/timestamps to LLM writes thread from structured data, not raw transcript.
3. AI Company contract system (aicompany/contract.py): Every agent output must pass Contract.validate() before forwarding. No natural language between agents. Schema with optional fields, type coercion, nested validation.

See `references/deterministic-hybrid-architecture.md` for detailed implementation patterns.

---

## 📐 Output documents

Mỗi phase nên produce ít nhất 1 file markdown:

| Phase | Output file | Format |
|-------|-------------|--------|
| Competitor analysis | `01-competitor-analysis.html` | HTML (render đẹp) hoặc MD |
| Architecture | `02-architecture.md` | MD với diagrams |
| Interaction flow | `03-interaction-flows.md` | MD với timeline scenarios |
| Critique | `04-critique.md` | MD với severity labels |
| Priorities | `05-roadmap.md` | MD với dependency graph |

## 🎨 Bước 6: UI Prototype — Interactive HTML Mockup ⚠️ QUAN TRỌNG

> **Lesson from user (Jul 2026):** Sau khi có plan + architecture + priority, user KHÔNG muốn code ngay. User nói *"dựng tạm thời html lên để tôi review design đã"* — họ muốn THẤY giao diện trước, critique design rồi mới code.

Tạo một **file HTML tĩnh** prototype giao diện người dùng với **đầy đủ 3-5 màn hình chính**, dùng **Design System tokens** của user. File này là interactive mockup — click tab chuyển view, button toggle state — chứ không phải architecture diagram.

### Yêu cầu:

1. **Đúng Design System của user** — đọc từ `references/design-system-v1.md` (hoặc memory). Dùng `:root` CSS variables mapping trực tiếp:
   - Dark BG, Surface, Accent colors, Text primary/secondary
   - Card radius 28px, Button 56px/999px
   - 8pt grid spacing
   - Animation 200ms cubic-bezier

2. **Hiển thị các chế độ xem chính** — mỗi chế độ là một tab/section riêng:
   - Library view (grid/danh mục)
   - Feed view (scroll / TikTok-style)
   - Book view (reader / tuần tự)
   - Detail / search views nếu cần

3. **Nội dung giả thực tế** — dùng tiếng Việt, nội dung kiến thức có thật (ví dụ từ các session Hermes đã trả lời). Không dùng placeholder "Lorem ipsum".

4. **Interactivity tối thiểu** — click tab chuyển view, click item mở detail, button toggle state (like/bookmark). Dùng vanilla JS, không cần framework.

5. **Responsive** — xem được trên mobile (user thường xem từ điện thoại). `@media` queries breakpoints.

6. **File naming:** `<project>-preview.html` — lưu trong `preview/` folder của project hoặc chỗ dễ thấy.

> ⚠️ **Pitfall:** HTML prototype ≠ architecture diagram. Architecture diagram giải thích HOW it works. UI prototype cho user thấy WHAT it looks like. Cả hai đều cần nhưng UI prototype là bước user yêu cầu review trước khi code.

> ⚠️ **Pitfall:** Đừng dùng component libraries (shadcn, MUI, Chakra) cho prototype — HTML tĩnh + CSS thuần để user critique NHANH, không phải build production code. Chỉ chuyển sang framework sau khi user duyệt design.

> ⚠️ **Pitfall:** Nếu có Design System spec, implement CSS tokens CHÍNH XÁC trước khi làm gì khác. Sai màu/radius là lỗi nghiêm trọng — user sẽ bắt fix ngay.

### Sau khi tạo xong HTML prototype:

```bash
# 1. Start local server
cd <project>/preview && python -m http.server <PORT>

# 2. Expose với tunnel để user xem từ điện thoại
npx.cmd localtunnel --port <PORT> --subdomain <project-name>-preview

# 3. Gửi link cho user kèm mô tả các chế độ xem
```

## 🎨 Bước 7 (bổ sung): Tạo Architecture Overview HTML

Sau khi user đã duyệt UI prototype, tạo thêm **một file HTML tổng hợp** về kiến trúc system:

File này nên bao gồm:
- **Architecture diagram** trực quan (dùng CSS box, không cần SVG/JS)
- **Pipeline flow** cho từng mode (real-time, after-process) — mỗi step kèm output mẫu
- **Interaction scenarios** dạng timeline T+0s → T+N
- **Module data map** (table: input → process → output)
- **State machine diagram**
- **Data models** (schemas) 
- **Storage architecture** (công nghệ + use case)

Kỹ thuật:
- Dùng **pure HTML + CSS** — không cần JS framework
- Dark theme (GitHub-style) cho nhất quán
- `@media` queries cho responsive (xem được trên mobile)
- Font: Inter (Google Fonts) + monospace cho code
- File name: `NN-system-flow-overview.html`

> **Pitfall:** Architecture overview khác UI prototype. UI prototype cho user thấy mặt — architecture overview cho team/dev hiểu ruột. Làm UI prototype TRƯỚC.

## 🌐 Bước 8: Share Design cho User xem từ xa

Sau khi tạo xong documents, user cần xem từ điện thoại / máy khác. Có 3 cách:

### Cách A: Local server (nhanh nhất, cần cùng mạng)
```bash
# Node.js
cd /path/to/project && node server.js 8080
# Mở: http://localhost:8080/
```

### Cách B: localtunnel (public URL, không cần cài đặt)
```bash
# localtunnel — dùng npm, auto-download qua npx
npx.cmd localtunnel --port 8080
# Output: your url is: https://<random>.loca.lt
```

### Cách D: Cloudflare Tunnel (production-ready, domain cố định)

Khi user có domain riêng đã dùng Cloudflare, dùng **cloudflared tunnel named**:

**🔴 Pitfall — tunnel credentials mismatch:**
Credential file (`*.json`) chứa `TunnelID` có thể KHÔNG trùng với tunnel thực tế trong Cloudflare account. Nếu tunnel báo `"Unauthorized: Tunnel not found"`, cần đồng bộ:

```bash
# 1. Lấy token thực tế của tunnel
cloudflared tunnel token TUNNEL-NAME

# 2. Decode token (base64 JSON) để lấy accountID + secret
# Token format: {"a":"accountID","s":"secret","t":"tunnelUUID"}

# 3. Tạo credentials file đúng format:
# {"AccountTag":"...","TunnelSecret":"...","TunnelID":"...","Endpoint":""}

# 4. Cập nhật config.yml trỏ đến credentials file mới
```

**🔴 Pitfall — protocol lỗi (QUIC):**
Nếu tunnel reconnect liên tục với lỗi `control stream failure`, thử chuyển sang HTTP2:
```bash
cloudflared tunnel --config config.yml run --protocol http2
```

**🔴 Pitfall — WARP interference (VN users):**
WARP + cloudflared tunnel xung đột. Nếu đang dùng WARP, tunnel không kết nối được. Cần disconnect WARP hoặc dùng protocol http2.

**🔴 Pitfall — Tunnel remote config overrides local config.yml:**
cloudflared tunnel đọc config từ Cloudflare Dashboard (remote) **trước** local config.yml. Nếu bạn cập nhật local config.yml mà tunnel vẫn dùng ingress rules cũ, đó là vì remote config đang override. Cách fix:

```bash
# 1. Đọc remote config hiện tại
curl -s -H "Authorization: Bearer $CF_TOKEN" \
  "https://api.cloudflare.com/client/v4/accounts/$ACCOUNT_ID/cfd_tunnel/$TUNNEL_ID/configurations"

# 2. Update remote config (thay vì local config.yml)
curl -s -X PUT \
  -H "Authorization: Bearer $CF_TOKEN" \
  -H "Content-Type: application/json" \
  "https://api.cloudflare.com/client/v4/accounts/$ACCOUNT_ID/cfd_tunnel/$TUNNEL_ID/configurations" \
  -d '{
    "config": {
      "ingress": [
        {"service": "http://localhost:PORT", "hostname": "domain.com"},
        {"service": "http_status:404"}
      ],
      "warp-routing": {"enabled": false}
    }
  }'
```
Khi dùng local config.yml mà tunnel ghi log `"Updated to new configuration"` + ingress từ remote, chứng tỏ remote config đang active → update remote config là cách nhanh nhất.

```bash
# Tạo config file với Windows path (quan trọng!)
# Dùng C:\Path\To\config.yml — KHÔNG dùng MSYS /c/... paths
cat > /c/Users/.../.cloudflared/my-tunnel-config.yml << 'EOF'
tunnel: <tunnel-uuid>
credentials-file: C:\Users\<user>\.cloudflared\<uuid>.json

ingress:
  - hostname: example.com
    service: http://localhost:5099
  - hostname: www.example.com
    service: http://localhost:5099
  - service: http_status:404
EOF

# Chạy tunnel (phải dùng Windows path cho --config)
cloudflared tunnel --config "C:\Users\<user>\.cloudflared\my-tunnel-config.yml" run
```

**🔴 Pitfall — cloudflared --config path trên Windows (MSYS2):**
- cloudflared là Windows native binary → không hiểu `/c/Users/...` (MSYS path)
- Luôn dùng `C:\Users\...` (Windows path) trong `--config`
- Trong bash script dùng single quotes hoặc double quotes: `--config "C:\Users\..."`

**DNS setup trên Cloudflare Dashboard (hoặc API):**
Sau khi tunnel chạy, cần CNAME record trỏ về tunnel endpoint. Có thể tạo bằng API (xem `references/tunnel-api-config.md` → DNS Record Creation):
```bash
# Hoặc thủ công: vào Cloudflare Dashboard → DNS → Add record
- `@` → `<tunnel-uuid>.cfargotunnel.com` (Proxy: ☁️ On)
- `www` → `example.com` (Proxy: ☁️ On)

**Check tunnel status:**
```bash
cloudflared tunnel info <tunnel-uuid>
# Hoặc xem log bằng process(action='log')
```

**Lưu ý trên Windows (MSYS2):**
- ⚠️ **Dùng `npx.cmd` không phải `npx`** — trên MSYS2/bash, `npx` fork thường lỗi không ra output; `npx.cmd` (Windows native) hoạt động ổn
- **Foreground trước** để lấy URL: chạy `npx.cmd localtunnel --port <PORT>` với timeout 25s → copy URL từ output
- **Background sau** để duy trì: chạy `npx.cmd localtunnel --port <PORT>` với `terminal(background=true)`
- Lần đầu truy cập: localtunnel có thể show interstitial "Click to Continue" — bấm qua là được
- **cloudflared** hoạt động ổn trên Windows nếu dùng đúng Windows path format. Vấn đề trước đây là do MSYS path (`/c/...`) không được Windows native binary hiểu — dùng `C:\...` là chạy ngay.

### Cách C: GitHub (vĩnh viễn, xem mọi lúc)
```bash
git init && git add . && git commit -m "initial"
gh repo create <name> --public --push --remote origin
# → https://github.com/<user>/<name>
```

**Note:** GitHub render .md đẹp. .html thì cần vào raw URL hoặc dùng GitHub Pages.

**🔴 Pitfall — Branch name mismatch (master vs main):**
Khi push lần đầu, GitHub hiện tại dùng `main` làm default branch, trong khi local git init tạo `master`:
```bash
# Tình huống: push bị reject vì non-fast-forward
git push -u origin main
# → ! [rejected] main -> main (non-fast-forward)

# Cách fix: force push (an toàn vì là repo mới, chưa có ai dùng)
git push -u origin main --force
```

**Cách tránh:** Ngay từ đầu rename branch trước khi push:
```bash
git branch -m master main
# Sau đó push bình thường
```

### Cách E: Cloudflare Workers (temporary preview, zero setup)

Khi user muốn deploy static HTML lên Cloudflare mà không cần domain/tunnel, dùng **wrangler deploy --temporary**:

```bash
# 1. Tạo worker.js với HTML inline
cat > worker.js << 'EOF'
export default { async fetch(request) {
  const html = `...HTML content...`;  // Escape backticks and ${}
  return new Response(html, { headers: { 'content-type': 'text/html;charset=UTF-8' }});
} }
EOF

# 2. Tạo wrangler.toml
cat > wrangler.toml << 'EOF'
compatibility_date = "2026-07-12"
name = "visit-card"  # tên tuỳ chọn
EOF

# 3. Deploy (không cần login, tạo temp account tự động)
cd /path/to/project
unset CLOUDFLARE_API_TOKEN  # quan trọng: --temporary không dùng được nếu đã auth
npx wrangler deploy --temporary worker.js
# Output: https://<name>.<random-account>.workers.dev
```

**Đặc điểm:**
- 🟢 Không cần Cloudflare account / API token
- 🟢 URL public ngay lập tức (`*.workers.dev`)
- 🟢 Hỗ trợ full static HTML (kể cả base64 ảnh)
- 🟡 File HTML tối đa ~1MB (worker size limit)
- 🟡 URL tồn tại vô thời hạn nhưng temp account có thể bị thu hồi
- 🔴 Cần `wrangler.toml` với `compatibility_date`
- 🔴 Không support custom domain (trừ khi upgrade)

**Pitfall — HTML embedding vào worker.js:**
Khi nhét HTML vào JS template literal, cần escape:
- `` ` `` → `` \` ``
- `${` → `\${`

Dùng Python script để build:
```python
with open('index.html') as f:
    html = f.read()
escaped = html.replace('`', '\\`').replace('${', '\\${')
worker = f"""export default {{
  async fetch(request) {{
    const html = `{escaped}`;
    return new Response(html, {{
      headers: {{ 'content-type': 'text/html;charset=UTF-8' }}
    }});
  }}
}}"""
with open('worker.js', 'w') as f:
    f.write(worker)
```

### So sánh các cách:

| Cách | Setup | Thời gian sống | Cần login? | Dùng được trên đt? | Custom domain? |
|------|-------|---------------|------------|-------------------|---------------|
| Local server | 0 (chạy 1 lệnh) | Khi server chạy | Không | Không (cùng mạng) | ❌ |
| **localtunnel** | 0 (npx.cmd auto-download) | Khi tunnel chạy | Không | ✅ Có | ❌ |
| SSH tunnel | 0 (dùng SSH có sẵn) | Khi tunnel chạy | Không | ✅ Có | ❌ |
| **Cloudflare Workers** | 1 file JS + wrangler | Vĩnh viễn (temp) | Không | ✅ Có | ❌ (cần upgrade) |
| **Cloudflare Tunnel** | Config file | Khi tunnel chạy | Có (CF token) | ✅ Có | ✅ Cấu hình được |
| GitHub | 1 lần init | Vĩnh viễn | Có | ✅ Có | ❌ |

**Recommend:** 
- Xem nhanh, tạm thời → **localtunnel** (Windows) hoặc **SSH tunnel** (Linux/Mac)
- Deploy static HTML không cần domain → **Cloudflare Workers** (`--temporary`)
- Production với domain riêng → **Cloudflare Tunnel**
- Lưu trữ lâu dài → **GitHub**

---

## 🌐 Vietnamese-specific considerations

Khi thiết kế hệ thống cho người dùng Việt Nam:

| Domain | Vietnamese-specific | Recommendation |
|--------|-------------------|----------------|
| **STT** | Accent, tone, code-switching | faster-whisper (hỗ trợ tiếng Việt tốt) |
| **NLP** | spaCy vi model accuracy thấp | Underthesea + rule-based hybrid |
| **Critique** | Sắc thái văn hóa | LLM (rule-based không đủ) |
| **UI** | Người dùng quen Telegram | Telegram bot > Web app |
| **Audio** | Tên riêng, từ mượn | Language detection tự động |

---

## 🛠️ Tool sử dụng trong worklow

| Công cụ | Khi nào dùng |
|----------|-------------|
| `write_file` | Tạo documents markdown |
| `terminal` | Kiểm tra dependencies, chạy server |
| `skill_manage` | Lưu workflow thành skill mới |
| `read_file` | Review design cũ để critique |
| `execute_code` | Script phân tích nặng |

---

## 🎨 Khi user có Design System riêng (design.md / DESIGN.md)

Nếu user đưa ra một file design system spec (thường là `design.md` với color tokens, typography, spacing, component standards):

1. **Đọc kỹ** — các token màu, spacing, radius là bất di bất dịch. Không deviate.
2. **Lưu reference** — copy design spec vào `references/design-system-v1.md` dưới skill phù hợp
3. **Implement CSS tokens** — dùng `:root` CSS variables mapping trực tiếp từ design tokens
4. **Strict checklist** — mọi component (button, card, input) phải đúng kích thước + radius từ spec
5. **Gửi preview link trước** — user critique design rồi mới refine

> **Pitfall:** Không tự ý chọn màu/mix style khi đã có design spec. User đã define — chỉ việc follow.

**Reference files:**
- `references/design-system-v1.md` — earlier version of user's design spec
- `references/user-design-system.md` — full Black/White/Yellow Premium Dashboard spec (2026-07-12), definitive version
- `references/port-health-monitor.md` — Python script + cron to auto-restart dead service ports

Sau khi có documents, dựng server để user xem đẹp:

```bash
# Node.js (nếu có npm)
npm install marked
node -e "
const h=require('http'),fs=require('fs'),m=require('marked');
h.createServer((q,r)=>{
  const p='.'+decodeURIComponent(q.url);
  if(p.endsWith('.md')) fs.readFile(p,'utf8',(e,d)=>r.end(m.parse(d)));
  else r.end('ok');
}).listen(8080)
" &
```

Hoặc dùng `server.js` pattern (xem reference file).

---

## Pitfalls

1. **❌ Code quá sớm.** Luôn luôn critique trước. Nếu user thúc, nói: "Em muốn critique design trước để tránh phải viết lại sau."
2. **❌ Bỏ qua Vietnamese-specific.** Thư viện tiếng Anh không làm việc tốt cho tiếng Việt.
3. **❌ Linear roadmap.** Phải map dependency graph trước khi assign priority.
4. **❌ Không vẽ interaction flow.** Không thể biết UX có vấn đề nếu không simulate user.
5. **❌ Over-engineering.** Bắt đầu với SQLite, không cần PostgreSQL. Bắt đầu với rule-based, thêm LLM sau.
6. **❌ Không có mock data fallback.** Khi DB chưa sẵn sàng (migration chưa chạy, credentials chưa có), build components với mock data trong client. Dùng pattern: nếu DB lỗi hoặc data rỗng -> render mock data + notice "chạy migration để có dữ liệu thật". Khi DB có dữ liệu, app tự động chuyển từ mock sang real.
7. **❌ Không tạo visual overview.** User cần cái nhìn tổng thể để phản hồi — HTML flow overview giúp user thấy được architecture trước khi code.
8. **❌ Không share design.** Sau khi có documents xong, phải share cho user xem được (tunnel / GitHub). Đừng để user chỉ đọc raw markdown trên terminal.
9. **❌ Không tạo UI prototype trước.** User muốn THẤY giao diện trước khi code. Đừng nhảy từ plan sang Next.js project ngay — dựng HTML prototype tĩnh trước, cho user review design, RỒI mới code. User đã nói: "dựng tạm thời html lên để tôi review design đã".
10. **❌ Sai Design System tokens.** Nếu user có design spec (màu, radius, spacing), phải dùng CHÍNH XÁC. Dùng :root CSS variables, không deviate. Sai màu #FFD600 hay radius 28px là lỗi nghiêm trọng.
11. **❌ Dùng component library cho prototype.** shadcn, MUI, Chakra cho prototype là sai cách — dùng HTML thuần + CSS, nhanh và nhẹ. User critique xong rồi mới chuyển sang framework.
