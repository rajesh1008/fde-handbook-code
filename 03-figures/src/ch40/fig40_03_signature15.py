"""Figure 40.3: Signature 15, first state. The disputed claim's v0 pack on day 177 (04-code/ch40/output/dispute.txt)."""
from _common import S, text  # noqa: F401
import signature15
t = text("dispute").split("REBUILT")[0]
assert "prompt and model      contradicted" in t
signature15.STATES["ch40-v0"] = dict(asof="day 177, v0 record", head="not anchored", changed=("prompt, model",), rows=[
    ("document", "sha256", "verified"), ("lineage", "chain", "verified"), ("retrieval", "index snapshot", "verified"),
    ("prompt, model", "name and commit", "contradicted"), ("score, route", "threshold record", "verified"),
    ("decision", "fields digest", "verified"), ("review", "review record", "verified"), ("action", "ledger entry", "verified")])
signature15.render("ch40-v0", "fig40-03", __file__)
