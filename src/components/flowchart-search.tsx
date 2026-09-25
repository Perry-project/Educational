"use client";

import { useId, useState } from "react";

// Search box for the flowchart: type part of a course, exam or career name
// and pick a suggestion to jump to that step.

export type SearchItem = {
  id: string;
  label: string;
  kind: string; // "Course", "Entrance exam", ...
  color: string; // CSS colour of the step's column
  text: string; // everything searchable, lower-case
};

const MAX = 8;

// Everyday words students type, mapped to the words the data uses.
const SYNONYMS: Record<string, string[]> = {
  doctor: ["medicine", "mbbs"], medical: ["medicine", "mbbs", "neet"], surgeon: ["medicine", "mbbs"],
  dentist: ["bds", "dental"], engineer: ["engineering", "b.tech"], lawyer: ["law", "llb"], advocate: ["law", "llb"],
  teacher: ["teaching"], nurse: ["nursing"], pharmacist: ["pharmacy", "b.pharm"],
  pilot: ["pilot", "aviation"], army: ["defence", "nda"], navy: ["navy", "naval"], "air force": ["air force", "afcat"],
  police: ["police", "constable"], ias: ["civil services"], ips: ["civil services"], chef: ["culinary"], cook: ["culinary"],
  computer: ["software", "information technology", "b.tech"], software: ["software", "information technology"], it: ["information technology"],
  accountant: ["accountancy", "ca", "cma"], bank: ["banking"], architect: ["architecture", "b.arch"],
  vet: ["veterinary", "bvsc"], farming: ["agriculture"], designer: ["design"], government: ["government", "govt"],
  "10th": ["class 10"], "12th": ["intermediate", "class 12"], inter: ["intermediate"], diploma: ["diploma", "polytechnic"],
};

// Alternatives a query word can match: itself, its synonyms, and a rough
// stem so "nurse" finds "nursing" and "engineers" finds "engineering".
function alternatives(word: string) {
  const syn = SYNONYMS[word] ?? [];
  // Two-letter words ("it") would match inside almost any text.
  if (word.length <= 2 && syn.length) return syn;
  const alts = [word, ...syn];
  if (word.length > 4) alts.push(word.replace(/(ing|ers|er|es|s|e)$/, ""));
  return alts;
}

export function searchItems(items: SearchItem[], query: string) {
  const words = query.toLowerCase().split(/\s+/).filter(Boolean);
  if (!words.length) return [];
  const q = words.join(" ");
  // Match at the start of a word, so "nda" doesn't hit "foundation".
  const esc = (s: string) => s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  const altsFor = words.map((w) => alternatives(w).map((a) => new RegExp(`(^|[^a-z0-9])${esc(a)}`)));
  return items
    .filter((it) => altsFor.every((alts) => alts.some((re) => re.test(it.text))))
    .sort((a, b) => {
      const rank = (it: SearchItem) => (it.label.toLowerCase().startsWith(q) ? 0 : it.label.toLowerCase().includes(q) ? 1 : 2);
      return rank(a) - rank(b) || a.label.localeCompare(b.label);
    })
    .slice(0, MAX);
}

export default function FlowchartSearch({ items, onChoose }: { items: SearchItem[]; onChoose: (id: string) => void }) {
  const [query, setQuery] = useState("");
  const [active, setActive] = useState(0);
  const [focused, setFocused] = useState(false);
  const listId = useId();
  const results = searchItems(items, query);
  const open = focused && query.trim() !== "";

  const choose = (id: string) => {
    setQuery("");
    setActive(0);
    onChoose(id);
  };

  return (
    <div style={{ position: "relative", flex: "1 1 280px", maxWidth: 420, minWidth: 0 }}>
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--muted)" strokeWidth="2" strokeLinecap="round" aria-hidden
        style={{ position: "absolute", left: 14, top: 12, pointerEvents: "none" }}>
        <circle cx="11" cy="11" r="7" /><path d="M20 20l-3.5-3.5" />
      </svg>
      <input
        type="search"
        value={query}
        onChange={(e) => { setQuery(e.target.value); setActive(0); }}
        onFocus={() => setFocused(true)}
        // Delay so a click on a suggestion lands before the list closes.
        onBlur={() => setTimeout(() => setFocused(false), 150)}
        onKeyDown={(e) => {
          if (e.key === "ArrowDown") { e.preventDefault(); setActive((a) => Math.min(a + 1, results.length - 1)); }
          else if (e.key === "ArrowUp") { e.preventDefault(); setActive((a) => Math.max(a - 1, 0)); }
          else if (e.key === "Enter" && results[active]) { e.preventDefault(); choose(results[active].id); }
          else if (e.key === "Escape") { e.stopPropagation(); setQuery(""); }
        }}
        placeholder="Search a course, exam or career (e.g. nurse, NEET, pilot)"
        aria-label="Search the flowchart"
        role="combobox"
        aria-expanded={open}
        aria-controls={listId}
        aria-autocomplete="list"
        aria-activedescendant={open && results[active] ? `${listId}-${active}` : undefined}
        className="c10-search"
        style={{
          width: "100%", height: 40, boxSizing: "border-box", padding: "0 14px 0 38px", borderRadius: 999,
          border: "1px solid var(--line)", background: "var(--surface)", color: "var(--ink)", font: "inherit", fontSize: 14,
        }}
      />
      {open && (
        <ul
          id={listId}
          role="listbox"
          style={{
            position: "absolute", zIndex: 30, top: 46, left: 0, right: 0, margin: 0, padding: 6, listStyle: "none",
            background: "var(--surface)", border: "1px solid var(--line)", borderRadius: 14, boxShadow: "0 18px 40px -18px rgba(0,0,0,.6)",
          }}
        >
          {results.length ? (
            results.map((r, i) => (
              <li
                key={r.id}
                id={`${listId}-${i}`}
                role="option"
                aria-selected={i === active}
                onMouseDown={(e) => { e.preventDefault(); choose(r.id); }}
                onMouseEnter={() => setActive(i)}
                style={{
                  display: "flex", alignItems: "center", gap: 10, minHeight: 44, padding: "6px 10px", borderRadius: 10, cursor: "pointer",
                  background: i === active ? "var(--bg)" : "transparent",
                }}
              >
                <span style={{ width: 8, height: 8, flex: "none", borderRadius: "50%", background: r.color }} />
                <span style={{ flex: 1, minWidth: 0, fontSize: 14, fontWeight: 600 }}>{r.label}</span>
                <span style={{ flex: "none", fontSize: 12, color: "var(--muted)" }}>{r.kind}</span>
              </li>
            ))
          ) : (
            <li style={{ padding: "10px 12px", fontSize: 14, color: "var(--muted)" }}>No matches. Try another word, like “doctor” or “engineering”.</li>
          )}
        </ul>
      )}
    </div>
  );
}
