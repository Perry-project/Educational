"use client";

import Link from "next/link";
import { useEffect, useMemo, useState, type CSSProperties, type ReactNode } from "react";
import "./metro-flow.css";
import { ICON, PointSection } from "./fact-points";
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
  class_10: "#75aef5",
  intermediate: "#f0b44c",
  degree: "#68c4b8",
  entrance_exam: "#f29676",
  working: "#c39cf5",
};
const STATE_TABS = [
  { id: "all", label: "AP & Telangana" },
  { id: "ap", label: "Andhra Pradesh" },
  { id: "ts", label: "Telangana" },
];
const display = "var(--metro-display), var(--metro-body), system-ui, sans-serif";
const soft = "#c9d0dc";
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

  const choose = (id: StopId) => {
    setFrom(id);
    setOpenId(null);
  };

  const rootStyle = { "--metro-body": bodyFont, "--metro-display": displayFont, fontFamily: bodyFont } as CSSProperties;
  const chip = (on: boolean): CSSProperties => ({
    background: on ? "var(--surface)" : "transparent", color: on ? "var(--ink)" : "var(--muted)", fontFamily: "inherit",
  });
  const stop = STOPS.find((s) => s.id === from);
  const color = from ? LINE[from] : "var(--accent)";

  return (
    <div className="metro min-h-[calc(100vh-var(--nav-h))]" style={rootStyle}>
      <div className="mx-auto flex max-w-[1100px] flex-col gap-9 px-5 pt-8 pb-16 lg:px-12">
        <header className="flex flex-col gap-3">
          <h1 className="m-0 text-[34px] leading-[1.08] font-extrabold tracking-tight lg:text-[44px]" style={{ fontFamily: display }}>
            Second Chance
          </h1>
          <p className="m-0 max-w-2xl text-base leading-relaxed lg:text-lg" style={{ color: "var(--muted)" }}>
            Stopped studying somewhere? There’s an official way back, for the same field or a new one. Every route here is a government or university program.
          </p>
        </header>

        <section className="flex flex-col gap-4" aria-labelledby="stop-q">
          <h2 id="stop-q" className="m-0 text-xl font-extrabold lg:text-2xl" style={{ fontFamily: display }}>Where did you stop?</h2>
          <div role="group" aria-labelledby="stop-q" className="grid grid-cols-2 gap-2 lg:grid-cols-5">
            {STOPS.map((s) => {
              const on = s.id === from;
              return (
                <button
                  key={s.id}
                  onClick={() => choose(s.id)}
                  aria-pressed={on}
                  className={`metro-row flex cursor-pointer items-center gap-2.5 rounded-2xl px-3.5 py-3 text-left sm:px-4 sm:py-3.5 lg:flex-col lg:items-start lg:gap-2.5 ${s.id === "working" ? "col-span-2 lg:col-span-1" : ""}`}
                  style={{
                    background: on ? "var(--surface)" : "transparent", color: "var(--ink)", fontFamily: "inherit",
                    border: `1px solid ${on ? LINE[s.id] : "var(--line)"}`,
                  }}
                >
                  <span className="h-3.5 w-3.5 shrink-0 rounded-full" style={{ border: `4px solid ${LINE[s.id]}`, background: on ? LINE[s.id] : "transparent" }} />
                  <span className="flex flex-col gap-0.5">
                    <span className="text-[15px] leading-snug font-bold sm:text-[16px]">{s.label}</span>
                    <span className="hidden text-[13px] leading-snug sm:block" style={{ color: "var(--muted)" }}>{s.long}</span>
                  </span>
                </button>
              );
            })}
          </div>
          <div role="group" aria-label="State" className="flex flex-wrap gap-1">
            {STATE_TABS.map((t) => (
              <button key={t.id} onClick={() => setState(t.id)} aria-pressed={state === t.id}
                className="metro-chip h-11 cursor-pointer rounded-full border-0 px-4 text-sm font-semibold" style={chip(state === t.id)}>
                {t.label}
              </button>
            ))}
          </div>
        </section>

        {!stop ? (
          openNow.length > 0 && (
            <section className="flex flex-col gap-3" aria-labelledby="open-now">
              <h2 id="open-now" className="m-0 text-xs font-bold tracking-widest uppercase" style={{ color: "var(--muted)" }}>Applications open now</h2>
              <ul className="m-0 flex list-none flex-col gap-1 p-0">
                {openNow.map((r) => (
                  <li key={r.id}>
                    <button
                      onClick={() => { setFrom(r.stoppedAt); setOpenId(r.id); }}
                      className="metro-row flex w-full cursor-pointer items-start gap-3 rounded-xl border-0 px-3 py-2.5 text-left"
                      style={{ background: "transparent", color: "var(--ink)", fontFamily: "inherit" }}
                    >
                      <span className="mt-1.5 h-2.5 w-2.5 shrink-0 rounded-full" style={{ background: LINE[r.stoppedAt] }} />
                      <span className="flex min-w-0 flex-col gap-0.5">
                        <span className="text-[16px] font-bold">{r.name}</span>
                        <span className="text-[13px] leading-snug" style={{ color: "var(--muted)" }}>{r.rows.find(([k]) => k === "Dates")?.[1]}</span>
                      </span>
                    </button>
                  </li>
                ))}
              </ul>
            </section>
          )
        ) : (
          <section className="flex flex-col gap-6" aria-labelledby="routes-h">
            <div className="flex flex-col gap-1">
              <span className="text-xs font-bold tracking-widest uppercase" style={{ color }}>{stop.long}</span>
              <h2 id="routes-h" className="m-0 text-2xl font-extrabold lg:text-[28px]" style={{ fontFamily: display }}>
                {shown.length} {shown.length === 1 ? "way" : "ways"} back
              </h2>
            </div>
            {shown.length === 0 ? (
              <p className="m-0 text-[15px]" style={{ color: "var(--muted)" }}>No routes for this state yet. Try “AP & Telangana”.</p>
            ) : (
              <ol aria-label="Routes" className="m-0 flex list-none flex-col p-0">
                {shown.map((r, i) => (
                  <Station
                    key={r.id} route={r} color={color} first={i === 0} last={i === shown.length - 1}
                    open={openId === r.id} onToggle={() => setOpenId(openId === r.id ? null : r.id)}
                  />
                ))}
              </ol>
            )}
          </section>
        )}

        <p className="m-0 text-[13px] leading-relaxed" style={{ color: "var(--muted)" }}>
          Dates and rules are from each program’s latest official notice. Always check the official website before applying.
        </p>
      </div>
    </div>
  );
}

function Station({
  route: r, color, first, last, open, onToggle,
}: {
  route: Route; color: string; first: boolean; last: boolean; open: boolean; onToggle: () => void;
}) {
  const panelId = `route-panel-${r.id}`;
  const meta = [r.scope === "National" ? "All-India" : r.scope, r.kind, r.body].filter(Boolean).join(" · ");
  const site = r.website && (
    <a href={`https://${r.website}`} target="_blank" rel="noreferrer" className="inline-flex items-center gap-1.5 self-start text-[15px] font-semibold no-underline" style={{ color: "var(--accent)", overflowWrap: "anywhere" }}>
      {r.website}
      <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round" aria-hidden><path d="M7 17L17 7M9 7h8v8" /></svg>
    </a>
  );

  return (
    <li id={`route-${r.id}`} className="grid grid-cols-[32px_minmax(0,1fr)] gap-x-4 sm:gap-x-5">
      <span className="relative flex justify-center">
        {/* The line runs through every station, from the first to the last. */}
        {!(first && last) && (
          <span className="absolute w-1.5" style={{ top: first ? 14 : 0, bottom: last ? "auto" : 0, height: last ? 14 : undefined, background: color }} />
        )}
        <span
          className="relative mt-0.5 block shrink-0 rounded-full"
          style={{
            width: open ? 28 : 24, height: open ? 28 : 24, boxSizing: "border-box",
            border: open ? "5px solid var(--ink)" : `5px solid ${color}`, background: open ? color : "var(--bg)",
            marginTop: open ? -1 : 1,
          }}
        />
      </span>
      <div className={`flex min-w-0 flex-col items-start gap-1.5 ${last ? "" : "pb-9"}`}>
        <button
          onClick={onToggle}
          aria-expanded={open}
          aria-controls={panelId}
          className="cursor-pointer border-0 bg-transparent p-0 text-left text-[19px] leading-snug font-bold"
          style={{ color: "var(--ink)", fontFamily: display }}
        >
          {r.name}
        </button>
        <span className="text-sm leading-snug" style={{ color: "var(--muted)" }}>{meta}</span>
        {r.open && (
          <span className="mt-1 rounded-full px-2.5 py-1 text-[12px] font-bold" style={{ background: "#173a2c", color: "#7ee0b0" }}>Applications open</span>
        )}
        {r.summary && <p className="m-0 mt-1 max-w-[62ch] text-[15px] leading-relaxed" style={{ color: soft }}>{r.summary}</p>}
        {!r.verified && <span className="text-[13px] font-semibold" style={{ color: "var(--muted)" }}>Details soon</span>}
        <button
          onClick={onToggle}
          aria-expanded={open}
          aria-controls={panelId}
          className="mt-1 inline-flex cursor-pointer items-center gap-1.5 border-0 bg-transparent p-0 text-[14px] font-semibold"
          style={{ color: "var(--accent)", fontFamily: "inherit" }}
        >
          {open ? "Hide details" : "Details"}
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round" aria-hidden style={{ transform: open ? "rotate(180deg)" : undefined }}><path d="M6 9l6 6 6-6" /></svg>
        </button>

        {open && (
          <div id={panelId} className="mt-3 flex w-full max-w-[720px] flex-col gap-4">
            {r.verified ? (
              <div className="flex flex-col gap-6">
                {r.rows.map(([k, v]) => (
                  <PointSection key={k} title={ROW_TITLE[k] ?? k} icon={ROW_ICON[k] ?? ICON.info} color={color} text={v} />
                ))}
              </div>
            ) : (
              <p className="m-0 rounded-xl px-4 py-3 text-[15px] leading-relaxed" style={{ background: "var(--surface)", color: soft }}>
                We’re still checking this route against its official notice. Until it’s added, use the official website below.
              </p>
            )}
            <div className="flex flex-wrap items-center gap-x-6 gap-y-2">
              {site}
              {r.examId && (
                <Link href={`/exams?exam=${r.examId}`} className="text-[15px] font-semibold no-underline" style={{ color: "var(--accent)" }}>
                  Exam details, syllabus and marks →
                </Link>
              )}
            </div>
            {r.source && (
              <p className="m-0 text-xs leading-relaxed" style={{ color: "var(--muted)", overflowWrap: "anywhere" }}>Source: {r.source}</p>
            )}
          </div>
        )}
      </div>
    </li>
  );
}
