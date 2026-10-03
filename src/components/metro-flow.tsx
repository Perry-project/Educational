"use client";

import { useEffect, useMemo, useState, type CSSProperties } from "react";
import "./metro-flow.css";
import { CLUSTER_DEFS, col, nodesFor, STATES, TS_COUNTERPARTS, type FlowNode, type StateKey } from "@/lib/class10-flow-data";
import type { FlowchartData, NodeDetail } from "@/lib/flowchart-db";
import { alternativesAt, careerCluster, CLUSTER_COLOR, fmtYears, pickRoute, routesTo, years } from "@/lib/metro-routes";
import FlowchartSearch, { type SearchItem } from "./flowchart-search";

// The "metro" flowchart (/flowchart), from the Claude Design canvas "Perry
// Flowchart Mobile Redesign", option B. Every career is a line from Class
// 10; its stops are the steps on the way (after Class 10, entrance exam,
// course). Routes come from the chart's real connections (metro-routes.ts)
// and every detail from Postgres (flowchart-db.ts).
//
// Phones (< lg): a "Pick your line" start screen, then the route top to
// bottom; a stop's details open in a bottom sheet.
// Desktop (lg+): line buttons across the top, the route left to right, and
// the selected stop's details in one wide panel underneath.
//
// The URL keeps ?career=, ?stop= and ?via= so a route can be shared. The
// state switch is a plain link (a full load): every detail changes anyway.

const KIND: Record<number, string> = { 1: "Starting point", 2: "After Class 10", 3: "Entrance exam", 4: "Course" };
const STOP_COLOR: Record<number, string> = { 1: "#e1e5eb", 2: "#75aef5", 3: "#f29676", 4: "#68c4b8" };

// Lines offered first, by careers.career_name, with the everyday name shown.
const FEATURED: [string, string][] = [
  ["Information Technology / Software Engineering", "Software engineer"],
  ["Medicine (MBBS)", "Doctor"],
  ["Defence Services (Army/Navy/Air Force Officer)", "Defence officer"],
  ["Chartered Accountancy (CA)", "Chartered accountant"],
  ["Law (5-year integrated LLB)", "Lawyer"],
  ["School Teaching (Govt & Private schools)", "Teacher"],
];

// Career label: the database name without its trailing "(...)" details.
const shortName = (name: string) => name.replace(/(\s*\([^)]*\))+\s*$/, "") || name;
const NOT_ANNOUNCED = /not yet (?:announced|released|open|notified)|not announced/i;
const display = "var(--metro-display), var(--metro-body), system-ui, sans-serif";

type Career = { id: string; name: string; label: string; cl: string; color: string };

export default function MetroFlow({
  data, initial, bodyFont, displayFont,
}: {
  data: FlowchartData;
  initial: { career: string | null; stop: string | null; via: string | null; step: string | null };
  bodyFont: string;
  displayFont: string;
}) {
  const state = data.state;
  const nodes = useMemo(() => nodesFor(state), [state]);
  const nodeById = useMemo(() => Object.fromEntries(nodes.map((n) => [n.id, n])) as Record<string, FlowNode>, [nodes]);

  const careers = useMemo<Career[]>(
    () => data.careers.map((c) => {
      const cl = careerCluster(c.name);
      return { id: `career_${c.id}`, name: c.name, label: shortName(c.name), cl, color: CLUSTER_COLOR[cl] };
    }),
    [data.careers],
  );
  const careerById = useMemo(() => Object.fromEntries(careers.map((c) => [c.id, c])), [careers]);

  // Featured lines that exist in this state (a Telangana counterpart stands
  // in for an AP-only career).
  const featured = useMemo(() => {
    const tsFor = Object.fromEntries(Object.entries(TS_COUNTERPARTS).map(([ts, ap]) => [ap, ts]));
    return FEATURED.flatMap(([name, chip]) => {
      const c = careers.find((x) => x.name === name) ?? careers.find((x) => x.name === tsFor[name]);
      return c ? [{ ...c, chip }] : [];
    });
  }, [careers]);

  // Opening state from the URL. ?step= (links shared from the old chart)
  // opens the first featured line through that step.
  const [careerId, setCareerId] = useState<string | null>(() => {
    if (initial.career && careerById[`career_${initial.career}`]) return `career_${initial.career}`;
    if (initial.step?.startsWith("career_") && careerById[initial.step]) return initial.step;
    if (initial.step && nodeById[initial.step]) {
      const hit = featured.find((c) => routesTo(c.id, c.name, nodes).some((r) => r.stops.includes(initial.step!)));
      return hit?.id ?? null;
    }
    return null;
  });
  const [via, setVia] = useState<string | null>(initial.via ?? (initial.step && nodeById[initial.step] ? initial.step : null));
  const [stop, setStop] = useState<string | null>(initial.stop ?? (initial.step && nodeById[initial.step] ? initial.step : null));
  const [sheetOpen, setSheetOpen] = useState(false);
  const [showAll, setShowAll] = useState(false);

  // Desktop always shows a line; phones start on "Pick your line".
  const active = careerById[careerId ?? ""] ?? featured[0] ?? careers[0];
  const routes = useMemo(() => (active ? routesTo(active.id, active.name, nodes) : []), [active, nodes]);
  const route = pickRoute(routes, via);
  const stops = route?.stops ?? (active ? ["start", active.id] : []);
  const selected =
    stop && stops.includes(stop)
      ? stop
      : stops.find((s) => col(s) === 3) ?? stops.find((s) => col(s) === 4) ?? active?.id ?? null;

  // Featured careers go by their everyday name ("Software engineer").
  const chipOf = useMemo(() => Object.fromEntries(featured.map((c) => [c.id, c.chip])), [featured]);
  const nameOf = (id: string) => nodeById[id]?.label ?? chipOf[id] ?? careerById[id]?.label ?? id;
  const lineColor = active?.color ?? "#5b9cf0";

  // When each stop happens: years worked out from the Duration rows, while
  // every duration so far is one clear number.
  const timeline = (() => {
    let done: number | null = 0;
    const labels: string[] = [];
    for (const s of stops) {
      const c = col(s);
      if (s === "start") labels.push("Now");
      else if (careerById[s]) labels.push("Then");
      else if (c === 3) labels.push(done ? `End of year ${fmtYears(done)}` : "Entrance exam");
      else {
        const d = years(data.details[s]?.rows.find(([k]) => k === "Duration")?.[1]);
        if (done === null || d === null) {
          done = null;
          labels.push(KIND[c]);
        } else {
          const from = done + 1;
          done += d;
          labels.push(d <= 1 ? `Year ${fmtYears(from)}` : `Years ${fmtYears(from)}–${fmtYears(done)}`);
        }
      }
    }
    return { labels, total: done };
  })();

  // Keep the line in the URL so it can be shared.
  useEffect(() => {
    const url = new URL(window.location.href);
    const set = (k: string, v: string | null) => (v ? url.searchParams.set(k, v) : url.searchParams.delete(k));
    set("career", careerId ? careerId.replace("career_", "") : null);
    set("via", careerId ? via : null);
    set("stop", careerId ? stop : null);
    url.searchParams.delete("step");
    window.history.replaceState(window.history.state, "", url);
  }, [careerId, via, stop]);

  // Escape closes the phone sheet.
  useEffect(() => {
    if (!sheetOpen) return;
    const onKey = (e: KeyboardEvent) => e.key === "Escape" && setSheetOpen(false);
    window.addEventListener("keydown", onKey);
    const prev = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    return () => { window.removeEventListener("keydown", onKey); document.body.style.overflow = prev; };
  }, [sheetOpen]);

  const openLine = (id: string) => {
    setCareerId(id);
    setVia(null);
    setStop(null);
    setShowAll(false);
    setSheetOpen(false);
    window.scrollTo({ top: 0 });
  };
  const pickStop = (id: string, sheet: boolean) => {
    setStop(id);
    if (sheet) setSheetOpen(true);
  };
  const changeTo = (id: string) => {
    setVia(id);
    setStop(id);
  };

  // Search careers by name and by every stop on their routes, so "NEET"
  // finds the medical careers.
  const searchIndex = useMemo<SearchItem[]>(
    () => careers.map((c) => {
      const onRoute = routesTo(c.id, c.name, nodes).flatMap((r) => r.stops).map((s) => nodeById[s]?.label ?? "");
      return {
        id: c.id, label: c.label, kind: CLUSTER_DEFS.find((d) => d.id === c.cl)?.name ?? "Career", color: c.color,
        text: [c.name, ...new Set(onRoute)].join(" ").toLowerCase(),
      };
    }),
    [careers, nodes, nodeById],
  );

  const clusterName = (cl: string) => CLUSTER_DEFS.find((d) => d.id === cl)?.name ?? "Other routes";
  const detail = selected ? data.details[selected] : undefined;
  const courseOnRoute = stops.find((s) => col(s) === 4 && nodeById[s]);
  const collegeCount = courseOnRoute ? data.details[courseOnRoute]?.colleges?.length ?? 0 : 0;
  const otherRoutes = routes.filter((r) => r !== route).slice(0, 4);
  const stateSwitch = (k: StateKey) => (k === "ap" ? "/flowchart" : `/flowchart?state=${k}`);

  const meta = [
    timeline.total ? `About ${fmtYears(timeline.total)} years` : null,
    `${stops.length} stops`,
    collegeCount && courseOnRoute ? `${collegeCount} ${nameOf(courseOnRoute)} colleges in ${STATES[state].short}` : null,
  ].filter(Boolean).join(" · ");

  const rootStyle = { "--metro-body": bodyFont, "--metro-display": displayFont, fontFamily: bodyFont } as CSSProperties;

  // ---------- pieces shared by both layouts ----------

  const stateMenu = (
    <div role="group" aria-label="State" className="flex flex-wrap gap-1">
      {(Object.keys(STATES) as StateKey[]).map((k) => (
        <a
          key={k}
          href={stateSwitch(k)}
          aria-current={state === k ? "page" : undefined}
          className="metro-chip inline-flex h-11 items-center rounded-full px-4 text-sm font-semibold no-underline"
          style={{ background: state === k ? "var(--surface)" : "transparent", color: state === k ? "var(--ink)" : "var(--muted)" }}
        >
          {STATES[k].name}
        </a>
      ))}
    </div>
  );

  const allCareers = showAll && (
    <div className="flex flex-col gap-6 rounded-3xl p-6" style={{ background: "var(--panel)" }}>
      {CLUSTER_DEFS.map((d) => {
        const list = careers.filter((c) => c.cl === d.id);
        if (!list.length) return null;
        return (
          <section key={d.id} className="flex flex-col gap-2">
            <h3 className="m-0 flex items-center gap-2 text-xs font-bold tracking-widest uppercase" style={{ color: "var(--muted)" }}>
              <span className="h-2.5 w-2.5 rounded-full" style={{ background: CLUSTER_COLOR[d.id] }} />
              {d.name}
            </h3>
            <div className="flex flex-wrap gap-x-1 gap-y-0">
              {list.map((c) => (
                <button
                  key={c.id}
                  onClick={() => openLine(c.id)}
                  className="metro-chip min-h-11 cursor-pointer rounded-full border-0 bg-transparent px-3 text-left text-[15px] font-medium"
                  style={{ color: c.id === active?.id ? "var(--ink)" : "#c9d0dc", fontFamily: "inherit" }}
                >
                  {c.label}
                </button>
              ))}
            </div>
          </section>
        );
      })}
    </div>
  );

  const changeLink = (s: string) => {
    const alts = route ? alternativesAt(routes, route, s, 2) : [];
    if (!alts.length || s === "start" || careerById[s]) return null;
    return (
      <span className="flex flex-col items-start gap-0">
        {alts.map((a) => (
          <button
            key={a}
            onClick={() => changeTo(a)}
            className="inline-flex min-h-10 cursor-pointer items-center gap-2 border-0 bg-transparent p-0 text-left text-sm font-semibold"
            style={{ color: STOP_COLOR[col(a)], fontFamily: "inherit" }}
          >
            <span className="h-3 w-3 shrink-0 rounded-full" style={{ border: `3px solid ${STOP_COLOR[col(a)]}` }} />
            Change: {nameOf(a)}
          </button>
        ))}
      </span>
    );
  };

  const subOf = (s: string) => nodeById[s]?.sub ?? (careerById[s] ? clusterName(careerById[s].cl) : "");

  const lineHeader = active && (
    <div className="flex flex-col gap-3">
      <span
        className="self-start rounded-md px-3 py-1 text-[13px] font-extrabold tracking-wide uppercase"
        style={{ background: lineColor, color: "#0b1324" }}
      >
        {clusterName(active.cl)} line
      </span>
      <h1 className="m-0 text-[32px] leading-[1.08] font-extrabold tracking-tight lg:text-5xl" style={{ fontFamily: display, textWrap: "balance" }}>
        Class 10 to {nameOf(active.id)}
      </h1>
      <p className="m-0 text-base lg:text-lg" style={{ color: "var(--muted)" }}>{meta}</p>
      {!route && (
        <p className="m-0 max-w-2xl text-[15px] leading-relaxed" style={{ color: "#c9d0dc" }}>
          No single course on this chart leads here. The details below explain the route.
        </p>
      )}
    </div>
  );

  const otherRoutesList = otherRoutes.length > 0 && (
    <section className="flex flex-col gap-4">
      <h2 className="m-0 text-xs font-bold tracking-widest uppercase" style={{ color: "var(--muted)" }}>Other ways to get here</h2>
      <div className="grid gap-x-10 gap-y-5 lg:grid-cols-2">
        {otherRoutes.map((r) => {
          const mid = r.stops.filter((s) => s !== "start" && !careerById[s]);
          return (
            <button
              key={r.stops.join(">")}
              onClick={() => { setVia(mid.find((s) => !route?.stops.includes(s)) ?? null); setStop(null); }}
              className="metro-row flex cursor-pointer flex-col gap-3 rounded-2xl border-0 bg-transparent p-3 text-left"
              style={{ color: "var(--ink)", fontFamily: "inherit" }}
            >
              <span className="text-base font-bold">Through {mid.map(nameOf).join(", then ")}</span>
              <MiniLine stops={r.stops.filter((s) => !careerById[s])} color={lineColor} nameOf={nameOf} />
            </button>
          );
        })}
      </div>
    </section>
  );

  // ---------- phone ----------

  const phoneStart = (
    <div className="flex flex-col gap-8 px-6 pt-8 pb-12 lg:hidden">
      <div className="flex flex-col gap-3">
        <h1 className="m-0 text-[38px] leading-[1.05] font-extrabold tracking-tight" style={{ fontFamily: display }}>Pick your line.</h1>
        <p className="m-0 max-w-[320px] text-base leading-relaxed" style={{ color: "var(--muted)" }}>
          Every career is a line from Class 10. Follow one to see its stops.
        </p>
      </div>
      {stateMenu}
      <div className="flex">
        <FlowchartSearch items={searchIndex} onChoose={openLine} />
      </div>
      <nav aria-label="Career lines" className="-mx-2 flex flex-col gap-1">
        {featured.map((c) => {
          const r = routesTo(c.id, c.name, nodes)[0];
          const mid = r ? r.stops.filter((s) => s !== "start" && !careerById[s]).map(nameOf) : [];
          return (
            <button
              key={c.id}
              onClick={() => openLine(c.id)}
              className="metro-row flex min-h-16 cursor-pointer items-center gap-4 rounded-2xl border-0 bg-transparent px-2 py-1.5 text-left"
              style={{ color: "var(--ink)", fontFamily: "inherit" }}
            >
              <span className="h-11 w-2 shrink-0 rounded" style={{ background: c.color }} />
              <span className="flex flex-col gap-0.5">
                <span className="text-lg font-bold">{c.chip}</span>
                <span className="text-sm" style={{ color: "var(--muted)" }}>{mid.join(" · ")}</span>
              </span>
            </button>
          );
        })}
      </nav>
      <button
        onClick={() => setShowAll(!showAll)}
        aria-expanded={showAll}
        className="inline-flex min-h-11 cursor-pointer items-center gap-2 self-start border-0 bg-transparent p-0 text-[15px] font-semibold"
        style={{ color: "var(--accent)", fontFamily: "inherit" }}
      >
        {showAll ? "Hide the full list" : `All ${careers.length} careers`}
      </button>
      {allCareers}
    </div>
  );

  const phoneRoute = active && (
    <div className="flex flex-col gap-8 px-6 pt-3 pb-12 lg:hidden">
      <button
        onClick={() => { setCareerId(null); setVia(null); setStop(null); }}
        aria-label="Back to all lines"
        className="-ml-3 grid h-11 w-11 cursor-pointer place-items-center rounded-full border-0 bg-transparent"
        style={{ color: "var(--ink)" }}
      >
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden><path d="M19 12H5M11 6l-6 6 6 6" /></svg>
      </button>
      {lineHeader}
      <ol aria-label="Stops" className="m-0 flex list-none flex-col p-0">
        {stops.map((s, i) => {
          const last = i === stops.length - 1;
          const isSel = s === selected;
          return (
            <li key={s} className="grid grid-cols-[64px_36px_minmax(0,1fr)] gap-x-3">
              <span className="pt-0.5 text-right text-[13px] font-semibold" style={{ color: isSel ? "var(--ink)" : "var(--muted)" }}>{timeline.labels[i]}</span>
              <span className="relative flex justify-center">
                {/* The line runs from this station down to the next one. */}
                {!last && <span className="absolute bottom-0 w-2" style={{ top: i === 0 ? 12 : 0, background: lineColor }} />}
                {last && <span className="absolute top-0 h-3.5 w-2" style={{ background: lineColor }} />}
                <Station last={last} selected={isSel} color={lineColor} />
              </span>
              <div className={`flex flex-col items-start gap-1.5 ${last ? "" : "pb-8"}`}>
                <button
                  onClick={() => pickStop(s, true)}
                  className="cursor-pointer border-0 bg-transparent p-0 text-left text-[19px] font-bold"
                  style={{ color: "var(--ink)", fontFamily: display }}
                >
                  {nameOf(s)}
                </button>
                <span className="text-sm leading-snug" style={{ color: "var(--muted)" }}>{subOf(s)}</span>
                {changeLink(s)}
              </div>
            </li>
          );
        })}
      </ol>
      {otherRoutesList}
    </div>
  );

  const phoneSheet = sheetOpen && selected && (
    <div className="fixed inset-0 z-[120] lg:hidden">
      <button aria-label="Close details" onClick={() => setSheetOpen(false)} className="absolute inset-0 cursor-default border-0" style={{ background: "rgba(5,8,15,0.6)" }} />
      <section
        role="dialog"
        aria-modal="true"
        aria-label={`${nameOf(selected)} details`}
        className="metro-sheet absolute inset-x-0 bottom-0 flex max-h-[85vh] flex-col overflow-auto rounded-t-3xl"
        style={{ background: "#121829", paddingBottom: "env(safe-area-inset-bottom)" }}
      >
        <div className="flex justify-center pt-2.5"><span className="h-1.5 w-11 rounded-full" style={{ background: "#2f384d" }} /></div>
        <div className="flex flex-col gap-6 px-6 pt-4 pb-8">
          <StopDetails
            key={selected} node={nodeById[selected]} detail={detail} title={nameOf(selected)}
            careerKind={careerById[selected] ? `Career · ${clusterName(careerById[selected].cl)}` : null}
            stopNo={stops.indexOf(selected) + 1} region={STATES[state].short} lineColor={lineColor}
            onClose={() => setSheetOpen(false)}
          />
        </div>
      </section>
    </div>
  );

  // ---------- desktop ----------

  const desktop = active && (
    <div className="mx-auto hidden max-w-[1440px] flex-col gap-11 px-12 pt-4 pb-16 lg:flex">
      <nav aria-label="Career lines" className="flex flex-wrap items-center gap-x-6 gap-y-3 pb-5" style={{ borderBottom: "1px solid #1f2738" }}>
        <div className="flex min-w-0 flex-[999_1_640px] flex-wrap gap-1.5">
          {featured.map((c) => {
            const on = c.id === active.id;
            return (
              <button
                key={c.id}
                onClick={() => openLine(c.id)}
                aria-current={on ? "true" : undefined}
                className="metro-chip inline-flex h-11 cursor-pointer items-center gap-2.5 rounded-full border-0 pr-[18px] pl-3.5 text-[15px]"
                style={{ background: on ? "var(--surface)" : "transparent", color: on ? "var(--ink)" : "var(--muted)", fontWeight: on ? 700 : 600, fontFamily: "inherit" }}
              >
                <span className="h-[22px] w-1.5 rounded-sm" style={{ background: c.color }} />
                {c.chip}
              </button>
            );
          })}
          <button
            onClick={() => setShowAll(!showAll)}
            aria-expanded={showAll}
            className="inline-flex h-11 cursor-pointer items-center border-0 bg-transparent px-3.5 text-[15px] font-semibold"
            style={{ color: "var(--accent)", fontFamily: "inherit" }}
          >
            {showAll ? "Hide the full list" : `+ ${careers.length - featured.length} more`}
          </button>
        </div>
        <FlowchartSearch items={searchIndex} onChoose={openLine} />
      </nav>
      {allCareers}

      <section className="flex flex-wrap items-end justify-between gap-6">
        {lineHeader}
        {stateMenu}
      </section>

      <ol aria-label="Stops" className="relative m-0 grid list-none gap-x-6 p-0" style={{ gridTemplateColumns: `repeat(${stops.length}, minmax(0, 1fr))` }}>
        <span aria-hidden className="absolute top-[43px] h-2 rounded" style={{ left: `${50 / stops.length}%`, right: `${50 / stops.length}%`, background: lineColor }} />
        {stops.map((s, i) => {
          const isSel = s === selected;
          return (
            <li key={s} className="relative flex flex-col items-center gap-3 text-center">
              <span className="text-sm font-semibold" style={{ color: isSel ? "var(--ink)" : "var(--muted)" }}>{timeline.labels[i]}</span>
              <button
                onClick={() => pickStop(s, false)}
                aria-label={`${nameOf(s)} details`}
                aria-pressed={isSel}
                className="grid cursor-pointer place-items-center border-0 bg-transparent p-0"
              >
                <Station last={i === stops.length - 1} selected={isSel} color={lineColor} big />
              </button>
              <button
                onClick={() => pickStop(s, false)}
                className="cursor-pointer border-0 bg-transparent p-0 text-[22px] font-bold"
                style={{ color: "var(--ink)", fontFamily: display }}
              >
                {nameOf(s)}
              </button>
              <span className="text-[15px] leading-relaxed" style={{ color: "var(--muted)", textWrap: "balance" }}>{subOf(s)}</span>
              {changeLink(s)}
            </li>
          );
        })}
      </ol>

      {selected && (
        <section aria-label={`${nameOf(selected)} details`} className="grid gap-10 rounded-[28px] px-10 py-9 lg:grid-cols-[minmax(0,1fr)_minmax(0,2fr)]" style={{ background: "var(--panel)" }}>
          <StopDetails
            key={selected} node={nodeById[selected]} detail={detail} title={nameOf(selected)}
            careerKind={careerById[selected] ? `Career · ${clusterName(careerById[selected].cl)}` : null}
            stopNo={stops.indexOf(selected) + 1} region={STATES[state].short} lineColor={lineColor} wide
          />
        </section>
      )}

      {otherRoutesList}
    </div>
  );

  return (
    <div className="metro min-h-[calc(100vh-var(--nav-h))]" style={rootStyle}>
      {careerId ? phoneRoute : phoneStart}
      {desktop}
      {phoneSheet}
      <p className="mx-auto max-w-[1440px] px-6 pb-10 text-[13px] leading-relaxed lg:px-12" style={{ color: "var(--muted)" }}>
        Dates are from the most recent official notices. Always check the current notification before applying.
      </p>
    </div>
  );
}

function Station({ last, selected, color, big }: { last: boolean; selected: boolean; color: string; big?: boolean }) {
  const size = (selected ? 36 : last ? 32 : 26) + (big ? 4 : 0);
  return (
    <span
      className="relative block shrink-0 rounded-full"
      style={{
        width: size, height: size, boxSizing: "border-box",
        border: selected || last ? "5px solid var(--ink)" : `6px solid ${color}`,
        background: selected || last ? color : "var(--bg)",
        marginTop: selected ? -4 : last ? -2 : 0,
      }}
    />
  );
}

function MiniLine({ stops, color, nameOf }: { stops: string[]; color: string; nameOf: (id: string) => string }) {
  return (
    <span className="relative grid" style={{ gridTemplateColumns: `repeat(${stops.length}, minmax(0, 1fr))` }}>
      <span className="absolute top-[7px] h-1.5 rounded" style={{ left: 10, right: `calc(${100 / stops.length}% - 10px)`, background: color }} />
      {stops.map((s) => (
        <span key={s} className="relative flex flex-col gap-2 pr-2 text-xs leading-tight font-semibold" style={{ color: "#c9d0dc", overflowWrap: "anywhere" }}>
          <span className="h-5 w-5 rounded-full" style={{ border: `5px solid ${color}`, background: "var(--bg)", boxSizing: "border-box" }} />
          {s === "start" ? "Class 10" : nameOf(s)}
        </span>
      ))}
    </span>
  );
}

// A long value shows its first sentence, with "Show more".
function Fact({ text }: { text: string }) {
  const [open, setOpen] = useState(false);
  if (text.length <= 220 || open) return <>{text}</>;
  const cut = text.slice(0, text.lastIndexOf(" ", 200)) + "…";
  return (
    <>
      {cut}{" "}
      <button onClick={() => setOpen(true)} className="cursor-pointer border-0 bg-transparent p-0 font-semibold" style={{ color: "var(--accent)", fontFamily: "inherit", fontSize: "inherit" }}>
        Show more
      </button>
    </>
  );
}

function StopDetails({
  node, detail, title, careerKind, stopNo, region, lineColor, wide, onClose,
}: {
  node?: FlowNode; detail?: NodeDetail; title: string; careerKind: string | null;
  stopNo: number; region: string; lineColor: string; wide?: boolean; onClose?: () => void;
}) {
  const kind = careerKind ?? (node ? KIND[node.col] : "");
  const rows = (detail?.rows ?? []).filter(([k, v]) => !(k === "Full name" && v === title));
  const isCourse = node?.col === 4;
  const intro = (
    <div className="flex flex-col gap-3">
      <div className="flex items-start gap-3">
        <div className="flex flex-1 flex-col gap-1.5">
          <span className="text-xs font-bold tracking-widest uppercase" style={{ color: "var(--muted)" }}>Stop {stopNo} · {kind}</span>
          <h2 className="m-0 text-[26px] leading-tight font-extrabold lg:text-[32px]" style={{ fontFamily: display }}>{title}</h2>
        </div>
        {onClose && (
          <button onClick={onClose} aria-label="Close details" className="grid h-11 w-11 shrink-0 cursor-pointer place-items-center rounded-full bg-transparent" style={{ border: "1px solid var(--line)", color: "var(--ink)" }}>
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" aria-hidden><path d="M6 6l12 12M18 6L6 18" /></svg>
          </button>
        )}
      </div>
      {node?.full && <p className="m-0 text-base leading-relaxed" style={{ color: "#c9d0dc" }}>{node.full}</p>}
      {detail?.note && <p className="m-0 rounded-xl px-4 py-3 text-sm leading-relaxed" style={{ background: "#2b2412", color: "#f0d9a0" }}>{detail.note}</p>}
      {!detail && <p className="m-0 text-sm" style={{ color: "var(--muted)" }}>Details for this stop haven’t been added yet.</p>}
    </div>
  );
  const source = detail?.source && (
    <p className="m-0 text-xs leading-relaxed" style={{ color: "var(--muted)", overflowWrap: "anywhere" }}>
      Source: <Fact text={detail.source} />
    </p>
  );

  const body = (
    <div className="flex min-w-0 flex-col gap-8">
      {rows.length > 0 && (
        <dl className={`m-0 grid gap-x-10 ${wide ? "lg:grid-cols-2" : ""}`}>
          {rows.map(([k, v]) => (
            <div key={k} className="flex flex-col gap-1 py-3" style={{ borderBottom: "1px solid var(--rule)" }}>
              <dt className="flex flex-wrap items-center gap-2 text-sm font-bold">
                {k}
                {(k === "Applications" || k === "Exam dates") && NOT_ANNOUNCED.test(v) && (
                  <span className="rounded-full px-2.5 py-0.5 text-xs font-bold" style={{ background: "#2b2412", color: "#f0c870" }}>Next dates not announced</span>
                )}
              </dt>
              <dd className="m-0 text-[15px] leading-relaxed" style={{ color: "#c9d0dc", overflowWrap: "anywhere" }}><Fact text={v} /></dd>
            </div>
          ))}
        </dl>
      )}
      {isCourse && (
        <section className="flex flex-col gap-3">
          <h3 className="m-0 text-xs font-bold tracking-widest uppercase" style={{ color: "var(--muted)" }}>
            Colleges in {region}{detail?.colleges?.length ? ` · ${detail.colleges.length}` : ""}
          </h3>
          {detail?.colleges?.length ? (
            <ul className="m-0 grid list-none gap-x-8 gap-y-2 p-0 sm:grid-cols-2">
              {detail.colleges.map((c) => (
                <li key={c.name} className="flex flex-col text-[15px]">
                  {c.name}
                  {c.ownership && <span className="text-xs" style={{ color: "var(--muted)" }}>{c.ownership}</span>}
                </li>
              ))}
            </ul>
          ) : (
            <p className="m-0 text-sm" style={{ color: "var(--muted)" }}>No {region} colleges listed for this course yet.</p>
          )}
        </section>
      )}
      {isCourse && (
        <section className="flex flex-col gap-3">
          <h3 className="m-0 text-xs font-bold tracking-widest uppercase" style={{ color: "var(--muted)" }}>
            What you’ll study{detail?.topics?.length ? ` · ${detail.topics.length} topics` : ""}
          </h3>
          {detail?.topics?.length ? (
            <>
              <ol className="m-0 flex list-none flex-col gap-2 p-0">
                {detail.topics.map((t, i) => (
                  <li key={t.name} className="flex gap-3 text-[15px]">
                    <span className="w-5 shrink-0 font-extrabold" style={{ color: lineColor }}>{i + 1}</span>
                    {t.name}
                  </li>
                ))}
              </ol>
              <span className="text-xs" style={{ color: "var(--muted)" }}>Topic guide is AI-assisted. Check your college’s syllabus.</span>
            </>
          ) : (
            <p className="m-0 text-sm" style={{ color: "var(--muted)" }}>Study topics for this course are being added.</p>
          )}
        </section>
      )}
      {source}
    </div>
  );

  return (
    <>
      {intro}
      {body}
    </>
  );
}
