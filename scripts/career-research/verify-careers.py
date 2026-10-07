"""Promotes career pipelines in db/seed/careers.json to tier_1_official once
every eligibility rule, exam and number in them has been read in the body's
own document (named in the row's source). Rows are rewritten from that
document, so anything the nightly routine took from aggregators (fees,
salaries, approximate percentages) is dropped rather than carried over.

Run from the project root:  python scripts/career-research/verify-careers.py
then:                        npm run db:import

Careers not listed here stay pending_review. Rows already promoted are
protected from nightly deltas by merge-drive-delta.mjs.
"""
import json
import os

AP = "Andhra Pradesh"
VERIFIED = {}


def verify(state, career, verified, source, **fields):
    VERIFIED[(state, career)] = {
        **fields, "source": source, "source_type": "government_notification",
        "data_tier": "tier_1_official", "verified_date": verified,
    }


# Exam rows already verified in the Exams tab are cited by name; their own
# documents are listed in db/seed/entrance_exams.json.
D = "2026-10-07"

verify(AP, "Engineering (B.Tech / B.E.)", D,
    "Exams tab (verified): AP EAPCET 2026 Instruction Booklet (JNTU Kakinada for APSCHE), JEE Main 2026 and JEE (Advanced) 2026 notices, GATE 2027 (IIT Madras); UPSC Engineering Services Examination 2027, Notice No. 02/2027-ENGG dated 16.09.2026: upsc.gov.in/sites/default/files/Notif-ESEP-2027-Engl-160926.pdf",
    entry_point="After Intermediate MPC (Maths, Physics, Chemistry)",
    required_exams="AP EAPCET (Engineering stream) for colleges in Andhra Pradesh; JEE Main for NITs, IIITs and other centrally funded institutes; JEE Advanced (top ~2,50,000 in JEE Main) for the IITs",
    eligibility="AP EAPCET: Intermediate MPC with at least 45% in the qualifying subjects (40% for reserved categories) and AP local/non-local status. JEE Main: Class 12 with Physics, Chemistry and Maths, no minimum-marks bar, up to 3 consecutive years. JEE Advanced: at most 2 attempts in consecutive years",
    govt_private_options="Government and private engineering colleges across Andhra Pradesh through AP EAPCET counselling; NITs, IIITs and IITs through JEE Main / JEE Advanced",
    next_step="Jobs in industry; M.Tech or PSU recruitment through GATE (any 3rd-year-or-higher engineering student can sit it; score valid 3 years); or UPSC Engineering Services for central government engineering posts (engineering degree, age 21-30, with relaxations)",
)

verify(AP, "Medicine (MBBS)", D,
    "Exams tab (verified): NTA NEET (UG) 2026 notices; Dr. NTR University of Health Sciences, Detailed Notification for MBBS & BDS admissions 2026-27: drntr.uhsap.in/index/notification/20260901205809253.pdf",
    entry_point="After Intermediate BiPC",
    required_exams="NEET-UG (NTA) - the single entrance exam for MBBS, BDS and AYUSH seats in India; AP seats are allotted by Dr. NTR University of Health Sciences counselling",
    eligibility="Class 12 / Intermediate with Physics, Chemistry and Biology: 50% for General, 40% for OBC/SC/ST. At least 17 years old by 31 December of the admission year; no upper age limit. To qualify in NEET-UG 2026: 50th percentile (General/EWS), 40th percentile (SC/ST/BC)",
    govt_private_options="Government, self-financing and private medical colleges in Andhra Pradesh, all through NEET-UG rank and Dr. NTR UHS counselling (competent authority and management quotas)",
    next_step="After the MBBS course and internship, register with the medical council to practise, or go on to postgraduate (MD/MS) specialisation",
)

verify(AP, "Law (5-year integrated LLB)", D,
    "Exams tab (verified): CLAT 2027 press release (Consortium of NLUs); AP LAWCET & PGLCET-2026 Instruction Booklet V2 (Sri Padmavati Mahila Visvavidyalayam for APSCHE); Bar Council of India, All India Bar Examination: allindiabarexamination.com/about.html",
    entry_point="After Class 12 / Intermediate (any stream)",
    required_exams="CLAT (UG) for the National Law Universities; AP LAWCET for 5-year LL.B. in Andhra Pradesh universities and law colleges",
    eligibility="CLAT: Class 12 pass, any stream. AP LAWCET (5-year LL.B.): Intermediate with 45% (42% BC, 40% SC/ST). AP LAWCET also admits graduates with 45% to the 3-year LL.B.",
    govt_private_options="National Law Universities through CLAT; university and affiliated (government and private) law colleges in Andhra Pradesh through AP LAWCET",
    next_step="Enrol as an advocate with the State Bar Council, then pass the All India Bar Examination (held by the Bar Council of India) to get the certificate of practice for any court in India; or judicial service exams, corporate law or an LL.M.",
)

verify(AP, "Civil Services (IAS/IPS/IFS - All India Services)", D,
    "Exams tab (verified): UPSC Examination Notice No. 05/2026-CSE (04.02.2026): upsc.gov.in/sites/default/files/Notif-CSP-2026-Engl-060226Rev.pdf",
    entry_point="After any bachelor's degree (final-year students may apply)",
    required_exams="UPSC Civil Services Examination: Preliminary (objective) -> Main (written) -> Personality Test",
    eligibility="A degree from a recognised university. Age 21-32 on 1 August of the exam year; upper age relaxed by 5 years for SC/ST, 3 for OBC, and for ex-servicemen and PwBD. Attempts: 6 (General/EWS), 9 (OBC and PwBD), unlimited for SC/ST within the age limit",
    govt_private_options="Government only: IAS, IPS, IFS and other Group A and B central services through UPSC",
    next_step="Allocation to a service by rank and preference, training at the service academy, then a career in public administration, policing or diplomacy",
)

verify(AP, "State Civil Services (AP Group services via APPSC)", D,
    "Exams tab (verified): APPSC Brief Notification No. 07/2026 (15/09/2026), Group-I Services: psc.ap.gov.in/Documents/NotificationDocuments/Group_I_072026.pdf",
    entry_point="After any bachelor's degree",
    required_exams="APPSC Group-I (and Group-II and other) exams: Preliminary -> Main -> Interview",
    eligibility="A bachelor's degree from a recognised university (a few posts need a specific degree, and police posts have physical standards). Age limits and reservations are in each detailed notification on psc.ap.gov.in",
    govt_private_options="Government only: Andhra Pradesh Public Service Commission recruits for posts such as Deputy Collector, Deputy Superintendent of Police, Assistant Commissioner of State Tax and Accounts Officer (Treasury)",
    next_step="Posting in the state administrative, police, revenue or finance services, with promotions within the state cadre",
)

verify(AP, "School Teaching (Govt & Private schools)", D,
    "Exams tab (verified): Government of AP, School Education Department, APTET-JUNE 2026 Notification No.01-APTET-JUNE-2026 dated 05-06-2026: tet2dsc.apcfss.in/TET-PDF/APTET-2026 Notification.pdf",
    entry_point="After Intermediate (D.El.Ed route, primary classes) or after a degree (B.Ed route)",
    required_exams="D.El.Ed or B.Ed -> AP TET (Paper 1A for Classes I-V, Paper 2A for Classes VI-VIII) -> AP DSC Teacher Recruitment Test for government posts",
    eligibility="An NCTE-recognised D.El.Ed or B.Ed (RCI for special education) with the marks set in the APTET Information Bulletin; final-semester students may sit AP TET. Unlimited attempts; the certificate is valid for life",
    govt_private_options="AP TET is required to teach Classes I-VIII in AP government, local body, model, residential, welfare, aided and private schools. Government posts are filled through AP DSC, where the TET score carries 20% weightage",
    next_step="Secondary Grade Teacher or School Assistant through DSC, with promotion to headmaster and education officer posts over time",
)

verify(AP, "Defence Services (Army/Navy/Air Force Officer)", D,
    "Exams tab (verified): UPSC Examination Notice No.10/2026-NDA-II and No.11/2026-CDS-II: upsc.gov.in/sites/default/files/Notif-NDA-II-2026-Engl-200526.pdf, Notif-CDS-II-2026-Engl-200526.pdf",
    entry_point="After Class 12 (NDA) or after a degree (CDS)",
    required_exams="NDA & NA exam (UPSC) after Class 12, or CDS exam (UPSC) after graduation; both followed by the SSB interview and medical tests",
    eligibility="NDA: Class 12 (any stream for the Army wing; Physics and Maths for Air Force and Navy), unmarried, within the birth-date window in each notice (open to men and women). CDS: a bachelor's degree (engineering degree for some IMA/INA/AFA entries); age limits by academy",
    govt_private_options="Government only: National Defence Academy, Indian Military Academy, Indian Naval Academy, Air Force Academy and Officers Training Academy",
    next_step="Commission as an officer in the Army, Navy or Air Force after training, then promotion through the officer ranks",
)

verify(AP, "Chartered Accountancy (CA)", D,
    "Exams tab (verified): ICAI Important Announcement No. 13-CA(EXAM)/SEPTEMBER-NOVEMBER/2026; ICAI FAQs on the CA course (icai-call-sahayata.icai.org/wp-content/uploads/2025/03/About-CA-Course-Oro-FAQ.pdf): Direct Entry eligibility and practical training",
    entry_point="After Class 12 (Foundation route) or after graduation (Direct Entry route)",
    required_exams="CA Foundation -> CA Intermediate -> Practical Training (2 years) -> CA Final -> ICAI membership",
    eligibility="Foundation: Class 12 pass (any stream), no age limit. Direct Entry to Intermediate: commerce graduates/post-graduates with at least 55%, other graduates with at least 60%, or those who passed the ICSI / ICMAI intermediate level",
    govt_private_options="A professional qualification of the Institute of Chartered Accountants of India (a statutory body), not a college degree; practical training is done under a practising chartered accountant",
    next_step="Membership of ICAI, then practice, audit and tax firms, or finance roles in companies and government",
)

verify(AP, "Banking (Probationary Officer / Clerk)", D,
    "Exams tab (verified): IBPS CRP-PO/MTs-XVI (30.06.2026), IBPS CRP-CSA-XVI (01.08.2026), SBI PO Advertisement CRPD/PO/2026-27/09",
    entry_point="After any bachelor's degree",
    required_exams="IBPS PO and IBPS Clerk for participating public sector banks; SBI PO for the State Bank of India (Prelims -> Mains -> interview/assessment for PO)",
    eligibility="A degree in any discipline. IBPS PO: age 20-30; IBPS Clerk: age 20-28 and proficiency in the official language of the State/UT applied for; SBI PO: age 21-30 (all with the usual SC/ST/OBC/PwBD relaxations)",
    govt_private_options="Public sector banks through IBPS and SBI exams; private banks recruit through their own processes",
    next_step="Probationary Officer (Junior Management Scale I) or clerk (Customer Service Associate), with promotion through the bank's officer scales",
)

verify(AP, "Architecture (B.Arch)", D,
    "Exams tab (verified): Council of Architecture, nata.in (NATA 2026 schedule and eligibility)",
    entry_point="After Intermediate / Class 12 with Maths",
    required_exams="NATA (Council of Architecture); some institutes also accept JEE Main Paper 2",
    eligibility="Class 12 with Physics, Chemistry and Maths, or a 3-year diploma with Maths; no upper age limit. Check the minimum marks in the current NATA brochure on nata.in",
    govt_private_options="B.Arch (5 years) at Council of Architecture-recognised government and private colleges",
    next_step="Register with the Council of Architecture to practise as an architect; or M.Arch, urban planning or practice in a firm",
)

verify(AP, "Pharmacy (B.Pharm)", D,
    "Exams tab (verified): APEAPCET-2026 Instruction Booklet (JNTU Kakinada for APSCHE): cets.apsche.ap.gov.in/EAPCET/PDF/APEAPCET2026_Instruction_Booklet_Engineering_V4.pdf",
    entry_point="After Intermediate MPC or BiPC",
    required_exams="AP EAPCET: Engineering stream for B.Pharmacy (MPC) and Pharm.D, Agriculture & Pharmacy stream for BiPC students",
    eligibility="Intermediate MPC or BiPC with at least 45% in the qualifying subjects (40% for reserved categories) and AP local/non-local status",
    govt_private_options="Government and private pharmacy colleges in Andhra Pradesh through AP EAPCET counselling",
    next_step="Register with the State Pharmacy Council to work as a pharmacist; or M.Pharm / Pharm.D, or jobs in pharmaceutical manufacturing and regulatory affairs",
)

verify(AP, "Nursing (B.Sc Nursing)", D,
    "Dr. NTR University of Health Sciences: Prospectus/Regulations for admission into B.Sc. (Nursing) 4-Years Degree Course 2026-27 (drntr.uhsap.in/index/notification/20260909153823350.pdf) and Notification (.../20260909153830487.pdf)",
    entry_point="After Intermediate BiPC (with English)",
    required_exams="NEET-UG; Dr. NTR UHS prepares the state merit list from the NEET-UG rank and allots seats by web counselling",
    eligibility="Intermediate with Physics, Chemistry and Biology and English as a compulsory subject: 45% in science subjects (40% for SC, ST and BC). At least 17 years old by 31 December of the admission year; no upper age limit",
    govt_private_options="Colleges affiliated to Dr. NTR UHS (competent authority and management quota seats); male candidates are admitted only in the colleges notified for them",
    next_step="Four-year (eight-semester) course, then registration as a nurse with the state nursing council; M.Sc Nursing for specialisation or teaching",
)

verify(AP, "Science / Research (Basic Sciences)", D,
    "OAMDC (APSCHE) FAQs: oamdc.ap.gov.in/FAQS.do; NTA Joint CSIR-UGC NET December 2025 Information Bulletin (chapter 2) and June 2026 FAQs (cdnbbsr.s3waas.gov.in/s3efdf562ce2fb0ad460fd8e9d33e57f57/uploads/2026/05/20260527531592516.pdf)",
    entry_point="After Intermediate MPC or BiPC",
    required_exams="B.Sc (admission to AP degree colleges through the OAMDC online admissions) -> M.Sc -> Joint CSIR-UGC NET for a research fellowship (JRF), PhD admission or lectureship",
    eligibility="CSIR-UGC NET: a master's degree with at least 55% (50% for OBC-NCL/SC/ST/PwD/third gender). JRF: at most 30 years old on 1 July of the exam year, relaxable up to 5 years for OBC-NCL/SC/ST/third gender/PwD/women; no upper age limit for Assistant Professor or PhD admission",
    govt_private_options="Government, aided and private degree colleges in AP through OAMDC; universities and research institutes for M.Sc and PhD",
    next_step="PhD and research careers in national laboratories and universities, college teaching, or industry R&D",
)

verify(AP, "Information Technology / Software Engineering", D,
    "Exams tab (verified): APEAPCET-2026 Instruction Booklet; OAMDC (APSCHE) FAQs: oamdc.ap.gov.in/FAQS.do (Computer Applications courses in degree colleges)",
    entry_point="After Intermediate MPC (B.Tech) or after Class 12 (BCA)",
    required_exams="AP EAPCET (Engineering stream) for B.Tech CSE/IT and related branches; BCA in AP degree colleges through the OAMDC online admissions",
    eligibility="B.Tech: Intermediate MPC with at least 45% in the qualifying subjects (40% for reserved categories). BCA: as notified on OAMDC for each course",
    govt_private_options="Government and private engineering colleges through AP EAPCET counselling; government, aided and private degree colleges for BCA through OAMDC",
    next_step="Jobs in IT services and product companies, M.Tech through GATE, or MCA after BCA",
)

verify(AP, "Agriculture & Veterinary Sciences", D,
    "Exams tab (verified): APEAPCET-2026 Instruction Booklet (courses admitted: B.Sc.(Ag), B.Sc.(Hort), B.V.Sc.&A.H, B.F.Sc, B.Tech (Agr. Engg.)); NTA ICAR AIEEA (PG)-2026 Information Bulletin (UG admission to ICAR-affiliated universities is through CUET-UG)",
    entry_point="After Intermediate BiPC (MPC for B.Tech Agricultural Engineering)",
    required_exams="AP EAPCET (Agriculture & Pharmacy stream) for B.Sc (Agriculture), B.Sc (Horticulture), B.V.Sc & A.H. and B.F.Sc in Andhra Pradesh; CUET-UG for UG seats at ICAR-affiliated universities in other states",
    eligibility="AP EAPCET: Intermediate BiPC (MPC for Agricultural Engineering) with at least 45% in the qualifying subjects (40% for reserved categories) and AP local/non-local status",
    govt_private_options="State agricultural, horticultural and veterinary university colleges and their affiliated colleges in Andhra Pradesh through AP EAPCET counselling",
    next_step="State agriculture, horticulture and animal husbandry department jobs, agribusiness and veterinary practice, or M.Sc/PhD (ICAR AIEEA PG)",
)

verify(AP, "Design (Fashion / Product / Communication Design)", D,
    "Exams tab (verified): NIFTEE-2026 Information Bulletin (NTA for NIFT); NID Admissions 2027-28 portal; UCEED 2027 Information Brochure (IIT Bombay)",
    entry_point="After Class 12 (any stream)",
    required_exams="NIFT entrance (B.Des, B.F.Tech), NID DAT (B.Des at the National Institutes of Design), UCEED (B.Des at IIT Bombay, Delhi, Guwahati, Hyderabad, Indore, Roorkee and IIITDM Jabalpur)",
    eligibility="NIFT B.Des: Class 12 in any stream, under 24 on 1 August of the admission year (5 years' relaxation for SC/ST/PwD); B.F.Tech needs Maths. UCEED: Class 12 in any stream, born on or after 1 Oct 2002 (1 Oct 1997 for SC/ST/PwD), at most two attempts",
    govt_private_options="NIFT (20 campuses, including NIFT Hyderabad), the NIDs and the IITs; many private design schools also accept these scores",
    next_step="Design jobs in fashion, product, communication and interiors, M.Des, or your own studio",
)

verify(AP, "Cost & Management Accountant (CMA)", D,
    "Institute of Cost Accountants of India, Course Eligibility: icmai.in/ClntStudents/CourseEligibility",
    entry_point="After Class 10 / 12 (Foundation) or after a degree (direct Intermediate)",
    required_exams="CMA Foundation -> CMA Intermediate -> CMA Final -> ICMAI membership",
    eligibility="Foundation: Class 10 pass to register, with Class 12 (10+2) to be completed; ICSI Foundation passers are exempted. Intermediate: 10+2 and CMA Foundation, or a degree from a recognised university, or engineering students who have completed the 2nd year. Provisional admission is allowed while awaiting results",
    govt_private_options="A professional qualification of the Institute of Cost Accountants of India (a statutory body), not a college degree",
    next_step="Membership of ICMAI, then cost and management accounting, corporate finance or government roles",
)

verify(AP, "Government Jobs - SSC CGL & Railways (RRB)", D,
    "Exams tab (verified): SSC Combined Graduate Level Examination 2026 notice (21.05.2026); Railway Recruitment Boards CEN 06/2025 (NTPC Graduate) and CEN 07/2025 (NTPC Under Graduate)",
    entry_point="After Class 12 (RRB NTPC Under Graduate posts) or after a degree (SSC CGL, RRB NTPC Graduate posts)",
    required_exams="SSC CGL: Tier-I -> Tier-II. RRB NTPC: computer-based tests, then a typing/aptitude test where applicable, document verification and medical exam",
    eligibility="SSC CGL: a bachelor's degree (some posts need specific subjects); age 18-27, 20-30 or 18-32 depending on the post. RRB NTPC Under Graduate: Class 12 with at least 50% (not required for SC/ST/PwBD/ex-servicemen), age 18-30. RRB NTPC Graduate: a degree, age 18-33. Usual category relaxations apply",
    govt_private_options="Government only: central ministries and departments (Group B and C posts) through SSC; Indian Railways non-technical posts through the RRBs",
    next_step="Posts such as Assistant Section Officer, Inspector, Auditor (SSC CGL) or Station Master, clerk and ticket supervisor (RRB NTPC), with departmental promotions",
)

verify(AP, "Hotel Management (BSc Hospitality & Hotel Administration)", D,
    "Exams tab (verified): NCHM JEE-2026 Information Bulletin (NTA for NCHMCT)",
    entry_point="After Class 12 (any stream, with English)",
    required_exams="NCHM JEE (conducted by NTA for the National Council for Hotel Management and Catering Technology)",
    eligibility="Passed or appearing in Class 12 with English as a subject; no age limit. A physical fitness certificate is needed at admission",
    govt_private_options="B.Sc Hospitality and Hotel Administration at NCHMCT-affiliated Institutes of Hotel Management: central, state, PSU, PPP and private",
    next_step="Management trainee roles in hotels and hospitality, or further study in hospitality management",
)

verify(AP, "Journalism & Mass Communication", D,
    "Exams tab (verified): NTA CUET (UG) 2026 press releases; Indian Institute of Mass Communication, Admission Notice (2026-27): iimc.gov.in/files/announcements/Admission-Notice-2026-27.pdf",
    entry_point="After Class 12 (any stream) for a bachelor's; after a degree for IIMC",
    required_exams="CUET-UG for journalism/mass communication degrees at participating universities; CUET-PG for IIMC's MA and PG Diploma programmes",
    eligibility="CUET-UG: Class 12 pass or appearing, any stream, no age limit. IIMC PG Diplomas: graduates in any discipline (final-year students may apply); IIMC MA programmes: a bachelor's degree with at least 55%",
    govt_private_options="Central, state and private universities through CUET-UG; IIMC (Delhi and regional campuses) through CUET-PG",
    next_step="Reporting, editing, broadcasting, digital media and public relations roles",
)

verify(AP, "Actuarial Science", D,
    "Institute of Actuaries of India, About ACET: actuariesindia.org/about-acet",
    entry_point="After Class 12 (or while awaiting Class 12 results)",
    required_exams="ACET (Actuarial Common Entrance Test) -> student membership of the Institute of Actuaries of India -> IAI actuarial exams",
    eligibility="Students who have appeared for 10+2 and await results, or anyone who has passed 10+2 or higher (graduates, engineers, CAs, CMAs, CSs and others). The ACET result is valid for 3 years for taking IAI student membership",
    govt_private_options="A professional qualification of the Institute of Actuaries of India (a statutory body), not a college degree; most students work while clearing the exams",
    next_step="Clear the IAI exams to become an Associate and then a Fellow, working in insurance, pensions and risk consulting",
)

verify(AP, "Merchant Navy - Officer Cadre (Nautical Science / Marine Engineering)", D,
    "Indian Maritime University, B.Tech (Marine Engineering) programme page: imu.edu.in/imunew/course-programs?course=2",
    entry_point="After Intermediate MPC",
    required_exams="IMU CET (Indian Maritime University Common Entrance Test) for B.Tech Marine Engineering, B.Sc Nautical Science and other IMU programmes",
    eligibility="10+2 with Physics, Chemistry and Maths: 60% aggregate in PCM (5% relaxation for SC/ST) and 50% in English. Maximum age for men 25 (OBC-NCL 28, SC/ST 30), for women 27 (OBC-NCL 30, SC/ST 32), counted from the start of the academic session. Must meet the Merchant Shipping medical standards",
    govt_private_options="Indian Maritime University (a central university) campuses and its affiliated institutes",
    next_step="Sail as a trainee officer, gain sea time and pass the competency exams to rise to Chief Engineer or Master (Captain)",
)

verify(AP, "Social Work (MSW - Master of Social Work)", D,
    "Exams tab (verified): APPGCET-2026 General Instructions (Sri Venkateswara University for APSCHE); TISS Admission Brochure for Post Graduate Programmes 2026-2027: tiss.ac.in/uploads/files/PG_Admission_Brochure_2026-2027-v3_kDx1Bo7.pdf",
    entry_point="After any bachelor's degree",
    required_exams="AP PGCET for MSW at Andhra Pradesh universities; CUET-PG for TISS (MA Social Work) and other central universities",
    eligibility="A bachelor's degree (course-wise conditions on the APPGCET portal; single-subject distance degrees are not eligible). TISS admits on the CUET-PG 2026 score alone (100% weightage), with no group discussion or interview",
    govt_private_options="University campus, constituent and affiliated colleges in AP through AP PGCET; TISS campuses (Mumbai, Tuljapur, Hyderabad, Guwahati) through CUET-PG",
    next_step="Medical and psychiatric social work, NGO and community development, CSR, school counselling, or lectureship after NET/SET",
)

verify(AP, "Data Science & Analytics", D,
    "Exams tab (verified): APEAPCET-2026 Instruction Booklet; OAMDC (APSCHE) FAQs: oamdc.ap.gov.in/FAQS.do",
    entry_point="After Intermediate MPC (B.Tech) or after Class 12 (B.Sc / BCA)",
    required_exams="AP EAPCET (Engineering stream) for B.Tech CSE (Data Science / AI & ML) branches; B.Sc and BCA in AP degree colleges through the OAMDC online admissions",
    eligibility="B.Tech: Intermediate MPC with at least 45% in the qualifying subjects (40% for reserved categories). B.Sc / BCA: as notified on OAMDC for each course",
    govt_private_options="Government and private engineering colleges through AP EAPCET counselling; degree colleges through OAMDC",
    next_step="Data analyst and data scientist roles, or M.Tech / M.Sc in data science",
)

verify(AP, "Dairy & Fisheries Science", D,
    "Exams tab (verified): APEAPCET-2026 Instruction Booklet (courses admitted include B.Tech (Dairy Technology) and B.F.Sc); NTA ICAR AIEEA (PG)-2026 Information Bulletin (UG at ICAR-affiliated universities through CUET-UG)",
    entry_point="After Intermediate (MPC for B.Tech Dairy Technology; BiPC for B.F.Sc Fisheries)",
    required_exams="AP EAPCET: Engineering stream for B.Tech (Dairy Technology), Agriculture & Pharmacy stream for B.F.Sc; CUET-UG for ICAR-affiliated universities in other states",
    eligibility="Intermediate MPC (Dairy Technology) or BiPC (Fisheries) with at least 45% in the qualifying subjects (40% for reserved categories) and AP local/non-local status",
    govt_private_options="State agricultural and veterinary university colleges in Andhra Pradesh through AP EAPCET counselling",
    next_step="Dairy development and fisheries department jobs, dairy processing and aquaculture industry, or M.Tech / M.F.Sc / PhD",
)

verify(AP, "Sports Coaching", D,
    "SAI Netaji Subhas National Institute of Sports, Patiala: Admission to 64th Batch Diploma Course in Sports Coaching (Session 2026-27): nsnis.org/wp-content/uploads/2026/03/Notification-for-Admission-to-Diploma-Course-in-Sports-Coaching-2026-27.pdf",
    entry_point="After Class 12 (Category A, eminent sportspersons) or after a degree (Category B)",
    required_exams="SAI NSNIS Diploma Course in Sports Coaching: online application, then an online admission test for eligible candidates (Category A sportspersons are admitted directly, subject to medical, fitness and skill tests)",
    eligibility="Category A: Class 12 pass plus Olympic, World Championship, Asian Games, Commonwealth Games or similar participation/medals. Category B: a degree plus participation in major international competitions, recognised senior nationals, Khelo India University Games or All India Inter-University Games (or two junior nationals/Khelo India Youth Games). Para-athletes in listed sports can also apply",
    govt_private_options="Sports Authority of India's NSNIS Patiala; private academies and clubs also employ coaches",
    next_step="Coaching at SAI centres, state sports departments, schools, colleges and academies",
)

verify(AP, "Government Group-D / Constable-Level Jobs (SSC GD Constable, SSC MTS, AP Police Constable)", D,
    "Exams tab (verified): SSC Constable (GD) 2026 notice (01.12.2025); SLPRB AP Notification Rc.No.91/SLPRB/Rect.2/2026 (16.09.2026); SSC Multi-Tasking (Non-Technical) Staff and Havaldar Examination 2025 notice: ssc.gov.in/api/attachment/uploads/masterData/NoticeBoards/Notice_of_adv_mts_2025.pdf",
    entry_point="After Class 10 (SSC GD Constable, SSC MTS) or after Intermediate (AP Police Constable)",
    required_exams="SSC GD Constable: computer-based test, physical efficiency and standards tests, medical. SSC MTS: computer-based test. AP Police Constable: SLPRB written test, physical tests and medical",
    eligibility="SSC GD: Class 10, age 18-23; height 170 cm (men), 157 cm (women). SSC MTS: Class 10 (Matriculation), age 18-25 (18-27 for Havaldar and some MTS posts). AP Police Constable (Civil/AR): Intermediate, age 18-24 on 01.07.2026; men 167.6 cm height and 86.3 cm chest with 5 cm expansion, women 152.5 cm and 40 kg. Category relaxations apply",
    govt_private_options="Government only: Central Armed Police Forces and Assam Rifles (SSC GD), central government offices (SSC MTS), Andhra Pradesh Police (SLPRB)",
    next_step="Promotion to Head Constable and Assistant Sub-Inspector over years of service, or departmental promotion in central offices",
)

verify(AP, "Aviation - Commercial Pilot (CPL)", D,
    "DGCA Pariksha FAQs for flight crew: pariksha.dgca.gov.in/Form/PLT_FAQs (FAQ 7-9)",
    entry_point="After Class 12 with Physics and Maths",
    required_exams="No entrance exam: training at a DGCA-approved Flying Training Organisation, plus the DGCA flight crew licence exams taken through pariksha.dgca.gov.in (requirements in DGCA CAR Section 7, Series B, Part I)",
    eligibility="10+2 with Physics and Maths from a recognised board (passed in both subjects); no maximum age to register as a flight crew candidate",
    govt_private_options="DGCA-approved Flying Training Organisations",
    next_step="After the licence, join an airline as a First Officer, do a type rating, and work up to Captain",
)

verify(AP, "Interior Design (B.Des / B.I.D.)", D,
    "Exams tab (verified): NIFTEE-2026 Information Bulletin (B.Des Fashion Interiors); NID Admissions 2027-28 portal; UCEED 2027 Information Brochure (IIT Bombay)",
    entry_point="After Class 12 (any stream)",
    required_exams="NIFT entrance (B.Des Fashion Interiors), NID DAT, UCEED, or a college's own design test",
    eligibility="NIFT B.Des: Class 12 in any stream, under 24 on 1 August of the admission year (5 years' relaxation for SC/ST/PwD). UCEED: Class 12 in any stream, at most two attempts, with the birth-date limits in the brochure",
    govt_private_options="NIFT (including NIFT Hyderabad), NIDs and IITs; private design colleges with their own tests or these scores",
    next_step="Junior interior designer in design or architecture firms, freelance practice, or M.Des",
)

verify(AP, "Real Estate / RERA-Registered Agent", D,
    "Andhra Pradesh Real Estate Regulatory Authority, AP Real Estate (Regulation and Development) Rules, 2017 Handbook (sections 5 and 9, FAQs): rera.ap.gov.in/rera/books/pdf/Handbook.pdf",
    entry_point="Any time after school; open to career-switchers",
    required_exams="No exam under the AP RERA rules: an agent registers online with AP RERA (Annexure 5 documents) before selling registered projects",
    eligibility="Registration documents include PAN, address proof of the place of business, photographs and IT returns (or an affidavit where returns don't apply)",
    govt_private_options="Registration with the Andhra Pradesh Real Estate Regulatory Authority; work independently or with developers",
    next_step="Registration is valid for five years; renew 3 months before expiry (renewal fee Rs 5,000 for an individual, Rs 25,000 for others)",
)


# ---------- apply ----------
path = os.path.join(os.path.dirname(__file__), "..", "..", "db", "seed", "careers.json")
rows = json.load(open(path, encoding="utf-8"))
found = set()
for r in rows:
    key = (r["state"], r["career_name"])
    if key in VERIFIED:
        r.update(VERIFIED[key])
        found.add(key)
missing = set(VERIFIED) - found
assert not missing, f"verify() names careers not in the seed: {missing}"
with open(path, "w", encoding="utf-8") as f:
    json.dump(rows, f, ensure_ascii=False, indent=2)
    f.write("\n")
print(f"{len(rows)} careers, {sum(r.get('data_tier') == 'tier_1_official' for r in rows)} verified")
