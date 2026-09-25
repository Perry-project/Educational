import { Figtree } from "next/font/google";
import Class10Flow from "@/components/class10-flow";
import { getFlowchartData } from "@/lib/flowchart-db";

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
  const [data, { step }] = await Promise.all([getFlowchartData(), searchParams]);
  // ?step=btech opens the chart with that step selected (shared links).
  const initialStep = typeof step === "string" ? step : null;
  return <Class10Flow data={data} fontFamily={figtree.style.fontFamily} initialStep={initialStep} />;
}
