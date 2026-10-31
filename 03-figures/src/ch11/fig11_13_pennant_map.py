"""Figure 11.13: Signature 4 at Pennant, day 28. One person in four columns; no champion."""
from _common import S, save
import signature4 as sig
import pennant
cols, ch = sig.from_map(pennant.DAY28, short=lambda p: {"ruiz": "Ruiz", "clerks": "clerks (14)", "compliance": "compliance"}[p.key])
fig, ax = S.figure(3.8)
sig.draw(ax, cols, ch, emphasis={"Ruiz", "nobody:champion"})
save(fig, 13, kind="diagram")
