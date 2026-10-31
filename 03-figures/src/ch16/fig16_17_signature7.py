"""Figure 16.17: Signature 7 (fieldkit after Chapter 16). Shared template signatures/signature7.py; the state is
registered as STATES['ch16'] here, so the template is not edited per chapter. New modules in emphasis."""
from _common import S  # noqa: F401  (sets paths)
import signature7
signature7.STATES.setdefault("ch16", dict(
    version="0.1.0",
    modules=[("access.py", "", "evidence", None), ("readiness.py", "", "data", None),
             ("fixtures.py", "", "system", None), ("engagement.py", "", "evidence", None),
             ("deployment.py", "", "evidence", None), ("cadence.py", "", "evidence", None),
             ("escalation.py", "", "evidence", None), ("datareadiness.py", "", "data", None),
             ("histories.py", "", "system", None),
             ("synthetic.py", "representativeness", "data", "new"), ("deid.py", "attack tests", "blocker", "new"),
             ("shadow.py", "tap, canaries", "system", "new"), ("sampling.py", "strata, manifest", "evidence", "new")],
    imports=[(2, 0), (2, 1), (8, 6), (8, 7)],
    labs=[("Ch 16 lab", "represent.py")],
    future=[]))  # the planned-versions lane is dropped here to keep the page under 7.2 in; the text lists them
signature7.render("ch16", "fig16-17", __file__)
