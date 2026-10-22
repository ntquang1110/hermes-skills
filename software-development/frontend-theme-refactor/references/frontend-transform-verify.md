# Frontend Transform — Script Skeleton + Verify (TFO làm mẫu)

Mẫu từ session TFO Plasma Core: index.html 139KB → 150KB, 2643 dòng, single file, FastAPI serve static.

## Skeleton transform script (Python, viết qua write_file)

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import io

P = r"D:/path/app/static/index.html"
s = io.open(P, encoding="utf-8", newline="").read()   # newline='' GIỮ CRLF

def rep(old, new, expect=1):
    global s
    n = s.count(old)
    if n != expect:
        print(f"!! EXPECT {expect} got {n}: {old[:60]!r}")
    s = s.replace(old, new)

# 1) CSS block swap: index slicing giữa <style> và </style>
i0 = s.index("<style>") + len("<style>")
i1 = s.index("</style>", i0)
s = s[:i0] + "\n" + NEW_CSS + "\n" + s[i1:]

# 2) Replace cụ thể (SVG icons, data-contract dots, class checkbox...)
rep('OLD_EXACT_STRING', 'NEW_STRING')

# 3) Global strip emoji chrome 'X ' (chạy SAU replace cụ thể)
for e in ['📌 ','⚠️ ','👤 ','🤖 ','✅ ','🔴 ','🔵 ','🟡 ','🟢 ','⏰ ','🎯 ','📁 ','📋 ','📅 ','📊 ','🎙️ ','💬 ','➕ ','✏️ ']:
    n = s.count(e)
    if n: print(f"  strip {e!r} x{n}")
    s = s.replace(e, "")

# 4) Inject JS (starfield/tilt...) trước </body>
s = s.replace("</body>", "\n<script>/* ... */</script>\n</body>", 1)

io.open(P, "w", encoding="utf-8", newline="").write(s)

# 5) Kiểm tra cuối: emoji còn lại
import re
from collections import Counter
c = Counter(re.findall("[\U0001F300-\U0001FAFF\u2600-\u27BF\u2B00-\u2BFF\uFE0F]", s))
print("remaining:", dict(c) if c else "NONE")
```

Kinh nghiệm:
- **Write qua write_file, không heredoc** (heredoc strip dấu tiếng Việt).
- **Đừng truyền emoji literal qua `python -c` trong bash** — astral char bị mangle → count 0 sai. Dùng `\U0001F3A4` style escape.
- **Check CRLF**: `repr(s[i-6:i+12])` — nếu thấy `\r\n` thì pattern phải dùng `\r\n` (pattern `\n` sẽ count 0 vô cớ).
- Có thể chạy 2 pass: pass 1 transform lớn, pass 2 fix sót (in "remaining" để biết còn gì).
- Git Bash grep MSYS KHÔNG match astral emoji — dùng Python để tìm emoji còn lại, không dùng grep.

## Verify checklist chi tiết

### 1. Detector audit (browser)
- Serve bản tạm bỏ guard: `python -m http.server 8130` trong static dir → browser_navigate → browser_console chạy IIFE detector (script `ui-audit.js` trong skill impeccable).
- Kỳ vọng: `tells: []` (hoặc chỉ glassmorphism chủ ý + hard-offset-shadow false positive), radii ∈ {8px,12px,20px,50%,top-tab}, fonts có Inter+Space Grotesk(+JetBrains Mono), h1=1 h2=N.

### 2. JS integrity
```js
(function(){var fns=['switchTab','loadTasks','toggleTask','loadKanban','loadCalendar','loadProjects','renderKanban','loadAgentBoard','openTaskChat','closeTaskChat','toggleChatVoice','openProjectModal','saveProject','exportProject','openNewTaskModal','submitNewTask','openTaskModal','saveTaskEdit','floatingRecord','openAgentSub','loadThread','sendThreadMessage','checkAuth','doLogout','quickEnroll'];var missing=fns.filter(function(f){return typeof window[f]!=='function';});return JSON.stringify({total:fns.length,missing:missing});})()
```
Mọi script block độc lập — 1 block syntax error không chặn block khác, nên phải check function ở TỪNG block.

### 3. Switch tab
```js
['calendar','projects','kanban','agent','system','dashboard'].forEach(t=>{try{switchTab(t);}catch(e){...}})
```

### 4. Template render với stub fetch
```js
window.fetch=function(u){var s=String(u);
 if(s.indexOf('/api/tasks')>-1){return Promise.resolve({json:function(){return Promise.resolve({tasks:[{id:1,title:'A',done:false,assignee:'Dev1'},{id:2,title:'B',done:true,assignee:'CMO'}]});}});}
 if(s.indexOf('/api/projects')>-1){return Promise.resolve({json:function(){return Promise.resolve({projects:[{id:'p1',name:'Test',status:'blocked',color:'#FFD600'}]});}});}
 if(s.indexOf('/api/issues')>-1){return Promise.resolve({json:function(){return Promise.resolve({issues:[]});}});}
 return Promise.resolve({json:function(){return Promise.resolve({});}});};
loadKanban(); // rồi check kanbanBoard.innerHTML
```
Check output: class dot/checkbox đúng, không emoji regex, onclick giữ nguyên.

### 5. Mobile
- Quét inline `style="grid-template-columns:..."` — đưa vào class + media `!important`.
- Media query thêm: `.stats-row-4 { grid-template-columns:repeat(2,1fr) !important; }` tại max-width.

### 6. App thật
- `curl -s http://localhost:PORT/static/index.html | grep -c "marker"` xác nhận serve bản mới (FastAPI StaticFiles đọc disk mỗi request, không cần restart).
- Login page render; route có auth guard (/app) còn chặn.

## Upload service 8899 (publish mockup)
- Auth: `curl -s -c cj.txt -X POST -d "passcode=0512" http://localhost:8899/_auth` (302 = OK).
- Upload: `curl -s -b cj.txt -F "file=@<file>;filename=x.html;type=text/html" http://localhost:8899/api/upload`.
- **`-F file=@` path có space → exit 26** — copy ra thư mục không space, cd vào đó, dùng tên file tương đối.
- **Response URL dùng Host header** → khi curl localhost được `https://localhost:8899/r/<id>` (dead link). Tự suy URL public: `https://uploadhtml.thefirstonly.com/r/<id>` rồi curl verify 200 trước khi gửi user.
