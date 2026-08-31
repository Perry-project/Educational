# Perry local database

Local Postgres mirror of the nightly "AP Career Database" Google Drive workbook,
split into separate, queryable lists instead of one big spreadsheet.

## Tables (see `schema.sql`)
- `states` — state dimension (currently just Andhra Pradesh; ready for Phase 6 expansion)
- `schools` — Class 1-10 school-stage options (govt/private/residential/open schooling)
- `pathways` — post-10th options (Intermediate streams, POLYCET, ITI, NIOS)
- `entrance_exams` — post-Intermediate entrance exams (AP EAPCET, NEET, CLAT, CA Foundation, NDA, CUET)
- `colleges` — named institutions (empty for now — the nightly job hasn't collected named colleges yet, only "government/private colleges" generically)
- `courses` — degrees/diplomas/trades a pathway or exam leads into
- `careers` — major/niche career pipelines (empty — Phase 4/5 of the nightly job not started yet)
- `progress_tracker` — mirrors the Drive workbook's own phase-completion tracker
- `import_log` — which Drive snapshot (by file ID + date) has been merged in already

## Seed data
`db/seed/*.json` is the current snapshot, transcribed from the 2026-08-29 Drive export.
These files are what `scripts/import-ap-database.mjs` reads and upserts into Postgres.

## Daily update flow
See the "Perry data pipeline" section in the root `CLAUDE.md` — at the start of each
session in this project, check Google Drive for a newer `AP Career Database - YYYY-MM-DD`
file, update the seed JSON with anything new, and re-run the import. Every table upserts
on its natural key (e.g. `school_type` per state), so re-running with new data merges
rather than duplicating or wiping what's already there.

## Setup
1. `createdb perry` (or via `psql`) with a dedicated `perry_app` role — not the Postgres superuser.
2. `psql -U perry_app -d perry -f db/schema.sql`
3. Copy `.env.example` to `.env` and fill in the real password.
4. `npm run db:import -- --file-id <id> --snapshot-date <date> --title "<title>"`
