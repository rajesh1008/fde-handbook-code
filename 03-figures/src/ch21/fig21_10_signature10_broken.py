"""Figure 21.10: Signature 10, broken state: the calculation cites the FX table by path (lineage_broken.txt)."""
import re
from _common import S, text  # noqa: F401
import signature10
t = text("lineage_broken")
re_val = re.search(r"recomputed ([\d,.]+), recorded", t).group(1)
signature10.STATES.setdefault("ch21-broken", dict(
    details=["hls-inv-77310.pdf", "page 1", "HLS-INV-03 + OCR", "reconcile.overbilling", "over-billed USD 412.50", "Dana Whitaker, day 66"],
    side=["sha256 9f2c41d0", "legibility 0.91", "EUR 9,870.00", "", "", "weekly freight audit"],
    ref=("fx_rates.csv", "path, overwritten daily"), broken=True, note=f"day 81 recompute: {re_val}"))
signature10.render("ch21-broken", "fig21-10", __file__)
