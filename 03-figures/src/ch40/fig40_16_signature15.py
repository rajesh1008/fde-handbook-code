"""Figure 40.16: Signature 15 after Chapter 40. A pinned v1 pack in the audit sample (04-code/ch40/output/audit.txt)."""
from _common import S, text  # noqa: F401
import signature15
a = text("audit"); head = a.split("chain head over the sample ")[1].split()[0]
assert "exceptions 0" in a and "findings on the agent: 0" in a
signature15.STATES["ch40-v1"] = dict(asof="day 214, pinned record", head=head, changed=("prompt, model",), rows=[
    ("document", "sha256", "verified"), ("lineage", "chain", "verified"), ("retrieval", "index snapshot", "verified"),
    ("prompt, model", "content hash at send", "verified"), ("score, route", "threshold record", "verified"),
    ("decision", "fields digest", "verified"), ("review", "review record", "verified"), ("action", "ledger entry", "verified")])
signature15.render("ch40-v1", "fig40-16", __file__)
