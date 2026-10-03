import { Figtree } from "next/font/google";
import Class10Flow from "@/components/class10-flow";
import { getFlowchartData } from "@/lib/flowchart-db";
import { stateOf } from "@/lib/class10-flow-data";

const figtree = Figtree({ subsets: ["latin"], weight: ["400", "500", "600", "700", "800"] });

export const metadata = {
  title: "Class 10 to Career — Perry",
  description: "Tap any step to see every route through it, from Class 10 to the careers it opens.",
};

// Read the database on every request, so a nightly import shows up without a rebuild.
export const dynamic = "force-dynamic";

export default async function FlowPage({
  searchParams,
}: {
  searchParams: Promise<{ [key: string]: string | string[] | undefined }>;
}) {
  const { step, state } = await searchParams;
  // ?state=ts shows the Telangana chart; Andhra Pradesh otherwise.
  const data = await getFlowchartData(stateOf(state));
  // ?step=btech opens the chart with that step selected (shared links).
  const initialStep = typeof step === "string" ? step : null;
  // Keyed by state so switching states starts the chart afresh.
  return <Class10Flow key={data.state} data={data} fontFamily={figtree.style.fontFamily} initialStep={initialStep} />;
}
