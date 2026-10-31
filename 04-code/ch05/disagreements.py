"""The first-month disagreement log: Callum Reid (from an integrator) and
Sofia Brennan (from a model lab) against Northlight's vendor rules.

Each entry: day, axis, engagement, Callum's instinct, Sofia's instinct, the
Northlight ruling, and whose instinct the ruling kept (C, S, both or neither).
"""
from __future__ import annotations

from collections import Counter

AXES = ["scope and change", "what goes in the product", "model or deterministic",
        "exit and hand-over", "where reuse goes", "whose stack"]

LOG = [
    (3, "scope and change", "Greystone", "write a change request for the referral form",
     "prompt the model to read it", "product backlog; no change request", "neither"),
    (4, "whose stack", "Pennant", "use the customer's cloud document service",
     "call the lab-hosted frontier model", "Northlight product inside the customer's cloud", "C"),
    (6, "model or deterministic", "Pennant", "one template per layout, 41 templates",
     "one prompt for all 41 layouts", "six layout families, rules first, model last", "neither"),
    (8, "scope and change", "Greystone", "bill the extra integration hours under T&M",
     "absorb them, it is a flagship", "bill to the cap, then Northlight absorbs; tell sales", "C"),
    (9, "where reuse goes", "Pennant", "keep a personal accelerator repo",
     "send failures to a research team", "product backlog with a reproduction", "neither"),
    (11, "exit and hand-over", "Pennant", "propose a run-state managed service",
     "hand over after the prototype passes", "hand over to product support after Live Stable", "neither"),
    (12, "what goes in the product", "Greystone", "build the SSO group mapping as client code",
     "put it in the platform; every customer has a directory", "productize: second customer asked", "S"),
    (15, "model or deterministic", "Pennant", "regex for dates, no model",
     "model for dates, it is good at it", "regex for printed dates; model for handwritten, measured", "both"),
    (17, "whose stack", "Greystone", "defer to the managed-service provider's standards",
     "bring the lab's evaluation suite", "customer's standards; Northlight eval suite inside them", "both"),
    (19, "exit and hand-over", "Greystone", "stay on after go-live as the run team",
     "leave at go-live", "stay to Live Stable, then product support", "neither"),
    (22, "where reuse goes", "Greystone", "tag the export as a reusable accelerator",
     "not worth keeping", "client-specific; document it, do not productize", "S"),
    (24, "what goes in the product", "Pennant", "customer-specific layout table in the customer's repo",
     "fine-tune on Pennant's layouts", "layout-family detector into the product", "neither"),
    (26, "scope and change", "Pennant", "re-scope the fixed fee for the new layouts",
     "absorb and move fast", "absorb, log it in the hours ledger, price the next deal from it", "S"),
    (29, "exit and hand-over", "Greystone", "write the exit date into the statement of work",
     "no exit date needed", "exit gate in the plan: Live Stable plus 30 days", "C"),
]


def summary():
    by_axis = Counter(e[1] for e in LOG)
    kept = Counter(e[6] for e in LOG)
    return by_axis, kept


def main():
    print(f"FIRST-MONTH DISAGREEMENT LOG  ({len(LOG)} entries, days 1 to 30)")
    for d, axis, eng, c, s, ruling, k in LOG:
        print(f"  day {d:>2}  {axis:<25}{eng:<10}kept: {k}")
        print(f"          Callum: {c}\n          Sofia:  {s}\n          ruling: {ruling}")
    by_axis, kept = summary()
    print("BY AXIS")
    for a in AXES:
        print(f"  {a:<26}{by_axis[a]}")
    print("WHOSE INSTINCT THE RULING KEPT")
    for k, label in (("C", "Callum (integrator)"), ("S", "Sofia (lab)"), ("both", "both"),
                     ("neither", "neither: the vendor rule won")):
        print(f"  {label:<30}{kept[k]}")


if __name__ == "__main__":
    main()
