"""Listing 4.5: lint a sales promise, then rewrite it as a deployment claim.

A promise passes only if somebody at the customer could check it: an accuracy number needs a scorer, a
document set with a count and a denominator; a date needs a gate and its dependencies with owners; an
integration or coverage claim needs the inventory it quantifies over."""
import re
from dataclasses import dataclass, field
from deployment import is_person

CLAIM_STATUSES = ("direct customer fact", "reconstructed from supplied artifact", "vendor position",
                  "proposed design", "decision required")
GATES = ("Architecture Review", "Build Complete", "Shadow Exit", "Model-Risk Approval", "Live Stable")


@dataclass
class Claim:
    text: str
    status: str
    scorer: str = ""
    documents: str = ""
    denominator: str = ""
    gate: str = ""
    depends_on: list = field(default_factory=list)   # (dependency, named owner)
    inventory: str = ""
    owner: str = ""                                  # for "decision required": who decides


def lint(c: Claim) -> list[str]:
    t = c.text.lower()
    out = []
    if c.status not in CLAIM_STATUSES:
        out.append(f"claim status '{c.status}' is not one of the five")
    if c.status == "decision required" and not is_person(c.owner):
        out.append("decision required, but no named person decides")
    if re.search(r"\d+(\.\d+)?\s*%|accura", t):
        if not is_person(c.scorer):
            out.append("accuracy with no named scorer at the customer")
        if not re.search(r"\d", c.documents):
            out.append("accuracy with no document set and count")
        if not c.denominator:
            out.append("accuracy with no denominator (fields? documents? auto-routed only?)")
    if re.search(r"\bday\b|\bdays\b|\bweeks?\b|\bmonths?\b|\blive\b", t):
        if c.gate not in GATES:
            out.append("a date with no gate")
        if not c.depends_on or not all(is_person(o) for _, o in c.depends_on):
            out.append("a date with no dependencies and owners")
    if re.search(r"integration|any document|every document|all documents", t) and not c.inventory:
        out.append("quantifies over an inventory nobody has made")
    return out


GRAHAM = [
    Claim("accuracy above 95% on Caldwell's documents", "vendor position"),
    Claim("live in production in under five months", "vendor position"),
    Claim("no integration work on Caldwell's side", "vendor position"),
    Claim("works on any document Caldwell receives", "vendor position"),
]

REWRITTEN = [
    Claim("of the fields the system sends to the claims core without review, at least 98% are correct when "
          "Anne Kessler's adjusters score them on the gold set; we report what share of fields qualifies",
          "proposed design", scorer="Anne Kessler",
          documents="gold set drawn from the production mix by channel, planned 300 documents, built once the claims sample arrives (requested day 9)",
          denominator="auto-routed fields only; review share reported alongside"),
    Claim("first production release planned between day 150 and day 200; Live Stable gate 30 days later",
          "proposed design", gate="Live Stable",
          depends_on=[("claims-core read-only service account", "Daniel Reyes"),
                      ("sample storage and retention decision", "Priya Natarajan"),
                      ("twelve pilot adjusters named", "Anne Kessler")]),
    Claim("integration work on Caldwell's side is listed, owned and sized before Build Complete: service "
          "account, gateway key rotation, claims-core write path, adjuster SSO group",
          "decision required", owner="Daniel Reyes",
          inventory="integration inventory v1, four items, Caldwell owners named"),
    Claim("coverage is reported per intake path and document type against the intake inventory; paths not "
          "covered go to the adjuster queue unchanged", "proposed design",
          inventory="intake path inventory (paths and monthly volumes), owed by Anne Kessler"),
]


def main():
    print("PROMISE LINT  Graham Lowell's four promises")
    rejected = 0
    for c in GRAHAM:
        problems = lint(c)
        rejected += bool(problems)
        print(f"  REJECT  {c.text}" if problems else f"  pass    {c.text}")
        for p in problems:
            print(f"            - {p}")
    print(f"rejected {rejected} of {len(GRAHAM)}")
    print()
    print("REWRITTEN AS DEPLOYMENT CLAIMS")
    for old, new in zip(GRAHAM, REWRITTEN):
        problems = lint(new)
        print(f"  [{new.status}] {'pass' if not problems else 'REJECT'}  was: {old.text}")
        for p in problems:
            print(f"            - {p}")
    print(f"rewritten claims passing: {sum(not lint(c) for c in REWRITTEN)} of {len(REWRITTEN)}")


if __name__ == "__main__":
    main()
