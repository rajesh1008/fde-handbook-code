"""Figure 34.2: what each reviewer on the customer side needs from engineering, and the artifact that answers it."""
from _common import S, save, blank
fig, ax = S.figure(height=4.9); blank(ax, (0, 10), (0, 8))
ask = [("procurement", "what are we buying?"), ("legal", "what are we promising?"),
       ("security and privacy", "where does the data go?"), ("finance", "what does it cost?")]
art = [("commitments register", "evidence"), ("service-level exhibit", "approval"),
       ("data map", "data"), ("hours and run-cost estimate", "cost")]
for i, ((who, q), (a, r)) in enumerate(zip(ask, art)):
    y = 6.2 - i * 1.95
    S.box(ax, 0.2, y, 3.9, 1.45, f"{who}\n{q}", role="model", fs=9.5)
    S.box(ax, 5.9, y, 3.9, 1.45, a, role=r, fs=10)
    S.arrow(ax, 4.1, y + 0.72, 5.9, y + 0.72)
S.label(ax, 5.0, 7.8, "one artifact each, owned by the FDE", fs=9.5)
save(fig, 2, kind="diagram", data="04-code/ch34 (extract.py, sl.py, dataterms.py, pricing.py)")
