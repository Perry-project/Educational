// Merges one nightly delta file ("AP Career Database - YYYY-MM-DD - delta.txt" or
// "Course Grip - YYYY-MM-DD - delta.txt", JSON written by the nightly Drive routines)
// into db/seed/*.json. Run `npm run db:import` afterwards
// to push the seeds into Postgres, then `npm run db:index` to publish a fresh INDEX.
//
// Usage: node scripts/merge-drive-delta.mjs --file <path to delta .txt/.json>
//
// Rows upsert on each table's natural key (same key = update, new key = append).
// Entrance exams already at tier_1_official are never overwritten - they were checked
// by hand against official notifications, and the nightly routine only has secondary
// sources. Such rows are reported as skipped so a human can review the proposed change.

import { readFileSync, writeFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import path from "node:path";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const seedDir = path.join(__dirname, "..", "db", "seed");

const KEYS = {
  schools: "school_type",
  pathways: "pathway_name",
  entrance_exams: "exam_name",
  careers: "career_name",
};

function parseArgs() {
  const args = process.argv.slice(2);
  const out = {};
  for (let i = 0; i < args.length; i += 2) {
    out[args[i].replace(/^--/, "")] = args[i + 1];
  }
  return out;
}

const seedPath = (name) => path.join(seedDir, `${name}.json`);
const loadSeed = (name) => JSON.parse(readFileSync(seedPath(name), "utf-8"));

const { file } = parseArgs();
if (!file) {
  console.error("Usage: node scripts/merge-drive-delta.mjs --file <delta file>");
  process.exit(1);
}

// Drive's text reader can add markdown escapes (\_ \[ \]) if the file was copied from
// read_file_content output rather than downloaded; strip them before parsing.
let raw = readFileSync(file, "utf-8").replace(/^﻿/, "");
let delta;
try {
  delta = JSON.parse(raw);
} catch {
  delta = JSON.parse(raw.replace(/\\([_\[\]<>~*])/g, "$1"));
}

const summary = [];
for (const [table, key] of Object.entries(KEYS)) {
  const incoming = delta.upserts?.[table] ?? [];
  if (!incoming.length) continue;
  const rows = loadSeed(table);
  let added = 0, updated = 0;
  const skipped = [];
  for (const r of incoming) {
    if (!r[key]) throw new Error(`${table} row missing "${key}": ${JSON.stringify(r).slice(0, 120)}`);
    const existing = rows.find((x) => x[key] === r[key] && x.state === r.state);
    if (existing) {
      if (table === "entrance_exams" && existing.data_tier === "tier_1_official") {
        skipped.push(r[key]);
        continue;
      }
      Object.assign(existing, r);
      updated++;
    } else {
      rows.push(table === "entrance_exams"
        ? { ...r, source_type: r.source_type ?? "secondary_aggregator", data_tier: "pending_review", verified_date: null }
        : r);
      added++;
    }
  }
  writeFileSync(seedPath(table), JSON.stringify(rows, null, 2) + "\n");
  summary.push(`${table}: +${added} new, ${updated} updated` + (skipped.length ? `, skipped tier_1 rows: ${skipped.join("; ")}` : ""));
}

// Course Grip deltas: course_topics upsert on (course_name, topic_name), matching the
// table's (course_id, topic_name) unique key. course_name must exist in courses.json.
const topics = delta.upserts?.course_topics ?? [];
if (topics.length) {
  const courseNames = new Set(loadSeed("courses").map((c) => c.course_name));
  const rows = loadSeed("course_topics");
  let added = 0, updated = 0;
  for (const r of topics) {
    if (!courseNames.has(r.course_name)) throw new Error(`course_topics row has unknown course_name: ${r.course_name}`);
    const existing = rows.find((x) => x.course_name === r.course_name && x.topic_name === r.topic_name);
    if (existing) { Object.assign(existing, r); updated++; }
    else { rows.push(r); added++; }
  }
  writeFileSync(seedPath("course_topics"), "[\n" + rows.map((r) => "  " + JSON.stringify(r)).join(",\n") + "\n]\n");
  summary.push(`course_topics: +${added} new, ${updated} updated`);
}

if (delta.progress_tracker?.length) {
  const pt = loadSeed("progress_tracker");
  for (const r of delta.progress_tracker) {
    const i = pt.findIndex((x) => x.phase === Number(r.phase));
    const row = { ...r, phase: Number(r.phase) };
    if (i >= 0) pt[i] = { ...pt[i], ...row };
    else pt.push(row);
  }
  pt.sort((a, b) => a.phase - b.phase);
  writeFileSync(seedPath("progress_tracker"), "[\n" + pt.map((r) => "  " + JSON.stringify(r)).join(",\n") + "\n]\n");
  summary.push(`progress_tracker: ${delta.progress_tracker.length} phase rows merged`);
}

console.log(`Merged delta ${delta.snapshot_date ?? "?"} (checkpoint ${delta.checkpoint ?? "?"}):\n  ` + (summary.join("\n  ") || "nothing to merge"));
