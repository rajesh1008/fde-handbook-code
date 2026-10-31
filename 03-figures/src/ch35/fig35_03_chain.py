"""Figure 35.3: Greystone's business associate chain, and the two hops that sat outside it on day 122."""
from _common import S, save, blank
fig, ax = S.figure(height=4.9); blank(ax, (0, 10), (0, 8))
S.box(ax, 0.2, 5.8, 3.0, 1.6, "Greystone\ncovered entity", role="model", fs=10)
S.box(ax, 3.6, 5.8, 3.0, 1.6, "Northlight\nBAA GA-02", role="system", fs=10)
S.box(ax, 7.0, 5.8, 2.8, 1.6, "model provider\nsubcontractor BAA", role="system", fs=9.5)
S.arrow(ax, 3.2, 6.6, 3.6, 6.6); S.arrow(ax, 6.6, 6.6, 7.0, 6.6)
S.box(ax, 7.0, 3.3, 2.8, 1.6, "abuse monitoring\nExhibit C", role="approval", fs=9.5)
S.box(ax, 7.0, 0.6, 2.8, 1.6, "stored requests\nno basis", role="blocker", fs=9.5)
S.box(ax, 3.6, 3.3, 3.0, 1.6, "trace vendor\nno BAA", role="blocker", fs=9.5)
S.box(ax, 0.2, 3.3, 3.0, 1.6, "gateway bodies\nunsigned log", role="blocker", fs=9.5)
S.arrow(ax, 8.4, 5.8, 8.4, 4.9); S.arrow(ax, 9.5, 5.8, 9.5, 2.2)
S.arrow(ax, 5.1, 5.8, 5.1, 4.9); S.arrow(ax, 1.7, 5.8, 1.7, 4.9)
save(fig, 3, kind="diagram", data="04-code/ch35/output/datamap_v1.txt")
