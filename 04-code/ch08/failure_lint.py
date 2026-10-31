"""Failure injection (Chapter 8): lint scope draft v0.3 (day 24), then the signed v1.0 (day 28). Deterministic stand-in.

v0.3 carries the two failures the chapter is about: two success criteria with no measurement (C-08 is the sales
promise copied in, C-09 is a wish), and a vendor position that three documents later reads as a customer
requirement (SD-15). The evaluation suite refuses any criterion the lint rejects.
"""
from collections import Counter
from caldwell_scope import draft_v03, signed

for doc in (draft_v03(), signed()):
    found = doc.lint()
    print(f"LINT  {doc.customer} scope {doc.version}  day {doc.day}: {len(found)} findings")
    for key, code, msg in found:
        print(f"  {key:<6}{code:<24}{msg}")
    exported = [c["key"] for c in doc.suite_config()]
    refused = [c.key for c in doc.criteria if c.key not in exported]
    print(f"  evaluation suite accepts {len(exported)} of {len(doc.criteria)} criteria" +
          (f"; refuses {', '.join(refused)}" if refused else ""))
    by = Counter(code for _, code, _ in found)
    if by:
        print("  by finding: " + ", ".join(f"{k.lower()} {v}" for k, v in by.most_common()))
    print()
