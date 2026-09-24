// Writes "AP Career Database - INDEX - YYYY-MM-DD.txt": the key of every row already in
// db/seed plus the progress tracker. The nightly Drive routine reads the newest INDEX to
// know what exists, so it only researches new rows and saves them as a small delta.
//
// Usage: node scripts/write-drive-index.mjs [--out <dir>]
// Default --out is the Google Drive for desktop folder "G:/My Drive", which syncs the
// file to Drive with no manual upload.

import { readFileSync, writeFileSync, existsSync } from "node:fs";
import { fileURLToPath } from "node:url";
import path from "node:path";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const seedDir = path.join(__dirname, "..", "db", "seed");
const loadSeed = (name) => JSON.parse(readFileSync(path.join(seedDir, `${name}.json`), "utf-8"));

const args = process.argv.slice(2);
const outFlag = args.indexOf("--out");
const outDir = outFlag >= 0 ? args[outFlag + 1] : "G:/My Drive";
if (!existsSync(outDir)) {
  console.error(`Output folder not found: ${outDir} (is Google Drive for desktop running?)`);
  process.exit(1);
}

const today = new Date().toLocaleDateString("en-CA", { timeZone: "Asia/Kolkata" });
const index = {
  index_date: today,
  note: "Keys of every row already in the Perry database. A nightly delta must not re-add these unless it is correcting or extending that row (same key = update).",
  keys: {
    schools: loadSeed("schools").map((r) => r.school_type),
    pathways: loadSeed("pathways").map((r) => r.pathway_name),
    entrance_exams: loadSeed("entrance_exams").map((r) =>
      r.exam_name + (r.data_tier === "tier_1_official" ? "  [tier_1_official - do not modify]" : "")),
    careers: loadSeed("careers").map((r) => `${r.career_name} (${r.category})`),
    courses: loadSeed("courses").map((r) => r.course_name),
  },
  // Topic names per course, for the nightly Course Grip routine (every course listed,
  // including ones with no topics yet, so it can pick the least-covered).
  course_topics: Object.fromEntries(loadSeed("courses").map((c) => [
    c.course_name,
    loadSeed("course_topics").filter((t) => t.course_name === c.course_name)
      .sort((a, b) => a.sequence_order - b.sequence_order).map((t) => t.topic_name),
  ])),
  progress_tracker: loadSeed("progress_tracker"),
};

const out = path.join(outDir, `AP Career Database - INDEX - ${today}.txt`);
writeFileSync(out, JSON.stringify(index, null, 1));
console.log(`Wrote ${out}`);
