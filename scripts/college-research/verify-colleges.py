"""Promotes rows in db/seed/colleges.json to tier_1_official, each rewritten from
an official list or prospectus (named in its source), read first-hand on 2026-10-31.

Run from the project root:  python scripts/college-research/verify-colleges.py
then:                        npm run db:import

Still pending_review: engineering colleges (JNTUK/JNTUA/JNTU-GV, AU, SVU, the private
universities and affiliated colleges - the AP EAPCET counselling institute list is
empty between counselling cycles), pharmacy colleges, polytechnics (AP POLYCET site
closed for the year), law colleges under AP LAWCET, Acharya Nagarjuna University,
Sri Padmavati Mahila Visvavidyalayam, SVIMS College of Nursing, DIET Boyapalem.
"""
import json
import os

AP = "Andhra Pradesh"
V = "2026-10-31"
GOV = "government_notification"

NMC = ("National Medical Commission, 'List of colleges teaching MBBS' (nmc.org.in/page/information-desk-for-students-to-study-in-india-list-of-college-teaching-mbbs, "
       "Andhra Pradesh entries, read 2026-10-31)")
def nmc(own, seats, univ="Dr. N.T.R. University of Health Sciences"):
    route = ("NEET-UG; affiliated to " + univ + ". Seats are filled through NEET-UG counselling - check each year's Medical Counselling "
             "Committee and Andhra Pradesh state counselling notifications")
    return dict(ownership=own, offers_courses=f"MBBS ({seats} seats a year per NMC)", admission_route=route, source=NMC)

COLLEGES = {
    "Andhra Medical College, Visakhapatnam": nmc("Government", 250),
    "Guntur Medical College, Guntur": nmc("Government", 250),
    "Rangaraya Medical College, Kakinada": nmc("Government", 250),
    "Kurnool Medical College, Kurnool": nmc("Government", 250),
    "Siddhartha Medical College, Vijayawada": nmc("Government", 250),
    "Sri Padmavathi Medical College for Women, Tirupati": nmc("Government", 175, "Sri Venkateswara Institute of Medical Sciences (SVIMS), Tirupati"),
    "NRI Medical College, Guntur": nmc("Private", 200),
    "Narayana Medical College, Nellore": nmc("Private", 250),
    "Maharajah's Institute of Medical Sciences, Vizianagaram": nmc("Private", 200),
    "P.E.S. Institute of Medical Sciences and Research, Kuppam": nmc("Private", 150),
    "Great Eastern Medical School and Hospital, Srikakulam": nmc("Private", 250),
    "GITAM Institute of Medical Sciences and Research, Visakhapatnam": dict(
        ownership="Private (deemed university)",
        offers_courses="MBBS (150 seats a year per NMC)",
        admission_route="NEET-UG; affiliated to GITAM (Deemed to be University), Visakhapatnam - not to Dr. N.T.R. UHS. Deemed-university MBBS seats are filled through NEET-UG counselling by the Medical Counselling Committee (MCC); check the MCC notification",
        source=NMC),
    "AIIMS Mangalagiri, Vijayawada": dict(
        ownership="Government (Central, Institute of National Importance)",
        offers_courses="MBBS (125 seats), B.Sc Nursing (Hons), B.Sc allied and healthcare courses, MD/MS/DM/MCh and others",
        admission_route="MBBS: NEET-UG, with seats allotted through Medical Counselling Committee (MCC) counselling (not state counselling). B.Sc (Hons) Nursing and allied courses: as per AIIMS admission notices on aiimsmangalagiri.edu.in",
        source="AIIMS Mangalagiri MBBS Prospectus 2026 and Instructions for MBBS Admissions 2026 (aiimsmangalagiri.edu.in/wp-content/uploads/2026/08/), and the institute's Admission menu, read 2026-10-31"),
    "Damodaram Sanjivayya National Law University (DSNLU), Visakhapatnam": dict(
        ownership="Government (State national law university)",
        offers_courses="Law (BA LLB Hons, 5-year integrated), LLM",
        admission_route="CLAT (UG) - DSNLU Visakhapatnam is a participating university for CLAT 2027. CLAT 2027 is on 06-12-2026 (2-4 PM); online applications 03-08-2026 to 31-10-2026",
        source="Consortium of NLUs: CLAT 2027 participating universities page (consortiumofnlus.ac.in/clat-2027/participating_universities.html) and CLAT 2027 press release dated 22-07-2026"),
    "School of Planning and Architecture (SPA), Vijayawada": dict(
        ownership="Government (Central, Institute of National Importance)",
        offers_courses="B.Arch and B.Plan (UG), plus PG programmes",
        admission_route="UG (B.Arch / B.Plan): through JoSAA / CSAB central counselling (JEE Main based); foreign / NRI seats through DASA. Not through NATA / APSCHE counselling",
        source="SPA Vijayawada Admissions page (spav.ac.in/spavadmissions.php: instructions for students admitted to UG programmes through JoSAA/CSAB and DASA, 2025 and 2026), read 2026-10-31"),
    "Acharya N.G. Ranga Agricultural University (ANGRAU), Guntur": dict(
        ownership="Government (State agricultural university)",
        offers_courses="Agriculture: B.Sc (Hons) Agriculture at 7 constituent colleges (Bapatla, Naira, Rajahmahendravaram, S.V. Agricultural College Tirupati, Mahanandi, Udayagiri, Pulivendula) and 6 affiliated colleges; B.Tech (Food Technology) at Bapatla and Pulivendula. (B.V.Sc & A.H is offered by Sri Venkateswara Veterinary University, not ANGRAU)",
        admission_route="AP EAPCET (Agriculture stream) rank, through ANGRAU's online counselling (ugadmissionsangrau.aptonline.in); 2026-27 Phase II allotment released 19-10-2026",
        source="ANGRAU Information Brochure for UG admissions 2026-27 (ugadmissionsangrau.aptonline.in/ANGRAUGRADU, file PDF20260729114322.pdf) and the ANGRAU UG admissions portal, read 2026-10-31"),
    "NTR College of Veterinary Science, Gannavaram (Sri Venkateswara Veterinary University)": dict(
        ownership="Government (constituent college of Sri Venkateswara Veterinary University, Tirupati)",
        offers_courses="Veterinary Sciences: B.V.Sc & A.H (70 seats: 64 + 6 EWS); 5.5 years including internship (VCI MSVE 2016)",
        admission_route="AP EAPCET (Agriculture stream) rank through SVVU's online admission (apsvvu-ugadmissions.aptonline.in); All India Quota B.V.Sc seats through the Veterinary Council of India portal (vci.admissions.nic.in)",
        source="SVVU Information brochure for B.V.Sc & A.H admissions 2026-27 (apsvvu-ugadmissions.aptonline.in/SVVU, file PDF20261026115304.pdf) and svvu.edu.in, read 2026-10-31"),
}

path = os.path.join(os.path.dirname(__file__), "..", "..", "db", "seed", "colleges.json")
rows = json.load(open(path, encoding="utf-8"))
by_key = {r["college_name"]: r for r in rows if r["state"] == AP}
missing = set(COLLEGES) - set(by_key)
assert not missing, f"not in seed: {missing}"
for k, fields in COLLEGES.items():
    by_key[k].update(fields, source_type=GOV, data_tier="tier_1_official", verified_date=V)
with open(path, "w", encoding="utf-8") as f:
    json.dump(rows, f, ensure_ascii=False, indent=2)
    f.write("\n")
print(f"colleges: {len(COLLEGES)} rows verified")
