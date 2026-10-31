"""Chapter 45 fixtures. Deterministic stand-in: the loops, scores and transcripts are fixtures written for this
lab, shaped like Northlight's records; no candidate data and no model calls."""
import _paths  # noqa: F401
from fieldkit.hiring import Probe, Round, Loop, Score, SELF_REPORT

O = Probe
S = lambda c: Probe(c, SELF_REPORT)

# The loop that hired the two engineers who left (Chapter 44): every observed round tests build.
LOOP_V0 = Loop("v0 (before)", [
    Round("R1", "recruiter screen", 30, (S("communication"), S("build"))),
    Round("R2", "coding screen", 60, (O("build"),)),
    Round("R3", "take-home: build an assistant over 200 PDFs", 480, (O("build"),), takehome=True),
    Round("R4", "system design", 60, (O("build"), O("decomposition"))),
    Round("R5", "culture chat", 45, (S("communication"), S("judgment"), S("discovery"))),
])

# The redesigned loop: six rounds, every competency observed at least twice, take-home optional and capped.
LOOP_V1 = Loop("v1 (after)", [
    Round("S1", "screen: explain a system you shipped to a non-engineer", 30, (O("communication"), S("judgment"))),
    Round("T1", "technical: fix a broken integration (live, or 3-hour take-home plus review)", 60, (O("build"), O("decomposition"))),
    Round("S2", "scenario: the constraint arrives mid-build", 45, (O("judgment"), O("communication"))),
    Round("D1", "on-site discovery exercise with a role-played operator", 60, (O("discovery"), O("decomposition"))),
    Round("H1", "hiring manager: one engagement, taken apart", 45, (O("judgment"), O("discovery"))),
    Round("C1", "customer panel: architect and security lead", 45, (O("communication"), O("build"))),
])

EV = {  # evidence notes, one per score, as the interviewer wrote them
    "c214": {
        ("T1", "build"): [("Callum Reid", 4, "fixed the ingest in 22 minutes, added a failing test first, clean diff")],
        ("T1", "decomposition"): [("Callum Reid", 3, "split the fix into parse, map and write steps with owners named")],
        ("D1", "discovery"): [("Sofia Brennan", 1, "proposed a pipeline at minute 6 after two questions, never asked about exceptions")],
        ("D1", "decomposition"): [("Sofia Brennan", 2, "boxes drawn early, inputs never tied to what the operator said")],
        ("H1", "discovery"): [("Laura Finch", 2, "described a past discovery as reading the API docs, no user named")],
        ("H1", "judgment"): [("Laura Finch", 2, "named the security constraint but would build around it quietly")],
        ("S2", "judgment"): [("Sofia Brennan", 3, "chose shadow mode over a deadline and gave the reason in one sentence")],
        ("S2", "communication"): [("Sofia Brennan", 3, "explained the delay to the sponsor role-player with a date")],
        ("S1", "communication"): [("Laura Finch", 3, "explained the system to a non-engineer with one number")],
        ("C1", "communication"): [("Callum Reid", 2, "answered the security lead with a framework list, not our controls")],
        ("C1", "build"): [("Callum Reid", 4, "sketched the gateway adapter and rotation handling on the spot")],
    },
    "c231": {
        ("T1", "build"): [("Callum Reid", 3, "working fix in 41 minutes, test for the bad row, did not refactor")],
        ("T1", "decomposition"): [("Callum Reid", 3, "listed steps, inputs and outputs before typing anything")],
        ("D1", "discovery"): [("Sofia Brennan", 4, "found nine of eleven facts and three exceptions, confirmed back twice")],
        ("D1", "decomposition"): [("Sofia Brennan", 3, "steps ordered by risk once the exceptions were known")],
        ("H1", "discovery"): [("Laura Finch", 3, "named the operator who corrected the process map and what changed")],
        ("H1", "judgment"): [("Laura Finch", 4, "said what would have changed the decision and who signed it")],
        ("S2", "judgment"): [("Sofia Brennan", 3, "chose the narrower scope and wrote down what was dropped")],
        ("S2", "communication"): [("Sofia Brennan", 4, "gave the sponsor role-player a number and a next step")],
        ("S1", "communication"): [("Laura Finch", 3, "pitched to a non-engineer, answered the question asked")],
        ("C1", "communication"): [("Callum Reid", 3, "answered the security lead with our controls and one gap")],
        ("C1", "build"): [("Callum Reid", 3, "described the gateway path and what fails on key rotation")],
    },
    "c236": {
        ("T1", "build"): [("Callum Reid", 3, "working fix in 48 minutes with a test for the null case")],
        ("T1", "decomposition"): [("Callum Reid", 3, "steps and owners named before the first change")],
        ("D1", "discovery"): [("Sofia Brennan", 3, "found seven facts and two exceptions, confirmed back once")],
        ("D1", "decomposition"): [("Sofia Brennan", 3, "decomposed only after discovery, interfaces named")],
        ("H1", "discovery"): [("Laura Finch", 3, "named the user who changed the scope and the date")],
        ("H1", "judgment"): [("Laura Finch", 3, "picked the narrower scope with a reason")],
        ("S2", "judgment"): [("Sofia Brennan", 3, "good")],  # refused: no evidence written
        ("S2", "communication"): [("Sofia Brennan", 2, "accurate but pitched at engineers, sponsor role-player lost")],
        ("S1", "communication"): [("Laura Finch", 4, "explained the system with a number and a next step")],
        ("C1", "communication"): [("Callum Reid", 3, "answered the architect directly and named the open item", False)],
        ("C1", "build"): [("Callum Reid", 3, "described the adapter and the rotation failure")],
        ("C1", "judgment"): [("Callum Reid", 4, "seemed to have very sound judgment overall in the room")],  # not probed in C1
    },
}


def scores(cid):
    out = []
    for (rnd, comp), rows in EV[cid].items():
        for row in rows:
            who, v, ev = row[:3]
            before = row[3] if len(row) > 3 else True
            out.append(Score(who, rnd, comp, v, ev, before))
    return out


# What the old loop recorded for the same build-heavy profile: observed build scores only.
V0_SCORES = [("R2", "build", 4), ("R3", "build", 4), ("R4", "build", 4), ("R4", "decomposition", 3)]

# Discovery exercise: a returns-authorization desk at a parts distributor (practice workflow, not a customer).
FACTS = {  # id: is an exception
    "F1": False,  # requests arrive by email and a web form
    "F2": False,  # order number is in the subject line most of the time
    "F3": False,  # the ERP holds the order and the ship date
    "F4": False,  # 30-day window from delivery, not from order
    "F5": False,  # reason codes are free text
    "F6": False,  # refunds go back to the original payment
    "F7": False,  # the desk replies within one working day
    "F8": True,   # refunds over 500 dollars need the supervisor
    "F9": True,   # distributor accounts have 60 days, not 30
    "F10": True,  # hazardous parts cannot be shipped back; credit only
    "F11": True,  # the supervisor overrides the window for three named accounts
}
TRANSCRIPTS = {
    "c214": [(2, "question", "F1"), (4, "question", "F2"), (6, "solution", None), (9, "solution", None),
             (14, "solution", None), (20, "question", "F3"), (26, "solution", None), (33, "solution", None),
             (41, "solution", None)],
    "c231": [(1, "question", "F1"), (3, "question", "F2"), (5, "question", "F3"), (8, "question", "F4"),
             (10, "confirm", "F4"), (12, "question", "F5"), (15, "question", "F8"), (17, "question", "F6"),
             (19, "question", None), (21, "question", "F9"), (23, "confirm", "F9"), (26, "question", "F10"),
             (28, "question", "F7"), (31, "solution", None), (36, "confirm", None), (44, "solution", None)],
}

STEPS = {  # whiteboard: classify this workflow (same desk)
    "1 receive request": "deterministic", "2 extract order number": "rules", "3 look up order": "deterministic",
    "4 check the window": "rules", "5 classify free-text reason": "small model", "6 approve refund over $500": "human decision",
    "7 draft the reply": "frontier model", "8 issue the refund": "deterministic",
}
CLASSIFY = {
    "c214": {"1 receive request": "deterministic", "2 extract order number": "frontier model",
             "3 look up order": "deterministic", "4 check the window": "frontier model",
             "5 classify free-text reason": "frontier model", "6 approve refund over $500": "frontier model",
             "7 draft the reply": "frontier model", "8 issue the refund": "deterministic"},
    "c231": {"1 receive request": "deterministic", "2 extract order number": "rules", "3 look up order": "deterministic",
             "4 check the window": "rules", "5 classify free-text reason": "rules",
             "6 approve refund over $500": "human decision", "7 draft the reply": "frontier model",
             "8 issue the refund": "deterministic"},
}

TAKEHOME = {
    "v0": [("working assistant over the PDFs", 0.30, True), ("retrieval quality", 0.20, True),
           ("code quality", 0.20, True), ("tests", 0.15, True), ("README", 0.15, True)],
    "v1": [("fix the failing ingest", 0.20, True), ("find the conflict in the constraint memo", 0.25, False),
           ("the three questions for the customer", 0.20, False), ("decision log: what was not built", 0.15, False),
           ("30-minute review conversation", 0.20, False)],
}

# Calibration: three interviewers score six recorded sessions on five competencies.
BASE = [[2, 3, 3, 2, 3], [4, 3, 3, 4, 3], [1, 2, 4, 2, 2], [3, 3, 2, 3, 4], [2, 2, 3, 3, 2], [3, 4, 3, 3, 3]]
COMP = ("discovery", "decomposition", "build", "judgment", "communication")


def calibration(when):
    out = []
    for s, row in enumerate(BASE, 1):
        for c, v in zip(COMP, row):
            out.append(("Laura Finch", s, c, v))
            sofia = v - 1 if (when == "before" and (s, c) in {(2, "judgment"), (4, "communication"), (6, "decomposition")}) \
                else v - 1 if (when == "after" and (s, c) == (2, "judgment")) else v
            out.append(("Sofia Brennan", s, c, max(1, sofia)))
            bump = (c in ("build", "decomposition") or (s, c) in {(1, "communication"), (5, "communication")}) \
                if when == "before" else (s, c) in {(3, "build"), (5, "decomposition")}
            out.append(("Callum Reid", s, c, min(4, v + 2 if (when == "before" and c == "build" and s in (1, 5)) else v + 1) if bump else v))
    return out


ANSWERS = {
    "weak": ("Well, there are many ways to run discovery and it really depends on the customer. I usually start by "
             "understanding their goals and then I map the process with them and make sure everyone is aligned. "
             "Communication is key, and I try to be flexible."),
    "strong": ("I run discovery by watching the work before I ask about it. At Caldwell the process map listed three "
               "intake paths and the desk showed eleven, so the map missed eight on day 9. Two of the extra paths were "
               "exceptions only one adjuster handled, and those became the first test cases. That stops being true "
               "when the work is not observable, a batch job at night, and then I read the logs instead. "
               "I would show you the walk-through notes with the eleven paths and who confirmed each one."),
}
