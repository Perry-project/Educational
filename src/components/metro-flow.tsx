"use client";

import Link from "next/link";
import { useState } from "react";
import "./metro-flow.css";
import type { FlowNode } from "@/lib/class10-flow-data";
import type { NodeDetail } from "@/lib/flowchart-db";
import { Fold, ICON, PointList, PointSection, SubjectList } from "./fact-points";
import Icon from "./icon";

// The details of one step on the career map (flow-chart.tsx): who can apply,
// dates, syllabus, colleges, study topics and jobs, from Postgres
// (flowchart-db.ts). The first few sections show; longer ones fold away.

const KIND: Record<number, string> = { 1: "Starting point", 2: "After Class 10", 3: "Entrance exam", 4: "Course" };
const NOT_ANNOUNCED = /not yet (?:announced|released|open|notified)|not announced/i;

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

export function StopDetails({
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
      {!compact && node?.full && node.full.length < 160 && <p className="m-0 text-[16px] leading-snug" style={{ color: "var(--soft)" }}>{node.full}</p>}
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
            <div key={k} className="flex flex-col gap-0.5 rounded-lg px-3 py-2.5" style={{ background: "var(--bg)", boxShadow: "inset 0 0 0 1px var(--line)" }}>
              <dt className="text-[12.5px] font-medium" style={{ color: "var(--muted)" }}>{SECTION[k]?.title ?? k}</dt>
              <dd className="m-0 text-[15px] leading-snug font-semibold" style={{ color: "var(--ink)" }}>{v}</dd>
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
