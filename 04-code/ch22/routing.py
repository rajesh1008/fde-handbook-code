"""Listing 22.4: route every document that is not matched to a named queue with a packet a person can act on."""
import _paths  # noqa: F401
from collections import Counter
from shadow_week import week
from pipeline import QUEUES, RULE_OWNER, bk_ref

if __name__ == "__main__":
    docs, bk, res, g, store, refs, fx = week()
    q = Counter(r["queue"] for r in res if r["queue"])
    print("queue            documents  owner")
    for k in ("sender request", "clerk read", "reconciliation", "escalation"):
        print(f"{k:<16} {q[k]:>9}  {QUEUES[k]}")
    print(f"{'total routed':<16} {sum(q.values()):>9}  of {len(res)} ({sum(q.values()) / len(res):.1%})")
    why = Counter()
    for r in res:
        if r["queue"] == "sender request":
            why["X12 refused" if r["why"].startswith("X12") else r["why"].split("  ")[-1].split(":")[0].strip()] += 0
    rule = Counter(k for r in res if r["queue"] == "reconciliation" for k, v in r["rules"].items() if v[0] == "disagree")
    print("reconciliation exceptions by rule:", ", ".join(f"{k} {rule[k]} ({RULE_OWNER[k]})" for k in sorted(rule)))
    held = Counter("X12 envelope" if r["why"].startswith("X12") else ("legibility" if "reject" in r["why"] else "completeness or consistency")
                   for r in res if r["queue"] == "sender request")
    print("sender requests by cause:", dict(sorted(held.items())))
    clerk = Counter(r["why"][:3] for r in res if r["queue"] == "clerk read")
    esc = Counter(r["why"][:3] for r in res if r["queue"] == "escalation")
    print("clerk reads by step:", dict(sorted(clerk.items())), " escalations by step:", dict(sorted(esc.items())))
    ex = next(r for d, r in zip(docs, res) if r["queue"] == "reconciliation" and "R3" in r["why"] and d.get("currency") == "EUR")
    d = next(d for d in docs if d["doc_id"] == ex["doc_id"])
    print()
    print("packet for", ex["doc_id"])
    print(f"  queue: reconciliation   owner of the rule: {RULE_OWNER['R3']}   day {d['day']}")
    print(f"  document: {d['channel']} {d['kind']} from {d['sender']}, linked {bk_ref(ex['linked'])} by {ex['linked_by'][10:]}")
    print(f"  rule R3 disagrees: {ex['rules']['R3'][1]}")
    print(f"  references: {fx} (owner {refs.meta(fx)['owner']}); rate card lane contract")
    print(f"  lineage claim: {ex['claim']}")
    print("  the person decides: dispute with carrier / accept and note / correct the TMS booking")
