"""Listing 24.5: three ways to carry the adjuster across the boundary, 600 turns, 3,000 results (stand-in)."""
import random
import _paths  # noqa: F401
from fieldkit.surface import Token, TokenBroker, AudienceMismatch
from caldwell import SOURCES

rng = random.Random(24)
USERS = [f"adj{i:02d}" for i in range(1, 15)]
CLAIMS = []
for i in range(2000):
    r = rng.random()
    restr = "siu" if r < 0.025 else ("legal hold" if r < 0.038 else None)
    CLAIMS.append(dict(id=f"CL-{i:05d}", restr=restr, assigned=rng.choice(USERS)))


def readable(user, c):
    return c["restr"] is None or c["assigned"] == user


TURNS = sorted((rng.uniform(0, 8 * 3600), rng.choice(USERS), [rng.choice(CLAIMS) for _ in range(5)]) for _ in range(600))

# 1. the surface forwards its own sign-in token (audience: the suite) to the brain
b1 = TokenBroker(); refused = 0
for t, u, _ in TURNS:
    try:
        b1.accept(Token(u, "https://suite.example/graph", 0, 9e9), t)
    except AudienceMismatch:
        refused += 1
print(f"1 forwarded suite token:   {refused}/600 turns refused at the brain (audience mismatch)")

# 2. the shortcut: the brain queries every source as its own service role
shown = sum(1 for _, u, rs in TURNS for c in rs if not readable(u, c))
kinds = {}
for _, u, rs in TURNS:
    for c in rs:
        if not readable(u, c):
            kinds[c["restr"]] = kinds.get(c["restr"], 0) + 1
print(f"2 service role nl-brain-svc: {shown} of 3,000 results the adjuster may not read ("
      + ", ".join(f"{k} {v}" for k, v in sorted(kinds.items())) + ")")

# 3. on-behalf-of: one assertion for the brain, exchanged per source; the source filters by the user
b3 = TokenBroker(); added = []; leak = 0
for t, u, rs in TURNS:
    a = Token(u, "api://nl-brain", t - 60, t + 3540)
    ms = [b3.exchange(a, s.audience, t)[1] for s in SOURCES]
    added.append(max(ms))                       # exchanges run in parallel with the fan-out
    returned = [c for c in rs if readable(u, c)]   # each source filters with the user's own token
    leak += sum(1 for c in returned if not readable(u, c))
filtered = 3000 - sum(1 for _, u, rs in TURNS for c in rs if readable(u, c))
print(f"3 on-behalf-of + recheck:   {leak} results the adjuster may not read; {filtered} withheld by the sources")
st = b3.stats
print(f"   exchanges {st['exchanged']}, cache hits {st['cache_hit']} ({100*st['cache_hit']/(st['exchanged']+st['cache_hit']):.1f}%), "
      f"added latency per turn mean {sum(added)/len(added):.0f} ms, max {max(added):.0f} ms")
