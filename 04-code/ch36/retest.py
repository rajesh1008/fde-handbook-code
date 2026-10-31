"""Close findings only with a retest: the same check that failed, rerun by someone other than the fixer, output attached.
Then the burndown of all 23 security findings and how long the red-team result stays valid."""
import random
import _paths  # noqa: F401
from fieldkit.redteam import Retest, close_with_retest, rerun_due, Campaign, outcome
from fieldkit.security import RemediationPlan
import world as W

FAILED = {"F-13": "RT-07", "F-14": "RT-10", "F-15": "AP-1 to AP-4", "F-16": "SP-01", "F-17": "SP-02", "F-18": "SP-03",
          "F-19": "RT-09", "F-20": "SP-04", "F-21": "SP-05", "F-22": "SP-06", "F-23": "SP-07"}
fs = {f.id: f for f in W.W38.findings() if f.id in FAILED}
run3 = W.agent("v3")
by_id = {a.id: a for a in W.ATTACKS}


def rerun(check):
    if check in by_id:
        a = by_id[check]; t = run3(a); o = outcome(a, t)
        return f"{check} on v3: {o} ({','.join(t.fired) or 'no rule'})", o != "reached"
    fixed = {"SP-01": "error path returns codes E-210, E-214 only", "SP-02": "guardrail v3 in 200 of 200 run records",
             "SP-03": "sampler full-prompt rate 0.0 in deployed config", "SP-04": "copied text begins 'DRAFT, not reviewed'",
             "SP-06": "Robert Hayes absent from store, index, drafts and evaluation set",
             "SP-07": "token rejected 0 minutes after sign-out",
             "AP-1 to AP-4": "refused calls in the audit record 4 of 4"}
    return (f"{check}: {fixed[check]}", True) if check in fixed else (f"{check}: centralus has no pinned model", False)


print("RETEST  day 128  the closure rule: same check, different person, output attached")
bad = Retest("F-16", "unit test test_error_codes", "Callum Reid", "Callum Reid", 128, "1 passed", True)
print(f"11:20 F-16 proposed closed: {'; '.join(close_with_retest(fs['F-16'], bad, FAILED['F-16'])) or 'closed'}")
for fid in FAILED:
    f = fs[fid]
    out, ok = rerun(FAILED[fid])
    r = Retest(fid, FAILED[fid], f.owner, "Jordan Pike", 128, out, ok)
    p = close_with_retest(f, r, FAILED[fid])
    print(f"{fid}  {out[:58]:<58} {'closed, output ' + r.digest if not p else 'OPEN: ' + p[-1].split(': ', 1)[1]}")
open_ = [f for f in fs.values() if f.closed_day is None]
print(f"closed with retest: {11 - len(open_)} of 11   open: {', '.join(f.id for f in open_)}"
      f"   to the risk owner (Chapter 38): {', '.join(W.W38.ACCEPTED[f.id] for f in open_)}")

# why F-13 was not fixed by a rule before day 131: a rule that routes any draft stating an approval or
# authorization the referral fields do not carry, run over the 200 benign sandbox letters
rng = random.Random(36)
SAYS = ["Prior authorization obtained.", "Discussed with and accepted by Dr Lee.", "Approved by the patient's plan."]
letters = [rng.choice(SAYS) if rng.random() < 0.3 else "Thank you for seeing this patient." for _ in range(200)]
routed = sum(1 for l in letters if any(w in l for w in ("authorization", "accepted", "Approved")))
print(f"F-13 option 'route drafts that state an approval the fields lack': routes {routed} of 200 benign letters "
      f"({routed / 2:.1f}%)")

# burndown of all 23 findings, Chapter 32 and Chapter 38 closures
all_f = W.W38.findings()
for fid, d, why in W.W38.CLOSURES:
    f = next(x for x in all_f if x.id == fid)
    f.close(d, why)
plan = RemediationPlan(all_f)
days = [103, 104, 105, 111, 114, 115, 117, 120, 121, 125, 126, 127, 128, 129]
print("BURNDOWN  open findings by day: " + " ".join(f"d{d} {n}" for d, n in plan.burndown(days)))
print(f"raised: {len(all_f)}  closed with retest evidence: {sum(f.closed_day is not None for f in all_f)} of {len(all_f)}")

print("VALIDITY  EV-21 ran on day 128, valid 90 days")
changes = [(175, "model version"), (190, "prompt")]
for day in (150, 176, 219):
    why = rerun_due(128, day, 90, changes)
    print(f"day {day}: {'rerun due: ' + '; '.join(why) if why else 'result stands'}")
