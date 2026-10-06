import { pool } from "./db";
import { IN_AP, type DataTier, type NodeTier } from "./flow-data";

export type CollegeMatch = {
  collegeName: string;
  ownership: string | null;
  admissionRoute: string | null;
  tier: NodeTier;
};

type CollegeRow = {
  college_name: string;
  ownership: string | null;
  offers_courses: string | null;
  admission_route: string | null;
  source: string | null;
  source_type: string | null;
  data_tier: DataTier;
  verified_date: string | null;
};

// offers_courses is a free-text, comma-separated list transcribed from the
// Drive snapshot (colleges has no normalized join to courses), so matching a
// course to its colleges is a substring test rather than a foreign key.
// Server-only (imports `pool`/`pg`) — never import this from a "use client"
// file; see decision-logic.ts for the client-safe half of this feature.
export async function getCollegesForCourse(courseName: string): Promise<CollegeMatch[]> {
  const { rows } = await pool.query<CollegeRow>(
    `SELECT college_name, ownership, offers_courses, admission_route, source, source_type, data_tier, verified_date::text
     FROM colleges
     WHERE offers_courses ILIKE '%' || $1 || '%' AND ${IN_AP}
     ORDER BY college_name`,
    [courseName]
  );

  return rows.map((r) => ({
    collegeName: r.college_name,
    ownership: r.ownership,
    admissionRoute: r.admission_route,
    tier: {
      dataTier: r.data_tier,
      sourceType: r.source_type,
      verifiedDate: r.verified_date,
      source: r.source,
    },
  }));
}
