"""the three ledgers side by side, which buckets are closed, and the calibration factor per bucket."""
import statistics, sys
import _paths  # noqa: F401
from world import ACTUAL, ESTIMATE, CLOSED, BUCKETS, total, tax, RATE


def factors(closed_only=True):
    out = {}
    for b in BUCKETS:
        rs = [ACTUAL[n][b] / ESTIMATE[n][b] for n in ACTUAL if (b in CLOSED[n] or not closed_only)]
        out[b] = (statistics.median(rs), len(rs), rs)
    return out


def main(mode="closed"):
    print(f"hours ledger frozen at day 190 (deterministic stand-in), US dollars at ${RATE:.0f} an hour")
    print(f"{'bucket':<12}" + "".join(f"{n:>22}" for n in ACTUAL))
    for b in BUCKETS:
        row = ""
        for n in ACTUAL:
            mark = "" if b in CLOSED[n] else " open"
            row += f"{ACTUAL[n][b]:>7,.0f} / {ESTIMATE[n][b]:>6,.0f}{mark:>5}  "
        print(f"{b:<12}{row}")
    print(f"{'total':<12}" + "".join(f"{total(ACTUAL[n]):>7,.0f} / {total(ESTIMATE[n]):>6,.0f}       " for n in ACTUAL))
    print("integration tax (actual)  " + "   ".join(f"{n} {tax(n):.2f}" for n in ACTUAL))
    print()
    f = factors(closed_only=(mode == "closed"))
    print(f"calibration factor = median(actual / estimate) over {'closed buckets only' if mode == 'closed' else 'ALL buckets, open ones included'}")
    for b in BUCKETS:
        med, k, rs = f[b]
        note = "  <- one engagement only" if k == 1 else ""
        if b == "integration":
            note = "  <- priced with the reserve, not the median"
        print(f"  {b:<12} {med:5.2f}  from {k}  ({', '.join(f'{r:.2f}' for r in rs)}){note}")
    return f


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "closed")
