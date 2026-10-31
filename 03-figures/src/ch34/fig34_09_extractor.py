"""Figure 34.9: the contract-commitment extractor: clause to commitment to checks to a priced line."""
from _common import S, save, blank
fig, ax = S.figure(height=4.9); blank(ax, (0, 10), (0, 8))
steps = [("clause text", "data"), ("vendor\ncommitments", "model"), ("measurable?\ncontrolled?", "evidence"),
         ("priced line\nwith a basis", "cost"), ("margin beside\nrenewal GP", "approval")]
for i, (t, r) in enumerate(steps):
    S.box(ax, 0.05 + i * 2.0, 4.6, 1.75, 1.7, t, role=r, fs=9.5)
    if i:
        S.arrow(ax, i * 2.0 - 0.2, 5.45, i * 2.0 + 0.05, 5.45)
S.box(ax, 3.6, 1.2, 3.2, 1.7, "findings go to\nthe commercial lead", role="blocker", fs=9.5)
S.arrow(ax, 4.9, 4.6, 5.2, 2.9)
save(fig, 9, kind="diagram", data="fieldkit/contract.py; 04-code/ch34/extract.py")
