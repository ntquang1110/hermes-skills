# Production Mode Deployment — Knowledge Flow

## Why production mode

`next start` (production) uses webpack-compiled bundles — no Turbopack, no Jest workers, no dev overlay. It's stable for daily browsing.

## Startup sequence

```bash
# 1. Export env vars (REQUIRED — next start ignores .env.local)
export NEXT_PUBLIC_SUPABASE_URL="https://vgozvweyqcqkayafntwx.supabase.co"
export NEXT_PUBLIC_SUPABASE_ANON_KEY="sb_publishable__Dcy-82VKsvQxSmtO1yD7Q_1_3gfp4_"

# 2. Build
cd /c/Users/NTQUANG_DELL/knowledge-flow
npx next build

# 3. Start
npx next start --port 3003
```

## After code changes

```bash
cd /c/Users/NTQUANG_DELL/knowledge-flow

# 1. Build new bundles
npx next build

# 2. Find and kill old server
netstat -ano | grep ":3003 " | grep LISTENING
taskkill /F /PID <pid>

# 3. Export env vars (every time — they don't persist across SSH)
export NEXT_PUBLIC_SUPABASE_URL="https://vgozvweyqcqkayafntwx.supabase.co"
export NEXT_PUBLIC_SUPABASE_ANON_KEY="sb_publishable__Dcy-82VKsvQxSmtO1yD7Q_1_3gfp4_"

# 4. Restart
npx next start --port 3003

# 5. Restart tunnel if needed
cloudflared tunnel --url http://localhost:3003 --protocol http2 --config ""
```

## Verification

```bash
curl -s http://localhost:3003/api/cards | python -c "import json,sys; d=json.loads(sys.stdin.read()); print(f'{len(d)} cards')"
curl -s http://localhost:3003/api/read-status
curl -s http://localhost:3003
```

## Kill tunnel

```bash
process(action='list')  # find cloudflared session_id
process(action='kill', session_id='...')
```

## Env vars (sensitive)

```
NEXT_PUBLIC_SUPABASE_URL: https://vgozvweyqcqkayafntwx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY: sb_publishable__Dcy-82VKsvQxSmtO1yD7Q_1_3gfp4_
KNOWLEDGE_API_KEY: hermes-knowledge-secret
```

These must be exported before `next start`.
