"use client";

import { useEffect, useLayoutEffect, useMemo, useRef, useState, type CSSProperties } from "react";
import "./metro-flow.css";
import { CAREER_LINKS, CLUSTER_DEFS, EDGES, col, nodesFor, STATES, type FlowNode, type StateKey } from "@/lib/class10-flow-data";
import type { FlowchartData } from "@/lib/flowchart-db";
import { careerCluster, CLUSTER_COLOR, routesTo, type Route } from "@/lib/metro-routes";
import FlowchartSearch, { type SearchItem } from "./flowchart-search";
import PageHead from "./page-head";
import Icon from "./icon";
import { StopDetails } from "./metro-flow";

// The /flowchart page: a real flowchart of every route from Class 10 to a
// career, drawn from the chart's own connections (class10-flow-data.ts) and
// the careers in Postgres.
//
// Desktop: columns left to right (Class 10 → after Class 10 → entrance exam
// → course → after a degree → career), boxes joined by SVG connectors.
// Phones: the same chart top to bottom, the connectors running down between
// the stages. Tapping a box lights up every route through it and opens its
// details (a side panel on desktop, a bottom sheet on phones). A field
// filter shows only the steps that lead to that field's careers; with all
// fields, the last column holds the fields themselves.
//
// The URL keeps ?field=, ?career= / ?stop= and ?state= so a view can be shared.

type Career = { id: string; name: string; label: string; cl: string; color: string };
type Edge = { f: string; t: string; dash: boolean };
type Box = { x: number; y: number; w: number; h: number };

const LANES = ["Class 10", "After Class 10", "Entrance exam", "Course", "After a degree", "Career"];
// Exams taken after a degree sit in their own column, after the courses.
const AFTER_DEGREE = new Set(["icet", "icar", "cds", "afcat"]);
const KIND = ["Starting point", "After Class 10", "Entrance exam", "Course", "Exam after a degree", "Career"];

const isCareer = (id: string) => id.startsWith("career_");
const isField = (id: string) => id.startsWith("field:");
const laneOf = (id: string) =>
  isCareer(id) || isField(id) ? 5 : id === "start" ? 0 : AFTER_DEGREE.has(id) ? 4 : col(id) === 2 ? 1 : col(id) === 3 ? 2 : 3;
const shortName = (name: string) => name.replace(/(\s*\([^)]*\))+\s*$/, "") || name;

export default function FlowChart({
  data, initial, bodyFont,
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
  const routesOf = useMemo(
    () => Object.fromEntries(careers.map((c) => [c.id, routesTo(c.id, c.name, nodes)])) as Record<string, Route[]>,
    [careers, nodes],
  );

  // Opening view from the URL.
  const initialCareer = initial.career && careerById[`career_${initial.career}`] ? `career_${initial.career}` : null;
  const initialStop = [initial.stop, initial.step].find((s) => s && (nodeById[s] || careerById[s])) ?? null;
  const [field, setField] = useState<string | null>(
    initialCareer ? careerById[initialCareer].cl : CLUSTER_DEFS.some((d) => d.id === initial.field) ? initial.field : null,
  );
  const [focus, setFocus] = useState<string | null>(initialCareer ?? initialStop);
  const [panelOpen, setPanelOpen] = useState(!!(initialCareer ?? initialStop));

  const fields = useMemo(
    () => CLUSTER_DEFS.map((d) => ({ ...d, color: CLUSTER_COLOR[d.id], count: careers.filter((c) => c.cl === d.id).length })).filter((f) => f.count),
    [careers],
  );

  // ---------- the graph on screen ----------
  const graph = useMemo(() => {
    const has = new Set(nodes.map((n) => n.id));
    const base: Edge[] = EDGES.filter((e) => has.has(e.f) && has.has(e.t)).map(({ f, t, dash }) => ({ f, t, dash }));
    const careerEdges = (c: Career): Edge[] =>
      (CAREER_LINKS[c.name]?.from ?? []).filter((f) => has.has(f)).map((f) => ({ f, t: c.id, dash: col(f) === 3 }));

    let ids: string[];
    let edges: Edge[];
    if (field) {
      // Only the steps on a route to one of this field's careers, and only
      // the connections those routes use.
      const list = careers.filter((c) => c.cl === field);
      const on = new Set<string>(["start"]);
      const pairs = new Set<string>();
      for (const c of list) {
        on.add(c.id);
        for (const r of routesOf[c.id]) {
          r.stops.forEach((s) => on.add(s));
          r.stops.slice(1).forEach((s, i) => pairs.add(`${r.stops[i]}>${s}`));
        }
      }
      ids = [...nodes.map((n) => n.id).filter((id) => on.has(id)), ...list.map((c) => c.id)];
      edges = [...base, ...list.flatMap(careerEdges)].filter((e) => pairs.has(`${e.f}>${e.t}`));
    } else {
      // Every step; the last column holds the fields, each joined to the
      // courses and exams its careers come from.
      const seen = new Map<string, Edge>();
      for (const c of careers) {
        for (const e of careerEdges(c)) {
          const k = `${e.f}>field:${c.cl}`;
          const prev = seen.get(k);
          if (!prev || (prev.dash && !e.dash)) seen.set(k, { f: e.f, t: `field:${c.cl}`, dash: e.dash });
        }
      }
      ids = [...nodes.map((n) => n.id), ...fields.map((f) => `field:${f.id}`)];
      edges = [...base, ...seen.values()];
    }

    // Columns, each ordered by where its boxes' parents sit, so fewer lines cross.
    const lanes: string[][] = LANES.map(() => []);
    ids.forEach((id) => lanes[laneOf(id)].push(id));
    const parents: Record<string, string[]> = {};
    edges.forEach((e) => (parents[e.t] = parents[e.t] || []).push(e.f));
    const rank: Record<string, number> = {};
    for (const lane of lanes) {
      const bary = (id: string) => {
        const ps = (parents[id] ?? []).filter((p) => rank[p] !== undefined && laneOf(p) < laneOf(id));
        return ps.length ? ps.reduce((a, p) => a + rank[p], 0) / ps.length : Infinity;
      };
      const order = new Map(lane.map((id, i) => [id, i]));
      lane.sort((a, b) => bary(a) - bary(b) || order.get(a)! - order.get(b)!);
      lane.forEach((id, i) => (rank[id] = i / Math.max(1, lane.length - 1)));
    }
    return { lanes: lanes.map((l, i) => ({ i, ids: l })).filter((l) => l.ids.length), edges };
  }, [nodes, careers, routesOf, field, fields]);

  // If the focused box isn't on this view any more, let it go.
  const visible = useMemo(() => new Set(graph.lanes.flatMap((l) => l.ids)), [graph]);
  const focused = focus && visible.has(focus) ? focus : null;
  const panelShown = panelOpen && !!focused;

  // ---------- what lights up: every route through the focused box ----------
  const lit = useMemo(() => {
    if (!focused) return null;
    const up: Record<string, string[]> = {}, down: Record<string, string[]> = {};
    graph.edges.forEach((e) => {
      (down[e.f] = down[e.f] || []).push(e.t);
      (up[e.t] = up[e.t] || []).push(e.f);
    });
    const walk = (start: string, next: Record<string, string[]>) => {
      const seen = new Set<string>([start]);
      const stack = [start];
      while (stack.length) for (const n of next[stack.pop()!] ?? []) if (!seen.has(n)) { seen.add(n); stack.push(n); }
      return seen;
    };
    const anc = walk(focused, up), desc = walk(focused, down);
    return { boxes: new Set([...anc, ...desc]), edge: (e: Edge) => (anc.has(e.f) && anc.has(e.t)) || (desc.has(e.f) && desc.has(e.t)) };
  }, [focused, graph.edges]);

  // ---------- measuring the boxes to draw the connectors ----------
  const wrapRef = useRef<HTMLDivElement>(null);
  const boxRefs = useRef<Record<string, HTMLElement | null>>({});
  const [geo, setGeo] = useState<{ w: number; h: number; at: Record<string, Box> } | null>(null);
  const [wide, setWide] = useState(false);

  useEffect(() => {
    const mq = window.matchMedia("(min-width: 1024px)");
    const on = () => setWide(mq.matches);
    on();
    mq.addEventListener("change", on);
    return () => mq.removeEventListener("change", on);
  }, []);

  useLayoutEffect(() => {
    const wrap = wrapRef.current;
    if (!wrap) return;
    let frame = 0;
    const measure = () => {
      cancelAnimationFrame(frame);
      frame = requestAnimationFrame(() => {
        const o = wrap.getBoundingClientRect();
        const at: Record<string, Box> = {};
        for (const [id, el] of Object.entries(boxRefs.current)) {
          if (!el || !visible.has(id)) continue;
          const r = el.getBoundingClientRect();
          at[id] = { x: r.left - o.left, y: r.top - o.top, w: r.width, h: r.height };
        }
        setGeo({ w: wrap.scrollWidth, h: wrap.scrollHeight, at });
      });
    };
    measure();
    const ro = new ResizeObserver(measure);
    ro.observe(wrap);
    return () => { ro.disconnect(); cancelAnimationFrame(frame); };
  }, [graph, visible, wide]);

  // With the side panel open, keep the focused box in view beside it.
  useEffect(() => {
    if (!wide || !panelShown || !focused) return;
    const el = boxRefs.current[focused], scroller = wrapRef.current?.parentElement;
    if (!el || !scroller) return;
    const b = el.getBoundingClientRect(), v = scroller.getBoundingClientRect();
    if (b.right > v.right - 16) scroller.scrollBy({ left: b.right - v.right + 48, behavior: "smooth" });
    else if (b.left < v.left) scroller.scrollBy({ left: b.left - v.left - 48, behavior: "smooth" });
  }, [focused, panelShown, wide, geo]);

  const pathOf = (e: Edge) => {
    const s = geo?.at[e.f], t = geo?.at[e.t];
    if (!s || !t) return null;
    if (wide) {
      const sx = s.x + s.w, sy = s.y + s.h / 2, tx = t.x, ty = t.y + t.h / 2;
      const c = Math.max(28, (tx - sx) / 2);
      return `M${sx},${sy} C${sx + c},${sy} ${tx - c},${ty} ${tx - 2},${ty}`;
    }
    const sx = s.x + s.w / 2, sy = s.y + s.h, tx = t.x + t.w / 2, ty = t.y;
    const c = Math.max(24, (ty - sy) / 2);
    return `M${sx},${sy} C${sx},${sy + c} ${tx},${ty - c} ${tx},${ty - 2}`;
  };

  // ---------- URL, keyboard ----------
  useEffect(() => {
    const url = new URL(window.location.href);
    const set = (k: string, v: string | null) => (v ? url.searchParams.set(k, v) : url.searchParams.delete(k));
    set("field", field);
    set("career", focused && isCareer(focused) ? focused.replace("career_", "") : null);
    set("stop", focused && !isCareer(focused) && !isField(focused) ? focused : null);
    url.searchParams.delete("step");
    url.searchParams.delete("via");
    window.history.replaceState(window.history.state, "", url);
  }, [field, focused]);

  useEffect(() => {
    if (!panelShown) return;
    const onKey = (e: KeyboardEvent) => e.key === "Escape" && setPanelOpen(false);
    window.addEventListener("keydown", onKey);
    if (!wide) {
      const prev = document.body.style.overflow;
      document.body.style.overflow = "hidden";
      return () => { window.removeEventListener("keydown", onKey); document.body.style.overflow = prev; };
    }
    return () => window.removeEventListener("keydown", onKey);
  }, [panelShown, wide]);

  const choose = (id: string) => {
    if (isField(id)) {
      setField(id.slice(6));
      setFocus(null);
      setPanelOpen(false);
      return;
    }
    if (focused === id) {
      setPanelOpen(!panelOpen);
      return;
    }
    setFocus(id);
    setPanelOpen(true);
  };
  const clear = () => { setFocus(null); setPanelOpen(false); };

  // Search: careers by name and by every step on their routes ("NEET" finds the medical careers).
  const searchIndex = useMemo<SearchItem[]>(
    () => careers.map((c) => ({
      id: c.id, label: c.label, kind: CLUSTER_DEFS.find((d) => d.id === c.cl)?.name ?? "Career", color: c.color,
      text: [c.name, ...new Set(routesOf[c.id].flatMap((r) => r.stops).map((s) => nodeById[s]?.label ?? ""))].join(" ").toLowerCase(),
    })),
    [careers, routesOf, nodeById],
  );
  const openCareer = (id: string) => {
    setField(careerById[id]?.cl ?? null);
    setFocus(id);
    setPanelOpen(true);
  };

  const labelOf = (id: string) =>
    nodeById[id]?.label ?? careerById[id]?.label ?? fields.find((f) => `field:${f.id}` === id)?.name ?? id;
  const fieldName = (cl: string) => CLUSTER_DEFS.find((d) => d.id === cl)?.name ?? "Other routes";
  const rootStyle = { "--metro-body": bodyFont, "--metro-display": bodyFont, fontFamily: bodyFont } as CSSProperties;
  const stateHref = (k: StateKey) => {
    const q = new URLSearchParams();
    if (k === "ts") q.set("state", "ts");
    if (field) q.set("field", field);
    const s = q.toString();
    return s ? `/flowchart?${s}` : "/flowchart";
  };

  // ---------- one box ----------
  const box = (id: string) => {
    const career = careerById[id];
    const fieldBox = isField(id) ? fields.find((f) => `field:${f.id}` === id) : null;
    const node = nodeById[id];
    const isFocus = id === focused;
    const isLit = !lit || lit.boxes.has(id);
    const color = career?.color ?? fieldBox?.color;
    const routes = career ? routesOf[id].length : 0;
    const sub = node?.sub
      ?? (fieldBox ? `${fieldBox.count} careers` : career ? (routes ? `${routes} ${routes === 1 ? "route" : "routes"} from Class 10` : "Route in details") : "");
    const start = id === "start";
    return (
      <button
        key={id}
        ref={(el) => { boxRefs.current[id] = el; }}
        onClick={() => choose(id)}
        aria-pressed={isFocus}
        aria-label={`${labelOf(id)}${sub ? `, ${sub}` : ""}`}
        className="fc-box relative flex w-full cursor-pointer items-start gap-2.5 rounded-lg border-0 px-3 py-2.5 text-left"
        style={{
          background: isFocus ? "var(--accent-soft)" : start ? "var(--ink)" : "var(--panel)",
          color: start && !isFocus ? "#fff" : "var(--ink)",
          boxShadow: isFocus ? "0 0 0 2px var(--accent)" : lit && isLit ? "0 0 0 1.5px #a5b4fc" : "0 0 0 1px var(--line)",
          opacity: isLit ? 1 : 0.32,
          fontFamily: "inherit",
        }}
      >
        {color && (
          <span className="mt-0.5 shrink-0" style={{ color }}>
            <Icon name={career?.cl ?? fieldBox!.id} size={16} />
          </span>
        )}
        <span className="flex min-w-0 flex-col">
          <span className="text-[14px] leading-snug font-semibold">{labelOf(id)}</span>
          {sub && <span className="line-clamp-1 text-[12.5px] leading-snug" style={{ color: start && !isFocus ? "#cbd5e1" : "var(--muted)" }}>{sub}</span>}
        </span>
      </button>
    );
  };

  // ---------- the details of the focused box ----------
  const details = focused && (() => {
    const career = careerById[focused];
    const node = nodeById[focused];
    const routes = career ? routesOf[focused] : [];
    const best = routes[0];
    const leadsTo = !career ? graph.lanes.flatMap((l) => l.ids).filter((id) => lit?.boxes.has(id) && laneOf(id) === 5) : [];
    return (
      <div className="flex flex-col gap-6">
        <div className="flex items-start gap-3">
          <div className="flex min-w-0 flex-1 flex-col gap-1">
            <span className="flex items-center gap-1.5 text-[13px] font-medium" style={{ color: career ? career.color : "var(--muted)" }}>
              {career && <Icon name={career.cl} size={15} />}
              {career ? fieldName(career.cl) : KIND[laneOf(focused)]}
            </span>
            <h2 className="m-0 text-[22px] leading-tight font-bold tracking-tight">{labelOf(focused)}</h2>
            {node?.full && node.full !== node.label && <p className="m-0 text-[14px]" style={{ color: "var(--muted)" }}>{node.full}</p>}
          </div>
          <button onClick={() => setPanelOpen(false)} aria-label="Close details" className="metro-chip grid h-10 w-10 shrink-0 cursor-pointer place-items-center rounded-lg border-0" style={{ background: "var(--surface)", color: "var(--ink)" }}>
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" aria-hidden><path d="M6 6l12 12M18 6L6 18" /></svg>
          </button>
        </div>

        {career && best && (
          <section className="flex flex-col gap-2 rounded-lg p-4" style={{ background: "var(--bg)", boxShadow: "inset 0 0 0 1px var(--line)" }}>
            <h3 className="m-0 text-[13px] font-semibold" style={{ color: "var(--muted)" }}>
              Main route{routes.length > 1 ? ` · ${routes.length - 1} more highlighted on the chart` : ""}
            </h3>
            <ol className="m-0 flex list-none flex-wrap items-center gap-x-1.5 gap-y-1 p-0 text-[14px] font-medium">
              {best.stops.map((s, i) => (
                <li key={s} className="flex items-center gap-1.5">
                  {i > 0 && <span style={{ color: "var(--muted)" }}><Icon name="chevronRight" size={14} /></span>}
                  {s === "start" ? "Class 10" : labelOf(s)}
                </li>
              ))}
            </ol>
          </section>
        )}
        {!career && leadsTo.length > 0 && (
          <p className="m-0 text-[14px]" style={{ color: "var(--soft)" }}>
            Leads to {leadsTo.length} {field ? (leadsTo.length === 1 ? "career" : "careers") : (leadsTo.length === 1 ? "field" : "fields")} on this chart, highlighted.
          </p>
        )}

        <StopDetails
          node={node} detail={data.details[focused]} title={labelOf(focused)}
          careerKind={career ? `Career · ${fieldName(career.cl)}` : null}
          stopNo={1} region={STATES[state].short} lineColor={career?.color ?? "#4f46e5"} compact
        />
      </div>
    );
  })();

  return (
    <div className="metro min-h-[calc(100vh-var(--nav-h))]" style={rootStyle}>
      <PageHead title="Career map" width={1280}>
        Every route from Class 10 to a career. Tap any box to light up the routes through it.
      </PageHead>

      {/* ---------- controls ---------- */}
      <div className="z-[40] lg:sticky lg:top-[var(--nav-h)]" style={{ background: "rgba(248,250,252,0.97)", borderBottom: "1px solid var(--line)" }}>
        <div className="mx-auto flex max-w-[1280px] flex-col gap-3 px-4 py-3 sm:px-6 lg:px-8">
          <div className="flex flex-wrap items-center gap-3">
            <div role="group" aria-label="State" className="flex rounded-lg p-0.5" style={{ background: "var(--surface)" }}>
              {(Object.keys(STATES) as StateKey[]).map((k) => (
                <a key={k} href={stateHref(k)} aria-current={state === k ? "page" : undefined}
                  className="inline-flex h-9 items-center rounded-md px-3 text-[14px] font-medium no-underline"
                  style={state === k ? { background: "var(--panel)", color: "var(--ink)", boxShadow: "0 0 0 1px var(--line)" } : { color: "var(--muted)" }}>
                  {STATES[k].name}
                </a>
              ))}
            </div>
            <div className="min-w-[220px] flex-1 lg:max-w-[380px]">
              <FlowchartSearch items={searchIndex} onChoose={openCareer} />
            </div>
            {focused && (
              <button onClick={clear} className="metro-chip inline-flex h-9 cursor-pointer items-center gap-1.5 rounded-lg border-0 px-3 text-[14px] font-medium" style={{ background: "var(--panel)", color: "var(--soft)", boxShadow: "inset 0 0 0 1px var(--line)", fontFamily: "inherit" }}>
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round" aria-hidden><path d="M6 6l12 12M18 6L6 18" /></svg>
                Clear highlight
              </button>
            )}
          </div>
          <div role="group" aria-label="Career field" className="metro-fade-x -mx-1 flex gap-1.5 overflow-x-auto px-1 pb-0.5">
            {[{ id: null as string | null, name: "All fields", color: "var(--accent)", count: careers.length }, ...fields].map((f) => {
              const on = field === f.id;
              return (
                <button
                  key={f.id ?? "all"}
                  onClick={() => setField(f.id)}
                  aria-pressed={on}
                  className="metro-chip inline-flex h-9 shrink-0 cursor-pointer items-center gap-1.5 rounded-lg border-0 px-3 text-[14px] font-medium"
                  style={{ background: on ? "var(--accent)" : "var(--panel)", color: on ? "#fff" : "var(--soft)", boxShadow: on ? "none" : "inset 0 0 0 1px var(--line)", fontFamily: "inherit" }}
                >
                  {f.id && <span style={{ color: on ? "#fff" : f.color }}><Icon name={f.id} size={15} /></span>}
                  {f.name}
                </button>
              );
            })}
          </div>
        </div>
      </div>

      {/* ---------- the chart ---------- */}
      <div className="mx-auto max-w-[1280px] px-4 pt-5 pb-10 sm:px-6 lg:px-8" style={{ paddingRight: panelShown && wide ? "max(32px, calc(472px - (100vw - 1280px) / 2))" : undefined }}>
        <div className="mb-4 flex flex-wrap items-center gap-x-5 gap-y-2 text-[13px]" style={{ color: "var(--muted)" }}>
          <span className="flex items-center gap-2">
            <svg width="28" height="6" aria-hidden><path d="M1 3H27" stroke="#94a3b8" strokeWidth="1.6" /></svg> Main route
          </span>
          <span className="flex items-center gap-2">
            <svg width="28" height="6" aria-hidden><path d="M1 3H27" stroke="#94a3b8" strokeWidth="1.6" strokeDasharray="4 3" /></svg> Other route
          </span>
          {!field && <span>Pick a field above, or the last column, to see its careers.</span>}
        </div>

        <div className={wide ? "overflow-x-auto pb-2" : ""}>
          <div ref={wrapRef} className="relative" style={{ minWidth: wide ? graph.lanes.length * 208 - 36 : undefined }}>
            {/* Connectors sit under the boxes. */}
            {geo && (
              <svg className="pointer-events-none absolute top-0 left-0" width={geo.w} height={geo.h} aria-hidden style={{ overflow: "visible" }}>
                <defs>
                  <marker id="fc-arrow" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
                    <path d="M0,0 L8,4 L0,8 z" fill="#94a3b8" />
                  </marker>
                  <marker id="fc-arrow-lit" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
                    <path d="M0,0 L8,4 L0,8 z" fill="#4f46e5" />
                  </marker>
                </defs>
                {[...graph.edges].sort((a, b) => Number(!!lit?.edge(a)) - Number(!!lit?.edge(b))).map((e) => {
                  const d = pathOf(e);
                  if (!d) return null;
                  const on = lit?.edge(e);
                  return (
                    <path
                      key={`${e.f}>${e.t}`} d={d} fill="none"
                      stroke={on ? "#4f46e5" : "#94a3b8"}
                      strokeWidth={on ? 2.2 : 1.3}
                      strokeDasharray={e.dash ? "5 4" : undefined}
                      opacity={lit ? (on ? 1 : 0.12) : field ? 0.8 : 0.35}
                      markerEnd={`url(#${on ? "fc-arrow-lit" : "fc-arrow"})`}
                      style={{ transition: "opacity .2s ease, stroke .2s ease" }}
                    />
                  );
                })}
              </svg>
            )}

            <div className={wide ? "relative flex items-start gap-9" : "relative flex flex-col gap-11"}>
              {graph.lanes.map((lane) => (
                <section key={lane.i} aria-label={LANES[lane.i]} className={wide ? "flex w-[172px] shrink-0 flex-col gap-2.5" : "flex flex-col gap-2.5"}>
                  <h2 className="m-0 flex items-baseline justify-between gap-2 pb-1 text-[12px] font-semibold tracking-wide uppercase" style={{ color: "var(--muted)" }}>
                    {lane.i === 5 && !field ? "Career fields" : LANES[lane.i]}
                    <span className="font-medium normal-case">{lane.ids.length}</span>
                  </h2>
                  <div className={wide ? "flex flex-col gap-2.5" : lane.ids.length === 1 ? "grid grid-cols-1" : "grid grid-cols-2 gap-2"}>
                    {lane.ids.map(box)}
                  </div>
                </section>
              ))}
            </div>
          </div>
        </div>

        <p className="mt-8 mb-0 text-[14px]" style={{ color: "var(--muted)" }}>
          Always check the current official notification before applying.
        </p>
      </div>

      {/* ---------- details: side panel on desktop, bottom sheet on phones ---------- */}
      {panelShown && details && (
        wide ? (
          <aside
            aria-label={`${labelOf(focused!)} details`}
            className="metro-scroll fixed right-0 bottom-0 z-[90] w-[440px] overflow-y-auto p-6"
            style={{ top: "var(--nav-h)", background: "var(--panel)", borderLeft: "1px solid var(--line)", boxShadow: "-12px 0 32px -16px rgba(15,23,42,.18)" }}
          >
            {details}
          </aside>
        ) : (
          <div className="fixed inset-0 z-[120]">
            <button aria-label="Close details" onClick={() => setPanelOpen(false)} className="absolute inset-0 cursor-default border-0" style={{ background: "rgba(15,23,42,0.45)" }} />
            <section role="dialog" aria-modal="true" aria-label={`${labelOf(focused!)} details`}
              className="metro-sheet absolute inset-x-0 bottom-0 max-h-[82vh] overflow-y-auto rounded-t-2xl px-5 pt-3 pb-8"
              style={{ background: "var(--panel)", paddingBottom: "calc(32px + env(safe-area-inset-bottom))" }}>
              <div className="mb-3 flex justify-center"><span className="h-1.5 w-10 rounded-full" style={{ background: "var(--line)" }} /></div>
              {details}
            </section>
          </div>
        )
      )}
    </div>
  );
}
