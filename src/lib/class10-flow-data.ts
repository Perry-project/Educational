// Content and route topology for the "Class 10 to Career" flowchart (/flow),
// ported verbatim from the Claude Design project "Class 10 to Career.dc.html".

export type StreamKey = "sci" | "com" | "hum" | "voc";

export type FlowNode = {
  id: string;
  col: 1 | 2 | 3 | 4;
  label: string;
  sub: string;
  st: StreamKey[];
  full: string;
  elig: string;
  when: string;
  by: string;
  note?: string;
};

export type FlowEdge = { f: string; t: string; dash: boolean; only?: string[] };

const S: StreamKey = "sci",
  C: StreamKey = "com",
  H: StreamKey = "hum",
  V: StreamKey = "voc",
  A3 = [S, C, H],
  A4 = [S, C, H, V];

export const NODES: FlowNode[] = [
  {id:'start',col:1,label:'Class 10 Pass',sub:'SSC · AP Board',st:A4,full:'Secondary School Certificate (Class 10)',elig:'Pass in the SSC Public Examination, or CBSE / ICSE equivalent',when:'Results usually April–May',by:'Board of Secondary Education, AP'},
  {id:'mpc',col:2,label:'Intermediate MPC',sub:'Maths · Physics · Chemistry',st:[S],full:'Two-year Intermediate course, MPC group',elig:'Class 10 pass',when:'2 years (Class 11–12)',by:'Board of Intermediate Education, AP'},
  {id:'bipc',col:2,label:'Intermediate BiPC',sub:'Biology · Physics · Chemistry',st:[S],full:'Two-year Intermediate course, BiPC group',elig:'Class 10 pass',when:'2 years (Class 11–12)',by:'Board of Intermediate Education, AP'},
  {id:'mec',col:2,label:'Intermediate MEC',sub:'Maths · Economics · Commerce',st:[C],full:'Two-year Intermediate course, MEC group',elig:'Class 10 pass',when:'2 years (Class 11–12)',by:'Board of Intermediate Education, AP'},
  {id:'cec',col:2,label:'Intermediate CEC',sub:'Civics · Economics · Commerce',st:[C,H],full:'Two-year Intermediate course, CEC group',elig:'Class 10 pass',when:'2 years (Class 11–12)',by:'Board of Intermediate Education, AP'},
  {id:'hec',col:2,label:'Intermediate HEC',sub:'History · Economics · Civics',st:[H],full:'Two-year Intermediate course, HEC group',elig:'Class 10 pass',when:'2 years (Class 11–12)',by:'Board of Intermediate Education, AP'},
  {id:'polycet',col:2,label:'AP POLYCET',sub:'Entrance for polytechnic diploma',st:[V],full:'Polytechnic Common Entrance Test',elig:'Class 10 pass; students awaiting results may apply',when:'Exam usually April–May',by:'SBTET, Andhra Pradesh'},
  {id:'iti_eng',col:2,label:'ITI Engineering Trades',sub:'Electrician, Fitter, Mechanic…',st:[V],full:'Industrial Training Institute, engineering trades',elig:'Class 10 pass (Class 8 for a few trades)',when:'1–2 years, by trade',by:'DGT, Govt. of India · AP Employment & Training'},
  {id:'iti_non',col:2,label:'ITI Non-Engineering Trades',sub:'COPA, Dress Making, Stenography…',st:[V],full:'Industrial Training Institute, non-engineering trades',elig:'Class 10 pass',when:'1 year for most trades',by:'DGT, Govt. of India · AP Employment & Training'},
  {id:'nios',col:2,label:'NIOS Senior Secondary',sub:'Open schooling, flexible subjects',st:A3,full:'National Institute of Open Schooling, Class 12 equivalent',elig:'Class 10 pass',when:'Usually 2 years; admission valid for 5 years',by:'NIOS, Ministry of Education'},
  {id:'res',col:2,label:'Residential schools',sub:'JNV · Sainik · Gurukulam',st:A3,full:'Continue Class 11–12 at a residential school',elig:'Already enrolled, or through the school’s own Class 11 admission',when:'2 years (Class 11–12)',by:'NVS · Sainik Schools Society · AP Gurukulam societies'},
  {id:'eapcet',col:3,label:'AP EAPCET',sub:'Engineering, Agri & Pharmacy',st:[S],full:'Engineering, Agriculture & Pharmacy Common Entrance Test',elig:'Intermediate MPC (engineering) or BiPC (agriculture, pharmacy), with minimum marks',when:'Usually May',by:'APSCHE, via a state university'},
  {id:'neet',col:3,label:'NEET-UG',sub:'Medical & allied courses',st:[S],full:'National Eligibility cum Entrance Test (UG)',elig:'Class 12 with Physics, Chemistry, Biology and English; age 17+',when:'Usually first Sunday of May',by:'National Testing Agency (NTA)'},
  {id:'jeemain',col:3,label:'JEE Main',sub:'NITs, IIITs · gateway to JEE Adv.',st:[S],full:'Joint Entrance Examination (Main)',elig:'Class 12 with Physics, Chemistry, Maths',when:'Two sessions: January and April',by:'National Testing Agency (NTA)'},
  {id:'jeeadv',col:3,label:'JEE Advanced',sub:'IIT admissions',st:[S],full:'Joint Entrance Examination (Advanced)',elig:'Top JEE Main rankers (about 2.5 lakh); max two attempts',when:'Usually late May',by:'One of the IITs, rotating yearly'},
  {id:'nata',col:3,label:'NATA',sub:'Architecture aptitude',st:[S],full:'National Aptitude Test in Architecture',elig:'Class 12 with Physics, Chemistry, Maths',when:'Several attempts, roughly April–July',by:'Council of Architecture'},
  {id:'cuet',col:3,label:'CUET-UG',sub:'Central & participating universities',st:A3,full:'Common University Entrance Test (UG)',elig:'Class 12, any stream; subject choice depends on course',when:'Usually May–June',by:'National Testing Agency (NTA)'},
  {id:'clat',col:3,label:'CLAT',sub:'National Law Universities',st:[C,H,S],full:'Common Law Admission Test (UG)',elig:'Class 12 with 45% (40% for SC/ST)',when:'Usually December, for the next year',by:'Consortium of National Law Universities'},
  {id:'cafnd',col:3,label:'CA Foundation',sub:'First level of Chartered Accountancy',st:[C,H],full:'Chartered Accountancy Foundation examination',elig:'Register after Class 10; appear after Class 12',when:'Held more than once a year',by:'ICAI'},
  {id:'nda',col:3,label:'NDA',sub:'Army, Navy & Air Force wings',st:A3,full:'National Defence Academy & Naval Academy Examination',elig:'Age 16.5–19.5; Class 12 (Physics & Maths for Navy and Air Force)',when:'Twice a year: April and September',by:'UPSC'},
  {id:'ecet',col:3,label:'AP ECET',sub:'Diploma → B.Tech 2nd year',st:[V],full:'Engineering Common Entrance Test (lateral entry)',elig:'Diploma in Engineering, or B.Sc with Maths',when:'Usually May',by:'APSCHE, via a state university'},
  {id:'icet',col:3,label:'AP ICET',sub:'MBA / MCA, after a degree',st:[C,S],full:'Integrated Common Entrance Test',elig:'Any bachelor’s degree with 50% (45% reserved); Maths at Class 12 for MCA',when:'Usually May',by:'APSCHE, via a state university'},
  {id:'icar',col:3,label:'ICAR AIEEA',sub:'Agri universities, ICAR quota',st:[S],full:'ICAR All India Entrance Examination for Admission',elig:'Class 12 with PCB, PCM or Agriculture',when:'Under review',by:'ICAR',note:'ICAR has reportedly admitted UG students through CUET-UG in recent years. This entry is being reviewed.'},
  {id:'cds',col:3,label:'CDS',sub:'Officer entry after a degree',st:A3,full:'Combined Defence Services Examination',elig:'Graduate; age limits vary by academy (about 19–25)',when:'Twice a year',by:'UPSC'},
  {id:'afcat',col:3,label:'AFCAT',sub:'Air Force officer entry',st:[S],full:'Air Force Common Admission Test',elig:'Graduate; Maths & Physics at Class 12 for flying branch',when:'Twice a year, roughly February and August',by:'Indian Air Force'},
  {id:'btech',col:4,label:'B.Tech',sub:'Engineering degree',st:[S,V],full:'Bachelor of Technology',elig:'EAPCET or JEE rank; diploma holders join 2nd year via AP ECET',when:'4 years (3 with lateral entry)',by:'AICTE · APSCHE counselling'},
  {id:'diploma',col:4,label:'Polytechnic Diploma',sub:'Engineering diploma',st:[V],full:'Diploma in Engineering & Technology',elig:'POLYCET rank; ITI holders may join 2nd year',when:'3 years (3.5 for some branches)',by:'SBTET, Andhra Pradesh'},
  {id:'mbbs',col:4,label:'MBBS',sub:'Bachelor of Medicine & Surgery',st:[S],full:'Bachelor of Medicine, Bachelor of Surgery',elig:'NEET-UG rank; state counselling by the health university, all-India quota by MCC',when:'5.5 years including 1-year internship',by:'National Medical Commission'},
  {id:'bds',col:4,label:'BDS',sub:'Dental surgery',st:[S],full:'Bachelor of Dental Surgery',elig:'NEET-UG rank',when:'5 years including internship',by:'Dental Council of India'},
  {id:'ayush',col:4,label:'AYUSH',sub:'BAMS · BHMS · BUMS',st:[S],full:'Ayurveda, Homoeopathy and Unani degrees',elig:'NEET-UG rank',when:'5.5 years including internship',by:'NCISM · NCH'},
  {id:'nursing',col:4,label:'B.Sc Nursing',sub:'Nursing degree',st:[S],full:'Bachelor of Science in Nursing',elig:'Class 12 with PCB and English; entrance route varies by year',when:'4 years',by:'Indian Nursing Council',note:'NEET-UG scores have been reported as the admission route in AP. Confirm in this year’s notification.'},
  {id:'bpharm',col:4,label:'B.Pharm',sub:'Pharmacy degree',st:[S],full:'Bachelor of Pharmacy',elig:'AP EAPCET rank (MPC or BiPC)',when:'4 years',by:'Pharmacy Council of India'},
  {id:'agri',col:4,label:'Agri & Vet (BVSc)',sub:'B.Sc Agriculture · BVSc',st:[S],full:'Agriculture, horticulture and veterinary degrees',elig:'EAPCET agriculture stream for B.Sc Agri; BVSc route varies',when:'4 years (Agri) · 5.5 years (BVSc)',by:'State agricultural and veterinary universities'},
  {id:'bcom',col:4,label:'B.Com / BBA',sub:'Commerce & business',st:[C],full:'Bachelor of Commerce / Business Administration',elig:'Intermediate, any stream; CUET for central universities',when:'3 years (4 with honours)',by:'State universities · APSCHE'},
  {id:'ca',col:4,label:'CA',sub:'Chartered Accountancy',st:[C,H],full:'Chartered Accountant qualification',elig:'Pass CA Foundation, then Intermediate and Final',when:'About 4.5–5 years including articleship',by:'ICAI'},
  {id:'llb',col:4,label:'Law (LLB)',sub:'5-year integrated BA / BBA LLB',st:[C,H],full:'Integrated Bachelor of Laws',elig:'CLAT for NLUs; AP LAWCET for state colleges',when:'5 years',by:'Bar Council of India'},
  {id:'ba',col:4,label:'BA Humanities',sub:'Arts & social sciences',st:[H],full:'Bachelor of Arts',elig:'Intermediate, any stream; CUET for central universities',when:'3 years (4 with honours)',by:'State universities · APSCHE'},
  {id:'bsc',col:4,label:'B.Sc Basic Sciences',sub:'Physics, Chemistry, Maths, Life sciences',st:[S],full:'Bachelor of Science',elig:'Intermediate MPC or BiPC; CUET for central universities',when:'3 years (4 with honours)',by:'State universities · APSCHE'},
  {id:'barch',col:4,label:'B.Arch',sub:'Architecture degree',st:[S],full:'Bachelor of Architecture',elig:'NATA score or JEE Main Paper 2',when:'5 years',by:'Council of Architecture'},
  {id:'ndatrain',col:4,label:'NDA Officer Training',sub:'Cadet training',st:A3,full:'Training at the National Defence Academy',elig:'Clear NDA written exam, SSB interview and medical',when:'3 years at NDA, then about 1 year at service academy',by:'Ministry of Defence'},
  {id:'iticeng',col:4,label:'ITI Certificate (Eng)',sub:'National Trade Certificate',st:[V],full:'National Trade Certificate, engineering trades',elig:'Complete ITI training and pass the trade test',when:'1–2 years',by:'DGT, Govt. of India'},
  {id:'iticnon',col:4,label:'ITI Certificate (Non-Eng)',sub:'National Trade Certificate',st:[V],full:'National Trade Certificate, non-engineering trades',elig:'Complete ITI training and pass the trade test',when:'1 year for most trades',by:'DGT, Govt. of India'},
];

export const byId: Record<string, FlowNode> = {};
NODES.forEach((n) => (byId[n.id] = n));

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

type ClusterDef = { id: string; name: string; list: [string, string[]][] };
const CL_DEFS: ClusterDef[] = [
  {id:'cl_eng',name:'Engineering & Tech',list:[['Software Engineer',['btech']],['Civil Engineer',['btech']],['Mechanical Engineer',['btech']],['Electrical Engineer',['btech']],['Electronics & Communication Engineer',['btech']],['Data Scientist',['btech','bsc']],['Junior Engineer (Govt.)',['diploma','btech']],['Diploma Technician',['diploma']],['Electrician',['iticeng']],['Fitter / Machinist',['iticeng']],['Automobile Mechanic',['iticeng']],['Computer Operator',['iticnon']]]},
  {id:'cl_med',name:'Medicine & Health',list:[['Doctor',['mbbs']],['Specialist Surgeon',['mbbs']],['Dentist',['bds']],['Ayurveda / Homoeopathy Doctor',['ayush']],['Nurse',['nursing']],['Pharmacist',['bpharm']],['Drug Inspector',['bpharm']],['Veterinarian',['agri']],['Public Health Officer',['mbbs','nursing']]]},
  {id:'cl_com',name:'Commerce & Finance',list:[['Chartered Accountant',['ca']],['Accountant',['bcom']],['Bank Officer',['bcom','bsc','ba']],['Financial Analyst',['bcom','ca']],['Business Manager (MBA)',['icet']],['Tax Consultant',['ca','bcom']],['Entrepreneur',['bcom','btech']],['Stenographer / Office Assistant',['iticnon']]]},
  {id:'cl_law',name:'Law & Civil Services',list:[['Advocate',['llb']],['Corporate Lawyer',['llb']],['Judge (Judicial Services)',['llb']],['IAS / IPS Officer',['ba','bsc','bcom','btech']],['APPSC Group-1 Officer',['ba','bsc','bcom']],['Legal Advisor',['llb']],['Policy Analyst',['ba']]]},
  {id:'cl_def',name:'Defence',list:[['Army Officer',['ndatrain']],['Navy Officer',['ndatrain']],['Air Force Officer',['ndatrain']],['Officer via CDS',['cds']],['Air Force Technical Officer',['afcat']],['Military Nursing Officer',['nursing']]]},
  {id:'cl_des',name:'Design & Arts',list:[['Architect',['barch']],['Urban Planner',['barch']],['Interior Designer',['barch']],['Journalist',['ba']],['Graphic Designer',['ba']],['Dress Designer',['iticnon']],['Content Writer / Translator',['ba']]]},
  {id:'cl_sci',name:'Science & Research',list:[['Research Scientist',['bsc']],['Agricultural Officer',['agri']],['Agri Scientist (ICAR)',['agri']],['Horticulture Officer',['agri']],['Statistician',['bsc']],['Environmental Scientist',['bsc']],['Biotechnologist',['bsc','btech']],['Psychologist',['ba','bsc']],['Professor / Lecturer',['bsc','ba']],['Lab Technician',['bsc']]]},
];

export type Career = { id: string; label: string; from: string[]; cl: Cluster; st: StreamKey[] };
export type Cluster = { id: string; name: string; items: Career[] };

export const CAREERS: Career[] = [];
export const crById: Record<string, Career> = {};
export const clById: Record<string, Cluster> = {};
export const CL: Cluster[] = CL_DEFS.map((def) => {
  const cl: Cluster = { id: def.id, name: def.name, items: [] };
  clById[cl.id] = cl;
  cl.items = def.list.map(([label, from], i) => {
    const st = [...new Set(from.flatMap((f) => byId[f].st))];
    const c: Career = { id: `${cl.id}_${i}`, label, from, cl, st };
    CAREERS.push(c);
    crById[c.id] = c;
    return c;
  });
  return cl;
});

export const col = (id: string) => (byId[id] ? byId[id].col : 5);

type Link = { f: string; t: string; dash: boolean; only?: string[] };
export const kids: Record<string, Link[]> = {};
export const pars: Record<string, Link[]> = {};
const link = (e: Link) => {
  (kids[e.f] = kids[e.f] || []).push(e);
  (pars[e.t] = pars[e.t] || []).push(e);
};
EDGES.forEach(link);
CAREERS.forEach((c) => c.from.forEach((f) => link({ f, t: c.id, dash: col(f) === 3 })));

// Lines drawn on the chart: node-to-node edges plus one line from each
// source course/exam into the career cluster card (careers live inside it).
export type DrawEdge = { f: string; t: string; dash: boolean; cl?: Cluster };
export const DRAW: DrawEdge[] = [
  ...EDGES,
  ...CL.flatMap((cl) =>
    [...new Set(cl.items.flatMap((c) => c.from))].map((f) => ({ f, t: cl.id, dash: col(f) === 3, cl }))
  ),
];

function down(id: string) {
  const out = new Set<string>(), seen = new Set<string>();
  const st: [string, string[] | null][] = [[id, null]];
  while (st.length) {
    const [x, only] = st.pop()!;
    const k = x + "|" + (only || "");
    if (seen.has(k)) continue;
    seen.add(k);
    out.add(x);
    (kids[x] || []).forEach((e) => {
      if (only && col(e.t) === 4 && !only.includes(e.t)) return;
      st.push([e.t, e.only || (col(e.t) < 4 ? only : null)]);
    });
  }
  return out;
}

function up(id: string) {
  const out = new Set<string>(), seen = new Set<string>();
  const st: [string, string | null][] = [[id, null]];
  while (st.length) {
    const [x, course] = st.pop()!;
    const k = x + "|" + (course || "");
    if (seen.has(k)) continue;
    seen.add(k);
    out.add(x);
    (pars[x] || []).forEach((e) => {
      if (e.only && course && !e.only.includes(course)) return;
      st.push([e.f, col(x) === 4 ? x : course]);
    });
  }
  return out;
}

// Every node on some route through `sel`: all its ancestors and descendants.
// For a cluster, the ancestors of each career inside it.
export function routeSet(sel: string) {
  if (clById[sel]) {
    const out = new Set([sel]);
    clById[sel].items.forEach((c) => up(c.id).forEach((x) => out.add(x)));
    return out;
  }
  const out = up(sel);
  down(sel).forEach((x) => out.add(x));
  return out;
}

export const nameOf = (id: string) =>
  byId[id] ? byId[id].label : crById[id] ? crById[id].label : clById[id].name;
