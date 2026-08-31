import FlowExplorer from "@/components/flow-explorer";
import { getFlowGraph } from "@/lib/flow-data";

export const metadata = {
  title: "Flow Explorer — Perry",
  description: "Trace a route from a Class 10 pass through to the course it admits into.",
};

export default async function FlowPage() {
  const graph = await getFlowGraph();

  return (
    <div className="mx-auto max-w-[1440px] px-6 py-10">
      <h1 className="text-2xl font-semibold tracking-tight">Class 10 to Career</h1>
      <p className="mt-2 max-w-2xl text-sm text-black/60 dark:text-white/60">
        Every pathway, entrance exam, and course currently in the Perry database, laid out as one interactive
        flow. Tap a card to trace its route.
      </p>
      <div className="mt-6">
        <FlowExplorer graph={graph} />
      </div>
    </div>
  );
}
