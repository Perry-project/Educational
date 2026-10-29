"use client";

import { useEffect, useLayoutEffect, useMemo, useRef, useState, type CSSProperties } from "react";
import "./metro-flow.css";
import { CAREER_LINKS, CLUSTER_DEFS, EDGES, col, nodesFor, STATES, type FlowNode, type StateKey } from "@/lib/class10-flow-data";
import type { FlowchartData } from "@/lib/flowchart-db";
import { careerCluster, CLUSTER_COLOR, routesTo } from "@/lib/metro-routes";
import FlowchartSearch, { type SearchItem } from "./flowchart-search";
import PageHead from "./page-head";
import Icon from "./icon";
import { StopDetails } from "./metro-flow";

// The /flowchart page: a flowchart you build by tapping. It starts with
// Class 10 and the choices after it; tapping a choice opens its next steps
// beside it (desktop) or below it (phones), joined by connector lines, until
// a career. Boxes show only a name; a step's details open only when asked
// (the "Details" button under a chosen step, or tapping a career).
// Steps and connections come from class10-flow-data.ts, details from Postgres.
//
// The URL keeps ?path= (or ?career=, which opens that career's main route)
// so a route can be shared.

type Career = { id: string; name: string; label: string; cl: string; color: string };
type Kid = { id: string; dash: boolean };
type Box = { x: number; y: number; w: number; h: number };

const isCareer = (id: string) => id.startsWith("career_");
const shortName = (name: string) => name.replace(/(\s*\([^)]*\))+\s*$/, "") || name;
const KIND = (id: string) =>
  id === "start" ? "Starting point" : isCareer(id) ? "Career" : ({ 2: "After Class 10", 3: "Entrance exam", 4: "Course" } as Record<number, string>)[col(id)] ?? "Step";

export default function FlowChart({
  data, initial, bodyFont,
}: {
  data: FlowchartData;
  initial: { career: string | null; stop: string | null; via: string | null; step: string | null; field: string | null; path?: string | null };
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

  // What comes after a step. `prev` matters where a connection only leads to
  // some courses (Intermediate MPC → AP EAPCET leads on to B.Tech and
  // B.Pharm, not Agriculture).
  const childrenOf = useMemo(() => {
    const has = new Set(nodes.map((n) => n.id));
    return (id: string, prev: string | null): Kid[] => {
      if (isCareer(id)) return [];
      const only = prev ? EDGES.find((e) => e.f === prev && e.t === id && e.only)?.only : undefined;
      const seen = new Set<string>();
      const steps: Kid[] = [];
      for (const e of EDGES) {
        if (e.f !== id || !has.has(e.t) || seen.has(e.t)) continue;
        if (only && col(e.t) === 4 && !only.includes(e.t)) continue;
        seen.add(e.t);
        steps.push({ id: e.t, dash: e.dash });
      }
      const jobs = careers
        .filter((c) => CAREER_LINKS[c.name]?.from.includes(id))
        .map((c) => ({ id: c.id, dash: col(id) === 3 }));
      return [...steps.sort((a, b) => Number(a.dash) - Number(b.dash)), ...jobs];
    };
  }, [nodes, careers]);

  // Opening path from the URL: ?path=, else a career's main route, else Class 10.
  const [path, setPath] = useState<string[]>(() => {
    const fromUrl = initial.path?.split(",").filter(Boolean) ?? [];
    if (fromUrl[0] === "start" && fromUrl.every((id, i) => i === 0 || childrenOf(fromUrl[i - 1], fromUrl[i - 2] ?? null).some((k) => k.id === id))) return fromUrl;
    const c = initial.career && careerById[`career_${initial.career}`];
    if (c) {
      const r = routesTo(c.id, c.name, nodes)[0];
      if (r) return r.stops;
    }
    return ["start"];
  });
  const [detailsOf, setDetailsOf] = useState<string | null>(() => (initial.career && careerById[`career_${initial.career}`] ? `career_${initial.career}` : null));

  // The levels on screen: Class 10, then the choices after each chosen step.
  const levels = useMemo(() => {
    const out: { parent: string | null; kids: Kid[] }[] = [{ parent: null, kids: [{ id: "start", dash: false }] }];
    path.forEach((id, i) => {
      const kids = childrenOf(id, path[i - 1] ?? null);
      if (kids.length) out.push({ parent: id, kids });
    });
    return out;
  }, [path, childrenOf]);

  const choose = (level: number, id: string) => {
    tapped.current = true;
    // Level n holds the choices after path[n-1]; choosing one replaces the rest of the path.
    if (path[level] === id && path.length === level + 1 && !isCareer(id) && level > 0) {
      setPath(path.slice(0, level)); // tapping the chosen step again closes it
      return;
    }
    const next = [...path.slice(0, level), id];
    setPath(next);
    if (isCareer(id)) setDetailsOf(id);
    else if (detailsOf && !next.includes(detailsOf)) setDetailsOf(null);
  };

  // ---------- desktop: measure boxes, draw connectors ----------
  const [wide, setWide] = useState(false);
  useEffect(() => {
    const mq = window.matchMedia("(min-width: 1024px)");
    const on = () => setWide(mq.matches);
    on();
    mq.addEventListener("change", on);
    return () => mq.removeEventListener("change", on);
  }, []);

  const wrapRef = useRef<HTMLDivElement>(null);
  const scrollRef = useRef<HTMLDivElement>(null);
  const boxRefs = useRef<Record<string, HTMLElement | null>>({});
  const [geo, setGeo] = useState<{ w: number; h: number; at: Record<string, Box> } | null>(null);
  const key = (level: number, id: string) => `${level}:${id}`;

  useLayoutEffect(() => {
    const wrap = wrapRef.current;
    if (!wrap || !wide) return;
    let frame = 0;
    const measure = () => {
      cancelAnimationFrame(frame);
      frame = requestAnimationFrame(() => {
        const o = wrap.getBoundingClientRect();
        const at: Record<string, Box> = {};
        for (const [k, el] of Object.entries(boxRefs.current)) {
          if (!el || !el.isConnected) continue;
          const r = el.getBoundingClientRect();
          at[k] = { x: r.left - o.left, y: r.top - o.top, w: r.width, h: r.height };
        }
        setGeo({ w: wrap.scrollWidth, h: wrap.scrollHeight, at });
      });
    };
    measure();
    const ro = new ResizeObserver(measure);
    ro.observe(wrap);
    return () => { ro.disconnect(); cancelAnimationFrame(frame); };
  }, [levels, wide]);

  // After a tap, the new column slides into view (desktop) or the new
  // choices scroll up (phones). Not on first load: a shared link opens as is.
  const depth = levels.length;
  const tapped = useRef(false);
  useEffect(() => {
    if (!tapped.current) return;
    if (wide) scrollRef.current?.scrollTo({ left: scrollRef.current.scrollWidth, behavior: "smooth" });
    else document.getElementById("fc-choices")?.scrollIntoView({ behavior: "smooth", block: "nearest" });
  }, [depth, path, wide]);

  // ---------- URL, keyboard ----------
  useEffect(() => {
    const url = new URL(window.location.href);
    if (path.length > 1) url.searchParams.set("path", path.join(","));
    else url.searchParams.delete("path");
    ["career", "stop", "via", "step", "field"].forEach((k) => url.searchParams.delete(k));
    window.history.replaceState(window.history.state, "", url);
  }, [path]);

  useEffect(() => {
    if (!detailsOf) return;
    const onKey = (e: KeyboardEvent) => e.key === "Escape" && setDetailsOf(null);
    window.addEventListener("keydown", onKey);
    if (!wide) {
      const prev = document.body.style.overflow;
      document.body.style.overflow = "hidden";
      return () => { window.removeEventListener("keydown", onKey); document.body.style.overflow = prev; };
    }
    return () => window.removeEventListener("keydown", onKey);
  }, [detailsOf, wide]);

  // ---------- search: jump straight to a career's main route ----------
  const searchIndex = useMemo<SearchItem[]>(
    () => careers.map((c) => ({
      id: c.id, label: c.label, kind: CLUSTER_DEFS.find((d) => d.id === c.cl)?.name ?? "Career", color: c.color,
      text: [c.name, ...new Set(routesTo(c.id, c.name, nodes).flatMap((r) => r.stops).map((s) => nodeById[s]?.label ?? ""))].join(" ").toLowerCase(),
    })),
    [careers, nodes, nodeById],
  );
  const openCareer = (id: string) => {
    const c = careerById[id];
    const r = c && routesTo(c.id, c.name, nodes)[0];
    setPath(r ? r.stops : ["start", id]);
    setDetailsOf(id);
  };

  const labelOf = (id: string) => nodeById[id]?.label ?? careerById[id]?.label ?? id;
  const fieldName = (cl: string) => CLUSTER_DEFS.find((d) => d.id === cl)?.name ?? "Other routes";
  const rootStyle = { "--metro-body": bodyFont, "--metro-display": bodyFont, fontFamily: bodyFont } as CSSProperties;
  const stateHref = (k: StateKey) => (k === "ts" ? "/flowchart?state=ts" : "/flowchart");
  const heading = (i: number) => (i === 0 ? "Start" : i === 1 ? "After Class 10" : `After ${labelOf(levels[i].parent!)}`);

  // ---------- one box ----------
  const box = (level: number, k: Kid) => {
    const id = k.id;
    const chosen = path[level] === id;
    const career = careerById[id];
    const start = id === "start";
    const faded = !chosen && path.length > level && !start;
    return (
      <button
        key={id}
        ref={(el) => { boxRefs.current[key(level, id)] = el; }}
        onClick={() => choose(level, id)}
        aria-pressed={chosen}
        className="fc-node flex w-full cursor-pointer items-center gap-3 rounded-xl border-0 px-4 text-left"
        style={{
          minHeight: 56,
          background: start ? "var(--ink)" : chosen ? "var(--accent)" : "var(--panel)",
          color: start || chosen ? "#fff" : "var(--ink)",
          boxShadow: start || chosen ? "none" : "0 0 0 1px var(--line), 0 1px 2px rgba(15,23,42,.04)",
          opacity: faded ? 0.55 : 1,
          fontFamily: "inherit",
        }}
      >
        {career && <span aria-hidden className="h-2.5 w-2.5 shrink-0 rounded-full" style={{ background: chosen ? "#fff" : career.color }} />}
        <span className="min-w-0 flex-1 text-[15px] leading-snug font-semibold">{start ? "Class 10 pass" : labelOf(id)}</span>
        {!career && !start && (
          <span className="shrink-0" style={{ opacity: chosen ? 0.9 : 0.45 }}><Icon name={wide ? "chevronRight" : "chevronDown"} size={18} /></span>
        )}
      </button>
    );
  };

  // The choices of an open level, split into next steps and careers.
  const groupsOf = (kids: Kid[]) => {
    const steps = kids.filter((k) => !isCareer(k.id)), jobs = kids.filter((k) => isCareer(k.id));
    return [
      { title: steps.length && jobs.length ? "Next step" : null, kids: steps },
      { title: steps.length && jobs.length ? "Careers" : null, kids: jobs },
    ].filter((g) => g.kids.length);
  };
  const changeButton = (level: number) => (
    <button onClick={() => { setPath(path.slice(0, level)); setDetailsOf(null); }}
      className="inline-flex min-h-10 cursor-pointer items-center border-0 bg-transparent px-1 text-[14px] font-medium"
      style={{ color: "var(--muted)", fontFamily: "inherit" }}>
      Change
    </button>
  );

  const detailsButton = (id: string) =>
    id !== "start" && (
      <button
        onClick={() => setDetailsOf(id)}
        className="inline-flex min-h-10 cursor-pointer items-center gap-1.5 self-start border-0 bg-transparent px-1 text-[14px] font-semibold"
        style={{ color: "var(--accent)", fontFamily: "inherit" }}
      >
        <Icon name="info" size={16} /> Details
      </button>
    );

  const connectors = wide && geo && (
    <svg className="pointer-events-none absolute top-0 left-0" width={geo.w} height={geo.h} aria-hidden style={{ overflow: "visible" }}>
      <defs>
        <marker id="fc-a" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#cbd5e1" /></marker>
        <marker id="fc-a-on" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#4f46e5" /></marker>
      </defs>
      {levels.slice(1).flatMap((lv, i) => {
        const level = i + 1;
        const s = geo.at[key(level - 1, lv.parent!)];
        if (!s) return [];
        return [...lv.kids].sort((a, b) => Number(path[level] === a.id) - Number(path[level] === b.id)).map((k) => {
          const t = geo.at[key(level, k.id)];
          if (!t) return null;
          const on = path[level] === k.id;
          const sx = s.x + s.w, sy = s.y + s.h / 2, tx = t.x - 3, ty = t.y + t.h / 2, c = (tx - sx) / 2;
          return (
            <path
              key={`${level}:${k.id}`} d={`M${sx},${sy} C${sx + c},${sy} ${tx - c},${ty} ${tx},${ty}`} fill="none"
              stroke={on ? "#4f46e5" : "#cbd5e1"} strokeWidth={on ? 2.5 : 1.5} strokeDasharray={k.dash ? "5 5" : undefined}
              markerEnd={`url(#${on ? "fc-a-on" : "fc-a"})`}
            />
          );
        });
      })}
    </svg>
  );

  // ---------- the details of one step ----------
  const details = detailsOf && (() => {
    const career = careerById[detailsOf];
    const node = nodeById[detailsOf];
    return (
      <div className="flex flex-col gap-6">
        <div className="flex items-start gap-3">
          <div className="flex min-w-0 flex-1 flex-col gap-1">
            <span className="text-[13px] font-medium" style={{ color: career ? career.color : "var(--muted)" }}>
              {career ? fieldName(career.cl) : KIND(detailsOf)}
            </span>
            <h2 className="m-0 text-[22px] leading-tight font-bold tracking-tight">{labelOf(detailsOf)}</h2>
            {node?.full && node.full !== node.label && <p className="m-0 text-[14px]" style={{ color: "var(--muted)" }}>{node.full}</p>}
          </div>
          <button onClick={() => setDetailsOf(null)} aria-label="Close details" className="metro-chip grid h-10 w-10 shrink-0 cursor-pointer place-items-center rounded-lg border-0" style={{ background: "var(--surface)", color: "var(--ink)" }}>
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" aria-hidden><path d="M6 6l12 12M18 6L6 18" /></svg>
          </button>
        </div>
        <StopDetails
          node={node} detail={data.details[detailsOf]} title={labelOf(detailsOf)}
          careerKind={career ? `Career · ${fieldName(career.cl)}` : null}
          stopNo={1} region={STATES[state].short} lineColor={career?.color ?? "#4f46e5"} compact
        />
      </div>
    );
  })();

  return (
    <div className="metro min-h-[calc(100vh-var(--nav-h))]" style={rootStyle}>
      <PageHead title="Career map" width={1280}>
        Start at Class 10 and tap a step to see where it leads.
      </PageHead>

      <div className="mx-auto flex max-w-[1280px] flex-wrap items-center gap-3 px-4 pt-6 sm:px-6 lg:px-8">
        <div role="group" aria-label="State" className="flex rounded-lg p-0.5" style={{ background: "var(--surface)" }}>
          {(Object.keys(STATES) as StateKey[]).map((k) => (
            <a key={k} href={stateHref(k)} aria-current={state === k ? "page" : undefined}
              className="inline-flex h-9 items-center rounded-md px-3 text-[14px] font-medium no-underline"
              style={state === k ? { background: "var(--panel)", color: "var(--ink)", boxShadow: "0 0 0 1px var(--line)" } : { color: "var(--muted)" }}>
              {STATES[k].name}
            </a>
          ))}
        </div>
        <div className="min-w-[220px] flex-1 lg:max-w-[360px]">
          <FlowchartSearch items={searchIndex} onChoose={openCareer} />
        </div>
        {path.length > 1 && (
          <button onClick={() => { setPath(["start"]); setDetailsOf(null); }}
            className="metro-chip inline-flex h-9 cursor-pointer items-center gap-1.5 rounded-lg border-0 px-3 text-[14px] font-medium"
            style={{ background: "var(--panel)", color: "var(--soft)", boxShadow: "inset 0 0 0 1px var(--line)", fontFamily: "inherit" }}>
            <Icon name="rotate" size={15} /> Start over
          </button>
        )}
      </div>

      {wide ? (
        // ---------- desktop: columns left to right ----------
        <div
          ref={scrollRef}
          className="metro-scroll overflow-x-auto pt-8 pb-14"
          style={{ paddingLeft: "max(32px, calc((100vw - 1280px) / 2 + 32px))", paddingRight: detailsOf ? 480 : 32 }}
        >
          <div ref={wrapRef} className="relative flex w-max items-start gap-[56px]">
            {connectors}
            {levels.map((lv, level) => {
              const chosen = path[level];
              return (
                <section key={level} aria-label={heading(level)} className="relative flex w-[208px] shrink-0 flex-col gap-3.5">
                  <h2 className="m-0 mb-1 truncate text-[13px] font-medium" style={{ color: "var(--muted)" }}>{heading(level)}</h2>
                  {chosen ? (
                    <div className="flex flex-col">
                      {box(level, { id: chosen, dash: false })}
                      {level > 0 && (
                        <div className="flex items-center justify-between">
                          {isCareer(chosen) ? <span /> : detailsButton(chosen)}
                          {changeButton(level)}
                        </div>
                      )}
                    </div>
                  ) : (
                    groupsOf(lv.kids).map((g) => (
                      <div key={g.title ?? "all"} className="flex flex-col gap-3.5">
                        {g.title && <h3 className="m-0 mt-2 text-[12px] font-semibold tracking-wide uppercase" style={{ color: "var(--muted)" }}>{g.title}</h3>}
                        {g.kids.map((k) => box(level, k))}
                      </div>
                    ))
                  )}
                </section>
              );
            })}
          </div>
        </div>
      ) : (
        // ---------- phones: chosen steps stacked, the current choices below ----------
        <div className="mx-auto max-w-[560px] px-4 pt-7 pb-12">
          <ol className="m-0 flex list-none flex-col p-0">
            {levels.map((lv, level) => {
              const chosen = path[level];
              const open = !chosen;
              const shown = open ? lv.kids : lv.kids.filter((k) => k.id === chosen);
              return (
                <li key={level} id={open && level > 0 ? "fc-choices" : undefined} className="flex flex-col" style={{ scrollMarginTop: "calc(var(--nav-h) + 12px)" }}>
                  {level > 0 && (
                    <span aria-hidden className="flex flex-col items-center py-1.5" style={{ color: "#a5b4fc" }}>
                      <span className="h-7 w-0.5" style={{ background: "#a5b4fc" }} />
                      <Icon name="chevronDown" size={18} strokeWidth={2.5} />
                    </span>
                  )}
                  {open && level > 0 && (
                    <h2 className="m-0 mb-3 text-center text-[14px] font-medium" style={{ color: "var(--muted)" }}>
                      {level === 1 ? "Choose what comes after Class 10" : `After ${labelOf(lv.parent!)}, choose one`}
                    </h2>
                  )}
                  {open ? (
                    <div className="flex flex-col gap-3">
                      {groupsOf(shown).map((g) => (
                        <div key={g.title ?? "all"} className="flex flex-col gap-3">
                          {g.title && <h3 className="m-0 mt-2 text-[12px] font-semibold tracking-wide uppercase" style={{ color: "var(--muted)" }}>{g.title}</h3>}
                          {g.kids.map((k) => box(level, k))}
                        </div>
                      ))}
                    </div>
                  ) : (
                    shown.map((k) => (
                      <div key={k.id} className="flex flex-col">
                        {box(level, k)}
                        {level > 0 && (
                          <div className="flex items-center justify-between px-1">
                            {isCareer(k.id) ? <span /> : detailsButton(k.id)}
                            {changeButton(level)}
                          </div>
                        )}
                      </div>
                    ))
                  )}
                </li>
              );
            })}
          </ol>
        </div>
      )}

      <p className="mx-auto mt-0 max-w-[1280px] px-4 pb-10 text-[14px] sm:px-6 lg:px-8" style={{ color: "var(--muted)" }}>
        Solid lines are the usual route, dashed lines another way in. Always check the official notification before applying.
      </p>

      {/* ---------- details: side panel on desktop, bottom sheet on phones ---------- */}
      {details && (
        wide ? (
          <aside aria-label={`${labelOf(detailsOf!)} details`} className="metro-scroll fixed right-0 bottom-0 z-[90] w-[440px] overflow-y-auto p-6"
            style={{ top: "var(--nav-h)", background: "var(--panel)", borderLeft: "1px solid var(--line)", boxShadow: "-12px 0 32px -16px rgba(15,23,42,.18)" }}>
            {details}
          </aside>
        ) : (
          <div className="fixed inset-0 z-[120]">
            <button aria-label="Close details" onClick={() => setDetailsOf(null)} className="absolute inset-0 cursor-default border-0" style={{ background: "rgba(15,23,42,0.45)" }} />
            <section role="dialog" aria-modal="true" aria-label={`${labelOf(detailsOf!)} details`}
              className="metro-sheet absolute inset-x-0 bottom-0 max-h-[82vh] overflow-y-auto rounded-t-2xl px-5 pt-3"
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
