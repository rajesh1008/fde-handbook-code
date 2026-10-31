"""Figure 44.8: solo ownership and pods, the two staffing structures compared at month 12."""
from _common import S, save, blank
fig, ax = S.figure(height=4.4); blank(ax, (0, 10), (0, 6.6))
S.label(ax, 2.3, 6.25, "solo: one owner per customer", fs=10)
S.label(ax, 7.4, 6.25, "pods: shared context", fs=10)
for i, c in enumerate(["Caldwell", "Greystone", "Pennant", "Harbourline"]):
    y = 5.0 - i * 1.25
    S.box(ax, 0.2, y, 1.9, 0.75, c, role="data", fs=9)
    S.box(ax, 2.6, y, 1.9, 0.75, "one FDE", role="model", fs=9)
    S.arrow(ax, 2.1, y + 0.37, 2.6, y + 0.37, weight="control")
S.box(ax, 0.2, 0.0, 4.3, 0.6, "two floaters", role="evidence", fs=9)
for k, (pod, cs) in enumerate((("pod A, three FDEs", ["Caldwell", "Greystone"]), ("pod B, three FDEs", ["Pennant", "Harbourline"]))):
    y0 = 3.4 - k * 2.6
    S.box(ax, 5.4, y0, 2.0, 2.0, pod, role="system", fs=9)
    for j, c in enumerate(cs):
        S.box(ax, 8.0, y0 + 1.1 - j * 1.0, 1.9, 0.75, c, role="data", fs=9)
        S.arrow(ax, 7.4, y0 + 1.0, 8.0, y0 + 1.45 - j * 1.0, weight="control")
S.box(ax, 5.4, 2.65, 4.5, 0.55, "shared evaluation lead", role="approval", fs=9)
save(fig, 8, kind="diagram", data="04-code/ch44/practice.py PLANS")
