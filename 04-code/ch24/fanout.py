"""Listing 24.4: six sources per turn, called in sequence (the failure injection) and in parallel."""
import random, sys
import _paths  # noqa: F401
from fieldkit.surface import run_turn, percentile
from caldwell import SOURCES, BUDGET_P95_MS, TIMEOUT_MS

N = 500


def exchanges(rng):
    # 10% of source tokens are fresh exchanges (95 ms); the rest come from the broker's cache (4 ms)
    return {s.name: (95.0 if rng.random() < 0.10 else 4.0) for s in SOURCES}


def run(mode, timeout=None, seed=24):
    rng = random.Random(seed)
    return [run_turn(SOURCES, rng, mode=mode, exchange_ms=exchanges(rng), timeout_ms=timeout) for _ in range(N)]


def line(label, turns):
    tot = [t.total_ms for t in turns]; fan = [t.fanout_ms for t in turns]
    over = sum(1 for x in tot if x > BUDGET_P95_MS)
    return (f"{label:<26} fan-out p50 {percentile(fan,50):6.0f} p95 {percentile(fan,95):6.0f} | turn p50 "
            f"{percentile(tot,50):6.0f} p95 {percentile(tot,95):6.0f} ms | over 4 s {over:>3}/{N}")


if __name__ == "__main__":
    print(f"Caldwell adjuster turn, {N} turns, six sources (deterministic stand-in, seed 24)")
    rng = random.Random(7)
    print("per-source latency, ms (p50 / p95 over 2,000 samples):")
    for s in SOURCES:
        xs = [s.sample(rng) for _ in range(2000)]
        print(f"  {s.name:<14} {percentile(xs,50):6.0f} / {percentile(xs,95):6.0f}")
    seq, par, cut = run("sequential"), run("parallel"), run("parallel", TIMEOUT_MS)
    print(line("sequential (injected)", seq))
    print(line("parallel", par))
    print(line(f"parallel, timeout {TIMEOUT_MS}", cut))
    r = percentile([t.fanout_ms for t in seq], 50) / percentile([t.fanout_ms for t in par], 50)
    print(f"sequential / parallel fan-out at p50: {r:.1f}x")
    slow = {}
    for t in par:
        slow[t.slowest] = slow.get(t.slowest, 0) + 1
    print("slowest source in the parallel turns: " + ", ".join(f"{k} {v}" for k, v in sorted(slow.items(), key=lambda kv: -kv[1])))
    part = sum(1 for t in cut if t.partial)
    by = {}
    for t in cut:
        for p in t.partial:
            by[p] = by.get(p, 0) + 1
    print(f"turns with a marked partial answer at {TIMEOUT_MS} ms: {part} ({100*part/N:.1f}%): "
          + ", ".join(f"{k} {v}" for k, v in sorted(by.items(), key=lambda kv: -kv[1])))
    for label, ts in (("sequential", seq), ("parallel", par), ("timeout", cut)):
        xs = [t.total_ms for t in ts]
        print(f"cdf {label}: " + " ".join(f"{percentile(xs, p):.0f}" for p in range(0, 101, 5)))
    print("one turn (turn 1), start-end ms per source:")
    for label, ts in (("sequential", seq), ("parallel", par)):
        t = ts[0]
        print(f"  {label}: " + "; ".join(f"{k} {a:.0f}-{b:.0f}" for k, (a, b) in t.calls.items()) + f"; total {t.total_ms:.0f}")
