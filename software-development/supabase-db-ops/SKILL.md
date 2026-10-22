---
name: supabase-db-ops
description: "Chạy SQL migration + verify schema trên Supabase khi REST/SDK bị chặn: dùng connection Postgres trực tiếp qua pg client (SUPABASE_PASSWORD). Covers /pg/query 404, exec_sql missing, RPC signature verification."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [supabase, postgres, sql, migration, database]
---

# Supabase DB Ops — Migration & Verify

Chạy DDL/migration lên Supabase + verify schema đã apply, khi các đường REST/SDK thông thường bị chặn.

## ⚠️ Đường cũ KHÔNG hoạt động (verified 2026-07-26)

| Cách | Kết quả | Vì sao |
|------|---------|--------|
| `POST {url}/pg/query` (service role) | **404 "requested path is invalid"** | Endpoint deprecated, không còn cho project mới |
| RPC `exec_sql` | **404 PGRST202** | Function không tồn tại trên DB (cần tạo thủ công trước) |

→ Đừng mất thời gian thử lại 2 cách này. Dùng connection trực tiếp.

## ✅ Cách hoạt động: Postgres direct connection

Project có sẵn `pg` trong devDependencies. `.env` có `SUPABASE_PASSWORD` (password của user `postgres`).

Connection string build từ env:
```
SUPABASE_URL = https://<ref>.supabase.co
→ postgresql://postgres:<urlencoded-SUPABASE_PASSWORD>@db.<ref>.supabase.co:5432/postgres
```

Script mẫu (lưu thành `scripts/run-sql-direct.mjs` trong project):
```js
import dotenv from "dotenv";
import fs from "fs";
import pg from "pg";
dotenv.config();
const { Client } = pg;
const host = process.env.SUPABASE_URL.replace("https://", "").replace(".supabase.co", "");
const connStr = "postgresql://postgres:" + encodeURIComponent(process.env.SUPABASE_PASSWORD || "") + "@db." + host + ".supabase.co:5432/postgres";
const client = new Client({ connectionString: connStr, connectionTimeoutMillis: 15000 });
await client.connect();
const res = await client.query(fs.readFileSync(process.argv[2], "utf-8"));
console.log("SQL OK. rows:", res.rowCount);
await client.end();
```

Chạy: `npx tsx scripts/run-sql-direct.mjs sql/<file>.sql`

**Lưu ý:**
- Dùng `.mjs` không phải `.ts` — `.ts` bị lỗi ESM default import (`dotenv`/`fs`/`pg` không có default export khi tsx type-check)
- `npx tsx -e "..."` với import inline cũng bị fail im lặng (output trống) — luôn viết file rồi chạy

## Verify migration đã apply

Script verify query `pg_proc` + `information_schema.columns`:
```sql
-- RPC tồn tại?
SELECT proname, pg_get_function_identity_arguments(oid) AS args
FROM pg_proc p JOIN pg_namespace n ON n.oid = p.pronamespace
WHERE p.proname = '<fn>' AND n.nspname = 'public';

-- Column tồn tại?
SELECT column_name FROM information_schema.columns
WHERE table_name = '<table>' AND column_name IN (...);
```

## RPC signature check (quan trọng khi đổi cách client gọi)

Khi client đổi từ `JSON.stringify(arr)` → truyền array trực tiếp (Supabase JS serialize thành JSONB):
- Verify signature khớp: `confirm_payment(p_payment_id uuid, p_confirmed_by text, p_allocations jsonb)`
- Nếu RPC khai báo `TEXT` cho tham số từng là string → đổi client sẽ vỡ. Luôn check `pg_get_function_identity_arguments` trước.

## Pitfalls

- `SUPABASE_PASSWORD` trong `.env` là password DB (user postgres) — KHÔNG phải service role key
- Connection qua `db.<ref>.supabase.co:5432` hoạt động từ máy local; nếu timeout/refused → thử pooler `aws-0-<region>.pooler.supabase.com:5432` với user `postgres.<ref>`
- Lỗi pre-existing TS lint (`esModuleInterop`, `downlevelIteration`...) trong repo không liên quan edit của mình — build `vite` vẫn pass, đừng hoảng
- Migration file phải có comment header (chuẩn repo: `-- ========== MÔ TẢ THAY ĐỔI / Ngày / ==========`)

## Scripts (skill này)

- `scripts/run-sql-direct.mjs` — chạy 1 file SQL migration qua direct connection. Copy vào project `scripts/` rồi `npx tsx scripts/run-sql-direct.mjs sql/<file>.sql`
- `scripts/verify-sql-applied.mjs` — verify RPC tồn tại + columns + RPC signature. Copy vào project rồi `npx tsx scripts/verify-sql-applied.mjs`

