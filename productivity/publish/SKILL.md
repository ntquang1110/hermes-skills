---
name: publish
description: "Publish HTML, markdown, or text online with a preview URL."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [publish, upload, gist, preview, html, markdown, text, sharing, kv, unslop]
    related_skills: [html-unslop, field-map, github-auth]
---

# Publish (publish)

Skill **duy nhất** cho mọi nhu cầu xuất bản nội dung online. Nhận bất kỳ content nào (HTML, markdown, text), xử lý, và trả link preview ngay.

> Kết hợp `content-publish` + `md-publish` + `html-publishing` thành 1. HTML tự động qua `html-unslop` (skill riêng) trước khi publish.

## Flow

```
[Content] → [html-unslop (nếu HTML)] → [publish] → preview.thefirstonly.com/<id>
```

1. **Nhận** content (paste, file, stdin, hoặc skill khác truyền vào)
2. **Unslop** nếu là HTML (gọi skill `html-unslop`)
3. **Detect** loại: HTML / Markdown / Text
4. **Upload** KV (mặc định) hoặc Gist
5. **Trả** preview URL

## When to Use

- User paste HTML → muốn link xem online
- User viết markdown/ghi chú → muốn share
- User có text file → muốn URL tạm
- Agent skill khác sinh HTML → cần publish (field-map, design, report...)

**Không dùng cho:**
- File >1MB (KV/Gist giới hạn)
- File binary (ảnh, PDF)
- Download/attachment hosting (dùng object storage)
- Full website với custom domain (dùng GitHub Pages/VPS)

## Backends

| Backend | Command | Yêu cầu | Dùng khi | Preview |
|---------|---------|---------|----------|---------|
| **KV** (mặc định) | `--kv` | Không cần gì | HTML, text, publish nhanh | `preview.thefirstonly.com/<id>` |
| **Gist** | `--gist` | GitHub PAT | Markdown (render native), cần lưu nguồn | `gist.github.com/<user>/<id>` |

## Quick Usage

```bash
# HTML → KV (auto unslop, no PAT)
python scripts/content-upload.py --content "<h1>Hello</h1>" --title "Page"
python scripts/content-upload.py --file report.html --title "Báo cáo"

# Markdown → Gist (render native)
python scripts/content-upload.py --gist --content "# Note" --title "Note"

# Text → KV
python scripts/content-upload.py --content "plain text" --title "Text"

# Pipe stdin
cat doc.md | python scripts/content-upload.py --title "Doc"

# Force filename (chỉ với --gist)
python scripts/content-upload.py --gist --content "<h1>X</h1>" --name page.html
```

Output JSON: `{preview_url, gist_url, gist_id, filename, type}`

## Workflow trong Agent

```python
from hermes_tools import terminal

# Cách 1: script helper (recommended)
result = terminal(f'python scripts/content-upload.py --content {shell_quote(content)} --title "Page"', timeout=30)

# Cách 2: file có sẵn
result = terminal(f'python scripts/content-upload.py --file /path/file.html --title "Report"', timeout=30)
```

## Content Auto-Detection

| Content bắt đầu/ chứa | Extension | Backend | Preview |
|----------------------|-----------|---------|---------|
| `<html>`, `<div>`, `<h1>`... | `.html` | KV | `preview.thefirstonly.com/<id>` |
| `#`, `*`, `-`, `` ` ``, `\|`, `>` (markdown) | `.md` | Gist | `gist.github.com/...` |
| Còn lại | `.txt` | KV | `preview.thefirstonly.com/<id>` |

## Markdown Methods (từ md-publish)

Ngoài upload markdown → Gist, còn có thể convert MD → HTML:
```bash
python scripts/md-to-html.py --file doc.md --output doc.html
# Rồi upload HTML → KV
```

## Scripts

- `scripts/content-upload.py` — main script (upload KV/Gist + auto unslop)
- `scripts/md-to-html.py` — markdown → styled HTML converter
- `scripts/worker-gist-preview.js` — Cloudflare Worker source
- `scripts/wrangler.toml` — Worker config (KV + Gist backends)
- `templates/responsive-base.html` — responsive boilerplate (mobile-first, table→card)
- `references/` — standalone-page, kflow-push, research-protocol, interactive-dashboard...

## Notion Integration (optional workflow)

Sau khi có preview URL, có thể lưu thêm vào Notion (workflow cá nhân).

- **Kiến thức DB** (structured): entry với Name, Link, Chuyên ngành, Phân loại
  - DB ID: `38aee73e-673a-800e-b564-c2fc25c58097`
  - Chuyên ngành select: `Sinh học`, `Chăn nuôi`; Phân loại: `Bệnh học`, `Sản xuất`, `Tế bào`, `Virus`, `Tên lửa`
- **Standalone page** (không phù hợp DB): dưới "Blog của Quang" (`ae7b638f-5ab1-484e-a082-ed2888c8ae05`)
- Notion API key: `~/.hermes/.env` `NOTION_API_KEY`, version `2025-09-03`

```python
def create_notion_entry(name, link, chuyen_nganh='', phan_loai=''):
    import requests, os
    api_key = ''
    env = os.path.expanduser('~/AppData/Local/hermes/.env')
    with open(env) as f:
        for line in f:
            if 'NOTION_API_KEY' in line and line.strip() and not line.strip().startswith('#'):
                api_key = line.split('=', 1)[1].strip()
    headers = {'Authorization': f'Bearer {api_key}', 'Notion-Version': '2025-09-03', 'Content-Type': 'application/json'}
    properties = {'Name': {'title': [{'text': {'content': name}}]},
                  'Link': {'rich_text': [{'text': {'content': link}}]}}
    if chuyen_nganh: properties['Chuyên ngành'] = {'select': {'name': chuyen_nganh}}
    if phan_loai:    properties['Phân loại']    = {'select': {'name': phan_loai}}
    r = requests.post('https://api.notion.com/v1/pages',
        headers=headers, json={'parent': {'database_id': '38aee73e-673a-800e-b564-c2fc25c58097'}, 'properties': properties})
    return r.json() if r.status_code == 200 else r.text
```

**Notion logic:** Nội dung có Chuyên ngành/Phân loại hợp lý (Sinh học, Chăn nuôi...) → DB entry. Khác → standalone page. Luôn hỏi Chuyên ngành/Phân loại trước khi tạo DB entry. **Ngoại lệ:** user nói "không về Notion" / "chỉ cần link" → skip hoàn toàn, đừng hỏi.

## Common Pitfalls

1. **HTML auto-unslop.** Mọi HTML qua `html-unslop` — nếu user muốn giữ nguyên AI style (thương hiệu), dùng flag bỏ qua.
2. **Gist private.** Mặc định private — hỏi user nếu muốn public.
3. **File >1MB.** KV/Gist chặn. Báo user.
4. **Auto-detect nhầm.** Content lẫn lộn — ưu tiên HTML (KV render được). Dùng `--name` để force.
5. **preview.thefirstonly.com down.** Check DNS CNAME → Cloudflare Worker. `preview.thefirstonly.com` cũng có tunnel route tới KFlow (`localhost:3003`) — nếu preview 404/lạc vào KFlow, traffic đang về tunnel thay vì worker. Verify bằng curl preview thật, đừng giả định.
6. **Ký tự đặc biệt.** Dùng `shell_quote()` hoặc `json.dumps()` khi nhúng content.
7. **`read_file` làm hỏng HTML.** Trả về kèm số dòng (`1|<!DOCTYPE...`). Dùng `terminal('cat file.html')` để lấy raw. Không đưa `read_file` content vào upload.
8. **JS template literal escape.** KHÔNG dùng `\"` bên trong backtick. Render button có `data-tab`, sau đó `addEventListener` — không dùng inline `onclick` với escape. Tránh `javascript:` href.
9. **LUÔN verify bằng browser** trước khi báo xong: `browser_navigate(preview_url)` + `browser_console` đếm tab, click thực tế, check `js_errors`.
10. **Cache bản cũ.** User thấy bản cũ — test lại bằng browser, nếu browser chạy đúng là cache phía user → hard refresh (Ctrl+Shift+R) hoặc tab ẩn danh. Đừng sửa code khi code đã đúng.
11. **Cloudflare 1010 = chặn User-Agent, KHÔNG phải file quá cỡ.** Triệu chứng: POST `/api/store` trả `ConnectionResetError` hoặc HTTP 1010, trong khi GET trang preview vẫn 200. Nguyên nhân: Cloudflare WAF chặn UA `python-requests` / `urllib`. KHÔNG chẩn đoán thành "payload quá lớn" rồi đi minify file — sai hướng. Đã vá `scripts/content-upload.py` bằng header User-Agent giả lập trình duyệt; nếu vẫn gặp, gửi trực tiếp bằng `urllib` kèm `User-Agent: Mozilla/5.0 ... Chrome/… Safari/537.36`.
12. **Cỡ chữ sau khi co là lỗi hay gặp nhất ở sơ đồ SVG.** SVG dùng đơn vị user, khi khung hẹp (mobile 360px) thì scale = khung/viewBox và chữ co theo. viewBox rộng 700 đặt trong khung 328px → scale 0,469 → chữ 20 đơn vị chỉ còn 9,4px. Ngưỡng: **≥12px sau co**. Cách chắc ăn: sơ đồ dạng chuỗi/cột dùng HTML/CSS (cỡ chữ thật, tự xếp cột), chỉ dùng SVG khi cần topology thật.

## Verify sau khi publish (bắt buộc với HTML)

Mỗi lần POST tạo ID mới. **Link đưa user phải là bản publish cuối**, không phải bản đầu.

Không kết luận cỡ chữ bằng mắt trên screenshot: ảnh bị scale nên chữ trông nhỏ hơn thực tế. Đo bằng DOM.

**1. Tràn khung (desktop)**

```js
(()=>{const bad=[];document.querySelectorAll('.canvas').forEach((c,i)=>{const cr=c.getBoundingClientRect();c.querySelectorAll('*').forEach(el=>{const r=el.getBoundingClientRect();if(r.height>0&&(r.bottom>cr.bottom+1||r.right>cr.right+1))bad.push([i,el.className||el.tagName]);});});return JSON.stringify(bad);})()
```

Bắt mọi phần tử con tràn khỏi khung có `height` cố định. Lỗi hay gặp nhất: cung tròn / mũi tên đặt `top` + `height` lớn hơn khung → bị cắt cụt.

**2. Mobile 360px**

Media query trong iframe đánh giá theo bề rộng iframe. Nhúng iframe 360px rồi đo bên trong:

```js
const f=document.createElement('iframe');f.id='mobT';f.style.cssText='position:fixed;left:-9999px;top:0;width:360px;height:1700px;border:0';f.src=location.href;document.body.appendChild(f);
```

Chờ load rồi đo:

```js
(()=>{const f=document.getElementById('mobT'),d=f.contentDocument,w=f.contentWindow;const small=[];d.querySelectorAll('p,li,span,b,em,div').forEach(el=>{if(el.children.length)return;const fs=parseFloat(w.getComputedStyle(el).fontSize);const t=(el.innerText||'').trim();if(t&&fs<12)small.push([el.className,fs]);});return JSON.stringify({nBelow:small.length,below12:small,hOverflow:d.documentElement.scrollWidth>d.documentElement.clientWidth});})()
```

Ngưỡng: **0 phần tử chữ dưới 12px**, `hOverflow` = false.

Nhãn eyebrow 10px (`10px` + `letter-spacing`) phải nâng lên 12px trong media query. Nhớ specificity: `.fast .fl` (0,2,0) thắng `.fl` (0,1,0), nên phải viết lại đủ selector cha trong media query.

**3. Xem bằng mắt**

Đổi iframe sang `position:fixed;left:0;top:0;z-index:99999` rồi `browser_vision`. Dùng để soi bố cục, không dùng để kết luận cỡ chữ.

**4. Chống typo entity**

Viết tay `&#432;` rất dễ rơi dấu `;` thừa vào giữa từ: `l;&#432;&#7907;ng` hiển thị thành `l;ượng`. Quét trước khi publish:

```python
import io,re
s=io.open(p,encoding='utf-8').read()
print(re.findall(r"[A-Za-z];&#\d+;", s))       # phải rỗng
s2=re.sub(r"([A-Za-z]);(&#\d+;)", r"\1\2", s)   # sửa tự động
```

Kiểm tra thêm: mọi `&#\d+;` decode ra ký tự thật (`html.unescape`), không có `U+FFFD`, token lạ ngoài bảng chữ Việt chỉ được là ký hiệu toán (ρ, ×, ∝, ⁴).

**5. Đừng dùng `browser_navigate` để verify**

Nó trả về snapshot toàn trang, rất tốn token. Dùng `browser_console` với `location.href='<url>'` rồi đo bằng DOM.

## Verification Checklist

- [ ] Upload HTML → preview URL mở được trên mobile
- [ ] Không có phần tử con tràn khỏi khung (script mục 1)
- [ ] Mobile 360px: 0 chữ dưới 12px, không tràn ngang
- [ ] Không có `;` thừa trước entity (mục 4)
- [ ] Link gửi user là bản publish CUỐI
- [ ] HTML render đúng, JS không vỡ (unslop bảo vệ script)
- [ ] Upload markdown → Gist render đúng
- [ ] Upload text → hiển thị plain trên KV
- [ ] File path upload hoạt động
- [ ] Stdin pipe hoạt động
- [ ] Tag balance OK (validation sau unslop)

## Related Skills

- `html-unslop` — pre-processor: strip AI-isms khỏi HTML (tự động, gọi từ đây)
- `field-map` — tạo knowledge map HTML (dùng publish để share)
- `github-auth` — setup GitHub PAT
- `notion` — API Notion (tạo page/DB entry nếu cần)
13. **Lỗi `TimeoutError` / `ConnectionReset` khi POST file ~600KB–1MB KHÔNG phải file quá cỡ — là `timeout=30` trong script quá ngắn.** Đo thật 20/10/2026: payload 649KB mất **29–45 giây** mới trả 200, nên 30s là chết giữa đường; retry cũng chết. Đã vá `content-upload.py` → `timeout=180`. Nếu vẫn reset: gửi lại bằng `requests.post(..., timeout=180)` có retry 4 lần cách 8s (đã thành công ở lần thử đầu). **Đừng minify/đi cắt nội dung để chữa lỗi này.**
14. **KV không có slug — mỗi lần publish là URL mới, không ghi đè.** `randomId()` 12 ký tự. Hệ quả: hai trang link chéo nhau sẽ luôn trỏ bản liền trước. Cách chốt: giữ một file config (ví dụ `visual/preview-links.json`) chứa URL 2 trang, builder đọc config khi dựng, publish xong ghi lại URL mới vào config. Link cũ vẫn sống vĩnh viễn nên không gãy.
15. **File HTML nhiều dữ liệu: kiểm trùng lặp trước khi đổ lỗi cho KV.** Trường hợp thật: bảng "điểm neo" 22 mục chiếm 414KB vì mỗi mục chép nguyên văn câu, mà một câu xuất hiện ở nhiều mục. Gom về **bảng câu dùng chung + mục chỉ giữ chỉ số** → 414KB còn 128KB, cả trang 991KB còn 749KB, không mất chữ nào. Đo bằng `json.dumps(v, ensure_ascii=False).encode()` từng key để biết key nào phình, đừng đoán.

