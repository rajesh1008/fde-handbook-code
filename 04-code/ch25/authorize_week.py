"""Listing 25.2: every call the planner emitted in the shadow week (days 111 to 115), checked with its values."""
import _paths  # noqa: F401
from collections import Counter
from fieldkit.actions import Proposal, intent_key
from policy import caldwell_authorizer
from sim import documents

az = caldwell_authorizer()
docs = [d for day in range(111, 116) for d in documents(238, day, seed=day)]
props = []
for d in docs:
    p = d["payload"]
    if d["kind"] == "supporting":
        props.append(Proposal(intent_key("CM", d["doc_id"], "attach_document"), "attach_document", "prod",
                              {"doc": d["doc_id"]}, d["doc_id"]))
        continue
    props.append(Proposal(intent_key("CM", d["doc_id"], "draft_claim"), "draft_claim", "prod", dict(p),
                          d["doc_id"]))
    if p["loss_type"] == "AUTO" and d["conf"] < 0.5:            # the planner suggests a reserve
        props.append(Proposal(intent_key("CM", d["doc_id"], "draft_claim", 2), "draft_claim", "prod",
                              dict(p, reserve=2500), d["doc_id"]))
    if d["error"] == "loss_date" and p["loss_date"] > "2026-10-31":
        pass
    if d["error"] == "policy_no" and d["conf"] < 0.55:
        props.append(Proposal(intent_key("CM", d["doc_id"], "draft_claim", 2), "draft_claim", "prod",
                              dict(p, policy_no=p["policy_no"].replace("CM-", "")), d["doc_id"]))
    if d["conf"] < 0.4:                                         # the planner skips the review queue
        props.append(Proposal(intent_key("CM", d["doc_id"], "create_claim"), "create_claim", "prod", dict(p),
                              d["doc_id"]))
res = Counter()
for p in props:
    dec = az.authorize(p)
    res[(p.op, "allowed" if dec.allowed else f"denied:{dec.stage}")] += 1
print(f"documents {len(docs)}  calls proposed {len(props)}")
for (op, out), n in sorted(res.items()):
    print(f"  {op:<16} {out:<20} {n:>5}")
den = sum(n for (op, out), n in res.items() if out.startswith("denied"))
print(f"denied {den}  ({den / len(props):.1%} of calls); allowed calls needing a person: 0 (drafts only in prod)")
