"""Figure 31.9: what the agent remembers within a claim, across claims and never (memory.txt)."""
from _common import S, save, blank
fig, ax = S.figure(height=4.2); blank(ax, (0, 10), (0, 6))
S.box(ax, 0.1, 3.0, 3.1, 2.6, "Within a claim\nfields, pointers,\ndraft, route\n90 days shadow\n30 days live", "system", fs=9)
S.box(ax, 3.45, 3.0, 3.1, 2.6, "Across claims\nnumbers only:\norientation, template,\nband counts", "data", fs=9)
S.box(ax, 6.8, 3.0, 3.1, 2.6, "Never\ntext, images,\nIDs, bank, medical", "blocker", fs=9)
S.box(ax, 0.1, 0.4, 6.45, 1.6, "Caldwell store and log;\nlegal hold stops deletion", "evidence", fs=9)
S.box(ax, 6.8, 0.4, 3.1, 1.6, "Memory release:\nnot granted", "approval", fs=9, lw=S.LW["emphasis"])
S.arrow(ax, 1.65, 3.0, 1.65, 2.0); S.arrow(ax, 5.0, 3.0, 5.0, 2.0)
save(fig, 9, kind="diagram", data="04-code/ch31/state.py, output/memory.txt")
