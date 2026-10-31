"""claims-core as a WriteBack target, reached only through its two first-notice screens."""
import _paths  # noqa: F401
from fieldkit.connectors import ScreenConnector, ScreenSpec
from sim import FNOL1, FNOL2, as_record

SPECS = [ScreenSpec("FNOL-1", FNOL1, {"policy_no": "Policy No", "claimant": "Claimant", "loss_date": "Loss Date",
                                      "loss_type": "Loss Type", "agent_ref": "Agent Ref"}),
         ScreenSpec("FNOL-2", FNOL2, {"report_date": "Report Date", "cause_code": "Cause of Loss",
                                      "zip": "Loss ZIP"})]


class ClaimsCoreTarget:
    def __init__(self, app):
        self.app, self.sc = app, ScreenConnector(app, SPECS)

    def find(self, key):
        return next((cid for cid, c in self.app.claims.items()
                     if c.get("Agent Ref") == key and c["status"] == "OPEN"), None)

    def write(self, r, key):
        ok, cid, _ = self.sc.submit("FNOL-1", {f: r[f] for f in ("policy_no", "claimant", "loss_date", "loss_type")}
                                    | {"agent_ref": key}, key)
        return self.sc.submit("FNOL-2", {"report_date": r["report_date"], "cause_code": r["cause_code"],
                                         "zip": r["zip"], "_cid": cid}, key)

    def readback(self, cid):
        return as_record(self.sc.read("FNOL-1", cid) and self.app.read("FNOL-1", cid))

    def void(self, cid):
        return self.app.void(cid)


def naive_write(target, key, r):
    """What the first build did: write, and on a timeout write again."""
    try:
        return target.write(r, key)
    except TimeoutError:
        return target.write(r, key)
