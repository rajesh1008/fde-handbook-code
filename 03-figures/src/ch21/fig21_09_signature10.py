"""Figure 21.9: Signature 10, the lineage chain for one Pennant output (template signatures/signature10.py)."""
from _common import S  # noqa: F401  (sets paths)
import signature10
signature10.STATES.setdefault("ch21", dict(
    details=["hls-inv-77310.pdf", "page 1", "HLS-INV-03 + OCR", "reconcile.overbilling", "over-billed USD 412.50", "Dana Whitaker, day 66"],
    side=["sha256 9f2c41d0", "legibility 0.91", "EUR 9,870.00", "", "", "weekly freight audit"],
    ref=("fx_rates@1f8a22b1", "as of day 66"), broken=False, note=""))
signature10.render("ch21", "fig21-09", __file__)
