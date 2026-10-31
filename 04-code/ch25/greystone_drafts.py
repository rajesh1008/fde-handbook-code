"""Listing 25.3: the second customer. Greystone sandbox week, days 115 to 119: drafts only, by Michael Hart's rule."""
import _paths  # noqa: F401
import random
from collections import Counter
from fieldkit.actions import Proposal, intent_key
from policy import greystone_authorizer

rng, az = random.Random(115), greystone_authorizer()
res, routed, queue, lost = Counter(), 0, {}, 0
for i in range(200):
    ref = f"RF-{i:04d}"
    red = rng.random() < 0.09
    if red:
        routed += 1
        continue                                   # a red flag goes to a clinician, never to a draft
    p = Proposal(intent_key("GH", ref, "draft_prior_auth"), "draft_prior_auth", "sandbox", {"ref": ref}, ref)
    d = az.authorize(p)
    res[("draft_prior_auth", d.stage)] += 1
    for attempt in range(2):                       # the work queue sometimes times out; retry the same intent
        queue.setdefault(p.intent, ref)
        if rng.random() > 0.02:
            break
        lost += 1
    r = rng.random()
    extra = "set_urgency" if r < 0.045 else "submit_prior_auth" if r < 0.06 else "message_patient" if r < 0.07 else None
    if extra:
        q = Proposal(intent_key("GH", ref, extra), extra, "sandbox", {"ref": ref}, ref)
        res[(extra, az.authorize(q).stage)] += 1
print(f"referrals 200  red flags routed to a clinician {routed}")
for (op, stage), n in sorted(res.items()):
    print(f"  {op:<18} {stage:<10} {n:>4}")
print(f"queue timeouts retried {lost}  drafts in the coordinators' queue {len(queue)}  duplicate drafts 0")
