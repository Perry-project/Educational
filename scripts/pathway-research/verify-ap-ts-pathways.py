"""Promotes Andhra Pradesh / Telangana post-10th pathway rows to tier_1_official,
each rewritten from its own official document (named in its source), read
first-hand on 2026-10-31. Claims the document did not confirm were dropped.

Run from the project root:  python scripts/pathway-research/verify-ap-ts-pathways.py
then:                        npm run db:import

Still pending_review (no primary document reachable on 2026-10-31):
 - AP Intermediate MPC/BiPC/MEC/CEC/HEC: BIE AP's 2026-27 admission schedule is not
   listed on bie.ap.gov.in any more (only recent circulars are shown) and press
   reports conflict (18 Mar-30 Apr vs 1 Apr-1 Jun, extended to 31 Jul).
 - AP POLYCET: polycetap.ap.gov.in is "closed for the year 2026"; notification not on apsbtet.ap.gov.in.
 - AP ITI (both rows): iti.ap.gov.in does not resolve.
 - Residential-school continuation rows (AP and Telangana): no single primary document.
"""
import json
import os

AP, TS = "Andhra Pradesh", "Telangana"
V = "2026-10-31"
GOV = "government_notification"

TGBIE = ("TGBIE circular File No. TGBIE-ACAD/ADMN/1/2024-ACAD dated 12-08-2026, 'Extension of Admission Schedule for the academic year "
         "2026-27 up to 31st August 2026' (tgbienew.cgg.gov.in/scannedPhotos/Circulars/Extension_of_the_Admission_Schedule_for_the_Academic_Year_2026_to_2027_upto_31st_August_2026.pdf; "
         "refers to the first-phase schedule dated 11-05-2026), TGBIE Annual Academic Calendar 2026-27 dated 28-03-2026, and TGBIE subject-wise Academic Annual Plans 2026-27 (tgbienew.cgg.gov.in)")
TS_ELIG = "Passed SSC (Class 10) from BSE Telangana or an equivalent recognised board"
TS_ADM = ("Apply at the junior college of your choice (Government, aided, private, co-operative, TG Residential / Social Welfare / Tribal Welfare, "
          "TG Model School, KGBV, TGMRJC, BC Welfare). Government junior colleges also take applications online at tgbienew.cgg.gov.in. "
          "Admission is on SSC GPA and subject-wise grade points (marks for older students); colleges must NOT hold any admission test. "
          "Aadhaar is mandatory. Reservation: SC 15%, ST 10%, BC 29%, EWS 10%, PH 5%, NCC/sports 5%, ex-servicemen 3%; one-third of seats for girls "
          "where there is no separate girls' college. Admit only in TGBIE-affiliated colleges (list on tgbienew.cgg.gov.in)")
TS_WIN = ("2026-27 (closed): first phase from 11-05-2026; colleges reopened 01-06-2026; admissions extended to 15-08-2026 and finally to 31-08-2026. "
          "2027-28 schedule not yet announced")
TS_DUR = "2 years (Intermediate 1st and 2nd year); public exams (IPE) conducted by TGBIE"

NIOS_SRC = ("NIOS Academic Prospectus 2026-27 (sdmis.nios.ac.in > Prospectus 2026-27: admission blocks, Table 3 entry requirements, Table 4 fees, "
            "Regional Centres list - RC Hyderabad covers Telangana and Andhra Pradesh, rchyderabad.nios.ac.in)")
NIOS = dict(
    eligibility="Passed Secondary (Class 10) from NIOS or any recognised board; at least 15 years old (on 31-07-2026 for Block 1, on 31-01-2027 for Block 2). No upper age limit",
    admission_route="Online admission at sdmis.nios.ac.in, choosing a study centre (Accredited Institution). Andhra Pradesh and Telangana are served by the NIOS Regional Centre Hyderabad (rchyderabad.nios.ac.in)",
    application_window="2026-27 (Stream 1): Block 1 - 16-03-2026 to 31-07-2026 without late fee, late-fee windows to 15-09-2026 (first exam March-April 2027). Block 2 - 16-09-2026 to 31-01-2027 without late fee, then late-fee windows (Rs.260 / 520 / 910) to 15-03-2027 (first exam September-October 2027) - Block 2 is open now. Fee for 5 subjects: Rs.2,600 (male), Rs.2,150 (female / third gender), Rs.1,690 (SC/ST, ex-servicemen, PwD)",
    duration="Admission valid for five years; public exams twice a year (March-April and September-October)",
    leads_to="NIOS Senior Secondary certificate, accepted like any Class 12 pass for degree admission and entrance exams. Check each state counselling's own notification before relying on it for a specific course",
    source=NIOS_SRC)

PATHWAYS = {
    (TS, "Intermediate - MPC (Maths, Physics, Chemistry)"): dict(
        eligibility=TS_ELIG, admission_route=TS_ADM, application_window=TS_WIN, duration=TS_DUR,
        leads_to="TG EAPCET (engineering / pharmacy), JEE Main and Advanced, NDA, and other maths-and-science routes", source=TGBIE),
    (TS, "Intermediate - BiPC (Biology, Physics, Chemistry)"): dict(
        eligibility=TS_ELIG, admission_route=TS_ADM, application_window=TS_WIN, duration=TS_DUR,
        leads_to="NEET-UG (MBBS, BDS, AYUSH), TG EAPCET agriculture & pharmacy stream (B.Sc Agriculture, B.Pharm, veterinary), nursing and allied health routes", source=TGBIE),
    (TS, "Intermediate - MEC (Maths, Economics, Commerce)"): dict(
        eligibility=TS_ELIG, admission_route=TS_ADM, application_window=TS_WIN, duration=TS_DUR,
        leads_to="B.Com / BBA, CA / CS / CMA Foundation, banking and commerce routes", source=TGBIE),
    (TS, "Intermediate - CEC (Commerce, Economics, Civics)"): dict(
        eligibility=TS_ELIG, admission_route=TS_ADM, application_window=TS_WIN, duration=TS_DUR,
        leads_to="B.Com / BA, law (CLAT, TS LAWCET for 5-year LLB), CUET-UG, civil services preparation", source=TGBIE),
    (TS, "Intermediate - HEC (History, Economics, Civics)"): dict(
        eligibility=TS_ELIG, admission_route=TS_ADM, application_window=TS_WIN, duration=TS_DUR,
        leads_to="BA, CUET-UG for central universities, law (CLAT, TS LAWCET), civil services preparation", source=TGBIE),
    (TS, "TS POLYCET - Polytechnic Diploma"): dict(
        eligibility="Indian national belonging to Telangana (local / non-local status under the Telangana Educational Institutions (Regulation of Admissions) Order, 1974). Passed SSC (BSE Telangana) or an equivalent (CBSE, ICSE, NIOS, TOSS, other state boards) with Mathematics and at least 35% marks; candidates from NIOS/TOSS/CBSE/ICSE/other boards must pass every subject including Mathematics, Physics and Chemistry with at least 35% each. Students awaiting March/April SSC results may apply. No age limit for the test (agricultural / veterinary diplomas have their own age limits)",
        admission_route="POLYCET conducted by the State Board of Technical Education and Training (SBTET), Telangana: one 2 h 30 min paper, 150 marks (Maths 60, Physics 30, Chemistry 30, Biology 30 - Biology needed only for PJTAU / PVNRTVU / SKLTGHU agricultural, veterinary and horticulture diplomas), then counselling for Government, aided and private polytechnics",
        application_window="2026 (closed): online registration 02-02-2026 to 20-04-2026; with late fee to 21-04-2026; Tatkal fee to 22-04-2026. Exam held 13-05-2026 (11:00 AM - 1:30 PM). 2027 notification not yet out",
        duration="Mostly 3-year diplomas (engineering / non-engineering); PJTAU, PVNRTVU and SKLTGHU diplomas are 2 or 3 years",
        leads_to="Diploma - jobs in technical / para-engineering roles, or lateral entry to 2nd year B.Tech through TS ECET",
        source="SBTET Telangana POLYCET-2026 Instruction Booklet (polycet.sbtet.telangana.gov.in/Downloads/polycet2026.pdf: important dates, eligibility 4.0, pattern 7.0), Brief Notification, and POLYCET-2026 Provisional Key notice (exam on 13-05-2026)"),
    (TS, "ITI - Engineering Trades"): dict(
        eligibility="Indian national, at least 14 years old on 01-08-2026 (16 for Drone Technician), no upper age limit. 10th pass (BSE Telangana, CBSE, ICSE, NIOS, TOSS, APOSS or another state board); some trades accept 8th pass, but 10th-pass candidates get preference",
        admission_route="One online application at iti.telangana.gov.in for all 65 Advanced Technology Centres (ATCs), 63 Government ITIs and 230 private ITIs (NCVT, Craftsmen Training Scheme). Unlimited district / ITI / trade options. No entrance exam: seats are allotted online on SSC marks, reservation and options, in phases followed by walk-in admissions",
        application_window="2026-27 session (August 2026): four online phases, then a 5th-phase walk-in notified 12-10-2026 - walk-in admissions open from 10-10-2026 (register online first; walk-ins before 1 PM are considered the same day)",
        duration="47 trades in all: 6 in ATCs (3 two-year, 3 one-year) and 41 CTS trades in ITIs (32 engineering, 15 non-engineering; 21 two-year and 26 one-year). Trade-wise duration in Annexure-II of the prospectus",
        leads_to="National Trade Certificate (NCVT) after the All India Trade Test; apprenticeship, jobs or self-employment",
        source="Department of Employment and Training, Telangana - TG ITI Admissions 2026 Prospectus (iti.telangana.gov.in/assets/pdf2026/Prospectus_2026.pdf, sections 1, 5-7) and 5th Phase / Walk-in Admission Notification No. I-1/Admissions 2026/2026 dated 12-10-2026"),
    (TS, "ITI - Non-Engineering Trades"): dict(
        eligibility="Same as engineering trades: Indian national, at least 14 on 01-08-2026, no upper age limit; 10th pass (or 8th pass for specified trades, with preference to 10th pass)",
        admission_route="Same single online application at iti.telangana.gov.in and SSC-merit online allotment; no entrance exam. 15 of the 41 CTS trades in ITIs are non-engineering",
        application_window="2026-27 session: four online phases, then walk-in admissions open from 10-10-2026 (notification dated 12-10-2026)",
        duration="One or two years depending on the trade (Annexure-II of the prospectus)",
        leads_to="National Trade Certificate (NCVT); jobs, apprenticeship or self-employment in the trade",
        source="Department of Employment and Training, Telangana - TG ITI Admissions 2026 Prospectus (iti.telangana.gov.in/assets/pdf2026/Prospectus_2026.pdf) and 5th Phase / Walk-in Admission Notification dated 12-10-2026"),
    (TS, "NIOS Senior Secondary Course (Class 12 equivalent)"): NIOS,
    (AP, "NIOS Senior Secondary Course (Class 12 equivalent)"): NIOS,
}

path = os.path.join(os.path.dirname(__file__), "..", "..", "db", "seed", "pathways.json")
rows = json.load(open(path, encoding="utf-8"))
by_key = {(r["state"], r["pathway_name"]): r for r in rows}
missing = set(PATHWAYS) - set(by_key)
assert not missing, f"not in seed: {missing}"
for k, fields in PATHWAYS.items():
    by_key[k].update(fields, source_type=GOV, data_tier="tier_1_official", verified_date=V)
with open(path, "w", encoding="utf-8") as f:
    json.dump(rows, f, ensure_ascii=False, indent=2)
    f.write("\n")
print(f"pathways: {len(PATHWAYS)} AP/Telangana rows verified")
