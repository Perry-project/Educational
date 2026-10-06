-- Perry education database schema
-- Separates schools, pathways, entrance exams, colleges, courses, and careers
-- so each list can be queried/filtered independently (per user request).
--
-- Data-trust tiers (see CLAUDE.md "Data safety tiers"): every row that carries
-- a data_tier column must be one of:
--   tier_1_official   - primary government/official-portal source, ready to
--                        show a student as fact (exam dates, cutoffs, syllabus)
--   tier_2_reported   - self-reported figures (placement rates) shown only as
--                        a sourced range with corroborating sources
--   tier_3_advisory   - AI-assisted guidance, always labeled as such
--   pending_review     - not yet checked against a tier-1 source; the default
--                        for anything transcribed from a secondary aggregator
-- No UI may present a pending_review or tier_2_reported row as settled fact.

CREATE TABLE IF NOT EXISTS states (
  id SERIAL PRIMARY KEY,
  name TEXT UNIQUE NOT NULL
);

-- Phase 1: school stage options (Class 1-10 boards/routes)
CREATE TABLE IF NOT EXISTS schools (
  id SERIAL PRIMARY KEY,
  state_id INT REFERENCES states(id) ON DELETE CASCADE,
  school_type TEXT NOT NULL,
  board_authority TEXT,
  ownership TEXT,              -- Government / Private / Government-aided
  classes_covered TEXT,
  medium_of_instruction TEXT,
  key_exam TEXT,
  exam_window TEXT,
  passing_criteria TEXT,
  next_step TEXT,
  approx_fee TEXT,
  source TEXT,
  source_type TEXT,
  data_tier TEXT NOT NULL DEFAULT 'pending_review'
    CHECK (data_tier IN ('tier_1_official','tier_2_reported','tier_3_advisory','pending_review')),
  verified_date DATE,
  updated_at TIMESTAMP DEFAULT now(),
  UNIQUE(state_id, school_type)
);

ALTER TABLE schools ADD COLUMN IF NOT EXISTS source_type TEXT;
ALTER TABLE schools ADD COLUMN IF NOT EXISTS data_tier TEXT NOT NULL DEFAULT 'pending_review';
ALTER TABLE schools ADD COLUMN IF NOT EXISTS verified_date DATE;
ALTER TABLE schools DROP CONSTRAINT IF EXISTS schools_data_tier_check;
ALTER TABLE schools ADD CONSTRAINT schools_data_tier_check
  CHECK (data_tier IN ('tier_1_official','tier_2_reported','tier_3_advisory','pending_review'));

-- Phase 2: post-10th pathways (Intermediate streams, POLYCET, ITI, NIOS, etc.)
CREATE TABLE IF NOT EXISTS pathways (
  id SERIAL PRIMARY KEY,
  state_id INT REFERENCES states(id) ON DELETE CASCADE,
  pathway_name TEXT NOT NULL,
  eligibility TEXT,
  admission_route TEXT,
  application_window TEXT,
  duration TEXT,
  leads_to TEXT,
  source TEXT,
  source_type TEXT,
  data_tier TEXT NOT NULL DEFAULT 'pending_review'
    CHECK (data_tier IN ('tier_1_official','tier_2_reported','tier_3_advisory','pending_review')),
  verified_date DATE,
  updated_at TIMESTAMP DEFAULT now(),
  UNIQUE(state_id, pathway_name)
);

ALTER TABLE pathways ADD COLUMN IF NOT EXISTS source_type TEXT;
ALTER TABLE pathways ADD COLUMN IF NOT EXISTS data_tier TEXT NOT NULL DEFAULT 'pending_review';
ALTER TABLE pathways ADD COLUMN IF NOT EXISTS verified_date DATE;
ALTER TABLE pathways DROP CONSTRAINT IF EXISTS pathways_data_tier_check;
ALTER TABLE pathways ADD CONSTRAINT pathways_data_tier_check
  CHECK (data_tier IN ('tier_1_official','tier_2_reported','tier_3_advisory','pending_review'));

-- Phase 3: entrance exams list
CREATE TABLE IF NOT EXISTS entrance_exams (
  id SERIAL PRIMARY KEY,
  state_id INT REFERENCES states(id) ON DELETE CASCADE,
  exam_name TEXT NOT NULL,
  full_form_body TEXT,
  eligibility TEXT,
  application_window TEXT,
  exam_date TEXT,
  admits_into TEXT,
  source TEXT,
  source_type TEXT,             -- government_notification / official_portal / secondary_aggregator / unverified
  data_tier TEXT NOT NULL DEFAULT 'pending_review'
    CHECK (data_tier IN ('tier_1_official','tier_2_reported','tier_3_advisory','pending_review')),
  verified_date DATE,
  updated_at TIMESTAMP DEFAULT now(),
  UNIQUE(state_id, exam_name)
);
ALTER TABLE entrance_exams ADD COLUMN IF NOT EXISTS source_type TEXT;
ALTER TABLE entrance_exams ADD COLUMN IF NOT EXISTS data_tier TEXT NOT NULL DEFAULT 'pending_review';
ALTER TABLE entrance_exams ADD COLUMN IF NOT EXISTS verified_date DATE;
ALTER TABLE entrance_exams DROP CONSTRAINT IF EXISTS entrance_exams_data_tier_check;
ALTER TABLE entrance_exams ADD CONSTRAINT entrance_exams_data_tier_check
  CHECK (data_tier IN ('tier_1_official','tier_2_reported','tier_3_advisory','pending_review'));

-- college list (separate from exams/courses; enriched as Phase 4/5 data arrives)
CREATE TABLE IF NOT EXISTS colleges (
  id SERIAL PRIMARY KEY,
  state_id INT REFERENCES states(id) ON DELETE CASCADE,
  college_name TEXT NOT NULL,
  ownership TEXT,               -- Government / Private
  offers_courses TEXT,
  admission_route TEXT,
  source TEXT,
  source_type TEXT,
  data_tier TEXT NOT NULL DEFAULT 'pending_review'
    CHECK (data_tier IN ('tier_1_official','tier_2_reported','tier_3_advisory','pending_review')),
  verified_date DATE,
  updated_at TIMESTAMP DEFAULT now(),
  UNIQUE(state_id, college_name)
);
ALTER TABLE colleges ADD COLUMN IF NOT EXISTS source_type TEXT;
ALTER TABLE colleges ADD COLUMN IF NOT EXISTS data_tier TEXT NOT NULL DEFAULT 'pending_review';
ALTER TABLE colleges ADD COLUMN IF NOT EXISTS verified_date DATE;
ALTER TABLE colleges DROP CONSTRAINT IF EXISTS colleges_data_tier_check;
ALTER TABLE colleges ADD CONSTRAINT colleges_data_tier_check
  CHECK (data_tier IN ('tier_1_official','tier_2_reported','tier_3_advisory','pending_review'));

-- course list (degrees/diplomas/trades a pathway or exam admits into)
CREATE TABLE IF NOT EXISTS courses (
  id SERIAL PRIMARY KEY,
  course_name TEXT NOT NULL UNIQUE,
  category TEXT,                 -- Engineering / Medicine / Commerce / Law / Diploma / Trade / Humanities
  typical_duration TEXT,
  entry_via TEXT,
  source TEXT,
  source_type TEXT,
  data_tier TEXT NOT NULL DEFAULT 'pending_review'
    CHECK (data_tier IN ('tier_1_official','tier_2_reported','tier_3_advisory','pending_review')),
  verified_date DATE,
  updated_at TIMESTAMP DEFAULT now()
);
ALTER TABLE courses ADD COLUMN IF NOT EXISTS source_type TEXT;
ALTER TABLE courses ADD COLUMN IF NOT EXISTS data_tier TEXT NOT NULL DEFAULT 'pending_review';
ALTER TABLE courses ADD COLUMN IF NOT EXISTS verified_date DATE;
ALTER TABLE courses DROP CONSTRAINT IF EXISTS courses_data_tier_check;
ALTER TABLE courses ADD CONSTRAINT courses_data_tier_check
  CHECK (data_tier IN ('tier_1_official','tier_2_reported','tier_3_advisory','pending_review'));

-- Per-course syllabus/topic map, populated by the nightly 12am-2am "Course Grip"
-- research routine: what a student needs to master for a strong foundation in
-- each course, and what later courses/careers that foundation feeds into.
CREATE TABLE IF NOT EXISTS course_topics (
  id SERIAL PRIMARY KEY,
  course_id INT REFERENCES courses(id) ON DELETE CASCADE,
  topic_name TEXT NOT NULL,
  sequence_order INT,             -- suggested study order within the course
  why_it_matters TEXT,            -- why mastering this topic builds a strong grip
  builds_toward TEXT,             -- future courses/careers/specializations this feeds into
  source TEXT,
  updated_at TIMESTAMP DEFAULT now(),
  UNIQUE(course_id, topic_name)
);

-- Phase 2 (roadmap): category-wise admission cutoffs, keyed college x course x
-- reservation category x year. Empty until sourced from official DOST/EAPCET
-- counseling records (db/seed/cutoffs.json) - see CLAUDE.md data-safety tiers.
-- Every row must be tier_1_official; there is no lower-tier use for a cutoff mark.
CREATE TABLE IF NOT EXISTS cutoffs (
  id SERIAL PRIMARY KEY,
  college_id INT REFERENCES colleges(id) ON DELETE CASCADE,
  course_id INT REFERENCES courses(id) ON DELETE CASCADE,
  category TEXT NOT NULL,        -- OC / BC-A / BC-B / BC-C / BC-D / BC-E / SC / ST / EWS
  year INT NOT NULL,
  closing_rank INT,
  closing_marks NUMERIC,
  source TEXT NOT NULL,          -- link to the official counseling/GO document
  source_type TEXT NOT NULL DEFAULT 'government_notification'
    CHECK (source_type IN ('government_notification','official_portal')),
  data_tier TEXT NOT NULL DEFAULT 'tier_1_official'
    CHECK (data_tier = 'tier_1_official'),
  verified_date DATE NOT NULL,
  updated_at TIMESTAMP DEFAULT now(),
  UNIQUE(college_id, course_id, category, year)
);

-- Phase 4/5: career pipelines (not yet populated by the nightly job, table ready)
CREATE TABLE IF NOT EXISTS careers (
  id SERIAL PRIMARY KEY,
  state_id INT REFERENCES states(id) ON DELETE CASCADE,
  career_name TEXT NOT NULL,
  category TEXT,                 -- major / niche
  entry_point TEXT,
  required_exams TEXT,
  eligibility TEXT,
  govt_private_options TEXT,
  next_step TEXT,
  source TEXT,
  source_type TEXT,
  data_tier TEXT NOT NULL DEFAULT 'pending_review'
    CHECK (data_tier IN ('tier_1_official','tier_2_reported','tier_3_advisory','pending_review')),
  verified_date DATE,
  updated_at TIMESTAMP DEFAULT now(),
  UNIQUE(state_id, career_name)
);

ALTER TABLE careers ADD COLUMN IF NOT EXISTS source_type TEXT;
ALTER TABLE careers ADD COLUMN IF NOT EXISTS data_tier TEXT NOT NULL DEFAULT 'pending_review';
ALTER TABLE careers ADD COLUMN IF NOT EXISTS verified_date DATE;
ALTER TABLE careers DROP CONSTRAINT IF EXISTS careers_data_tier_check;
ALTER TABLE careers ADD CONSTRAINT careers_data_tier_check
  CHECK (data_tier IN ('tier_1_official','tier_2_reported','tier_3_advisory','pending_review'));

-- Mirrors the "Progress Tracker" tab from the nightly Drive workbook
CREATE TABLE IF NOT EXISTS progress_tracker (
  id SERIAL PRIMARY KEY,
  phase INT NOT NULL UNIQUE,
  topic TEXT,
  scope TEXT,
  status TEXT,
  last_updated DATE,
  notes TEXT
);

-- Tracks which nightly Google Drive snapshot has already been merged in,
-- so re-running the import on a later day only adds what's new.
CREATE TABLE IF NOT EXISTS import_log (
  id SERIAL PRIMARY KEY,
  source_file_id TEXT UNIQUE NOT NULL,
  source_title TEXT,
  snapshot_date DATE,
  imported_at TIMESTAMP DEFAULT now(),
  rows_imported INT
);

-- Exams tab (/exams): every exam a student in AP or Telangana may sit, from
-- Class 1-10 scholarship and admission tests to entrance exams and government
-- job exams. The entrance_exams table holds them all; these columns sort them.
ALTER TABLE entrance_exams ADD COLUMN IF NOT EXISTS scope TEXT;            -- National / Andhra Pradesh / Telangana
ALTER TABLE entrance_exams ADD COLUMN IF NOT EXISTS stage TEXT;            -- school / after_10 / after_12 / after_degree / jobs
ALTER TABLE entrance_exams ADD COLUMN IF NOT EXISTS category TEXT;         -- Engineering, Medical, Scholarship, Defence, Teaching jobs ...
ALTER TABLE entrance_exams ADD COLUMN IF NOT EXISTS body_type TEXT;        -- Government / Private
ALTER TABLE entrance_exams ADD COLUMN IF NOT EXISTS conducting_body TEXT;
ALTER TABLE entrance_exams ADD COLUMN IF NOT EXISTS official_website TEXT;
ALTER TABLE entrance_exams ADD COLUMN IF NOT EXISTS exam_pattern TEXT;     -- questions, marks, duration, negative marking

-- Subjects an exam tests, with the topics its official syllabus lists.
CREATE TABLE IF NOT EXISTS exam_subjects (
  id SERIAL PRIMARY KEY,
  exam_id INT REFERENCES entrance_exams(id) ON DELETE CASCADE,
  subject TEXT NOT NULL,
  topics TEXT,
  sequence_order INT,
  source TEXT,
  source_type TEXT,
  data_tier TEXT NOT NULL DEFAULT 'pending_review'
    CHECK (data_tier IN ('tier_1_official','tier_2_reported','tier_3_advisory','pending_review')),
  verified_date DATE,
  updated_at TIMESTAMP DEFAULT now(),
  UNIQUE(exam_id, subject)
);

-- Category-wise qualifying marks / cutoffs for an exam (not a college's
-- closing rank: that is the cutoffs table). Tier-1 only, like cutoffs: a
-- row needs the official document it came from.
CREATE TABLE IF NOT EXISTS exam_cutoffs (
  id SERIAL PRIMARY KEY,
  exam_id INT REFERENCES entrance_exams(id) ON DELETE CASCADE,
  year INT NOT NULL,
  category TEXT NOT NULL,         -- General / EWS / OBC-NCL / BC / SC / ST / PwD ...
  kind TEXT NOT NULL,             -- qualifying_marks / qualifying_percentile / cutoff_score / eligibility_marks / seat_reservation
  value TEXT NOT NULL,            -- e.g. "50 of 200 (25%)", "93.10 percentile", "No minimum"
  note TEXT,
  source TEXT NOT NULL,
  source_type TEXT NOT NULL DEFAULT 'government_notification'
    CHECK (source_type IN ('government_notification','official_portal')),
  data_tier TEXT NOT NULL DEFAULT 'tier_1_official'
    CHECK (data_tier = 'tier_1_official'),
  verified_date DATE NOT NULL,
  updated_at TIMESTAMP DEFAULT now(),
  UNIQUE(exam_id, year, category, kind)
);

-- Second Chance tab (/second-chance): official routes back into education or
-- work for a student who stopped somewhere — failed or left Class 10,
-- Intermediate or a degree, didn't clear an entrance exam, or is already
-- working. Same rule as the exams: a route's details reach a student only
-- once checked against its official notification (tier_1_official); until
-- then only its name, body and official website are shown.
CREATE TABLE IF NOT EXISTS second_chance_routes (
  id SERIAL PRIMARY KEY,
  stopped_at TEXT NOT NULL,       -- class_10 / intermediate / degree / entrance_exam / working
  route_name TEXT NOT NULL,
  scope TEXT NOT NULL,            -- National / Andhra Pradesh / Telangana
  kind TEXT,                      -- Retake exam / Open school / Skill training / Diploma / Degree / Rule
  conducting_body TEXT,
  official_website TEXT,
  summary TEXT,                   -- what the route is, in a line
  who_can TEXT,                   -- eligibility
  how_to_apply TEXT,
  next_dates TEXT,
  leads_to TEXT,
  related_exam TEXT,              -- entrance_exams.exam_name to link to on /exams, when the route is an exam
  sequence_order INT,
  source TEXT,
  source_type TEXT,
  data_tier TEXT NOT NULL DEFAULT 'pending_review'
    CHECK (data_tier IN ('tier_1_official','tier_2_reported','tier_3_advisory','pending_review')),
  verified_date DATE,
  updated_at TIMESTAMP DEFAULT now(),
  UNIQUE(stopped_at, route_name, scope)
);
