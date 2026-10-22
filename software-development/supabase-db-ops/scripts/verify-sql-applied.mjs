/**
 * Verify migration đã apply lên Supabase + RPC signature.
 * Usage: npx tsx scripts/verify-sql-applied.mjs
 * Kiểm tra: RPC create_export_stock_order, warehouses cols, orders vtp cols, products weightGram
 */
import dotenv from "dotenv";
import pg from "pg";
dotenv.config();
const { Client } = pg;
const host = process.env.SUPABASE_URL.replace("https://", "").replace(".supabase.co", "");
const client = new Client({ connectionString: "postgresql://postgres:" + encodeURIComponent(process.env.SUPABASE_PASSWORD || "") + "@db." + host + ".supabase.co:5432/postgres", connectionTimeoutMillis: 15000 });
await client.connect();

// 1. RPC tồn tại + signature
const r1 = await client.query(`SELECT proname, pg_get_function_identity_arguments(oid) AS args FROM pg_proc p JOIN pg_namespace n ON n.oid = p.pronamespace WHERE p.proname = 'create_export_stock_order' AND n.nspname = 'public'`);
console.log("RPC create_export_stock_order:", r1.rowCount > 0 ? "✅ EXISTS " + r1.rows[0].args : "❌ MISSING");

// 2. Columns check
const r2 = await client.query(`SELECT table_name, column_name FROM information_schema.columns WHERE column_name IN ('provinceId','senderName','wardId','vtpOrderNumber','shippingProvinceId','weightGram') ORDER BY table_name, column_name`);
console.log("Columns:", r2.rowCount);
for (const c of r2.rows) console.log(`  - ${c.table_name}.${c.column_name}`);

// 3. RPC signature confirm_payment (quan trọng khi client đổi array vs string)
const r3 = await client.query(`SELECT pg_get_function_identity_arguments(oid) AS args FROM pg_proc p JOIN pg_namespace n ON n.oid = p.pronamespace WHERE p.proname = 'confirm_payment' AND n.nspname = 'public'`);
console.log("confirm_payment signature:", r3.rows[0]?.args || "❌ MISSING");

await client.end();
