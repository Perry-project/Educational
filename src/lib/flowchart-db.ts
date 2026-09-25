import { pool } from "./db";
import { NODES } from "./class10-flow-data";
import { forStudents } from "./student-text";

// Everything the /flowchart details panel shows, read from Postgres so the
// chart grows with each nightly import.

export type Topic = { name: string; why: string | null; buildsToward: string | null };
export type CollegeRef = { name: string; ownership: string | null };
export type NodeDetail = {
  rows: [string, string][];
  source: string | null;
  colleges?: CollegeRef[];
  topics?: Topic[];
};
export type CareerRow = { id: number; name: string };
export type FlowchartData = {
  details: Record<string, NodeDetail>;
  careers: CareerRow[];
};

// Keeps only rows that have a value, in student-facing wording.
const rowsOf = (pairs: [string, string | null][]): [string, string][] =>
  pairs
    .map(([k, v]): [string, string | null] => [k, forStudents(v)])
    .filter((p): p is [string, string] => !!p[1] && p[1].trim() !== "");

// Which colleges offer a course. colleges.offers_courses is a free-text,
// comma-separated list ("B.Com / BBA, B.Sc (Basic Sciences)", "MBBS (women)",
// "Law (BA LLB Hons, 5-year integrated)"), so it is split into items (commas
// inside brackets don't split) and each item is matched on how it starts.
// Matching anywhere in the text would, for example, count
// "Law (BA/BBA/B.Com LLB)" as a B.Com course.
const COLLEGE_MATCH: Record<string, RegExp> = {
  btech: /^B\.Tech/i,
  diploma: /^Polytechnic/i,
  mbbs: /^MBBS/i,
  bds: /^BDS\b/i,
  ayush: /^(AYUSH|BAMS|BHMS)/i,
  nursing: /^B\.Sc Nursing/i,
  bpharm: /^B\.Pharm/i,
  agri: /^(Agricultur|Veterinar)/i,
  bcom: /^(B\.Com|BBA)/i,
  llb: /^Law\b/i,
  ba: /^BA Humanities/i,
  bsc: /^B\.Sc \(Basic/i,
  barch: /^B\.Arch/i,
};
const courseItems = (offers: string | null) =>
  (offers ?? "").split(/,(?![^(]*\))/).map((item) => item.trim());

export async function getFlowchartData(): Promise<FlowchartData> {
  const [pathways, exams, courses, careers, colleges, topics] = await Promise.all([
    pool.query("SELECT pathway_name, eligibility, admission_route, application_window, duration, leads_to, source FROM pathways"),
    pool.query("SELECT exam_name, full_form_body, eligibility, application_window, exam_date, admits_into, source FROM entrance_exams"),
    pool.query("SELECT id, course_name, category, typical_duration, entry_via, source FROM courses"),
    pool.query("SELECT id, career_name, entry_point, required_exams, eligibility, govt_private_options, next_step, source FROM careers ORDER BY id"),
    pool.query("SELECT college_name, ownership, offers_courses FROM colleges ORDER BY ownership, college_name"),
    pool.query("SELECT course_id, topic_name, sequence_order, why_it_matters, builds_toward FROM course_topics ORDER BY course_id, sequence_order"),
  ]);

  const byName = <T extends Record<string, unknown>>(rows: T[], key: keyof T) =>
    new Map(rows.map((r) => [r[key] as string, r]));
  const pathwayRow = byName(pathways.rows, "pathway_name");
  const examRow = byName(exams.rows, "exam_name");
  const courseRow = byName(courses.rows, "course_name");

  const details: Record<string, NodeDetail> = {};
  for (const n of NODES) {
    if (!n.db) continue;
    if (n.col === 2) {
      const r = pathwayRow.get(n.db);
      if (!r) continue;
      details[n.id] = {
        rows: rowsOf([
          ["Eligibility", r.eligibility],
          ["Duration", r.duration],
          ["How to apply", r.admission_route],
          ["Applications", r.application_window],
          ["Leads to", r.leads_to],
        ]),
        source: forStudents(r.source),
      };
    } else if (n.col === 3) {
      const r = examRow.get(n.db);
      if (!r) continue;
      details[n.id] = {
        rows: rowsOf([
          ["About", r.full_form_body],
          ["Eligibility", r.eligibility],
          ["Applications", r.application_window],
          ["Exam dates", r.exam_date],
          ["Admits into", r.admits_into],
        ]),
        source: forStudents(r.source),
      };
    } else if (n.col === 4) {
      const r = courseRow.get(n.db);
      if (!r) continue;
      const match = COLLEGE_MATCH[n.id];
      details[n.id] = {
        rows: rowsOf([
          ["Field", r.category],
          ["Duration", r.typical_duration],
          ["Entry via", r.entry_via],
        ]),
        source: forStudents(r.source),
        colleges: match
          ? colleges.rows
              .filter((c) => courseItems(c.offers_courses).some((item) => match.test(item)))
              .map((c) => ({ name: c.college_name, ownership: c.ownership }))
          : [],
        topics: topics.rows
          .filter((t) => t.course_id === r.id)
          .map((t) => ({ name: t.topic_name, why: t.why_it_matters, buildsToward: t.builds_toward })),
      };
    }
  }

  for (const r of careers.rows) {
    details[`career_${r.id}`] = {
      rows: rowsOf([
        ["Full name", r.career_name],
        ["When to start", r.entry_point],
        ["Exams", r.required_exams],
        ["Eligibility", r.eligibility],
        ["Govt / Private", r.govt_private_options],
        ["Next step", r.next_step],
      ]),
      source: forStudents(r.source),
    };
  }

  // The start card has no table behind it.
  details.start = {
    rows: [
      ["Eligibility", "Pass the SSC Public Examination, or a CBSE / ICSE / NIOS equivalent"],
      ["Next", "Choose an Intermediate group, AP POLYCET, an ITI trade, NIOS or a residential school"],
    ],
    source: null,
  };

  return { details, careers: careers.rows.map((r) => ({ id: r.id, name: r.career_name })) };
}
