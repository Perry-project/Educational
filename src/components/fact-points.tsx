"use client";

import { useState, type ReactNode } from "react";

// Turns a database text field into something a student can scan: separate
// points instead of one paragraph, "Govt: ... Private: ..." as labelled
// points, short comma lists as chips, and the numbers that matter (dates,
// percentages, fees, durations) picked out in the text.

// Sentence ends that aren't abbreviations ("Rs.", "e.g.", "No.", "B.Tech." ...).
const ABBREV = /(?:\b(?:Rs|e\.g|i\.e|etc|No|Nos|Dr|St|Sr|Jr|vs|approx|Govt|Dept|Univ|Prof|Mr|Mrs|Ms|viz|incl|max|min)|\b[A-Z])\.$/i;

function splitTopLevel(text: string, sep: RegExp): string[] {
  // Splits on sep only outside brackets, so "(via AP EAPCET, NEET)" stays whole.
  const out: string[] = [];
  let depth = 0, cur = "";
  for (let i = 0; i < text.length; i++) {
    const ch = text[i];
    if (ch === "(" || ch === "[") depth++;
    if ((ch === ")" || ch === "]") && depth > 0) depth--;
    const rest = text.slice(i);
    const m = depth === 0 ? rest.match(sep) : null;
    if (m && m.index === 0) {
      out.push(cur);
      cur = "";
      i += m[0].length - 1;
      continue;
    }
    cur += ch;
  }
  out.push(cur);
  return out.map((s) => s.trim()).filter(Boolean);
}

function sentences(text: string): string[] {
  // Splits after ". " at the top level only (never inside brackets, so
  // "B.Tech.(Agr. Engg.)" stays whole), and not after an abbreviation.
  const parts: string[] = [];
  let depth = 0, cur = "";
  for (let i = 0; i < text.length; i++) {
    const ch = text[i];
    if (ch === "(" || ch === "[") depth++;
    if ((ch === ")" || ch === "]") && depth > 0) depth--;
    cur += ch;
    if (depth === 0 && /[.!?]/.test(ch) && text[i + 1] === " " && /[A-Z0-9(]/.test(text[i + 2] ?? "") && !ABBREV.test(cur.trim())) {
      parts.push(cur.trim());
      cur = "";
    }
  }
  if (cur.trim()) parts.push(cur.trim());
  return parts;
}

export type Point = { label: string | null; text: string };

// Labelled parts such as "Govt: ... Private: ..." or "Engineering stream: ...".
const LABEL = /^(Govt|Government|Private|Public|Engineering(?: stream)?|Agriculture(?: & Pharmacy)?(?: stream)?|Pharmacy(?: stream)?|Medical|Diploma|Note|Paper [IVX0-9]+[A-Z]?|Session \d|Stage \d|Phase[- ]?[IVX0-9]+|Prelims|Mains|Male|Female|Men|Women|AP|Telangana|TS|TG)\s*[:\-–]\s+/i;

export function toPoints(text: string): Point[] {
  const clean = text.replace(/\s+/g, " ").trim().replace(/\.$/, "");
  // Labels can appear mid-text ("... colleges. Private: ..."): break before them.
  const chunks = clean
    .split(/(?<=[.;])\s+(?=(?:Govt|Government|Private)\s*:)/)
    .flatMap((c) => splitTopLevel(c, /^;\s*/))
    // "A, OR B, OR C" lists alternatives: one point each.
    .flatMap((c) => splitTopLevel(c, /^,?\s+OR\s+/))
    // Numbered parts "(i) ... (ii) ..." or "(1) ... (2) ..." are separate points.
    .flatMap((c) => c.split(/\s+(?=\((?:i{1,3}|iv|vi{0,3}|ix|x|[1-9])\)\s)/))
    .flatMap(sentences);
  return chunks.map((c) => {
    const m = c.match(LABEL);
    const body = (m ? c.slice(m[0].length) : c).replace(/^(?:[-–•]|\((?:i{1,3}|iv|vi{0,3}|ix|x|[1-9])\))\s*/, "").replace(/[.;,]\s*$/, "");
    return { label: m ? m[1].replace(/^Govt$/i, "Government") : null, text: body.charAt(0).toUpperCase() + body.slice(1) };
  }).filter((p) => p.text);
}

// A short list ("Engineering (via AP EAPCET), Architecture (NATA), Defence (NDA)")
// shows as chips instead of a sentence.
export function toChips(text: string): string[] | null {
  if (/[.;:]\s/.test(text)) return null;
  const items = splitTopLevel(text.replace(/,?\s+and\s+(?=[^,]*$)/, ", "), /^,\s*/);
  return items.length >= 3 && items.every((i) => i.length <= 40) ? items : null;
}

// Line icons for section headings (24px grid, stroked).
export const ICON = {
  info: <><circle cx="12" cy="12" r="9" /><path d="M12 11v5M12 8h.01" /></>,
  person: <><circle cx="12" cy="8" r="4" /><path d="M4 21c1.5-4 4.5-6 8-6s6.5 2 8 6" /></>,
  calendar: <><rect x="3.5" y="5" width="17" height="15" rx="2.5" /><path d="M3.5 10h17M8 3v4M16 3v4" /></>,
  pen: <><path d="M4 20h4L19 9l-4-4L4 16z" /><path d="M13.5 6.5l4 4" /></>,
  arrow: <><path d="M5 12h14M13 6l6 6-6 6" /></>,
  building: <><path d="M4 21V8l8-5 8 5v13" /><path d="M9 21v-6h6v6M4 21h16" /></>,
  flag: <><path d="M5 21V4M5 4h11l-2 4 2 4H5" /></>,
  clock: <><circle cx="12" cy="12" r="9" /><path d="M12 7v5l3 2" /></>,
  list: <><path d="M9 6h11M9 12h11M9 18h11M4.5 6h.01M4.5 12h.01M4.5 18h.01" /></>,
  book: <><path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H20v15H6.5A2.5 2.5 0 0 0 4 20.5z" /><path d="M4 20.5A2.5 2.5 0 0 0 6.5 23H20v-5" /></>,
  chart: <><path d="M4 20V10M10 20V4M16 20v-7M22 20H2" /></>,
  link: <><path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1" /><path d="M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1-1" /></>,
};

// One heading-with-icon section of points: the details panels on the
// flowchart, /exams and /second-chance all use it.
export function PointSection({
  title, icon, color, text, badge, children,
}: {
  title: string; icon: ReactNode; color: string; text?: string; badge?: string | null; children?: ReactNode;
}) {
  return (
    <section className="flex min-w-0 flex-col gap-3">
      <h3 className="m-0 flex flex-wrap items-center gap-2.5 text-[16px] font-bold" style={{ fontFamily: "var(--metro-display), var(--metro-body), system-ui, sans-serif" }}>
        <span aria-hidden className="grid h-8 w-8 shrink-0 place-items-center rounded-full" style={{ background: "var(--surface)", color }}>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">{icon}</svg>
        </span>
        {title}
        {badge && (
          <span className="rounded-full px-2.5 py-0.5 text-xs font-bold" style={{ background: "#2b2412", color: "#f0c870", fontFamily: "inherit" }}>{badge}</span>
        )}
      </h3>
      {text && <PointList text={text} color={color} />}
      {children}
    </section>
  );
}

// Numbers that matter: dates, date ranges, percentages, money, durations, ages.
const MONTH = "(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*";
const KEY = new RegExp(
  [
    `\\b\\d{1,2}(?:st|nd|rd|th)?\\s+${MONTH}(?:\\s+\\d{4})?(?:\\s*(?:-|–|to)\\s*\\d{1,2}(?:st|nd|rd|th)?\\s+${MONTH}(?:\\s+\\d{4})?)?`,
    `\\b${MONTH}\\s+\\d{4}`,
    `\\b${MONTH}\\s+\\d{1,2}(?!\\d)(?:,\\s*\\d{4})?`,
    `\\b\\d{1,2}[-./]\\d{1,2}[-./]\\d{2,4}(?:\\s*(?:-|–|to)\\s*\\d{1,2}[-./]\\d{1,2}[-./]\\d{2,4})?`,
    `(?:\\bRs\\.?|₹)\\s?[\\d,]*\\d(?:\\.\\d+)?(?:\\s*(?:lakh|crore))?(?:\\s*[-–]\\s*[\\d,]*\\d(?:\\s*(?:lakh|crore))?(?![-./]\\d))?`,
    `\\b\\d+(?:\\.\\d+)?(?:\\s*(?:-|–|to)\\s*\\d+(?:\\.\\d+)?)?\\s?%`,
    `\\b\\d+(?:\\.\\d+)?(?:th|st|nd|rd)?\\s+percentile`,
    `\\b\\d+(?:\\s*(?:-|–|to)\\s*\\d+)?\\s+(?:years?|months?|weeks?|hours?|minutes?)\\b`,
  ].join("|"),
  "gi",
);

export function Highlight({ text }: { text: string }) {
  const out: ReactNode[] = [];
  let last = 0;
  for (const m of text.matchAll(KEY)) {
    if (m.index! > last) out.push(text.slice(last, m.index));
    out.push(<strong key={m.index} className="font-semibold whitespace-nowrap" style={{ color: "var(--ink)" }}>{m[0]}</strong>);
    last = m.index! + m[0].length;
  }
  out.push(text.slice(last));
  return <>{out}</>;
}

// The points of one field, with the first few shown and "Show N more" for the rest.
export function PointList({ text, color, limit = 4, full }: { text: string; color: string; limit?: number; full?: boolean }) {
  const [open, setOpen] = useState(false);
  const chips = toChips(text);
  if (chips) {
    return (
      <ul className="m-0 flex list-none flex-wrap gap-2 p-0">
        {chips.map((c) => (
          <li key={c} className="rounded-full px-3 py-1.5 text-[14px] leading-snug" style={{ background: "var(--surface)", color: "#dfe4ec" }}>{c}</li>
        ))}
      </ul>
    );
  }
  const points = toPoints(text);
  const shown = full || open ? points : points.slice(0, limit);
  return (
    <div className="flex flex-col gap-2">
      <ul className="m-0 flex list-none flex-col gap-2.5 p-0">
        {shown.map((p, i) => (
          <li key={i} className="grid grid-cols-[14px_minmax(0,1fr)] gap-x-2.5 text-[15px] leading-relaxed" style={{ color: "#c9d0dc" }}>
            <span aria-hidden className="mt-[9px] h-1.5 w-1.5 rounded-full" style={{ background: color }} />
            <span style={{ overflowWrap: "anywhere" }}>
              {p.label && <span className="mr-1.5 font-bold" style={{ color: "var(--ink)" }}>{p.label}:</span>}
              <Highlight text={p.text} />
            </span>
          </li>
        ))}
      </ul>
      {!full && points.length > limit && (
        <button onClick={() => setOpen(!open)} className="self-start cursor-pointer border-0 bg-transparent p-0 pl-6 text-[14px] font-semibold" style={{ color: "var(--accent)", fontFamily: "inherit" }}>
          {open ? "Show less" : `Show ${points.length - limit} more`}
        </button>
      )}
    </div>
  );
}
