"""Figure 32.16: Signature 13, the gate stack (first appearance; four customers on day 103 of Greystone)."""
from _common import S, world  # noqa: F401  (sets paths)
import signature13
signature13.STATES.setdefault("ch32", dict(
    asof="as of Greystone day 103",
    rows=[(s.customer, [(g.status, g.day) for g in s.gates]) for s in world.stacks()],
    changed=(("Greystone", "security"),)))
signature13.render("ch32", "fig32-16", __file__)
