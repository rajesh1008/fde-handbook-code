"""Chapter 12 fixtures: Harbourline Bank's RFP for commercial-lending document intelligence, as Northlight answered it.
Harbourline is a fictional bank; every RFP line, standard, clarification and response sentence below was written for
this lab. Amounts are Canadian dollars. Week numbers count from the day the RFP was issued; register days count from
contract signature (day 0)."""
import _path  # noqa: F401
from fieldkit.bid import Question, Standard, Clarification

# --------------------------------------------------------------------------------------------- the questions (200)
SECTIONS = [  # key, title, engineering, joint, sales
    ("A", "Company, references and standing", 0, 2, 16),
    ("B", "Commercial and pricing", 0, 6, 20),
    ("C", "Legal, privacy terms, liability", 0, 5, 15),
    ("D", "Solution and target architecture", 24, 4, 0),
    ("E", "Security, identity, data protection", 22, 6, 0),
    ("F", "Model risk, evaluation, monitoring", 18, 5, 0),
    ("G", "Implementation and ways of working", 9, 12, 2),
    ("H", "Operations, support, service levels", 8, 10, 4),
    ("I", "Exit, portability, transition", 4, 5, 3),
]
NAMED = {
    "D-01": "Describe the target architecture for the solution within Harbourline's platform standards.",
    "D-05": "Describe how the solution uses Harbourline's model gateway.",
    "E-03": "Describe how users and services authenticate.",
    "F-02": "Describe how the solution will be evaluated before production use.",
    "G-01": "Describe your ways of working with Harbourline teams during implementation.",
    "H-06": "Describe logging, monitoring and evidence retention.",
    "I-01": "Describe how Harbourline could exit the service.",
    "C-07": "Describe how Harbourline data is used by your models, and the contractual terms that govern it.",
    "G-03": "Describe the delivery team and how many engineer days the fee includes.",
    "H-04": "State the availability service level and the Harbourline services it depends on.",
}
MISROUTED = {"C-07", "G-03", "H-04"}   # joint questions the bid manager sent to sales alone in week 1
TAGS = {"engineering": ("architecture",), "joint": ("delivery", "terms"), "sales": ("price",)}


def questions():
    qs = []
    for sec, title, e, j, s in SECTIONS:
        owners = ["joint"] * j + ["engineering"] * e + ["sales"] * s
        if sec == "C":                        # in C the joint questions come after the first six legal ones
            owners = ["sales"] * 6 + ["joint"] * j + ["sales"] * (s - 6)
        if sec == "H":
            owners = ["engineering"] * 3 + ["joint"] * j + ["engineering"] * (e - 3) + ["sales"] * s
        for i, o in enumerate(owners, 1):
            key = f"{sec}-{i:02d}"
            routed = "sales" if key in MISROUTED else o
            qs.append(Question(key, sec, NAMED.get(key, f"{title}: question {i}."), TAGS[o], routed))
    return qs


# --------------------------------------------------------------------------------------------- platform standards (47)
_NOT_COMPLY = {
    "PS-ID-02": ("identity", "Users are provisioned by SCIM from the bank directory.", "comply with configuration",
                 "SCIM connector to the endpoint in RFP Appendix C", "R", True, ""),
    "PS-DR-04": ("data", "No telemetry leaves Canada.", "comply with configuration",
                 "product telemetry switched off; RFP Appendix C region list", "R", False, ""),
    "PS-DR-06": ("data", "Data at rest is encrypted with bank-held keys.", "comply with configuration",
                 "customer-managed keys; RFP Appendix C key service", "R", True, ""),
    "PS-NET-03": ("network", "Services are reached by private endpoint only.", "comply with configuration",
                  "private endpoint per component", "V", False, ""),
    "PS-LOG-02": ("logging", "Logs use the bank's event format.", "comply with configuration",
                  "log formatter set to the bank schema; RFP Appendix C", "R", True, ""),
    "PS-SUR-03": ("surface", "Add-ins are published through the bank's app catalog.", "comply with configuration",
                  "add-in manifest; RFP Appendix D", "R", True, ""),
    "PS-GW-04": ("gateway", "No direct provider keys in any environment.", "deviation requested",
                 "offline evaluation harness calls the provider in an isolated test tenant", "V", True, "Martin Shaw"),
    "PS-CHG-03": ("change", "Production changes go through the change board with ten days' notice.",
                  "deviation requested", "prompt and threshold changes as a pre-approved standard change", "V", True,
                  "Martin Shaw"),
    "PS-SUR-01": ("surface", "User-facing tools run inside the productivity suite.", "deviation requested",
                  "reviewer console as a web app for six operations staff (CL-23 permits a request)", "R", True,
                  "Martin Shaw"),
    "PS-SUR-04": ("surface", "Mobile apps are distributed through the bank's store.", "not applicable", "", "V",
                  False, ""),
    "PS-NET-07": ("network", "Branch network segmentation.", "not applicable", "", "V", False, ""),
}
AREAS = [("ID", "identity", 6), ("DR", "data", 8), ("GW", "gateway", 5), ("LOG", "logging", 7),
         ("CHG", "change", 6), ("NET", "network", 7), ("SUR", "surface", 4), ("MRM", "model risk", 4)]
CUSTOMER_SYSTEM_AREAS = {"identity", "gateway", "logging", "change"}


def standards(draft="v1.0"):
    out = []
    for code, area, n in AREAS:
        for i in range(1, n + 1):
            key = f"PS-{code}-{i:02d}"
            if key in _NOT_COMPLY:
                a, text, outcome, ev, evs, names, appr = _NOT_COMPLY[key]
            else:
                a, text, outcome = area, f"{area} standard {i}", "comply"
                names = area in CUSTOMER_SYSTEM_AREAS
                ev, evs = ("RFP Appendix C" if names else "product documentation"), ("R" if names else "V")
                appr = ""
            if draft == "v0.6" and key == "PS-LOG-03":
                text, ev, evs = "Logs are retained seven years in the bank SIEM.", "product supports log export", "V"
            elif key == "PS-LOG-03":
                text, ev, evs = ("Logs are retained seven years in the bank SIEM.",
                                 "RFP Appendix C, SIEM intake by HTTPS collector", "R")
            if draft == "v0.6" and key == "PS-CHG-03":
                appr = "the change board"
            out.append(Standard(key, a, text, outcome, ev, evs, names, appr))
    return out


# --------------------------------------------------------------------------------------------- clarification log (38)
_CL = {
    9: ("Is write access to the origination system in scope for release one?", "No. Read-only in release one.",
        ("origination system",), ("write",), False, 1),
    12: ("Does the document store raise events when files arrive?", "No. Bidders should poll or list.",
         ("document store",), ("event",), False, 1),
    17: ("Does the model gateway support streaming responses?",
         "Not in the current release. It is on the gateway roadmap with no committed date.",
         ("gateway",), ("stream",), False, 1),
    23: ("Must every user-facing tool run inside the productivity suite?",
         "Yes for relationship managers and credit officers. Tools for fewer than ten staff may request a deviation.",
         (), (), True, 1),
    29: ("Does the document store keep version history?", "Yes, every version, for seven years.",
         ("document store",), ("version history",), True, 2),
    31: ("May bidders use Harbourline data to train or improve general models?", "No.",
         ("harbourline data",), ("train", "improve"), False, 2),
}


def clarifications():
    out = []
    for n in range(1, 39):
        q, a, subj, attr, holds, rnd = _CL.get(n, (f"clarification {n}", "answered in the log", (), (), True,
                                                   1 if n <= 24 else 2))
        out.append(Clarification(f"CL-{n:02d}", q, a, subj, attr, holds, rnd))
    return out


# --------------------------------------------------------------------------------------------- Northlight's response
RESPONSE_V10 = {
    "D-01": """Release one is read-and-draft: the system reads commercial-lending documents and drafts credit memo
sections for a credit officer to edit [R: RFP 1.3]. Relationship managers and credit officers will work inside the
productivity suite, as Harbourline's standards require [R: PS-SUR-01, CL-23]. Harbourline's document store does not
raise events on new files [R: CL-12]. We will find new files with a scheduled listing every 10 minutes [P].
Harbourline's document store keeps a version history for every file [R: CL-29]. Harbourline's origination system is
read-only to the solution in release one [R: CL-09]. The boundary to the origination system will carry no write path
until Harbourline decides release two scope [D: David Okafor, day 120].""",
    "D-05": """Harbourline's model gateway does not stream responses in its current release [R: CL-17]. We will return
each drafted memo section when it is complete [P]. Drafted sections will be returned through the gateway within 20
seconds for 95% of sections in shadow [V]. If incremental delivery arrives in the gateway, we will adopt it as a change
request rather than as a dependency [P]. Every model call will go through the bank's gateway, using only models on
Harbourline's approved list [R: PS-GW-01]. The approved model for release one will be chosen by Harbourline's model
risk function [D: Helen Marsh, day 30].""",
    "E-03": """Users will authenticate through Harbourline's directory with single sign-on, and the solution will hold no
local passwords [R: PS-ID-01]. Service calls will use workload identities issued by the bank, one per component, with
no shared service accounts [R: PS-ID-04]. We will provision and remove users through the bank's directory on the
day of a joiner or leaver event [V].""",
    "F-02": """Before Shadow Exit, Harbourline's credit officers will score 400 drafted memos against Harbourline's credit
review rubric [P]. The target is agreement with credit officers on at least 90% of scored memos, with the scorer and
the set named in the scope [P]. Ratios, joins and thresholds will be computed in code, never by the model, and every
computed figure in a draft will carry its lineage [V]. Model-risk approval is a separate gate owned by Harbourline,
and sprint acceptance does not grant it [R: RFP 6.4]. The sample size for shadow scoring will be set by Harbourline
under its model risk standard [D: Helen Marsh, day 45].""",
    "G-01": """We will run two-week sprints with a review on day 10 of each sprint, attended by Harbourline's product
owner [P]. An item will be Ready when it has a priority, a named accountable owner at Harbourline and acceptance
criteria that can be tested [P]. An item will be Done when the evidence for each criterion is attached [P]. An item
will be accepted, accepted with a dated follow-up, or not accepted, and a follow-up without a date will count as not
accepted [P]. Acceptance will not be production approval, and the five gates will stay with their Harbourline owners
[P]. Harbourline's product owner for the program will be named by the accountable executive [D: David Okafor, day
14].""",
    "H-02": """The service will be available 99.5% of business hours, measured at the add-in, excluding outages of
Harbourline's gateway and directory [V]. Service credits are set out in Schedule B.""",
    "H-06": """Every model call, retrieval and user action will be logged with a trace identifier [V]. Logs will be
retained for seven years in the bank's SIEM, as PS-LOG-03 requires [R: PS-LOG-03]. Traces will reach the bank's SIEM
within 5 minutes of the event [V].""",
    "I-01": """Harbourline will receive its prompts, evaluation sets, decision records and logs in open formats within 30
days of exit [V]. Northlight will support a transition for up to 90 days at the rates in Schedule B [V]. Harbourline
data will not be used to train or improve general models [R: CL-31].""",
}

# Draft v0.9 (week 5): the failure injection. A gateway capability stated as a direct customer fact on the strength of
# a remark at the bidders' conference, which the written clarification CL-17 contradicts; and a document-store claim
# written as a vendor position about the bank's own estate.
RESPONSE_V09 = dict(RESPONSE_V10)
RESPONSE_V09["D-05"] = """Harbourline's model gateway supports streaming responses, so drafted text appears in the
credit officer's pane as it is written [F: Martin Shaw, bidders' conference]. Drafted sections will begin to appear
within 2 seconds [V]. Every model call will go through the bank's gateway, using only models on Harbourline's approved
list [R: PS-GW-01]. The approved model for release one will be chosen by Harbourline's model risk function [D: Helen
Marsh, day 30]."""
RESPONSE_V09["D-01"] = RESPONSE_V10["D-01"].replace("[R: CL-29]", "[V]")

NOT_PROMISED = [
    "an accuracy figure before Harbourline's scorers and set are named",
    "any write to the origination system in release one",
    "a production date: the five gates belong to Harbourline's owners",
    "streaming drafts: CL-17 says the gateway does not stream",
]
BOUNDARY = ("Release one reads and drafts; a credit officer edits and owns every memo, and nothing we deliver is "
            "approved for production until Harbourline's gates say so.")

# Owners and due days (register days from signature) for vendor numbers and proposed designs.
OWNER_FOR = {k: "Laura Finch" for k in RESPONSE_V10}
DUE_FOR = {"D-01": 40, "D-05": 40, "E-03": 40, "F-02": 45, "G-01": 14, "H-02": 40, "H-06": 40, "I-01": 90}

# --------------------------------------------------------------------------------------------- the panel (sixty)
GROUPS = [  # name, with proof, rehearsed no proof, not rehearsed
    ("architecture and integration", 10, 1, 1),
    ("security and data", 9, 2, 0),
    ("model risk and evaluation", 9, 2, 1),
    ("delivery and ways of working", 8, 1, 0),
    ("operations and support", 7, 1, 0),
    ("commercial-technical and exit", 5, 2, 1),
]
# Of the sixty, the panel asked these (group index, rank within group); plus four questions not on the list.
ASKED = [(0, i) for i in (0, 1, 2, 3, 4, 5, 10)] + [(1, i) for i in (0, 1, 2, 9)] + \
        [(2, i) for i in (0, 1, 2, 3, 9, 11)] + [(3, i) for i in (0, 1)] + [(4, 0)] + [(5, i) for i in (0, 5)]
OFF_LIST = ["notice period if the provider retires the validated model version",
            "who at Northlight can stop the service out of hours",
            "how a relationship manager reports a wrong draft",
            "what the six-person console deviation costs if refused"]


def panel():
    rows = []
    for g, (name, proof, noproof, none) in enumerate(GROUPS):
        for i, st in enumerate(["proof"] * proof + ["rehearsed"] * noproof + ["not rehearsed"] * none):
            rows.append(dict(group=name, rank=i, status=st, asked=(g, i) in ASKED))
    return rows
