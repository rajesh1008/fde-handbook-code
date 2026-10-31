"""fieldkit v1.1 question bank (Chapter 7). Standard library only.

A discovery question has four parts: the question, why the data is needed (the decision it feeds), the expected
answer (with the claim status of whoever gave it), and the edge cases to listen for. A fifth field, `changes`,
names the design element that moves if the answer differs. The bank lints questions, builds a prep sheet for one
audience inside a time budget, records answers with who gave them, and reconciles answers against expectations.
"""
from __future__ import annotations
from dataclasses import dataclass, field

LAYER = "v1.1"
STATUSES = ("direct customer fact", "reconstructed from supplied artifact", "vendor position",
            "proposed design", "decision required")
CATEGORIES = ("functional", "technical", "data", "identity", "audit")
ROLES = ("data owner", "security lead", "model-risk officer", "operator", "sponsor", "architect", "platform")
OUTCOMES = ("confirmed", "refined", "redirected", "contradicted", "unanswered")
# how likely an expected answer is to be wrong, by where it came from (prep ordering; see section 7.1)
STATUS_WEIGHT = {"vendor position": 3.0, "proposed design": 2.5, "decision required": 2.5,
                 "reconstructed from supplied artifact": 1.5, "direct customer fact": 1.0}


@dataclass
class Question:
    qid: str
    category: str
    audience: str            # the role that owns the answer
    text: str
    why: str                 # the decision the answer feeds
    expected: str
    status: str              # claim status of the expected answer
    expected_from: str       # who gave the expected answer (a role, or "Northlight")
    edge_cases: tuple = ()
    changes: str = ""        # design element that moves if the answer differs
    impact: int = 1          # 1 = one component, 2 = a data path, 3 = the architecture or a gate
    rapid: bool = False      # answerable in under sixty seconds (yes, no, a number or a name)
    minutes: float = 1.5
    sources: tuple = ()      # discovery items (paths, exceptions, gaps, notes) this question serves

    def problems(self):
        p = []
        if not self.text.strip().endswith("?"):
            p.append("not phrased as a question")
        if len(self.why.split()) < 4:
            p.append("why is missing or too short to name a decision")
        if not self.expected.strip():
            p.append("no expected answer (write one, even 'unknown, decision required')")
        if self.status not in STATUSES:
            p.append(f"unknown status {self.status!r}")
        if not self.edge_cases:
            p.append("no edge cases to listen for")
        if not self.changes.strip():
            p.append("does not say what changes if the answer differs")
        if self.category not in CATEGORIES:
            p.append(f"unknown category {self.category!r}")
        if self.audience not in ROLES:
            p.append(f"unknown audience {self.audience!r}")
        if self.rapid and self.minutes > 1.0:
            p.append("rapid question budgeted over a minute")
        return p

    def warnings(self):
        w = []
        if self.status == "vendor position":
            w.append("expected answer is a vendor position: ask it, do not build on it")
        if self.status == "direct customer fact" and self.expected_from != self.audience:
            w.append(f"expected answer came from {self.expected_from}, who does not own it")
        return w

    def weight(self):
        w = STATUS_WEIGHT[self.status]
        if self.status == "direct customer fact" and self.expected_from != self.audience:
            w += 1.0
        return w * self.impact


@dataclass
class Answer:
    qid: str
    day: int
    who: str
    role: str
    outcome: str
    text: str
    elapsed_min: float = 1.0
    edge_cases_seen: tuple = ()
    redirect_to: str = ""

    def problems(self):
        p = []
        if self.outcome not in OUTCOMES:
            p.append(f"unknown outcome {self.outcome!r}")
        if self.outcome == "redirected" and not self.redirect_to:
            p.append("redirected answer names no owner")
        return p


class Bank:
    def __init__(self, name):
        self.name = name
        self.questions: dict[str, Question] = {}
        self.answers: dict[str, Answer] = {}

    def add(self, q: Question, strict=True):
        if q.qid in self.questions:
            raise ValueError(f"duplicate qid {q.qid}")
        if strict and q.problems():
            raise ValueError(f"{q.qid}: " + "; ".join(q.problems()))
        self.questions[q.qid] = q
        return q

    def lint(self):
        out = []
        for q in self.questions.values():
            out += [(q.qid, "error", m) for m in q.problems()]
            out += [(q.qid, "warning", m) for m in q.warnings()]
        return out

    def for_audience(self, audience):
        return [q for q in self.questions.values() if q.audience == audience]

    def prep(self, audience, minutes, rapid_first=True):
        """Order one audience's questions for a session of `minutes`: the rapid round first, then by weight.
        Returns (asked, dropped)."""
        qs = self.for_audience(audience)
        rapid = [q for q in qs if q.rapid] if rapid_first else []
        rest = sorted([q for q in qs if q not in rapid], key=lambda q: (-q.weight(), q.qid))
        asked, dropped, used = [], [], 0.0
        for q in rapid + rest:
            if used + q.minutes <= minutes + 1e-9:
                asked.append(q); used += q.minutes
            else:
                dropped.append(q)
        return asked, dropped

    def record(self, a: Answer):
        if a.qid not in self.questions:
            raise KeyError(a.qid)
        if a.problems():
            raise ValueError(f"{a.qid}: " + "; ".join(a.problems()))
        self.answers[a.qid] = a
        return a

    def reconcile(self):
        r = Reconciliation()
        for qid, q in self.questions.items():
            a = self.answers.get(qid)
            if a is None:
                continue
            authoritative = a.role == q.audience
            if not authoritative:
                r.wrong_person.append((q, a))
                continue
            r.by_outcome[a.outcome] = r.by_outcome.get(a.outcome, 0) + 1
            s = r.by_status.setdefault(q.status, [0, 0])
            s[0] += 1
            if a.outcome == "contradicted":
                s[1] += 1
                r.design_changes.append((q, a))
            if a.outcome == "redirected":
                r.follow_ups.append((q, a))
            r.edge_cases_listed += len(q.edge_cases)
            r.edge_cases_seen += len(a.edge_cases_seen)
            r.elapsed += a.elapsed_min
        return r


@dataclass
class Reconciliation:
    by_outcome: dict = field(default_factory=dict)
    by_status: dict = field(default_factory=dict)     # status -> [asked, contradicted]
    design_changes: list = field(default_factory=list)
    follow_ups: list = field(default_factory=list)
    wrong_person: list = field(default_factory=list)
    edge_cases_listed: int = 0
    edge_cases_seen: int = 0
    elapsed: float = 0.0

    @property
    def answered(self):
        return sum(v for k, v in self.by_outcome.items() if k != "unanswered")


def acting_for_gaps(needs, grants):
    """Actions an agent needs that the person it acts for may not perform. Each gap is a design constraint:
    the agent may not exceed the person, so the gap needs a decision by whoever owns the entitlement."""
    return [n for n in needs if n not in grants]


def coverage(questions, items):
    """Discovery items (ids) with no question serving them."""
    served = {s for q in questions for s in q.sources}
    return [i for i in items if i not in served]
