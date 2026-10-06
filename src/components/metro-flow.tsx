"use client";

import Link from "next/link";
import { useEffect, useMemo, useRef, useState, type CSSProperties } from "react";
import "./metro-flow.css";
import { CLUSTER_DEFS, col, nodesFor, STATES, TS_COUNTERPARTS, type FlowNode, type StateKey } from "@/lib/class10-flow-data";
import type { FlowchartData, NodeDetail } from "@/lib/flowchart-db";
import { alternativesAt, careerCluster, CLUSTER_COLOR, fmtYears, pickRoute, routesTo, years } from "@/lib/metro-routes";
import { GOVT_GROUPS, isComputing, STEP_MENUS } from "@/lib/flow-menus";
import FlowMenuBar, { type BarMenu } from "./flow-menu-bar";
import FlowchartSearch, { type SearchItem } from "./flowchart-search";
import { ICON, PointSection } from "./fact-points";

// The "metro" flowchart (/flowchart), from the Claude Design canvas "Perry
// Flowchart Mobile Redesign", option B. Every career is a line from Class
// 10; its stops are the steps on the way (after Class 10, entrance exam,
// course). Routes come from the chart's real connections (metro-routes.ts)
// and every detail from Postgres (flowchart-db.ts).
//
// Every screen size opens on "Pick your line": no route is shown until the
// student chooses a career.
// Phones (< lg): the route top to bottom; a stop's details open in a bottom
// sheet.
// Desktop (lg+): dropdown menus across the top (flow-menus.ts), the route top to bottom in a
// left column that stays in view, and the selected stop's full details on
// the right.
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
  initial: { career: string | null; stop: string | null; via: string | null; step: string | null; field: string | null };
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
  const [field, setField] = useState<string | null>(initial.field);
  const panelRef = useRef<HTMLElement>(null);

  // Until a line is picked, the start screen shows; `active` falls back to
  // the first featured line only so the line view's values stay defined.
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
    set("field", careerId ? null : field);
    url.searchParams.delete("step");
    window.history.replaceState(window.history.state, "", url);
  }, [careerId, via, stop, field]);

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
    setSheetOpen(false);
    window.scrollTo({ top: 0 });
  };
  // On desktop, a new stop's details start from their top, even if the
  // last stop's long panel was scrolled past.
  const toPanelTop = () => {
    const top = panelRef.current?.getBoundingClientRect().top;
    if (top !== undefined && top < 0) window.scrollBy({ top: top - 100 });
  };
  const pickStop = (id: string, sheet: boolean) => {
    setStop(id);
    if (sheet) setSheetOpen(true);
    else toPanelTop();
  };
  const changeTo = (id: string) => {
    setVia(id);
    setStop(id);
    toPanelTop();
  };

  const routesOf = useMemo(
    () => Object.fromEntries(careers.map((c) => [c.id, routesTo(c.id, c.name, nodes)])),
    [careers, nodes],
  );

  // A step from the menus opens a line through it (a featured one first),
  // with that step's details showing.
  const openStep = (id: string) => {
    const through = (c: Career) => routesOf[c.id]?.some((r) => r.stops.includes(id));
    const c = featured.find(through) ?? careers.find(through);
    if (!c) return;
    openLine(c.id);
    setVia(id);
    setStop(id);
  };

  // The desktop menus: steps by kind, careers by field, and government jobs
  // again on their own. Steps with no career route through them are left out.
  const menus = useMemo<BarMenu[]>(() => {
    const reachable = new Set(Object.values(routesOf).flatMap((rs) => rs.flatMap((r) => r.stops)));
    const careerItem = (c: Career) => ({ id: c.id, label: chipOf[c.id] ?? c.label });
    const steps = STEP_MENUS.map((m) => ({
      id: m.id, label: m.label,
      groups: m.groups.map((g) => ({
        title: g.title,
        items: g.ids.filter((id) => nodeById[id] && reachable.has(id))
          .map((id) => ({ id, label: nodeById[id].label, sub: nodeById[id].sub, color: STOP_COLOR[col(id)] })),
      })).filter((g) => g.items.length),
    }));
    const byField = CLUSTER_DEFS.flatMap((d) => {
      const list = careers.filter((c) => c.cl === d.id);
      const color = CLUSTER_COLOR[d.id];
      if (d.id === "cl_eng") return [
        { title: "Computer & IT", color, items: list.filter((c) => isComputing(c.name)).map(careerItem) },
        { title: "Core engineering", color, items: list.filter((c) => !isComputing(c.name)).map(careerItem) },
      ];
      return [{ title: d.name, color, items: list.map(careerItem) }];
    }).filter((g) => g.items.length);
    const govt = GOVT_GROUPS.map(([title, re]) => ({
      title, items: careers.filter((c) => re.test(c.name)).map(careerItem),
    })).filter((g) => g.items.length);
    return [...steps, { id: "careers", label: "Careers", groups: byField }, { id: "govt", label: "Government jobs", groups: govt }];
  }, [routesOf, careers, nodeById, chipOf]);

  // Search careers by name and by every stop on their routes, so "NEET"
  // finds the medical careers.
  const searchIndex = useMemo<SearchItem[]>(
    () => careers.map((c) => {
      const onRoute = routesOf[c.id].flatMap((r) => r.stops).map((s) => nodeById[s]?.label ?? "");
      return {
        id: c.id, label: c.label, kind: CLUSTER_DEFS.find((d) => d.id === c.cl)?.name ?? "Career", color: c.color,
        text: [c.name, ...new Set(onRoute)].join(" ").toLowerCase(),
      };
    }),
    [careers, routesOf, nodeById],
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
      <h1 className="m-0 text-[32px] leading-[1.08] font-extrabold tracking-tight lg:text-[44px]" style={{ fontFamily: display, textWrap: "balance" }}>
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

  // The start screen asks for a field first, then shows only that field's
  // careers, the everyday-named featured ones first.
  const fields = useMemo(() => {
    const rank = (c: Career) => {
      const i = featured.findIndex((f) => f.id === c.id);
      return i < 0 ? featured.length : i;
    };
    return CLUSTER_DEFS.map((d) => ({
      ...d,
      color: CLUSTER_COLOR[d.id],
      list: careers.filter((c) => c.cl === d.id).sort((a, b) => rank(a) - rank(b)),
    })).filter((f) => f.list.length);
  }, [careers, featured]);
  const shownField = fields.find((f) => f.id === field) ?? null;
  const revealField = useRef(false);
  const chooseField = (id: string) => {
    revealField.current = true;
    setField(field === id ? null : id);
  };
  // On a phone the chosen field's careers render below the fold, so bring
  // them into view once they're on the page (not on a shared ?field= link).
  useEffect(() => {
    if (!revealField.current) return;
    revealField.current = false;
    const el = document.getElementById("field-lines");
    if (el && el.getBoundingClientRect().top > window.innerHeight * 0.6) el.scrollIntoView({ behavior: "smooth", block: "start" });
  }, [field]);

  const start = (
    <div className="mx-auto flex w-full max-w-[1100px] flex-col gap-8 px-6 pt-8 pb-12 lg:px-12 lg:pt-12">
      <div className="hidden lg:block">
        <FlowMenuBar menus={menus} current={new Set()} onChoose={(id) => (careerById[id] ? openLine(id) : openStep(id))} />
      </div>
      <div className="flex flex-col gap-3">
        <h1 className="m-0 text-[38px] leading-[1.05] font-extrabold tracking-tight lg:text-[52px]" style={{ fontFamily: display }}>Pick your line.</h1>
        <p className="m-0 max-w-[320px] text-base leading-relaxed lg:max-w-xl lg:text-lg" style={{ color: "var(--muted)" }}>
          Every career is a line from Class 10. Pick a field, then follow a line to see its stops.
        </p>
      </div>
      {stateMenu}
      <div className="flex">
        <FlowchartSearch items={searchIndex} onChoose={openLine} />
      </div>
      <section aria-labelledby="field-q" className="flex flex-col gap-4">
        <h2 id="field-q" className="m-0 text-xl font-extrabold lg:text-2xl" style={{ fontFamily: display }}>Which field interests you?</h2>
        <div role="group" aria-labelledby="field-q" className="grid grid-cols-2 gap-2 lg:grid-cols-3">
          {fields.map((f, i) => {
            const on = f.id === field;
            const lone = i === fields.length - 1 && fields.length % 2 === 1;
            return (
              <button
                key={f.id}
                onClick={() => chooseField(f.id)}
                aria-pressed={on}
                aria-controls="field-lines"
                className={`metro-row flex min-h-[92px] cursor-pointer flex-col items-start gap-2 rounded-2xl px-4 py-3.5 text-left ${lone ? "col-span-2 lg:col-span-1" : ""}`}
                style={{ background: on ? "var(--surface)" : "transparent", color: "var(--ink)", border: `1px solid ${on ? f.color : "var(--line)"}`, fontFamily: "inherit" }}
              >
                <span className="h-1.5 w-8 rounded-full" style={{ background: f.color }} />
                <span className="text-[15px] leading-snug font-bold lg:text-base">{f.name}</span>
                <span className="text-[13px]" style={{ color: "var(--muted)" }}>
                  {f.list.length} {f.list.length === 1 ? "career" : "careers"}
                </span>
              </button>
            );
          })}
        </div>
      </section>
      {shownField && (
        <section id="field-lines" aria-labelledby="field-h" className="flex flex-col gap-3" style={{ scrollMarginTop: "calc(var(--nav-h) + 16px)" }}>
          <div className="flex flex-col gap-1">
            <span className="text-xs font-bold tracking-widest uppercase" style={{ color: shownField.color }}>{shownField.list.length} lines</span>
            <h2 id="field-h" className="m-0 text-2xl font-extrabold lg:text-[28px]" style={{ fontFamily: display }}>{shownField.name}</h2>
          </div>
          <nav aria-label={`${shownField.name} careers`} className="-mx-2 grid gap-1 lg:grid-cols-2 lg:gap-2 xl:grid-cols-3">
            {shownField.list.map((c) => {
              const r = routesOf[c.id]?.[0];
              const mid = r ? r.stops.filter((s) => s !== "start" && !careerById[s]).map(nameOf) : [];
              return (
                <button
                  key={c.id}
                  onClick={() => openLine(c.id)}
                  className="metro-row flex min-h-16 cursor-pointer items-center gap-4 rounded-2xl border-0 bg-transparent px-2 py-1.5 text-left"
                  style={{ color: "var(--ink)", fontFamily: "inherit" }}
                >
                  <span className="h-11 w-2 shrink-0 rounded" style={{ background: c.color }} />
                  <span className="flex min-w-0 flex-col gap-0.5">
                    <span className="text-lg leading-snug font-bold">{chipOf[c.id] ?? c.label}</span>
                    <span className="text-sm leading-snug" style={{ color: "var(--muted)" }}>
                      {mid.length ? mid.join(" · ") : "Straight from Class 10"}
                    </span>
                  </span>
                </button>
              );
            })}
          </nav>
        </section>
      )}
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
    <div className="mx-auto hidden max-w-[1440px] flex-col gap-8 px-12 pt-4 pb-16 lg:flex">
      <nav aria-label="Flowchart menus" className="flex flex-wrap items-center gap-x-6 gap-y-3 pb-5" style={{ borderBottom: "1px solid #1f2738" }}>
        <button
          onClick={() => { setCareerId(null); setVia(null); setStop(null); }}
          className="metro-chip inline-flex h-10 cursor-pointer items-center gap-2 rounded-full border-0 bg-transparent px-3 text-sm font-semibold"
          style={{ color: "var(--muted)", fontFamily: "inherit" }}
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden><path d="M19 12H5M11 6l-6 6 6 6" /></svg>
          All lines
        </button>
        <FlowMenuBar menus={menus} current={new Set(stops)} onChoose={(id) => (careerById[id] ? openLine(id) : openStep(id))} />
        <FlowchartSearch items={searchIndex} onChoose={openLine} />
      </nav>

      <section className="flex flex-wrap items-end justify-between gap-6">
        {lineHeader}
        {stateMenu}
      </section>

      {/* The line runs down the left and stays in view; the selected stop's
          full details fill the right. */}
      <div className="grid grid-cols-[440px_minmax(0,1fr)] items-start gap-10 xl:grid-cols-[480px_minmax(0,1fr)]">
        <aside className="metro-scroll sticky flex max-h-[calc(100vh-var(--nav-h)-48px)] flex-col gap-8 overflow-y-auto pr-1" style={{ top: "calc(var(--nav-h) + 24px)" }}>
          <ol aria-label="Stops" className="m-0 flex list-none flex-col p-0">
            {stops.map((s, i) => {
              const last = i === stops.length - 1;
              const isSel = s === selected;
              const alts = route && s !== "start" && !careerById[s] ? alternativesAt(routes, route, s, 3) : [];
              return (
                <li key={s} className="grid grid-cols-[96px_36px_minmax(0,1fr)] gap-x-3">
                  <span className="pt-3 text-right text-[13px] font-semibold" style={{ color: isSel ? "var(--ink)" : "var(--muted)" }}>{timeline.labels[i]}</span>
                  <span className="relative flex justify-center pt-2.5">
                    {/* The line runs from this station down to the next one. */}
                    {!last && <span className="absolute bottom-0 w-2" style={{ top: i === 0 ? 22 : 0, background: lineColor }} />}
                    {last && <span className="absolute top-0 h-6 w-2" style={{ background: lineColor }} />}
                    <Station last={last} selected={isSel} color={lineColor} />
                  </span>
                  <div className={`flex min-w-0 flex-col items-stretch gap-2 ${last ? "" : "pb-5"}`}>
                    <button
                      onClick={() => pickStop(s, false)}
                      aria-pressed={isSel}
                      className="metro-row flex cursor-pointer flex-col items-start gap-0.5 rounded-xl border-0 px-3 py-2 text-left"
                      style={{ background: isSel ? "var(--surface)" : "transparent", color: "var(--ink)", fontFamily: "inherit" }}
                    >
                      <span className="text-[19px] font-bold" style={{ fontFamily: display }}>{nameOf(s)}</span>
                      <span className="text-sm leading-snug" style={{ color: "var(--muted)" }}>{subOf(s)}</span>
                    </button>
                    {alts.length > 0 && (
                      <div className="flex flex-col items-start gap-1.5 pl-3">
                        <span className="text-xs font-semibold" style={{ color: "var(--muted)" }}>Or instead of {nameOf(s)}:</span>
                        <div className="flex flex-wrap gap-1.5">
                          {alts.map((a) => (
                            <button
                              key={a}
                              onClick={() => changeTo(a)}
                              title={`Switch the route to go through ${nameOf(a)}`}
                              className="metro-alt inline-flex min-h-9 cursor-pointer items-center gap-1.5 rounded-full bg-transparent px-3 text-[13px] font-semibold"
                              style={{ border: `1px dashed ${STOP_COLOR[col(a)]}`, color: STOP_COLOR[col(a)], fontFamily: "inherit" }}
                            >
                              {nameOf(a)}
                              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden><path d="M5 12h14M13 6l6 6-6 6" /></svg>
                            </button>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                </li>
              );
            })}
          </ol>

          {otherRoutes.length > 0 && (
            <section className="flex flex-col gap-2 pl-[120px]">
              <h2 className="m-0 px-3 text-xs font-bold tracking-widest uppercase" style={{ color: "var(--muted)" }}>Other ways to get here</h2>
              {otherRoutes.map((r) => {
                const mid = r.stops.filter((s) => s !== "start" && !careerById[s]);
                return (
                  <button
                    key={r.stops.join(">")}
                    onClick={() => { setVia(mid.find((s) => !route?.stops.includes(s)) ?? null); setStop(null); }}
                    className="metro-row cursor-pointer rounded-xl border-0 bg-transparent px-3 py-2 text-left text-sm leading-snug"
                    style={{ color: "#c9d0dc", fontFamily: "inherit" }}
                  >
                    {mid.map(nameOf).join(" → ")}
                  </button>
                );
              })}
            </section>
          )}
        </aside>

        {selected && (
          <section ref={panelRef} aria-label={`${nameOf(selected)} details`} className="flex min-w-0 flex-col gap-8 rounded-[28px] px-10 py-9" style={{ background: "var(--panel)" }}>
            <StopDetails
              key={selected} node={nodeById[selected]} detail={detail} title={nameOf(selected)}
              careerKind={careerById[selected] ? `Career · ${clusterName(careerById[selected].cl)}` : null}
              stopNo={stops.indexOf(selected) + 1} region={STATES[state].short} lineColor={lineColor} wide
            />
          </section>
        )}
      </div>
    </div>
  );

  return (
    <div className="metro min-h-[calc(100vh-var(--nav-h))]" style={rootStyle}>
      {careerId ? <>{phoneRoute}{desktop}</> : start}
      {phoneSheet}
      <p className={`mx-auto px-6 pb-10 text-[13px] leading-relaxed lg:px-12 ${careerId ? "max-w-[1440px]" : "max-w-[1100px]"}`} style={{ color: "var(--muted)" }}>
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

// A long value shows its first sentence, with "Show more" (phones only;
// the desktop panel has room for all of it).
function Fact({ text, full }: { text: string; full?: boolean }) {
  const [open, setOpen] = useState(false);
  if (full || text.length <= 220 || open) return <>{text}</>;
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

// Which /second-chance group a flowchart stop leads to if a student stops
// there. Leaving an ITI or polytechnic midway still leaves them with only
// Class 10, so those stops point to the Class 10 routes.
function stoppedAtOf(node: FlowNode) {
  if (["polycet", "iti_eng", "iti_non", "diploma", "iticeng", "iticnon"].includes(node.id)) return "class_10";
  return ({ 1: "class_10", 2: "intermediate", 3: "entrance_exam", 4: "degree" } as const)[node.col];
}

const TILE_KEYS = new Set(["Full name", "Duration", "Field", "Entry via", "When to start"]);
const SECTION_ORDER = ["About", "Eligibility", "When to start", "Exams", "How to apply", "Applications", "Exam dates", "Admits into", "Leads to", "Govt / Private", "Next", "Next step", "Entry via"];
const SECTION: Record<string, { title: string; icon: React.ReactNode }> = {
  "About": { title: "About", icon: ICON.info },
  "Eligibility": { title: "Who can apply", icon: ICON.person },
  "When to start": { title: "When to start", icon: ICON.clock },
  "Exams": { title: "Exams to take", icon: ICON.list },
  "How to apply": { title: "How to apply", icon: ICON.pen },
  "Applications": { title: "When to apply", icon: ICON.calendar },
  "Exam dates": { title: "Exam dates", icon: ICON.calendar },
  "Admits into": { title: "Gets you into", icon: ICON.arrow },
  "Leads to": { title: "Where it leads", icon: ICON.arrow },
  "Govt / Private": { title: "Government & private options", icon: ICON.building },
  "Next": { title: "What comes next", icon: ICON.flag },
  "Next step": { title: "After this", icon: ICON.flag },
  "Duration": { title: "Duration", icon: ICON.clock },
  "Field": { title: "Field", icon: ICON.list },
  "Entry via": { title: "Entry via", icon: ICON.arrow },
};

function StopDetails({
  node, detail, title, careerKind, stopNo, region, lineColor, wide, onClose,
}: {
  node?: FlowNode; detail?: NodeDetail; title: string; careerKind: string | null;
  stopNo: number; region: string; lineColor: string; wide?: boolean; onClose?: () => void;
}) {
  const kind = careerKind ?? (node ? KIND[node.col] : "");
  const rows = (detail?.rows ?? []).filter(([k, v]) => !(k === "Full name" && v === title));
  const isCourse = node?.col === 4;
  // Short facts (duration, field...) become tiles across the top; the rest are
  // sections of points, in the order a student asks about them.
  const isTile = ([k, v]: [string, string]) => TILE_KEYS.has(k) && v.length <= 60;
  const tiles = rows.filter(isTile);
  const sections = rows.filter((r) => !isTile(r))
    .sort((a, b) => (SECTION_ORDER.indexOf(a[0]) + 99) % 99 - (SECTION_ORDER.indexOf(b[0]) + 99) % 99);
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
      {node && (
        <Link href={`/second-chance?from=${stoppedAtOf(node)}`} className="inline-flex items-center gap-1.5 self-start text-[15px] font-semibold no-underline" style={{ color: "var(--accent)" }}>
          If you stop here: ways back →
        </Link>
      )}
    </div>
  );
  const source = detail?.source && (
    <p className="m-0 text-xs leading-relaxed" style={{ color: "var(--muted)", overflowWrap: "anywhere" }}>
      Source: <Fact text={detail.source} />
    </p>
  );

  const body = (
    <div className="flex min-w-0 flex-col gap-8">
      {tiles.length > 0 && (
        <dl className="m-0 grid grid-cols-2 gap-2.5 sm:grid-cols-3">
          {tiles.map(([k, v]) => (
            <div key={k} className="flex flex-col gap-1 rounded-2xl px-4 py-3" style={{ background: "var(--surface)" }}>
              <dt className="text-[12px] font-bold tracking-wider uppercase" style={{ color: "var(--muted)" }}>{SECTION[k]?.title ?? k}</dt>
              <dd className="m-0 text-[15px] leading-snug font-semibold" style={{ color: "var(--ink)" }}>{v}</dd>
            </div>
          ))}
        </dl>
      )}
      {sections.length > 0 && (
        <div className={`grid gap-x-10 gap-y-7 ${wide ? "xl:grid-cols-2" : ""}`}>
          {sections.map(([k, v]) => {
            const s = SECTION[k] ?? { title: k, icon: ICON.info };
            return (
              <PointSection
                key={k} title={s.title} icon={s.icon} color={lineColor} text={v}
                badge={(k === "Applications" || k === "Exam dates") && NOT_ANNOUNCED.test(v) ? "Next dates not announced" : null}
              />
            );
          })}
        </div>
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
