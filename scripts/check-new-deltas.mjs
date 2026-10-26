// Lists nightly delta files in Google Drive for desktop ("G:/My Drive") that are not yet in
// the local import_log, with a count of rows per table in each. Run by the SessionStart
// hook in .claude/settings.json so every session opens knowing what new data is waiting.
//
// Usage: node scripts/check-new-deltas.mjs [--dir <folder>]

import { readFileSync, readdirSync, statSync, existsSync } from "node:fs";
import { fileURLToPath } from "node:url";
import path from "node:path";
import pg from "pg";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const envPath = path.join(__dirname, "..", ".env");
if (existsSync(envPath)) process.loadEnvFile(envPath);

const args = process.argv.slice(2);
const dirFlag = args.indexOf("--dir");
const dir = dirFlag >= 0 ? args[dirFlag + 1] : "G:/My Drive";
if (!existsSync(dir)) {
  console.log(`[Perry delta check] ${dir} not found (is Google Drive for desktop running?). Search Drive directly instead.`);
  process.exit(0);
}

// "Course Grip - 2026-10-20 - delta (1).txt": Drive for desktop adds " (n)" when a
// routine saves several checkpoints with the same title; keep the newest per routine+date.
const pattern = /^(AP Career Database|Course Grip|Second Chance) - (\d{4}-\d{2}-\d{2}) - delta( \(\d+\))?\.txt$/;
const newest = new Map();
for (const name of readdirSync(dir)) {
  const m = name.match(pattern);
  if (!m) continue;
  const mtime = statSync(path.join(dir, name)).mtimeMs;
  const key = `${m[1]}|${m[2]}`;
  if (!newest.has(key) || newest.get(key).mtime < mtime) {
    newest.set(key, { routine: m[1], date: m[2], name, mtime, title: `${m[1]} - ${m[2]} - delta.txt` });
  }
}

let imported = new Set();
const client = new pg.Client({ connectionString: process.env.DATABASE_URL });
try {
  await client.connect();
  // Titles were logged with suffixes like " (checkpoint 3)", so match on routine + date.
  const { rows } = await client.query("SELECT source_title FROM import_log");
  for (const { source_title } of rows) {
    const m = source_title.match(/^(AP Career Database|Course Grip|Second Chance) - (\d{4}-\d{2}-\d{2}) - delta/);
    if (m) imported.add(`${m[1]}|${m[2]}`);
  }
} catch (err) {
  console.log(`[Perry delta check] Could not read import_log (${err.message}). Is local Postgres running?`);
  process.exit(0);
} finally {
  await client.end().catch(() => {});
}

const pending = [...newest.values()]
  .filter((f) => !imported.has(`${f.routine}|${f.date}`))
  .sort((a, b) => a.date.localeCompare(b.date) || a.routine.localeCompare(b.routine));

if (pending.length === 0) {
  console.log("[Perry delta check] No new nightly data: every delta in G:/My Drive is already imported.");
  process.exit(0);
}

console.log(`[Perry delta check] ${pending.length} new delta file(s) waiting to be imported:`);
for (const f of pending) {
  let summary;
  try {
    const delta = JSON.parse(readFileSync(path.join(dir, f.name), "utf-8"));
    const parts = Object.entries(delta.upserts ?? {}).map(([table, rows]) => `${table}: ${Array.isArray(rows) ? rows.length : "?"}`);
    if (delta.progress_tracker) parts.push(`progress_tracker: ${delta.progress_tracker.length}`);
    if (delta.not_found?.length) parts.push(`not_found notes: ${delta.not_found.length}`);
    summary = parts.join(", ") || "empty";
  } catch (err) {
    summary = `could not parse (${err.message})`;
  }
  console.log(`- ${f.title}  [local file: ${path.join(dir, f.name)}]  ${summary}`);
}
console.log("Follow the CLAUDE.md session routine: report this to the user, import, verify, update the live flowchart.");
