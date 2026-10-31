"""Listing 31.6: state and memory scopes, retention and erasure (deterministic stand-in)."""
from agent import Release, Gateway, run
from state import ClaimStateStore, Value, ScopeViolation, NEVER, OPS_KEYS
from walkthrough import EMILY
from world import shadow

store = ClaimStateStore()
run(EMILY, Release(), Gateway(), store)
k = EMILY.key
print(f"claim scope: {k} holds {len(store.claims[k].items)} items: {', '.join(sorted(store.claims[k].items))}")
tries = [("document_text", Value(EMILY.text, k, "E-142-017 p1")),
         ("loss_location", Value("basement", "IK-142-0031", "E-142-031 p1"))]
for name, v in tries:
    try:
        store.put(k, name, v, 142)
    except ScopeViolation as e:
        print(f"  refused: {e}")
docs = [d for d in shadow() if d["channel"] == "fax"]
senders = {}
for d in docs:
    senders.setdefault(d["id"][-2:], [0, 0])[0] += 1
    senders[d["id"][-2:]][1] += d["rotated"]
for s, (n, r) in sorted(senders.items())[:3]:
    store.put_ops("sender_orientation", f"fax-sender-{s}", r / n, 153)
print(f"operational scope: {sum(len(v) for v in store.ops.values())} numbers under {', '.join(store.ops)}")
for key, sub, val in (("sender_orientation", "fax-sender-07", "usually upside down, ask for J. Doe"),
                      ("claimant_history", "Emily Carter", 2)):
    try:
        store.put_ops(key, sub, val, 153)
    except ScopeViolation as e:
        print(f"  refused: {e}")
print(f"never stored: {', '.join(NEVER)}")
for i, d in enumerate([x for x in shadow() if x["day"] == 142][:40]):
    store.open(f"IK-142-{i + 100:04d}", "shadow", 142); store.put(f"IK-142-{i + 100:04d}", "loss_type",
                                                                   Value("water", f"IK-142-{i + 100:04d}", "p1"), 142)
store.hold("IK-142-0105", 200, "Caldwell legal", "matter CM-L-0091 (synthetic)")
print(f"\nretention job, day 231: {store.retention(231)}")
print(f"retention job, day 232: {store.retention(232)}")
store2 = ClaimStateStore(); run(EMILY, Release(), Gateway(), store2)
r = store2.erase(k, 160, "erasure request PR-0042 (synthetic)")
print(f"\nerasure of {k} on day 160: {r['erased']} items {r['status']}; outside the agent's store and routed to "
      f"Caldwell's privacy process: {'; '.join(r['outside'])}")
print("\naccess and deletion log, last 5 of", len(store.log) + len(store2.log))
for row in (store.log + store2.log)[-5:]:
    print("  day %s  %-15s %-28s %s %s" % row)
