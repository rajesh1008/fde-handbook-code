"""Listing 24.2: score four surface options on ten weighted dimensions, then try to break the answer."""
import _paths  # noqa: F401
from fieldkit.surface import Option, total, contributions, rank, lead, flip_point, sensitivity, weight_draws
from caldwell import DIMS, WEIGHTS, OPTIONS, GROUP_ADOPTION, TIME_IN_TOOL

print("Caldwell surface decision, day 110 weights (sum %d)" % sum(WEIGHTS.values()))
for d in DIMS:
    print(f"  {d:<28} w={WEIGHTS[d]:>2}  scores " + " ".join(f"{o.key}{o.scores[d]}" for o in OPTIONS))
print("\ntotals (0-100):")
for k, t in rank(OPTIONS, WEIGHTS):
    name = next(o.name for o in OPTIONS if o.key == k)
    print(f"  {k} {t:5.1f}  {name}")
gap, runner = lead(OPTIONS, WEIGHTS, "C")
print(f"lead of C over best other ({runner}): {gap:.1f} points")
print("\ncontributions to C and A (points):")
cc, ca = contributions(OPTIONS[2], WEIGHTS), contributions(OPTIONS[0], WEIGHTS)
for d in DIMS:
    print(f"  {d:<28} C {cc[d]:5.1f}  A {ca[d]:5.1f}  diff {cc[d] - ca[d]:+5.1f}")

print("\nsensitivity: lead of C when one weight is halved / raised by half")
for d, ((g1, r1), (g2, r2)) in sensitivity(OPTIONS, WEIGHTS, "C").items():
    print(f"  {d:<28} x0.5 {g1:+5.1f} (vs {r1})  x1.5 {g2:+5.1f} (vs {r2})")
print("\nflip points (multiplier on one weight at which C stops winning; others fixed):")
for d in DIMS:
    down, up = flip_point(OPTIONS, WEIGHTS, d, "C")
    if down or up:
        w = WEIGHTS[d]
        print(f"  {d:<28} " + (f"down at x{down:.2f} (weight {w*down:.1f})  " if down else "") +
              (f"up at x{up:.2f} (weight {w*up:.1f})" if up else ""))
print("  every other dimension: no flip between x0 and x4")

wins = weight_draws(OPTIONS, WEIGHTS, n=2000, concentration=60, seed=24)
print("\nweight draws (2,000 Dirichlet draws around the agreed weights, concentration 60):")
for o in OPTIONS:
    print(f"  {o.key} wins {wins[o.key]:>4} ({100*wins[o.key]/2000:.1f}%)")

print("\nper user group (adoption rescored from the day-104 time-in-tool sample):")
for g, adopt in GROUP_ADOPTION.items():
    opts = [Option(o.key, o.name, dict(o.scores, adoption=a)) for o, a in zip(OPTIONS, adopt)]
    r = rank(opts, WEIGHTS)
    print(f"  {g:<14} " + "  ".join(f"{k} {t:.1f}" for k, t in r) + f"   winner {r[0][0]}")
print("\ntime in tool, share of logged minutes (day 104):")
for g, m in TIME_IN_TOOL.items():
    suite = sum(v for k, v in m.items() if k.startswith("suite"))
    print(f"  {g:<14} suite {suite}%: " + "; ".join(f"{k} {v}%" for k, v in m.items()))
