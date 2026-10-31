"""Figure 42.9: the eight Live Stable criteria, review on day 60 as handed over (v0) and on day 90 (v1)."""
from _common import S, save, text, blank
st = {m: [l.startswith("met") for l in text(f"livestable_{m}").splitlines() if l[:4] in ("met ", "OPEN")] for m in ("v0", "v1")}
names = ["no open Sev-1", "match and silent", "monitor read", "drill alone", "model change", "deputies", "readiness", "gold set"]
fig, ax = S.figure(height=4.6); blank(ax, (0, 10), (0, 9.6))
ax.text(5.1, 9.0, "day 60", ha="center", fontsize=10, weight="bold"); ax.text(7.9, 9.0, "day 90", ha="center", fontsize=10, weight="bold")
for i, n in enumerate(names):
    y = 7.8 - i * 1.0
    ax.text(3.8, y + 0.4, n, ha="right", va="center", fontsize=9.5)
    for j, m in enumerate(("v0", "v1")):
        ok = st[m][i]
        S.box(ax, 4.2 + j * 2.8, y, 1.8, 0.8, "met" if ok else "open", role="approval" if ok else "blocker", fs=9.5)
save(fig, 9, kind="diagram", data="04-code/ch42/output/livestable_v0.txt, livestable_v1.txt")
