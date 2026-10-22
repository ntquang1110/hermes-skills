/**
 * Gist + KV HTML Preview Worker
 *
 * Two storage backends:
 *   1. KV (direct) — POST /api/store with HTML → get preview URL
 *   2. GitHub Gist — GET /<gist_id> or /<gist_id>/filename or ?url=
 *
 * Routes:
 *   POST /api/store   { content: "<html>..." }  →  { id, preview_url }
 *   GET  /<id>                                     →  rendered HTML (KV → Gist)
 *   GET  /<id>/<filename>                          →  rendered HTML (Gist only)
 *   GET  /?url=<raw_url>                           →  rendered HTML (Gist only)
 */

const DEFAULT_FILE = 'index.html';
const GITHUB_USER  = 'ntquang1110';

// ─── MAIN ───
export default {
  async fetch(request, env) {
    const url     = new URL(request.url);
    const path    = url.pathname.replace(/^\/+/, '').replace(/\/+$/, '');
    const method  = request.method;
    const GITHUB_PAT = env.GITHUB_PAT || '';
    const STORE  = env.HTML_STORE;

    // CORS preflight
    if (method === 'OPTIONS') {
      return new Response(null, { headers: corsHeaders() });
    }

    // ── POST /api/store ──────────────────────────────────
    if (method === 'POST' && path === 'api/store') {
      try {
        return await handleStore(request, STORE);
      } catch (err) {
        return new Response(`Error: ${err.message}`, {
          status: 500,
          headers: { 'Content-Type': 'text/plain; charset=utf-8' },
        });
      }
    }

    // ── GET / — Homepage ─────────────────────────────────
    if (method === 'GET' && !path && !url.searchParams.has('gist') && !url.searchParams.has('url')) {
      return serveHome();
    }

    // ── GET /<id> — Serve from KV or Gist ────────────────
    // Try KV first (direct-stored content)
    if (method === 'GET' && path && STORE) {
      const kvContent = await STORE.get(path);
      if (kvContent !== null) {
        return new Response(kvContent, {
          headers: {
            'Content-Type': 'text/html; charset=utf-8',
            'Cache-Control': 'public, max-age=3600, s-maxage=3600',
            'Access-Control-Allow-Origin': '*',
            'X-Robots-Tag': 'noindex',
            'X-Source': 'kv',
            ...corsHeaders(),
          },
        });
      }
    }

    // Fallback: GitHub Gist
    return serveFromGist(url, path, GITHUB_PAT);
  },
};

// ─── STORE: POST /api/store ─────────────────────────────
async function handleStore(request, STORE) {
  let content;

  // Parse body: JSON or raw text
  const ct = request.headers.get('content-type') || '';
  if (ct.includes('application/json')) {
    const body = await request.json();
    content = body.content || body.html || '';
  } else {
    content = await request.text();
  }

  if (!content || content.trim().length === 0) {
    return new Response(JSON.stringify({ error: 'Empty content' }), {
      status: 400,
      headers: { 'Content-Type': 'application/json', ...corsHeaders() },
    });
  }

  // Validate size (KV max 25MB per value, but let's cap at 1MB)
  if (content.length > 1_048_576) {
    return new Response(JSON.stringify({ error: 'Content too large (>1MB)' }), {
      status: 413,
      headers: { 'Content-Type': 'application/json', ...corsHeaders() },
    });
  }

  // Generate unique ID (12 chars, URL-safe)
  const id = randomId();
  await STORE.put(id, content); // no expiration = permanent

  return new Response(JSON.stringify({
    id,
    preview_url: `https://preview.thefirstonly.com/${id}`,
    size: content.length,
  }), {
    headers: { 'Content-Type': 'application/json', ...corsHeaders() },
  });
}

// ─── GIST FETCH ─────────────────────────────────────────
async function serveFromGist(url, path, GITHUB_PAT) {
  // Build raw Gist URL
  let rawUrl;
  if (url.searchParams.has('url')) {
    rawUrl = url.searchParams.get('url');
  } else if (path) {
    const key = url.searchParams.get('gist') || path;
    const parts = key.split('/');
    const gistId   = parts[0].replace(/[^a-f0-9]/gi, '');
    const filename = parts[1] ? parts[1].trim() : DEFAULT_FILE;
    rawUrl = `https://gist.githubusercontent.com/${GITHUB_USER}/${gistId}/raw/${filename}`;
  } else {
    return new Response('Missing parameter', {
      status: 400,
      headers: { 'Content-Type': 'text/plain; charset=utf-8' },
    });
  }

  try {
    const fetchHeaders = { 'User-Agent': 'GistPreviewWorker/2.0' };
    if (GITHUB_PAT) {
      fetchHeaders['Authorization'] = `token ${GITHUB_PAT}`;
    }

    const gistResp = await fetch(rawUrl, { headers: fetchHeaders });

    if (!gistResp.ok) {
      const errText = await gistResp.text();
      const status  = gistResp.status;
      let msg;
      if (status === 404) {
        msg = `404 — Not found.\n  ${rawUrl}\n\nCheck ID or use POST /api/store for direct storage.`;
      } else if (status === 429) {
        msg = '429 — Rate limit. Refresh the page.';
      } else if (status === 403) {
        msg = `403 — Access denied (private?).\n  ${rawUrl}`;
      } else {
        msg = `GitHub HTTP ${status}\n  ${errText.slice(0, 500)}`;
      }
      return new Response(msg, {
        status,
        headers: { 'Content-Type': 'text/plain; charset=utf-8' },
      });
    }

    const content = await gistResp.text();
    return new Response(content, {
      headers: {
        'Content-Type': 'text/html; charset=utf-8',
        'Cache-Control': 'public, max-age=3600, s-maxage=3600',
        'Access-Control-Allow-Origin': '*',
        'X-Robots-Tag': 'noindex',
        'X-Source': 'gist',
        ...corsHeaders(),
      },
    });

  } catch (err) {
    return new Response(`Bad gateway: ${err.message}`, {
      status: 502,
      headers: { 'Content-Type': 'text/plain; charset=utf-8' },
    });
  }
}

// ─── HELPERS ────────────────────────────────────────────
function randomId() {
  // Simple random ID using Math.random (available in CF Workers)
  const chars = 'abcdefghijklmnopqrstuvwxyz0123456789';
  let id = '';
  for (let i = 0; i < 12; i++) {
    id += chars[Math.floor(Math.random() * chars.length)];
  }
  return id;
}

function corsHeaders() {
  return {
    'Access-Control-Allow-Origin':  '*',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
  };
}

// ─── HOMEPAGE ───────────────────────────────────────────
const HOME_HTML = `<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Gist HTML Preview</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    max-width: 780px; margin: 60px auto; padding: 0 24px;
    line-height: 1.6; color: #1f2937;
  }
  h1 { font-size: 2rem; margin-bottom: 0.5rem; }
  p { color: #6b7280; margin-bottom: 2rem; }
  h2 { font-size: 1.2rem; margin: 1.5rem 0 0.75rem; color: #374151; }
  code {
    background: #f3f4f6; padding: 2px 6px; border-radius: 4px;
    font-size: 0.9em; word-break: break-all;
  }
  .example {
    background: #f9fafb; border: 1px solid #e5e7eb;
    border-radius: 8px; padding: 16px 20px; margin-bottom: 12px;
  }
  .example h3 { font-size: 1rem; margin-bottom: 6px; color: #374151; }
  .example code.block {
    display: block; padding: 12px; margin-top: 4px;
    background: #1f2937; color: #e5e7eb; border-radius: 6px;
    font-size: 0.85rem; white-space: pre-wrap;
  }
  .tag {
    display: inline-block; font-size: 0.7rem; font-weight: 700;
    padding: 2px 8px; border-radius: 4px; margin-left: 6px;
    vertical-align: middle; letter-spacing: 0.04em;
  }
  .tag-kv { background: #dbeafe; color: #1d4ed8; }
  .tag-gist { background: #fef3c7; color: #92400e; }
  footer { margin-top: 48px; font-size: 0.85rem; color: #9ca3af; text-align: center; }
</style>
</head>
<body>
<h1>📄 Gist + KV Preview</h1>
<p>Two ways to preview HTML: store directly (KV) or via GitHub Gist</p>

<h2>🆕 Direct — không cần Gist</h2>
<div class="example">
  <h3>POST /api/store <span class="tag tag-kv">KV</span></h3>
  <code class="block">curl -X POST https://preview.thefirstonly.com/api/store \\
  -H "Content-Type: application/json" \\
  -d '{"content": "\u003Ch1\u003EHello\u003C/h1\u003E"}'</code>
  <p style="margin-top:8px;font-size:0.85rem;color:#6b7280;">→ Trả về JSON: <code>{"id":"abc123","preview_url":"https://preview.thefirstonly.com/abc123"}</code></p>
</div>

<h2>📁 Từ GitHub Gist</h2>
<div class="example">
  <h3>/&lt;gist_id&gt; <span class="tag tag-gist">Gist</span></h3>
  <code class="block">https://preview.thefirstonly.com/abc123</code>
</div>
<div class="example">
  <h3>/&lt;gist_id&gt;/&lt;filename&gt;</h3>
  <code class="block">https://preview.thefirstonly.com/abc123/report.html</code>
</div>
<div class="example">
  <h3>?url=&lt;raw_url&gt;</h3>
  <code class="block">https://preview.thefirstonly.com/?url=https://gist.githubusercontent.com/.../raw/index.html</code>
</div>

<footer>Preview Worker · KV + Gist backends</footer>
</body>
</html>`;

function serveHome() {
  return new Response(HOME_HTML, {
    headers: { 'Content-Type': 'text/html; charset=utf-8' },
  });
}
