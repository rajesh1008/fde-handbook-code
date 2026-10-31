"""Listing 25.4: the same day through the Executor: one intent key per document, retries owned by the
executor, a rejection from claims-core final for that intent."""
import _paths  # noqa: F401
from collections import Counter
from fieldkit.actions import ActionLedger, Executor, Proposal, intent_key
from fieldkit.connectors import WriteBack
from policy import caldwell_authorizer
from sim import ClaimsCore
import contextlib, io
with contextlib.redirect_stdout(io.StringIO()):
    from day109_retry import docs, LOSE, GUESS

core, led = ClaimsCore(lose=dict(LOSE)), ActionLedger()
ex = Executor(WriteBack(core, verify_fields=("policy_no", "loss_date", "cause_code")), caldwell_authorizer(), led,
              "svc-nl-claims-wr", "preprod")
calls = 0
for d in docs:
    rec = dict(d["payload"], doc_id=d["doc_id"])
    p = Proposal(intent_key("CM", d["doc_id"], "create_claim"), "create_claim", "preprod", rec, d["doc_id"])
    for attempt in range(3):
        calls += 1
        a = ex.run(p, approved_by="adjuster accept", day=109)
        if a.state != "unknown":
            break
    if a.state == "held":                         # the agent loop tries its old trick once more
        guess = Proposal(p.intent, p.op, p.env, dict(rec, cause_code=GUESS[rec["loss_type"]]), p.source)
        ex.run(guess, approved_by="adjuster accept", day=109)
ext = core.extract()
biz = Counter((r["policy_no"], r["loss_date"], r["claimant"]) for r in ext)
print(f"documents {len(docs)}  executor calls {calls}  action records {len(led.actions)}")
print(f"action states {led.by_state()}")
print(f"open claims {len(ext)}  duplicates {sum(n - 1 for n in biz.values() if n > 1)}  "
      f"voided shells {sum(1 for r in core.claims.values() if r['status'] == 'VOID')}")
den = [a for a in led.actions if a.state == "denied"]
print(f"denied resubmits {len(den)}  stage {sorted({a.stage for a in den})}")
a = next(a for a in led.actions if a.state == "unknown")
print("an unknown, then its retry:")
for r in [x for x in led.actions if x.intent == a.intent]:
    print(f"  {r.action_id} {r.state:<9} target={r.target_id} raw={r.raw} hash={r.request_hash}")
