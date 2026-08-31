"use client";

import { useCallback, useMemo, useState, type ComponentType, type CSSProperties } from "react";
import "./flow-explorer.css";
import type { FlowGraph, FlowNode, FlowNodeType, Stream } from "@/lib/flow-data";
import { IconScience, IconCommerce, IconHumanities, IconVocational, IconExam, IconCourse } from "./flow-icons";

const TYPE_LABEL: Record<FlowNodeType, string> = {
  root: "Start",
  pathway: "Pathway",
  exam: "Entrance exam",
  course: "Course",
};

const COLUMN_LABEL = ["Pathway", "Leads to", "Course"];

const STREAMS: Stream[] = ["Science", "Commerce", "Humanities", "Vocational"];

// One saturated gradient per stream — this same color carries through every
// card downstream of it, so a whole drilled-in path visually reads as
// belonging to one field, not just the first column.
const STREAM_COLOR: Record<Stream, { from: string; to: string; solid: string }> = {
  Science: { from: "#2f80ed", to: "#56ccf2", solid: "#2f80ed" },
  Commerce: { from: "#f2994a", to: "#f2c94c", solid: "#e08e2d" },
  Humanities: { from: "#eb5757", to: "#f2799a", solid: "#e0526b" },
  Vocational: { from: "#11998e", to: "#38ef7d", solid: "#119174" },
};

const STREAM_ICON: Record<Stream, ComponentType> = {
  Science: IconScience,
  Commerce: IconCommerce,
  Humanities: IconHumanities,
  Vocational: IconVocational,
};

type ChildItem = { node: FlowNode; secondary: boolean };

function cardIcon(node: FlowNode) {
  if (node.type === "pathway" && node.stream) return STREAM_ICON[node.stream];
  if (node.type === "exam") return IconExam;
  return IconCourse;
}

export default function FlowExplorer({ graph }: { graph: FlowGraph }) {
  const [path, setPath] = useState<string[]>([]);
  const [stream, setStream] = useState<Stream | null>(null);

  const byId = useMemo(() => new Map(graph.nodes.map((n) => [n.id, n])), [graph.nodes]);

  const childrenOf = useCallback(
    (id: string): ChildItem[] =>
      graph.edges
        .filter((e) => e.source === id)
        .map((e) => ({ node: byId.get(e.target)!, secondary: !!e.secondary })),
    [graph.edges, byId]
  );

  const columns = useMemo(() => {
    const cols: { parentId: string; items: ChildItem[] }[] = [];
    let parent = "root";
    for (let depth = 0; depth < 4; depth++) {
      let items = childrenOf(parent);
      if (depth === 0 && stream) {
        items = items.filter(({ node }) => node.stream === stream);
      }
      if (items.length === 0) break;
      cols.push({ parentId: parent, items });
      const chosen = path[depth];
      if (!chosen) break;
      parent = chosen;
    }
    return cols;
  }, [path, stream, childrenOf]);

  const selectAt = useCallback((depth: number, id: string) => {
    setPath((prev) => (prev[depth] === id ? prev.slice(0, depth) : [...prev.slice(0, depth), id]));
  }, []);

  const selectStream = useCallback((next: Stream | null) => {
    setStream((prev) => (prev === next ? null : next));
    setPath([]);
  }, []);

  const currentId = path[path.length - 1] ?? "root";
  const focusNode = byId.get(currentId)!;
  const crumbs = [byId.get("root")!, ...path.map((id) => byId.get(id)!)];

  // The color the whole drilled-in path threads through: the stream of
  // whichever pathway (column 0) is currently selected.
  const threadStream = path[0] ? byId.get(path[0])?.stream : undefined;

  return (
    <div className="flow-explorer flex flex-col gap-4">
      <div className="flex flex-wrap gap-1.5">
        <button
          type="button"
          onClick={() => selectStream(null)}
          className={`fe-chip ${stream === null ? "is-active" : ""}`}
        >
          All streams
        </button>
        {STREAMS.map((s) => (
          <button
            key={s}
            type="button"
            onClick={() => selectStream(s)}
            className={`fe-chip ${stream === s ? "is-active" : ""}`}
            style={stream === s ? { background: STREAM_COLOR[s].solid, borderColor: STREAM_COLOR[s].solid } : undefined}
          >
            {s}
          </button>
        ))}
      </div>

      <nav className="flex flex-wrap items-center gap-1 text-sm">
        {crumbs.map((crumb, i) => (
          <span key={crumb.id} className="flex items-center gap-1">
            {i > 0 && <span className="text-black/25 dark:text-white/25">›</span>}
            <button
              type="button"
              onClick={() => setPath(path.slice(0, i))}
              className={`fe-crumb ${i === crumbs.length - 1 ? "is-current" : ""}`}
            >
              {crumb.label}
            </button>
          </span>
        ))}
      </nav>

      <div className="fe-columns flex gap-4 overflow-x-auto pb-2">
        {columns.map((col, depth) => {
          const colColor = depth === 0 ? null : threadStream ? STREAM_COLOR[threadStream] : null;
          return (
            <div
              key={col.parentId}
              className={`fe-column flex w-64 shrink-0 flex-col gap-2 ${depth > 0 ? "fe-column--threaded" : ""}`}
              style={colColor ? ({ "--fe-thread": colColor.solid } as CSSProperties) : undefined}
            >
              <div className="text-[11px] font-semibold tracking-wide text-black/45 uppercase dark:text-white/45">
                {COLUMN_LABEL[depth] ?? "Next step"}
              </div>
              <div className="flex flex-col gap-2">
                {col.items.map(({ node, secondary }) => {
                  const isSelected = path[depth] === node.id;
                  const hasChildren = childrenOf(node.id).length > 0;
                  const color = depth === 0 && node.stream ? STREAM_COLOR[node.stream] : colColor;
                  const Icon = cardIcon(node);
                  return (
                    <button
                      key={node.id}
                      type="button"
                      onClick={() => selectAt(depth, node.id)}
                      className={`fe-card ${isSelected ? "is-selected" : ""}`}
                      style={
                        color
                          ? { background: `linear-gradient(135deg, ${color.from}, ${color.to})`, color: "#fff" }
                          : undefined
                      }
                    >
                      <div className="fe-card-top">
                        <span className="fe-icon-badge">
                          <Icon />
                        </span>
                        {hasChildren && <span className={`fe-chevron ${isSelected ? "is-open" : ""}`}>›</span>}
                      </div>
                      <div className="fe-card-label">{node.label}</div>
                      {node.sub && <div className="fe-card-sub">{node.sub}</div>}
                      {secondary && <div className="fe-card-tag">Alternate route</div>}
                    </button>
                  );
                })}
              </div>
            </div>
          );
        })}
      </div>

      <div className={`fe-detail fe-detail--${focusNode.type}`}>
        <div className="text-[11px] font-semibold tracking-wide text-black/45 uppercase dark:text-white/45">
          {TYPE_LABEL[focusNode.type]}
        </div>
        <h2 className="mt-1 text-base font-semibold">{focusNode.label}</h2>
        <dl className="mt-3 grid gap-3 sm:grid-cols-2">
          {focusNode.facts.length > 0 ? (
            focusNode.facts.map((f) => (
              <div key={f.label}>
                <dt className="text-[11px] font-semibold tracking-wide text-black/45 uppercase dark:text-white/45">
                  {f.label}
                </dt>
                <dd className="mt-0.5 text-sm text-black/75 dark:text-white/75">{f.value}</dd>
              </div>
            ))
          ) : (
            <p className="text-sm text-black/50 dark:text-white/50">No additional detail on file for this node yet.</p>
          )}
        </dl>
      </div>
    </div>
  );
}
