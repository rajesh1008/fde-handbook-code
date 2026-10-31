"""Figure 15.13: Signature 6, first appearance. The day each access-ladder rung was reached, per customer.
Data: 04-code/ch15/ladder_dates.py (fieldkit v2 histories for Caldwell and Greystone; Chapter 1 fixtures for Pennant
and Harbourline). The two sampled rungs this chapter is about are drawn in the emphasis stroke."""
from _common import R
import signature6
from fieldkit.fixtures import pennant_tracker, harbourline_tracker
from fieldkit.histories import caldwell_history, greystone_history, rung_reached_days
signature6.STATES.setdefault("ch15", dict(lanes=[
    ("Caldwell", 54, rung_reached_days(caldwell_history().replay(54)), ["sampled"]),
    ("Greystone", 112, rung_reached_days(greystone_history().replay(112)), ["sampled"]),
    ("Pennant", 11, rung_reached_days(pennant_tracker()), []),
    ("Harbourline", 6, rung_reached_days(harbourline_tracker()), []),
]))
signature6.render("ch15", "fig15-13", __file__)
