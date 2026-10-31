"""Listing 33.6 and 33.7: the failure injection (a metric Caldwell cannot compute without Northlight) and the fix."""
from world import M, METRICS_V1, METRICS_V2, VENDOR_IDS


def report(metrics, label):
    res = M.computability(metrics, "Caldwell", VENDOR_IDS)
    bad = [m for m, b in res if b]
    print(f"{label}: {len(metrics) - len(bad)} of {len(metrics)} metrics computable by Caldwell alone")
    for m, b in res:
        print(f"  {m.mid} {m.name:<52} {'OK' if not b else 'NEEDS NORTHLIGHT'}")
        for x in b:
            print(f"       - {x}")
    return bad


if __name__ == "__main__":
    report(METRICS_V1, "pack v1 (day 140)")
    print()
    report(METRICS_V2, "pack v2 (day 144)")
    print()
    print("M1 recomputed by Caldwell's job (runs as cw-claims-batch on day 149, Tom Whitfield's audit labels)")
    weeks = [(134, 981, 8), (141, 847, 11), (148, 845, 27)]  # Chapter 27 weekly audits
    for day, n, k in weeks:
        lo = M.wilson_lower(k, n)
        flag = "RE-CALIBRATE" if lo > 0.02 else "within promise"
        print(f"  day {day}: {k:>2} of {n} proceed fields wrong ({k / n:.1%}, low {lo:.1%}) -> {flag}")
