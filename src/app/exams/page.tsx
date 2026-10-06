import { Figtree, Sora } from "next/font/google";
import ExamsBrowser from "@/components/exams-browser";
import { getExams } from "@/lib/exams-db";

const figtree = Figtree({ subsets: ["latin"], weight: ["400", "500", "600", "700", "800"] });
const sora = Sora({ subsets: ["latin"], weight: ["600", "700", "800"] });

export const metadata = {
  title: "Exams — Perry",
  description: "Every exam from Class 1 to a government job, for Andhra Pradesh and Telangana students: dates, syllabus and qualifying marks.",
};

// Read the database on every request, so a nightly import shows up without a rebuild.
export const dynamic = "force-dynamic";

const param = (v: string | string[] | undefined) => (typeof v === "string" && v ? v : null);

export default async function ExamsPage({
  searchParams,
}: {
  searchParams: Promise<{ [key: string]: string | string[] | undefined }>;
}) {
  const sp = await searchParams;
  const exams = await getExams();
  // ?exam=12&state=ts&stage=jobs&type=Private opens a shared view.
  const initial = { exam: param(sp.exam), state: param(sp.state), stage: param(sp.stage), type: param(sp.type) };
  return <ExamsBrowser exams={exams} initial={initial} bodyFont={figtree.style.fontFamily} displayFont={sora.style.fontFamily} />;
}
