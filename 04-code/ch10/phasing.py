"""Listing 10.6: when the tax exceeds the model work. Pennant's 41 layouts by monthly volume (seeded stand-in,
about 9,100 documents and messages a month), and three options for phase one."""
import _path  # noqa: F401
from inventories import pennant, PENNANT_KINDS

MONTHLY = 9100
layouts = []                      # (rank, kind, likely hours); volume falls with rank (Zipf, s = 1.1)
for kind, n, lo, li, hi in PENNANT_KINDS:
    layouts += [(kind, li)] * n
w = [1 / (r ** 1.1) for r in range(1, len(layouts) + 1)]
vol = [MONTHLY * x / sum(w) for x in w]
inv = pennant(); total = inv.total(); model = inv.model_hours[1]
fmt = sum(h for _, h in layouts); rest = total - fmt

def option(name, keep, reuse=0.0, queue_h=0):
    h = sum(layouts[i][1] for i in range(keep)) + rest + queue_h
    cov = sum(vol[:keep]) / MONTHLY
    print(f"{name:<40}{keep:>8}{cov:>9.0%}{h:>9,.0f}{h / model:>6.2f}{h * (1 - reuse) / model:>17.2f}")

print(f"{'option':<40}{'layouts':>8}{'volume':>9}{'hours':>9}{'tax':>6}{'engagement tax*':>17}")
option("A  all 41 layouts in phase one", 41)
option("B  top 12 by volume, rest to a queue", 12, queue_h=40)
option("C  B, carrier connectors as product", 12, reuse=0.35, queue_h=40)
print("* option C: 35% of integration hours funded by Northlight's product budget as reusable connectors")
top = sum(vol[:12]) / MONTHLY
print(f"top 12 layouts carry {top:.0%} of monthly volume; the other 29 carry {1 - top:.0%} ({MONTHLY * (1 - top):,.0f} a month)")
