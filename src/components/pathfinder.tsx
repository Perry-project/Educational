"use client";

import Link from "next/link";
import { useEffect, useMemo, useState, type CSSProperties } from "react";
import "./metro-flow.css";
import type { FlowGraph, FlowNode } from "@/lib/flow-data";
import { ADVISORY_QUIZ, pathsToCareer, scoreQuiz } from "@/lib/decision-logic";
import type { CollegeMatch } from "@/lib/decision-data";
import { CLUSTER_COLOR, careerCluster } from "@/lib/metro-routes";
import { forStudents } from "@/lib/student-text";
import PageHead from "./page-head";
import Icon from "./icon";

// The /pathfinder page, in the flowchart's Metro style. A student either
// picks a career or answers three questions for a few suggestions (AI-
// assisted, advisory only). A chosen career shows each course route into it
// as a line of stations: start, entrance exam, course, career.

type Mode = "choose" | "quiz" | "pick";

const OFFICIAL_SOURCES = "cets.apsche.ap.gov.in (entrance tests) and cap.apcfss.in (counselling and seat allotment)";
const display = "var(--metro-display), var(--metro-body), system-ui, sans-serif";
const soft = "var(--soft)";
const checked = (n: { tier?: FlowNode["tier"] }) => n.tier?.dataTier === "tier_1_official";
// Careers students ask about most, offered as one-tap shortcuts.
const POPULAR = [/software|information technology/i, /medicine|mbbs/i, /teach/i, /chartered/i, /civil services/i, /nurs/i, /law/i, /defence/i];

export default function Pathfinder({
  graph, collegesByCourse, bodyFont, displayFont,
}: {
  graph: FlowGraph;
  collegesByCourse: Record<string, CollegeMatch[]>;
  bodyFont: string;
  displayFont: string;
}) {
  const [mode, setMode] = useState<Mode>("choose");
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [suggested, setSuggested] = useState<string[]>([]);
  const [careerId, setCareerId] = useState<string | null>(null);

  const careers = useMemo(() => graph.nodes.filter((n) => n.type === "career"), [graph.nodes]);
  const byId = useMemo(() => new Map(graph.nodes.map((n) => [n.id, n])), [graph.nodes]);
  const paths = useMemo(() => (careerId ? pathsToCareer(graph, careerId) : []), [graph, careerId]);
  const career = careerId ? byId.get(careerId) : undefined;

  const startOver = () => {
    setMode("choose");
    setAnswers({});
    setSuggested([]);
    setCareerId(null);
  };
  // Each step replaces the page's content, so start it from the top (on a
  // phone the button tapped is usually far down the previous step).
  const step = `${mode}|${careerId}|${suggested.join()}`;
  useEffect(() => {
    if (window.scrollY > 0) window.scrollTo({ top: 0 });
  }, [step]);

  const lineColor = (n: FlowNode) => CLUSTER_COLOR[careerCluster(n.label)];

  const rootStyle = { "--metro-body": bodyFont, "--metro-display": displayFont, fontFamily: bodyFont } as CSSProperties;
  const quiet = "inline-flex min-h-10 cursor-pointer items-center border-0 bg-transparent p-0 text-[15px] font-semibold";
  const ai = (text: string) => (
    <span className="self-start rounded-full px-3 py-1 text-[12px] font-bold" style={{ background: "var(--info-bg)", color: "var(--info-ink)" }}>{text}</span>
  );

  let body;
  if (career) {
    const color = lineColor(career);
    body = (
      <section className="flex flex-col gap-8" aria-labelledby="career-h">
        <div className="flex flex-col gap-2">
          <h2 id="career-h" className="m-0 text-[28px] leading-tight font-bold tracking-tight lg:text-[34px]">{career.label}</h2>
          <div className="flex flex-wrap gap-x-6 gap-y-2 pt-1">
            {career.dbId && (
              <Link href={`/flowchart?career=${career.dbId}`} className="text-[15px] font-semibold no-underline" style={{ color: "var(--accent)" }}>
                See this line on the flowchart →
              </Link>
            )}
            <button onClick={() => setCareerId(null)} className={quiet} style={{ color: "var(--muted)", fontFamily: "inherit" }}>Pick another career</button>
          </div>
        </div>

        {paths.length === 0 ? (
          <p className="m-0 text-[15px]" style={{ color: "var(--muted)" }}>No course route is mapped to this career yet.</p>
        ) : (
          paths.map(({ course, exams, pathways }, i) => {
            const colleges = collegesByCourse[course.id] ?? [];
            const stations: { kind: string; title: string; detail?: string | null; note?: string | null; href?: string }[] = [
              { kind: "Start", title: pathways.length ? pathways.map((p) => p.label).join(" or ") : "Class 10 pass" },
              ...exams.map((e) => ({
                kind: "Entrance exam",
                title: e.label,
                detail: checked(e) ? forStudents(e.sub) : null,
                note: checked(e) ? null : "Details soon",
                href: e.dbId ? `/exams?exam=${e.dbId}` : undefined,
              })),
              { kind: "Course", title: course.label, detail: checked(course) ? course.sub || null : null },
              { kind: "Career", title: career.label },
            ];
            return (
              <article key={course.id} className="flex flex-col gap-5 rounded-3xl p-5 sm:p-7" style={{ background: "var(--panel)" }}>
                <h3 className="m-0 text-[22px] font-bold" style={{ fontFamily: display }}>
                  {paths.length > 1 ? `Route ${i + 1} of ${paths.length}: ` : ""}via {course.label}
                </h3>
                <ol className="m-0 flex list-none flex-col p-0">
                  {stations.map((s, j) => {
                    const first = j === 0, last = j === stations.length - 1;
                    return (
                      <li key={s.kind + s.title} className="grid grid-cols-[28px_minmax(0,1fr)] gap-x-4">
                        <span className="relative flex justify-center">
                          <span className="absolute w-1.5" style={{ top: first ? 12 : 0, bottom: last ? "auto" : 0, height: last ? 12 : undefined, background: color }} />
                          <span className="relative mt-0.5 block h-6 w-6 shrink-0 rounded-full" style={{ boxSizing: "border-box", border: `5px solid ${color}`, background: last ? color : "var(--bg)" }} />
                        </span>
                        <div className={`flex min-w-0 flex-col gap-0.5 ${last ? "" : "pb-6"}`}>
                          <span className="text-[14px] font-semibold" style={{ color: "var(--muted)" }}>{s.kind}</span>
                          <span className="text-[18px] leading-snug font-bold" style={{ fontFamily: display }}>{s.title}</span>
                          {s.detail && <span className="line-clamp-2 max-w-[70ch] text-[14px] leading-snug" style={{ color: soft }}>{s.detail}</span>}
                          {s.note && <span className="text-[13px] font-semibold" style={{ color: "var(--muted)" }}>{s.note}</span>}
                          {s.href && (
                            <Link href={s.href} className="mt-1 text-[14px] font-semibold no-underline" style={{ color: "var(--accent)" }}>
                              Dates, syllabus and marks →
                            </Link>
                          )}
                        </div>
                      </li>
                    );
                  })}
                </ol>

                <div className="flex flex-col gap-3 border-t pt-5" style={{ borderColor: "var(--rule)" }}>
                  <h3 className="m-0 text-[16px] font-extrabold" style={{ fontFamily: display }}>Colleges offering {course.label}</h3>
                  {colleges.length === 0 ? (
                    <p className="m-0 text-[15px]" style={{ color: "var(--muted)" }}>None on file yet.</p>
                  ) : (
                    <>
                      <ul className="m-0 grid list-none gap-2 p-0 sm:grid-cols-2">
                        {colleges.slice(0, 6).map((c) => (
                          <li key={c.collegeName} className="rounded-xl px-4 py-3" style={{ background: "var(--surface)" }}>
                            <span className="block text-[15px] leading-snug font-semibold">{c.collegeName}</span>
                            {c.ownership && <span className="mt-0.5 block text-[13px]" style={{ color: "var(--muted)" }}>{c.ownership}</span>}
                          </li>
                        ))}
                      </ul>
                      <p className="m-0 text-[13px] leading-relaxed" style={{ color: "var(--muted)" }}>
                        {colleges.length > 6 && `+${colleges.length - 6} more on file. `}
                        {colleges.some((c) => c.tier.dataTier !== "tier_1_official") &&
                          "This list is still being checked against official counselling records."}
                      </p>
                    </>
                  )}
                </div>

                <div className="flex flex-col gap-2 rounded-2xl px-4 py-4" style={{ background: "var(--surface)" }}>
                  <h3 className="m-0 text-[15px] font-extrabold" style={{ fontFamily: display }}>Which college can I get into?</h3>
                  <p className="m-0 text-[14px] leading-relaxed" style={{ color: soft }}>
                    Not on Perry yet, and we won’t guess. Check {OFFICIAL_SOURCES} for last year’s closing ranks.
                  </p>
                </div>
              </article>
            );
          })
        )}
      </section>
    );
  } else if (mode === "pick" || (mode === "quiz" && suggested.length > 0)) {
    const list = mode === "pick" ? careers : suggested.map((id) => byId.get(id)!).filter(Boolean);
    body = (
      <section className="flex flex-col gap-4" aria-labelledby="pick-h">
        {mode === "quiz" && ai("AI-assisted · a few directions to explore, not a verdict")}
        <h2 id="pick-h" className="m-0 text-xl font-extrabold lg:text-2xl" style={{ fontFamily: display }}>
          {mode === "pick" ? "Which career are you aiming for?" : "You could look at"}
        </h2>
        <ul className="m-0 grid list-none gap-2 p-0 sm:grid-cols-2 lg:grid-cols-3">
          {list.map((c) => (
            <li key={c.id}>
              <button
                onClick={() => setCareerId(c.id)}
                className="metro-row flex h-full w-full cursor-pointer items-start gap-3 rounded-2xl px-4 py-3.5 text-left"
                style={{ background: "var(--surface)", color: "var(--ink)", border: 0, fontFamily: "inherit" }}
              >
                <span className="mt-1.5 h-3 w-3 shrink-0 rounded-full" style={{ background: lineColor(c) }} />
                <span className="flex min-w-0 flex-col gap-0.5">
                  <span className="text-[16px] leading-snug font-bold">{c.label}</span>
                  {c.sub && <span className="line-clamp-2 text-[13px] leading-snug" style={{ color: "var(--muted)" }}>{forStudents(c.sub)}</span>}
                </span>
              </button>
            </li>
          ))}
        </ul>
        <button onClick={startOver} className={`${quiet} self-start`} style={{ color: "var(--muted)", fontFamily: "inherit" }}>‹ Start over</button>
      </section>
    );
  } else if (mode === "quiz") {
    const done = ADVISORY_QUIZ.every((q) => answers[q.id]);
    body = (
      <section className="flex flex-col gap-7" aria-label="Questions">
        {ai("AI-assisted · advisory only")}
        {ADVISORY_QUIZ.map((q, i) => (
          <div key={q.id} role="group" aria-labelledby={`q-${q.id}`} className="flex flex-col gap-3">
            <h2 id={`q-${q.id}`} className="m-0 text-[18px] font-extrabold lg:text-xl" style={{ fontFamily: display }}>
              <span style={{ color: "var(--muted)" }}>{i + 1}.</span> {q.prompt}
            </h2>
            <div className="flex flex-wrap gap-2">
              {q.options.map((opt) => {
                const on = answers[q.id] === opt.id;
                return (
                  <button
                    key={opt.id}
                    onClick={() => setAnswers((a) => ({ ...a, [q.id]: opt.id }))}
                    aria-pressed={on}
                    className="metro-chip min-h-11 cursor-pointer rounded-full px-4 py-2 text-left text-[15px] font-semibold"
                    style={{
                      background: on ? "var(--ink)" : "transparent", color: on ? "var(--bg)" : "var(--ink)",
                      border: `1px solid ${on ? "var(--ink)" : "var(--line)"}`, fontFamily: "inherit",
                    }}
                  >
                    {opt.label}
                  </button>
                );
              })}
            </div>
          </div>
        ))}
        <div className="flex items-center gap-5">
          <button
            disabled={!done}
            onClick={() => setSuggested(scoreQuiz(answers, ADVISORY_QUIZ).filter((id) => byId.has(id)))}
            className="btn cursor-pointer border-0 disabled:cursor-not-allowed disabled:opacity-40"
            style={{ fontFamily: "inherit" }}
          >
            See suggestions
          </button>
          <button onClick={startOver} className={quiet} style={{ color: "var(--muted)", fontFamily: "inherit" }}>Start over</button>
        </div>
      </section>
    );
  } else {
    const choices = [
      { id: "pick" as const, title: "I know what I’m aiming for", text: "Pick a career. See the exams, course and colleges on the way.", color: "#2563eb" },
      { id: "quiz" as const, title: "Help me figure it out", text: "Answer three quick questions. Get a few careers to explore.", color: "#7c3aed" },
    ];
    const popular = POPULAR.flatMap((re) => careers.find((c) => re.test(c.label)) ?? []);
    body = (
      <div className="flex flex-col gap-12">
      <div className="grid gap-3 sm:grid-cols-2">
        {choices.map((c) => (
          <button
            key={c.id}
            onClick={() => setMode(c.id)}
            className="metro-step flex min-h-[148px] cursor-pointer flex-col items-start gap-3 rounded-xl border-0 p-5 text-left"
            style={{ background: "var(--panel)", boxShadow: "inset 0 0 0 1px var(--line)", color: "var(--ink)", fontFamily: "inherit" }}
          >
            <span className="grid h-10 w-10 place-items-center rounded-lg" style={{ background: "var(--accent-soft)", color: "var(--accent)" }}><Icon name={c.id === "pick" ? "map" : "compass"} size={20} /></span>
            <span className="text-[18px] leading-tight font-semibold">{c.title}</span>
            <span className="text-[15px] leading-snug" style={{ color: "var(--muted)" }}>{c.text}</span>
            <span className="mt-auto flex items-center gap-1 text-[14px] font-semibold" style={{ color: "var(--accent)" }}>Start <Icon name="arrowRight" size={15} /></span>
          </button>
        ))}
      </div>
      {popular.length > 0 && (
        <section aria-labelledby="popular-h" className="flex flex-col gap-4">
          <h2 id="popular-h" className="m-0 text-[18px] font-bold">Or jump straight to a career</h2>
          <ul className="m-0 flex list-none flex-wrap gap-2 p-0">
            {popular.map((c) => (
              <li key={c.id}>
                <button
                  onClick={() => setCareerId(c.id)}
                  className="metro-chip inline-flex min-h-11 cursor-pointer items-center gap-2 rounded-lg border-0 px-4 text-[15px] font-medium"
                  style={{ background: "var(--panel)", boxShadow: "inset 0 0 0 1px var(--line)", color: "var(--ink)", fontFamily: "inherit" }}
                >
                  <span aria-hidden className="h-3 w-3 rounded-full" style={{ background: lineColor(c) }} />
                  {c.label.replace(/\s*\([^)]*\)\s*$/, "")}
                </button>
              </li>
            ))}
          </ul>
        </section>
      )}
      </div>
    );
  }

  return (
    <div className="metro min-h-[calc(100vh-var(--nav-h))]" style={rootStyle}>
      <PageHead title="Find my path">
        Know the career you want? See the route to it. Not sure yet? Answer three questions.
      </PageHead>
      <div className="mx-auto flex max-w-[1100px] flex-col gap-9 px-5 pt-9 pb-16 lg:px-12">
        {body}
      </div>
    </div>
  );
}
