import Pathfinder from "@/components/pathfinder";
import { getFlowGraph } from "@/lib/flow-data";
import { getCollegesForCourse, type CollegeMatch } from "@/lib/decision-data";

export const metadata = {
  title: "Pathfinder — Perry",
  description: "Pick a career, or let Perry suggest a few — then see the exam, syllabus, and college steps to get there.",
};

export default async function PathfinderPage() {
  const graph = await getFlowGraph();

  const courseNodes = graph.nodes.filter((n) => n.type === "course");
  const collegesByCourseEntries = await Promise.all(
    courseNodes.map(async (course) => [course.id, await getCollegesForCourse(course.label)] as const)
  );
  const collegesByCourse: Record<string, CollegeMatch[]> = Object.fromEntries(collegesByCourseEntries);

  return (
    <div className="mx-auto max-w-[1100px] px-6 py-10">
      <h1 className="text-2xl font-semibold tracking-tight">Find Your Path</h1>
      <p className="mt-2 max-w-2xl text-sm text-black/60 dark:text-white/60">
        Tell Perry what you&apos;re aiming for — or answer a few quick questions if you&apos;re not sure yet — and
        see the real exams, syllabus focus, and colleges between here and there.
      </p>
      <div className="mt-6">
        <Pathfinder graph={graph} collegesByCourse={collegesByCourse} />
      </div>
    </div>
  );
}
