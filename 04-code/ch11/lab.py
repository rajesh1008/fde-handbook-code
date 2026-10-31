"""Chapter 11 lab runner.  python lab.py kickoff|day12|day40|champions|three|oakley|status|series|architects"""
import sys, statistics
import _path  # noqa: F401
from fieldkit.cadence import bus_factor
import stakeholders as S, champions as C, greystone as G, caldwell, pennant, oakley41, plan, status


def run(cmd):
    if cmd == "kickoff":
        print(S.report(G.KICKOFF))
    elif cmd == "day12":
        print(S.report(G.DAY12))
    elif cmd == "day40":
        print(S.report(G.at_day(G.DAY12, G.CONTACT_DAY40, 40)))
    elif cmd == "champions":
        print(C.register_report(G.CHAMPIONS, 12))
    elif cmd == "three":
        for m in (caldwell.DAY25, pennant.DAY28):
            print(S.report(m)); print()
        print("bus factor across the three working maps")
        for f in bus_factor(S.holdings([G.DAY12, caldwell.DAY25, pennant.DAY28])):
            if f.startswith("concentration"):
                print("  " + f)
    elif cmd == "oakley":
        print(oakley41.summary()); print(); print(plan.report())
    elif cmd == "status":
        for name, s in (("DRAFT", status.DRAFT_W6), ("REWRITE", status.HONEST_W6)):
            print(f"== {name}"); print(status.render(s)); probs = status.lint(s)
            print(f"LINT  {len(probs)} problem(s)"); [print(f"  - {p}") for p in probs]; print()
    elif cmd == "series":
        print("week  day  reported  computed  forecast pilot")
        for w, d, rep, comp, fc in status.series():
            flag = "  <- hides" if rep != comp else ""
            print(f"{w:>4} {d:>4}  {rep:<8}  {comp:<8}  day {fc}{flag}")
    elif cmd == "architects":
        print("Review requests to Priya Natarajan, days to a written answer")
        for kind, days in caldwell.REVIEWS.items():
            print(f"  {kind:<20} n={len(days)}  median {statistics.median(days):>4} days  max {max(days)}")


if __name__ == "__main__":
    for c in sys.argv[1:] or ["kickoff"]:
        run(c)
