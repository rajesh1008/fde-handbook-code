"""fieldkit v5 (Chapter 41): the hand-over test.

Hand-over readiness is scored from evidence the customer produced alone, never from documents that exist.
Item credit: alone 1.0 (a customer person did it with no vendor hands), assisted 0.5 (a customer person did it
with the vendor present or helping), exists 0.0 (the artifact exists, nobody at the customer has used it),
missing 0.0. Gate items cap the score at GATE_CAP while any of them is below "alone".
Also here: alert routing check, runbook lint, RACI check, reading-path coverage, and a deterministic drill.
Book layer; the package version stays 0.1.0.
"""
from dataclasses import dataclass, field, replace

CREDIT = {"alone": 1.0, "assisted": 0.5, "exists": 0.0, "missing": 0.0}
GATE_CAP = 0.6
FAILURE_CLASS_MODE = {"quality": "shadow", "data": "off", "security": "off", "availability": "fail-closed"}


@dataclass(frozen=True)
class Item:
    id: str
    dim: str
    text: str
    status: str
    by: tuple = ()
    gate: bool = False

    def __post_init__(self):
        if self.status not in CREDIT:
            raise ValueError(f"{self.id}: unknown status {self.status}")
        if self.status in ("alone", "assisted") and not self.by:
            raise ValueError(f"{self.id}: {self.status} needs a named customer person")


@dataclass
class Score:
    naive: float
    raw: float
    gated: float
    failing_gates: list = field(default_factory=list)

    @property
    def capped(self):
        return self.gated < self.raw


def score(items):
    n = len(items)
    naive = sum(i.status != "missing" for i in items) / n
    raw = sum(CREDIT[i.status] for i in items) / n
    failing = [i.id for i in items if i.gate and i.status != "alone"]
    gated = min(raw, GATE_CAP) if failing else raw
    return Score(round(naive, 3), round(raw, 3), round(gated, 3), failing)


def without(items, person):
    """The same items if one person leaves: anything only that person demonstrated falls back to 'exists'."""
    out = []
    for i in items:
        by = tuple(p for p in i.by if p != person)
        if i.status in ("alone", "assisted") and not by:
            out.append(replace(i, status="exists", by=()))
        else:
            out.append(replace(i, by=by))
    return out


def single_points(items):
    """Per person: how far the gated score falls if that person leaves. Largest drop first."""
    base = score(items).gated
    people = sorted({p for i in items for p in i.by})
    drops = [(p, round(base - score(without(items, p)).gated, 3)) for p in people]
    return sorted([d for d in drops if d[1] > 0], key=lambda d: (-d[1], d[0]))


@dataclass(frozen=True)
class Alert:
    id: str
    monitor: str
    dest: str
    runbook: str = ""


def route_check(alerts, customer_domains):
    """Every alert must land at a destination the customer owns. Returns the alerts that do not."""
    bad = []
    for a in alerts:
        dom = a.dest.split("@")[-1] if "@" in a.dest else a.dest.split(":")[0]
        if dom not in customer_domains:
            bad.append(a)
    return bad


@dataclass(frozen=True)
class Step:
    action: str
    by_role: str
    verify: str = ""
    abort_if: str = ""


@dataclass(frozen=True)
class Runbook:
    id: str
    title: str
    trigger: str
    failure_class: str
    mode: str
    owner: str
    steps: tuple
    exit_via: str = ""


def lint_runbook(rb, customer_people, alerts, vendor_words=("northlight", "nl-")):
    """Findings as (rule, detail). RB1 owner, RB2 verify, RB3 trigger routed, RB4 mode rule, RB5 vendor, RB6 off exit."""
    f = []
    if rb.owner not in customer_people:
        f.append(("RB1", f"owner {rb.owner!r} is not a customer person"))
    for n, s in enumerate(rb.steps, 1):
        if not s.verify:
            f.append(("RB2", f"step {n} has no verify line"))
        text = (s.action + " " + s.by_role).lower()
        if any(w in text for w in vendor_words):
            f.append(("RB5", f"step {n} needs the vendor: {s.action}"))
    trig = [a for a in alerts if a.id == rb.trigger]
    if not trig:
        f.append(("RB3", f"trigger {rb.trigger} is not an alert rule"))
    want = FAILURE_CLASS_MODE.get(rb.failure_class)
    if want != rb.mode:
        f.append(("RB4", f"{rb.failure_class} problems go to {want}, runbook says {rb.mode}"))
    if rb.mode == "off" and rb.exit_via != "shadow":
        f.append(("RB6", "off returns via shadow, never directly to live"))
    return f


def raci_check(rows, customer_people, vendor="Northlight"):
    """rows: (activity, R, A, C/I). Exactly one A per activity, a customer person, never the vendor."""
    f = []
    for act, r, a, ci in rows:
        accs = [x.strip() for x in a.split(",") if x.strip()]
        if len(accs) != 1:
            f.append((act, f"{len(accs)} accountable"))
        elif accs[0] == vendor or accs[0].startswith(vendor):
            f.append((act, "vendor accountable"))
        elif accs[0] not in customer_people:
            f.append((act, f"accountable {accs[0]!r} is not a named customer person"))
    return f


def path_coverage(paths, needs):
    """paths: stakeholder -> section ids; needs: stakeholder -> section ids their duties require. Missing per path."""
    return {s: sorted(set(needs.get(s, ())) - set(paths.get(s, ()))) for s in needs if set(needs[s]) - set(paths.get(s, ()))}


@dataclass(frozen=True)
class Scenario:
    name: str
    fault_at: int            # minutes after midnight, site time
    alert: str               # alert rule the fault raises first
    detect_lag: int          # rule evaluation delay, minutes
    backstop: str = ""       # second alert that fires from downstream symptoms
    backstop_at: int = 0
    deadline: int = 0        # minutes after midnight; 0 = none


def drill(sc, alerts, rota, runbook_minutes, customer_domains, detect_max=15, mitigate_max=60):
    """Deterministic drill. rota: destination -> (party, ack_minutes or None if nobody is on).
    The vendor is an observer: a page that reaches it counts as a touch and is never acted on."""
    route = {a.id: a.dest for a in alerts}
    log, touches = [], 0
    detected = None
    for aid, t in ((sc.alert, sc.fault_at + sc.detect_lag), (sc.backstop, sc.backstop_at)):
        if not aid or detected is not None:
            continue
        dest = route[aid]
        party, ack = rota.get(dest, ("nobody", None))
        log.append((t, f"{aid} fires, routed to {dest}"))
        if dest.split("@")[-1] not in customer_domains:
            touches += 1
            log.append((t, f"page reaches {party} (observer, hands off): vendor touch"))
            continue
        if ack is None:
            log.append((t, f"page reaches {party}: nobody on rota"))
            continue
        if detected is None:
            detected = t + ack
            log.append((detected, f"{party} acknowledges"))
    if detected is None:
        return dict(log=log, detect=None, mitigate=None, touches=touches, passed=False, deadline_missed=bool(sc.deadline))
    t = detected
    for step, mins in runbook_minutes:
        t += mins
        log.append((t, f"verified: {step}"))
    det, mit = detected - sc.fault_at, t - sc.fault_at
    missed = bool(sc.deadline) and t > sc.deadline
    passed = touches == 0 and det <= detect_max and mit <= mitigate_max and not missed
    return dict(log=log, detect=det, mitigate=mit, touches=touches, passed=passed, deadline_missed=missed)


def hhmm(m):
    return f"{m // 60:02d}:{m % 60:02d}"
