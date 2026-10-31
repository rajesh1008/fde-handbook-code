"""Estates (fieldkit v2.5, Chapter 20): one toolkit, three clouds.

The rule is one interface per concern and one thin adapter per cloud. The core (the evaluation
suite, the gateway adapter, the connectors) never imports a cloud SDK. It talks to five ports:

* identity  who the workload is: a role, a managed identity or a service account, never a key file;
* secrets   read at call time from the customer's own store;
* model     one call shape in, one ModelResult out, with the served version always reported;
* logs      the customer's sink, and only the customer's sink;
* network   a probe that proves the private path works and the public path does not.

Model access is pinned per estate and per region. resolve_pin refuses to substitute a version:
when the pinned version is not offered in any region the residency rule allows, it raises
VersionUnavailable with the three options a person must choose between. conformance() turns one
deployment's evidence into the fourteen parity checks of Table 20.3. Standard library only.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field

PORTS = ("identity", "secrets", "model", "logs", "network")

# What the toolkit deliberately does not hide behind the ports (Table 20.2).
REFUSE_TO_ABSTRACT = [
    ("identity", "written in each cloud's own terms, because the customer's identity team reviews it in those terms"),
    ("network", "private endpoints, perimeters and egress rules belong to the customer and live in the customer's IaC"),
    ("region and residency", "which region may hold which data is the customer's decision, never a default"),
    ("model version", "a different version is a model change; no adapter may choose one"),
    ("cost", "each estate's cost is read from that estate's own records, never averaged across clouds"),
]

UNAVAILABLE_OPTIONS = [
    ("wait", "stay on the approved path and get a date from the provider for the pinned version in an allowed region"),
    ("move region", "process where the pin is offered, only if the customer's residency owner changes the rule in writing"),
    ("change the pin", "validate the offered version on in-region data with the evaluation suite and record a model change"),
]


@dataclass
class ModelResult:
    output: dict
    served_version: str | None
    tokens_in: int
    tokens_out: int
    region: str
    request_id: str | None = None


@dataclass(frozen=True)
class ModelPin:
    family: str
    version: str
    regions: tuple          # the regions the residency rule allows for this workload, in order of preference
    evidence: str = ""      # where the validation of this version is recorded


class VersionUnavailable(Exception):
    def __init__(self, pin: ModelPin, offered: dict, elsewhere: list):
        self.pin, self.offered, self.elsewhere = pin, offered, elsewhere
        where = "; ".join(f"{r}: {', '.join(v) or 'none'}" for r, v in offered.items())
        super().__init__(f"{pin.family} is pinned to {pin.version}, which no allowed region offers ({where})")

    def options(self) -> list[tuple[str, str]]:
        out = list(UNAVAILABLE_OPTIONS)
        if not self.elsewhere:
            out = [o for o in out if o[0] != "move region"]
        return out


def resolve_pin(pin: ModelPin, catalog: dict) -> tuple[str, str]:
    """catalog[region][family] -> versions offered there. Returns (region, version) or raises."""
    for region in pin.regions:
        if pin.version in catalog.get(region, {}).get(pin.family, []):
            return region, pin.version
    offered = {r: list(catalog.get(r, {}).get(pin.family, [])) for r in pin.regions}
    elsewhere = sorted(r for r, fams in catalog.items()
                       if r not in pin.regions and pin.version in fams.get(pin.family, []))
    raise VersionUnavailable(pin, offered, elsewhere)


def resolve_latest(family: str, region: str, catalog: dict) -> tuple[str, str]:
    """What an unpinned 'latest' does: whatever the region offers. Shown only to be refused."""
    return region, max(catalog[region][family])


CHECKS = [
    ("I1", "identity", "workload identity, no static credential"),
    ("I2", "secrets", "secret or token read at call time"),
    ("I3", "secrets", "calls survive a rotation or token expiry"),
    ("N1", "network", "model reached over the private path"),
    ("N2", "network", "public endpoint refused from the workload"),
    ("N3", "network", "egress to an unlisted host refused"),
    ("M1", "model", "processing region inside the residency rule"),
    ("M2", "model", "served version equals the pin on every call"),
    ("M3", "model", "no deprecation notice past its warning date"),
    ("L1", "logs", "logs only in the customer's sink"),
    ("L2", "logs", "one call record with tokens per model call"),
    ("E1", "suite", "evaluation suite ran on the customer's signed set"),
    ("C1", "iac", "IaC plan passes the customer's policy scanner"),
    ("C2", "iac", "deployed state matches the IaC (no drift)"),
]


@dataclass
class Evidence:
    """What one deployment to one estate proved. Every field is filled by exercising the estate."""
    credential: str = "workload"            # workload | static_key | person
    secret_at_call: bool = False
    rotation_ok: bool = False
    private_ok: bool = False
    public_refused: bool = False
    egress_refused: bool = False
    region: str = ""
    allowed_regions: tuple = ()
    served: Counter = field(default_factory=Counter)
    pinned: str = ""
    deprecations_red: int = 0
    foreign_log_records: int = 0
    calls: int = 0
    records_with_tokens: int = 0
    suite_ran: bool = False
    scanner_findings: list = field(default_factory=list)
    drift: list = field(default_factory=list)


def conformance(ev: Evidence) -> list[tuple[str, bool, str]]:
    off_pin = sum(n for v, n in ev.served.items() if v != ev.pinned)
    res = {
        "I1": (ev.credential == "workload", ev.credential),
        "I2": (ev.secret_at_call, "at call" if ev.secret_at_call else "cached at start"),
        "I3": (ev.rotation_ok, "ok" if ev.rotation_ok else "failed after rotation"),
        "N1": (ev.private_ok, "private" if ev.private_ok else "no private path"),
        "N2": (ev.public_refused, "refused" if ev.public_refused else "public reachable"),
        "N3": (ev.egress_refused, "refused" if ev.egress_refused else "egress open"),
        "M1": (ev.region in ev.allowed_regions, ev.region),
        "M2": (ev.calls > 0 and off_pin == 0, f"{off_pin} of {sum(ev.served.values())} off pin"),
        "M3": (ev.deprecations_red == 0, f"{ev.deprecations_red} past warning"),
        "L1": (ev.foreign_log_records == 0, f"{ev.foreign_log_records} records outside"),
        "L2": (ev.calls > 0 and ev.records_with_tokens == ev.calls, f"{ev.records_with_tokens}/{ev.calls}"),
        "E1": (ev.suite_ran, "ran" if ev.suite_ran else "not run"),
        "C1": (not ev.scanner_findings, ", ".join(ev.scanner_findings) or "clean"),
        "C2": (not ev.drift, ", ".join(ev.drift) or "none"),
    }
    return [(cid, res[cid][0], res[cid][1]) for cid, _, _ in CHECKS]


def passed(results) -> int:
    return sum(1 for _, ok, _ in results if ok)


def estate_cost(model_per_doc: float, fixed_monthly: dict, docs_per_month: int) -> dict:
    """Cost per scored document on one estate: model calls plus that estate's fixed bill spread over volume."""
    fixed = sum(fixed_monthly.values())
    share = fixed / max(docs_per_month, 1)
    return dict(model=round(model_per_doc, 4), fixed_monthly=round(fixed, 2), fixed_per_doc=round(share, 4),
                total=round(model_per_doc + share, 4),
                volume_where_fixed_equals_model=int(fixed / model_per_doc) if model_per_doc else None)
