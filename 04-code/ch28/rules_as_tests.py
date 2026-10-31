"""Listing 28.2: every rule tested both ways; what the v1 tests of I-04 missed."""
import _paths  # noqa: F401
from fieldkit.guardrails import test_rules
from pipeline import suite
from cases import tests, I04_CODE_CASE, I04_TEXT_CASE, I04_TWINS
from rules import version, CARDS

for v in ("v1", "v2", "v3"):
    s = suite(v)
    t = [x for x in tests(v) if x.rid in s.cards]
    r = test_rules(s, t)
    print(f"suite {v}: {len(s.live())} live rules, {len(t)} tests, {r.passed} pass, {len(r.failures)} fail, "
          f"untested {len(r.untested)}, missing checks {len(s.missing())}")
    for f in r.failures:
        print(f"   FAIL {f}")
print()
print("the day 124 test cases against each version of I-04")
for v in ("v1", "v2", "v3"):
    s = suite(v)
    row = []
    for name, c, want in [("code F10.239", I04_CODE_CASE, False), ("text only 'detox'", I04_TEXT_CASE, False),
                          ("twin F17.210", I04_TWINS[0], True), ("twin F10.10 history", I04_TWINS[1], True)]:
        got = s.check_one("I-04", c).ok
        row.append(f"{name}: {'pass' if got else 'catch'}{'' if got == want else ' (WRONG)'}")
    print(f"  I-04 {v}: " + "; ".join(row))
print()
s = suite("v3")
broken = dict(s.checks); broken.pop("O-11")
from fieldkit.guardrails import GuardrailSuite
from checks import checks
gs = GuardrailSuite(version(CARDS, "v3"), broken)
from cases import ctx
print(f"fail-closed demo: O-11 check removed -> missing {gs.missing()}, clean draft decision: {gs.run('output', ctx()).effect}")
