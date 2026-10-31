"""Chapter 44 practice layer: staffing, hiring and career checks for an FDE function.

Lab-local (fieldkit unchanged; reuses fieldkit.cadence.bus_factor and fieldkit.pyramid). Deterministic stand-in.
"""
import _paths  # noqa: F401
from itertools import combinations
from fieldkit.cadence import bus_factor
import world as W

ANCHORS = {  # behavioral anchors for the discovery role-play, the exercise raters disagreed on most
    1: "pitches a solution before the second question; never asks what happens to the work after the operator",
    2: "asks about the task but not the exceptions; leaves without a number or a name for who measures it",
    3: "walks the work end to end, finds the exception path, leaves with a baseline and who owns it",
    4: "as 3, and finds the constraint nobody stated (a gate, a union rule, a second system) and tests it aloud",
}


# ---- headcount ------------------------------------------------------------------------------------------------
def headcount(events=W.EVENTS, months=12):
    on, rows = set(), []
    for m in range(1, months + 1):
        for (em, p, kind, _n) in events:
            if em == m:
                (on.add if kind == "in" else on.discard)(p)
        rows.append((m, len(on), sorted(on)))
    return rows


# ---- skill profile --------------------------------------------------------------------------------------------
def holders(people, level=3, profile=W.PROFILE):
    return {c: [(p, "Northlight") for p in people if profile[p][c] >= level] for c in W.COMPETENCIES}


def profile_flags(people, level=3):
    h = holders(people, level)
    flags = bus_factor({c: v for c, v in h.items() if v})
    flags += [f"no holder: {c}" for c, v in h.items() if not v]
    return flags


# ---- hiring rubric --------------------------------------------------------------------------------------------
def observed(exercises):
    return sorted({c for cs in exercises.values() for c in cs}, key=W.COMPETENCIES.index)


def decide(scores, exercises=W.EXERCISES, weights=W.WEIGHTS, floors=W.FLOORS, bar=W.BAR, mode="new"):
    seen = observed(exercises)
    if mode == "old":
        vals = [scores[c] for c in seen if scores.get(c) is not None]
        mean = sum(vals) / len(vals)
        return ("hire" if mean >= W.OLD_BAR else "no hire"), round(mean, 2), f"mean of {', '.join(W.SHORT[c] for c in seen)}"
    missing = [c for c in floors if c not in seen or scores.get(c) is None]
    if missing:
        return "no decision", None, "not observed: " + ", ".join(missing)
    total = sum(weights[c] * scores[c] for c in W.COMPETENCIES if scores.get(c) is not None)
    breach = [f"{c} {scores[c]} < {f}" for c, f in floors.items() if scores[c] < f]
    if breach:
        return "no hire", round(total, 2), "floor: " + "; ".join(breach)
    if total < bar:
        return "no hire", round(total, 2), f"below bar {bar}"
    return "hire", round(total, 2), "meets bar and every floor"


# ---- calibration ----------------------------------------------------------------------------------------------
def kappa(a, b, cats=(1, 2, 3, 4)):
    n = len(a)
    po = sum(x == y for x, y in zip(a, b)) / n
    pe = sum((a.count(k) / n) * (b.count(k) / n) for k in cats)
    return (po - pe) / (1 - pe) if pe < 1 else 1.0


def calibration(ratings):
    pairs = list(combinations(ratings, 2))
    ks = {f"{x.split()[0]}/{y.split()[0]}": kappa(ratings[x], ratings[y]) for x, y in pairs}
    n = len(next(iter(ratings.values())))
    exact = sum(len({ratings[r][i] for r in ratings}) == 1 for i in range(n))
    spread = [max(ratings[r][i] for r in ratings) - min(ratings[r][i] for r in ratings) for i in range(n)]
    return dict(pairs=ks, mean_kappa=sum(ks.values()) / len(ks), unanimous=exact, n=n, max_spread=max(spread),
                spread2=sum(s >= 2 for s in spread))


# ---- pods vs solo ---------------------------------------------------------------------------------------------
PLANS = {
    "solo (one FDE per customer)": {
        "Caldwell": [("Sofia Brennan", 1.0)], "Greystone": [("Aisha Rahman", 1.0)],
        "Pennant": [("Leo Martens", 1.0)], "Harbourline": [("lead FDE", 1.0)],
        "_float": [("Callum Reid", 1.0), ("Imogen Clarke", 1.0)]},
    "pods (two pods of three)": {
        "Caldwell": "A", "Greystone": "A", "Pennant": "B", "Harbourline": "B",
        "_pods": {"A": [("Callum Reid", 1.0), ("Aisha Rahman", 1.0), ("Sofia Brennan", 1.0)],
                  "B": [("lead FDE", 1.0), ("Leo Martens", 1.0), ("Imogen Clarke", 1.0)]}},
    "pods + shared evaluation lead": {
        "Caldwell": "A", "Greystone": "A", "Pennant": "B", "Harbourline": "B",
        "_pods": {"A": [("Callum Reid", 1.0), ("Aisha Rahman", 1.0), ("Sofia Brennan", 0.5)],
                  "B": [("lead FDE", 1.0), ("Leo Martens", 1.0), ("Imogen Clarke", 1.0), ("Sofia Brennan", 0.5)]}},
}
COORD_HOURS = {"solo": 2.0, "pods": 4.5}   # hours a week per person spent on internal coordination (Northlight log)


def staff_of(plan, eng):
    v = plan[eng]
    return plan["_pods"][v] if isinstance(v, str) else v


def evaluate_plan(name, plan):
    out = dict(name=name, engagements={}, met=0, needed=0, single=0)
    for eng, e in W.ENGAGEMENTS.items():
        staff = [p for p, _f in staff_of(plan, eng)]
        caps = {c: [(p, "Northlight") for p in staff if W.PROFILE[p][c] >= 3] for c in e["needs"]}
        met = [c for c, v in caps.items() if v]
        single = [c for c, v in caps.items() if len(v) == 1]
        out["engagements"][eng] = dict(staff=staff, met=met, gaps=[c for c in e["needs"] if c not in met], single=single,
                                       oncall=len(staff) if eng == "Pennant" else None)
        out["met"] += len(met); out["needed"] += len(e["needs"]); out["single"] += len(single)
    if "_pods" in plan:
        out["load"] = {}
        for pod, members in plan["_pods"].items():
            fte = sum(f for _p, f in members)
            need = sum(W.ENGAGEMENTS[e]["fte"] for e, v in plan.items() if v == pod)
            out["load"][pod] = (round(need, 1), round(fte, 1), round(need / fte, 2))
        people = {p for ms in plan["_pods"].values() for p, _f in ms}
        out["coord"] = COORD_HOURS["pods"] * len(people)
    else:
        out["load"] = {e: (W.ENGAGEMENTS[e]["fte"], 1.0, W.ENGAGEMENTS[e]["fte"]) for e in W.ENGAGEMENTS}
        out["coord"] = COORD_HOURS["solo"] * 6
    return out


# ---- rotation and load ----------------------------------------------------------------------------------------
def load_index(travel, pages, tenure):
    return round(travel / 10 + pages / 4 + max(0, tenure - W.MAX_MONTHS_ON_ACCOUNT) * 0.25, 2)


def load_series(person, policy=False, load=W.LOAD, rota_depth=W.ROTA_DEPTH):
    d, out, tenure, prev = load[person], [], 0, None
    for i in range(12):
        t, pg, acc = d["travel"][i], d["pages"][i], d["account"][i]
        if t is None:
            out.append(None); tenure, prev = 0, None; continue
        tenure = tenure + 1 if acc == prev else 1
        prev = acc
        if policy:
            t = min(t, W.TRAVEL_CAP)
            pg = pg / rota_depth if acc == "Pennant" and pg > 2 else pg
            tenure = min(tenure, W.MAX_MONTHS_ON_ACCOUNT)
        out.append(load_index(t, pg, tenure))
    return out


def red_months(series):
    reds = []
    for i in range(1, 12):
        if series[i] is not None and series[i - 1] is not None and series[i] >= W.LOAD_RED and series[i - 1] >= W.LOAD_RED:
            reds.append(i + 1)
    return reds


# ---- career ladder --------------------------------------------------------------------------------------------
def ladder_check(packet, level):
    crit = W.CRITERIA[level]
    ignored = {k: v for k, v in packet.items() if k in W.NOT_EVIDENCE}
    have = {k: v for k, v in packet.items() if k not in W.NOT_EVIDENCE}
    rows = [(k, need, have.get(k, 0), have.get(k, 0) >= need) for k, need in crit.items()]
    return dict(ready=all(r[3] for r in rows), rows=rows, ignored=ignored)


# ---- what to learn --------------------------------------------------------------------------------------------
def durable_value(half_life, transfer, cap=10):
    return round(transfer * min(half_life, cap) / cap, 2)


# ---- going independent ----------------------------------------------------------------------------------------
def portfolio_score(claims):
    showable = [c for c in claims if c[2] in ("shareable", "anonymized")]
    with_metric = [c for c in showable if c[3]]
    return dict(claims=len(claims), showable=len(showable), with_metric=len(with_metric))


def runway(s, r=W.RUNWAY, months=18, lag=1):
    work = [0.0] * (months + 2)
    ramp, m = s["ramp"], s["first_month"]
    for i in range(m, months + 1):
        k = min(i - m, len(ramp) - 1)
        if s.get("ends") and s["ends"] < i <= s["ends"] + s.get("gap", 0):
            continue
        if s.get("ends") and i > s["ends"] + s.get("gap", 0):
            k = min(i - s["ends"] - s["gap"] - 1, len(ramp) - 1)
            work[i] = r["day_rate"] * r["working_days"] * [0.2, 0.35, 0.45, 0.5][k]
            continue
        work[i] = r["day_rate"] * r["working_days"] * ramp[k]
    cash, series = r["savings"], []
    for i in range(1, months + 1):
        cash += (work[i - lag] if i - lag >= 1 else 0.0) - r["fixed_monthly"]
        series.append(round(cash))
    return series
