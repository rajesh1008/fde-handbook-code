"""Per-class table behind the Shadow Exit decision: p7 and rc-1 by stratum, rc-1 interval, verdict at 80%."""
import _paths  # noqa: F401
from fieldkit.gates import wilson, judge, Measurement
import world

print(f"{'stratum':22} {'docs':>4} {'p7 d94':>7} {'rc-1 d156':>9} {'95% interval':>16}  verdict at 80%")
for c, (d, k) in world.STRATA.items():
    lo, hi = wilson(k, d * 10)
    v = judge(world.S1, Measurement("S-1", k, d * 10, scope=c)).verdict
    print(f"{c:22} {d:>4} {world.P7[c]:>6.1f}% {k / (d * 10):>8.1%} {lo:>7.1%} to {hi:.1%}  {v}")
lo, hi = wilson(1689, 2010)
print(f"{'all fields':22} {201:>4} {76.7:>6.1f}% {1689 / 2010:>8.1%} {lo:>7.1%} to {hi:.1%}  met")
print("classes never at the bar in any scored release: first notice, fax (62.8% p7, 74.4% rc-1)")
