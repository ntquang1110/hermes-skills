# Quick Node.js File Server cho Design Review

Dùng để serve folder local, render .md đẹp, xem như Chrome.

## Tạo server nhanh

```bash
cd /path/to/project
npm install marked
```

Tạo file `serve-docs.js`:

```javascript
const http = require('http');
const fs = require('fs');
const path = require('path');
const marked = require('marked');

const PORT = process.argv[2] || 8080;
const ROOT = process.cwd();
const HIDDEN = ['node_modules', 'package-lock.json', 'package.json', '.git'];

const MIME = {
  '.html': 'text/html; charset=utf-8',
  '.md':   'text/html; charset=utf-8',
  '.css':  'text/css',
  '.js':   'application/javascript',
  '.png':  'image/png',
  '.jpg':  'image/jpeg',
  '.svg':  'image/svg+xml',
};

http.createServer((req, res) => {
  const url = decodeURIComponent(req.url.split('?')[0]);
  const full = path.join(ROOT, url);

  if (!full.startsWith(ROOT)) return res.writeHead(403).end('Forbidden');

  fs.stat(full, (err, stat) => {
    if (err) return res.writeHead(404).end('Not found');

    if (stat.isDirectory()) {
      fs.readdir(full, { withFileTypes: true }, (_, entries) => {
        const files = entries
          .filter(e => !e.name.startsWith('.') && !HIDDEN.includes(e.name))
          .map(e => ({
            name: e.name + (e.isDirectory() ? '/' : ''),
            isDir: e.isDirectory(),
          }))
          .sort((a, b) => b.isDir - a.isDir || a.name.localeCompare(b.name));

        res.writeHead(200, { 'Content-Type': 'text/html' });
        res.end(`<!DOCTYPE html>
<html lang="vi"><head><meta charset="UTF-8">
<title>${path.basename(url) || 'Home'}</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
  background:#0d1117;color:#c9d1d9;padding:40px;max-width:900px;margin:0 auto}
h1{color:#f0f6fc;margin-bottom:20px}
a{color:#58a6ff;text-decoration:none;display:block;padding:8px 12px;
  border-bottom:1px solid #21262d;font-size:1em}
a:hover{background:#161b22}
.dir{color:#58a6ff}.file{color:#c9d1d9}.icon{margin-right:8px}
.footer{margin-top:40px;padding-top:20px;border-top:1px solid #21262d;
  color:#484f58;text-align:center;font-size:0.85em}
</style></head><body>
<h1>📁 ${path.basename(url) || 'Project'}</h1>
${files.map(f => `<a href="${f.name}" class="${f.isDir?'dir':'file'}">
  <span class="icon">${f.isDir?'📁':'📄'}</span>${f.name}</a>`).join('')}
<div class="footer">Node.js File Server</div></body></html>`);
      });
    } else if (path.extname(full) === '.md') {
      fs.readFile(full, 'utf8', (_, content) => {
        res.writeHead(200, { 'Content-Type': 'text/html' });
        res.end(`<!DOCTYPE html>
<html lang="vi"><head><meta charset="UTF-8">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github-dark.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
<script>hljs.highlightAll();</script>
<title>${path.basename(full)}</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
  background:#0d1117;color:#c9d1d9;line-height:1.7;padding:32px;max-width:900px;margin:0 auto}
.nav{padding:12px 0;border-bottom:1px solid #30363d;margin-bottom:24px;color:#8b949e}
.nav a{color:#58a6ff;text-decoration:none}
h1{border-bottom:1px solid #21262d;padding-bottom:8px;margin:24px 0 16px;color:#f0f6fc}
h2{border-bottom:1px solid #21262d;padding-bottom:6px;margin:20px 0 12px;color:#f0f6fc}
h3{margin:16px 0 8px;color:#f0f6fc}
p{margin:0 0 12px}
a{color:#58a6ff}
code{background:#161b22;padding:2px 6px;border-radius:4px;font-size:0.9em}
pre{background:#161b22;border:1px solid #30363d;border-radius:8px;padding:16px;margin:16px 0;overflow-x:auto}
pre code{background:none;padding:0}
table{border-collapse:collapse;margin:16px 0;width:100%}
th,td{border:1px solid #30363d;padding:8px 14px;text-align:left}
th{background:#161b22;color:#f0f6fc}
tr:hover td{background:#161b22}
blockquote{border-left:4px solid #30363d;padding:0 16px;margin:16px 0;color:#8b949e}
ul,ol{padding-left:24px;margin:8px 0 16px}
li{margin:4px 0}
</style></head><body>
<div class="nav">📁 <a href="/">Home</a> / ${path.basename(url)}</div>
${marked.parse(content)}
</body></html>`);
      });
    } else {
      const mime = MIME[path.extname(full)] || 'application/octet-stream';
      res.writeHead(200, { 'Content-Type': mime });
      fs.createReadStream(full).pipe(res);
    }
  });
}).listen(PORT, () => console.log(`🌐 http://localhost:${PORT}/`));
```

## Chạy

```bash
node serve-docs.js 8080
# Mở http://localhost:8080/
```

## Tính năng

- ✅ Directory listing (filter node_modules, .git, package files)
- ✅ .md rendered as HTML (highlight.js cho code blocks)
- ✅ .html native render
- ✅ Dark theme GitHub-style
- ✅ 404 handling
