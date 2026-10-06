import { pool } from "./db";
import { forStudents } from "./student-text";

// Everything the /exams page shows, read from Postgres: every exam in the
// entrance_exams table, with the subjects it tests (exam_subjects) and its
// category-wise qualifying marks (exam_cutoffs).
//
// Only verified rows (tier_1_official) carry their details to the page: an
// exam still pending_review is listed by name, body and official website,
// with its dates, syllabus and marks left out until they're checked.

export type ExamSubject = { subject: string; topics: string | null };
export type ExamCutoff = { year: number; category: string; kind: string; value: string; note: string | null };
export type Exam = {
  id: number;
  name: string;
  fullForm: string | null;
  scope: string; // National / Andhra Pradesh / Telangana
  stage: string; // school / after_10 / after_12 / after_degree / jobs
  category: string;
  bodyType: string | null; // Government / Private
  body: string | null;
  website: string | null;
  verified: boolean;
  verifiedOn: string | null;
  rows: [string, string][];
  pattern: string | null;
  subjects: ExamSubject[];
  cutoffs: ExamCutoff[];
  source: string | null;
};

const clean = (v: string | null) => {
  const t = forStudents(v);
  return t && t.trim() ? t : null;
};

export async function getExams(): Promise<Exam[]> {
  const [exams, subjects, cutoffs] = await Promise.all([
    pool.query(
      `SELECT x.id, exam_name, full_form_body, eligibility, application_window, exam_date, admits_into,
              source, data_tier, verified_date::text, scope, stage, category, body_type, conducting_body,
              official_website, exam_pattern, s.name AS state
       FROM entrance_exams x JOIN states s ON s.id = x.state_id
       ORDER BY exam_name`,
    ),
    pool.query(
      `SELECT exam_id, subject, topics FROM exam_subjects
       WHERE data_tier = 'tier_1_official' ORDER BY exam_id, sequence_order NULLS LAST, subject`,
    ),
    pool.query(`SELECT exam_id, year, category, kind, value, note FROM exam_cutoffs ORDER BY exam_id, year DESC, id`),
  ]);

  const subjectsOf = new Map<number, ExamSubject[]>();
  for (const r of subjects.rows) {
    const list = subjectsOf.get(r.exam_id) ?? [];
    list.push({ subject: r.subject, topics: clean(r.topics) });
    subjectsOf.set(r.exam_id, list);
  }
  const cutoffsOf = new Map<number, ExamCutoff[]>();
  for (const r of cutoffs.rows) {
    const list = cutoffsOf.get(r.exam_id) ?? [];
    list.push({ year: r.year, category: r.category, kind: r.kind, value: r.value, note: r.note });
    cutoffsOf.set(r.exam_id, list);
  }

  return exams.rows.map((r) => {
    const verified = r.data_tier === "tier_1_official";
    const rows = verified
      ? ([
          ["Who can take it", clean(r.eligibility)],
          ["Applications", clean(r.application_window)],
          ["Exam dates", clean(r.exam_date)],
          ["Leads to", clean(r.admits_into)],
        ].filter((p): p is [string, string] => !!p[1]))
      : [];
    return {
      id: r.id,
      name: r.exam_name,
      fullForm: clean(r.full_form_body),
      scope: r.scope ?? r.state,
      stage: r.stage ?? "after_12",
      category: r.category ?? "Other",
      bodyType: r.body_type,
      body: r.conducting_body,
      website: r.official_website,
      verified,
      verifiedOn: verified ? r.verified_date : null,
      rows,
      pattern: verified ? clean(r.exam_pattern) : null,
      subjects: verified ? subjectsOf.get(r.id) ?? [] : [],
      cutoffs: verified ? cutoffsOf.get(r.id) ?? [] : [],
      source: verified ? clean(r.source) : null,
    };
  });
}
