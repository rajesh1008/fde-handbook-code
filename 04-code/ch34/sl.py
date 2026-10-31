"""Listing 34.4/34.5: service levels for a probabilistic system, worked for all four customers."""
import _paths  # noqa: F401
from fieldkit.contract import design_service_level, point_rule, zero_tolerance_breach

ROWS = [  # customer, metric (bad event), scorer, acceptable, unacceptable, true rate now, source of 'now'
    ("Caldwell", "post-review document error", "Caldwell claims quality team", 0.010, 0.030, 0.009,
     "Ch27: 36 of 4,000"),
    ("Greystone", "draft needs material correction", "Greystone clinical reviewers", 0.150, 0.250, 0.120,
     "stand-in"),
    ("Pennant", "shipment not matched", "Pennant reconciliation team", 0.170, 0.250, 0.170, "canon: 83% matched"),
    ("Pennant", "silently wrong match", "Pennant reconciliation team", 0.002, 0.010, 0.0015, "stand-in"),
    ("Harbourline", "memo disagrees with reviewer", "bank credit reviewers", 0.100, 0.200, 0.090, "stand-in"),
]


def caldwell_design():
    r = ROWS[0]
    return design_service_level(r[0], r[1], r[2], r[3], r[4])


def main():
    print("ONE CLAUSE, THREE RULES  Caldwell post-review document error, true rate 0.9% (Ch27)")
    print("  rule                                   n    breach at   P(breach) at 0.9%  at 1.0%  at 3.0%")
    for label, s in [("point estimate above 1.0%", point_rule("c", "e", "s", 0.01, 0.03, 400, 0.010)),
                     ("point estimate above 2.0%", point_rule("c", "e", "s", 0.01, 0.03, 400, 0.020)),
                     ("designed: alpha 5%, power 80%", caldwell_design())]:
        print(f"  {label:36} {s.n:4}   {s.k:2} errors   {s.p_breach(0.009):17.1%}  {s.p_breach(0.010):7.1%}"
              f"  {s.p_breach(0.030):7.1%}")
    print("\nSAMPLE SIZE FOR THE CALDWELL DESIGN (alpha 5% at 1.0%, power at 3.0%)")
    for n in (100, 200, 310, 400, 800):
        s = design_service_level("c", "e", "s", 0.01, 0.03, n_min=n, n_max=n, step=1) or None
        if s:
            print(f"  n {n:4}  breach at {s.k:2}  power {s.p_breach(0.03):.1%}")
        else:
            from fieldkit.contract import binom_sf
            k = 1
            while binom_sf(k, n, 0.01) > 0.05:
                k += 1
            print(f"  n {n:4}  breach at {k:2}  power {binom_sf(k, n, 0.03):.1%}  (below 80%)")
    print("\nSERVICE LEVELS DESIGNED FOR ALL FOUR CUSTOMERS (alpha 5%, power 80%)")
    print("  customer     bad event                        acceptable  unacceptable  n     breach at   now    "
          "P(breach) now  expected breach months / 12")
    for c, m, sc, a, u, now, src in ROWS:
        s = design_service_level(c, m, sc, a, u)
        p = s.p_breach(now)
        print(f"  {c:12} {m:32} {a:9.1%}  {u:11.1%}   {s.n:4}  {s.k:3} ({s.threshold_pct:4.1f}%)  {now:5.2%}  "
              f"{p:12.1%}   {12 * p:5.2f}   [{src}]")
    print(f"  scorers: " + "; ".join(f"{r[0]}: {r[2]}" for r in ROWS))
    print("\nZERO-TOLERANCE CLAUSE  'no red flag is ever missed' (Greystone, stand-in rates)")
    for miss, k in [(0.01, 60), (0.005, 60), (0.001, 60)]:
        print(f"  per-flag miss {miss:.1%}, {k} red-flag referrals a month -> P(breach in a month) "
              f"{zero_tolerance_breach(miss, k):.1%}, in a year {1 - (1 - zero_tolerance_breach(miss, k)) ** 12:.1%}")


def reporting_and_remedies():
    """How to report one month, and what a chronic-breach remedy does (Caldwell design, n 310, k 7)."""
    from math import comb
    from fieldkit.contract import binom_sf, wilson_upper
    sl = caldwell_design()
    print()
    print("REPORTING ONE MONTH  (Caldwell, 310 documents; 95% upper bound, Wilson)")
    for k in (3, 6, 7, 9):
        verdict = "breach" if k >= sl.k else "no breach"
        print(f"  {k} errors in 310: sampled {k / 310:.2%}, upper bound {wilson_upper(k, 310):.2%}  -> {verdict}")
    print()
    print("REMEDIES ON A SAMPLED MEASURE  (chronic breach = 3 or more breach months in any 6)")

    def at_least(m, n, p):
        return sum(comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(m, n + 1))
    for rate in (0.009, 0.010, 0.020, 0.030):
        pm = binom_sf(sl.k, sl.n, rate)
        print(f"  true error {rate:.1%}: breach month {pm:5.1%}  any breach in 12 months {1 - (1 - pm) ** 12:5.1%}"
              f"  chronic in a 6-month window {at_least(3, 6, pm):5.1%}")


if __name__ == "__main__":
    main()
    reporting_and_remedies()
