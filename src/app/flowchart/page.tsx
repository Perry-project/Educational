import { Figtree, Sora } from "next/font/google";
import MetroFlow from "@/components/metro-flow";
import { getFlowchartData } from "@/lib/flowchart-db";
import { stateOf } from "@/lib/class10-flow-data";
import { cached } from "@/lib/cache";

const figtree = Figtree({ subsets: ["latin"], weight: ["400", "500", "600", "700", "800"] });
const sora = Sora({ subsets: ["latin"], weight: ["600", "700", "800"] });

export const metadata = {
  title: "Class 10 to Career — Perry",
  description: "Every career is a line from Class 10. Pick one to see its stops, exams and dates.",
};

// Rendered per request; the database reads behind it are cached for an hour (see lib/cache.ts).
export const dynamic = "force-dynamic";

const getCachedFlowchart = cached(getFlowchartData, "flowchart");

const param = (v: string | string[] | undefined) => (typeof v === "string" && v ? v : null);

export default async function FlowPage({
  searchParams,
}: {
  searchParams: Promise<{ [key: string]: string | string[] | undefined }>;
}) {
  const sp = await searchParams;
  // ?state=ts shows the Telangana chart; Andhra Pradesh otherwise.
  const data = await getCachedFlowchart(stateOf(sp.state));
  // ?career=12&stop=eapcet&via=jeemain opens a shared route, ?field=cl_med a
  // field on the start screen; ?step= links
  // from the old chart still open the matching line.
  const initial = { career: param(sp.career), stop: param(sp.stop), via: param(sp.via), step: param(sp.step), field: param(sp.field) };
  // Keyed by state so switching states starts the chart afresh.
  return (
    <MetroFlow
      key={data.state}
      data={data}
      initial={initial}
      bodyFont={figtree.style.fontFamily}
      displayFont={sora.style.fontFamily}
    />
  );
}
