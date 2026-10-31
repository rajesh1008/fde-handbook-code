"""Listing 31.4: the whole-agent shadow run, days 142 to 153 (deterministic stand-in; agreement is with what clerks
keyed, not accuracy)."""
import _paths  # noqa: F401
from collections import Counter
from fieldkit.routing import wilson
from world import shadow, SHADOW_DAYS, AUDIT, FIX_DAY, u, pick

docs = shadow()
print("day  docs  agree  share   rotated  template")
for d in SHADOW_DAYS:
    x = [y for y in docs if y["day"] == d]
    a = sum(y["agree"] for y in x)
    print(f"{d:<5}{len(x):<6}{a:<7}{a / len(x):6.1%}   {sum(y['rotated'] for y in x):<9}"
          f"{sum(y['cause'].startswith('broker') for y in x)}")
n, a = len(docs), sum(y["agree"] for y in docs)
lo, hi = wilson(a, n)
print(f"total {n} documents, {a} agree on all six fields: {a / n:.1%} (95% interval {lo:.1%} to {hi:.1%})")
print("\ndisagreements by cause (adjudicated by Lena Ortiz, days 154 and 155)")
for k, v in Counter(y["cause"] for y in docs if not y["agree"]).most_common():
    print(f"  {k:<36}{v}")
routed = [y for y in docs if not y["band"].startswith("none")]
b = Counter(y["band"] for y in routed)
print(f"\nrouted {len(routed)} of {n} (13 typed none before day {FIX_DAY}): " +
      ", ".join(f"{k} {b[k]} ({b[k] / len(routed):.1%})" for k in ("proceed", "review", "escalate")))
print("\naudit-shadow-400: field values after review vs Lena Ortiz's adjudicated values")
tot_e = tot_f = 0
band_err = Counter()
for period, days in (("pre", [d for d in SHADOW_DAYS if d < FIX_DAY]), ("post", [d for d in SHADOW_DAYS if d >= FIX_DAY])):
    ndoc, nerr = AUDIT[period]
    pool = pick([y["id"] for y in routed if y["day"] in days], ndoc, "audit")
    fields = [(i, f) for i in pool for f in range(10)]
    errs = pick(fields, nerr, "err")
    bands = {y["id"]: y["band"] for y in routed}
    band_err.update(bands[i] for i, _ in errs)
    lo, hi = wilson(nerr, len(fields))
    label = "days 142 to 149" if period == "pre" else "days 150 to 153"
    print(f"  {label}: {ndoc} documents, {len(fields)} fields, {nerr} wrong: {nerr / len(fields):.2%} ({lo:.2%} to {hi:.2%})")
    tot_e += nerr; tot_f += len(fields)
lo, hi = wilson(tot_e, tot_f)
print(f"  all: {tot_e} of {tot_f}: {tot_e / tot_f:.2%} (95% interval {lo:.2%} to {hi:.2%})")
print("  errors by band: " + ", ".join(f"{k} {band_err[k]}" for k in ("proceed", "review", "escalate")))
print("  Chapter 27 audit-400 (days 136 to 139): routing 0.9%, review-everything 1.1%")
