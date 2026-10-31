"""fieldkit.service (v5.2, Chapter 43; package stays 0.1.0): managed service or hand-over, the year after.

Five small pieces, each born from a failure in Chapter 43's two-year replay at Pennant and Caldwell:
  aged           hand-over readiness with use-decay: an item a customer person did alone counts "assisted" once
                 nobody at the customer has done it for 180 days and "exists" after 365; assisted decays at 180.
                 A capability the vendor exercises on the customer's behalf is not the customer's capability.
  Path           an operating model as numbers on both sides: monthly fee, vendor hours, customer hours, fixed
                 customer cost, ramp, which items the customer keeps practicing and how often, dated events,
                 vendor-only runbook steps and an assumed (never measured) renewal probability.
  two_year       a month-by-month model: customer cost, vendor fee, vendor cost, vendor margin, FDE share,
                 readiness with decay, and takeover hours (what it would cost the customer to run alone from here).
  exit_lint      every runbook step that touches an asset the customer does not own (a vendor host, account,
                 repository or vault) or an asset nobody registered. Unlike handover.lint_runbook's vendor rule,
                 it does not care who is listed as executing a step, only whether the customer could.
  exit_drill     a customer person runs a runbook as if the vendor were gone, minute by minute, against a deadline.
  price_retainer a retainer priced from an hours band at the loaded rate and a target margin, with an overage
                 rate, and the margin at partial, full and double use, with and without rollover of unused hours.
Pure Python, deterministic, no model calls.
"""
from __future__ import annotations
from dataclasses import dataclass, field, replace
import re
from .handover import score, without

MONTH_DAYS = 30
STALE_ALONE = (180, 365)          # alone -> assisted at 180 days unpractised, -> exists at 365
STALE_ASSISTED = 180              # assisted -> exists at 180
EXIT_HOURS = {"alone": 0, "assisted": 12, "exists": 36, "missing": 48}
REBUILD_HOURS = 20                # per runbook step that depends on a vendor-owned asset
EXIT_BASE = 40                    # contract, access and knowledge transfer for any takeover
FDE_MONTH_HOURS = 140             # billable-capacity hours in one FDE month


# ---------------------------------------------------------------- decay
def aged(item, since):
    """The item as it stands after `since` days without a customer person doing it."""
    st = item.status
    if st == "alone":
        st = "exists" if since >= STALE_ALONE[1] else "assisted" if since >= STALE_ALONE[0] else "alone"
    elif st == "assisted":
        st = "exists" if since >= STALE_ASSISTED else "assisted"
    return item if st == item.status else replace(item, status=st, by=item.by if st != "exists" else ())


# ---------------------------------------------------------------- the two-year model
def _y(v, month):
    return v if isinstance(v, (int, float)) else v[0] if month <= 12 else v[1]


@dataclass
class Path:
    name: str
    fee: object = 0.0               # monthly operations fee, number or (year one, year two); subscription excluded
    vendor_hours: object = 0.0
    customer_hours: object = 0.0
    customer_fixed: float = 0.0     # monthly non-hour customer cost (on-call allowance, tooling)
    ramp: tuple = ()                # extra customer hours in months 1..n
    practice: dict = field(default_factory=dict)  # item id (or "*") -> days between customer exercises
    events: tuple = ()              # (month, "alone", item, people) | (month, "lost", item) | (month, "leave", person)
    vendor_only_steps: int = 0
    renewal: float = 0.0            # assumed probability the service renews at month 12 (an input, not a measurement)


@dataclass
class Month:
    month: int
    customer_cost: float
    fee: float
    vendor_cost: float
    readiness: float
    capped: bool
    takeover_hours: float
    decayed: tuple

    @property
    def vendor_margin(self):
        return None if not self.fee else round((self.fee - self.vendor_cost) / self.fee, 3)


def takeover_hours(items, vendor_only_steps=0):
    return EXIT_BASE + sum(EXIT_HOURS[i.status] for i in items) + REBUILD_HOURS * vendor_only_steps


def two_year(path, items0, months=24, vendor_rate=150.0, customer_rate=110.0):
    state = {i.id: i for i in items0}
    last = {i.id: 0 for i in items0}
    rows = []
    for m in range(1, months + 1):
        day = m * MONTH_DAYS
        for ev in path.events:
            if ev[0] != m:
                continue
            if ev[1] == "alone":
                state[ev[2]] = replace(state[ev[2]], status="alone", by=tuple(ev[3])); last[ev[2]] = day
            elif ev[1] == "lost":
                state[ev[2]] = replace(state[ev[2]], status="exists", by=())
            elif ev[1] == "leave":
                state = {i.id: i for i in without(list(state.values()), ev[2])}
        for iid, it in state.items():
            p = path.practice.get(iid, path.practice.get("*"))
            if p and it.status in ("alone", "assisted") and day - last[iid] >= p:
                last[iid] = day
        now = [aged(state[i], day - last[i]) for i in state]
        s = score(now)
        hours = _y(path.customer_hours, m) + (path.ramp[m - 1] if m <= len(path.ramp) else 0)
        rows.append(Month(m, round(hours * customer_rate + path.customer_fixed + _y(path.fee, m), 2),
                          float(_y(path.fee, m)), round(_y(path.vendor_hours, m) * vendor_rate, 2), s.gated, s.capped,
                          takeover_hours(now, path.vendor_only_steps),
                          tuple(i.id for i, o in zip(now, state.values()) if i.status != o.status)))
    return rows


def summary(path, rows):
    """Per year: customer cost, vendor revenue, cost, gross profit, margin, FDE share; end-of-year readiness and
    takeover hours; two-year vendor gross profit weighted by the assumed renewal probability."""
    out = {}
    for y in (1, 2):
        r = [x for x in rows if (x.month - 1) // 12 == y - 1]
        if not r:
            continue
        rev, cost = sum(x.fee for x in r), sum(x.vendor_cost for x in r)
        out[y] = dict(customer=round(sum(x.customer_cost for x in r)), revenue=round(rev), cost=round(cost),
                      gp=round(rev - cost), margin=None if not rev else round((rev - cost) / rev, 3),
                      fde=round(cost / 150.0 / len(r) / FDE_MONTH_HOURS, 2), readiness=r[-1].readiness,
                      takeover=r[-1].takeover_hours)
    if 2 in out:
        out["weighted_gp"] = round(out[1]["gp"] + path.renewal * out[2]["gp"])
    return out


# ---------------------------------------------------------------- exit lint and drill
_ASSETY = re.compile(r"\b(?:[a-z0-9-]+\.)+example(?:/[\w./-]+)?|\b(?:gs|s3)://[\w./-]+|\bgithub\.com/[\w./-]+|"
                     r"\b[a-z]+-bastion-\d+\b|\bvault:[\w/-]+")


@dataclass(frozen=True)
class Finding:
    runbook: str
    step: int
    asset: str
    owner: str

    def __str__(self):
        return f"{self.runbook} step {self.step}: {self.asset} ({self.owner})"


def assets_in(text):
    return [a.rstrip(".,;") for a in _ASSETY.findall(text)]


def exit_lint(runbook, owners, customer="customer"):
    """Every step touching an asset the customer does not own, or one nobody registered (owner 'unregistered').
    owners: asset -> owner. A prefix match counts (a path inside a registered repository or bucket)."""
    out = []
    for n, s in enumerate(runbook.steps, 1):
        for a in assets_in(s.action + " " + s.verify):
            owner = next((o for k, o in owners.items() if a == k or a.startswith(k.rstrip("/") + "/")), "unregistered")
            if owner != customer:
                out.append(Finding(runbook.id, n, a, owner))
    return out


def exit_drill(runbook, owners, person, minutes, workarounds=None, start=120, deadline=210, customer="customer"):
    """`person` runs the runbook as if the vendor were gone. minutes[n] is the time step n takes. A step touching a
    vendor asset blocks unless `workarounds` names a customer route for it (asset -> (route, extra minutes))."""
    t, log, workarounds = start, [], workarounds or {}
    for n, s in enumerate(runbook.steps, 1):
        bad = [f for f in exit_lint(replace(runbook, steps=(s,)), owners, customer)]
        for f in bad:
            if f.asset in workarounds:
                route, extra = workarounds[f.asset]
                t += extra
                log.append((t, n, f"workaround for {f.asset}: {route} (+{extra} min)"))
            else:
                log.append((t, n, f"blocked: {f.asset} belongs to {f.owner}"))
                return dict(passed=False, person=person, end=t, deadline_missed=True, log=log, blocked_at=n)
        t += minutes[n - 1]
        log.append((t, n, s.action))
    return dict(passed=t <= deadline, person=person, end=t, deadline_missed=t > deadline, log=log, blocked_at=None)


# ---------------------------------------------------------------- retainer pricing
@dataclass(frozen=True)
class Retainer:
    band: float
    fee: float
    hourly: float
    overage: float
    rate: float

    def margin(self, used, carried=0.0):
        """Margin in a month with `used` hours; `carried` unused hours from earlier months are free to use."""
        billable_over = max(0.0, used - self.band - carried)
        rev = self.fee + billable_over * self.overage
        return round((rev - used * self.rate) / rev, 3)


def price_retainer(band, rate=150.0, target=0.60, overage_mult=1.25, round_to=100):
    fee = round(band * rate / (1 - target) / round_to) * round_to
    hourly = round(fee / band, 2)
    return Retainer(band, float(fee), hourly, round(hourly * overage_mult, 2), rate)
