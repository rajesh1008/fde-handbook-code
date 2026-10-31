"""Figure 11.1: the Greystone kickoff map (day 2) in the Signature 4 layout: no operator, no champion."""
from _common import S, save
import signature4 as sig
import greystone as G
cols, ch = sig.from_map(G.KICKOFF)
fig, ax = S.figure(3.8)
sig.draw(ax, cols, ch, emphasis={"nobody:operator"})
save(fig, 1, kind="diagram")
