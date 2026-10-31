"""The three customers' pipelines as data, classified by the autonomy decision tree (fieldkit.autonomy, v1.3).

Caldwell Mutual: the 12-step claims-intake pipeline that all eleven intake paths of Chapter 6 converge on.
Greystone Health: the 25-step electronic referral path walked in Chapter 14 (read from 04-code/ch14/pipeline.py).
Pennant Logistics: the 15-step shipment-document pipeline as designed in sprint 2 (proposed design) [CHECK ch22].
Step names are the customers' words, shortened. Owners are the people who maintain the written rules.
"""
import importlib.util, pathlib
import _path  # noqa: F401
from fieldkit.autonomy import Step

D = dict(determined=True)
def R(owner): return dict(written_rules=True, rule_owner=owner)
def C(check): return dict(closed_output=True, check=check)
O = dict()

CALDWELL = [
    Step("C01", "receive document and capture text from the intake path", **D),
    Step("C02", "read the received date from the stamp, fax header or mail header", **D),
    Step("C03", "parse the policy number by pattern and check digit", **D),
    Step("C04", "look up the policy and the coverage in force on the loss date", **D, ops=("join", "identity")),
    Step("C05", "match to an existing claim (claim number, or policy and loss date)", **D, ops=("identity",)),
    Step("C06", "classify the document into the four signed types or out of scope", **C("type in closed set; confidence 0.90 or a person")),
    Step("C07", "classify the loss cause into Caldwell's loss codes", **C("code in the loss-code table; confidence 0.85 or a person")),
    Step("C08", "read amounts and dates from the form's fixed zones and validate them", **D, ops=("arithmetic",)),
    Step("C09", "apply fast-track and adjuster routing rules", **R("Anne Kessler"), ops=("threshold",)),
    Step("C10", "apply special-investigation referral indicators", **R("special investigations unit lead"), ops=("threshold",)),
    Step("C11", "draft the first-notice summary for the adjuster, every statement cited", **O),
    Step("C12", "write the claim record and queue item to the claims system", **D),
]

PENNANT = [
    Step("N01", "receive EDI message or document scan from the intake queue", **D),
    Step("N02", "parse EDI segments into shipment fields", **D),
    Step("N03", "detect the layout family among the 41 known layouts", **C("family in the layout list; else unknown layout queue")),
    Step("N04", "read printed fields from the layout's template zones", **D),
    Step("N05", "read the handwritten delivery date", **C("valid date inside the shipment window; confidence 0.90 or a person")),
    Step("N06", "look up the carrier code in the carrier master", **D, ops=("join",)),
    Step("N07", "match the shipment to a booking by bill of lading number", **D, ops=("identity",)),
    Step("N08", "convert units and compute weights and charges", **D, ops=("arithmetic",)),
    Step("N09", "apply hazardous-goods and customs hold rules", **R("compliance manager"), ops=("threshold",)),
    Step("N10", "apply accessorial charge rules", **R("billing manager"), ops=("threshold",)),
    Step("N11", "apply service-level escalation rules", **R("Jenna Ruiz"), ops=("threshold",)),
    Step("N12", "read a free-text exception email and draft the exception note", **O),
    Step("N13", "write the booking to the transport management system", **D),
    Step("N14", "send the status message back to the shipper", **D),
    Step("N15", "archive the document with its retention tag", **D),
]


def _greystone():
    """Convert Chapter 14's 25 electronic steps into fieldkit Steps (same three answers, same owners)."""
    ch14 = pathlib.Path(__file__).resolve().parents[1] / "ch14"
    import sys
    sys.path.insert(0, str(ch14))
    spec = importlib.util.spec_from_file_location("ch14_pipeline", ch14 / "pipeline.py")
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    sys.path.remove(str(ch14))
    out = []
    for s in mod.ELECTRONIC:
        out.append(Step(s.n, s.name, determined=s.determined, written_rules=s.written_rules,
                        closed_output=s.closed_output, rule_owner=s.rule_owner,
                        check=("closed set or schema; draft only" if s.closed_output else None)))
    return out


GREYSTONE = _greystone()
CUSTOMERS = {"Caldwell Mutual": CALDWELL, "Greystone Health": GREYSTONE, "Pennant Logistics": PENNANT}
