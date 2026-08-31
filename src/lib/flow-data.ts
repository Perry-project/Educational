import { pool } from "./db";

export type FlowNodeType = "root" | "pathway" | "exam" | "course";

export type FlowFact = { label: string; value: string };

export type Stream = "Science" | "Commerce" | "Humanities" | "Vocational";

export type FlowNode = {
  id: string;
  type: FlowNodeType;
  label: string;
  sub: string;
  facts: FlowFact[];
  stream?: Stream;
};

export type FlowEdge = {
  id: string;
  source: string;
  target: string;
  secondary?: boolean;
};

export type FlowGraph = {
  nodes: FlowNode[];
  edges: FlowEdge[];
};

type PathwayRow = {
  pathway_name: string;
  eligibility: string | null;
  admission_route: string | null;
  duration: string | null;
  leads_to: string | null;
};

type ExamRow = {
  exam_name: string;
  full_form_body: string | null;
  eligibility: string | null;
  exam_date: string | null;
  admits_into: string | null;
};

type CourseRow = {
  course_name: string;
  category: string | null;
  typical_duration: string | null;
  entry_via: string | null;
};

// Maps a graph node id to the exact `pathway_name` / `exam_name` / `course_name`
// stored in Postgres, so labels and detail facts come from the live database
// rather than being hardcoded — only the topology (which id connects to which)
// and the layout are static, since the schema has no explicit foreign keys
// between these free-text tables.
const PATHWAY_IDS: Record<string, string> = {
  mpc: "Intermediate - MPC (Maths, Physics, Chemistry)",
  bipc: "Intermediate - BiPC (Biology, Physics, Chemistry)",
  mec: "Intermediate - MEC (Maths, Economics, Commerce)",
  cec: "Intermediate - CEC (Commerce, Economics, Civics)",
  hec: "Intermediate - HEC (History, Economics, Civics)",
  polycet: "AP POLYCET - Polytechnic Diploma",
  "iti-eng": "ITI - Engineering Trades",
  "iti-noneng": "ITI - Non-Engineering Trades",
};

// Coarse stream grouping for the Pathway column's filter chips. This is a UI
// classification, not a database column — the pathway table has no notion of
// "stream," so it lives here alongside the rest of the static topology.
const PATHWAY_STREAM: Record<string, Stream> = {
  mpc: "Science",
  bipc: "Science",
  mec: "Commerce",
  cec: "Commerce",
  hec: "Humanities",
  polycet: "Vocational",
  "iti-eng": "Vocational",
  "iti-noneng": "Vocational",
};

const EXAM_IDS: Record<string, string> = {
  eapcet: "AP EAPCET",
  neet: "NEET-UG",
  "ca-foundation": "CA Foundation",
  clat: "CLAT (UG)",
  nda: "NDA (National Defence Academy exam)",
  cuet: "CUET-UG",
};

const COURSE_IDS: Record<string, string> = {
  btech: "B.Tech / Engineering",
  "poly-diploma": "Polytechnic Diploma",
  mbbs: "MBBS",
  bds: "BDS",
  ayush: "AYUSH (BAMS/BHMS/BUMS/BSMS)",
  "bsc-nursing": "B.Sc Nursing",
  bpharm: "B.Pharm (Pharmacy)",
  bvsc: "Agriculture & Veterinary Sciences (BVSc & AH)",
  "bcom-bba": "B.Com / BBA",
  ca: "Chartered Accountancy (CA)",
  law: "Law (BA/BBA/B.Com LLB)",
  "ba-hum": "BA Humanities",
  "iti-cert-eng": "ITI Trade Certificate (Engineering trades)",
  "iti-cert-noneng": "ITI Trade Certificate (Non-Engineering trades)",
  "nda-training": "NDA / Naval Academy Officer Training",
};

// Primary route (solid) unless marked secondary (dashed — an alternate or
// lateral-entry path called out in the source pathway/exam's own text).
const EDGES: Omit<FlowEdge, "id">[] = [
  ...Object.keys(PATHWAY_IDS).map((id) => ({ source: "root", target: id })),
  { source: "mpc", target: "eapcet" },
  { source: "mpc", target: "nda" },
  { source: "mpc", target: "cuet", secondary: true },
  { source: "bipc", target: "neet" },
  { source: "bipc", target: "eapcet" },
  { source: "bipc", target: "cuet", secondary: true },
  { source: "mec", target: "ca-foundation" },
  { source: "mec", target: "bcom-bba" },
  { source: "mec", target: "cuet", secondary: true },
  { source: "cec", target: "clat" },
  { source: "cec", target: "bcom-bba" },
  { source: "cec", target: "cuet", secondary: true },
  { source: "hec", target: "ba-hum" },
  { source: "hec", target: "clat" },
  { source: "hec", target: "cuet", secondary: true },
  { source: "polycet", target: "poly-diploma" },
  { source: "polycet", target: "btech", secondary: true },
  { source: "iti-eng", target: "iti-cert-eng" },
  { source: "iti-eng", target: "poly-diploma", secondary: true },
  { source: "iti-noneng", target: "iti-cert-noneng" },
  { source: "eapcet", target: "btech" },
  { source: "eapcet", target: "bpharm" },
  { source: "eapcet", target: "bvsc" },
  { source: "neet", target: "mbbs" },
  { source: "neet", target: "bds" },
  { source: "neet", target: "ayush" },
  { source: "neet", target: "bsc-nursing" },
  { source: "ca-foundation", target: "ca" },
  { source: "clat", target: "law" },
  { source: "nda", target: "nda-training" },
];

export async function getFlowGraph(): Promise<FlowGraph> {
  const [{ rows: pathways }, { rows: exams }, { rows: courses }] = await Promise.all([
    pool.query<PathwayRow>(
      "SELECT pathway_name, eligibility, admission_route, duration, leads_to FROM pathways"
    ),
    pool.query<ExamRow>(
      "SELECT exam_name, full_form_body, eligibility, exam_date, admits_into FROM entrance_exams"
    ),
    pool.query<CourseRow>(
      "SELECT course_name, category, typical_duration, entry_via FROM courses"
    ),
  ]);

  const pathwayByName = new Map<string, PathwayRow>(pathways.map((r) => [r.pathway_name, r]));
  const examByName = new Map<string, ExamRow>(exams.map((r) => [r.exam_name, r]));
  const courseByName = new Map<string, CourseRow>(courses.map((r) => [r.course_name, r]));

  const nodes: FlowNode[] = [];

  nodes.push({
    id: "root",
    type: "root",
    label: "Class 10 Pass",
    sub: "Any recognised board",
    facts: [
      { label: "Eligibility", value: "Pass Class 10 from any recognised board — SSC, CBSE, ICSE, NIOS, or a residential-school board." },
      { label: "Next", value: "Choose Intermediate, AP POLYCET, or an ITI trade." },
    ],
  });

  for (const [id, name] of Object.entries(PATHWAY_IDS)) {
    const row = pathwayByName.get(name);
    nodes.push({
      id,
      type: "pathway",
      label: name.replace(/^Intermediate - /, "Intermediate — ").replace(/^AP POLYCET.*/, "AP POLYCET").replace(/^ITI - /, "ITI — "),
      sub: row?.duration ?? "",
      stream: PATHWAY_STREAM[id],
      facts: row
        ? [
            { label: "Eligibility", value: row.eligibility ?? "—" },
            { label: "Admission", value: row.admission_route ?? "—" },
            { label: "Leads to", value: row.leads_to ?? "—" },
          ]
        : [],
    });
  }

  for (const [id, name] of Object.entries(EXAM_IDS)) {
    const row = examByName.get(name);
    nodes.push({
      id,
      type: "exam",
      label: name,
      sub: row?.exam_date ?? "",
      facts: row
        ? [
            { label: "Body", value: row.full_form_body ?? "—" },
            { label: "Eligibility", value: row.eligibility ?? "—" },
            { label: "Admits into", value: row.admits_into ?? "—" },
          ]
        : [],
    });
  }

  for (const [id, name] of Object.entries(COURSE_IDS)) {
    const row = courseByName.get(name);
    nodes.push({
      id,
      type: "course",
      label: name,
      sub: row?.typical_duration ?? "",
      facts: row
        ? [
            { label: "Category", value: row.category ?? "—" },
            { label: "Duration", value: row.typical_duration ?? "—" },
            { label: "Entry via", value: row.entry_via ?? "—" },
          ]
        : [],
    });
  }

  const edges: FlowEdge[] = EDGES.map((e) => ({ ...e, id: `${e.source}__${e.target}` }));

  return { nodes, edges };
}
