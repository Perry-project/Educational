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

