import Link from "next/link";
import { pool } from "@/lib/db";

// Counts come from the database so they grow with each nightly import.
export const dynamic = "force-dynamic";

async function getCounts() {
  const { rows } = await pool.query(
    `SELECT (SELECT count(*) FROM pathways)::int AS pathways, (SELECT count(*) FROM entrance_exams)::int AS exams,
            (SELECT count(*) FROM courses)::int AS courses, (SELECT count(*) FROM careers)::int AS careers,
            (SELECT count(*) FROM colleges)::int AS colleges`
  );
  return rows[0] as Record<"pathways" | "exams" | "courses" | "careers" | "colleges", number>;
}

const steps = (n: Awaited<ReturnType<typeof getCounts>>) => [
  { n: 1, label: "Class 10 pass", sub: "SSC · CBSE · ICSE", color: "bg-slate-200 text-gray-900" },
  { n: 2, label: "After Class 10", sub: `${n.pathways} pathways · Intermediate, Polytechnic, ITI…`, color: "bg-blue-500/15 text-blue-200 border border-blue-400/30" },
  { n: 3, label: "Entrance exams", sub: `${n.exams} exams · EAPCET, NEET, JEE…`, color: "bg-orange-500/15 text-orange-200 border border-orange-400/30" },
  { n: 4, label: "Courses", sub: `${n.courses} courses · ${n.colleges} AP colleges`, color: "bg-teal-500/15 text-teal-200 border border-teal-400/30" },
  { n: 5, label: "Careers", sub: `${n.careers} careers`, color: "bg-pink-500/15 text-pink-200 border border-pink-400/30" },
];

const AUDIENCE = [
  { title: "Class 10 students", body: "Choosing a group or trade for the next two years." },
  { title: "Intermediate students", body: "Picking entrance exams and a degree." },
  { title: "Diploma & ITI students", body: "Finding lateral entry and next steps." },
  { title: "Parents & guardians", body: "Seeing every option before deciding together." },
];

const primaryBtn =
  "inline-flex items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-blue-500 to-violet-500 px-8 py-4 text-lg font-semibold text-white shadow-xl transition hover:from-blue-600 hover:to-violet-600";
const card = "rounded-2xl border border-gray-700 bg-gray-800/80 p-6";

export default async function Home() {
  const STEPS = steps(await getCounts());
  return (
    <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
      <section className="site-fade-up flex min-h-[calc(100svh-var(--nav-h))] flex-col items-center justify-center py-16 text-center">
        <p className="mb-5 rounded-full border border-blue-400/30 bg-blue-500/10 px-4 py-1.5 text-sm font-medium text-blue-200">
          For students in Andhra Pradesh
        </p>
        <h1 className="text-4xl font-bold leading-tight tracking-tight sm:text-5xl lg:text-6xl">
          See Every <span className="text-blue-400">Career Path</span>
          <br className="hidden sm:block" /> Before You Choose One
        </h1>
        <p className="mt-6 max-w-2xl text-lg leading-relaxed text-gray-300">
          Perry lays out every route from Class 10, through each group, entrance exam and course, to the careers it
          leads to, so you can see how they connect.
        </p>
        <div className="mt-10 flex flex-col gap-4 sm:flex-row">
          <Link href="/flowchart" className={primaryBtn}>
            Open Career Flowchart
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden>
              <path d="M5 12h14M13 6l6 6-6 6" />
            </svg>
          </Link>
          <Link
            href="/pathfinder"
            className="inline-flex items-center justify-center rounded-xl border border-gray-600 px-8 py-4 text-lg font-semibold text-gray-200 transition hover:bg-gray-800 hover:text-white"
          >
            Find my path
          </Link>
        </div>
      </section>

      <section className="grid items-center gap-10 py-16 md:grid-cols-2 md:gap-14">
        <div>
          <h2 className="mb-5 text-3xl font-semibold">Why Perry exists</h2>
          <p className="leading-relaxed text-gray-400">
            Most students don&apos;t struggle for lack of ability. They struggle because nobody shows them the full set
            of options. Perry puts every route on one page, one step at a time, so a choice made after Class 10 is an
            informed one.
          </p>
        </div>
        <div className={`${card} shadow-xl`}>
          <p className="mb-4 text-sm text-gray-400">How a route is laid out</p>
          <ol className="space-y-3">
            {STEPS.map((s, i) => (
              <li
                key={s.n}
                className={`flex items-center gap-3 rounded-lg p-3 transition hover:translate-x-1 ${s.color}`}
                style={{ marginLeft: `min(${i * 16}px, ${i * 4}vw)` }}
              >
                <span className="grid h-6 w-6 flex-none place-items-center rounded-full bg-black/25 text-xs font-bold">{s.n}</span>
                <span className="min-w-0">
                  <span className="block font-semibold">{s.label}</span>
                  <span className="block text-xs opacity-80">{s.sub}</span>
                </span>
              </li>
            ))}
          </ol>
        </div>
      </section>

      <section className="py-16">
        <h2 className="mb-12 text-center text-3xl font-semibold">What Perry offers, and what it doesn&apos;t</h2>
        <div className="grid gap-6 md:grid-cols-2 md:gap-10">
          <div className={card}>
            <h3 className="mb-4 text-xl font-semibold text-green-400">What you get</h3>
            <ul className="space-y-3 text-gray-300">
              <li>✔ One flowchart from Class 10 to careers</li>
              <li>✔ Andhra Pradesh groups, exams and colleges</li>
              <li>✔ Tap any step to trace its full route</li>
              <li>✔ Works on any phone, free, no sign-up</li>
            </ul>
          </div>
          <div className={card}>
            <h3 className="mb-4 text-xl font-semibold text-red-400">What you won&apos;t see</h3>
            <ul className="space-y-3 text-gray-300">
              <li>✖ Promises of guaranteed jobs or salaries</li>
              <li>✖ Guessed cutoffs or dates</li>
              <li>✖ Paid rankings or ads</li>
              <li>✖ Forced sign-ups</li>
            </ul>
          </div>
        </div>
      </section>

      <section className="py-16">
        <h2 className="mb-12 text-center text-3xl font-semibold">Who is Perry for?</h2>
        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
          {AUDIENCE.map((a) => (
            <div key={a.title} className={`${card} text-center transition-all duration-300 hover:-translate-y-1 hover:border-blue-500`}>
              <p className="text-lg font-medium">{a.title}</p>
              <p className="mt-2 text-sm text-gray-400">{a.body}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="py-24 text-center">
        <h2 className="mb-6 text-3xl font-bold sm:text-4xl">Start with understanding, not guessing</h2>
        <p className="mb-10 text-gray-400">Explore the paths calmly, one step at a time.</p>
        <Link href="/flowchart" className={primaryBtn}>
          Start exploring
        </Link>
      </section>
    </div>
  );
}
