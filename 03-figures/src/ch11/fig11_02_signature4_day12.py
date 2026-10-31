"""Figure 11.2: Signature 4, the sponsor map, Greystone day 12. Emphasis on what changed since the kickoff."""
from _common import S, save
import signature4 as sig
import greystone as G
cols, ch = sig.from_map(G.DAY12)
fig, ax = S.figure(3.8)
sig.draw(ax, cols, ch, emphasis={"Alvarez", "Monroe", "Ortega", "Shah"})
save(fig, 2, kind="diagram")
