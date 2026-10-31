"""Chapter 15: what shipped at Caldwell in each of the seven weeks before the first real file arrived.

Each item is something a named Caldwell person reviewed, or a check that runs unattended. The log is
the engagement repository's week notes (Chapter 3), counted.
"""
import json, pathlib

WEEKS = [
    (1, "synthetic", ["engagement repository", "access tracker, six requests", "synthetic claim set (day 6)"], 2),
    (2, "synthetic", ["re-baselined plan (day 12)", "demo-claim audit", "gold-set plan, 300 documents"], 3),
    (3, "synthetic", ["sandbox account (day 19)", "deploy script in the sandbox", "pipeline skeleton end to end"], 1),
    (4, "synthetic", ["schema validators", "deterministic routing rules", "evaluation harness code"], 2),
    (5, "synthetic", ["gateway adapter (key day 33)", "key-rotation check, every seven days", "SSO request filed"], 2),
    (6, "synthetic", ["register fields reviewed", "failure-injection tests", "redaction rule tested on synthetic files"], 3),
    (7, "sampled", ["readiness report on 200 files", "storage decision (day 48)", "dated escalation (day 47)"], 3),
]
print(f"{'week':<6}{'days':<9}{'rung':<11}{'shipped':>8}{'reviewed':>10}  items")
for w, rung, items, reviewed in WEEKS:
    print(f"{w:<6}{f'{7*w-6}-{7*w}':<9}{rung:<11}{len(items):>8}{reviewed:>10}  " + "; ".join(items))
syn = [w for w in WEEKS if w[1] == "synthetic"]
print(f"weeks on the synthetic rung with a shipped item: {sum(1 for w in syn if w[2])} of {len(syn)}; "
      f"items reviewed by a named Caldwell person: {sum(w[3] for w in WEEKS)} of {sum(len(w[2]) for w in WEEKS)}")
(pathlib.Path(__file__).with_name("output") / "weekly_progress.json").write_text(
    json.dumps([dict(week=w, rung=r, shipped=len(i), reviewed=v) for w, r, i, v in WEEKS], indent=1))
