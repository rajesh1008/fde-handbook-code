# Chapter 28 lab: Guardrails and the Customer's Rules

Greystone's 60 rules as rule cards, each with a check and two tests, run as input, output, action and budget
guardrails over the sandbox week (200 referrals) and the red team's set (140 attacks, 60 benign twins).
**Deterministic stand-in**: referrals, drafts, attacks, token counts, prices and latencies are synthetic; the rule
cards, checks, suite, budgets and breakers are the real code. No patient information.

Run: `./make_outputs.sh` (writes `output/*.txt` and runs the tests). Needs fieldkit (package 0.1.0, book layer v3.5).

| Script | Listing | What it shows |
|---|---|---|
| rules.py | (data) | the 60 rule cards and the statements they came from |
| world.py, cases.py, attacks.py | (data) | sandbox week, the injected referral, test cases, red-team set |
| checks.py | (code) | one check per rule; model-assisted rules use labeled pattern stand-ins |
| elicit.py | 28.1 | statements to rule cards; register coverage and lint |
| rules_as_tests.py | 28.2 | every rule tested both ways; what v1's tests of I-04 missed; fail closed |
| replay.py | 28.3 | the sandbox week and the injected referral through v1 and v2; cost per layer |
| redteam.py | 28.4 | 140 attacks and 60 twins against v2, v3 and a keyword guard; fleet breaker |
| tradeoff.py | 28.5 | six policy packs: attacks stopped against clean work queued |
| loop.py | 28.6 | the runaway lookup loop without and with budgets and the breaker |
| tryit.py a, b, c | Try It Yourself | weak progress signal; writing a card; the price of a VERIFY rule |

**On site.** The checks run inside Greystone's tenant in the same service as the authorizer (Chapter 25), under the
sandbox read identity. Model-assisted checks call the small model behind the gateway; their prompts and thresholds
are versioned with the rule register. The fleet breaker pages Northlight's on-call and notifies the managed-service
provider's run desk.
