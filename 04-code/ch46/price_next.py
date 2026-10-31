"""price the next engagement from the last three.

The next insurer (claims intake, the Caldwell playbook) is estimated bucket by bucket during discovery. Each
bucket is multiplied by its calibration factor from closed buckets; the integration line carries the 35%
reserve instead; the playbook credit is taken only for steps that pass the transfer check. The fixed fee is the
smallest multiple of $5,000 that meets the 60% year-one margin target at the priced hours.
"""
import math, sys
import _paths  # noqa: F401
from fieldkit.contract import CostLine, year_one_margin
from world import BUCKETS, RATE, FTE_MONTH, SUPPORT
from actuals import factors
from reserve import misses, reserve
from playbook import credit

ACV = 1_400_000; FTE = 2.5; TARGET = 0.60; FLOOR = 0.40; COMMIT = 50_000
REBUILD = 260   # PB-04 rebuilt on a nightly file export where the claims-core document API does not exist
ESTIMATE = dict(discovery=200, access=280, model=600, integration=560, gates=420, handover=240, blocked=175)


def priced_hours(mode="checked", res=None, use_factors=True):
    f = factors()
    r = reserve(misses()) if res is None else res
    out = {}
    for b in BUCKETS:
        c = credit("next insurer", mode, b)
        if b == "integration":
            out[b] = (ESTIMATE[b] - c) * (1 + r)
        else:
            out[b] = ESTIMATE[b] * (f[b][0] if use_factors else 1.0) - c
    return out, r


IDLE = 0.5      # share of a waiting engineer's month that still lands on the account (Chapter 2 blocked burn)


def year_one(hours, fee, overrun=0.0):
    """Integration overrun sits on the critical path: one engineer works it while the rest of the team waits."""
    H = sum(hours.values())
    months = (H - overrun) / (FTE * FTE_MONTH) + overrun / FTE_MONTH
    idle = overrun / FTE_MONTH * (FTE - 1) * FTE_MONTH * IDLE
    after = max(0.0, 12 - months)
    costs = [CostLine("fde", "FDE hours to production", (H + idle) * RATE, "priced"),
             CostLine("sustain", "sustain 0.5 FTE after production", 0.5 * FTE_MONTH * after * RATE, "priced"),
             CostLine("run", "model and hosting", 3000 * min(1.0, months) + 9000 * after, "priced"),
             CostLine("support", "product support and platform", SUPPORT * ACV, "allocated"),
             CostLine("commitments", "contract commitments", COMMIT, "assumed")]
    m, R, C = year_one_margin({"subscription": ACV, "fee": fee}, costs)
    return m, months, costs


def fee_for(hours, target=TARGET, overrun=0.0):
    """Smallest $5,000 step meeting the target; the reserve is priced as if used on the critical path."""
    fee = 0
    while year_one(hours, fee, overrun)[0] < target:
        fee += 5000
    return fee


def actual_hours(priced, r, miss, rebuild=0.0):
    """What the hours become if integration lands at `miss` x the credited P50 and a step that did not transfer is rebuilt."""
    h = dict(priced)
    base = priced["integration"] / (1 + r)
    h["integration"] = base * miss + rebuild
    return h, max(0.0, h["integration"] - base)


def main(mode="checked"):
    hours, r = priced_hours(mode)
    f = factors()
    print(f"next insurer, ACV ${ACV:,} (subscription from signature), FTE {FTE}, credit mode: {mode}")
    print(f"{'bucket':<12}{'estimate':>9}{'factor':>8}{'credit':>8}{'priced':>8}")
    for b in BUCKETS:
        fac = f"+{r:.0%}" if b == "integration" else f"{f[b][0]:.2f}"
        print(f"{b:<12}{ESTIMATE[b]:>9,.0f}{fac:>8}{credit('next insurer', mode, b):>8,}{hours[b]:>8,.0f}")
    H = sum(hours.values())
    print(f"{'total':<12}{sum(ESTIMATE.values()):>9,.0f}{'':>16}{H:>8,.0f}   cost ${H * RATE:,.0f}")
    reserve_h = hours["integration"] - hours["integration"] / (1 + r)
    print(f"reserve line: {reserve_h:,.0f} h = ${reserve_h * RATE:,.0f}")
    fee = fee_for(hours, overrun=reserve_h)
    m, months, _ = year_one(hours, fee, reserve_h)
    print(f"fixed fee ${fee:,} (services cost ${H * RATE:,.0f}; the subscription carries the rest)")
    print(f"forecast year-one margin at priced hours, reserve used {m:.1%}; production in month {months:.1f}")
    rebuild = REBUILD if mode == "naive" else 0.0
    for label, miss in (("integration on P50, reserve released", 1.00), ("worst miss so far (1.32)", 1.32),
                        ("reserve fully used (1.35)", 1.35), ("beyond the reserve (1.60)", 1.60)):
        ah, over = actual_hours(hours, r, miss, rebuild)
        mm, mo, _ = year_one(ah, fee, over)
        tag = "meets target" if mm >= TARGET else ("above floor" if mm >= FLOOR else "BELOW FLOOR")
        print(f"  {label:<40} margin {mm:6.1%}  month {mo:4.1f}  {tag}")
    if mode == "naive":
        print(f"  (PB-04 did not transfer: rebuilt on the nightly export, +{REBUILD} integration h)")
    return fee, m


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "checked")
