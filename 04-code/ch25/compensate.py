"""Listing 25.7: compensation in someone else's system. Find our duplicates by business key, keep the first
claim, void untouched duplicates through claims-core's own VOID-DUP, route touched ones to a person."""
import _paths  # noqa: F401
from collections import defaultdict
from fieldkit.actions import ActionLedger, Executor
from policy import caldwell_authorizer
import contextlib, io
with contextlib.redirect_stdout(io.StringIO()):
    import day109_retry as d109                  # re-runs the naive day; its printout belongs to Listing 25.6

core = d109.core
groups = defaultdict(list)
for r in core.extract():
    groups[(r["policy_no"], r["loss_date"], r["claimant"])].append(r["claim"])
TOUCHED = {}                                     # duplicates a reviewer had already opened by 09:00 on day 110
dup_list = [(cs[0], c) for cs in groups.values() if len(cs) > 1 for c in cs[1:]]
for i, (_, c) in enumerate(dup_list):
    if i % 4 == 1:
        TOUCHED[c] = "reviewer note added"
led = ActionLedger()
ex = Executor(d109.wb, caldwell_authorizer(), led, "svc-nl-claims-wr", "preprod")
for survivor, c in dup_list:
    a = ex.compensate(c, survivor, touched_by=TOUCHED.get(c), day=110)
    print(f"{a.action_id} {c} survivor {survivor} -> {a.state:<11} {a.reasons[0]}")
print(f"duplicates {len(dup_list)}  compensated {led.by_state().get('compensated', 0)}  "
      f"routed to the claims data team {led.by_state().get('routed', 0)}")
print(f"open claims after compensation {len(core.extract())}  "
      f"VOID-DUP {sum(1 for r in core.claims.values() if r['status'] == 'VOID-DUP')}")
guessed = [c for c, r in core.claims.items() if r["status"] == "OPEN" and r["loss_type"] == "WATER"
           and r["cause_code"] and not next(d for d in d109.docs if d["doc_id"] == r["doc_id"])["gold"]["cause_code"]]
for c in guessed:
    ex._rec(__import__("fieldkit.actions", fromlist=["Proposal"]).Proposal(
        f"confirm-{c}", "confirm_cause", "preprod", {"claim": c}, c),
        __import__("fieldkit.actions", fromlist=["Decision"]).Decision(False, "compensation",
                                                                       ["cause code was guessed; adjuster decides"]),
        "routed", day=110)
print(f"claims carrying a guessed cause code {len(guessed)}: routed to the senior adjuster, not voided, not edited")
