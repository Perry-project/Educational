import { Figtree, Sora } from "next/font/google";
import SecondChance from "@/components/second-chance";
import { getSecondChanceRoutes } from "@/lib/second-chance-db";
import { cached } from "@/lib/cache";

const figtree = Figtree({ subsets: ["latin"], weight: ["400", "500", "600", "700", "800"] });
const sora = Sora({ subsets: ["latin"], weight: ["600", "700", "800"] });

export const metadata = {
  title: "Second Chance — Perry",
  description: "Stopped studying after Class 10, Intermediate or a degree? Official routes back for Andhra Pradesh and Telangana students: supplementary exams, open schools, ITIs, open universities and apprenticeships.",
};

// Rendered per request; the database reads behind it are cached for an hour (see lib/cache.ts).
export const dynamic = "force-dynamic";

const getCachedRoutes = cached(getSecondChanceRoutes, "second-chance");

const param = (v: string | string[] | undefined) => (typeof v === "string" && v ? v : null);

export default async function SecondChancePage({
  searchParams,
}: {
  searchParams: Promise<{ [key: string]: string | string[] | undefined }>;
}) {
  const sp = await searchParams;
  const routes = await getCachedRoutes();
  // ?from=intermediate&state=ts&route=12 opens a shared view.
  const initial = { from: param(sp.from), state: param(sp.state), route: param(sp.route) };
  return <SecondChance routes={routes} initial={initial} bodyFont={figtree.style.fontFamily} displayFont={sora.style.fontFamily} />;
}
