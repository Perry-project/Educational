-- Perry education database schema
-- Separates schools, pathways, entrance exams, colleges, courses, and careers
-- so each list can be queried/filtered independently (per user request).

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
  updated_at TIMESTAMP DEFAULT now(),
  UNIQUE(state_id, school_type)
);

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
  updated_at TIMESTAMP DEFAULT now(),
  UNIQUE(state_id, pathway_name)
);

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
  updated_at TIMESTAMP DEFAULT now(),
  UNIQUE(state_id, exam_name)
);

-- college list (separate from exams/courses; enriched as Phase 4/5 data arrives)
CREATE TABLE IF NOT EXISTS colleges (
  id SERIAL PRIMARY KEY,
  state_id INT REFERENCES states(id) ON DELETE CASCADE,
  college_name TEXT NOT NULL,
  ownership TEXT,               -- Government / Private
  offers_courses TEXT,
  admission_route TEXT,
  source TEXT,
  updated_at TIMESTAMP DEFAULT now(),
  UNIQUE(state_id, college_name)
);

-- course list (degrees/diplomas/trades a pathway or exam admits into)
CREATE TABLE IF NOT EXISTS courses (
  id SERIAL PRIMARY KEY,
  course_name TEXT NOT NULL UNIQUE,
  category TEXT,                 -- Engineering / Medicine / Commerce / Law / Diploma / Trade / Humanities
  typical_duration TEXT,
  entry_via TEXT,
  source TEXT,
  updated_at TIMESTAMP DEFAULT now()
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
  updated_at TIMESTAMP DEFAULT now(),
  UNIQUE(state_id, career_name)
);

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
