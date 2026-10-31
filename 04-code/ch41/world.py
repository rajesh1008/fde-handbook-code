"""Chapter 41 lab world: Caldwell and Pennant hand-over data as a deterministic stand-in.
Names, roles and canon (modes rule, monitors M1 to M6, key rotation with one-hour grace, the 03:30 Pennant deadline)
come from the book's style sheet. Counts, minutes and item statuses are the lab's stand-in values, labeled as such."""
import _paths  # noqa: F401
from fieldkit.handover import Item, Alert, Step, Runbook, Scenario

CW = {"caldwellmutual.example"}
PN = {"pennant.example"}
CW_PEOPLE = {"Anne Kessler", "Priya Natarajan", "Tom Whitfield", "Lena Ortiz", "Ruth Calloway", "Owen Pryce",
             "Catherine Doyle", "Joan Mercer", "Daniel Reyes", "platform on-call rota"}
PN_PEOPLE = {"Jenna Ruiz", "Kofi Mensah", "Dana Whitaker", "Marisol Vega", "Annelies de Vries"}

ITEMS = [  # id, dimension, text, gate
    ("R1", "runbooks", "every runbook has a named customer owner", True),
    ("R2", "runbooks", "a runbook executed end to end in a drill", False),
    ("R3", "runbooks", "mode switch live to shadow to off done by the customer", False),
    ("R4", "runbooks", "gateway key rotation recovery done by the customer", False),
    ("E1", "reference", "engagement reference read along a stakeholder path and used", False),
    ("E2", "reference", "architecture view regenerated from the deployed config", False),
    ("E3", "reference", "every prompt and workaround has owner, rationale and test", False),
    ("T1", "training", "operators work every review queue task", False),
    ("T2", "training", "engineers ship a prompt change through the merge gate", False),
    ("T3", "training", "engineers run the evaluation suite and read the comparison", False),
    ("T4", "training", "engineers dry-run a model upgrade under change control", False),
    ("M1", "monitoring", "every alert routes to a customer-owned destination", True),
    ("M2", "monitoring", "monitors M1 to M6 computed by customer jobs", False),
    ("M3", "monitoring", "monthly monitoring report produced by the customer", False),
    ("M4", "monitoring", "on-call rota staffed by the customer", False),
    ("C1", "raci", "every activity has exactly one customer accountable", True),
    ("C2", "raci", "vendor appears only as responsible or consulted", False),
    ("D1", "drill", "failure drill passed by the customer alone", True),
    ("D2", "drill", "rollback drill run by the customer", False),
    ("D3", "drill", "return from off via shadow done by the customer", False),
]
_OC, _AK, _PN, _TW, _LO, _RC, _OP = ("platform on-call rota", "Anne Kessler", "Priya Natarajan", "Tom Whitfield",
                                     "Lena Ortiz", "Ruth Calloway", "Owen Pryce")
CALDWELL_AFTER = {  # day 183
    "R1": ("alone", (_AK, _PN, _RC)), "R2": ("alone", (_OC, _PN)), "R3": ("alone", (_AK, _OC)),
    "R4": ("alone", (_OC, _PN)), "E1": ("alone", (_OC, _OP, _TW)), "E2": ("alone", (_PN,)),
    "E3": ("assisted", (_OP, _PN)), "T1": ("alone", (_TW, _LO)), "T2": ("alone", (_OP, _OC)),
    "T3": ("alone", (_OP,)), "T4": ("assisted", (_PN, _OC)), "M1": ("alone", (_OC, _PN)),
    "M2": ("alone", (_OP, _RC)), "M3": ("assisted", (_AK, _RC)), "M4": ("alone", (_OC,)),
    "C1": ("alone", (_AK, _PN)), "C2": ("alone", (_AK, _PN)), "D1": ("alone", (_OC, _PN)),
    "D2": ("assisted", (_OC, _PN)), "D3": ("alone", (_AK, _OC, _RC)),
}
CALDWELL_BEFORE = dict(CALDWELL_AFTER, M1=("exists", ()), D1=("assisted", (_OC,)))  # day 176, drill 1
_JR, _KM, _DW, _MV = "Jenna Ruiz", "Kofi Mensah", "Dana Whitaker", "Marisol Vega"
PENNANT = {
    "R1": ("alone", (_JR, _KM)), "R2": ("exists", ()), "R3": ("alone", (_JR,)), "R4": ("exists", ()),
    "E1": ("assisted", (_KM, _DW)), "E2": ("exists", ()), "E3": ("exists", ()), "T1": ("alone", (_DW, _MV)),
    "T2": ("exists", ()), "T3": ("assisted", (_DW,)), "T4": ("exists", ()), "M1": ("exists", ()),
    "M2": ("assisted", (_KM,)), "M3": ("alone", (_JR,)), "M4": ("exists", ()), "C1": ("alone", (_JR, _KM, _DW)),
    "C2": ("assisted", (_KM,)), "D1": ("assisted", (_KM,)), "D2": ("exists", ()), "D3": ("assisted", (_JR, _KM)),
}


def items(state):
    return [Item(i, d, t, state[i][0], state[i][1], g) for i, d, t, g in ITEMS]


OC = "claims-oncall@caldwellmutual.example"
NL = "nl-caldwell-alerts@northlight.example"
ALERTS_V1 = [
    Alert("A-01", "M1 calibration drift", "claims-owner@caldwellmutual.example", "RB-01"),
    Alert("A-02", "M2 input drift", "claims-owner@caldwellmutual.example", "RB-01"),
    Alert("A-03", "manual intake backlog over 200", OC, "RB-05"),
    Alert("A-04", "M3 review override rate", "claims-owner@caldwellmutual.example", "RB-01"),
    Alert("A-05", "M4 citation audit overdue", "claims-owner@caldwellmutual.example", "RB-01"),
    Alert("A-06", "M5 route share outside band", "claims-owner@caldwellmutual.example", "RB-01"),
    Alert("A-07", "gateway 401 rate over 2%", NL, "RB-03"),
    Alert("A-08", "gateway p95 latency over 20 s", OC, "RB-05"),
    Alert("A-09", "reconciliation unexplained over 0", "claims-data@caldwellmutual.example", "RB-02"),
    Alert("A-10", "dead-letter queue over 25", OC, "RB-03"),
    Alert("A-11", "M6 monitoring job missed", "mrm-monitor@caldwellmutual.example", "RB-01"),
    Alert("A-12", "cost per document over budget", "claims-owner@caldwellmutual.example", ""),
    Alert("A-13", "pinned model deprecation notice", "claims-platform@caldwellmutual.example", "RB-06"),
    Alert("A-14", "audit log chain break", OC, "RB-04"),
]
ALERTS_V2 = [Alert(a.id, a.monitor, OC, a.runbook) if a.id == "A-07" else a for a in ALERTS_V1]
ROTA = {OC: ("Caldwell platform on-call", 4), NL: ("Northlight on-call", 0),
        "claims-owner@caldwellmutual.example": ("Anne Kessler's desk (business hours)", None),
        "claims-data@caldwellmutual.example": ("Ruth Calloway's team (business hours)", None)}

S = lambda a, r, v="", x="": Step(a, r, v, x)  # noqa: E731
RUNBOOKS_V2 = [
    Runbook("RB-01", "quality monitor alarm", "A-01", "quality", "shadow", "Anne Kessler", (
        S("set mode to shadow from the console", "claims owner", "console shows shadow, drafts stop reaching adjusters"),
        S("pull the alarm sample and rescore 30 with the rubric", "senior adjuster", "rescored sheet saved to the case"),
        S("open a change for the fix through the merge gate", "QE lead", "gate run attached, four-cell table green"),
        S("return to live after five clean shadow days", "claims owner", "decision record signed"))),
    Runbook("RB-02", "reconciliation unexplained count", "A-09", "data", "off", "Ruth Calloway", (
        S("set mode to off", "platform on-call", "runner stopped, intake falls back to manual queue"),
        S("list unexplained documents from the reconciliation report", "claims data manager", "list attached"),
        S("trace each to source, page, extraction", "claims data manager", "lineage row per document"),
        S("fix or quarantine, then rerun reconciliation", "platform on-call", "unexplained count is 0")),
        exit_via="shadow"),
    Runbook("RB-03", "gateway key rotation failure", "A-07", "availability", "fail-closed", "Priya Natarajan", (
        S("confirm 401s and that documents fail closed to the manual queue", "platform on-call", "401 rate and queue depth read"),
        S("fetch the current key from Caldwell's secrets manager and restart the adapter", "platform on-call",
          "adapter reports the new key id"),
        S("run the post-rotation smoke test", "platform on-call", "smoke test passes on five canned documents"),
        S("replay the dead-letter queue", "platform on-call", "dead-letter depth is 0"),
        S("reconcile and close the incident record", "platform on-call", "unexplained count is 0, record closed"))),
    Runbook("RB-04", "audit log chain break", "A-14", "security", "off", "Priya Natarajan", (
        S("set mode to off", "platform on-call", "runner stopped"),
        S("snapshot the log and notify security", "platform on-call", "ticket number recorded"),
        S("verify the chain from the last good hash", "architect", "break located to one segment")), exit_via="shadow"),
    Runbook("RB-05", "intake backlog or latency", "A-03", "availability", "fail-closed", "Tom Whitfield", (
        S("move manual queue to the overflow adjuster rota", "senior adjuster", "queue owner set"),
        S("check gateway latency and dead-letter depth", "platform on-call", "both read and logged"))),
    Runbook("RB-06", "pinned model deprecation notice", "A-13", "quality", "shadow", "Priya Natarajan", (
        S("record the notice in the deprecation register", "architect", "register row with retirement date"),
        S("run the candidate model in shadow against the gold set", "QE lead", "four-cell table attached"),
        S("raise the upgrade change under Caldwell change control", "architect", "change approved by the board"))),
]
_r = {rb.id: rb for rb in RUNBOOKS_V2}
RUNBOOKS_V1 = [
    _r["RB-01"],
    Runbook("RB-02", _r["RB-02"].title, "A-09", "data", "off", "Ruth Calloway", _r["RB-02"].steps, exit_via=""),
    Runbook("RB-03", _r["RB-03"].title, "A-07", "availability", "fail-closed", "Priya Natarajan",
            _r["RB-03"].steps[:1] + (S("page Callum Reid at Northlight for the new key", "platform on-call",
                                       "Northlight confirms"),) + _r["RB-03"].steps[2:]),
    _r["RB-04"],
    Runbook("RB-05", _r["RB-05"].title, "A-03", "availability", "fail-closed", "Tom Whitfield",
            (S("move manual queue to the overflow adjuster rota", "senior adjuster"),) + _r["RB-05"].steps[1:]),
    Runbook("RB-06", _r["RB-06"].title, "A-13", "quality", "shadow", "Sofia Brennan", _r["RB-06"].steps),
]
RB03_MINUTES = [("401s confirmed, documents fail closed", 6), ("new key loaded, adapter restarted", 9),
                ("smoke test passes", 4), ("dead-letter queue replayed", 8), ("reconciled, record closed", 5)]
KEY_DRILL = Scenario("gateway key rotation failure", fault_at=180, alert="A-07", detect_lag=2,
                     backstop="A-03", backstop_at=180 + 111)  # grace ends 03:00; backlog 200 at 1.8 docs/min

RACI_V1 = [
    ("set mode live, shadow or off", "platform on-call", "Anne Kessler", "Northlight informed"),
    ("weekly drift audit", "Owen Pryce", "Anne Kessler", "Northlight consulted"),
    ("gold set refresh every 30 days", "Sofia Brennan", "Northlight", "Owen Pryce consulted"),
    ("prompt change through merge gate", "Owen Pryce", "Priya Natarajan, Owen Pryce", "Northlight consulted"),
    ("monthly monitoring report", "Ruth Calloway", "Anne Kessler", "Catherine Doyle informed"),
    ("gateway key rotation", "platform on-call", "Priya Natarajan", "Northlight informed"),
    ("pinned model deprecation response", "Northlight", "Northlight", "Priya Natarajan consulted"),
    ("incident response", "platform on-call", "Priya Natarajan", "Northlight on-call consulted"),
    ("quarterly rollback drill", "platform on-call", "Priya Natarajan", "Northlight consulted"),
    ("product fixes and releases", "Northlight", "Priya Natarajan", "Owen Pryce consulted"),
]
RACI_V2 = [
    RACI_V1[0], RACI_V1[1],
    ("gold set refresh every 30 days", "Owen Pryce", "Owen Pryce", "Tom Whitfield consulted"),
    ("prompt change through merge gate", "Owen Pryce", "Owen Pryce", "Northlight consulted"),
    RACI_V1[4], RACI_V1[5],
    ("pinned model deprecation response", "Northlight (notice, candidate); Priya Natarajan (change)", "Priya Natarajan",
     "Owen Pryce consulted"),
    RACI_V1[7], RACI_V1[8], RACI_V1[9],
]

SECTIONS = {1: ("what it does and does not do", 6), 2: ("architecture as deployed", 12), 3: ("data map and retention", 10),
            4: ("modes and the switch", 5), 5: ("evaluation suite and gold set", 14), 6: ("monitors and monthly report", 11),
            7: ("alert catalog", 6), 8: ("runbooks", 18), 9: ("change and release", 9),
            10: ("decisions and workarounds register", 13), 11: ("RACI and contacts", 4), 12: ("Evidence Pack index", 7)}
NEEDS = {"operator": [1, 4, 11], "on-call engineer": [2, 4, 7, 8, 11], "owner": [1, 4, 6, 11, 12],
         "architect": [2, 3, 9, 10, 11], "QE lead": [5, 6, 9, 10], "model risk": [1, 5, 6, 12], "auditor": [3, 12, 11]}
PATHS_V1 = {"operator": [1, 4], "on-call engineer": [2, 4, 8], "owner": [1, 4, 6, 11, 12], "architect": [2, 3, 9, 10, 11],
            "QE lead": [5, 6, 9], "model risk": [1, 5, 6, 12], "auditor": [3, 12, 11]}
PATHS_V2 = dict(PATHS_V1, **{"operator": [1, 4, 11], "on-call engineer": [2, 4, 7, 8, 11], "QE lead": [5, 6, 9, 10]})

# training: tasks per cohort, statuses per session (a = alone, s = assisted, n = not yet)
TRAIN = {"operators (14 adjusters)": ["nnnnnnnn", "aassnnnn", "aaaaasss", "aaaaaaaa"],
         "engineers (platform and QE)": ["snnnnnnnnn", "aaassnnnnn", "aaaaaassss", "aaaaaaaass"]}
TRAIN_DAYS = [165, 170, 175, 180]
TRAIN_TASKS = {"operators (14 adjusters)": ["work the review queue", "mark a draft wrong with a reason code",
                                            "read the source citation", "send to manual intake",
                                            "flag a supplement", "read the console mode", "raise a quality flag",
                                            "work the overflow rota"],
               "engineers (platform and QE)": ["read the alert catalog", "switch modes", "rotate the key by hand",
                                               "run the smoke test", "replay the dead-letter queue",
                                               "run the evaluation suite", "read the four-cell comparison",
                                               "ship a prompt change", "dry-run a model upgrade",
                                               "rerun the rollback drill"]}

PN_NL = "nl-pennant-oncall@northlight.example"
PN_ALERTS_V1 = [Alert("P-01", "TMS CSV not arrived by 02:15", PN_NL, "PRB-01"),
                Alert("P-02", "file drop volume outside band", PN_NL, "PRB-01"),
                Alert("P-03", "exception queue over 400", "freight-audit@pennant.example", "PRB-02"),
                Alert("P-04", "FX table stale", "treasury@pennant.example", "PRB-03")]
PN_ALERTS_V2 = [Alert(a.id, a.monitor, "integration@pennant.example", a.runbook) if a.dest == PN_NL else a
                for a in PN_ALERTS_V1]
PN_ROTA = {PN_NL: ("Northlight on-call", 0), "integration@pennant.example": ("Kofi Mensah's team (from 06:00)", None)}
PN_DRILL = Scenario("file drop volume guard", fault_at=124, alert="P-02", detect_lag=2, deadline=210)
PN_MINUTES = [("volume checked against the TMS export log", 10), ("file re-pulled from TMS", 15),
              ("guard rerun, file accepted", 5), ("matching run completed", 25)]
