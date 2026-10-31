"""Figure 50.3: Signature 10, the lineage chain behind one ratio in a Harbourline memo."""
from _common import S, text  # noqa: F401
import signature10
assert "dscr               1.27x" in text("spread")
signature10.STATES.setdefault("ch50", dict(
    details=["Northgate FY2025 statements", "pages 4, 6, 9", "H03 table capture", "dscr 1.27x", "coverage 1.27x", "officer, in draft"],
    side=["hash recorded", "5 inputs", "C$ thousands", "", "", "draft only"],
    ref=("ratio definitions rev 2026-2", "covenant table, day 131"), broken=False, note=""))
signature10.render("ch50", "fig50-03", __file__)
