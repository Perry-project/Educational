"use client";

import { useEffect, useMemo, useRef, useState, type CSSProperties, type ReactNode } from "react";
import "./metro-flow.css";
import type { Exam } from "@/lib/exams-db";
import { Highlight, ICON, PointList, PointSection } from "./fact-points";

// The /exams page: every exam a student in Andhra Pradesh or Telangana may
// sit, from Class 1-10 scholarship and admission tests to government job
// exams. Filters across the top (state, stage, government / private, a
// search box); the list grouped by stage and field on the left, and the
// chosen exam's details on the right (a bottom sheet on phones).
//
// The URL keeps ?exam=, ?state=, ?stage= and ?type= so a view can be shared.

const STAGES: { id: string; label: string }[] = [
  { id: "school", label: "Class 1–10" },
  { id: "after_10", label: "After Class 10" },
  { id: "after_12", label: "After Intermediate" },
  { id: "after_degree", label: "After a degree" },
  { id: "jobs", label: "Government jobs" },
];
const STATE_TABS = [
  // Phones show the short "AP & TS" so the three tabs fit on one line.
  { id: "all", label: "AP & Telangana", short: "AP & TS" },
  { id: "ap", label: "Andhra Pradesh" },
  { id: "ts", label: "Telangana" },
];
const TYPES = [
  { id: "all", label: "All" },
  { id: "Government", label: "Government" },
  { id: "Private", label: "Private" },
];
const SCOPE_COLOR: Record<string, string> = { National: "#a9b4ff", "Andhra Pradesh": "#5b9cf0", Telangana: "#f0b44c" };
const KIND: Record<string, string> = {
  qualifying_marks: "Qualifying marks",
  qualifying_percentile: "Qualifying percentile",
  cutoff_score: "Cutoff",
  eligibility_marks: "Minimum marks to apply",
  seat_reservation: "Seat reservation",
};
const display = "var(--metro-display), var(--metro-body), system-ui, sans-serif";
const NOT_ANNOUNCED = /not yet (?:announced|released|open|notified)|not announced/i;
const ROW_TITLE: Record<string, string> = {
  "Who can take it": "Who can take it", "Applications": "When to apply", "Exam dates": "Exam dates", "Leads to": "Gets you into",
};
const ROW_ICON: Record<string, ReactNode> = {
  "Who can take it": ICON.person, "Applications": ICON.calendar, "Exam dates": ICON.calendar, "Leads to": ICON.arrow,
};

export type ExamsView = { exam: string | null; state: string | null; stage: string | null; type: string | null };

export default function ExamsBrowser({
  exams, initial, bodyFont, displayFont,
}: {
  exams: Exam[];
  initial: ExamsView;
  bodyFont: string;
  displayFont: string;
}) {
  const [state, setState] = useState(STATE_TABS.some((t) => t.id === initial.state) ? initial.state! : "all");
  const [stage, setStage] = useState<string | null>(STAGES.some((s) => s.id === initial.stage) ? initial.stage : null);
  const [type, setType] = useState(TYPES.some((t) => t.id === initial.type) ? initial.type! : "all");
  const [query, setQuery] = useState("");
  const [selectedId, setSelectedId] = useState<number | null>(initial.exam ? Number(initial.exam) || null : null);
  const [sheetOpen, setSheetOpen] = useState(false);
  const panelRef = useRef<HTMLElement>(null);

  // National exams show under either state.
  const shown = useMemo(() => {
    const q = query.trim().toLowerCase();
    return exams.filter((e) =>
      (state === "all" || e.scope === "National" || e.scope === (state === "ap" ? "Andhra Pradesh" : "Telangana")) &&
      (!stage || e.stage === stage) &&
      (type === "all" || e.bodyType === type) &&
      (!q || [e.name, e.fullForm, e.body, e.category].some((t) => t?.toLowerCase().includes(q))),
    );
  }, [exams, state, stage, type, query]);

  // Grouped by stage, then by field, verified exams first within a field.
  const groups = useMemo(() => STAGES.flatMap((st) => {
    const inStage = shown.filter((e) => e.stage === st.id);
    if (!inStage.length) return [];
    const cats = [...new Set(inStage.map((e) => e.category))].sort();
    return [{
      stage: st,
      count: inStage.length,
      cats: cats.map((c) => ({
        name: c,
        exams: inStage.filter((e) => e.category === c).sort((a, b) => Number(b.verified) - Number(a.verified) || a.name.localeCompare(b.name)),
      })),
    }];
  }), [shown]);

  const selected = shown.find((e) => e.id === selectedId) ?? groups[0]?.cats[0]?.exams[0] ?? null;

  useEffect(() => {
    const url = new URL(window.location.href);
    const set = (k: string, v: string | null) => (v ? url.searchParams.set(k, v) : url.searchParams.delete(k));
    set("exam", selectedId ? String(selectedId) : null);
    set("state", state === "all" ? null : state);
    set("stage", stage);
    set("type", type === "all" ? null : type);
    window.history.replaceState(window.history.state, "", url);
  }, [selectedId, state, stage, type]);

  // A shared ?exam= link opens that exam's details sheet on phones (desktop
  // shows the details panel anyway).
  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    if (initial.exam && !window.matchMedia("(min-width: 1024px)").matches) setSheetOpen(true);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    if (!sheetOpen) return;
    const onKey = (e: KeyboardEvent) => e.key === "Escape" && setSheetOpen(false);
    window.addEventListener("keydown", onKey);
    const prev = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    return () => { window.removeEventListener("keydown", onKey); document.body.style.overflow = prev; };
  }, [sheetOpen]);

  const choose = (id: number) => {
    setSelectedId(id);
    if (window.matchMedia("(min-width: 1024px)").matches) {
      const top = panelRef.current?.getBoundingClientRect().top;
      if (top !== undefined && top < 0) window.scrollBy({ top: top - 100 });
    } else {
      setSheetOpen(true);
    }
  };

  const verifiedCount = exams.filter((e) => e.verified).length;
  const rootStyle = { "--metro-body": bodyFont, "--metro-display": displayFont, fontFamily: bodyFont } as CSSProperties;

  const chip = (on: boolean): CSSProperties => ({
    background: on ? "var(--surface)" : "transparent", color: on ? "var(--ink)" : "var(--muted)", fontFamily: "inherit",
  });

  const filters = (
    <div className="flex flex-col gap-3">
      <div className="flex flex-wrap items-center gap-x-4 gap-y-2">
        <div role="group" aria-label="State" className="flex gap-1">
          {STATE_TABS.map((t) => (
            <button key={t.id} onClick={() => setState(t.id)} aria-pressed={state === t.id}
              className="metro-chip h-11 cursor-pointer rounded-full border-0 px-4 text-sm font-semibold" style={chip(state === t.id)}>
              {t.short ? <><span className="sm:hidden">{t.short}</span><span className="hidden sm:inline">{t.label}</span></> : t.label}
            </button>
          ))}
        </div>
        <span aria-hidden className="hidden h-6 w-px sm:block" style={{ background: "var(--line)" }} />
        <div role="group" aria-label="Government or private" className="flex flex-wrap gap-1">
          {TYPES.map((t) => (
            <button key={t.id} onClick={() => setType(t.id)} aria-pressed={type === t.id}
              className="metro-chip h-11 cursor-pointer rounded-full border-0 px-4 text-sm font-semibold" style={chip(type === t.id)}>
              {t.label}
            </button>
          ))}
        </div>
        <div className="relative min-w-0 flex-[1_1_240px] lg:max-w-[360px]">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--muted)" strokeWidth="2" strokeLinecap="round" aria-hidden className="pointer-events-none absolute top-3.5 left-3.5">
            <circle cx="11" cy="11" r="7" /><path d="M20 20l-3.5-3.5" />
          </svg>
          <input
            type="search" value={query} onChange={(e) => setQuery(e.target.value)}
            placeholder="Search exams (e.g. NEET, police, Navodaya)" aria-label="Search exams"
            className="c10-search h-11 w-full rounded-full pr-4 pl-10 text-sm"
            style={{ border: "1px solid var(--line)", background: "var(--surface)", color: "var(--ink)", font: "inherit" }}
          />
        </div>
      </div>
      <div role="group" aria-label="Stage" className="metro-fade-x -mx-1 flex gap-1 overflow-x-auto pb-1">
        <button onClick={() => setStage(null)} aria-pressed={!stage}
          className="metro-chip h-10 shrink-0 cursor-pointer rounded-full border-0 px-4 text-sm font-semibold" style={chip(!stage)}>
          All stages
        </button>
        {STAGES.map((s) => (
          <button key={s.id} onClick={() => setStage(stage === s.id ? null : s.id)} aria-pressed={stage === s.id}
            className="metro-chip h-10 shrink-0 cursor-pointer rounded-full border-0 px-4 text-sm font-semibold" style={chip(stage === s.id)}>
            {s.label}
          </button>
        ))}
      </div>
    </div>
  );

  const list = (
    <div className="flex flex-col gap-8">
      {groups.length === 0 && (
        <p className="m-0 text-[15px]" style={{ color: "var(--muted)" }}>No exams match. Try another word or clear a filter.</p>
      )}
      {groups.map((g) => (
        <section key={g.stage.id} className="flex flex-col gap-4">
          <h2 className="m-0 flex items-baseline gap-2 text-xl font-extrabold" style={{ fontFamily: display }}>
            {g.stage.label}
            <span className="text-sm font-semibold" style={{ color: "var(--muted)" }}>{g.count}</span>
          </h2>
          {g.cats.map((c) => (
            <div key={c.name} className="flex flex-col gap-1">
              <h3 className="m-0 px-3 text-xs font-bold tracking-widest uppercase" style={{ color: "var(--muted)" }}>{c.name}</h3>
              {c.exams.map((e) => {
                const on = e.id === selected?.id;
                return (
                  <button
                    key={e.id}
                    onClick={() => choose(e.id)}
                    aria-pressed={on}
                    className="metro-row flex cursor-pointer items-start gap-3 rounded-xl border-0 px-3 py-2.5 text-left"
                    style={{ background: on ? "var(--surface)" : "transparent", color: "var(--ink)", fontFamily: "inherit" }}
                  >
                    <span className="mt-1.5 h-2.5 w-2.5 shrink-0 rounded-full" style={{ background: SCOPE_COLOR[e.scope] ?? "var(--muted)" }} />
                    <span className="flex min-w-0 flex-1 flex-col gap-0.5">
                      <span className="text-[16px] font-bold">{e.name}</span>
                      <span className="text-[13px] leading-snug" style={{ color: "var(--muted)" }}>
                        {[e.scope === "National" ? "All-India" : e.scope, e.bodyType, e.body].filter(Boolean).join(" · ")}
                      </span>
                    </span>
                    {!e.verified && (
                      <span className="mt-0.5 shrink-0 text-[12px] font-semibold" style={{ color: "var(--muted)" }}>Details soon</span>
                    )}
                  </button>
                );
              })}
            </div>
          ))}
        </section>
      ))}
    </div>
  );

  return (
    <div className="metro min-h-[calc(100vh-var(--nav-h))]" style={rootStyle}>
      <div className="mx-auto flex max-w-[1440px] flex-col gap-8 px-5 pt-8 pb-16 lg:px-12">
        <header className="flex flex-col gap-3">
          <h1 className="m-0 text-[34px] leading-[1.08] font-extrabold tracking-tight lg:text-[44px]" style={{ fontFamily: display }}>Exams</h1>
          <p className="m-0 max-w-2xl text-base leading-relaxed lg:text-lg" style={{ color: "var(--muted)" }}>
            Every exam from Class 1 to a government job, for Andhra Pradesh and Telangana students. {exams.length} exams so far, {verifiedCount} with full details.
          </p>
        </header>
        {filters}
        <div className="grid items-start gap-10 lg:grid-cols-[minmax(0,440px)_minmax(0,1fr)] xl:grid-cols-[minmax(0,480px)_minmax(0,1fr)]">
          {list}
          {selected && (
            <section
              ref={panelRef}
              aria-label={`${selected.name} details`}
              className="sticky hidden max-h-[calc(100vh-var(--nav-h)-48px)] flex-col gap-7 overflow-y-auto rounded-[28px] px-10 py-9 lg:flex metro-scroll"
              style={{ background: "var(--panel)", top: "calc(var(--nav-h) + 24px)" }}
            >
              <ExamDetails key={selected.id} exam={selected} />
            </section>
          )}
        </div>
        <p className="m-0 text-[13px] leading-relaxed" style={{ color: "var(--muted)" }}>
          Dates and marks are from each exam’s most recent official notification. Always check the current notification before applying.
        </p>
      </div>

      {sheetOpen && selected && (
        <div className="fixed inset-0 z-[120] lg:hidden">
          <button aria-label="Close details" onClick={() => setSheetOpen(false)} className="absolute inset-0 cursor-default border-0" style={{ background: "rgba(5,8,15,0.6)" }} />
          <section
            role="dialog" aria-modal="true" aria-label={`${selected.name} details`}
            className="metro-sheet absolute inset-x-0 bottom-0 flex max-h-[88vh] flex-col overflow-auto rounded-t-3xl"
            style={{ background: "#121829", paddingBottom: "env(safe-area-inset-bottom)" }}
          >
            <div className="flex justify-center pt-2.5"><span className="h-1.5 w-11 rounded-full" style={{ background: "#2f384d" }} /></div>
            <div className="flex flex-col gap-6 px-6 pt-4 pb-8">
              <ExamDetails key={selected.id} exam={selected} onClose={() => setSheetOpen(false)} />
            </div>
          </section>
        </div>
      )}
    </div>
  );
}

function ExamDetails({ exam, onClose }: { exam: Exam; onClose?: () => void }) {
  const color = SCOPE_COLOR[exam.scope] ?? "var(--accent)";
  const years = [...new Set(exam.cutoffs.map((c) => c.year))];
  const site = exam.website && (
    <a href={`https://${exam.website}`} target="_blank" rel="noreferrer" className="inline-flex items-center gap-1.5 self-start text-[15px] font-semibold no-underline" style={{ color: "var(--accent)", overflowWrap: "anywhere" }}>
      {exam.website}
      <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round" aria-hidden><path d="M7 17L17 7M9 7h8v8" /></svg>
    </a>
  );

  return (
    <>
      <div className="flex flex-col gap-3">
        <div className="flex items-start gap-3">
          <div className="flex flex-1 flex-col gap-1.5">
            <span className="text-xs font-bold tracking-widest uppercase" style={{ color: "var(--muted)" }}>
              {[exam.scope === "National" ? "All-India" : exam.scope, exam.category].join(" · ")}
            </span>
            <h2 className="m-0 text-[26px] leading-tight font-extrabold lg:text-[32px]" style={{ fontFamily: display }}>{exam.name}</h2>
          </div>
          {onClose && (
            <button onClick={onClose} aria-label="Close details" className="grid h-11 w-11 shrink-0 cursor-pointer place-items-center rounded-full bg-transparent" style={{ border: "1px solid var(--line)", color: "var(--ink)" }}>
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" aria-hidden><path d="M6 6l12 12M18 6L6 18" /></svg>
            </button>
          )}
        </div>
        {exam.fullForm && <p className="m-0 text-base leading-relaxed" style={{ color: "#c9d0dc" }}>{exam.fullForm}</p>}
        <dl className="m-0 grid gap-x-8 gap-y-1 text-[15px] sm:grid-cols-2">
          {exam.body && (<div className="flex flex-col gap-0.5 py-1"><dt className="text-sm font-bold">Conducted by</dt><dd className="m-0" style={{ color: "#c9d0dc" }}>{exam.body}</dd></div>)}
          {exam.bodyType && (<div className="flex flex-col gap-0.5 py-1"><dt className="text-sm font-bold">Type</dt><dd className="m-0" style={{ color: "#c9d0dc" }}>{exam.bodyType}</dd></div>)}
        </dl>
        {site}
      </div>

      {!exam.verified ? (
        <p className="m-0 rounded-xl px-4 py-3 text-[15px] leading-relaxed" style={{ background: "#1a2133", color: "#c9d0dc" }}>
          We’re still checking this exam’s dates, syllabus and cutoff marks against its official notification. Until they’re added, use the official website above.
        </p>
      ) : (
        <>
          <div className="grid gap-x-10 gap-y-7 xl:grid-cols-2">
            {exam.rows.map(([k, v]) => (
              <PointSection
                key={k} title={ROW_TITLE[k] ?? k} icon={ROW_ICON[k] ?? ICON.info} color={color} text={v}
                badge={(k === "Applications" || k === "Exam dates") && NOT_ANNOUNCED.test(v) ? "Next dates not announced" : null}
              />
            ))}
          </div>
          {exam.pattern && <PointSection title="Exam pattern" icon={ICON.chart} color={color} text={exam.pattern} />}
          <PointSection title="Subjects & topics" icon={ICON.book} color={color}>
            {exam.subjects.length ? (
              <div className="flex flex-col gap-4">
                {exam.subjects.map((sub) => (
                  <div key={sub.subject} className="flex flex-col gap-2 rounded-2xl px-4 py-3.5" style={{ background: "var(--surface)" }}>
                    <span className="text-[15px] font-bold">{sub.subject}</span>
                    {sub.topics && <PointList text={sub.topics} color={color} limit={3} />}
                  </div>
                ))}
              </div>
            ) : (
              <p className="m-0 text-sm" style={{ color: "var(--muted)" }}>The syllabus for this exam hasn’t been added yet.</p>
            )}
          </PointSection>
          <PointSection title="Marks by category" icon={ICON.list} color={color}>
            {exam.cutoffs.length ? (
              years.map((y) => (
                <div key={y} className="flex flex-col gap-2">
                  <span className="text-sm font-semibold" style={{ color: "var(--muted)" }}>{y}</span>
                  <table className="w-full border-collapse text-left text-[15px]">
                    <tbody>
                      {exam.cutoffs.filter((c) => c.year === y).map((c) => (
                        <tr key={`${c.category}-${c.kind}`} style={{ borderBottom: "1px solid var(--rule)" }}>
                          <th scope="row" className="py-2 pr-4 font-semibold">{c.category}</th>
                          <td className="py-2 pr-4" style={{ color: "#c9d0dc" }}>
                            <Highlight text={c.value} />
                            {c.note && <span className="block text-[13px]" style={{ color: "var(--muted)" }}>{c.note}</span>}
                          </td>
                          <td className="py-2 text-right text-[13px]" style={{ color: "var(--muted)" }}>{KIND[c.kind] ?? c.kind}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              ))
            ) : (
              <p className="m-0 text-sm" style={{ color: "var(--muted)" }}>Category-wise marks for this exam haven’t been published or added yet.</p>
            )}
          </PointSection>
          {exam.source && (
            <p className="m-0 text-xs leading-relaxed" style={{ color: "var(--muted)", overflowWrap: "anywhere" }}>Source: {exam.source}</p>
          )}
        </>
      )}
    </>
  );
}
