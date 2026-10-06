"""Builds db/seed/second_chance_routes.json: the official routes back into
education or work for a student who stopped somewhere (failed or left
Class 10, Intermediate or a degree, didn't clear an entrance exam, or is
already working). Shown on the /second-chance page.

Run from the project root:  python scripts/second-chance-research/build-second-chance.py
then:                        npm run db:import

Rules (CLAUDE.md "Data safety tiers"): a route is tier_1_official only when
every fact in it was read in the body's own notification, prospectus or
portal (named in its source). Anything not yet read stays pending_review:
the page then shows only its name, body and official website.
"""
import json
import os

AP, TS, IN = "Andhra Pradesh", "Telangana", "National"
ROUTES = []


def route(stopped_at, scope, name, kind, body, website, related_exam=None):
    """A route listed by name, body and website only (pending_review)."""
    ROUTES.append({
        "stopped_at": stopped_at, "scope": scope, "route_name": name, "kind": kind,
        "conducting_body": body, "official_website": website, "related_exam": related_exam,
        "summary": None, "who_can": None, "how_to_apply": None, "next_dates": None, "leads_to": None,
        "sequence_order": sum(r["stopped_at"] == stopped_at for r in ROUTES) + 1,
        "source": None, "source_type": None, "data_tier": "pending_review", "verified_date": None,
    })


def verify(name, scope, verified, source, stopped_at=None, **fields):
    """Fill in a route's details once its official document has been read."""
    hits = [r for r in ROUTES if r["route_name"] == name and r["scope"] == scope
            and (stopped_at is None or r["stopped_at"] == stopped_at)]
    assert hits, f"verify() names a route not listed: {name} ({scope})"
    for r in hits:
        r.update(fields, source=source, source_type="government_notification",
                 data_tier="tier_1_official", verified_date=verified)


# =====================================================================
# The routes, by where the student stopped
# =====================================================================

# ---------- Failed or left Class 10 ----------
route("class_10", AP, "AP SSC Advanced Supplementary Exams", "Retake exam", "Directorate of Government Examinations, AP", "bse.ap.gov.in")
route("class_10", TS, "TS SSC Advanced Supplementary Exams", "Retake exam", "Directorate of Government Examinations, Telangana", "bse.telangana.gov.in")
route("class_10", AP, "AP Open School (APOSS) - SSC", "Open school", "Andhra Pradesh Open School Society", "apopenschool.ap.gov.in")
route("class_10", TS, "Telangana Open School (TOSS) - SSC", "Open school", "Telangana Open School Society", "telanganaopenschool.org")
route("class_10", IN, "NIOS Secondary (Class 10)", "Open school", "National Institute of Open Schooling", "nios.ac.in")
route("class_10", TS, "ITI trades (Telangana)", "Skill training", "Department of Employment and Training, Telangana", "iti.telangana.gov.in")
route("class_10", AP, "ITI trades (Andhra Pradesh)", "Skill training", "Department of Employment and Training, AP", "iti.ap.gov.in")

# ---------- Failed or left Intermediate ----------
route("intermediate", AP, "AP Intermediate: failed papers and improvement", "Retake exam", "Board of Intermediate Education, AP", "bie.ap.gov.in")
route("intermediate", TS, "TS Intermediate Advanced Supplementary Exams", "Retake exam", "Telangana Board of Intermediate Education", "tgbie.cgg.gov.in")
route("intermediate", AP, "AP Open School (APOSS) - Intermediate", "Open school", "Andhra Pradesh Open School Society", "apopenschool.ap.gov.in")
route("intermediate", TS, "Telangana Open School (TOSS) - Intermediate", "Open school", "Telangana Open School Society", "telanganaopenschool.org")
route("intermediate", IN, "NIOS Senior Secondary (Class 12)", "Open school", "National Institute of Open Schooling", "nios.ac.in")
route("intermediate", TS, "Polytechnic diploma (TS POLYCET)", "Diploma", "SBTET, Telangana", "polycet.sbtet.telangana.gov.in", related_exam="TS POLYCET")
route("intermediate", AP, "Polytechnic diploma (AP POLYCET)", "Diploma", "SBTET, Andhra Pradesh", "polycetap.ap.gov.in", related_exam="AP POLYCET")
route("intermediate", TS, "ITI trades (Telangana)", "Skill training", "Department of Employment and Training, Telangana", "iti.telangana.gov.in")

# ---------- Left a degree or B.Tech midway ----------
route("degree", IN, "Exit and rejoin a degree (Academic Bank of Credits)", "Rule", "UGC / Ministry of Education", "abc.gov.in")
route("degree", TS, "Dr. B.R. Ambedkar Open University (BRAOU) degree", "Open university", "Dr. B.R. Ambedkar Open University, Hyderabad", "braou.ac.in")
route("degree", IN, "IGNOU degree", "Open university", "Indira Gandhi National Open University", "ignou.ac.in")
route("degree", AP, "Diploma to B.Tech 2nd year (AP ECET)", "Lateral entry", "APSCHE (conducted by JNTU Anantapur)", "cets.apsche.ap.gov.in", related_exam="AP ECET")
route("degree", TS, "Diploma to B.Tech 2nd year (TS ECET)", "Lateral entry", "TGCHE (conducted by OU)", "ecet.tgche.ac.in",
      related_exam="TS ECET (Telangana State Engineering Common Entrance Test)")

# ---------- Didn't clear NEET, JEE or another entrance exam ----------
route("entrance_exam", IN, "Take NEET-UG again", "Retake exam", "National Testing Agency", "neet.nta.nic.in", related_exam="NEET-UG")
route("entrance_exam", IN, "Take JEE Main again", "Retake exam", "National Testing Agency", "jeemain.nta.nic.in", related_exam="JEE Main")
route("entrance_exam", IN, "JEE Advanced: the two-attempt limit", "Rule", "IITs (Joint Admission Board)", "jeeadv.ac.in", related_exam="JEE Advanced")
route("entrance_exam", AP, "Same Biology subjects, other courses (AP EAPCET Agriculture & Pharmacy)", "Other course", "APSCHE (conducted by JNTU Kakinada)", "cets.apsche.ap.gov.in", related_exam="AP EAPCET")
route("entrance_exam", TS, "Same Biology subjects, other courses (TG EAPCET Agriculture & Pharmacy)", "Other course", "TGCHE (conducted by JNTUH)", "eapcet.tgche.ac.in",
      related_exam="TG EAPCET (Telangana State Engineering, Agriculture & Pharmacy Common Entrance Test)")

# ---------- Working, or older ----------
route("working", IN, "Graduate and diploma apprenticeship (NATS)", "Paid apprenticeship", "Ministry of Education (Boards of Apprenticeship Training)", "nats.education.gov.in")
route("working", IN, "Trade apprenticeship (NAPS)", "Paid apprenticeship", "Ministry of Skill Development and Entrepreneurship", "apprenticeshipindia.gov.in")
route("working", IN, "Certify skills you already have (Recognition of Prior Learning)", "Skill certificate", "Skill India (NSDC / MSDE)", "skillindiadigital.gov.in")
route("working", AP, "AP Open School (APOSS) - SSC", "Open school", "Andhra Pradesh Open School Society", "apopenschool.ap.gov.in")
route("working", TS, "Telangana Open School (TOSS) - SSC", "Open school", "Telangana Open School Society", "telanganaopenschool.org")
route("working", TS, "Dr. B.R. Ambedkar Open University (BRAOU) degree", "Open university", "Dr. B.R. Ambedkar Open University, Hyderabad", "braou.ac.in")
route("working", IN, "IGNOU degree", "Open university", "Indira Gandhi National Open University", "ignou.ac.in")


# =====================================================================
# Verified details, each from the body's own document
# =====================================================================

# ---------- AP SSC Advanced Supplementary (May 2026) ----------
src = "Directorate of Government Examinations AP, Notification Rc.No.GE-EXAMOSSC(DD)/1/2025-DGE dated 29-04-2026 (fee due dates) and SSC Advanced Supplementary Examinations May 2026 time table dated 30-04-2026: bse.ap.gov.in/pdf/Due Dates ASE.pdf, bse.ap.gov.in/pdf/ASE TIME TABLE-MAY 2026.pdf"
verify("AP SSC Advanced Supplementary Exams", AP, "2026-10-05", src,
    summary="A second sitting, a few weeks after results, for students who failed subjects in the March SSC public exams. Pass the failed subjects and you get your SSC certificate the same year.",
    who_can="Students who failed one or more subjects in the March SSC (or Open School SSC) exams",
    how_to_apply="Through your school: the headmaster pays the fee and submits the application on bse.ap.gov.in. Fee Rs 110 for up to 3 subjects, Rs 125 for more",
    next_dates="2026: fee 01-09 May 2026 (late fee Rs 50 until the day before the exam); exams 25 May - 04 Jun 2026. The next one follows the March 2027 SSC exams",
    leads_to="SSC pass certificate, so you can join Intermediate, a polytechnic or an ITI in the same academic year",
)

# ---------- APOSS SSC and Intermediate (2026-27) ----------
src = "AP Open School Society: SSC Prospectus 2026-27 and Intermediate Prospectus 2026-27 (apopenschool.ap.gov.in/pdf/Prospectus_SSC_2026-27.pdf, .../Prospectus_Inter_2026-27.pdf); late-fee admission proceedings RC No. 3251023/ADMIN/2026 dated 28-09-2026 (apopenschool.ap.gov.in/pdf/Admissions_2026_27_NEW_2.pdf)"
verify("AP Open School (APOSS) - SSC", AP, "2026-10-05", src,
    summary="Study Class 10 from home or work through a study centre and write public exams twice a year. The APOSS SSC certificate is equivalent to the regular SSC for higher studies and jobs (G.O.Rt.No. 723, 2008).",
    who_can="Anyone at least 14 years old on 31 August of the admission year; no upper age limit. Not for students currently studying or already passed SSC in any board",
    how_to_apply="Online on apopenschool.ap.gov.in, then submit certificates at your chosen study centre (Accredited Institution). Women, SC, ST, BC, minorities, PH, transgender and ex-servicemen get a fee concession",
    next_dates="2026-27 admissions: 12 Jun - 30 Jul 2026, late fee to 15 Aug, then a last window 26-30 Sep 2026 with Rs 200 late fee (closed). Exams every March/April and May/June",
    leads_to="SSC-equivalent certificate. Pass five subjects; up to 9 exam chances in 5 years, and up to 2 subjects already passed elsewhere can be carried over",
)
verify("AP Open School (APOSS) - Intermediate", AP, "2026-10-05", src,
    summary="Complete Intermediate through a study centre at your own pace. The certificate is equivalent to the BIEAP Intermediate for higher studies and jobs (G.O.Rt.No. 170, 2010); MPC/BiPC students can sit JEE and NEET.",
    who_can="SSC pass, at least 15 years old on 31 August of the admission year; no upper age limit. Science groups need Maths and Science in Class 10. There must be a two-year gap between SSC and the Intermediate certificate",
    how_to_apply="Online on apopenschool.ap.gov.in, then certificate verification at the study centre",
    next_dates="2026-27 admissions: 12 Jun - 30 Jul 2026, late fee to 15 Aug, last window 26-30 Sep 2026 (closed). Exams every March/April and May/June",
    leads_to="Intermediate-equivalent certificate for degree courses (B.A., B.Com., B.Sc.), D.Ed., and entrance exams. Up to 9 exam chances in 5 years",
)

# ---------- TOSS SSC and Intermediate (2026-27) ----------
src = "Telangana Open School Society: Prospectus 2026-27 (English) telanganaopenschool.org/pdfs/EM_Prospectus26_27TOSS.pdf; extension proceedings Rc.No.915/B1/TOSS/2026 dated 30-09-2026 (telanganaopenschool.org/PDFS/Toss Admissions Extended 2026-27_3.pdf)"
verify("Telangana Open School (TOSS) - SSC", TS, "2026-10-05", src,
    summary="Study Class 10 through a study centre in Telugu, English, Urdu or Hindi medium. The TOSS SSC certificate is equivalent to the regular SSC (G.O.Rt.No. 723, 2008).",
    who_can="Anyone at least 14 years old on 31 August of the admission year; no upper age limit",
    how_to_apply="Online at toss.aptonline.in (link on telanganaopenschool.org), or at TG Online / MeeSeva centres; admission is through an Accredited Institution (study centre)",
    next_dates="2026-27 admissions OPEN: extended to 12 Oct 2026 with the normal fee. Exams usually April/May and October/November; first exam after one academic year",
    leads_to="SSC-equivalent certificate. Up to 9 exam chances in 5 years; up to 2 subjects passed in another board in the last 5 years can be carried over",
)
verify("Telangana Open School (TOSS) - Intermediate", TS, "2026-10-05", src,
    summary="Complete Intermediate through a study centre (science students at science junior colleges). The certificate is equivalent to the TGBIE Intermediate (G.O.Ms.No. 170, 2012).",
    who_can="SSC pass, at least 15 years old on 31 August of the admission year; no upper age limit. Science groups need the matching SSC subjects. A two-year gap from passing SSC is required for the certificate",
    how_to_apply="Online at toss.aptonline.in (link on telanganaopenschool.org), or at TG Online / MeeSeva centres",
    next_dates="2026-27 admissions OPEN: extended to 12 Oct 2026 with the normal fee",
    leads_to="Intermediate-equivalent certificate for degree courses and entrance exams. Up to 9 exam chances in 5 years; English is compulsory",
)
verify("Telangana Open School (TOSS) - SSC", TS, "2026-10-05", src, stopped_at="working",
    summary="Finish Class 10 while working: study at a centre near you and write exams when ready. No upper age limit.",
    who_can="Anyone at least 14 years old; no upper age limit",
    how_to_apply="Online at toss.aptonline.in or at a MeeSeva centre",
    next_dates="2026-27 admissions OPEN until 12 Oct 2026",
    leads_to="SSC-equivalent certificate, then Intermediate through TOSS, an ITI or a polytechnic",
)
verify("AP Open School (APOSS) - SSC", AP, "2026-10-05", "AP Open School Society SSC Prospectus 2026-27: apopenschool.ap.gov.in/pdf/Prospectus_SSC_2026-27.pdf", stopped_at="working",
    summary="Finish Class 10 while working: study at a centre near you and write exams twice a year. No upper age limit.",
    who_can="Anyone at least 14 years old; no upper age limit",
    how_to_apply="Online on apopenschool.ap.gov.in, then the study centre",
    next_dates="2026-27 admissions closed on 30 Sep 2026; the next round opens around June 2027",
    leads_to="SSC-equivalent certificate, then Intermediate through APOSS, an ITI or a polytechnic",
)

# ---------- NIOS (2026-27) ----------
src = "NIOS Notification 30/2026 dated 15-09-2026 (Stream-1 Block-I extended to 30.09.2026) and Notification 16/2026 dated 31-07-2026 (Stream-2 extended to 17.08.2026): nios.ac.in/media/documents/notification/yr2026/Admission/; course rules from nios.ac.in/departmentsunits/academic/secondary-course-equivalent-to-class-x.aspx and senior-secondary-course-equivalent-to-class-xii.aspx"
verify("NIOS Secondary (Class 10)", IN, "2026-10-05", src,
    summary="The national open school under the Ministry of Education. Study Class 10 at your own pace in many subjects and languages, and take exams when you're ready.",
    who_can="Anyone who wants a Class 10 certificate (see nios.ac.in for age and document rules)",
    how_to_apply="Online at sdmis.nios.ac.in",
    next_dates="2026-27: Stream-1 (Block I) admissions closed 30 Sep 2026; Stream-2 closed 17 Aug 2026",
    leads_to="Class 10 certificate. Pass at least five subjects, including one or two languages; up to seven subjects allowed",
)
verify("NIOS Senior Secondary (Class 12)", IN, "2026-10-05", src,
    summary="Complete Class 12 through the national open school, at your own pace.",
    who_can="Class 10 pass (see nios.ac.in for age and document rules)",
    how_to_apply="Online at sdmis.nios.ac.in",
    next_dates="2026-27: Stream-1 (Block I) admissions closed 30 Sep 2026; Stream-2 closed 17 Aug 2026",
    leads_to="Class 12 certificate (accepted by AICTE for its institutions). Pass at least five subjects, including one or two languages",
)

# ---------- ITI (Telangana, 2026) ----------
src = "Department of Employment & Training, Telangana: TG ITI Admissions 2026 Prospectus, iti.telangana.gov.in/assets/pdf2026/Prospectus_2026.pdf"
for stop in ("class_10", "intermediate"):
    verify("ITI trades (Telangana)", TS, "2026-10-05", src, stopped_at=stop,
        summary="One- or two-year hands-on trade training (about 70% practical) in 47 engineering and non-engineering trades at 65 Advanced Technology Centres, 63 government ITIs and 230 private ITIs.",
        who_can="Class 10 pass (SSC, CBSE, ICSE, NIOS, TOSS or APOSS); Class 8 pass is enough for some trades, with preference to Class 10. At least 14 years old on 01-08-2026 (16 for the drone course); no upper age limit",
        how_to_apply="One online application at iti.telangana.gov.in covers all ATCs and ITIs in the state",
        next_dates="2026-27 admissions were notified in 2026; check iti.telangana.gov.in for any remaining phase",
        leads_to="National Trade Certificate (NCVT) after the All India Trade Test, valid for jobs and apprenticeships across India",
    )

# ---------- BIEAP: failed papers, improvement, March 2027 ----------
src = "Board of Intermediate Education AP: Circular Rc.No.81/C25/IPASE May 2026 dated 18-04-2026 (improvement and failed candidates), Rc.No.ESE51-15/39/2021-C SEC-BIE dated 27-04-2026 (IPASE fee extension), Rc.No.81/C25/IPE March 2027 dated 23-09-2026 (IPE March 2027 fee due dates), all on bie.ap.gov.in"
verify("AP Intermediate: failed papers and improvement", AP, "2026-10-05", src,
    summary="Failed Intermediate subjects can be written again until you pass, with no limit on attempts. You can also re-write passed papers once to improve marks; the best marks count.",
    who_can="1st and 2nd year students who failed papers (no limit on attempts). Students who passed can take improvement in theory papers once (no improvement for practicals). Humanities students can also appear privately without attending college (attendance exempted)",
    how_to_apply="Through your junior college, which pays the fee on bie.ap.gov.in. Exam fee Rs 600 for one year, Rs 1,200 for both years; Rs 160 per paper for improvement",
    next_dates="IPE March 2027: fee without fine 24 Sep - 29 Oct 2026; with Rs 1,000 fine 30 Oct - 10 Nov 2026 (OPEN). Then the Advanced Supplementary exams in May 2027",
    leads_to="Intermediate pass certificate (or better marks), for degree courses, EAPCET and other entrance exams",
)

# ---------- UGC multiple entry and exit / ABC ----------
src = "UGC Curriculum and Credit Framework for Undergraduate Programmes (section 3.2.3): ugc.gov.in/pdfnews/7193743_FYUGP.pdf; Academic Bank of Credits FAQs on abc.gov.in"
verify("Exit and rejoin a degree (Academic Bank of Credits)", IN, "2026-10-05", src,
    summary="Under the national framework for degrees, leaving midway doesn't have to mean losing what you studied. Your credits are stored in the Academic Bank of Credits against your APAAR ID.",
    who_can="Students in degree programmes at universities that follow the UGC framework and are registered on ABC. Ask your college whether it offers exit and re-entry",
    how_to_apply="Get an APAAR ID and check your credits on abc.gov.in. To leave with an award: a UG Certificate after year 1 (40 credits plus a 4-credit summer vocational course) or a UG Diploma after year 2 (80 credits plus a 4-credit summer vocational course)",
    next_dates="You can rejoin within three years and must finish the degree within seven years in all",
    leads_to="A UG Certificate or UG Diploma now, and the full degree when you return",
)

# ---------- BRAOU (2026-27) ----------
src = "Dr. B.R. Ambedkar Open University, Admission Notification 2026-27 (version 8, 30-09-2026): braouonline.in/Admissions_2026/AdmissionNotification2026-Version8_30092026_6PM.pdf (from braouonline.in/MISC/AdmissionLinks.htm)"
for stop in ("degree", "working"):
    verify("Dr. B.R. Ambedkar Open University (BRAOU) degree", TS, "2026-10-05", src, stopped_at=stop,
        summary="A state open university in Hyderabad offering B.A., B.Com. and B.Sc. by distance learning in English, Telugu and Urdu medium, with study centres across Telangana. Useful if you left a regular degree or need to work while studying.",
        who_can="Intermediate or equivalent, NIOS Class 12, a 3-year polytechnic diploma, or a 2-year diploma or ITI (B.Sc. needs Intermediate with science subjects)",
        how_to_apply="Online at braouonline.in, then certificate verification at your study centre. Tuition about Rs 3,200 in year 1 and Rs 3,000 in years 2 and 3 (plus lab fees for science subjects). Students who ran out of time can seek re-admission at the university",
        next_dates="2026-27 admissions OPEN: started 17 Jun 2026, last date 13 Oct 2026",
        leads_to="A 3-year UG degree (six semesters), then PG programmes, government job exams, B.Ed. etc.",
    )

# ---------- IGNOU (July 2026 prospectus) ----------
src = "IGNOU Common Prospectus July 2026: ignou.ac.in/viewFile/services/Common_Prospectus/common-prospectus-july-2026-V-L-1-1.pdf"
for stop in ("degree", "working"):
    verify("IGNOU degree", IN, "2026-10-05", src, stopped_at=stop,
        summary="India's national open university. Degrees by distance learning are equivalent to regular degrees under UGC rules, and there are January and July admission cycles every year.",
        who_can="10+2 (Intermediate) or equivalent for bachelor's programmes. SC/ST students may get the programme fee waived (once, under the policy for that cycle)",
        how_to_apply="Online at ignouadmission.samarth.edu.in. If you studied part of a degree elsewhere, ask for credit transfer after admission (UGC framework; ABC supported)",
        next_dates="Two cycles a year (January and July); last dates are in the admission notification on ignou.ac.in",
        leads_to="UG degree (3 or 4 years, up to 6-8 years allowed), then PG, government job exams etc.",
    )

# ---------- Lateral entry and exam routes (from the verified exam rows) ----------
src = "Official APECET-2026 Instruction Booklet (JNTU Anantapur, on behalf of APSCHE): cets.apsche.ap.gov.in/ECET/PDF/APECET2026_InstructionBooklet_V6.pdf"
verify("Diploma to B.Tech 2nd year (AP ECET)", AP, "2026-10-05", src,
    summary="If you have (or are finishing) a diploma, you can join B.Tech or B.Pharmacy directly in the second year instead of starting over.",
    who_can="Diploma in Engineering/Technology/Pharmacy (or a 3-year B.Sc. with Maths) with at least 45% (40% for BC/SC/ST), AP local/non-local rules",
    how_to_apply="Online on cets.apsche.ap.gov.in when the ECET notification is out (around February)",
    next_dates="2026: applications to 12 Mar 2026, exam 23 Apr 2026. The 2027 notification is expected early 2027",
    leads_to="2nd year B.E./B.Tech or B.Pharmacy (seats 10% over the sanctioned intake)",
)
src = "Official TG ECET-2026 Notification and Detailed Notification (Osmania University, on behalf of TGCHE) on ecet.tgche.ac.in (as in the Exams tab)"
verify("Diploma to B.Tech 2nd year (TS ECET)", TS, "2026-10-05", src,
    summary="With a diploma (or a B.Sc with Maths), you can join B.Tech or B.Pharmacy in Telangana directly in the second year.",
    who_can="Diploma in Engineering/Technology/Pharmacy (or a 3-year B.Sc with Maths) with at least 45% (40% for reserved categories); final-year students may apply. Telangana local/non-local rules",
    how_to_apply="Online on ecet.tgche.ac.in when the notification is out (February)",
    next_dates="2026: applications from 09 Feb 2026, exam 15 May 2026. 2027 notification not yet released",
    leads_to="2nd year B.E./B.Tech or B.Pharmacy in Telangana. Qualifying mark 25% (no minimum for SC/ST)",
)
src = "NTA NEET (UG) 2026 public notices on neet.nta.nic.in (as in the Exams tab)"
verify("Take NEET-UG again", IN, "2026-10-05", src,
    summary="NEET-UG has no upper age limit, so you can prepare and sit it again next year.",
    who_can="Class 12 with Physics, Chemistry and Biology: 50% General, 40% OBC/SC/ST; at least 17 by 31 Dec of the admission year",
    how_to_apply="Register on neet.nta.nic.in when the 2027 information bulletin is released (expected around February 2027)",
    next_dates="NEET-UG 2027 notification not yet released as of Oct 2026",
    leads_to="MBBS, BDS, AYUSH, B.V.Sc and B.Sc Nursing seats",
)
src = "NTA JEE (Main) 2026 press release on jeemain.nta.nic.in (as in the Exams tab)"
verify("Take JEE Main again", IN, "2026-10-05", src,
    summary="JEE Main can be taken in three consecutive years from the year you pass Class 12, with up to two sessions a year, and there's no minimum-marks bar to sit it.",
    who_can="Passed Class 12 with Physics, Chemistry and Maths in 2025 or 2026, or appearing in 2027",
    how_to_apply="Register on jeemain.nta.nic.in when the 2027 notification is out",
    next_dates="JEE Main 2027 registration not yet open as of Oct 2026 (Session 1 is usually in January)",
    leads_to="NITs, IIITs and other centrally funded institutes; top ranks qualify for JEE Advanced",
)
src = "JEE (Advanced) 2026 notices on jeeadv.ac.in (as in the Exams tab)"
verify("JEE Advanced: the two-attempt limit", IN, "2026-10-05", src,
    summary="JEE Advanced allows only two attempts, in two consecutive years. If you used one this year, next year is your last chance for the IITs.",
    who_can="Top ~2,50,000 in JEE Main of the same year",
    how_to_apply="Register on jeeadv.ac.in after JEE Main results",
    next_dates="2027 dates not yet announced",
    leads_to="B.Tech and integrated programmes at the 23 IITs",
)
src = "APEAPCET-2026 Instruction Booklet (JNTU Kakinada, on behalf of APSCHE) on cets.apsche.ap.gov.in (as in the Exams tab)"
verify("Same Biology subjects, other courses (AP EAPCET Agriculture & Pharmacy)", AP, "2026-10-05", src,
    summary="If NEET didn't work out, the same BiPC subjects can take you into agriculture, horticulture, veterinary, fisheries and pharmacy degrees through AP EAPCET's Agriculture & Pharmacy stream.",
    who_can="Intermediate BiPC with at least 45% (40% for reserved categories), AP local/non-local rules",
    how_to_apply="Online on cets.apsche.ap.gov.in when the EAPCET notification is out (February)",
    next_dates="2026: applications to 24 Mar 2026; Agriculture & Pharmacy exam 19-20 May 2026. The 2027 notification is expected in February 2027",
    leads_to="B.Sc.(Ag), B.Sc.(Hort), B.V.Sc & A.H., B.F.Sc, B.Pharmacy, Pharm.D in Andhra Pradesh",
)
src = "TG EAPCET-2026 Detailed Notification (JNTUH, on behalf of TGCHE) on eapcet.tgche.ac.in (as in the Exams tab)"
verify("Same Biology subjects, other courses (TG EAPCET Agriculture & Pharmacy)", TS, "2026-10-05", src,
    summary="If NEET didn't work out, TG EAPCET's Agriculture & Pharmacy stream takes BiPC students into agriculture, veterinary, fisheries, pharmacy and nursing degrees in Telangana.",
    who_can="Intermediate BiPC with at least 45% (40% for reserved categories); age 17-22 (25 for SC/ST) for agriculture, veterinary and similar courses",
    how_to_apply="Online on eapcet.tgche.ac.in when the notification is out (February)",
    next_dates="2026: applications to 04 Apr 2026; Agriculture & Pharmacy exam 04-05 May 2026. 2027 notification not yet released",
    leads_to="B.Sc (Hons) Agriculture/Horticulture, B.V.Sc & A.H., B.F.Sc, B.Pharmacy, Pharm-D, B.Sc (Nursing)",
)
src = "POLYCET-2026 Instruction Booklet, SBTET Telangana: polycet.sbtet.telangana.gov.in/Downloads/polycet2026.pdf (as in the Exams tab)"
verify("Polytechnic diploma (TS POLYCET)", TS, "2026-10-05", src,
    summary="A polytechnic diploma needs only Class 10, so it's open even if Intermediate didn't work out. After the diploma, ECET takes you into B.Tech 2nd year.",
    who_can="SSC pass with Mathematics and at least 35%. No age limit for polytechnic courses (15-22 for agriculture, veterinary and horticulture diplomas)",
    how_to_apply="Online on polycet.sbtet.telangana.gov.in when the notification is out (February)",
    next_dates="2026: registration 02 Feb - 20 Apr 2026, exam 13 May 2026. 2027 dates not yet announced",
    leads_to="3-year engineering/technology diplomas at Telangana polytechnics; agriculture, veterinary and horticulture diplomas",
)

# ---------- NATS ----------
src = "National Apprenticeship Training Scheme portal (Ministry of Education): nats.education.gov.in/about-us.php, /students.php, /student_type.php"
verify("Graduate and diploma apprenticeship (NATS)", IN, "2026-10-05", src,
    summary="Paid on-the-job training for 6 months to 1 year with central, state and private employers, under the Apprentices Act. Half the stipend is reimbursed to the employer by the Government of India.",
    who_can="Graduates, diploma holders and vocational certificate holders who have passed out (students on sandwich courses can register separately); 126 subject fields",
    how_to_apply="Register on nats.education.gov.in (APAAR ID and Aadhaar e-KYC are mandatory), then apply to apprenticeship openings",
    next_dates="Openings are posted on the portal throughout the year",
    leads_to="Monthly stipend during training and a Government of India Certificate of Proficiency, registrable as work experience at employment exchanges",
)


# ---------- write ----------
out = os.path.join(os.path.dirname(__file__), "..", "..", "db", "seed", "second_chance_routes.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump(ROUTES, f, ensure_ascii=False, indent=2)
    f.write("\n")
verified = sum(r["data_tier"] == "tier_1_official" for r in ROUTES)
print(f"{len(ROUTES)} routes, {verified} verified")
