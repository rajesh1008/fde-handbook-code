"""Figure 35.7: the drawn map (5 hops) against the map generated from deployed configuration (14 hops)."""
from _common import S, save, blank, text
t = text("datamap_v1")
rows = [l.split()[0] for l in t.splitlines() if l.startswith("  ") and ("ok" in l.split()[-1] or "FLAG" in l)]
flag = {l.split()[0] for l in t.splitlines() if " FLAG " in l}
drawn = {"referral-intake", "drafting-service", "model-endpoint", "coordinator-queue", "run-records"}
assert len(rows) == 14 and len(flag) == 3
fig, ax = S.figure(height=5.6); blank(ax, (0, 10), (0, 8))
for i, name in enumerate(rows):
    col, r = divmod(i, 7)
    role = "blocker" if name in flag else ("evidence" if name in drawn else "data")
    S.box(ax, 0.3 + col * 5.0, 6.9 - r * 1.05, 4.4, 0.85, name, role=role, fs=9.5)
S.label(ax, 0.3, 7.85, "slate: on the drawing   amber: generated only   coral: flagged", fs=9.5)
save(fig, 7, kind="diagram", data="04-code/ch35/output/datamap_v1.txt")
