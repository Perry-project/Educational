// The dropdown menus across the top of the desktop flowchart (/flowchart):
// every stop and career on the chart, sorted into a few menus a student can
// scan. Steps are grouped here by node id; careers by their cluster, with
// Engineering split into computing and core, and government jobs gathered
// again in a menu of their own. Client-safe: no `pg` import.

export type MenuGroup = { title: string; ids: string[] };
export type Menu = { id: string; label: string; groups: MenuGroup[] };

// Steps by node id (class10-flow-data.ts). A step missing from a state's
// chart, or with no career route through it, is left out of that menu.
export const STEP_MENUS: Menu[] = [
  {
    id: "school",
    label: "School education",
    groups: [
      { title: "Intermediate (Class 11–12)", ids: ["mpc", "bipc", "mec", "cec", "hec"] },
      { title: "Diploma & ITI", ids: ["polycet", "iti_eng", "iti_non"] },
      { title: "Other ways to finish school", ids: ["nios", "res"] },
    ],
  },
  {
    id: "exams",
    label: "Entrance exams",
    groups: [
      { title: "Engineering", ids: ["eapcet", "jeemain", "jeeadv", "ecet"] },
      { title: "Medical", ids: ["neet"] },
      { title: "Law, commerce & universities", ids: ["clat", "cafnd", "cuet", "nata"] },
      { title: "Defence", ids: ["nda", "cds", "afcat"] },
      { title: "After a degree", ids: ["icet", "icar"] },
    ],
  },
  {
    id: "college",
    label: "College education",
    groups: [
      { title: "Engineering & architecture", ids: ["btech", "diploma", "barch"] },
      { title: "Medical & health", ids: ["mbbs", "bds", "ayush", "nursing", "bpharm"] },
      { title: "Science & agriculture", ids: ["bsc", "agri"] },
      { title: "Commerce, law & arts", ids: ["bcom", "ca", "llb", "ba"] },
      { title: "Defence & trades", ids: ["ndatrain", "iticeng", "iticnon"] },
    ],
  },
];

// Careers are matched by careers.career_name, so Telangana's own rows (with
// longer names) land in the same groups.
const COMPUTING = /information technology|software|data science|cybersecurity|ethical hacking/i;
export const isComputing = (name: string) => COMPUTING.test(name);

// The government jobs menu, first match wins.
export const GOVT_GROUPS: [string, RegExp][] = [
  ["Civil services", /civil services/i],
  ["SSC, railways & police", /ssc|railways|group-d|constable|stenograph/i],
  ["Banking & teaching", /banking|teaching/i],
  ["Defence & forest", /defence services|agniveer|forest range/i],
];

