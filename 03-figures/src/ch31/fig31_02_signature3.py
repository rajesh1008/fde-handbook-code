"""Figure 31.2: Signature 3 for the pilot build rc-1 (tree.txt)."""
from _common import S, save, text, nums
import signature3 as sig
line = [l for l in text("tree").splitlines() if l.startswith("split:")][0]
c = [int(x) for x in nums(line.split("|")[0])]
fig, ax = S.figure(4.4)
sig.draw(ax, c, f"rc-1: {c[0] + c[1]} of {sum(c)} steps\nneed no model")
save(fig, 2, kind="diagram", data="04-code/ch31/output/tree.txt")
