"use client";

import { useCallback, useEffect, useLayoutEffect, useMemo, useRef, useState, type CSSProperties, type ReactNode } from "react";
import "./class10-flow.css";
import {
  buildGraph, byId, col, NODES,
  type FlowNode, type StreamKey,
} from "@/lib/class10-flow-data";
import type { FlowchartData } from "@/lib/flowchart-db";
import DetailsPanel, { type Panel } from "./flowchart-panel";
import FlowchartSearch, { type SearchItem } from "./flowchart-search";

// Port of the Claude Design project "Class 10 to Career.dc.html", in the
// site's dark theme.
//
// Layouts:
//   - wide (>= STACK_BELOW px): five columns joined by connector lines; the
//     chart scales down to fit narrower windows instead of scrolling sideways,
//     and makes room for the details panel on the right when one is open.
//   - stacked (< STACK_BELOW px, phones and portrait tablets): columns become
//     steps one under another, cards flow into a grid, and details open as a
//     bottom sheet.
//
// Picking a step highlights every route through it. In focus mode (the
// default) steps off those routes are hidden, so the whole route fits on
// screen; on wide screens "Show all steps" dims them instead. The selected
// step is kept in the URL (?step=btech) so a route can be shared.

const KIND: Record<number, string> = { 1: "Starting point", 2: "Pathway after Class 10", 3: "Entrance exam", 4: "Course" };
const CHIPS: [StreamKey | null, string][] = [
  [null, "All streams"], ["sci", "Science"], ["com", "Commerce"], ["hum", "Humanities"], ["voc", "Vocational"],
];
// Narrowest the five-column grid can be: 150px start column, four 200px
// columns and four 64px gaps. Below this it's scaled down, not squeezed.
const CHART_W = 150 + 4 * 200 + 4 * 64;
const STACK_BELOW = 1024;
const PANEL_W = 368;
const NAV_H = 64;
const ROUTE_BAR_H = 56;

const stepDot = (n: number, size: number): CSSProperties => ({
  width: size, height: size, flex: "none", borderRadius: "50%", background: `var(--c${n})`,
  color: n === 1 ? "var(--startfg)" : "var(--surface)",
  display: "grid", placeItems: "center", fontSize: size > 24 ? 13 : 11, fontWeight: 700,
});

const pillBtn: CSSProperties = {
  whiteSpace: "nowrap", height: 36, padding: "0 14px", borderRadius: 999, border: "1px solid var(--line)",
  background: "var(--surface)", color: "var(--ink)", font: "inherit", fontSize: 13, fontWeight: 600, cursor: "pointer",
};

type Rect = { l: number; r: number; y: number };

export default function Class10Flow({
  data, fontFamily, initialStep,
}: {
  data: FlowchartData;
  fontFamily: string;
  initialStep: string | null;
}) {
  const { CL, clById, crById, DRAW, kids, pars, nameOf, routeSet } = useMemo(() => buildGraph(data.careers), [data.careers]);
  const known = (id: string | null) => !!id && (!!byId[id] || !!crById[id] || !!clById[id]);
  const firstStep = known(initialStep) ? initialStep : null;

  const [sel, setSel] = useState<string | null>(firstStep);
  const [panelOpen, setPanelOpen] = useState(!!firstStep);
  const [focus, setFocus] = useState(true);
  const [filter, setFilter] = useState<StreamKey | null>(null);
  const [open, setOpen] = useState<Record<string, boolean>>(() =>
    firstStep && crById[firstStep] ? { [crById[firstStep].cl.id]: true } : {});
  const [geo, setGeo] = useState<{ paths: Record<number, string>; gw: number; gh: number }>({ paths: {}, gw: 0, gh: 0 });
  const [rootW, setRootW] = useState(0);
  const [ih, setIh] = useState(0);

  const rootRef = useRef<HTMLDivElement>(null);
  const chartRef = useRef<HTMLDivElement>(null);
  const innerRef = useRef<HTMLDivElement>(null);
  const geoKey = useRef("");
  const scrollTo = useRef<string | null>(firstStep);
  const panelOpenRef = useRef(panelOpen);
  useEffect(() => { panelOpenRef.current = panelOpen; }, [panelOpen]);

  const stacked = rootW > 0 && rootW < STACK_BELOW;
  // Width the chart can use. With the panel open, the chart shrinks to make
  // room for it unless that would scale it below 75% - then the panel
  // overlaps the chart instead.
  const base = Math.min(rootW, 1720) - 56;
  const withPanel = base - PANEL_W - 32;
  const reserve = !stacked && !!sel && panelOpen && withPanel / CHART_W >= 0.75;
  const fit = stacked || !rootW ? 1 : Math.min(1, (reserve ? withPanel : base) / CHART_W);

  const measure = useCallback(() => {
    const c = chartRef.current;
    if (!c) return;
    const cr = c.getBoundingClientRect(), R: Record<string, Rect> = {};
    c.querySelectorAll<HTMLElement>("[data-nid]").forEach((el) => {
      const r = el.getBoundingClientRect();
      if (r.width) R[el.dataset.nid!] = { l: (r.left - cr.left) / fit, r: (r.right - cr.left) / fit, y: (r.top - cr.top + r.height / 2) / fit };
    });
    setIh(innerRef.current ? innerRef.current.offsetHeight : 0);
    const f = (v: number) => v.toFixed(1);
    // Right-angle connector with rounded corners, turning at x.
    const orth = (sx: number, sy: number, x: number, tx: number, ty: number) => {
      const dy = ty - sy, r = Math.min(7, Math.abs(dy) / 2), sgx = Math.sign(x - sx) || 1, tgx = Math.sign(tx - x) || 1;
      if (Math.abs(dy) < 1) return `M${f(sx)} ${f(sy)} H${f(tx)}`;
      const sg = Math.sign(dy);
      return `M${f(sx)} ${f(sy)} H${f(x - sgx * r)} Q${f(x)} ${f(sy)} ${f(x)} ${f(sy + sg * r)} V${f(ty - sg * r)} Q${f(x)} ${f(ty)} ${f(x + tgx * r)} ${f(ty)} H${f(tx)}`;
    };
    const paths: Record<number, string> = {};
    DRAW.forEach((e, i) => {
      const a = R[e.f], b = R[e.t];
      if (!a || !b) return;
      // Backward edges (e.g. Diploma → AP ECET) loop round the target's right side.
      paths[i] = col(e.f) > col(e.t)
        ? orth(a.l, a.y, b.r + (e.dash ? 20 : 28), b.r, b.y)
        : orth(a.r, a.y, a.r + (e.dash ? 40 : 24), b.l, b.y);
    });
    const next = { paths, gw: c.scrollWidth, gh: c.scrollHeight };
    const key = JSON.stringify(next);
    if (key !== geoKey.current) {
      geoKey.current = key;
      setGeo(next);
    }
  }, [fit, DRAW]);

  const clearRoute = useCallback(() => { setSel(null); setPanelOpen(false); }, []);

  // Escape closes the details panel first, then clears the route.
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key !== "Escape") return;
      if (panelOpenRef.current) setPanelOpen(false);
      else clearRoute();
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [clearRoute]);

  useEffect(() => {
    const onResize = () => {
      setRootW(rootRef.current ? rootRef.current.offsetWidth : window.innerWidth);
      measure();
    };
    onResize();
    let ro: ResizeObserver | null = null;
    if (typeof ResizeObserver !== "undefined") {
      ro = new ResizeObserver(onResize);
      [rootRef, chartRef].forEach((r) => r.current && ro!.observe(r.current));
    } else {
      window.addEventListener("resize", onResize);
    }
    document.fonts?.ready.then(measure);
    return () => { ro?.disconnect(); window.removeEventListener("resize", onResize); };
  }, [measure]);

  // Re-measure after every render: card positions depend on filter, open
  // clusters, focus mode and panel width.
  useLayoutEffect(() => {
    const raf = requestAnimationFrame(measure);
    return () => cancelAnimationFrame(raf);
  });

  // Keep the selected step in the URL so the route can be shared.
  useEffect(() => {
    const url = new URL(window.location.href);
    if (sel) url.searchParams.set("step", sel);
    else url.searchParams.delete("step");
    window.history.replaceState(window.history.state, "", url);
  }, [sel]);

  // After a search pick (or opening a shared link), bring the step into view.
  useEffect(() => {
    const id = scrollTo.current;
    if (!id || !rootW) return;
    scrollTo.current = null;
    const el = document.querySelector(`[data-nid="${id}"], [data-cid="${id}"]`);
    el?.scrollIntoView({ block: "center", behavior: "smooth" });
  });

  const pick = (id: string) => {
    if (id === sel) { clearRoute(); return; }
    setSel(id);
    setPanelOpen(true);
  };
  const toggleCl = (id: string) => {
    const o = !open[id];
    setOpen({ ...open, [id]: o });
    if (o) pick(id);
    else if (sel === id) clearRoute();
  };
  const choose = (id: string) => {
    if (crById[id]) setOpen((o) => ({ ...o, [crById[id].cl.id]: true }));
    setFilter(null);
    setSel(id);
    setPanelOpen(true);
    scrollTo.current = id;
  };

  const set = sel ? routeSet(sel) : null;
  const selCol = sel ? col(sel) : 0;
  const hideOff = stacked || focus; // hide (rather than dim) steps off the route
  const vis = (n: { st: StreamKey[] }) => !filter || n.st.includes(filter);

  const cardState = (n: FlowNode) => {
    const inS = !set || set.has(n.id);
    return {
      hidden: !vis(n) || (!!set && !inS && hideOff),
      opacity: set && !inS ? 0.26 : 1,
      boxShadow: sel === n.id ? `0 0 0 2px var(--c${n.col}), 0 8px 20px -10px var(--c${n.col})` : "none",
    };
  };

  const renderCards = (k: 2 | 3 | 4) => {
    let shown = 0;
    const els = NODES.filter((n) => n.col === k).map((n) => {
      const cs = cardState(n);
      // With a route selected, columns count the steps on it.
      if (!cs.hidden && (!set || set.has(n.id))) shown++;
      return (
        <button
          key={n.id}
          data-nid={n.id}
          onClick={() => pick(n.id)}
          aria-pressed={sel === n.id}
          className={`c10-card c10-card-${k}`}
          style={{
            display: cs.hidden ? "none" : "flex", opacity: cs.opacity, boxShadow: cs.boxShadow,
            flexDirection: "column", gap: 3, width: "100%", minHeight: 44, textAlign: "left", padding: "9px 11px",
            borderRadius: 10, border: `1px solid var(--c${k}b)`, background: `var(--c${k}t)`, color: "var(--ink)",
            font: "inherit", cursor: "pointer", transition: "opacity .2s,box-shadow .15s",
          }}
        >
          <span style={{ fontWeight: 700, fontSize: 14, lineHeight: 1.25 }}>{n.label}</span>
          <span style={{ fontSize: 12, color: "var(--muted)", lineHeight: 1.3 }}>{n.sub}</span>
        </button>
      );
    });
    return { els, shown };
  };

  const pathways = renderCards(2), exams = renderCards(3), courses = renderCards(4);

  const clusters = CL.map((cl) => {
    const cs = cl.items.filter(vis), inS = set ? cs.filter((c) => set.has(c.id)) : cs;
    const isOpen = !!open[cl.id] || !!(set && selCol >= 4 && inS.length);
    const hidden = !cs.length || (!!set && hideOff && !inS.length);
    return { cl, cs, inS, isOpen, hidden };
  });
  const counts = {
    p: pathways.shown, e: exams.shown, c: courses.shown,
    k: clusters.reduce((sum, c) => sum + (c.hidden ? 0 : c.inS.length), 0),
  };

  let edgesSvg: ReactNode = null;
  if (!stacked) {
    const on = (e: (typeof DRAW)[number]) =>
      e.cl
        ? set!.has(e.f) && e.cl.items.some((c) => set!.has(c.id) && c.from.includes(e.f))
        : set!.has(e.f) && set!.has(e.t);
    const paths = DRAW.map((e, i) => {
      const g = geo.paths[i];
      if (!g) return null;
      const hl = !!set && on(e);
      return { i, g, e, hl, dim: !!set && !hl };
    })
      .filter((p): p is NonNullable<typeof p> => !!p)
      .sort((a, b) => Number(a.hl) - Number(b.hl));
    edgesSvg = (
      <svg width={geo.gw} height={geo.gh} aria-hidden style={{ position: "absolute", left: 0, top: 0, pointerEvents: "none", overflow: "visible", zIndex: 0 }}>
        {paths.map((p) => (
          <path
            key={p.i}
            d={p.g}
            fill="none"
            style={{
              stroke: p.hl ? `var(--c${col(p.e.t)})` : "var(--edge)",
              strokeWidth: p.hl ? 2.2 : 1.2,
              strokeDasharray: p.e.dash ? "5 4" : "none",
              opacity: p.dim ? 0.1 : p.hl ? 1 : p.e.dash ? 0.5 : 0.75,
              transition: "opacity .2s",
            }}
          />
        ))}
      </svg>
    );
  }

  // Details for the selected step.
  let panel: Panel | null = null;
  const detail = sel ? data.details[sel] : undefined;
  const fromDb = {
    rows: detail?.rows ?? [], source: detail?.source ?? null,
    colleges: detail?.colleges ?? [], topics: detail?.topics ?? [],
  };
  if (sel && byId[sel]) {
    const n = byId[sel];
    panel = {
      kind: KIND[n.col], label: n.label, full: n.full, accent: `var(--c${n.col})`, ...fromDb, isCourse: n.col === 4,
      note: detail ? "" : "Details for this step haven’t been added yet.",
      from: (pars[sel] || []).map((e) => ({ id: e.f, dash: e.dash })),
      to: (kids[sel] || []).map((e) => ({ id: e.t, dash: e.dash })),
      fromTitle: "Comes from", toTitle: n.col === 4 ? "Careers" : "Leads to",
    };
  } else if (sel && crById[sel]) {
    const c = crById[sel];
    panel = {
      kind: "Career · " + c.cl.name, label: c.label, full: "", accent: "var(--c5)", ...fromDb, isCourse: false,
      // Drop the full-name row when it only repeats the heading.
      rows: fromDb.rows.filter(([k, v]) => k !== "Full name" || v !== c.label),
      note: c.from.length ? "" : "No single course on this chart leads here. See “When to start” and “Exams” above for the route.",
      from: c.from.map((f) => ({ id: f, dash: col(f) === 3 })), to: [],
      fromTitle: "Reached through", toTitle: "",
    };
  } else if (sel && clById[sel]) {
    const cl = clById[sel];
    panel = {
      kind: "Career cluster", label: cl.name, full: `${cl.items.length} careers`, accent: "var(--c5)", note: "",
      rows: [], source: null, colleges: [], topics: [], isCourse: false,
      from: [...new Set(cl.items.flatMap((c) => c.from))].map((f) => ({ id: f, dash: col(f) === 3 })),
      to: cl.items.map((c) => ({ id: c.id, dash: false })),
      fromTitle: "Reached through", toTitle: "Careers",
    };
  }

  const searchIndex = useMemo<SearchItem[]>(() => {
    const kinds: Record<number, string> = { 1: "Start", 2: "After Class 10", 3: "Entrance exam", 4: "Course" };
    const careerName = new Map(data.careers.map((c) => [`career_${c.id}`, c.name]));
    return [
      ...NODES.map((n) => ({
        id: n.id, label: n.label, kind: kinds[n.col], color: `var(--c${n.col})`,
        text: [n.label, n.sub, n.full, n.db ?? ""].join(" ").toLowerCase(),
      })),
      ...Object.values(crById).map((c) => ({
        id: c.id, label: c.label, kind: "Career", color: "var(--c5)",
        text: [c.label, careerName.get(c.id) ?? ""].join(" ").toLowerCase(),
      })),
      ...CL.map((cl) => ({ id: cl.id, label: cl.name, kind: "Career field", color: "var(--c5)", text: cl.name.toLowerCase() })),
    ];
  }, [data.careers, crById, CL]);

  const colHeads: [number, string, number | null][] = [[1, "Start", null], [2, "After Class 10", counts.p], [3, "Entrance exams", counts.e], [4, "Courses", counts.c], [5, "Careers", counts.k]];
  const stackedHead = (n: number) => {
    if (!stacked) return null;
    const [, title, count] = colHeads[n - 1];
    return (
      <>
        <h2 style={{ margin: 0, display: "flex", alignItems: "center", gap: 10 }}>
          <span style={stepDot(n, 28)}>{n}</span>
          <span style={{ fontWeight: 700, fontSize: 16 }}>{title}</span>
          {count !== null && <span style={{ color: "var(--muted)", fontSize: 14, fontWeight: 500 }}>{count}</span>}
        </h2>
        {set && count === 0 && (
          <p style={{ margin: 0, fontSize: 13, color: "var(--muted)" }}>No step here on this route.</p>
        )}
      </>
    );
  };
  const colWrap: CSSProperties = { position: "relative", zIndex: 1, display: "flex", flexDirection: "column", gap: 10, minWidth: 0 };
  const listCols = stacked ? "repeat(auto-fill,minmax(min(150px,100%),1fr))" : "minmax(0,1fr)";
  const start = cardState(byId.start);
  const shareUrl = typeof window === "undefined" || !sel ? "" : `${window.location.origin}/flowchart?step=${encodeURIComponent(sel)}`;

  return (
    <div ref={rootRef} className="c10" style={{ color: "var(--ink)", fontFamily }}>
      <div
        style={{
          maxWidth: 1720, margin: "0 auto", boxSizing: "border-box", transition: "padding .2s",
          padding: stacked ? "20px 16px 40px" : "28px 28px 48px", paddingRight: stacked ? 16 : reserve ? PANEL_W + 32 : 28,
        }}
      >
        <header style={{ display: "flex", flexDirection: "column", gap: 8, marginBottom: 20 }}>
          <span style={{ color: "var(--muted)", fontSize: 13, fontWeight: 600, letterSpacing: "0.06em", textTransform: "uppercase" }}>
            Career flowchart · Andhra Pradesh
          </span>
          <h1 style={{ margin: 0, fontSize: "clamp(30px,4vw,42px)", lineHeight: 1.05, fontWeight: 800, letterSpacing: "-0.02em" }}>Class 10 to Career</h1>
          <p style={{ margin: 0, color: "var(--muted)", fontSize: 15, lineHeight: 1.45, maxWidth: 560, textWrap: "pretty" }}>
            Tap any step to see every route through it, from Class 10 to the careers it opens.
          </p>
        </header>

        <div style={{ display: "flex", flexWrap: "wrap", alignItems: "center", gap: "12px 20px", marginBottom: 16 }}>
          <FlowchartSearch items={searchIndex} onChoose={choose} />
          {!stacked && (
            <div style={{ display: "flex", flexWrap: "wrap", alignItems: "center", gap: "8px 14px", fontSize: 12, color: "var(--muted)", marginLeft: "auto" }}>
              <span style={{ display: "flex", alignItems: "center", gap: 6 }}>
                <svg width="26" height="8" aria-hidden><line x1="0" y1="4" x2="26" y2="4" style={{ stroke: "var(--ink)", strokeWidth: 1.6 }} /></svg>Main route
              </span>
              <span style={{ display: "flex", alignItems: "center", gap: 6 }}>
                <svg width="26" height="8" aria-hidden><line x1="0" y1="4" x2="26" y2="4" style={{ stroke: "var(--ink)", strokeWidth: 1.6, strokeDasharray: "4 3" }} /></svg>Alternate / lateral
              </span>
            </div>
          )}
        </div>
        <div style={{ display: "flex", flexWrap: "wrap", gap: 8, marginBottom: 20 }} role="group" aria-label="Filter by stream">
          {CHIPS.map(([k, label]) => {
            const a = filter === k;
            return (
              <button
                key={label}
                onClick={() => setFilter(k)}
                aria-pressed={a}
                className="c10-pill"
                style={{
                  flex: "none", whiteSpace: "nowrap", height: 38, padding: "0 15px", borderRadius: 999,
                  border: `1px solid ${a ? "var(--ink)" : "var(--line)"}`, background: a ? "var(--ink)" : "var(--surface)", color: a ? "var(--bg)" : "var(--ink)",
                  font: "inherit", fontSize: 14, fontWeight: 600, cursor: "pointer", transition: "background .15s,color .15s",
                }}
              >
                {label}
              </button>
            );
          })}
        </div>

        {sel && (
          <div
            role="status"
            className="c10-routebar"
            style={{
              position: "sticky", top: NAV_H, zIndex: 15, minHeight: ROUTE_BAR_H, boxSizing: "border-box", margin: stacked ? "0 -8px 12px" : "0 -8px", padding: "6px 8px",
              display: "flex", flexWrap: "wrap", alignItems: "center", gap: 8,
            }}
          >
            <span style={{ flex: "1 1 160px", minWidth: 0, fontSize: 14, color: "var(--muted)" }}>
              Routes through <strong style={{ color: "var(--ink)" }}>{nameOf(sel)}</strong>
            </span>
            {!panelOpen && <button onClick={() => setPanelOpen(true)} className="c10-pill" style={pillBtn}>Details</button>}
            {!stacked && (
              <button onClick={() => setFocus(!focus)} aria-pressed={!focus} className="c10-pill" style={pillBtn}>
                {focus ? "Show all steps" : "Hide other steps"}
              </button>
            )}
            <button onClick={clearRoute} className="c10-pill" style={pillBtn}>Clear</button>
          </div>
        )}

        {!stacked && (
          // Column headers stay in view while scrolling. They live outside the
          // scaled chart (sticky positioning is unreliable inside a transform)
          // and scale their own contents by the same factor so columns line up.
          <div
            style={{
              position: "sticky", top: NAV_H + (sel ? ROUTE_BAR_H : 0), zIndex: 14, background: "var(--bg)", overflow: "hidden",
              margin: "0 -8px 12px", padding: "10px 8px 10px", borderBottom: "1px solid var(--line)",
            }}
          >
            <div
              style={{
                minWidth: CHART_W, width: fit < 1 ? CHART_W : "auto", transform: fit < 1 ? `scale(${fit})` : "none", transformOrigin: "0 0",
                display: "grid", gridTemplateColumns: "150px repeat(4,minmax(200px,1fr))", columnGap: 64, height: 22 * fit, alignItems: "start",
              }}
            >
              {colHeads.map(([n, title, count]) => (
                <div key={n} style={{ display: "flex", alignItems: "center", gap: 8, fontSize: 13, fontWeight: 700, height: 22 }}>
                  <span style={stepDot(n, 20)}>{n}</span>
                  {title}
                  {count !== null && <span style={{ color: "var(--muted)", fontWeight: 500 }}>{count}</span>}
                </div>
              ))}
            </div>
          </div>
        )}

        <div
          className="c10-clip"
          style={{ margin: "0 -8px", padding: "4px 8px 8px", height: fit < 1 && ih ? Math.ceil(ih * fit) + 12 : "auto" }}
        >
          <div
            ref={innerRef}
            style={{
              minWidth: stacked ? 0 : CHART_W, width: fit < 1 ? CHART_W : "auto",
              transform: fit < 1 ? `scale(${fit})` : "none", transformOrigin: "0 0",
            }}
          >
            <div
              ref={chartRef}
              style={{
                position: "relative", display: stacked ? "flex" : "grid", gridTemplateColumns: "150px repeat(4,minmax(200px,1fr))",
                flexDirection: "column", gap: stacked ? 32 : "0 64px", alignItems: stacked ? "stretch" : "center",
              }}
            >
              {edgesSvg}

              <div style={colWrap}>
                {stackedHead(1)}
                <button
                  data-nid="start"
                  onClick={() => pick("start")}
                  aria-pressed={sel === "start"}
                  className="c10-card"
                  style={{
                    display: start.hidden ? "none" : "flex", boxShadow: start.boxShadow, flexDirection: "column", gap: 4, width: "100%", textAlign: "left",
                    padding: 14, borderRadius: 12, border: 0, background: "var(--c1)", color: "var(--startfg)", font: "inherit", cursor: "pointer",
                  }}
                >
                  <span style={{ fontWeight: 800, fontSize: 16, lineHeight: 1.2 }}>Class 10 Pass</span>
                  <span style={{ fontSize: 12, opacity: 0.8, lineHeight: 1.3 }}>SSC · AP Board</span>
                </button>
              </div>

              {([[2, pathways], [3, exams], [4, courses]] as const).map(([k, group]) => (
                <div key={k} style={colWrap}>
                  {stackedHead(k)}
                  <div style={{ display: "grid", gridTemplateColumns: listCols, gap: 8 }}>{group.els}</div>
                </div>
              ))}

              <div style={colWrap}>
                {stackedHead(5)}
                <div style={{ display: "grid", gridTemplateColumns: stacked ? "repeat(auto-fill,minmax(min(260px,100%),1fr))" : "minmax(0,1fr)", alignItems: "start", gap: 8 }}>
                  {clusters.map(({ cl, cs, inS, isOpen, hidden }) => (
                    <div
                      key={cl.id}
                      style={{
                        display: hidden ? "none" : "flex", opacity: set && !inS.length ? 0.26 : 1, boxShadow: sel === cl.id ? "0 0 0 2px var(--c5)" : "none",
                        flexDirection: "column", border: "1px solid var(--c5b)", background: "var(--c5t)", borderRadius: 12, transition: "opacity .2s",
                      }}
                    >
                      <button
                        data-nid={cl.id}
                        onClick={() => toggleCl(cl.id)}
                        aria-expanded={isOpen}
                        className="c10-card"
                        style={{
                          display: "flex", alignItems: "center", gap: 8, width: "100%", minHeight: 48, padding: "9px 12px", borderRadius: 12,
                          background: "none", border: 0, font: "inherit", color: "var(--ink)", cursor: "pointer", textAlign: "left",
                        }}
                      >
                        <span style={{ flex: 1, display: "flex", flexDirection: "column", gap: 2 }}>
                          <span style={{ fontWeight: 700, fontSize: 14, lineHeight: 1.25 }}>{cl.name}</span>
                          <span style={{ fontSize: 12, color: "var(--muted)" }}>
                            {set ? `${inS.length} of ${cs.length} on this route` : `${cs.length} careers`}
                          </span>
                        </span>
                        <svg
                          width="14" height="14" viewBox="0 0 14 14" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" aria-hidden
                          style={{ flex: "none", transform: isOpen ? "rotate(180deg)" : "none", transition: "transform .2s", color: "var(--c5)" }}
                        >
                          <path d="M3.5 5.5L7 9l3.5-3.5" />
                        </svg>
                      </button>
                      {isOpen && (
                        <div style={{ display: "flex", flexDirection: "column", gap: 2, padding: "0 6px 6px" }}>
                          {cs.map((c) => {
                            const on = !set || set.has(c.id);
                            return (
                              <button
                                key={c.id}
                                data-cid={c.id}
                                onClick={() => pick(c.id)}
                                aria-pressed={sel === c.id}
                                className="c10-career"
                                style={{
                                  display: set && hideOff && !on ? "none" : "flex", opacity: set && !on ? 0.35 : 1,
                                  background: sel === c.id ? "var(--surface)" : "transparent", fontWeight: sel === c.id ? 700 : 500,
                                  alignItems: "center", gap: 8, width: "100%", minHeight: stacked ? 44 : 36, padding: "7px 8px", border: 0, borderRadius: 8,
                                  fontFamily: "inherit", fontSize: 13, color: "var(--ink)", textAlign: "left", cursor: "pointer", transition: "opacity .2s",
                                }}
                              >
                                <span style={{ width: 5, height: 5, borderRadius: "50%", background: "var(--c5)", flex: "none" }} />
                                {c.label}
                              </button>
                            );
                          })}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>

        <p style={{ margin: "36px 0 0", fontSize: 13, color: "var(--muted)", lineHeight: 1.5, maxWidth: 720, textWrap: "pretty" }}>
          Exam windows are typical of recent years, not confirmed dates. Always check eligibility and dates in the current official notification before applying.
        </p>
      </div>

      {panel && panelOpen && (
        <DetailsPanel
          panel={panel}
          stacked={stacked}
          shareUrl={shareUrl}
          onClose={() => setPanelOpen(false)}
          onPick={pick}
          nameOf={nameOf}
        />
      )}
    </div>
  );
}
