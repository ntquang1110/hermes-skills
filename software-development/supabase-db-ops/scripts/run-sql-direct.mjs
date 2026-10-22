/**
 * Chạy SQL migration lên Supabase qua connection Postgres trực tiếp.
 * Workaround khi /pg/query + exec_sql bị chặn.
 * Usage: npx tsx scripts/run-sql-direct.mjs sql/file.sql
 */
import dotenv from "dotenv";
import fs from "fs";
import pg from "pg";
dotenv.config();
const { Client } = pg;

const SQL_FILE = process.argv[2];
if (!SQL_FILE) { console.error("Usage: npx tsx scripts/run-sql-direct.mjs sql/file.sql"); process.exit(1); }
if (!fs.existsSync(SQL_FILE)) { console.error("File not found:", SQL_FILE); process.exit(1); }

const host = process.env.SUPABASE_URL.replace("https://", "").replace(".supabase.co", "");
const connStr = "postgresql://postgres:" + encodeURIComponent(process.env.SUPABASE_PASSWORD || "") + "@db." + host + ".supabase.co:5432/postgres";
const client = new Client({ connectionString: connStr, connectionTimeoutMillis: 15000 });

try {
  await client.connect();
  console.log("CONNECTED OK -> db." + host);
  const sql = fs.readFileSync(SQL_FILE, "utf-8");
  const res = await client.query(sql);
  console.log("SQL OK. rows:", res.rowCount);
  await client.end();
  process.exit(0);
} catch (e) {
  console.error("FAIL:", e.message);
  process.exit(1);
}
