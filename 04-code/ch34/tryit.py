"""Try It Yourself, Chapter 34. a: write the Caldwell accuracy level as a point rule; b: run the extractor on
Harbourline's Schedule A; c: Pennant fixed versus T&M with a cap."""
import sys
import _paths  # noqa: F401
from fieldkit.contract import point_rule, design_service_level, extract, lint
import world as W


def a():
    for n, thr in [(400, 0.010), (400, 0.0125), (1000, 0.010)]:
        s = point_rule("Caldwell", "post-review document error", "claims quality", 0.01, 0.03, n, thr)
        p = s.p_breach(0.009)
        print(f"a. point rule n {n:4} breach above {thr:.2%}: P(breach) at 0.9% {p:.1%} a month, "
              f"expected credits ${p * 7 * 0.05 * W.FEE_MONTH:,.0f} at 5%")
    d = design_service_level("Caldwell", "e", "s", 0.01, 0.03)
    print(f"a. designed rule n {d.n} breach at {d.k}: P(breach) at 0.9% {d.p_breach(0.009):.1%}")


def b():
    cs, cust, none = extract(W.HARBOURLINE_SCHEDULE_A)
    lint(cs, dependencies=W.HARBOURLINE_DEPS)
    print(f"b. Schedule A excerpt: {len(W.HARBOURLINE_SCHEDULE_A)} sentences, {len(cs)} commitments, "
          f"{len(none)} marketing (no obligation)")
    for c in cs:
        f = "; ".join(f"{k}: {w}" for k, w in c.findings) or "clean"
        print(f"   {c.cid:7} {c.kind:13} {f}")


def c():
    from pricing import CUST, draws, q
    from fieldkit.contract import services_net
    h = draws(CUST["Pennant"])
    for label, kw in [("fixed $120,000", dict(billing="fixed", fee=120_000)),
                      ("T&M $260, cap $450,000", dict(billing="tm", bill_rate=260, cap=450_000)),
                      ("T&M $260, cap $300,000", dict(billing="tm", bill_rate=260, cap=300_000))]:
        b_ = kw.pop("billing")
        print(f"c. Pennant {label:24} net P50 ${services_net(q(h, .5), 150, b_, **kw):>10,.0f}  "
              f"P90 ${services_net(q(h, .9), 150, b_, **kw):>10,.0f}")


if __name__ == "__main__":
    {"a": a, "b": b, "c": c}[sys.argv[1]]()
