"""Chapter 44 world: Northlight's FDE function over its first twelve months.

Deterministic, labeled stand-in. Every person, score and count here is modeled on the story (Northlight AI, Boston,
Laura Finch's FDE function) and replayed exactly so the outputs in the chapter reproduce. Month 1 is the month Callum
Reid and Sofia Brennan joined (their month one at Greystone). No model calls.
"""

COMPETENCIES = ["discovery", "decomposition", "build", "evaluation", "integration", "governance",
                "communication", "judgment"]
SHORT = dict(zip(COMPETENCIES, ["disc", "decomp", "build", "eval", "integ", "gov", "comm", "judg"]))

# Field profile, 0 to 3, from Laura Finch's month-7 evidence review (what each person had done on an engagement,
# not what they said in an interview). 3 = can lead it at a customer alone; 2 = does it alone; 1 = with help; 0 = not seen.
PROFILE = {
    "lead FDE":       dict(discovery=3, decomposition=3, build=2, evaluation=2, integration=3, governance=3, communication=3, judgment=3),
    "Callum Reid":    dict(discovery=2, decomposition=3, build=2, evaluation=1, integration=3, governance=2, communication=3, judgment=2),
    "Sofia Brennan":  dict(discovery=1, decomposition=2, build=3, evaluation=3, integration=1, governance=1, communication=2, judgment=2),
    "Jonah Webb":    dict(discovery=0, decomposition=2, build=3, evaluation=2, integration=2, governance=1, communication=1, judgment=1),
    "Maya Brooks":  dict(discovery=3, decomposition=2, build=2, evaluation=2, integration=2, governance=2, communication=3, judgment=3),
    "Aisha Rahman":   dict(discovery=3, decomposition=2, build=1, evaluation=2, integration=1, governance=3, communication=2, judgment=2),
    # month-12 hires from the redesigned exercise (profile at their month-12 start, from the exercise and references)
    "Leo Martens":    dict(discovery=3, decomposition=2, build=2, evaluation=2, integration=2, governance=1, communication=3, judgment=2),
    "Imogen Clarke":  dict(discovery=2, decomposition=3, build=3, evaluation=2, integration=2, governance=2, communication=2, judgment=2),
}

# Headcount events: (month, person, event, note)
EVENTS = [
    (1, "lead FDE", "in", "on the Caldwell account before the function existed"),
    (1, "Callum Reid", "in", "ex-integrator, Manchester"),
    (1, "Sofia Brennan", "in", "ex-model lab deployment team"),
    (4, "Jonah Webb", "in", "old loop: take-home build, system design, conversation"),
    (4, "Maya Brooks", "in", "old loop"),
    (7, "Aisha Rahman", "in", "old loop; ex-clinical informatics analyst"),
    (9, "Jonah Webb", "out", "moved to Northlight's platform team"),
    (11, "Maya Brooks", "out", "left Northlight to work independently"),
    (12, "Leo Martens", "in", "new exercise; ex-support engineer at a claims software firm"),
    (12, "Imogen Clarke", "in", "new exercise; ex-data engineer at a hospital system"),
]

# The four engagements in month 12 and the competencies each needs at level 3 somewhere on its staff.
ENGAGEMENTS = {
    "Caldwell":    dict(fte=0.3, needs=["evaluation", "governance"], phase="retained duties after hand-over"),
    "Greystone":   dict(fte=1.8, needs=["governance", "discovery", "evaluation", "communication"], phase="shadow"),
    "Pennant":     dict(fte=1.2, needs=["integration", "build", "judgment"], phase="managed service with on-call"),
    "Harbourline": dict(fte=2.4, needs=["governance", "evaluation", "communication", "discovery", "decomposition"], phase="build"),
}

# ---- hiring exercise ------------------------------------------------------------------------------------------
# Four exercises; each observes three competencies (1 to 4, behavioral anchors in practice.ANCHORS).
EXERCISES = {
    "E1 discovery role-play (45 min, role-played adjuster)": ["discovery", "communication", "judgment"],
    "E2 classify this workflow (40 min, whiteboard)": ["decomposition", "governance", "judgment"],
    "E3 paired build on a broken fixture (90 min)": ["build", "evaluation", "integration"],
    "E4 the sponsor note (30 min, written)": ["communication", "evaluation", "governance"],
}
OLD_LOOP = {
    "take-home build (4 h)": ["build", "evaluation"],
    "system design (60 min)": ["decomposition", "integration"],
    "conversation with Laura (45 min, unscored)": [],
}
WEIGHTS = dict(discovery=0.18, decomposition=0.12, build=0.15, evaluation=0.12, integration=0.10, governance=0.08,
               communication=0.13, judgment=0.12)
FLOORS = dict(discovery=2, build=2, communication=2, judgment=2)
BAR = 2.75          # weighted mean needed for an offer under the new rubric
OLD_BAR = 3.0       # mean of scored competencies under the old loop

# Candidate pool, months 9 to 11 (scores 1 to 4 per competency, consensus after the debrief).
CANDIDATES = {
    "C-1": dict(discovery=3, decomposition=3, build=3, evaluation=3, integration=2, governance=2, communication=3, judgment=3),
    "C-2": dict(discovery=2, decomposition=2, build=2, evaluation=2, integration=2, governance=2, communication=2, judgment=2),
    "C-3": dict(discovery=1, decomposition=4, build=4, evaluation=4, integration=4, governance=3, communication=2, judgment=2),
    "C-4": dict(discovery=4, decomposition=3, build=2, evaluation=2, integration=3, governance=3, communication=4, judgment=3),
    "C-5": dict(discovery=3, decomposition=2, build=1, evaluation=2, integration=2, governance=3, communication=3, judgment=3),
    "C-6": dict(discovery=3, decomposition=4, build=4, evaluation=3, integration=3, governance=2, communication=3, judgment=3),
    "C-7": dict(discovery=2, decomposition=3, build=3, evaluation=3, integration=3, governance=3, communication=2, judgment=1),
    "C-8": dict(discovery=3, decomposition=3, build=3, evaluation=3, integration=3, governance=3, communication=3, judgment=2),
}
OUTCOME = {"C-1": "declined (competing offer)", "C-4": "accepted: Leo Martens", "C-6": "accepted: Imogen Clarke",
           "C-8": "declined (competing offer)"}
# Jonah Webb's month-4 packet re-read under the new rubric: discovery was never observed.
JONAH_M4 = dict(discovery=None, decomposition=3, build=4, evaluation=3, integration=3, governance=None,
                communication=None, judgment=None)

# Discovery role-play ratings by three interviewers for eight recordings, before and after behavioral anchors.
RATERS = ["Laura Finch", "Callum Reid", "Sofia Brennan"]
RATINGS_BEFORE = {"Laura Finch": [2, 3, 1, 4, 3, 2, 3, 2], "Callum Reid": [3, 3, 2, 3, 2, 2, 4, 3],
                  "Sofia Brennan": [1, 2, 1, 3, 3, 3, 2, 2]}
RATINGS_AFTER = {"Laura Finch": [3, 2, 1, 4, 3, 3, 2, 3], "Callum Reid": [3, 2, 1, 4, 3, 3, 3, 3],
                 "Sofia Brennan": [3, 2, 2, 4, 3, 3, 2, 3]}

# ---- load and rotation ----------------------------------------------------------------------------------------
# Monthly travel days, overnight pages (22:00 to 06:00 local) and the account each person was on. None = not on team.
_ = None
LOAD = {
    "lead FDE":      dict(travel=[9, 10, 10, 9, 8, 9, 8, 7, 6, 7, 6, 5], pages=[0, 0, 1, 1, 2, 1, 1, 1, 0, 1, 1, 0],
                          account=["Caldwell"] * 9 + ["Harbourline"] * 3),
    "Callum Reid":   dict(travel=[11, 10, 9, 8, 8, 7, 7, 8, 7, 6, 6, 6], pages=[0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0],
                          account=["Greystone"] * 12),
    "Sofia Brennan": dict(travel=[8, 8, 7, 6, 6, 5, 6, 5, 5, 5, 6, 5], pages=[0, 0, 0, 1, 1, 2, 1, 1, 1, 1, 0, 0],
                          account=["Greystone"] * 3 + ["Caldwell"] * 9),
    "Jonah Webb":   dict(travel=[_, _, _, 6, 7, 8, 8, 9, _, _, _, _], pages=[_, _, _, 0, 1, 2, 2, 2, _, _, _, _],
                          account=[_, _, _, "Pennant", "Pennant", "Pennant", "Greystone", "Greystone", _, _, _, _]),
    "Maya Brooks": dict(travel=[_, _, _, 8, 10, 11, 12, 12, 12, 11, _, _], pages=[_, _, _, 0, 2, 5, 8, 11, 12, 14, _, _],
                          account=[_, _, _, "Pennant", "Pennant", "Pennant", "Pennant", "Pennant", "Pennant", "Pennant", _, _]),
    "Aisha Rahman":  dict(travel=[_, _, _, _, _, _, 6, 8, 9, 9, 8, 8], pages=[_, _, _, _, _, _, 0, 0, 1, 1, 2, 1],
                          account=[_, _, _, _, _, _, "Greystone", "Greystone", "Greystone", "Greystone", "Greystone", "Greystone"]),
    "Leo Martens":   dict(travel=[_] * 11 + [5], pages=[_] * 11 + [0], account=[_] * 11 + ["Pennant"]),
    "Imogen Clarke": dict(travel=[_] * 11 + [6], pages=[_] * 11 + [0], account=[_] * 11 + ["Harbourline"]),
}
LOAD_RED = 3.0          # load index at or above this for two consecutive months is a red flag
TRAVEL_CAP = 8          # days a month under the rotation policy
MAX_MONTHS_ON_ACCOUNT = 6
ROTA_DEPTH = 3          # people sharing an overnight rota under the policy

# ---- career ladder --------------------------------------------------------------------------------------------
LEVELS = ["FDE I", "FDE II", "Senior FDE", "Staff FDE", "Principal FDE"]
# Each level requires every evidence kind listed (counts are minimums); evidence is a dated artifact, not activity.
CRITERIA = {
    "FDE II": {"workstream to Build Complete": 1, "discovery session run alone": 1},
    "Senior FDE": {"workstream to Build Complete": 2, "discovery session run alone": 3, "gate passed as lead": 1,
                   "hand-over led (readiness >= 0.80)": 1, "named customer reference": 1},
    "Staff FDE": {"gate passed as lead": 3, "hand-over led (readiness >= 0.80)": 2, "customers led": 2,
                  "playbook adopted by another pod": 1, "review finding closed as owner": 2},
    "Principal FDE": {"customers led": 3, "practice change adopted": 1, "playbook adopted by another pod": 2,
                      "executive or regulator session led": 2},
}
NOT_EVIDENCE = {"commits", "pull requests", "demos given", "hours logged", "tickets closed", "slides written"}
PACKETS = {
    "Sofia Brennan (for Senior FDE, month 12)": {
        "workstream to Build Complete": 2, "discovery session run alone": 3, "gate passed as lead": 1,
        "hand-over led (readiness >= 0.80)": 1, "named customer reference": 2, "review finding closed as owner": 1},
    "Callum Reid (for Senior FDE, month 12)": {
        "workstream to Build Complete": 2, "discovery session run alone": 6, "gate passed as lead": 1,
        "named customer reference": 1, "review finding closed as owner": 4},
    "packet P-3 (for Senior FDE, failure injection)": {
        "commits": 412, "pull requests": 38, "demos given": 9, "hours logged": 1860, "tickets closed": 141,
        "workstream to Build Complete": 1},
}

# ---- what to learn --------------------------------------------------------------------------------------------
# (skill, half-life in years (Laura Finch's estimate, labeled as judgment), share of Northlight's hours-ledger
#  task codes across the four engagements where the skill was used, months 1 to 12)
SKILLS = [
    ("structured discovery interviewing", 15, 1.00), ("writing for a sponsor", 20, 1.00),
    ("evaluation design with domain experts", 8, 1.00), ("SQL and data modeling", 20, 0.90),
    ("identity and access patterns", 10, 0.90), ("answering a security questionnaire", 6, 0.80),
    ("one regulated domain in depth", 12, 0.50), ("cloud infrastructure as code", 4, 0.50),
    ("one agent framework's API", 1, 0.40), ("one model's quirks", 0.5, 0.70), ("prompt phrasing tricks", 0.5, 0.60),
]

# ---- going independent ----------------------------------------------------------------------------------------
# Portfolio claims: (claim, artifact, permission, metric with scorer)  permission: shareable | anonymized | blocked
PORTFOLIO_V1 = [
    ("cut intake backlog at a logistics customer", "internal dashboard screenshot", "blocked", "matched rate, customer team"),
    ("ran a shadow week on 2,100 documents", "customer report", "blocked", "agreement, customer reconciliation team"),
    ("built an EDI parser", "source code", "blocked", None),
    ("answered a 41-question security review", "questionnaire answers", "blocked", "findings, customer security lead"),
    ("designed an overnight on-call rota", "rota spreadsheet", "blocked", None),
    ("wrote a hand-over readiness report", "report", "blocked", "readiness, customer"),
    ("spoke at a meetup on shadow mode", "public talk recording", "shareable", None),
    ("open-source evaluation suite example", "public repository", "shareable", "accuracy, own gold set"),
    ("references from two customer engineers", "reference letters", "blocked", None),
]
PORTFOLIO_V2 = [
    ("cut intake backlog at a logistics customer", "anonymized case note, approved by Northlight", "anonymized", "matched rate, customer team"),
    ("ran a shadow week on 2,100 documents", "anonymized case note, approved by Northlight", "anonymized", "agreement, customer reconciliation team"),
    ("built an EDI parser", "rebuilt on public EDI samples, re-runnable", "shareable", "parse rate, own test set"),
    ("answered a 41-question security review", "method write-up, no customer content", "shareable", None),
    ("designed an overnight on-call rota", "rota template and load model", "shareable", "load index, own model"),
    ("wrote a hand-over readiness report", "blank template plus scoring code", "shareable", "readiness, re-runnable"),
    ("spoke at a meetup on shadow mode", "public talk recording", "shareable", None),
    ("open-source evaluation suite example", "public repository", "shareable", "accuracy, own gold set"),
    ("references from two customer engineers", "reference contacts, permission given", "shareable", None),
]
# Runway model, US dollars (illustrative; Chapter 46 owns pricing). Monthly fixed cost covers professional-indemnity
# insurance, health cover, tools, accounting and travel not billed to a client.
RUNWAY = dict(savings=60000, fixed_monthly=6500, day_rate=1400, working_days=20)
SCENARIOS = {
    "v1 portfolio (1 with a metric)": dict(first_month=6, ramp=[0.20, 0.35, 0.45, 0.50], clients=2),
    "v2 portfolio (6 with a metric)": dict(first_month=3, ramp=[0.40, 0.55, 0.60, 0.60], clients=2),
    "one client at 90%, ends month 6 (failure injection)": dict(first_month=2, ramp=[0.90, 0.90, 0.90, 0.90], clients=1, ends=6, gap=6),
}
