"""Listing 28.5: six policy packs on one curve: attacks stopped against clean work that still reaches the queue."""
import dataclasses
import _paths  # noqa: F401
from fieldkit.guardrails import GuardrailSuite
from rules import CARDS, version
from checks import checks
from pipeline import run, queued, suite
from attacks import attacks, twins, keyword_guard, escaped
from world import sandbox_week

A, T = attacks(), twins()
refs, drafts, actions, faults = sandbox_week()
faulty = {i for ids in faults.values() for i in ids}
v3 = suite("v3")
clean = [r for r in refs if r["id"] not in faulty and queued(run(v3, r, drafts.get(r["id"]), actions.get(r["id"])))]
benign = [(t["ref"], t["draft"], t["actions"]) for t in T] + [(r, drafts[r["id"]], actions[r["id"]]) for r in clean]


def sub(pred, v="v3"):
    return GuardrailSuite([c for c in version(CARDS, v) if pred(c)], checks(v))


strict = GuardrailSuite([dataclasses.replace(c, effect="route", route_to=c.route_to or "coordinator") if c.effect == "flag" else c
                         for c in CARDS], checks("v3"))
PACKS = [("P0 boundary and budgets only", sub(lambda c: c.source in ("boundary", "signed") or c.kind == "budget"), None),
         ("P1 + payer tables and regulation", sub(lambda c: c.source in ("boundary", "signed", "payer", "regulation") or c.kind == "budget"), None),
         ("P2 suite v2 (before the red team)", suite("v2"), None),
         ("P3 suite v3 (chosen)", v3, None),
         ("P4 v3 + keyword guard", v3, keyword_guard),
         ("P5 v3, every flag routes", strict, None)]
print(f"attacks: {len(A)}   benign set: {len(T)} twins + {len(clean)} clean sandbox referrals = {len(benign)}")
print(f"{'pack':<36} {'rules':>5} {'stopped':>8} {'benign queued':>14} {'benign queued, no flag':>23}")
for name, s, pre in PACKS:
    stopped = sum(not escaped(a, run(s, a["ref"], a["draft"], a["actions"], a["stop"], pre)) for a in A)
    res = [run(s, r, d, a, None, pre) for r, d, a in benign]
    q = sum(queued(x) for x in res)
    qf = sum(queued(x) and not x["flags"] for x in res)
    print(f"{name:<36} {len(s.live()):>5} {stopped:>4}/{len(A)} {q:>6}/{len(benign)} ({q / len(benign):.1%}) {qf:>6}/{len(benign)} ({qf / len(benign):.1%})")
