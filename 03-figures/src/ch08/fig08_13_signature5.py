"""Figure 8.13: Signature 5, first state: claim-status strips of Caldwell's signed scope v1.0 (day 28)."""
from _common import S, plt, save
import signature5 as sig
import caldwell_scope as cs
doc = cs.signed()
secs = [("scope", "scope"), ("criteria", "criteria"), ("volumes", "volumes"), ("out of scope", "out of scope"),
        ("register", "register")]
sig.STATES["ch08"] = dict(rows=[(n, doc.strip(k)) for n, k in secs], changed=["criteria"])
fig, ax = S.figure(3.9)
sig.draw(ax, "ch08")
save(fig, 13, kind="diagram", data="04-code/ch08 caldwell_scope.signed(); signature5.STATES['ch08']")
