"""Try It Yourself, Chapter 24. a: score your own options; b: add a seventh source; c: change the token lifetime."""
import random, sys
import _paths  # noqa: F401
from fieldkit.surface import Option, rank, flip_point, weight_draws, Source, run_turn, percentile, Token, TokenBroker
from caldwell import DIMS, WEIGHTS, OPTIONS, SOURCES

which = sys.argv[1] if len(sys.argv) > 1 else "a"
if which == "a":
    # a team whose users live in a line-of-business tool, not the suite: adoption favours a new application
    opts = [Option(o.key, o.name, dict(o.scores, adoption=a)) for o, a in zip(OPTIONS, [4, 2, 3, 3])]
    for wa in (16, 8, 24):
        w = dict(WEIGHTS, adoption=wa)
        r = rank(opts, w); wins = weight_draws(opts, w, n=1000, seed=1)
        print(f"adoption weight {wa:>2}: " + "  ".join(f"{k} {t:.1f}" for k, t in r) + f"  | draws won by {r[0][0]}: {wins[r[0][0]]/10:.1f}%")
elif which == "b":
    extra = Source("vendor-network", 1800, 0.45, "api://caldwell-vendors")
    srcs = SOURCES + [extra]
    for label, to in (("no timeout", None), ("timeout 2500", 2500), ("timeout 2000", 2000)):
        rng = random.Random(24)
        ts = [run_turn(srcs, rng, "parallel", timeout_ms=to) for _ in range(500)]
        part = sum(1 for t in ts if t.partial)
        print(f"7 sources, {label:<13} turn p95 {percentile([t.total_ms for t in ts],95):5.0f} ms, partial {part:>3}/500")
else:
    for ttl in (300, 900, 3600):
        b = TokenBroker(ttl_s=ttl); rng = random.Random(24)
        for t in sorted(rng.uniform(0, 8 * 3600) for _ in range(600)):
            u = f"adj{rng.randint(1, 14):02d}"
            a = Token(u, "api://nl-brain", t - 60, t + 3540)
            for s in SOURCES:
                b.exchange(a, s.audience, t)
        st = b.stats
        print(f"token lifetime {ttl:>4} s: exchanges {st['exchanged']:>4}, cache hits {st['cache_hit']:>4} "
              f"({100*st['cache_hit']/3600:.1f}%), worst-case revocation lag {ttl/60:.0f} min")
