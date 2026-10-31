"""fieldkit.integration (book layer v1.4, Chapter 10): the integration-tax estimator.

The integration tax is integration hours per hour of model work (Chapter 2). This module estimates it before the
build from a systems inventory: one Line per piece of integration work, tagged with one of six sources, a
three-point estimate in hours, the claim status of the fact the hours rest on, the customer role who can confirm
that fact, and (for unconfirmed facts) the priced alternative if the fact turns out to be false.
Standard library only; every random draw is seeded so a run is repeatable.
"""
from __future__ import annotations
import random
from dataclasses import dataclass, field, replace

INTEGRATION_VERSION = "1.4"
SOURCES = ("access", "identity", "formats", "exceptions", "environments", "gateways")
STATUSES = ("direct customer fact", "reconstructed from supplied artifact", "vendor position",
            "proposed design", "decision required")
# how far the high end stretches beyond the estimator's own high, by the status of the fact underneath
SPREAD = {"direct customer fact": 1.0, "reconstructed from supplied artifact": 1.25, "vendor position": 1.6,
          "proposed design": 1.5, "decision required": 1.8}
UNCONFIRMED = ("vendor position", "proposed design", "decision required")
MUST_PRICE = ("vendor position", "decision required")   # facts about the customer's estate that Northlight does not own


@dataclass
class Line:
    lid: str
    source: str
    system: str
    what: str
    low: float
    likely: float
    high: float
    status: str
    rests_on: str
    owner: str = ""                       # customer role that can confirm or deny the fact
    alt: list = field(default_factory=list)   # Lines that replace this one if the fact is false

    def problems(self):
        p = []
        if self.source not in SOURCES: p.append(f"{self.lid}: unknown source {self.source!r}")
        if self.status not in STATUSES: p.append(f"{self.lid}: unknown status {self.status!r}")
        if not (0 <= self.low <= self.likely <= self.high): p.append(f"{self.lid}: needs low <= likely <= high")
        if not self.rests_on.strip(): p.append(f"{self.lid}: no fact named under the hours")
        return p

    @property
    def stretched_high(self):
        return self.likely + (self.high - self.likely) * SPREAD[self.status]

    @property
    def exposure(self):
        """Extra likely hours if the fact underneath is false (0 when no alternative is priced)."""
        return sum(a.likely for a in self.alt) - self.likely if self.alt else 0.0


@dataclass
class Range:
    p10: float
    p50: float
    p90: float


@dataclass
class Estimate:
    hours: Range
    tax: Range
    point_hours: float
    point_tax: float


class Inventory:
    def __init__(self, customer, model_hours, day=None):
        self.customer, self.model_hours, self.day, self.lines = customer, tuple(model_hours), day, []

    def add(self, *lines):
        for ln in lines:
            bad = ln.problems()
            if bad: raise ValueError("; ".join(bad))
            self.lines.append(ln)
        return self

    def total(self):
        return sum(l.likely for l in self.lines)

    def point_tax(self):
        return self.total() / self.model_hours[1]

    def by_source(self):
        out = {s: 0.0 for s in SOURCES}
        for l in self.lines: out[l.source] += l.likely
        return out

    def unconfirmed(self):
        return [l for l in self.lines if l.status in UNCONFIRMED]

    def exposure(self):
        return sum(l.exposure for l in self.unconfirmed())

    def simulate(self, n=20000, seed=10):
        rng = random.Random(seed); hs, ts = [], []
        ml, mm, mh = self.model_hours
        for _ in range(n):
            h = sum(rng.triangular(l.low, l.stretched_high, l.likely) for l in self.lines)
            m = rng.triangular(ml, mh, mm)
            hs.append(h); ts.append(h / m)
        q = lambda xs, p: sorted(xs)[int(p * (len(xs) - 1))]
        return Estimate(Range(q(hs, .1), q(hs, .5), q(hs, .9)), Range(q(ts, .1), q(ts, .5), q(ts, .9)),
                        self.total(), self.point_tax())

    def deny(self, lid, by, day):
        """The fact under line lid is false: replace it with its priced alternative (or fail loudly)."""
        new = Inventory(self.customer, self.model_hours, day)
        for l in self.lines:
            if l.lid != lid: new.lines.append(l); continue
            if not l.alt:
                raise ValueError(f"{lid} denied by {by} on day {day}, and no alternative was priced")
            new.lines.extend(replace(a, rests_on=f"{a.rests_on} (after denial by {by}, day {day})") for a in l.alt)
        return new

    def lint(self):
        """Refusals that stop an estimate going to the customer."""
        out = []
        for l in self.unconfirmed():
            if not l.owner:
                out.append(f"{l.lid}: rests on a {l.status} with no customer owner to confirm it")
            if l.status in MUST_PRICE and not l.alt:   # size does not matter: a 40 h line can hide a 450 h denial
                out.append(f"{l.lid}: {l.likely:.0f} h on a {l.status} with no priced alternative")
        return out

    def drivers(self, k=3):
        """Lines that contribute most to the width of the range (stretched high minus low)."""
        return sorted(self.lines, key=lambda l: l.stretched_high - l.low, reverse=True)[:k]

    def customer_page(self, est=None):
        est = est or self.simulate(); r = []
        r.append(f"INTEGRATION ESTIMATE  {self.customer}  day {self.day}  (fieldkit.integration {INTEGRATION_VERSION})")
        r.append(f"  integration hours: {est.hours.p10:,.0f} to {est.hours.p90:,.0f} (P10 to P90), median {est.hours.p50:,.0f};"
                 f" sum of most-likely lines {est.point_hours:,.0f}")
        r.append(f"  model work hours:  {self.model_hours[0]:,.0f} to {self.model_hours[2]:,.0f}, most likely {self.model_hours[1]:,.0f}")
        r.append(f"  integration tax:   {est.tax.p10:.2f} to {est.tax.p90:.2f}, median {est.tax.p50:.2f};"
                 f" sum of most-likely lines {est.point_tax:.2f}")
        r.append("  what drives the width:")
        for l in self.drivers():
            r.append(f"    {l.lid:<6}{l.what} ({l.low:.0f} to {l.stretched_high:.0f} h; {l.status})")
        r.append("  facts you own that move the estimate:")
        for l in sorted(self.unconfirmed(), key=lambda l: -max(l.exposure, l.likely)):
            ex = f"+{l.exposure:.0f} h if not" if l.alt else "not priced"
            r.append(f"    {l.lid:<6}{l.rests_on}  owner: {l.owner or 'NONE'}  ({ex})")
        lint = self.lint()
        r.append("  lint: " + ("clean" if not lint else f"{len(lint)} refusal(s), do not send"))
        r += [f"    {x}" for x in lint]
        return "\n".join(r)
