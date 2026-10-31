"""Try It Yourself, Chapter 25. python tryit.py a|b|c"""
import _paths  # noqa: F401
import sys, contextlib, io
from collections import Counter
from fieldkit.actions import Grant, ReleaseBoundary, Authorizer, Proposal, intent_key, Executor, ActionLedger
from fieldkit.connectors import WriteBack
from sim import ClaimsCore, documents

x = sys.argv[1] if len(sys.argv) > 1 else "a"
if x == "a":       # (a) key per call against key per intent, as the lost-response rate rises
    docs = [d for d in documents(200, 120, seed=120) if d["kind"] == "fnol" and d["payload"]["cause_code"]]
    for every in (50, 20, 10, 5):
        out = []
        for per_intent in (False, True):
            core = ClaimsCore(lose={d["doc_id"]: 1 for i, d in enumerate(docs) if i % every == 0})
            wb, n = WriteBack(core, verify_fields=("policy_no",)), 0
            for d in docs:
                for _ in range(3):
                    n += 1
                    k = intent_key("CM", d["doc_id"], "create_claim") if per_intent else f"call-{n}"
                    if wb.submit(k, dict(d["payload"], doc_id=d["doc_id"])).state == "verified":
                        break
            c = Counter((r["policy_no"], r["claimant"]) for r in core.extract())
            out.append(sum(v - 1 for v in c.values()))
        print(f"lost 1 in {every:>2}: duplicates key-per-call {out[0]:>3}  key-per-intent {out[1]}")
elif x == "b":     # (b) the capacity model: change the reviewers' hours and find the best escalation rate
    import review_surface  # noqa: F401  prints the table at two hours; edit CAP_MIN there and re-run
elif x == "c":     # (c) grant Greystone write in the sandbox and see what still refuses
    b = ReleaseBoundary("Greystone Health", [Grant("write", ("sandbox",), ("submit_prior_auth", "draft_prior_auth"),
                                                   "test only", 0)],
                        refused={"submit_prior_auth": "Michael Hart: a person submits"})
    az = Authorizer(b, key_prefix="GH")
    for op in ("draft_prior_auth", "submit_prior_auth"):
        d = az.authorize(Proposal(intent_key("GH", "RF-1", op), op, "sandbox", {"ref": "RF-1"}, "RF-1"))
        print(f"{op:<18} allowed={d.allowed} stage={d.stage} {d.reasons}")
