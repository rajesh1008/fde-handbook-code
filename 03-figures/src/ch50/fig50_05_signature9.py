"""Figure 50.5: Signature 9 for Harbourline; the surface in the suite, the brain in the governed cloud."""
from _common import S  # noqa: F401
import signature9
signature9.STATES.setdefault("ch50", dict(zone=("suite: credit officer", "bank's governed cloud"),
    surface=["suite add-in pane", "bank sign-in", "draft memo, cited"],
    brain=dict(flag="read-and-draft flag", broker="token broker", orch="spread and draft", model="model via bank gateway",
               verify="numeric gate, lineage", audit="lineage store", sources="package, policy"),
    crossing=("1 package per request", "draft with lineage"), broken=None, note=""))
signature9.render("ch50", "fig50-05", __file__)
