"""Run linter v0 and v1 over the fifteen story snapshots and the injected case (Greystone's kickoff map)."""
import _paths  # noqa: F401
from linter import RULES
from world import STORIES, INJECTED
from catalog import BY_RULE


def rule_of(m, gated):
    return RULES[int(m["rule"][1:]) - 1](m, gated)


def main():
    caught = {False: 0, True: 0}
    print(f"{'case':4} {'rule':4} {'engagement':24} {'v0':5} {'v1':5} anti-pattern")
    for m in STORIES + [INJECTED]:
        s0, _ = rule_of(m, False)
        s1, d1 = rule_of(m, True)
        if m is not INJECTED:
            caught[False] += s0 == "FLAG"; caught[True] += s1 == "FLAG"
        print(f"{m['id']:4} {m['rule']:4} {m['who']:24} {s0:5} {s1:5} {BY_RULE[m['rule']].anti} ({m['when']})")
        print(f"{'':10}v1: {d1}")
    print(f"\nstories flagged: v0 {caught[False]} of {len(STORIES)}, v1 {caught[True]} of {len(STORIES)}")
    s0, d0 = rule_of(INJECTED, False)
    s1, d1 = rule_of(INJECTED, True)
    print(f"injected Greystone day-2 map: v0 {s0} ({d0}); v1 {s1} ({d1})")


if __name__ == "__main__":
    main()
