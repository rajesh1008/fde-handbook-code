"""Figure 12.5: Signature 5, claim-status strips of Northlight's submitted response v1.0, one row per answer; the
ringed rows changed after the v0.9 lint (extract_run.py, failure_contradiction.py)."""
from _common import S, plt, save
import signature5 as sig
from fieldkit.bid import extract, strip
from harbourline import RESPONSE_V10
claims = extract(RESPONSE_V10)
sig.STATES["ch12"] = dict(rows=[(a, strip([c for c in claims if c.answer == a])) for a in RESPONSE_V10],
                          changed=["D-01", "D-05"])
fig, ax = S.figure(4.6)
sig.draw(ax, "ch12")
save(fig, 5, kind="diagram", data="04-code/ch12 extract(RESPONSE_V10); signature5.STATES['ch12']")
