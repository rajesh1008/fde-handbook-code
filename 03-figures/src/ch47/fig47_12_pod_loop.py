"""Figure 47.12: the anatomy of a loop (Figure 25.13's drawing, loop_anatomy.draw) labeled with FK-N1 v1,
Northlight's own nightly fieldkit regeneration loop after the stop registry (Section 47.7).
Values are read from 04-code/ch47/output/pod_loops.json (the lab's deterministic stand-in)."""
import json
from _common import S, save, OUT
import loop_anatomy
d = json.load(open(OUT / "pod_loops.json"))
stop = d["spec"]["stop"]
fig, ax = S.figure(height=4.6)
loop_anatomy.draw(ax, dict(
    trigger="trigger\ncloud API changed",
    run="run\nregenerate adapter",
    verify="independent verification\nnl-platform-ci, 46 tests",
    stop=f"stop condition met?\n46 of 46, {stop['wall_clock_min']} min, by hash",
    state="persisted state\noutside the repository",
    human="intervention points\nthree named roles",
    cost=f"cost bound ${d['spec']['cost_bound_usd']:.2f} a night at the gateway key"))
save(fig, 12, kind="diagram", data="04-code/ch47/output/pod_loops.json (FK-N1 v1)")
