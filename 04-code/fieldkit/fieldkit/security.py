"""fieldkit.security (book layer v4, Chapter 32): the security questionnaire as data with evidence links.

An answer passes only when every piece of evidence it cites is in the register, in date on the day of the check,
in scope for this customer's deployment, owned by a named person, and the claim is shown rather than assumed.
A link is not evidence. The module also carries the review's other artifacts: data flows a reviewer can verify
against what was observed, a threat model (STRIDE plus an agent category, scored before and after controls),
findings that close only with retest evidence, and the gate stack (security, model risk, procurement, legal, data
protection) with dated conditions.
"""
from __future__ import annotations

import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field

CLAIMS = ("measured", "configured", "documented", "assumed")
SEVERITY = ("high", "medium", "low")
STRIDE = ("spoofing", "tampering", "repudiation", "information disclosure", "denial of service",
          "elevation of privilege")
AGENT = "agent misuse"          # the "A": instructions in content, unsafe tool calls, subverted reasoning
CATEGORIES = STRIDE + (AGENT,)
GATES = ("security", "model risk", "procurement", "legal", "data protection")
STATUS = ("not started", "in review", "returned", "conditional", "passed")

_NOT_A_PERSON = re.compile(r"^(?:|tbd|tbc|n/?a|none|unknown|.*\b(?:team|group|office|department|desk|ops|"
                           r"operations|committee|function|vendor|provider|northlight|us)\b.*)$", re.I)


def is_person(name: str) -> bool:
    """A named individual: two or more capitalized words, not a team, a placeholder or the vendor."""
    name = (name or "").strip()
    return bool(re.match(r"^[A-Z][a-z]+(?: [A-Z][a-z'-]+)+$", name)) and not _NOT_A_PERSON.match(name)


# ------------------------------------------------------------------------------------------- evidence and answers
@dataclass(frozen=True)
class Evidence:
    id: str
    kind: str
    title: str
    owner: str
    issued_day: int
    valid_days: int
    scope: str = "any"            # "any" or the deployment it describes, e.g. "greystone-azure"
    digest: str = ""

    @property
    def expires_day(self) -> int:
        return self.issued_day + self.valid_days

    def problems(self, day: int, scope: str) -> list[str]:
        p = []
        if day >= self.expires_day:
            p.append(f"expired day {self.expires_day}")
        if self.scope not in ("any", scope):
            p.append(f"describes {self.scope}")
        if not is_person(self.owner):
            p.append(f"owner '{self.owner}' is not a person")
        return p


@dataclass(frozen=True)
class Answer:
    qid: str
    theme: str
    question: str
    text: str
    evidence: tuple = ()
    claim: str = "documented"
    design_changing: bool = False

    def __post_init__(self):
        assert self.claim in CLAIMS, self.claim


@dataclass(frozen=True)
class Verdict:
    qid: str
    passed: bool
    reasons: tuple = ()


def link_check(answers) -> list[Verdict]:
    """The naive check: an answer 'has evidence' if it links to something. Kept to show what it misses."""
    return [Verdict(a.qid, bool(a.evidence), () if a.evidence else ("no evidence",)) for a in answers]


def evidence_check(answers, register: dict, day: int, scope: str) -> list[Verdict]:
    out = []
    for a in answers:
        r = [] if a.evidence else ["no evidence"]
        for e in a.evidence:
            ev = register.get(e)
            if ev is None:
                r.append(f"{e} not in register")
                continue
            r += [f"{e} {p}" for p in ev.problems(day, scope)]
        if a.claim == "assumed":
            r.append("claim assumed, not shown")
        out.append(Verdict(a.qid, not r, tuple(r)))
    return out


def reuse(answers) -> Counter:
    """How many answers each evidence item carries. One stale document can fail several answers at once."""
    return Counter(e for a in answers for e in a.evidence)


def expiring(register: dict, answers, day: int, horizon: int):
    """Evidence that expires within `horizon` days of `day`, with the answers it would take down."""
    backs = defaultdict(list)
    for a in answers:
        for e in a.evidence:
            backs[e].append(a.qid)
    rows = [(ev.expires_day, ev.id, ev.title, backs[ev.id]) for ev in register.values()
            if day <= ev.expires_day < day + horizon and backs[ev.id]]
    return sorted(rows)


# ------------------------------------------------------------------------------------------------------ data flows
@dataclass(frozen=True)
class Flow:
    id: str
    source: str
    dest: str
    data: str                     # "phi", "metadata", "secret", "none"
    boundary: str = ""            # the trust boundary crossed, if any
    control: str = ""
    verify: str = ""              # how the reviewer can check it without trusting the vendor

    def lint(self) -> list[str]:
        p = []
        if self.boundary and not self.control:
            p.append(f"{self.id} crosses {self.boundary} with no control")
        if not self.verify:
            p.append(f"{self.id} has no way to verify")
        return p


def reconcile_flows(declared, observed_pairs):
    """Compare declared flows with (source, dest) pairs seen in flow logs and diagnostic settings."""
    d = {(f.source, f.dest): f.id for f in declared}
    seen = set(observed_pairs)
    undeclared = sorted(p for p in seen if p not in d)
    unseen = sorted(d[p] for p in d if p not in seen)
    return dict(matched=sum(1 for p in seen if p in d), undeclared=undeclared, unseen=unseen)


# ---------------------------------------------------------------------------------------------------- threat model
def band(score: int) -> str:
    return "high" if score >= 12 else "medium" if score >= 6 else "low"


@dataclass(frozen=True)
class Threat:
    id: str
    component: str
    category: str
    text: str
    likelihood: int
    impact: int
    controls: tuple = ()
    residual: tuple = None        # (likelihood, impact) with controls in place; None = no control yet
    finding: str = ""

    def __post_init__(self):
        assert self.category in CATEGORIES, self.category

    @property
    def inherent(self) -> int:
        return self.likelihood * self.impact

    @property
    def residual_score(self) -> int:
        l, i = self.residual or (self.likelihood, self.impact)
        return l * i


@dataclass
class ThreatModel:
    system: str
    threats: list

    def grid(self):
        g = defaultdict(int)
        for t in self.threats:
            g[(t.component, t.category)] += 1
        return g

    def by_category(self) -> Counter:
        return Counter(t.category for t in self.threats)

    def stride_only(self) -> int:
        return sum(1 for t in self.threats if t.category != AGENT)

    def bands(self, residual=True) -> Counter:
        return Counter(band(t.residual_score if residual else t.inherent) for t in self.threats)

    def uncontrolled(self):
        return [t for t in self.threats if not t.controls or band(t.residual_score) == "high"]


# ------------------------------------------------------------------------------------- findings and remediation
@dataclass
class Finding:
    id: str
    source: str                   # question id or threat id
    kind: str                     # "evidence" or "design"
    severity: str
    summary: str
    owner: str
    remediation: str
    raised_day: int
    due_day: int
    compensating: str = ""
    retest: str = ""
    closed_day: int | None = None

    def close(self, day: int, retest: str):
        if not retest:
            raise ValueError(f"{self.id}: a finding closes with retest evidence, not with a fix")
        self.retest, self.closed_day = retest, day

    def lint(self) -> list[str]:
        p = []
        if not is_person(self.owner):
            p.append(f"{self.id} owner '{self.owner}' is not a person")
        if not self.remediation:
            p.append(f"{self.id} has no remediation")
        if self.severity == "high" and self.due_day - self.raised_day > 30 and not self.compensating:
            p.append(f"{self.id} high, due in {self.due_day - self.raised_day} days, no compensating control")
        return p


@dataclass
class RemediationPlan:
    findings: list

    def open_on(self, day: int):
        return [f for f in self.findings if f.raised_day <= day and (f.closed_day is None or f.closed_day > day)]

    def burndown(self, days):
        return [(d, len(self.open_on(d))) for d in days]

    def overdue(self, day: int):
        return [f for f in self.open_on(day) if f.due_day < day]

    def lint(self) -> list[str]:
        return [p for f in self.findings for p in f.lint()]


def review(verdicts, findings):
    """The review result: an answer passes when its evidence check passed and no finding is raised against it."""
    against = {f.source for f in findings}
    passed = [v.qid for v in verdicts if v.passed and v.qid not in against]
    return dict(asked=len(verdicts), passed=len(passed), findings=len(findings),
                outcome="passed" if not findings else "returned with findings")


# ------------------------------------------------------------------------------------------------------ gate stack
@dataclass
class Gate:
    name: str
    status: str
    owner: str = ""
    day: int | None = None
    conditions: list = field(default_factory=list)   # (text, owner, due_day)

    def __post_init__(self):
        assert self.name in GATES and self.status in STATUS, (self.name, self.status)

    def lint(self) -> list[str]:
        p = []
        for text, owner, due in self.conditions:
            if not is_person(owner) or due is None:
                p.append(f"{self.name}: condition '{text}' needs a person and a day")
        if self.status in ("passed", "conditional", "returned") and self.day is None:
            p.append(f"{self.name}: {self.status} with no day")
        return p


@dataclass
class GateStack:
    customer: str
    gates: list

    def blocking(self):
        return [g.name for g in self.gates if g.status not in ("passed", "conditional")]

    def ready(self) -> bool:
        return not self.blocking() and not self.lint()

    def lint(self) -> list[str]:
        return [p for g in self.gates for p in g.lint()]
