import { SYSTEM_FONT } from "@/lib/fonts";
import Pathfinder from "@/components/pathfinder";
import { getFlowGraph } from "@/lib/flow-data";
import { getCollegesForCourse, type CollegeMatch } from "@/lib/decision-data";
import { cached } from "@/lib/cache";


export const metadata = {
  title: "Pathfinder — Perry",
  description: "Pick a career, or let Perry suggest a few, then see the exam, course and college steps to get there.",
};

// Rendered per request; the database reads behind it are cached for an hour (see lib/cache.ts).
export const dynamic = "force-dynamic";

// The graph plus one college query per course, cached together.
const getPathfinderData = cached(async () => {
  const graph = await getFlowGraph();

  const courseNodes = graph.nodes.filter((n) => n.type === "course");
  const collegesByCourseEntries = await Promise.all(
    courseNodes.map(async (course) => [course.id, await getCollegesForCourse(course.label)] as const)
  );
  const collegesByCourse: Record<string, CollegeMatch[]> = Object.fromEntries(collegesByCourseEntries);
  return { graph, collegesByCourse };
}, "pathfinder");

export default async function PathfinderPage() {
  const { graph, collegesByCourse } = await getPathfinderData();

  return (
    <Pathfinder
      graph={graph}
      collegesByCourse={collegesByCourse}
      bodyFont={SYSTEM_FONT}
      displayFont={SYSTEM_FONT}
    />
  );
}
