"""Figure 47.9: the failure injection: a playbook that passes the form lint fails at N17, which has no gateway."""
from _common import S, save, blank
fig, ax = S.figure(height=4.4); blank(ax, (0, 10), (0, 7))
S.box(ax, 0.2, 4.6, 2.6, 1.6, "PB-1@1.3\nform lint: pass", role="data", fs=10)
S.box(ax, 3.7, 4.6, 2.6, 1.6, "N17: no\nmodel gateway", role="evidence", fs=10)
S.box(ax, 7.2, 4.6, 2.6, 1.6, "day 23: step S4\nfails", role="blocker", fs=10)
S.box(ax, 0.2, 0.6, 2.6, 1.6, "PB-1@1.4\ndeclares gateway", role="data", fs=10)
S.box(ax, 3.7, 0.6, 2.6, 1.6, "day 0: match\nblocked", role="approval", fs=10)
S.box(ax, 7.2, 0.6, 2.6, 1.6, "PB-4 first,\nthen PB-1", role="system", fs=10)
S.arrow(ax, 2.8, 5.4, 3.7, 5.4); S.arrow(ax, 6.3, 5.4, 7.2, 5.4)
S.arrow(ax, 2.8, 1.4, 3.7, 1.4); S.arrow(ax, 6.3, 1.4, 7.2, 1.4, weight="emphasis")
S.arrow(ax, 1.5, 4.6, 1.5, 2.2, ls="--"); S.label(ax, 1.7, 3.3, "probe P5", fs=9)
save(fig, 9, kind="diagram", data="04-code/ch47/output/registry_n17.txt, registry_probe.txt, registry_match.txt")
