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
import { Fold, ICON, PointList, PointSection, SubjectList } from "./fact-points";
import PageHead from "./page-head";
import Icon from "./icon";

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
const STOP_COLOR: Record<number, string> = { 1: "#475569", 2: "#2563eb", 3: "#c2410c", 4: "#0f766e" };

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
  const lineColor = active?.color ?? "#4f46e5";

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
          style={{ background: state === k ? "var(--chip-on)" : "var(--surface)", color: state === k ? "var(--chip-on-ink)" : "var(--ink)" }}
        >
          {STATES[k].name}
        </a>
      ))}
    </div>
  );


  const subOf = (s: string) => nodeById[s]?.sub ?? (careerById[s] ? clusterName(careerById[s].cl) : "");

  const lineHeader = active && (
    <div className="flex flex-col gap-3">
      <span className="flex items-center gap-2 self-start text-[14px] font-medium" style={{ color: lineColor }}>
        <Icon name={active.cl} size={18} />
        {clusterName(active.cl)}
      </span>
      <h1 className="m-0 text-[28px] leading-tight font-bold tracking-tight lg:text-[38px]" style={{ textWrap: "balance" }}>
        Class 10 to {nameOf(active.id)}
      </h1>
      <p className="m-0 text-[15px]" style={{ color: "var(--muted)" }}>{meta}</p>
      {!route && (
        <p className="m-0 max-w-2xl text-[15px] leading-relaxed" style={{ color: "var(--soft)" }}>
          No single course on this chart leads here. The details below explain the route.
        </p>
      )}
    </div>
  );

  const otherRoutesList = otherRoutes.length > 0 && (
    <section className="flex flex-col gap-4">
      <h2 className="m-0 text-[20px] font-bold">Other ways to get here</h2>
      <div className="grid gap-x-10 gap-y-5 lg:grid-cols-2">
        {otherRoutes.map((r) => {
          const mid = r.stops.filter((s) => s !== "start" && !careerById[s]);
          return (
            <button
              key={r.stops.join(">")}
              onClick={() => { setVia(mid.find((s) => !route?.stops.includes(s)) ?? null); setStop(null); }}
              className="metro-row flex cursor-pointer flex-col gap-3 rounded-xl border-0 p-4 text-left"
              style={{ background: "var(--panel)", boxShadow: "inset 0 0 0 1px var(--line)", color: "var(--ink)", fontFamily: "inherit" }}
            >
              <span className="text-[15px] font-semibold">Through {mid.map(nameOf).join(", then ")}</span>
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
    <>
    <PageHead title="Career map">
      Every career is a line from Class 10. Pick a field, then a line to see its stops.
    </PageHead>
    <div className="mx-auto flex w-full max-w-[1100px] flex-col gap-8 px-5 pt-8 pb-12 lg:px-12">
      <div className="hidden lg:block">
        <FlowMenuBar menus={menus} current={new Set()} onChoose={(id) => (careerById[id] ? openLine(id) : openStep(id))} />
      </div>
      <div className="flex flex-wrap items-center gap-x-6 gap-y-4">
        {stateMenu}
        <FlowchartSearch items={searchIndex} onChoose={openLine} />
      </div>
      <section aria-labelledby="field-q" className="flex flex-col gap-4">
        <h2 id="field-q" className="m-0 text-[20px] font-bold lg:text-[22px]">Which field interests you?</h2>
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
                className={`metro-step flex min-h-[104px] cursor-pointer flex-col items-start gap-2 rounded-xl border-0 p-4 text-left ${lone ? "col-span-2 lg:col-span-1" : ""}`}
                style={{
                  background: on ? "var(--accent-soft)" : "var(--panel)", color: "var(--ink)", fontFamily: "inherit",
                  boxShadow: `inset 0 0 0 ${on ? 2 : 1}px ${on ? "var(--accent)" : "var(--line)"}`,
                }}
              >
                <span style={{ color: f.color }}><Icon name={f.id} size={22} /></span>
                <span className="text-[16px] leading-snug font-semibold">{f.name}</span>
                <span className="text-[14px]" style={{ color: "var(--muted)" }}>
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
            <h2 id="field-h" className="m-0 text-[20px] font-bold lg:text-[22px]">{shownField.name}</h2>
            <span className="text-[16px]" style={{ color: "var(--muted)" }}>{shownField.list.length} lines. Tap one to see its stops.</span>
          </div>
          <nav aria-label={`${shownField.name} careers`} className="grid gap-2 lg:grid-cols-2 xl:grid-cols-3">
            {shownField.list.map((c) => {
              const r = routesOf[c.id]?.[0];
              const mid = r ? r.stops.filter((s) => s !== "start" && !careerById[s]).map(nameOf) : [];
              return (
                <button
                  key={c.id}
                  onClick={() => openLine(c.id)}
                  className="metro-step flex min-h-16 cursor-pointer items-center gap-3 rounded-xl border-0 px-4 py-3 text-left"
                  style={{ background: "var(--panel)", boxShadow: "inset 0 0 0 1px var(--line)", color: "var(--ink)", fontFamily: "inherit" }}
                >
                  <span className="flex min-w-0 flex-1 flex-col gap-0.5">
                    <span className="text-[16px] leading-snug font-semibold">{chipOf[c.id] ?? c.label}</span>
                    <span className="text-sm leading-snug" style={{ color: "var(--muted)" }}>
                      {mid.length ? mid.join(" → ") : "Straight from Class 10"}
                    </span>
                  </span>
                  <span className="shrink-0" style={{ color: "var(--muted)" }}><Icon name="chevronRight" size={18} /></span>
                </button>
              );
            })}
          </nav>
        </section>
      )}
    </div>
    </>
  );

  // ---------- phone: a vertical timeline of expandable step cards ----------

  const phoneRoute = active && (
    <div className="flex flex-col gap-7 px-4 pt-4 pb-10 lg:hidden">
      <button
        onClick={() => { setCareerId(null); setVia(null); setStop(null); }}
        className="inline-flex min-h-11 cursor-pointer items-center gap-1.5 self-start border-0 bg-transparent p-0 text-[15px] font-medium"
        style={{ color: "var(--accent)", fontFamily: "inherit" }}
      >
        <Icon name="arrowLeft" size={18} /> All careers
      </button>
      {lineHeader}
      <ol aria-label="Steps" className="m-0 flex list-none flex-col p-0">
        {stops.map((s, i) => {
          const last = i === stops.length - 1;
          const open = stop === s;
          const alts = route && s !== "start" && !careerById[s] ? alternativesAt(routes, route, s, 3) : [];
          return (
            <li key={s} className="grid grid-cols-[32px_minmax(0,1fr)] gap-x-3">
              <span className="relative flex justify-center">
                {!last && <span aria-hidden className="absolute top-8 bottom-0 w-0.5" style={{ background: "var(--line)" }} />}
                <span
                  aria-hidden
                  className="relative mt-3 grid h-8 w-8 place-items-center rounded-full text-[13px] font-semibold"
                  style={last
                    ? { background: "var(--ok)", color: "#fff" }
                    : open ? { background: "var(--accent)", color: "#fff" } : { background: "var(--panel)", color: "var(--ink)", boxShadow: "inset 0 0 0 1px var(--line)" }}
                >
                  {last ? <Icon name="check" size={16} /> : i + 1}
                </span>
              </span>
              <div className={last ? "" : "pb-3"}>
                <div className="overflow-hidden rounded-xl" style={{ background: "var(--panel)", boxShadow: `inset 0 0 0 ${open ? 2 : 1}px ${open ? "var(--accent)" : "var(--line)"}` }}>
                  <button
                    onClick={() => setStop(open ? null : s)}
                    aria-expanded={open}
                    aria-controls={`step-${s}`}
                    className="flex min-h-14 w-full cursor-pointer items-center gap-3 border-0 bg-transparent px-4 py-3 text-left"
                    style={{ color: "var(--ink)", fontFamily: "inherit" }}
                  >
                    <span className="flex min-w-0 flex-1 flex-col gap-0.5">
                      <span className="text-[13px]" style={{ color: "var(--muted)" }}>{timeline.labels[i]} · {careerById[s] ? "Career" : KIND[col(s)]}</span>
                      <span className="text-[17px] leading-snug font-semibold">{nameOf(s)}</span>
                      {subOf(s) && <span className="text-[14px] leading-snug" style={{ color: "var(--muted)" }}>{subOf(s)}</span>}
                    </span>
                    <span className="shrink-0 transition-transform duration-200" style={{ transform: open ? "rotate(180deg)" : undefined, color: "var(--muted)" }}>
                      <Icon name="chevronDown" size={20} />
                    </span>
                  </button>
                  {open && (
                    <div id={`step-${s}`} className="flex flex-col gap-6 px-4 pt-2 pb-5" style={{ borderTop: "1px solid var(--line)" }}>
                      <StopDetails
                        node={nodeById[s]} detail={data.details[s]} title={nameOf(s)}
                        careerKind={careerById[s] ? `Career · ${clusterName(careerById[s].cl)}` : null}
                        stopNo={i + 1} region={STATES[state].short} lineColor={lineColor} compact
                      />
                    </div>
                  )}
                </div>
                {alts.length > 0 && (
                  <div className="flex flex-wrap items-center gap-x-3 gap-y-1 px-1 pt-2 text-[14px]">
                    <span style={{ color: "var(--muted)" }}>Or instead:</span>
                    {alts.map((a) => (
                      <button key={a} onClick={() => changeTo(a)} className="inline-flex min-h-9 cursor-pointer items-center gap-1 border-0 bg-transparent p-0 font-medium" style={{ color: "var(--accent)", fontFamily: "inherit" }}>
                        {nameOf(a)} <Icon name="arrowRight" size={14} />
                      </button>
                    ))}
                  </div>
                )}
              </div>
            </li>
          );
        })}
      </ol>
      {otherRoutesList}
    </div>
  );

  // ---------- desktop: steps as columns, left to right, details below ----------

  const desktop = active && (
    <div className="mx-auto hidden max-w-[1280px] flex-col gap-8 px-8 pt-4 pb-14 lg:flex">
      <nav aria-label="Career map menus" className="flex flex-wrap items-center gap-x-5 gap-y-3 pb-4" style={{ borderBottom: "1px solid var(--line)" }}>
        <button
          onClick={() => { setCareerId(null); setVia(null); setStop(null); }}
          className="metro-chip inline-flex h-10 cursor-pointer items-center gap-1.5 rounded-lg border-0 bg-transparent px-3 text-[14px] font-medium"
          style={{ color: "var(--accent)", fontFamily: "inherit" }}
        >
          <Icon name="arrowLeft" size={16} /> All careers
        </button>
        <FlowMenuBar menus={menus} current={new Set(stops)} onChoose={(id) => (careerById[id] ? openLine(id) : openStep(id))} />
        <FlowchartSearch items={searchIndex} onChoose={openLine} />
      </nav>

      <section className="flex flex-wrap items-end justify-between gap-6">
        {lineHeader}
        {stateMenu}
      </section>

      <ol aria-label="Steps" className="m-0 flex list-none items-stretch gap-0 overflow-x-auto p-0 pb-1">
        {stops.map((s, i) => {
          const last = i === stops.length - 1;
          const isSel = s === selected;
          const alts = route && s !== "start" && !careerById[s] ? alternativesAt(routes, route, s, 3) : [];
          return (
            <li key={s} className="flex min-w-[190px] flex-1 items-stretch">
              <div className="flex min-w-0 flex-1 flex-col gap-2">
                <button
                  onClick={() => pickStop(s, false)}
                  aria-pressed={isSel}
                  className="metro-step flex min-h-[132px] w-full cursor-pointer flex-col items-start gap-1.5 rounded-xl border-0 p-4 text-left"
                  style={{
                    background: isSel ? "var(--accent-soft)" : "var(--panel)", color: "var(--ink)", fontFamily: "inherit",
                    boxShadow: `inset 0 0 0 ${isSel ? 2 : 1}px ${isSel ? "var(--accent)" : "var(--line)"}`,
                  }}
                >
                  <span className="flex w-full items-center justify-between gap-2 text-[13px]" style={{ color: "var(--muted)" }}>
                    <span>Step {i + 1} · {careerById[s] ? "Career" : KIND[col(s)]}</span>
                    {last && <span style={{ color: "var(--ok)" }}><Icon name="check" size={16} /></span>}
                  </span>
                  <span className="text-[17px] leading-snug font-semibold">{nameOf(s)}</span>
                  {subOf(s) && <span className="text-[14px] leading-snug" style={{ color: "var(--muted)" }}>{subOf(s)}</span>}
                  <span className="mt-auto pt-2 text-[13px] font-medium" style={{ color: "var(--soft)" }}>{timeline.labels[i]}</span>
                </button>
                {alts.length > 0 && (
                  <div className="flex flex-col items-start gap-0.5 px-1 text-[13px]">
                    <span style={{ color: "var(--muted)" }}>Or instead:</span>
                    {alts.map((a) => (
                      <button key={a} onClick={() => changeTo(a)} title={`Switch the route to go through ${nameOf(a)}`} className="inline-flex min-h-8 cursor-pointer items-center gap-1 border-0 bg-transparent p-0 text-left font-medium" style={{ color: "var(--accent)", fontFamily: "inherit" }}>
                        {nameOf(a)} <Icon name="arrowRight" size={13} />
                      </button>
                    ))}
                  </div>
                )}
              </div>
              {!last && (
                <span aria-hidden className="flex w-9 shrink-0 items-start justify-center pt-[54px]" style={{ color: "var(--muted)" }}>
                  <Icon name="chevronRight" size={22} />
                </span>
              )}
            </li>
          );
        })}
      </ol>

      {selected && (
        <section ref={panelRef} aria-label={`${nameOf(selected)} details`} className="flex min-w-0 flex-col gap-8 rounded-2xl p-8" style={{ background: "var(--panel)", boxShadow: "inset 0 0 0 1px var(--line)", scrollMarginTop: "calc(var(--nav-h) + 16px)" }}>
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
      {careerId ? <>{phoneRoute}{desktop}</> : start}
      <p className={`mx-auto px-4 pb-10 text-[14px] leading-relaxed lg:px-8 ${careerId ? "max-w-[1280px]" : "max-w-[1100px]"}`} style={{ color: "var(--muted)" }}>
        Always check the current official notification before applying.
      </p>
    </div>
  );
}

function MiniLine({ stops, color, nameOf }: { stops: string[]; color: string; nameOf: (id: string) => string }) {
  return (
    <span className="relative grid" style={{ gridTemplateColumns: `repeat(${stops.length}, minmax(0, 1fr))` }}>
      <span className="absolute top-[7px] h-1.5 rounded" style={{ left: 10, right: `calc(${100 / stops.length}% - 10px)`, background: color }} />
      {stops.map((s) => (
        <span key={s} className="relative flex flex-col gap-2 pr-2 text-xs leading-tight font-semibold" style={{ color: "var(--soft)", overflowWrap: "anywhere" }}>
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
  node, detail, title, careerKind, stopNo, region, lineColor, wide, compact,
}: {
  node?: FlowNode; detail?: NodeDetail; title: string; careerKind: string | null;
  stopNo: number; region: string; lineColor: string; wide?: boolean; compact?: boolean;
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
      {!compact && (
        <div className="flex flex-col gap-1">
          <span className="text-[13px]" style={{ color: "var(--muted)" }}>Step {stopNo} · {kind}</span>
          <h2 className="m-0 text-[26px] leading-tight font-bold tracking-tight">{title}</h2>
        </div>
      )}
      {node?.full && node.full.length < 160 && <p className="m-0 text-[16px] leading-snug" style={{ color: "var(--soft)" }}>{node.full}</p>}
      {detail?.note && <p className="m-0 rounded-lg px-4 py-3 text-[14px] leading-relaxed" style={{ background: "var(--warn-bg)", color: "var(--warn-ink)", boxShadow: "inset 0 0 0 1px var(--warn-line)" }}>{detail.note}</p>}
      {!detail && <p className="m-0 text-sm" style={{ color: "var(--muted)" }}>Details for this stop haven’t been added yet.</p>}
      {node && (
        <Link href={`/second-chance?from=${stoppedAtOf(node)}`} className="link inline-flex items-center gap-1.5 self-start text-[15px]">
          If you stop here: ways back <Icon name="arrowRight" size={15} />
        </Link>
      )}
    </div>
  );
  const source = detail?.source && (
    <p className="m-0 text-xs leading-relaxed" style={{ color: "var(--muted)", overflowWrap: "anywhere" }}>
      Source: <Fact text={detail.source} />
    </p>
  );

  // The first four sections show; everything longer folds away until tapped.
  const main = sections.slice(0, 4);
  const more = sections.slice(4);
  const body = (
    <div className="flex min-w-0 flex-col gap-8">
      {tiles.length > 0 && (
        <dl className="m-0 grid grid-cols-2 gap-2 sm:grid-cols-3">
          {tiles.map(([k, v]) => (
            <div key={k} className="flex flex-col gap-1 rounded-2xl px-4 py-3" style={{ background: "var(--surface)" }}>
              <dt className="text-[14px] font-semibold" style={{ color: "var(--muted)" }}>{SECTION[k]?.title ?? k}</dt>
              <dd className="m-0 text-[17px] leading-snug font-semibold" style={{ color: "var(--ink)" }}>{v}</dd>
            </div>
          ))}
        </dl>
      )}
      {main.length > 0 && (
        <div className={`grid gap-x-10 gap-y-7 ${wide ? "xl:grid-cols-2" : ""}`}>
          {main.map(([k, v]) => {
            const s = SECTION[k] ?? { title: k, icon: ICON.info };
            return (
              <PointSection
                key={k} title={s.title} icon={s.icon} color={lineColor} text={v}
                badge={(k === "Applications" || k === "Exam dates") && NOT_ANNOUNCED.test(v) ? "Not announced yet" : null}
              />
            );
          })}
        </div>
      )}
      <div className="flex flex-col gap-2">
        {more.map(([k, v]) => (
          <Fold key={k} title={SECTION[k]?.title ?? k}>
            <PointList text={v} color={lineColor} full />
          </Fold>
        ))}
        {detail?.jobs && (
          <Fold title="Jobs you can do" meta="AI-assisted list">
            <PointList text={detail.jobs} color={lineColor} full />
          </Fold>
        )}
        {node?.col === 3 && detail && (
          <Fold title="Syllabus" meta={detail.subjects?.length ? `${detail.subjects.length} subjects` : "not added yet"}>
            <SubjectList subjects={detail.subjects ?? []} color={lineColor} empty="The syllabus for this exam hasn’t been added yet." />
          </Fold>
        )}
        {isCourse && (
          <Fold title={`Colleges in ${region}`} meta={detail?.colleges?.length ? `${detail.colleges.length} listed` : "none listed yet"}>
            {detail?.colleges?.length ? (
              <ul className="m-0 grid list-none gap-x-8 gap-y-2 p-0 sm:grid-cols-2">
                {detail.colleges.map((c) => (
                  <li key={c.name} className="flex flex-col text-[16px]">
                    {c.name}
                    {c.ownership && <span className="text-[14px]" style={{ color: "var(--muted)" }}>{c.ownership}</span>}
                  </li>
                ))}
              </ul>
            ) : (
              <p className="m-0 text-[16px]" style={{ color: "var(--muted)" }}>No {region} colleges listed for this course yet.</p>
            )}
          </Fold>
        )}
        {isCourse && (
          <Fold title="What you’ll study" meta={detail?.topics?.length ? `${detail.topics.length} topics, AI-assisted` : "being added"}>
            {detail?.topics?.length ? (
              <>
                <ol className="m-0 flex list-none flex-col gap-2 p-0">
                  {detail.topics.map((t, i) => (
                    <li key={t.name} className="flex gap-3 text-[16px]">
                      <span className="w-5 shrink-0 font-bold" style={{ color: lineColor }}>{i + 1}</span>
                      {t.name}
                    </li>
                  ))}
                </ol>
                <span className="text-[14px]" style={{ color: "var(--muted)" }}>Topic guide is AI-assisted. Check your college’s syllabus.</span>
              </>
            ) : (
              <p className="m-0 text-[16px]" style={{ color: "var(--muted)" }}>Study topics for this course are being added.</p>
            )}
          </Fold>
        )}
      </div>
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
