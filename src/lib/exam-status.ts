// An exam's application status, read only from the dates in its official
// "Applications" text. No dates, or only past ones, means the next window
// isn't announced: Perry never guesses one. Client-safe.

export type AppStatus = { kind: "open" | "soon" | "na"; label: string };

const MONTHS = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"];

function datesIn(text: string): Date[] {
  const out: Date[] = [];
  for (const m of text.matchAll(/\b(\d{1,2})[-./](\d{1,2})[-./](\d{4})\b/g)) {
    out.push(new Date(Date.UTC(+m[3], +m[2] - 1, +m[1])));
  }
  for (const m of text.matchAll(/\b(\d{1,2})(?:st|nd|rd|th)?\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?,?\s+(\d{4})\b/gi)) {
    out.push(new Date(Date.UTC(+m[3], MONTHS.indexOf(m[2].slice(0, 3).toLowerCase()), +m[1])));
  }
  return out.filter((d) => !Number.isNaN(d.getTime()));
}

// Today in India, as a UTC midnight date so it compares with the parsed dates.
function todayIST(now = new Date()): Date {
  const [y, m, d] = new Intl.DateTimeFormat("en-CA", { timeZone: "Asia/Kolkata" }).format(now).split("-").map(Number);
  return new Date(Date.UTC(y, m - 1, d));
}

const short = (d: Date) => new Intl.DateTimeFormat("en-IN", { day: "numeric", month: "short", timeZone: "UTC" }).format(d);

export function applicationStatus(text: string | null | undefined, now?: Date): AppStatus {
  const na: AppStatus = { kind: "na", label: "Not announced yet" };
  if (!text) return na;
  const dates = datesIn(text);
  if (!dates.length) return na;
  const today = todayIST(now);
  const first = new Date(Math.min(...dates.map(Number)));
  const last = new Date(Math.max(...dates.map(Number)));
  if (today > last) return na;
  if (today < first) return { kind: "soon", label: `Opens ${short(first)}` };
  return { kind: "open", label: `Applications open · till ${short(last)}` };
}
