"use client";

import { useEffect, useMemo, useRef, useState, type CSSProperties, type ReactNode } from "react";
import "./metro-flow.css";
import type { Exam } from "@/lib/exams-db";
import { Fold, Highlight, ICON, PointList, PointSection, SubjectList } from "./fact-points";
import PageHead from "./page-head";
import Icon from "./icon";
import { applicationStatus } from "@/lib/exam-status";

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
const SCOPE_COLOR: Record<string, string> = { National: "#475569", "Andhra Pradesh": "#2563eb", Telangana: "#b45309" };
const KIND: Record<string, string> = {
  qualifying_marks: "Qualifying marks",
  qualifying_percentile: "Qualifying percentile",
  cutoff_score: "Cutoff",
  eligibility_marks: "Minimum marks to apply",
  seat_reservation: "Seat reservation",
};
const PER_STAGE = 6; // exams shown per stage before "Show all"
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
  const [openStages, setOpenStages] = useState<Set<string>>(new Set());
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

  const rootStyle = { "--metro-body": bodyFont, "--metro-display": displayFont, fontFamily: bodyFont } as CSSProperties;

  const chip = (on: boolean): CSSProperties => ({
    background: on ? "var(--chip-on)" : "var(--panel)", color: on ? "var(--chip-on-ink)" : "var(--soft)", fontFamily: "inherit",
    boxShadow: on ? "none" : "inset 0 0 0 1px var(--line)",
  });

  const filters = (
    <div className="flex flex-col gap-3">
      <div className="flex flex-wrap items-center gap-x-4 gap-y-2">
        <div role="group" aria-label="State" className="flex gap-1">
          {STATE_TABS.map((t) => (
            <button key={t.id} onClick={() => setState(t.id)} aria-pressed={state === t.id}
              className="metro-chip h-10 cursor-pointer rounded-lg border-0 px-3.5 text-[14px] font-medium" style={chip(state === t.id)}>
              {t.short ? <><span className="sm:hidden">{t.short}</span><span className="hidden sm:inline">{t.label}</span></> : t.label}
            </button>
          ))}
        </div>
                <div role="group" aria-label="Government or private" className="flex flex-wrap gap-1">
          {TYPES.map((t) => (
            <button key={t.id} onClick={() => setType(t.id)} aria-pressed={type === t.id}
              className="metro-chip h-10 cursor-pointer rounded-lg border-0 px-3.5 text-[14px] font-medium" style={chip(type === t.id)}>
              {t.label}
            </button>
          ))}
        </div>
        <div className="relative min-w-0 flex-[1_1_240px] lg:max-w-[360px]">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--muted)" strokeWidth="2" strokeLinecap="round" aria-hidden className="pointer-events-none absolute top-3 left-3.5">
            <circle cx="11" cy="11" r="7" /><path d="M20 20l-3.5-3.5" />
          </svg>
          <input
            type="search" value={query} onChange={(e) => setQuery(e.target.value)}
            placeholder="Search exams (e.g. NEET, police, Navodaya)" aria-label="Search exams"
            className="c10-search h-10 w-full rounded-lg pr-4 pl-10 text-[15px]"
            style={{ border: "1px solid var(--line)", background: "var(--panel)", color: "var(--ink)", font: "inherit" }}
          />
        </div>
      </div>
      <div role="group" aria-label="Stage" className="metro-fade-x -mx-1 flex gap-1 overflow-x-auto pb-1">
        <button onClick={() => setStage(null)} aria-pressed={!stage}
          className="metro-chip h-10 shrink-0 cursor-pointer rounded-lg border-0 px-3.5 text-[14px] font-medium" style={chip(!stage)}>
          All stages
        </button>
        {STAGES.map((s) => (
          <button key={s.id} onClick={() => setStage(stage === s.id ? null : s.id)} aria-pressed={stage === s.id}
            className="metro-chip h-10 shrink-0 cursor-pointer rounded-lg border-0 px-3.5 text-[14px] font-medium" style={chip(stage === s.id)}>
            {s.label}
          </button>
        ))}
      </div>
    </div>
  );

  // Each stage shows its first few exams; "Show all" opens the rest. A
  // chosen stage or a search shows everything that matches.
  const showAll = !!stage || !!query.trim();
  const list = (
    <div className="flex flex-col gap-8">
      {groups.length === 0 && (
        <p className="m-0 text-[17px]" style={{ color: "var(--muted)" }}>No exams match. Try another word or clear a filter.</p>
      )}
      {groups.map((g) => {
        const all = showAll || openStages.has(g.stage.id);
        let left = all ? Infinity : PER_STAGE;
        const cats = g.cats.map((c) => {
          const take = c.exams.slice(0, Math.max(0, left));
          left -= take.length;
          return { ...c, exams: take };
        }).filter((c) => c.exams.length);
        return (
          <section key={g.stage.id} aria-labelledby={`stage-${g.stage.id}`} className="flex flex-col gap-3">
            <h2 id={`stage-${g.stage.id}`} className="m-0 flex items-baseline gap-2 text-[18px] font-bold">
              {g.stage.label}
              <span className="text-[14px] font-medium" style={{ color: "var(--muted)" }}>{g.count} exams</span>
            </h2>
            <div className="overflow-hidden rounded-xl" style={{ background: "var(--panel)", boxShadow: "inset 0 0 0 1px var(--line)" }}>
              {cats.map((c, ci) => (
                <div key={c.name} className="flex flex-col" style={{ borderTop: ci ? "1px solid var(--line)" : undefined }}>
                  <h3 className="m-0 px-4 pt-3 pb-1 text-[12px] font-semibold tracking-wide uppercase" style={{ color: "var(--muted)" }}>{c.name}</h3>
                  {c.exams.map((e) => {
                    const on = e.id === selected?.id;
                    const st = e.verified ? applicationStatus(e.rows.find(([k]) => k === "Applications")?.[1]) : null;
                    return (
                      <button
                        key={e.id}
                        onClick={() => choose(e.id)}
                        aria-pressed={on}
                        className="metro-row relative flex min-h-14 cursor-pointer items-center gap-3 border-0 px-4 py-2.5 text-left"
                        style={{ background: on ? "var(--accent-soft)" : "transparent", color: "var(--ink)", fontFamily: "inherit" }}
                      >
                        {on && <span aria-hidden className="absolute inset-y-0 left-0 w-[3px]" style={{ background: "var(--accent)" }} />}
                        <span className="flex min-w-0 flex-1 flex-col gap-0.5">
                          <span className="text-[15px] leading-snug font-semibold">{e.name}</span>
                          <span className="flex items-center gap-1.5 text-[13px]" style={{ color: "var(--muted)" }}>
                            <span aria-hidden className="h-2 w-2 rounded-full" style={{ background: SCOPE_COLOR[e.scope] ?? "var(--muted)" }} />
                            {e.scope === "National" ? "All-India" : e.scope}
                            {e.bodyType ? ` · ${e.bodyType}` : ""}
                          </span>
                        </span>
                        {st ? (
                          <span className={`pill shrink-0 ${st.kind === "open" ? "pill-open" : st.kind === "soon" ? "pill-soon" : "pill-na"}`}>
                            {st.kind === "open" ? "Applications open" : st.kind === "soon" ? st.label : "Not announced"}
                          </span>
                        ) : (
                          <span className="shrink-0 text-[13px]" style={{ color: "var(--muted)" }}>Details soon</span>
                        )}
                      </button>
                    );
                  })}
                </div>
              ))}
              {!all && g.count > PER_STAGE && (
                <button
                  onClick={() => setOpenStages((s) => new Set(s).add(g.stage.id))}
                  className="metro-row flex min-h-12 w-full cursor-pointer items-center justify-center gap-1.5 border-0 text-[14px] font-semibold"
                  style={{ background: "var(--bg)", color: "var(--accent)", borderTop: "1px solid var(--line)", fontFamily: "inherit" }}
                >
                  Show all {g.count} {g.stage.label.toLowerCase().startsWith("government") ? "job exams" : "exams"}
                  <Icon name="chevronDown" size={16} />
                </button>
              )}
            </div>
          </section>
        );
      })}
    </div>
  );

  return (
    <div className="metro min-h-[calc(100vh-var(--nav-h))]" style={rootStyle}>
      <PageHead title="Exams" width={1280}>
        {exams.length} exams, from Class 6 entrance tests to government jobs. Tap one to see its dates.
      </PageHead>
      <div className="mx-auto flex max-w-[1280px] flex-col gap-6 px-4 pt-6 pb-16 sm:px-6 lg:px-8">
        {filters}
        <div className="grid items-start gap-10 lg:grid-cols-[minmax(0,440px)_minmax(0,1fr)] xl:grid-cols-[minmax(0,480px)_minmax(0,1fr)]">
          {list}
          {selected && (
            <section
              ref={panelRef}
              aria-label={`${selected.name} details`}
              className="sticky hidden max-h-[calc(100vh-var(--nav-h)-48px)] flex-col gap-7 overflow-y-auto rounded-xl p-8 lg:flex metro-scroll"
              style={{ background: "var(--panel)", boxShadow: "inset 0 0 0 1px var(--line)", top: "calc(var(--nav-h) + 24px)" }}
            >
              <ExamDetails key={selected.id} exam={selected} />
            </section>
          )}
        </div>
        <p className="m-0 text-[15px] leading-relaxed" style={{ color: "var(--muted)" }}>
          Always check the current official notification before applying.
        </p>
      </div>

      {sheetOpen && selected && (
        <div className="fixed inset-0 z-[120] lg:hidden">
          <button aria-label="Close details" onClick={() => setSheetOpen(false)} className="absolute inset-0 cursor-default border-0" style={{ background: "rgba(14,24,34,0.55)" }} />
          <section
            role="dialog" aria-modal="true" aria-label={`${selected.name} details`}
            className="metro-sheet absolute inset-x-0 bottom-0 flex max-h-[88vh] flex-col overflow-auto rounded-t-3xl"
            style={{ background: "var(--bg)", paddingBottom: "env(safe-area-inset-bottom)" }}
          >
            <div className="flex justify-center pt-2.5"><span className="h-1.5 w-11 rounded-full" style={{ background: "var(--line)" }} /></div>
            <div className="flex flex-col gap-6 px-6 pt-4 pb-8">
              <ExamDetails key={selected.id} exam={selected} onClose={() => setSheetOpen(false)} />
            </div>
          </section>
        </div>
      )}
    </div>
  );
}

// The order a student asks in: when, can I, where does it lead.
const KEY_ORDER = ["Exam dates", "Applications", "Who can take it", "Leads to"];

function ExamDetails({ exam, onClose }: { exam: Exam; onClose?: () => void }) {
  const color = SCOPE_COLOR[exam.scope] ?? "var(--accent)";
  const years = [...new Set(exam.cutoffs.map((c) => c.year))];
  const rows = [...exam.rows].sort((a, b) => (KEY_ORDER.indexOf(a[0]) + 99) % 99 - (KEY_ORDER.indexOf(b[0]) + 99) % 99);
  const site = exam.website && (
    <a href={`https://${exam.website}`} target="_blank" rel="noreferrer" className="inline-flex items-center gap-1.5 self-start text-[14px] font-semibold no-underline hover:underline" style={{ color: "var(--ok)", overflowWrap: "anywhere" }}>
      <Icon name="shieldCheck" size={16} /> Official website: {exam.website} <Icon name="external" size={13} />
    </a>
  );

  return (
    <>
      <div className="flex flex-col gap-3">
        <div className="flex items-start gap-3">
          <div className="flex flex-1 flex-col gap-1.5">
            <h2 className="m-0 text-[24px] leading-tight font-bold tracking-tight lg:text-[28px]">{exam.name}</h2>
            <span className="text-[14px]" style={{ color: "var(--muted)" }}>
              {[exam.scope === "National" ? "All-India" : exam.scope, exam.category, exam.bodyType].filter(Boolean).join(" · ")}
            </span>
          </div>
          {onClose && (
            <button onClick={onClose} aria-label="Close details" className="metro-chip grid h-11 w-11 shrink-0 cursor-pointer place-items-center rounded-lg border-0" style={{ background: "var(--surface)", color: "var(--ink)" }}>
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" aria-hidden><path d="M6 6l12 12M18 6L6 18" /></svg>
            </button>
          )}
        </div>
        {exam.verified && (() => {
          const st = applicationStatus(exam.rows.find(([k]) => k === "Applications")?.[1]);
          return <span className={`pill self-start ${st.kind === "open" ? "pill-open" : st.kind === "soon" ? "pill-soon" : "pill-na"}`}>{st.label}</span>;
        })()}
        {exam.fullForm && exam.fullForm.length < 140 && <p className="m-0 text-[15px] leading-snug" style={{ color: "var(--soft)" }}>{exam.fullForm}</p>}
        {exam.body && <p className="m-0 text-[14px]" style={{ color: "var(--muted)" }}>Conducted by {exam.body}</p>}
        {site}
      </div>

      {!exam.verified ? (
        <p className="m-0 rounded-lg px-4 py-3 text-[15px] leading-relaxed" style={{ background: "var(--warn-bg)", color: "var(--warn-ink)", boxShadow: "inset 0 0 0 1px var(--warn-line)" }}>
          Dates and marks for this exam are still being checked. Use the official website until they’re added.
        </p>
      ) : (
        <>
          <div className="grid gap-x-10 gap-y-7 xl:grid-cols-2">
            {rows.map(([k, v]) => (
              <PointSection
                key={k} title={ROW_TITLE[k] ?? k} icon={ROW_ICON[k] ?? ICON.info} color={color} text={v}
                badge={(k === "Applications" || k === "Exam dates") && NOT_ANNOUNCED.test(v) ? "Not announced yet" : null}
              />
            ))}
          </div>
          <div className="flex flex-col gap-2">
            {exam.pattern && (
              <Fold title="Exam pattern">
                <PointList text={exam.pattern} color={color} full />
              </Fold>
            )}
            <Fold title="Syllabus" meta={exam.subjects.length ? `${exam.subjects.length} ${exam.subjects.length === 1 ? "subject" : "subjects"}` : "not added yet"}>
              <SubjectList subjects={exam.subjects} color={color} empty="The syllabus for this exam hasn’t been added yet." />
            </Fold>
            <Fold title="Marks by category" meta={years.length ? years.join(", ") : "not published yet"}>
              {exam.cutoffs.length ? (
                years.map((y) => (
                  <div key={y} className="flex flex-col gap-2">
                    <span className="text-[15px] font-semibold" style={{ color: "var(--muted)" }}>{y}</span>
                    <table className="w-full border-collapse text-left text-[16px]">
                      <tbody>
                        {exam.cutoffs.filter((c) => c.year === y).map((c) => (
                          <tr key={`${c.category}-${c.kind}`} style={{ borderBottom: "1px solid var(--rule)" }}>
                            <th scope="row" className="py-2 pr-4 font-semibold">{c.category}</th>
                            <td className="py-2 pr-4" style={{ color: "var(--soft)" }}>
                              <Highlight text={c.value} />
                              {c.note && <span className="block text-[14px]" style={{ color: "var(--muted)" }}>{c.note}</span>}
                            </td>
                            <td className="py-2 text-right text-[14px]" style={{ color: "var(--muted)" }}>{KIND[c.kind] ?? c.kind}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                ))
              ) : (
                <p className="m-0 text-[16px]" style={{ color: "var(--muted)" }}>Category-wise marks for this exam haven’t been published or added yet.</p>
              )}
            </Fold>
          </div>
          {exam.source && (
            <p className="m-0 text-[13px] leading-relaxed" style={{ color: "var(--muted)", overflowWrap: "anywhere" }}>Source: {exam.source}</p>
          )}
        </>
      )}
    </>
  );
}
