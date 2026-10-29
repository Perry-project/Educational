import Link from "next/link";
import Icon from "@/components/icon";
import PageHead from "@/components/page-head";

export const metadata = {
  title: "About — Perry",
  description: "Why Perry exists, how it checks its facts, and what comes next.",
};

const FACTS = [
  ["shieldCheck", "Dates, syllabus and cutoffs", "Only from the official notification or portal, with a link so you can check it yourself."],
  ["clock", "Not announced yet", "When a date isn’t out, Perry says so. It never estimates a date or a cutoff."],
  ["info", "Placement figures", "Never shown as one number. Only as a range, with who reported it."],
  ["compass", "Suggestions and study topics", "Marked as AI-assisted: a guide to explore, not a final answer."],
];

const ROADMAP = [
  { title: "Career map, exams, second chances and news", body: "Every route from Class 10, every exam with its dates, official ways back, and daily news.", now: true },
  { title: "More colleges and cutoffs", body: "College lists and last year’s closing ranks for each course, from counselling records." },
  { title: "Personal guidance", body: "Suggestions matched to a student’s interests and marks, once the data behind them is fully checked." },
];

export default function About() {
  return (
    <>
      <PageHead title="About Perry">
        A free map of every route from Class 10 to a career, for students and parents in Andhra Pradesh and Telangana.
      </PageHead>

      <div className="mx-auto flex max-w-[860px] flex-col gap-12 px-4 pt-10 pb-20 sm:px-6 lg:px-8">
        <section aria-labelledby="why-h" className="flex flex-col gap-3">
          <h2 id="why-h" className="m-0 text-[20px] font-bold">Why Perry exists</h2>
          <p className="m-0 text-[16px] leading-relaxed" style={{ color: "var(--soft)" }}>
            After Class 10, students choose a path that shapes the next ten years, often under pressure and with very little clear
            information. Perry lays out the whole system step by step: the group, the entrance exam, the course and the career,
            so students and parents can compare options and decide together.
          </p>
        </section>

        <section aria-labelledby="facts-h" className="flex flex-col gap-4">
          <h2 id="facts-h" className="m-0 text-[20px] font-bold">How information is handled</h2>
          <ul className="m-0 grid list-none gap-3 p-0 sm:grid-cols-2">
            {FACTS.map(([icon, title, text]) => (
              <li key={title} className="card flex flex-col gap-2 p-5">
                <span style={{ color: "var(--teal)" }}><Icon name={icon} size={20} /></span>
                <span className="text-[15px] font-semibold">{title}</span>
                <span className="text-[14px] leading-relaxed" style={{ color: "var(--muted)" }}>{text}</span>
              </li>
            ))}
          </ul>
        </section>

        <section aria-labelledby="next-h" className="flex flex-col gap-4">
          <h2 id="next-h" className="m-0 text-[20px] font-bold">Roadmap</h2>
          <ol className="m-0 flex list-none flex-col gap-3 p-0">
            {ROADMAP.map((r) => (
              <li key={r.title} className="card flex items-start gap-3 p-5">
                <span className="mt-0.5" style={{ color: r.now ? "var(--teal)" : "var(--muted)" }}><Icon name={r.now ? "checkCircle" : "clock"} size={20} /></span>
                <span className="flex flex-col gap-1">
                  <span className="flex flex-wrap items-center gap-2 text-[15px] font-semibold">
                    {r.title}{r.now && <span className="pill pill-open">Live now</span>}
                  </span>
                  <span className="text-[14px] leading-relaxed" style={{ color: "var(--muted)" }}>{r.body}</span>
                </span>
              </li>
            ))}
          </ol>
        </section>

        <div className="flex flex-wrap items-center gap-3">
          <Link href="/flowchart" className="btn">Open the career map <Icon name="arrowRight" size={16} /></Link>
          <Link href="/disclaimer" className="btn btn-secondary">Read the disclaimer</Link>
        </div>
      </div>
    </>
  );
}
