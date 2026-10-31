"""Listing 19.7: Caldwell intake wired end to end on the 200-document sample. Three intake connectors, the
deterministic extraction stand-in, write-back through the first-notice screens, the supporting-document index
file, and reconciliation against the next morning's claims-core extract. Then the first build, reconciled the
same way. Deterministic stand-in data; no model call."""
import hashlib
import _paths  # noqa: F401
from fieldkit.connectors import FileDrop, MailQueue, Message, Rule, WriteBack, reconcile
from adapter import ClaimsCoreTarget, naive_write
from sim import ClaimsCore, RULES, as_record, caldwell_sample

docs = caldwell_sample()
# --- intake: scan vendor batches, fax index, mailbox
scan = [d for d in docs if d["channel"] == "scan"]
fax = [d for d in docs if d["channel"] == "fax"]
mail = [d for d in docs if d["channel"] == "mail"]
sd = FileDrop("scan-vendor", ["doc_id", "pages", "received_ts"], deadline_min=6 * 60)
got = set()
batches = [scan[i:i + 9] for i in range(0, len(scan), 9)]
for i, b in enumerate(batches + [batches[3]]):                     # the vendor re-sends batch 4
    body = "doc_id,pages,received_ts\n" + "\n".join(f"{d['doc']},2,{d.get('report_date', '')}" for d in b)
    r = sd.check(f"batch{i:02d}.csv", body.encode(), 5 * 60)
    if r.status == "accepted":
        got |= {d["doc"] for d in b}
fx = FileDrop("fax-index", ["fax_id", "from", "pages", "received_ts"], deadline_min=24 * 60)
body = "fax_id,from,pages,received_ts\n" + "\n".join(f"{d['doc']},+18605550100,3,x" for d in fax)
if fx.check("fax_index.csv", body.encode(), 23 * 60).status == "accepted":
    got |= {d["doc"] for d in fax}
mq = MailQueue()
msgs = [Message(f"<{d['doc']}@b>", "b", d["doc"], [(d["doc"], hashlib.sha256(d["doc"].encode()).digest())])
        for d in mail]
for m in msgs + msgs[:6]:
    if mq.accept(m):
        got.add(m.subject)
print(f"intake: scan {len(scan)} (batches {len(batches)}, 1 re-send refused), fax {len(fax)}, mail {len(mail)}"
      f" (6 redeliveries caught); documents in {len(got)} of {len(docs)}")
# --- write-back, fixed
fn = {d["doc"]: d for d in docs if d["kind"] == "fnol" and d["doc"] in got}
sup = [d for d in docs if d["kind"] == "support" and d["doc"] in got]
catalog = [Rule(r, RULES[r][0], RULES[r][1]) for r in ("V-031", "V-118")]
F = ["policy_no", "claimant", "loss_date", "loss_type", "cause_code", "zip"]


def run(fixed):
    app = ClaimsCore("preprod", lose_response=[k for k, d in fn.items() if d["timeout"]])
    t = ClaimsCoreTarget(app)
    held = set()
    if fixed:
        wb = WriteBack(t, catalog, F)
        for k, d in fn.items():
            wb.submit(k, d)
        for e in [e for e in wb.outbox.entries.values() if e.state == "unknown"]:
            wb.submit(e.key, e.record)
        held = {e.key for e in wb.outbox.held()}
    else:
        for k, d in fn.items():
            naive_write(t, k, d)
    actual, seen = {}, {}
    for c in app.extract():                                        # the next-morning extract
        if c["status"] == "VOID":
            continue
        k = c["Agent Ref"]; seen[k] = seen.get(k, 0) + 1
        actual[k if seen[k] == 1 else f"{k}#{seen[k]}"] = as_record(c) | {"_status": c["status"]}
    return reconcile(fn, actual, F, held, orphan=lambda r: r["_status"] == "SHELL"), app


rec, app = run(True)
print(f"first notices {len(fn)}: reconciliation {rec.counts()}  unexplained {rec.unexplained}")
# --- supporting documents through the vendor index loader (nightly, reject report next morning)
loaded = {d["doc"]: {"claim_ref": d["claim_ref"]} for d in sup if not d["archived"]}
rejects = [d["doc"] for d in sup if d["archived"]]
rs = reconcile({d["doc"]: {"claim_ref": d["claim_ref"]} for d in sup}, loaded, ["claim_ref"], held=rejects)
print(f"supporting documents {len(sup)}: reconciliation {rs.counts()}  unexplained {rs.unexplained}")
print(f"end to end: {len(rec.matched) + len(rs.matched)} of {len(docs)} landed and verified, "
      f"{len(rec.held) + len(rs.held)} with a person, {rec.unexplained + rs.unexplained} unexplained")
naive, _ = run(False)
print(f"\nfirst build, same sample, same reconciliation: {naive.counts()}  unexplained {naive.unexplained}")
