"""Listing 31.1: the decision tree applied to the pilot build, and what one document costs (deterministic stand-in)."""
import _paths  # noqa: F401
from fieldkit.autonomy import split, table, share, no_model_share
from agent import STEPS, Gateway
from world import shadow

print(table(STEPS))
sp = split(STEPS)
print("\nsplit:", " / ".join(f"{v} {k}" for k, v in sp.items()),
      f"| deterministic {share(STEPS):.0%} of steps, no model {no_model_share(STEPS):.0%}")
docs = [d for d in shadow() if not d["band"].startswith("none")]
n = len(docs)
nonemail = sum(d["channel"] != "email" for d in docs)
narr = round(0.71 * n)                                   # stand-in: 71% carry a loss narrative for C07
calls = n + narr + n
print(f"\nmodel calls over the shadow window: C06 {n}, C07 {narr}, C11 {n} -> {calls / n:.2f} per document ({n} routed)")
g = Gateway()
c11 = 5200 * g.RATE_IN + 450 * g.RATE_OUT
rows = [("capture and OCR (C01)", (nonemail * 0.0042 + (n - nonemail) * 0.0010) / n),
        ("C06 document type, c06-p4 prompted", g.PRICE["c06-p4"]),
        ("C07 cause code, small", g.PRICE["c07-small-2"] * narr / n),
        ("C11 summary and fields, frontier", c11),
        ("retrieval for C11", 0.0006),
        ("router, guardrails, state, logs", 0.0005)]
bands = {b: sum(d["band"] == b for d in docs) for b in ("proceed", "review", "escalate")}
review = bands["review"] / n * 60 / 3600 * 46
escal = bands["escalate"] / n * 240 / 3600 * 46
rows += [("review band, 60 s at $46/hour", review), ("escalations, 240 s at $46/hour", escal)]
print("\ncost per routed document (stand-in rates; loaded rate $46/hour)")
for k, v in rows:
    print(f"  {k:<36} ${v:.4f}")
machine = sum(v for _, v in rows[:6])
total = sum(v for _, v in rows)
print(f"  {'machine total':<36} ${machine:.4f}\n  {'people total':<36} ${review + escal:.4f}\n  {'all':<36} ${total:.4f}")
print(f"model and compute are {machine / total:.1%} of the cost per document; review labor is {1 - machine / total:.1%}")
print(f"at 11,244 in-scope documents a month: machine ${machine * 11244:,.0f}, people ${(review + escal) * 11244:,.0f}")
