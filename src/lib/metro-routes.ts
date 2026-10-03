// Routes for the "metro" flowchart (/flowchart): every way from Class 10 to a
// career, read off the chart's existing connections (EDGES and CAREER_LINKS
// in class10-flow-data.ts), so the routes grow with the data rather than
// being drawn by hand. Client-safe: no `pg` import.

import { CAREER_LINKS, col, EDGES, type FlowNode } from "./class10-flow-data";

export type Route = {
  stops: string[]; // node ids from "start" to the career id, in order
  dashed: number; // alternate / lateral connections used
};

type Link = { f: string; t: string; dash: boolean; only?: string[] };

// Each career is drawn in its field's colour.
export const CLUSTER_COLOR: Record<string, string> = {
  cl_eng: "#5b9cf0",
  cl_med: "#ef6f8e",
  cl_com: "#f0b44c",
  cl_gov: "#a78bfa",
  cl_def: "#4fc3a1",
  cl_des: "#67d4e8",
  cl_sci: "#9bd36a",
  cl_skl: "#e8875a",
  cl_oth: "#9aa3b2",
};

export const careerCluster = (name: string) => CAREER_LINKS[name]?.cl ?? "cl_oth";

// Every route to the career over this state's cards, best first: fewest
// alternate connections, then the best stream fit, then fewest stops, then
// the chart's own order.
export function routesTo(careerId: string, careerName: string, nodes: FlowNode[]): Route[] {
  const has = new Set(nodes.map((n) => n.id));
  const pars: Record<string, Link[]> = {};
  const add = (e: Link) => (pars[e.t] = pars[e.t] || []).push(e);
  EDGES.filter((e) => has.has(e.f) && has.has(e.t)).forEach(add);
  (CAREER_LINKS[careerName]?.from ?? [])
    .filter((f) => has.has(f))
    .forEach((f) => add({ f, t: careerId, dash: col(f) === 3 }));

  const out: Route[] = [];
  // Walk up from the career to "start". `course` is the course on the route
  // so far: an edge with `only` (MPC → AP EAPCET leads on to B.Tech and
  // B.Pharm, not Agriculture) only counts towards those courses.
  const walk = (id: string, path: string[], dashed: number, course: string | null) => {
    if (id === "start") {
      out.push({ stops: [...path].reverse(), dashed });
      return;
    }
    if (path.length > 7) return;
    for (const e of pars[id] ?? []) {
      if (path.includes(e.f)) continue;
      if (e.only && course && !e.only.includes(course)) continue;
      walk(e.f, [...path, e.f], dashed + (e.dash ? 1 : 0), col(e.f) === 4 ? e.f : course);
    }
  };
  walk(careerId, [careerId], 0, null);

  // Between equally direct routes, prefer the one whose first stop suits the
  // course: a BA through HEC rather than MEC, B.Com through MEC, not MPC.
  const st = Object.fromEntries(nodes.map((n) => [n.id, n.st]));
  const fit = (r: Route) => {
    const first = r.stops.find((s) => col(s) === 2);
    const course = [...r.stops].reverse().find((s) => col(s) === 4);
    if (!first || !course) return 0;
    const a = st[first], c = st[course];
    return a.every((x) => c.includes(x)) ? 0 : a.some((x) => c.includes(x)) ? 1 : 2;
  };
  const order = new Map(out.map((r, i) => [r, i]));
  return out.sort(
    (a, b) => a.dashed - b.dashed || fit(a) - fit(b) || a.stops.length - b.stops.length || order.get(a)! - order.get(b)!,
  );
}

// The route to show: the best one through `via` (a stop the student switched
// to), else the best one overall.
export const pickRoute = (routes: Route[], via: string | null) =>
  (via && routes.find((r) => r.stops.includes(via))) || routes[0] || null;

// Other stops a student can take instead of `stop`: the same kind of step
// (column) on another route to this career, best route first.
export function alternativesAt(routes: Route[], current: Route, stop: string, max = 3): string[] {
  const c = col(stop);
  const seen = new Set(current.stops);
  const alts: string[] = [];
  for (const r of routes) {
    for (const s of r.stops) {
      if (col(s) === c && !seen.has(s) && !alts.includes(s)) alts.push(s);
    }
  }
  return alts.slice(0, max);
}

// Years from a "Duration" value, only when it's one clear number at the
// start ("2 years (Class 11 + 12)", "5.5 years"); ranges and lists like
// "1-2 years" or "2, 3, or 3.5 years" give null, so nothing is guessed.
export function years(duration: string | undefined): number | null {
  const m = duration?.match(/^\s*(\d+(?:\.\d+)?)\s*years?\b/i);
  return m ? Number(m[1]) : null;
}

export const fmtYears = (n: number) => (Number.isInteger(n) ? String(n) : `${Math.floor(n)}½`);
