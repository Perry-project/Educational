"use client";

import { useEffect, useRef, useState } from "react";

// The desktop flowchart's menu bar: one button per menu (School education,
// Entrance exams, ...), each opening a wide panel of grouped links. Opens on
// click; Escape, a click outside or a choice closes it.

export type MenuItem = { id: string; label: string; sub?: string; color?: string };
export type BarMenu = { id: string; label: string; groups: { title: string; color?: string; items: MenuItem[] }[] };

export default function FlowMenuBar({
  menus, current, onChoose,
}: {
  menus: BarMenu[];
  current: Set<string>; // ids on the line shown now, marked in the menus
  onChoose: (id: string) => void;
}) {
  const [open, setOpen] = useState<string | null>(null);
  const bar = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!open) return;
    const onKey = (e: KeyboardEvent) => e.key === "Escape" && setOpen(null);
    const onDown = (e: PointerEvent) => !bar.current?.contains(e.target as Node) && setOpen(null);
    window.addEventListener("keydown", onKey);
    window.addEventListener("pointerdown", onDown);
    return () => { window.removeEventListener("keydown", onKey); window.removeEventListener("pointerdown", onDown); };
  }, [open]);

  const menu = menus.find((m) => m.id === open);

  return (
    <div ref={bar} className="relative flex min-w-0 flex-[999_1_640px] flex-wrap gap-1">
      {menus.map((m) => {
        const on = m.id === open;
        const hasCurrent = m.groups.some((g) => g.items.some((it) => current.has(it.id)));
        return (
          <button
            key={m.id}
            onClick={() => setOpen(on ? null : m.id)}
            aria-expanded={on}
            aria-haspopup="true"
            className="metro-chip inline-flex h-11 cursor-pointer items-center gap-1.5 rounded-full border-0 px-4 text-[15px] font-semibold"
            style={{ background: on ? "var(--surface)" : "transparent", color: on || hasCurrent ? "var(--ink)" : "var(--muted)", fontFamily: "inherit" }}
          >
            {m.label}
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden style={{ transform: on ? "rotate(180deg)" : undefined, transition: "transform .15s" }}>
              <path d="M6 9l6 6 6-6" />
            </svg>
          </button>
        );
      })}

      {menu && (
        <div
          role="menu"
          aria-label={menu.label}
          className="metro-scroll absolute top-[calc(100%+10px)] left-0 z-50 max-h-[calc(100vh-var(--nav-h)-120px)] max-w-[calc(100vw-96px)] overflow-y-auto rounded-3xl p-6"
          style={{
            background: "#141b2c", border: "1px solid var(--line)", boxShadow: "0 24px 60px rgba(0,0,0,.45)",
            width: Math.min(menu.groups.length, 4) * 250 + 48,
          }}
        >
          {/* Groups flow down columns, so short and long groups pack together. */}
          <div className="gap-x-6" style={{ columnCount: Math.min(menu.groups.length, 4) }}>
          {menu.groups.map((g) => (
            <section key={g.title} className="mb-5 flex break-inside-avoid flex-col gap-0.5">
              <h3 className="m-0 mb-1 flex items-center gap-2 text-xs font-bold tracking-widest uppercase" style={{ color: "var(--muted)" }}>
                {g.color && <span className="h-2.5 w-2.5 rounded-full" style={{ background: g.color }} />}
                {g.title}
              </h3>
              {g.items.map((it) => {
                const on = current.has(it.id);
                return (
                  <button
                    key={it.id}
                    role="menuitem"
                    onClick={() => { setOpen(null); onChoose(it.id); }}
                    className="metro-row flex w-full cursor-pointer flex-col items-start gap-0.5 rounded-xl border-0 px-3 py-1.5 text-left"
                    style={{ background: on ? "var(--surface)" : "transparent", color: "var(--ink)", fontFamily: "inherit" }}
                  >
                    <span className="flex items-center gap-2 text-[15px] font-semibold">
                      {it.color && <span className="h-3 w-3 shrink-0 rounded-full" style={{ border: `3px solid ${it.color}` }} />}
                      {it.label}
                    </span>
                    {it.sub && <span className="text-[13px] leading-snug" style={{ color: "var(--muted)" }}>{it.sub}</span>}
                  </button>
                );
              })}
            </section>
          ))}
          </div>
        </div>
      )}
    </div>
  );
}
