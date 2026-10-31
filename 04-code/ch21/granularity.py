"""Listing 21.8: lineage for every output, or for decisions only?"""
import _paths  # noqa: F401
from pennant import u

MONTH_OUTPUTS = 9000      # documents reconciled per month (stand-in)
DECISION_SHARE = 0.13     # outputs that are a claim or an exception
NODE_BYTES = 640          # measured from LineageStore.size_bytes() on the lab chain / nodes
NODES = 8
QUESTIONS = 40            # audit and dispute questions in the stand-in log

if __name__ == "__main__":
    kinds = ["decision" if u(i, "q") < 0.55 else "non-decision" for i in range(QUESTIONS)]
    dec = kinds.count("decision")
    for name, share in (("every output", 1.0), ("decisions only", DECISION_SHARE)):
        mb = MONTH_OUTPUTS * share * NODES * NODE_BYTES / 1e6
        answerable = QUESTIONS if share == 1.0 else dec
        print(f"{name:<15} {mb:6.1f} MB per month, questions answerable from the chain {answerable}/{QUESTIONS} ({answerable / QUESTIONS:.0%})")
    print(f"the {QUESTIONS - dec} unanswerable ones ask why something was NOT flagged, e.g. 'why did invoice 77412 match?'")
