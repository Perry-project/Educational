"""Promotes Karnataka pathway and school rows to tier_1_official, each rewritten
from its own official document (named in its source) and read first-hand on
2026-10-31. Claims the document did not confirm were dropped, not carried over.

Run from the project root:  python scripts/karnataka-research/verify-karnataka.py
then:                        npm run db:import

Rows not listed here (CBSE/ICSE affiliation NOC rules, RTE 25% quota litigation,
residential-school PUC continuation, and the 2026-10-28 school rows) stay
pending_review until their own primary documents are read.
"""
import json
import os

KA = "Karnataka"
V = "2026-10-31"
GOV = "government_notification"

PUE = ("Department of School Education (Pre-University), Karnataka - Guidelines 2026-27 (Margasuchi), "
       "pue.karnataka.gov.in/uploads/guidelines_2026-27_1780740642.pdf: Chapter 1 admission calendar (p.2), "
       "Chapter 2 languages, electives and the approved subject combinations (pp.4-5), Chapter 3 1st PUC admission rules (pp.6-8)")
PUE_ADM = ("Apply directly to a Pre-University college; there is no state entrance test. Students passing Karnataka SSLC (or an "
           "equivalent exam of a COBSE-listed board) are eligible. Students from CBSE / ICSE / other boards or other states first get a "
           "provisional eligibility certificate online on the PU portal (pue.karnataka.gov.in), which the college verifies before admitting. "
           "Colleges may admit only to the languages and combinations the Department has sanctioned for them, at most 80 students per section, "
           "and enter every admission on the SATS portal")
PUE_WIN = ("2026-27 cycle (closed): 1st PUC admissions opened 24-04-2026; without penalty until 30-06-2026; with a Rs.670 late fee "
           "01-07-2026 to 10-07-2026; with a special penalty (Rs.2,220 + Rs.670) 11-07-2026 to 30-07-2026. Classes began 25-05-2026. "
           "The Department later issued a circular extending the 1st PUC admission date (see pue.karnataka.gov.in recent circulars). "
           "2027-28 dates not yet announced")
PUE_ELIG = "Passed Karnataka SSLC (Class 10) or an equivalent exam from a COBSE-listed board"
PUE_DUR = "2 years (1st PUC + 2nd PUC, Classes 11-12). Each student takes 2 languages (Part 1) and one combination of 4 elective subjects (Part 2)"

PATHWAYS = {
    "PUC Science - PCMB (Physics, Chemistry, Mathematics, Biology)": dict(
        eligibility=PUE_ELIG, admission_route=PUE_ADM, application_window=PUE_WIN, duration=PUE_DUR,
        leads_to="2nd PUC board exam (KSEAB) in Physics, Chemistry, Mathematics and Biology - the combination that keeps open KCET for Engineering, Farm Science and B.Pharm and NEET-UG for Medicine. PCMB is one of the 6 Science combinations the Department has approved (codes 33 34 35 36)",
        source=PUE),
    "PUC Science - PCMC (Physics, Chemistry, Mathematics, Computer Science)": dict(
        eligibility=PUE_ELIG, admission_route=PUE_ADM, application_window=PUE_WIN, duration=PUE_DUR,
        leads_to="2nd PUC board exam (KSEAB) in Physics, Chemistry, Mathematics and Computer Science - meets the KCET Engineering requirement (Physics and Mathematics plus Chemistry / Computer Science) and JEE Main. One of the 6 approved Science combinations (codes 33 34 35 41); the others add Electronics, Statistics, Geology or Home Science",
        source=PUE),
    "PUC Commerce - EBAC (Economics, Business Studies, Accountancy, Computer Science)": dict(
        eligibility=PUE_ELIG, admission_route=PUE_ADM, application_window=PUE_WIN, duration=PUE_DUR,
        leads_to="2nd PUC board exam (KSEAB) in Economics, Business Studies, Accountancy and Computer Science, then B.Com / BBA / BCA and CA-CS-CMA Foundation routes. One of the 9 approved Commerce combinations (codes 22 27 30 41)",
        source=PUE),
    "PUC Commerce - EBAS (Economics, Business Studies, Accountancy, Statistics)": dict(
        eligibility=PUE_ELIG, admission_route=PUE_ADM, application_window=PUE_WIN, duration=PUE_DUR,
        leads_to="2nd PUC board exam (KSEAB) in Economics, Business Studies, Accountancy and Statistics, then B.Com / Economics / Statistics degrees and CA-CS-CMA Foundation routes. One of the 9 approved Commerce combinations (codes 22 27 30 31)",
        source=PUE),
    "PUC Arts/Humanities (multiple combinations, e.g. HEPyS, EPPyS)": dict(
        eligibility=PUE_ELIG, admission_route=PUE_ADM, application_window=PUE_WIN, duration=PUE_DUR,
        leads_to="2nd PUC board exam (KSEAB) in the chosen Arts combination, then BA, law (CLAT / 5-year LLB), journalism, social work and other degree routes. The Department has approved 37 Arts combinations, e.g. HEPS (History, Economics, Political Science, Sociology), HEPyS (History, Economics, Sociology, Psychology) and EPPyS (Economics, Sociology, Political Science, Psychology)",
        source=PUE),
    "Karnataka Polytechnic Diploma - Merit-based (SSLC marks) via DTE Karnataka": dict(
        eligibility="Karnataka candidates only. Indian citizen who passed Karnataka SSLC or an equivalent exam; for engineering diploma courses at least 35% overall in SSLC",
        admission_route="No entrance exam (Karnataka has no POLYCET). For Government and aided polytechnics, download the application form and priority sheet from dtek.karnataka.gov.in / dtetech.karnataka.gov.in and submit it to the principal of any nearby Government polytechnic (or Code-1 aided polytechnic). Seats are then allotted online on SSLC-marks merit and reservation; seats left after allotment are filled offline at the polytechnic. Private polytechnics admit separately. Note: DCET (KEA) is a different exam, for diploma holders entering B.E. 2nd year",
        application_window="2026-27 cycle (closed): forms submitted 21-04-2026 to 16-05-2026; provisional merit list 16-05-2026, final merit list 18-05-2026, seat allotment 22-05-2026, admission 23-05-2026 to 25-05-2026, leftover seats filled offline 26-05-2026 to 30-05-2026. 2027-28 dates not yet announced",
        duration="Diploma (1st semester entry); engineering and non-engineering programmes",
        leads_to="Diploma - employment, or lateral entry to 2nd year B.E. through KEA's DCET",
        source="Department of Technical Education, Karnataka - 1st Semester Diploma Engineering & Non-Engineering Admission 2026-27 e-Information Brochure (dtetech.karnataka.gov.in/kartechnical/Files/DIP_ADMN_BROCHURE.pdf, admission process and schedule p.4) and DTE admission overview page (dtek.karnataka.gov.in/48/admission-overview: eligibility, 35% SSLC for engineering courses)"),
    "ITI - Engineering Trades": dict(
        eligibility="At least 14 years old on 01-08-2026. Indian citizen who studied at least 5 years between Classes 1 and 10 in recognised schools in Karnataka (exceptions for children of Central / State government employees posted in Karnataka, and Horanadu/Gadinadu Kannadigas). Most trades need a Class 10 pass (SSLC / KOS / CBSE / ICSE / NIOS or a COBSE-recognised board); Carpenter, Sheet Metal Worker, Welder, Wireman, Mason, Painter and Plumber also accept Class 8 pass or SSLC fail",
        admission_route="No entrance exam. Apply online at cite.karnataka.gov.in (Commissionerate of Industrial Training and Employment), choosing 1-20 trade/ITI options; free help desks at every ITI. Seats in 270 Government and 192 aided private ITIs (NCVT-affiliated units only) are allotted on merit and reservation in online rounds, then a casual round. Documents are verified at a Government ITI of the candidate's choice (Rs.50 fee)",
        application_window="2026 (August session, closed): online applications 27-04-2026 to 08-05-2026 (notification dated 24-04-2026); casual-round notification issued 27-05-2026. 2027 dates not yet announced",
        duration="Set by DGT per trade (NCVT); see the trade list on cite.karnataka.gov.in",
        leads_to="National Trade Certificate (NCVT) on passing the trade exam, then apprenticeship, skilled-trade jobs or further study",
        source="Commissionerate of Industrial Training and Employment, Karnataka - ITI admission notification for Government and aided ITIs, August 2026 session, dated 24-04-2026 (cite.karnataka.gov.in > Admission Notification, DITE/TRG/TRG-1/CR1/2026-2027/1); casual-round notification 2026-2027/2 dated 27-05-2026"),
    "ITI - Non-Engineering Trades": dict(
        eligibility="Same as Engineering trades: at least 14 on 01-08-2026, 5 years of schooling in Karnataka (with the listed exceptions). Most trades need a Class 10 pass; Dress Making, Sewing Technology and Surface Ornamentation Technique also accept Class 8 pass or SSLC fail",
        admission_route="Same single online process as Engineering trades at cite.karnataka.gov.in: merit-and-reservation online seat allotment across Government and aided ITIs, no entrance exam",
        application_window="2026 (August session, closed): online applications 27-04-2026 to 08-05-2026; casual round notified 27-05-2026. 2027 dates not yet announced",
        duration="Set by DGT per trade (NCVT); see the trade list on cite.karnataka.gov.in",
        leads_to="National Trade Certificate (NCVT) - self-employment, apprenticeship or jobs in the trade",
        source="Commissionerate of Industrial Training and Employment, Karnataka - ITI admission notification dated 24-04-2026 (cite.karnataka.gov.in, DITE/TRG/TRG-1/CR1/2026-2027/1)"),
    "NIOS Senior Secondary Course (Class 12 equivalent)": dict(
        eligibility="Passed Secondary (Class 10) from a recognised board; at least 15 years old (on 31-07-2026 for Block 1, on 31-01-2027 for Block 2). No upper age limit",
        admission_route="Online admission at sdmis.nios.ac.in (NIOS, Ministry of Education). Karnataka is served by the NIOS Regional Centre Bengaluru (RC 17); learners pick a study centre (Accredited Institution) while applying",
        application_window="2026-27 (Stream 1): Block 1 - 16-03-2026 to 31-07-2026 without late fee, then late-fee windows to 15-09-2026 (first exam March-April 2027). Block 2 - 16-09-2026 to 31-01-2027 without late fee, then late-fee windows (Rs.260 / 520 / 910) to 15-03-2027 (first exam September-October 2027). Fee for 5 subjects: Rs.2,600 (male), Rs.2,150 (female / third gender), Rs.1,690 (SC/ST, ex-servicemen, PwD)",
        duration="Admission is valid for five years, with public exams twice a year",
        leads_to="NIOS Senior Secondary certificate, accepted for degree admission and entrance exams like any Class 12 pass",
        source="NIOS Academic Prospectus 2026-27 (sdmis.nios.ac.in > Prospectus 2026-27: admission blocks p.21, entry requirements Table 3, fee Table 4) and NIOS Regional Centre list (nios.ac.in/about-us/regional-centre-website.aspx)"),
}

SCHOOLS = {
    "Jawahar Navodaya Vidyalaya (JNV)": dict(
        board_authority="Navodaya Vidyalaya Samiti (NVS), an autonomous body under the Ministry of Education, Government of India",
        ownership="Government (Central)",
        classes_covered="Classes 6-12 (co-educational, residential)",
        medium_of_instruction="Mother tongue or regional language up to Class 8; then English for Mathematics and Science and Hindi for Social Science. In Karnataka the JNVST can be written in Hindi, English, Kannada, Telugu, Marathi, Urdu, Malayalam or Tamil",
        key_exam="JNVST (Jawahar Navodaya Vidyalaya Selection Test) for Class 6; CBSE board exams in Classes 10 and 12",
        exam_window="JNVST 2027 (for 2027-28): last date to apply online was 31-07-2026; the test is on 28-11-2026 and admit cards are out at cbseitms.rcil.gov.in/nvs",
        passing_criteria="Admission on merit in the JNVST. Candidates must be born between 01-05-2015 and 31-07-2017, and must be bona fide residents of the district studying Class 5 there in 2026-27 (or in a neighbouring district within 10 km of home, still applying to their home district's JNV)",
        next_step="Students continue at the JNV through Class 12 under CBSE. Karnataka has 31 JNVs (30 + 1)",
        approx_fee="Education, board, lodging, uniform and textbooks are free. Classes 9-12 pay Vidyalaya Vikas Nidhi of Rs.600 a month (wards of Government employees up to Rs.1,500 or the Children Education Allowance); SC/ST, Divyang, all girls and BPL families are exempt",
        source="NVS JNVST 2027 Prospectus (cbseitms.rcil.gov.in/nvs/assets/pdf/Final_Prospectus_2027.pdf: introduction, state-wise JNV table, eligibility clause 4, medium table) and the JNVST portal announcement"),
    "Kendriya Vidyalaya (KV)": dict(
        board_authority="Kendriya Vidyalaya Sangathan (KVS), Ministry of Education, Government of India; Karnataka's KVs are under KVS Regional Office Bengaluru",
        ownership="Government (Central)",
        classes_covered="Balvatika (pre-primary, in selected KVs) and Classes 1-12",
        medium_of_instruction="CBSE-affiliated; the medium was not checked against a primary document",
        key_exam="CBSE board exams in Classes 10 and 12; no entrance test for Balvatika or Class 1",
        exam_window="2026-27 admissions (closed): online registration for Balvatika-1 & 3 and Class 1 from 20-03-2026 to 02-04-2026; provisional lists 08/09-04-2026, 16-04-2026 and 21-04-2026; offline registration for Balvatika-2 and Class 2 onwards (except 11) 02-04-2026 to 08-04-2026, subject to vacancies. 2027-28 schedule not yet announced",
        passing_criteria="Class 1 / Balvatika seats are filled from the online lists in this order: RTE seats, Service Priority Categories I and II, then any shortfall in the SC/ST/OBC (NCL) quotas, with offline notifications if online applications fall short",
        next_step="KVS Bengaluru Region lists 58 KVs (60,145 students). Students take CBSE board exams and go on to the same routes as other CBSE students",
        approx_fee="Not yet checked against the current KVS fee order",
        source="KVS Regional Office Bengaluru - Proposed Schedule for Admission 2026-27 (cdnbbsr.s3waas.gov.in/s3kv01edb5f385049e35efd27c9a97d11f/uploads/2026/03/2026032313.pdf) and robangalore.kvs.gov.in (KV and student counts, read 2026-10-31)"),
    "NIOS (National Institute of Open Schooling) - Secondary Course": dict(
        board_authority="National Institute of Open Schooling (NIOS), Ministry of Education, Government of India - the same national open-schooling board as in AP/Telangana; Karnataka is served by NIOS Regional Centre Bengaluru (RC 17)",
        ownership="Government (Central, autonomous); taught through NIOS Accredited Institutions (study centres)",
        classes_covered="Secondary Course (Class 10 equivalent)",
        medium_of_instruction="Not checked against a primary document for Karnataka",
        key_exam="NIOS Secondary public exam, held twice a year (March-April and September-October)",
        exam_window="2026-27 admission: Block 1 - 16-03-2026 to 31-07-2026 without late fee, late-fee windows to 15-09-2026 (first exam March-April 2027). Block 2 - 16-09-2026 to 31-01-2027 without late fee, late-fee windows to 15-03-2027 (first exam September-October 2027)",
        passing_criteria="Entry: at least 14 years old (on 31-07-2026 for Block 1, 31-01-2027 for Block 2), with a Class 8 marksheet or self-certificate; no upper age limit. Admission is valid for five years",
        next_step="NIOS Senior Secondary, or a Karnataka PU college (NIOS is a COBSE-listed board)",
        approx_fee="Admission fee for 5 subjects: Rs.2,340 (male), Rs.1,890 (female / third gender), Rs.1,560 (SC/ST, ex-servicemen, PwD); exam fees are extra",
        source="NIOS Academic Prospectus 2026-27 (sdmis.nios.ac.in > Prospectus 2026-27: admission blocks, Table 3 entry requirements, Table 4 fees) and NIOS Regional Centre list (nios.ac.in)"),
}

root = os.path.join(os.path.dirname(__file__), "..", "..", "db", "seed")
for name, updates, key in (("pathways", PATHWAYS, "pathway_name"), ("schools", SCHOOLS, "school_type")):
    path = os.path.join(root, f"{name}.json")
    rows = json.load(open(path, encoding="utf-8"))
    by_key = {r[key]: r for r in rows if r["state"] == KA}
    missing = set(updates) - set(by_key)
    assert not missing, f"{name}: not in seed: {missing}"
    for k, fields in updates.items():
        by_key[k].update(fields, source_type=GOV, data_tier="tier_1_official", verified_date=V)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"{name}: {len(updates)} Karnataka rows verified")
