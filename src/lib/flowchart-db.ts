import { pool } from "./db";
import { nodesFor, STATES, TS_COUNTERPARTS, type StateKey } from "./class10-flow-data";
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
  // Set when the details shown come from another state's row.
  note?: string;
};
export type CareerRow = { id: number; name: string };
export type FlowchartData = {
  state: StateKey;
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

// Notes for details borrowed from Andhra Pradesh rows on the Telangana chart.
// National exams are the same for every state; most careers have no
// Telangana row yet, so their AP details are shown, clearly labelled.
const NATIONAL_EXAM_NOTE = "A national exam, the same for Telangana students. Some notes below mention Andhra Pradesh.";
const AP_CAREER_NOTE =
  "Telangana details for this career haven’t been added yet. The details below are for Andhra Pradesh: state exams, colleges and recruiting bodies may differ.";
// Course rows aren't per state; their "Entry via" names AP's state exams.
const TS_EXAM_NAMES: [RegExp, string][] = [[/\bAP EAPCET\b/g, "TG EAPCET"], [/\bAP POLYCET\b/g, "TS POLYCET"]];

const START_ROWS: Record<StateKey, [string, string][]> = {
  ap: [
    ["Eligibility", "Pass the SSC Public Examination, or a CBSE / ICSE / NIOS equivalent"],
    ["Next", "Choose an Intermediate group, AP POLYCET, an ITI trade, NIOS or a residential school"],
  ],
  ts: [
    ["Eligibility", "Pass the SSC examination of the Board of Secondary Education, Telangana, or a CBSE / ICSE / NIOS equivalent"],
    ["Next", "Choose an Intermediate group, TS POLYCET, an ITI trade or NIOS"],
  ],
};

// Pathways from different states share names ("Intermediate - MPC ..."), so
// rows are always picked by state as well as by name.
export async function getFlowchartData(state: StateKey = "ap"): Promise<FlowchartData> {
  const stateName = STATES[state].name;
  const withState = (table: string, cols: string, order = "") =>
    pool.query(`SELECT ${cols}, s.name AS state FROM ${table} x JOIN states s ON s.id = x.state_id ${order}`);
  const [pathways, exams, courses, careers, colleges, topics] = await Promise.all([
    withState("pathways", "pathway_name, eligibility, admission_route, application_window, duration, leads_to, x.source"),
    withState("entrance_exams", "exam_name, full_form_body, eligibility, application_window, exam_date, admits_into, x.source"),
    pool.query("SELECT id, course_name, category, typical_duration, entry_via, source FROM courses"),
    withState("careers", "x.id, career_name, entry_point, required_exams, eligibility, govt_private_options, next_step, x.source", "ORDER BY x.id"),
    withState("colleges", "college_name, ownership, offers_courses", "ORDER BY ownership, college_name"),
    pool.query("SELECT course_id, topic_name, sequence_order, why_it_matters, builds_toward FROM course_topics ORDER BY course_id, sequence_order"),
  ]);

  const inState = <T extends { state: string }>(rows: T[], name: string) => rows.filter((r) => r.state === name);
  const byName = <T extends Record<string, unknown>>(rows: T[], key: keyof T) =>
    new Map(rows.map((r) => [r[key] as string, r]));
  const pathwayRow = byName(inState(pathways.rows, stateName), "pathway_name");
  const examRow = byName(inState(exams.rows, stateName), "exam_name");
  // National exams (NEET, JEE, CLAT, ...) are stored once, under AP.
  const apExamRow = byName(inState(exams.rows, STATES.ap.name), "exam_name");
  const courseRow = byName(courses.rows, "course_name");
  const stateColleges = inState(colleges.rows, stateName);
  const entryVia = (v: string | null) =>
    state === "ts" && v ? TS_EXAM_NAMES.reduce((t, [re, name]) => t.replace(re, name), v) : v;
  // Topics name the careers they build toward; on the Telangana chart, AP
  // careers with a Telangana counterpart are named as that counterpart.
  const tsCareerNames = Object.entries(TS_COUNTERPARTS).map(([ts, ap]) => [ap, ts.replace(/\s*\((major|niche)\)$/, "")]);
  const buildsToward = (v: string | null) =>
    state === "ts" && v ? tsCareerNames.reduce((t, [ap, ts]) => t.split(ap).join(ts), v) : v;

  const details: Record<string, NodeDetail> = {};
  for (const n of nodesFor(state)) {
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
      const own = examRow.get(n.db);
      const r = own ?? apExamRow.get(n.db);
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
        note: own ? undefined : NATIONAL_EXAM_NOTE,
      };
    } else if (n.col === 4) {
      const r = courseRow.get(n.db);
      if (!r) continue;
      const match = COLLEGE_MATCH[n.id];
      details[n.id] = {
        rows: rowsOf([
          ["Field", r.category],
          ["Duration", r.typical_duration],
          ["Entry via", entryVia(r.entry_via)],
        ]),
        source: forStudents(r.source),
        colleges: match
          ? stateColleges
              .filter((c) => courseItems(c.offers_courses).some((item) => match.test(item)))
              .map((c) => ({ name: c.college_name, ownership: c.ownership }))
          : [],
        topics: topics.rows
          .filter((t) => t.course_id === r.id)
          .map((t) => ({ name: t.topic_name, why: t.why_it_matters, buildsToward: buildsToward(t.builds_toward) })),
      };
    }
  }

  // Telangana chart: Telangana's own careers, plus AP careers that have no
  // Telangana counterpart yet.
  const replaced = new Set(Object.values(TS_COUNTERPARTS));
  const shown = state === "ap"
    ? inState(careers.rows, STATES.ap.name)
    : careers.rows.filter((r) => r.state === stateName || (r.state === STATES.ap.name && !replaced.has(r.career_name)));

  for (const r of shown) {
    details[`career_${r.id}`] = {
      note: r.state === stateName ? undefined : AP_CAREER_NOTE,
      rows: rowsOf([
        // The research routine appends the category to some names.
        ["Full name", r.career_name.replace(/\s*\((major|niche)\)$/, "")],
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
  details.start = { rows: START_ROWS[state], source: null };

  return { state, details, careers: shown.map((r) => ({ id: r.id, name: r.career_name })) };
}
