"""Listing 25.6: failure injection. Day 109 replay in pre-production, the agent loop as first built:
every tool call made its own key, and the model retried whatever came back not verified."""
import _paths  # noqa: F401
from collections import Counter
from fieldkit.connectors import WriteBack, reconcile
from sim import documents, ClaimsCore

docs = [d for d in documents(245, 109, seed=109) if d["kind"] == "fnol"][:231]
for d in [d for d in docs if d["payload"]["loss_type"] == "WATER"][3:60:14]:
    d["gold"]["cause_code"] = d["payload"]["cause_code"] = ""   # the letter never states a cause
LOSE = {d["doc_id"]: (2 if i in (32, 157) else 1) for i, d in enumerate(docs) if i % 25 == 7}
GUESS = {"WATER": "WTR-01"}


def naive_day(core):
    wb, calls, narrative = WriteBack(core, verify_fields=("policy_no",)), 0, []
    for d in docs:
        rec = dict(d["payload"], doc_id=d["doc_id"])
        for attempt in range(3):
            calls += 1
            e = wb.submit(f"call-{calls:05d}", rec)              # a fresh key for every call
            if e.state == "verified":
                narrative.append((d["doc_id"], f"Created claim {e.target_id} for {rec['claimant']}."))
                break
            if e.reasons and e.reasons[0].startswith("rejected V-118"):
                rec = dict(rec, cause_code=GUESS[rec["loss_type"]])   # the model "fixes" the rejection
    return wb, calls, narrative


core = ClaimsCore(lose=LOSE)
wb, calls, narrative = naive_day(core)
ext = core.extract()
by_key = reconcile({e.key: e.record for e in wb.outbox.entries.values() if e.state == "verified"},
                   {r["agent_ref"]: r for r in ext}, ["policy_no"])
biz = Counter((r["policy_no"], r["loss_date"], r["claimant"]) for r in ext)
dups = sum(n - 1 for n in biz.values() if n > 1)
guessed = [r for r in ext if r["loss_type"] == "WATER" and r["cause_code"] == "WTR-01" and
           not next(d for d in docs if d["doc_id"] == r["doc_id"])["payload"]["cause_code"]]
print(f"documents {len(docs)}  tool calls {calls}  lost responses {sum(LOSE.values())} on {len(LOSE)} documents")
print(f"open claims {len(ext)}  for documents {len({r['doc_id'] for r in ext})}")
print(f"reconcile by key: matched {by_key.counts()['matched']}  unexplained {by_key.unexplained}")
print(f"business-key duplicates (policy, loss date, claimant): {dups}")
print(f"V-118 rejections resubmitted with a guessed cause code: {len(guessed)}")
said_ok = sum(1 for _, s in narrative if s.startswith("Created claim"))
print(f"model narrative lines saying 'Created claim': {said_ok}  mentioning a retry or duplicate: "
      f"{sum(1 for _, s in narrative if 'retry' in s or 'duplicate' in s)}")
open("output/day109_state.txt", "w").write(repr(dict(dups=dups, guessed=len(guessed), lost=sum(LOSE.values()),
                                                     docs=len(docs), calls=calls)))
