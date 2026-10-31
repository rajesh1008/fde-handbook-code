"""Figure 9.16: the sponsor's slide and the redrawn slide, same promise, honest parts."""
from _common import S, save, blank
fig, ax = S.figure(4.0); blank(ax, (0, 10), (0, 6))
S.label(ax, 0.3, 5.5, "the slide as bought", fs=10, weight="bold"); S.label(ax, 5.4, 5.5, "the slide as built", fs=10, weight="bold")
S.box(ax, 0.3, 1.4, 4.0, 3.6, "one agent reads,\ndecides and files\nevery claim", role="cost", fs=10.5)
S.box(ax, 5.4, 4.0, 4.3, 1.0, "claims assistant", role="evidence", fs=10.5)
S.box(ax, 5.4, 2.7, 2.1, 1.0, "checks\n9 steps", role="system", fs=10)
S.box(ax, 7.6, 2.7, 2.1, 1.0, "models\n3 steps", role="model", fs=10)
S.box(ax, 5.4, 1.4, 4.3, 1.0, "adjuster decides", role="approval", fs=10.5)
S.arrow(ax, 4.4, 3.2, 5.3, 3.2)
save(fig, 16, kind="diagram")
