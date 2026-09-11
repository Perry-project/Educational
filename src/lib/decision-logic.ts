import type { FlowGraph, FlowNode } from "./flow-data";

// One step of the "known interest" flow: given a chosen career node, walk the
// flow graph's edges backward to find the course(s) that lead into it, and
// each course's own exam(s) and pathway(s). Pure graph traversal — no query —
// since getFlowGraph() already carries this topology. Client-safe (no `pg`
// import anywhere in this file) so pathfinder.tsx can call it directly.
export type CareerPath = {
  career: FlowNode;
  course: FlowNode;
  exams: FlowNode[];
  pathways: FlowNode[];
};

export function pathsToCareer(graph: FlowGraph, careerId: string): CareerPath[] {
  const byId = new Map(graph.nodes.map((n) => [n.id, n]));
  const career = byId.get(careerId);
  if (!career) return [];

  const courseIds = graph.edges.filter((e) => e.target === careerId).map((e) => e.source);

  return courseIds
    .map((courseId) => byId.get(courseId))
    .filter((n): n is FlowNode => !!n && n.type === "course")
    .map((course) => {
      const examIds = graph.edges.filter((e) => e.target === course.id).map((e) => e.source);
      const exams = examIds.map((id) => byId.get(id)).filter((n): n is FlowNode => !!n && n.type === "exam");

      const pathwayIds = exams.flatMap((exam) =>
        graph.edges.filter((e) => e.target === exam.id).map((e) => e.source)
      );
      const pathways = [...new Set(pathwayIds)]
        .map((id) => byId.get(id))
        .filter((n): n is FlowNode => !!n && n.type === "pathway");

      return { career, course, exams, pathways };
    });
}

// Advisory quiz for a student who doesn't yet know what they're interested
// in. Tier 3 by definition (see CLAUDE.md "Data safety tiers") — a nudge
// toward 2-3 directions to explore, never presented as a recommendation of
// fact. Career ids match the CAREER_IDS keys in flow-data.ts; suggestions are
// filtered against the live graph at render time so a renamed/removed career
// id never points somewhere that no longer exists.
export type QuizQuestion = {
  id: string;
  prompt: string;
  options: { id: string; label: string; suggests: string[] }[];
};

export const ADVISORY_QUIZ: QuizQuestion[] = [
  {
    id: "subject",
    prompt: "Which subject do you enjoy most right now?",
    options: [
      { id: "math-science", label: "Maths / Physics / Chemistry", suggests: ["engineering", "architecture", "science-research"] },
      { id: "biology", label: "Biology", suggests: ["medicine", "nursing", "pharmacy"] },
      { id: "numbers-money", label: "Numbers, accounts, or business", suggests: ["ca-career", "banking"] },
      { id: "reading-arguing", label: "Reading, debating, or current affairs", suggests: ["law-career", "civil-services", "teaching"] },
    ],
  },
  {
    id: "workstyle",
    prompt: "Which sounds more like your ideal workday?",
    options: [
      { id: "build-fix", label: "Building or fixing something technical", suggests: ["engineering", "architecture"] },
      { id: "help-people", label: "Directly helping or treating people", suggests: ["medicine", "nursing", "pharmacy"] },
      { id: "structure-rules", label: "Working within clear structure and rules", suggests: ["defence", "civil-services", "state-civil-services"] },
      { id: "numbers-strategy", label: "Analysing numbers or making a case", suggests: ["ca-career", "banking", "law-career"] },
    ],
  },
  {
    id: "setting",
    prompt: "Government path, private path, or open to either?",
    options: [
      { id: "govt", label: "Government service specifically", suggests: ["civil-services", "state-civil-services", "defence", "teaching"] },
      { id: "private", label: "Private sector / self-directed career", suggests: ["engineering", "ca-career", "banking"] },
      { id: "either", label: "Either is fine", suggests: ["medicine", "pharmacy", "law-career", "architecture", "science-research"] },
    ],
  },
];

export function scoreQuiz(answers: Record<string, string>, quiz: QuizQuestion[]): string[] {
  const tally = new Map<string, number>();
  for (const q of quiz) {
    const chosenId = answers[q.id];
    const option = q.options.find((o) => o.id === chosenId);
    if (!option) continue;
    for (const careerId of option.suggests) {
      tally.set(careerId, (tally.get(careerId) ?? 0) + 1);
    }
  }
  return [...tally.entries()].sort((a, b) => b[1] - a[1]).slice(0, 3).map(([id]) => id);
}
