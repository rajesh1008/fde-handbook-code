"""Signature 17, the margin waterfall. Caldwell year one, from revenue to gross margin,
with the integration tax itemized by its six sources. Days 191 to 365 are forecast and labeled."""
import _paths  # noqa: F401
from fieldkit.contract import CostLine, year_one_margin, renewal_weighted_two_year
from world import ACTUAL, CALDWELL_SOURCES, RATE, FTE_MONTH, SUPPORT, CONTRACT
from phases import run_cost

ACV = CONTRACT["caldwell"]["acv"]; FEE = CONTRACT["caldwell"]["fee"]


def lines():
    a = ACTUAL["caldwell"]
    out = [CostLine(b, b, a[b] * RATE, "measured") for b in ("discovery", "access", "model", "gates", "handover", "blocked")]
    out += [CostLine("tax:" + s, "integration: " + s, h * RATE, "measured") for s, h in CALDWELL_SOURCES.items()]
    sustain_h = round(0.5 * FTE_MONTH * (365 - 190) * 12 / 365)
    out += [CostLine("sustain", "sustain 0.5 FTE, days 191 to 365", sustain_h * RATE, "forecast"),
            CostLine("run", "model and hosting", run_cost("caldwell", 1, 365), "measured, then forecast"),
            CostLine("support", "product support and platform", SUPPORT * ACV, "allocated"),
            CostLine("commitments", "contract v5 commitments", 142_000, "forecast at day 149")]
    return out


def main():
    rev = {"subscription": ACV, "services fee": FEE}
    L = lines()
    assert sum(CALDWELL_SOURCES.values()) == ACTUAL["caldwell"]["integration"]
    m, R, C = year_one_margin(rev, L)
    print(f"Caldwell year one, US dollars (deterministic stand-in; days 191 to 365 forecast)")
    print(f"  {'revenue':<35} ${R:>11,.0f}")
    run = R
    for c in L:
        run -= c.amount
        print(f"  - {c.label:<33} ${c.amount:>9,.0f} -> ${run:>11,.0f}  {c.basis}")
    print(f"  {'gross profit':<35} ${R - C:>11,.0f}")
    print(f"  year-one gross margin {m:.1%}   \n  (target 60%, floor 40%; v5 forecast 48.7%; Chapter 2 field estimate 62.4%)")
    tax_cost = sum(c.amount for c in L if c.key.startswith("tax:"))
    print(f"  integration tax itemized: {tax_cost / R:.1%} of revenue; formats + exceptions = "
          f"{(CALDWELL_SOURCES['formats'] + CALDWELL_SOURCES['exceptions']) / ACTUAL['caldwell']['integration']:.0%} of it")
    gp2 = ACV - (0.5 * FTE_MONTH * 12 * RATE) - 9000 * 12 - SUPPORT * ACV - 120_000
    two = renewal_weighted_two_year(R - C, gp2, 0.80)
    print(f"  two-year renewal-weighted gross profit (live month 5.2, renewal 80%): ${two:,.0f}  [forecast]")
    return m


if __name__ == "__main__":
    main()
