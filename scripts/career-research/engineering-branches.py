"""Adds one career line per engineering branch to db/seed/careers.json, so the
/flowchart Engineering field shows Civil, Mechanical, Chemical ... instead of
a single "Engineering" line, and gives every engineering career a list of
the jobs it leads to.

Run from the project root:  python scripts/career-research/engineering-branches.py
then:                        npm run db:import

What each row says and where it comes from:
- How to get in: the AP EAPCET, JEE Main and JEE (Advanced) rows already
  verified in the Exams tab (db/seed/entrance_exams.json).
- Diploma lateral entry: the AP ECET branch papers in the Exams tab (a branch
  is offered only where AP ECET has a paper for it).
- GATE paper and the PSUs that use GATE scores: GATE 2027 (IIT Madras),
  gate2027.iitm.ac.in/exam_papers_and_syllabus and /opportunities.
- UPSC Engineering Services: Civil, Mechanical, Electrical and Electronics &
  Telecommunication only (Notice No. 02/2027-ENGG).
These parts are tier_1_official. `job_roles` (the "Jobs" list) is
AI-assisted guidance, tier 3, and the site labels it that way.
"""
import json
import os

AP = "Andhra Pradesh"
VERIFIED = "2026-10-12"

EAPCET_ELIGIBILITY = (
    "AP EAPCET: Intermediate MPC with at least 45% in the qualifying subjects (40% for reserved categories) "
    "and AP local/non-local status. JEE Main: Class 12 with Physics, Chemistry and Maths. "
    "JEE Advanced: at most 2 attempts in consecutive years"
)
GATE_SRC = "GATE 2027 (IIT Madras): gate2027.iitm.ac.in/exam_papers_and_syllabus (paper codes) and /opportunities (PSUs that use GATE scores)"
ESE_SRC = "UPSC Engineering Services Examination 2027, Notice No. 02/2027-ENGG dated 16.09.2026 (Civil, Mechanical, Electrical, Electronics & Telecommunication)"
EXAMS_SRC = "Exams tab (verified): AP EAPCET 2026 Instruction Booklet, AP ECET 2026 branch papers, JEE Main 2026 and JEE (Advanced) 2026 notices"


def branch(name, category, gate, *, ecet, ese=None, psus, entry_extra="", exams_extra="", jobs, next_extra=""):
    """One engineering branch. `gate` is (code, paper name); `ese` the UPSC
    ESE category if the branch has one; `psus` PSUs from GATE 2027's own list
    that hire in this field (each PSU's notice names its disciplines)."""
    code, paper = gate
    entry = "After Intermediate MPC (4-year B.Tech)"
    if ecet:
        entry += ", or after a Polytechnic diploma in this branch (straight into B.Tech 2nd year through AP ECET)"
    govt = [
        f"Government: PSUs that recruit through GATE scores ({code} paper) - GATE 2027's list includes {psus}; each PSU's notification says which disciplines it hires",
    ]
    if ese:
        govt.append(f"UPSC Engineering Services ({ese} category) for central government engineering posts (engineering degree, age 21-30, with relaxations)")
    govt.append("state engineering departments recruit through APPSC/TSPSC notifications")
    return {
        "state": AP,
        "career_name": name,
        "category": category,
        "entry_point": entry + entry_extra,
        "required_exams": "AP EAPCET (Engineering stream) for colleges in Andhra Pradesh; JEE Main for NITs and IIITs; JEE Advanced for the IITs"
            + ("; AP ECET for diploma holders (lateral entry)" if ecet else "") + exams_extra,
        "eligibility": EAPCET_ELIGIBILITY,
        "govt_private_options": "; ".join(govt) + ". Private: see the jobs below",
        "next_step": f"M.Tech/M.E. through GATE paper {code} ({paper}) or AP PGECET; GATE score is valid for 3 years" + next_extra,
        "job_roles": jobs,
        "source": "; ".join([EXAMS_SRC, GATE_SRC] + ([ESE_SRC] if ese else [])),
        "source_type": "government_notification",
        "data_tier": "tier_1_official",
        "verified_date": VERIFIED,
    }


BRANCHES = [
    branch("Civil Engineering", "major", ("CE", "Civil Engineering"), ecet=True, ese="Civil",
        psus="NHAI, AAI, CVPPL, DVC, EIL, IOCL, NLCIL, NPCIL, NTPC and POWERGRID",
        jobs="Site engineer on buildings, roads and bridges; structural design engineer; highway and transportation engineer; "
             "water resources and irrigation engineer; geotechnical engineer; quantity surveyor and estimator; "
             "project planning and billing engineer; Assistant Engineer in state departments (Roads & Buildings, Panchayat Raj, irrigation, municipal); "
             "with an M.Tech or M.Plan: environmental engineer or town planner"),
    branch("Mechanical Engineering", "major", ("ME", "Mechanical Engineering"), ecet=True, ese="Mechanical",
        psus="BHEL, NTPC, IOCL, ONGC, GAIL, HAL, SAIL, RINL, NLCIL, Coal India, NPCIL and MDSL",
        jobs="Design engineer (CAD/CAE); production and manufacturing engineer; maintenance engineer in power plants, refineries and steel plants; "
             "quality engineer; automobile and EV engineer; HVAC and thermal engineer; aircraft maintenance (with DGCA licence); "
             "robotics and automation engineer; supply-chain and industrial engineer (GATE also has a Production & Industrial paper, PI)",
        next_extra="; GATE also has a Production & Industrial Engineering paper (PI)"),
    branch("Electrical & Electronics Engineering (EEE)", "major", ("EE", "Electrical Engineering"), ecet=True, ese="Electrical",
        psus="POWERGRID, GRID-INDIA, NTPC, BHEL, DVC, NLCIL, NPCIL, OPGC, Coal India and IOCL",
        jobs="Power-plant and substation engineer; transmission and distribution engineer (state DISCOMs and transmission companies); "
             "electrical design engineer for buildings and industry; renewable-energy (solar and wind) engineer; "
             "electric-vehicle and battery engineer; control and automation (PLC/SCADA) engineer; railway electrification; "
             "Assistant Engineer in state power utilities"),
    branch("Electronics & Communication Engineering (ECE)", "major", ("EC", "Electronics & Communication Engineering"), ecet=True,
        ese="Electronics & Telecommunication",
        psus="BSNL, ECIL, BHEL, HAL, AAI, POWERGRID and NTPC",
        jobs="VLSI and chip design engineer; embedded systems engineer; telecom and network engineer (4G/5G, optical fibre); "
             "electronics hardware and PCB design engineer; signal-processing engineer; IoT engineer; "
             "avionics and defence electronics; software jobs (many ECE graduates join IT companies)"),
    branch("Chemical Engineering", "major", ("CH", "Chemical Engineering"), ecet=True,
        psus="IOCL, ONGC, GAIL, EIL, NALCO, SAIL, RINL and NLCIL",
        jobs="Process engineer in oil refineries and petrochemicals; production engineer in pharmaceuticals, fertilisers, cement, paper, sugar and food plants; "
             "process design engineer (engineering consultancies); safety and environment engineer (HSE); "
             "quality control; water and effluent treatment; research in polymers, batteries and green hydrogen"),
    branch("Aerospace / Aeronautical Engineering", "niche", ("AE", "Aerospace Engineering"), ecet=False,
        psus="HAL and AAI",
        jobs="Aircraft design and structures engineer; aerodynamics and propulsion engineer; aircraft maintenance engineer (with DGCA licence); "
             "space and satellite engineer; drone (UAV) design; flight testing; defence aerospace labs"),
    branch("Biotechnology Engineering", "niche", ("BT", "Biotechnology"), ecet=True,
        psus="(GATE BT is used mainly for M.Tech and PhD admissions; few PSUs recruit in this field)",
        jobs="Production and quality roles in biopharma, vaccines and fermentation plants; research associate in labs; "
             "bioprocess engineer; clinical research and regulatory affairs; bioinformatics; food and agricultural biotech"),
    branch("Metallurgical & Materials Engineering", "niche", ("MT", "Metallurgical Engineering"), ecet=True,
        psus="SAIL, RINL, NALCO, NMDC, HAL, BHEL and NPCIL",
        jobs="Steel, aluminium and copper plant engineer; welding and foundry engineer; materials testing and failure analysis; "
             "quality control in automobile and aerospace parts; heat treatment and corrosion engineer; materials research"),
    branch("Mining Engineering", "niche", ("MN", "Mining Engineering"), ecet=True,
        psus="Coal India, NMDC, NLCIL, NTPC, SAIL and RINL",
        jobs="Mine planning and production engineer in coal, iron ore and limestone mines; mine safety officer; "
             "mine surveyor; mineral exploration; mine manager (after the statutory certificate of competency from DGMS)"),
    branch("Petroleum Engineering", "niche", ("PE", "Petroleum Engineering"), ecet=False,
        psus="ONGC, IOCL, GAIL and EIL",
        jobs="Drilling engineer; reservoir engineer; production engineer on oil and gas fields; pipeline engineer; "
             "refinery operations; offshore operations; gas and LNG terminals"),
    branch("Agricultural Engineering", "niche", ("AG", "Agricultural Engineering"), ecet=True,
        psus="(GATE AG is used mainly for M.Tech admissions)",
        exams_extra="; B.Tech Agricultural Engineering is in the AP EAPCET Engineering stream (MPC)",
        jobs="Farm machinery and tractor industry engineer; irrigation and water management engineer; soil and water conservation; "
             "food processing and post-harvest engineer; agricultural engineer in state agriculture and irrigation departments; "
             "precision farming and agri-drones"),
    branch("Electronics & Instrumentation Engineering (EIE)", "niche", ("IN", "Instrumentation Engineering"), ecet=True,
        psus="IOCL, NTPC, BHEL, ONGC, NPCIL, ECIL and GAIL",
        jobs="Instrumentation engineer in refineries, power plants, chemical and pharma plants; control systems (DCS/PLC/SCADA) engineer; "
             "industrial automation; calibration and testing; sensor and medical-instrument design"),
    branch("Biomedical Engineering", "niche", ("BM", "Biomedical Engineering"), ecet=False,
        psus="(GATE BM is used mainly for M.Tech admissions)",
        jobs="Biomedical engineer in hospitals (equipment maintenance); medical device design and testing; "
             "field service engineer for imaging machines (MRI, CT, X-ray); regulatory and quality roles; rehabilitation devices"),
    branch("Robotics & Automation", "niche", ("RA", "Robotics & Automation, new in GATE 2027"), ecet=False,
        psus="(a new paper; PSUs list the papers they accept in each notification)",
        jobs="Robotics engineer; industrial automation and PLC engineer; machine vision engineer; "
             "drone and autonomous-vehicle engineer; mechatronics design engineer"),
    branch("Naval Architecture & Marine Engineering", "niche", ("NM", "Naval Architecture & Marine Engineering"), ecet=False,
        psus="MDSL (shipbuilding)",
        jobs="Ship design engineer (naval architect); shipyard production engineer; offshore structures engineer; "
             "ship surveyor with classification societies; marine engineer (sea-going, after DG Shipping certificates)"),
]

# Jobs for the engineering lines that already exist (AI-assisted, tier 3).
EXISTING_JOBS = {
    "Engineering (B.Tech / B.E.)":
        "Pick a branch below the general line for its jobs: each engineering branch (Civil, Mechanical, Chemical ...) has its own line",
    "Information Technology / Software Engineering":
        "Software developer (web, mobile, backend); full-stack engineer; cloud and DevOps engineer; QA and test automation engineer; "
        "AI/ML engineer; database administrator; product and project roles after experience",
    "Data Science & Analytics":
        "Data analyst; business analyst; data scientist; machine learning engineer; data engineer; analytics roles in banks, e-commerce and healthcare",
    "Ethical Hacking / Cybersecurity":
        "Security analyst (SOC); penetration tester; network security engineer; incident responder; cyber forensics; cloud security engineer",
}

path = os.path.join(os.path.dirname(__file__), "..", "..", "db", "seed", "careers.json")
rows = json.load(open(path, encoding="utf-8"))
by_key = {(r["state"], r["career_name"]): r for r in rows}
added = 0
for b in BRANCHES:
    key = (b["state"], b["career_name"])
    if key in by_key:
        by_key[key].update(b)
    else:
        rows.append(b)
        added += 1
for name, jobs in EXISTING_JOBS.items():
    by_key[(AP, name)]["job_roles"] = jobs
with open(path, "w", encoding="utf-8") as f:
    json.dump(rows, f, ensure_ascii=False, indent=2)
    f.write("\n")
print(f"{len(rows)} careers ({added} new engineering branches)")
