"""Listing 26.1: the same extractor, two evaluation suites. Where the 23 points went."""
import json
from collections import defaultdict
from world import gold_items, northlight_items, judge_v1, weighted_acc, acc, FIELDS, CRITICAL

nl, gold = northlight_items(), gold_items()
steps = [
    ("Northlight's 300 cases, Northlight's judge", acc(nl, judge_v1)),
    ("Anne's 300 documents, Northlight's judge", weighted_acc(gold, judge_v1)),
    ("Anne's documents, exact match, Northlight's definitions", weighted_acc(gold, lambda it: it.nl_ok)),
    ("Anne's documents, Caldwell's definitions, her adjusters", weighted_acc(gold)),
]
print("field accuracy, extract-2026-04 with prompt p6 (3,000 fields per suite)")
prev = None
for name, v in steps:
    d = "" if prev is None else f"  ({100 * (v - prev):+.1f} points)"
    print(f"  {name:<58} {v:6.1%}{d}")
    prev = v
print(f"  unweighted on the gold set (for the record):               {acc(gold):6.1%}")

print("\nby field: Northlight's judge on Anne's documents vs Anne's adjusters")
byf = {}
for f in FIELDS:
    its = [it for it in gold if it.field == f]
    a, b = weighted_acc(its, judge_v1), weighted_acc(its)
    byf[f] = (a, b)
    print(f"  {f:<18} judge {a:6.1%}   adjusters {b:6.1%}   gap {100 * (a - b):5.1f}")

docs = defaultdict(list)
for it in gold:
    docs[it.doc].append(it)
bad_crit = sum(any(not it.anne_ok for it in its if it.field in CRITICAL) for its in docs.values())
bad_any = sum(any(not it.anne_ok for it in its) for its in docs.values())
print("\nthe same results counted the way an adjuster meets them (300 documents)")
print(f"  documents with a routing field wrong (policy, loss date, cause code): {bad_crit} ({bad_crit / 300:.0%})")
print(f"  documents with any of ten fields wrong:                           {bad_any} ({bad_any / 300:.0%})")
json.dump(dict(steps=steps, byfield=byf, bad_crit=bad_crit, bad_any=bad_any),
          open("output/vendor_vs_customer.json", "w"), indent=1)
