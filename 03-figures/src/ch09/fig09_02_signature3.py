"""Figure 9.2: Signature 3, the autonomy decision tree, with the steps of all three customers (52)."""
from _common import S, save
import signature3 as sig
from fieldkit.autonomy import split, CLASSES
import pipelines as pl
sp = split(pl.CALDWELL + pl.GREYSTONE + pl.PENNANT)
c = [sp[k] for k in CLASSES]
fig, ax = S.figure(4.4)
sig.draw(ax, c, f"{c[0] + c[1]} of {sum(c)} = {(c[0] + c[1]) / sum(c):.0%}\nneed no model")
save(fig, 2, kind="diagram")
