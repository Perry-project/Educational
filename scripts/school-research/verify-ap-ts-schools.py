"""Promotes Andhra Pradesh / Telangana school-stage rows to tier_1_official, each
rewritten from its own official document (named in its source), read first-hand
on 2026-10-31. Claims the document did not confirm were dropped or marked
"not yet available".

Run from the project root:  python scripts/school-research/verify-ap-ts-schools.py
then:                        npm run db:import

Still pending_review after 2026-10-31 (primary document not reached or not specific enough):
 AP: CBSE, ICSE, AP Gurukulam (4 societies; only the APREIS APRS CAT 2026 prospectus was found),
     EMRS (28 co-ed EMRS listed on aptwgurukulam.ap.gov.in, but no 2026 admission notice), the 8
     GO.19 school types, RTE 25% quota.
 TS: State Board (DGE site gives age 14+ and fee Rs.125, but not the pass marks or 2026 dates),
     CBSE, ICSE, EMRS (23 CBSE co-ed EMRS per tsemrs.telangana.gov.in; only 2025-26 guidelines
     posted), KGBV, TMREIS (documents are behind javascript links), RTE 25% quota.
"""
import json
import os

AP, TS = "Andhra Pradesh", "Telangana"
V = "2026-10-31"
GOV = "government_notification"

JNV_SRC = ("NVS JNVST 2027 Prospectus (cbseitms.rcil.gov.in/nvs/assets/pdf/Final_Prospectus_2027.pdf: section 1.1 state-wise JNVs, "
           "eligibility clause 4, reservation of seats, medium-of-test table) and the JNVST portal announcement (admit cards live)")
def jnv(count, langs):
    return dict(
        board_authority="Navodaya Vidyalaya Samiti (NVS), an autonomous body under the Ministry of Education, Government of India; CBSE-affiliated",
        ownership="Government (Central), co-educational and residential",
        classes_covered="Classes 6-12",
        medium_of_instruction=f"Mother tongue or regional language up to Class 8, then English for Mathematics and Science and Hindi for Social Science. The JNVST can be written in {langs}",
        key_exam="JNVST (Jawahar Navodaya Vidyalaya Selection Test) for Class 6; CBSE board exams in Classes 10 and 12",
        exam_window="JNVST 2027 (for 2027-28): last date to apply was 31-07-2026; the test is on 28-11-2026 and admit cards are out at cbseitms.rcil.gov.in/nvs",
        passing_criteria="Merit in the JNVST. Born between 01-05-2015 and 31-07-2017; bona fide resident of the district and studying Class 5 there in 2026-27 (or in a neighbouring district within 10 km of home, still applying to the home district's JNV). At least 75% of seats go to rural candidates; SC/ST seats in proportion to district population (at least 15% / 7.5%), 27% OBC (central list), at least one-third girls. Up to 80 students per JNV",
        next_step=f"Students continue at the JNV through Class 12 under CBSE. {count}",
        approx_fee="Education, board, lodging, uniforms and textbooks are free. Classes 9-12 pay Vidyalaya Vikas Nidhi of Rs.600 a month (wards of Government employees up to Rs.1,500 or the Children Education Allowance); SC/ST, Divyang, all girls and BPL families are exempt",
        source=JNV_SRC)

KV_SRC = ("KVS Proposed Schedule for Admission 2026-27 (cdnbbsr.s3waas.gov.in/s3kv01edb5f385049e35efd27c9a97d11f/uploads/2026/03/2026032313.pdf) "
          "and KVS Regional Office Hyderabad website (rohyderabad.kvs.gov.in: 85 KVs, 71,521 students, read 2026-10-31)")
KV = dict(
    board_authority="Kendriya Vidyalaya Sangathan (KVS), Ministry of Education, Government of India; CBSE-affiliated. Regional Office Hyderabad lists 85 KVs",
    ownership="Government (Central), non-residential",
    classes_covered="Balvatika (pre-primary, in selected KVs) and Classes 1-12",
    medium_of_instruction="Not yet checked against a primary KVS document",
    key_exam="CBSE board exams in Classes 10 and 12; no entrance test for Balvatika or Class 1",
    exam_window="2026-27 admissions (closed): online registration for Balvatika-1 & 3 and Class 1 from 20-03-2026 to 02-04-2026; provisional lists 08/09-04-2026, 16-04-2026 and 21-04-2026; offline registration for Balvatika-2 and Class 2 onwards (except 11) 02-04-2026 to 08-04-2026, subject to vacancies. 2027-28 schedule not yet announced",
    passing_criteria="Class 1 / Balvatika seats are filled from the online lists in this order: RTE seats, Service Priority Categories I and II, then any shortfall in the SC/ST/OBC (NCL) quotas, with an offline notification if online applications fall short",
    next_step="CBSE board exams in Classes 10 and 12, then the same routes as other CBSE students",
    approx_fee="Not yet checked against the current KVS fee order",
    source=KV_SRC)

NIOS_SRC = ("NIOS Academic Prospectus 2026-27 (sdmis.nios.ac.in > Prospectus 2026-27: medium of instruction, scheme of studies, admission blocks, "
            "Table 3 entry requirements, Table 4 fees, Regional Centres list - RC Hyderabad covers Telangana and Andhra Pradesh)")
NIOS = dict(
    board_authority="National Institute of Open Schooling (NIOS), Ministry of Education, Government of India; Andhra Pradesh and Telangana are served by NIOS Regional Centre Hyderabad (rchyderabad.nios.ac.in)",
    ownership="Government (Central, autonomous); taught through NIOS Accredited Institutions (study centres)",
    classes_covered="Secondary Course (Class 10 equivalent)",
    medium_of_instruction="Secondary can be taken in Hindi, English, Urdu, Marathi, Telugu, Gujarati, Malayalam, Tamil, Odia, Punjabi, Assamese, Sanskrit or Kannada medium",
    key_exam="NIOS Secondary public exam, twice a year (March-April and September-October)",
    exam_window="2026-27 admission: Block 1 - 16-03-2026 to 31-07-2026 without late fee, late-fee windows to 15-09-2026 (first exam March-April 2027). Block 2 - 16-09-2026 to 31-01-2027 without late fee, late-fee windows to 15-03-2027 (first exam September-October 2027) - Block 2 is open now",
    passing_criteria="Entry: at least 14 years old (on 31-07-2026 for Block 1, 31-01-2027 for Block 2) with a Class 8 marksheet or self-certificate; no upper age limit. To pass, clear at least five subjects (one or two languages plus others) with 33% aggregate (theory plus practical / internal) in each. Admission is valid for five years",
    next_step="NIOS Senior Secondary, or Intermediate / POLYCET / ITI like any Class 10 pass",
    approx_fee="Admission fee for 5 subjects: Rs.2,340 (male), Rs.1,890 (female / third gender), Rs.1,560 (SC/ST, ex-servicemen, PwD); exam fees are extra",
    source=NIOS_SRC)

RMS_SRC = ("Rashtriya Military Schools official website (rashtriyamilitaryschools.edu.in: 'Our Schools' and 'Admission' pages, and the latest-news "
           "item 'Applications for admission to Class VI and IX for boys and girls'), read 2026-10-31")
def rms(state):
    return dict(
        board_authority="Rashtriya Military Schools, Ministry of Defence, Government of India; CBSE-affiliated",
        ownership="Government (Central), residential (boarders only)",
        classes_covered="Classes 6-12 (entry at Class 6 and Class 9)",
        medium_of_instruction="English",
        key_exam="RMS Common Entrance Test (OMR based) for Class 6 and Class 9, held in December",
        exam_window="Last date and test date are set in each year's CET notification on rashtriyamilitaryschools.edu.in",
        passing_criteria="Age 10-12 years for Class 6 and 13-15 years for Class 9 on 31 March of the admission year; admission against available vacancies. The site's admission page says admissions are for boys only, but its latest notice invites boys and girls - check the current CET notification",
        next_step=f"There is no RMS in {state}: the five campuses are at Ajmer and Dholpur (Rajasthan), Bengaluru and Belgaum (Karnataka) and Chail (Himachal Pradesh), open to students from any state through the CET",
        approx_fee="Not yet checked against a primary document",
        source=RMS_SRC)

SCHOOLS = {
    (AP, "Jawahar Navodaya Vidyalaya (JNV)"): jnv("Andhra Pradesh has 15 JNVs (13 plus 2 sanctioned for SC/ST-concentrated districts)", "Hindi, English, Telugu, Marathi, Urdu, Oriya or Kannada"),
    (TS, "Jawahar Navodaya Vidyalaya (JNV)"): jnv("Telangana has 15 functional JNVs", "Hindi, English, Telugu, Kannada, Marathi or Urdu"),
    (AP, "Kendriya Vidyalaya (KV)"): KV,
    (TS, "Kendriya Vidyalaya (KV)"): KV,
    (AP, "NIOS (National Institute of Open Schooling) - Secondary Course"): NIOS,
    (TS, "NIOS (National Institute of Open Schooling) - Secondary Course"): NIOS,
    (AP, "Rashtriya Military School (RMS) - none located in AP"): rms("Andhra Pradesh"),
    (TS, "Rashtriya Military School (RMS) - none located in Telangana"): rms("Telangana"),
    (AP, "Sainik School"): dict(
        board_authority="Sainik Schools Society, Ministry of Defence, Government of India; CBSE-affiliated",
        ownership="Government (Central), residential",
        classes_covered="Classes 6-12 (entry at Class 6 and Class 9)",
        medium_of_instruction="English",
        key_exam="AISSEE (All India Sainik Schools Entrance Examination), conducted by NTA",
        exam_window="AISSEE-2026 is complete (results declared, online counselling running). The AISSEE-2027 information bulletin is not yet out; watch sainikschoolsociety.in and exams.nta.nic.in/sainik-school-society",
        passing_criteria="Admission at Class 6 and Class 9 on AISSEE performance; eligibility, exam scheme and reservation are set in each year's Information Bulletin",
        next_step="Andhra Pradesh has two Sainik Schools: Sainik School Korukonda and Sainik School Kalikiri. Students continue to Class 12 with preparation for NDA",
        approx_fee="Set by each school (Korukonda collects the 2026-27 school fee online on sainikschoolkorukonda.org); amount not yet checked",
        source="Sainik Schools Society website (sainikschoolsociety.in: home page and 'Existing Schools' list) and Sainik School Korukonda website (sainikschoolkorukonda.org), read 2026-10-31"),
    (TS, "Sainik School - none located in Telangana"): dict(
        board_authority="Sainik Schools Society, Ministry of Defence, Government of India",
        ownership="Government (Central), residential - none of the Society's existing schools is in Telangana",
        classes_covered="Classes 6-12 at Sainik Schools in other states",
        medium_of_instruction="English",
        key_exam="AISSEE (All India Sainik Schools Entrance Examination), conducted by NTA, for Class 6 and Class 9",
        exam_window="AISSEE-2027 information bulletin not yet out; watch sainikschoolsociety.in",
        passing_criteria="Admission on AISSEE performance as per each year's Information Bulletin",
        next_step="Telangana students can apply through AISSEE to Sainik Schools elsewhere, e.g. Korukonda or Kalikiri in Andhra Pradesh. The Society also affiliates new partnership Sainik Schools; their state-wise list was not checked. (The TGSWREIS 'Sainik schools' at Rukmapur and Jagathgirigutta are Telangana welfare-society schools, entered through TGCET, not Sainik Schools Society schools)",
        approx_fee="Set by each school",
        source="Sainik Schools Society website (sainikschoolsociety.in: 'Existing Schools' and 'New Schools' pages), read 2026-10-31"),
    (AP, "State Board (Govt & Govt-aided) School"): dict(
        board_authority="Board of Secondary Education, Andhra Pradesh (Directorate of Government Examinations)",
        ownership="Government and Government-aided (many private schools also follow the State syllabus)",
        classes_covered="Classes 1-10 (Class 10 is the SSC board-exam year)",
        medium_of_instruction="Set per school (medium is recorded for each candidate in the SSC nominal roll)",
        key_exam="SSC Public Examination (Class 10); Advanced Supplementary Examination (ASE) in May for those who fail",
        exam_window="SSC March 2026 was held 16-03-2026 to 01-04-2026 (9:30 AM - 12:45 PM; science papers 9:30-11:30 AM); ASE May 2026 results are out. SSC 2027 blueprint and model papers were released 12-07-2026; the 2027 time table is not yet out",
        passing_criteria="Each subject is examined for 100 marks with no weightage for internal marks (G.O.Ms.No.41, 2019): First language, Second language, English, Mathematics, Social Studies, and General Science as two papers (Physical Science and Biological Science, 50 marks each on separate days). The pass mark is not yet confirmed from a BSEAP document",
        next_step="Intermediate (BIE AP), AP POLYCET diploma, ITI, or APOSS / NIOS open schooling",
        approx_fee="Free in government schools; SSC exam fee as notified by BSEAP each year",
        source="BSEAP (bse.ap.gov.in): SSC Public Examinations March 2026 revised time table dated 04-02-2026, Head Masters' instructions Rc.No.HMI/1/SSC-2025-DGE dated 02-12-2025, press note Rc.No.01/DCGE-1/Confd/SSC March 2027 dated 12-07-2026"),
    (AP, "Kasturba Gandhi Balika Vidyalaya (KGBV)"): dict(
        board_authority="Samagra Shiksha, Government of Andhra Pradesh (KGBV admissions portal apkgbv.apcfss.in); State syllabus (BSEAP SSC, BIE AP Intermediate)",
        ownership="Government, residential, girls only",
        classes_covered="Classes 6-10, and Intermediate (Junior and Senior) where the KGBV is upgraded",
        medium_of_instruction="Not yet checked against a primary document",
        key_exam="Admission by application, no entrance test; SSC (BSEAP) at Class 10",
        exam_window="2026-27 admissions (closed): online applications for Class 6, Classes 7-10 and Junior Intermediate from 12-03-2026 to 22-04-2026. 2027-28 schedule not yet announced",
        passing_criteria="For girls, with priority to SC, ST, BC, minority and economically weaker families; supports rural girls and dropouts returning to school",
        next_step="Continue to Intermediate at an upgraded KGBV, or move to Intermediate / AP POLYCET / ITI",
        approx_fee="Free education, hostel, textbooks, uniforms and meals",
        source="AP KGBV admissions portal (apkgbv.apcfss.in), Admission Notification 2026-27 page, read 2026-10-31"),
    (TS, "Telangana Gurukulam Residential Schools (TSWREIS / TTWREIS / MJPTBCWREIS / TREIS)"): dict(
        board_authority="Four Telangana welfare residential societies: TGSWREIS (Social Welfare), TGTWREIS (Tribal Welfare), MJPTBCWREIS (BC Welfare) and TREIS (general)",
        ownership="Government (State), residential",
        classes_covered="Entry at Class 5 in all four societies; backlog / regular seats in Classes 6-9 in TGSWREIS, TGTWREIS and MJPTBCWREIS (including the TGSWREIS Sainik schools at Rukmapur and Jagathgirigutta and a fine arts school)",
        medium_of_instruction="Not yet checked against a primary document",
        key_exam="TGCET (Telangana Government Common Entrance Test): 2 hours, 100 objective questions, no negative marks (Class 5: Telugu 20, English 25, Maths 25, EVS 20, Mental Ability 10)",
        exam_window="TGCET 2026 (for 2026-27, closed): online applications until 21-01-2026 (fee Rs.100), test on 22-02-2026, 11 AM - 1 PM. 2027 notification not yet out; watch tgcet.cgg.gov.in",
        passing_criteria="Must have studied Class 4 (for Class 5 entry) for the full 2025-26 year in the same erstwhile district; admission is district-specific, on merit and reservation. Parents' income below Rs.1,50,000 a year (rural) or Rs.2,00,000 (urban). Class 5 age: born 01-09-2013 to 31-08-2017 for SC/ST, 01-09-2015 to 31-08-2017 for BC / minority / others. Up to 80 students per school in Class 5",
        next_step="Continue in the society's schools to Class 10 and its junior colleges for Intermediate",
        approx_fee="Free education with boarding and lodging; TREIS students get food, books and cosmetic charges, while the other three societies also provide uniforms, kit and stationery",
        source="TGCET-2026 Prospectus for admission to residential educational institutions 2026-27 (tgcet.cgg.gov.in > Prospectus - TGCMNCET2026)"),
    (TS, "Telangana Model School (TMS/TGMS)"): dict(
        board_authority="Telangana Model Schools (School Education Department, Government of Telangana); 194 schools in educationally backward mandals",
        ownership="Government",
        classes_covered="Classes 6-10 and Intermediate",
        medium_of_instruction="English",
        key_exam="Model Schools Admission Test (MSAT) for Class 6 and for vacant seats in Classes 7-10",
        exam_window="2026-27 (closed): notification 17-01-2026; online applications 28-01-2026 to 28-02-2026; hall tickets from 09-04-2026; test on 19-04-2026 (Class 6, 10 AM - 12 noon; Classes 7-10, 2-4 PM); selection lists 23-05-2026, finalised 29-05-2026. 2027 notification not yet out",
        passing_criteria="Seats filled on merit in the admission test under the rule of reservation (G.O.Ms.No.24, 10-06-2016), with local / non-local status. Class 6 has 100 seats per school in two sections; Classes 7-10 only against vacancies",
        next_step="Continue to Class 10 and Intermediate at the Model School, or move to POLYCET / ITI",
        approx_fee="No fee; free textbooks and uniforms, mid-day meals for Classes 6-10, hostel for up to 100 girl students",
        source="Telangana Model Schools Information Bulletin about Model Schools Admission Test 2026 (telanganams.cgg.gov.in > Notification - TGMS VI CLASS - 2026)"),
}

path = os.path.join(os.path.dirname(__file__), "..", "..", "db", "seed", "schools.json")
rows = json.load(open(path, encoding="utf-8"))
by_key = {(r["state"], r["school_type"]): r for r in rows}
missing = set(SCHOOLS) - set(by_key)
assert not missing, f"not in seed: {missing}"
for k, fields in SCHOOLS.items():
    by_key[k].update(fields, source_type=GOV, data_tier="tier_1_official", verified_date=V)
with open(path, "w", encoding="utf-8") as f:
    json.dump(rows, f, ensure_ascii=False, indent=2)
    f.write("\n")
print(f"schools: {len(SCHOOLS)} AP/Telangana rows verified")
