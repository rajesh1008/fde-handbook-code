"""Figure 18.3: Caldwell's golden path, read as six questions, with the owner who answers each."""
from _common import S, save, blank
fig, ax = S.figure(height=3.9)
blank(ax, (0, 10), (0, 6))
steps = [("runtime", "team account", "system"), ("identity", "role per\nworkload", "approval"),
         ("secrets", "read at call", "data"), ("model calls", "gateway only", "blocker"),
         ("evaluation", "their stack", "evidence"), ("logs", "audit store", "evidence")]
for i, (s, ans, role) in enumerate(steps):
    x = 0.1 + i * 1.65
    S.box(ax, x, 2.6, 1.45, 1.3, s, role=role, fs=10)
    S.label(ax, x + 0.72, 2.45, ans, fs=10, ha="center", va="top")
    if i < 5:
        S.arrow(ax, x + 1.45, 3.25, x + 1.65, 3.25)
S.label(ax, 0.1, 4.6, "the paved road: each step has an owner", fs=10)
S.label(ax, 0.1, 0.5, "off the road: an exception and a review slot", fs=10, color=S.PAL["slate"])
save(fig, 3, kind="diagram", data="chapter text (Section 18.2)")
