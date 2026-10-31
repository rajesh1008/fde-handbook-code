"""Figure 24.14: Signature 9, broken state: the day-115 shortcut in which the orchestrator queried the sources as its
own service role, bypassing the broker (identity.txt). Same template as Figure 24.3."""
import re
from _common import S, text  # noqa: F401
import signature9
n = re.search(r"nl-brain-svc: (\d+) of 3,000", text("identity")).group(1)
st = dict(signature9.STATES["ch24"]); st["broken"] = "broker"
st["note"] = f"service role: {n} of 3,000 results unreadable"
signature9.STATES.setdefault("ch24-shortcut", st)
signature9.render("ch24-shortcut", "fig24-15", __file__)
