// Turns researcher-facing database text into student-facing text.
//
// The nightly research routine writes its working notes into the same
// fields students read ("CORRECTED (verified Sept 2026): ...", "unverified,
// needs follow-up"). The database keeps them - they're the audit trail the
// data-safety rules rely on - but students see this cleaned version:
// process notes are dropped, and uncertainty is kept but reworded as
// "not yet confirmed" instead of being hidden.

// RULES-START
const RULES: [RegExp, string][] = [
  // Process notes about the research itself: drop.
  [/CORRECTED \(verified [^)]*\):\s*/gi, ""],
  [/\s*[-–]\s*confirmed accurate,? verified [A-Za-z]+ \d{4}/gi, ""],
  [/\s*[-–]\s*CORRECTS an earlier[\s\S]*?(?:supersedes it\.|\.(?=\s|$)|$)/gi, "."],
  [/\s*\([^)]*not fetched[^)]*\)/gi, ""],
  [/\s*\(via a secondary source\)/gi, ""],
  [/\s*[-–,]\s*flagged (?:for follow-up|below)/gi, ""],
  [/\s+(?:during|as of) this (?:check|pass|session)/gi, ""],
  [/\s+this (?:session|pass)\b/gi, ""],
  [/\s*\(not [^)]*previously listed[^)]*\)/gi, ""],
  [/\s*\(not (?:January|February|March|April|May|June|July|August|September|October|November|December)\)/g, ""],
  [/\bactually held\b/gi, "held"],
  [/,? needs [\w-]+ follow-up/gi, ""],
  // Uncertainty: keep, in plain words.
  [/NOT YET PRIMARY-VERIFIED:/g, "Note:"],
  [/\s*[-–,;]?\s*unverified,? needs follow-up/gi, " (not yet confirmed)"],
  [/,? needs follow-up/gi, ""],
  [/\bnot (?:independently |separately |fully )?(?:verified|confirmed)(?: in (?:general|available sources))?/gi, "not yet confirmed"],
  [/\bnot AP-verified\b/gi, "not confirmed for AP"],
  [/\bunverified\b/gi, "not yet confirmed"],
  [/\bacross trackers\b/gi, "across sources"],
  [/(not yet confirmed)\s*\(not yet confirmed\)/gi, "$1"],
  // Tidy up what the removals leave behind.
  [/\.\s*\./g, "."],
  [/\s+([.,;)])/g, "$1"],
  [/\s{2,}/g, " "],
];
// RULES-END

export function forStudents(text: string): string;
export function forStudents(text: string | null): string | null;
export function forStudents(text: string | null): string | null {
  if (!text) return text;
  return RULES.reduce((t, [re, to]) => t.replace(re, to), text).trim();
}
