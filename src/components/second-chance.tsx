"use client";

import Link from "next/link";
import { useEffect, useMemo, useState, type CSSProperties, type ReactNode } from "react";
import "./metro-flow.css";
import { ICON, PointSection } from "./fact-points";
import PageHead from "./page-head";
import Icon from "./icon";
import type { Route } from "@/lib/second-chance-db";
import { STOPS, type StopId } from "@/lib/second-chance-stops";

// The /second-chance page: official routes back into education or work for
// a student who stopped somewhere. It opens with one question, "Where did
// you stop?"; the answer shows that group's routes as stations on a line,
// in the flowchart's Metro style. A station opens in place to show who can
// use the route, how to apply, the dates and where it leads.
//
// The URL keeps ?from=, ?state= and ?route= so a view can be shared, and
// the flowchart's "If you stop here" links land on ?from=.

const LINE: Record<StopId, string> = {
  class_10: "#2563eb",
  intermediate: "#b45309",
  degree: "#0f766e",
  entrance_exam: "#c2410c",
  working: "#7c3aed",
};
const STATE_TABS = [
  // Phones show the short "AP & TS" so the three tabs fit on one line.
  { id: "all", label: "AP & Telangana", short: "AP & TS" },
  { id: "ap", label: "Andhra Pradesh" },
  { id: "ts", label: "Telangana" },
];
const ROW_TITLE: Record<string, string> = { "Who can use it": "Who can use it", "How to apply": "How to apply", "Dates": "Key dates", "Leads to": "Where it leads" };
const ROW_ICON: Record<string, ReactNode> = { "Who can use it": ICON.person, "How to apply": ICON.pen, "Dates": ICON.calendar, "Leads to": ICON.arrow };

export type SecondChanceView = { from: string | null; state: string | null; route: string | null };

export default function SecondChance({
  routes, initial, bodyFont, displayFont,
}: {
  routes: Route[];
  initial: SecondChanceView;
  bodyFont: string;
  displayFont: string;
}) {
  const initialRoute = routes.find((r) => String(r.id) === initial.route) ?? null;
  const [from, setFrom] = useState<StopId | null>(
    initialRoute?.stoppedAt ?? (STOPS.find((s) => s.id === initial.from)?.id ?? null),
  );
  const [state, setState] = useState(STATE_TABS.some((t) => t.id === initial.state) ? initial.state! : "all");
  const [openId, setOpenId] = useState<number | null>(initialRoute?.id ?? null);

  // National routes show under either state.
  const inState = (r: Route) =>
    state === "all" || r.scope === "National" || r.scope === (state === "ap" ? "Andhra Pradesh" : "Telangana");
  const shown = useMemo(
    () => routes.filter((r) => r.stoppedAt === from && inState(r)),
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [routes, from, state],
  );
  const openNow = useMemo(() => {
    const seen = new Set<string>();
    return routes.filter((r) => r.open && inState(r) && !seen.has(r.name + r.scope) && seen.add(r.name + r.scope));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [routes, state]);

  useEffect(() => {
    const url = new URL(window.location.href);
    const set = (k: string, v: string | null) => (v ? url.searchParams.set(k, v) : url.searchParams.delete(k));
    set("from", from);
    set("state", state === "all" ? null : state);
    set("route", openId ? String(openId) : null);
    window.history.replaceState(window.history.state, "", url);
  }, [from, state, openId]);

  // A shared ?route= link scrolls to its station once.
  useEffect(() => {
    if (initialRoute) document.getElementById(`route-${initialRoute.id}`)?.scrollIntoView({ block: "center" });
  }, [initialRoute]);

  // On a phone the routes appear below the fold, so bring them into view.
  const reveal = (id: string) =>
    requestAnimationFrame(() => {
      const el = document.getElementById(id);
      if (el && el.getBoundingClientRect().top > window.innerHeight * 0.6) el.scrollIntoView({ behavior: "smooth", block: "start" });
    });

  const choose = (id: StopId) => {
    setFrom(id);
    setOpenId(null);
    reveal("routes-h");
  };

  const rootStyle = { "--metro-body": bodyFont, "--metro-display": displayFont, fontFamily: bodyFont } as CSSProperties;
  const chip = (on: boolean): CSSProperties => ({
    background: on ? "var(--chip-on)" : "var(--panel)", color: on ? "var(--chip-on-ink)" : "var(--soft)", fontFamily: "inherit",
    boxShadow: on ? "none" : "inset 0 0 0 1px var(--line)",
  });
  const stop = STOPS.find((s) => s.id === from);
  const color = from ? LINE[from] : "var(--accent)";

  return (
    <div className="metro min-h-[calc(100vh-var(--nav-h))]" style={rootStyle}>
      <PageHead title="Second chance">
        Stopped studying somewhere? There’s an official way back. Start with where you stopped.
      </PageHead>
      <div className="mx-auto flex max-w-[860px] flex-col gap-8 px-4 pt-6 pb-16 sm:px-6 lg:px-8">

        <section className="flex flex-col gap-3" aria-labelledby="stop-q">
          <h2 id="stop-q" className="m-0 text-[18px] font-bold">Where did you stop?</h2>
          <div role="group" aria-labelledby="stop-q" className="overflow-hidden rounded-xl" style={{ background: "var(--panel)", boxShadow: "inset 0 0 0 1px var(--line)" }}>
            {STOPS.map((s, i) => {
              const on = s.id === from;
              return (
                <button
                  key={s.id}
                  onClick={() => choose(s.id)}
                  aria-pressed={on}
                  className="metro-row relative flex min-h-[64px] w-full cursor-pointer items-center gap-4 border-0 px-4 py-3 text-left"
                  style={{
                    background: on ? "var(--accent-soft)" : "transparent", color: "var(--ink)", fontFamily: "inherit",
                    borderTop: i ? "1px solid var(--line)" : undefined,
                  }}
                >
                  {on && <span aria-hidden className="absolute inset-y-0 left-0 w-[3px]" style={{ background: "var(--accent)" }} />}
                  <span aria-hidden className="grid h-10 w-10 shrink-0 place-items-center rounded-lg" style={{ background: on ? "var(--accent)" : "var(--surface)", color: on ? "#fff" : LINE[s.id] }}>
                    <Icon name={STOP_ICON[s.id]} size={20} />
                  </span>
                  <span className="flex min-w-0 flex-1 flex-col">
                    <span className="text-[16px] font-semibold">{s.label}</span>
                    <span className="text-[14px] leading-snug" style={{ color: "var(--muted)" }}>{s.long}</span>
                  </span>
                  <span className="shrink-0" style={{ color: on ? "var(--accent)" : "var(--muted)" }}>
                    <Icon name={on ? "check" : "chevronRight"} size={20} />
                  </span>
                </button>
              );
            })}
          </div>
          <div role="group" aria-label="State" className="flex flex-wrap gap-2">
            {STATE_TABS.map((t) => (
              <button key={t.id} onClick={() => setState(t.id)} aria-pressed={state === t.id}
                className="metro-chip h-10 cursor-pointer rounded-lg border-0 px-3.5 text-[14px] font-medium" style={chip(state === t.id)}>
                {t.short ? <><span className="sm:hidden">{t.short}</span><span className="hidden sm:inline">{t.label}</span></> : t.label}
              </button>
            ))}
          </div>
        </section>

        {!stop ? (
          openNow.length > 0 && (
            <section className="flex flex-col gap-3" aria-labelledby="open-now">
              <h2 id="open-now" className="m-0 flex items-center gap-2 text-[18px] font-bold">
                Applications open now <span className="pill pill-open">{openNow.length}</span>
              </h2>
              <ul className="m-0 flex list-none flex-col gap-2 p-0">
                {openNow.map((r) => (
                  <li key={r.id}>
                    <button
                      onClick={() => { setFrom(r.stoppedAt); setOpenId(r.id); reveal(`route-${r.id}`); }}
                      className="metro-step flex w-full cursor-pointer items-start gap-3 rounded-xl border-0 p-4 text-left"
                      style={{ background: "var(--panel)", boxShadow: "inset 0 0 0 1px var(--line)", color: "var(--ink)", fontFamily: "inherit" }}
                    >
                      <span className="flex min-w-0 flex-1 flex-col gap-1">
                        <span className="text-[15px] font-semibold">{r.name}</span>
                        <span className="line-clamp-2 text-[14px] leading-snug" style={{ color: "var(--muted)" }}>{r.rows.find(([k]) => k === "Dates")?.[1]}</span>
                      </span>
                      <span className="shrink-0 pt-0.5" style={{ color: "var(--muted)" }}><Icon name="chevronRight" size={18} /></span>
                    </button>
                  </li>
                ))}
              </ul>
            </section>
          )
        ) : (
          <section className="flex flex-col gap-4" aria-labelledby="routes-h">
            <div className="flex flex-col gap-1">
              <h2 id="routes-h" className="m-0 text-[20px] font-bold" style={{ scrollMarginTop: "calc(var(--nav-h) + 56px)" }}>
                {shown.length} {shown.length === 1 ? "way" : "ways"} back
              </h2>
              <span className="text-[14px]" style={{ color: "var(--muted)" }}>{stop.long}. Tap a route for how to apply.</span>
            </div>
            {shown.length === 0 ? (
              <p className="m-0 text-[15px]" style={{ color: "var(--muted)" }}>No routes for this state yet. Try “AP & Telangana”.</p>
            ) : (
              <ol aria-label="Routes" className="m-0 flex list-none flex-col gap-3 p-0">
                {shown.map((r) => (
                  <RouteCard key={r.id} route={r} color={color} open={openId === r.id} onToggle={() => setOpenId(openId === r.id ? null : r.id)} />
                ))}
              </ol>
            )}
          </section>
        )}

        <p className="m-0 text-[14px] leading-relaxed" style={{ color: "var(--muted)" }}>
          Always check the official website before applying.
        </p>
      </div>
    </div>
  );
}

const STOP_ICON: Record<StopId, string> = {
  class_10: "school", intermediate: "book", degree: "cap", entrance_exam: "file", working: "briefcase",
};

function RouteCard({
  route: r, color, open, onToggle,
}: {
  route: Route; color: string; open: boolean; onToggle: () => void;
}) {
  const panelId = `route-panel-${r.id}`;
  const meta = [r.scope === "National" ? "All-India" : r.scope, r.kind].filter(Boolean).join(" · ");
  return (
    <li id={`route-${r.id}`} className="overflow-hidden rounded-xl" style={{ background: "var(--panel)", boxShadow: `inset 0 0 0 ${open ? 2 : 1}px ${open ? "var(--accent)" : "var(--line)"}`, scrollMarginTop: "calc(var(--nav-h) + 16px)" }}>
      <button
        onClick={onToggle}
        aria-expanded={open}
        aria-controls={panelId}
        className="flex w-full cursor-pointer items-start gap-3 border-0 bg-transparent p-4 text-left"
        style={{ color: "var(--ink)", fontFamily: "inherit" }}
      >
        <span className="flex min-w-0 flex-1 flex-col gap-1.5">
          <span className="flex flex-wrap items-center gap-x-2 gap-y-1">
            <span className="text-[16px] leading-snug font-semibold">{r.name}</span>
            {r.open ? <span className="pill pill-open">Applications open</span> : !r.verified && <span className="pill pill-na">Details soon</span>}
          </span>
          <span className="text-[13px]" style={{ color: "var(--muted)" }}>{meta}</span>
          {r.summary && <span className={`text-[14px] leading-relaxed ${open ? "" : "line-clamp-2"}`} style={{ color: "var(--soft)" }}>{r.summary}</span>}
        </span>
        <span className="shrink-0 pt-0.5 transition-transform duration-200" style={{ color: "var(--muted)", transform: open ? "rotate(180deg)" : undefined }}>
          <Icon name="chevronDown" size={20} />
        </span>
      </button>

      {open && (
        <div id={panelId} className="flex flex-col gap-5 px-4 pt-4 pb-5" style={{ borderTop: "1px solid var(--line)" }}>
          {r.verified ? (
            r.rows.map(([k, v]) => <PointSection key={k} title={ROW_TITLE[k] ?? k} icon={ROW_ICON[k] ?? ICON.info} color={color} text={v} />)
          ) : (
            <p className="m-0 rounded-lg px-4 py-3 text-[14px] leading-relaxed" style={{ background: "var(--warn-bg)", color: "var(--warn-ink)", boxShadow: "inset 0 0 0 1px var(--warn-line)" }}>
              We’re still checking this route against its official notice. Until then, use the official website below.
            </p>
          )}
          <div className="flex flex-wrap items-center gap-x-6 gap-y-2">
            {r.website && (
              <a href={`https://${r.website}`} target="_blank" rel="noreferrer" className="inline-flex items-center gap-1.5 text-[14px] font-semibold no-underline hover:underline" style={{ color: "var(--ok)", overflowWrap: "anywhere" }}>
                <Icon name="shieldCheck" size={16} /> {r.website} <Icon name="external" size={13} />
              </a>
            )}
            {r.examId && (
              <Link href={`/exams?exam=${r.examId}`} className="link inline-flex items-center gap-1 text-[14px]">
                Exam dates, syllabus and marks <Icon name="arrowRight" size={14} />
              </Link>
            )}
          </div>
          {r.source && <p className="m-0 text-[12px] leading-relaxed" style={{ color: "var(--muted)", overflowWrap: "anywhere" }}>Source: {r.source}</p>}
        </div>
      )}
    </li>
  );
}
