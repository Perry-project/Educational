"""Builds db/seed/exam_focus.json: for each subject an exam tests
(db/seed/exam_subjects.json), the topics a student should concentrate on
first and why.

This is study guidance (tier_3_advisory), AI-assisted, and the site labels it
that way. It is built from the official syllabus already on the subject row:
it names topics from that syllabus and explains why they repay the effort
(they carry a large share of the paper's marks where the official notice
gives a split, or other chapters depend on them). It never states a
chapter-wise weightage that the official documents don't give.

Run from the project root:  python scripts/exam-research/build-exam-focus.py
then:                        npm run db:import
"""
import json
import os

ROOT = os.path.join(os.path.dirname(__file__), "..", "..", "db", "seed")
SUBJECTS = json.load(open(os.path.join(ROOT, "exam_subjects.json"), encoding="utf-8"))
FOCUS = []


def focus(exam, subject_prefix, items):
    """`subject_prefix` picks the exam_subjects row by how its subject starts,
    so the long official subject names don't need retyping."""
    rows = [r for r in SUBJECTS if r["exam_name"] == exam and r["subject"].startswith(subject_prefix)
            and not r["subject"][len(subject_prefix):][:1].isalnum()]
    assert len(rows) == 1, f"{exam} / {subject_prefix}: {len(rows)} matching subjects"
    r = rows[0]
    for i, (topic, why) in enumerate(items, 1):
        FOCUS.append({"state": r["state"], "exam_name": exam, "subject": r["subject"],
                      "topic": topic, "why": why, "sequence_order": i})


def same(exams, subject_prefix, items):
    for e in exams:
        focus(e, subject_prefix, items)


TG_EAPCET = "TG EAPCET (Telangana State Engineering, Agriculture & Pharmacy Common Entrance Test)"
TS_ECET = "TS ECET (Telangana State Engineering Common Entrance Test)"
TS_ICET = "TS ICET (Telangana State Integrated Common Entrance Test)"

# ---------- Engineering entrance (Intermediate syllabus) ----------
EAPCET_MATHS = [
    ("Calculus: limits, differentiation and its applications, integration, definite integrals",
     "The biggest single block of the Maths syllabus, and differential equations build on it, so time spent here pays across many questions."),
    ("Coordinate geometry: straight lines, circles, parabola, ellipse, hyperbola, 3D",
     "A long list of chapters that all use the same formulas and methods; practise them together."),
    ("Algebra: matrices, complex numbers, quadratic expressions, permutations and combinations, binomial theorem",
     "Formula-based chapters where quick, accurate working wins easy marks."),
    ("Vectors and probability",
     "Shorter chapters with standard question types: learn the formulas and the common problem patterns."),
    ("Trigonometry: identities, equations and properties of triangles",
     "Used everywhere else in the paper (calculus and coordinate geometry), so weak trigonometry costs marks in other chapters too."),
]
EAPCET_PHYSICS = [
    ("Mechanics: laws of motion, work-energy, rotational motion, gravitation",
     "The first-year foundation: most later chapters reuse these ideas and equations."),
    ("Electricity and magnetism: electrostatics, current electricity, magnetism, electromagnetic induction, AC",
     "A large connected block of the second-year syllabus."),
    ("Modern physics: dual nature, atoms, nuclei, semiconductor electronics",
     "Short chapters with direct, formula-based questions: high return for little time."),
    ("Optics and waves",
     "Standard ray-optics and wave-optics problems repeat in pattern; practise the sign conventions."),
]
EAPCET_CHEMISTRY = [
    ("Organic chemistry: basics, hydrocarbons, haloalkanes, compounds with C, H, O and nitrogen",
     "Many syllabus chapters share the same reaction logic; learn named reactions and conversions together."),
    ("Physical chemistry: stoichiometry, thermodynamics, equilibrium, electrochemistry, kinetics, solutions",
     "Numerical chapters where practice turns into sure marks."),
    ("Inorganic chemistry: periodicity, chemical bonding, p-, d- and f-block elements, coordination compounds",
     "Memory-based: revise from the textbook tables repeatedly rather than once."),
    ("Atomic structure and chemical bonding",
     "The base for the whole subject; gaps here show up in every other chapter."),
]
EAPCET_BOTANY = [
    ("Plant physiology", "Process-based chapters (photosynthesis, respiration, growth) that are asked in detail."),
    ("Genetics, molecular biology and biotechnology", "Concept-heavy chapters with problem-style questions."),
    ("Cell structure and function", "Basic to both Botany and Zoology."),
    ("Reproduction in plants and plant systematics", "Fact-rich chapters: revise diagrams and examples."),
]
EAPCET_ZOOLOGY = [
    ("Human anatomy and physiology I-IV", "Four syllabus units on one theme: the largest block of Zoology."),
    ("Genetics and organic evolution", "Concepts and problem questions that overlap with Botany genetics."),
    ("Human reproduction", "Detailed, diagram-based chapter."),
    ("Animal diversity and structural organisation", "Classification facts: revise with tables."),
]
focus("AP EAPCET", "Mathematics", EAPCET_MATHS)
focus("AP EAPCET", "Physics", EAPCET_PHYSICS)
focus("AP EAPCET", "Chemistry", EAPCET_CHEMISTRY)
focus(TG_EAPCET, "Mathematics", EAPCET_MATHS)
focus(TG_EAPCET, "Physics", EAPCET_PHYSICS)
focus(TG_EAPCET, "Chemistry", EAPCET_CHEMISTRY)
focus(TG_EAPCET, "Botany", EAPCET_BOTANY)
focus(TG_EAPCET, "Zoology", EAPCET_ZOOLOGY)

JEE_MATHS = [
    ("Calculus: limits, continuity, differentiability, integral calculus, differential equations",
     "The largest part of the syllabus, and it ties into coordinate geometry and other chapters."),
    ("Coordinate geometry and 3D geometry with vectors",
     "Many chapters solved with the same tools; strong algebra makes them fast."),
    ("Algebra: complex numbers, quadratic equations, matrices and determinants, sequences and series, binomial theorem, permutations and combinations",
     "Broad algebra base used throughout the paper."),
    ("Probability and statistics", "Tricky but scoring once the counting methods are clear."),
]
JEE_PHYSICS = [
    ("Mechanics: kinematics, laws of motion, work-energy, rotational motion, gravitation",
     "The foundation for almost every other chapter."),
    ("Electrostatics, current electricity, magnetism and electromagnetic induction",
     "A large, connected block of the syllabus."),
    ("Modern physics: dual nature, atoms and nuclei, electronic devices",
     "Short chapters with direct questions."),
    ("Optics, waves and thermodynamics", "Standard problem types that repeat."),
]
JEE_CHEMISTRY = [
    ("Organic chemistry: basic principles, hydrocarbons, compounds containing halogens, oxygen and nitrogen",
     "Reaction mechanisms link the chapters: understand them instead of memorising each reaction."),
    ("Physical chemistry: thermodynamics, equilibrium, electrochemistry, kinetics, solutions",
     "Numerical, so practice converts directly into marks."),
    ("Inorganic chemistry: chemical bonding, coordination compounds, p-, d- and f-block elements",
     "Read the NCERT textbook line by line: questions are often taken straight from it."),
    ("Atomic structure and some basic concepts (mole concept)", "Used in every numerical in the subject."),
]
focus("JEE Main", "Mathematics", JEE_MATHS)
focus("JEE Main", "Physics", JEE_PHYSICS)
focus("JEE Main", "Chemistry", JEE_CHEMISTRY)
focus("JEE Advanced", "Mathematics", JEE_MATHS[:2] + [
    ("Algebra and matrices", "Concepts are tested deeply and combined with other chapters."),
    ("Probability", "A frequent source of multi-concept questions."),
])
focus("JEE Advanced", "Physics", [
    ("Mechanics", "Deep, multi-step problems are built on it; it is also the base for the rest of the paper."),
    ("Electricity and magnetism", "A large part of the syllabus with challenging problems."),
    ("Modern physics and optics", "Concept-heavy chapters that reward clear understanding."),
    ("Thermal physics", "Thermodynamics and heat transfer problems that combine with other topics."),
])
focus("JEE Advanced", "Chemistry", [
    ("Organic chemistry: mechanisms and conversions", "Questions test reasoning through reaction steps, not memory alone."),
    ("Physical chemistry: equilibrium, electrochemistry, kinetics, thermodynamics", "Numerical-heavy, high-precision questions."),
    ("Inorganic chemistry: bonding, coordination compounds, qualitative analysis", "Conceptual questions drawn closely from the textbook."),
])

focus("VITEEE", "Mathematics or Biology", [
    ("Calculus and coordinate geometry (Maths route)", "The largest parts of the Class 11-12 Maths syllabus."),
    ("Algebra, vectors and probability (Maths route)", "Formula-based chapters for quick marks."),
    ("Genetics, human physiology and biotechnology (Biology route)", "Core Class 12 biology chapters."),
])
focus("VITEEE", "Physics", [
    ("Mechanics and electricity & magnetism", "The two biggest blocks of Class 11-12 physics."),
    ("Modern physics and semiconductors", "Short chapters with direct questions."),
])
focus("VITEEE", "Chemistry", [
    ("Organic chemistry", "A large share of Class 12 chemistry."),
    ("Physical chemistry numericals", "Practice turns these into sure marks."),
])
focus("VITEEE", "English", [
    ("Reading comprehension and grammar", "English and aptitude are a small part of the paper: aim for full marks with light, steady practice."),
])

# ---------- Medical ----------
focus("NEET-UG", "Biology", [
    ("Human physiology", "A large Class 11 block; questions come directly from NCERT text and diagrams."),
    ("Genetics and evolution", "A major Class 12 unit with both concept and problem questions."),
    ("Reproduction", "Plant and human reproduction together form a big, NCERT-based part."),
    ("Ecology and environment", "Fact-based and quick to revise: scoring for most students."),
    ("Biotechnology and its applications", "Short unit with direct NCERT questions."),
    ("Cell structure and function, and plant physiology", "Basic chapters that support the rest of Biology."),
])
focus("NEET-UG", "Physics", [
    ("Mechanics: kinematics, laws of motion, work-energy, rotational motion", "The foundation for the whole subject."),
    ("Electrostatics, current electricity and magnetism", "A large connected block of Class 12."),
    ("Modern physics: dual nature, atoms and nuclei, electronic devices", "Short chapters with formula-based questions: quick marks."),
    ("Optics", "Standard ray-optics questions repeat; practise sign conventions."),
])
focus("NEET-UG", "Chemistry", [
    ("Organic chemistry: basic principles, hydrocarbons, compounds with halogens, oxygen and nitrogen", "Reaction-based questions, often straight from NCERT."),
    ("Inorganic chemistry: chemical bonding, coordination compounds, p-, d- and f-block elements", "Read NCERT line by line: many questions come word for word."),
    ("Physical chemistry: mole concept, equilibrium, thermodynamics, electrochemistry, kinetics", "Numerical chapters: practice makes them reliable marks."),
])

# ---------- Diploma lateral entry ----------
ECET_COMMON = {
    "Mathematics": [("Calculus (differentiation, integration, differential equations)", "The core of diploma-level engineering maths."),
                    ("Matrices, trigonometry and complex numbers", "Formula-based topics for sure marks.")],
    "Physics": [("Units, mechanics and heat", "Basic diploma physics that most questions draw on."),
                ("Modern physics and electricity basics", "Short, direct topics.")],
    "Chemistry": [("Fundamentals: atomic structure, bonding, solutions, acids and bases", "The base of diploma chemistry."),
                  ("Electrochemistry, corrosion, water treatment and polymers", "Applied engineering-chemistry topics.")],
    "Engineering paper": [("Your own branch's core subjects from the diploma syllabus", "The branch paper carries half the total marks, so revise your diploma core subjects most."),
                          ("Numerical problems from those subjects", "Practise solving, not just reading.")],
}
for exam in ("AP ECET", TS_ECET):
    for subj, items in ECET_COMMON.items():
        focus(exam, subj, items)

# ---------- MBA / MCA ----------
ICET_ANALYTICAL = [
    ("Problem solving: series, coding-decoding, analogies, arrangements", "The larger part of the section: speed comes from practice."),
    ("Data sufficiency", "A fixed block of questions with a learnable method."),
    ("Data analysis from tables and graphs", "Quick marks with careful reading."),
]
ICET_MATHS = [
    ("Arithmetic: percentages, profit and loss, ratio, time and work, time and distance", "The largest block of the section."),
    ("Algebra and geometry", "Standard school-level formulas."),
    ("Statistics", "A small block that is easy to score."),
]
ICET_COMM = [
    ("Reading comprehension", "Several passages: regular reading improves speed."),
    ("Functional grammar and vocabulary", "Learnable rules and word lists."),
    ("Business and computer terminology", "Memory-based: revise standard term lists."),
]
for exam in ("AP ICET", TS_ICET):
    focus(exam, "Section A", ICET_ANALYTICAL)
focus("AP ICET", "Section B", ICET_COMM)
focus("AP ICET", "Section C", ICET_MATHS)
focus(TS_ICET, "Section B", ICET_MATHS)
focus(TS_ICET, "Section C", ICET_COMM)

# ---------- Law ----------
focus("CLAT (UG)", "Legal Reasoning", [
    ("Applying a given legal principle to facts", "About a quarter of the paper: answer from the principle given, not from outside knowledge."),
    ("Reading current legal news (constitutional, criminal, contract and tort themes)", "Passages are built on topical legal issues."),
])
focus("CLAT (UG)", "Current Affairs", [
    ("Last 12 months of national and international news", "About a quarter of the paper: read a daily newspaper and monthly summaries."),
    ("Background of major events (history, organisations, awards, reports)", "Questions ask about the context around the news passage."),
])
focus("CLAT (UG)", "English", [
    ("Reading speed and comprehension of 450-word passages", "Every English question is passage-based."),
    ("Inference and the main idea", "Most questions test understanding, not grammar rules."),
])
focus("CLAT (UG)", "Logical Reasoning", [
    ("Arguments: premises, conclusions, assumptions, strengthen and weaken", "The core of the section."),
    ("Inference and analogies", "Practise with timed passages."),
])
focus("CLAT (UG)", "Quantitative", [
    ("Ratios, percentages and data interpretation from short sets", "About 10% of the paper at Class 10 level: aim for full marks."),
])
for exam in ("AP LAWCET", "TS LAWCET"):
    focus(exam, "Part C", [
        ("The Constitution of India: fundamental rights, directive principles, Parliament, judiciary", "The base of the law-aptitude part, the largest of the three."),
        ("Basic principles of law: contracts, torts, crimes", "Elementary legal principles are asked directly."),
        ("Legal comprehension passages", "Read the principle and apply it to the facts given."),
    ])
    focus(exam, "Part B", [("Current affairs of the last year: national, state and international", "Read a newspaper daily and revise monthly summaries.")])
    focus(exam, "Part A", [("General knowledge (static GK) and mental ability (reasoning)", "Reasoning is quick to improve with practice; static GK needs steady revision.")])

# ---------- Defence ----------
focus("NDA (National Defence Academy exam)", "Paper I:", [
    ("Calculus: differential and integral calculus, differential equations", "Large share of the Class 11-12 syllabus tested."),
    ("Algebra, matrices and determinants", "Formula-based and fast to score."),
    ("Trigonometry", "Asked directly and used in other chapters."),
    ("Analytical geometry (2D and 3D) and vectors", "Standard problem types."),
    ("Statistics and probability", "Short, scoring chapters."),
])
focus("NDA (National Defence Academy exam)", "Paper II: General Ability Test, Part A", [
    ("Grammar and usage, vocabulary", "Spotting errors, synonyms and antonyms make up much of the section."),
    ("Comprehension", "Regular reading improves speed and accuracy."),
])
focus("NDA (National Defence Academy exam)", "Paper II: General Ability Test, Part B", [
    ("Physics", "The largest share of General Knowledge (about 25%, per the notice)."),
    ("History and freedom movement, and geography", "About 20% each, per the notice."),
    ("Chemistry and general science", "Together about 25%: Class 10-level concepts."),
    ("Current events", "About 10%: follow the news for the past year."),
])
focus("CDS (Combined Defence Services exam)", "English", [
    ("Spotting errors, sentence improvement, synonyms and antonyms, comprehension", "The standard question types of the paper."),
])
focus("CDS (Combined Defence Services exam)", "General Knowledge", [
    ("Current events and defence news", "Asked every year."),
    ("Indian history and geography", "Named in the syllabus."),
    ("Everyday science", "Class 10-level science applied to daily life."),
])
focus("CDS (Combined Defence Services exam)", "Elementary Mathematics", [
    ("Arithmetic: percentages, ratios, time and work, interest", "Class 10-level, a large part of the paper."),
    ("Algebra, geometry and mensuration", "Formula-based chapters."),
    ("Trigonometry and statistics", "Short, scoring topics."),
])
focus("AFCAT", "Numerical Ability", [
    ("Percentage, ratio, profit and loss, time and work, speed and distance", "Class 10-level arithmetic that most questions use."),
    ("Simplification and number series", "Quick marks with practice."),
])
focus("AFCAT", "Reasoning and Military Aptitude", [
    ("Non-verbal reasoning: figures, patterns, spatial ability", "A distinctive part of AFCAT; practise with past-style figure questions."),
    ("Verbal reasoning: analogies, series, coding", "Standard reasoning types."),
])
focus("AFCAT", "English", [
    ("Vocabulary: synonyms, antonyms, idioms, one-word substitution", "Many of the questions."),
    ("Comprehension and error detection", "Regular reading helps."),
])
focus("AFCAT", "General Awareness", [
    ("Defence and current affairs", "Named in the syllabus and asked often."),
    ("History, geography, polity and basic science", "Static general knowledge: revise steadily."),
])

# ---------- Government jobs ----------
SSC_QUANT = [
    ("Arithmetic: percentages, ratio, profit and loss, interest, time and work, speed and distance", "The bulk of the quantitative questions."),
    ("Geometry, mensuration and trigonometry", "Formula-based; learn the standard results."),
    ("Data interpretation (bar and pie charts)", "Quick marks with careful reading."),
]
SSC_REASONING = [
    ("Analogies, classification, series, coding-decoding", "The most common question types."),
    ("Non-verbal: paper folding, embedded figures, mirror images", "Easy once practised."),
]
SSC_GA = [
    ("Current affairs of the last 6-12 months", "Asked every year."),
    ("Static GK: history, geography, polity, economy", "Revise steadily with short notes."),
    ("Everyday science", "Class 10-level biology, physics and chemistry."),
]
SSC_ENGLISH = [
    ("Error spotting, fill in the blanks, sentence improvement", "Grammar rules apply across many questions."),
    ("Vocabulary: synonyms, antonyms, idioms, one-word substitution", "Build a word list and revise it."),
    ("Comprehension and cloze test", "Regular reading improves speed."),
]
focus("SSC CGL", "Tier-I: Quantitative", SSC_QUANT)
focus("SSC CGL", "Tier-I: General Intelligence", SSC_REASONING)
focus("SSC CGL", "Tier-I: General Awareness", SSC_GA)
focus("SSC CGL", "Tier-I: English", SSC_ENGLISH)
focus("SSC CHSL", "Tier-I: Quantitative", SSC_QUANT)
focus("SSC CHSL", "Tier-I: General Intelligence", SSC_REASONING)
focus("SSC CHSL", "Tier-I: General Awareness", SSC_GA)
focus("SSC CHSL", "Tier-I: English", SSC_ENGLISH)
focus("SSC GD Constable", "Elementary Mathematics", SSC_QUANT[:1] + [("Number system and simplification", "Basic and quick to score.")])
focus("SSC GD Constable", "General Intelligence", SSC_REASONING)
focus("SSC GD Constable", "General Knowledge", SSC_GA)
focus("SSC GD Constable", "English / Hindi", [("Basic comprehension, grammar and vocabulary", "School-level language: steady practice is enough.")])

RRB_MATHS = [
    ("Arithmetic: percentages, ratio, interest, profit and loss, time and work, time and distance", "Most of the maths questions."),
    ("Number system, simplification (BODMAS), LCM and HCF", "Fast marks with practice."),
    ("Mensuration, geometry and trigonometry", "Standard formulas."),
]
RRB_REASONING = [
    ("Series, analogies, coding-decoding, classification", "The common question types."),
    ("Syllogism, Venn diagrams, puzzles and seating arrangements", "Practise to gain speed."),
]
focus("RRB Group D (Level 1)", "Mathematics", RRB_MATHS)
focus("RRB Group D (Level 1)", "General Intelligence", RRB_REASONING)
focus("RRB Group D (Level 1)", "General Science", [
    ("Class 10 Physics, Chemistry and Biology (NCERT/CBSE)", "The syllabus is stated as Class 10 CBSE level: revise those textbooks."),
])
focus("RRB Group D (Level 1)", "General Awareness", [("Current affairs: science, sports, culture, economy, politics", "Follow the news for the past year.")])
focus("RRB NTPC", "Mathematics", RRB_MATHS)
focus("RRB NTPC", "General Intelligence", RRB_REASONING)
focus("RRB NTPC", "General Awareness", [
    ("Current events and government schemes", "Named first in the syllabus."),
    ("Indian history, geography, polity and economy", "Static GK revised steadily."),
    ("General science up to Class 10 and basics of computers", "Named in the syllabus."),
])

focus("UPSC Civil Services Examination", "Prelims GS Paper I", [
    ("Indian polity and governance", "Asked every year; read the Constitution's key parts and current issues."),
    ("Economy and environment", "Large, current-affairs-linked areas."),
    ("History (modern India and the national movement first)", "A steady source of questions."),
    ("Current events", "Integrated across every subject."),
])
focus("UPSC Civil Services Examination", "Prelims GS Paper II", [
    ("Comprehension and basic numeracy", "The paper only needs 33% to qualify, but don't neglect it: many candidates fail here."),
])
focus("UPSC Civil Services Examination", "Mains GS II", [("Constitution, governance and international relations", "Answer-writing practice with current examples matters most.")])
focus("UPSC Civil Services Examination", "Mains GS III", [("Economy, environment, science and technology, security", "Link static topics to current developments.")])
focus("UPSC Civil Services Examination", "Mains GS IV", [("Ethics case studies", "Practise structured answers to case studies.")])

focus("TGPSC Group 2", "Paper I:", [
    ("Telangana: geography, society, culture, heritage and state policies", "Telangana-specific topics run through every paper."),
    ("Current affairs and general science", "Asked every year."),
    ("Logical reasoning and data interpretation", "Practice-based, scoring part."),
])
focus("TGPSC Group 2", "Paper II:", [("Indian Constitution and politics", "A core block."), ("Socio-cultural history of India and Telangana", "Fact-heavy: revise with notes.")])
focus("TGPSC Group 2", "Paper III", [("Economy and development of Telangana", "State economy and schemes are emphasised."), ("Indian economy: issues and challenges", "Link to current data.")])
focus("TGPSC Group 2", "Paper IV", [("The three phases of the Telangana movement (1948-2014)", "The whole paper: learn the timeline, people and events of each phase.")])

# ---------- Teaching ----------
focus("TS TET", "Paper I: Child Development", [
    ("Learning theories (Piaget, Vygotsky, Kohlberg) and individual differences", "The most-asked part of child development."),
    ("Inclusive education and the learning process", "Applied questions on classroom situations."),
])
focus("TS TET", "Paper I: Mathematics", [("Classes I-V content: numbers, fractions, measurement, geometry", "24 of the 30 questions are content."), ("Mathematics pedagogy", "6 questions: how children learn maths.")])
focus("TS TET", "Paper I: Environmental Studies", [("Classes I-V EVS content", "24 of the 30 questions."), ("EVS pedagogy", "6 questions.")])
focus("TS TET", "Paper I: Language I", [("Comprehension and grammar", "Most of the section."), ("Language pedagogy", "6 questions.")])
focus("TS TET", "Paper I: Language II", [("Comprehension and grammar", "Most of the section."), ("English pedagogy", "6 questions.")])
focus("TS TET", "Paper II: Mathematics and Science", [
    ("Classes VI-VIII maths content", "24 questions."),
    ("Physical and biological science content", "12 questions each."),
    ("Pedagogy of maths and science", "6 questions each."),
])
focus("TS TET", "Paper II: Social Studies", [("History, geography, civics and economics of Classes VI-VIII", "48 content questions."), ("Social studies pedagogy", "12 questions.")])
for exam, parts in (("AP EdCET", ("Part A", "Part B", "Part C")),):
    focus(exam, "Part A", [("Comprehension, grammar and vocabulary", "School-to-degree-level English.")])
    focus(exam, "Part B", [("Teaching aptitude and current events", "Teaching aptitude questions test how you'd handle classroom situations.")])
    focus(exam, "Part C", [("Your chosen methodology subject at degree level", "The largest part: revise your degree syllabus in that subject.")])
focus("TS EdCET", "Subject content", [("Class 10 maths, science and social studies (Telangana curriculum)", "60 marks: the biggest part.")])
focus("TS EdCET", "General Knowledge", [("Current issues in education and general knowledge", "30 marks.")])

# ---------- After Class 10 ----------
for subj in ("Mathematics", "Physics", "Chemistry"):
    focus("TS POLYCET", subj, [(f"The Telangana SSC Class 10 {subj} textbook, chapter by chapter",
                                "The exam follows the Class 10 syllabus: solve every textbook exercise and example."
                                + (" Maths is the largest subject (60 questions)." if subj == "Mathematics" else ""))])

focus("AP SSC Public Examinations", "Mathematics", [
    ("Probability (13 marks) and statistics (12 marks)", "The two highest-mark chapters in the official blueprint."),
    ("Pair of linear equations (11) and coordinate geometry (10)", "Next highest in the blueprint."),
    ("Real numbers (9), polynomials, quadratic equations and trigonometry (7 each)", "Steady marks from formula-based chapters."),
])
focus("AP SSC Public Examinations", "Physical Science", [
    ("Carbon and its compounds, light, electricity (11 marks each)", "The highest-mark chapters in the official blueprint."),
    ("Acids, bases and salts (10)", "Next highest."),
])
focus("AP SSC Public Examinations", "Biological Science", [
    ("Life processes (14 marks)", "The highest-mark chapter in the official blueprint."),
    ("How organisms reproduce, heredity, our environment (10 each)", "Together 30 marks."),
])
focus("AP SSC Public Examinations", "Social Studies", [
    ("All four parts equally: geography, history, civics, economics", "Each carries 25 marks in the official pattern: don't skip any."),
    ("Map work (India map)", "Practise locating the places in the textbook lists."),
])
focus("AP SSC Public Examinations", "English", [
    ("Reading comprehension and creative expression (30 marks each)", "The two biggest sections."),
    ("Grammar and vocabulary (20 marks each)", "Rule-based, so practice gives sure marks."),
])

# ---------- School admissions ----------
focus("JNVST (Navodaya Class 6)", "Section 1a", [("Figure series, pattern completion, mirror and water images, embedded figures", "Non-verbal: practise many figure questions.")])
focus("JNVST (Navodaya Class 6)", "Section 2", [
    ("Fractions, factors and multiples, LCM and HCF", "Core Class 5 arithmetic."),
    ("Measurement, perimeter and area, data from tables", "Applied word problems."),
])
focus("JNVST (Navodaya Class 6)", "Section 3", [("Reading passages", "All 20 questions come from 4 passages: read short stories and practise answering.")])
focus("JNVST (Navodaya Class 6)", "Section 1b", [("Human body, natural world and science in daily life", "Class 5 EVS topics named in the syllabus.")])
focus("JNVST (Navodaya Class 9 lateral entry)", "Mathematics", [("Class 8 maths: algebra, linear equations, comparing quantities, mensuration", "35 marks: the largest section with science.")])
focus("JNVST (Navodaya Class 9 lateral entry)", "General Science", [("Class 8 science chapters listed in the prospectus", "35 marks.")])
focus("JNVST (Navodaya Class 9 lateral entry)", "English", [("Comprehension and grammar (tenses, reported speech, prepositions)", "15 marks.")])
focus("AISSEE (Sainik Schools Class 6 & 9)", "Class 6: Mathematics", [
    ("Fractions, decimals, LCM and HCF, percentages, profit and loss", "Maths carries 150 of the 300 marks for Class 6 (3 marks a question)."),
    ("Area, perimeter, angles and volume", "Geometry and measurement questions."),
])
focus("AISSEE (Sainik Schools Class 6 & 9)", "Class 9: Mathematics", [
    ("Class 8 maths: algebra, linear equations, percentages, interest, mensuration", "Maths carries 200 of the 400 marks for Class 9 (4 marks a question)."),
    ("Geometry: triangles, quadrilaterals, Pythagoras theorem", "Frequent topics in the syllabus list."),
])
for subj in ("Class 6: Intelligence", "Class 9: Intelligence"):
    focus("AISSEE (Sainik Schools Class 6 & 9)", subj, [("Analogies, series, classification and patterns", "Practice-based and quick to improve.")])

# ---------- Engineering PG and PSU jobs ----------
focus("GATE", "General Aptitude", [
    ("Quantitative aptitude and data interpretation", "General Aptitude is 15 of the 100 marks in every paper, and it's school-level: aim for nearly full marks here."),
    ("Verbal aptitude: grammar and vocabulary in context", "Short questions that are quick to answer with regular practice."),
    ("Spatial aptitude: rotation, mirroring, paper folding", "Unfamiliar at first, but a few hours of practice makes these easy."),
])
focus("GATE", "Engineering Mathematics", [
    ("Linear algebra (eigenvalues, systems of equations)", "Asked in almost every engineering paper's 13-mark maths section."),
    ("Calculus and differential equations", "Used again inside the core subject questions."),
    ("Probability and statistics", "Short, formula-based questions."),
])
focus("GATE", "Civil Engineering", [
    ("Structural engineering (solid mechanics, structural analysis, RCC and steel)", "The biggest section of the CE syllabus."),
    ("Geotechnical engineering", "A large, numerical section."),
    ("Environmental and transportation engineering", "Formula-based: quick marks once the IS-code methods are learnt."),
])
focus("GATE", "Mechanical Engineering", [
    ("Thermodynamics and heat transfer", "Core of the thermal sciences section."),
    ("Strength of materials and theory of machines", "Core of applied mechanics and design."),
    ("Manufacturing and industrial engineering", "Many direct, formula-based questions."),
])
focus("GATE", "Electrical Engineering", [
    ("Electric circuits and electrical machines", "Basics that the rest of the paper builds on."),
    ("Power systems and power electronics", "Large, numerical sections."),
    ("Control systems and signals and systems", "Standard methods that repeat."),
])
focus("GATE", "Electronics & Communication", [
    ("Networks, signals and systems", "The base of the whole EC paper."),
    ("Analog and digital circuits", "Large sections with numerical questions."),
    ("Communications", "Formula-based and scoring."),
])
focus("GATE", "Computer Science", [
    ("Algorithms and data structures", "Core of the paper; also what job interviews test."),
    ("Operating systems, databases and computer networks", "Three large, concept-plus-numerical sections."),
    ("Theory of computation and digital logic", "Precise topics that reward practice."),
    ("Discrete mathematics", "Part of CS's own maths section."),
])
focus("GATE", "Chemical Engineering", [
    ("Mass transfer and heat transfer", "Big, numerical sections."),
    ("Chemical reaction engineering and thermodynamics", "Core theory used throughout the paper."),
    ("Fluid mechanics and process control", "Standard problem types."),
])
focus("CA Foundation", "Paper 1", [
    ("Final accounts, partnership and company accounts", "Long practical questions that carry big marks."),
    ("Accounting process, depreciation and inventories", "The basics behind every other chapter."),
])
focus("CA Foundation", "Paper 2", [
    ("Indian Contract Act, 1872", "The largest and most basic law in the paper; other laws build on it."),
    ("Companies Act and Sale of Goods Act", "Frequently asked, with case-based questions."),
    ("Writing answers with the section and a conclusion", "This paper is descriptive: practise structured answers."),
])
focus("CA Foundation", "Paper 3", [
    ("Statistics (Part C)", "A large part of the paper with standard methods."),
    ("Business mathematics: mathematics of finance, permutations and combinations, sequences, calculus", "Formula-based chapters for sure marks."),
    ("Logical reasoning (Part B)", "Quick to master with practice."),
])
focus("CA Foundation", "Paper 4", [
    ("Demand and supply, production and cost, price determination in markets", "Core microeconomics chapters."),
    ("National income, money market and the Indian economy", "Macroeconomics chapters with factual questions."),
])
focus("CUET-UG", "Domain subjects", [
    ("The NCERT Class 12 textbook of each domain subject you choose", "The syllabus is the NCERT Class 12 syllabus: questions follow the textbook closely."),
    ("Choosing subjects", "Pick the subjects your target university programme requires: check the university's list before applying."),
])
focus("CUET-UG", "General Aptitude", [
    ("Quantitative reasoning and logical reasoning", "Practice-based and quick to improve."),
    ("Current affairs and general knowledge", "Follow the news for the past year."),
])
focus("CUET-UG", "Languages", [
    ("Reading comprehension", "Most language questions come from passages."),
    ("Vocabulary", "Build a word list and revise it."),
])
focus("NATA", "Part A", [
    ("3D composition (30 marks)", "The highest-mark drawing question: practise building models with simple kits."),
    ("Sketching with scale, proportion, shade and shadow", "Draw buildings, people and street scenes from life regularly."),
    ("Composition and colour", "Practise arranging shapes and colouring them neatly within the time."),
])
focus("NATA", "Part B", [
    ("Visual reasoning and 2D/3D composition", "A distinctive part of the paper."),
    ("Architecture general knowledge: famous buildings, architects, materials", "Read about well-known Indian and world buildings."),
    ("Basic mathematics and geometry", "Class 10-12 level numerical ability."),
])
focus("BITSAT", "Physics", EAPCET_PHYSICS[:3])
focus("BITSAT", "Chemistry", EAPCET_CHEMISTRY[:3])
focus("BITSAT", "Mathematics", [
    ("Calculus and coordinate geometry", "Large parts of the Maths syllabus (40 questions, the biggest section)."),
    ("Algebra, probability and vectors", "Formula-based chapters for quick marks."),
])
focus("BITSAT", "English Proficiency", [
    ("Logical reasoning (20 questions)", "Twice the questions of English: practise verbal and non-verbal reasoning."),
    ("Grammar and vocabulary", "Short questions that are quick to answer."),
])
focus("SRMJEEE", "Mathematics or Biology", [("Class 11-12 calculus, algebra and coordinate geometry (or Class 12 biology)", "The largest section: 40 of the 130 questions. There's no negative marking, so answer every question.")])
focus("CAT", "Verbal Ability", [
    ("Reading comprehension", "Most of this section is passage-based: read editorials and long-form articles daily."),
    ("Para-jumbles and para-summary", "Typed-answer questions with no negative marking: always attempt them."),
])
focus("CAT", "Data Interpretation", [
    ("Solving complete sets", "Questions come in sets: choose the sets you can finish and solve them fully."),
    ("Arrangements, tables and charts", "The common set types."),
])
focus("CAT", "Quantitative Ability", [
    ("Arithmetic: percentages, ratios, time-speed-distance, time and work", "A large share of the section."),
    ("Algebra: equations, inequalities, functions", "The other big block."),
    ("Geometry and number systems", "Fewer questions but regular."),
])
focus("NCHM JEE", "English Language", [("Grammar, vocabulary and comprehension", "The biggest section: 45 of 120 questions.")])
focus("NCHM JEE", "Aptitude for Service Sector", [("Hospitality situations and customer service judgement", "30 questions: think about how a hotel professional should respond.")])
focus("NIFT Entrance", "General Ability Test", [
    ("Communication ability and English comprehension", "Usually the largest GAT section in NIFT's own breakdowns."),
    ("Quantitative ability (percentages, interest, ratio, work, distance)", "School-level arithmetic."),
])
focus("NIFT Entrance", "Creative Ability Test", [("Drawing, colouring and visual ideas", "Practise sketching and illustrating ideas within a time limit.")])
focus("ICAR AIEEA", "One Major Subject-Group", [("Your degree's core subjects for the group you choose", "The whole paper is in one subject group: revise your B.Sc / B.Tech syllabus in that area.")])

# ---------- Government and banking jobs ----------
BANK_QUANT = [("Data interpretation: tables, bar, line and pie charts", "A large share of the quant questions, especially in Mains."),
              ("Simplification, approximation and number series", "Quick marks in Prelims."),
              ("Arithmetic: percentage, profit and loss, interest, time and work", "Used in word problems and data interpretation.")]
BANK_REASONING = [("Puzzles and seating arrangements", "The biggest block of reasoning questions."),
                  ("Syllogism, inequalities, coding-decoding, blood relations", "Short questions for quick marks.")]
BANK_ENGLISH = [("Reading comprehension", "Usually the largest part of the English section."),
                ("Error spotting, fillers and para-jumbles", "Grammar practice gives sure marks.")]
BANK_GA = [("Banking and financial awareness: RBI, monetary policy, banking terms", "Named in the syllabus and asked often."),
           ("Current affairs of the last 6 months", "The bulk of general awareness.")]
focus("IBPS PO", "Prelims: English", BANK_ENGLISH)
focus("IBPS PO", "Prelims: Quantitative", BANK_QUANT)
focus("IBPS PO", "Prelims: Reasoning", BANK_REASONING)
focus("IBPS PO", "Mains: General", BANK_GA)
focus("IBPS PO", "Mains: Data Analysis", BANK_QUANT[:1])
focus("IBPS Clerk", "Prelims", [BANK_QUANT[1], BANK_REASONING[0], BANK_ENGLISH[0]])
focus("IBPS Clerk", "Mains: General /", BANK_GA)
focus("IBPS Clerk", "Mains: Reasoning", BANK_REASONING)
focus("IBPS Clerk", "Mains: Quantitative", BANK_QUANT)
focus("SBI PO", "Prelims", [BANK_QUANT[1], BANK_REASONING[0], BANK_ENGLISH[0]])
focus("SBI PO", "Mains: Reasoning", BANK_REASONING)
focus("SBI PO", "Mains: Data Analysis", BANK_QUANT[:1])
focus("SBI PO", "Mains: General", BANK_GA)

focus("APPSC Group 1", "Screening Paper I", [
    ("All four parts equally: history and culture, polity, economy, geography", "Each part carries 30 of the 120 marks."),
    ("Andhra Pradesh economy and planning", "AP-specific questions sit inside part C."),
])
focus("APPSC Group 1", "Screening Paper II", [
    ("Mental ability, administrative and psychological abilities", "Half the paper (60 marks): practice-based and scoring."),
    ("Current events and science and technology", "30 marks each."),
])
focus("APPSC Group 2", "Screening", [("General studies and mental ability", "Mental ability questions reward practice; general studies needs steady revision.")])
focus("APPSC Group 2", "Mains Paper I", [("Social and cultural history of Andhra Pradesh", "AP-specific history is the core of this paper."), ("The Indian Constitution", "The other half of the paper.")])
focus("APPSC Group 2", "Mains Paper II", [("Indian and AP economy", "Link facts to current budgets and schemes."), ("Science and technology", "The other half of the paper.")])
focus("TGPSC Group 1", "Mains Paper VI", [("The three phases of the Telangana movement", "A full paper on its own: learn the timeline, people and events.")])
focus("TGPSC Group 4", "Paper I", [("Telangana history, movement, geography and economy", "Telangana topics run through the paper."), ("Current affairs and everyday science", "Asked every year.")])
focus("TGPSC Group 4", "Paper II", [("Secretarial abilities: reasoning, comprehension, arranging and filing", "The whole second paper: practise with past-style questions.")])

# ---------- After Class 10 ----------
for _exam in ("APRJC CET", "TGRJC CET"):
    focus(_exam, "Mathematics", [("Your Class 10 maths textbook exercises", "50 marks: every chapter of the Class 10 syllabus can be asked.")])
    focus(_exam, "Physical Science", [("Class 10 physics and chemistry chapters", "50 marks for MPC and BPC groups.")])
    focus(_exam, "English", [("Grammar and reading comprehension", "50 marks in every group.")])

# ---------- write ----------
with open(os.path.join(ROOT, "exam_focus.json"), "w", encoding="utf-8") as f:
    json.dump(FOCUS, f, ensure_ascii=False, indent=2)
    f.write("\n")
exams = {(r["state"], r["exam_name"]) for r in FOCUS}
print(f"{len(FOCUS)} focus topics across {len(exams)} exams")
