"""Try It Yourself, Chapter 19. python tryit.py a|b|c"""
import sys
import _paths  # noqa: F401
from fieldkit.connectors import FileDrop, Rule, WriteBack, reconcile
from adapter import ClaimsCoreTarget
from sim import ClaimsCore, HEADER, RULES, as_record, caldwell_sample, nightly_csv

ex = sys.argv[1] if len(sys.argv) > 1 else "a"
fn = {d["doc"]: d for d in caldwell_sample() if d["kind"] == "fnol"}
F = ["policy_no", "claimant", "loss_date", "loss_type", "cause_code", "zip"]
if ex == "a":   # widen the volume band and watch the truncated night get in
    for low in (0.6, 0.4):
        fd = FileDrop("t", HEADER, 210, low=low, key=lambda d: d.weekday() < 5)
        for n in range(1, 24):
            c, d = nightly_csv(n, rows=18200 if n == 23 else None)
            b = fd.check(f"n{n}", c, 140, label=d)
        print(f"low={low}: night 23 ({b.rows:,} rows) -> {b.status} {b.reasons}")
elif ex == "b":  # drop V-118 from the catalog, with and without compensation
    for comp in (True, False):
        app = ClaimsCore("preprod")
        wb = WriteBack(ClaimsCoreTarget(app), [Rule("V-031", *RULES["V-031"])], F, compensate=comp)
        for k, d in fn.items():
            wb.submit(k, d)
        shells = sum(1 for c in app.claims.values() if c["status"] == "SHELL")
        print(f"catalog without V-118, compensate={comp}: outbox {wb.outbox.by_state()}  orphan shells {shells}"
              f"  screen steps {wb.t.sc.steps}")
elif ex == "c":  # reconcile against your own log, then against the system
    app = ClaimsCore("preprod")
    wb = WriteBack(ClaimsCoreTarget(app), [Rule(r, *RULES[r]) for r in ("V-031", "V-118", "V-127")], F)
    for k, d in fn.items():
        wb.submit(k, d)
    victim = next(cid for cid, c in app.claims.items() if c["status"] == "OPEN")
    app.void(victim)                                  # an adjuster voids one overnight as a "duplicate"
    held = {e.key for e in wb.outbox.held()}
    mine = {e.key: e.record for e in wb.outbox.entries.values() if e.state == "verified"}
    theirs = {c["Agent Ref"]: as_record(c) for c in app.extract() if c["status"] == "OPEN"}
    print("against our outbox  :", reconcile(fn, mine, F, held).counts())
    print("against the extract :", reconcile(fn, theirs, F, held).counts())
