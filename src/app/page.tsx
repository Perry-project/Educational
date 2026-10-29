import Link from "next/link";
import Icon from "@/components/icon";
import { pool } from "@/lib/db";
import { cached } from "@/lib/cache";
import { CLUSTER_DEFS } from "@/lib/class10-flow-data";
import { careerCluster, CLUSTER_COLOR } from "@/lib/metro-routes";

// Counts come from the database, so they follow each nightly import (cached for an hour).
export const dynamic = "force-dynamic";

const getHome = cached(async () => {
  const [counts, careers] = await Promise.all([
    pool.query(
      `SELECT (SELECT count(*) FROM entrance_exams)::int AS exams, (SELECT count(*) FROM careers)::int AS careers,
              (SELECT count(*) FROM second_chance_routes)::int AS routes, (SELECT count(*) FROM colleges)::int AS colleges`
    ),
    pool.query(
      `SELECT career_name FROM careers c JOIN states s ON s.id = c.state_id WHERE s.name = 'Andhra Pradesh' ORDER BY career_name`
    ),
  ]);
  return {
    counts: counts.rows[0] as Record<"exams" | "careers" | "routes" | "colleges", number>,
    careers: careers.rows.map((r) => r.career_name as string),
  };
}, "home");

const START = [
  { href: "/flowchart", icon: "school", title: "In Class 10", text: "Compare MPC, BiPC, CEC, Polytechnic and ITI, and see where each one leads." },
  { href: "/exams?stage=after_12", icon: "book", title: "In Intermediate", text: "Find the entrance exams for engineering, medicine, law and more." },
  { href: "/exams?stage=jobs", icon: "cap", title: "Finishing a degree", text: "PG entrance exams and government job exams, with dates." },
  { href: "/second-chance", icon: "rotate", title: "Stopped studying", text: "Official ways back: open schools, supplementary exams, ITIs." },
];

// The sample route shown in the hero: the real steps of one common line.
const PREVIEW = [
  { step: "Starting point", name: "Class 10 pass", note: "SSC · CBSE · ICSE" },
  { step: "Years 1–2", name: "Intermediate MPC", note: "Maths, Physics, Chemistry" },
  { step: "Entrance exam", name: "AP EAPCET", note: "or JEE Main", pill: true },
  { step: "Years 3–6", name: "B.Tech", note: "4-year engineering degree" },
  { step: "Career", name: "Software engineer", done: true },
];

export default async function Home() {
  const { counts, careers } = await getHome();

  const fields = CLUSTER_DEFS.map((d) => ({
    ...d, color: CLUSTER_COLOR[d.id], count: careers.filter((c) => careerCluster(c) === d.id).length,
  })).filter((f) => f.count && f.id !== "cl_oth");

  const tools = [
    { href: "/flowchart", icon: "map", title: "Career map", text: `${counts.careers} careers, each traced step by step from Class 10.`, cta: "Open the map" },
    { href: "/exams", icon: "file", title: "Exams", text: `${counts.exams} exams with eligibility, dates, syllabus and cutoff marks.`, cta: "Browse exams" },
    { href: "/second-chance", icon: "rotate", title: "Second chance", text: `${counts.routes} official routes back for students who stopped studying.`, cta: "See the ways back" },
    { href: "/current-affairs", icon: "news", title: "News", text: "Daily current affairs for exam preparation, sorted by topic.", cta: "Read today’s news" },
  ];

  return (
    <>
      {/* ---------- hero ---------- */}
      <section style={{ background: "#fff", borderBottom: "1px solid var(--border)" }}>
        <div className="wrap grid items-center gap-10 py-12 lg:grid-cols-[1.1fr_1fr] lg:gap-16 lg:py-20">
          <div className="fade-in flex flex-col items-start gap-6">
            <span className="pill pill-na">Free · No sign-up · Andhra Pradesh &amp; Telangana</span>
            <h1 className="m-0 text-[34px] leading-[1.12] font-bold tracking-tight sm:text-[44px] lg:text-[54px]" style={{ color: "var(--ink)" }}>
              Plan your path from Class&nbsp;10 to a career
            </h1>
            <p className="m-0 max-w-[52ch] text-[17px] leading-relaxed lg:text-[18px]" style={{ color: "var(--soft)" }}>
              See every route, step by step: the group to choose, the entrance exams to write, the courses and colleges,
              and the careers they lead to. Built for students and parents.
            </p>
            <div className="flex w-full flex-col gap-3 sm:w-auto sm:flex-row">
              <Link href="/flowchart" className="btn !min-h-12 !px-6 text-[16px]">
                Open the career map <Icon name="arrowRight" size={18} />
              </Link>
              <Link href="/exams" className="btn btn-secondary !min-h-12 !px-6 text-[16px]">Browse {counts.exams} exams</Link>
            </div>
            <ul className="m-0 flex list-none flex-wrap gap-x-6 gap-y-2 p-0 text-[14px]" style={{ color: "var(--soft)" }}>
              {[["shieldCheck", "Dates from official notices"], ["clock", "Never guesses a date"], ["heart", "Free, no ads"]].map(([icon, text]) => (
                <li key={text} className="flex items-center gap-2">
                  <span style={{ color: "var(--teal)" }}><Icon name={icon} size={17} /></span>{text}
                </li>
              ))}
            </ul>
          </div>

          {/* A real route, drawn in CSS: what the career map shows. */}
          <div className="fade-in card p-5 sm:p-6" style={{ animationDelay: "120ms" }} aria-label="Example route: Class 10 to software engineer">
            <div className="mb-5 flex items-center justify-between gap-3">
              <span className="flex items-center gap-2 text-[14px] font-semibold" style={{ color: CLUSTER_COLOR.cl_eng }}>
                <Icon name="cl_eng" size={18} /> Engineering &amp; Tech
              </span>
              <span className="text-[13px]" style={{ color: "var(--muted)" }}>About 6 years · 5 steps</span>
            </div>
            <ol className="m-0 flex list-none flex-col p-0">
              {PREVIEW.map((p, i) => {
                const last = i === PREVIEW.length - 1;
                return (
                  <li key={p.name} className="grid grid-cols-[28px_minmax(0,1fr)] gap-x-3">
                    <span className="relative flex justify-center">
                      {!last && <span aria-hidden className="absolute top-7 bottom-0 w-0.5" style={{ background: "var(--border)" }} />}
                      <span aria-hidden className="relative grid h-7 w-7 place-items-center rounded-full text-[12px] font-semibold"
                        style={p.done ? { background: "var(--teal)", color: "#fff" } : { background: "#fff", color: "var(--ink)", boxShadow: "inset 0 0 0 1px var(--border)" }}>
                        {p.done ? <Icon name="check" size={14} strokeWidth={3} /> : i + 1}
                      </span>
                    </span>
                    <div className={`flex flex-wrap items-start justify-between gap-x-3 gap-y-1 ${last ? "" : "pb-4"}`}>
                      <span className="flex min-w-0 flex-col">
                        <span className="text-[12px]" style={{ color: "var(--muted)" }}>{p.step}</span>
                        <span className="text-[15px] font-semibold" style={{ color: "var(--ink)" }}>{p.name}</span>
                        {p.note && <span className="text-[13px]" style={{ color: "var(--muted)" }}>{p.note}</span>}
                      </span>
                      {p.pill && <span className="pill pill-na">Next dates not announced</span>}
                    </div>
                  </li>
                );
              })}
            </ol>
          </div>
        </div>
      </section>

      {/* ---------- where are you now ---------- */}
      <section className="wrap py-14 lg:py-20" aria-labelledby="start-h">
        <div className="mb-8 flex flex-col gap-2">
          <h2 id="start-h" className="m-0 text-[24px] font-bold tracking-tight lg:text-[30px]">Where are you now?</h2>
          <p className="m-0 text-[16px]" style={{ color: "var(--muted)" }}>Pick your stage. Perry opens the right place to start.</p>
        </div>
        <ul className="m-0 grid list-none gap-3 p-0 sm:grid-cols-2 lg:grid-cols-4">
          {START.map((s) => (
            <li key={s.href}>
              <Link href={s.href} className="card press flex h-full flex-col gap-3 p-5 no-underline" style={{ color: "var(--ink)" }}>
                <span className="grid h-10 w-10 place-items-center rounded-lg" style={{ background: "var(--indigo-soft)", color: "var(--indigo)" }}>
                  <Icon name={s.icon} size={20} />
                </span>
                <span className="text-[17px] font-semibold">{s.title}</span>
                <span className="text-[14px] leading-relaxed" style={{ color: "var(--muted)" }}>{s.text}</span>
                <span className="mt-auto flex items-center gap-1 pt-1 text-[14px] font-semibold" style={{ color: "var(--indigo)" }}>
                  Start here <Icon name="arrowRight" size={15} />
                </span>
              </Link>
            </li>
          ))}
        </ul>
      </section>

      {/* ---------- tools ---------- */}
      <section style={{ background: "#fff", borderBlock: "1px solid var(--border)" }} aria-labelledby="tools-h">
        <div className="wrap py-14 lg:py-20">
          <div className="mb-8 flex flex-col gap-2">
            <h2 id="tools-h" className="m-0 text-[24px] font-bold tracking-tight lg:text-[30px]">Everything in one place</h2>
            <p className="m-0 text-[16px]" style={{ color: "var(--muted)" }}>Four tools, one set of checked facts.</p>
          </div>
          <div className="grid gap-px overflow-hidden rounded-xl sm:grid-cols-2" style={{ background: "var(--border)", border: "1px solid var(--border)" }}>
            {tools.map((t) => (
              <Link key={t.href} href={t.href} className="group flex flex-col gap-3 p-6 no-underline transition-colors hover:bg-[var(--bg)] lg:p-8" style={{ background: "#fff", color: "var(--ink)" }}>
                <span style={{ color: "var(--indigo)" }}><Icon name={t.icon} size={24} /></span>
                <span className="text-[18px] font-semibold">{t.title}</span>
                <span className="max-w-[44ch] text-[15px] leading-relaxed" style={{ color: "var(--muted)" }}>{t.text}</span>
                <span className="mt-1 flex items-center gap-1 text-[14px] font-semibold" style={{ color: "var(--indigo)" }}>
                  {t.cta} <span className="transition-transform group-hover:translate-x-0.5"><Icon name="arrowRight" size={15} /></span>
                </span>
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* ---------- fields ---------- */}
      <section className="wrap py-14 lg:py-20" aria-labelledby="fields-h">
        <div className="mb-8 flex flex-col gap-2">
          <h2 id="fields-h" className="m-0 text-[24px] font-bold tracking-tight lg:text-[30px]">Explore careers by field</h2>
          <p className="m-0 text-[16px]" style={{ color: "var(--muted)" }}>Each field opens its careers on the map.</p>
        </div>
        <ul className="m-0 grid list-none grid-cols-2 gap-3 p-0 lg:grid-cols-4">
          {fields.map((f) => (
            <li key={f.id}>
              <Link href={`/flowchart?field=${f.id}`} className="card press flex h-full min-h-[112px] flex-col gap-2 p-4 no-underline" style={{ color: "var(--ink)" }}>
                <span style={{ color: f.color }}><Icon name={f.id} size={22} /></span>
                <span className="text-[15px] leading-snug font-semibold">{f.name}</span>
                <span className="mt-auto text-[13px]" style={{ color: "var(--muted)" }}>{f.count} careers</span>
              </Link>
            </li>
          ))}
        </ul>
      </section>

      {/* ---------- how facts are handled ---------- */}
      <section style={{ background: "#fff", borderBlock: "1px solid var(--border)" }} aria-labelledby="trust-h">
        <div className="wrap py-14 lg:py-20">
          <h2 id="trust-h" className="m-0 mb-8 text-[24px] font-bold tracking-tight lg:text-[30px]">Information you can rely on</h2>
          <div className="grid gap-8 md:grid-cols-3">
            {[
              ["shieldCheck", "From official sources", "Exam dates, eligibility and cutoffs come from the official notification or portal, linked so you can check them yourself."],
              ["clock", "Never guessed", "If a date isn’t announced yet, Perry says “Not announced yet”. It never estimates a date or a cutoff."],
              ["heart", "Free for everyone", "No sign-up, no ads and no paid rankings. Light enough to load quickly on any phone."],
            ].map(([icon, title, text]) => (
              <div key={title} className="flex flex-col gap-2">
                <span className="grid h-10 w-10 place-items-center rounded-lg" style={{ background: "var(--teal-soft)", color: "var(--teal-ink)" }}><Icon name={icon} size={20} /></span>
                <h3 className="m-0 mt-1 text-[17px] font-semibold">{title}</h3>
                <p className="m-0 text-[15px] leading-relaxed" style={{ color: "var(--muted)" }}>{text}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ---------- closing ---------- */}
      <section className="wrap py-14 lg:py-20" aria-labelledby="cta-h">
        <div className="card flex flex-col items-start gap-5 p-6 sm:p-10 lg:flex-row lg:items-center lg:justify-between">
          <div className="flex flex-col gap-2">
            <h2 id="cta-h" className="m-0 text-[22px] font-bold tracking-tight lg:text-[26px]">Not sure which career fits you?</h2>
            <p className="m-0 max-w-[56ch] text-[16px]" style={{ color: "var(--muted)" }}>
              Answer three quick questions and get a few careers to explore, each with its full route.
            </p>
          </div>
          <Link href="/pathfinder" className="btn !min-h-12 shrink-0 !px-6 text-[16px]">
            Find my path <Icon name="arrowRight" size={18} />
          </Link>
        </div>
      </section>
    </>
  );
}
