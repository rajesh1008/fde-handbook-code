"""Chapter 4 fixtures: the 25 proofs a deployment needs, filled in for each customer on a given day.
Caldwell facts on days 1 to 9 come from Chapter 3 [CHECK ch03]. All names are fictional."""
import copy
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "fieldkit"))
from deployment import Checklist, Proof

CALDWELL_PEOPLE = ("Daniel Reyes", "Anne Kessler", "Priya Natarajan", "Tom Whitfield")
GREYSTONE_PEOPLE = ("Sam Oakley", "Michael Hart", "Marcus Bell")
PENNANT_PEOPLE = ("Jenna Ruiz",)

# (key, dimension, requirement, must_pass)
REQUIRED = [
    ("cap-customer-docs", "capability", "fields correct on the customer's own documents, scored by its expert", True),
    ("cap-gold-set", "capability", "per-field accuracy on a gold set drawn from the production mix", True),
    ("cap-by-channel", "capability", "accuracy reported per intake channel and document type", False),
    ("cap-unreadable", "capability", "known behavior on unreadable, partial and out-of-scope documents", False),
    ("cap-cost", "capability", "cost per document at the customer's volume", False),
    ("wf-intake-paths", "workflow", "every intake path inventoried, with monthly volume", True),
    ("wf-landing", "workflow", "output lands in the system of record where the work happens", True),
    ("wf-exceptions", "workflow", "exceptions route to a named human queue", False),
    ("wf-review-time", "workflow", "review time per item measured against today's process", False),
    ("wf-volume", "workflow", "peak volume and latency known and tested", False),
    ("ctl-account", "controls", "runs in the customer's cloud account and network", True),
    ("ctl-gateway", "controls", "every model call goes through the customer's gateway", True),
    ("ctl-retention", "controls", "data location and retention decided by the customer", True),
    ("ctl-identity", "controls", "runs under a customer service identity with least privilege", True),
    ("ctl-arch-review", "controls", "Architecture Review gate passed", True),
    ("own-exec", "ownership", "accountable executive accepts the acceptance criteria", True),
    ("own-gold-set", "ownership", "owner of the gold set and of what 'correct' means", True),
    ("own-operations", "ownership", "owner of the running system after hand-over", True),
    ("own-model-risk", "ownership", "model-risk approver named", True),
    ("own-override", "ownership", "rule for who decides when the output is wrong in production", False),
    ("rec-lineage", "reconstructability", "every output traces to document, page and field", True),
    ("rec-versions", "reconstructability", "prompt, model and code version recorded on every run", False),
    ("rec-logs", "reconstructability", "gateway logs retained where the customer can read them", False),
    ("rec-review", "reconstructability", "reviewer corrections retained with who and when", False),
    ("rec-evidence-pack", "reconstructability", "evidence pack format agreed with model risk", True),
]


def blank(system, people):
    c = Checklist(system, customer_people=people)
    for key, dim, req, must in REQUIRED:
        c.add(Proof(key, dim, req, must_pass=must))
    return c


def demo_as_sold():
    """What the sales demo on Northlight's own demo set put on the table, scored on the same 25 proofs."""
    c = blank("Caldwell Mutual, demo as sold", CALDWELL_PEOPLE)
    c.update("cap-customer-docs", status="held", measured_by="Graham Lowell",
             on_what="Northlight demo set, 100 fields on ten documents", evidence="sales deck slide 7")
    c.update("cap-by-channel", status="partial", measured_by="Graham Lowell",
             on_what="demo set: email and scanned PDF only", evidence="sales deck slide 8")
    c.update("cap-cost", status="partial", measured_by="Graham Lowell",
             on_what="list price per page, no Caldwell volume", evidence="pricing sheet")
    return c


def caldwell(day=10):
    c = blank("Caldwell Mutual", CALDWELL_PEOPLE)
    # Day 2: Anne scored the demo on ten of her documents (58 of 100 fields). A stand-in, not a gold set.
    c.update("cap-customer-docs", status="partial", measured_by="Anne Kessler",
             on_what="ten documents (4 email, 3 fax, 3 mail), 100 fields, day 2, demo stand-in",
             evidence="evidence/day2-demo-score.json")
    c.update("cap-by-channel", status="partial", measured_by="Anne Kessler",
             on_what="same ten documents: email 72%, fax 53%, mail 43%", evidence="evidence/day2-demo-score.json")
    # Anne agreed on day 8 to own the gold set and the definition of 'correct' for each field.
    c.update("own-gold-set", status="held", measured_by="Anne Kessler", on_what="field definitions note, day 8",
             evidence="decisions/gold-set-owner.md", owner="Anne Kessler", accepted_day=8,
             authority="defines correct for each field; assigns adjusters to score")
    # Daniel signed the contract, but has not yet accepted criteria that differ from the sales deck.
    c.update("own-exec", status="partial", measured_by="Daniel Reyes", on_what="signed order form, day 0",
             evidence="contract/order-form.pdf", owner="Daniel Reyes", accepted_day=None,
             authority="budget, production change windows")
    if day >= 12:
        c.update("own-exec", status="held", accepted_day=12, on_what="re-baselined acceptance criteria, day 12",
                 evidence="decisions/rebaseline-day12.md")
        c.update("ctl-retention", status="partial", measured_by="Priya Natarajan",
                 on_what="storage question raised day 12, decision open", evidence="decisions/sample-storage.md")
    return c


def caldwell_projected(no_owner=False):
    """Caldwell as it could look at shadow exit if the plan holds. With no_owner, every owner is wiped."""
    c = caldwell(day=12)
    c.system = "Caldwell Mutual, projected"
    for p in c.proofs.values():
        p.status = "held"
        p.measured_by = p.measured_by or {"capability": "Anne Kessler", "workflow": "Tom Whitfield",
                                          "controls": "Priya Natarajan", "ownership": "Daniel Reyes",
                                          "reconstructability": "Priya Natarajan"}[p.dimension]
        p.on_what = p.on_what or "shadow-mode records, projected"
    for key in ("cap-cost", "wf-volume", "rec-logs"):
        c.proofs[key].status = "partial"
    owners = {"own-exec": ("Daniel Reyes", "budget, production change windows"),
              "own-gold-set": ("Anne Kessler", "defines correct for each field"),
              "own-operations": ("Daniel Reyes", "claims platform run budget and on-call"),
              "own-model-risk": ("Priya Natarajan", "chairs the model-risk review"),
              "own-override": ("Anne Kessler", "adjuster override rule")}
    for key, (who, auth) in owners.items():
        c.update(key, owner=who, accepted_day=140, authority=auth)
    if no_owner:
        c.system = "Caldwell Mutual, projected, owners removed"
        c.update("own-exec", owner="Claims Operations", accepted_day=None, authority="")
        c.update("own-operations", owner="TBD", accepted_day=None, authority="")
        c.update("own-model-risk", owner="Model Risk Committee", accepted_day=None, authority="")
        c.update("own-override", owner="", accepted_day=None, authority="")
    return c


def greystone_sales_demo():
    """Greystone at signature: the demo ran on synthetic referral packets; Michael Hart is named owner."""
    c = blank("Greystone Health", GREYSTONE_PEOPLE)
    c.update("cap-customer-docs", status="held", measured_by="Sam Oakley",
             on_what="40 synthetic referral packets", evidence="demo/greystone-synthetic.json")
    c.update("own-exec", status="held", measured_by="Marcus Bell", on_what="order form, procurement file",
             evidence="contract/order-form.pdf", owner="Michael Hart", accepted_day=0, authority="")
    c.update("own-gold-set", status="held", measured_by="Michael Hart", on_what="kickoff agenda",
             evidence="notes/kickoff.md", owner="Michael Hart", accepted_day=0,
             authority="clinical definitions for referral triage")
    c.update("ctl-account", status="partial", measured_by="Sam Oakley",
             on_what="Azure subscription request, security questionnaire open (41 questions)",
             evidence="access/azure-subscription.md")
    return c


def pennant_sales_demo():
    """Pennant at signature: the demo matched clean EDI 214 messages; Jenna Ruiz is sponsor and owner."""
    c = blank("Pennant Logistics", PENNANT_PEOPLE)
    c.update("cap-customer-docs", status="partial", measured_by="Jenna Ruiz",
             on_what="one week of EDI 214 messages, no scans or photos", evidence="evidence/edi-week.json")
    c.update("ctl-account", status="held", measured_by="Jenna Ruiz", on_what="GCP project granted day 5",
             evidence="access/gcp-project.md")
    for key, auth in (("own-exec", "operations budget"), ("own-gold-set", "defines a matched shipment"),
                      ("own-operations", "operations budget")):
        c.update(key, status="held", measured_by="Jenna Ruiz", on_what="kickoff notes", evidence="notes/kickoff.md",
                 owner="Jenna Ruiz", accepted_day=2, authority=auth)
    return c
