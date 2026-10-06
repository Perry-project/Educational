"""Builds db/seed/exam_subjects.json and db/seed/exam_cutoffs.json from the
exam research below, each entry transcribed from the exam's own official
notification, syllabus or information bulletin (named in its source).

Run from the project root:  python scripts/exam-research/build-exam-seeds.py
then:                        npm run db:import

Rules (CLAUDE.md "Data safety tiers"): subjects and qualifying marks are
tier_1_official only when copied from the primary document; anything else
stays out. Topics are summarised to unit/chapter level, in the document's
own wording and order.
"""
import json
import os

AP, TS = "Andhra Pradesh", "Telangana"
SUBJECTS = []
CUTOFFS = []


def subjects(state, exam, source, verified, items):
    for i, (subject, topics) in enumerate(items, 1):
        SUBJECTS.append({
            "state": state, "exam_name": exam, "subject": subject, "topics": topics,
            "sequence_order": i, "source": source, "source_type": "government_notification",
            "data_tier": "tier_1_official", "verified_date": verified,
        })


VERIFIED_ROWS = {}


def verify(state, exam, verified, source, **fields):
    """Promote a catalogue exam to tier_1_official once its own official
    notification has been read: fields are full_form_body, eligibility,
    application_window, exam_date, admits_into, exam_pattern, ..."""
    VERIFIED_ROWS[(state, exam)] = {
        **fields, "source": source, "source_type": "government_notification",
        "data_tier": "tier_1_official", "verified_date": verified,
    }


def cutoffs(state, exam, year, source, verified, items, kind="qualifying_marks"):
    for category, value, note in items:
        CUTOFFS.append({
            "state": state, "exam_name": exam, "year": year, "category": category, "kind": kind,
            "value": value, "note": note, "source": source,
            "source_type": "government_notification", "verified_date": verified,
        })


# ---------- TG EAPCET 2026 ----------
TG_EAPCET = "TG EAPCET (Telangana State Engineering, Agriculture & Pharmacy Common Entrance Test)"
src = "TG EAPCET-2026 Instruction Booklet (E stream) and Syllabus-E / Syllabus-AP, JNTUH: eapcet.tgche.ac.in/TGEAPCET/Doc2026/"
subjects(TS, TG_EAPCET, src, "2026-10-04", [
    ("Mathematics (Engineering stream: 80 questions)",
     "Algebra: functions, mathematical induction, matrices, complex numbers, De Moivre's theorem, quadratic expressions, theory of equations, permutations and combinations, binomial theorem, partial fractions; "
     "Trigonometry: ratios up to transformations, trigonometric equations, inverse trigonometric and hyperbolic functions, properties of triangles; "
     "Vector algebra: addition and product of vectors; Probability: probability, random variables and distributions; "
     "Coordinate geometry: locus, straight lines, pair of lines, circles, system of circles, parabola, ellipse, hyperbola, 3D coordinates, direction cosines and ratios, plane; "
     "Calculus: limits and continuity, differentiation, applications of derivatives, integration, definite integrals, differential equations"),
    ("Physics (40 questions in each stream)",
     "Physical world; units and measurements; motion in a straight line and in a plane; laws of motion; work, energy and power; systems of particles and rotational motion; oscillations; gravitation; "
     "mechanical properties of solids and fluids; thermal properties of matter; thermodynamics; kinetic theory; waves; ray optics and optical instruments; wave optics; "
     "electric charges and fields; electrostatic potential and capacitance; current electricity; moving charges and magnetism; magnetism and matter; electromagnetic induction; alternating current; "
     "electromagnetic waves; dual nature of radiation and matter; atoms; nuclei; semiconductor electronics; communication systems"),
    ("Chemistry (40 questions in each stream)",
     "Atomic structure; classification of elements and periodicity; chemical bonding and molecular structure; states of matter: gases and liquids; stoichiometry; thermodynamics; chemical equilibrium and acids-bases; "
     "hydrogen and its compounds; s-block elements; environmental chemistry; organic chemistry basics and hydrocarbons; solid state; solutions; electrochemistry and chemical kinetics; surface chemistry; "
     "general principles of metallurgy; p-block elements; d and f block elements and coordination compounds; polymers; biomolecules; chemistry in everyday life; haloalkanes and haloarenes; "
     "organic compounds containing C, H and O (alcohols, phenols, ethers, aldehydes, ketones, carboxylic acids); organic compounds containing nitrogen"),
    ("Botany (Agriculture & Pharmacy stream)",
     "Diversity in the living world; morphology of plants; reproduction in plants; plant systematics; cell structure and function; internal organisation of plants; plant ecology; plant physiology; "
     "microbiology; genetics; molecular biology; biotechnology; plants, microbes and human welfare"),
    ("Zoology (Agriculture & Pharmacy stream)",
     "Diversity of the living world; structural organisation in animals; animal diversity I (invertebrate phyla) and II (chordata); locomotion and reproduction in protozoa; biology and human welfare; "
     "type study of Periplaneta americana; ecology and environment; human anatomy and physiology I-IV; human reproduction; genetics; organic evolution; applied biology"),
])
cutoffs(TS, TG_EAPCET, 2026, src, "2026-10-04", [
    ("General / BC / EWS", "25% of the maximum marks (40 of 160, normalised)", "Needed to be ranked"),
    ("SC / ST", "No minimum", "Admission limited to the seats reserved for SC/ST"),
])

# ---------- TS ECET 2026 ----------
TS_ECET = "TS ECET (Telangana State Engineering Common Entrance Test)"
src = "TG ECET-2026 Detailed Notification and Pattern of Examination, Osmania University: ecet.tgche.ac.in/UI/Documents/"
subjects(TS, TS_ECET, src, "2026-10-04", [
    ("Mathematics (diploma candidates, 50 marks)", "Common to all engineering branches"),
    ("Physics (diploma candidates, 25 marks)", "Common to all engineering branches"),
    ("Chemistry (diploma candidates, 25 marks)", "Common to all engineering branches"),
    ("Engineering paper (diploma candidates, 100 marks)",
     "Separate paper for each diploma branch: Civil, Electrical & Electronics, Mechanical, Electronics & Communication, Computer Science, Chemical, Metallurgical, Mining, Electronics & Instrumentation"),
    ("B.Sc (Mathematics) candidates (200 marks)", "Mathematics 100 marks, Analytical Ability 50 marks, Communicative English 50 marks"),
    ("Pharmacy (200 marks)", "Pharmaceutics, Pharmacology, Pharmacognosy, Pharmaceutical Chemistry (50 marks each)"),
])
cutoffs(TS, TS_ECET, 2026, src, "2026-10-04", [
    ("General / BC / EWS", "25% of the aggregate (50 of 200)", "Needed to be ranked"),
    ("SC / ST", "No minimum", "Rank is cancelled if the SC/ST claim is later found invalid"),
])

# ---------- TS ICET 2026 ----------
TS_ICET = "TS ICET (Telangana State Integrated Common Entrance Test)"
src = "TG ICET-2026 Notification and Syllabus (Mahatma Gandhi University, Nalgonda): icet.tgche.ac.in/Documents/2026Docs/"
subjects(TS, TS_ICET, src, "2026-10-04", [
    ("Section A: Analytical Ability (75 questions)",
     "Data sufficiency (20); problem solving (55): number and letter series, analogies, odd one out, missing numbers; data analysis from tables, graphs, bar and pie charts, Venn diagrams; coding and decoding; calendar, clock, blood relation, schedule and seating arrangement problems"),
    ("Section B: Mathematical Ability (75 questions)",
     "Arithmetic (35): indices, ratio and proportion, surds, divisibility, LCM and GCD, percentages, profit and loss, partnership, pipes and cisterns, time and distance, time and work, areas, volumes, mensuration, modular arithmetic; "
     "Algebra and geometry (30): sets, polynomials, remainder theorem, linear equations, progressions, trigonometric ratios and identities, heights and distances, plane geometry of lines, triangles, quadrilaterals and circles, coordinate geometry; "
     "Statistics (10): mean, median, mode, simple probability"),
    ("Section C: Communication Ability (50 questions)",
     "Vocabulary, synonyms and antonyms, tense and voice, phrasal verbs and idioms, articles and prepositions, computer terminology, business terminology, three comprehension passages"),
])
cutoffs(TS, TS_ICET, 2026, src, "2026-10-04", [
    ("General / BC / EWS", "25% (50 of 200)", "Needed to be ranked"),
    ("SC / ST", "No minimum", "Rank is cancelled if the SC/ST claim is later found invalid"),
])

# ---------- AFCAT 02/2026 ----------
src = "AFCAT 02/2026 Notification, para 8.1-8.2 (Indian Air Force): afcat.edcil.co.in/assets/images/news/AFCAT_02_2026/"
subjects(AP, "AFCAT", src, "2026-10-04", [
    ("English", "Comprehension, error detection, sentence completion, synonyms and antonyms, cloze test, idioms and phrases, analogy, sentence rearrangement, one-word substitution, transformation of sentences, homonyms"),
    ("General Awareness", "History, geography, sports, national and international organisations, art and culture, personalities, environment and ecology, Indian polity, economy, basic science, science and technology, current affairs, defence"),
    ("Numerical Ability (Class 10 level)", "Decimal fractions, time and work, average and percentage, profit and loss, ratio and proportion, simple and compound interest, time and distance (trains, boats and streams), area and perimeter, probability, number system and series, mixtures and alligation, squares, cubes and roots, HCF and LCM, mensuration, heights and distances, mean, median and mode, exponents and powers"),
    ("Reasoning and Military Aptitude", "Verbal and non-verbal reasoning"),
])
# AFCAT publishes no fixed qualifying marks: the notification says the IAF
# fixes them at its discretion, so no cutoff row is recorded.

# ---------- AP EAPCET 2026 (Engineering) ----------
src = "AP EAPCET-2026 Instruction Booklet (Engineering) V4, Annexure-I syllabus and section 9 qualifying marks (JNTU Kakinada for APSCHE): cets.apsche.ap.gov.in/EAPCET/PDF/APEAPCET2026_Instruction_Booklet_Engineering_V4.pdf"
subjects(AP, "AP EAPCET", src, "2026-10-04", [
    ("Mathematics (Engineering stream: 80 questions)",
     "Algebra: functions, mathematical induction, matrices, complex numbers, De Moivre's theorem, quadratic expressions, theory of equations, permutations and combinations, binomial theorem, partial fractions; "
     "Trigonometry: ratios up to transformations, trigonometric equations, inverse trigonometric and hyperbolic functions, properties of triangles; "
     "Vector algebra: addition and product of vectors; Measures of dispersion and probability: probability, random variables and distributions; "
     "Coordinate geometry: locus, transformation of axes, straight lines, pair of lines, circles, system of circles, parabola, ellipse, hyperbola, 3D coordinates, direction cosines and ratios, plane; "
     "Calculus: limits and continuity, differentiation, applications of derivatives, integration, definite integrals, differential equations"),
    ("Physics (40 questions)",
     "Physical world; units and measurements; motion in a straight line and in a plane; laws of motion; work, energy and power; systems of particles and rotational motion; oscillations; gravitation; "
     "mechanical properties of solids and fluids; thermal properties of matter; thermodynamics; kinetic theory; waves; ray optics and optical instruments; wave optics; electric charges and fields; "
     "electrostatic potential and capacitance; current electricity; moving charges and magnetism; magnetism and matter; electromagnetic induction; alternating current; electromagnetic waves; "
     "dual nature of radiation and matter; atoms; nuclei; semiconductor electronics; communication systems"),
    ("Chemistry (40 questions)",
     "Atomic structure; classification of elements and periodicity; chemical bonding and molecular structure; states of matter; stoichiometry; thermodynamics; chemical equilibrium and acids-bases; "
     "hydrogen and its compounds; s-block elements; p-block elements (groups 13 and 14); environmental chemistry; organic chemistry basics and hydrocarbons; solid state; solutions; "
     "electrochemistry and chemical kinetics; surface chemistry; general principles of metallurgy; p-block elements; d and f block elements and coordination compounds; polymers; biomolecules; "
     "chemistry in everyday life; haloalkanes and haloarenes; organic compounds containing C, H and O; organic compounds containing nitrogen"),
])
cutoffs(AP, "AP EAPCET", 2026, src, "2026-10-04", [
    ("General / BC / EWS", "25% of the maximum marks (40 of 160)", "Needed to be ranked. Ranks combine 75% EAPCET marks with 25% Intermediate group-subject marks"),
    ("SC / ST", "No minimum", "Admission limited to the seats reserved for SC/ST (G.O.Ms. No. 179, 1986)"),
])

# ---------- AP ECET 2026 ----------
src = "APECET-2026 Instruction Booklet V6, sections on pattern and 5.0 qualifying marks (JNTU Anantapur for APSCHE): cets.apsche.ap.gov.in/ECET/PDF/APECET2026_InstructionBooklet_V6.pdf"
subjects(AP, "AP ECET", src, "2026-10-04", [
    ("Mathematics (engineering stream, 50 marks)", "Common to all branches"),
    ("Physics (engineering stream, 25 marks)", "Common to all branches"),
    ("Chemistry (engineering stream, 25 marks)", "Common to all branches"),
    ("Engineering paper (100 marks)",
     "Separate paper for each branch: Civil, Electrical, Mechanical, Electronics & Communication, Computer Science, Chemical, Metallurgical, Mining, Electronics & Instrumentation, Ceramic Technology, Biotechnology, Agricultural Engineering"),
    ("Pharmacy stream (200 marks)", "Pharmaceutics, Pharmaceutical Chemistry, Pharmacognosy, Pharmacology (50 marks each)"),
    ("B.Sc (Mathematics) stream", "Mathematics 100 marks, Analytical Ability 50 marks, Communicative English 50 marks"),
])
cutoffs(AP, "AP ECET", 2026, src, "2026-10-04", [
    ("General / BC / EWS", "25% of the aggregate (50 of 200)", "Needed to be ranked"),
    ("SC / ST", "No minimum", "Rank is cancelled if the SC/ST claim is later found invalid"),
])

# ---------- AP ICET 2026 ----------
src = "APICET-2026 Instruction Booklet V2, pattern, syllabus and merit list sections (for APSCHE): cets.apsche.ap.gov.in/ICET/PDF/APICET2026_InstructionBooklet_V2.pdf"
subjects(AP, "AP ICET", src, "2026-10-04", [
    ("Section A: Analytical Ability (75 questions)",
     "Data sufficiency (20); problem solving (55): sequences and series, analogies, odd one out, missing numbers; data analysis from tables, graphs, bar and pie charts, Venn diagrams and passages; coding and decoding; calendar, clock, blood relation, schedule and seating arrangement problems"),
    ("Section B: Communication Ability (70 questions)",
     "Vocabulary (15), functional grammar (20), business and computer terminology (15), reading comprehension: 4 passages (20)"),
    ("Section C: Mathematical Ability (55 questions)",
     "Arithmetic (35): indices, ratio and proportion, surds, divisibility, LCM and GCD, percentages, profit and loss, partnership, pipes and cisterns, time, distance and work, areas, volumes, mensuration, modular arithmetic; "
     "Algebra and geometry (10): statements and truth tables, sets, relations and functions, equation of a line, trigonometric ratios and identities, heights and distances, polynomials, remainder theorem, progressions, binomial theorem, matrices, limits and derivatives, plane and coordinate geometry; "
     "Statistics (10): frequency distributions, mean, median, mode, standard deviation, correlation, simple probability"),
])
cutoffs(AP, "AP ICET", 2026, src, "2026-10-04", [
    ("General / BC / EWS", "25% (50 of 200)", "Needed to be ranked"),
    ("SC / ST", "No minimum", "Rank is cancelled if the SC/ST claim is later found invalid"),
])

# Physics and Chemistry units shared by the NMC (NEET) and NTA (JEE Main)
# 2026 syllabi, which use the same unit list.
PHY_20 = ("Physics and measurement; kinematics; laws of motion; work, energy and power; rotational motion; gravitation; properties of solids and liquids; thermodynamics; "
          "kinetic theory of gases; oscillations and waves; electrostatics; current electricity; magnetic effects of current and magnetism; electromagnetic induction and alternating currents; "
          "electromagnetic waves; optics; dual nature of matter and radiation; atoms and nuclei; electronic devices; experimental skills")
CHEM_20 = ("Physical: some basic concepts in chemistry, atomic structure, chemical bonding and molecular structure, chemical thermodynamics, solutions, equilibrium, redox reactions and electrochemistry, chemical kinetics; "
           "Inorganic: classification of elements and periodicity, p-block elements, d- and f-block elements, coordination compounds; "
           "Organic: purification and characterisation of organic compounds, basic principles of organic chemistry, hydrocarbons, compounds containing halogens, oxygen and nitrogen, biomolecules, principles of practical chemistry")

# ---------- NEET-UG 2026 ----------
src = "NEET (UG)-2026 Information Bulletin, Chapter 8 qualifying criteria and pattern (NTA): cdnbbsr.s3waas.gov.in/s37bc1ec1d9c3426357e69acd5bf320061/uploads/2026/02/202602231394640855.pdf; syllabus notified by NMC: .../uploads/2026/01/202601081066816297.pdf"
subjects(AP, "NEET-UG", src, "2026-10-04", [
    ("Physics (45 questions)", PHY_20),
    ("Chemistry (45 questions)", CHEM_20),
    ("Biology: Botany & Zoology (90 questions)",
     "Diversity in living world; structural organisation in animals and plants; cell structure and function; plant physiology; human physiology; reproduction; genetics and evolution; biology and human welfare; biotechnology and its applications; ecology and environment"),
])
cutoffs(AP, "NEET-UG", 2026, src, "2026-10-04", [
    ("General / General-EWS", "50th percentile", "Minimum to be eligible for MBBS/BDS/AYUSH admission"),
    ("SC / ST / OBC-NCL", "40th percentile", None),
    ("PwBD (General / General-EWS)", "45th percentile", None),
    ("PwBD (SC / ST / OBC-NCL)", "40th percentile", None),
], kind="qualifying_percentile")

# ---------- JEE Main 2026 ----------
src = "JEE (Main)-2026 Information Bulletin, section 2.4 pattern (NTA): cdnbbsr.s3waas.gov.in/s3f8e59f4b2fe7c5705bf878bbd494ccdf/uploads/2025/11/202511021649722475.pdf; syllabus .../uploads/2025/10/202510311323551056.pdf"
subjects(AP, "JEE Main", src, "2026-10-04", [
    ("Mathematics (20 MCQ + 5 numerical)",
     "Sets, relations and functions; complex numbers and quadratic equations; matrices and determinants; permutations and combinations; binomial theorem; sequences and series; limits, continuity and differentiability; "
     "integral calculus; differential equations; coordinate geometry; three-dimensional geometry; vector algebra; statistics and probability; trigonometry"),
    ("Physics (20 MCQ + 5 numerical)", PHY_20),
    ("Chemistry (20 MCQ + 5 numerical)", CHEM_20),
])
src = "NTA Press Release, 20 April 2026, 'Declaration of the Result/NTA Scores for JEE (Main) - 2026 of Paper 1 (B.E./B.Tech.)': cdnbbsr.s3waas.gov.in/s3f8e59f4b2fe7c5705bf878bbd494ccdf/uploads/2026/04/20260420809492136.pdf"
cutoffs(AP, "JEE Main", 2026, src, "2026-10-04", [
    ("UR (General)", "93.4123549 percentile", "To be eligible for JEE (Advanced) 2026; 96,873 candidates"),
    ("EWS", "82.4164528 percentile", "To be eligible for JEE (Advanced) 2026; 25,009 candidates"),
    ("OBC-NCL", "80.9232583 percentile", "To be eligible for JEE (Advanced) 2026; 67,597 candidates"),
    ("SC", "63.9172792 percentile", "To be eligible for JEE (Advanced) 2026; 37,522 candidates"),
    ("ST", "52.0174712 percentile", "To be eligible for JEE (Advanced) 2026; 18,790 candidates"),
    ("UR-PwBD", "0.0023186 percentile", "To be eligible for JEE (Advanced) 2026; 4,391 candidates"),
], kind="cutoff_score")

# ---------- NDA & NA (II) 2026 ----------
NDA = "NDA (National Defence Academy exam)"
src = "UPSC Examination Notice No.10/2026-NDA-II, Appendix I scheme and syllabus: upsc.gov.in/sites/default/files/Notif-NDA-II-2026-Engl-200526.pdf"
subjects(AP, NDA, src, "2026-10-04", [
    ("Paper I: Mathematics (300 marks)",
     "Algebra; matrices and determinants; trigonometry; analytical geometry of two and three dimensions; differential calculus; integral calculus and differential equations; vector algebra; statistics and probability"),
    ("Paper II: General Ability Test, Part A English (200 marks)", "Grammar and usage, vocabulary, comprehension and cohesion in extended text"),
    ("Paper II: General Ability Test, Part B General Knowledge (400 marks)",
     "Physics (about 25%), Chemistry (15%), General Science (10%), History and Freedom Movement (20%), Geography (20%), Current Events (10%)"),
])
# UPSC fixes NDA qualifying marks at its discretion after each exam; none are
# published in the notification, so no cutoff row is recorded.

# ---------- CDS (II) 2026 ----------
CDS = "CDS (Combined Defence Services exam)"
src = "UPSC Examination Notice No.11/2026-CDS-II, Appendix I scheme and syllabus: upsc.gov.in/sites/default/files/Notif-CDS-II-2026-Engl-200526.pdf"
subjects(AP, CDS, src, "2026-10-04", [
    ("English (100 marks)", "Understanding of English and workmanlike use of words"),
    ("General Knowledge (100 marks)", "Current events and everyday science as expected of an educated person, plus Indian history and geography"),
    ("Elementary Mathematics (100 marks; IMA, INA and AFA only)", "Arithmetic, algebra, trigonometry, geometry, mensuration, statistics (Class 10 level)"),
])

# ---------- JEE (Advanced) 2026 ----------
src = "JEE (Advanced) 2026 Information Brochure (IIT Roorkee), sections 9, 22 and Annexure-I syllabi: jeeadv.ac.in/documents/IBEnglish_2026.pdf"
subjects(AP, "JEE Advanced", src, "2026-10-04", [
    ("Mathematics",
     "Sets, relations and functions; algebra; matrices; probability and statistics; trigonometry; analytical geometry; differential calculus; integral calculus; vectors"),
    ("Physics",
     "General (units, dimensions, measurement and experiments); mechanics; thermal physics; electricity and magnetism; electromagnetic waves; optics; modern physics"),
    ("Chemistry",
     "General topics; atomic structure; chemical bonding; chemical thermodynamics; chemical and ionic equilibrium; electrochemistry; chemical kinetics; solid state; solutions; surface chemistry; "
     "periodicity; hydrogen; s-, p-, d- and f-block elements; coordination compounds; isolation of metals; qualitative analysis; environmental chemistry; "
     "basic principles of organic chemistry; alkanes, alkenes and alkynes; benzene; phenols; alkyl halides; alcohols; ethers; aldehydes and ketones; carboxylic acids; amines; haloarenes; biomolecules; polymers; chemistry in everyday life; practical organic chemistry"),
])
cutoffs(AP, "JEE Advanced", 2026, src, "2026-10-04", [
    ("Common Rank List (all)", "10% in each subject and 35% aggregate", None),
    ("GEN-EWS", "9% in each subject and 31.5% aggregate", None),
    ("OBC-NCL", "9% in each subject and 31.5% aggregate", None),
    ("SC", "5% in each subject and 17.5% aggregate", None),
    ("ST", "5% in each subject and 17.5% aggregate", None),
    ("PwD (all rank lists)", "5% in each subject and 17.5% aggregate", None),
    ("Preparatory course (SC/ST/PwD)", "2.5% in each subject and 8.75% aggregate", None),
])

# ---------- CLAT 2027 (UG) ----------
src = "Consortium of NLUs, CLAT 2027 UG pages: consortiumofnlus.ac.in/clat-2027/ug-question-format.html, ug-syllabus.html, ug-eligibility.html (checked 04 Oct 2026)"
subjects(AP, "CLAT (UG)", src, "2026-10-04", [
    ("English Language (22-26 questions, about 20%)", "Passages of about 450 words; comprehension, inferences and conclusions, summarising, comparing arguments, meaning of words in context"),
    ("Current Affairs including General Knowledge (28-32 questions, about 25%)", "Passages from news and non-fiction; contemporary events of significance in India and the world, arts and culture, international affairs, historical events of continuing significance"),
    ("Legal Reasoning (28-32 questions, about 25%)", "Passages on factual situations or scenarios involving legal matters, public policy or moral philosophy; applying given rules and principles, no prior knowledge of law needed"),
    ("Logical Reasoning (22-26 questions, about 20%)", "Passages of about 450 words; recognising arguments, premises and conclusions, critically analysing reasoning, drawing inferences, relationships and analogies, contradictions and equivalence"),
    ("Quantitative Techniques (10-14 questions, about 10%)", "Short sets of facts, propositions or numerical information; Class 10 level mathematics: ratios and proportions, basic algebra, mensuration, statistical estimation"),
])
cutoffs(AP, "CLAT (UG)", 2027, src, "2026-10-04", [
    ("General / OBC / EWS", "45% in Class 12 (10+2)", "Minimum to apply; no upper age limit"),
    ("SC / ST / PwD", "40% in Class 12 (10+2)", "Minimum to apply"),
], kind="eligibility_marks")

# Minimum qualifying-exam marks to apply, from the same official notifications
# as the qualifying marks above.
cutoffs(TS, TG_EAPCET, 2026, "TG EAPCET-2026 Detailed Notification, para 2(c)(ii) (JNTUH): eapcet.tgche.ac.in/TGEAPCET/Doc2026/Detailed Notification-2026.pdf", "2026-10-04", [
    ("General", "45% in MPC/BiPC subjects of Intermediate taken together", "Minimum to be eligible"),
    ("Reserved categories", "40% in MPC/BiPC subjects of Intermediate taken together", "Minimum to be eligible"),
], kind="eligibility_marks")
cutoffs(TS, TS_ECET, 2026, "TG ECET-2026 Detailed Notification, para 2(v) (Osmania University): ecet.tgche.ac.in/UI/Documents/Detailed Notification.pdf", "2026-10-04", [
    ("General", "45% in the Diploma or B.Sc (Mathematics)", "Minimum to be eligible"),
    ("Reserved categories", "40% in the Diploma or B.Sc (Mathematics)", "Minimum to be eligible"),
], kind="eligibility_marks")
cutoffs(TS, TS_ICET, 2026, "TG ICET-2026 Notification, para I(e)(iv) (Mahatma Gandhi University): icet.tgche.ac.in/Documents/2026Docs/TG ICET 2026 - Notification.pdf", "2026-10-04", [
    ("Unreserved", "50% in the qualifying degree", "Minimum to be eligible"),
    ("SC / ST / BC", "45% in the qualifying degree", "Minimum to be eligible"),
], kind="eligibility_marks")

# =====================================================================
# Batch 2 (2026-10-04): catalogue exams promoted to tier_1_official.
# =====================================================================

# ---------- TS POLYCET 2026 ----------
src = "POLYCET-2026 Instruction Booklet, SBTET Telangana (I/1025907/2026): polycet.sbtet.telangana.gov.in/Downloads/polycet2026.pdf"
verify(TS, "TS POLYCET", "2026-10-04", src,
    full_form_body="Polytechnic Common Entrance Test conducted by the State Board of Technical Education and Training (SBTET), Telangana, for diploma courses in polytechnics, and agriculture, veterinary and horticulture diplomas of PJTAU, PVNRTVU and SKLTGHU",
    eligibility="Indian national meeting Telangana local/non-local rules; passed SSC (or CBSE/ICSE/NIOS/TOSS equivalent) with Mathematics and at least 35% marks (equivalent boards: 35% in each subject incl. Maths, Physics, Chemistry). Students writing SSC in March/April 2026 may apply. No age limit for polytechnics; agriculture/veterinary/horticulture diplomas need age 15-22 (as on 31.12.2026)",
    application_window="2026: online registration 02 Feb - 20 Apr 2026; with Rs 100 late fee to 21 Apr; with Rs 300 Tatkal fee to 22 Apr 2026",
    exam_date="13 May 2026 (Wednesday), 11:00 AM - 1:30 PM; results about 12 days after the exam. 2027 dates not yet announced",
    admits_into="Diploma courses in Engineering/Non-Engineering/Technology at government, aided and private polytechnics in Telangana (MPC rank), and agriculture, veterinary and horticulture diplomas of PJTAU, PVNRTVU and SKLTGHU (MBiPC rank)",
    exam_pattern="Pen and paper, 2½ hours, 150 multiple-choice questions of 1 mark: Mathematics 60, Physics 30, Chemistry 30, Biology 30. Syllabus is Telangana SSC 2025-26. Two ranks: MPC (out of 120) for polytechnics and MBiPC (Maths scaled to 30) for agriculture/veterinary diplomas.",
)
subjects(TS, "TS POLYCET", src, "2026-10-04", [
    ("Mathematics (60 questions)", "Telangana SSC (Class 10) 2025-26 syllabus"),
    ("Physics (30 questions)", "Telangana SSC (Class 10) 2025-26 syllabus"),
    ("Chemistry (30 questions)", "Telangana SSC (Class 10) 2025-26 syllabus"),
    ("Biology (30 questions; for agriculture/veterinary/horticulture diplomas)", "Telangana SSC (Class 10) 2025-26 syllabus"),
])
cutoffs(TS, "TS POLYCET", 2026, src, "2026-10-04", [
    ("General / BC / EWS", "36 of 120 (30%) in Maths, Physics and Chemistry together", "Same 30% (Maths scaled to 30, with Biology) for agriculture/veterinary diplomas"),
    ("SC / ST", "1 mark", "Ranked with at least 1 mark; may compete for SC/ST seats below 30%"),
])
cutoffs(TS, "TS POLYCET", 2026, src, "2026-10-04", [
    ("All categories", "35% in SSC with Mathematics", "Minimum to apply"),
], kind="eligibility_marks")

# ---------- JNVST 2027 (Class 6) ----------
src = "JNVST-2027 Prospectus (Navodaya Vidyalaya Samiti), Class VI admission 2027-28: cbseitms.rcil.gov.in/nvs/assets/pdf/Final_Prospectus_2027.pdf (linked from navodaya.gov.in)"
verify(AP, "JNVST (Navodaya Class 6)", "2026-10-04", src,
    eligibility="Bona fide resident of the district studying in Class V in 2026-27 at a recognised school in that district; born between 01.05.2015 and 31.07.2017 (both inclusive); must have studied the full academic session of Classes III, IV and V",
    application_window="JNVST 2027: online application (free) on navodaya.gov.in; last date 31 July 2026 (closed)",
    exam_date="28 November 2026 (single phase for summer- and winter-bound JNVs), 11:30 AM - 1:30 PM. Result expected by end of March 2027",
    admits_into="Class VI in the Jawahar Navodaya Vidyalaya of the student's district for 2027-28 (co-educational, residential; free education, board and lodging); up to 80 seats per JNV",
    exam_pattern="Pen and paper (OMR), 2 hours, 80 objective questions for 100 marks, 1.25 marks each, no negative marking: Mental Ability 20 + Environmental Studies 20 (50 marks, 60 min), Arithmetic 20 (25 marks, 30 min), Language 20 (25 marks, 30 min). Extra 40 minutes for Divyang students. Written in the student's chosen language/medium.",
)
subjects(AP, "JNVST (Navodaya Class 6)", src, "2026-10-04", [
    ("Section 1a: Mental Ability Test (questions 1-20)", "Non-verbal test on figures and diagrams: pattern completion, figure series completion, geometrical figure completion (triangle, square, circle), mirror and water images, embedded figures"),
    ("Section 1b: Environmental Studies (questions 21-40)", "15 MCQs and one passage with 5 questions. The natural world (transport, rivers, mountains, plants and animals, natural disasters, shelters, water cycle); the human body (food and nutrients, hygiene, senses, digestive, circulatory and respiratory systems); science in daily life (food preservation, water and air pollution, conservation of water and soil); social surroundings (superlatives of India, states and capitals, national symbols, landscapes, festivals, seasons, forests, crops, clothes and fibres)"),
    ("Section 2: Arithmetic (20 questions)", "Number system and number names; four operations on whole numbers; factors and multiples; fractions (adding/subtracting like fractions, multiplication); measurement of length, mass, capacity, time and money with unit conversion; simplification; perimeter and area of polygons, squares, rectangles and triangles; types of angles, directions and mapping; data from bar diagrams, tables and pictographs"),
    ("Section 3: Language (20 questions)", "Four reading passages, each followed by 5 questions"),
])
cutoffs(AP, "JNVST (Navodaya Class 6)", 2027, src, "2026-10-04", [
    ("All candidates", "14 in Mental Ability + EVS, 7 in Arithmetic, 7 in Language", "Must reach the minimum in each of the three sections"),
])
cutoffs(AP, "JNVST (Navodaya Class 6)", 2027, src, "2026-10-04", [
    ("Rural", "At least 75% of seats in a district", "Must have studied Classes III-V in rural schools"),
    ("SC / ST", "In proportion to district population; at least 15% SC and 7.5% ST", "SC and ST together capped at 50%"),
    ("OBC (Central list)", "27%", "Over and above SC/ST; needs a valid Central OBC certificate"),
    ("Girls", "At least one third of seats", None),
], kind="seat_reservation")

# ---------- AISSEE 2026 (Sainik Schools) ----------
AISSEE = "AISSEE (Sainik Schools Class 6 & 9)"
src = "AISSEE-2026 Information Bulletin (NTA for Sainik Schools Society): cdnbbsr.s3waas.gov.in/s388a839f2f6f1427879fc33ee4acf4f66/uploads/2025/10/20251010937989896.pdf (from exams.nta.nic.in/sainik-school-society/)"
verify(AP, AISSEE, "2026-10-04", src,
    full_form_body="All India Sainik Schools Entrance Examination, conducted by the National Testing Agency for admission to Class 6 and Class 9 of the 33 Sainik Schools and approved New Sainik Schools (Ministry of Defence)",
    eligibility="Class 6: aged 10-12 on 31 March 2026 (born 01 Apr 2014 - 31 Mar 2016); girls eligible. Class 9: aged 13-15 (born 01 Apr 2011 - 31 Mar 2013); girls eligible subject to vacancies. Ages as on 31 March 2026",
    application_window="AISSEE 2026: online applications 10-30 Oct 2025 (fee by 31 Oct); fee Rs 850 (General / defence wards / OBC-NCL) or Rs 700 (SC/ST). AISSEE 2027 notification not yet released as of 04 Oct 2026",
    exam_date="AISSEE 2026 held in January 2026 (pen and paper, OMR). Class 6: 2:00-4:30 PM; Class 9: 2:00-5:00 PM. AISSEE 2027 date not yet announced",
    admits_into="Class 6 and Class 9 in Sainik Schools (English-medium residential schools preparing students for NDA and other officer academies) and approved New Sainik Schools, through e-counselling by school, gender and category merit lists",
    exam_pattern="Class 6: 150 minutes, 125 questions, 300 marks: Language 25 (2 marks each), Mathematics 50 (3 each), Intelligence 25 (2 each), General Knowledge 25 (2 each); paper in any of 13 languages. Class 9: 180 minutes, 150 questions, 400 marks: Mathematics 50 (4 each), Intelligence 25, English 25, General Science 25, Social Science 25 (2 each); English only.",
)
subjects(AP, AISSEE, src, "2026-10-04", [
    ("Class 6: Mathematics (50 questions, 150 marks)", "Natural numbers, LCM and HCF, unitary method, fractions, ratio and proportion, profit and loss, simplification, average, percentage, area and perimeter, simple interest, lines and angles, complementary and supplementary angles, conversion of units, Roman numerals, types of angles, circle, volume of cube and cuboid, prime and composite numbers, plane figures, decimals, speed and time, operations on numbers, temperature, arranging fractions"),
    ("Class 6: Intelligence (25 questions, 50 marks)", "Analogies (mathematical and verbal), patterns (spatial and mathematical), classification, visual and logical reasoning, series and sequences, critical thinking and problem solving, family relations"),
    ("Class 6: Language (25 questions, 50 marks)", "Up to Class 5 level: comprehension passage, prepositions, articles, vocabulary, verbs, confusing words, question tags, types of sentences, tenses, nouns, pronouns, spelling, word order, sentence formation, antonyms, synonyms, adjectives, interjections, idioms and phrases, collective nouns, number, gender, adverbs, rhyming words, singular/plural"),
    ("Class 6: General Knowledge (25 questions, 50 marks)", "National symbols, India at a glance, art and culture, awards, personalities, Indian defence, sports, national and international organisations, solar system and earth, mountains, water cycle, energy, climate and natural calamities, water use, digestion and food preservation, farming and seeds, tribal communities and forests, scientific devices, water pollution and diseases, humans and animals, plant, animal and human functions, senses and young ones of animals"),
    ("Class 9: Mathematics (50 questions, 200 marks)", "Rational numbers, linear equations in one variable, quadrilaterals, triangles and angle sum, Pythagoras theorem, squares and square roots, cubes and cube roots, comparing quantities, percentage, profit and loss, algebraic expressions, simple and compound interest, discount, solid shapes and 2D/3D views, Euler's formula, mensuration, area, volume and surface area, exponents and powers, direct and inverse proportion, factorisation, data handling, bar and line graphs, playing with numbers, divisibility, statistics (mean, median, mode), probability, parallel lines, time and work"),
    ("Class 9: Intelligence (25 questions, 50 marks)", "Analogies, patterns, classification, visual and logical reasoning, series and sequences, critical thinking and problem solving, family relations"),
    ("Class 9: English (25 questions, 50 marks)", "Spotting errors, comprehension, antonyms, synonyms, prepositions, articles, verbs, tenses, narration, modals, confusing words, subject-verb agreement, spelling, word order, idioms and phrases, sentence improvement and transformation, phrases and clauses, nouns, adjectives, interjections, question tags, adverbs, conjunctions, conditionals, voice, types of sentences, pronouns, gender and number"),
    ("Class 9: General Science (25 questions, 50 marks)", "Coal and petroleum, combustion and flame, cell structure, reproduction in plants and animals, force, friction and pressure, natural phenomena, sound, reflection and dispersion of light, metals and non-metals, synthetic fibres and plastics, chemical effects of current, stars and solar system, air and water pollution, global warming, micro-organisms, calorific value, electroplating, crops and agricultural practices, conservation, biosphere reserves and national parks, adolescence and puberty, endocrine glands and hormones"),
    ("Class 9: Social Science (25 questions, 50 marks)", "Geographical diversity of India, resources and conservation, weather and climate, landforms, locating places on earth, oceans and continents, types of government, the Constitution, universal franchise and elections, Parliament, local self-government, from barter to money, markets, economic activity, early Indian civilisation and cultural roots, cities and states, rise of empires, the Gupta era, the Marathas, the colonial era"),
])
cutoffs(AP, AISSEE, 2026, src, "2026-10-04", [
    ("General / OBC-NCL / Defence (Sainik Schools)", "25% in each section and 40% aggregate", None),
    ("SC / ST (Sainik Schools)", "No minimum", "The 25%/40% rule does not apply to SC/ST in Sainik Schools"),
    ("All candidates (approved New Sainik Schools)", "25% in each section and 40% aggregate", "Applies to SC/ST too"),
])
cutoffs(AP, AISSEE, 2026, src, "2026-10-04", [
    ("Home State / UT", "67% of seats", "Remaining 33% for other states and UTs"),
    ("SC", "15% of seats", None),
    ("ST", "7.5% of seats", None),
    ("OBC-NCL (Central list)", "27% of seats", None),
    ("Wards of defence personnel and ex-servicemen", "25% of seats", "Within the home-state and other-state quotas"),
], kind="seat_reservation")

# ---------- AP SSC Public Examinations 2027 ----------
src = "Board of Secondary Education AP: Press Note Rc.No.01/DCGE-1/Confd/SSC March 2027 (12-07-2026) and the subject blueprints & model papers for SSC Public Examinations 2026-27: bse.ap.gov.in/SUBJECT_WISE_MODEL_PAPER_27.htm (MQP_27/15E Maths, 19E Physical Science, 20E Biology, 21E Social Studies, 13E English)"
verify(AP, "AP SSC Public Examinations", "2026-10-04", src,
    full_form_body="Class 10 Secondary School Certificate (SSC) public examinations of the Board of Secondary Education, Andhra Pradesh, conducted by the Directorate of Government Examinations",
    eligibility="Students studying Class X in a recognised school in Andhra Pradesh during 2026-27 (SSC Public Examinations 2027)",
    application_window="Exam fee notification for March 2027 not yet released as of 04 Oct 2026; blueprints and model papers for 2027 were released on 12 Jul 2026",
    exam_date="SSC Public Examinations 2027 (March 2027); timetable not yet announced as of 04 Oct 2026",
    admits_into="Class 10 (SSC) certificate, needed for Intermediate, AP POLYCET, ITI, APRJC and other routes after Class 10",
    exam_pattern="Written papers. Languages, English, Mathematics and Social Studies: 3 hours 15 minutes (15 minutes reading time), 100 marks each. General Science is two papers of 50 marks, 2 hours each: Paper I Physical Science, Paper II Biological Science. Questions are 1-mark objective, 2-mark very short, 4-mark short and 8-mark essay answers; marks split 60% awareness, 20% sensitivity, 20% creativity (English 65/15/20).",
)
subjects(AP, "AP SSC Public Examinations", src, "2026-10-04", [
    ("Mathematics (100 marks, 33 questions)", "Chapter marks: real numbers 9, polynomials 7, pair of linear equations 11, quadratic equations 7, arithmetic progressions 5, triangles 3, coordinate geometry 10, introduction to trigonometry 7, applications of trigonometry 3, circles 7, areas related to circles 1, surface areas and volumes 5, statistics 12, probability 13 (plus 40 marks of internal choice)"),
    ("Physical Science, General Science Paper I (50 marks, 17 questions)", "Chemical reactions and equations 9, acids, bases and salts 10, metals and non-metals 9, carbon and its compounds 11, light: reflection and refraction 11, the human eye and the colourful world 9, electricity 11, magnetic effects of electric current 8 (plus 28 marks of choice)"),
    ("Biological Science, General Science Paper II (50 marks, 17 questions)", "Life processes 14, control and coordination 6, how do organisms reproduce 10, heredity 10, our environment 10 (plus 20 marks of choice)"),
    ("Social Studies (100 marks: 25 each)", "Geography: resources and development, forest and wildlife, water resources, agriculture, minerals and energy, manufacturing industries, lifelines of national economy (map); History: rise of nationalism in Europe, nationalism in India, the making of a global world, print culture and the modern world; Civics: power sharing, federalism, gender, religion and caste, political parties, outcomes of democracy; Economics: development, sectors of the Indian economy, money and credit, globalisation and the Indian economy"),
    ("English (100 marks, 37 questions)", "Reading comprehension 30, grammar 20, vocabulary 20, creative expression 30"),
    ("First and second languages", "Telugu, Hindi, Urdu, Kannada, Odia, Sanskrit and other language papers, each with its own blueprint"),
])

# ---------- TS LAWCET 2026 ----------
src = "TG LAWCET & PGLCET-2026 Detailed Notification, Important Dates (1st extension) and Syllabus, Osmania University for TGCHE: lawcet.tgche.ac.in/Documents/"
verify(TS, "TS LAWCET", "2026-10-04", src,
    full_form_body="Telangana Law Common Entrance Test for 3-year and 5-year LL.B. courses in Telangana state universities and their affiliated colleges, conducted by Osmania University on behalf of TGCHE",
    eligibility="3-year LL.B.: any graduate degree (10+2+3) with 45% aggregate (42% OBC, 40% SC/ST); a PG degree or B.Ed with the same percentage also counts. 5-year LL.B.: Intermediate (10+2) or equivalent, incl. Polytechnic Diploma, with 45% (42% OBC, 40% SC/ST). Final-year students may apply but must pass by counselling. No age limit (Bar Council of India)",
    application_window="2026: notification 08 Feb 2026, applications from 10 Feb; last date without late fee 10 Apr 2026 (after extension); late fee Rs 500 to 20 Apr, Rs 1,000 to 30 Apr, Rs 2,000 to 05 May, Rs 4,000 to 10 May, Rs 10,000 to 13 May 2026. Fee Rs 900 (Rs 600 SC/ST/PH). 2027 notification not yet released as of 04 Oct 2026",
    exam_date="18 May 2026: 3-year LL.B. 9:30-11:00 AM and 12:30-2:00 PM; 5-year LL.B. 4:00-5:30 PM. Results 05 Jun 2026 (tentative). 2027 date not yet announced",
    admits_into="3-year and 5-year LL.B. in Telangana state universities and affiliated law colleges for 2026-27",
    exam_pattern="90 minutes, 120 objective questions of 1 mark: Part A General Knowledge and Mental Ability 30, Part B Current Affairs 30, Part C Aptitude for the Study of Law 60 (10 on legal passages). Intermediate level for 5-year, degree level for 3-year.",
)
subjects(TS, "TS LAWCET", src, "2026-10-04", [
    ("Part A: General Knowledge and Mental Ability (30)", "General knowledge and mental ability"),
    ("Part B: Current Affairs (30)", "Current affairs"),
    ("Part C: Aptitude for the Study of Law (60)", "Elementary principles of law and the Constitution of India; 10 questions on legal comprehension passages"),
])
cutoffs(TS, "TS LAWCET", 2026, src, "2026-10-04", [
    ("General / BC / EWS", "35% (42 of 120)", "Needed to be ranked"),
    ("SC / ST", "No minimum", None),
])
cutoffs(TS, "TS LAWCET", 2026, src, "2026-10-04", [
    ("General", "45% in the degree (3-year) or Intermediate (5-year)", "44.5% and above is treated as 45%"),
    ("OBC", "42%", "41.5% and above is treated as 42%; OBC certificate required"),
    ("SC / ST", "40%", "39.5% and above is treated as 40%"),
], kind="eligibility_marks")

# ---------- TS EdCET 2026 ----------
src = "TG Ed.CET-2026 Information Booklet and Revised Schedule (Kakatiya University, Warangal for TGCHE): edcet.tgche.ac.in/Documents/Information Booklet of TG EdCET-2026.pdf, .../Schedule.pdf"
verify(TS, "TS EdCET", "2026-10-04", src,
    full_form_body="Telangana Education Common Entrance Test for the 2-year B.Ed course, conducted by Kakatiya University, Warangal on behalf of TGCHE",
    eligibility="Meets Telangana local/non-local rules; any bachelor's degree (B.A, B.Com, B.Sc, B.Sc Home Science, BCA, BBM, BBA, B.A Oriental Languages) or a master's degree with at least 50% aggregate, or B.E/B.Tech with 50%; SC/ST/BC and other reserved categories 40%. Final-year students may apply. The teaching subject (methodology) you can choose depends on your degree subjects",
    application_window="2026: notification 20 Feb 2026; applications from 23 Feb; last date without late fee 22 Apr 2026; late fee Rs 250 to 25 Apr, Rs 500 to 27 Apr, Rs 1,000 to 07 May, Rs 5,000 on 08-09 May 2026. Fee Rs 750 (OC/BC), Rs 550 (SC/ST/PH). 2027 notification not yet released as of 04 Oct 2026",
    exam_date="15 May 2026 (computer-based), two sessions: 10:00 AM-12:00 noon and 2:00-4:00 PM. Results 30 May 2026. 2027 date not yet announced",
    admits_into="2-year B.Ed in colleges of education in Telangana for 2026-27",
    exam_pattern="Computer-based, 2 hours, 150 multiple-choice questions of 1 mark. Paper in English-Telugu or English-Urdu.",
)
subjects(TS, "TS EdCET", src, "2026-10-04", [
    ("Subject content up to Class 10, Telangana curriculum (60)", "Mathematics 20, Physical and Biological Science 20, Social Studies 20"),
    ("Teaching Aptitude (20)", "Aptitude for teaching"),
    ("General English (20)", "English language"),
    ("General Knowledge and Educational Issues (30)", "General knowledge and current issues in education"),
    ("Computer Awareness (20)", "Basic computer knowledge"),
])
cutoffs(TS, "TS EdCET", 2026, src, "2026-10-04", [
    ("General / BC / EWS", "25% (38 of 150)", "Needed to be ranked"),
    ("SC / ST", "No minimum", "But 38 marks needed to claim NCC, sports, PH or armed-forces quota seats"),
])
cutoffs(TS, "TS EdCET", 2026, src, "2026-10-04", [
    ("General", "50% in the qualifying degree", "Minimum to apply"),
    ("SC / ST / BC and other reserved categories", "40% in the qualifying degree", "Minimum to apply"),
], kind="eligibility_marks")

# ---------- TS PGECET 2026 ----------
src = "TG PGECET-2026 General Information, Important Dates and Pattern of Entrance Test (for TGCHE): pgecet.tgche.ac.in/Docs2026/"
verify(TS, "TS PGECET", "2026-10-04", src,
    full_form_body="Telangana Post Graduate Engineering Common Entrance Test for M.E./M.Tech/M.Pharm/M.Arch and Pharm-D (Post Baccalaureate) admissions in Telangana, conducted on behalf of TGCHE",
    eligibility="Indian national from Telangana meeting local/non-local rules; at least 50% marks (45% for reserved categories) in the qualifying degree. GATE-qualified candidates get first preference for PG seats; remaining seats go by PGECET rank",
    application_window="2026: notification 23 Feb 2026; applications from 27 Feb; last date without late fee 06 May 2026, then late-fee windows (up to Rs 10,000) through May 2026. 2027 notification not yet released as of 04 Oct 2026",
    exam_date="29 May - 01 Jun 2026 (computer-based); hall tickets from 22 May 2026. 2027 dates not yet announced",
    admits_into="M.E./M.Tech, M.Pharm, M.Arch and Pharm-D (PB) in Telangana institutions for 2026-27 (seats left after GATE-qualified candidates)",
    exam_pattern="Computer-based, 2 hours, 120 multiple-choice questions of 1 mark in the chosen test paper (branch). No negative marking. Held at Hyderabad and Warangal regional centres.",
)
cutoffs(TS, "TS PGECET", 2026, src, "2026-10-04", [
    ("General / BC / EWS", "25% (30 of 120)", "Needed to be ranked"),
    ("SC / ST", "No minimum", None),
])
cutoffs(TS, "TS PGECET", 2026, src, "2026-10-04", [
    ("General", "50% in the qualifying degree", "Minimum to apply"),
    ("Reserved categories", "45% in the qualifying degree", "Minimum to apply"),
], kind="eligibility_marks")

# ---------- TS CPGET 2026 ----------
src = "TG CPGET-2026 Information Brochure, Revised Activity Schedule and Examination Pattern (Kakatiya University for TGCHE): cpget.tgche.ac.in/PDF/CPGETPDF/"
verify(TS, "TS CPGET", "2026-10-04", src,
    full_form_body="Telangana Common Post Graduate Entrance Test for MA, M.Sc, M.Com, M.Ed and other PG/PG diploma courses of Osmania, Kakatiya, Telangana, Mahatma Gandhi, Palamuru, Satavahana, Veeranari Chakali Ilamma Women's, JNTUH and Dr. Manmohan Singh Earth Sciences universities; conducted by Kakatiya University on behalf of TGCHE (conducting university for 2026)",
    eligibility="A bachelor's degree in the relevant subject (course-wise conditions in the brochure); Arts and Science courses need at least 40% (or equivalent CGPA) in the qualifying exam, a pass is enough for SC/ST",
    application_window="2026: notification and applications from 15 May 2026; last date without late fee 15 Jun 2026; Rs 500 late fee to 17 Jun, Rs 2,000 to 19 Jun 2026. Fee Rs 800 (OC/BC), Rs 600 (SC/ST/PH), Rs 450 per extra subject. 2027 notification not yet released as of 04 Oct 2026",
    exam_date="08-16 Jul 2026 (computer-based); results 05 Aug 2026 (tentative). 2027 dates not yet announced",
    admits_into="PG and PG diploma courses in campus, constituent and affiliated colleges of the nine participating universities, through web-based counselling",
    exam_pattern="Computer-based, 90 minutes, 100 objective questions of 1 mark in the chosen subject, framed only from that subject's syllabus. M.Sc Biochemistry, Environmental Science, Forensic Science, Genetics and Microbiology share one test: Part A Chemistry 40 + Part B one B.Sc optional 60. M.Sc Biotechnology: Chemistry 40 + Biotechnology 60.",
)
cutoffs(TS, "TS CPGET", 2026, src, "2026-10-04", [
    ("General / BC / EWS (Arts and Science courses)", "40% in the qualifying degree or equivalent CGPA", "Minimum to apply"),
    ("SC / ST", "A pass in the qualifying degree", "Minimum to apply"),
], kind="eligibility_marks")

# ---------- AP CETs 2026: APSCHE master notification ----------
# APSCHE "AP-CETs-2026 Notification" (03.02.2026) names each CET's conducting
# university, exam dates and registration start.
AP_CETS_SRC = "APSCHE AP-CETs-2026 Notification dated 03.02.2026: cets.apsche.ap.gov.in/EDCET/PDF/APEDCET2026_Notification.pdf"

# ---------- AP EdCET 2026 ----------
src = AP_CETS_SRC + "; APEdCET-2026 Eligibility, Syllabus and Examination Schedule: cets.apsche.ap.gov.in/EDCET/PDF/"
verify(AP, "AP EdCET", "2026-10-04", src,
    conducting_body="Dravidian University, Kuppam (on behalf of APSCHE)",
    full_form_body="Andhra Pradesh Education Common Entrance Test for the 2-year B.Ed course, conducted by Dravidian University on behalf of APSCHE",
    eligibility="Indian national meeting AP local/non-local rules; at least 19 years old on 1 July 2026, no upper age limit. At least 50% in the bachelor's and/or master's degree (B.E./B.Tech with science and maths: 55%); SC, ST, BC and physically challenged candidates 40%. The teaching subject (methodology) depends on degree and Intermediate subjects: Mathematics, Physical Sciences, Biological Sciences, Social Studies, English",
    application_window="2026: registration from 11 Feb 2026 (APSCHE notification). 2027 notification not yet released as of 04 Oct 2026",
    exam_date="08 May 2026 (computer-based): Session 1 9:00-11:00 AM Mathematics, Biological Science, Physical Science; Session 2 12:30-2:30 PM Social Studies, English. (APSCHE's February notification had listed 04 May 2026.) 2027 date not yet announced",
    admits_into="2-year B.Ed in colleges of education in Andhra Pradesh for 2026-27",
    exam_pattern="Computer-based, 2 hours. Part A General English, Part B General Knowledge and Teaching Aptitude, Part C one methodology subject at degree level (Mathematics, Physical Sciences, Biological Sciences, Social Studies or English).",
)
subjects(AP, "AP EdCET", src, "2026-10-04", [
    ("Part A: General English", "Reading comprehension; correction of sentences, articles, prepositions, tenses, spelling; vocabulary, synonyms, antonyms; transformation of sentences, voice, direct and indirect speech"),
    ("Part B: General Knowledge and Teaching Aptitude", "Environment and society, current events and everyday science, India and its neighbours (history, culture, geography, ecology, economics, policy, research), and teaching aptitude: communication, dealing with children, individual differences, analytical thinking"),
    ("Part C: one methodology subject (degree level)", "Mathematics, Physical Sciences, Biological Sciences, Social Studies or English, from the B.A./B.Com./B.Sc. (CBCS) degree syllabus"),
])
cutoffs(AP, "AP EdCET", 2026, src, "2026-10-04", [
    ("General", "50% in the degree (B.E./B.Tech: 55%)", "Minimum to apply"),
    ("SC / ST / BC / physically challenged", "40% in the qualifying exam", "Minimum to apply"),
], kind="eligibility_marks")

# ---------- AP LAWCET 2026 ----------
src = "AP LAWCET & PGLCET-2026 Instruction Booklet V2 (Sri Padmavati Mahila Visvavidyalayam, Tirupati for APSCHE): cets.apsche.ap.gov.in/LAWCET/PDF/APLAWCET2026_IntructionsBooklet_V2.pdf"
verify(AP, "AP LAWCET", "2026-10-04", src,
    conducting_body="Sri Padmavati Mahila Visvavidyalayam, Tirupati (on behalf of APSCHE)",
    full_form_body="Andhra Pradesh Law Common Entrance Test for 3-year and 5-year LL.B. courses, conducted by Sri Padmavati Mahila Visvavidyalayam, Tirupati on behalf of APSCHE",
    eligibility="3-year LL.B.: a graduate degree (10+2+3) with 45% aggregate (42% BC, 40% SC/ST), or a PG degree with the same percentage. 5-year LL.B.: Intermediate (10+2) with 45% (42% BC, 40% SC/ST). 44.5%, 41.5% and 39.5% are treated as 45%, 42% and 40%",
    application_window="2026: notification 04 Feb 2026; applications 12 Feb - 20 Mar 2026 without late fee; late fee Rs 1,000 to 28 Mar, Rs 2,000 to 31 Mar, Rs 4,000 to 03 Apr, Rs 10,000 to 06 Apr 2026. 2027 notification not yet released as of 04 Oct 2026",
    exam_date="04 May 2026 (computer-based); preliminary key 07 May 2026. 2027 date not yet announced",
    admits_into="3-year and 5-year LL.B. in Andhra Pradesh universities and affiliated law colleges for 2026-27",
    exam_pattern="Computer-based, 90 minutes, 120 questions of 1 mark: Part A General Knowledge and Mental Ability 30, Part B Current Affairs 30, Part C Aptitude for the Study of Law 60.",
)
subjects(AP, "AP LAWCET", src, "2026-10-04", [
    ("Part A: General Knowledge and Mental Ability (30)", "General knowledge and mental ability"),
    ("Part B: Current Affairs (30)", "Current affairs"),
    ("Part C: Aptitude for the Study of Law (60)", "Elementary knowledge of the basic principles of law and the Constitution of India"),
])
cutoffs(AP, "AP LAWCET", 2026, src, "2026-10-04", [
    ("General / BC / EWS", "35% (42 of 120)", "Needed to be ranked"),
    ("SC / ST", "No minimum", None),
])
cutoffs(AP, "AP LAWCET", 2026, src, "2026-10-04", [
    ("General", "45% in the degree (3-year) or Intermediate (5-year)", "Minimum to apply"),
    ("BC", "42%", "Minimum to apply"),
    ("SC / ST", "40%", "Minimum to apply"),
], kind="eligibility_marks")

# ---------- AP PGECET 2026 ----------
src = "APPGECET-2026 Instruction Booklet V2 (Andhra University, Visakhapatnam for APSCHE): cets.apsche.ap.gov.in/PGECET/PDF/APPGECET2026_InstructionBooklet_V2.pdf; " + AP_CETS_SRC
verify(AP, "AP PGECET", "2026-10-04", src,
    conducting_body="Andhra University, Visakhapatnam (on behalf of APSCHE)",
    full_form_body="Andhra Pradesh Post Graduate Engineering Common Entrance Test for M.Tech, M.Pharmacy and Pharm.D (Post Baccalaureate), conducted by Andhra University on behalf of APSCHE",
    eligibility="Meets AP local/non-local rules; a relevant bachelor's degree with at least 50% (45% for reserved categories) from an AICTE/UGC-approved institution. GATE/GPAT-qualified candidates are admitted first; remaining seats go by PGECET rank",
    application_window="2026: notification 04 Feb 2026; applications 06 Feb - 20 Mar 2026 without late fee; late fee Rs 1,000 to 23 Mar, Rs 2,000 to 26 Mar, Rs 4,000 to 28 Mar, Rs 10,000 to 01 Apr 2026. 2027 notification not yet released as of 04 Oct 2026",
    exam_date="28-30 Apr 2026 (computer-based); preliminary key 06 May 2026. 2027 dates not yet announced",
    admits_into="M.Tech, M.Pharmacy and Pharm.D (PB) in Andhra Pradesh universities and colleges for 2026-27 (seats left after GATE/GPAT candidates)",
    exam_pattern="Computer-based, 120 multiple-choice questions for 120 marks in the chosen subject paper, English medium. No negative marking.",
)
cutoffs(AP, "AP PGECET", 2026, src, "2026-10-04", [
    ("General / BC / EWS", "25% (30 of 120)", "Needed to be ranked"),
    ("SC / ST", "No minimum", None),
])
cutoffs(AP, "AP PGECET", 2026, src, "2026-10-04", [
    ("General", "50% in the relevant bachelor's degree", "Minimum to apply"),
    ("Reserved categories", "45%", "Minimum to apply"),
], kind="eligibility_marks")

# ---------- AP PGCET 2026 ----------
src = "APPGCET-2026 General Instructions and Day-wise Examination Schedule (Sri Venkateswara University for APSCHE): cets.apsche.ap.gov.in/PGCET/PDF/; " + AP_CETS_SRC
verify(AP, "AP PGCET", "2026-10-04", src,
    eligibility="A bachelor's degree in the relevant subject (course-wise conditions on the APPGCET portal). Degrees done with a single subject in open/distance mode are not eligible for PG courses. Eligibility is checked only at admission",
    application_window="2026: registration from 09 Feb 2026 (APSCHE notification). 2027 notification not yet released as of 04 Oct 2026",
    exam_date="08-11 May 2026 (computer-based), subject-wise sessions per the day-wise schedule. 2027 dates not yet announced",
    admits_into="PG courses in campus, constituent and affiliated colleges of Sri Venkateswara, Andhra, Sri Krishnadevaraya, Acharya Nagarjuna, Sri Padmavathi Mahila, Yogi Vemana, Rayalaseema, Vikrama Simhapuri, Dravidian, Krishna, Adi Kavi Nannaya, Dr. B.R. Ambedkar, Dr. Abdul Haq Urdu and other participating universities, through web counselling",
    exam_pattern="Computer-based, 90 minutes, 100 multiple-choice questions of 1 mark in the chosen subject. M.P.Ed: 100-mark theory test on the B.P.Ed syllabus plus 100 marks for sports achievements (merit out of 200).",
)

# ---------- AP PECET 2026 ----------
src = "APPECET-2026 Instructions Booklet V2 (Acharya Nagarjuna University for APSCHE): cets.apsche.ap.gov.in/PECET/PDF/APPECET2026_InstructionsBooklet_V2.pdf"
verify(AP, "AP PECET", "2026-10-04", src,
    eligibility="B.P.Ed (2 years): appeared or passed a 3-year degree and at least 19 years old on 01.07.2026. D.P.Ed (2 years): appeared or passed Intermediate and at least 16 years old on 01.07.2026. Pass certificate needed at counselling",
    application_window="2026: applications from 13 Feb 2026; last date without late fee 30 Apr 2026, Rs 1,000 late fee to 15 May, Rs 2,000 to 25 May 2026. 2027 notification not yet released as of 04 Oct 2026",
    exam_date="Physical Efficiency and Games Skill Test from 03 to 08 Jun 2026 at 7:00 AM, at Acharya Nagarjuna University campus only; results about a week after the last test day. 2027 dates not yet announced",
    admits_into="First year of B.P.Ed (2 years) and D.P.Ed (2 years) in Andhra Pradesh",
    exam_pattern="No written paper. Physical Efficiency Test, 400 marks: men 100 m run, shot put (6 kg), 800 m run, long jump or high jump; women 100 m run, shot put (4 kg), 400 m run, long jump or high jump (100 marks each). Skill Test in one chosen game, 100 marks: ball badminton, basketball, cricket, football, handball, hockey, kabaddi, kho-kho, shuttle badminton, tennis or volleyball.",
)
cutoffs(AP, "AP PECET", 2026, src, "2026-10-04", [
    ("General / BC / EWS", "30% of 500 marks (150)", "Physical efficiency and skill test together, excluding incentive marks"),
    ("SC / ST", "No minimum", None),
])

# ---------- UPSC Civil Services Examination ----------
src = "UPSC Examination Notice No. 05/2026-CSE (04.02.2026): upsc.gov.in/sites/default/files/Notif-CSP-2026-Engl-060226Rev.pdf; UPSC Programme of Examinations 2027: upsc.gov.in/sites/default/files/Calendar-Year-2027-Engl-200526.pdf"
verify(AP, "UPSC Civil Services Examination", "2026-10-04", src,
    eligibility="A graduate degree from a recognised university (final-year students may apply). Age 21-32 on 1 August of the exam year (CSE 2026: born 2 Aug 1994 - 1 Aug 2005); upper age relaxed by 5 years for SC/ST, 3 for OBC, and for ex-servicemen and PwBD. Attempts: 6 for General/EWS, 9 for OBC and PwBD (General/EWS/OBC), unlimited for SC/ST",
    application_window="CSE 2026: notice 04 Feb 2026, last date 24 Feb 2026 (closed). CSE 2027: notification due 13 Jan 2027, last date 02 Feb 2027 (UPSC 2027 calendar)",
    exam_date="CSE 2026 Prelims held 24 May 2026; Mains 2026 in progress. CSE 2027 Prelims: 23 May 2027 (UPSC calendar)",
    admits_into="IAS, IPS, IFS (Foreign Service) and other Group A and B central civil services; about 933 vacancies in CSE 2026",
    exam_pattern="Three stages. Prelims (objective): GS Paper I 200 marks and GS Paper II (CSAT) 200 marks, 2 hours each; Paper II is qualifying at 33%, ranking by Paper I. Mains (written): qualifying papers in an Indian language and English (300 each), then Essay, GS I-IV and two optional-subject papers (250 each) = 1,750 marks. Personality Test (interview): 275 marks. Final merit out of 2,025.",
)
subjects(AP, "UPSC Civil Services Examination", src, "2026-10-04", [
    ("Prelims GS Paper I (200 marks)", "Current events; history of India and the national movement; Indian and world geography; Indian polity and governance; economic and social development; environment, biodiversity and climate change; general science"),
    ("Prelims GS Paper II / CSAT (200 marks, qualifying 33%)", "Comprehension; interpersonal and communication skills; logical reasoning and analytical ability; decision making and problem solving; general mental ability; basic numeracy and data interpretation (Class 10 level)"),
    ("Mains GS I (250)", "Indian heritage and culture, history and geography of the world and society"),
    ("Mains GS II (250)", "Governance, Constitution, polity, social justice and international relations"),
    ("Mains GS III (250)", "Technology, economic development, biodiversity, environment, security and disaster management"),
    ("Mains GS IV (250)", "Ethics, integrity and aptitude"),
    ("Mains Essay and optional subject (250 + 2 x 250)", "One essay paper and two papers in one optional subject chosen by the candidate"),
])
cutoffs(AP, "UPSC Civil Services Examination", 2026, src, "2026-10-04", [
    ("All categories", "33% in Prelims GS Paper II (CSAT)", "Qualifying only; Prelims merit is decided by GS Paper I"),
])

# ---------- SSC CGL 2026 ----------
src = "SSC Notice, Combined Graduate Level Examination 2026 (21.05.2026): ssc.gov.in/api/attachment/uploads/masterData/NoticeBoards/Notice_of_adv_cgl_2025.pdf; Important Notice on Tier-I schedule (12.09.2026): .../Important Notice 2026_cgle_2026_12092026.pdf"
verify(AP, "SSC CGL", "2026-10-04", src,
    eligibility="A bachelor's degree from a recognised university (some posts need specific subjects, e.g. Statistics); qualification as on 01.08.2026. Age as on 01.08.2026 depends on the post: 18-27, 20-30 or 18-32 years. Upper age relaxed by 5 years for SC/ST, 3 for OBC, 10 for PwBD (13 PwBD-OBC, 15 PwBD-SC/ST), and for ex-servicemen",
    application_window="CGL 2026: online applications 21 May - 22 Jun 2026 (reopened 23-25 Jun 2026); closed",
    exam_date="CGL 2026 Tier-I (computer-based): 30 Sep - 30 Oct 2026 (SSC notice of 12.09.2026). Tier-II tentatively December 2026",
    admits_into="Group B and Group C posts in central government ministries and departments (Assistant Section Officer, Inspector, Auditor, Accountant, Postal Assistant and others), pay levels 4-7",
    exam_pattern="Tier-I: 100 objective questions, 200 marks, 1 hour (15-minute timer per section): General Intelligence and Reasoning 25, General Awareness 25, Quantitative Aptitude 25, English Comprehension 25; 0.50 marks deducted per wrong answer. Tier-II: Paper I (compulsory) with Mathematical Abilities, Reasoning, English, General Awareness, Computer Knowledge Test and Data Entry Speed Test, 1 mark deducted per wrong answer; Paper II (Statistics) and Paper III (Finance and Economics) only for certain posts, 0.50 deducted per wrong answer.",
)
subjects(AP, "SSC CGL", src, "2026-10-04", [
    ("Tier-I: General Intelligence and Reasoning (25 questions, 50 marks)", "Verbal and non-verbal reasoning: analogies, classification, series, coding-decoding, space visualisation, Venn diagrams, syllogisms, statement-conclusion, paper folding, embedded figures, arithmetical reasoning"),
    ("Tier-I: General Awareness (25, 50 marks)", "Environment and society, current events, everyday science, India and its neighbours: history, culture, geography, economy, general policy and scientific research"),
    ("Tier-I: Quantitative Aptitude (25, 50 marks)", "Quantitative aptitude as per the notice syllabus"),
    ("Tier-I: English Comprehension (25, 50 marks)", "English comprehension"),
])
cutoffs(AP, "SSC CGL", 2026, src, "2026-10-04", [
    ("UR (General)", "30%", "Minimum in Tier-I and in each Tier-II section/paper"),
    ("OBC / EWS", "25%", None),
    ("All other categories (SC, ST, PwBD, ESM)", "20%", None),
])

# ---------- SSC CHSL 2026 ----------
src = "SSC Notice, Combined Higher Secondary (10+2) Level Examination 2026 (F. No. HQ-C1102/5/2026-C-1): ssc.gov.in/api/attachment/uploads/masterData/NoticeBoards/Notice_of_adv_chsle_2026.pdf"
verify(AP, "SSC CHSL", "2026-10-04", src,
    eligibility="Passed 12th standard (10+2) or equivalent; students appearing in Class 12 may also apply. Age 18-27 on 01.08.2026 (born 02.08.1999 - 01.08.2008); upper age relaxed by 5 years for SC/ST, 3 for OBC, 10 for PwBD and for ex-servicemen",
    application_window="CHSL 2026: online applications 07 Sep - 07 Oct 2026 (23:00 hrs); fee payment till 08 Oct 2026; correction window 14-16 Oct 2026. OPEN as of 04 Oct 2026",
    exam_date="Tier-I and Tier-II (computer-based) dates to be notified later",
    admits_into="Group C posts: Lower Divisional Clerk / Junior Secretariat Assistant and Data Entry Operators in central government ministries, departments and offices",
    exam_pattern="Tier-I: 100 objective questions, 200 marks, 60 minutes (15-minute timer per part): English Language 25, General Intelligence 25, Quantitative Aptitude (basic arithmetic) 25, General Awareness 25; 0.50 marks deducted per wrong answer; parts II-IV also in the language opted. Tier-II: four sections incl. skill/typing test, 1 mark deducted per wrong answer in sections I-III; all sections must be qualified.",
)
subjects(AP, "SSC CHSL", src, "2026-10-04", [
    ("Tier-I: English Language (25 questions, 50 marks)", "Spot the error, fill in the blanks, synonyms/homonyms, antonyms, spellings, idioms and phrases, one-word substitution, sentence improvement, active/passive voice, direct/indirect speech, sentence and paragraph shuffling, cloze passage, comprehension passage"),
    ("Tier-I: General Intelligence (25, 50 marks)", "Verbal and non-verbal: semantic, number and figural analogy, classification and series, symbolic operations, trends, space orientation, Venn diagrams, drawing inferences, paper folding, embedded figures, critical thinking, problem solving, emotional and social intelligence, word building, coding-decoding, numerical operations"),
    ("Tier-I: Quantitative Aptitude (25, 50 marks)", "Number systems; percentages, ratio and proportion, square roots, averages, simple and compound interest, profit and loss, discount, partnership, mixture and alligation, time and distance, time and work; basic algebra and graphs of linear equations; geometry of triangles and circles; mensuration of 2D and 3D figures; trigonometric ratios, heights and distances; histograms, frequency polygons, bar and pie charts"),
    ("Tier-I: General Awareness (25, 50 marks)", "Environment and society, current events, everyday science, India and its neighbours: history, culture, geography, economy, general policy and scientific research"),
])
cutoffs(AP, "SSC CHSL", 2026, src, "2026-10-04", [
    ("UR (General)", "30%", "Minimum in Tier-I and in sections I-III of Tier-II"),
    ("OBC / EWS", "25%", None),
    ("All other categories", "20%", None),
])

# ---------- SSC GD Constable 2026 (2027 cycle per SSC calendar) ----------
src = "SSC Notice, Constable (GD) in CAPFs, SSF and Rifleman (GD) in Assam Rifles Examination 2026 (01.12.2025): ssc.gov.in/api/attachment/uploads/masterData/NoticeBoards/notice_01122025.pdf; schedule notice 22.05.2026; SSC Tentative Calendar 2026-27 (ssc.gov.in/for-candidates/examination-calendar)"
verify(AP, "SSC GD Constable", "2026-10-04", src,
    eligibility="Indian citizen; passed Matriculation / Class 10 from a recognised board. Age 18-23 (GD 2026: on 01.01.2026, born 02.01.2003 - 01.01.2008); upper age relaxed by 5 years for SC/ST, 3 for OBC, and for ex-servicemen. Physical standards: height 170 cm (men), 157 cm (women), with relaxations for some categories; men's chest 80 cm unexpanded + 5 cm expansion",
    application_window="GD 2026: applications 01-31 Dec 2025 (closed). GD 2027: SSC calendar shows the notice in September 2026 and closing in October 2026; not yet published on the notice board as of 04 Oct 2026",
    exam_date="GD 2026 computer-based exam Feb-May 2026 (last date moved from 28 to 27 May 2026). GD 2027: January-March 2027 (SSC tentative calendar)",
    admits_into="Constable (GD) in BSF, CISF, CRPF, ITBP, SSB, SSF and Rifleman (GD) in Assam Rifles; CAPF vacancies are allotted state/UT-wise; 10% for ex-servicemen",
    exam_pattern="Stages: computer-based exam, Physical Efficiency Test, Physical Standard Test, medical and documents. CBE: 80 questions of 2 marks (160 marks), 60 minutes: General Intelligence and Reasoning 20, General Knowledge and Awareness 20, Elementary Mathematics 20, English/Hindi 20; 0.25 marks deducted per wrong answer; in English, Hindi and 13 regional languages incl. Telugu. PET race: men 5 km in 24 min, women 1.6 km in 8½ min (Ladakh region: 1.6 km in 7 min / 800 m in 5 min). NCC certificate holders get bonus marks.",
)
subjects(AP, "SSC GD Constable", src, "2026-10-04", [
    ("General Intelligence and Reasoning (20 questions, 40 marks)", "Analytical aptitude, patterns, analogies, similarities and differences, spatial visualisation and orientation, visual memory, arithmetical reasoning, figural classification, number and non-verbal series, coding and decoding"),
    ("General Knowledge and General Awareness (20, 40 marks)", "Current events, everyday science, India and its neighbours: sports, history, culture, geography, economy, polity, Indian Constitution, scientific research"),
    ("Elementary Mathematics (20, 40 marks)", "Number systems, whole numbers, decimals and fractions, arithmetic operations, percentages, ratio and proportion, averages, interest, profit and loss, discount, mensuration, time and distance, time and work"),
    ("English / Hindi (20, 40 marks)", "Basic understanding and comprehension of English or Hindi"),
])
cutoffs(AP, "SSC GD Constable", 2026, src, "2026-10-04", [
    ("UR (General)", "30%", "In the computer-based exam, to be shortlisted for PET/PST (NCC bonus not counted)"),
    ("OBC / EWS", "25%", None),
    ("All other categories", "20%", None),
])

# ---------- IBPS PO (CRP-PO/MT-XVI) ----------
src = "IBPS Detailed Notification CRP-PO/MTs-XVI (30.06.2026) and corrigenda: ibps.in/wp-content/uploads/Detailed-Notification_CRP-PO-XVI_Final_V1_30.06.2026.pdf (from ibps.in/index.php/management-trainees-xvi/)"
verify(AP, "IBPS PO", "2026-10-04", src,
    full_form_body="Common Recruitment Process for Probationary Officers / Management Trainees (CRP-PO/MT-XVI) in participating public sector banks, conducted by the Institute of Banking Personnel Selection, for 2027-28 vacancies",
    eligibility="A degree (graduation) in any discipline from a recognised university. Age 20-30 on 01.07.2026 (born 02.07.1996 - 01.07.2006); upper age relaxed by 5 years for SC/ST, 3 for OBC (non-creamy layer), 10 for PwBD, 5 for ex-servicemen",
    application_window="CRP-PO/MT-XVI: online registration 01-21 Jul 2026 (closed)",
    exam_date="Preliminary: August 2026; Main: October 2026; Personality Test November 2026; interviews November-December 2026 (tentative schedule in the notification)",
    admits_into="Probationary Officer / Management Trainee in participating public sector banks (provisional allotment by IBPS)",
    exam_pattern="Online Preliminary: 100 questions, 100 marks, 60 minutes (20 min each): English Language 30, Quantitative Aptitude 35, Reasoning Ability 35 questions; sectional cut-offs. Online Main: 170 objective questions, 200 marks, 160 minutes (Reasoning; General/Economy/Banking/Digital/Financial Awareness incl. RBI circulars; English Language; Data Analysis and Interpretation) plus a 25-mark descriptive paper (essay and comprehension, 30 min). One-fourth of a question's marks deducted per wrong answer. Then a non-qualifying Personality Test and a 100-mark interview; final merit Main:Interview = 80:20.",
)
cutoffs(AP, "IBPS PO", 2026, src, "2026-10-04", [
    ("General / EWS", "At least 40% in the interview", "Exam cut-offs are decided by IBPS after each stage"),
    ("SC / ST / OBC / PwBD", "At least 35% in the interview", None),
])

# ---------- IBPS Clerk (CRP-CSA-XVI) ----------
src = "IBPS Notification CRP-CSA-XVI (01.08.2026) and corrigendum 29.09.2026: ibps.in/wp-content/uploads/Notification_CRP_CSA_XVI-Final.pdf (from ibps.in/index.php/clerical-cadre-xvi/)"
verify(AP, "IBPS Clerk", "2026-10-04", src,
    full_form_body="Common Recruitment Process for Customer Service Associates (clerical cadre), CRP-CSA-XVI, in participating public sector banks, conducted by the Institute of Banking Personnel Selection",
    eligibility="A degree (graduation) in any discipline; must read, write, speak and understand the official language of the State/UT applied for (Local Language Proficiency Test). Apply for one State/UT only. Age 20-28 on 01.08.2026 (born 02.08.1998 - 01.08.2006), with the usual SC/ST/OBC/PwBD/ex-servicemen relaxations",
    application_window="CRP-CSA-XVI: online registration 01-21 Aug 2026 (closed)",
    exam_date="Preliminary: October 2026 (call letters out); Main: November 2026; provisional allotment March 2027 (tentative)",
    admits_into="Customer Service Associate (clerk) in participating public sector banks in the State/UT applied for",
    exam_pattern="Online Preliminary: 100 questions, 100 marks, 60 minutes (20 min each): English 30, Numerical Ability 35, Reasoning 35; sectional cut-offs. Online Main: 160 questions, 200 marks, 125 minutes: General/Financial Awareness 40 (50 marks, 20 min), General English 40 (40 marks, 35 min), Reasoning Ability 40 (60 marks, 35 min), Quantitative Aptitude 40 (50 marks, 35 min). Most tests are offered in English, Hindi and a language of the State applied for (Telugu for Andhra Pradesh). No interview.",
)

# =====================================================================
# Batch 3 (2026-10-04): remaining catalogue exams.
# =====================================================================

# ---------- VITEEE 2026 ----------
src = "VITEEE 2026 Prospectus (Vellore Institute of Technology): vit.ac.in/files/VITEEE/VITEEE_Prospectus.pdf (linked from viteee.vit.ac.in)"
verify(AP, "VITEEE", "2026-10-04", src,
    eligibility="Passed or appearing in Class 12 (2026) with at least 60% aggregate in Physics, Chemistry and Mathematics and at least 50% in Mathematics (or 60% in Physics, Chemistry and Biology with 50% in Biology for some programmes); 50% for SC/ST and candidates from J&K, Ladakh and the North-Eastern states. Only students from regular full-time schooling with English as a subject are eligible; one attempt per year",
    application_window="VITEEE 2026: applications online at viteee.vit.ac.in (closed); slot booking opened in the second week of April 2026. VITEEE 2027 prospectus not yet released as of 04 Oct 2026",
    exam_date="VITEEE 2026: 28 Apr - 03 May 2026 (computer-based, booked slots). 2027 dates not yet announced",
    admits_into="B.Tech programmes at VIT Vellore, VIT Chennai, VIT-AP (Amaravati) and VIT Bhopal, through online counselling by VITEEE rank",
    exam_pattern="Computer-based, 2 hours 30 minutes, 125 multiple-choice questions in English: Mathematics or Biology 40, Physics 35, Chemistry 35, English 5, Aptitude 10. +4 per correct answer, -1 per wrong answer.",
)
subjects(AP, "VITEEE", src, "2026-10-04", [
    ("Mathematics or Biology (40 questions)", "Class 11-12 level; Biology route only for the biology-related B.Tech programmes"),
    ("Physics (35)", "Class 11-12 level"),
    ("Chemistry (35)", "Class 11-12 level"),
    ("English (5) and Aptitude (10)", "English usage and general aptitude"),
])
cutoffs(AP, "VITEEE", 2026, src, "2026-10-04", [
    ("General", "60% in PCM (or PCB) with 50% in Maths (or Biology)", "Minimum Class 12 marks to apply"),
    ("SC / ST; J&K, Ladakh and North-East", "50% in PCM/PCB", "Minimum Class 12 marks to apply"),
], kind="eligibility_marks")

# ---------- SRMJEEE (UG) 2026 ----------
src = "SRMJEEE (UG) 2026 Examination Pattern (SRM Institute of Science and Technology): webstor.srmist.edu.in/web_assets/downloads/2026/srmjeee-examination-pattern.pdf"
verify(AP, "SRMJEEE", "2026-10-04", src,
    admits_into="B.Tech at SRM Institute of Science and Technology campuses (B.Arch is through NATA)",
    exam_pattern="130 questions, 130 marks, 2 hours 30 minutes: Physics 35, Chemistry 35, Mathematics or Biology 40, English and Aptitude 20. No negative marking.",
)

# ---------- KLEEE 2026 ----------
src = "KL University (Koneru Lakshmaiah Education Foundation) UG application page, KLEEE-2026 Important Dates: kluniversity.in/howto1.aspx (checked 04 Oct 2026)"
verify(AP, "KLEEE", "2026-10-04", src,
    application_window="KLEEE 2026 Phase I: last date 12 Nov 2025, admit cards 13 Nov 2025. Phases II and III shown as 'yet to be announced' on the official page as of 04 Oct 2026",
    exam_date="KLEEE 2026 Phase I: 14-18 Nov 2025. KL also holds KLSAT (science), KLMAT (management), KLECET (lateral entry) and KLHAT (humanities) on the same dates",
    admits_into="B.Tech and other UG programmes at KL University (Vaddeswaram, Vijayawada and other KLEF campuses)",
)

# ---------- GITAM GAT ----------
src = "GITAM (Deemed to be University) admissions FAQs: gitam.edu/admissions/faqs (checked 04 Oct 2026); applications at apply.gitam.edu"
verify(AP, "GITAM GAT", "2026-10-04", src,
    eligibility="All students joining GITAM must take GAT (GITAM Admission Test), held every year",
    application_window="Online at apply.gitam.edu",
    admits_into="UG and PG programmes at GITAM's Visakhapatnam, Hyderabad and Bengaluru campuses; GAT rank also decides merit scholarships",
    exam_pattern="Computer-based test taken at centres across India.",
)

# ---------- NCHM JEE 2026 ----------
src = "NCHM JEE-2026 Information Bulletin (NTA for NCHMCT): cdnbbsr.s3waas.gov.in/s388a839f2f6f1427879fc33ee4acf4f66/uploads/2025/12/20260102470139941.pdf (from exams.nta.nic.in/NCHM/)"
verify(AP, "NCHM JEE", "2026-10-04", src,
    eligibility="Passed or appearing in 10+2 (or equivalent) with English as a subject; no age limit (NEP). Physical fitness certificate needed at admission",
    application_window="NCHM JEE 2026: online 26 Dec 2025 - 25 Jan 2026 (closed); fee Rs 1,000 (General/OBC-NCL), Rs 700 (EWS), Rs 450 (SC/ST/PwD/Third Gender). 2027 bulletin not yet released as of 04 Oct 2026",
    exam_date="NCHM JEE 2026 held 25 Apr 2026, 11:00 AM - 1:00 PM (computer-based). 2027 date not yet announced",
    admits_into="B.Sc Hospitality and Hotel Administration at NCHMCT-affiliated Institutes of Hotel Management (central, state, PSU, PPP and private)",
    exam_pattern="Computer-based, 2 hours, 120 multiple-choice questions in English or Hindi across Numerical Ability and Analytical Aptitude, Reasoning and Logical Deduction, General Knowledge and Current Affairs, English Language, and Aptitude for Service Sector. +4 per correct answer, -1 per wrong answer.",
)

# ---------- UCEED 2027 ----------
src = "UCEED 2027 Information Brochure (IIT Bombay, released 01 Oct 2026): uceed.iitb.ac.in/2027/assets/downloads/docs/UCEED2027_Information_Brochure.pdf"
verify(AP, "UCEED", "2026-10-04", src,
    eligibility="Passed Class 12 (or equivalent) in 2026 or appearing in 2027, in ANY stream (Science, Commerce or Arts & Humanities). Born on or after 1 Oct 2002 (OPEN/EWS/OBC-NCL) or 1 Oct 1997 (SC/ST/PwD). At most two attempts, in consecutive years",
    application_window="UCEED 2027: online registration 01-31 Oct 2026 (OPEN as of 04 Oct 2026); with Rs 500 late fee to 06 Nov 2026 (5 pm). Fee Rs 2,000 for women and SC/ST/PwD, Rs 4,000 for others",
    exam_date="17 Jan 2027 (Sunday), 9:00 AM - 12:00 noon. Admit cards from 01 Jan 2027; results 06 Mar 2027; B.Des applications from 15 Mar 2027",
    admits_into="B.Des at IIT Bombay, IIT Delhi, IIT Guwahati, IIT Hyderabad, IIT Indore, IIT Roorkee and IIITDM Jabalpur (apply separately after qualifying); many other design schools accept UCEED scores",
    exam_pattern="One 3-hour paper, 300 marks, English only. Part A (computer-based, 200 marks, 2 hours): 14 numerical-answer questions (4 marks, no negative), 15 multiple-select questions (up to 4 marks with partial marks, -1 if wrong), 28 multiple-choice questions (3 marks, -0.71 if wrong). Part B (100 marks, 1 hour): two drawing / design aptitude questions answered on paper. Part B is marked only for candidates shortlisted on Part A; rank by Part A + Part B.",
)
cutoffs(AP, "UCEED", 2027, src, "2026-10-04", [
    ("OPEN", "Part A: mean + 2 x standard deviation of all Part A marks; Part B: 15 of 100", "Top 6,400 on Part A are shortlisted if more than that clear the Part A mark"),
    ("OBC-NCL / EWS", "Part A: 0.9 x the OPEN mark; Part B: 13.5", None),
    ("SC / ST / PwD", "Part A: 0.5 x the OPEN mark; Part B: 7.5", None),
])

# ---------- NID DAT 2027 ----------
src = "NID Admissions 2027-28 portal, Important Updates: admissions.nid.edu/NIDA2027/Default.aspx (checked 04 Oct 2026); B.Des admissions handbook 2027-28 listed there"
verify(AP, "NID DAT", "2026-10-04", src,
    application_window="NID 2027-28: online applications for the 5.5-year Professional Education Master of Design (Integrated Pathway) / B.Des at NID Ahmedabad, Gandhinagar and Bengaluru close 11:59 pm, 30 Nov 2026 (OPEN as of 04 Oct 2026). Also B.Des at other NIDs via their campus links",
    exam_date="Design Aptitude Test dates for 2027 to be announced on admissions.nid.edu",
    admits_into="B.Des / 5.5-year integrated design programme at the National Institutes of Design",
)

# ---------- IPMAT (IIM Indore) 2026 ----------
src = "IIM Indore, FAQs on the Integrated Programme in Management (IPM 2026-31): iimidr.ac.in/wp-content/uploads/2026/01/FAQs-IPM.pdf"
verify(AP, "IPMAT", "2026-10-04", src,
    full_form_body="IPM Aptitude Test of IIM Indore for its 5-year Integrated Programme in Management (BA Foundations of Management + MBA dual degree)",
    eligibility="Eligibility for domestic and international applicants is published on iimidr.ac.in (IPM admissions details); students from IGCSE and IB schools can also apply",
    application_window="IPM 2026-31 batch: notification 02 Feb 2026, online applications 02 Feb - 14 Mar 2026 (closed). 2027 schedule not yet announced as of 04 Oct 2026",
    exam_date="IPM Aptitude Test 2026: 04 May 2026 (afternoon); shortlist 25 May, personal interviews 15-18 Jun, offers 26 Jun 2026",
    admits_into="5-year IPM at IIM Indore (exit with a BA after 3 years possible); course fee Rs 6 lakh a year for the first three years for domestic students",
    exam_pattern="Aptitude test, then personal interview for shortlisted candidates.",
)

# ---------- GATE 2027 ----------
src = "GATE 2027 official website (IIT Madras, organising institute): gate2027.iitm.ac.in - Important Dates, Eligibility Criteria, Question Paper Pattern (checked 04 Oct 2026)"
verify(AP, "GATE", "2026-10-04", src,
    conducting_body="IISc and the IITs for the National Coordination Board, Ministry of Education; organised in 2027 by IIT Madras",
    official_website="gate2027.iitm.ac.in",
    eligibility="Students in the 3rd or higher year of any undergraduate degree, or graduates of any government-approved degree in Engineering, Technology, Architecture, Science, Commerce, Arts or Humanities; also holders of approved professional-society qualifications (IE, IETE, AeSI and others). No age limit stated. Registration through a verified DigiLocker account is mandatory for Indian nationals",
    application_window="GATE 2027: registration opened 02 Sep 2026; regular registration extended to 05 Oct 2026; with late fee to 12 Oct 2026 (OPEN as of 04 Oct 2026); application corrections 14-21 Oct 2026",
    exam_date="06, 07, 13, 14, 20 and 21 Feb 2027 (computer-based). Exam cities announced 04 Jan 2027; results 19 Mar 2027",
    admits_into="M.Tech/M.E./direct PhD admissions with possible financial assistance at MoE-supported institutions; many PSUs recruit through GATE scores. Score valid for 3 years",
    exam_pattern="Computer-based, 3 hours, English, 65 questions for 100 marks: General Aptitude 10 questions (15 marks) + 55 subject questions (85 marks, including 13 marks of Engineering Mathematics in most engineering papers). MCQ, multiple-select and numerical-answer questions of 1 or 2 marks; 1/3 or 2/3 mark deducted for a wrong MCQ, no negative marking for MSQ/NAT. 30 test papers (new: Robotics and Automation); up to two papers allowed.",
)

# ---------- IOQM 2026 (Mathematical Olympiad stage 1) ----------
src = "IOQM 2026-27 official portal (MTA(I) with HBCSE): ioqm.mtai.org.in (timelines, FAQs); HBCSE Mathematical Olympiad 2026-2027 page: olympiads.hbcse.tifr.res.in/mathematical-olympiad-2026-2027/"
verify(AP, "IOQM (Mathematics Olympiad)", "2026-10-04", src,
    official_website="ioqm.mtai.org.in",
    eligibility="Born between 1 Aug 2007 and 31 Jul 2014 and studying in Class 8, 9, 10, 11 or 12. Students who have already passed the Class 12 board exam are not eligible (even in a gap year)",
    application_window="IOQM 2026: enrolment through a registered school/centre 01 Jun - 27 Jul 2026, fee Rs 180 (KV/JNV) or Rs 300 (others) (closed)",
    exam_date="IOQM 2026 held 06 Sep 2026. Next stages: RMO 15 Nov 2026 (1-4 pm, 6 proof questions, 3 hours); INMO 17 Jan 2027 (12-4:30 pm, 6 proof questions, 4.5 hours)",
    admits_into="Stage 1 of the Mathematical Olympiad programme: IOQM -> RMO -> INMO -> IMO training camp -> International Mathematical Olympiad",
    exam_pattern="Offline, OMR answer sheet, no negative marking.",
)

# ---------- NSEJS 2026 (Junior Science Olympiad stage 1) ----------
src = "IAPT NSE 2026 Students' Brochure: iapt.org.in/wp-content/uploads/NSE-2026-Student-Brochure.pdf"
verify(AP, "NSEJS (Junior Science Olympiad)", "2026-10-04", src,
    eligibility="Indian passport-eligible; born between 1 Jan 2012 and 31 Dec 2013; living and studying in India (or in the Indian school system) since 30 Nov 2024; must not have completed the Class 10 board exam before 30 Nov 2026; must not write NSEA/NSEB/NSEC/NSEP 2026",
    application_window="Registration through an NSE centre (school) on iapt.manageexam.com",
    exam_date="Sunday 22 Nov 2026, 2:30-4:30 PM, at the registered NSE centre",
    admits_into="Stage 1 of the Junior Science Olympiad: selected students go to INJSO (stage 2) and onward to the International Junior Science Olympiad",
    exam_pattern="2 hours, 216 marks: 48 multiple-choice questions (+3, -1) and 12 questions with one or more correct options (6 marks, all correct options needed). Class 10 CBSE level, Biology, Chemistry and Physics with equal emphasis. Paper in English, Hindi, Gujarati, Bangla, Kannada, Tamil and Telugu.",
)
cutoffs(AP, "NSEJS (Junior Science Olympiad)", 2026, src, "2026-10-04", [
    ("Minimum Admissible Score (all)", "50% of the average of the top ten scores", "Needed to be considered for stage 2"),
    ("Merit Index (all)", "80% of the average of the top ten scores", "Scoring at or above it qualifies directly for stage 2"),
], kind="cutoff_score")

# ---------- AP Police Constable & SI 2026 ----------
src = "SLPRB AP Notifications Rc.No.91/SLPRB/Rect.2/2026 (Police Constables) and Rc.No.81/SLPRB/Rect.1/2026 (Sub-Inspectors), 16.09.2026, and Press Note 16.09.2026: slprb.ap.gov.in/2026_PDFS/"
verify(AP, "AP Police Constable & SI", "2026-10-04", src,
    eligibility="Constable (Civil, AR): Intermediate passed by 01.07.2026; age 18-24 on 01.07.2026 (Firemen and Warders 18-32; serving AP Home Guards 18-32). Sub-Inspector (Civil, AR, SPF): a degree by 01.07.2026; age 21-27 on 01.07.2026. Upper age relaxed for BC, SC, ST and others as per the notification. Physical standards (men): height 167.6 cm and chest 86.3 cm with 5 cm expansion; women: height 152.5 cm, weight 40 kg (lower standards for Aboriginal STs of agency areas)",
    application_window="2026 notifications issued 16 Sep 2026; online application and preliminary test dates to be announced by press release on slprb.ap.gov.in (not yet announced as of 04 Oct 2026)",
    exam_date="Preliminary written test dates to be announced",
    admits_into="2026 vacancies: SI (Civil) 253, RSI (AR) 116, SI (SPF) 9, SI (Communications) 50, SI (PTO) 10; Police Constables (Civil) 542, (AR) 285, Communications 200, PTO drivers/mechanics 213; Firemen 158; Warders 171; Scientific Assistants (FSL) 43",
    exam_pattern="Constable: preliminary written test (3 hours, 200 objective questions, 200 marks) -> physical measurements -> physical efficiency (1600 m run in 8 min for men / 10 min 30 s for women, plus 100 m run or long jump) -> final written test (200 marks). SI: preliminary test of two papers (Arithmetic & Reasoning, SSC standard; General Studies, degree standard; 100 marks each) -> physical tests -> final written exam of four papers (English and Telugu/Urdu descriptive, Arithmetic & Reasoning, General Studies).",
)
cutoffs(AP, "AP Police Constable & SI", 2026, src, "2026-10-04", [
    ("OC (including EWS)", "40%", "In the preliminary test (each paper for SI) and in the final written exam"),
    ("BC", "35%", None),
    ("SC / ST", "30%", None),
])

# ---------- TGPSC Group 1 (latest: Notification 02/2024) ----------
src = "TGPSC Notification No. 02/2024, Group-I Services (from websitenew.tgpsc.gov.in/notifications); no newer Group-I notification listed as of 04 Oct 2026"
verify(TS, "TGPSC Group 1", "2026-10-04", src,
    official_website="websitenew.tgpsc.gov.in",
    eligibility="A bachelor's degree (some posts need specific degrees). 2024 cycle: age 18-46 on 01.07.2024 for most posts (21 minimum for some; uniformed posts have their own limits and physical standards); upper age relaxed for SC/ST/BC and others",
    application_window="Latest notification 02/2024 (563 posts). No new Group-I notification published as of 04 Oct 2026",
    exam_date="2024 cycle: Prelims May/June 2024, Mains September/October 2024. Next cycle not yet announced",
    admits_into="Telangana Group-I posts such as Deputy Collector, DSP, Commercial Tax Officer, District Registrar, Assistant Accounts Officer and others",
    exam_pattern="Preliminary test: General Studies & Mental Ability, 150 objective questions, 150 marks, 2½ hours (screening; 1:50 shortlisted for Mains). Main (descriptive, 3 hours each): General English (qualifying) plus six papers of 150 marks: General Essay; History, Culture and Geography; Indian Society, Constitution and Governance; Economy and Development; Science, Technology and Data Interpretation; Telangana Movement and State Formation.",
)

# ---------- TGPSC Group 4 (latest: Notification 19/2022) ----------
src = "TGPSC Notification No. 19/2022, Group-IV Services, Annexure-III scheme and syllabus (from websitenew.tgpsc.gov.in/notifications); no newer Group-IV notification listed as of 04 Oct 2026"
verify(TS, "TGPSC Group 4", "2026-10-04", src,
    official_website="websitenew.tgpsc.gov.in",
    eligibility="Junior Assistant and similar posts: a bachelor's degree (some posts need B.Com or specific marks); age 18-44 on 01.07.2022 in the 2022 cycle, with relaxations",
    application_window="Latest notification 19/2022. No new Group-IV notification published as of 04 Oct 2026",
    exam_date="Next cycle not yet announced",
    admits_into="Junior Assistant, Junior Accountant, Ward Officer, Typist and similar posts across Telangana government departments",
    exam_pattern="Two objective papers, 150 questions and 150 minutes each, 300 marks: Paper I General Studies (current affairs, international relations, everyday science, environment and disaster management, geography and economy of India and Telangana, Indian Constitution, Telangana history and movement and more); Paper II Secretarial Abilities. In English, Telugu and Urdu.",
)

# ---------- APPSC Group 1 (Notification 07/2026) ----------
src = "APPSC Brief Notification No. 07/2026 (15/09/2026), Group-I Services: psc.ap.gov.in/Documents/NotificationDocuments/Group_I_072026.pdf (from portal-psc.ap.gov.in Recruitment Notifications)"
verify(AP, "APPSC Group 1", "2026-10-04", src,
    eligibility="A bachelor's degree from a recognised university (B.E./B.Tech in ECE/Telecom/Radio Engineering for one post; physical standards for police posts). Age limits and community details are in the detailed notification, due on psc.ap.gov.in on or before 06 Oct 2026",
    application_window="Online at psc.ap.gov.in from 06 Oct to 27 Oct 2026 (11:59 PM); One Time Profile Registration (OTPR) needed first",
    exam_date="Screening test (offline, OMR) date to be announced",
    admits_into="Group-I posts such as Deputy Collector, Assistant Commissioner of State Tax, Deputy Superintendent of Police, Accounts Officer (Treasury), District Employment Officer, Assistant Audit Officer and Divisional Development Officer",
    exam_pattern="Screening test (objective, degree standard; 1/3 mark deducted per wrong answer): Paper I General Studies (120 questions, 120 marks, 120 minutes: history and culture; constitution, polity, social justice and international relations; Indian and AP economy and planning; geography) and Paper II General Aptitude (120 questions, 120 marks: mental ability, administrative and psychological abilities; science and technology; current events). Mains (descriptive, 3 hours each): Telugu and English papers (qualifying, 150 each) plus five papers of 150 marks: General Essay; History, Culture and Geography of India and AP; Polity, Constitution, Governance, Law and Ethics; Economy and Development of India and AP; Science, Technology and Environment. Interview 75 marks. Total 825.",
)

# ---------- NMMS 2026 (Andhra Pradesh) ----------
src = "Directorate of Government Examinations AP, Notification Rc.No.208/NMMSS/2026 dated 10/09/2026: bse.ap.gov.in/NMMS/Notification_NMMS_2026.PDF (from bse.ap.gov.in/NMMS.aspx)"
verify(AP, "NMMS (Andhra Pradesh)", "2026-10-04", src,
    eligibility="Class VIII students in 2026-27 at Government, Local Body (ZP/Municipal), Government-aided, AP Model (day scholars only) or MPUP schools; at least 55% (OC/BC) or 50% (SC/ST) in Class VII (2025-26), or B+ grade; parents' combined annual income below Rs 3,50,000 (MRO income certificate needed)",
    application_window="Online through the school headmaster on bse.ap.gov.in from 11 Sep 2026; last date for upload by HM 12 Oct 2026, fee payment by 13 Oct 2026 (OPEN as of 04 Oct 2026). Fee Rs 100 (OC/BC), Rs 50 (SC/ST) via SBI Collect",
    exam_date="15 Nov 2026 (Sunday), 10:00 AM - 1:00 PM, at revenue division headquarters in all 28 districts; in Telugu, English or Urdu",
    admits_into="National Means-cum-Merit Scholarship (central scheme) for students who qualify, to continue studies from Class IX",
)
subjects(AP, "NMMS (Andhra Pradesh)", src, "2026-10-04", [
    ("Syllabus", "Class VII (2025-26) course and Class VIII (2026-27) course up to October"),
])
cutoffs(AP, "NMMS (Andhra Pradesh)", 2026, src, "2026-10-04", [
    ("OC / BC", "55% in Class VII (or B+)", "Minimum to apply"),
    ("SC / ST", "50% in Class VII (or B+)", "Minimum to apply"),
], kind="eligibility_marks")

# ---------- APRJC CET 2026-27 ----------
src = "APREIS APRJC CET Prospectus 2026-27: aprs.apcfss.in/APRJC_CET_Prospectus_2026_27.pdf"
verify(AP, "APRJC CET", "2026-10-04", src,
    eligibility="Resident of India who studied in Andhra Pradesh, and passed SSC or equivalent in 2025-26 (not compartmental)",
    application_window="2026-27: notification 16 Feb 2026; online applications 18 Feb - 31 Mar 2026 (closed). 2027-28 prospectus not yet released as of 04 Oct 2026",
    exam_date="24 Apr 2026 at the 28 district headquarters; group-wise counselling 20-22 May 2026",
    admits_into="Intermediate (English medium, residential) at AP Residential Junior Colleges in MPC, BPC, MEC, CEC, EET and CGT groups, with long-term coaching for IIT/NEET/CA",
    exam_pattern="Pen and paper (OMR), 2 hours 30 minutes, 150 marks of Class 10 standard multiple-choice questions, three subjects of 50 marks by group: MPC/EET - English, Mathematics, Physical Science; BPC/CGT - English, Physical Science, Biological Science; MEC/CEC - English, Mathematics, Social Studies. Papers in English & Telugu or English & Urdu.",
)
cutoffs(AP, "APRJC CET", 2026, src, "2026-10-04", [
    ("OC", "38% of seats", "General colleges"),
    ("BC-A / BC-B / BC-C / BC-D / BC-E", "7% / 10% / 1% / 7% / 4%", None),
    ("SC Group-I / II / III", "1% / 6.5% / 7.5%", None),
    ("ST", "6%", None),
    ("Special categories", "PHC 3%, Sports 3%, Children of Armed Personnel 3%, Orphans 3%", None),
    ("Minority colleges", "Minority 73%; SC and ST as above", None),
], kind="seat_reservation")

# ---------- APRS CAT 2026-27 ----------
src = "APREIS APRS CAT Prospectus 2026-27 (in Telugu), sections 5-6 and 11: aprs.apcfss.in/APRS_CAT_Prospectus_2026_27.pdf"
verify(AP, "APRS CAT (AP Residential Schools)", "2026-10-04", src,
    eligibility="Parents' annual income (2025-26) not above Rs 2,50,000, or a white ration card (income limit does not apply to children of soldiers); age limits by class and category as listed in the prospectus. Minority-category seats in minority schools are also filled through the CAT",
    application_window="2026-27: notification 16 Feb 2026; online applications 18 Feb - 31 Mar 2026 on aprs.apcfss.in, fee Rs 100 (closed). Phase-II selection lists released. 2027-28 prospectus not yet released as of 04 Oct 2026",
    exam_date="24 Apr 2026, 10:00 AM - 12:00 noon, at district centres; results and first selection list 15 May 2026",
    admits_into="Class 5 and vacant seats in Classes 6, 7 and 8 of AP Residential Schools (general and minority)",
)

# ---------- TGRJC CET 2026 ----------
src = "TGREIS TGRJC-CET 2026 Prospectus (from tgrjc.cgg.gov.in/TGRJCWEB/)"
verify(TS, "TGRJC CET", "2026-10-04", src,
    eligibility="Resident of India who studied the previous classes in Telangana; passed Class 10 at the FIRST attempt in March 2026 (earlier pass-outs not eligible); SSC GPA at least 6 (Open category) or 5 (BC, SC, ST, minority), and GPA 4 in English for all",
    application_window="2026: online applications 16 Mar - 15 Apr 2026, fee Rs 200 (closed). 2027 notification not yet released as of 04 Oct 2026",
    exam_date="03 May 2026, 10:00 AM - 12:30 PM, at any chosen centre",
    admits_into="First-year Intermediate (MPC, BPC, MEC) in 35 Telangana Residential Junior Colleges for 2026-27",
    exam_pattern="Objective (OMR), 2½ hours, 150 marks (50 per subject), Telangana Class 10 syllabus, bilingual Telugu/English: MPC - English, Mathematics, Physical Science; BPC - English, Biological Science, Physical Science; MEC - English, Social Studies, Mathematics.",
)
cutoffs(TS, "TGRJC CET", 2026, src, "2026-10-04", [
    ("Open category", "SSC GPA 6 and English GPA 4", "Minimum to apply"),
    ("BC / SC / ST / minority", "SSC GPA 5 and English GPA 4", "Minimum to apply"),
], kind="eligibility_marks")

# ---------- TGCET 2026 (Telangana Gurukulam) ----------
src = "TGCET-2026 Prospectus for admission into residential institutions 2026-27 (TGSWREIS, TGTWREIS, MJPTBCWREIS, TREIS), from tgcet.cgg.gov.in/TGCETWEB/"
verify(TS, "TGCET (Telangana Gurukulam Class 5)", "2026-10-04", src,
    full_form_body="Telangana Gurukulam Common Entrance Test for Class 5 in four residential school societies and Classes 6-9 (vacant seats) in three societies",
    eligibility="Studying Class IV (for Class V) or Classes V-VIII for the full year 2025-26 in the same erstwhile district; parents' annual income below Rs 1,50,000 (rural) or Rs 2,00,000 (urban). Age on 31.08.2026 for Class V: born 01.09.2015-31.08.2017 (BC, minority, others) or 01.09.2013-31.08.2017 (SC/ST); two more years allowed per higher class",
    application_window="2026: online applications 11 Dec 2025 - 21 Jan 2026 (closed). 2027 notification not yet released as of 04 Oct 2026",
    exam_date="22 Feb 2026 (Sunday), 11:00 AM - 1:00 PM",
    admits_into="Class V (and vacant seats in VI-IX) in Telangana Social Welfare, Tribal Welfare, MJP BC Welfare and general residential (Gurukulam) schools; admission by erstwhile district, merit and reservation",
    exam_pattern="2 hours, 100 objective questions, 100 marks, no negative marking, Telugu and English. Class V: Telugu 20, English 25, Maths 25, EVS 20, Mental Ability 10. Class VI: Telugu 20, English 20, Maths 25, EVS 25, GK & current affairs 10. Class VII: English 20, Maths 25, Science 25, Social 20, GK 10. Classes VIII-IX: English 20, Maths 25, Physical Science 13, Biological Science 12, Social 20, GK 10.",
)

# ---------- AP Model Schools Class 6 test 2026 ----------
src = "Director of School Education AP, Proceedings Rc.No.ESE02-34/2/2022-AD-APMS dt 09-06-2026 (leftover seats): apms.apcfss.in/pdfs/leftover.pdf; apms.apcfss.in home page (checked 04 Oct 2026)"
verify(AP, "AP Model Schools Admission Test (Class 6)", "2026-10-04", src,
    application_window="2026-27: Class VI entrance test applications closed; leftover seats in Classes VI-IX and Intermediate opened online from 10 Jun 2026 (now closed)",
    exam_date="Class VI entrance test 2026 held (spring 2026); 2027 dates not yet announced",
    admits_into="Class VI in AP Model Schools (English medium); merit list from the entrance test, then leftover seats filled giving preference to local candidates, irrespective of cut-off marks",
)

# ---------- TS Model Schools 2026 ----------
src = "Telangana Model Schools admission portal: telanganams.cgg.gov.in (Notification - TGMS VI CLASS - 2026 and VII to X CLASS - 2026; checked 04 Oct 2026)"
verify(TS, "TS Model Schools Entrance (Class 6)", "2026-10-04", src,
    official_website="telanganams.cgg.gov.in",
    application_window="2026: Class VI applications and payment 28 Jan - 11 Mar 2026; Classes VII-X 28 Jan - 10 Mar 2026 (closed)",
    exam_date="19 Apr 2026: Class VI 10:00 AM - 12:00 noon; Classes VII-X 2:00-4:00 PM",
    admits_into="Class VI (and vacant seats in VII-X) in Telangana Model Schools",
)

# ---------- BITSAT 2026 ----------
src = "BITSAT-2026 Brochure (BITS Pilani): admissions.bits-pilani.ac.in/FD/downloads/BITSAT-2026_Brochure.pdf; timeline from bitsadmission.com/BITSAT_LP/index.html"
verify(AP, "BITSAT", "2026-10-04", src,
    eligibility="Passed Class 12 (2026 or appearing) with Physics, Chemistry, Mathematics (or Biology for B.Pharm, Environmental & Sustainability Engg., M.Sc. Biological Sciences), English and five subjects in all; at least 75% aggregate in PCM/PCB AND at least 60% in each of the three (74.9% is not rounded up). State/CBSE board toppers get direct admission",
    application_window="BITSAT 2026: Session 1 applications to 19 Mar 2026; Session 2 registration 20 Apr - 05 May 2026 (closed). 2027 not yet announced as of 04 Oct 2026",
    exam_date="BITSAT 2026: Session 1 15-16 Apr 2026; Session 2 24-26 May 2026 (computer-based)",
    admits_into="B.E., B.Pharm and M.Sc. (integrated first degree) at BITS Pilani campuses: Pilani, K K Birla Goa and Hyderabad",
    exam_pattern="Computer-based, 3 hours, 130 multiple-choice questions: Physics 30, Chemistry 30, English Proficiency 10, Logical Reasoning 20, Mathematics or Biology 40. +3 per correct answer, -1 per wrong answer. Candidates who answer all 130 may attempt 12 extra questions.",
)
cutoffs(AP, "BITSAT", 2026, src, "2026-10-04", [
    ("All candidates", "75% aggregate in PCM/PCB and 60% in each subject (Class 12)", "Minimum to be eligible; no category relaxation stated"),
], kind="eligibility_marks")

# ---------- NMMS 2026 (Telangana) ----------
src = "Director of Government Examinations Telangana, Notification Rc.No.03/E/2026-1 dated 20-07-2026: bse.telangana.gov.in/pdf/NMMSSE_2026-27_Notification.pdf (from bse.telangana.gov.in/NMMS.aspx)"
verify(TS, "NMMS (Telangana)", "2026-10-05", src,
    eligibility="Class VIII students in 2026-27 at ZP/Local Body, Government, Government-aided or Model (non-residential) schools; at least 55% (SC/ST 50%) or equivalent grade in Class VII (2025-26); parents' combined annual income below Rs 3,50,000 (MRO or employer certificate). Students of residential schools (TS Residential, Social/Tribal/Minority Welfare, Ashram, KGBV, residential Model Schools), JNV, KV, private unaided and Sainik schools are not eligible",
    application_window="Online on bse.telangana.gov.in; last date to register and pay fee 24 Aug 2026 (closed). Fee Rs 100 (OC/BC), Rs 50 (SC/ST/PH) via SBI Collect",
    exam_date="01 Nov 2026 (Sunday), 9:30 AM - 12:30 PM, at revenue division headquarters in all 33 districts; in Telugu, Hindi, Urdu or English",
    admits_into="National Means-cum-Merit Scholarship (central scheme) for students who qualify, to continue studies from Class IX",
)
cutoffs(TS, "NMMS (Telangana)", 2026, src, "2026-10-05", [
    ("OC / BC", "55% in Class VII (or equivalent grade)", "Minimum to apply"),
    ("SC / ST", "50% in Class VII (or equivalent grade)", "Minimum to apply"),
], kind="eligibility_marks")

# ---------- JNVST 2027 (Class 9 lateral entry) ----------
JNV9 = "JNVST (Navodaya Class 9 lateral entry)"
src = "NVS Prospectus-cum-Notification, Lateral Entry Selection Test for Class IX (2027-28): cbseitms.nic.in/2026/nvsix_9/assets/pdf/FINAL_CLASS_IX_PROSPECTUS_2027.pdf"
verify(AP, JNV9, "2026-10-05", src,
    eligibility="Bona fide resident of the district studying Class VIII in 2026-27 at a Government or Government-recognised school in that same district; born between 01 May 2012 and 31 July 2014 (both inclusive, all categories); Indian national. Not eligible: students who already passed Class VIII earlier, or who sat the lateral entry test before",
    application_window="Online (free) on navodaya.gov.in; last date 30 Sep 2026 (closed), followed by a two-day correction window",
    exam_date="10 Apr 2027 (Saturday), at the district's JNV or another NVS centre; admit cards about a month before",
    admits_into="Class IX in the district's Jawahar Navodaya Vidyalaya for 2027-28, only against vacant seats; admission needs a Class VIII pass in 2026-27",
    exam_pattern="Pen and paper (OMR), 2½ hours, 100 objective questions of 1 mark each, no negative marking: English 15, Hindi 15, Mathematics 35, General Science 35, at Class VIII level. Extra 50 minutes for Divyang students. Question paper in English or Hindi. Merit is on Mathematics + Science + the better of the two languages.",
)
subjects(AP, JNV9, src, "2026-10-05", [
    ("English (15 marks)", "Unseen passage comprehension; word and sentence structure; spelling; rearranging jumbled words; passivation; degrees of comparison; modal auxiliaries; prepositions; tense forms; reported speech"),
    ("Hindi (15 marks)", "Class VIII Hindi comprehension and grammar (ten topics, listed in Hindi in the prospectus)"),
    ("Mathematics (35 marks)", "Rational numbers; squares and square roots; cubes and cube roots; exponents and powers; direct and inverse proportions; comparing quantities (percentage, profit and loss, discount, simple and compound interest); algebraic expressions and identities including factorisation; linear equations in one variable; understanding quadrilaterals; mensuration (area of plane figures, surface area and volume of cube, cuboid, cylinder); data handling (bar graph, pie chart, probability)"),
    ("General Science (35 marks)", "Class 8 chapters: crop production and management; microorganisms; coal and petroleum; combustion and flame; conservation of plants and animals; reproduction in animals; reaching the age of adolescence; force and pressure; friction; sound; chemical effects of electric current; some natural phenomena (lightning, earthquakes); light"),
])
cutoffs(AP, JNV9, 2027, src, "2026-10-05", [
    ("All candidates", "Minimum qualifying marks (set by NVS) in each of the four subjects", "Exact marks not published in the prospectus"),
])
cutoffs(AP, JNV9, 2027, src, "2026-10-05", [
    ("SC / ST / OBC (Central list) / Divyang", "Vacant seats in each category stay reserved for that category", "Unfilled reserved seats may go to other qualified candidates"),
], kind="seat_reservation")

# ---------- CAT 2026 ----------
src = "CAT 2026 Information Bulletin (26-07-2026, V2) and Eligibility note: cdn.digialm.com/per/g06/pub/32842/EForms/image/CAT2026/CAT2026InformationBulletin_26-07-2026_V2.pdf; dates and FAQs on iimcat.ac.in"
verify(AP, "CAT", "2026-10-05", src,
    eligibility="Bachelor's degree with at least 50% marks or equivalent CGPA (45% for SC, ST and PwBD), or a professional qualification (CA/CS/CMA/FIAI) with the same percentage; final-year students may apply and join provisionally. Each IIM sets its own further cut-offs",
    application_window="CAT 2026: registration 03 Aug - 22 Sep 2026, 5:00 PM (closed; extended from 15 Sep). Fee Rs 1,350 (SC/ST/PwBD), Rs 2,700 (others)",
    exam_date="29 Nov 2026 (Sunday), computer-based, three sessions, about 170 test cities; admit cards from 04 Nov 2026; results expected first week of January 2027 (score valid to 31 Dec 2027)",
    admits_into="Management programmes (PGP/MBA and others) at the 22 IIMs, including IIM Visakhapatnam, and many non-IIM institutes that use CAT scores",
    exam_pattern="Computer-based, 2 hours, three sections answered in a fixed order: Verbal Ability & Reading Comprehension; Data Interpretation & Logical Reasoning; Quantitative Ability. MCQs: +3 correct, -1 wrong. Typed-answer (non-MCQ) questions: +3 correct, no negative marking. On-screen calculator; no fixed syllabus. PwBD candidates get 40 extra minutes.",
)
cutoffs(AP, "CAT", 2026, src, "2026-10-05", [
    ("General / EWS / NC-OBC", "50% in Bachelor's degree", "Minimum to be eligible"),
    ("SC / ST / PwBD", "45% in Bachelor's degree", "Minimum to be eligible"),
], kind="eligibility_marks")
cutoffs(AP, "CAT", 2026, src, "2026-10-05", [
    ("SC", "15% of seats", None),
    ("ST", "7.5% of seats", None),
    ("NC-OBC (Central list)", "27% of seats", None),
    ("EWS", "Up to 10% of seats", None),
    ("PwBD", "5% of seats", None),
], kind="seat_reservation")

# ---------- NIFT Entrance (NIFTEE 2026) ----------
src = "NIFTEE-2026 Information Bulletin (NTA for NIFT): cdnbbsr.s3waas.gov.in/s388a839f2f6f1427879fc33ee4acf4f66/uploads/2025/12/202512081380584374.pdf (from exams.nta.nic.in/niftee/); NIFT notices on nift.ac.in/admissions"
verify(AP, "NIFT Entrance", "2026-10-05", src,
    eligibility="B.Des: passed Class 12 (any stream; NIOS with five subjects; or a 3/4-year AICTE/State Board diploma after Class 10). B.F.Tech: Class 12 with Mathematics, or a 3/4-year engineering diploma. Must be under 24 years on 1 August of the admission year (5 years' relaxation for SC/ST/PwD)",
    application_window="NIFTEE 2026: online on exams.nta.nic.in/niftee from 08 Dec 2025; last date 06 Jan 2026, with late fee 07-10 Jan 2026 (closed). Fee Rs 2,000 (Open/EWS/OBC-NCL), Rs 500 (SC/ST/PwD). NIFTEE 2027 not yet announced as of 05 Oct 2026",
    exam_date="NIFTEE 2026 Stage 1: 08 Feb 2026 (GAT computer-based, CAT on paper); Stage 2 (Situation Test) 26 Apr 2026. Exam centres in AP include Rajahmundry, Tirupati, Vijayawada and Visakhapatnam",
    admits_into="B.Des (Fashion, Accessory, Knitwear, Leather, Textile Design, Fashion Communication, Fashion Interiors) and B.F.Tech (Apparel Production) at NIFT's 20 campuses, including NIFT Hyderabad; also M.Des, MFM, M.F.Tech and lateral entry",
    exam_pattern="B.Des: General Ability Test (GAT, computer-based) + Creative Ability Test (CAT, pen and paper), then a Situation Test for shortlisted candidates; rank = entrance exam + Situation Test. B.F.Tech: GAT only. Objective questions 1 mark each, -0.25 for a wrong answer. Paper in Hindi and English.",
)
cutoffs(AP, "NIFT Entrance", 2026, src, "2026-10-05", [
    ("PwD (40% or more disability)", "5% horizontal reservation across SC, ST, OBC (NCL) and Open", "Unfilled PwD seats go back to the same category in the spot round"),
], kind="seat_reservation")

# ---------- SBI PO 2026 ----------
src = "SBI Recruitment of Probationary Officers, Advertisement No. CRPD/PO/2026-27/09: sbi.bank.in/csfile/18062026_1_Detailed_Adv.2026.pdf (from sbi.bank.in/web/careers/current-openings)"
verify(AP, "SBI PO", "2026-10-05", src,
    eligibility="Graduation in any discipline by 30 Sep 2026 (final-year students may apply provisionally). Age 21-30 on 01 Apr 2026 (born 02.04.1996 - 01.04.2005); upper age relaxed by 3 years OBC-NCL, 5 SC/ST, 10-15 PwBD. Attempts (counted at Mains): 6 for UR/EWS, 9 for OBC and PwBD, no limit for SC/ST",
    application_window="2026 (1,500 vacancies): online 18 Jun - 08 Jul 2026 (closed). Fee Rs 750 (UR/EWS/OBC), nil for SC/ST/PwBD",
    exam_date="2026 cycle: Prelims August 2026, Mains August/September 2026, Phase III (psychometric test, group exercise, interview) September-November 2026; final result October-December 2026 (tentative per advertisement)",
    admits_into="Probationary Officer in State Bank of India (Junior Management Grade Scale I), posted anywhere in India; 3-year service bond",
    exam_pattern="Prelims (online, 1 hour, 100 marks): English 40 Qs, Quantitative Aptitude 30, Reasoning 30, 20 minutes each; no sectional cut-off. Mains (online): objective 200 marks in 3 hours (Reasoning & Computer Aptitude 40 Qs/60 marks; Data Analysis & Interpretation 30/60; General Awareness/Economy/Banking 60/60; English 40/20) + descriptive 30 marks in 30 minutes (email, situation analysis, report or precis). 1/4 mark deducted per wrong answer. Final merit: Mains 75% + group exercise & interview 25%.",
)
cutoffs(AP, "SBI PO", 2026, src, "2026-10-05", [
    ("SC", "234 posts", None),
    ("ST", "144 posts", None),
    ("OBC (non-creamy layer)", "390 posts", None),
    ("EWS", "144 posts", None),
    ("UR", "588 posts", None),
    ("PwBD", "4% horizontal (61 posts)", "VI 15, HI 16, LD 14, other 16"),
], kind="seat_reservation")

# ---------- RRB Group D (Level 1), CEN 09/2025 ----------
src = "Railway Recruitment Boards, Centralised Employment Notification CEN No. 09/2025 (Level 1 posts), updated 30.01.2026, with Corrigenda 1-2: rrbsecunderabad.gov.in/wp-content/uploads/2026/01/Final-Detailed-CEN-09-2025-Level-1-updated-on-30.01.2026.pdf"
verify(AP, "RRB Group D (Level 1)", "2026-10-05", src,
    eligibility="10th pass, or ITI, or equivalent, or National Apprenticeship Certificate (NAC) from NCVT, by the closing date (results-awaited candidates may not apply). Age 18-33 on 01 Jan 2026: UR/EWS born 02.01.1993 - 01.01.2008, OBC-NCL from 02.01.1990, SC/ST from 02.01.1988",
    application_window="CEN 09/2025 (22,195 posts): online 31 Jan - 02 Mar 2026 (closed). Fee Rs 500 (Rs 400 refunded on taking the CBT); Rs 250 for SC, ST, ex-servicemen, PwBD, women, transgender, minorities and EBC (fully refunded on taking the CBT). Candidates in AP/Telangana usually apply to RRB Secunderabad",
    exam_date="CBT dates announced on RRB websites and e-call letters (CEN 09/2025 CBT held in 2026). Next Level 1 CEN not yet notified as of 05 Oct 2026",
    admits_into="Level 1 posts (7th CPC, starting pay Rs 18,000) in Indian Railways, e.g. Track Maintainer Grade IV, Pointsman B, and Assistant posts in Electrical, Mechanical, S&T and Engineering departments",
    exam_pattern="Single-stage computer-based test, 90 minutes (120 with scribe), 100 questions of 1 mark: General Science 25 (Class 10 Physics, Chemistry, Life Sciences), Mathematics 25, General Intelligence & Reasoning 30, General Awareness & Current Affairs 20. 1/3 mark deducted per wrong answer. Then a qualifying Physical Efficiency Test: men carry 35 kg for 100 m in 2 min and run 1,000 m in 4 min 15 s; women carry 20 kg for 100 m in 2 min and run 1,000 m in 5 min 40 s. Then document verification and medical.",
)
subjects(AP, "RRB Group D (Level 1)", src, "2026-10-05", [
    ("Mathematics (25 questions)", "Number system, BODMAS, decimals, fractions, LCM, HCF, ratio and proportion, percentages, mensuration, time and work, time and distance, simple and compound interest, profit and loss, algebra, geometry and trigonometry, elementary statistics, square root, age calculations, calendar and clock, pipes and cisterns"),
    ("General Intelligence & Reasoning (30 questions)", "Analogies, alphabetical and number series, coding and decoding, mathematical operations, relationships, syllogism, jumbling, Venn diagrams, data interpretation and sufficiency, conclusions and decision making, similarities and differences, analytical reasoning, classification, directions, statement - arguments and assumptions"),
    ("General Science (25 questions)", "Physics, Chemistry and Life Sciences at Class 10 (CBSE) level"),
    ("General Awareness & Current Affairs (20 questions)", "Current affairs in science and technology, sports, culture, personalities, economics, politics and other important subjects"),
])
cutoffs(AP, "RRB Group D (Level 1)", 2026, src, "2026-10-05", [
    ("UR / EWS", "40% in the CBT", "Minimum to be shortlisted"),
    ("OBC (NCL) / SC / ST", "30% in the CBT", "Minimum to be shortlisted"),
    ("PwBD", "May be relaxed by 2 marks", "Only if PwBD candidates fall short of reserved vacancies"),
])

# ---------- RRB NTPC (CEN 06/2025 Graduate, CEN 07/2025 Under Graduate) ----------
src = "Railway Recruitment Boards, CEN No. 06/2025 NTPC (Graduate) and CEN No. 07/2025 NTPC (Under Graduate): rrbsecunderabad.gov.in/wp-content/uploads/2025/10/Final-CEN-06-2025-21-10-2025-Publish.pdf and .../CEN-07-2025-NTPC-Under-Graduate-English.pdf"
verify(AP, "RRB NTPC", "2026-10-05", src,
    eligibility="Under Graduate posts (Commercial cum Ticket Clerk, Accounts Clerk cum Typist, Junior Clerk cum Typist, Trains Clerk): Class 12 or equivalent with at least 50% (not required for SC/ST/PwBD/ex-servicemen or those with higher qualifications), age 18-30 on 01 Jan 2026. Graduate posts (Station Master, Goods Train Manager, Chief Commercial cum Ticket Supervisor, Junior Accounts Assistant cum Typist, Senior Clerk cum Typist, Traffic Assistant): a degree, age 18-33. Results-awaited candidates may not apply",
    application_window="Last cycle: Graduate CEN 06/2025 (5,810 posts) 21 Oct - 20 Nov 2025; Under Graduate CEN 07/2025 (3,058 posts) 28 Oct - 27 Nov 2025 (both closed). Fee Rs 500 (Rs 400 refunded after CBT 1); Rs 250 for SC, ST, ex-servicemen, PwBD, women, transgender, minorities, EBC (refunded after CBT 1). The 2026 cycle (CEN 06/2026, 07/2026) had only an indicative notice as of 05 Oct 2026",
    exam_date="CBT dates are announced on RRB websites (apply through one RRB; RRB Secunderabad covers AP and Telangana)",
    admits_into="Non-technical railway posts at Pay Levels 2-6 (starting pay Rs 19,900 for UG posts up to Rs 35,400 for Station Master)",
    exam_pattern="CBT 1 (screening): 90 minutes, 100 questions - General Awareness 40, Mathematics 30, General Intelligence & Reasoning 30. CBT 2: 90 minutes, 120 questions - General Awareness 50, Mathematics 35, Reasoning 35. 1/3 mark deducted per wrong answer; 120 minutes with a scribe. Typist posts add a qualifying typing test (30 wpm English / 25 wpm Hindi); Station Master and Traffic Assistant add a Computer Based Aptitude Test (T-score 42 in each battery, no relaxation; merit 70% CBT 2 + 30% CBAT). Questions in English, Hindi and 13 languages including Telugu.",
)
subjects(AP, "RRB NTPC", src, "2026-10-05", [
    ("Mathematics", "Number system, decimals, fractions, LCM, HCF, ratio and proportion, percentage, mensuration, time and work, time and distance, simple and compound interest, profit and loss, elementary algebra, geometry and trigonometry, elementary statistics"),
    ("General Intelligence & Reasoning", "Analogies, number and alphabetical series, coding and decoding, mathematical operations, similarities and differences, relationships, analytical reasoning, syllogism, jumbling, Venn diagrams, puzzles, data sufficiency, statement-conclusion, statement-courses of action, decision making, maps, interpretation of graphs"),
    ("General Awareness", "Current events; games and sports; art and culture of India; Indian literature; monuments and places of India; general science and life science (up to Class 10 CBSE); history of India and the freedom struggle; geography of India and the world; Indian polity and governance; science and technology including space and nuclear programmes; UN and world organisations; environment; basics of computers; common abbreviations; transport systems; Indian economy; famous personalities; flagship government programmes; flora and fauna; important government and public sector organisations"),
])
cutoffs(AP, "RRB NTPC", 2026, src, "2026-10-05", [
    ("UR / EWS", "40% in each CBT", "Minimum for eligibility"),
    ("OBC (NCL) / SC", "30% in each CBT", "Minimum for eligibility"),
    ("ST", "25% in each CBT", "Minimum for eligibility"),
    ("PwBD", "May be relaxed by 2 marks", "Only if PwBD candidates fall short of reserved vacancies"),
])

# ---------- TGPSC Group 2 (Notification 28/2022) ----------
src = "TSPSC (now TGPSC) Notification No. 28/2022, Group-II Services, with Annexure-III Scheme and Syllabus: websitenew.tgpsc.gov.in/directRecruitment (latest Group-II notification listed as of 05 Oct 2026)"
verify(TS, "TGPSC Group 2", "2026-10-05", src,
    eligibility="A degree from a recognised university (some posts need a specific degree, e.g. Law for ASO in Law Department, BSW for some welfare posts). Age 18-44 (reckoned on 01 Jul 2022 for this notification; relaxations per state rules). Some posts carry physical standards",
    application_window="Last notification 28/2022 (783 posts): online 18 Jan - 16 Feb 2023 (closed). No newer Group-II notification on tgpsc.gov.in as of 05 Oct 2026. Fee: Rs 200 application + Rs 120 exam (exam fee waived for unemployed applicants)",
    exam_date="Not announced; watch tgpsc.gov.in for the next Group-II notification",
    admits_into="Telangana state posts such as Municipal Commissioner Gr-III, Assistant Commercial Tax Officer, Naib Tahsildar, Sub-Registrar Gr-II, Mandal Panchayat Officer, Assistant Section Officer (Secretariat and departments), Assistant BC/Tribal/SC Development Officer",
    exam_pattern="Written, objective (OMR/CBRT): four papers of 150 questions, 150 marks, 2½ hours each, total 600. Paper I General Studies & General Abilities; Paper II History, Polity & Society; Paper III Economy & Development; Paper IV Telangana Movement & State Formation. Selection on written marks, then certificate verification. In English, Telugu and Urdu.",
)
subjects(TS, "TGPSC Group 2", src, "2026-10-05", [
    ("Paper I: General Studies and General Abilities", "Current affairs; international relations and events; general science and India's achievements in science and technology; environment and disaster management; world, Indian and Telangana geography; history and cultural heritage of India; society, culture, heritage, arts and literature of Telangana; policies of Telangana State; social exclusion, rights issues and inclusive policies; logical reasoning, analytical ability and data interpretation; basic English (Class 10 standard)"),
    ("Paper II: History, Polity and Society", "Socio-cultural history of India and Telangana; overview of the Indian Constitution and politics; social structure, issues and public policies"),
    ("Paper III: Economy and Development", "Indian economy: issues and challenges; economy and development of Telangana; issues of development and change"),
    ("Paper IV: Telangana Movement and State Formation", "The idea of Telangana (1948-1970); mobilisational phase (1971-1990); towards formation of Telangana State (1991-2014)"),
])
cutoffs(TS, "TGPSC Group 2", 2023, src, "2026-10-05", [
    ("OC / Sportsmen / EWS", "40% in the written exam", "Minimum to qualify"),
    ("BC", "35% in the written exam", "Minimum to qualify"),
    ("SC / ST / PH", "30% in the written exam", "Minimum to qualify"),
])

# ---------- TS TET (structure from the Special TGTET 2026-II bulletin) ----------
src = "Department of School Education Telangana, Information Bulletin, Special TGTET-In-service Teachers-2026-II (TGTET Cell, SCERT): tgtet.aptonline.in/Documents/InformationBulletinTGTET_In-ServiceTeachers2026-II.pdf; TET structure per G.O. Ms. No. 36 (2015) as amended to G.O. Ms. No. 28 (13.11.2025)"
verify(TS, "TS TET", "2026-10-05", src,
    full_form_body="Telangana Teacher Eligibility Test (TGTET), conducted by the Department of School Education / SCERT, Telangana",
    official_website="schooledu.telangana.gov.in",
    eligibility="Passing TET is required to be appointed as a teacher for Classes I-VIII. Paper I is for Classes I-V teachers, Paper II for Classes VI-VIII. Professional qualifications (D.El.Ed / B.Ed etc.) are set in each regular TET notification under NCTE norms",
    application_window="The state holds two regular TETs a year; the next regular TET notification was not yet out as of 05 Oct 2026. (A Special TGTET 2026-II, fee payment 07-16 Oct 2026, is ONLY for in-service government teachers and cannot be used for direct recruitment)",
    exam_date="Regular TET dates are announced in each notification. Special in-service TET: 16-21 Nov 2026 (computer-based)",
    admits_into="TET pass certificate, required to apply for government teacher recruitment (TG DSC) and private school teacher posts for Classes I-VIII",
    exam_pattern="Computer-based, no negative marking, 150 MCQs of 1 mark per paper, 2½ hours each. Paper I: Child Development & Pedagogy 30, Language I 30, English 30, Mathematics 30, Environmental Studies 30 (Classes I-V syllabus). Paper II: Child Development & Pedagogy 30, Language I 30, English 30, and 60 on either Mathematics & Science or Social Studies (Classes VI-VIII syllabus). Bilingual paper: English plus the chosen Language I.",
)
subjects(TS, "TS TET", src, "2026-10-05", [
    ("Paper I: Child Development and Pedagogy (30)", "Educational psychology of teaching and learning at the primary level"),
    ("Paper I: Language I (30)", "One of Telugu, Urdu, Hindi, Bengali, Kannada, Marathi, Tamil, Gujarati (studied up to Class X): proficiency, elements of language, communication and comprehension; 6 questions on pedagogy"),
    ("Paper I: Language II - English (30)", "Proficiency, elements of language, communication and comprehension (up to Class X level); 6 questions on pedagogy"),
    ("Paper I: Mathematics (30)", "Classes I-V topics (difficulty up to Class X): 24 content, 6 pedagogy"),
    ("Paper I: Environmental Studies (30)", "Classes I-V topics (difficulty up to Class X): 24 content, 6 pedagogy"),
    ("Paper II: Mathematics and Science (60)", "Classes VI-VIII topics (difficulty up to Class 12): Mathematics 30 (24 content, 6 pedagogy); Science 30 (Physical Science 12, Biological Science 12, pedagogy 6)"),
    ("Paper II: Social Studies (60)", "History, Geography, Civics and Economics, Classes VI-VIII: 48 content, 12 pedagogy"),
])
cutoffs(TS, "TS TET", 2026, src, "2026-10-05", [
    ("General / EWS", "60% and above", "Pass mark"),
    ("BC", "50% and above", "Pass mark"),
    ("SC / ST / Differently abled", "40% and above", "Pass mark"),
])

# ---------- AP TET (June 2026) ----------
src = "Government of AP, School Education Department, APTET-JUNE 2026 Notification No.01-APTET-JUNE-2026 dated 05-06-2026: tet2dsc.apcfss.in/TET-PDF/APTET-2026 Notification.pdf"
verify(AP, "AP TET", "2026-10-05", src,
    official_website="tet2dsc.apcfss.in",
    eligibility="D.El.Ed / B.Ed or equivalent (NCTE-recognised; RCI for special education) with the marks set in the Information Bulletin; final-semester students may appear but cannot use the certificate for teacher recruitment until they qualify. Paper 1A for Classes I-V, Paper 2A for Classes VI-VIII; 1B/2B for special schools. Unlimited attempts; can re-sit to improve the score",
    application_window="APTET June 2026: online 05 Jun - 05 Jul 2026 on cse.ap.gov.in / tet2dsc.apcfss.in (closed). Fee Rs 1,000 per paper",
    exam_date="APTET June 2026: computer-based, 05-21 Aug 2026 (two sessions daily); initial key 24 Aug 2026. The state holds TET periodically; next session not yet notified as of 05 Oct 2026",
    admits_into="APTET certificate (valid for life), required to be a teacher for Classes I-VIII in AP government, local body, model, residential, welfare, aided and private schools. APTET score carries 20% weightage in the AP DSC Teacher Recruitment Test",
    exam_pattern="Computer-based, 150 marks per paper (Paper 1A/1B for Classes I-V, Paper 2A/2B for Classes VI-VIII); section break-up in the Information Bulletin. Marks normalised across shifts.",
)
cutoffs(AP, "AP TET", 2026, src, "2026-10-05", [
    ("OC / EWS", "60% (90 of 150)", "Pass mark"),
    ("BC", "50% (75 of 150)", "Pass mark"),
    ("SC / ST / PwBD / Ex-servicemen", "40% (60 of 150)", "Pass mark"),
])

# ---------- exam patterns (written into entrance_exams.json) ----------
# Only for exams whose row is already tier_1_official and whose pattern comes
# from the same official document.
PATTERNS = {
    (TS, TG_EAPCET): "Computer-based, 3 hours, 160 multiple-choice questions of 1 mark each. Engineering: 80 Mathematics, 40 Physics, 40 Chemistry. Agriculture & Pharmacy: Biology (Botany and Zoology), Physics and Chemistry. No negative marking. Held in several sessions; marks are normalised across sessions.",
    (TS, TS_ECET): "Computer-based, 3 hours, 200 marks. Diploma (engineering): Mathematics 50, Physics 25, Chemistry 25, branch Engineering paper 100. B.Sc (Maths): Mathematics 100, Analytical Ability 50, Communicative English 50. Pharmacy: four subjects of 50 marks each.",
    (TS, TS_ICET): "Computer-based, 150 minutes, 200 questions of 1 mark each: Analytical Ability 75, Mathematical Ability 75, Communication Ability 50. Sections A and B in English & Telugu or English & Urdu; Section C in English only.",
    (AP, "AP EAPCET"): "Computer-based, 3 hours, 160 multiple-choice questions of 1 mark each: 80 Mathematics, 40 Physics, 40 Chemistry (Engineering stream). No negative marking. Ranks: 75% weightage to normalised EAPCET marks and 25% to Intermediate group-subject marks.",
    (AP, "AP ECET"): "Computer-based, 200 objective questions, 200 marks. Engineering: Mathematics 50, Physics 25, Chemistry 25, branch Engineering paper 100. Pharmacy: four sections of 50 marks. B.Sc (Maths): Mathematics 100, Analytical Ability 50, Communicative English 50.",
    (AP, "AP ICET"): "Computer-based, 150 minutes, 200 questions of 1 mark each: Analytical Ability 75, Communication Ability 70, Mathematical Ability 55. No negative marking. Section B in English only; Sections A and C in English and Telugu.",
    (AP, "NEET-UG"): "Pen and paper (OMR), 3 hours, 180 compulsory multiple-choice questions, 720 marks: Physics 45, Chemistry 45, Biology (Botany & Zoology) 90. +4 for a correct answer, -1 for a wrong one, 0 if unanswered. 13 languages including Telugu.",
    (AP, "JEE Main"): "Paper 1 (B.E./B.Tech): computer-based, 3 hours, 75 questions, 300 marks. Each of Mathematics, Physics and Chemistry has 20 multiple-choice and 5 numerical-answer questions. +4 for a correct answer, -1 for a wrong one in both sections. Two sessions (January and April); the better NTA score counts. 13 languages including Telugu.",
    (AP, NDA): "Written: Mathematics (2½ hours, 300 marks) and General Ability Test (2½ hours, 600 marks), objective questions; one-third of a question's marks deducted for each wrong answer. Then the SSB test/interview (900 marks). Total 1,800. No calculators.",
    (AP, CDS): "Written, objective, 2 hours per paper: English, General Knowledge and Elementary Mathematics (100 marks each) for IMA, INA and AFA; English and General Knowledge only for OTA. Written and interview marks are equal: 300 each for IMA/INA/AFA, 200 each for OTA. Negative marking for wrong answers.",
    (AP, "JEE Advanced"): "Two compulsory papers of 3 hours each on the same day (Paper 1 morning, Paper 2 afternoon), computer-based, each covering Mathematics, Physics and Chemistry. Only the top 2,50,000 JEE (Main) B.E./B.Tech candidates may register (10% GEN-EWS, 27% OBC-NCL, 15% SC, 7.5% ST, 40.5% open; 5% PwD within each). At most two attempts in consecutive years.",
    (AP, "CLAT (UG)"): "2 hours, 120 multiple-choice questions of 1 mark each, passage-based: English 22-26, Current Affairs & GK 28-32, Legal Reasoning 28-32, Logical Reasoning 22-26, Quantitative Techniques 10-14. 0.25 marks deducted for each wrong answer.",
    (AP, "AFCAT"): "Online, 2 hours, 100 objective questions, 300 marks, English only. +3 for each correct answer, -1 for each wrong answer, 0 for unattempted. Numerical Ability at Class 10 level; other sections at graduation level.",
}

# ---------- write ----------
root = os.path.join(os.path.dirname(__file__), "..", "..", "db", "seed")
exams_path = os.path.join(root, "entrance_exams.json")
exams = json.load(open(exams_path, encoding="utf-8"))
missing = set(VERIFIED_ROWS) - {(r["state"], r["exam_name"]) for r in exams}
assert not missing, f"verify() names an exam not in entrance_exams.json: {missing}"
for r in exams:
    r.update(VERIFIED_ROWS.get((r["state"], r["exam_name"]), {}))
for r in exams:
    pattern = PATTERNS.get((r["state"], r["exam_name"]))
    if pattern:
        assert r["data_tier"] == "tier_1_official", r["exam_name"]
        r["exam_pattern"] = pattern
with open(exams_path, "w", encoding="utf-8") as f:
    json.dump(exams, f, ensure_ascii=False, indent=2)
    f.write("\n")
for name, rows in (("exam_subjects", SUBJECTS), ("exam_cutoffs", CUTOFFS)):
    with open(os.path.join(root, f"{name}.json"), "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)
        f.write("\n")
print(f"{len(SUBJECTS)} subjects, {len(CUTOFFS)} cutoff rows")
