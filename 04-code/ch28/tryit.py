"""Try It Yourself. python tryit.py a | b | c"""
import sys
import dataclasses
import _paths  # noqa: F401
from fieldkit.guardrails import Budget, CircuitBreaker, RuleCard, GuardrailSuite, RuleTest, test_rules
from loop import agent, show

part = sys.argv[1] if len(sys.argv) > 1 else "a"
if part == "a":
    print("Try 1: the second failure. The progress signal counts any change in the result as progress.")
    r = agent(Budget(max_steps=12, max_tool_calls=20, max_repeat=99, max_tokens=10**9, max_cost=99), CircuitBreaker(3),
              progress_rule="result changed")
    show("weak progress signal, repeat budget off: the breaker never opens; the step budget stops the run", r)
    r2 = agent(Budget(max_steps=12, max_tool_calls=20, max_repeat=99, max_tokens=10**9, max_cost=99), CircuitBreaker(3),
               progress_rule="fewer candidates")
    show("progress means fewer candidate records: the breaker opens", r2)
elif part == "b":
    print("Try 2: write the card for a rule you just heard, then its two tests.")
    card = RuleCard("I-13", "A referral from an urgent care clinic waits for the primary physician's note.", "input",
                    "session", "Denise Alvarez", "Keisha Monroe", 121, effect="route", status="VERIFY")
    print("lint before:", card.lint())
    card = dataclasses.replace(card, route_to="coordinator", review_by=135)
    print("lint after: ", card.lint())
    s = GuardrailSuite([card], {"I-13": lambda c: (not (c["src"] == "urgent care" and not c["pcp_note"]), "waiting on PCP note")})
    r = test_rules(s, [RuleTest("I-13", "urgent care, no note", dict(src="urgent care", pcp_note=False), False)])
    print("one test only -> untested:", r.untested)
    r = test_rules(s, [RuleTest("I-13", "urgent care, no note", dict(src="urgent care", pcp_note=False), False),
                       RuleTest("I-13", "urgent care with note", dict(src="urgent care", pcp_note=True), True)])
    print("both tests -> untested:", r.untested, " failures:", r.failures)
elif part == "c":
    print("Try 3: the price of a VERIFY rule. O-03 at Michael's 90 days against the 30 days Keisha quoted.")
    from world import sandbox_week
    refs, drafts, actions, faults = sandbox_week()
    for days in (90, 60, 30):
        n = sum(1 for d in drafts.values() if any(a > days for a in d["lab_ages"]))
        print(f"  limit {days:>3} days: {n:>3} of {len(drafts)} drafts flagged ({n / len(drafts):.1%})")
