"""Listing 34.1/34.2: the contract-commitment extractor on Caldwell's addendum, v0 pricing, the measurability
check (the failure: an accuracy service level nobody can measure), and the margin priced honestly."""
import sys
import _paths  # noqa: F401
from collections import Counter
from fieldkit.contract import extract, lint, CostLine
import world as W


def credits(c, honest, version):
    """Year-one service credits for a service-level commitment."""
    pct = c.params.get("credit_pct", 0) / 100
    if c.metric == "accuracy":
        if version == "v5":
            from sl import caldwell_design
            p = caldwell_design().p_breach(0.009)
            return p * W.CREDIT_MONTHS * pct * W.FEE_MONTH, f"P(breach) {p:.1%} a month at 0.9% error"
        met = c.params["threshold"] <= W.READINGS[0][1]
        if not honest:
            return 0.0, f"reading '{W.READINGS[0][0]}' = {W.READINGS[0][1]}% -> met"
        missed = sum(r[1] < c.params["threshold"] for r in W.READINGS)
        return (W.CREDIT_MONTHS * pct * W.FEE_MONTH,
                f"{missed} of {len(W.READINGS)} readings miss; Caldwell chooses -> missed {W.CREDIT_MONTHS} of "
                f"{W.CREDIT_MONTHS} months" + ("" if met else ""))
    if c.metric == "availability":
        a = W.AVAILABILITY[c.params["measured_at"]]
        if a >= c.params["threshold"]:
            return 0.0, f"{a}% at the {c.params['measured_at']} -> met"
        return W.CREDIT_MONTHS * pct * W.FEE_MONTH, f"{a}% at the {c.params['measured_at']} -> missed"
    return 0.0, ""


def base_costs():
    sustain_h = W.SUSTAIN_FTE * W.HOURS_PER_FTE_MONTH * (12 - W.LIVE_DAY / W.DAYS_PER_MONTH)
    pre_m = W.LIVE_DAY / W.DAYS_PER_MONTH
    return [
        CostLine("B1", f"FDE hours to go-live ({W.HOURS_TO_DAY_136:,} measured to day 136 + "
                       f"{W.HOURS_DAY_136_TO_LIVE} forecast)", (W.HOURS_TO_DAY_136 + W.HOURS_DAY_136_TO_LIVE)
                 * W.LOADED_RATE, "measured"),
        CostLine("B2", f"sustain 0.5 FTE after go-live ({sustain_h:,.0f} h)", sustain_h * W.LOADED_RATE, "estimated"),
        CostLine("B3", "run cost ($3,000 a month before go-live, $9,000 after)", 3000 * pre_m + 9000 * (12 - pre_m),
                 "estimated"),
        CostLine("B4", "platform and support share, 10% of subscription", 160_000, "estimated"),
    ]


REVENUE = {"subscription from signature": 1_600_000, "deployment fee, fixed price": 200_000}


def price(version="v3", honest=True, naive=False, show=True):
    clauses = W.CALDWELL_V3 if version == "v3" else W.CALDWELL_V5
    book = W.V3_COSTS if version == "v3" else W.V5_COSTS
    cs, cust, none = extract(clauses)
    lint(cs, dependencies=W.CALDWELL_DEPS, decisions=W.CALDWELL_DECISIONS, naive=naive)
    lines = []
    for c in cs:
        if c.kind == "service level" and c.metric in ("accuracy", "availability"):
            amt, why = credits(c, honest, version)
            lines.append((c, CostLine(c.cid, f"credits: {why}", amt, "computed")))
        elif c.cid in book:
            lines.append((c, book[c.cid]))
        else:
            lines.append((c, CostLine(c.cid, "UNPRICED", 0, "none")))
    return cs, cust, none, lines


def margin(lines):
    rev = sum(REVENUE.values())
    cost = sum(l.amount for l in base_costs()) + sum(l.amount for _, l in lines)
    return (rev - cost) / rev, rev, cost


def show_commitments(cs, cust, none, title):
    print(f"CONTRACT-COMMITMENT EXTRACTOR  {title}")
    print(f"  clauses {len(cs) + len(cust) + len(none)}  vendor commitments {len(cs)}  customer obligations "
          f"{len(cust)}  no obligation {len(none)}")
    kinds = Counter(c.kind for c in cs)
    print("  by kind: " + ", ".join(f"{k} {n}" for k, n in sorted(kinds.items(), key=lambda x: (-x[1], x[0]))))


def run(stage):
    if stage == "v0":
        cs, cust, none, lines = price("v3", honest=False, naive=True)
        show_commitments(cs, cust, none, W.V3)
        print("\nv0 PRICING (day 137): any number in a service level counts as a measure")
        for c, l in lines:
            print(f"  {c.cid:8} {c.kind:13} ${l.amount:>9,.0f}  {l.basis:9} {l.label}")
        m, rev, cost = margin(lines)
        print(f"  findings: {sum(len(c.findings) for c in cs)}")
        print(f"  year-one revenue ${rev:,.0f}  cost ${cost:,.0f}  gross margin {m:.1%}   (floor 40%, target 60%)")
    elif stage == "check":
        cs, cust, none, lines = price("v3", honest=True)
        print("MEASURABILITY AND CONTROL CHECK (day 138)  " + W.V3)
        n = 0
        for c in cs:
            for kind, why in c.findings:
                n += 1
                print(f"  {c.cid:8} {kind:19} {why}")
        print(f"  {n} findings on {sum(1 for c in cs if c.findings)} of {len(cs)} commitments")
        print("\nPRICED HONESTLY: an unmeasurable service level is priced at the reading the other party controls")
        for c, l in lines:
            if c.kind == "service level" and l.amount:
                print(f"  {c.cid:8} ${l.amount:>9,.0f}  {l.label}")
        base = sum(l.amount for l in base_costs())
        adds = sum(l.amount for _, l in lines)
        m, rev, cost = margin(lines)
        print(f"  base cost before the addendum ${base:,.0f} -> margin {(rev - base) / rev:.1%}")
        print(f"  addendum commitments          ${adds:,.0f}")
        print(f"  year-one revenue ${rev:,.0f}  cost ${cost:,.0f}  gross margin {m:.1%}   (forecast)")
    elif stage == "v5":
        cs, cust, none, lines = price("v5", honest=True)
        show_commitments(cs, cust, none, W.V5)
        n = sum(len(c.findings) for c in cs)
        print(f"  findings: {n}")
        for c, l in lines:
            print(f"  {c.cid:8} {c.kind:13} ${l.amount:>9,.0f}  {l.basis:9} {l.label}")
        m, rev, cost = margin(lines)
        print(f"  year-one revenue ${rev:,.0f}  cost ${cost:,.0f}  gross margin {m:.1%}   (forecast)")


if __name__ == "__main__":
    run(sys.argv[1] if len(sys.argv) > 1 else "v0")
