"use client";

import { useEffect, useRef, useState, type CSSProperties, type TouchEvent } from "react";
import { col } from "@/lib/class10-flow-data";
import type { CollegeRef, Topic } from "@/lib/flowchart-db";

// The details panel for the selected flowchart step: a side panel on wide
// screens, a bottom sheet (drag the handle down to close) on phones and
// portrait tablets.

export type Chip = { id: string; dash: boolean };
export type Panel = {
  kind: string; label: string; full: string; accent: string; rows: [string, string][]; note: string;
  from: Chip[]; to: Chip[]; fromTitle: string; toTitle: string;
  source: string | null; colleges: CollegeRef[]; topics: Topic[];
  // Courses always show their colleges / topics sections, with a note when
  // there's nothing yet; other steps don't have them at all.
  isCourse: boolean;
};

const PANEL_W = 368;
const LONG = 220; // longer values start collapsed

const sectionHead = (text: string) => (
  <h3 style={{ margin: 0, fontSize: 12, fontWeight: 700, letterSpacing: "0.06em", textTransform: "uppercase", color: "var(--muted)" }}>{text}</h3>
);
const muted: CSSProperties = { margin: 0, fontSize: 13, lineHeight: 1.5, color: "var(--muted)" };

// First sentence (or clause) of a long value, for the collapsed view.
function lead(text: string) {
  const m = /[.;](\s|$)/g;
  let hit: RegExpExecArray | null;
  while ((hit = m.exec(text))) {
    if (hit.index >= 60 && hit.index <= 240) return text.slice(0, hit.index + 1);
    if (hit.index > 240) break;
  }
  return text.slice(0, text.lastIndexOf(" ", 200)) + "…";
}

function Fact({ text }: { text: string }) {
  const [more, setMore] = useState(false);
  if (text.length <= LONG) return <>{text}</>;
  return (
    <>
      {more ? text : lead(text)}{" "}
      <button
        onClick={() => setMore(!more)}
        aria-expanded={more}
        style={{ border: 0, padding: 0, background: "none", color: "var(--c2)", font: "inherit", fontSize: 13, fontWeight: 600, cursor: "pointer" }}
      >
        {more ? "Show less" : "Show more"}
      </button>
    </>
  );
}

export default function DetailsPanel({
  panel, stacked, shareUrl, onClose, onPick, nameOf,
}: {
  panel: Panel;
  stacked: boolean;
  shareUrl: string;
  onClose: () => void;
  onPick: (id: string) => void;
  nameOf: (id: string) => string;
}) {
  const [dragY, setDragY] = useState(0);
  const [copied, setCopied] = useState(false);
  const startY = useRef<number | null>(null);
  const scrollRef = useRef<HTMLElement>(null);

  // A new step starts at the top of the panel.
  useEffect(() => { scrollRef.current?.scrollTo({ top: 0 }); }, [panel.label]);

  // While the bottom sheet is open, the page behind it doesn't scroll.
  useEffect(() => {
    if (!stacked) return;
    const prev = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    return () => { document.body.style.overflow = prev; };
  }, [stacked]);

  const share = async () => {
    try {
      if (navigator.share) await navigator.share({ title: `${panel.label} — Perry`, url: shareUrl });
      else {
        await navigator.clipboard.writeText(shareUrl);
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
      }
    } catch {
      // Share sheet dismissed, or clipboard blocked: nothing to do.
    }
  };

  const drag = stacked
    ? {
        onTouchStart: (e: TouchEvent) => { startY.current = e.touches[0].clientY; },
        onTouchMove: (e: TouchEvent) => {
          if (startY.current !== null) setDragY(Math.max(0, e.touches[0].clientY - startY.current));
        },
        onTouchEnd: () => {
          if (dragY > 90) onClose();
          startY.current = null;
          setDragY(0);
        },
      }
    : {};

  const place: CSSProperties = stacked
    ? { top: "auto", right: 0, bottom: 0, left: 0, width: "auto", maxHeight: "78vh", borderRadius: "18px 18px 0 0", paddingBottom: "env(safe-area-inset-bottom)" }
    : { top: "calc(var(--nav-h) + 16px)", right: 16, bottom: 16, left: "auto", width: PANEL_W, maxHeight: "none", borderRadius: 16 };

  const chipList = (list: Chip[]) => (
    <div style={{ display: "flex", flexWrap: "wrap", gap: 6 }}>
      {list.map((ch) => (
        <button
          key={ch.id}
          onClick={() => onPick(ch.id)}
          className="c10-chip"
          style={{
            display: "flex", alignItems: "center", gap: 6, minHeight: stacked ? 40 : 34, padding: "6px 12px", lineHeight: 1.3, textAlign: "left",
            boxSizing: "border-box", borderRadius: 20, border: `1px ${ch.dash ? "dashed" : "solid"} var(--edge)`,
            background: "var(--bg)", color: "var(--ink)", font: "inherit", fontSize: 13, fontWeight: 600, cursor: "pointer",
          }}
        >
          <span style={{ width: 7, height: 7, flex: "none", borderRadius: "50%", background: `var(--c${col(ch.id)})` }} />
          {nameOf(ch.id)}
        </button>
      ))}
    </div>
  );

  const iconBtn: CSSProperties = {
    height: 36, flex: "none", borderRadius: 18, border: "1px solid var(--line)", background: "var(--bg)", color: "var(--ink)",
    font: "inherit", cursor: "pointer", display: "inline-flex", alignItems: "center", justifyContent: "center", gap: 6,
  };

  return (
    <aside
      ref={scrollRef}
      aria-label="Details"
      style={{
        position: "fixed", zIndex: 20, ...place, background: "var(--surface)", border: "1px solid var(--line)",
        boxShadow: "0 24px 60px -24px rgba(0,0,0,0.4)", overflow: "auto", overscrollBehavior: "contain",
        display: "flex", flexDirection: "column", boxSizing: "border-box",
        transform: dragY ? `translateY(${dragY}px)` : undefined, transition: dragY ? "none" : "transform .2s",
      }}
    >
      <div style={{ height: 5, flex: "none", background: panel.accent }} />
      {stacked && (
        <div {...drag} aria-hidden style={{ flex: "none", display: "grid", placeItems: "center", height: 22, touchAction: "none", cursor: "grab" }}>
          <span style={{ width: 44, height: 5, borderRadius: 3, background: "var(--line)" }} />
        </div>
      )}
      <div style={{ padding: stacked ? "4px 20px 26px" : "18px 22px 26px", display: "flex", flexDirection: "column", gap: 18 }}>
        <div {...drag} style={{ display: "flex", alignItems: "center", justifyContent: "space-between", gap: 12 }}>
          <span style={{ fontSize: 12, fontWeight: 700, letterSpacing: "0.06em", textTransform: "uppercase", color: "var(--muted)" }}>{panel.kind}</span>
          <span style={{ display: "flex", gap: 8 }}>
            <button onClick={share} className="c10-pill" style={{ ...iconBtn, padding: "0 12px", fontSize: 13, fontWeight: 600 }}>
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden>
                <path d="M4 12v7a1 1 0 0 0 1 1h14a1 1 0 0 0 1-1v-7M16 6l-4-4-4 4M12 2v14" />
              </svg>
              {copied ? "Link copied" : "Share"}
            </button>
            <button onClick={onClose} aria-label="Close details" className="c10-pill" style={{ ...iconBtn, width: 36, fontSize: 18, lineHeight: 1 }}>
              ×
            </button>
          </span>
        </div>
        <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
          <h2 style={{ margin: 0, fontSize: 26, lineHeight: 1.15, fontWeight: 800, letterSpacing: "-0.01em" }}>{panel.label}</h2>
          {panel.full && <p style={{ margin: 0, color: "var(--muted)", fontSize: 14, lineHeight: 1.4 }}>{panel.full}</p>}
        </div>

        {panel.rows.length > 0 && (
          <dl style={{ margin: 0, display: "flex", flexDirection: "column" }}>
            {panel.rows.map(([k, v]) => (
              <div key={k} style={{ display: "grid", gridTemplateColumns: stacked ? "96px minmax(0,1fr)" : "104px minmax(0,1fr)", gap: 12, padding: "11px 0", borderTop: "1px solid var(--line)" }}>
                <dt style={{ fontSize: 13, color: "var(--muted)", fontWeight: 600 }}>{k}</dt>
                <dd style={{ margin: 0, minWidth: 0, fontSize: 14, lineHeight: 1.45, textWrap: "pretty", overflowWrap: "anywhere" }}>
                  <Fact text={v} />
                </dd>
              </div>
            ))}
          </dl>
        )}
        {panel.note && <p style={{ ...muted, textWrap: "pretty" }}>{panel.note}</p>}

        {panel.isCourse && (
          <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
            {sectionHead(`Colleges in AP${panel.colleges.length ? ` · ${panel.colleges.length}` : ""}`)}
            {panel.colleges.length ? (
              <ul style={{ margin: 0, padding: 0, listStyle: "none", display: "flex", flexDirection: "column", gap: 6 }}>
                {panel.colleges.map((c) => (
                  <li key={c.name} style={{ display: "flex", justifyContent: "space-between", gap: 10, fontSize: 13, lineHeight: 1.4 }}>
                    <span>{c.name}</span>
                    {c.ownership && (
                      <span style={{ flex: "none", fontSize: 11, fontWeight: 600, color: "var(--muted)", border: "1px solid var(--line)", borderRadius: 999, padding: "1px 8px", height: "fit-content" }}>
                        {c.ownership === "Government" ? "Govt" : c.ownership}
                      </span>
                    )}
                  </li>
                ))}
              </ul>
            ) : (
              <p style={muted}>No AP colleges listed for this course yet.</p>
            )}
          </div>
        )}

        {panel.isCourse && (
          <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
            {sectionHead(`What you’ll study${panel.topics.length ? ` · ${panel.topics.length} topics` : ""}`)}
            {panel.topics.length ? (
              <ol style={{ margin: 0, padding: 0, listStyle: "none", display: "flex", flexDirection: "column", gap: 4 }}>
                {panel.topics.map((t, i) => (
                  <li key={t.name}>
                    <details className="c10-topic">
                      <summary style={{ display: "flex", gap: 8, cursor: "pointer", fontSize: 13, fontWeight: 600, lineHeight: 1.4, padding: "7px 0" }}>
                        <span style={{ flex: "none", width: 20, color: "var(--c4)" }}>{i + 1}.</span>
                        <span>{t.name}</span>
                      </summary>
                      <div style={{ padding: "0 0 8px 28px", display: "flex", flexDirection: "column", gap: 6, fontSize: 13, lineHeight: 1.5, color: "var(--muted)" }}>
                        {t.why && <p style={{ margin: 0 }}>{t.why}</p>}
                        {t.buildsToward && <p style={{ margin: 0 }}><strong style={{ color: "var(--ink)" }}>Leads to:</strong> {t.buildsToward}</p>}
                      </div>
                    </details>
                  </li>
                ))}
              </ol>
            ) : (
              <p style={muted}>Study topics for this course are being added. Check back soon.</p>
            )}
          </div>
        )}

        {panel.from.length > 0 && (
          <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
            {sectionHead(panel.fromTitle)}
            {chipList(panel.from)}
          </div>
        )}
        {panel.to.length > 0 && (
          <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
            {sectionHead(panel.toTitle)}
            {chipList(panel.to)}
            <span style={{ fontSize: 12, color: "var(--muted)" }}>Dashed chips are alternate or lateral routes.</span>
          </div>
        )}
        {panel.source && (
          <p style={{ ...muted, fontSize: 12, paddingTop: 12, borderTop: "1px solid var(--line)", overflowWrap: "anywhere" }}>
            <strong>Source:</strong> {panel.source}
          </p>
        )}
      </div>
    </aside>
  );
}
