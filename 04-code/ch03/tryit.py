"""Try It Yourself, Chapter 3. Three ways to re-read the same 100 corrections.

  python tryit.py a   score whole documents: how many could an adjuster accept untouched?
  python tryit.py b   weight the fields the way Anne Kessler weights them
  python tryit.py c   drop the two fields the demo never had a meaning for, and see what is left
"""
import sys
from collections import defaultdict

from caldwell_docs import caldwell_docs
from demo_extract import extract
from scoring import score

# Anne's weights (day 2): a wrong policy number, loss date, received date or injury flag sends the claim to
# the wrong queue or starts the wrong clock; the rest cost an adjuster a minute.
ANNE_WEIGHTS = {"policy_number": 3, "loss_date": 3, "date_received": 3, "injury_reported": 3,
                "claimant_name": 2, "loss_type": 2}


def variant_a(rows):
    per = defaultdict(list)
    for r in rows:
        per[r["doc"]].append(r["ok"])
    clean = [d for d, v in per.items() if all(v)]
    one_fix = [d for d, v in per.items() if v.count(False) == 1]
    print(f"documents with every field right: {len(clean)}/10")
    print(f"documents needing exactly one correction: {len(one_fix)}/10 {one_fix}")
    print(f"field score for comparison: {sum(r['ok'] for r in rows)}/100")


def variant_b(rows):
    got = sum(ANNE_WEIGHTS.get(r["field"], 1) for r in rows if r["ok"])
    tot = sum(ANNE_WEIGHTS.get(r["field"], 1) for r in rows)
    print(f"weighted score: {got}/{tot} = {100 * got / tot:.0f}%  (unweighted 58%)")
    for f, w in sorted(ANNE_WEIGHTS.items(), key=lambda x: -x[1]):
        ok = sum(r["ok"] for r in rows if r["field"] == f)
        print(f"  weight {w}  {f:<16} {ok}/10")


def variant_c(rows):
    keep = [r for r in rows if r["field"] not in ("date_received", "intake_channel")]
    ok = sum(r["ok"] for r in keep)
    print(f"without date_received and intake_channel: {ok}/{len(keep)} = {100 * ok / len(keep):.1f}%")
    by = defaultdict(list)
    for r in keep:
        by[r["channel"]].append(r["ok"])
    for ch, v in by.items():
        print(f"  {ch:<6} {sum(v)}/{len(v)} = {100 * sum(v) / len(v):.0f}%")


if __name__ == "__main__":
    rows = score(caldwell_docs(), extract)
    {"a": variant_a, "b": variant_b, "c": variant_c}[sys.argv[1] if len(sys.argv) > 1 else "a"](rows)
