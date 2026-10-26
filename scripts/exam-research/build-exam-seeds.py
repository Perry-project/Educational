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

# ---------- APPSC Group 2 (Brief Notification 37/2026) ----------
src = "APPSC Brief Notification No. 37/2026 dated 13/10/2026, Group-II Services, with scheme and syllabus (psc.ap.gov.in/Documents/NotificationDocuments/Group_II_372026.pdf). Previous cycle: Notification 11/2023 (897 posts, selection list 27/01/2026)"
verify(AP, "APPSC Group 2", "2026-10-26", src,
    eligibility="A Bachelor's degree from a recognised university for most posts; ASO (Finance) needs a degree in Mathematics, Economics or Commerce; ASO (Law) needs a Law degree; Senior and Junior Accountant need a degree (Commerce/Economics/Mathematics preferred) plus an SBTET computer certificate course or a computer degree (BCA, B.Sc/B.Com/B.A. Computers, B.Tech CS/IT). Age limits and other conditions will be in the Detailed Notification, due on or before 10/11/2026",
    application_window="Notification 37/2026 (686 provisional posts): online 10/11/2026 - 30/11/2026 (11:59 PM) on psc.ap.gov.in. Fee in the Detailed Notification",
    exam_date="Screening test (offline, OMR) date to be announced in the Detailed Notification",
    admits_into="686 AP state posts: Deputy Tahsildar 200, Deputy MPDO 176, Senior Accountant 90, ASO (GAD) 71, Junior Accountant 48, GST Officer 40, Prohibition & Excise Sub-Inspector 29, Assistant Registrar of Cooperative Societies 10, Sub-Registrar Gr-II 7, Municipal Commissioner Gr-III 6, ASO (Finance) 5, ASO (Law) 4",
)
PATTERNS[(AP, "APPSC Group 2")] = "Screening test: General Studies & Mental Ability, 150 objective questions, 150 marks, 150 minutes (degree standard). Main exam: two objective papers of 150 questions, 150 marks, 150 minutes each (Paper I: social and cultural history of AP and the Indian Constitution; Paper II: Indian and AP economy, science and technology). 1/3 mark deducted for each wrong answer. Then a Computer Proficiency Test (qualifying)."

# ---------- TG DSC (DSC-2024) ----------
src = "Commissioner of School Education, Telangana: Information Bulletin to Notification 24/RC-1/TRT/DSC/2024 dated 29.02.2024 (tgdsc.aptonline.in/tgdsc/docs/Information Bulletin of TS DSC-2024.pdf). The TG DSC portal lists no newer DSC notification as of 12 Oct 2026"
verify(TS, "TG DSC", "2026-10-12", src,
    eligibility="The academic and training qualification set for each post in the bulletin, plus a pass in TSTET / APTET / CTET in the matching paper and subject (e.g. Paper-II for School Assistants). Age 18-46 (DSC-2024); relaxations as per rules",
    application_window="Last notification DSC-2024 (11,062 posts): online 04 Mar - 02 Apr 2024 (closed), Rs 1,000 fee per post. No DSC 2026 notification on tgdsc.aptonline.in as of 12 Oct 2026",
    exam_date="Not announced; watch tgdsc.aptonline.in and schooledu.telangana.gov.in for the next DSC",
    admits_into="Teaching posts in Telangana government and local body schools: School Assistant, Secondary Grade Teacher, Language Pandit, Physical Education Teacher, Special Education Teacher",
)
PATTERNS[(TS, "TG DSC")] = "Computer Based Test. Final marks out of 100: 80 from the written test and 20 from the TET score (TSTET / APTET / CTET). For School Assistant (Physical Education) and PET, all 100 marks are from the written test."

# ---------- TS Police Constable & SI 2026 ----------
src = "TSLPRB press notes Rc Nos. 189, 225, 234 & 279/Rect./Rect.1, 2 & 3/2026 dated 01-08-2026 (application dates and fees), 08-09-2026 (last date extended to 16 Sep) and 17-09-2026 (applications closed; tentative PWT dates): tgprb.in/SI_PC_2026/"
verify(TS, "TS Police Constable & SI", "2026-10-12", src,
    eligibility="Educational qualification, age and physical standards are set in the four detailed notifications of 29 Jul 2026 on tgprb.in. For this recruitment the government added 7 years to the upper age limit for SI/ASI-level and PC (Driver) posts, and 10 years for other PC-level posts",
    application_window="2026: 4 notifications dated 29 Jul 2026 for 7,437 posts (298 SI/ASI level, 7,139 PC level). Online 19 Aug - 16 Sep 2026 (closed). One-time fee Rs 1,500 for SI level / Rs 1,200 for PC level (Rs 750 / Rs 600 for SC/ST local candidates)",
    exam_date="Preliminary Written Test tentatively 29 Nov 2026 (SI level) and 20 Dec 2026 (PC level); then PMT/PET and the final written exam",
    admits_into="Police (Civil, AR, TGSP, SAR CPL) Sub-Inspectors and Constables, SPF, Fire (Station Fire Officer, Fire Fighter), Prisons (Deputy Jailor, Warder), ASI (Finger Print Bureau) and PC Driver/Mechanic posts in Telangana",
)
PATTERNS[(TS, "TS Police Constable & SI")] = "Preliminary Written Test (one 3-hour exam for PC level, one for SI level; none for technical posts) -> Physical Measurement / Efficiency Test -> trade or driving test for PC Mechanic/Driver -> final written exam (one 3-hour exam for PC level; four 3-hour papers incl. two descriptive for SI level) -> certificate verification."

# ---------- Subjects added 2026-10-12 ----------
# Exams verified earlier whose subjects weren't listed yet. Each list is
# read from the official document named; where that document gives only the
# sections (not a topic list), the topics say no more than the document does.
_SEED_EXAMS = {(r["state"], r["exam_name"]): r for r in json.load(open(
    os.path.join(os.path.dirname(__file__), "..", "..", "db", "seed", "entrance_exams.json"), encoding="utf-8"))}


# ---------- APPSC Group 4 (latest: Notification 22/2025) ----------
src = "APPSC Notification No.22/2025 dated 24.09.2025, Junior Office Assistant in A.P. Director General of Prisons and Correctional Services under Group-IV Services, with Annexure-II Scheme & Syllabus and CPT scheme (psc.ap.gov.in/Documents/NotificationDocuments/JrOfficeAsst_Notification_222025_24092025.pdf); final key and marks list published 07/05/2026. Latest Group-IV notification on portal-psc.ap.gov.in as of 13 Oct 2026"
verify(AP, "APPSC Group 4", "2026-10-13", src,
    eligibility="A Bachelor's degree from any university in India recognised by the UGC, or equivalent. Age 18-42 on 01.07.2025 for this notification (G.O.Ms.No.36, 04.03.2025); relaxations as per rules (e.g. SC/ST/BC/EWS 5 years). Must also pass the Computer Proficiency Test before appointment",
    application_window="Last notification 22/2025 (1 district post, Prisons Dept): online 25 Sep - 15 Oct 2025 (closed; final key and marks list published 07 May 2026). Earlier: 06/2022 and 23/2021 (Junior Assistant cum Computer Assistant, Revenue). No newer Group-IV notification as of 13 Oct 2026. Fee: Rs 250 processing + Rs 80 exam (exam fee waived for SC, ST, BC, PBD and ex-servicemen)",
    exam_date="Not announced; watch psc.ap.gov.in for the next Group-IV notification",
    admits_into="Group-IV clerical posts in AP government departments, e.g. Junior Assistant, Junior Assistant cum Computer Assistant, Junior Office Assistant, Typist. District cadre: the District Selection Committee selects from the Commission's district ranking list",
)
PATTERNS[(AP, "APPSC Group 4")] = "Written exam (objective, OMR): Paper I General Studies & Mental Ability (degree standard) and Paper II General English & General Telugu (SSC standard, 75 marks each), 150 questions, 150 marks, 150 minutes each, total 300. 1/3 mark deducted for each wrong answer. Shortlisted candidates then take a Computer Proficiency Test (practical, 60 minutes, 100 marks; qualifying)."
subjects(AP, "APPSC Group 4", src, "2026-10-13", [
    ("Paper I: General Studies & Mental Ability (150 marks)", "Current events (international, national, AP); general science and contemporary developments in science, technology and IT; history of India with a focus on AP and the national movement; geography of India with focus on AP; Indian polity and governance; Indian economy and planning; sustainable development and environmental protection; disaster management; logical reasoning and analytical ability; data analysis and interpretation"),
    ("Paper II: General English & General Telugu (150 marks)", "English: comprehension, usage and idioms, vocabulary and punctuation, logical re-arrangement of sentences, grammar. Telugu: synonyms and vocabulary, grammar, Telugu-English and English-Telugu meanings, usage and idiom"),
    ("Computer Proficiency Test (qualifying, 100 marks)", "Introduction to computers, software types, operating systems, Windows; office automation tasks in MS Word, MS Excel and MS PowerPoint"),
])
cutoffs(AP, "APPSC Group 4", 2025, src, "2026-10-13", [
    ("OC / Ex-Servicemen / EWS", "40% aggregate in the written exam", "Minimum to qualify"),
    ("BC", "35% aggregate in the written exam", "Minimum to qualify"),
    ("SC / ST / PBD", "30% aggregate in the written exam", "Minimum to qualify"),
    ("OC (CPT)", "40 of 100", "Computer Proficiency Test, qualifying"),
    ("BC (CPT)", "35 of 100", "Computer Proficiency Test, qualifying"),
    ("SC / ST / PBD (CPT)", "30 of 100", "Computer Proficiency Test, qualifying"),
])

# ---------- APPSC Group 3 (scheme only; no current notification) ----------
src = "APPSC Group-III Services, Scheme and Syllabus for recruitment to the post of Panchayat Secretary (Grade-IV), A.P. Panchayat Raj Subordinate Service, dated 15.11.2016 (psc.ap.gov.in/Documents/Syllabus1/Group-III Panchayat Raj Secretary 15.11.2016.PDF). No Group-III notification on the recruitment notifications list at portal-psc.ap.gov.in as of 13 Oct 2026"
verify(AP, "APPSC Group 3", "2026-10-13", src,
    eligibility="Not yet available: set in each notification, and there is no current Group-III notification",
    application_window="No Group-III notification on psc.ap.gov.in as of 13 Oct 2026",
    exam_date="Not announced",
    admits_into="Panchayat Secretary (Grade-IV), A.P. Panchayat Raj Subordinate Service (the post covered by the last published Group-III scheme)",
)
PATTERNS[(AP, "APPSC Group 3")] = "2016 scheme (degree standard, objective): Screening test of 150 questions, 150 marks, 150 minutes. Main exam: Paper 1 General Studies & Mental Ability and Paper 2 Rural Development and Problems in Rural Areas with special reference to AP, 150 questions, 150 marks, 150 minutes each, total 300. The scheme in a future notification may differ."

# ---------- TGPSC Group 3 (latest: Notification 29/2022) ----------
src = "TSPSC (now TGPSC) Notification No.29/2022 dated 30/12/2022, Group-III Services (General Recruitment), with Annexure-III Scheme and Syllabus, and Addendum web note (Feb 2023) adding 12 posts to Post Code 15 (websitenew.tgpsc.gov.in/directRecruitment). Latest Group-III notification listed as of 13 Oct 2026"
verify(TS, "TGPSC Group 3", "2026-10-13", src,
    scope=TS, stage="jobs", category="State services", body_type="Government",
    conducting_body="Telangana Public Service Commission", official_website="websitenew.tgpsc.gov.in",
    eligibility="A degree from a recognised university for almost all posts; a few need more (e.g. computers as a subject for some posts, a typewriting pass for typist posts). Age 18-44 on 01.07.2022 for this notification; relaxations as per rules",
    application_window="Last notification 29/2022 (1,363 posts across 105 post codes, plus 12 added by addendum): online 24 Jan - 23 Feb 2023 (closed). No newer Group-III notification on tgpsc.gov.in as of 13 Oct 2026. Fee: Rs 200 application + Rs 80 exam (exam fee waived for unemployed applicants)",
    exam_date="Not announced; watch websitenew.tgpsc.gov.in for the next Group-III notification",
    admits_into="Telangana state posts such as Senior Accountant, Auditor, Senior Auditor, Assistant Auditor, Junior Assistant and Junior Assistant cum Typist across government departments and HODs",
    exam_pattern="Written, objective (CBRT/OMR): three papers of 150 questions, 150 marks, 2½ hours each, total 450. Paper I General Studies & General Abilities; Paper II History, Polity & Society; Paper III Economy & Development. Selection on written marks, then certificate verification. In English, Telugu and Urdu.",
)
subjects(TS, "TGPSC Group 3", src, "2026-10-13", [
    ("Paper I: General Studies and General Abilities", "Current affairs; international relations and events; general science and India's achievements in science and technology; environmental issues and disaster management; world, Indian and Telangana geography; history and cultural heritage of India; society, culture, heritage, arts and literature of Telangana; policies of Telangana State; social exclusion, rights issues and inclusive policies; logical reasoning, analytical ability and data interpretation; basic English (8th class standard)"),
    ("Paper II: History, Polity and Society", "Socio-cultural history of Telangana and formation of Telangana State; overview of the Indian Constitution and politics; social structure, issues and public policies"),
    ("Paper III: Economy and Development", "Indian economy: issues and challenges; economy and development of Telangana; issues of development and change"),
])
cutoffs(TS, "TGPSC Group 3", 2023, src, "2026-10-13", [
    ("OC / Sportsmen / Ex-servicemen / EWS", "40% in the written exam", "Minimum to qualify"),
    ("BC", "35% in the written exam", "Minimum to qualify"),
    ("SC / ST / PH", "30% in the written exam", "Minimum to qualify"),
])

# ---------- AP Judicial Service: Civil Judge (Junior Division), Notification 118/2026 ----------
src = "High Court of Andhra Pradesh Notification No.118/2026-RC dated 25.09.2026, Civil Judge (Junior Division), under the A.P. State Judicial (Service & Cadre) Rules, 2026 (linked from aphc.gov.in; PDF at g03.tcsion.com/per/g03/pub/726/EForms/image/ImageDocUpload/71161/7/3301224270.pdf), and the application portal's key dates (cdn3.digialm.com/EForms/configuredHtml/2381/102127/Index.html)"
AP_CJ = "AP Judicial Service (Civil Judge) Exam"
verify(AP, AP_CJ, "2026-10-14", src,
    scope=AP, stage="jobs", category="Law & judiciary", body_type="Government",
    conducting_body="High Court of Andhra Pradesh", official_website="aphc.gov.in",
    full_form_body="Direct recruitment and recruitment by transfer to Civil Judge (Junior Division) in the Andhra Pradesh State Judicial Service, conducted by the High Court of Andhra Pradesh",
    eligibility="Direct recruitment: a law degree obtained at least one year before the notification date (no years-of-practice condition in 2026, citing the Supreme Court's judgment of 21.08.2026 in Bhumika Trust v. Union of India, W.P.(C) 1110/2025). Must not have completed 35 years on 01.09.2026; 5 years' relaxation for SC/ST/BC/EWS, 10 years for persons with benchmark disabilities. Recruitment by transfer: law degree, a confirmed member or approved probationer in the listed High Court / district judiciary / prosecution / Law Department posts, under 48 on 01.09.2026",
    application_window="Notification 118/2026: 119 posts (96 direct recruitment, 23 by transfer). Online 01.10.2026 - 26.10.2026 (11:59 PM) on aphc.gov.in. Fee Rs 1,500 for OC/EWS/BC, Rs 750 for SC/ST/persons with benchmark disabilities",
    exam_date="Screening test (computer based): date to be notified; hall tickets one week before it",
    admits_into="Civil Judge (Junior Division), A.P. State Judicial Service, pay scale Rs 77,840 - 1,36,520. Selected candidates are Trainee Judicial Officers: one year at the Judicial Academy, then one year of law clerkship, before regular posting",
    exam_pattern="Screening test (CBT): 100 objective questions, 100 marks, 2 hours; 40% needed, shortlisted 1:10, marks not counted in the final merit. Written exam: Paper I Civil Laws, Paper II Criminal Laws, Paper III English (translation English<->Telugu 40 marks + essay on legal subjects 60 marks), 100 marks and 3 hours each, answered in English; Paper III is qualifying (40% in each part). Viva voce 50 marks, called 1:3. Merit on Papers I and II plus viva voce.",
)
subjects(AP, AP_CJ, src, "2026-10-14", [
    ("Civil Laws (screening test and Paper I)", "Code of Civil Procedure 1908; Indian Contract Act 1872; Hindu Marriage Act 1955; Hindu Succession Act 1956; Indian Easements Act 1882; Specific Relief Act 1963; Limitation Act 1963; Transfer of Property Act 1882; Civil Rules of Practice; Registration Act 1908 and Indian Stamp Act 1899; A.P. Land Encroachment Act 1905; Indian Evidence Act 1872; Bharatiya Sakshya Adhiniyam 2023"),
    ("Criminal Laws (screening test and Paper II)", "Code of Criminal Procedure 1973; Indian Evidence Act 1872; Indian Penal Code 1860; Bharatiya Nagarik Suraksha Sanhita 2023; Bharatiya Sakshya Adhiniyam 2023; Bharatiya Nyaya Sanhita 2023; Negotiable Instruments Act 1881; Protection of Women from Domestic Violence Act 2005; Criminal Rules of Practice; A.P. Excise Act 1968; A.P. Gaming Act 1974; Juvenile Justice Act 2015; Food Safety and Standards Act 2006; Information Technology Act 2000; POCSO Act 2012; A.P. Forest Act 1967"),
    ("Paper III: English (qualifying)", "Part I (40 marks): translate a passage English to Telugu and Telugu to English. Part II (60 marks): essay writing on legal subjects"),
])
cutoffs(AP, AP_CJ, 2026, src, "2026-10-14", [
    ("All (screening test)", "40% of 100", "To be shortlisted (1:10) for the written exam"),
    ("OC / EWS", "55% in Paper I and Paper II each, 60% aggregate", "Written exam, to be called for viva voce"),
    ("BC", "50% in Paper I and Paper II each, 55% aggregate", "Written exam, to be called for viva voce"),
    ("SC / ST / PwBD", "45% in Paper I and Paper II each, 50% aggregate", "Written exam, to be called for viva voce"),
    ("OC / EWS (final)", "60% aggregate of written exam and viva voce", "Needed for selection"),
    ("BC (final)", "55% aggregate of written exam and viva voce", "Needed for selection"),
    ("SC / ST / PwBD (final)", "50% aggregate of written exam and viva voce", "Needed for selection"),
])

# ---------- Telangana Judicial Service: Civil Judge (Junior Division), Notification 45/2025 ----------
src = "High Court for the State of Telangana Notification No.45/2025-RC dated 01.12.2025, Civil Judge (Junior Division), under the Telangana State Judicial (Service and Cadre) Rules, 2023 (PDF at g03.tcsion.com/per/g03/pub/726/EForms/image/ImageDocUpload/71161/2/9501106140.pdf, via cdn3.digialm.com/EForms/configuredHtml/2775/96831/Index.html); tshc.gov.in home page notice of viva-voce call letters for the 94 posts, seen 14 Oct 2026. Latest Civil Judge notification as of 14 Oct 2026"
TS_CJ = "Telangana State Judicial Service (Civil Judge) Exam"
verify(TS, TS_CJ, "2026-10-14", src,
    scope=TS, stage="jobs", category="Law & judiciary", body_type="Government",
    conducting_body="High Court for the State of Telangana", official_website="tshc.gov.in",
    full_form_body="Direct recruitment and recruitment by transfer to Civil Judge (Junior Division) in the Telangana State Judicial Service, conducted by the High Court for the State of Telangana",
    eligibility="As in Notification 45/2025 (direct recruitment): a law degree, enrolled as an advocate, and at least 3 years' practice before the Telangana High Court or courts under it on the notification date (law clerk / research assistant service counts). Age 23 to 35 (40 for EWS, SC, ST and BC) on the notification date; +10 years for differently-abled persons. Must read, speak and write Telugu fluently. The next notification may change these: Andhra Pradesh's 2026 notification dropped its practice condition after a Supreme Court judgment of 21.08.2026",
    application_window="Last notification 45/2025: 94 posts (66 direct recruitment, 28 by transfer). Online 08.12.2025 - 29.12.2025 (closed; viva-voce call letters issued). Fee Rs 1,250 for OC/BC, Rs 600 for EWS/PwD/SC/ST. No newer notification on tshc.gov.in as of 14 Oct 2026",
    exam_date="2025 cycle at the viva-voce stage. Not announced for the next cycle; watch tshc.gov.in",
    admits_into="Civil Judge (Junior Division), Telangana State Judicial Service, pay scale Rs 77,840 - 1,36,520; one year's training at the Telangana State Judicial Academy, two years' probation",
    exam_pattern="Screening test (CBT): 100 objective questions, 100 marks, 2 hours; 40% needed, shortlisted 1:10, marks not counted. Written exam: Paper I Civil Laws, Paper II Criminal Laws, Paper III English (Part I translation English<->Telugu 30 marks, Part II essay on legal subjects, grammar and vocabulary 70 marks; qualifying, 50% in each part), 100 marks and 3 hours each. Viva voce 30 marks, called 1:3. Final selection on Papers I and II plus viva voce.",
)
subjects(TS, TS_CJ, src, "2026-10-14", [
    ("Civil Laws (screening test and Paper I)", "Code of Civil Procedure 1908 with Civil Rules of Practice 1990; Indian Contract Act 1872 and Sale of Goods Act; Indian Evidence Act 1872; Hindu Succession Act 1956; Hindu Marriage Act 1955; Specific Relief Act 1963; Indian Easements Act 1882; Limitation Act 1963; Transfer of Property Act 1882; Indian Stamp Act 1899 and Registration Act 1908; Commercial Courts Act 2015; Indian Succession Act 1925; laws on Hindu adoption, guardianship and maintenance; Legal Services Authorities Act 1987; Telangana Land Encroachment Act 1905; Telangana Buildings (Lease, Rent & Eviction) Control Act 1960"),
    ("Criminal Laws (screening test and Paper II)", "Code of Criminal Procedure 1973; Indian Evidence Act 1872; Indian Penal Code 1860; Negotiable Instruments Act 1881 (sections 138-148A); Telangana Prohibition Act 1995; Telangana Excise Act 1968; Juvenile Justice Act 2015; Protection of Women from Domestic Violence Act 2005; forest laws in Telangana and Wild Life Protection Act 1972; POCSO Act 2012; Mental Health Care Act 2017; Immoral Traffic Prevention Act 1956; Criminal Rules of Practice 1990; Telangana Gaming Act 1974; Unlawful Activities (Prevention) Act 1967; Bharatiya Nyaya Sanhita; Bharatiya Nagarik Suraksha Sanhita; Bharatiya Sakshya Adhiniyam"),
    ("Paper III: English (qualifying)", "Part I (30 marks): translation English to Telugu and Telugu to English. Part II (70 marks): essay on legal subjects, grammar and vocabulary"),
])
cutoffs(TS, TS_CJ, 2025, src, "2026-10-14", [
    ("All (screening test)", "40% of 100", "To be shortlisted (1:10) for the written exam"),
    ("OC / EWS", "60% in Paper I and Paper II each", "Written exam, to be called for viva voce"),
    ("BC", "55% in Paper I and Paper II each", "Written exam, to be called for viva voce"),
    ("SC / ST / PwD", "50% in Paper I and Paper II each", "Written exam, to be called for viva voce"),
    ("SC / ST / PwD (viva voce)", "40% of 30", "Needed to be recommended"),
    ("Others (viva voce)", "50% of 30", "Needed to be recommended"),
])

# ---------- CTET 22nd edition (Sept 2026, moved to Dec 2026) ----------
src = "CBSE CTET Information Bulletin, September 2026 (22nd edition) and public notices dated 08.05.2026, 25.08.2026 (applications reopened) and 14.09.2026 (exam on 12-13 Dec 2026): ctet.nic.in"
CTET = "CTET (Central Teacher Eligibility Test)"
verify(AP, CTET, "2026-10-14", src,
    scope="National", stage="jobs", category="Teaching jobs", body_type="Government",
    conducting_body="Central Board of Secondary Education (CBSE)", official_website="ctet.nic.in",
    full_form_body="Central Teacher Eligibility Test, conducted by CBSE: Paper I for teachers of Classes I-V, Paper II for Classes VI-VIII. Separate from the state AP TET / TS TET",
    eligibility="The minimum qualifications notified by NCTE (see ncte.gov.in) and the recruitment rules of the appropriate government / KVS / NVS; reserved categories get up to 5% relaxation in the qualifying marks of the minimum educational qualification. The candidate checks their own eligibility; the recruiter verifies it finally",
    application_window="22nd edition: online 11.05.2026 - 10.06.2026, reopened 25.08.2026 - 01.09.2026 after a Supreme Court judgment (closed). Fee: General/OBC(NCL) Rs 1,000 for one paper, Rs 1,200 for both; SC/ST/differently abled Rs 500 / Rs 600",
    exam_date="12 and 13 December 2026 (moved from 6 Sep 2026 by CBSE notice of 14.09.2026). Exam city and date shown on the portal 15 days before; admit card 2 days before",
    admits_into="Eligibility (not a rank) for teaching posts in central government schools (KVS, NVS, Central Tibetan Schools, etc.); unaided private schools may also accept it. Certificate valid for life; no limit on attempts",
    exam_pattern="Offline OMR, 2½ hours per paper, 150 MCQs of 1 mark each, no negative marking, bilingual (Hindi/English). Paper I: Child Development & Pedagogy, Mathematics, Environmental Studies, Language I, Language II (30 each). Paper II: Child Development & Pedagogy 30, Mathematics & Science or Social Studies 60, Language I 30, Language II 30.",
)
subjects(AP, CTET, src, "2026-10-14", [
    ("Paper I (Classes I-V): Child Development and Pedagogy, 30 marks", "Educational psychology of teaching and learning for ages 6-11: characteristics and needs of diverse learners, interaction with learners, qualities of a good facilitator of learning"),
    ("Paper I: Mathematics and Environmental Studies, 30 marks each", "Concepts, problem solving and pedagogy, spread over the NCERT Classes I-V syllabus, with difficulty up to the secondary stage"),
    ("Paper I and II: Language I and Language II, 30 marks each", "Language I: proficiency in the medium of instruction. Language II (a different language): elements of language, communication and comprehension. 20 languages offered, including Telugu, English and Urdu"),
    ("Paper II (Classes VI-VIII): Child Development and Pedagogy, 30 marks", "Educational psychology of teaching and learning for ages 11-14"),
    ("Paper II: Mathematics & Science or Social Studies, 60 marks", "Maths and Science teachers take Mathematics and Science; Social Studies teachers take Social Studies / Social Science; any other teacher takes either. Based on the NCERT Classes VI-VIII syllabus, difficulty up to senior secondary"),
])
cutoffs(AP, CTET, 2026, src, "2026-10-14", [
    ("All", "60% (90 of 150)", "TET pass, per NCTE notification of 11.02.2011; school managements may give concessions to SC/ST/OBC/differently abled per their reservation policy"),
])

# ---------- UGC NET December 2026 ----------
src = "NTA Information Bulletin, UGC-NET December 2026, and public notice dated 08.10.2026 opening registration: ugcnet.nta.nic.in"
NET = "UGC NET (National Eligibility Test)"
verify(AP, NET, "2026-10-14", src,
    scope="National", stage="after_degree", category="Research & teaching (PG)", body_type="Government",
    conducting_body="National Testing Agency (NTA) for the University Grants Commission", official_website="ugcnet.nta.nic.in",
    full_form_body="UGC National Eligibility Test, conducted by NTA in 87 subjects: decides eligibility for Junior Research Fellowship, Assistant Professor and Ph.D. admission in Indian universities and colleges",
    eligibility="A Master's degree or equivalent with at least 55% (50% for OBC-NCL, SC, ST, PwD/PwBD and third gender), no rounding off; final-year Master's students may apply provisionally. Age: JRF not more than 30 on 01.12.2026 (up to 5 years' relaxation for OBC-NCL, SC, ST, PwD, third gender, women, research experience and armed forces service; 3 years for LL.M.; at most 5 in total). No upper age limit for Assistant Professor or Ph.D. admission",
    application_window="December 2026: online 08.10.2026 - 28.10.2026 (11:50 PM); with Rs 500 late fee 29-31.10.2026; corrections 02-04.11.2026. Fee: General Rs 1,150, General-EWS/OBC-NCL Rs 600, SC/ST/PwD/third gender Rs 325",
    exam_date="14 - 19 December 2026 (CBT); city slip and admit card dates to be announced",
    admits_into="JRF with Assistant Professor eligibility, Assistant Professor eligibility with Ph.D. admission, or Ph.D. admission only. Held twice a year (June and December)",
    exam_pattern="CBT, 3 hours with no break. Paper 1 (teaching and research aptitude: reasoning, reading comprehension, divergent thinking, general awareness): 50 questions, 100 marks. Paper 2 (your subject): 100 questions, 200 marks. 2 marks per correct answer, no negative marking.",
)
subjects(AP, NET, src, "2026-10-14", [
    ("Paper 1: Teaching and Research Aptitude (50 questions, 100 marks)", "Compulsory for all: teaching and research aptitude, reasoning ability, reading comprehension, divergent thinking and general awareness"),
    ("Paper 2: your chosen subject (100 questions, 200 marks)", "One of 87 subjects at post-graduation level; each subject's syllabus is on ugcnetonline.in/syllabus-new.php"),
])
cutoffs(AP, NET, 2026, src, "2026-10-14", [
    ("General / General-EWS", "40% aggregate of both papers", "Minimum to be considered; only the top 6% of candidates who appeared are declared qualified for Assistant Professor"),
    ("OBC-NCL / SC / ST / PwD / third gender", "35% aggregate of both papers", "Minimum to be considered; qualified numbers are split by category and subject"),
])

# =====================================================================
# Batch 2026-10-20: exams from the 10-16..10-19 deltas, each checked
# against its own official document (the deltas cited aggregators only).
# =====================================================================

# ---------- AP DSC-2026 (APTRT-2026), brief notification ----------
src = "School Education Department, AP: Brief Notification No. 1/DSC-2026 / APTRT-2026 dated 13.10.2026 (G.O.Ms.No.28, School Education (Services-I), 13.10.2026) and press release of 13.10.2026: tet2dsc.apcfss.in/DSC2026/notifications/DSC-2026 General notification (1).pdf, .../DSC2026/DSC-2026 Press Note English.pdf"
verify(AP, "AP DSC", "2026-10-20", src,
    conducting_body="Director of School Education, Andhra Pradesh", official_website="tet2dsc.apcfss.in",
    full_form_body="DSC-2026 / Andhra Pradesh Teacher Recruitment Test (APTRT-2026), conducted by the Director of School Education, Andhra Pradesh",
    eligibility="Not yet available: qualifications, age limits and eligibility conditions will be in the Detailed Notification, due on tet2dsc.apcfss.in on or before 03.11.2026",
    application_window="Brief notification issued 13.10.2026. Online applications only, through tet2dsc.apcfss.in, during the period given in the Detailed Notification (due on or before 03.11.2026). Fee not yet announced",
    exam_date="Computer Based Test (objective). Date not yet announced: it will be in the Detailed Notification",
    admits_into="2,721 tentative teacher posts: 906 School Assistant and 1,205 SGT in Govt/ZP/MPP/Municipal schools; 150 SA and 200 SGT (Special Education); 260 in societies and other managements (30 Principal, 81 PGT, 113 TGT, 2 Physical Director, 34 PET in APSWREIS, APTWREIS, MJPAPBCWREIS, APREIS, AP Model Schools and the WDA, TG & SC Dept.). Vacancies are tentative; final ones with rosters come in the Detailed Notification",
    exam_pattern="Computer Based Test (objective type). Syllabus already published on tet2dsc.apcfss.in (DSC_2026 Suggestive Syllabus). Full scheme in the Detailed Notification",
)

# ---------- RMS CET 2026 (Rashtriya Military Schools, Class VI & IX for 2027-28) ----------
src = "NTA Information Bulletin, RMS CET-2026 (Oct 2026), chapters 2-3; RMS Common Prospectus 2027-28; NTA FAQs 18.10.2026: exams.nta.nic.in/rmscet/ (cdnbbsr.s3waas.gov.in/s388a839f2f6f1427879fc33ee4acf4f66/uploads/2026/10/20261015369621797.pdf)"
verify(AP, "RMS CET (Rashtriya Military Schools)", "2026-10-20", src,
    conducting_body="National Testing Agency (NTA), for the Ministry of Defence (Army)", official_website="exams.nta.nic.in/rmscet",
    full_form_body="Rashtriya Military Schools Common Entrance Test for Class VI and Class IX at the five RMSs (Chail, Ajmer, Dholpur, Belgaum, Bengaluru), conducted by NTA (Stage-I written exam); medical exam and interview by the RMSs. There is no RMS in Andhra Pradesh or Telangana",
    eligibility="Boys and girls. Class VI: aged 10-13 on 31.03.2027 (born 01.04.2014 - 31.03.2017), passed or studying in Class V. Class IX: aged 13-16 on 31.03.2027 (born 01.04.2011 - 31.03.2014), passed Class VIII from a recognised school. Six months' upper-age relaxation for wards of personnel killed in action. Seats: 70% wards of JCOs/OR, 20% wards of officers, 10% civilians; OBC-NCL 27%, SC 15%, ST 7.5% within each; girls 10% (Class VI capped at 30 seats)",
    application_window="Online 23.09.2026 - 20.10.2026 (5 PM; fee by 11:50 PM). Late window with Rs 500 late fee 21.10.2026 - 25.10.2026. Corrections 27-28.10.2026. Fee Rs 1,000 General/OBC, Rs 750 SC/ST and wards of personnel killed in action",
    exam_date="Stage-I written exam: 13 December 2026 (Sunday), 2 hours 30 minutes, OMR. City slip last week of November; admit card 5-7 days before. Result January 2027; medical and interview February-March 2027; joining by April 2027",
    admits_into="Class VI or IX at a Rashtriya Military School (English-medium, co-ed, boarding only, CBSE; Science stream only after Class 10), run by the Ministry of Defence to prepare cadets for the Defence Services",
    exam_pattern="Class VI (Class V standard, bilingual): English 50 (qualifying, 35%, not counted in merit), Intelligence 50, Mathematics 50, General Knowledge & Current Affairs 50 (40% each to qualify); interview 20. Class IX (Class VIII standard, English only): Paper 1 English 50 + Hindi 20 + Social Science 30 = 100; Paper 2 Mathematics 50 + Science 50 = 100 (50% in each paper to qualify); interview 50. Ties broken on Mathematics marks first",
)
cutoffs(AP, "RMS CET (Rashtriya Military Schools)", 2026, src, "2026-10-20", [
    ("All (Class VI, English)", "35%", "Qualifying only, not counted in the merit list"),
    ("All (Class VI, Intelligence / Mathematics / GK)", "40% in each", "Minimum to qualify"),
    ("All (Class IX, Paper 1 and Paper 2)", "50% in each", "Minimum to qualify"),
])

# ---------- INI-CET January 2027 session ----------
src = "AIIMS New Delhi, Tentative Schedule of Entrance Examinations 2026: aiimsexams.ac.in/landingpage/key-dates (seen 20 Oct 2026)"
verify(AP, "INI-CET (Institute of National Importance Combined Entrance Test)", "2026-10-20", src,
    scope="National", stage="after_degree", category="Medical (PG)", body_type="Government",
    conducting_body="All India Institute of Medical Sciences (AIIMS), New Delhi", official_website="aiimsexams.ac.in",
    full_form_body="Institute of National Importance Combined Entrance Test for PG medical courses (MD/MS/MDS, 6-year M.Ch/DM), conducted by AIIMS New Delhi for AIIMS campuses, JIPMER, NIMHANS, PGIMER and SCTIMST",
    eligibility="As set out in the INI-CET prospectus on aiimsexams.ac.in (MBBS / BDS route); not transcribed here",
    application_window="January 2027 session: registration has closed. The next (July 2027) session's dates will be announced on aiimsexams.ac.in",
    exam_date="January 2027 session: 1 November 2026 (Sunday); result 7 November 2026 (Saturday). Counselling dates to be declared. The July 2026 session was held on 16 May 2026",
    admits_into="MD, MS, MDS, 6-year M.Ch and DM seats at AIIMS (all campuses), JIPMER Puducherry, NIMHANS Bengaluru, PGIMER Chandigarh and SCTIMST Trivandrum; separate from NEET-PG. Held twice a year (January and July sessions)",
)

# ---------- ACET December 2026 ----------
src = "Institute of Actuaries of India, 'ACET December 2026 - Registration Announcement (Home based Online Exam)' dated 23.07.2026: actuariesindia.org/sites/default/files/2026-07/Registration Announcement_ACET December 2026.pdf"
verify(AP, "ACET (Actuarial Common Entrance Test)", "2026-10-20", src,
    scope="National", stage="after_12", category="Actuarial science", body_type="Government",
    conducting_body="Institute of Actuaries of India (IAI), a statutory body", official_website="actuariesindia.org",
    full_form_body="Actuarial Common Entrance Test, conducted by the Institute of Actuaries of India: the entry test for IAI student membership",
    eligibility="Anyone who has passed 10+2 or a higher course, is studying a higher course, or has appeared for 10+2 and awaits results",
    application_window="December 2026 session (ACET37): registration 28 July 2026 (3 PM) - 4 November 2026 (3 PM) on actuariesindia.org. Fee Rs 500",
    exam_date="5 December 2026, 10 AM - 1 PM, online from home (licensed Windows 10+ laptop/desktop with webcam and microphone, Chrome, 5 Mbps wired/wifi; no tablets, phones, macOS or Linux, no mobile hotspot). Results 16 December 2026",
    admits_into="Student membership of the Institute of Actuaries of India, the start of the actuarial exams leading to Associate and Fellow; a non-ACET route also exists for some candidates",
)

# ---------- CLAT 2027 PG (LL.M.) ----------
src = "Consortium of NLUs, CLAT 2027 press release of 22.07.2026 (consortiumofnlus.ac.in/clat-2027/notifications/Press_Release_CLAT_2027.pdf) and CLAT 2027 PG pages pg-eligibility.html, pg-question-format.html (checked 20 Oct 2026)"
verify(AP, "CLAT-PG (LLM)", "2026-10-20", src,
    scope="National", stage="after_degree", category="Law (PG)", body_type="Government",
    conducting_body="Consortium of National Law Universities", official_website="consortiumofnlus.ac.in",
    full_form_body="Common Law Admission Test 2027, postgraduate paper, conducted by the Consortium of National Law Universities for LL.M. admission at the member NLUs",
    eligibility="LL.B. or equivalent with at least 50% marks (45% for SC/ST/PwD). Those appearing for the qualifying exam in 2027 may apply but must show proof of passing at admission. No upper age limit",
    application_window="Online 3 August 2026 - 31 October 2026 on consortiumofnlus.ac.in",
    exam_date="6 December 2026 (Sunday), 2 PM - 4 PM",
    admits_into="One-year LL.M. at the National Law Universities in the CLAT Consortium",
    exam_pattern="120 multiple-choice questions of 1 mark, 2 hours, 0.25 deducted per wrong answer. Constitutional Law, and other areas: Jurisprudence, Administrative Law, Contract, Torts, Family Law, Criminal Law, Property Law, Company Law, Public International Law, Tax Law, Environmental Law, Labour & Industrial Law",
)

# ---------- AILET 2027 ----------
src = "National Law University Delhi, Notification dated 23.07.2026 (nationallawuniversitydelhi.in/notification/AILET_2027.pdf) and Admission Announcement 2027-28 dated 07.08.2026 (.../notification/Admision Notice_AILET 2027.pdf)"
verify(AP, "AILET (All India Law Entrance Test)", "2026-10-20", src,
    scope="National", stage="after_12", category="Law", body_type="Government",
    conducting_body="National Law University Delhi", official_website="nationallawuniversitydelhi.in",
    full_form_body="All India Law Entrance Test 2027, conducted by National Law University Delhi for its own B.A.LL.B. (Hons.) and LL.M. (NLU Delhi does not take CLAT scores)",
    eligibility="B.A.LL.B.: 10+2 or equivalent with 45% (42% OBC, 40% SC/ST); Class 12 candidates of 2027 may apply. LL.M.: LL.B. with 50% (45% SC/ST/PwD); final-year LL.B. students of 2027 may apply",
    application_window="Online from 7 August 2026 to 10 November 2026 on nationallawuniversitydelhi.in. Fee Rs 3,000; Rs 1,000 for SC/ST/PwD; SC/ST and women candidates below the poverty line exempt",
    exam_date="13 December 2026 (Sunday), 2 PM - 4 PM. Test cities include Hyderabad and Visakhapatnam",
    admits_into="NLU Delhi only: Five-year B.A.LL.B. (Hons.), 110 seats on AILET merit (+5 foreign nationals, +5 OCI/PIO); one-year LL.M., 70 seats (+10). Ph.D. and other PG programmes use a separate test (AIET, 2 May 2027)",
)

# ---------- XAT 2027 ----------
src = "XLRI, XAT 2027 Bulletin (xatonline.in/assets/pdf/xat-bulletin-2027.pdf) and XAT 2027 FAQs (xatonline.in/faq), checked 20 Oct 2026"
verify(AP, "XAT (Xavier Aptitude Test)", "2026-10-20", src,
    scope="National", stage="after_degree", category="Management", body_type="Private",
    conducting_body="XLRI - Xavier School of Management, Jamshedpur (for XAMI)", official_website="xatonline.in",
    full_form_body="Xavier Aptitude Test 2027, conducted by XLRI Jamshedpur on behalf of the Xavier Association of Management Institutes",
    eligibility="A recognised Bachelor's degree of at least three years (or equivalent) in any discipline; final-year students finishing by 11 June 2027 may apply",
    application_window="XAT and XLRI registration 15 July - 6 December 2026 on xatonline.in. Fee Rs 2,300, plus Rs 200 for each XLRI programme",
    exam_date="3 January 2027 (Sunday), 2 PM - 5 PM. Admit card from 20 December 2026 (tentative). Result last week of January 2027; score card downloadable 31 January - 30 June 2027",
    admits_into="MBA/PGDM at XLRI and the XAMI member and associate institutes; the XAT score is accepted by over 250 institutes",
    exam_pattern="Computer-based, 3 hours, overall time limit only (no sectional timers); sections can be attempted in any order; on-screen scientific calculator available",
)

# ---------- SNAP 2026 (admissions 2027) ----------
src = "Symbiosis International (Deemed University), SNAP 2026 official pages: snaptest.org/snap-important-dates, /eligibility, /test-structure (checked 20 Oct 2026)"
verify(AP, "SNAP (Symbiosis National Aptitude Test)", "2026-10-20", src,
    scope="National", stage="after_degree", category="Management", body_type="Private",
    conducting_body="Symbiosis International (Deemed University)", official_website="snaptest.org",
    full_form_body="Symbiosis National Aptitude Test 2026, for M.B.A. admission (2027 intake) at 17 Symbiosis institutes",
    eligibility="Graduate from a recognised university / Institution of National Importance with at least 50% (45% for SC/ST); some programmes add their own conditions (see snaptest.org/eligibility)",
    application_window="SNAP 2026 registration and payment close 25 November 2026 (snaptest.org)",
    exam_date="Up to three attempts, best score counts: SNAP 01 on 13 Dec 2026, SNAP 02 on 19 Dec 2026, SNAP 03 on 26 Dec 2026 (admit cards 7, 11 and 18 Dec). Result 12 January 2027",
    admits_into="32 M.B.A. programmes at 17 Symbiosis institutes in Pune, Nashik, Nagpur, Hyderabad, Noida and Bengaluru, followed by each institute's own selection process",
    exam_pattern="Computer-based, 60 minutes, 60 questions of 1 mark: General English 10, Analytical & Logical Reasoning 20, Quantitative / Data Interpretation / Data Sufficiency 20, Ethics, Morality and Values 10. 25% negative marking",
)

# ---------- RRB JE: CEN 04/2026 ----------
src = "Railway Recruitment Boards, Detailed Centralised Employment Notice CEN No. 04/2026 (JE & DMS): rrbsecunderabad.gov.in/wp-content/uploads/2026/08/CEN-04-2026JE_English.pdf"
verify(AP, "RRB JE (Railway Recruitment Board - Junior Engineer)", "2026-10-20", src,
    scope="National", stage="jobs", category="Railway jobs", body_type="Government",
    conducting_body="Railway Recruitment Boards (RRBs)", official_website="rrbsecunderabad.gov.in",
    full_form_body="Recruitment of Junior Engineers and Depot Material Superintendents in Indian Railways through the Railway Recruitment Boards (CEN 04/2026)",
    eligibility="Three-year Diploma in Engineering, or B.E./B.Tech, in the branch mapped to each post (some JE posts also accept a 3-year B.Sc in Civil Engineering; DMS takes a diploma in any engineering branch). Must hold the qualification by 13.09.2026; those awaiting results could not apply. Age 18-33 on 01.01.2027, with category relaxations",
    application_window="CEN 04/2026: online 14.08.2026 - 13.09.2026 (closed). Fee Rs 500 (Rs 400 refunded on taking CBT-1); Rs 250 for SC, ST, ex-servicemen, PwBD, women, transgender, minorities and EBC (fully refunded on taking CBT-1)",
    exam_date="CBT, document verification and medical exam dates to be announced on the RRB websites",
    admits_into="3,993 posts of Junior Engineer and Depot Material Superintendent across Indian Railways; Pay Level 6, initial pay Rs 35,400",
    exam_pattern="CBT-1 (screening): 100 questions, 90 minutes: Mathematics 30, General Intelligence & Reasoning 25, General Awareness 15, General Science 30 (up to Class 10). CBT-2 (15x vacancies called): 150 questions, 120 minutes: General Awareness 15, Physics & Chemistry 15, Basics of Computers 10, Environment & Pollution Control 10, Technical Abilities 100 (by exam group: Civil, Electrical, Electronics, Mechanical and allied). 1/3 mark deducted per wrong answer. Then document verification and medical exam",
)
cutoffs(AP, "RRB JE (Railway Recruitment Board - Junior Engineer)", 2026, src, "2026-10-20", [
    ("UR / EWS", "40%", "Minimum in each CBT to be eligible"),
    ("OBC (NCL) / SC", "30%", "Minimum in each CBT to be eligible"),
    ("ST", "25%", "Minimum in each CBT to be eligible; PwBD may get 2 marks' relaxation if short of candidates"),
])

# ---------- IBPS CRP RRBs XV ----------
src = "IBPS Detailed Notification CRP RRBs XV dated 01.09.2026 (ibps.in/wp-content/uploads/CRP-RRBs-XV-notification_Revised.pdf), extension corrigendum 21.09.2026, Annexure I vacancies as on 25.09.2026 (from ibps.in/index.php/rural-bank-xv/)"
verify(AP, "IBPS RRB (Regional Rural Banks - CRP RRB)", "2026-10-20", src,
    scope="National", stage="jobs", category="Banking jobs", body_type="Government",
    conducting_body="Institute of Banking Personnel Selection (IBPS)", official_website="ibps.in",
    full_form_body="Common Recruitment Process for Officers (Scale I, II, III) and Office Assistants (Multipurpose) in Regional Rural Banks, CRP RRBs XV",
    eligibility="Office Assistant and Officer Scale I: a Bachelor's degree in any discipline, plus proficiency in the local language of the RRB; computer knowledge desirable (Scale I prefers agriculture, horticulture, veterinary, fisheries and related degrees). Age on 01.09.2026: Office Assistant 18-28, Officer Scale I 18-30, Scale II 21-32, Scale III 21-40; relaxation SC/ST 5 years, OBC-NCL 3, PwBD 10",
    application_window="Online 01.09.2026 - 27.09.2026 (extended from 21.09.2026; closed). Fee Rs 850, or Rs 175 for SC/ST/PwBD (and ESM/DESM for Office Assistant)",
    exam_date="Tentative: preliminary exam (Officer Scale I and Office Assistant) November/December 2026; main / single exam December 2026 / January 2027; Officer interviews January/February 2027. Exact dates on the call letters",
    admits_into="Office Assistant (Multipurpose) and Officer Scale I/II/III posts in Regional Rural Banks. Indicative vacancies (25.09.2026): Andhra Pradesh Grameena Bank 900 Office Assistant and 400 Officer Scale I; Telangana Grameena Bank 750 Office Assistant and 160 Officer Scale I",
    exam_pattern="Officer Scale I and Office Assistant: online preliminary, then main exam; Scale I also has an interview. Officer Scale II and III: a single online exam, then interview. Office Assistants are selected on the main exam alone",
)

# ---------- SSC CPO 2026 ----------
src = "Staff Selection Commission, Notice: Sub-Inspector in Delhi Police and Central Armed Police Forces Examination, 2026 (F. E/37/2026-C-2, uploaded 10.09.2026): ssc.gov.in/api/attachment/uploads/masterData/NoticeBoards/Notice_of_adv_capf_2026.pdf"
verify(AP, "SSC CPO (Central Police Organisation - Sub Inspector)", "2026-10-20", src,
    scope="National", stage="jobs", category="Police", body_type="Government",
    conducting_body="Staff Selection Commission (SSC)", official_website="ssc.gov.in",
    full_form_body="Sub-Inspector in Delhi Police and Central Armed Police Forces Examination, 2026 (SSC CPO), conducted by the Staff Selection Commission",
    eligibility="Bachelor's degree (SI in Delhi Police and SI (GD) in CAPFs); SI (Fire) in CISF needs a B.Sc with Physics, Chemistry and Maths, or Class 10 plus a 3-year engineering diploma in listed branches. Age on 01.08.2026: 20-25 (born 02.08.2001 - 01.08.2006); SI (Fire) 18-30. Male SI in Delhi Police must hold an LMV (motorcycle and car) driving licence by the PE&MT, otherwise CAPFs only",
    application_window="Online 10.09.2026 - 30.09.2026 (closed); corrections 08-10.10.2026. Fee Rs 100; women, SC, ST and eligible ex-servicemen exempt",
    exam_date="Paper-I (computer based): schedule to be notified by SSC",
    admits_into="1,871 tentative posts at Pay Level 6 (Rs 35,400-1,12,400): SI (Executive) Delhi Police 205 male + 112 female; SI (GD) in CAPFs (CRPF, BSF, ITBP, CISF, SSB) 1,320; SI (Fire) CISF 234. Liable to serve anywhere in India",
    exam_pattern="Paper-I (100 questions, 100 marks: Reasoning, General Knowledge, Quantitative Aptitude, English, 25 each), then PST/PET, Paper-II, and detailed medical exam; all stages compulsory. 0.25 deducted per wrong answer in Paper-I, 0.50 in Paper-II. Exam centres in AP include Guntur, Kurnool, Rajahmundry, Tirupati, Visakhapatnam, Vijayawada and Kakinada",
)

# ---------- FMGE October 2026 ----------
src = "NBEMS Information Bulletin, FMGE October 2026 v2.2 (nbe.edu.in/IB/FMGE october 2026 information bulletin v2.2.pdf) and NBEMS notice dated 19.10.2026 on test city allocation and deficient documents (natboard.edu.in, Public Notices)"
verify(AP, "FMGE (Foreign Medical Graduate Examination)", "2026-10-20", src,
    official_website="natboard.edu.in",
    full_form_body="Foreign Medical Graduate Examination, the screening test under the Screening Test Regulations, 2002, conducted by the National Board of Examinations in Medical Sciences (NBEMS); now held three times a year",
    eligibility="Indian citizens / OCI holding a primary medical qualification from a medical institution outside India, with the documents the bulletin lists (Primary Medical Qualification certificate attested or apostilled, Eligibility Certificate or admission letter, proof of citizenship). Only candidates with both the Eligibility Certificate (if applicable) and the pass / degree certificate may appear",
    application_window="October 2026 session: online 11.09.2026 - 25.09.2026 (closed). Deficient documents and images can be fixed until 21.10.2026, 11:55 PM. Fee Rs 4,650 (Rs 3,940.68 + 18% GST)",
    exam_date="31 October 2026; test city shown in applicant login from 20.10.2026; admit cards 27.10.2026. The previous session was on 28.06.2026",
    admits_into="Eligibility for provisional or permanent registration with the National Medical Commission or a State Medical Council, needed to practise medicine in India with a foreign medical degree. It is a pass/fail licensing test, not an admission test",
    exam_pattern="One computer-based paper of 300 multiple-choice questions in two parts of 150 questions (150 minutes each) on the same day, English only. Pass: at least 150 of 300. Part-wise marks are not published; no re-totalling, re-evaluation or grace marks",
)
cutoffs(AP, "FMGE (Foreign Medical Graduate Examination)", 2026, src, "2026-10-20", [
    ("All", "150 of 300", "Minimum to pass"),
])

# ---------- NEET-PG (2026 cycle; 2027 not yet notified) ----------
src = "NBEMS Information Bulletin, NEET-PG 2026 (linked from natboard.edu.in NEET-PG page); NBEMS notices: result declared 24.09.2026, scorecard 01.10.2026. No NEET-PG 2027 bulletin on natboard.edu.in as of 20 Oct 2026"
verify(AP, "NEET-PG (National Eligibility cum Entrance Test - Postgraduate)", "2026-10-20", src,
    official_website="natboard.edu.in",
    full_form_body="National Eligibility cum Entrance Test for postgraduate medical courses (MD/MS/PG Diploma, DNB), conducted by the National Board of Examinations in Medical Sciences (NBEMS)",
    eligibility="As in NEET-PG 2026: an MBBS degree or provisional pass certificate recognised under the NMC Act, permanent or provisional MBBS registration with the NMC / a State Medical Council, and one year's internship completed by the cut-off date (30.09.2026 for the 2026 cycle)",
    application_window="NEET-PG 2027: not yet notified (no bulletin on natboard.edu.in as of 20 Oct 2026). The 2026 cycle's window was 01.07.2026 - 21.07.2026; fee Rs 3,500 General/OBC/EWS, Rs 2,500 SC/ST/PwBD",
    exam_date="NEET-PG 2027: not yet announced. NEET-PG 2026 was held on 30.08.2026; result declared 24.09.2026",
    admits_into="MD, MS, PG Diploma and DNB seats across India (all-India and state quota counselling). AIIMS, JIPMER, PGIMER, NIMHANS and SCTIMST admit through INI-CET instead",
    exam_pattern="NEET-PG 2026: computer-based, 180 MCQs, 3 hours 30 minutes, five time-bound sections (A-E) of 36 questions and 42 minutes each; +4 for a correct answer, -1 for a wrong one, English only",
)
cutoffs(AP, "NEET-PG (National Eligibility cum Entrance Test - Postgraduate)", 2026, src, "2026-10-20", [
    ("General / EWS", "50th percentile", "Minimum qualifying percentile, as notified in the bulletin (may be lowered later by the government)"),
    ("UR PwBD", "45th percentile", "Minimum qualifying percentile"),
    ("SC / ST / OBC (incl. their PwBD)", "40th percentile", "Minimum qualifying percentile"),
], kind="qualifying_percentile")

# ---------- NEET-SS (2025 cycle is the latest; 2026 not yet notified) ----------
src = "NBEMS Information Bulletin, NEET-SS 2025 (nbe.edu.in/IB/NEET-SS 2025 information bulletin.pdf); NBEMS notice of 22.09.2026 reducing the NEET-SS 2025 qualifying percentile. No NEET-SS 2026 bulletin on natboard.edu.in as of 20 Oct 2026"
verify(AP, "NEET-SS (NEET Super Specialty)", "2026-10-20", src,
    official_website="natboard.edu.in",
    full_form_body="National Eligibility cum Entrance Test - Super Specialty, conducted by NBEMS for DM, MCh and DrNB super-specialty courses",
    eligibility="As in NEET-SS 2025: a recognised MD / MS / DNB (or provisional pass certificate) in the eligible feeder specialty for the chosen question-paper group, held by the cut-off date (31.01.2026 for the 2025 cycle)",
    application_window="NEET-SS 2026: not yet notified (no bulletin on natboard.edu.in as of 20 Oct 2026). The 2025 cycle's window was 05.11.2025 - 25.11.2025; fee Rs 3,500 per question-paper group",
    exam_date="NEET-SS 2026: not yet announced. NEET-SS 2025 was held on 26-27.12.2025, result by 28.01.2026; its counselling was still running in Sept 2026",
    admits_into="DM / MCh seats in all medical colleges (including private and armed forces) and DrNB super-specialty seats. Not used by AIIMS, PGIMER, JIPMER, NIMHANS or SCTIMST (they run INI-SS)",
)

# ---------- GPAT (2026 cycle; 2027 not yet notified) ----------
src = "NBEMS Information Bulletin, GPAT 2026 (nbe.edu.in/IB/Information bulletin GPAT 2026.pdf). No GPAT 2027 bulletin on natboard.edu.in as of 20 Oct 2026"
verify(AP, "GPAT (Graduate Pharmacy Aptitude Test)", "2026-10-20", src,
    official_website="natboard.edu.in",
    full_form_body="Graduate Pharmacy Aptitude Test, conducted by the National Board of Examinations in Medical Sciences (NBEMS) for M.Pharm admission",
    eligibility="As in GPAT 2026: a B.Pharm degree (including lateral entry) from a recognised institution. Final-year (4th year) B.Pharm students may appear; 3rd-year students may also appear, for 2027-28 admission",
    application_window="GPAT 2027: not yet notified (no bulletin on natboard.edu.in as of 20 Oct 2026). GPAT 2026 fee: Rs 3,500 General/OBC/EWS, Rs 2,500 SC/ST/PwD",
    exam_date="GPAT 2027: not yet announced. GPAT 2026 was held on 07.03.2026, result by 07.04.2026",
    admits_into="M.Pharm (and some PhD) admissions at AICTE-approved institutions; the score is valid for three years",
    exam_pattern="GPAT 2026: computer-based, 125 MCQs, 500 marks, 3 hours, five timed sections of 25 questions (36 minutes each); +4 / -1. Pharmaceutical Chemistry 38 questions, Pharmaceutics 38, Pharmacognosy 10, Pharmacology 28, other B.Pharm subjects 11",
)

# ---------- CMAT (2026 cycle; 2027 not yet notified) ----------
src = "NTA Information Bulletin, CMAT-2026 (cdnbbsr.s3waas.gov.in/s3a381c2c35c9157f6b67fd07d5a200ae1/uploads/2025/10/202510171049586023.pdf) and NTA admit card notice 21.01.2026; cmat.nta.nic.in shows no CMAT-2027 notice as of 20 Oct 2026"
verify(AP, "CMAT (Common Management Admission Test)", "2026-10-20", src,
    official_website="cmat.nta.nic.in",
    full_form_body="Common Management Admission Test, conducted by the National Testing Agency (NTA) for admission to AICTE-approved management programmes",
    eligibility="A Bachelor's degree in any discipline (final-year students whose result comes before admission may apply); Indian citizens; no age limit",
    application_window="CMAT 2027: not yet notified on cmat.nta.nic.in (as of 20 Oct 2026). Last cycle: 17.10.2025 - 17.11.2025. Fee (2026): Rs 2,500 General male; Rs 1,250 for women, Gen-EWS, SC, ST, PwD, OBC-NCL and third gender",
    exam_date="CMAT 2027: not yet announced. CMAT 2026 was held on 25.01.2026 (CBT, 9 AM - 12 noon)",
    admits_into="MBA/PGDM at AICTE-approved institutions, university departments and affiliated colleges that accept CMAT; each sets its own cut-off, followed by GD/PI",
    exam_pattern="Computer-based, 180 minutes, English only, 100 questions, 400 marks: Quantitative Techniques & Data Interpretation, Logical Reasoning, Language Comprehension, General Awareness, Innovation & Entrepreneurship (20 questions, 80 marks each)",
)

# ---------- NMAT by GMAC 2026 ----------
src = "GMAC, NMAT by GMAC exam page: mba.com/exams/nmat (checked 20 Oct 2026)"
verify(AP, "NMAT by GMAC", "2026-10-20", src,
    official_website="mba.com/exams/nmat",
    full_form_body="NMAT by GMAC, a computer-adaptive management entrance test owned and run by the Graduate Management Admission Council (GMAC)",
    eligibility="Not stated on the official exam page; check the criteria of each NMAT-accepting school",
    application_window="Current testing year: registration and scheduling 20 August - 25 October 2026 on mba.com",
    exam_date="Flexible testing window 2 November - 20 December 2026 at test centres in 70+ Indian cities; up to 3 attempts, best score sent. Unofficial score shown instantly; scorecard within 48 hours",
    admits_into="MBA and management programmes at 58+ NMAT-accepting B-schools (including NMIMS)",
    exam_pattern="Computer-adaptive, no negative marking, equal weight for all sections, candidate chooses the section order",
)


# =====================================================================
# Batch 2026-10-26: exams from the 10-20..10-25 deltas, each checked
# against its own official document (the deltas cited aggregators only).
# =====================================================================

# ---------- Joint CSIR-UGC NET December 2026 ----------
src = "NTA Information Bulletin, Joint CSIR-UGC NET December 2026 (cdnbbsr.s3waas.gov.in/s3efdf562ce2fb0ad460fd8e9d33e57f57/uploads/2026/10/202610071407707951.pdf) and public notice of 07.10.2026 inviting applications, both on csirnet.nta.nic.in"
verify(AP, "CSIR NET (CSIR-UGC NET for Science)", "2026-10-26", src,
    scope="National", stage="after_degree", category="Research & teaching (PG)", body_type="Government",
    conducting_body="National Testing Agency (NTA), for CSIR and UGC", official_website="csirnet.nta.nic.in",
    full_form_body="Joint CSIR-UGC National Eligibility Test, conducted by NTA, for Junior Research Fellowship (JRF), appointment as Assistant Professor and Ph.D. admission in five science subjects: Chemical Sciences; Earth, Atmospheric, Ocean and Planetary Sciences; Life Sciences and Biotechnology; Mathematical Sciences; Physical Sciences",
    eligibility="Master's degree or equivalent with at least 55% (50% for OBC-NCL, SC, ST, PwBD and third gender), no rounding off; final-year Master's students may apply provisionally. JRF: not more than 30 years as on 1 December 2026, relaxable up to 5 years for OBC-NCL, SC, ST, PwBD, third gender and women. No upper age limit for Assistant Professor or Ph.D. admission",
    application_window="December 2026: online 07.10.2026 - 05.11.2026 (11:50 PM) on csirnet.nta.nic.in. With Rs 500 late fee: 06.11.2026 - 09.11.2026. Corrections 10-12.11.2026. Fee Rs 1,150 General; Rs 600 General-EWS/OBC-NCL; Rs 325 SC/ST/PwBD/third gender",
    exam_date="19, 22 and 27 December 2026, Computer Based Test, 3 hours; shift 1 9 AM - 12 noon, shift 2 3 PM - 6 PM. City slip and admit card dates to be announced",
    admits_into="Junior Research Fellowship (with eligibility for Assistant Professor and Ph.D.), Assistant Professor eligibility with Ph.D. admission, or Ph.D. admission only, depending on the category you qualify in",
    exam_pattern="One objective paper in your subject with Parts A (general aptitude), B and C (subject). Each paper has a set number of questions to answer per part (e.g. Chemical, Earth, Life and Physical Sciences: 15, 35 and 25). Negative marking of 25% in most parts; none in Part C of Mathematical Sciences, where all correct options must be marked",
)

# ---------- ICSI CSEET February 2027 ----------
src = "ICSI: 'Restructured CSEET' page (icsi.edu/restructured-cseet, updated 21.10.2026: registration for February 2027 session, last date 31.10.2026); Time Table for CSEET February 2027 (cms_uploads/cseet-time-table-february2027-07551067.pdf, dated 07.10.2026); Announcement on restructuring of CSEET effective June 2026 and CSEET FAQs (both dated 08.09.2026)"
verify(AP, "ICSI CSEET (Company Secretary Executive Entrance Test)", "2026-10-26", src,
    conducting_body="The Institute of Company Secretaries of India (ICSI)", official_website="icsi.edu/cseet",
    full_form_body="Company Secretary Executive Entrance Test, conducted by the Institute of Company Secretaries of India: the entry test for the CS course (restructured from June 2026, held at exam centres three times a year: February, June and October)",
    eligibility="Indian nationals who have passed or are appearing in Class 12 (10+2) or equivalent. Exempted (can register straight for CS Executive): graduates and post-graduates, final-year UG students (provisional), CS Foundation passed, CA Intermediate passed, CMA Final passed, and 5-year integrated programme students who have passed or are in the 6th semester. Completing the Student Induction Programme is required before exam enrolment",
    application_window="February 2027 session: registration 1 July - 31 October 2026 on icsi.edu (smash.icsi.edu). Registrations from 1 November count for the June session. Fee Rs 7,500 at registration (includes Student Induction Programme and online classes) plus Rs 1,500 exam fee per session; 50% concession for SC/ST and PwD",
    exam_date="February 2027 session, at exam centres, 2 PM onwards (15 minutes' reading time): 1 Feb 2027 Business Communication; 2 Feb Fundamentals of Accounting; 3 Feb Economic and Business Environment; 4 Feb Business Laws and Management (OMR)",
    admits_into="Registration for the CS Executive Programme (within one year of the CSEET result), the next stage towards becoming a Company Secretary",
    exam_pattern="Four papers of 100 marks each: Business Communication, Fundamentals of Accounting, Economic and Business Environment (3 hours each, subjective) and Business Laws and Management (2 hours, OMR: Business Laws 60 + Business Management 40). Pass: at least 40% in each paper and 50% aggregate in one sitting",
)
cutoffs(AP, "ICSI CSEET (Company Secretary Executive Entrance Test)", 2027, src, "2026-10-26", [
    ("All", "40% in each paper, 50% aggregate", "In one sitting; no exemptions or carry-forward of marks"),
])

# ---------- IIT JAM 2027 ----------
src = "JAM 2027 website, IIT Kharagpur (organising institute): jam.iitkgp.ac.in home page (important dates), test-schedule.html and exam-eligibilityreq.html, checked 26 Oct 2026"
verify(AP, "IIT JAM (Joint Admission Test for M.Sc.)", "2026-10-26", src,
    scope="National", stage="after_degree", category="University PG admissions", body_type="Government",
    conducting_body="IIT Kharagpur (organising institute for JAM 2027)", official_website="jam.iitkgp.ac.in",
    full_form_body="Joint Admission Test for Masters (JAM) 2027, organised by IIT Kharagpur, for M.Sc. and other postgraduate science programmes at the IITs and other participating institutes",
    eligibility="Anyone who has completed an undergraduate degree, or is appearing for the final exam of the qualifying degree in 2027. The degree must be completed before admission, and each admitting institute sets its own minimum-marks requirement",
    application_window="JAM 2027: online application opened 11 September 2026 and closed 24 October 2026 (extended last date). Applications are now closed",
    exam_date="14 February 2027 (Sunday), computer based. Forenoon 9:30 AM - 12:30 PM: Chemistry, Geology, Mathematics. Afternoon 2:30 PM - 5:30 PM: Biotechnology, Economics, Mathematical Statistics, Physics. You can take one paper, or two if they are in different sessions. Results 18 March 2027. No exam centres outside India",
    admits_into="M.Sc., joint M.Sc.-Ph.D., M.Sc.-Ph.D. dual degree and similar postgraduate science programmes at the IITs and other institutes that admit through JAM",
)

# ---------- UPSC CAPF (Assistant Commandants) 2026 ----------
src = "UPSC Examination Notice No. 08/2026-CAPF dated 20.02.2026 (upsc.gov.in/sites/default/files/ExamNotifi_CAPF_AC_Exam_2026_Eng_20022026.pdf), press note 10.07.2026, time-table, notice 08.09.2026 (PST/PET document window) and UPSC Annual Calendar 2027 (Calendar-Year-2027-Engl-200526.pdf)"
verify(AP, "UPSC CAPF (AC) Exam", "2026-10-26", src,
    scope="National", stage="jobs", category="Police", body_type="Government",
    conducting_body="Union Public Service Commission (UPSC)", official_website="upsc.gov.in",
    full_form_body="Central Armed Police Forces (Assistant Commandants) Examination, conducted by UPSC, for Group 'A' Assistant Commandant posts in BSF, CRPF, CISF, ITBP and SSB",
    eligibility="A Bachelor's degree (final-year students may apply). Age 20-25 on 1 August of the exam year (2026 exam: born 02.08.2001 - 01.08.2006); relaxations as per rules. Physical and medical standards apply",
    application_window="2026 exam: online until 12 March 2026 (closed). Fee Rs 200; women, SC and ST exempt. 2027 exam: per the UPSC calendar, exam on 4 July 2027; notification and application dates will be in the 2027 notice on upsc.gov.in",
    exam_date="2026 written exam held 19 July 2026 (written result 25 August 2026); qualified candidates are now in the Physical Standards / Physical Efficiency Test stage, followed by interview (150 marks) and medical. Next written exam: 4 July 2027 (UPSC calendar)",
    admits_into="Assistant Commandant (Group A) in the Central Armed Police Forces. 2026 vacancies: BSF 108, CRPF 106, CISF 70, SSB 53, ITBP 12 (349, tentative)",
    exam_pattern="Paper I: General Ability and Intelligence, 250 marks, objective, 10 AM - 12 noon. Paper II: General Studies, Essay and Comprehension, 200 marks, conventional, 2 PM - 5 PM. Then Physical Standards / Physical Efficiency Tests (qualifying), interview / personality test (150 marks) and medical standards tests",
)

# ---------- Indian Forest Service Examination ----------
src = "UPSC Examination Notice No. 06/2026-IFoSE dated 04.02.2026 (upsc.gov.in/sites/default/files/Notif-IFSP-2026-Engl-060226Rev.pdf), IFoS (Main) 2026 time-table (TT-IFSM-26-Engl-170926.pdf) and UPSC Annual Calendar 2027 (Calendar-Year-2027-Engl-200526.pdf)"
verify(AP, "IFoS (Indian Forest Service Examination)", "2026-10-26", src,
    conducting_body="Union Public Service Commission (UPSC)", official_website="upsc.gov.in",
    full_form_body="Indian Forest Service Examination, conducted by UPSC: the preliminary stage is the Civil Services (Preliminary) Examination, followed by a separate IFoS Main exam and interview",
    eligibility="A Bachelor's degree with at least one of Animal Husbandry & Veterinary Science, Botany, Chemistry, Geology, Mathematics, Physics, Statistics or Zoology, or a Bachelor's degree in Agriculture, Forestry or Engineering. Age 21-32 on 1 August of the exam year (2026: born 02.08.1994 - 01.08.2005); relaxations as per rules. Six attempts (nine for OBC; no limit for SC/ST)",
    application_window="2027 exam (UPSC calendar): notification 13 January 2027, apply by 2 February 2027 on upsc.gov.in. 2026 exam: applied by 24 February 2026, fee Rs 100 (women, SC, ST and PwBD exempt)",
    exam_date="2027: Preliminary (through the Civil Services Prelims) 23 May 2027; Main from 21 November 2027 (7 days). 2026 Main exam is on 22-29 November 2026",
    admits_into="Indian Forest Service (IFS), an All India Service managing forests and wildlife; about 80 vacancies in 2026",
)

# ---------- APPSC Forest Range Officer (Notification 16/2026) ----------
src = "APPSC Notification No. 16/2026 dated 16.10.2026, Forest Range Officer in A.P. Forest Service (psc.ap.gov.in/Documents/NotificationDocuments/FRODetailedNotification_162026.pdf) and web note of 16.10.2026"
verify(AP, "APPSC Forest Range Officer", "2026-10-26", src,
    conducting_body="Andhra Pradesh Public Service Commission (APPSC)", official_website="psc.ap.gov.in",
    full_form_body="Direct recruitment to the post of Forest Range Officer in the A.P. Forest Service, conducted by APPSC",
    eligibility="A Bachelor's degree in Agriculture, Botany, Chemistry, Computer Applications/Computer Science, Engineering (Agriculture, Chemical, Civil, Computer, Electrical, Electronics or Mechanical), Environmental Science, Forestry, Geology, Horticulture, Mathematics, Physics, Statistics, Veterinary Science or Zoology. Age 18-30 on 01.07.2026; relaxations as per rules. Physical standards: men at least 163 cm, chest 79 cm, walk 25 km in 4 hours; women at least 150 cm, chest 74 cm, walk 16 km in 4 hours",
    application_window="Online 16.10.2026 - 05.11.2026 (11:59 PM) on psc.ap.gov.in (OTPR registration needed). Fee Rs 250 processing + Rs 120 exam fee; exam fee waived for SC, ST, BC, ex-servicemen and white-card families of AP",
    exam_date="Computer based test; date to be announced by APPSC",
    admits_into="Forest Range Officer, A.P. Forest Service: 5 posts (including 1 carried forward), pay Rs 48,440 - 1,37,220",
    exam_pattern="Degree-standard objective exam: qualifying test in General English (50) and General Telugu (50); then Paper I General Studies & Mental Ability, Paper II Mathematics (SSC standard), Paper III General Forestry I, Paper IV General Forestry II, 150 marks each (600 total). 1/3 mark deducted for each wrong answer. Then a walking test and medical exam by the Forest Department",
)
cutoffs(AP, "APPSC Forest Range Officer", 2026, src, "2026-10-26", [
    ("OC / EWS / Sportspersons / Ex-Servicemen", "40%", "Minimum aggregate to be considered for selection"),
    ("BC", "35%", "Minimum aggregate to be considered for selection"),
    ("SC / ST", "30%", "Minimum aggregate to be considered for selection"),
])

# ---------- IBPS SO (CRP SPL-XVI) ----------
src = "IBPS Detailed Notification CRP SPL-XVI dated 30.06.2026 (ibps.in/wp-content/uploads/Detailed-Notification-CRP-SPL-XVI_Final_V1_30.06.2026.pdf), corrigendum of 20.07.2026 (updated vacancies), combined schedule for CRP PO/MT-XVI and SPL-XVI, and the CRP SPL-XVI page on ibps.in (prelim scores and main call letters out), checked 26 Oct 2026"
verify(AP, "IBPS SO (Specialist Officer, CRP SPL)", "2026-10-26", src,
    scope="National", stage="jobs", category="Banking jobs", body_type="Government",
    conducting_body="Institute of Banking Personnel Selection (IBPS)", official_website="ibps.in",
    full_form_body="Common Recruitment Process for Specialist Officers (CRP SPL-XVI, vacancies of 2027-28) in participating public sector banks, conducted by IBPS",
    eligibility="Age 20-30 on 01.07.2026 (born 02.07.1996 - 01.07.2006); relaxations as per rules. Qualification by post: IT Officer (4-year B.E./B.Tech in CS/IT/electronics branches, or a related PG degree), Agricultural Field Officer (4-year degree in agriculture and allied fields), Rajbhasha Adhikari (PG in Hindi with English, or the reverse), Law Officer (LL.B. and enrolled with the Bar Council), HR/Personnel Officer and Marketing Officer (graduate plus a 2-year full-time PG in the field)",
    application_window="CRP SPL-XVI: online 01.07.2026 - 21.07.2026 (closed). Fee Rs 850; Rs 175 for SC/ST/PwBD",
    exam_date="Preliminary exam held (scores published); Online Main exam call letters issued. Interviews November/December 2026; provisional allotment January 2027 (IBPS tentative schedule)",
    admits_into="Scale-I specialist officer posts in public sector banks: IT Officer, Agricultural Field Officer, Rajbhasha Adhikari, Law Officer, HR/Personnel Officer, Marketing Officer. Indicative vacancies in Annexure-I (updated 20.07.2026)",
    exam_pattern="Online Preliminary (100 questions, 125 marks): English, Reasoning and Quantitative Aptitude (General Awareness on Banking instead of Quant for Law Officer and Rajbhasha Adhikari). Online Main: professional knowledge test of the post (Rajbhasha Adhikari: objective plus descriptive). Then interview",
)

# ---------- CUET (PG) ----------
src = "NTA CUET (PG) page exams.nta.nic.in/cuet-pg (notices for CUET (PG)-2026; no CUET (PG)-2027 notice as of 26 Oct 2026)"
verify(AP, "CUET-PG (Common University Entrance Test - Postgraduate)", "2026-10-26", src,
    scope="National", stage="after_degree", category="University PG admissions", body_type="Government",
    conducting_body="National Testing Agency (NTA)", official_website="exams.nta.nic.in/cuet-pg",
    full_form_body="Common University Entrance Test for Postgraduate Programmes, conducted by NTA for admission to PG programmes at central and other participating universities",
    eligibility="Set by each participating university for each PG programme (usually a relevant Bachelor's degree); not yet available for the 2027 cycle",
    application_window="CUET (PG)-2027 not yet notified as of 26 Oct 2026; watch exams.nta.nic.in/cuet-pg",
    exam_date="Not yet announced for 2027. CUET (PG)-2026 was held on 6-27 March 2026 (computer based)",
    admits_into="Master's programmes at central universities (such as University of Hyderabad and Central University of Andhra Pradesh) and other participating universities",
)


def src_of(state, exam):
    """The verified row's own source: the subjects come from the same document."""
    return (VERIFIED_ROWS.get((state, exam)) or _SEED_EXAMS[(state, exam)])["source"]


V = "2026-10-12"

src = ("GATE 2027 Information Brochure (IIT Madras), General Aptitude syllabus: gate2027ib.iitm.ac.in/GATE2027-IB.pdf; "
       "paper syllabi: gate2027.iitm.ac.in/exam_papers_and_syllabus (CE, ME, EE, EC, CS, CH); marks split: gate2027.iitm.ac.in/question_paper_pattern")
subjects(AP, "GATE", src, V, [
    ("General Aptitude (common to all 30 papers, 15 marks)",
     "Verbal aptitude: basic English grammar, vocabulary in context, reading comprehension, narrative sequencing; "
     "Quantitative aptitude: data interpretation from bar and pie charts, 2D and 3D plots, maps and tables, ratios, percentages, powers, exponents and logarithms, permutations and combinations, series, mensuration and geometry, elementary statistics and probability; "
     "Analytical aptitude: deduction and induction, analogy, numerical relations and reasoning; "
     "Spatial aptitude: translation, rotation, scaling, mirroring, assembling and grouping of shapes, paper folding, cutting and patterns in 2D and 3D"),
    ("Engineering Mathematics (13 marks in most engineering papers; topics differ by paper)",
     "Linear algebra (matrices, systems of equations, eigenvalues and eigenvectors); calculus (limits, continuity, mean value theorems, maxima and minima, definite integrals, partial derivatives, vector calculus); "
     "differential equations; probability and statistics; numerical methods; complex variables in some papers; discrete mathematics (logic, sets, graphs, combinatorics) in the CS paper"),
    ("Civil Engineering paper (CE)",
     "Structural engineering (engineering and solid mechanics, structural analysis, concrete and steel structures); geotechnical engineering; water resources engineering; environmental engineering; transportation engineering; geomatics engineering; construction materials and management"),
    ("Mechanical Engineering paper (ME)",
     "Applied mechanics and design (engineering mechanics, mechanics of materials, theory of machines, vibrations, machine design); fluid mechanics and thermal sciences (fluid mechanics, heat transfer, thermodynamics, applications); materials, manufacturing and industrial engineering"),
    ("Electrical Engineering paper (EE)",
     "Electric circuits; electromagnetic fields; signals and systems; electrical machines; power systems; control systems; electrical and electronic measurements; analog and digital electronics; power electronics"),
    ("Electronics & Communication Engineering paper (EC)",
     "Networks, signals and systems; electronic devices; analog circuits; digital circuits; control systems; communications; electromagnetics"),
    ("Computer Science & Information Technology paper (CS)",
     "Digital logic; computer organisation and architecture; programming and data structures; algorithms; theory of computation; compiler design; operating systems; databases; computer networks"),
    ("Chemical Engineering paper (CH)",
     "Process calculations; thermodynamics; fluid mechanics and mechanical operations; heat transfer; mass transfer; chemical reaction engineering; instrumentation and process control; plant design and economics; chemical technology"),
    ("Other papers (AE, AG, AR, BM, BT, CY, DA, ES, EY, GE, GG, IN, MA, MN, MT, NM, PE, PH, PI, RA, ST, XE, XH, XL)",
     "Each has its own syllabus PDF on gate2027.iitm.ac.in/exam_papers_and_syllabus; most engineering papers also include the 13-mark Engineering Mathematics section"),
])

src = "CUET (UG) 2026 Information Bulletin (NTA), Broad features, Scheme of Examination and Appendix II: cdnbbsr.s3waas.gov.in/s3d1a21da7bca4abff8b0b61b87597de73/uploads/2026/01/202601031633478370.pdf (from cuet.nta.nic.in)"
subjects(AP, "CUET-UG", src, V, [
    ("Languages (13, including English, Hindi, Telugu, Tamil, Kannada and Urdu)",
     "Reading comprehension of factual, literary and narrative passages; literary aptitude; vocabulary"),
    ("Domain subjects (23; take the ones your university programme asks for)",
     "Questions follow the NCERT Class 12 syllabus of the subject: Accountancy, Agriculture, Anthropology, Biology, Business Studies, Chemistry, Computer Science, Economics, Environmental Science, Fine Arts, Geography, History, Home Science, Knowledge Tradition, Mass Media, Mathematics / Applied Mathematics, Performing Arts, Physical Education, Physics, Political Science, Psychology, Sanskrit, Sociology"),
    ("General Aptitude Test",
     "General knowledge, current affairs, general mental ability, numerical ability, quantitative reasoning (arithmetic, algebra, geometry, mensuration, statistics), logical and analytical reasoning"),
])

src = ("ICAI Board of Studies, Foundation study material (new scheme, applicable for May 2026 exams onwards), chapter lists: "
       "boslive.icai.org/study_material_new_paper_details.php?c=foundation and icai.org/post/19139 (Paper 3); papers 3 and 4 are 2 hours, papers 1 and 2 are 3 hours (ICAI Announcement 13-CA(EXAM)/2026)")
subjects(AP, "CA Foundation", src, V, [
    ("Paper 1: Accounting (3 hours)",
     "Theoretical framework; accounting process; bank reconciliation statement; inventories; depreciation and amortisation; bills of exchange and promissory notes; final accounts of sole proprietors; not-for-profit organisations; accounts from incomplete records; partnership and LLP accounts; company accounts"),
    ("Paper 2: Business Laws (3 hours)",
     "Indian regulatory framework; Indian Contract Act, 1872; Sale of Goods Act, 1930; Indian Partnership Act, 1932; Limited Liability Partnership Act, 2008; Companies Act, 2013; Negotiable Instruments Act, 1881"),
    ("Paper 3: Quantitative Aptitude (2 hours)",
     "Part A Business Mathematics: ratio and proportion, indices, logarithms, equations, linear inequalities, mathematics of finance, permutations and combinations, sequences and series, sets, relations and functions, limits and continuity, differential and integral calculus in business; "
     "Part B Logical Reasoning: number series, coding and decoding, odd man out, direction sense, seating arrangements, blood relations; "
     "Part C Statistics: statistical description of data and sampling, central tendency and dispersion, probability, theoretical distributions, correlation and regression, index numbers"),
    ("Paper 4: Business Economics (2 hours)",
     "Nature and scope of business economics; demand and supply; production and cost; price determination in different markets; business cycles; national income; public finance; money market; international trade; Indian economy"),
])

src = "NATA 2026 Brochure (Council of Architecture), section 4 'Questions & Marks of Examination': nata.in/assets/pdf/Final-NATA-BROCHURE-2026.pdf"
subjects(AP, "NATA", src, V, [
    ("Part A: Drawing and Composition Test (offline, 90 minutes, 80 marks)",
     "A1 Composition and colour (25 marks): compositions for given situations, rearranging shapes and colouring them; A2 Sketching and composition in black and white (25 marks): drawing buildings, people, environment and products with scale, proportion, texture, shade and shadow; A3 3D composition (30 marks) with the kit provided"),
    ("Part B: MCQ and NCQ (computer-based adaptive, 90 minutes, 42 MCQs + 8 NCQs, 120 marks)",
     "Visual reasoning (2D and 3D composition); logical derivation; general knowledge of architecture and design (important buildings, history, materials and construction technology, current issues); language interpretation and English grammar; design sensitivity and thinking; numerical ability (basic mathematics and geometry)"),
])

src = "ICAR AIEEA (PG)-2026 Information Bulletin (NTA), sections 2.1-2.4 and Annexure III: cdnbbsr.s3waas.gov.in/s388a839f2f6f1427879fc33ee4acf4f66/uploads/2026/05/202605091397132773.pdf"
subjects(AP, "ICAR AIEEA", src, V, [
    ("One Major Subject-Group paper (120 MCQs, 2 hours, +4 / -1)",
     "Choose one of 20 Major Subject-Groups matching your degree: Plant Biotechnology, Plant Sciences, Physical Science, Entomology and Nematology, Agronomy, Social Sciences, Statistical Sciences, Horticulture, Forestry, Agricultural Engineering and Technology, Community Science, Animal Biotechnology, Veterinary Science, Animal Sciences, Fisheries Science, Dairy Science, Dairy Technology, Food Science Technology, Agri Business Management, Water Science and Technology. Syllabus for each on icar.org.in/node/21053"),
])

src = src_of(AP, "BITSAT") + "; syllabus: Annexure-1 of the same brochure"
subjects(AP, "BITSAT", src, V, [
    ("Physics (30 questions)",
     "Units and measurement; kinematics; Newton's laws; impulse and momentum; work and energy; rotational motion; gravitation; mechanics of solids and fluids; oscillations; waves; heat and thermodynamics; electrostatics; current electricity; magnetic effect of current; electromagnetic induction; optics; modern physics; electronic devices"),
    ("Chemistry (30 questions)",
     "States of matter; atomic structure; periodicity and bonding; thermodynamics; physical and chemical equilibria; electrochemistry; chemical kinetics; hydrogen and s-block elements; p-, d- and f-block elements; principles of organic chemistry and hydrocarbons; stereochemistry; organic compounds with oxygen and nitrogen; biological, industrial and environmental chemistry; theoretical principles of experimental chemistry"),
    ("English Proficiency (10) and Logical Reasoning (20)",
     "Grammar; vocabulary; reading comprehension; composition; verbal reasoning; non-verbal reasoning"),
    ("Mathematics (40 questions; Biology for B.Pharm and a few programmes)",
     "Algebra; trigonometry; 2D and 3D coordinate geometry; differential calculus; integral calculus; ordinary differential equations; probability; vectors; statistics; linear programming"),
])

subjects(AP, "SRMJEEE", src_of(AP, "SRMJEEE"), V, [
    ("Physics (35 questions)", "Class 11-12 physics"),
    ("Chemistry (35 questions)", "Class 11-12 chemistry"),
    ("Mathematics or Biology (40 questions)", "Class 11-12 mathematics, or biology for the biology-based programmes"),
    ("English and Aptitude (20 questions)", "English usage and general aptitude"),
])

src = src_of(AP, "NCHM JEE") + "; section 4 Scheme of Examination"
subjects(AP, "NCHM JEE", src, V, [
    ("Numerical Ability and Analytical Aptitude (15 questions)", "Numerical ability and analytical aptitude"),
    ("Reasoning and Logical Deduction (15)", "Reasoning and logical deduction"),
    ("General Knowledge & Current Affairs (15)", "General knowledge and current affairs"),
    ("English Language (45)", "English language"),
    ("Aptitude for Service Sector (30)", "Aptitude for the hospitality and service sector"),
])

src = src_of(AP, "NIFT Entrance") + "; UG exam structure and GAT component descriptions"
subjects(AP, "NIFT Entrance", src, V, [
    ("General Ability Test (GAT, computer-based)",
     "Quantitative ability: addition, multiplication, division, fractions, percentage, rate of interest, work and task, ratio and proportion, distance; "
     "communication ability and English comprehension: synonyms, antonyms, word meanings, singular and plural, one-word substitutes, idioms and phrases, spellings, comprehension of a passage; "
     "analytical and logical ability: inference and logic, creative and lateral thinking; general knowledge and current affairs"),
    ("Creative Ability Test (CAT, pen and paper; B.Des only)",
     "Intuitive ability, observation, concept development and design ability; creative use of colour and illustration"),
    ("Situation Test (B.Des, shortlisted candidates)",
     "Make a model from a given set of materials: judged on space visualisation, creative use of material, composition of elements and colour scheme"),
])

subjects(AP, "UCEED", src_of(AP, "UCEED"), V, [
    ("Part A (computer-based, 200 marks, 2 hours)", "14 numerical-answer, 15 multiple-select and 28 multiple-choice questions on design aptitude"),
    ("Part B (on paper, 100 marks, 1 hour)", "Two drawing and design aptitude questions; marked only for candidates shortlisted on Part A"),
])

subjects(AP, "CAT", src_of(AP, "CAT"), V, [
    ("Verbal Ability & Reading Comprehension", "No fixed syllabus: reading comprehension passages and verbal ability questions"),
    ("Data Interpretation & Logical Reasoning", "No fixed syllabus: data sets, charts and tables, and logical reasoning sets"),
    ("Quantitative Ability", "No fixed syllabus: school-level mathematics applied to problems; on-screen calculator allowed"),
])

subjects(AP, "NSEJS (Junior Science Olympiad)", src_of(AP, "NSEJS (Junior Science Olympiad)"), V, [
    ("Physics, Chemistry and Biology (equal emphasis)", "Broadly Class 10 CBSE level: all the basic subjects of science"),
])

subjects(TS, "TGCET (Telangana Gurukulam Class 5)", src_of(TS, "TGCET (Telangana Gurukulam Class 5)"), V, [
    ("Class V entry: Telugu 20, English 25, Maths 25, EVS 20, Mental Ability 10", "100 objective questions"),
    ("Class VI entry: Telugu 20, English 20, Maths 25, EVS 25, GK & current affairs 10", "100 objective questions"),
    ("Class VII entry: English 20, Maths 25, Science 25, Social 20, GK 10", "100 objective questions"),
    ("Classes VIII-IX entry: English 20, Maths 25, Physical Science 13, Biological Science 12, Social 20, GK 10", "100 objective questions"),
])

for _exam, _state in (("APRJC CET", AP), ("TGRJC CET", TS)):
    subjects(_state, _exam, src_of(_state, _exam), V, [
        ("English (50 marks, every group)", "Class 10 standard English"),
        ("Mathematics (50 marks; MPC and MEC groups)", "Class 10 mathematics"),
        ("Physical Science (50 marks; MPC and BPC groups)", "Class 10 physical science"),
        ("Biological Science (50 marks; BPC group)", "Class 10 biological science"),
        ("Social Studies (50 marks; MEC and CEC groups)", "Class 10 social studies"),
    ])

src = src_of(AP, "APPSC Group 1") + "; Scheme and Syllabus (G.O.Ms.No.158, GAD, 26-12-2018) in the same notification"
subjects(AP, "APPSC Group 1", src, V, [
    ("Screening Paper I: General Studies (120 questions, 120 marks)",
     "A. History and culture (30); B. Constitution, polity, social justice and international relations (30); C. Indian and Andhra Pradesh economy and planning (30); D. Geography (30)"),
    ("Screening Paper II: General Aptitude (120 questions, 120 marks)",
     "A. General mental ability, administrative and psychological abilities (60); B(i) Science and technology (30); B(ii) Current events of regional, national and international importance (30)"),
    ("Mains: Telugu and English papers (150 marks each, qualifying)", "Language papers that must be passed but don't count in the ranking"),
    ("Mains Paper I: General Essay (150)", "Contemporary themes of regional, national and international importance"),
    ("Mains Paper II: History, Culture and Geography of India and AP (150)", "History, culture and geography of India and Andhra Pradesh"),
    ("Mains Paper III: Polity, Constitution, Governance, Law and Ethics (150)", "Polity, constitution, governance, law and ethics"),
    ("Mains Paper IV: Economy and Development of India and AP (150)", "Economy and development of India and Andhra Pradesh"),
    ("Mains Paper V: Science, Technology and Environmental Issues (150)", "Science, technology and environmental issues"),
])

subjects(AP, "APPSC Group 2", src_of(AP, "APPSC Group 2"), V, [
    ("Screening: General Studies & Mental Ability (150 marks)", "Degree-standard general studies and mental ability"),
    ("Mains Paper I (150 marks)", "Social and cultural history of Andhra Pradesh; the Indian Constitution"),
    ("Mains Paper II (150 marks)", "Indian and Andhra Pradesh economy; science and technology"),
])

subjects(TS, "TGPSC Group 1", src_of(TS, "TGPSC Group 1"), V, [
    ("Preliminary: General Studies & Mental Ability (150 marks)", "Screening test; 1:50 shortlisted for Mains"),
    ("Mains: General English (qualifying)", "Must be passed; not counted in the ranking"),
    ("Mains Paper I: General Essay (150)", "Essays"),
    ("Mains Paper II: History, Culture and Geography (150)", "History, culture and geography"),
    ("Mains Paper III: Indian Society, Constitution and Governance (150)", "Indian society, the Constitution and governance"),
    ("Mains Paper IV: Economy and Development (150)", "Economy and development"),
    ("Mains Paper V: Science, Technology and Data Interpretation (150)", "Science and technology; data interpretation"),
    ("Mains Paper VI: Telangana Movement and State Formation (150)", "The Telangana movement and formation of the state"),
])

subjects(TS, "TGPSC Group 4", src_of(TS, "TGPSC Group 4"), V, [
    ("Paper I: General Studies (150 questions)",
     "Current affairs; international relations; everyday science; environment and disaster management; geography and economy of India and Telangana; Indian Constitution; Telangana history and movement"),
    ("Paper II: Secretarial Abilities (150 questions)", "Secretarial abilities"),
])

subjects(AP, "IBPS PO", src_of(AP, "IBPS PO"), V, [
    ("Prelims: English Language (30 questions)", "English language"),
    ("Prelims: Quantitative Aptitude (35)", "Quantitative aptitude"),
    ("Prelims: Reasoning Ability (35)", "Reasoning ability"),
    ("Mains: Reasoning", "Reasoning"),
    ("Mains: General / Economy / Banking / Digital / Financial Awareness", "Including RBI circulars"),
    ("Mains: English Language", "English language"),
    ("Mains: Data Analysis and Interpretation", "Data analysis and interpretation"),
    ("Mains: Descriptive paper (25 marks, 30 minutes)", "Essay and comprehension"),
])

subjects(AP, "IBPS Clerk", src_of(AP, "IBPS Clerk"), V, [
    ("Prelims: English (30), Numerical Ability (35), Reasoning (35)", "20 minutes per section, sectional cut-offs"),
    ("Mains: General / Financial Awareness (40 questions, 50 marks)", "General and financial awareness"),
    ("Mains: General English (40 questions, 40 marks)", "English"),
    ("Mains: Reasoning Ability (40 questions, 60 marks)", "Reasoning"),
    ("Mains: Quantitative Aptitude (40 questions, 50 marks)", "Quantitative aptitude"),
])

subjects(AP, "SBI PO", src_of(AP, "SBI PO"), V, [
    ("Prelims: English (40), Quantitative Aptitude (30), Reasoning (30)", "20 minutes each, no sectional cut-off"),
    ("Mains: Reasoning & Computer Aptitude (40 questions, 60 marks)", "Reasoning and computer aptitude"),
    ("Mains: Data Analysis & Interpretation (30 questions, 60 marks)", "Data analysis and interpretation"),
    ("Mains: General Awareness / Economy / Banking (60 questions, 60 marks)", "General, economy and banking awareness"),
    ("Mains: English (40 questions, 20 marks)", "English"),
    ("Mains: Descriptive (30 marks)", "Email, situation analysis, report or precis"),
])

subjects(AP, "AP Police Constable & SI", src_of(AP, "AP Police Constable & SI"), V, [
    ("Constable: preliminary and final written tests (200 marks each)", "Objective questions"),
    ("SI: Arithmetic & Reasoning (SSC standard)", "Arithmetic and reasoning"),
    ("SI: General Studies (degree standard)", "General studies"),
    ("SI final: English and Telugu/Urdu (descriptive)", "Language papers"),
])

for _exam, _state in (("AP PGECET", AP), ("TS PGECET", TS)):
    subjects(_state, _exam, src_of(_state, _exam), V, [
        ("Your branch's test paper (120 questions)", "One paper in your B.Tech / B.Pharm branch, from that branch's degree syllabus; each paper's syllabus is on the official website"),
    ])
subjects(TS, "TS CPGET", src_of(TS, "TS CPGET"), V, [
    ("The subject of the M.A. / M.Sc / M.Com you want (100 questions)", "Questions only from that subject's degree syllabus"),
    ("Shared life-science test (Biochemistry, Environmental Science, Forensic Science, Genetics, Microbiology)", "Part A Chemistry (40) + Part B one B.Sc optional (60)"),
    ("M.Sc Biotechnology test", "Chemistry (40) + Biotechnology (60)"),
])
subjects(AP, "AP PGCET", src_of(AP, "AP PGCET"), V, [
    ("The subject of the PG course you want (100 questions)", "From that subject's degree syllabus; M.P.Ed: B.P.Ed syllabus test plus 100 marks for sports achievements"),
])
subjects(AP, "AP PECET", src_of(AP, "AP PECET"), V, [
    ("Physical Efficiency Test (400 marks)", "Men: 100 m run, shot put (6 kg), 800 m run, long or high jump; women: 100 m run, shot put (4 kg), 400 m run, long or high jump (100 marks each)"),
    ("Skill Test in one game (100 marks)", "Ball badminton, basketball, cricket, football, handball, hockey, kabaddi, kho-kho, shuttle badminton, tennis or volleyball"),
])

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
