"""fieldkit v4.1 (Chapter 33): model risk and the customer's governance.

The classification test as data: a system is split into components, each component carries the facts a model-risk
policy asks about (is it quantitative, was it trained or fitted on the customer's data, which design choices were
made for this customer, does its output feed a core business decision), and a framework is an ordered list of rules
that turns those facts into an outcome. Frameworks are data, so the same components can be classified under the
customer's policy, under a second customer's policy or under the vendor's first guess, and a design change is
re-classified by re-running the test, never by memory.

Also here: the validation plan each outcome requires, the model-risk pack generated from evaluation-suite evidence
(with a lint for missing items), the monitoring computability check (every metric input must be owned, stored and
runnable by the customer without the vendor), repeat-run stability for a model you do not own, the validator's
question map (evidence, translation, boundary) and review conditions with an owner and a due day.
"""
from dataclasses import dataclass, field
import hashlib
import json
import math

FULL = "full scope"
REGISTERED = "registered, not validated"
TOOL = "registered as a tool"
NOT_MODEL = "not a model"
OUTSIDE = "outside model-risk scope"
OUTCOMES = (FULL, REGISTERED, TOOL, NOT_MODEL, OUTSIDE)

FACTS = ("quantitative", "trained_on_customer_data", "core_decision", "vendor_model")


@dataclass(frozen=True)
class Component:
    cid: str
    name: str
    kind: str                       # code, rules, prompted, fine-tuned, fitted, retrieval, judge
    quantitative: bool              # produces an estimate or a classification by a learned or statistical method
    trained_on_customer_data: bool  # weights or a fitted map changed by the customer's data
    core_decision: bool             # output feeds a decision in a core business process
    vendor_model: bool = False      # the underlying model belongs to someone else
    design_choices: tuple = ()      # choices made for this customer: prompt, retrieval set, thresholds, examples
    owner: str = ""                 # model owner at the customer
    since_day: int = 0

    def facts(self):
        return {k: getattr(self, k) for k in FACTS}


@dataclass(frozen=True)
class Rule:
    when: dict          # fact -> required value; empty matches everything
    outcome: str
    reason: str

    def matches(self, c):
        return all(getattr(c, k) == v for k, v in self.when.items())


@dataclass(frozen=True)
class Framework:
    name: str
    rules: tuple
    note: str = ""

    def classify(self, c):
        for r in self.rules:
            if r.matches(c):
                return r.outcome, r.reason
        raise ValueError(f"{self.name}: no rule matches {c.cid}")


@dataclass(frozen=True)
class Classification:
    cid: str
    outcome: str
    reason: str
    design_choices: tuple


def classify_all(framework, components):
    out = []
    for c in components:
        o, why = framework.classify(c)
        out.append(Classification(c.cid, o, why, c.design_choices))
    return out


def counts(classes):
    n = {o: 0 for o in OUTCOMES}
    for k in classes:
        n[k.outcome] += 1
    return {o: v for o, v in n.items() if v}


def diff(before, after):
    """Components whose outcome changed (or appeared) between two runs of the test."""
    b = {k.cid: k.outcome for k in before}
    return [(k.cid, b.get(k.cid, "absent"), k.outcome) for k in after if b.get(k.cid) != k.outcome]


def register_digest(classes):
    s = json.dumps([(k.cid, k.outcome) for k in classes], sort_keys=True)
    return hashlib.sha256(s.encode()).hexdigest()[:12]


# What each outcome must show before use (the validation plan). Items are evidence keys.
PLAN = {
    FULL: ("purpose", "conceptual_soundness", "development_data", "outcomes", "benchmark", "sensitivity",
           "stability", "limits", "monitoring", "change_control"),
    REGISTERED: ("purpose", "vendor_due_diligence", "design_review", "outcomes", "sensitivity", "stability",
                 "limits", "monitoring", "change_control"),
    TOOL: ("purpose", "validity_check", "change_control"),
    NOT_MODEL: ("change_control",),
    OUTSIDE: (),
}


@dataclass(frozen=True)
class Evidence:
    key: str            # evidence key from PLAN
    cid: str            # component, or "*" for system-wide evidence
    claim: str          # the number or statement
    measured_by: str    # who scored or produced it
    on: str             # on what
    source: str         # artifact path or record


def plan_for(classes):
    return [(k.cid, item) for k in classes for item in PLAN[k.outcome]]


@dataclass
class Pack:
    customer: str
    version: str
    classes: list
    evidence: list
    metrics: list = field(default_factory=list)

    def find(self, cid, key):
        return [e for e in self.evidence if e.key == key and e.cid in (cid, "*")]

    def gaps(self):
        return [(cid, item) for cid, item in plan_for(self.classes) if not self.find(cid, item)]

    def lint(self):
        """Structural problems: missing plan items, evidence without a scorer, monitoring without a metric."""
        p = [f"missing {item} for {cid}" for cid, item in self.gaps()]
        p += [f"evidence {e.key}/{e.cid} names no scorer" for e in self.evidence if not e.measured_by.strip()]
        need = {k.cid for k in self.classes if "monitoring" in PLAN[k.outcome]}
        have = {c for m in self.metrics for c in m.covers}
        p += [f"no monitoring metric covers {c}" for c in sorted(need - have)]
        return p

    def items(self):
        return len(plan_for(self.classes))


@dataclass(frozen=True)
class Input:
    name: str
    owner_org: str      # organization that owns the input or code
    location: str       # where it lives
    runs_as: str = ""   # identity that runs the job, if this input is a job


@dataclass(frozen=True)
class Metric:
    mid: str
    name: str
    threshold: str
    owner: str          # named person at the customer who reads it
    covers: tuple       # component ids
    inputs: tuple       # Input records: data, labels, code, identity

    def blockers(self, customer, vendor_identities=()):
        out = []
        for i in self.inputs:
            if i.owner_org != customer:
                out.append(f"{i.name} owned by {i.owner_org} ({i.location})")
            if i.runs_as and i.runs_as in vendor_identities:
                out.append(f"{i.name} runs as {i.runs_as}, an identity the vendor operates")
        return out


def computability(metrics, customer, vendor_identities=()):
    """For each metric: can the customer compute it alone, after the vendor has gone?"""
    return [(m, m.blockers(customer, vendor_identities)) for m in metrics]


def repeat_agreement(runs):
    """runs: list of answers to the same input under fixed conditions. Share equal to the modal answer, and the mode."""
    tally = {}
    for a in runs:
        tally[a] = tally.get(a, 0) + 1
    mode = max(tally, key=lambda a: (tally[a], str(a)))
    return tally[mode] / len(runs), mode


def wilson_lower(k, n, z=1.96):
    if n == 0:
        return 0.0
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    r = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (c - r) / d


EVIDENCE_ANSWER, TRANSLATION, BOUNDARY = "evidence", "translation", "boundary"


@dataclass(frozen=True)
class ValidatorQuestion:
    qid: str
    asked: str
    answer_type: str     # evidence, translation or boundary
    answer: str
    compensating: str = ""   # required when answer_type is boundary

    def problems(self):
        if self.answer_type not in (EVIDENCE_ANSWER, TRANSLATION, BOUNDARY):
            return [f"{self.qid}: unknown answer type"]
        if self.answer_type == BOUNDARY and not self.compensating:
            return [f"{self.qid}: a boundary needs a compensating control"]
        return []


@dataclass(frozen=True)
class Condition:
    cid: str
    text: str
    owner: str
    due_day: int
    closes_when: str

    def status(self, day, met=False):
        if met:
            return "met"
        return "open" if day <= self.due_day else "overdue"
