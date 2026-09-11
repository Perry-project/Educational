@AGENTS.md

# Perry data pipeline

A nightly cloud routine ("AP Career Database") collects education/career data for
Andhra Pradesh and saves it as a Google Drive file titled `AP Career Database - YYYY-MM-DD`.
This project has a local Postgres database (see `db/schema.sql`) that mirrors that data,
split into `schools`, `pathways`, `entrance_exams`, `colleges`, `courses`, `careers`,
and `progress_tracker` tables, plus an `import_log` table tracking which Drive snapshot
was last merged in.

At the start of a session in this folder:
1. Search Google Drive (`title contains 'AP Career Database'`) for the newest snapshot by `createdTime`.
2. Check the local `import_log` table (`SELECT * FROM import_log ORDER BY snapshot_date DESC LIMIT 1`) to see if that snapshot has already been imported.
3. If there's a newer, not-yet-imported snapshot: fetch its content, update the relevant `db/seed/*.json` file(s) with anything new or changed (merge, don't overwrite unrelated rows), then run `npm run db:import -- --file-id <driveFileId> --snapshot-date <YYYY-MM-DD> --title "<file title>"`.
4. If nothing new exists, say so briefly and move on — don't re-run the import needlessly.

Do not import files from `Desktop/Perry`, `Desktop/Project`, or `perry-site.zip` into
this project. This is a fresh build — those are reference-only, not a source to port from.

## Data safety tiers

Perry gives students information they'll make real admission decisions on, so every
fact carries a `data_tier` (see `db/schema.sql` for the enforced column/values):

- `tier_1_official` — exam dates, syllabus, cutoff marks, reservation-category cutoffs.
  Primary source only: an official government notification or official exam/counseling
  portal. Never AI-estimated or sourced from a secondary aggregator (careers360,
  shiksha, collegedekho, etc.) — those sites can inform research but the row only
  moves to `tier_1_official` once backed by the primary document itself.
- `tier_2_reported` — placement rates, college outcome claims. Self-reported and
  unreliable industry-wide; show only as a sourced range with the reporting source
  named, ideally with a second, independent corroborating source. Never a bare
  point figure presented as fact.
- `tier_3_advisory` — AI-assisted guidance (course topics, "why it matters," interest
  discovery). Always labeled as AI-assisted, never presented as settled fact. The
  nightly "Course Grip" routine below writes exclusively at this tier.
- `pending_review` — the default for anything not yet checked against a tier-1
  source, including all seed rows transcribed from secondary aggregators to date.
  Do not present a `pending_review` row to a student as verified.

Rules that apply regardless of tier: no guessing where the record is missing (say
"not yet available" instead of estimating a cutoff or date); stale tier-1 data older
than one admission cycle gets an expiry flag, not silent reuse; every tier-1 fact
keeps a `source` reference a student can follow themselves. See the published
roadmap for the phased plan to bring existing data up to `tier_1_official`.

## Nightly "Course Grip" research routine (12:00 AM – 2:00 AM)

A second nightly cloud routine, separate from the Drive-based import above, runs every
night in the 12:00 AM–2:00 AM window. Its job: build out the `course_topics` table
(schema in `db/schema.sql`, seed in `db/seed/course_topics.json`) — a per-course map of
what a student needs to study to get a genuinely strong grip on that course, and what
it sets them up for afterward.

Each run:
1. Pick 2–3 courses from the `courses` table that have the fewest rows in `course_topics`
   (query: `SELECT c.course_name, count(t.id) FROM courses c LEFT JOIN course_topics t ON t.course_id = c.id GROUP BY c.course_name ORDER BY count(t.id) ASC, c.course_name LIMIT 3`),
   so coverage grows evenly across all 15 courses rather than going deep on one and
   ignoring the rest.
2. For each picked course, research and write one row per core topic into
   `db/seed/course_topics.json` (merge — never overwrite another course's existing
   topics), each with:
   - `course_name` (must match a `courses.course_name` exactly)
   - `topic_name`
   - `sequence_order` (the order to study it in, for a genuine foundation-first build-up)
   - `why_it_matters` (why mastering this specific topic matters for real command of the subject)
   - `builds_toward` (which later courses, specializations, or careers in this database
     this topic sets the student up for — cross-reference the `careers` and `courses` tables)
   - `source`
3. Run `npm run db:import` to merge the updated seed into Postgres (safe to re-run;
   `course_topics` upserts on `(course_id, topic_name)`).
4. If every course already has solid topic coverage, do a pass improving depth/accuracy
   on the thinnest existing course instead of stopping early.

