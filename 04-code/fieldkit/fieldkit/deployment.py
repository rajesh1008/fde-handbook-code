"""Deployment-readiness checklist, scored (Chapter 4). Promoted to fieldkit as fieldkit.deployment.

A demo proves a capability. A deployment has to prove five things, and this module keeps them apart:

    capability          the system does the task on the customer's documents, scored by the customer's expert
    workflow            the output lands where the work happens, exceptions have a route, volume is known
    controls            it runs under the customer's identity, network, gateway and retention rules
    ownership           named people at the customer accept named parts of it, with authority to do so
    reconstructability  any output can be rebuilt months later from retained records, for an auditor

Two scorers live here on purpose. `naive_score` is the weighted average most teams build first; it is kept
so the failure can be shown. `assess` is the one to use: must-pass items block, a proof only counts when it
names a person who measured it and what they measured it on, and an owner only counts when the owner is a
person who has accepted, with authority over the thing they own.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

DIMENSIONS = ("capability", "workflow", "controls", "ownership", "reconstructability")
STATUSES = ("held", "partial", "missing")
_CREDIT = {"held": 1.0, "partial": 0.5, "missing": 0.0}
# Names that are not a person: a team, a function, a placeholder, or the vendor itself.
_NOT_A_PERSON = re.compile(r"^(?:|tbd|tbc|n/?a|none|unknown|.*\b(?:team|group|office|department|ops|"
                           r"operations|committee|function|vendor|northlight|us)\b.*)$", re.I)


def is_person(name: str) -> bool:
    """A named individual: two or more capitalised words, and not a team, placeholder or the vendor."""
    name = (name or "").strip()
    return bool(re.match(r"^[A-Z][a-z]+(?: [A-Z][a-z'-]+)+$", name)) and not _NOT_A_PERSON.match(name)


@dataclass
class Proof:
    key: str
    dimension: str
    requirement: str
    status: str = "missing"
    must_pass: bool = False
    weight: float = 1.0
    measured_by: str = ""        # the person who produced the evidence
    on_what: str = ""            # what it was measured on, with a count
    evidence: str = ""           # where the record is (path in the engagement repository)
    owner: str = ""              # for ownership items: the person who accepts this
    accepted_day: int | None = None
    authority: str = ""          # what the owner can actually decide; empty means not established

    def __post_init__(self):
        if self.dimension not in DIMENSIONS:
            raise ValueError(f"dimension must be one of {DIMENSIONS}, got {self.dimension!r}")
        if self.status not in STATUSES:
            raise ValueError(f"status must be one of {STATUSES}, got {self.status!r}")

    def problems(self, customer_people=()) -> list[str]:
        """Why a claimed 'held' or 'partial' does not count. Empty list means the claim stands.

        customer_people: the customer's named people. A capability proof only counts when one of them
        measured it: the vendor scoring its own demo is not evidence about the customer's documents."""
        if self.status == "missing":
            return []
        out = []
        if not is_person(self.measured_by):
            out.append(f"no person measured it ({self.measured_by or 'blank'})")
        elif self.dimension == "capability" and customer_people and self.measured_by not in customer_people:
            out.append(f"measured by {self.measured_by}, not by the customer's expert")
        if not self.on_what:
            out.append("does not say what it was measured on")
        elif self.dimension == "capability" and "synthetic" in self.on_what.lower():
            out.append("measured on synthetic data: proves the plumbing, not the accuracy")
        if self.dimension == "ownership":
            if not is_person(self.owner):
                out.append(f"owner is not a named person ({self.owner or 'blank'})")
            elif self.accepted_day is None:
                out.append(f"{self.owner} has not accepted")
            elif not self.authority:
                out.append(f"{self.owner} is named without authority over it")
        return out

    def counted(self, customer_people=()) -> str:
        """The status after checking: a claim with problems counts as missing."""
        return "missing" if self.problems(customer_people) else self.status


@dataclass
class Verdict:
    system: str
    day: int
    naive: float
    gated: float
    by_dimension: dict
    blocking: list = field(default_factory=list)
    discounted: list = field(default_factory=list)
    claimed_dimensions: tuple = ()

    @property
    def label(self) -> str:
        if self.claimed_dimensions == ("capability",):
            return "DEMO ONLY"          # nothing but capability was ever claimed
        return "READY" if not self.blocking and self.gated >= 0.8 else "NOT READY"

    def summary(self) -> str:
        lines = [f"DEPLOYMENT READINESS  {self.system}  day {self.day}",
                 f"  naive weighted score   {self.naive:.2f}  " + ("READY" if self.naive >= 0.8 else "NOT READY"),
                 f"  gated score            {self.gated:.2f}  {self.label}"]
        lines += [f"  {d:<19}{self.by_dimension[d]:.2f}" for d in DIMENSIONS]
        missing = [b.split(" ")[0] for b in self.blocking if b.endswith(": missing")]
        lines += [f"  BLOCKING {b}" for b in self.blocking if not b.endswith(": missing")]
        if missing:
            lines.append(f"  BLOCKING {len(missing)} must-pass proofs missing: " + ", ".join(missing))
        blocked = {b.split(" ")[0] for b in self.blocking}
        lines += [f"  discounted {d}" for d in self.discounted if d.split(":")[0] not in blocked]
        return "\n".join(lines)


class Checklist:
    def __init__(self, system: str, customer_people=()):
        self.system = system
        self.customer_people = tuple(customer_people)
        self.proofs: dict[str, Proof] = {}

    def add(self, proof: Proof) -> Proof:
        self.proofs[proof.key] = proof
        return proof

    def update(self, key: str, **changes) -> Proof:
        p = self.proofs[key]
        for k, v in changes.items():
            setattr(p, k, v)
        p.__post_init__()
        return p

    def _score(self, statuses: dict[str, str], dims=DIMENSIONS) -> float:
        items = [p for p in self.proofs.values() if p.dimension in dims]
        total = sum(p.weight for p in items)
        return sum(p.weight * _CREDIT[statuses[p.key]] for p in items) / total if total else 0.0

    def naive_score(self) -> float:
        """The weighted average of claimed statuses. Shown to fail; do not gate on it."""
        return self._score({k: p.status for k, p in self.proofs.items()})

    def assess(self, day: int) -> Verdict:
        cp = self.customer_people
        counted = {k: p.counted(cp) for k, p in self.proofs.items()}
        by_dim = {d: round(self._score(counted, (d,)), 2) for d in DIMENSIONS}
        blocking, discounted = [], []
        for p in self.proofs.values():
            if p.problems(cp):
                discounted.append(f"{p.key}: claimed {p.status}, " + "; ".join(p.problems(cp)))
            if p.must_pass and counted[p.key] != "held":
                why = "; ".join(p.problems(cp)) or counted[p.key]
                blocking.append(f"{p.key} ({p.dimension}): {why}")
        for d in DIMENSIONS:
            if not any(p.dimension == d for p in self.proofs.values()):
                blocking.append(f"no proofs listed for {d}")
        claimed = tuple(d for d in DIMENSIONS if any(p.dimension == d and p.status != "missing"
                                                     for p in self.proofs.values()))
        return Verdict(self.system, day, round(self.naive_score(), 2), round(self._score(counted), 2),
                       by_dim, blocking, discounted, claimed)

    def table(self) -> str:
        rows = [f"{'key':<24}{'dimension':<19}{'claimed':<9}{'counted':<9}must"]
        for p in self.proofs.values():
            rows.append(f"{p.key:<24}{p.dimension:<19}{p.status:<9}{p.counted(self.customer_people):<9}"
                        f"{'yes' if p.must_pass else ''}")
        return "\n".join(rows)
