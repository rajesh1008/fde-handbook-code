"""Try It Yourself, Chapter 26: a) how many expert labels does the judge correction need,
b) one number or one per stratum, c) loosen Caldwell's gate and see what would ship."""
import sys
import _paths  # noqa: F401
from world import gold_items, judge_v1, judge_v2, candidate, acc, weighted_acc, CRITICAL
from fieldkit.evals import corrected_interval, CustomerGate

if __name__ == "__main__":
    v = sys.argv[1] if len(sys.argv) > 1 else "a"
    items = gold_items()
    test = [it for it in items if it.split == "test"]
    if v == "a":
        cal_pool = [it for it in items if it.split == "dev"] + test[:1000]
        for name, j in (("judge_v1", judge_v1), ("judge_v2", judge_v2)):
            for n_docs in (25, 50, 100):
                cal = cal_pool[:n_docs * 10]
                p, lo, hi = corrected_interval([j(it) for it in test], [j(it) for it in cal],
                                               [it.anne_ok for it in cal], reps=1000)
                print(f"{name}, {n_docs:3d} expert-labeled documents for calibration: {p:.1%} "
                      f"({lo:.1%} to {hi:.1%}, width {100 * (hi - lo):.1f} points)")
    elif v == "b":
        print(f"one number, weighted to the month's mix: {weighted_acc(items):.1%}")
        print(f"one number, unweighted: {acc(items):.1%}")
        for s in sorted({it.stratum for it in items}, key=lambda s: acc([i for i in items if i.stratum == s])):
            sub = [it for it in items if it.stratum == s]
            print(f"  {s:<22} {acc(sub):.1%}  ({len(sub) // 10} documents)")
    else:
        w = {it.key: it.weight for it in items}
        p7 = {it.key: candidate(it, "p7") for it in items}
        alias = {it.key: candidate(it, "p7+alias") for it in items}
        for lost in (0, 3, 10):
            g = CustomerGate("Caldwell", "Anne Kessler", "Kessler's adjusters", "gold-set-300", CRITICAL,
                             max_lost_critical=lost)
            status, reasons, cells, wb, wa = g.check(p7, alias, weight_of=w.get)
            print(f"lost critical items allowed {lost:2d}: {status:<12} weighted {wb:.1%} -> {wa:.1%}")
        g = CustomerGate("Caldwell", "Anne Kessler", "Kessler's adjusters", "gold-set-300", ())
        print(f"no critical fields declared:     {g.check(p7, alias, weight_of=w.get)[0]}  "
              f"(the five lost policy numbers ship without anyone reading them)")
