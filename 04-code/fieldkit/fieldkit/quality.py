"""Upfront quality scoring and the per-source register (fieldkit v2.6, Chapter 21).

A document is scored at the door, before extraction spends money on it, on three
dimensions: completeness, legibility and consistency. Each dimension score is the
share of its checks that passed. The verdict is driven by hard gates, never by an
average, because an average lets a perfect legibility score hide a missing currency.

Decisions:
  accept   every hard check passed; the document flows downstream
  request  something is missing or contradicts itself; ask the sender, do not guess
  reject   the page cannot be read reliably; ask for a resend

The SourceRegister records, per source, what each field means, who owns it, what
the deployment is entitled to do with it, how fresh it must be, and what it is
valid for. A source used outside its "valid for" list is a finding, not a warning.
"""
from dataclasses import dataclass, field
from typing import Callable, Optional

DIMENSIONS = ("completeness", "legibility", "consistency")


@dataclass(frozen=True)
class Check:
    name: str
    dimension: str
    fn: Callable[[dict], Optional[str]]   # None if passed, else a short reason
    hard: bool = True


@dataclass
class Verdict:
    doc_id: str
    decision: str
    scores: dict
    failures: list
    scorer_version: str

    @property
    def score(self) -> float:
        """The weakest dimension, not the mean."""
        return min(self.scores.values())

    @property
    def mean(self) -> float:
        return sum(self.scores.values()) / len(self.scores)

    def line(self) -> str:
        why = "; ".join(f"{n}: {d}" for n, _, d in self.failures) or "-"
        return f"{self.doc_id:<8} {self.decision:<7} score {self.score:.2f}  {why}"


class QualityScorer:
    def __init__(self, checks, version: str):
        for c in checks:
            if c.dimension not in DIMENSIONS:
                raise ValueError(f"unknown dimension {c.dimension}")
        self.checks = list(checks)
        self.version = version

    def score(self, doc: dict) -> Verdict:
        tally = {d: [0, 0] for d in DIMENSIONS}
        fails = []
        for c in self.checks:
            reason = c.fn(doc)
            if reason == "n/a":
                continue
            tally[c.dimension][1] += 1
            if reason is None:
                tally[c.dimension][0] += 1
            else:
                fails.append((c.name, c.dimension, reason, c.hard))
        scores = {d: (p / t if t else 1.0) for d, (p, t) in tally.items()}
        hard = [f for f in fails if f[3]]
        if any(f[1] == "legibility" for f in hard):
            decision = "reject"
        elif hard:
            decision = "request"
        else:
            decision = "accept"
        return Verdict(doc["doc_id"], decision, scores, [f[:3] for f in fails], self.version)

    def run(self, docs):
        return [self.score(d) for d in docs]


def summarize(verdicts) -> dict:
    n = len(verdicts)
    out = {"documents": n}
    for d in ("accept", "request", "reject"):
        out[d] = sum(v.decision == d for v in verdicts)
    out["held"] = out["request"] + out["reject"]
    out["held_share"] = out["held"] / n if n else 0.0
    return out


def request_for(verdict: Verdict, sender: str, meanings: dict) -> str:
    """The message that goes back to the sender instead of a guess."""
    lines = [f"To: {sender}", f"Re: document {verdict.doc_id} (held at intake, scorer {verdict.scorer_version})"]
    if verdict.decision == "reject":
        lines.append("The scan could not be read reliably. Please resend a clear copy or the original PDF.")
    for name, dim, reason in verdict.failures:
        if dim == "legibility":
            continue
        key = name.replace("has ", "")
        lines.append(f"- {reason}: {meanings.get(key, key)}")
    lines.append("We have not processed this document and will not estimate the missing values.")
    return "\n".join(lines)


@dataclass
class SourceSpec:
    name: str
    owner: Optional[str]
    meanings: dict                 # field -> what it means at this source
    entitlement: str               # what the deployment may do with it
    freshness_hours: Optional[int]  # None means "no promise"
    valid_for: tuple = ()
    versioned: bool = True          # can yesterday's content be recovered?


class SourceRegister:
    def __init__(self, specs=()):
        self.specs = {s.name: s for s in specs}

    def add(self, spec: SourceSpec):
        self.specs[spec.name] = spec

    def findings(self, name: str):
        s = self.specs.get(name)
        if s is None:
            return [f"{name}: not in the register"]
        out = []
        if not s.owner:
            out.append(f"{name}: no named owner")
        if s.freshness_hours is None:
            out.append(f"{name}: no freshness promise")
        if not s.versioned:
            out.append(f"{name}: overwritten in place, no history")
        if not s.valid_for:
            out.append(f"{name}: valid-for list is empty")
        return out

    def check_use(self, name: str, fields, age_hours: float, purpose: str):
        s = self.specs.get(name)
        if s is None:
            return [f"{name}: not in the register"]
        out = []
        unknown = [f for f in fields if f not in s.meanings]
        if unknown:
            out.append(f"{name}: fields with no registered meaning: {', '.join(unknown)}")
        if s.freshness_hours is not None and age_hours > s.freshness_hours:
            out.append(f"{name}: {age_hours:.0f} h old, promise is {s.freshness_hours} h")
        if purpose not in s.valid_for:
            out.append(f"{name}: not valid for '{purpose}' (valid for: {', '.join(s.valid_for) or 'nothing yet'})")
        return out

    def same_meaning(self, a: str, b: str, field_name: str) -> bool:
        return self.specs[a].meanings.get(field_name) == self.specs[b].meanings.get(field_name)
