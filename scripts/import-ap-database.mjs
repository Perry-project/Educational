// Imports the nightly "AP Career Database" Google Drive snapshot into the local
// Postgres database, split into schools / pathways / entrance_exams / courses /
// colleges / careers / progress_tracker. Safe to re-run: every table upserts on
// its natural key, so running today's data on top of yesterday's just merges.
//
// Usage: node scripts/import-ap-database.mjs --file-id <driveFileId> --snapshot-date YYYY-MM-DD --title "AP Career Database - YYYY-MM-DD"
// Seed JSON (transcribed from the Drive snapshot) lives in db/seed/*.json.

import { readFileSync, existsSync } from "node:fs";
import { fileURLToPath } from "node:url";
import path from "node:path";
import pg from "pg";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const repoRoot = path.join(__dirname, "..");
const seedDir = path.join(repoRoot, "db", "seed");

const envPath = path.join(repoRoot, ".env");
if (existsSync(envPath)) {
  process.loadEnvFile(envPath);
}

function loadSeed(name) {
  return JSON.parse(readFileSync(path.join(seedDir, `${name}.json`), "utf-8"));
}

function parseArgs() {
  const args = process.argv.slice(2);
  const out = {};
  for (let i = 0; i < args.length; i += 2) {
    out[args[i].replace(/^--/, "")] = args[i + 1];
  }
  return out;
}

async function getStateId(client, cache, name) {
  if (cache.has(name)) return cache.get(name);
  const res = await client.query(
    `INSERT INTO states (name) VALUES ($1)
     ON CONFLICT (name) DO UPDATE SET name = EXCLUDED.name
     RETURNING id`,
    [name]
  );
  cache.set(name, res.rows[0].id);
  return res.rows[0].id;
}

async function importSchools(client, stateCache) {
  const rows = loadSeed("schools");
  for (const r of rows) {
    const stateId = await getStateId(client, stateCache, r.state);
    await client.query(
      `INSERT INTO schools (state_id, school_type, board_authority, ownership, classes_covered,
         medium_of_instruction, key_exam, exam_window, passing_criteria, next_step, approx_fee, source, updated_at)
       VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12, now())
       ON CONFLICT (state_id, school_type) DO UPDATE SET
         board_authority = EXCLUDED.board_authority,
         ownership = EXCLUDED.ownership,
         classes_covered = EXCLUDED.classes_covered,
         medium_of_instruction = EXCLUDED.medium_of_instruction,
         key_exam = EXCLUDED.key_exam,
         exam_window = EXCLUDED.exam_window,
         passing_criteria = EXCLUDED.passing_criteria,
         next_step = EXCLUDED.next_step,
         approx_fee = EXCLUDED.approx_fee,
         source = EXCLUDED.source,
         updated_at = now()`,
      [stateId, r.school_type, r.board_authority, r.ownership, r.classes_covered,
       r.medium_of_instruction, r.key_exam, r.exam_window, r.passing_criteria,
       r.next_step, r.approx_fee, r.source]
    );
  }
  return rows.length;
}

async function importPathways(client, stateCache) {
  const rows = loadSeed("pathways");
  for (const r of rows) {
    const stateId = await getStateId(client, stateCache, r.state);
    await client.query(
      `INSERT INTO pathways (state_id, pathway_name, eligibility, admission_route,
         application_window, duration, leads_to, source, updated_at)
       VALUES ($1,$2,$3,$4,$5,$6,$7,$8, now())
       ON CONFLICT (state_id, pathway_name) DO UPDATE SET
         eligibility = EXCLUDED.eligibility,
         admission_route = EXCLUDED.admission_route,
         application_window = EXCLUDED.application_window,
         duration = EXCLUDED.duration,
         leads_to = EXCLUDED.leads_to,
         source = EXCLUDED.source,
         updated_at = now()`,
      [stateId, r.pathway_name, r.eligibility, r.admission_route,
       r.application_window, r.duration, r.leads_to, r.source]
    );
  }
  return rows.length;
}

async function importEntranceExams(client, stateCache) {
  const rows = loadSeed("entrance_exams");
  for (const r of rows) {
    const stateId = await getStateId(client, stateCache, r.state);
    await client.query(
      `INSERT INTO entrance_exams (state_id, exam_name, full_form_body, eligibility,
         application_window, exam_date, admits_into, source, source_type, data_tier, verified_date, updated_at)
       VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11, now())
       ON CONFLICT (state_id, exam_name) DO UPDATE SET
         full_form_body = EXCLUDED.full_form_body,
         eligibility = EXCLUDED.eligibility,
         application_window = EXCLUDED.application_window,
         exam_date = EXCLUDED.exam_date,
         admits_into = EXCLUDED.admits_into,
         source = EXCLUDED.source,
         source_type = EXCLUDED.source_type,
         data_tier = EXCLUDED.data_tier,
         verified_date = EXCLUDED.verified_date,
         updated_at = now()`,
      [stateId, r.exam_name, r.full_form_body, r.eligibility,
       r.application_window, r.exam_date, r.admits_into, r.source,
       r.source_type ?? null, r.data_tier ?? "pending_review", r.verified_date ?? null]
    );
  }
  return rows.length;
}

async function importCourses(client) {
  const rows = loadSeed("courses");
  for (const r of rows) {
    await client.query(
      `INSERT INTO courses (course_name, category, typical_duration, entry_via, source, source_type, data_tier, verified_date, updated_at)
       VALUES ($1,$2,$3,$4,$5,$6,$7,$8, now())
       ON CONFLICT (course_name) DO UPDATE SET
         category = EXCLUDED.category,
         typical_duration = EXCLUDED.typical_duration,
         entry_via = EXCLUDED.entry_via,
         source = EXCLUDED.source,
         source_type = EXCLUDED.source_type,
         data_tier = EXCLUDED.data_tier,
         verified_date = EXCLUDED.verified_date,
         updated_at = now()`,
      [r.course_name, r.category, r.typical_duration, r.entry_via, r.source,
       r.source_type ?? null, r.data_tier ?? "pending_review", r.verified_date ?? null]
    );
  }
  return rows.length;
}

async function importCourseTopics(client) {
  const rows = loadSeed("course_topics");
  let imported = 0;
  for (const r of rows) {
    const res = await client.query(`SELECT id FROM courses WHERE course_name = $1`, [r.course_name]);
    if (res.rows.length === 0) {
      console.warn(`Skipping topic "${r.topic_name}": no course named "${r.course_name}" in courses table`);
      continue;
    }
    const courseId = res.rows[0].id;
    await client.query(
      `INSERT INTO course_topics (course_id, topic_name, sequence_order, why_it_matters, builds_toward, source, updated_at)
       VALUES ($1,$2,$3,$4,$5,$6, now())
       ON CONFLICT (course_id, topic_name) DO UPDATE SET
         sequence_order = EXCLUDED.sequence_order,
         why_it_matters = EXCLUDED.why_it_matters,
         builds_toward = EXCLUDED.builds_toward,
         source = EXCLUDED.source,
         updated_at = now()`,
      [courseId, r.topic_name, r.sequence_order ?? null, r.why_it_matters, r.builds_toward, r.source]
    );
    imported++;
  }
  return imported;
}

async function importColleges(client, stateCache) {
  const rows = loadSeed("colleges");
  for (const r of rows) {
    const stateId = await getStateId(client, stateCache, r.state);
    await client.query(
      `INSERT INTO colleges (state_id, college_name, ownership, offers_courses, admission_route, source, source_type, data_tier, verified_date, updated_at)
       VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9, now())
       ON CONFLICT (state_id, college_name) DO UPDATE SET
         ownership = EXCLUDED.ownership,
         offers_courses = EXCLUDED.offers_courses,
         admission_route = EXCLUDED.admission_route,
         source = EXCLUDED.source,
         source_type = EXCLUDED.source_type,
         data_tier = EXCLUDED.data_tier,
         verified_date = EXCLUDED.verified_date,
         updated_at = now()`,
      [stateId, r.college_name, r.ownership, r.offers_courses, r.admission_route, r.source,
       r.source_type ?? null, r.data_tier ?? "pending_review", r.verified_date ?? null]
    );
  }
  return rows.length;
}

async function importCutoffs(client) {
  const rows = loadSeed("cutoffs");
  let imported = 0;
  for (const r of rows) {
    const collegeRes = await client.query(`SELECT id FROM colleges WHERE college_name = $1`, [r.college_name]);
    const courseRes = await client.query(`SELECT id FROM courses WHERE course_name = $1`, [r.course_name]);
    if (collegeRes.rows.length === 0 || courseRes.rows.length === 0) {
      console.warn(`Skipping cutoff for "${r.college_name}" / "${r.course_name}": college or course not found`);
      continue;
    }
    if (!r.source || !r.verified_date) {
      console.warn(`Skipping cutoff for "${r.college_name}" / "${r.course_name}" / ${r.category} ${r.year}: missing required source or verified_date (tier_1_official only)`);
      continue;
    }
    await client.query(
      `INSERT INTO cutoffs (college_id, course_id, category, year, closing_rank, closing_marks,
         source, source_type, verified_date, updated_at)
       VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9, now())
       ON CONFLICT (college_id, course_id, category, year) DO UPDATE SET
         closing_rank = EXCLUDED.closing_rank,
         closing_marks = EXCLUDED.closing_marks,
         source = EXCLUDED.source,
         source_type = EXCLUDED.source_type,
         verified_date = EXCLUDED.verified_date,
         updated_at = now()`,
      [collegeRes.rows[0].id, courseRes.rows[0].id, r.category, r.year,
       r.closing_rank ?? null, r.closing_marks ?? null,
       r.source, r.source_type ?? "government_notification", r.verified_date]
    );
    imported++;
  }
  return imported;
}

async function importCareers(client, stateCache) {
  const rows = loadSeed("careers");
  for (const r of rows) {
    const stateId = await getStateId(client, stateCache, r.state);
    await client.query(
      `INSERT INTO careers (state_id, career_name, category, entry_point, required_exams,
         eligibility, govt_private_options, next_step, source, updated_at)
       VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9, now())
       ON CONFLICT (state_id, career_name) DO UPDATE SET
         category = EXCLUDED.category,
         entry_point = EXCLUDED.entry_point,
         required_exams = EXCLUDED.required_exams,
         eligibility = EXCLUDED.eligibility,
         govt_private_options = EXCLUDED.govt_private_options,
         next_step = EXCLUDED.next_step,
         source = EXCLUDED.source,
         updated_at = now()`,
      [stateId, r.career_name, r.category, r.entry_point, r.required_exams,
       r.eligibility, r.govt_private_options, r.next_step, r.source]
    );
  }
  return rows.length;
}

async function importProgressTracker(client) {
  const rows = loadSeed("progress_tracker");
  for (const r of rows) {
    await client.query(
      `INSERT INTO progress_tracker (phase, topic, scope, status, last_updated, notes)
       VALUES ($1,$2,$3,$4,$5,$6)
       ON CONFLICT (phase) DO UPDATE SET
         topic = EXCLUDED.topic,
         scope = EXCLUDED.scope,
         status = EXCLUDED.status,
         last_updated = EXCLUDED.last_updated,
         notes = EXCLUDED.notes`,
      [r.phase, r.topic, r.scope, r.status, r.last_updated, r.notes]
    );
  }
  return rows.length;
}

async function main() {
  const args = parseArgs();
  const fileId = args["file-id"] ?? "manual-transcription";
  const snapshotDate = args["snapshot-date"] ?? null;
  const title = args["title"] ?? "AP Career Database (manual import)";

  const client = new pg.Client({
    connectionString: process.env.DATABASE_URL,
  });
  await client.connect();

  try {
    await client.query("BEGIN");
    const stateCache = new Map();

    const schoolsCount = await importSchools(client, stateCache);
    const pathwaysCount = await importPathways(client, stateCache);
    const examsCount = await importEntranceExams(client, stateCache);
    const coursesCount = await importCourses(client);
    const topicsCount = await importCourseTopics(client);
    const collegesCount = await importColleges(client, stateCache);
    const cutoffsCount = await importCutoffs(client);
    const careersCount = await importCareers(client, stateCache);
    const progressCount = await importProgressTracker(client);

    const totalRows = schoolsCount + pathwaysCount + examsCount + coursesCount + topicsCount + collegesCount + cutoffsCount + careersCount + progressCount;

    await client.query(
      `INSERT INTO import_log (source_file_id, source_title, snapshot_date, imported_at, rows_imported)
       VALUES ($1,$2,$3, now(), $4)
       ON CONFLICT (source_file_id) DO UPDATE SET
         source_title = EXCLUDED.source_title,
         snapshot_date = EXCLUDED.snapshot_date,
         imported_at = now(),
         rows_imported = EXCLUDED.rows_imported`,
      [fileId, title, snapshotDate, totalRows]
    );

    await client.query("COMMIT");

    console.log(`Imported: ${schoolsCount} schools, ${pathwaysCount} pathways, ${examsCount} entrance exams, ${coursesCount} courses, ${topicsCount} course topics, ${collegesCount} colleges, ${cutoffsCount} cutoffs, ${careersCount} careers, ${progressCount} progress-tracker rows.`);
  } catch (err) {
    await client.query("ROLLBACK");
    throw err;
  } finally {
    await client.end();
  }
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
