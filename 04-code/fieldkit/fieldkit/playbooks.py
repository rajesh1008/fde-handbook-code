"""fieldkit v5.4 (Chapter 47): engagement linter and playbook registry.

Book layer; the package version stays 0.1.0. Four parts, all plain data and plain functions:

* recurrence: what repeats across engagements, counted by shape (variants), not by name.
* Playbook, Step, Registry: versioned playbooks whose steps declare the estate facts they need; the registry
  matches a playbook to a customer estate before anyone starts work, tracks adoptions and deprecations.
* lint_playbook, lint_engagement: rule-based linters. P1 to P5 for playbooks (P5 is the assumption probe: a step
  that names an estate capability it has not declared). E1 to E8 for engagement manifests.
* FieldReport, rank_reports, loop_metrics, continuity: the product loop and the customer's view of a changing team.
"""
from __future__ import annotations

import re
import statistics
from dataclasses import dataclass, field

# Words in a step that mean "this step needs something from the customer's estate". Value: the estate fact.
CAPABILITY_WORDS = {
    "gateway": "gateway", "vault": "vault", "secret store": "vault", "single sign-on": "sso", "sso": "sso",
    "fhir": "fhir", "x12": "edi", "edi": "edi", "message queue": "queue", "object store": "object_store",
    "private endpoint": "private_network",
}
SEMVER = re.compile(r"^\d+\.\d+(\.\d+)?$")


# ---------------------------------------------------------------- what repeats ----------------------------------
def classify(n: int, variants: int, *, platform_min: int = 8, platform_ratio: float = 0.25,
             playbook_min: int = 3, playbook_ratio: float = 0.5) -> str:
    """platform | playbook | bespoke, from how many engagements built it and how many distinct shapes it took."""
    if n == 0:
        return "bespoke"
    ratio = variants / n
    if n >= platform_min and ratio <= platform_ratio:
        return "platform"
    if n >= playbook_min and ratio <= playbook_ratio:
        return "playbook"
    return "bespoke"


def classify_by_name(n: int, *, platform_min: int = 8, playbook_min: int = 3) -> str:
    """The naive count: how often the component's name appears. Kept so the lab can show what it gets wrong."""
    return "platform" if n >= platform_min else "playbook" if n >= playbook_min else "bespoke"


def recurrence(instances):
    """instances: iterable of (engagement, component, shape, hours). Returns rows sorted by engagements, desc."""
    by = {}
    for eng, comp, shape, hours in instances:
        r = by.setdefault(comp, dict(component=comp, engagements=set(), shapes=set(), hours=0))
        r["engagements"].add(eng)
        r["shapes"].add(shape)
        r["hours"] += hours
    rows = []
    for r in by.values():
        n, v = len(r["engagements"]), len(r["shapes"])
        rows.append(dict(component=r["component"], n=n, variants=v, hours=r["hours"],
                         by_name=classify_by_name(n), by_shape=classify(n, v)))
    return sorted(rows, key=lambda r: (-r["n"], r["variants"], r["component"]))


# ---------------------------------------------------------------- playbooks -------------------------------------
@dataclass
class Step:
    sid: str
    text: str
    owner: str = ""
    test: str = ""
    requires: dict = field(default_factory=dict)   # estate fact -> set of allowed values


@dataclass
class Playbook:
    pid: str
    version: str
    title: str
    origin: str
    owner: str
    workflow: str
    steps: list
    proven_at: list = field(default_factory=list)  # engagements where it reached live
    maturity: str = "draft"                        # draft | shadow | live | absorbed

    @property
    def key(self):
        return f"{self.pid}@{self.version}"

    def requires(self):
        out = {}
        for s in self.steps:
            for fact, allowed in s.requires.items():
                out.setdefault(fact, set(allowed))
                out[fact] &= set(allowed)
        return out


def implied_capabilities(text: str):
    t = text.lower()
    return sorted({fact for word, fact in CAPABILITY_WORDS.items() if re.search(r"\b" + re.escape(word) + r"\b", t)})


def lint_playbook(pb: Playbook, *, probe: bool = True):
    """Findings as (rule, where, message). probe=False is the form-only linter of v5.4 before the assumption probe."""
    f = []
    if not SEMVER.match(pb.version):
        f.append(("P3", pb.key, f"version {pb.version!r} is not major.minor[.patch]"))
    if pb.maturity in ("live", "absorbed") and not pb.proven_at:
        f.append(("P4", pb.key, "maturity live with no engagement where it reached live"))
    if not pb.owner:
        f.append(("P1", pb.key, "playbook has no owner"))
    for s in pb.steps:
        if not s.owner:
            f.append(("P1", s.sid, "step has no owner role"))
        if not s.test:
            f.append(("P2", s.sid, "step has no test"))
        if probe:
            for fact in implied_capabilities(s.text):
                if fact not in s.requires:
                    f.append(("P5", s.sid, f"step text needs '{fact}' but does not declare it"))
    return f


def check_preconditions(pb: Playbook, estate: dict):
    """Unmet (step, fact, allowed, have) against an estate profile: a dict of fact -> value."""
    out = []
    for s in pb.steps:
        for fact, allowed in s.requires.items():
            have = estate.get(fact, "unknown")
            if have not in allowed:
                out.append((s.sid, fact, sorted(allowed), have))
    return out


class Registry:
    """Versioned playbooks, adoptions and deprecations. match() runs before work starts, not on deploy day."""

    def __init__(self):
        self.books, self.adoptions, self.deprecated = {}, {}, {}

    def add(self, pb: Playbook, *, probe: bool = True):
        findings = lint_playbook(pb, probe=probe)
        if findings:
            raise ValueError(f"{pb.key} fails lint: {findings[0]}")
        self.books[pb.key] = pb
        return pb

    def versions(self, pid):
        return sorted((b for b in self.books.values() if b.pid == pid),
                      key=lambda b: tuple(int(x) for x in b.version.split(".")))

    def latest(self, pid):
        live = [b for b in self.versions(pid) if b.key not in self.deprecated]
        return live[-1] if live else None

    def match(self, estate: dict, workflow: str):
        rows = []
        for pid in sorted({b.pid for b in self.books.values()}):
            pb = self.latest(pid)
            if pb is None or pb.workflow not in (workflow, "any"):
                continue
            unmet = check_preconditions(pb, estate)
            rows.append((pb.key, "ready" if not unmet else "blocked", unmet))
        return rows

    def adopt(self, engagement, key):
        if key not in self.books:
            raise KeyError(key)
        self.adoptions[engagement] = key

    def deprecate(self, key, *, reason, migrate_by):
        self.deprecated[key] = dict(reason=reason, migrate_by=migrate_by)

    def on(self, key):
        return sorted(e for e, k in self.adoptions.items() if k == key)


# ---------------------------------------------------------------- engagement linter -----------------------------
RULES = {
    "E1": "playbook declared and in the registry, or bespoke with a registered reason",
    "E2": "playbook version not deprecated past its migrate-by month",
    "E3": "model calls through the platform gateway adapter, or a registered deviation",
    "E4": "evaluation suite present with a named customer gold-set owner",
    "E5": "after hand-over, every alert route owned by a customer address",
    "E6": "every deviation has a reason, an owner and an unexpired review month",
    "E7": "fieldkit pinned to the book layer the playbook needs",
    "E8": "secrets held in the customer's vault",
}


def lint_engagement(m: dict, registry: Registry, *, month: int):
    """m: engagement manifest (dict). Findings as (rule, engagement, message)."""
    e, f = m["id"], []
    dev = {d["what"]: d for d in m.get("deviations", [])}
    pb = m.get("playbook")
    if pb is None:
        if "playbook" not in dev:
            f.append(("E1", e, "no playbook and no registered reason for bespoke"))
    elif pb not in registry.books:
        f.append(("E1", e, f"playbook {pb} is not in the registry"))
    elif pb in registry.deprecated and month > registry.deprecated[pb]["migrate_by"]:
        f.append(("E2", e, f"{pb} deprecated; migrate-by month {registry.deprecated[pb]['migrate_by']} passed"))
    if m.get("adapter") != "fieldkit.gateway" and "adapter" not in dev:
        f.append(("E3", e, f"model calls through {m.get('adapter')!r}, no registered deviation"))
    if not m.get("eval_suite"):
        f.append(("E4", e, "no evaluation suite"))
    elif not m.get("gold_owner"):
        f.append(("E4", e, "evaluation suite has no named customer gold-set owner"))
    if m.get("phase") in ("handed over", "retained duties") and any(
            not r.endswith(m["customer_domain"]) for r in m.get("alert_routes", [])):
        f.append(("E5", e, "an alert route goes to a non-customer address after hand-over"))
    for d in m.get("deviations", []):
        if not (d.get("reason") and d.get("owner")) or d.get("review_by", 0) < month:
            f.append(("E6", e, f"deviation '{d['what']}' lacks reason/owner or its review month passed"))
    need = m.get("needs_layer", 0)
    if m.get("fieldkit_layer", 0) < need:
        f.append(("E7", e, f"fieldkit layer {m.get('fieldkit_layer')} below the {need} the playbook needs"))
    if m.get("secrets_owner") != "customer":
        f.append(("E8", e, f"secrets held by {m.get('secrets_owner')!r}"))
    return f


# ---------------------------------------------------------------- the product loop ------------------------------
@dataclass
class FieldReport:
    rid: str
    title: str
    origin: str
    engagements: list            # engagements where the same need was met with bespoke work
    hours: list                  # bespoke hours per engagement (same order)
    votes: int = 0               # requests logged by sales and account teams
    acv_usd: int = 0             # annual contract value of the loudest requester
    artifact: str = ""           # path to working field code with a test; empty means none
    first_month: int = 0


def evidence_score(r: FieldReport):
    """Engagements times median bespoke hours, and zero without a working artifact. Units: hours a year at risk."""
    if not r.artifact or not r.hours:
        return 0.0
    return len(r.engagements) * statistics.median(r.hours)


def rank_reports(reports, by="evidence"):
    if by == "votes":
        key = lambda r: (-(r.votes * 1_000_000 + r.acv_usd), r.rid)
    else:
        key = lambda r: (-evidence_score(r), r.rid)
    return sorted(reports, key=key)


def loop_metrics(shipped):
    """shipped: list of dicts with first_month, shipped_month, adopted (engagements), hours_before, hours_after."""
    lead = [s["shipped_month"] - s["first_month"] for s in shipped]
    saved = sum((s["hours_before"] - s["hours_after"]) * len(s["adopted"]) for s in shipped)
    return dict(features=len(shipped), median_lead_months=statistics.median(lead) if lead else None,
                adopting_engagements=len({e for s in shipped for e in s["adopted"]}), hours_saved=saved)


def continuity(changes, *, overlap_min=10, notice_min=30):
    """changes: list of (customer, month, outgoing, incoming, overlap_days, notice_days). Per-customer verdicts."""
    out = {}
    for cust, month, old, new, overlap, notice in changes:
        r = out.setdefault(cust, dict(changes=0, bad=[]))
        r["changes"] += 1
        if overlap < overlap_min or notice < notice_min:
            r["bad"].append((month, old, new, overlap, notice))
    return out
