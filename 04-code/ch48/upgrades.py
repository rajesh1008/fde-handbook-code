"""Model upgrades at three customers: one replay of three model versions against each customer's own gold set and
floors, through fieldkit.liveops.upgrade_gate. The judgments are stored counts from each customer's scorer on its gold
set (deterministic stand-in): Caldwell 628 documents (Lena Ortiz, Tom Whitfield), Pennant 400 EU documents
(Dana Whitaker), Greystone 300 referral packets (Tess Moreno)."""
import _paths  # noqa: F401
from fieldkit.liveops import upgrade_gate, deprecation_plan
from fieldkit.evals import wilson

VERSIONS = ["extract-2026-04", "extract-2027-01", "extract-2027-04"]
GOLD = {"Caldwell": 628, "Pennant": 400, "Greystone": 300}
CRIT = {"Caldwell": "critical fields", "Pennant": "customs code", "Greystone": "criteria citation"}
# per version: fully correct, critical field correct, silently wrong, cost per document (USD), p95 seconds
JUDGED = {
    "Caldwell": {"extract-2026-04": (562, 616, 5, 0.0556, 6.1), "extract-2027-01": (571, 618, 4, 0.0521, 5.4),
                 "extract-2027-04": (574, 619, 4, 0.0589, 5.2)},
    "Pennant": {"extract-2026-04": (352, 391, 6, 0.0358, 4.1), "extract-2027-01": (361, 386, 6, 0.0331, 3.9),
                "extract-2027-04": (365, 392, 5, 0.0329, 3.8)},
    "Greystone": {"extract-2026-04": (254, 295, 4, 0.2673, 16.0), "extract-2027-01": (262, 287, 4, 0.2410, 14.0),
                  "extract-2027-04": (266, 297, 3, 0.2490, 15.0)},
}
FLOORS = {  # (fully, critical, silent-wrong upper bound, cost, p95); set by the customer's decider
    "Caldwell": (0.875, 0.970, 0.020, 0.0600, 8.0),
    "Pennant": (0.850, 0.950, 0.035, 0.0400, 6.0),
    "Greystone": (0.800, 0.970, 0.040, 0.3000, 20.0),
}
LOST = {("Caldwell", "extract-2027-01"): (2, "Anne Kessler"), ("Pennant", "extract-2027-01"): (7, "Tasha Greene"),
        ("Greystone", "extract-2027-01"): (9, None), ("Caldwell", "extract-2027-04"): (1, "Anne Kessler"),
        ("Pennant", "extract-2027-04"): (0, None), ("Greystone", "extract-2027-04"): (1, "Michael Hart")}
ACCEPT = {("Pennant", "extract-2027-01"): {"customs code": "Joanne Pruitt (MC-EU-03)"}}


def dims(c, v):
    n = GOLD[c]; f, k, s, cost, p95 = JUDGED[c][v]
    return dict(fully=round(f / n, 3), crit=round(k / n, 3), silent_upper=round(wilson(s, n)[1], 3), cost=cost, p95=p95)


def gate(c, cand, inc, accepted=None):
    a, b = dims(c, cand), dims(c, inc)
    fl = FLOORS[c]
    d = {"fully correct": (a["fully"], b["fully"], fl[0], True),
         CRIT[c]: (a["crit"], b["crit"], fl[1], True),
         "silent-wrong upper": (a["silent_upper"], b["silent_upper"], fl[2], False),
         "cost per document": (a["cost"], b["cost"], fl[3], False),
         "p95 seconds": (a["p95"], b["p95"], fl[4], False)}
    lost, sign = LOST.get((c, cand), (0, None))
    return upgrade_gate(d, lost, sign, accepted)


def replay():
    out = {}
    for c in GOLD:
        out[c] = {}
        inc = "extract-2026-04"
        for v in VERSIONS[1:]:
            verdict, why = gate(c, v, inc)
            acc = ACCEPT.get((c, v))
            final = None
            if verdict == "HOLD" and acc:
                final, why2 = gate(c, v, inc, acc)
                why = why + [f"after acceptance: {final}"]
            out[c][v] = (inc, verdict, final, why)
            if (final or verdict) == "PROMOTE" and v == "extract-2027-01":
                inc = v
    return out


def pooled(cand, inc="extract-2026-04"):
    """v0: one Northlight gate on the three gold sets pooled, with the loosest floors."""
    n = sum(GOLD.values())
    tot = lambda v, i: sum(JUDGED[c][v][i] for c in GOLD)
    d = {"fully correct": (round(tot(cand, 0) / n, 3), round(tot(inc, 0) / n, 3), 0.80, True),
         "critical field": (round(tot(cand, 1) / n, 3), round(tot(inc, 1) / n, 3), 0.95, True),
         "silent-wrong upper": (round(wilson(tot(cand, 2), n)[1], 3), round(wilson(tot(inc, 2), n)[1], 3), 0.04, False)}
    return n, upgrade_gate(d, 0)


def main():
    n, (v, why) = pooled("extract-2027-01")
    print(f"v0 POOLED GATE  extract-2027-01 vs extract-2026-04 on {n} pooled documents: {v}")
    for w in why:
        print(f"    {w}")
    print()
    print("MODEL UPGRADE REPLAY  three customers x three model versions  (deterministic stand-in)")
    for c in GOLD:
        print(f"\n{c}: gold set {GOLD[c]}; floors fully {FLOORS[c][0]}, {CRIT[c]} {FLOORS[c][1]}, "
              f"silent-wrong upper {FLOORS[c][2]}, cost {FLOORS[c][3]}, p95 {FLOORS[c][4]}")
        for v in VERSIONS:
            d = dims(c, v)
            print(f"  {v}: fully {d['fully']:.3f}  {CRIT[c]} {d['crit']:.3f}  silent-wrong upper {d['silent_upper']:.3f}"
                  f"  cost {d['cost']:.4f}  p95 {d['p95']}")
    print("\nVERDICTS (candidate against the incumbent the customer is running at the time)")
    res = replay()
    for c, rows in res.items():
        for v, (inc, verdict, final, why) in rows.items():
            print(f"  {c:<9} {v} vs {inc}: {verdict}" + (f" -> {final}" if final else ""))
            for w in why:
                print(f"      {w}")
    print("\nGreystone: extract-2026-04 retirement on Azure westus3 read against the change calendar")
    p = deprecation_plan(notice_day=470, retire_day=590, freezes=[(440, 461), (575, 588)], evidence_days=30)
    print("  " + "  ".join(f"{k}={v}" for k, v in p.items()))
    return res


if __name__ == "__main__":
    main()
