"""Figure 18.2: the four jobs a gateway does for the customer and what each one costs the FDE."""
from _common import S, save, blank
fig, ax = S.figure(height=3.9)
blank(ax, (0, 10), (0, 6))
jobs = [("policy", "who calls what", "approval"), ("cost", "quota, chargeback", "cost"),
        ("audit", "their log", "evidence"), ("safety filters", "inputs refused", "blocker")]
costs = ["rotating key", "429s", "logs not yours", "filtered 400s"]
for i, ((j, what, role), c) in enumerate(zip(jobs, costs)):
    x = 0.1 + i * 2.5
    S.box(ax, x, 3.2, 2.2, 1.3, j, role=role, fs=11)
    S.label(ax, x + 1.1, 4.65, what, fs=10, ha="center", va="bottom")
    S.box(ax, x, 0.9, 2.2, 1.3, c, role="system", fs=10, ls="--")
    S.arrow(ax, x + 1.1, 3.2, x + 1.1, 2.2)
S.label(ax, 0.1, 0.2, "top: customer reason; bottom: what the FDE builds", fs=10, color=S.PAL["slate"])
save(fig, 2, kind="diagram", data="chapter text (Section 18.1)")
