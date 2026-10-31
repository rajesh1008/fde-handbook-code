"""Figure 50.12: Signature 16, David Okafor's pack at go-live (day 171); five tiles changed since day 118."""
from _common import S  # noqa: F401
import sys
sys.path.insert(0, str(S.ROOT / "04-code/ch50")) if hasattr(S, "ROOT") else None
import signature16, execpack
from fieldkit.gates import pack
p0, p = pack(execpack.STATES[118]), pack(execpack.STATES[171])
before = {a.name: a.status for a in p0["rows"]}
short = {"decision record": "gate register, AR to MRA", "lineage": "lineage store, Canada",
         "model and prompt versions": "bank inventory, 7", "evaluation at the time": "validation, sub two",
         "human review": "600 memos scored", "authority boundary": "Schedule D, release one",
         "incident history": "op risk register", "monitoring": "first report day 201"}
tiles = [(a.name, a.status, short[a.name], f"{a.owner.split()[-1]} d{a.day}" if a.owner and a.day else "") for a in p["rows"]]
signature16.STATES.setdefault("ch50", dict(asof="Harbourline Bank, day 171", digest=p["digest"], tiles=tiles,
    changed=tuple(a.name for a in p["rows"] if a.status != before[a.name])))
signature16.render("ch50", "fig50-12", __file__)
