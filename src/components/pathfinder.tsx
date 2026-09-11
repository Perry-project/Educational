"use client";

import { useMemo, useState } from "react";
import type { FlowGraph } from "@/lib/flow-data";
import { ADVISORY_QUIZ, pathsToCareer, scoreQuiz } from "@/lib/decision-logic";
import type { CollegeMatch } from "@/lib/decision-data";
import { TierBadge } from "./tier-badge";

type Mode = "choose" | "quiz" | "result";

const OFFICIAL_SOURCES = "cets.apsche.ap.gov.in (entrance tests) and cap.apcfss.in (counselling/seat allotment)";

export default function Pathfinder({
  graph,
  collegesByCourse,
}: {
  graph: FlowGraph;
  collegesByCourse: Record<string, CollegeMatch[]>;
}) {
  const [mode, setMode] = useState<Mode>("choose");
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [suggested, setSuggested] = useState<string[]>([]);
  const [careerId, setCareerId] = useState<string | null>(null);

  const careers = useMemo(() => graph.nodes.filter((n) => n.type === "career"), [graph.nodes]);
  const byId = useMemo(() => new Map(graph.nodes.map((n) => [n.id, n])), [graph.nodes]);

  const paths = useMemo(() => (careerId ? pathsToCareer(graph, careerId) : []), [graph, careerId]);

  const startOver = () => {
    setMode("choose");
    setAnswers({});
    setSuggested([]);
    setCareerId(null);
  };

  const submitQuiz = () => {
    const top = scoreQuiz(answers, ADVISORY_QUIZ).filter((id) => byId.has(id));
    setSuggested(top);
  };

  if (mode === "choose") {
    return (
      <div className="flex flex-col gap-4 sm:flex-row">
        <button
          type="button"
          onClick={() => setMode("result")}
          className="flex-1 rounded-lg border border-black/10 p-5 text-left transition hover:border-black/25 dark:border-white/15 dark:hover:border-white/30"
        >
          <div className="text-sm font-semibold">I know what I&apos;m aiming for</div>
          <p className="mt-1 text-sm text-black/60 dark:text-white/60">
            Pick a career directly and see the exams, syllabus, and colleges between here and there.
          </p>
        </button>
        <button
          type="button"
          onClick={() => setMode("quiz")}
          className="flex-1 rounded-lg border border-black/10 p-5 text-left transition hover:border-black/25 dark:border-white/15 dark:hover:border-white/30"
        >
          <div className="text-sm font-semibold">Help me figure it out</div>
          <p className="mt-1 text-sm text-black/60 dark:text-white/60">
            Answer three quick questions — Perry will suggest a few directions to look at (advisory, not a verdict).
          </p>
        </button>
      </div>
    );
  }

  if (mode === "quiz" && suggested.length === 0) {
    const answeredCount = Object.keys(answers).length;
    return (
      <div className="flex flex-col gap-6">
        <span className="inline-flex w-fit items-center rounded-full bg-sky-500/15 px-2 py-0.5 text-[11px] font-semibold text-sky-700 dark:text-sky-400">
          AI-assisted — advisory only, not a recommendation of fact
        </span>
        {ADVISORY_QUIZ.map((q) => (
          <div key={q.id}>
            <div className="text-sm font-medium">{q.prompt}</div>
            <div className="mt-2 flex flex-wrap gap-2">
              {q.options.map((opt) => (
                <button
                  key={opt.id}
                  type="button"
                  onClick={() => setAnswers((a) => ({ ...a, [q.id]: opt.id }))}
                  className={`rounded-full border px-3 py-1.5 text-sm transition ${
                    answers[q.id] === opt.id
                      ? "border-black bg-black text-white dark:border-white dark:bg-white dark:text-black"
                      : "border-black/15 hover:border-black/35 dark:border-white/20 dark:hover:border-white/40"
                  }`}
                >
                  {opt.label}
                </button>
              ))}
            </div>
          </div>
        ))}
        <div className="flex items-center gap-3">
          <button
            type="button"
            disabled={answeredCount < ADVISORY_QUIZ.length}
            onClick={submitQuiz}
            className="rounded-md bg-black px-4 py-2 text-sm font-semibold text-white disabled:opacity-30 dark:bg-white dark:text-black"
          >
            See suggestions
          </button>
          <button type="button" onClick={startOver} className="text-sm text-black/50 hover:text-black dark:text-white/50 dark:hover:text-white">
            Start over
          </button>
        </div>
      </div>
    );
  }

  if (mode === "quiz" && suggested.length > 0) {
    return (
      <div className="flex flex-col gap-4">
        <span className="inline-flex w-fit items-center rounded-full bg-sky-500/15 px-2 py-0.5 text-[11px] font-semibold text-sky-700 dark:text-sky-400">
          AI-assisted — a few directions worth exploring, not a verdict
        </span>
        <div className="flex flex-col gap-2 sm:flex-row">
          {suggested.map((id) => {
            const node = byId.get(id)!;
            return (
              <button
                key={id}
                type="button"
                onClick={() => {
                  setCareerId(id);
                  setMode("result");
                }}
                className="flex-1 rounded-lg border border-black/10 p-4 text-left transition hover:border-black/25 dark:border-white/15 dark:hover:border-white/30"
              >
                <div className="text-sm font-semibold">{node.label}</div>
                <div className="mt-1 text-xs text-black/55 dark:text-white/55">{node.sub}</div>
              </button>
            );
          })}
        </div>
        <button type="button" onClick={startOver} className="w-fit text-sm text-black/50 hover:text-black dark:text-white/50 dark:hover:text-white">
          Start over
        </button>
      </div>
    );
  }

  // mode === "result"
  if (!careerId) {
    return (
      <div className="flex flex-col gap-4">
        <div className="flex flex-wrap gap-2">
          {careers.map((c) => (
            <button
              key={c.id}
              type="button"
              onClick={() => setCareerId(c.id)}
              className="rounded-full border border-black/15 px-3 py-1.5 text-sm transition hover:border-black/35 dark:border-white/20 dark:hover:border-white/40"
            >
              {c.label}
            </button>
          ))}
        </div>
        <button type="button" onClick={startOver} className="w-fit text-sm text-black/50 hover:text-black dark:text-white/50 dark:hover:text-white">
          ‹ Back
        </button>
      </div>
    );
  }

  const career = byId.get(careerId)!;

  return (
    <div className="flex flex-col gap-8">
      <div className="flex items-center justify-between">
        <div>
          <div className="text-[11px] font-semibold tracking-wide text-black/45 uppercase dark:text-white/45">Target career</div>
          <h2 className="text-lg font-semibold">{career.label}</h2>
        </div>
        <button type="button" onClick={startOver} className="text-sm text-black/50 hover:text-black dark:text-white/50 dark:hover:text-white">
          Start over
        </button>
      </div>

      {paths.length === 0 && (
        <p className="text-sm text-black/60 dark:text-white/60">
          No course route is mapped to this career in the database yet.
        </p>
      )}

      {paths.map(({ course, exams, pathways }) => (
        <div key={course.id} className="rounded-lg border border-black/10 dark:border-white/15">
          <div className="border-b border-black/10 p-4 dark:border-white/15">
            <div className="flex items-center justify-between gap-3">
              <div>
                <div className="text-[11px] font-semibold tracking-wide text-black/45 uppercase dark:text-white/45">Course</div>
                <div className="text-sm font-semibold">{course.label}</div>
              </div>
              <TierBadge tier={course.tier} />
            </div>
            {pathways.length > 0 && (
              <p className="mt-2 text-xs text-black/55 dark:text-white/55">
                Starting point: {pathways.map((p) => p.label).join(" or ")}
              </p>
            )}
          </div>

          <div className="grid gap-4 p-4 sm:grid-cols-2">
            <div>
              <div className="text-[11px] font-semibold tracking-wide text-black/45 uppercase dark:text-white/45">
                Entrance exam{exams.length !== 1 ? "s" : ""}
              </div>
              <div className="mt-2 flex flex-col gap-3">
                {exams.length === 0 && <p className="text-sm text-black/50 dark:text-white/50">None on file.</p>}
                {exams.map((exam) => (
                  <div key={exam.id} className="rounded-md bg-black/[0.03] p-3 dark:bg-white/[0.05]">
                    <div className="flex items-start justify-between gap-2">
                      <div className="text-sm font-medium">{exam.label}</div>
                    </div>
                    <div className="mt-1">
                      <TierBadge tier={exam.tier} />
                    </div>
                    {exam.sub && <div className="mt-1 text-xs text-black/55 dark:text-white/55">{exam.sub}</div>}
                  </div>
                ))}
              </div>
            </div>

            <div>
              <div className="text-[11px] font-semibold tracking-wide text-black/45 uppercase dark:text-white/45">Colleges offering this</div>
              <div className="mt-2 flex flex-col gap-2">
                {(collegesByCourse[course.id] ?? []).length === 0 && (
                  <p className="text-sm text-black/50 dark:text-white/50">None on file yet.</p>
                )}
                {(collegesByCourse[course.id] ?? []).slice(0, 6).map((c) => (
                  <div key={c.collegeName} className="rounded-md bg-black/[0.03] p-3 dark:bg-white/[0.05]">
                    <div className="text-sm font-medium">{c.collegeName}</div>
                    <div className="mt-0.5 text-xs text-black/55 dark:text-white/55">
                      {[c.ownership, c.admissionRoute].filter(Boolean).join(" · ")}
                    </div>
                    <div className="mt-1">
                      <TierBadge tier={c.tier} />
                    </div>
                  </div>
                ))}
                {(collegesByCourse[course.id] ?? []).length > 6 && (
                  <p className="text-xs text-black/45 dark:text-white/45">
                    +{(collegesByCourse[course.id] ?? []).length - 6} more on file.
                  </p>
                )}
              </div>
            </div>
          </div>

          <div className="border-t border-black/10 p-4 dark:border-white/15">
            <div className="text-[11px] font-semibold tracking-wide text-black/45 uppercase dark:text-white/45">
              Which college can I realistically get into?
            </div>
            <p className="mt-1 text-sm text-black/60 dark:text-white/60">
              Not yet available. Category-wise cutoff ranks (OC/BC/SC/ST/EWS) aren&apos;t in the database yet — this
              is in-progress work, not a gap we&apos;re guessing around. Check {OFFICIAL_SOURCES} directly for
              current closing ranks in the meantime.
            </p>
          </div>
        </div>
      ))}
    </div>
  );
}
