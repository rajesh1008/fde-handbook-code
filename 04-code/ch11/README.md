# Chapter 11 lab: the sponsor map as data

> **Stand-in notice.** Every person, day and number here belongs to the book's fictional customers (Greystone Health,
> Caldwell Mutual, Pennant Logistics). The plan durations in `plan.py` are labelled planning assumptions, not
> measurements. Outputs are deterministic: no randomness, no network, no model calls. Regenerate with `./make_outputs.sh`.

Signature 4 is the sponsor map: sponsor, operator, blocker, approver and owner, plus the champion network, for each
customer. This lab keeps it as data so a script, not a mood, says when it is incomplete or stale.

| File | What it does | Listing |
|---|---|---|
| `stakeholders.py` | `Person`, `StakeholderMap`, `check()` (missing roles, blockers without reasons, staleness by role, concentration, sponsor-approver), naive and gated scores | 11.1 |
| `champions.py` | Champion register: why, can, cannot, every ask; flags asks that bypass an approver | 11.3 |
| `greystone.py` | Kickoff map (day 2, no operator: the failure injection), working map (day 12), contacts at day 40, champions, design changes | 11.2 |
| `caldwell.py`, `pennant.py` | The other two working maps; Caldwell architecture review fixture | 11.5, 11.8 |
| `oakley41.py`, `plan.py` | Sam Oakley's 41 questions by theme; two stand-in plans (approvers at sign-off vs at design) | 11.4 |
| `status.py` | Seven-part weekly status, computed color, truth lint (reuses `fieldkit.cadence.lint_status`) | 11.6, 11.7 |
| `lab.py` | Runner: `kickoff day12 day40 champions three oakley status series architects` | all |
| `tryit.py` | Try It Yourself 1, 2, 3 | boxes |
| `test_ch11.py` | Six tests, including the failure injection | |

`fieldkit`: book layer unchanged at v1.4; the lab borrows the Chapter 13 cadence layer (`cadence.lint_status`, `cadence.bus_factor`, `cadence.GATES`). No new module.
