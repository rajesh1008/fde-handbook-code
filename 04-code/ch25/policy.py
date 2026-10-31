"""Release boundaries and authorizers for Caldwell and Greystone, as approved in the chapter."""
import _paths  # noqa: F401
from fieldkit.actions import Grant, ReleaseBoundary, Authorizer
from fieldkit.connectors import Rule

CALDWELL = ReleaseBoundary("Caldwell Mutual", [
    Grant("read", ("prod", "preprod"), ("read_document", "read_policy"), "Daniel Reyes", 104,
          "svc-nl-claims-ro"),
    Grant("draft", ("prod",), ("draft_claim",), "Anne Kessler", 104, "shown in the review surface only"),
    Grant("write", ("preprod",), ("create_claim",), "Daniel Reyes", 104, "after an adjuster accepts"),
], refused={"set_reserve": "Anne Kessler: reserves are an adjuster's decision",
            "set_status": "Anne Kessler: claim status belongs to claims-core",
            "assign_adjuster": "Anne Kessler: assignment rules run in claims-core"})

GREYSTONE = ReleaseBoundary("Greystone Health", [
    Grant("read", ("sandbox",), ("read_referral",), "Sam Oakley", 113, "sandbox feed"),
    Grant("draft", ("sandbox",), ("draft_prior_auth",), "Michael Hart", 113, "coordinator work queue"),
], refused={"submit_prior_auth": "Michael Hart: a person submits",
            "set_urgency": "Michael Hart: urgency is a clinical call",
            "message_patient": "Michael Hart: no automated patient contact"})

PROTECTED = ("status", "reserve", "adjuster", "coverage")
RULES = [Rule("V-127", "loss no later than the report date", lambda a: a.get("loss_date", "") <= "2026-10-31"),
         Rule("F-01", "policy number shape", lambda a: str(a.get("policy_no", "")).startswith("CM-"))]


def caldwell_authorizer():
    return Authorizer(CALDWELL, protected=PROTECTED, rules=RULES, key_prefix="CM")


def greystone_authorizer():
    return Authorizer(GREYSTONE, protected=("urgency", "submitted"), key_prefix="GH")
