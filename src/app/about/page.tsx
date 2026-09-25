import Link from "next/link";

export const metadata = {
  title: "About — Perry",
  description: "Why Perry exists and where it is going.",
};

const ROADMAP = [
  { title: "Phase 1 — Class 10 to Career flowchart", body: "Every Andhra Pradesh route from Class 10 through groups, exams and courses to careers.", now: true },
  { title: "Phase 2 — Exams, courses & colleges", body: "Pages for each entrance exam, course and AP college, with study topics for every course." },
  { title: "Phase 3 — Personal guidance", body: "Suggestions matched to a student's interests and marks, once the data behind them is fully checked." },
];

const card = "rounded-2xl border border-gray-700 bg-gray-800/80 p-6";

export default function About() {
  return (
    <div className="mx-auto max-w-4xl px-4 py-14 sm:px-6 lg:px-8">
      <header className="site-fade-up text-center">
        <h1 className="text-4xl font-bold tracking-tight">About Perry</h1>
        <p className="mt-4 text-gray-400">A clear, structured way to see career paths before choosing one.</p>
      </header>

      <section className="mt-14 space-y-12">
        <div>
          <h2 className="mb-3 text-xl font-semibold text-[var(--site-heading)]">The problem</h2>
          <p className="leading-relaxed text-gray-300">
            After Class 10, students face pressure from every side and very little clear information. Choices that
            shape the next five to ten years are often made without seeing all the options or where each one leads.
          </p>
        </div>
        <div>
          <h2 className="mb-3 text-xl font-semibold text-[var(--site-heading)]">Our approach</h2>
          <p className="leading-relaxed text-gray-300">
            Perry turns the whole system into one visual flowchart. Students tap any step, whether a group, an exam, a
            course or a career, and see every route through it, so they can compare paths calmly and decide for
            themselves.
          </p>
        </div>
      </section>

      <section className="mt-16">
        <h2 className="mb-6 text-center text-xl font-semibold text-[var(--site-heading)]">Mission &amp; vision</h2>
        <div className="grid gap-6 md:grid-cols-2">
          <div className={card}>
            <h3 className="mb-2 text-lg font-semibold">Our mission</h3>
            <p className="text-sm leading-relaxed text-gray-300">
              Give every student clear, honest and structured career guidance, free and without sign-ups.
            </p>
          </div>
          <div className={card}>
            <h3 className="mb-2 text-lg font-semibold">Our vision</h3>
            <p className="text-sm leading-relaxed text-gray-300">
              A trusted place where any student in India can explore education and career paths without
              misinformation or pressure.
            </p>
          </div>
        </div>
      </section>

      <section className="mt-16">
        <h2 className="mb-6 text-center text-xl font-semibold text-[var(--site-heading)]">Roadmap</h2>
        <ol className="space-y-4">
          {ROADMAP.map((r) => (
            <li key={r.title} className={`${card} p-5 ${r.now ? "border-blue-500/60" : ""}`}>
              <p className="flex flex-wrap items-center gap-2 font-semibold">
                {r.title}
                {r.now && <span className="rounded-full bg-blue-500/20 px-2 py-0.5 text-xs font-medium text-blue-300">Live now</span>}
              </p>
              <p className="mt-1 text-sm text-gray-300">{r.body}</p>
            </li>
          ))}
        </ol>
      </section>

      <p className="mt-16 border-t border-gray-800 pt-8 text-center text-sm text-gray-400">
        Ready to look around?{" "}
        <Link href="/flowchart" className="font-medium text-blue-400 hover:text-blue-300">
          Open the flowchart →
        </Link>
      </p>
    </div>
  );
}
