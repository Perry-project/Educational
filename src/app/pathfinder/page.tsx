import { Figtree, Sora } from "next/font/google";
import Pathfinder from "@/components/pathfinder";
import { getFlowGraph } from "@/lib/flow-data";
import { getCollegesForCourse, type CollegeMatch } from "@/lib/decision-data";

const figtree = Figtree({ subsets: ["latin"], weight: ["400", "500", "600", "700", "800"] });
const sora = Sora({ subsets: ["latin"], weight: ["600", "700", "800"] });

export const metadata = {
  title: "Pathfinder — Perry",
  description: "Pick a career, or let Perry suggest a few, then see the exam, course and college steps to get there.",
};

// Read the database on every request, so a nightly import shows up without a rebuild.
export const dynamic = "force-dynamic";

export default async function PathfinderPage() {
  const graph = await getFlowGraph();

  const courseNodes = graph.nodes.filter((n) => n.type === "course");
  const collegesByCourseEntries = await Promise.all(
    courseNodes.map(async (course) => [course.id, await getCollegesForCourse(course.label)] as const)
  );
  const collegesByCourse: Record<string, CollegeMatch[]> = Object.fromEntries(collegesByCourseEntries);

  return (
    <Pathfinder
      graph={graph}
      collegesByCourse={collegesByCourse}
      bodyFont={figtree.style.fontFamily}
      displayFont={sora.style.fontFamily}
    />
  );
}
