"""Listing 19.6: the same 152 writes through WriteBack: an idempotency key stored in Agent Ref, a preflight
against the production rule catalog Caldwell exported on day 66, a read-back of every field we wrote,
compensation for a rejected shell, and a retry pass for writes whose outcome is unknown."""
import _paths  # noqa: F401
from fieldkit.connectors import Rule, WriteBack
from adapter import ClaimsCoreTarget
from sim import ClaimsCore, RULES, caldwell_sample

fn = [d for d in caldwell_sample() if d["kind"] == "fnol"]
catalog = [Rule(r, RULES[r][0], RULES[r][1]) for r in ("V-031", "V-118")]   # exported day 66; V-127 came day 69
app = ClaimsCore("preprod", lose_response=[d["doc"] for d in fn if d["timeout"]])
wb = WriteBack(ClaimsCoreTarget(app), catalog,
               verify_fields=["policy_no", "claimant", "loss_date", "loss_type", "cause_code", "zip"])
for d in fn:
    wb.submit(d["doc"], d)
print("after first pass :", wb.outbox.by_state())
for e in [e for e in wb.outbox.entries.values() if e.state == "unknown"]:
    wb.submit(e.key, e.record)
print("after retry pass :", wb.outbox.by_state())
reasons = {}
for e in wb.outbox.held():
    k = e.reasons[0].split(";")[0].split(" ")[0] + " " + e.reasons[0].split(";")[0].split(" ")[1]
    reasons[k] = reasons.get(k, 0) + 1
print("held, by reason  :", reasons)
for e in wb.outbox.held():
    if not e.reasons[0].startswith("preflight"):
        print(f"  {e.key}: {e.reasons[0]}")
st = {}
for c in app.claims.values():
    st[c["status"]] = st.get(c["status"], 0) + 1
refs = [c["Agent Ref"] for c in app.claims.values() if c["status"] == "OPEN"]
print(f"claims in system {len(app.claims)}  by status {dict(sorted(st.items()))}  duplicate claims "
      f"{len(refs) - len(set(refs))}  screen steps {wb.t.sc.steps}")
