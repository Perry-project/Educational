import { pool } from "./db";
import { forStudents } from "./student-text";
import type { StopId } from "./second-chance-stops";

// Everything the /second-chance page shows, read from Postgres: the
// second_chance_routes table, one row per official route back into
// education or work, grouped by where the student stopped.
//
// Same rule as the exams: only verified rows (tier_1_official) carry their
// details to the page. A pending_review route is listed by name, body and
// official website only.

export type Route = {
  id: number;
  stoppedAt: StopId;
  name: string;
  scope: string; // National / Andhra Pradesh / Telangana
  kind: string | null;
  body: string | null;
  website: string | null;
  verified: boolean;
  summary: string | null;
  rows: [string, string][];
  open: boolean; // applications open right now, per the official dates
  examId: number | null; // the matching exam on /exams, when the route is an exam
  source: string | null;
};

const clean = (v: string | null) => {
  const t = forStudents(v);
  return t && t.trim() ? t : null;
};

export async function getSecondChanceRoutes(): Promise<Route[]> {
  const { rows } = await pool.query(
    `SELECT r.id, r.stopped_at, r.route_name, r.scope, r.kind, r.conducting_body, r.official_website,
            r.summary, r.who_can, r.how_to_apply, r.next_dates, r.leads_to, r.source, r.data_tier,
            (SELECT x.id FROM entrance_exams x WHERE x.exam_name = r.related_exam
              ORDER BY x.data_tier = 'tier_1_official' DESC LIMIT 1) AS exam_id
     FROM second_chance_routes r
     ORDER BY r.stopped_at, r.sequence_order NULLS LAST, r.route_name`,
  );
  return rows.map((r) => {
    const verified = r.data_tier === "tier_1_official";
    const dates = verified ? clean(r.next_dates) : null;
    return {
      id: r.id,
      stoppedAt: r.stopped_at,
      name: r.route_name,
      scope: r.scope,
      kind: r.kind,
      body: r.conducting_body,
      website: r.official_website,
      verified,
      summary: verified ? clean(r.summary) : null,
      rows: verified
        ? ([
            ["Who can use it", clean(r.who_can)],
            ["How to apply", clean(r.how_to_apply)],
            // The "Applications open" badge says it; the text doesn't need "(OPEN)" too.
            ["Dates", dates && dates.replace(/\s*\(OPEN[^)]*\)/g, "").replace(/\bOPEN:?\s+/g, "")],
            ["Leads to", clean(r.leads_to)],
          ].filter((p): p is [string, string] => !!p[1]))
        : [],
      open: !!dates && /\bOPEN\b/.test(dates),
      examId: r.exam_id,
      source: verified ? clean(r.source) : null,
    };
  });
}
