"""Promotes rows in db/seed/courses.json to tier_1_official, each rewritten from
official documents (named in its source), read first-hand on 2026-10-31.

Run from the project root:  python scripts/college-research/verify-courses.py
then:                        npm run db:import

Still pending_review: courses whose duration or entry route was not confirmed in a
primary document this session (B.Tech, Polytechnic, MBBS, BDS, AYUSH, B.Sc Nursing,
B.Pharm, B.Com/BBA, CA, BA, ITI x2, NDA - the UPSC notice URL now returns a web page,
B.Sc).
"""
import json
import os

V = "2026-10-31"
GOV = "government_notification"

COURSES = {
    "Agriculture & Veterinary Sciences (BVSc & AH)": dict(
        typical_duration="5.5 years: five professional years, the fourth lasting 1.5 years, and the fifth a one-year internship (VCI Minimum Standards of Veterinary Education 2016)",
        entry_via="AP EAPCET (Agriculture stream) for Sri Venkateswara Veterinary University seats in AP (TG EAPCET for PVNRTVU in Telangana); All India Quota through the Veterinary Council of India",
        source="SVVU Information brochure for B.V.Sc & A.H admissions 2026-27 (apsvvu-ugadmissions.aptonline.in/SVVU) and PVNRTVU Prospectus 2026-27 (pvnrtvu.tgonline.in/Files/Prospectus_Updated.pdf)"),
    "Law (BA/BBA/B.Com LLB)": dict(
        typical_duration="5 years (integrated LL.B. after Intermediate); a 3-year LL.B. is available after a degree",
        entry_via="AP LAWCET for law colleges of Andhra Pradesh universities (5-year LL.B.: Intermediate with 45%, 42% BC, 40% SC/ST); CLAT for national law universities such as DSNLU Visakhapatnam",
        source="AP LAWCET & PGLCET-2026 Instruction Booklet V2 (cets.apsche.ap.gov.in/LAWCET/PDF/APLAWCET2026_IntructionsBooklet_V2.pdf) and Consortium of NLUs CLAT 2027 participating universities and press release (consortiumofnlus.ac.in)"),
    "B.Arch (Architecture)": dict(
        typical_duration="5 years",
        entry_via="NATA (Council of Architecture) for most colleges; JEE Main Paper 2 through JoSAA / CSAB at central institutes such as SPA Vijayawada",
        source="Council of Architecture NATA site (nata.in) and SPA Vijayawada Admissions page (spav.ac.in/spavadmissions.php), read 2026-10-31"),
}

path = os.path.join(os.path.dirname(__file__), "..", "..", "db", "seed", "courses.json")
rows = json.load(open(path, encoding="utf-8"))
by_key = {r["course_name"]: r for r in rows}
missing = set(COURSES) - set(by_key)
assert not missing, f"not in seed: {missing}"
for k, fields in COURSES.items():
    by_key[k].update(fields, source_type=GOV, data_tier="tier_1_official", verified_date=V)
with open(path, "w", encoding="utf-8") as f:
    json.dump(rows, f, ensure_ascii=False, indent=2)
    f.write("\n")
print(f"courses: {len(COURSES)} rows verified")
