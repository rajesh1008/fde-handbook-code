"""fieldkit.environment: the customer's environment as records (Chapter 17, fieldkit v2.2, book layer).

One part per question an enterprise architect asks before customer data moves:
- TENANCY, tenancy_gaps, choose_tenancy: where the code runs, and which controls the customer holds there.
- Delegation, RightsGate: on-behalf-of identity, with the user's rights rechecked before any result is returned.
- EgressRule, EgressPolicy: default-deny egress to named destinations; every decision lands in the customer's log.
- find_secrets, KeyRecord, key_findings: no literal secrets in code or config; every key has a customer owner,
  a customer holder and a rotation.
- AuditLog: an append-only, hash-chained log the customer owns and can verify without the vendor's help.
- Answer, EnvironmentDoc: the three questions answered in writing, production and pre-production, with a lint that
  rejects any answer the customer cannot verify for itself.
"""
from __future__ import annotations

import fnmatch
import hashlib
import json
import re
from dataclasses import dataclass, field

# ------------------------------------------------------------------------------------------------ tenancy
CONTROLS = ("network", "identity", "keys", "logs", "change", "incident")
TENANCY = {
    "vendor-shared": dict(label="vendor's shared service", customer_holds=()),
    "vendor-dedicated": dict(label="vendor-hosted, single tenant", customer_holds=("keys",)),
    "customer-account": dict(label="customer's account, vendor deploys",
                             customer_holds=("network", "identity", "keys", "logs")),
    "customer-operated": dict(label="customer's account, customer deploys", customer_holds=CONTROLS),
}


def tenancy_gaps(option: str, required) -> list:
    """Controls the customer requires but would not hold under this tenancy option."""
    held = set(TENANCY[option]["customer_holds"])
    return [c for c in CONTROLS if c in set(required) and c not in held]


def choose_tenancy(required) -> str:
    """The option with the least customer burden that leaves no required control with the vendor."""
    for option in TENANCY:
        if not tenancy_gaps(option, required):
            return option
    raise ValueError(f"no tenancy option covers {sorted(required)}")


# ------------------------------------------------------------------------------------------------ audit log
@dataclass
class AuditLog:
    """Append-only log owned by the customer. Each record carries the hash of the one before it, so the owner can
    prove nothing was removed or edited, without asking the vendor."""
    owner: str
    records: list = field(default_factory=list)

    def append(self, **event) -> dict:
        prev = self.records[-1]["hash"] if self.records else "0" * 16
        body = json.dumps(event, sort_keys=True, default=str)
        rec = dict(seq=len(self.records) + 1, **event, prev=prev,
                   hash=hashlib.sha256((prev + body).encode()).hexdigest()[:16])
        self.records.append(rec)
        return rec

    def query(self, **match) -> list:
        return [r for r in self.records if all(r.get(k) == v for k, v in match.items())]

    def verify(self) -> list:
        """Sequence numbers where the chain breaks; an empty list means the log is intact."""
        bad, prev = [], "0" * 16
        for r in self.records:
            event = {k: v for k, v in r.items() if k not in ("seq", "prev", "hash")}
            h = hashlib.sha256((prev + json.dumps(event, sort_keys=True, default=str)).encode()).hexdigest()[:16]
            if r["prev"] != prev or r["hash"] != h:
                bad.append(r["seq"])
            prev = r["hash"]
        return bad


# ------------------------------------------------------------------------------------------------ egress
@dataclass(frozen=True)
class EgressRule:
    name: str
    host: str            # exact name or glob, for example "*.us-east-1.amazonaws.com"
    port: int = 443
    owner: str = ""      # the customer person who answers for this destination
    reason: str = ""


@dataclass
class EgressPolicy:
    """Default deny. A destination is reachable only if a named rule allows it, and every decision, allowed or
    denied, is written to the customer's log, because a denial is evidence too."""
    source: str
    rules: list
    log: AuditLog | None = None

    def check(self, host: str, port: int = 443, t: str = "") -> bool:
        rule = next((r for r in self.rules if fnmatch.fnmatch(host, r.host) and r.port == port), None)
        if self.log is not None:
            self.log.append(t=t, kind="egress", source=self.source, dest=f"{host}:{port}",
                            action="ALLOW" if rule else "DENY", rule=rule.name if rule else "default-deny")
        return rule is not None

    def lint(self) -> list:
        out = []
        for r in self.rules:
            if not r.owner:
                out.append(f"rule {r.name}: no customer owner")
            if not r.reason:
                out.append(f"rule {r.name}: no reason")
            if "*" in r.host or r.host == "0.0.0.0/0":
                out.append(f"rule {r.name}: wildcard destination {r.host} (name the endpoint)")
        return out


# ------------------------------------------------------------------------------------------------ identity
@dataclass(frozen=True)
class Delegation:
    """The agent acts for one user, for one purpose, for a short time. Minutes since midnight, for the lab."""
    user: str
    agent: str
    purpose: str
    scopes: tuple
    issued: int
    expires: int

    def valid_at(self, t: int) -> bool:
        return self.issued <= t < self.expires


class RightsGate:
    """Recheck the user's own rights, with the customer's authorization service, at the moment a result is about to
    be returned. Retrieval may run under a narrower service identity; release never does."""

    def __init__(self, can_read, log: AuditLog | None = None):
        self.can_read = can_read      # can_read(user, resource, t) -> bool, asked of the customer's system
        self.log = log

    def release(self, d: Delegation, results, t: int):
        released, withheld = [], []
        for res in results:
            if not d.valid_at(t):
                reason = "delegation expired"
            elif not self.can_read(d.user, res, t):
                reason = "user may not read"
            else:
                released.append(res)
                continue
            withheld.append((res, reason))
            if self.log is not None:
                self.log.append(t=t, kind="rights-recheck", user=d.user, agent=d.agent, purpose=d.purpose,
                                resource=res, action="WITHHELD", reason=reason)
        return released, withheld


# ------------------------------------------------------------------------------------------------ secrets
SECRET_PATTERNS = [
    ("cloud access key", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("literal key or token", re.compile(r"(?i)\"?(api[_-]?key|secret|token|password|key)\"?\s*[:=]\s*\"[A-Za-z0-9_\-]{20,}\"")),
    ("private key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("vendor-format key", re.compile(r"\b[a-z]{2,6}_(live|sbx|test|prod)_[A-Za-z0-9]{16,}\b")),
]


def find_secrets(text: str, path: str = "") -> list:
    """(path, line number, kind) for every literal secret; a reference such as valueFrom an ARN is not a secret."""
    hits = []
    for n, line in enumerate(text.splitlines(), 1):
        for kind, pat in SECRET_PATTERNS:
            if pat.search(line):
                hits.append((path, n, kind))
                break
    return hits


@dataclass(frozen=True)
class KeyRecord:
    name: str
    holder: str           # who can use the key material
    owner: str            # who can rotate, revoke and read its usage log
    store: str
    rotation_days: int | None
    used_by: str


def key_findings(keys, customer: str) -> list:
    out = []
    for k in keys:
        if k.owner != customer:
            out.append(f"{k.name}: owned by {k.owner}, not {customer}")
        if k.holder != customer:
            out.append(f"{k.name}: key material held by {k.holder}")
        if not k.rotation_days:
            out.append(f"{k.name}: no rotation")
    return out


# ------------------------------------------------------------------------------------------------ three questions
QUESTIONS = ("where", "identity", "logs")
PHASES = ("production", "pre-production")
REGION = re.compile(r"\b(us|eu|ca|ap)-[a-z]+-\d\b|\b(eastus|westus|centralus|canadacentral)\d?\b|\b(us|europe|northamerica)-[a-z]+\d\b")


@dataclass(frozen=True)
class Answer:
    question: str      # where | identity | logs
    phase: str         # production | pre-production
    text: str
    evidence: str      # an identifier the customer can look up in its own systems
    owner_org: str     # whose organization answers for it


@dataclass
class EnvironmentDoc:
    customer: str
    vendor: str
    answers: list

    def lint(self) -> list:
        out, have = [], {(a.question, a.phase) for a in self.answers}
        for q in QUESTIONS:
            for p in PHASES:
                if (q, p) not in have:
                    out.append(f"{q} / {p}: not answered")
        v = self.vendor.lower()
        for a in self.answers:
            tag = f"{a.question} / {a.phase}"
            if not a.evidence.strip():
                out.append(f"{tag}: no evidence the customer can check")
            elif v in a.evidence.lower():
                out.append(f"{tag}: evidence lives with the vendor")
            if a.owner_org != self.customer:
                out.append(f"{tag}: answered for by {a.owner_org}, not {self.customer}")
            if a.question == "where" and not REGION.search(a.text + " " + a.evidence):
                out.append(f"{tag}: no region named")
            if a.question == "logs" and not (re.search(r"readers?", a.text) and re.search(r"\d+ days", a.text)):
                out.append(f"{tag}: no named readers and retention")
        return out
