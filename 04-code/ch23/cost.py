"""Section 23.5: cost attribution. Every line names who pays and which cost center is charged (stand-in rates)."""
import _paths  # noqa: F401
import caldwell_docs as C
from fieldkit.retrieval import CostMeter, token_cost, evaluate

TOK = 380; EMB = 0.02; GEN_IN = 2.50          # USD per million tokens, stand-in rates [CHECK ch26 chargeback]
SEARCHES = 4100                                # review-screen retrievals a month in shadow (stand-in)
ix, recs, acl, versions = C.build(day=88); C.apply_register(ix, C.lifecycle_register(versions))
n = len(ix.passages)

def meter(k, eval_cc=""):
    m = CostMeter()
    m.add("embed library", "Caldwell", "CC-CLM-OPS via nl-index", "one-time", token_cost(n * TOK, EMB), "6,452 x 380 tokens")
    m.add("re-embed + revalidate per pin", "Caldwell", "CC-CLM-OPS via nl-index", "per-event", token_cost(n * TOK, EMB) + 6 * 46, "at most every 90 days")
    m.add("query embeddings", "Caldwell", "CC-CLM-OPS via nl-shadow", "monthly", token_cost(SEARCHES * 30, EMB), "30 tokens a query")
    m.add("retrieved context in drafting calls", "Caldwell", "CC-CLM-OPS via nl-shadow", "monthly", token_cost(SEARCHES * k * TOK, GEN_IN), f"k={k}")
    m.add("PostgreSQL share (pgvector)", "Caldwell", "CC-ARCH-PLATFORM", "monthly", 38.0, "approved cluster")
    m.add("nightly ACL sync job", "Caldwell", "CC-ARCH-PLATFORM", "monthly", 9.0, "30 runs")
    m.add("question-set runs", "Caldwell", eval_cc, "monthly", token_cost(150 * 8 * (30 + k * TOK), GEN_IN) + 8 * token_cost(150 * 30, EMB), "8 runs a month")
    m.add("index maintenance engineering", "Northlight", "NL-DELIVERY", "monthly", 6 * 95.0, "6 h at USD 95 (stand-in)")
    return m

m = meter(10)
print("first meter, day 98: unattributed lines ->", [l.item for l in m.unattributed()],
      "(evaluation calls ran under nl-shadow and landed in production spend)")
m = meter(10, "CC-CLM-OPS via nl-eval")
print("after moving evaluation to nl-eval:", len(m.unattributed()), "unattributed")
print()
print(f"{'line':36s} {'payer':10s} {'cost center':26s} {'kind':9s} {'USD':>9s}")
for l in m.lines:
    print(f"{l.item:36s} {l.payer:10s} {l.cost_center:26s} {l.kind:9s} {l.usd:9.2f}")
print()
for k in (10, 5):
    mk = meter(k, "CC-CLM-OPS via nl-eval"); cal = mk.monthly_by_payer()["Caldwell"]
    rec = evaluate(ix, C.questions(recs), C.who_for, k=k)["recall"]
    ctx = [l.usd for l in mk.lines if l.item.startswith("retrieved")][0]
    print(f"k={k:2d}: Caldwell USD {cal:7.2f} a month, context share {ctx / cal:.0%}, "
          f"USD {cal / SEARCHES:.4f} per retrieval, recall at {k} {rec:.2f}")
print(f"Northlight engineering USD {m.monthly_by_payer()['Northlight']:.2f} a month (its own delivery cost, never on Caldwell's bill)")
