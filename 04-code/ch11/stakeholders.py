"""Chapter 11 lab: the sponsor map as data (Signature 4) with a staleness check.

A map is a list of people. Each person holds zero or more of the five roles (sponsor, operator, blocker,
approver, owner), may belong to the champion network, and carries the engagement day of the last direct
contact and how the role is known. check() refuses a map you cannot plan from. Standard library only.
"""
from dataclasses import dataclass, field

ROLES = ("sponsor", "operator", "blocker", "approver", "owner")
REQUIRED = ("sponsor", "operator", "approver", "owner")       # an empty blocker column is a WARN, not a pass
STALE_AFTER = {"sponsor": 14, "operator": 10, "blocker": 10, "approver": 14, "owner": 14, "champion": 14}
CONFIRMED = ("observed", "own words")                          # "kickoff" and "org chart" are hypotheses
MAX_ROLES = 3

MISSING = {
    "sponsor": "nobody is named who wants this badly enough to spend political capital on it",
    "operator": "nobody who will use the system every day is on the map",
    "approver": "nobody is named who can say yes at the gate",
    "owner": "nobody is named who will own the system after Northlight leaves",
}


@dataclass
class Person:
    key: str
    name: str
    title: str
    roles: tuple = ()
    last_contact: int | None = None       # engagement day of the last direct contact; None means never met
    champion: bool = False
    reasons: tuple = ()                    # a blocker's written reasons, in the blocker's words
    source: str = "kickoff"               # kickoff | org chart | observed | own words


@dataclass
class StakeholderMap:
    customer: str
    day: int
    people: list = field(default_factory=list)

    def holders(self, role):
        return [p for p in self.people if role in p.roles]

    def champions(self):
        return [p for p in self.people if p.champion]


def limit_for(p):
    lims = [STALE_AFTER[r] for r in p.roles] + ([STALE_AFTER["champion"]] if p.champion else [])
    return min(lims) if lims else None


def check(m, today=None):
    """Return a list of (level, code, message). Any BLOCK means the map is not usable for planning."""
    today = m.day if today is None else today
    out = []
    for r in REQUIRED:
        if not m.holders(r):
            out.append(("BLOCK", f"no-{r}", MISSING[r]))
    if not m.holders("blocker"):
        out.append(("WARN", "no-blocker", "nobody is listed as able to stop this; find them before they find you"))
    for p in m.people:
        if len(p.roles) > MAX_ROLES:
            out.append(("WARN", "concentration", f"{p.name} holds {len(p.roles)} of 5 roles; one absence stops the work"))
        if "blocker" in p.roles and not p.reasons:
            out.append(("BLOCK", "blocker-no-reasons", f"{p.name}: a blocker with no written reasons is a guess about a person"))
        if p.champion and "approver" in p.roles:
            out.append(("WARN", "champion-approver", f"{p.name} is champion and approver; never ask both of the same decision"))
        if {"sponsor", "approver"} <= set(p.roles):
            out.append(("WARN", "sponsor-approver", f"{p.name} is sponsor and approver; name who carries the asks while {p.name.split()[-1]} rules"))
        lim = limit_for(p)
        if lim is None:
            continue
        if p.last_contact is None:
            out.append(("WARN", "never-met", f"{p.name} ({'/'.join(p.roles) or 'champion'}): never met"))
        elif today - p.last_contact > lim:
            out.append(("WARN", "stale", f"{p.name} ({'/'.join(p.roles) or 'champion'}): last contact day "
                                          f"{p.last_contact}, {today - p.last_contact} days ago, limit {lim}"))
        if p.roles and p.source not in CONFIRMED:
            out.append(("WARN", "unconfirmed", f"{p.name}: role '{'/'.join(p.roles)}' known only from {p.source}"))
    return out


def naive_score(m):
    """What a slide shows: share of the five role columns with any name in them."""
    return sum(1 for r in ROLES if m.holders(r)) / len(ROLES)


def gated_score(m, today=None):
    """Full credit for a role only when a holder is confirmed and in contact inside the limit; half otherwise."""
    today = m.day if today is None else today
    total = 0.0
    for r in ROLES:
        best = 0.0
        for p in m.holders(r):
            fresh = p.last_contact is not None and today - p.last_contact <= limit_for(p)
            ok = fresh and p.source in CONFIRMED and (r != "blocker" or p.reasons)
            best = max(best, 1.0 if ok else 0.5)
        total += best
    return total / len(ROLES)


def verdict(m, today=None):
    issues = check(m, today)
    return "NOT USABLE" if any(lv == "BLOCK" for lv, _, _ in issues) else "USABLE"


def report(m, today=None):
    today = m.day if today is None else today
    lines = [f"{m.customer} map, day {m.day}, checked day {today}: {len(m.people)} people"]
    for r in ROLES:
        names = ", ".join(p.name for p in m.holders(r)) or "(nobody)"
        lines.append(f"  {r:<9} {names}")
    lines.append(f"  {'champion':<9} {', '.join(p.name for p in m.champions()) or '(nobody)'}")
    for lv, code, msg in check(m, today):
        lines.append(f"  {lv:<5} {code:<19} {msg}")
    lines.append(f"  naive score {naive_score(m):.2f}   gated score {gated_score(m, today):.2f}   verdict {verdict(m, today)}")
    return "\n".join(lines)


def holdings(maps):
    """Feed fieldkit.cadence.bus_factor: role -> [(person, customer)] across maps."""
    h = {}
    for m in maps:
        for r in ROLES:
            h[f"{m.customer}:{r}"] = [(p.name, m.customer) for p in m.holders(r)]
    return h
