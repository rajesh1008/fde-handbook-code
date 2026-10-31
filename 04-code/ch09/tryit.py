"""Try It Yourself, Chapter 9.  python tryit.py 1|2|3"""
import sys, random
import _path  # noqa: F401
from fieldkit.autonomy import Step, TreeError, walk, SHORT, split, CLASSES
import costs as K
from pipelines import CALDWELL


def try1():
    """Classify a workflow of your own. The example has two mistakes the tree refuses."""
    mine = [
        Step("W1", "read the invoice number and supplier from the header", determined=True),
        Step("W2", "approve invoices under the spending limit", written_rules=True, rule_owner=None, ops=("threshold",)),
        Step("W3", "read the line items into a schema", closed_output=True, check="schema; totals reconcile", ops=("arithmetic",)),
        Step("W4", "write a short note on unusual items for the approver"),
    ]
    print("TRY 1: classify a workflow of your own")
    for s in mine:
        try:
            cls, ans = walk(s); print(f"  {s.n} {SHORT[cls]:<8} {' / '.join(ans)}")
        except TreeError as e:
            print(f"  {s.n} REFUSED  {e}")
    print("  fix: name the owner of the spending limit; move the totals check to a code step after W3")


def try2():
    """Put your own contract prices in and see what the fall depends on."""
    print("TRY 2: frontier price against the fall, scanned Caldwell document")
    base = K.PRICE["frontier"]
    for f in (0.5, 1.0, 2.0):
        K.PRICE["frontier"] = (base[0] * f, base[1] * f)
        _, demo = K.demo_cost("scan"); _, new = K.pipeline_cost([7, 2, 2, 1], "scan")
        print(f"  frontier price x{f:<4} demo {demo:.4f}  pipeline {new:.4f}  fall {1 - new / demo:.0%}")
    K.PRICE["frontier"] = base


def try3():
    """Send one small-model step to the frontier model instead ("just use the big one")."""
    print("TRY 3: C07 loss cause sent to the frontier model")
    rng = random.Random(3)
    for label, c in (("as classified", [7, 2, 2, 1]), ("C07 to frontier", [7, 2, 1, 2])):
        _, cost = K.pipeline_cost(c, "scan")
        lat = sorted(K.pipeline_latency(c, rng)[1] for _ in range(400))
        print(f"  {label:<16} classes {c}  $/doc {cost:.4f}  p50 {lat[200]:.1f}s  p95 {lat[380]:.1f}s")
    print("  the closed output and its check do not change; only the bill and the wait do")


if __name__ == "__main__":
    {"1": try1, "2": try2, "3": try3}[sys.argv[1] if len(sys.argv) > 1 else "1"]()
