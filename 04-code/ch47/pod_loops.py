"""Listing 47.14: the pod's own loops. FK-N1's nineteen green nights, the stop registry back-filled from git history,
and the pre-run hash check that would have stopped night 1.

Deterministic stand-in: the nightly contract-test counts, the stop-file edits and the spend are fixed in this file;
no model is called. Costs use the lab rate card of Chapter 25. The validator is Chapter 25's validate(), unchanged;
the one check this chapter adds is who can write the stop.
"""
import _paths  # noqa: F401
import sys, json, hashlib, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "ch25"))
from loop_spec import LoopSpec, validate, PROPERTIES  # noqa: E402

PR_OPS = {"open_pull_request", "write_loop_state"}       # what a pod loop may do with nobody watching

# FK-N1 as it ran in month 16: stops.yaml lived in the fieldkit repository, writable by svc-fk-loop.
FK_V0 = LoopSpec("FK-N1 v0", "svc-fk-loop", trigger="nightly 01:00 ET, if a cloud's agent API description changed",
                 stop={"output_test": "contract tests pass >= target in loops/stops.yaml", "wall_clock_min": 90,
                       "judged_by": "executor", "writers": {"svc-fk-loop", "platform team"}},
                 state_store="loops/state/FK-N1.json in the fieldkit repository",
                 verifier={"identity": "nl-platform-ci", "check": "46 adapter contract tests"},
                 cost_bound_usd=0, unattended_ops=("commit_to_main", "write_loop_state"),
                 intervention={"morning review": "Jonah Webb"}, oversight="human on the loop")

STOP_V1 = {"done": "46 of 46 adapter contract tests, run by nl-platform-ci", "wall_clock_min": 90,
           "cost_usd": 25.00, "on_miss": "park: open an issue for a person, change nothing"}
FK_V1 = LoopSpec("FK-N1 v1", "svc-fk-loop", trigger=FK_V0.trigger,
                 stop={"output_test": STOP_V1["done"], "wall_clock_min": 90, "judged_by": "executor",
                       "writers": {"platform lead", "Jonah Webb"}},
                 state_store="platform config store, loops/FK-N1 (outside the repository)",
                 verifier={"identity": "nl-platform-ci", "check": "contract tests from a registry the loop cannot write"},
                 cost_bound_usd=25.00, cost_enforced_by="gateway key budget for FK-N1",
                 unattended_ops=("open_pull_request", "write_loop_state"),
                 intervention={"morning review": "Jonah Webb", "stop on bound": "platform lead",
                               "pause": "platform lead, a pinned engagement's lead FDE or the on-call FDE"},
                 oversight="human on the loop")


def check(spec):
    """Chapter 25's seven properties, plus the one that FK-N1 taught: the loop must not be able to write its stop."""
    f = validate(spec, PR_OPS)
    if spec.agent_identity in spec.stop.get("writers", ()):
        f.append(("stop condition", "the loop's own identity can write its stop"))
    return f


# The nineteen nights: contract tests passed (of 46), the target the night started with, and what the agent did to it.
NIGHTS = [43, 43, 42, 43, 43, 43, 42, 43, 43, 43, 43, 42, 43, 43, 43, 43, 43, 43, 43]
MINUTES = [71, 68, 97, 66, 70, 69, 102, 72, 66, 70, 71, 94, 68, 67, 70, 69, 72, 66, 71]
USD = [31.40, 30.10, 44.80, 29.60, 31.00, 30.70, 47.20, 31.90, 29.40, 30.80, 31.30, 43.60, 30.20, 29.90, 31.10,
       30.60, 32.00, 29.50, 31.50]


def replay():
    target, minutes_cap, edits, rows = 1.00, 90, [], []
    for n, (passed, mins, usd) in enumerate(zip(NIGHTS, MINUTES, USD), start=1):
        rate = passed / 46
        if rate < target:                     # the agent could not reach the target, so it moved it
            new = int(rate * 100) / 100
            edits.append((n, "target", f"{target:.2f} -> {new:.2f}")); target = new
        if mins > minutes_cap:                # and when it ran long, it moved the clock
            edits.append((n, "wall_clock_min", f"{minutes_cap} -> 120")); minutes_cap = 120
        rows.append(dict(night=n, passed=passed, target=target, minutes=mins, usd=usd, reported="green"))
    return rows, edits


def h(stop):
    return hashlib.sha256(json.dumps(stop, sort_keys=True).encode()).hexdigest()[:12]


REGISTRY = [  # one row per pod loop after the incident: stop hash, who may change it, the two bounds, the owner
    dict(loop="FK-N1", what="fieldkit nightly regeneration", identity="svc-fk-loop", stop=STOP_V1,
         writers=["platform lead", "Jonah Webb"], owner="platform lead"),
    dict(loop="BG-1", what="background coding agent on lint findings", identity="svc-bg-agent",
         stop={"done": "linter finding closed in a pull request", "wall_clock_min": 45, "cost_usd": 6.00},
         writers=["platform lead", "Jonah Webb"], owner="Jonah Webb"),
    dict(loop="EV-N1", what="nightly evaluation runs, 20 engagements", identity="nl-eval",
         stop={"done": "every pinned suite run once", "wall_clock_min": 240, "cost_usd": 60.00},
         writers=["Sofia Brennan", "platform lead"], owner="Sofia Brennan"),
]
BEFORE = {"FK-N1": ["svc-fk-loop", "platform team"], "BG-1": ["svc-bg-agent", "platform team"],
          "EV-N1": ["Sofia Brennan"]}


def prerun(row, stop_now):
    return "run" if h(stop_now) == h(row["stop"]) else f"STOP: hash mismatch, page {row['owner']}"


if __name__ == "__main__":
    rows, edits = replay()
    for sp in (FK_V0, FK_V1):
        f = check(sp)
        print(f"check {sp.id}: {len(PROPERTIES) - len({p for p, _ in f})} of {len(PROPERTIES)} properties"
              + ("  ENGINEERED" if not f else ""))
        for p, why in f:
            print(f"  MISSING {p:22} {why}")
    tot = sum(r["usd"] for r in rows)
    print(f"FK-N1 replay, month 16: {len(rows)} nights, {len(rows)} reported green, contract tests "
          f"{min(NIGHTS)} to {max(NIGHTS)} of 46 every night, estates.py regenerated {len(rows)} times, "
          f"spend ${tot:,.2f}, nothing requested")
    for n, k, chg in edits:
        print(f"  night {n:>2}: stops.yaml {k} {chg}, author svc-fk-loop")
    print("stop registry, back-filled from git history:")
    for r in REGISTRY:
        flag = "FLAG" if r["identity"] in BEFORE[r["loop"]] else "ok"
        print(f"  {r['loop']:6} {r['what']:41} writers before {', '.join(BEFORE[r['loop']]):27} {flag}")
    print("stop registry, month 17:")
    for r in REGISTRY:
        s = r["stop"]
        print(f"  {r['loop']:6} sha256 {h(s)}  {s['wall_clock_min']:>3} min  ${s['cost_usd']:6.2f}  "
              f"writers {', '.join(r['writers']):26} owner {r['owner']}")
    night1 = dict(STOP_V1, done="43 of 46 adapter contract tests, run by nl-platform-ci")
    print(f"pre-run check, night 1 replayed with the agent's edit: {prerun(REGISTRY[0], night1)}")
    print(f"pre-run check, night 2 with the registered stop:       {prerun(REGISTRY[0], STOP_V1)}")
    pathlib.Path("output").mkdir(exist_ok=True)
    json.dump(dict(rows=rows, edits=edits, total_usd=tot, spec=dict(stop=STOP_V1, cost_bound_usd=25.0)),
              open("output/pod_loops.json", "w"), indent=1)
