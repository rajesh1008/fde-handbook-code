"""Figure 50.13: Signature 14, Harbourline's shadow funnel, days 120 to 149."""
from _common import S, save, js
import signature14 as G
f = js("funnel.json"); rows = G.caldwell(f)
assert f["seen"] == 638 and f["agree"] == 546
fig, ax = S.figure(height=4.4); G.draw(ax, rows, f["seen"], unit="packages"); G.legend(ax, rows)
save(fig, 13, data="04-code/ch50/output/funnel.json")
