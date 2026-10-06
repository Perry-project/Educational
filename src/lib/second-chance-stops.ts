// Where a student stopped: the five groups on /second-chance. Kept apart from
// second-chance-db.ts so the browser bundle doesn't pull in the database code.
export const STOPS = [
  { id: "class_10", label: "Class 10", long: "Failed or left Class 10" },
  { id: "intermediate", label: "Intermediate", long: "Failed or left Intermediate" },
  { id: "degree", label: "Degree or B.Tech", long: "Left a degree or B.Tech midway" },
  { id: "entrance_exam", label: "NEET, JEE or another exam", long: "Didn't clear an entrance exam" },
  { id: "working", label: "Working or older", long: "Already working, or older" },
] as const;

export type StopId = (typeof STOPS)[number]["id"];
