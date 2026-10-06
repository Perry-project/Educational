# Perry

Career guidance for students in Andhra Pradesh and Telangana: every route from Class 10 to a career, the exams on the
way, and official ways back for students who stopped studying.

Built with Next.js and PostgreSQL.

## Run locally

1. Copy `.env.example` to `.env` and set `DATABASE_URL` to a PostgreSQL database.
2. Create the tables and load the data:
   ```bash
   psql "$DATABASE_URL" -f db/schema.sql
   npm install
   npm run db:import
   ```
3. Start the site with `npm run dev` and open http://localhost:3000.

## Pages

- `/flowchart`: Class 10 to career, one line per career
- `/exams`: exams from school level to government jobs
- `/second-chance`: official routes back into education or work
- `/pathfinder`: pick a career, or answer three questions for ideas

## Data

`db/seed/*.json` is the source data. Exam dates, syllabus and cutoffs are added only from official notices; see
`CLAUDE.md` for the data rules and the nightly research pipeline.
