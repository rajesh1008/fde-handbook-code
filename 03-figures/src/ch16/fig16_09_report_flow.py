"""Figure 16.9: the representativeness report: three tests, one verdict, one permitted use."""
from _common import S, save, blank
fig, ax = S.figure(height=3.9)
blank(ax, (0, 10), (0, 6))
tests = ["feature PSI\nbelow 0.25", "exception\ncoverage", "classifier\nAUC below 0.75"]
for i, t in enumerate(tests):
    S.box(ax, 0.2, 4.4 - i * 1.6, 2.8, 1.2, t, role="evidence", fs=10)
    S.arrow(ax, 3.0, 5.0 - i * 1.6, 4.2, 3.4)
S.box(ax, 4.2, 2.8, 2.0, 1.2, "verdict", role="model", fs=11)
S.box(ax, 7.2, 4.0, 2.6, 1.2, "all pass:\nregression use", role="system", fs=10)
S.box(ax, 7.2, 1.4, 2.6, 1.2, "any fail:\nplumbing only", role="cost", fs=10)
S.arrow(ax, 6.2, 3.6, 7.2, 4.6); S.arrow(ax, 6.2, 3.2, 7.2, 2.0)
save(fig, 9, kind="diagram", data="04-code/fieldkit/fieldkit/synthetic.py")
