"""Listing 34.10/34.11: Marcus Bell's clauses. Greystone's amendment as procurement redlined it on day 108 and as
signed on day 127, the trigger that starts the subscription, and what a month of delay costs."""
import sys, pathlib
import _paths  # noqa: F401
from fieldkit.contract import extract, lint, trigger_findings
import world as W
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "ch02"))
from margin import pilot_month_cost  # noqa: E402
import contracts as C2  # noqa: E402


def report(clauses, title):
    cs, cust, none = extract(clauses)
    lint(cs, dependencies=W.GREYSTONE_DEPS, decisions=W.GREYSTONE_DECISIONS)
    trig = trigger_findings(cust)
    print(f"{title}: {len(cs)} vendor commitments, {len(cust)} customer obligations")
    n = 0
    for c in cs:
        for k, why in c.findings:
            n += 1
            print(f"  {c.cid:8} {k:19} {why}")
    for cid, k, why in trig:
        n += 1
        print(f"  {cid:8} {k:19} {why}")
    for c in cs:
        if c.kind == "service level":
            print(f"  {c.cid:8} service level parts: " + ", ".join(f"{k}={v}" for k, v in c.params.items()
                                                                     if k in ("unit", "scorer", "sample", "window",
                                                                              "threshold")) +
                  f"; remedy: {c.remedy or '-'}; missing: {', '.join(c.missing) or 'none'}")
    print(f"  findings: {n}\n")


def main():
    report(W.GREYSTONE_108, W.G108)
    report(W.GREYSTONE_127, W.G127)
    m = pilot_month_cost(C2.CONTRACTS["greystone"], C2.FIELD_ESTIMATE["greystone"])
    print("WHAT ONE MONTH WITHOUT ACCEPTANCE COSTS NORTHLIGHT (Ch2 model, Greystone)")
    print(f"  deferred subscription ${m['deferred_subscription']:,.0f} + FDE burn ${m['fde_cost']:,.0f} "
          f"({m['fde_hours']:.0f} h) + run ${m['run']:,.0f} = ${m['total']:,.0f}")
    print("\nGATES WAITING ON EACH OTHER (Greystone, days)")
    for d, e in [(104, "security review: 29 passed, 12 findings (Ch32)"),
                 (108, "Marcus Bell's redline: GA-01 to GA-07"),
                 (113, "FDE sends the engineering exhibit: data map, acceptance test, action list"),
                 (120, "F-10 closed: provider retention terms confirmed (owner Marcus Bell)"),
                 (124, "Exhibit A agreed: Michael Hart's reviewers score 110 referrals"),
                 (127, "amendment signed"),
                 (131, "pilot starts [CHECK ch38]")]:
        print(f"  day {d:3}  {e}")


if __name__ == "__main__":
    main()
