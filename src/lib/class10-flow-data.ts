// Route topology for the "Class 10 to Career" flowchart (/flowchart):
// the steps, their connections and which career field each career is in.
// metro-routes.ts turns this into routes; metro-flow.tsx draws them.
//
// Only what the database can't provide lives here: which card sits in which
// column, the short card labels, stream tags, the arrows between cards, and
// which career cluster each career belongs to. Every detail a student reads
// in the details panel comes from Postgres (src/lib/flowchart-db.ts).
// Client-safe: no `pg` import.

export type StreamKey = "sci" | "com" | "hum" | "voc";

export type FlowNode = {
  id: string;
  col: 1 | 2 | 3 | 4;
  label: string;
  sub: string;
  st: StreamKey[];
  full: string;
  // Exact pathway_name / exam_name / course_name of this card's row.
  db?: string;
};

export type FlowEdge = { f: string; t: string; dash: boolean; only?: string[] };

const S: StreamKey = "sci",
  C: StreamKey = "com",
  H: StreamKey = "hum",
  V: StreamKey = "voc",
  A3 = [S, C, H],
  A4 = [S, C, H, V];

export const NODES: FlowNode[] = [
  {id:'start',col:1,label:'Class 10 Pass',sub:'SSC · AP Board',st:A4,full:'Secondary School Certificate (Class 10)'},
  {id:'mpc',col:2,label:'Intermediate MPC',sub:'Maths · Physics · Chemistry',st:[S],full:'Two-year Intermediate course, MPC group',db:'Intermediate - MPC (Maths, Physics, Chemistry)'},
  {id:'bipc',col:2,label:'Intermediate BiPC',sub:'Biology · Physics · Chemistry',st:[S],full:'Two-year Intermediate course, BiPC group',db:'Intermediate - BiPC (Biology, Physics, Chemistry)'},
  {id:'mec',col:2,label:'Intermediate MEC',sub:'Maths · Economics · Commerce',st:[C],full:'Two-year Intermediate course, MEC group',db:'Intermediate - MEC (Maths, Economics, Commerce)'},
  {id:'cec',col:2,label:'Intermediate CEC',sub:'Civics · Economics · Commerce',st:[C,H],full:'Two-year Intermediate course, CEC group',db:'Intermediate - CEC (Commerce, Economics, Civics)'},
  {id:'hec',col:2,label:'Intermediate HEC',sub:'History · Economics · Civics',st:[H],full:'Two-year Intermediate course, HEC group',db:'Intermediate - HEC (History, Economics, Civics)'},
  {id:'polycet',col:2,label:'AP POLYCET',sub:'Entrance for polytechnic diploma',st:[V],full:'Polytechnic Common Entrance Test',db:'AP POLYCET - Polytechnic Diploma'},
  {id:'iti_eng',col:2,label:'ITI Engineering Trades',sub:'Electrician, Fitter, Mechanic…',st:[V],full:'Industrial Training Institute, engineering trades',db:'ITI - Engineering Trades'},
  {id:'iti_non',col:2,label:'ITI Non-Engineering Trades',sub:'COPA, Dress Making, Stenography…',st:[V],full:'Industrial Training Institute, non-engineering trades',db:'ITI - Non-Engineering Trades'},
  {id:'nios',col:2,label:'NIOS Senior Secondary',sub:'Open schooling, flexible subjects',st:A3,full:'National Institute of Open Schooling, Class 12 equivalent',db:'NIOS Senior Secondary Course (Class 12 equivalent)'},
  {id:'res',col:2,label:'Residential schools',sub:'JNV · Sainik · Gurukulam',st:A3,full:'Continue Class 11–12 at a residential school',db:'Continuation at a Central/State residential school (JNV, Sainik, RMS, AP Gurukulam, EMRS) into Class 11-12'},
  {id:'eapcet',col:3,label:'AP EAPCET',sub:'Engineering, Agri & Pharmacy',st:[S],full:'Engineering, Agriculture & Pharmacy Common Entrance Test',db:'AP EAPCET'},
  {id:'neet',col:3,label:'NEET-UG',sub:'Medical & allied courses',st:[S],full:'National Eligibility cum Entrance Test (UG)',db:'NEET-UG'},
  {id:'jeemain',col:3,label:'JEE Main',sub:'NITs, IIITs · gateway to JEE Adv.',st:[S],full:'Joint Entrance Examination (Main)',db:'JEE Main'},
  {id:'jeeadv',col:3,label:'JEE Advanced',sub:'IIT admissions',st:[S],full:'Joint Entrance Examination (Advanced)',db:'JEE Advanced'},
  {id:'nata',col:3,label:'NATA',sub:'Architecture aptitude',st:[S],full:'National Aptitude Test in Architecture',db:'NATA'},
  {id:'cuet',col:3,label:'CUET-UG',sub:'Central & participating universities',st:A3,full:'Common University Entrance Test (UG)',db:'CUET-UG'},
  {id:'clat',col:3,label:'CLAT',sub:'National Law Universities',st:[C,H,S],full:'Common Law Admission Test (UG)',db:'CLAT (UG)'},
  {id:'cafnd',col:3,label:'CA Foundation',sub:'First level of Chartered Accountancy',st:[C,H],full:'Chartered Accountancy Foundation examination',db:'CA Foundation'},
  {id:'nda',col:3,label:'NDA',sub:'Army, Navy & Air Force wings',st:A3,full:'National Defence Academy & Naval Academy Examination',db:'NDA (National Defence Academy exam)'},
  {id:'ecet',col:3,label:'AP ECET',sub:'Diploma → B.Tech 2nd year',st:[V],full:'Engineering Common Entrance Test (lateral entry)',db:'AP ECET'},
  {id:'icet',col:3,label:'AP ICET',sub:'MBA / MCA, after a degree',st:[C,S],full:'Integrated Common Entrance Test',db:'AP ICET'},
  {id:'icar',col:3,label:'ICAR AIEEA',sub:'Agri universities, ICAR quota',st:[S],full:'ICAR All India Entrance Examination for Admission',db:'ICAR AIEEA'},
  {id:'cds',col:3,label:'CDS',sub:'Officer entry after a degree',st:A3,full:'Combined Defence Services Examination',db:'CDS (Combined Defence Services exam)'},
  {id:'afcat',col:3,label:'AFCAT',sub:'Air Force officer entry',st:[S],full:'Air Force Common Admission Test',db:'AFCAT'},
  {id:'btech',col:4,label:'B.Tech',sub:'Engineering degree',st:[S,V],full:'Bachelor of Technology',db:'B.Tech / Engineering'},
  {id:'diploma',col:4,label:'Polytechnic Diploma',sub:'Engineering diploma',st:[V],full:'Diploma in Engineering & Technology',db:'Polytechnic Diploma'},
  {id:'mbbs',col:4,label:'MBBS',sub:'Bachelor of Medicine & Surgery',st:[S],full:'Bachelor of Medicine, Bachelor of Surgery',db:'MBBS'},
  {id:'bds',col:4,label:'BDS',sub:'Dental surgery',st:[S],full:'Bachelor of Dental Surgery',db:'BDS'},
  {id:'ayush',col:4,label:'AYUSH',sub:'BAMS · BHMS · BUMS',st:[S],full:'Ayurveda, Homoeopathy and Unani degrees',db:'AYUSH (BAMS/BHMS/BUMS/BSMS)'},
  {id:'nursing',col:4,label:'B.Sc Nursing',sub:'Nursing degree',st:[S],full:'Bachelor of Science in Nursing',db:'B.Sc Nursing'},
  {id:'bpharm',col:4,label:'B.Pharm',sub:'Pharmacy degree',st:[S],full:'Bachelor of Pharmacy',db:'B.Pharm (Pharmacy)'},
  {id:'agri',col:4,label:'Agri & Vet (BVSc)',sub:'B.Sc Agriculture · BVSc',st:[S],full:'Agriculture, horticulture and veterinary degrees',db:'Agriculture & Veterinary Sciences (BVSc & AH)'},
  {id:'bcom',col:4,label:'B.Com / BBA',sub:'Commerce & business',st:[C],full:'Bachelor of Commerce / Business Administration',db:'B.Com / BBA'},
  {id:'ca',col:4,label:'CA',sub:'Chartered Accountancy',st:[C,H],full:'Chartered Accountant qualification',db:'Chartered Accountancy (CA)'},
  {id:'llb',col:4,label:'Law (LLB)',sub:'5-year integrated BA / BBA LLB',st:[C,H],full:'Integrated Bachelor of Laws',db:'Law (BA/BBA/B.Com LLB)'},
  {id:'ba',col:4,label:'BA Humanities',sub:'Arts & social sciences',st:[H],full:'Bachelor of Arts',db:'BA Humanities'},
  {id:'bsc',col:4,label:'B.Sc Basic Sciences',sub:'Physics, Chemistry, Maths, Life sciences',st:[S],full:'Bachelor of Science',db:'B.Sc (Basic Sciences)'},
  {id:'barch',col:4,label:'B.Arch',sub:'Architecture degree',st:[S],full:'Bachelor of Architecture',db:'B.Arch (Architecture)'},
  {id:'ndatrain',col:4,label:'NDA Officer Training',sub:'Cadet training',st:A3,full:'Training at the National Defence Academy',db:'NDA / Naval Academy Officer Training'},
  {id:'iticeng',col:4,label:'ITI Certificate (Eng)',sub:'National Trade Certificate',st:[V],full:'National Trade Certificate, engineering trades',db:'ITI Trade Certificate (Engineering trades)'},
  {id:'iticnon',col:4,label:'ITI Certificate (Non-Eng)',sub:'National Trade Certificate',st:[V],full:'National Trade Certificate, non-engineering trades',db:'ITI Trade Certificate (Non-Engineering trades)'},
];

export const byId: Record<string, FlowNode> = {};
NODES.forEach((n) => (byId[n.id] = n));

// The chart covers one state at a time (?state=ts). Telangana reuses the same
// steps under its own names and rows; a card mapped to null has no Telangana
// row yet and is left off that chart rather than showing AP details.
export type StateKey = "ap" | "ts";
export const STATES: Record<StateKey, { name: string; short: string }> = {
  ap: { name: "Andhra Pradesh", short: "AP" },
  ts: { name: "Telangana", short: "Telangana" },
};
export const stateOf = (v: unknown): StateKey => (v === "ts" ? "ts" : "ap");

const TS_NODES: Record<string, Partial<FlowNode> | null> = {
  start: { sub: "SSC · Telangana Board" },
  polycet: { label: "TS POLYCET", db: "TS POLYCET - Polytechnic Diploma" },
  res: null,
  eapcet: { label: "TG EAPCET", db: "TG EAPCET (Telangana State Engineering, Agriculture & Pharmacy Common Entrance Test)" },
  ecet: { label: "TS ECET", db: "TS ECET (Telangana State Engineering Common Entrance Test)" },
  icet: { label: "TS ICET", db: "TS ICET (Telangana State Integrated Common Entrance Test)" },
};

export const nodesFor = (state: StateKey): FlowNode[] =>
  state === "ap"
    ? NODES
    : NODES.flatMap((n) => {
        const o = TS_NODES[n.id];
        return o === null ? [] : [{ ...n, ...o }];
      });

// Solid = main route, dashed = alternate / lateral. `only` restricts which
// courses a route continues to through that exam (e.g. MPC → EAPCET only
// leads on to B.Tech and B.Pharm, not Agri).
export const EDGES: FlowEdge[] = [];
const s = (f: string, ts: string[], only?: string[]) => ts.forEach((t) => EDGES.push({ f, t, dash: false, only }));
const d = (f: string, ts: string[], only?: string[]) => ts.forEach((t) => EDGES.push({ f, t, dash: true, only }));
s('start',['mpc','bipc','mec','cec','hec','polycet','iti_eng','iti_non','nios','res']);
s('mpc',['eapcet'],['btech','bpharm']);s('mpc',['jeemain','jeeadv','nata','nda']);d('mpc',['cuet','clat','cafnd','bsc']);
s('bipc',['eapcet'],['bpharm','agri']);s('bipc',['neet']);d('bipc',['icar','cuet','bsc','nda']);
s('mec',['cafnd','cuet']);d('mec',['clat','nda','bcom']);
s('cec',['clat','cafnd','cuet']);d('cec',['nda','bcom']);
s('hec',['clat','cuet']);d('hec',['nda','ba']);
s('polycet',['diploma']);s('iti_eng',['iticeng']);d('iti_eng',['diploma']);s('iti_non',['iticnon']);
d('nios',['neet','jeemain','eapcet','cuet','clat','nda','cafnd']);
s('res',['nda']);d('res',['jeemain','neet','cuet','eapcet']);
s('eapcet',['btech','bpharm','agri']);s('neet',['mbbs','bds','ayush','nursing']);d('neet',['agri']);
s('jeemain',['btech']);d('jeemain',['barch']);s('jeeadv',['btech']);s('nata',['barch']);
s('cuet',['bcom','ba','bsc']);d('cuet',['llb','agri']);s('clat',['llb']);s('cafnd',['ca']);s('nda',['ndatrain']);d('icar',['agri']);
d('diploma',['ecet']);d('ecet',['btech']);
d('btech',['icet','afcat']);d('bcom',['icet']);d('ba',['cds']);d('bsc',['cds','afcat']);

export const CLUSTER_DEFS: { id: string; name: string }[] = [
  { id: "cl_eng", name: "Engineering & Tech" },
  { id: "cl_med", name: "Medicine & Health" },
  { id: "cl_com", name: "Commerce & Finance" },
  { id: "cl_gov", name: "Law & Public Service" },
  { id: "cl_def", name: "Defence, Navy & Aviation" },
  { id: "cl_des", name: "Design, Media & Arts" },
  { id: "cl_sci", name: "Science, Agriculture & Nature" },
  { id: "cl_skl", name: "Hospitality & Skills" },
  { id: "cl_oth", name: "Other routes" },
];

// Where each careers.career_name sits: its cluster, and the cards it's
// reached from (read off the row's own entry_point / required_exams text).
// Careers with no single course or exam card behind them (e.g. Hotel
// Management via NCHMCT JEE) have no links: they appear in their cluster and
// the details panel explains the route. Careers missing from this map (new
// rows from the nightly routine) land in "Other routes".
export const CAREER_LINKS: Record<string, { cl: string; from: string[] }> = {
  "Engineering (B.Tech / B.E.)": { cl: "cl_eng", from: ["btech"] },
  "Information Technology / Software Engineering": { cl: "cl_eng", from: ["btech"] },
  "Data Science & Analytics": { cl: "cl_eng", from: ["btech", "bsc"] },
  "Ethical Hacking / Cybersecurity": { cl: "cl_eng", from: ["btech"] },

  "Medicine (MBBS)": { cl: "cl_med", from: ["mbbs"] },
  "Nursing (B.Sc Nursing)": { cl: "cl_med", from: ["nursing"] },
  "Pharmacy (B.Pharm)": { cl: "cl_med", from: ["bpharm"] },
  "Physiotherapy (BPT - Bachelor of Physiotherapy)": { cl: "cl_med", from: ["neet"] },
  "Yoga & Naturopathy (BNYS)": { cl: "cl_med", from: ["neet"] },
  "Occupational Therapy (BOT/BOTh)": { cl: "cl_med", from: ["bipc"] },
  "Paramedic / EMT (Emergency Medical Technician)": { cl: "cl_med", from: [] },
  "Speech-Language Pathology & Audiology (BASLP)": { cl: "cl_med", from: [] },
  "Psychology / Counselling": { cl: "cl_med", from: ["ba", "bsc"] },

  "Chartered Accountancy (CA)": { cl: "cl_com", from: ["ca"] },
  "Company Secretary (CS)": { cl: "cl_com", from: ["bcom"] },
  "Cost & Management Accountant (CMA)": { cl: "cl_com", from: ["bcom"] },
  "Banking (Probationary Officer / Clerk)": { cl: "cl_com", from: ["bcom", "ba", "bsc", "btech"] },
  "Actuarial Science": { cl: "cl_com", from: [] },
  "Real Estate / RERA-Registered Agent": { cl: "cl_com", from: [] },
  "ESG / Sustainability Consulting": { cl: "cl_com", from: ["bcom", "ba", "bsc", "btech"] },

  "Law (5-year integrated LLB)": { cl: "cl_gov", from: ["llb"] },
  "Civil Services (IAS/IPS/IFS - All India Services)": { cl: "cl_gov", from: ["ba", "bsc", "bcom", "btech"] },
  "State Civil Services (AP Group services via APPSC)": { cl: "cl_gov", from: ["ba", "bsc", "bcom", "btech"] },
  "Government Jobs - SSC CGL & Railways (RRB)": { cl: "cl_gov", from: ["ba", "bsc", "bcom", "btech"] },
  "Government Group-D / Constable-Level Jobs (SSC GD Constable, SSC MTS, AP Police Constable)": { cl: "cl_gov", from: ["start"] },
  "School Teaching (Govt & Private schools)": { cl: "cl_gov", from: ["ba", "bsc", "bcom"] },
  "Social Work (MSW - Master of Social Work)": { cl: "cl_gov", from: ["ba"] },
  "Court Stenography / Stenographer (Government)": { cl: "cl_gov", from: ["ba", "bcom"] },
  "Court Interpreter / Translator": { cl: "cl_gov", from: ["ba"] },

  "Defence Services (Army/Navy/Air Force Officer)": { cl: "cl_def", from: ["ndatrain", "cds"] },
  "Indian Air Force - Agniveer Vayu (Airmen) & AFCAT (Officer Entry)": { cl: "cl_def", from: ["afcat"] },
  "Merchant Navy - Officer Cadre (Nautical Science / Marine Engineering)": { cl: "cl_def", from: ["mpc"] },
  "Merchant Navy - Rating Entry (GP Rating)": { cl: "cl_def", from: ["start"] },
  "Aviation - Commercial Pilot (CPL)": { cl: "cl_def", from: ["mpc"] },
  "Aviation - Cabin Crew": { cl: "cl_def", from: [] },
  "Drone Pilot / Remote Pilot Certificate (RPAS)": { cl: "cl_def", from: ["start"] },

  "Architecture (B.Arch)": { cl: "cl_des", from: ["barch"] },
  "Interior Design (B.Des / B.I.D.)": { cl: "cl_des", from: [] },
  "Design (Fashion / Product / Communication Design)": { cl: "cl_des", from: [] },
  "Fashion Design & Styling": { cl: "cl_des", from: [] },
  "Animation, VFX & Game Design": { cl: "cl_des", from: [] },
  "Fine Arts & Performing Arts": { cl: "cl_des", from: [] },
  "Photography (Professional)": { cl: "cl_des", from: [] },
  "Journalism & Mass Communication": { cl: "cl_des", from: ["cuet"] },
  "Radio Jockey (RJ) / Voice-Over Artist": { cl: "cl_des", from: [] },
  "Puppetry / Theatre Arts": { cl: "cl_des", from: [] },

  "Science / Research (Basic Sciences)": { cl: "cl_sci", from: ["bsc"] },
  "Agriculture & Veterinary Sciences": { cl: "cl_sci", from: ["agri"] },
  "Dairy & Fisheries Science": { cl: "cl_sci", from: ["icar"] },
  "Veterinary Assistant / Livestock Inspector (Diploma route)": { cl: "cl_sci", from: ["start"] },
  "Forestry / Forest Range Officer": { cl: "cl_sci", from: ["bsc", "agri"] },
  "Wildlife Biology / Wildlife Conservation": { cl: "cl_sci", from: ["bsc"] },
  "Sports Science / Exercise Science": { cl: "cl_sci", from: [] },

  "Hotel Management (BSc Hospitality & Hotel Administration)": { cl: "cl_skl", from: [] },
  "Culinary Arts (Chef / Bakery & Confectionery)": { cl: "cl_skl", from: [] },
  "Baking & Confectionery Entrepreneurship (home/small bakery business)": { cl: "cl_skl", from: [] },
  "Event Management": { cl: "cl_skl", from: [] },
  "Pet Grooming & Canine Styling": { cl: "cl_skl", from: [] },
  "Sports Coaching": { cl: "cl_skl", from: [] },
};

// Telangana careers that stand in for an AP-specific career on the Telangana
// chart (same cluster and links). Other careers have no Telangana row yet.
export const TS_COUNTERPARTS: Record<string, string> = {
  "State Civil Services (Telangana Group services via TSPSC) (major)": "State Civil Services (AP Group services via APPSC)",
  "Government Group-D/Constable-Level Jobs - Telangana (TS Police Constable via TSLPRB, TSPSC Group-4) (major)":
    "Government Group-D / Constable-Level Jobs (SSC GD Constable, SSC MTS, AP Police Constable)",
  "School Teaching - Telangana (TS TET & TG DSC via Telangana School Education Dept) (major)": "School Teaching (Govt & Private schools)",
  "Forestry / Forest Range Officer - Telangana (TSPSC FRO & Forest Beat Officer) (niche)": "Forestry / Forest Range Officer",
};
for (const [ts, ap] of Object.entries(TS_COUNTERPARTS)) CAREER_LINKS[ts] = CAREER_LINKS[ap];

export const col = (id: string) => (byId[id] ? byId[id].col : 5);
