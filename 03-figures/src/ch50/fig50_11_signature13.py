"""Figure 50.11: Signature 13 in its five-gate form, Harbourline at the return (day 126) and at go-live (day 171)."""
from _common import S, text  # noqa: F401
import signature13
assert "Model-Risk Approval  passed with conditions   day 158" in text("committee_s2")
rows = [("day 61", [("passed", 61)] + [("not started", None)] * 4),
        ("day 118", [("passed", 61), ("passed", 112), ("not started", None), ("in review", 118), ("not started", None)]),
        ("day 126", [("passed", 61), ("passed", 112), ("in review", None), ("returned", 126), ("not started", None)]),
        ("day 171", [("passed", 61), ("passed", 112), ("conditional", 150), ("conditional", 158), ("not started", None)])]
signature13.STATES.setdefault("ch50", dict(asof="Harbourline Bank", rows=rows,
    changed=(("day 171", "Shadow Exit"), ("day 171", "Model-Risk Approval")),
    gates=("Architecture Review", "Build Complete", "Shadow Exit", "Model-Risk Approval", "Live Stable"),
    head=(("Architecture", "Review"), ("Build", "Complete"), ("Shadow", "Exit"), ("Model-Risk", "Approval"), ("Live", "Stable"))))
signature13.render("ch50", "fig50-11", __file__)
