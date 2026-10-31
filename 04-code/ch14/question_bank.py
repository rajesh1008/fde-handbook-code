"""Chapter 14: the question bank for the two rooms at Greystone (Michael Hart's and Sam Oakley's).

Every question has four parts: the question, why we need the answer (what it changes in the build), the answer we
expect, and the edge cases that would break the expectation. A question without a "why" is a survey question;
the lint refuses it. Answers are recorded with the person who gave them, the day, and a claim status
(Chapter 8 statuses [CHECK ch08]).
"""
from __future__ import annotations
from dataclasses import dataclass

STATUSES = ("direct customer fact", "reconstructed from an artifact", "vendor position",
            "proposed design", "decision required")


@dataclass
class Question:
    key: str
    room: str            # "Michael" | "Sam" | "floor" (coordinators, at the desk)
    text: str
    why: str
    expected: str
    edge: str
    blocking: bool = False
    day_answered: int | None = None
    answered_by: str = ""
    answer: str = ""
    status: str = ""     # one of STATUSES once answered

    def __post_init__(self):
        if self.status and self.status not in STATUSES:
            raise ValueError(f"{self.key}: unknown status {self.status!r}")


def lint(bank) -> list[str]:
    out = []
    for q in bank:
        for part in ("why", "expected", "edge"):
            if not getattr(q, part).strip():
                out.append(f"NO-{part.upper()} {q.key}: {q.text}")
        if q.day_answered is not None and not q.answered_by:
            out.append(f"ANSWER-NO-PERSON {q.key}")
        if q.day_answered is not None and q.status not in STATUSES:
            out.append(f"ANSWER-NO-STATUS {q.key}")
    return out


def tally(bank, through_day: int) -> dict:
    answered = [q for q in bank if q.day_answered is not None and q.day_answered <= through_day]
    open_block = [q for q in bank if q.blocking and (q.day_answered is None or q.day_answered > through_day)]
    by_status = {s: sum(1 for q in answered if q.status == s) for s in STATUSES}
    return dict(asked=len(bank), answered=len(answered), blocking_open=len(open_block), by_status=by_status)


M, S, F = "Michael", "Sam", "floor"
H, O, C = "Michael Hart", "Sam Oakley", "referral coordinator"
DF, RA, VP, PD, DR = STATUSES

# (key, room, question, why, expected, edge, blocking, day, by, status)
_ROWS = [
 ("M01", M, "Which referral types make up the 31-day backlog?", "decides which path release 1 covers",
  "specialty referrals needing prior authorization", "a backlog driven by one specialty", True, 15, H, DF),
 ("M02", M, "Who decides a referral is urgent today?", "decides whether urgency is a rule or a judgment",
  "the receiving clinician", "coordinators upgrading by phone", True, 15, H, DF),
 ("M03", M, "May the system draft the letter a coordinator sends?", "sets the autonomy level for E17",
  "yes, as a draft", "letters that go out unread under deadline", True, 17, H, DF),
 ("M04", M, "May the system submit to a payer?", "sets the autonomy level for submission",
  "no", "payer portals that auto-submit on save", True, 17, H, DF),
 ("M05", M, "Who scores a draft as acceptable?", "an accuracy number needs a scorer",
  "two coordinators from different clinics, Hart breaks ties", "coordinators who disagree on local rules", True, 16, H, DF),
 ("M06", M, "What does a good referral summary contain?", "the scoring rubric", "reason, history, question asked",
  "specialties that want different sections", False, 16, H, DF),
 ("M07", M, "Which red-flag terms must reach a clinician?", "E15 rule set and its owner",
  "a written list per specialty", "no list exists; it is in people's heads", True, 17, H, RA),
 ("M08", M, "Do clinic routing rules exist in writing?", "E13 is rules only if someone owns them",
  "partly, in clinic binders", "rules that differ by clinic for the same specialty", False, 17, C, RA),
 ("M09", M, "Which payers cover most prior-authorization volume?", "the criteria checklist for E19",
  "four payers cover most", "a payer with criteria behind a portal login", False, 16, "revenue-cycle lead", RA),
 ("M10", M, "What does a coordinator do when an attachment is missing?", "E10 template and its wording",
  "phone or portal message", "requests that go to the patient instead", False, 15, C, DF),
 ("M11", M, "How many referrals arrive per week, and by what route?", "sizes the pipeline and volumes",
  "mostly electronic", "routes nobody in the room uses", True, 19, C, DF),
 ("M12", M, "What would make you stop the pilot?", "the stop rule in the scoping document",
  "a wrong patient or a missed red flag", "a rule nobody will enforce", True, 18, H, DF),
 ("M13", M, "Who owns the referral workflow operationally?", "the scope needs an owner with authority",
  "VP ambulatory operations", "an owner with no budget", True, 18, H, DF),
 ("M14", M, "Can patients be identified without a record number?", "decides if matching is deterministic",
  "always via the record number", "outside referrals with name and birth date only", False, 19, C, DF),
 ("M15", M, "Which diagnosis codes does a letter need?", "E20 and payer checklists", "the codes on the order",
  "payers needing more specific codes", False, 17, "revenue-cycle lead", RA),
 ("M16", M, "How long should a draft take to review?", "the value case is review time saved",
  "under three minutes", "drafts longer than the notes", False, None, "", ""),
 ("M17", M, "Which clinics run the pilot?", "evaluation design and shadow scope",
  "two clinics with different rules", "a clinic that is mid-merger", True, 18, H, PD),
 ("M18", M, "What counts as a pilot?", "the date we project means something",
  "draft-only shadow on live referrals", "a demo on synthetic packets called a pilot", True, 18, H, PD),
 ("S01", S, "Where may referral data be processed?", "decides the deployment pattern", "Greystone's Azure tenant",
  "a model endpoint outside the tenant", True, 16, O, DF),
 ("S02", S, "How do vendor engineers get access?", "decides the access request we file", "just-in-time, named",
  "no standing identities for any vendor", True, 16, O, DF),
 ("S03", S, "What identity does a service use?", "decides the service design", "managed identity in Entra ID",
  "secrets in configuration", True, 16, O, DF),
 ("S04", S, "Which questionnaire must we answer, and how long is it?", "the security review clock",
  "41 questions", "questions that need a sub-processor list", True, 16, O, DF),
 ("S05", S, "When does the privacy board meet?", "the date we project depends on it",
  "monthly, complete submissions ten days ahead", "a board that defers incomplete items", True, 16, O, DF),
 ("S06", S, "What does the board need to approve the sample?", "submission contents", "minimum necessary rationale",
  "a fields list we cannot produce yet", True, 16, O, DF),
 ("S07", S, "Who changes the network routes and firewall?", "the change after review",
  "the managed-service provider", "a change freeze", True, 16, O, DF),
 ("S08", S, "How long does a managed-service provider change take?", "the critical path to data",
  "about 18 days", "a quarter-end freeze", True, 16, "managed-service provider lead", VP),
 ("S09", S, "When is the next Architecture Review slot?", "the critical path to data", "about day 94",
  "slots filled by a merger project", True, 16, O, RA),
 ("S10", S, "Which model endpoints are approved?", "decides which classes we can build", "the gateway list",
  "no small-model hosting approved", False, 16, O, DF),
 ("S11", S, "Do audit records go to your log platform?", "E25 destination", "yes, the central platform",
  "retention rules that differ by data type", False, 16, O, DF),
 ("S12", S, "Can drafts be stored, and for how long?", "storage design", "in tenant, 30 days",
  "drafts treated as part of the medical record", False, None, "", ""),
 ("S13", S, "Who signs that controls are acceptable?", "who signs the controls section", "Sam Oakley",
  "a committee with no date", True, 18, O, DF),
 ("S14", S, "Does the EHR allow writes from a service?", "E21 design", "through the interface engine only",
  "no write access for release 1", True, 17, O, DF),
 ("S15", S, "Are fax servers in scope of your controls?", "a path we have not seen", "not asked",
  "clinic-level fax inboxes", False, 19, O, DF),
 ("S16", S, "What would make you stop the pilot?", "the stop rule in the scoping document",
  "any data outside the tenant", "a stop with no named authority", True, 18, O, DF),
]

BANK = [Question(k, r, t, w, e, g, b, d, by, e if d is not None else "", st)
        for (k, r, t, w, e, g, b, d, by, st) in _ROWS]

# Where the answer given was not the answer expected. Day 19 is the morning read-back.
SURPRISES = {
    "M07": "partly written; the rest lives with two senior coordinators",
    "M11": "electronic 412, fax 253 in four days at two clinics (38% fax)",
    "M14": "no: faxed referrals often carry only name and birth date",
    "S15": "no; clinic fax servers sit outside the reviewed boundary",
}
for _q in BANK:
    if _q.key in SURPRISES:
        _q.answer = SURPRISES[_q.key]

# The Friday-before draft (day 12): four questions written as a survey, without the other three parts.
DRAFT_DEFECTS = [
    Question("X01", M, "Tell us about your referral process.", "", "", ""),
    Question("X02", M, "What are your pain points?", "", "", ""),
    Question("X03", S, "What are your security requirements?", "", "", ""),
    Question("X04", S, "Is AI allowed?", "", "yes or no", ""),
]
